#!/usr/bin/env python3
"""
Party Megamix builder for Maestro clips (Eva & Techno Girls).

Step 1 (this script, normal Python):
  * scans the Maestro output folders for video clips (recursive)
  * scores every clip (sharpness, colour, exposure, faces, motion, Maestro prompt)
  * removes near-duplicates and sorts clips into "girls" and "landscape"
  * scans the music folder (latest singles + "Gebirgsrauschen"), detects tempo/beats
    and picks the most energetic section of every song
  * finds lipsync clips: clips that carry a song in their audio track (or reference it
    in Maestro metadata) are locked to the exact song position
  * writes plan.json + review.html (contact sheet with every chosen shot)
  * optional: --render renders a 1920x1080 preview MP4 with ffmpeg (no Resolve needed)

Step 2: megamix_resolve.py (run from DaVinci Resolve: Workspace > Scripts) reads
plan.json and builds the 1080p timeline in DaVinci Resolve.

Requirements: Python 3.9+, ffmpeg/ffprobe on PATH, `pip install numpy opencv-python`.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np

try:
    import cv2
except ImportError:  # pragma: no cover
    sys.exit("OpenCV fehlt: pip install opencv-python")

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
AUDIO_EXT = {".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg", ".aif", ".aiff"}

GIRL_WORDS = ["eva", "techno", "girl", "woman", "women", "dancer", "dancing", "singer",
              "vocalist", "model", "she ", "her ", "frau", "maedchen", "mädchen", "dj"]
LAND_WORDS = ["landscape", "mountain", "alps", "alpine", "gebirge", "berg", "lake", "see ",
              "forest", "wald", "valley", "tal", "river", "waterfall", "sunset", "sunrise",
              "clouds", "nebel", "fog", "glacier", "meadow", "wiese", "ocean", "beach",
              "aerial", "drone", "panorama", "sky", "snow", "gebirgsrauschen", "nature"]

SR = 22050          # analysis sample rate
HOP = 512           # onset hop -> ~43 frames/s
FPS_ENV = SR / HOP


# ----------------------------------------------------------------------------- utils
def run(cmd, **kw):
    # ffprobe prints UTF-8; Windows would otherwise decode with cp1252 and crash on umlauts
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def ffprobe(path: Path) -> dict:
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format",
             "-show_streams", str(path)])
    if r.returncode != 0:
        return {}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {}


def maestro_metadata(probe: dict, path: Path) -> dict:
    """Maestro/WanGP stores its generation settings as JSON in the 'comment' tag."""
    tags = {k.lower(): v for k, v in probe.get("format", {}).get("tags", {}).items()}
    for key in ("comment", "description"):
        if key in tags:
            try:
                return json.loads(tags[key])
            except (json.JSONDecodeError, TypeError):
                pass
    side = path.with_suffix(".json")
    if side.exists():
        try:
            return json.loads(side.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def decode_audio(path: Path, start: float = 0.0, dur: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "quiet", "-ss", f"{start:.3f}", "-i", str(path)]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    r = subprocess.run(cmd, capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def band_features(y: np.ndarray, n_bands: int = 24) -> np.ndarray:
    """Log energies in log-spaced frequency bands, ~43 frames/s -> (frames, bands).
    Carries melody/vocal information, so it locates a clip inside a song far more
    reliably than a pure rhythm envelope (techno beats repeat every bar)."""
    n_fft = 2048
    if len(y) < n_fft:
        return np.zeros((1, n_bands), dtype=np.float32)
    frames = 1 + (len(y) - n_fft) // HOP
    out = np.empty((frames, n_bands), dtype=np.float32)
    edges = np.unique(np.geomspace(3, n_fft // 2, n_bands + 1).astype(int))
    win = np.hanning(n_fft).astype(np.float32)
    for c0 in range(0, frames, 4096):                     # chunked: songs can be long
        c1 = min(frames, c0 + 4096)
        idx = np.arange(n_fft)[None, :] + HOP * np.arange(c0, c1)[:, None]
        spec = np.abs(np.fft.rfft(y[idx] * win, axis=1)) ** 2
        bands = np.add.reduceat(spec, edges[:-1], axis=1)
        out[c0:c1, : bands.shape[1]] = np.log10(bands + 1e-8)
    return out[:, : len(edges) - 1]


def onset_envelope(y: np.ndarray, feats: np.ndarray | None = None) -> np.ndarray:
    """Spectral-flux onset strength, ~43 values per second."""
    spec = band_features(y) if feats is None else feats
    if len(spec) < 2:
        return np.zeros(1, dtype=np.float32)
    flux = np.maximum(0, np.diff(spec, axis=0)).sum(axis=1)
    flux = np.concatenate([[0], flux])
    flux -= flux.mean()
    flux /= (flux.std() + 1e-9)
    return flux.astype(np.float32)


def rms_curve(y: np.ndarray, win_s: float = 1.0) -> np.ndarray:
    w = int(SR * win_s)
    if len(y) < w:
        return np.array([float(np.sqrt(np.mean(y ** 2) + 1e-12))])
    n = len(y) // w
    return np.sqrt((y[: n * w].reshape(n, w) ** 2).mean(axis=1))


def estimate_beats(env: np.ndarray, lo=110.0, hi=150.0):
    """Return (bpm, first_beat_time). Techno-friendly tempo window."""
    if len(env) < FPS_ENV * 8:
        return 128.0, 0.0
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    best, best_lag = -1e9, None
    for bpm in np.arange(lo, hi, 0.25):
        lag = FPS_ENV * 60.0 / bpm
        score = 0.0
        for k in (1, 2, 4):
            i = int(round(lag * k))
            if i < len(ac):
                score += ac[i] / k
        if score > best:
            best, best_lag = score, lag
    coarse = 60.0 * FPS_ENV / best_lag

    def grid_score(bpm):
        period = FPS_ENV * 60.0 / bpm
        best_sc, best_ph = -1e9, 0.0
        for ph in np.arange(0, period, 0.5):
            pos = np.arange(ph, len(env) - 1, period)
            i0 = pos.astype(int)
            fr = pos - i0
            v = env[i0] * (1 - fr) + env[i0 + 1] * fr          # sub-frame interpolation
            sc = v.mean()
            if sc > best_sc:
                best_sc, best_ph = sc, ph
        return best_sc, best_ph

    # fine search: over a whole track a 0.5 BPM error drifts by beats, so refine to 0.01
    cands = np.arange(coarse - 1.0, coarse + 1.0, 0.05)
    sc = [grid_score(b)[0] for b in cands]
    b0 = cands[int(np.argmax(sc))]
    cands = np.arange(b0 - 0.06, b0 + 0.06, 0.01)
    res = [grid_score(b) for b in cands]
    k = int(np.argmax([r[0] for r in res]))
    bpm, ph = float(cands[k]), res[k][1]
    return bpm, float(ph / FPS_ENV)


def norm(vals):
    a = np.asarray(vals, dtype=float)
    if len(a) == 0 or a.max() - a.min() < 1e-9:
        return np.full(len(a), 0.5)
    return (a - a.min()) / (a.max() - a.min())


# ----------------------------------------------------------------------------- clips
@dataclass
class Clip:
    path: str
    duration: float
    width: int
    height: int
    fps: float
    has_audio: bool
    prompt: str = ""
    audio_ref: str = ""
    audio_ref_start: float = 0.0
    sharp: float = 0.0
    color: float = 0.0
    expo: float = 0.0
    motion: float = 0.0
    faces: float = 0.0
    best_t: float = 0.0          # best starting point inside the clip
    dhash: str = ""
    kind: str = "girls"          # girls | landscape
    score: float = 0.0
    lipsync_song: str = ""       # song path the clip is locked to
    lipsync_offset: float = 0.0  # song time (s) that corresponds to clip t=0
    lipsync_conf: float = 0.0
    thumb: str = ""


_face = None


def face_detector():
    """Haar face detector; returns None if this OpenCV build has no cascades."""
    global _face
    if _face is None:
        try:
            _face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        except AttributeError:
            print("Hinweis: OpenCV ohne Gesichtserkennung (pip install 'opencv-python<5') - nutze nur Prompts/Dateinamen.")
            _face = False
    return _face


def dhash(img) -> str:
    g = cv2.cvtColor(cv2.resize(img, (9, 8)), cv2.COLOR_BGR2GRAY)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    return "".join("1" if b else "0" for b in bits)


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def analyze_clip(path: Path, thumbs: Path) -> Clip | None:
    probe = ffprobe(path)
    if not probe:
        return None
    vs = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
    if not vs:
        return None
    v = vs[0]
    dur = float(probe.get("format", {}).get("duration") or v.get("duration") or 0)
    if dur < 1.0:
        return None
    num, _, den = (v.get("r_frame_rate") or "25/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 25.0
    meta = maestro_metadata(probe, path)
    prompt = " ".join(str(meta.get(k, "")) for k in ("prompt", "video_prompt", "image_prompt"))
    audio_ref = ""
    for k in ("audio_guide", "audio_source", "audio_conditioning_guide"):
        if meta.get(k):
            audio_ref = str(meta[k])
            break
    c = Clip(path=str(path), duration=dur, width=int(v.get("width", 0)),
             height=int(v.get("height", 0)), fps=fps,
             has_audio=any(s.get("codec_type") == "audio" for s in probe.get("streams", [])),
             prompt=prompt.strip(), audio_ref=audio_ref,
             audio_ref_start=float(meta.get("audio_start_sec") or meta.get("multi_clip_audio_start_sec") or 0))

    cap = cv2.VideoCapture(str(path))
    samples = 8
    sharp, col, expo, faces, mot, per_t = [], [], [], [], [], []
    prev = None
    mid_img = None
    for i in range(samples):
        t = dur * (i + 0.5) / samples
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, img = cap.read()
        if not ok:
            continue
        small = cv2.resize(img, (480, int(480 * img.shape[0] / max(1, img.shape[1]))))
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        s = cv2.Laplacian(g, cv2.CV_64F).var()
        b, gg, r = [small[:, :, k].astype(float) for k in range(3)]
        rg, yb = np.abs(r - gg), np.abs(0.5 * (r + gg) - b)
        cf = math.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * math.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
        m = g.mean() / 255.0
        e = 1.0 - min(1.0, abs(m - 0.5) * 2.2)        # penalise too dark / too bright
        det = face_detector()
        fc = len(det.detectMultiScale(g, 1.15, 5, minSize=(30, 30))) if det else 0
        mo = float(np.abs(g.astype(float) - prev).mean()) if prev is not None and prev.shape == g.shape else 0.0
        prev = g.astype(float)
        sharp.append(s); col.append(cf); expo.append(e); faces.append(fc); mot.append(mo)
        per_t.append((t, s * (0.5 + e) * (1 + min(fc, 2) * 0.3)))
        if i == samples // 2:
            mid_img = img
    cap.release()
    if not sharp:
        return None
    c.sharp = float(np.median(sharp))
    c.color = float(np.mean(col))
    c.expo = float(np.mean(expo))
    c.faces = float(np.mean([min(f, 3) for f in faces]))
    c.motion = float(np.mean(mot[1:]) if len(mot) > 1 else 0)
    c.best_t = max(0.0, max(per_t, key=lambda x: x[1])[0] - 1.0)
    img = mid_img if mid_img is not None else img
    c.dhash = dhash(img)
    tp = thumbs / (hashlib.md5(str(path).encode()).hexdigest()[:12] + ".jpg")
    cv2.imwrite(str(tp), cv2.resize(img, (320, int(320 * img.shape[0] / max(1, img.shape[1])))))
    c.thumb = str(tp)

    text = (prompt + " " + path.as_posix()).lower()
    g_hits = sum(w in text for w in GIRL_WORDS)
    l_hits = sum(w in text for w in LAND_WORDS)
    if c.faces >= 0.25 or g_hits > l_hits:
        c.kind = "girls"
    elif l_hits > 0 or c.faces < 0.1:
        c.kind = "landscape"
    return c


def score_clips(clips: list[Clip], focus_words: list[str]):
    sh, co, mo = norm([math.log1p(c.sharp) for c in clips]), norm([c.color for c in clips]), norm([c.motion for c in clips])
    for i, c in enumerate(clips):
        res = min(1.0, (c.width * c.height) / (1920 * 1080))
        text = (c.prompt + " " + c.path).lower()
        focus = 0.15 * sum(w in text for w in focus_words)
        s = 0.32 * sh[i] + 0.22 * co[i] + 0.16 * c.expo + 0.12 * res + 0.10 * min(1, mo[i] * 1.5) + min(0.3, focus)
        if c.kind == "girls":
            s += 0.08 * min(1.0, c.faces)
        if c.lipsync_song:
            s += 0.25
        c.score = float(s)


def dedupe(clips: list[Clip], thr: int = 4) -> list[Clip]:
    keep: list[Clip] = []
    for c in sorted(clips, key=lambda c: -c.score):
        if all(hamming(c.dhash, k.dhash) > thr for k in keep):
            keep.append(c)
    return keep


# ----------------------------------------------------------------------------- songs
@dataclass
class Song:
    path: str
    title: str
    duration: float
    bpm: float = 128.0
    first_beat: float = 0.0
    mtime: float = 0.0
    seg_start: float = 0.0
    seg_end: float = 0.0
    tl_start: float = 0.0     # timeline position (s)
    energy: float = 0.0


def analyze_song(path: Path) -> Song | None:
    probe = ffprobe(path)
    dur = float(probe.get("format", {}).get("duration") or 0)
    if dur < 20:
        return None
    y = decode_audio(path)
    feats = band_features(y)
    env = onset_envelope(y, feats)
    bpm, fb = estimate_beats(env)
    rms = rms_curve(y)
    s = Song(path=str(path), title=path.stem, duration=dur, bpm=bpm, first_beat=fb,
             mtime=path.stat().st_mtime, energy=float(np.percentile(rms, 80)))
    s._rms = rms        # type: ignore[attr-defined]
    s._feats = feats    # type: ignore[attr-defined]
    return s


def pick_section(song: Song, length: float, locked=()):
    """Most energetic window, snapped to an 8-bar phrase grid.
    Windows that contain lipsync clips of this song get a big bonus."""
    beat = 60.0 / song.bpm
    phrase = beat * 32                                # 8 bars of 4/4
    length = max(phrase, round(length / phrase) * phrase) if length > phrase else length
    length = min(length, song.duration - 1)
    rms = getattr(song, "_rms", None)
    best, best_s = -1, song.first_beat
    s = song.first_beat
    while s + length <= song.duration - 0.5:
        a, b = int(s), int(min(len(rms), s + length)) if rms is not None else (0, 0)
        e = float(rms[a:b].mean()) if rms is not None and b > a else 0
        e *= 1.0 - 0.15 * (s / song.duration)        # slight preference for earlier drops
        cover = sum(max(0.0, min(s + length, b) - max(s, a)) for a, b in locked)
        e *= 1.0 + 0.08 * cover                        # +8 % per lipsync second
        if e > best:
            best, best_s = e, s
        s += phrase
    song.seg_start, song.seg_end = best_s, best_s + length


# ----------------------------------------------------------------------------- lipsync
def find_lipsync(clips: list[Clip], songs: list[Song], min_conf: float):
    """Correlate each clip's own audio track against every song -> exact song offset."""
    def zn(f):
        f = f - f.mean(axis=0, keepdims=True)
        return f / (f.std(axis=0, keepdims=True) + 1e-6)
    song_f = {s.path: zn(s._feats) for s in songs}      # type: ignore[attr-defined]
    by_stem = {Path(s.path).stem.lower(): s for s in songs}
    for c in clips:
        # fast path: Maestro metadata names the song
        if c.audio_ref:
            stem = Path(c.audio_ref.replace("\\", "/")).stem.lower()
            for k, s in by_stem.items():
                if stem and (stem in k or k in stem):
                    c.lipsync_song, c.lipsync_offset, c.lipsync_conf = s.path, c.audio_ref_start, 0.9
                    break
        if not c.has_audio:
            continue
        y = decode_audio(Path(c.path))
        if len(y) < SR * 2 or float(np.abs(y).mean()) < 1e-4:
            continue
        cf = band_features(y)
        cf = cf - cf.mean(axis=0, keepdims=True)
        L = len(cf)
        best = (0.0, None, 0.0, 0.0)
        for s in songs:
            sf = song_f[s.path]
            if len(sf) <= L:
                continue
            n = 1 << int(math.ceil(math.log2(len(sf) + L)))
            corr = np.zeros(len(sf) - L + 1)
            num_sq = np.zeros(len(sf) - L + 1)
            for b in range(sf.shape[1]):                    # sum of per-band correlations
                a_, c_ = sf[:, b], cf[:, b]
                corr += np.fft.irfft(np.fft.rfft(a_, n) * np.conj(np.fft.rfft(c_, n)), n)[: len(corr)]
                cs = np.cumsum(np.concatenate([[0], a_])); cs2 = np.cumsum(np.concatenate([[0], a_ ** 2]))
                win_sum, win_sq = cs[L:] - cs[:-L], cs2[L:] - cs2[:-L]
                num_sq += np.maximum(win_sq - win_sum ** 2 / L, 1e-9)[: len(corr)]
            ncc = corr / (np.sqrt(num_sq) * (np.linalg.norm(cf) + 1e-9))
            i = int(np.argmax(ncc))
            # ambiguity check: 2nd best peak at least 2 s away (repeated chorus)
            mask = np.ones(len(ncc), bool); mask[max(0, i - int(2 * FPS_ENV)): i + int(2 * FPS_ENV)] = False
            second = float(ncc[mask].max()) if mask.any() else 0.0
            if ncc[i] > best[0]:
                best = (float(ncc[i]), s, i / FPS_ENV, second)
        if best[1] is not None and best[0] >= min_conf and best[0] > c.lipsync_conf:
            c.lipsync_song, c.lipsync_offset, c.lipsync_conf = best[1].path, best[2], best[0]
            if best[3] > best[0] - 0.05:
                print(f"  Achtung: {Path(c.path).name} passt an mehreren Stellen von "
                      f"{Path(best[1].path).name} (Refrain?) - bitte in Resolve pruefen.")


# ----------------------------------------------------------------------------- plan
def build_plan(clips, songs, minutes, landscape_every, rng):
    total = minutes * 60.0
    n = len(songs)
    per = total / n
    xfade = 0.0
    t = 0.0
    shots = []
    girls = [c for c in clips if c.kind == "girls"]
    lands = [c for c in clips if c.kind == "landscape"]
    usage: dict[str, int] = {}

    def take(pool, need):
        pool = [c for c in pool if c.duration >= min(need, 1.5)]
        if not pool:
            return None
        pool.sort(key=lambda c: (usage.get(c.path, 0), -c.score + rng.random() * 0.15))
        c = pool[0]
        usage[c.path] = usage.get(c.path, 0) + 1
        return c

    for si, s in enumerate(songs):
        pick_section(s, per, [(c.lipsync_offset, c.lipsync_offset + c.duration)
                              for c in clips if c.lipsync_song == s.path])
        if si == n - 1:   # last song fills to exactly the target length
            s.seg_end = min(s.duration - 0.2, s.seg_start + (total - t))
        s.tl_start = t
        seg_len = s.seg_end - s.seg_start
        beat = 60.0 / s.bpm
        # lipsync windows for this song
        locked = []
        for c in clips:
            if c.lipsync_song != s.path:
                continue
            a = max(s.seg_start, c.lipsync_offset)
            b = min(s.seg_end, c.lipsync_offset + c.duration)
            if b - a >= 2 * beat:
                locked.append((a, b, c))
        locked.sort(key=lambda x: (x[0], -x[2].score))
        occupied = []
        for a, b, c in locked:
            if any(not (b <= oa or a >= ob) for oa, ob in occupied):
                continue
            occupied.append((a, b))
            shots.append(dict(kind="lipsync", clip=c.path, src_in=a - c.lipsync_offset,
                              src_out=b - c.lipsync_offset, tl_in=t + (a - s.seg_start),
                              tl_out=t + (b - s.seg_start), song=s.title))
            usage[c.path] = usage.get(c.path, 0) + 1
        # beat-cut B-roll for the rest
        pos = s.seg_start
        shot_no = 0
        grid0 = s.first_beat + math.ceil((pos - s.first_beat) / beat) * beat if pos > s.first_beat else pos
        while pos < s.seg_end - 0.05:
            nxt_lock = min([oa for oa, ob in occupied if oa >= pos - 1e-6] + [s.seg_end])
            inside = [ob for oa, ob in occupied if oa - 1e-6 <= pos < ob]
            if inside:
                pos = max(inside)
                continue
            bars = rng.choice([1, 2, 2, 2, 4]) if seg_len > 30 else 2
            length = bars * 4 * beat
            end = min(pos + length, nxt_lock, s.seg_end)
            if end - pos < beat * 0.9 and end < s.seg_end:
                pos = end
                continue
            shot_no += 1
            pool = lands if (landscape_every and shot_no % landscape_every == 0 and lands) else girls or lands
            c = take(pool, end - pos) or take(clips, end - pos)
            if c is None:
                break
            need = end - pos
            src_in = c.best_t if c.best_t + need <= c.duration else max(0.0, c.duration - need)
            src_out = min(c.duration, src_in + need)
            shots.append(dict(kind=c.kind, clip=c.path, src_in=src_in, src_out=src_out,
                              tl_in=t + (pos - s.seg_start), tl_out=t + (pos - s.seg_start) + (src_out - src_in),
                              song=s.title))
            pos = end
        t += seg_len - xfade
    shots.sort(key=lambda x: x["tl_in"])
    return shots, t


# ----------------------------------------------------------------------------- outputs
def write_review(out: Path, clips, songs, shots):
    by = {c.path: c for c in clips}
    rows = []
    for s in songs:
        cells = []
        for sh in shots:
            if sh["song"] != s.title:
                continue
            c = by[sh["clip"]]
            rel = os.path.relpath(c.thumb, out).replace("\\", "/")
            badge = {"lipsync": "LIPSYNC", "landscape": "LANDSCHAFT"}.get(sh["kind"], "GIRLS")
            cells.append(f'<figure class="{sh["kind"]}"><img src="{html.escape(rel)}" loading="lazy">'
                         f'<figcaption>{badge} · {sh["tl_in"]/60:.0f}:{sh["tl_in"]%60:04.1f} · '
                         f'{html.escape(Path(c.path).name)}</figcaption></figure>')
        rows.append(f'<section><h2>{html.escape(s.title)} <small>{s.bpm:.1f} BPM · '
                    f'{s.seg_start:.0f}s–{s.seg_end:.0f}s · ab {s.tl_start/60:.0f}:{s.tl_start%60:02.0f}</small></h2>'
                    f'<div class="grid">{"".join(cells)}</div></section>')
    (out / "review.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Megamix Review</title>
<style>body{{background:#111;color:#eee;font:14px system-ui;margin:16px}}h2 small{{color:#999;font-weight:400}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}}
figure{{margin:0;border:2px solid #333;border-radius:6px;overflow:hidden}}figure img{{width:100%;display:block}}
figure.lipsync{{border-color:#e0f}}figure.landscape{{border-color:#2a8}}figcaption{{font-size:11px;padding:4px;color:#bbb;word-break:break-all}}</style>
<h1>Party Megamix – Eva &amp; Techno Girls</h1><p>{len(shots)} Schnitte · {len(songs)} Songs · lila = Lipsync, grün = Landschaft</p>
{''.join(rows)}""", encoding="utf-8")


def render_preview(out: Path, songs, shots, total, width=1920, height=1080, fps=30, crossfade=2.0):
    """ffmpeg-only 1080p render (fallback / preview without DaVinci)."""
    tmp = Path(tempfile.mkdtemp(prefix="megamix_", dir=out))
    vf = (f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},"
          f"fps={fps},format=yuv420p,setsar=1")
    parts = []
    for i, sh in enumerate(shots):
        p = tmp / f"v{i:05d}.mp4"
        d = sh["tl_out"] - sh["tl_in"]
        r = run(["ffmpeg", "-y", "-v", "error", "-ss", f"{sh['src_in']:.3f}", "-i", sh["clip"], "-t", f"{d:.3f}",
                 "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(p)])
        if r.returncode == 0:
            parts.append((sh["tl_in"], p, d))
        print(f"\r  Video-Schnitt {i+1}/{len(shots)}", end="", flush=True)
    print()
    # fill gaps with black so audio stays in sync
    lst = tmp / "list.txt"
    cur = 0.0
    with lst.open("w") as f:
        for tl_in, p, d in parts:
            if tl_in > cur + 0.02:
                gp = tmp / f"gap{int(cur*1000)}.mp4"
                run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=black:s={width}x{height}:r={fps}",
                     "-t", f"{tl_in-cur:.3f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(gp)])
                f.write(f"file '{gp.as_posix()}'\n")
            f.write(f"file '{p.as_posix()}'\n")
            cur = max(cur, tl_in + d)
    video = tmp / "video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    # audio: song sections, consecutive ones overlapped by a short crossfade at the seam
    inputs, filt, labels = [], [], []
    for i, s in enumerate(songs):
        inputs += ["-ss", f"{s.seg_start:.3f}", "-t", f"{s.seg_end - s.seg_start + crossfade:.3f}", "-i", s.path]
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,"
                    f"afade=t=out:st={s.seg_end - s.seg_start:.3f}:d={crossfade},"
                    f"adelay={int(s.tl_start*1000)}|{int(s.tl_start*1000)}[a{i}]")
        labels.append(f"[a{i}]")
    filt.append(f"{''.join(labels)}amix=inputs={len(songs)}:normalize=0,alimiter=limit=0.95,"
                f"atrim=0:{total:.3f}[aout]")
    audio = tmp / "audio.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[aout]", str(audio)])
    final = out / "Party_Megamix_Eva_Technogirls_1080p.mp4"
    r = run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", str(final)])
    if r.returncode != 0:
        print(r.stderr)
    shutil.rmtree(tmp, ignore_errors=True)
    return final


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clips", nargs="+", required=True, help="Maestro-Ordner mit Clips (z.B. Maestro/app/outputs)")
    ap.add_argument("--music", nargs="+", required=True, help="Ordner/Dateien mit den Single-WAVs")
    ap.add_argument("--out", default="megamix_out")
    ap.add_argument("--minutes", type=float, default=30)
    ap.add_argument("--songs", type=int, default=25, help="Anzahl Songs (20-30)")
    ap.add_argument("--must", nargs="*", default=["gebirgsrauschen"], help="Songs die sicher rein muessen (Teil des Namens)")
    ap.add_argument("--focus", nargs="*", default=["eva", "techno"], help="Bevorzugte Begriffe in Prompt/Dateiname")
    ap.add_argument("--max-clips", type=int, default=400, help="beste N Clips nach Bewertung behalten")
    ap.add_argument("--landscape-every", type=int, default=4, help="jeder N-te Schnitt eine Landschaft (0=aus)")
    ap.add_argument("--lipsync-conf", type=float, default=0.55, help="Mindest-Korrelation fuer Lipsync-Erkennung")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--render", action="store_true", help="zusaetzlich 1080p-MP4 mit ffmpeg rendern")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg/ffprobe nicht gefunden (PATH).")
    out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    thumbs = out / "thumbs"; thumbs.mkdir(exist_ok=True)
    rng = random.Random(a.seed)

    vids = sorted({p.resolve() for d in a.clips for p in Path(d).rglob("*")
                   if p.suffix.lower() in VIDEO_EXT and "trash" not in p.as_posix().lower()})
    auds = []
    for d in a.music:
        p = Path(d)
        auds += [p] if p.is_file() else [q for q in p.rglob("*") if q.suffix.lower() in AUDIO_EXT]
    print(f"{len(vids)} Videoclips, {len(auds)} Audiodateien gefunden.")
    if not vids or not auds:
        sys.exit("Keine Clips oder keine Musik gefunden – Pfade pruefen.")

    print("Analysiere Songs (Tempo/Beats/Energie)...")
    songs = [s for s in (analyze_song(p) for p in auds) if s]
    seen, uniq = set(), []
    for s in sorted(songs, key=lambda s: -s.mtime):          # neueste Singles zuerst
        key = re.sub(r"([\s_\-]*(\(.*?\)|final|master|v\d+))+$", "", s.title.lower())
        if key not in seen:
            seen.add(key); uniq.append(s)
    must = [s for s in uniq if any(m.lower() in s.title.lower() for m in a.must)]
    rest = [s for s in uniq if s not in must]
    chosen = (must + rest)[: max(1, a.songs)]
    if len(chosen) < a.songs:
        print(f"Hinweis: nur {len(chosen)} verschiedene Songs vorhanden.")
    # DJ order: sort by tempo, put Gebirgsrauschen as the finale
    finale = [s for s in chosen if any(m.lower() in s.title.lower() for m in a.must)][:1]
    order = sorted([s for s in chosen if s not in finale], key=lambda s: s.bpm) + finale
    for s in order:
        print(f"  {s.title:40s} {s.bpm:6.1f} BPM  {s.duration/60:4.1f} min")

    print("Analysiere Clips (Schaerfe, Farbe, Gesichter, Bewegung)...")
    clips = []
    for i, p in enumerate(vids):
        c = analyze_clip(p, thumbs)
        if c:
            clips.append(c)
        print(f"\r  {i+1}/{len(vids)}", end="", flush=True)
    print()
    print("Suche Lipsync-Clips (Audio-Korrelation)...")
    find_lipsync(clips, order, a.lipsync_conf)
    score_clips(clips, a.focus)
    clips = dedupe(clips)[: a.max_clips]
    print(f"  {sum(c.kind=='girls' for c in clips)} Girls-Clips, {sum(c.kind=='landscape' for c in clips)} Landschaften, "
          f"{sum(bool(c.lipsync_song) for c in clips)} Lipsync-Clips")

    shots, total = build_plan(clips, order, a.minutes, a.landscape_every, rng)
    plan = dict(width=1920, height=1080, fps=30, total_seconds=total,
                songs=[asdict(s) for s in order],
                shots=shots, clips=[asdict(c) for c in clips if any(sh["clip"] == c.path for sh in shots)])
    (out / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    write_review(out, clips, order, shots)
    print(f"Plan: {len(shots)} Schnitte, {total/60:.1f} min -> {out/'plan.json'}")
    print(f"Vorschau der Auswahl: {out/'review.html'}")
    if a.render:
        print("Rendere 1080p-MP4 mit ffmpeg...")
        print("Fertig:", render_preview(out, order, shots, total))


if __name__ == "__main__":
    main()
