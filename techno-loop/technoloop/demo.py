"""Synthetic test project: three tiny techno tracks and generated test clips.

Lets you check ffmpeg, the GPU encoder and the whole build without Maestro.
"""

from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

from . import ffmpeg_tools as ff

SR = 44100


def _track(bpm: float, seconds: float, seed: int, breakdown: tuple[float, float]) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    out = np.zeros(n)
    beat = 60.0 / bpm
    k_len = int(0.35 * SR)
    tk = np.arange(k_len) / SR
    freq = 45 + 110 * np.exp(-tk * 28)
    kick = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tk * 7.5)
    hat = rng.normal(0, 1, int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90)
    hat = np.diff(hat, prepend=0)
    t = 0.0
    i = 0
    while t < seconds:
        p = int(t * SR)
        in_break = breakdown[0] <= t < breakdown[1]
        if not in_break:
            m = min(k_len, n - p)
            out[p:p + m] += 0.9 * kick[:m]
        q = int((t + beat / 2) * SR)
        if q < n:
            m = min(len(hat), n - q)
            out[q:q + m] += 0.25 * hat[:m]
        # Off-beat bass stab.
        b0 = int((t + beat * 0.5) * SR)
        bl = int(beat * 0.4 * SR)
        if b0 + bl < n:
            tb = np.arange(bl) / SR
            f = 55 * (1.5 if (i // 8) % 2 else 1.0)
            out[b0:b0 + bl] += 0.35 * np.sign(np.sin(2 * np.pi * f * tb)) * np.exp(-tb * 9)
        t += beat
        i += 1
    pad = np.sin(2 * np.pi * 220 * np.arange(n) / SR) * 0.05 * (0.5 + 0.5 * np.sin(np.arange(n) / SR * 0.7))
    out += pad
    return out / (np.abs(out).max() + 1e-9) * 0.9


def _write_wav(path: Path, mono: np.ndarray) -> None:
    data = (np.clip(mono, -1, 1) * 32767).astype("<i2")
    stereo = np.repeat(data[:, None], 2, axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


CLIP_SOURCES = [
    ("lasers", "gradients=s=1280x704:r=24:speed=0.04:c0=0x001020:c1=0x00c8ff:c2=0x200030:c3=0xff3b30:n=4"),
    ("crowd", "cellauto=s=1280x704:r=24:rule=110:random_fill_ratio=0.5,format=rgb24,colorchannelmixer=rr=0.2:gg=0.6:bb=1.0"),
    ("stage_loop", "mandelbrot=s=1280x704:r=24:start_scale=1.5:end_scale=0.6"),
    ("lights", "life=s=1280x704:r=24:mold=12:life_color=#00c8ff:death_color=#2a0010:mold_color=#ff3b30"),
]


def make_demo(target: Path) -> None:
    (target / "musik").mkdir(parents=True, exist_ok=True)
    clips_dir = target / "clips"
    clips_dir.mkdir(exist_ok=True)
    songs = [("01 - Demo Artist - Night Drive", 124, 41), ("02 - Nova & Mila - Turtle Stage", 128, 38),
             ("03 - Demo Artist - Laser Rain", 132, 36)]
    for k, (name, bpm, secs) in enumerate(songs):
        path = target / "musik" / f"{name}.wav"
        if not path.exists():
            _write_wav(path, _track(bpm, secs, k, (secs * 0.45, secs * 0.6)))
            print(f"  Song: {path.name}")
    for name, src in CLIP_SOURCES:
        path = clips_dir / f"{name}.mp4"
        if not path.exists():
            ff.run([ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error", "-f", "lavfi", "-i", src,
                    "-t", "7.3", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast", str(path)])
            print(f"  Clip: {path.name}")
    project = {
        "name": "demo_techno_loop",
        "clips_folder": "clips",
        "songs_folder": "musik",
        "audio": {"duration_minutes": 0, "crossfade_seconds": 4},
        "video": {"workers": 2, "clip_cache": 4},
        "titles": {"watermark": "TECHNO LOOP DEMO"},
        "scenes": [],
    }
    (target / "projekt.json").write_text(json.dumps(project, indent=2), encoding="utf-8")
