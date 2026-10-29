"""Clip pool and the beat-synchronous edit plan (EDL).

A handful of short clips becomes an hour of footage that does not read as a
loop: every cut lands on a beat (shorter cuts on drops, longer in breakdowns),
no clip or scene repeats back-to-back, and each use gets its own in-point,
speed, direction, mirror, zoom/pan drift and colour look.
"""

from __future__ import annotations

import bisect
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from . import ffmpeg_tools as ff
from .audio import Analysis, TimelineEntry
from .config import VIDEO_EXTENSIONS, ConfigError, Project

N_GRADES = 6  # see render.GRADES


@dataclass
class Clip:
    path: str
    scene: str
    frames: int
    fps: float
    width: int
    height: int
    loop: bool
    tags: list
    weight: float = 1.0
    reverse_ok: bool = True
    mirror_ok: bool = True


@dataclass
class Segment:
    t0: float
    t1: float
    clip: int
    src_start: float   # source frame at t0
    rate: float        # source frames per output second (negative = reverse)
    wrap: str          # loop | clamp | pingpong
    mirror: bool
    zoom0: float
    zoom1: float
    pan0: tuple
    pan1: tuple
    grade: int
    transition: str    # cut | flash | fade


def collect_clips(project: Project) -> list[Clip]:
    scene_cfg = {s["id"]: s for s in project["scenes"]}
    sources: list[tuple[Path, dict]] = []
    if project.scenes_dir.is_dir():
        for path in sorted(project.scenes_dir.iterdir()):
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                meta_file = path.with_suffix(".json")
                meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.is_file() else {}
                meta.setdefault("scene", path.stem.split("__")[0])
                sources.append((path, meta))
    extra = project.path(project.get("clips_folder"))
    if extra and extra.is_dir():
        for path in sorted(extra.rglob("*")):
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                stem = path.stem.lower()
                sources.append((path, {"scene": path.stem.split("__")[0], "loop": "loop" in stem}))
    clips = []
    for path, meta in sources:
        scfg = scene_cfg.get(meta["scene"], {})
        if scfg.get("skip"):
            continue
        info = ff.probe(path)
        if not info.get("width"):
            print(f"  übersprungen (kein Video lesbar): {path.name}")
            continue
        fps = float(info.get("fps") or 24.0)
        frames = int(info.get("frames") or round(float(info.get("duration") or 0) * fps))
        if frames < 8:
            continue
        clips.append(Clip(
            path=str(path), scene=meta["scene"], frames=frames, fps=fps,
            width=int(info["width"]), height=int(info["height"]),
            loop=bool(meta.get("loop", False)),
            tags=list(scfg.get("tags") or meta.get("tags") or []),
            weight=float(scfg.get("weight", 1.0)),
            reverse_ok=bool(scfg.get("reverse_ok", "girls" not in (scfg.get("tags") or meta.get("tags") or []))),
            mirror_ok=bool(scfg.get("mirror_ok", True)),
        ))
    if not clips:
        raise ConfigError(
            f"Keine Clips gefunden. Erst 'Szenen rendern' ausführen (Ordner {project.scenes_dir}) "
            "oder fertige MP4s in clips_folder legen."
        )
    return clips


def song_switch_times(timeline: list[TimelineEntry]) -> list[float]:
    """When the on-screen title changes: middle of each crossfade."""
    times = [0.0]
    for prev, cur in zip(timeline, timeline[1:]):
        times.append(0.5 * (cur.start + prev.end))
    return times


def plan_edl(project: Project, clips: list[Clip], analysis: Analysis,
             timeline: list[TimelineEntry], prefix: list[Segment] | None = None) -> list[Segment]:
    """Plan the cuts. `prefix` = segments kept from the previous build (see reusable_prefix)."""
    m = project["montage"]
    prefix = list(prefix or [])
    start_t = prefix[-1].t1 if prefix else 0.0
    rng = random.Random(project["seed"] * 7919 + 17 + (int(round(start_t * 1000)) if prefix else 0))
    total = analysis.n_frames / analysis.fps
    beats = analysis.beats
    if len(beats) < 4:  # no usable rhythm (silence, spoken word…) -> 120 BPM grid
        beats = np.arange(0.0, total, 0.5)
        bars = np.arange(len(beats)) % 4 == 0
        levels = np.ones(len(beats), dtype=np.float32)
    else:
        bars, levels = analysis.beat_bar, analysis.beat_level
    beats = list(beats)
    switches = song_switch_times(timeline)[1:]
    min_len = float(m["min_segment_seconds"])
    avoid = int(m["avoid_repeat"])
    last_used = {i: -1e9 for i in range(len(clips))}
    history: list[int] = [s.clip for s in prefix]
    for s in prefix:
        last_used[s.clip] = s.t0
    segments: list[Segment] = prefix

    t = start_t
    bi = bisect.bisect_left(beats, t + 1e-3)
    # A kept prefix ends either anywhere or exactly on the first beat after a song change.
    pending_flash = bool(prefix) and any(prefix[-1].t0 < sw <= t for sw in switches)
    while t < total - 0.05:
        level = float(levels[min(bi, len(levels) - 1)]) if len(levels) else 1.0
        choices = m["cut_beats_high"] if level >= 0.85 else m["cut_beats_low"]
        if 0.6 <= level < 0.85:
            choices = list(m["cut_beats_high"]) + list(m["cut_beats_low"])
        n = int(rng.choice(choices))
        j = bi + n
        # Prefer to land on a bar (downbeat).
        for jj in range(j, min(j + 4, len(beats))):
            if bars[jj]:
                j = jj
                break
        t_end = beats[j] if j < len(beats) else total
        # Never run across a song change: cut exactly there (first beat after the switch).
        s_idx = bisect.bisect_right(switches, t + 0.25)
        force_flash = False
        if s_idx < len(switches) and switches[s_idx] < t_end:
            k = bisect.bisect_left(beats, switches[s_idx])
            t_end = beats[k] if k < len(beats) else switches[s_idx]
            force_flash = True
        if t_end - t < min_len and t_end < total:
            # Too short: extend to the next bar unless that crosses a song change.
            k = bisect.bisect_right(beats, t + min_len)
            while k < len(beats) and not bars[k]:
                k += 1
            cand = beats[k] if k < len(beats) else total
            if not force_flash or cand <= t_end:
                t_end = cand
        if total - t_end < min_len:
            t_end = total
        dur = t_end - t

        # Clip choice: avoid recent clips and the previous scene, favour rarely used clips.
        recent = set(history[-avoid:])
        prev_scene = clips[history[-1]].scene if history else None
        prev_tags = set(clips[history[-1]].tags) if history else set()
        weights = []
        for i, c in enumerate(clips):
            if i in recent and len(clips) > avoid:
                weights.append(0.0)
                continue
            w = c.weight * (0.05 + min(1.0, (t - last_used[i]) / 90.0) ** 2)
            if c.scene == prev_scene and len(clips) > 2:
                w *= 0.08
            if prev_tags and set(c.tags) == prev_tags:
                w *= 0.6
            weights.append(w)
        if sum(weights) <= 0:
            weights = [c.weight for c in clips]
        ci = rng.choices(range(len(clips)), weights=weights)[0]
        clip = clips[ci]
        history.append(ci)
        last_used[ci] = t

        lo, hi = m["speed_range"]
        speed = rng.uniform(lo, hi)
        direction = -1 if clip.reverse_ok and rng.random() < float(m["reverse_chance"]) else 1
        usable = clip.frames - 1
        need = dur * speed * clip.fps
        if clip.loop:
            wrap = "loop"
            start = rng.uniform(0, usable)
        elif need <= usable:
            wrap = "clamp"
            start = rng.uniform(0, usable - need)
            if direction < 0:
                start += need
        elif need <= usable * 1.3:
            wrap = "clamp"
            speed *= usable / need
            start = float(usable) if direction < 0 else 0.0
        else:
            wrap = "pingpong"
            start = rng.uniform(0, usable)
        rate = direction * speed * clip.fps

        z_lo, z_hi = m["zoom_range"]
        zoom0 = rng.uniform(z_lo, z_hi)
        zoom1 = min(z_hi + 0.05, max(1.0, zoom0 + rng.uniform(-0.07, 0.09)))
        pan0 = (rng.uniform(-1, 1), rng.uniform(-0.6, 0.6))
        pan1 = (max(-1, min(1, pan0[0] + rng.uniform(-0.5, 0.5))), max(-1, min(1, pan0[1] + rng.uniform(-0.3, 0.3))))
        grade = 0
        if m.get("grades", True):
            grade = 0 if rng.random() < 0.4 else rng.randrange(1, N_GRADES)

        if pending_flash and segments:
            transition = "flash"
        elif rng.random() < float(m["flash_chance"]) * (1.4 if level >= 0.85 else 0.5):
            transition = "flash"
        elif level < 0.85 and rng.random() < float(m["fade_chance"]) * 2:
            transition = "fade"
        else:
            transition = "cut"
        pending_flash = force_flash

        segments.append(Segment(
            t0=t, t1=t_end, clip=ci, src_start=start, rate=rate, wrap=wrap,
            mirror=bool(m.get("mirror", True) and clip.mirror_ok and rng.random() < 0.5),
            zoom0=zoom0, zoom1=zoom1, pan0=pan0, pan1=pan1, grade=grade, transition=transition,
        ))
        t = t_end
        bi = bisect.bisect_left(beats, t + 1e-3)
    if segments:
        segments[0].transition = "cut"
    return segments


def plan_signature(project: Project) -> str:
    """Settings that shape the cut. If they change, the whole plan is made anew."""
    keys = {"montage": project["montage"], "seed": project["seed"], "fps": project["video"]["fps"]}
    return hashlib.sha1(json.dumps(keys, sort_keys=True).encode()).hexdigest()[:16]


def _same_song(a: TimelineEntry, b: TimelineEntry) -> bool:
    return (a.path == b.path and abs(a.start - b.start) < 1e-3 and abs(a.end - b.end) < 1e-3
            and abs(a.gain_db - b.gain_db) < 1e-3)


def reusable_prefix(path: Path, project: Project, clips: list[Clip], timeline: list[TimelineEntry],
                    crossfade: float, end_fade: float) -> list[Segment]:
    """Segments of the previous build that are still valid.

    Everything before the first song that changed (or before the crossfade into a
    newly appended song) is kept as it was, so the start of the video stays
    identical and its rendered parts can be reused. New clips only show up after
    that point.
    """
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if data.get("signature") != plan_signature(project) or not data.get("timeline"):
        return []
    old_tl = [TimelineEntry(**e) for e in data["timeline"]]
    if len(old_tl) == len(timeline) and all(_same_song(a, b) for a, b in zip(old_tl, timeline)) \
            and abs(data.get("crossfade", 0) - crossfade) < 1e-6 and abs(data.get("end_fade", 0) - end_fade) < 1e-6:
        stable = float("inf")
    else:
        margin = max(data.get("crossfade", 0), data.get("end_fade", 0), crossfade, end_fade)
        stable = 0.0
        for k, (a, b) in enumerate(zip(old_tl, timeline)):
            if not _same_song(a, b):
                stable = min(a.start, b.start) if k else 0.0
                break
            if k == len(old_tl) - 1 or k == len(timeline) - 1:
                # The song that used to end the video (end fade) or now ends it.
                stable = min(a.end, b.end) - margin
                break
    by_path = {c.path: i for i, c in enumerate(clips)}
    old_clips = data["clips"]
    kept: list[Segment] = []
    for raw in data["segments"]:
        seg = Segment(**{**raw, "pan0": tuple(raw["pan0"]), "pan1": tuple(raw["pan1"])})
        old_clip = old_clips[seg.clip]
        new_index = by_path.get(old_clip["path"])
        if seg.t1 > stable - 0.5 or new_index is None or clips[new_index].frames != old_clip["frames"]:
            break
        seg.clip = new_index
        kept.append(seg)
    return kept


def save_edl(path: Path, clips: list[Clip], segments: list[Segment], project: Project | None = None,
             timeline: list[TimelineEntry] | None = None, crossfade: float = 0.0, end_fade: float = 0.0) -> None:
    path.write_text(json.dumps({
        "signature": plan_signature(project) if project else "",
        "timeline": [asdict(e) for e in timeline or []],
        "crossfade": crossfade,
        "end_fade": end_fade,
        "clips": [asdict(c) for c in clips],
        "segments": [asdict(s) for s in segments],
    }, indent=1), encoding="utf-8")


def load_edl(path: Path) -> tuple[list[Clip], list[Segment]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    clips = [Clip(**c) for c in data["clips"]]
    segments = [Segment(**{**s, "pan0": tuple(s["pan0"]), "pan1": tuple(s["pan1"])}) for s in data["segments"]]
    return clips, segments


def describe(clips: list[Clip], segments: list[Segment]) -> str:
    uses: dict[str, int] = {}
    for s in segments:
        uses[clips[s.clip].scene] = uses.get(clips[s.clip].scene, 0) + 1
    avg = (segments[-1].t1 / len(segments)) if segments else 0
    lines = [f"{len(segments)} Schnitte aus {len(clips)} Clips, Ø {avg:.1f}s pro Einstellung"]
    lines += [f"    {scene:<22} {n:>4}×" for scene, n in sorted(uses.items(), key=lambda kv: -kv[1])]
    return "\n".join(lines)
