"""Playlist mixing (ffmpeg) and music analysis (numpy only).

The analysis produces everything the video side needs, one value per output
frame: the speaker-cone excursion (a damped spring driven by the kick/bass),
tweeter excitation (hi-hats), kick intensity, plus a beat/bar/phrase grid
that the montage planner cuts on.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import ffmpeg_tools as ff
from .config import Project, Song

ANALYSIS_SR = 22050
ENV_HOP = 105  # 210 envelope samples per second
ANALYSIS_VERSION = 4


# ── playlist & mix ──────────────────────────────────────────────────────────

@dataclass
class TimelineEntry:
    index: int          # position in the played playlist (0-based)
    number: int         # track number shown on screen (1-based, unique songs)
    count: int          # number of unique songs
    path: str
    title: str
    artist: str
    start: float        # seconds in the final mix
    end: float
    gain_db: float

    @property
    def display(self) -> str:
        return f"{self.artist} – {self.title}" if self.artist else self.title


@dataclass
class MixResult:
    path: Path
    duration: float
    timeline: list[TimelineEntry] = field(default_factory=list)


def _song_stats(song: Song, cache_dir: Path) -> dict:
    """Exact decoded duration + integrated loudness (cached per file)."""
    stat = song.path.stat()
    key = hashlib.sha1(f"{song.path}|{stat.st_size}|{stat.st_mtime_ns}".encode()).hexdigest()[:16]
    cache_file = cache_dir / "songs" / f"{key}.json"
    if cache_file.is_file():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    proc = subprocess.run(
        [ff.ffmpeg(), "-hide_banner", "-nostats", "-i", str(song.path), "-vn",
         "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    text = proc.stderr.decode("utf-8", "replace")
    if proc.returncode != 0:
        raise ff.FFmpegError(f"Song kann nicht gelesen werden: {song.path}\n{text[-800:]}")
    match = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", text, re.S)
    loudness = float(json.loads(match.group(0))["input_i"]) if match else -14.0
    if not np.isfinite(loudness) or loudness < -70:
        loudness = -14.0
    info = ff.probe(song.path)
    stats = {"duration": float(info.get("duration") or 0.0), "lufs": loudness, "tags": info.get("tags", {})}
    if stats["duration"] <= 0:
        raise ff.FFmpegError(f"Song hat keine Länge: {song.path}")
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(stats), encoding="utf-8")
    return stats


def plan_playlist(project: Project, songs: list[Song], stats: list[dict]) -> list[int]:
    """Song order (indices). Repeats the list until the minimum length is reached."""
    acfg = project["audio"]
    xf = float(acfg["crossfade_seconds"])
    target = float(acfg.get("duration_minutes") or 0) * 60.0
    rng = random.Random(project["seed"])
    base = list(range(len(songs)))
    if acfg.get("shuffle"):
        rng.shuffle(base)
    order = list(base)
    total = sum(stats[i]["duration"] for i in order) - xf * (len(order) - 1)
    while target and total < target:
        cycle = list(base)
        if acfg.get("shuffle") or len(cycle) > 2:
            rng.shuffle(cycle)
            if len(cycle) > 1 and cycle[0] == order[-1]:
                cycle.append(cycle.pop(0))
        for i in cycle:
            order.append(i)
            total += stats[i]["duration"] - xf
            if total >= target:
                break
    return order


def build_mix(project: Project) -> MixResult:
    acfg = project["audio"]
    cache = project.cache_dir
    cache.mkdir(parents=True, exist_ok=True)
    songs = project.songs()
    print(f"Analysiere {len(songs)} Songs (Lautheit/Länge) …")
    stats = [_song_stats(song, cache) for song in songs]
    for song, st in zip(songs, stats):
        tags = st.get("tags") or {}
        if not song.explicit and tags.get("title"):
            song.title = tags["title"].strip()
            song.artist = (tags.get("artist") or song.artist).strip()

    order = plan_playlist(project, songs, stats)
    xf = max(0.0, float(acfg["crossfade_seconds"]))
    xf = min(xf, 0.45 * min(stats[i]["duration"] for i in order))
    target_lufs = float(acfg["target_lufs"])

    timeline: list[TimelineEntry] = []
    t = 0.0
    for pos, i in enumerate(order):
        dur = stats[i]["duration"]
        gain = max(-20.0, min(12.0, target_lufs - stats[i]["lufs"]))
        timeline.append(TimelineEntry(
            index=pos, number=i + 1, count=len(songs), path=str(songs[i].path),
            title=songs[i].title, artist=songs[i].artist, start=t, end=t + dur, gain_db=gain,
        ))
        t += dur - xf
    natural = timeline[-1].end
    target = float(acfg.get("duration_minutes") or 0) * 60.0
    total = natural
    if target and len(order) > len(songs) and natural > target:
        last = timeline[-1]
        if natural - target > 0.5 * (last.end - last.start):
            # Rather end a bit early on a complete song than on a short fragment.
            timeline.pop()
            total = timeline[-1].end
        else:
            total = target
    for entry in timeline:
        entry.end = min(entry.end, total)
    timeline = [e for e in timeline if e.start < total - 1.0]

    sr = int(acfg["sample_rate"])
    signature = hashlib.sha1(json.dumps(
        [[e.path, round(e.gain_db, 2)] for e in timeline] + [xf, total, sr, acfg["true_peak"], acfg["end_fade_seconds"]]
    ).encode()).hexdigest()[:12]
    mix_path = cache / f"mix_{signature}.flac"
    if not mix_path.is_file():
        print(f"Mische {len(timeline)} Tracks ({total / 60:.1f} min, Crossfade {xf:.1f}s, Ziel {target_lufs} LUFS) …")
        args = [ff.ffmpeg(), "-hide_banner", "-y", "-loglevel", "error"]
        for entry in timeline:
            args += ["-i", entry.path]
        parts = []
        for k, entry in enumerate(timeline):
            parts.append(
                f"[{k}:a]aresample={sr},aformat=sample_fmts=fltp:channel_layouts=stereo,"
                f"volume={entry.gain_db:.2f}dB[a{k}]"
            )
        last = "a0"
        for k in range(1, len(timeline)):
            out = f"x{k}"
            parts.append(f"[{last}][a{k}]acrossfade=d={xf:.3f}:c1=tri:c2=tri[{out}]")
            last = out
        peak = 10 ** (float(acfg["true_peak"]) / 20.0)
        fade = min(float(acfg["end_fade_seconds"]), total / 4)
        parts.append(
            f"[{last}]alimiter=limit={peak:.4f}:level=0,atrim=0:{total:.3f},"
            f"afade=t=out:st={max(0.0, total - fade):.3f}:d={fade:.3f}[out]"
        )
        args += ["-filter_complex", ";".join(parts), "-map", "[out]", "-c:a", "flac",
                 "-sample_fmt", "s16", str(mix_path.with_suffix(".tmp.flac"))]
        ff.run(args)
        mix_path.with_suffix(".tmp.flac").replace(mix_path)
    duration = float(ff.probe(mix_path).get("duration") or total)
    (cache / "timeline.json").write_text(
        json.dumps([e.__dict__ for e in timeline], indent=2, ensure_ascii=False), encoding="utf-8",
    )
    return MixResult(mix_path, duration, timeline)


# ── analysis ────────────────────────────────────────────────────────────────

@dataclass
class Analysis:
    fps: float
    n_frames: int
    cone: np.ndarray       # spring excursion per frame (≈ -0.4 … 1.3)
    tweeter: np.ndarray    # 0 … 1
    kick: np.ndarray       # 0 … 1 (bass drive before the spring)
    beats: np.ndarray      # beat times (s)
    beat_bar: np.ndarray   # bool: first beat of a bar
    beat_phrase: np.ndarray  # bool: first beat of a 16-beat phrase
    beat_level: np.ndarray   # section energy relative to the song (≈ 0.3 … 1.3)
    bpm: list = field(default_factory=list)

    def save(self, path: Path) -> None:
        np.savez_compressed(
            path, fps=self.fps, n_frames=self.n_frames, cone=self.cone, tweeter=self.tweeter,
            kick=self.kick, beats=self.beats, beat_bar=self.beat_bar, beat_phrase=self.beat_phrase,
            beat_level=self.beat_level, bpm=np.array(self.bpm, dtype=np.float64),
        )

    @classmethod
    def load(cls, path: Path) -> "Analysis":
        d = np.load(path)
        return cls(float(d["fps"]), int(d["n_frames"]), d["cone"], d["tweeter"], d["kick"], d["beats"],
                   d["beat_bar"], d["beat_phrase"], d["beat_level"], list(d["bpm"]))


def _decode_mono(path: Path, sr: int = ANALYSIS_SR) -> np.ndarray:
    proc = ff.run([ff.ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(path),
                   "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(proc.stdout, dtype=np.float32)


def band_envelope(x: np.ndarray, sr: int, lo: float, hi: float, hop: int = ENV_HOP) -> np.ndarray:
    """RMS envelope of a band-passed signal (chunked FFT filter, numpy only)."""
    chunk, pad = 1 << 20, 8192
    n_env = len(x) // hop
    env = np.empty(n_env, dtype=np.float32)
    pos = 0
    filled = 0
    while filled < n_env:
        a = max(0, pos - pad)
        b = min(len(x), pos + chunk + pad)
        seg = x[a:b].astype(np.float64)
        spec = np.fft.rfft(seg)
        freqs = np.fft.rfftfreq(len(seg), 1.0 / sr)
        # Smooth (raised-cosine) band edges avoid ringing.
        w = np.ones_like(freqs)
        lo_w, hi_w = lo * 0.25, hi * 0.15
        w[freqs < lo - lo_w] = 0
        m = (freqs >= lo - lo_w) & (freqs < lo)
        w[m] = 0.5 - 0.5 * np.cos(np.pi * (freqs[m] - (lo - lo_w)) / lo_w)
        w[freqs > hi + hi_w] = 0
        m = (freqs > hi) & (freqs <= hi + hi_w)
        w[m] = 0.5 + 0.5 * np.cos(np.pi * (freqs[m] - hi) / hi_w)
        y = np.fft.irfft(spec * w, n=len(seg))[pos - a: pos - a + chunk]
        k = min(len(y) // hop, n_env - filled)
        if k <= 0:
            break
        env[filled:filled + k] = np.sqrt(np.mean(y[: k * hop].reshape(k, hop) ** 2, axis=1))
        filled += k
        pos += k * hop
    return env[:filled]


def _smooth(x: np.ndarray, k: int) -> np.ndarray:
    """Moving average that keeps the input length (also for very short inputs)."""
    k = max(1, min(int(k), len(x)))
    return np.convolve(x, np.ones(k) / k, mode="same")


def onset_envelope(bass_env: np.ndarray) -> np.ndarray:
    """Kick onsets: positive slope of the log-compressed bass envelope.

    log1p with a reference level keeps near-silent passages from turning
    into large, noisy log differences.
    """
    env = bass_env.astype(np.float64)
    ref = np.percentile(env, 95) + 1e-9
    lb = np.log1p(20.0 * env / ref)
    onset = np.clip(np.diff(lb, prepend=lb[0]), 0, None)
    return np.convolve(onset, np.hanning(5) / np.hanning(5).sum(), mode="same")


def _comb_beats(onset: np.ndarray, rate: float, bpm_lo=100.0, bpm_hi=180.0) -> tuple[float, float, float]:
    """Fixed-tempo beat grid: returns (period_samples, phase_samples, bpm)."""
    o = onset - onset.mean()
    n = len(o)
    if n < rate * 8:
        bpm = 128.0
        return 60 * rate / bpm, 0.0, bpm
    spec = np.fft.rfft(o, 2 * n)
    ac = np.fft.irfft(spec * np.conj(spec))[:n]
    bpms = np.arange(bpm_lo, bpm_hi, 0.25)
    lags = 60 * rate / bpms
    vals = np.interp(lags, np.arange(n), ac)
    prior = np.exp(-0.5 * (np.log2(bpms / 128.0) / 0.4) ** 2)
    coarse = bpms[int(np.argmax(vals * prior))]
    # Fine search of tempo and phase on the comb.
    best = (-np.inf, 0.0, 0.0)
    k = np.arange(int(n / (60 * rate / (coarse + 2))) + 1)
    for bpm in np.arange(coarse - 1.0, coarse + 1.0001, 0.02):
        period = 60 * rate / bpm
        phases = np.arange(0, period, 1.0)
        pos = phases[:, None] + k[None, :] * period
        valid = pos < n - 1
        idx = np.clip(pos.astype(np.int64), 0, n - 1)
        score = (onset[idx] * valid).sum(axis=1) / np.maximum(valid.sum(axis=1), 1)
        j = int(np.argmax(score))
        if score[j] > best[0]:
            best = (score[j], period, phases[j])
    _, period, phase = best
    return period, phase, 60 * rate / period


def analyze(project: Project, mix: MixResult) -> Analysis:
    fps = float(project["video"]["fps"])
    st = mix.path.stat()
    key = hashlib.sha1(f"{mix.path.name}|{st.st_size}|{fps}|{ANALYSIS_VERSION}|"
                       f"{json.dumps(project['speakers'], sort_keys=True)}".encode()).hexdigest()[:12]
    cache_file = project.cache_dir / f"analyse_{key}.npz"
    if cache_file.is_file():
        return Analysis.load(cache_file)
    print("Analysiere Beats und Bass …")
    x = _decode_mono(mix.path)
    rate = ANALYSIS_SR / ENV_HOP
    bass = band_envelope(x, ANALYSIS_SR, 35, 130)
    highs = band_envelope(x, ANALYSIS_SR, 5000, 10500)
    full = band_envelope(x, ANALYSIS_SR, 30, 10500)
    del x
    n_env = min(len(bass), len(highs), len(full))
    bass, highs, full = bass[:n_env], highs[:n_env], full[:n_env]

    drive = np.zeros(n_env, dtype=np.float64)
    tweet = np.zeros(n_env, dtype=np.float64)
    beats, bars, phrases, levels, bpms = [], [], [], [], []
    timeline = mix.timeline
    for i, entry in enumerate(timeline):
        own_a = entry.start + (0.5 * (timeline[i - 1].end - entry.start) if i > 0 else 0.0)
        own_b = entry.end - (0.5 * (entry.end - timeline[i + 1].start) if i + 1 < len(timeline) else 0.0)
        a, b = int(own_a * rate), min(n_env, int(own_b * rate))
        if b - a < rate:
            continue
        # Per-song normalisation so quiet and loud tracks both move the cones.
        seg = bass[a:b].astype(np.float64)
        ref = np.percentile(seg, 98) + 1e-9
        v = np.clip(seg / ref, 0, 1.25) ** 1.6
        gate = 0.22
        drive[a:b] = np.clip((v - gate) / (1 - gate), 0, None)
        hs = highs[a:b].astype(np.float64)
        tweet[a:b] = np.clip(hs / (np.percentile(hs, 97) + 1e-9), 0, 1.2) ** 1.3

        # Beat grid from the kick onsets of the song (analyse the whole song, keep the owned part).
        sa, sb = int(entry.start * rate), min(n_env, int(entry.end * rate))
        period, phase, bpm = _comb_beats(onset_envelope(bass[sa:sb]), rate)
        bpms.append(round(float(bpm), 2))
        times = entry.start + (phase + np.arange(0, (sb - sa - phase) / period) * period) / rate
        # Phrase offset: beat where the energy changes most often (drops / breakdowns).
        fidx = np.clip(((times - entry.start) * rate).astype(int) + sa, 0, n_env - 1)
        energy = full[fidx].astype(np.float64)
        if len(energy) >= 48:
            sm = _smooth(energy, 4)
            nov = np.zeros_like(sm)
            for kk in range(8, len(sm) - 8):
                nov[kk] = abs(sm[kk:kk + 8].mean() - sm[kk - 8:kk].mean())
            offset = int(np.argmax([nov[m::16].sum() for m in range(16)]))
        else:
            offset = 0
        smooth = _smooth(energy, 16)
        level = smooth / (np.median(smooth) + 1e-9)
        rel = np.arange(len(times)) - offset
        keep = (times >= own_a) & (times < own_b)
        beats.append(times[keep])
        bars.append((rel % 4 == 0)[keep])
        phrases.append((rel % 16 == 0)[keep])
        levels.append(level[keep])

    # Damped spring = speaker cone. Semi-implicit Euler at the envelope rate.
    scfg = project["speakers"]
    w = 2 * np.pi * float(scfg["spring_hz"])
    zeta = float(scfg["damping"])
    dt = 1.0 / rate
    cone = np.zeros(n_env)
    xpos = vel = 0.0
    for k in range(n_env):
        acc = w * w * (drive[k] - xpos) - 2 * zeta * w * vel
        vel += acc * dt
        xpos += vel * dt
        cone[k] = xpos
    tweet = np.convolve(tweet, np.ones(3) / 3, mode="same")

    n_frames = int(mix.duration * fps)
    sample = np.clip((np.arange(n_frames) / fps * rate).astype(int), 0, n_env - 1)
    concat = (lambda parts, dt_: np.concatenate(parts).astype(dt_) if parts else np.zeros(0, dt_))
    result = Analysis(
        fps=fps, n_frames=n_frames,
        cone=cone[sample].astype(np.float32), tweeter=np.clip(tweet[sample], 0, 1).astype(np.float32),
        kick=np.clip(drive[sample], 0, 1).astype(np.float32),
        beats=concat(beats, np.float64), beat_bar=concat(bars, bool),
        beat_phrase=concat(phrases, bool), beat_level=concat(levels, np.float32), bpm=bpms,
    )
    result.save(cache_file)
    print("  Tempi: " + ", ".join(f"{b:.0f}" for b in bpms) + " BPM")
    return result
