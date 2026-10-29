"""Export for DaVinci Resolve: cut list (EDL), transparent overlay video, music as WAV.

In Resolve: import the scene clips, then the EDL as a timeline (every cut on
V1, with speed/reverse), put the overlay (speakers + titles with alpha) on V2
and the music on A1. Zoom/mirror/colour looks/flashes of the automatic render
are not part of the EDL - that is what you grade and edit in Resolve.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from . import ffmpeg_tools as ff
from .audio import MixResult
from .config import Project
from .montage import Clip, Segment


def source_indices(seg: Segment, clip: Clip, frames: np.ndarray, fps: float) -> np.ndarray:
    """Source frame per output frame - the same mapping the renderer uses."""
    n = clip.frames
    pos = seg.src_start + seg.rate * (frames / fps - seg.t0)
    fl = np.floor(pos).astype(np.int64)
    if seg.wrap == "loop":
        return fl % max(1, n - 1)
    if seg.wrap == "pingpong":
        period = max(1, 2 * (n - 1))
        m = fl % period
        return np.where(m < n, m, period - m)
    return np.clip(fl, 0, n - 1)


def segment_events(seg: Segment, clip: Clip, fps: float) -> list[dict]:
    """One EDL event per continuous run (a looped or ping-pong segment becomes several)."""
    r0, r1 = int(round(seg.t0 * fps)), int(round(seg.t1 * fps))
    if r1 <= r0:
        return []
    frames = np.arange(r0, r1)
    idx = source_indices(seg, clip, frames, fps)
    jump = 2 * abs(seg.rate) / fps + 2
    events, start, direction = [], 0, 0
    for k in range(1, len(idx) + 1):
        d = int(idx[k] - idx[k - 1]) if k < len(idx) else 0
        broken = k == len(idx) or abs(d) > jump or (d != 0 and direction != 0 and np.sign(d) != direction)
        if d != 0 and direction == 0 and not broken:
            direction = int(np.sign(d))
        if broken:
            run_dir = direction or (1 if seg.rate >= 0 else -1)
            events.append({
                "clip": clip, "src_in": int(idx[start]), "rec_in": r0 + start, "rec_out": r0 + k,
                "speed": run_dir * abs(seg.rate) / clip.fps * fps,
            # Reverse runs: give the lowest frame of the used span as source in (stays inside the media).
            "src_low": int(idx[start:k].min()),
            })
            start, direction = k, 0
    return events


def _tc(frames: int, fps: int) -> str:
    h, rem = divmod(int(frames), 3600 * fps)
    m, rem = divmod(rem, 60 * fps)
    s, f = divmod(rem, fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def _reel(clip: Clip) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", Path(clip.path).stem)[:32] or "CLIP"


def build_edl(title: str, clips: list[Clip], segments: list[Segment], fps: float) -> str:
    ifps = int(round(fps))
    offset = 3600 * ifps  # timeline starts at 01:00:00:00 like Resolve's default
    lines = [f"TITLE: {title}", "FCM: NON-DROP FRAME", ""]
    num = 0
    for seg in segments:
        for ev in segment_events(seg, clips[seg.clip], fps):
            num += 1
            dur = ev["rec_out"] - ev["rec_in"]
            reel = _reel(ev["clip"])
            src_in = ev["src_in"] if ev["speed"] >= 0 else ev["src_low"]
            lines.append(f"{num:03d}  {reel:<8} V     C        {_tc(src_in, ifps)} {_tc(src_in + dur, ifps)} "
                         f"{_tc(offset + ev['rec_in'], ifps)} {_tc(offset + ev['rec_out'], ifps)}")
            if abs(ev["speed"] - fps) > 0.05:
                lines.append(f"M2   {reel:<8} {ev['speed']:05.1f}                {_tc(src_in, ifps)}")
            lines.append(f"* FROM CLIP NAME: {Path(ev['clip'].path).name}")
            lines.append("")
    return "\r\n".join(lines) + "\r\n"


def export_resolve(project: Project, config_path: str, state_dir: Path, mix: MixResult,
                   clips: list[Clip], segments: list[Segment], n_frames: int, workers: int) -> Path:
    from .render import render_video

    fps = float(project["video"]["fps"])
    if abs(fps - round(fps)) > 1e-6:
        raise ValueError("Der Resolve-Export braucht eine ganzzahlige Bildrate (z. B. 24).")
    out = project.output_dir / f"{project['name']}_resolve"
    out.mkdir(parents=True, exist_ok=True)
    name = project["name"]
    edl = out / f"{name}_schnitt.edl"
    edl.write_text(build_edl(name, clips, segments, fps), encoding="utf-8")
    print(f"Schnittliste: {edl}")
    wav = out / f"{name}_musik.wav"
    ff.run([ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error", "-i", str(mix.path),
            "-c:a", "pcm_s24le", "-ar", str(project["audio"]["sample_rate"]), str(wav)])
    print(f"Musik: {wav}")
    from .render import OVERLAY_CODECS

    codec = str(project["resolve"].get("overlay_codec", "png"))
    overlay = None
    if codec != "keins":
        overlay = out / f"{name}_overlay_lautsprecher_titel{OVERLAY_CODECS[codec][1]}"
        if codec == "png":
            gb = n_frames / fps / 3600 * 20 * (project["video"]["width"] * project["video"]["height"]) / (1920 * 1080)
            print(f"Overlay mit Transparenz (PNG): ca. {gb:.0f} GB – kleiner: \"resolve\": {{\"overlay_codec\": \"vp9\"}}")
        render_video(project, config_path, state_dir, None, overlay, 0, n_frames, workers,
                     use_cache=False, kind="overlay")
    folders = sorted({str(Path(c.path).parent) for c in clips})
    (out / "LIESMICH_Resolve.txt").write_text(
        "DaVinci Resolve – so geht's\n"
        "============================\n\n"
        f"1. Projekt mit {int(fps)} fps und {project['video']['width']}x{project['video']['height']} anlegen.\n"
        "2. Projekteinstellungen > Allgemeine Optionen > Conform-Optionen:\n"
        "   'Assist using reel names from the: Source clip filename' anhaken.\n"
        "3. Diese Clip-Ordner in den Media Pool importieren:\n"
        + "".join(f"     {f}\n" for f in folders) +
        f"4. Datei > Importieren > Timeline > '{edl.name}' (Quellclips aus dem Media Pool verwenden).\n"
        + (f"5. '{overlay.name}' auf Spur V2 ab 01:00:00:00 (Lautsprecher + Titel, mit Transparenz).\n"
           if overlay else "5. (Overlay abgeschaltet: resolve.overlay_codec = keins)\n") +
        f"6. '{wav.name}' auf Spur A1 ab 01:00:00:00.\n\n"
        "Im EDL stecken alle Schnitte mit Tempo/Rückwärts. Zoom, Spiegeln, Farblooks und Blitze der\n"
        "automatischen Version sind nicht enthalten – die machst du in Resolve nach deinem Geschmack.\n",
        encoding="utf-8",
    )
    return out
