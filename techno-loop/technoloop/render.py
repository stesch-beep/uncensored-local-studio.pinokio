"""Frame renderer and the parallel chunked encode."""

from __future__ import annotations

import bisect
import hashlib
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

    def render_overlay(self, f: int) -> np.ndarray:
        """Only speakers + titles on a transparent BGRA frame (DaVinci Resolve export)."""
        frame = np.zeros((self.H, self.W, 4), np.uint8)
        if self.speakers.enabled:
            self.speakers.draw(frame, float(self.a.cone[f]), float(self.a.tweeter[f]), float(self.a.kick[f]))
        self.titles.draw(frame, f / self.fps)
        return frame

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
    final = Path(job["out"])
    out = final.with_name(final.stem + ".tmp" + final.suffix)
    log = open(final.with_suffix(".log"), "wb")
    overlay = job.get("kind") == "overlay"
    codec = OVERLAY_CODECS[job["encoder"]][0] if overlay else \
        ff.encoder_args(job["encoder"], int(v["quality"]), int(v["fps"]))
    args = [ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "warning",
            "-f", "rawvideo", "-pix_fmt", "bgra" if overlay else "bgr24",
            "-s", f"{renderer.W}x{renderer.H}", "-r", str(v["fps"]),
            "-i", "-", *codec, "-an", "-video_track_timescale", "90000", str(out)]
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
            frame = renderer.render_overlay(f) if overlay else renderer.render(f)
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
        tail = final.with_suffix(".log").read_text(encoding="utf-8", errors="replace")[-1500:]
        out.unlink(missing_ok=True)
        raise ff.FFmpegError(f"Encoder-Fehler in Teil {job['index']}:\n{tail}")
    out.replace(final)
    final.with_suffix(".log").unlink(missing_ok=True)
    if _progress is not None:
        _progress[job["index"]] = job["f1"] - job["f0"]
    return str(final)


CHUNK_VERSION = 1

# Overlay with alpha for DaVinci Resolve: (ffmpeg args, file extension)
OVERLAY_CODECS = {
    "png": (["-c:v", "png", "-pred", "mixed", "-pix_fmt", "rgba"], ".mov"),        # ~20 GB/h @1080p, sicher
    "qtrle": (["-c:v", "qtrle", "-pix_fmt", "argb"], ".mov"),                     # QuickTime Animation
    "prores4444": (["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"], ".mov"),
    "vp9": (["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "28", "-row-mt", "1",
             "-deadline", "good", "-cpu-used", "4"], ".webm"),                     # winzig, Resolve-Version abhängig
}


def _chunk_grid(segments: list[Segment], fps: float, f0: int, f1: int, chunk_s: float) -> list[tuple[int, int]]:
    """Chunks of about `chunk_s` seconds, each starting on a cut.

    Boundaries are taken from a fixed time grid (first cut after every multiple
    of chunk_s), so they stay the same when songs are appended -> cache hits.
    """
    cuts = sorted({int(round(s.t0 * fps)) for s in segments if f0 < round(s.t0 * fps) < f1})
    step = max(1.0, chunk_s) * fps
    bounds = [f0]
    k = int(f0 // step) + 1
    while True:
        i = bisect.bisect_left(cuts, k * step)
        if i >= len(cuts) or cuts[i] >= f1 - fps:
            break
        if cuts[i] > bounds[-1]:
            bounds.append(cuts[i])
        while k * step <= cuts[i]:
            k += 1
    bounds.append(f1)
    return list(zip(bounds[:-1], bounds[1:]))


def _file_id(path: str) -> list:
    try:
        st = os.stat(path)
        return [path, st.st_size, st.st_mtime_ns]
    except OSError:
        return [path, 0, 0]


def _chunk_key(project: Project, encoder: str, clips: list[Clip], segments: list[Segment],
               analysis: Analysis, timeline: list[TimelineEntry], a: int, b: int) -> str:
    """Everything that influences the pixels of frames [a, b)."""
    from . import __version__
    from dataclasses import asdict

    fps = analysis.fps
    t0, t1 = a / fps - 1.0, b / fps
    h = hashlib.sha1()
    cfg = {k: project[k] for k in ("video", "montage", "speakers", "titles", "seed")}
    cfg["video"] = {k: v for k, v in cfg["video"].items() if k not in ("workers", "clip_cache", "chunk_seconds")}
    cfg["crossfade"] = project["audio"]["crossfade_seconds"]
    extra = [_file_id(str(project.path(project["speakers"].get("image"))))] if project["speakers"].get("image") else []
    h.update(json.dumps([CHUNK_VERSION, __version__, encoder, cfg, extra, a, b], sort_keys=True, default=str).encode())
    for seg in segments:
        if seg.t1 > t0 and seg.t0 < t1:
            d = asdict(seg)
            clip = clips[seg.clip]
            d["clip"] = _file_id(clip.path) + [clip.frames, clip.loop]
            h.update(json.dumps(d, sort_keys=True).encode())
    for arr in (analysis.cone, analysis.tweeter, analysis.kick):
        h.update(np.ascontiguousarray(arr[a:b]).tobytes())
    show_total = project["titles"].get("show_total", False)
    for e in timeline:
        if e.end > t0 - 15 and e.start < t1 + 15:
            h.update(json.dumps([e.number, e.title, e.artist, round(e.start, 4), round(e.end, 4),
                                 e.count if show_total else 0]).encode())
    return h.hexdigest()[:20]


def render_video(project: Project, config_path: str, state_dir: Path, mix_path: Path | None,
                 out_path: Path, f0: int, f1: int, workers: int, *, use_cache: bool = True,
                 kind: str = "final") -> Path:
    """Render frames [f0, f1) and mux the audio.

    Full builds keep every rendered chunk in arbeitsordner/render/teile; a later
    build only renders chunks whose content changed (e.g. after appending songs).
    kind="overlay" renders only speakers + titles with alpha (PNG in MOV, no audio).
    """
    v = project["video"]
    fps = float(v["fps"])
    overlay = kind == "overlay"
    if overlay:
        encoder = str(project.get("resolve", {}).get("overlay_codec", "png"))
        if encoder not in OVERLAY_CODECS:
            raise ValueError(f"resolve.overlay_codec muss eins von {', '.join(OVERLAY_CODECS)} sein.")
    else:
        encoder = ff.pick_encoder(v.get("codec", "h264"), v.get("encoder", "auto"))
    _, analysis, clips, segments, timeline = _load_state(config_path, str(state_dir))
    chunks = _chunk_grid(segments, fps, f0, f1, float(v.get("chunk_seconds") or 120))
    part_dir = state_dir / ("teile" if use_cache else ("overlay_teile" if overlay else "vorschau_teile"))
    part_dir.mkdir(exist_ok=True)
    if not use_cache:
        for old in part_dir.glob("*"):
            old.unlink()
    jobs, parts = [], []
    for i, (a, b) in enumerate(chunks):
        key = _chunk_key(project, encoder, clips, segments, analysis, timeline, a, b)
        out = part_dir / f"{a:08d}_{key}{OVERLAY_CODECS[encoder][1] if overlay else '.mp4'}"
        parts.append(str(out))
        if not out.is_file():
            jobs.append({"config": config_path, "state": str(state_dir), "index": len(jobs), "kind": kind,
                         "f0": a, "f1": b, "encoder": encoder, "out": str(out)})
    reused = len(chunks) - len(jobs)
    total = sum(j["f1"] - j["f0"] for j in jobs)
    if reused:
        print(f"{reused} von {len(chunks)} Teilen sind schon fertig und werden wiederverwendet.")
    if jobs:
        print(f"Rendere {total} Frames ({total / fps / 60:.1f} min) in {len(jobs)} Teilen mit "
              f"{min(workers, len(jobs))} Prozess(en), Encoder {encoder} …")
        started = time.time()
        ctx = mp.get_context("spawn")
        progress = ctx.Array("i", len(jobs), lock=False)
        with ctx.Pool(processes=max(1, min(workers, len(jobs))), initializer=_init_worker,
                      initargs=(progress,)) as pool:
            result = pool.map_async(render_chunk, jobs, chunksize=1)
            while not result.ready():
                result.wait(2.0)
                done = sum(progress)
                el = time.time() - started
                speed = done / el if el > 0 else 0
                eta = (total - done) / speed if speed > 0 else 0
                print(f"\r  {100 * done / total:5.1f}%  {speed:5.1f} fps  noch ~{eta / 60:4.1f} min   ",
                      end="", flush=True)
            result.get()
        print(f"\r  100.0%  fertig in {(time.time() - started) / 60:.1f} min" + " " * 30)

    list_file = part_dir / "liste.txt"
    quote = lambda p: Path(p).as_posix().replace("'", "'\\''")
    list_file.write_text("".join(f"file '{quote(p)}'\n" for p in parts), encoding="utf-8")
    acfg = project["audio"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Füge {'Overlay' if overlay else 'Video und Audio'} zusammen → {out_path}")
    if overlay:
        ff.run([ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", str(list_file), "-c:v", "copy", str(out_path)])
    else:
        ff.run([
            ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-ss", f"{f0 / fps:.3f}", "-t", f"{(f1 - f0) / fps:.3f}", "-i", str(mix_path),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            "-c:a", "aac", "-b:a", str(acfg["bitrate"]), "-ar", str(acfg["sample_rate"]),
            "-shortest", "-movflags", "+faststart", str(out_path),
        ])
    keep = {Path(p).name for p in parts}
    for old in [q for q in part_dir.glob("*") if q.suffix in (".mp4", ".mov", ".webm")]:
        if old.name not in keep or not use_cache:
            old.unlink(missing_ok=True)
    return out_path


def default_workers(project: Project) -> int:
    w = int(project["video"].get("workers") or 0)
    if w > 0:
        return w
    return max(1, min(4, (os.cpu_count() or 2) // 2))
