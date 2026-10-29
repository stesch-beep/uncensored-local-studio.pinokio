"""Loudspeaker overlay whose woofer cone pumps with the kick.

Layers are premultiplied float32 BGRA. The static parts (cabinet, frame,
surround) are drawn once; per frame only the cone and the dust cap are scaled
(the cap a bit more than the cone, so the membrane reads as moving towards the
viewer), relit, and the LED ring's brightness follows the bass.
"""

from __future__ import annotations

import cv2
import numpy as np

from .config import Project

SS = 2  # supersampling for the procedural drawing


def hex_to_bgr(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return float(b), float(g), float(r)


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _premul(bgr: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    return np.dstack([bgr * alpha[..., None], alpha]).astype(np.float32)


def _over_full(dst: np.ndarray, src: np.ndarray) -> None:
    dst *= 1.0 - src[..., 3:4]
    dst += src


def _clip_box(dst_shape, w, h, x, y):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(dst_shape[1], x + w), min(dst_shape[0], y + h)
    return x0, y0, x1, y1


def _over(dst: np.ndarray, src: np.ndarray, x: int, y: int) -> None:
    """Premultiplied 'over' of BGRA src into dst (float, 3 or 4 channels) at (x, y), clipped."""
    h, w = src.shape[:2]
    x0, y0, x1, y1 = _clip_box(dst.shape, w, h, x, y)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    c = d.shape[2]
    d *= 1.0 - s[..., 3:4]
    d += s[..., :c]


class Sprite:
    """Static premultiplied sprite with cached inverse alpha for fast blending."""

    def __init__(self, bgra: np.ndarray):
        self.bgra = bgra.astype(np.float32)
        self.rgb = np.ascontiguousarray(self.bgra[..., :3])
        a = self.bgra[..., 3]
        self.alpha = np.ascontiguousarray(a)
        self.inv = cv2.merge([1.0 - a] * 3)
        self.shape = self.bgra.shape[:2]


def blend_sprite(frame: np.ndarray, sprite, x: int, y: int, opacity: float = 1.0) -> None:
    """Premultiplied sprite (Sprite or BGRA float array) over a uint8 BGR frame, in place."""
    if not isinstance(sprite, Sprite):
        sprite = Sprite(sprite)
    h, w = sprite.shape
    x0, y0, x1, y1 = _clip_box(frame.shape, w, h, x, y)
    if x1 <= x0 or y1 <= y0 or opacity <= 0:
        return
    sl = (slice(y0 - y, y1 - y), slice(x0 - x, x1 - x))
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    if opacity >= 0.999:
        cv2.multiply(roi, sprite.inv[sl], dst=roi)
        cv2.add(roi, sprite.rgb[sl], dst=roi)
    else:
        a = sprite.alpha[sl] * opacity
        roi *= (1.0 - a)[..., None]
        roi += sprite.rgb[sl] * opacity
    frame[y0:y1, x0:x1] = cv2.convertScaleAbs(roi)


class SpeakerSprite:
    def __init__(self, height: int, led_bgr, cfg: dict, image_path=None, rng_seed: int = 0):
        self.cfg = cfg
        self.excursion = float(cfg["excursion"])
        self.led = np.array(led_bgr, dtype=np.float32)
        self.cap = None
        self.dome = None
        self.tweet = None
        self.led_alpha = None
        if image_path:
            self._from_image(image_path, height)
        else:
            self._procedural(height, rng_seed)
        self.base = Sprite(self.base_bgra)
        self.shape = self.base.shape
        cx, cy, R = self.woofer
        r = int(np.ceil(R * 1.35))
        self.led_box = _clip_box(self.shape, 2 * r, 2 * r, int(cx - r), int(cy - r))
        self.led_rgb = None
        if self.led_alpha is not None:
            x0, y0, x1, y1 = self.led_box
            self.led_rgb = np.ascontiguousarray(self.led_alpha[y0:y1, x0:x1, None] * self.led[None, None])

    # -- procedural cabinet -------------------------------------------------
    def _procedural(self, height: int, seed: int) -> None:
        H = height * SS
        W = int(H / 1.5)
        pad = int(0.09 * W)
        CH, CW = H + 2 * pad, W + 2 * pad
        rng = np.random.default_rng(seed)
        yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)

        # Cabinet body: rounded corners, vertical gradient, grain, bevelled edge, drop shadow.
        r = 0.06 * W
        qx = np.clip(np.abs(xx - CW / 2) - (W / 2 - r), 0, None)
        qy = np.clip(np.abs(yy - CH / 2) - (H / 2 - r), 0, None)
        dist = np.sqrt(qx ** 2 + qy ** 2) - r
        cab = _smoothstep(1.5, -1.5, dist)
        grad = 1.0 - 0.35 * ((yy - pad) / H)
        noise = cv2.GaussianBlur(rng.normal(0, 1, (CH, CW)).astype(np.float32), (0, 0), 1.2)
        body = np.array([20, 19, 17], np.float32) * (grad + 0.05 * noise)[..., None]
        edge = _smoothstep(-9 * SS, -2 * SS, dist) * (1 - _smoothstep(-2 * SS, 0, dist))
        light = np.clip(1.0 - (yy - pad) / H * 1.2, 0, 1) * 0.9 + 0.1
        body += np.array([70, 72, 78], np.float32) * (edge * light)[..., None]
        shadow = cv2.GaussianBlur(cab, (0, 0), pad / 2.5)
        shadow = np.roll(shadow, int(pad * 0.35), axis=0) * 0.75
        base = _premul(np.zeros((CH, CW, 3), np.float32), shadow)
        _over_full(base, _premul(body, cab))

        woofer = (CW / 2, pad + 0.64 * H, 0.40 * W)
        tweet = (CW / 2, pad + 0.20 * H, 0.12 * W)
        lx, ly = -0.55, -0.83  # light from the upper left

        for (cx, cy, R), big in ((woofer, True), (tweet, False)):
            dx, dy = xx - cx, yy - cy
            rr = np.sqrt(dx * dx + dy * dy)
            th = np.arctan2(dy, dx)
            # Metal mounting ring with a brushed highlight and screws.
            frame = _smoothstep(R * 1.17, R * 1.15, rr) * _smoothstep(R * 0.97, R * 0.99, rr)
            spec = 0.5 + 0.5 * np.cos(th - np.arctan2(ly, lx))
            metal = np.array([62, 64, 70], np.float32)[None, None] * (0.45 + 0.9 * spec ** 3)[..., None]
            metal += (8 * np.sin(rr * 0.9))[..., None]
            _over_full(base, _premul(metal, frame))
            n_screws = 8 if big else 4
            for k in range(n_screws):
                a = 2 * np.pi * k / n_screws + np.pi / n_screws
                sx, sy = cx + np.cos(a) * R * 1.08, cy + np.sin(a) * R * 1.08
                sr = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2)
                sa = _smoothstep(R * 0.045 + 1, R * 0.045 - 1, sr)
                sh = np.clip(0.35 - ((xx - sx) * lx + (yy - sy) * ly) / (R * 0.05), 0, 1.4)
                _over_full(base, _premul(np.array([90, 92, 98], np.float32) * sh[..., None], sa))
            # Rubber surround: half torus lit from the upper left.
            inner, outer = (R * 0.80, R * 1.0) if big else (R * 0.70, R * 1.0)
            u = np.clip((rr - (inner + outer) / 2) / ((outer - inner) / 2), -1, 1)
            hgt = np.sqrt(np.clip(1 - u * u, 0, 1))
            nx, ny = u * np.cos(th), u * np.sin(th)
            shade = np.clip(-(nx * lx + ny * ly) * 0.9 + hgt * 0.35, 0, None)
            sur_a = _smoothstep(outer + 1, outer - 1, rr) * _smoothstep(inner - 3, inner, rr)
            rubber = np.array([24, 24, 27], np.float32)[None, None] * (0.35 + 1.3 * shade)[..., None]
            rubber += 40 * (np.clip(shade - 0.75, 0, 1) ** 2)[..., None]
            _over_full(base, _premul(rubber, sur_a))
            if big:
                # Emissive LED ring just outside the surround (brightness animated per frame).
                ring = np.exp(-((rr - R * 1.005) / (R * 0.012)) ** 2)
                glow = np.exp(-((rr - R * 1.005) / (R * 0.10)) ** 2) * 0.55
                led_alpha = (ring + glow).astype(np.float32)

        cx, cy, R = woofer
        size = int(np.ceil(R * 0.84 * 2)) + 4
        cone, cap = self._draw_cone(size, R, lx, ly, rng)
        tR = tweet[2]
        tsize = int(np.ceil(tR * 0.74 * 2)) + 4
        dome = self._draw_dome(tsize, tR * 0.72, lx, ly)

        down = lambda img, w, h: cv2.resize(img, (w // SS, h // SS), interpolation=cv2.INTER_AREA)
        self.base_bgra = down(base, CW, CH)
        self.led_alpha = down(led_alpha, CW, CH)
        self.cone = down(cone, size, size)
        self.cap = down(cap, size, size)
        self.dome = down(dome, tsize, tsize)
        self.woofer = tuple(v / SS for v in woofer)
        self.tweet = tuple(v / SS for v in tweet)

    @staticmethod
    def _draw_cone(size, R, lx, ly, rng):
        c = size / 2
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
        dx, dy = xx - c, yy - c
        rr = np.sqrt(dx * dx + dy * dy)
        th = np.arctan2(dy, dx)
        cap_r, cone_r = 0.27 * R, 0.82 * R
        # Cone: shallow funnel, the surface normal tilts towards the centre.
        t = np.clip((rr - cap_r) / (cone_r - cap_r), 0, 1)
        nx, ny = -np.cos(th) * 0.55, -np.sin(th) * 0.55
        diffuse = np.clip(0.55 - (nx * lx + ny * ly) * 0.8, 0.15, 1.2)
        ribs = 1 + 0.07 * np.sin(t * 2 * np.pi * 7) * (1 - t)
        fibres = cv2.GaussianBlur(rng.normal(0, 1, (size, size)).astype(np.float32), (0, 0), 0.8) * 0.05
        col = np.array([30, 30, 33], np.float32)[None, None] * (diffuse * ribs * (0.85 + 0.3 * t) + fibres)[..., None]
        # Contact shadow around the dust cap (stays on the cone when the cap moves).
        col *= (1 - 0.5 * np.exp(-((rr - cap_r * 1.02) / (cap_r * 0.12)) ** 2))[..., None]
        cone = _premul(col, _smoothstep(cone_r + 1.5, cone_r - 1.5, rr))
        # Dust cap: glossy dome, separate layer.
        u = np.clip(rr / cap_r, 0, 1)
        h = np.sqrt(np.clip(1 - u * u, 0, 1))
        ndl = np.clip(-(dx / cap_r * lx + dy / cap_r * ly) * 0.8 + h * 0.6, 0, None)
        spec = np.clip(ndl - 0.85, 0, 1) ** 2 * 6
        cap_col = np.array([38, 38, 43], np.float32)[None, None] * (0.35 + ndl)[..., None] + (150 * spec)[..., None]
        cap = _premul(cap_col, _smoothstep(cap_r + 1.5, cap_r - 1.5, rr))
        return cone, cap

    @staticmethod
    def _draw_dome(size, R, lx, ly):
        c = size / 2
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
        dx, dy = (xx - c) / R, (yy - c) / R
        rr = np.sqrt(dx * dx + dy * dy)
        h = np.sqrt(np.clip(1 - rr * rr, 0, 1))
        ndl = np.clip(-(dx * lx + dy * ly) * 0.8 + h * 0.6, 0, None)
        spec = np.clip(ndl - 0.8, 0, 1) ** 2 * 8
        col = np.array([48, 48, 54], np.float32)[None, None] * (0.3 + ndl)[..., None] + (170 * spec)[..., None]
        return _premul(col, _smoothstep(1.0 + 1.5 / R, 1.0 - 1.5 / R, rr))

    # -- user supplied speaker picture ----------------------------------------
    def _from_image(self, image_path, height: int) -> None:
        img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise FileNotFoundError(f"Lautsprecher-Bild nicht lesbar: {image_path}")
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
        elif img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        scale = height / img.shape[0]
        img = cv2.resize(img, (max(1, int(img.shape[1] * scale)), height), interpolation=cv2.INTER_AREA)
        a = img[..., 3].astype(np.float32) / 255.0
        self.base_bgra = _premul(img[..., :3].astype(np.float32), a)
        h, w = self.base_bgra.shape[:2]
        cx, cy, cr = self.cfg["cone"]
        self.woofer = (cx * w, cy * h, cr * w / 0.82)
        self.cone = self._cut_disk(self.base_bgra, cx * w, cy * h, cr * w)
        tw = self.cfg.get("tweeter")
        if tw:
            self.tweet = (tw[0] * w, tw[1] * h, tw[2] * w / 0.72)
            self.dome = self._cut_disk(self.base_bgra, tw[0] * w, tw[1] * h, tw[2] * w)

    @staticmethod
    def _cut_disk(img, cx, cy, r):
        size = int(np.ceil(2 * r)) + 4
        x0, y0 = int(round(cx - size / 2)), int(round(cy - size / 2))
        out = np.zeros((size, size, 4), np.float32)
        _over(out, img, -x0, -y0)
        yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
        rr = np.sqrt((xx - (cx - x0)) ** 2 + (yy - (cy - y0)) ** 2)
        out *= _smoothstep(r + 1.0, r - 1.5, rr)[..., None]
        return out

    # -- per frame ------------------------------------------------------------
    def draw(self, frame: np.ndarray, x: int, y: int, cone: float, tweeter: float, kick: float) -> None:
        h, w = self.shape
        x0, y0, x1, y1 = _clip_box(frame.shape, w, h, x, y)
        if x1 <= x0 or y1 <= y0:
            return
        sl = (slice(y0 - y, y1 - y), slice(x0 - x, x1 - x))
        roi = frame[y0:y1, x0:x1].astype(np.float32)
        cv2.multiply(roi, self.base.inv[sl], dst=roi)
        cv2.add(roi, self.base.rgb[sl], dst=roi)
        ox, oy = x0 - x, y0 - y  # sprite coords -> roi coords

        cx, cy, _ = self.woofer
        cone = float(cone)
        lift = float(np.clip(1.0 + 0.45 * cone, 0.65, 1.6))
        for layer, gain in ((self.cone, 1.0), (self.cap, 1.9)):
            if layer is None:
                continue
            s = 1.0 + self.excursion * gain * cone
            size = max(4, int(round(layer.shape[0] * s)))
            scaled = cv2.resize(layer, (size, size), interpolation=cv2.INTER_LINEAR)
            scaled[..., :3] *= lift
            _over(roi, scaled, int(round(cx - size / 2)) - ox, int(round(cy - size / 2)) - oy)
        if self.dome is not None and self.tweet is not None:
            tx, ty, _ = self.tweet
            ts = 1.0 + 0.07 * float(tweeter)
            tsize = max(4, int(round(self.dome.shape[0] * ts)))
            d = cv2.resize(self.dome, (tsize, tsize), interpolation=cv2.INTER_LINEAR)
            _over(roi, d, int(round(tx - tsize / 2)) - ox, int(round(ty - tsize / 2)) - oy)
        if self.led_rgb is not None and self.cfg.get("glow", True):
            bx0, by0, bx1, by1 = self.led_box
            rx0, ry0 = max(bx0 - ox, 0), max(by0 - oy, 0)
            rx1, ry1 = min(bx1 - ox, roi.shape[1]), min(by1 - oy, roi.shape[0])
            if rx1 > rx0 and ry1 > ry0:
                led = self.led_rgb[ry0 + oy - by0:ry1 + oy - by0, rx0 + ox - bx0:rx1 + ox - bx0]
                sub = roi[ry0:ry1, rx0:rx1]
                cv2.scaleAdd(led, 0.18 + 0.95 * float(kick), sub, dst=sub)
        frame[y0:y1, x0:x1] = cv2.convertScaleAbs(roi)


class SpeakerOverlay:
    """All speakers of the video, positioned on the output frame."""

    def __init__(self, project: Project, width: int, height: int):
        cfg = project["speakers"]
        self.enabled = bool(cfg.get("enabled", True))
        self.items = []
        if not self.enabled:
            return
        sh = int(height * float(cfg["size"]))
        margin = int(height * float(cfg["margin"]))
        image = project.path(cfg.get("image"))
        colors = [hex_to_bgr(c) for c in (cfg.get("led_colors") or ["#00c8ff"])]
        for k, pos in enumerate(cfg.get("positions") or []):
            sprite = SpeakerSprite(sh, colors[k % len(colors)], cfg, image_path=image, rng_seed=k + 1)
            h, w = sprite.shape
            # Procedural sprites carry a shadow margin around the cabinet.
            pad = 0 if image else int(round(0.09 * w / 1.18))
            if isinstance(pos, (list, tuple)):
                x, y = int(pos[0] * width - w / 2), int(pos[1] * height - h / 2)
            else:
                if "left" in pos:
                    x = margin - pad
                elif "right" in pos:
                    x = width - margin - w + pad
                else:
                    x = (width - w) // 2
                y = height - margin - h + pad if "bottom" in pos else margin - pad
            self.items.append((sprite, x, y))

    def side_reserved(self, width: int) -> int:
        """Pixels covered by speakers at the left/right edge (for the title layout)."""
        reserved = 0
        for sprite, x, _ in self.items:
            w = sprite.shape[1]
            reserved = max(reserved, x + w if x + w / 2 < width / 2 else width - x)
        return reserved

    def draw(self, frame: np.ndarray, cone: float, tweeter: float, kick: float) -> None:
        for k, (sprite, x, y) in enumerate(self.items):
            # Left/right react very slightly differently, so it feels less mechanical.
            c = cone * (1.0 if k % 2 == 0 else 0.94)
            sprite.draw(frame, x, y, c, tweeter, kick)
