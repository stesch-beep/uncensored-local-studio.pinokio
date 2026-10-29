"""Frame renderer and the parallel chunked encode."""

from __future__ import annotations

import bisect
import json
import multiprocessing as mp
import os
import queue
import subprocess
import threading
import time
from collections import OrderedDict
from pathlib import Path

import cv2
import numpy as np

from . import ffmpeg_tools as ff
from .audio import Analysis, TimelineEntry
from .config import Project, load_project
from .montage import Clip, Segment, load_edl
from .speakers import SpeakerOverlay
from .titles import TitleOverlay


def _grade(sat=1.0, hue_deg=0.0, temp=0.0, contrast=1.0, lift=0.0):
    """3x4 BGR colour matrix: saturation, hue rotation, temperature, contrast."""
    lum = np.array([0.114, 0.587, 0.299])  # B, G, R weights
    s = np.outer(np.ones(3), lum) * (1 - sat) + np.eye(3) * sat
    a = np.radians(hue_deg)
    k = np.ones((3, 3)) / 3.0
    rot = np.cos(a) * np.eye(3) + (1 - np.cos(a)) * k + np.sin(a) * np.sqrt(1 / 3.0) * np.array(
        [[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    t = np.diag([1 - temp, 1.0, 1 + temp])  # B, G, R
    m = contrast * (t @ rot @ s)
    offset = 128 * (1 - contrast) + lift
    return np.hstack([m, np.full((3, 1), offset)])


GRADES = [
    _grade(),                                                     # neutral
    _grade(sat=1.15, hue_deg=-12, temp=-0.10, contrast=1.08),      # icy cyan
    _grade(sat=1.20, hue_deg=18, temp=0.02, contrast=1.06),        # magenta club
    _grade(sat=1.05, temp=0.12, contrast=1.10, lift=-4),           # warm amber
    _grade(sat=0.75, temp=-0.16, contrast=1.18, lift=-6),          # cold steel
    _grade(sat=1.30, hue_deg=-25, contrast=1.12, lift=-3),         # deep blue/red
]


class ClipCache:
    def __init__(self, capacity: int):
        self.capacity = max(1, capacity)
        self.items: OrderedDict[str, np.ndarray] = OrderedDict()

    def get(self, clip: Clip) -> np.ndarray:
        if clip.path in self.items:
            self.items.move_to_end(clip.path)
            return self.items[clip.path]
        proc = subprocess.run(
            [ff.ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", clip.path, "-an",
             "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            raise ff.FFmpegError(f"Clip nicht lesbar: {clip.path}\n{proc.stderr.decode('utf-8', 'replace')[-400:]}")
        n = len(proc.stdout) // (clip.width * clip.height * 3)
        frames = np.frombuffer(proc.stdout, np.uint8)[: n * clip.width * clip.height * 3]
        frames = frames.reshape(n, clip.height, clip.width, 3)
        self.items[clip.path] = frames
        while len(self.items) > self.capacity:
            self.items.popitem(last=False)
        return frames


class FrameRenderer:
    def __init__(self, project: Project, analysis: Analysis, clips: list[Clip],
                 segments: list[Segment], timeline: list[TimelineEntry]):
        v = project["video"]
        self.W, self.H, self.fps = int(v["width"]), int(v["height"]), float(v["fps"])
        self.m = project["montage"]
        self.a = analysis
        self.clips, self.segments = clips, segments
        self.starts = [s.t0 for s in segments]
        self.cache = ClipCache(int(v["clip_cache"]))
        self.speakers = SpeakerOverlay(project, self.W, self.H)
        self.titles = TitleOverlay(project, timeline, self.W, self.H, self.speakers.side_reserved(self.W))
        rng = np.random.default_rng(project["seed"])
        vig = float(self.m["vignette"])
        self.vignette = None
        if vig > 0:
            yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
            d = np.sqrt(((xx - self.W / 2) / (self.W / 2)) ** 2 + ((yy - self.H / 2) / (self.H / 2)) ** 2) / np.sqrt(2)
            mask = 1.0 - vig * np.clip(d - 0.35, 0, None) ** 1.6 / (0.65 ** 1.6)
            self.vignette = cv2.merge([(mask * 255).astype(np.uint8)] * 3)
        g = float(self.m["grain"])
        self.grain = []
        if g > 0:
            for _ in range(6):
                n = rng.normal(0, 7.0 * g, (self.H // 2, self.W // 2)).astype(np.float32)
                n = cv2.resize(n, (self.W, self.H), interpolation=cv2.INTER_LINEAR)
                pos = cv2.merge([np.clip(n, 0, 255).astype(np.uint8)] * 3)
                neg = cv2.merge([np.clip(-n, 0, 255).astype(np.uint8)] * 3)
                self.grain.append((pos, neg))

    def _source(self, seg: Segment, t: float, f: int) -> np.ndarray:
        clip = self.clips[seg.clip]
        frames = self.cache.get(clip)
        n = len(frames)
        pos = seg.src_start + seg.rate * (t - seg.t0)
        if seg.wrap == "loop":
            period = max(1, n - 1)  # last frame == first frame of a closed loop
            idx = int(np.floor(pos)) % period
        elif seg.wrap == "pingpong":
            period = max(1, 2 * (n - 1))
            m = int(np.floor(pos)) % period
            idx = m if m < n else period - m
        else:
            idx = int(np.clip(np.floor(pos), 0, n - 1))
        src = frames[idx]
        # Geometry: cover-fit, slow zoom/pan drift, bass pump, optional mirror.
        u = np.clip((t - seg.t0) / max(1e-3, seg.t1 - seg.t0), 0, 1)
        zoom = seg.zoom0 + (seg.zoom1 - seg.zoom0) * u
        zoom *= 1.0 + float(self.m["bass_zoom"]) * float(self.a.kick[f])
        h, w = src.shape[:2]
        S = max(self.W / w, self.H / h) * zoom
        px = seg.pan0[0] + (seg.pan1[0] - seg.pan0[0]) * u
        py = seg.pan0[1] + (seg.pan1[1] - seg.pan0[1]) * u
        slack_x = max(0.0, w - self.W / S)
        slack_y = max(0.0, h - self.H / S)
        cx = w / 2 + px * slack_x / 2
        cy = h / 2 + py * slack_y / 2
        sx = -S if seg.mirror else S
        M = np.array([[sx, 0, self.W / 2 - sx * cx], [0, S, self.H / 2 - S * cy]], np.float32)
        out = cv2.warpAffine(src, M, (self.W, self.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        grade = GRADES[seg.grade % len(GRADES)].copy()
        pump = 1.0 + float(self.m["light_pump"]) * float(self.a.kick[f])
        grade[:, :3] *= pump
        return cv2.transform(out, grade.astype(np.float32))

    def render(self, f: int) -> np.ndarray:
        t = f / self.fps
        si = max(0, bisect.bisect_right(self.starts, t) - 1)
        seg = self.segments[si]
        frame = self._source(seg, t, f)
        k = int(round((t - seg.t0) * self.fps))
        if si > 0 and seg.transition == "fade" and k < int(self.m["fade_frames"]):
            prev = self._source(self.segments[si - 1], t, f)
            a = (k + 1) / (int(self.m["fade_frames"]) + 1)
            frame = cv2.addWeighted(frame, a, prev, 1 - a, 0)
        elif seg.transition == "flash" and k < 6:
            a = 0.85 * np.exp(-k / 1.6)
            frame = cv2.convertScaleAbs(frame, alpha=1 - a, beta=255 * a)
        if self.vignette is not None:
            frame = cv2.multiply(frame, self.vignette, scale=1 / 255.0)
        if self.grain:
            pos, neg = self.grain[f % len(self.grain)]
            frame = cv2.subtract(cv2.add(frame, pos), neg)
        if self.speakers.enabled:
            self.speakers.draw(frame, float(self.a.cone[f]), float(self.a.tweeter[f]), float(self.a.kick[f]))
        self.titles.draw(frame, t)
        return frame


# ── workers ──────────────────────────────────────────────────────────────────

_progress = None


def _init_worker(progress):
    global _progress
    _progress = progress
    cv2.setNumThreads(2)


def _load_state(config_path: str, state_dir: str):
    project = load_project(config_path)
    state = Path(state_dir)
    analysis = Analysis.load(state / "analysis.npz")
    clips, segments = load_edl(state / "edl.json")
    timeline = [TimelineEntry(**e) for e in json.loads((state / "timeline.json").read_text(encoding="utf-8"))]
    return project, analysis, clips, segments, timeline


def render_chunk(job: dict) -> str:
    project, analysis, clips, segments, timeline = _load_state(job["config"], job["state"])
    renderer = FrameRenderer(project, analysis, clips, segments, timeline)
    v = project["video"]
    out = Path(job["out"])
    log = open(out.with_suffix(".log"), "wb")
    args = [ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "warning",
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{renderer.W}x{renderer.H}", "-r", str(v["fps"]),
            "-i", "-", *ff.encoder_args(job["encoder"], int(v["quality"]), int(v["fps"])),
            "-an", "-video_track_timescale", "90000", str(out)]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
    q: queue.Queue = queue.Queue(maxsize=6)
    error: list[BaseException] = []

    def writer():
        try:
            while True:
                item = q.get()
                if item is None:
                    break
                proc.stdin.write(item)
        except BaseException as exc:  # broken pipe -> ffmpeg died, reported below
            error.append(exc)

    th = threading.Thread(target=writer, daemon=True)
    th.start()
    try:
        for n, f in enumerate(range(job["f0"], job["f1"])):
            frame = renderer.render(f)
            q.put(np.ascontiguousarray(frame).tobytes())
            if _progress is not None and n % 12 == 0:
                _progress[job["index"]] = n
            if error:
                break
    finally:
        q.put(None)
        th.join()
        try:
            proc.stdin.close()
        except OSError:
            pass
        proc.wait()
        log.close()
    if proc.returncode != 0 or error:
        tail = out.with_suffix(".log").read_text(encoding="utf-8", errors="replace")[-1500:]
        raise ff.FFmpegError(f"Encoder-Fehler in Teil {job['index']}:\n{tail}")
    if _progress is not None:
        _progress[job["index"]] = job["f1"] - job["f0"]
    return str(out)


def _split(segments: list[Segment], fps: float, f0: int, f1: int, parts: int) -> list[tuple[int, int]]:
    """Chunk boundaries on segment cuts (so every chunk starts at a fresh shot)."""
    cuts = sorted({int(round(s.t0 * fps)) for s in segments if f0 < round(s.t0 * fps) < f1})
    bounds = [f0]
    for k in range(1, parts):
        target = f0 + (f1 - f0) * k / parts
        if cuts:
            best = min(cuts, key=lambda c: abs(c - target))
            if best > bounds[-1] + fps:
                bounds.append(best)
    bounds.append(f1)
    return list(zip(bounds[:-1], bounds[1:]))


def render_video(project: Project, config_path: str, state_dir: Path, mix_path: Path,
                 out_path: Path, f0: int, f1: int, workers: int) -> Path:
    v = project["video"]
    fps = float(v["fps"])
    encoder = ff.pick_encoder(v.get("codec", "h264"), v.get("encoder", "auto"))
    _, segments = load_edl(state_dir / "edl.json")
    chunks = _split(segments, fps, f0, f1, max(1, workers) * (2 if workers > 1 else 1))
    chunk_dir = state_dir / "chunks"
    chunk_dir.mkdir(exist_ok=True)
    for old in chunk_dir.glob("teil_*"):
        old.unlink()
    jobs = [{
        "config": config_path, "state": str(state_dir), "index": i, "f0": a, "f1": b,
        "encoder": encoder, "out": str(chunk_dir / f"teil_{i:03d}.mp4"),
    } for i, (a, b) in enumerate(chunks)]
    total = f1 - f0
    print(f"Rendere {total} Frames ({total / fps / 60:.1f} min) in {len(jobs)} Teilen mit {workers} Prozess(en), "
          f"Encoder {encoder} …")
    started = time.time()
    ctx = mp.get_context("spawn")
    progress = ctx.Array("i", len(jobs), lock=False)
    with ctx.Pool(processes=max(1, workers), initializer=_init_worker, initargs=(progress,)) as pool:
        result = pool.map_async(render_chunk, jobs, chunksize=1)
        while not result.ready():
            result.wait(2.0)
            done = sum(progress)
            el = time.time() - started
            speed = done / el if el > 0 else 0
            eta = (total - done) / speed if speed > 0 else 0
            print(f"\r  {100 * done / total:5.1f}%  {speed:5.1f} fps  noch ~{eta / 60:4.1f} min   ", end="", flush=True)
        parts = result.get()
    print(f"\r  100.0%  fertig in {(time.time() - started) / 60:.1f} min" + " " * 30)

    list_file = chunk_dir / "liste.txt"
    quote = lambda p: Path(p).as_posix().replace("'", "'\\''")
    list_file.write_text("".join(f"file '{quote(p)}'\n" for p in parts), encoding="utf-8")
    acfg = project["audio"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Füge Video und Audio zusammen → {out_path}")
    ff.run([
        ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-ss", f"{f0 / fps:.3f}", "-t", f"{(f1 - f0) / fps:.3f}", "-i", str(mix_path),
        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-c:a", "aac", "-b:a", str(acfg["bitrate"]), "-ar", str(acfg["sample_rate"]),
        "-shortest", "-movflags", "+faststart", str(out_path),
    ])
    for p in parts:
        Path(p).unlink(missing_ok=True)
        Path(p).with_suffix(".log").unlink(missing_ok=True)
    return out_path


def default_workers(project: Project) -> int:
    w = int(project["video"].get("workers") or 0)
    if w > 0:
        return w
    return max(1, min(4, (os.cpu_count() or 2) // 2))
