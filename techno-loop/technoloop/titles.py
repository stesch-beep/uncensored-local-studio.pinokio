"""'Now playing' panel, per-song intro card and optional watermark."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .audio import TimelineEntry
from .config import Project
from .speakers import Sprite, blend_sprite, hex_to_bgr

BOLD_FONTS = [
    "C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
LIGHT_FONTS = [
    "C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _font(explicit, candidates, size: int, variation: str | None = None):
    paths = ([str(explicit)] if explicit else []) + candidates
    windir = os.environ.get("WINDIR")
    if windir:
        paths += [str(Path(windir) / "Fonts" / Path(p).name) for p in candidates if p.startswith("C:/Windows")]
    for path in paths:
        if path and Path(path).is_file():
            font = ImageFont.truetype(path, size)
            if variation:
                try:
                    font.set_variation_by_name(variation)
                except Exception:
                    pass
            return font
    return ImageFont.load_default(size=size)


def _rgba_to_sprite(img: Image.Image) -> np.ndarray:
    arr = np.asarray(img, dtype=np.float32)
    a = arr[..., 3:4] / 255.0
    bgr = arr[..., [2, 1, 0]] * a
    return Sprite(np.concatenate([bgr, a], axis=2))


def _spaced(draw: ImageDraw.ImageDraw, xy, text, font, fill, spacing: float) -> float:
    """Draw letter-spaced text, return the advance width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x - xy[0] - spacing


def _spaced_width(draw, text, font, spacing: float) -> float:
    return sum(draw.textlength(ch, font=font) for ch in text) + spacing * max(0, len(text) - 1)


def _fit(draw, text, font_factory, size, max_w, spacing_factor=0.0):
    while size > 10:
        font = font_factory(size)
        if _spaced_width(draw, text, font, size * spacing_factor) <= max_w:
            return font, text
        size -= 2
    font = font_factory(size)
    while text and _spaced_width(draw, text + "…", font, size * spacing_factor) > max_w:
        text = text[:-1]
    return font, text + "…"


class TitleOverlay:
    def __init__(self, project: Project, timeline: list[TimelineEntry], width: int, height: int,
                 side_reserved: int = 0):
        self.cfg = cfg = project["titles"]
        self.enabled = bool(cfg.get("enabled", True))
        self.W, self.H = width, height
        self.timeline = timeline
        self.switches = [0.0] + [0.5 * (cur.start + prev.end) for prev, cur in zip(timeline, timeline[1:])]
        self.accent = cfg.get("accent", "#00c8ff")
        self.accent_bgr = hex_to_bgr(self.accent)
        scale = float(cfg.get("scale", 1.0)) * height / 1080.0
        self.scale = scale
        self.margin = int(height * 0.035)
        position = cfg.get("position", "bottom-center")
        if position == "bottom-center":
            self.max_w = max(int(width * 0.3), width - 2 * side_reserved - 2 * self.margin)
        else:
            self.max_w = int(width * 0.48)
        self.position = position
        bold = lambda s: _font(project.path(cfg.get("font")), BOLD_FONTS, s, "Bold")
        light = lambda s: _font(project.path(cfg.get("font_light")), LIGHT_FONTS, s, "Light")
        self._bold, self._light = bold, light
        self.panels = []
        self.cards = []
        if self.enabled:
            for entry in timeline:
                self.panels.append(self._panel(entry))
                self.cards.append(self._card(entry) if cfg.get("intro_card", True) else None)
        self.watermark = self._watermark(cfg.get("watermark")) if cfg.get("watermark") else None

    def _text(self, value: str) -> str:
        return value.upper() if self.cfg.get("uppercase", True) else value

    def _panel(self, entry: TimelineEntry):
        s = self.scale
        pad_x, pad_y = int(26 * s), int(18 * s)
        bar_w = max(3, int(6 * s))
        probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        inner_max = self.max_w - 2 * pad_x - bar_w - int(14 * s)
        label = self.cfg.get("label", "NOW PLAYING")
        if self.cfg.get("show_number", True):
            # Without the total by default: appending songs then leaves earlier titles unchanged.
            total = f" / {entry.count:02d}" if self.cfg.get("show_total", False) else ""
            label = f"{label}  ·  {entry.number:02d}{total}"
        f_label = self._bold(int(20 * s))
        f_title, title = _fit(probe, self._text(entry.title), self._bold, int(50 * s), inner_max, 0.04)
        f_artist, artist = _fit(probe, self._text(entry.artist or ""), self._light, int(30 * s), inner_max, 0.08)
        lw = _spaced_width(probe, label, f_label, 20 * s * 0.25)
        tw = _spaced_width(probe, title, f_title, f_title.size * 0.04)
        aw = _spaced_width(probe, artist, f_artist, f_artist.size * 0.08) if artist else 0
        content_w = int(max(lw, tw, aw))
        w = content_w + 2 * pad_x + bar_w + int(14 * s)
        h_label, h_title, h_artist = int(28 * s), int(f_title.size * 1.18), int(f_artist.size * 1.3) if artist else 0
        prog_h = int(16 * s) if self.cfg.get("show_progress", True) else 0
        h = pad_y + h_label + h_title + h_artist + prog_h + pad_y
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(10 * s), fill=(5, 8, 14, 165))
        r, g, b = (int(self.accent[i:i + 2], 16) for i in (1, 3, 5))
        d.rectangle((0, int(10 * s), bar_w, h - int(10 * s)), fill=(r, g, b, 255))
        x = bar_w + pad_x
        y = pad_y
        _spaced(d, (x, y), label, f_label, (r, g, b, 255), 20 * s * 0.25)
        y += h_label
        _spaced(d, (x, y), title, f_title, (255, 255, 255, 255), f_title.size * 0.04)
        y += h_title
        if artist:
            _spaced(d, (x, y), artist, f_artist, (200, 210, 225, 255), f_artist.size * 0.08)
            y += h_artist
        prog = None
        if prog_h:
            py = y + int(6 * s)
            prog = (x, py, x + content_w, py + max(2, int(4 * s)))
            d.rectangle(prog, fill=(255, 255, 255, 55))
        return {"sprite": _rgba_to_sprite(img), "progress": prog, "size": (w, h)}

    def _card(self, entry: TimelineEntry):
        s = self.scale
        probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        max_w = int(self.W * 0.8)
        f_title, title = _fit(probe, self._text(entry.title), self._bold, int(96 * s), max_w, 0.06)
        f_artist, artist = _fit(probe, self._text(entry.artist or ""), self._light, int(44 * s), max_w, 0.3)
        tw = _spaced_width(probe, title, f_title, f_title.size * 0.06)
        aw = _spaced_width(probe, artist, f_artist, f_artist.size * 0.3) if artist else 0
        w = int(max(tw, aw)) + int(60 * s)
        h = int(f_title.size * 1.25 + (f_artist.size * 1.6 if artist else 0) + 50 * s)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        r, g, b = (int(self.accent[i:i + 2], 16) for i in (1, 3, 5))
        y = int(10 * s)
        if artist:
            _spaced(d, ((w - aw) / 2, y), artist, f_artist, (r, g, b, 255), f_artist.size * 0.3)
            y += int(f_artist.size * 1.6)
        # Soft dark halo behind the big title for readability on bright frames.
        halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        _spaced(hd, ((w - tw) / 2, y), title, f_title, (0, 0, 0, 200), f_title.size * 0.06)
        from PIL import ImageFilter

        halo = halo.filter(ImageFilter.GaussianBlur(int(14 * s)))
        img = Image.alpha_composite(halo, img)
        d = ImageDraw.Draw(img)
        _spaced(d, ((w - tw) / 2, y), title, f_title, (255, 255, 255, 255), f_title.size * 0.06)
        line_y = y + int(f_title.size * 1.15)
        d.rectangle(((w - tw) / 2, line_y, (w + tw) / 2, line_y + max(2, int(3 * s))), fill=(r, g, b, 230))
        return _rgba_to_sprite(img)

    def _watermark(self, text: str):
        s = self.scale
        font = self._bold(int(26 * s))
        probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        w = int(_spaced_width(probe, text, font, 26 * s * 0.3)) + 8
        img = Image.new("RGBA", (w, int(40 * s)), (0, 0, 0, 0))
        _spaced(ImageDraw.Draw(img), (4, 2), text, font, (255, 255, 255, 150), 26 * s * 0.3)
        return _rgba_to_sprite(img)

    def song_at(self, t: float) -> int:
        k = 0
        for i, sw in enumerate(self.switches):
            if t >= sw:
                k = i
        return k

    def draw(self, frame: np.ndarray, t: float) -> None:
        if self.watermark is not None:
            wm = self.watermark
            blend_sprite(frame, wm, self.W - wm.shape[1] - self.margin, self.margin, 1.0)
        if not self.enabled or not self.panels:
            return
        k = self.song_at(t)
        entry = self.timeline[k]
        since = t - self.switches[k]
        until_next = (self.switches[k + 1] - t) if k + 1 < len(self.switches) else 1e9
        alpha = min(1.0, since / 0.6, until_next / 0.4)
        alpha = max(0.0, alpha)
        panel = self.panels[k]
        pw, ph = panel["size"]
        slide = int((1.0 - min(1.0, since / 0.6)) ** 2 * 30 * self.scale)
        if self.position == "bottom-center":
            x, y = (self.W - pw) // 2, self.H - self.margin - ph + slide
        elif self.position == "top-left":
            x, y = self.margin, self.margin + slide
        elif self.position == "bottom-left":
            x, y = self.margin, self.H - self.margin - ph + slide
        else:  # top-center
            x, y = (self.W - pw) // 2, self.margin + slide
        if alpha > 0:
            blend_sprite(frame, panel["sprite"], x, y, alpha)
            prog = panel["progress"]
            if prog and alpha > 0.98:
                frac = np.clip((t - entry.start) / max(1e-3, entry.end - entry.start), 0, 1)
                x0, y0, x1, y1 = prog
                xe = int(x0 + (x1 - x0) * frac)
                if xe > x0:
                    frame[y + y0:y + y1, x + x0:x + xe] = self.accent_bgr
        card = self.cards[k] if self.cards else None
        dur = float(self.cfg.get("intro_seconds", 4.5))
        if card is not None and since < dur:
            a = min(1.0, since / 0.5, (dur - since) / 0.8)
            if a > 0:
                ch, cw = card.shape
                rise = int((1 - min(1.0, since / 0.8)) ** 2 * 24 * self.scale)
                blend_sprite(frame, card, (self.W - cw) // 2, int(self.H * 0.40 - ch / 2) + rise, a)
