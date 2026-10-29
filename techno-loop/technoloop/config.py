"""Project configuration: defaults, loading and path resolution."""

from __future__ import annotations

import copy
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULTS = {
    "name": "techno_loop_1h",
    "work_dir": "arbeitsordner",
    "output_dir": "ausgabe",
    "seed": 1234,
    "maestro": {
        "url": "auto",
        # H3 Fused 4-Step – Frames (Turbo eingebaut, 4 Schritte). Start = Endbild -> nahtloser Loop.
        "model": "minimax_h3_fused_turbo",
        # H3 Fused 4-Step – References, für Szenen nur mit Identitätsbildern.
        "omni_model": "minimax_h3_ref2va_fused_turbo",
        # Ältere Maestro-Versionen ohne Fused-Modell: normales H3 + Turbo-LoRA.
        "fallback_model": "minimax_h3",
        "fallback_omni_model": "minimax_h3_ref2va",
        # Name of a preset saved in Maestro (e.g. "H3 Steps4"). If found, its
        # steps/LoRAs/params win over the values below.
        "preset": "H3 Steps4",
        "resolution": "1280x704",
        "frames": 175,
        "steps": 4,
        "turbo": "auto",  # auto = Turbo-LoRA nur bei Modellen ohne eingebauten Turbo
        "turbo_lora": "minimax_h3_turbo_4step_ckpt500.safetensors",
        "turbo_strength": 0.7,
        "variants": 2,
        "poll_seconds": 3,
        "timeout_minutes": 180,
        "workspace": "",
        "extra_params": {},
    },
    "keyframes": {
        # Standbilder der Girls pro Szene (werden in H3 erster = letzter Frame -> nahtloser Loop).
        "engine": "maestro",            # maestro | comfyui
        "model": "qwen_image_21_7B",     # Maestro: Qwen Image 2.1 (bis 10 Referenzbilder); Turbo: qwen_image_21_7B_turbo
        "fallback_model": "krea2_turbo_edit",  # ältere Maestro-Versionen: Krea 2 Turbo Identity Edit
        "resolution": "1280x720",
        "steps": 0,                      # 0 = Standard des Modells
        "folder": "bilder/keyframes",
        "candidates": 1,
        "extra_params": {},
        "comfyui_url": "http://127.0.0.1:8188",
        "comfyui_workflow": "",          # Workflow im API-Format (ComfyUI: "Export (API)")
    },
    "style": (
        "Cinematic live festival concert footage at night, gigantic main stage, "
        "dense haze, deep blue and cyan lighting with red accents, sharp laser beams, "
        "high contrast, anamorphic wide lens, 35mm film grain"
    ),
    "soundscape": "Huge festival crowd cheering, deep sub-bass rumble from the sound system, no human voices.",
    "music": "Driving peak-time techno at 130 BPM with a heavy four-on-the-floor kick.",
    "style_reference": "",
    "girls": [],
    "scenes": [],
    "clips_folder": "",
    "songs_folder": "musik",
    "songs": [],
    # Where {"find": "..."} playlist entries and the 'lieder' / 'song-dazu' commands look for songs.
    "song_search": [
        "musik", "~/Downloads", "~/Downloads/suno", "C:/Download", "C:/Download/suno",
        "C:/Downloads", "C:/Downloads/suno", "F:/Pinokio Projekt Fire und ice", "F:/Pinokio Projekt",
    ],
    "song_search_depth": 3,
    "default_artist": "",
    "audio": {
        "crossfade_seconds": 6.0,
        "target_lufs": -14.0,
        "true_peak": -1.0,
        "duration_minutes": 0,
        "shuffle": False,
        "sample_rate": 48000,
        "bitrate": "320k",
        "end_fade_seconds": 6.0,
    },
    "video": {
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "codec": "h264",
        "encoder": "auto",
        "quality": 19,
        "workers": 3,
        "clip_cache": 4,
        "chunk_seconds": 120,
    },
    "montage": {
        "cut_beats_high": [4, 8, 8, 16],
        "cut_beats_low": [8, 16, 16, 32],
        "min_segment_seconds": 1.5,
        "speed_range": [0.92, 1.08],
        "zoom_range": [1.0, 1.18],
        "mirror": True,
        "reverse_chance": 0.15,
        "flash_chance": 0.12,
        "fade_chance": 0.10,
        "fade_frames": 8,
        "avoid_repeat": 4,
        "bass_zoom": 0.02,
        "light_pump": 0.12,
        "grain": 0.25,
        "vignette": 0.35,
        "grades": True,
    },
    "speakers": {
        "enabled": True,
        "image": "",
        "cone": [0.5, 0.64, 0.33],
        "tweeter": [0.5, 0.2, 0.1],
        "size": 0.40,
        "positions": ["bottom-left", "bottom-right"],
        "margin": 0.02,
        "excursion": 0.085,
        "led_colors": ["#00c8ff", "#ff3b30"],
        "spring_hz": 9.0,
        "damping": 0.45,
        "glow": True,
    },
    "resolve": {
        # png (sicher, ca. 20 GB pro Stunde bei 1080p) | qtrle | prores4444 | vp9 (winzig, WebM) | keins
        "overlay_codec": "png",
    },
    "titles": {
        "enabled": True,
        "position": "bottom-center",
        "font": "",
        "font_light": "",
        "label": "NOW PLAYING",
        "accent": "#00c8ff",
        "show_number": True,
        "show_total": False,
        "show_progress": True,
        "intro_card": True,
        "intro_seconds": 4.5,
        "scale": 1.0,
        "watermark": "",
    },
}

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus", ".wma"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}


class ConfigError(RuntimeError):
    pass


def _deep_merge(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if key.startswith("_"):
            continue  # "_hinweis" style comment keys
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


@dataclass
class Song:
    path: Path
    title: str
    artist: str
    explicit: bool = False  # title given in projekt.json -> never replaced by file tags

    @property
    def display(self) -> str:
        return f"{self.artist} – {self.title}" if self.artist else self.title


@dataclass
class Project:
    data: dict
    base_dir: Path
    config_path: Path | None = None

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def path(self, value) -> Path | None:
        if not value:
            return None
        p = Path(os.path.expandvars(os.path.expanduser(str(value))))
        return p if p.is_absolute() else (self.base_dir / p).resolve()

    @property
    def work_dir(self) -> Path:
        return self.path(self.data["work_dir"])

    @property
    def scenes_dir(self) -> Path:
        return self.work_dir / "szenen"

    @property
    def cache_dir(self) -> Path:
        return self.work_dir / "cache"

    @property
    def output_dir(self) -> Path:
        return self.path(self.data["output_dir"])

    def songs(self) -> list[Song]:
        from .songs import resolve_playlist

        return resolve_playlist(self)


def parse_song_name(path: Path) -> tuple[str, str]:
    """'03 - Artist - Title.mp3' -> ('Title', 'Artist'); 'Title.mp3' -> ('Title', '')."""
    stem = re.sub(r"^\s*\d{1,3}\s*[-._)]\s*", "", path.stem)
    stem = re.sub(r"\s*\(\d{1,2}\)$", "", stem)  # "Song (1).wav" = second download of the same song
    stem = stem.replace("_", " ").strip()
    parts = [p.strip() for p in re.split(r"\s+[-–—]\s+", stem) if p.strip()]
    if len(parts) >= 2:
        return " - ".join(parts[1:]), parts[0]
    return stem, ""


def load_project(path: str | os.PathLike) -> Project:
    config_path = Path(path).resolve()
    if not config_path.is_file():
        raise ConfigError(f"Projektdatei nicht gefunden: {config_path}")
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"{config_path.name} ist kein gültiges JSON (Zeile {error.lineno}, Spalte {error.colno}): {error.msg}"
        ) from error
    project = Project(_deep_merge(DEFAULTS, raw), config_path.parent, config_path)
    for index, scene in enumerate(project.data["scenes"]):
        if not scene.get("id"):
            raise ConfigError(f"Szene {index + 1} hat keine \"id\".")
        if not re.fullmatch(r"[A-Za-z0-9_\-]+", scene["id"]):
            raise ConfigError(f"Szenen-id '{scene['id']}' darf nur Buchstaben, Zahlen, _ und - enthalten.")
    return project
