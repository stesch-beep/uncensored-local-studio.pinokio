"""Locating and calling ffmpeg / ffprobe."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


class FFmpegError(RuntimeError):
    pass


def _pinokio_candidates(name: str) -> list[Path]:
    exe = name + (".exe" if os.name == "nt" else "")
    home = Path.home()
    roots = [home / "pinokio" / "bin", Path("C:/pinokio/bin")]
    out = []
    for root in roots:
        out += [
            root / "miniconda" / "Library" / "bin" / exe,
            root / "miniconda" / "bin" / exe,
            root / "ffmpeg-env" / "Library" / "bin" / exe,
        ]
    return out


@lru_cache(maxsize=None)
def find_tool(name: str) -> str:
    env = os.environ.get(name.upper())
    if env and Path(env).is_file():
        return env
    found = shutil.which(name)
    if found:
        return found
    for candidate in _pinokio_candidates(name):
        if candidate.is_file():
            return str(candidate)
    if name == "ffmpeg":
        try:
            import imageio_ffmpeg

            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass
    raise FFmpegError(
        f"{name} wurde nicht gefunden. Installiere es (Windows: 'winget install Gyan.FFmpeg') "
        f"oder setze die Umgebungsvariable {name.upper()} auf den Pfad zur {name}.exe."
    )


def ffmpeg() -> str:
    return find_tool("ffmpeg")


def run(args: list[str], *, capture: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-15:]
        raise FFmpegError(f"{Path(args[0]).name} ist fehlgeschlagen:\n" + "\n".join(tail))
    return proc


def probe(path: Path) -> dict:
    """Duration/fps/frames/size of a media file (ffprobe if present, else ffmpeg -i parsing)."""
    try:
        ffprobe = find_tool("ffprobe")
    except FFmpegError:
        ffprobe = None
    if ffprobe:
        proc = run([
            ffprobe, "-v", "error", "-print_format", "json",
            "-show_format", "-show_streams", str(path),
        ])
        data = json.loads(proc.stdout.decode("utf-8", "replace") or "{}")
        info = {"duration": float(data.get("format", {}).get("duration") or 0.0), "tags": {}}
        for key, value in (data.get("format", {}).get("tags") or {}).items():
            info["tags"][key.lower()] = value
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and "width" not in info:
                num, _, den = str(stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1").partition("/")
                fps = float(num) / float(den or 1) if float(den or 1) else 0.0
                info.update(width=int(stream["width"]), height=int(stream["height"]), fps=fps)
                if stream.get("nb_frames"):
                    info["frames"] = int(stream["nb_frames"])
            if stream.get("codec_type") == "audio":
                info["has_audio"] = True
        return info
    # Fallback: parse "Duration:" from ffmpeg's banner.
    proc = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)], stderr=subprocess.PIPE)
    text = proc.stderr.decode("utf-8", "replace")
    import re

    info = {"duration": 0.0, "tags": {}}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", text)
    if m:
        info["duration"] = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    m = re.search(r"Video: .*?, (\d{2,5})x(\d{2,5}).*?, ([\d.]+) fps", text)
    if m:
        info.update(width=int(m[1]), height=int(m[2]), fps=float(m[3]))
    return info


ENCODERS = {
    "h264": ["h264_nvenc", "libx264"],
    "hevc": ["hevc_nvenc", "libx265"],
    "av1": ["av1_nvenc", "libsvtav1"],
}


@lru_cache(maxsize=None)
def encoder_works(encoder: str) -> bool:
    proc = subprocess.run(
        [ffmpeg(), "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
         "color=c=black:s=256x144:r=24:d=0.5", "-c:v", encoder, "-f", "null", "-"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def pick_encoder(codec: str, requested: str = "auto") -> str:
    if requested and requested != "auto":
        if not encoder_works(requested):
            raise FFmpegError(f"Encoder '{requested}' funktioniert mit diesem ffmpeg nicht.")
        return requested
    for encoder in ENCODERS.get(codec, ENCODERS["h264"]):
        if encoder_works(encoder):
            return encoder
    raise FFmpegError(f"Kein funktionierender Encoder für '{codec}' gefunden.")


def encoder_args(encoder: str, quality: int, fps: int) -> list[str]:
    gop = str(int(fps) * 2)
    if encoder.endswith("_nvenc"):
        return [
            "-c:v", encoder, "-preset", "p5", "-tune", "hq", "-rc", "vbr",
            "-cq", str(quality), "-b:v", "0", "-maxrate", "40M", "-bufsize", "80M",
            "-g", gop, "-bf", "2", "-pix_fmt", "yuv420p",
        ]
    if encoder == "libx264":
        return ["-c:v", "libx264", "-preset", "medium", "-crf", str(quality), "-g", gop, "-pix_fmt", "yuv420p"]
    if encoder == "libx265":
        return ["-c:v", "libx265", "-preset", "medium", "-crf", str(quality + 2), "-g", gop, "-pix_fmt", "yuv420p", "-tag:v", "hvc1"]
    return ["-c:v", encoder, "-crf", str(quality + 10), "-g", gop, "-pix_fmt", "yuv420p"]
