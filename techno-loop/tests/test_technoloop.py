"""Tests: python -m unittest discover -s tests   (from the techno-loop folder)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from technoloop import audio, demo, ffmpeg_tools as ff, maestro, montage  # noqa: E402
from technoloop.config import load_project, parse_song_name  # noqa: E402

HAVE_FFMPEG = shutil.which("ffmpeg") is not None


class Basics(unittest.TestCase):
    def test_snap_frames(self):
        self.assertEqual(maestro.snap_frames(175), 175)
        self.assertEqual(maestro.snap_frames(180), 175)
        self.assertEqual(maestro.snap_frames(10), 124)
        self.assertEqual(maestro.snap_frames(999), 345)
        for n in (124, 141, 243, 345):
            self.assertEqual((maestro.snap_frames(n) - 5) % 17, 0)

    def test_preset_with_turbo_checkbox_keeps_its_steps(self):
        mcfg = {"steps": 4, "turbo": True, "turbo_lora": "minimax_h3_turbo_4step_ckpt500.safetensors",
                "turbo_strength": 0.7}
        preset = {"activated_loras": ["style.safetensors"], "loras_multipliers": "",
                  "params": {"num_inference_steps": 4, "minimax_h3_turbo_mode": True}}
        loras, mult, steps = maestro._lora_settings(mcfg, preset)
        self.assertEqual(loras, ["style.safetensors", "minimax_h3_turbo_4step_ckpt500.safetensors"])
        self.assertEqual(mult, "1.00 0.70")
        self.assertEqual(steps, 4)

    def test_parse_song_name(self):
        self.assertEqual(parse_song_name(Path("03 - Amelie Lens - Feel It.mp3")), ("Feel It", "Amelie Lens"))
        self.assertEqual(parse_song_name(Path("Only Title.wav")), ("Only Title", ""))
        self.assertEqual(parse_song_name(Path("12_Artist - A - B.flac")), ("A - B", "Artist"))
        self.assertEqual(parse_song_name(Path("Ice Storm (1).wav")), ("Ice Storm", ""))

    def test_normalize_for_search(self):
        from technoloop.songs import normalize

        self.assertEqual(normalize("Symphonie und Odyssee"), normalize("symphonie_und_odyssee"))
        self.assertEqual(normalize("Für Elise"), "fuerelise")
        self.assertIn(normalize("feuer und eis"), normalize("02 - Feuer und Eis (Remix)"))


class FakeMaestro(BaseHTTPRequestHandler):
    jobs: dict = {}
    requests: list = []
    uploads: list = []
    presets: list = []
    video_bytes = b""
    image_bytes = b""

    def log_message(self, *args):
        pass

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/v1/defaults/"):
            model = self.path.rsplit("/", 1)[-1]
            if model not in ("minimax_h3", "minimax_h3_ref2va", "krea2_turbo_edit"):
                return self._json({"detail": "Unknown model"}, 404)
            return self._json({"prompt": "default", "num_inference_steps": 20, "video_length": 124,
                               "sliding_window_size": 345, "resolution": "864x480", "guidance_scale": 1.0,
                               "image_prompt_type": ""})
        if self.path == "/api/v1/presets":
            return self._json({"presets": self.presets})
        if self.path.startswith("/api/v1/status/"):
            job = self.jobs[self.path.rsplit("/", 1)[-1]]
            job["polls"] += 1
            done = job["polls"] > 1
            return self._json({"job_id": job["id"], "status": "completed" if done else "running",
                               "progress": 100 if done else 50, "step": 2, "total_steps": 4, "phase": "",
                               "message": "", "output_files": [f"{job['id']}{job['ext']}"] if done else [],
                               "error": None, "oom_info": None})
        if self.path.startswith("/api/v1/file/"):
            data = self.image_bytes if self.path.endswith(".png") else self.video_bytes
            self.send_response(200)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self._json({"detail": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        if self.path == "/api/v1/upload":
            assert b'name="file"' in body
            name = f"/srv/maestro/uploads/u{len(self.uploads)}.png"
            self.uploads.append(name)
            return self._json({"filename": name.rsplit("/", 1)[-1], "path": name, "url": "x"})
        if self.path == "/api/v1/generate":
            payload = json.loads(body)
            self.requests.append(payload)
            job_id = f"job{len(self.requests)}"
            self.jobs[job_id] = {"id": job_id, "polls": 0, "ext": ".png" if payload.get("image_mode") == 1 else ".mp4"}
            return self._json({"job_id": job_id})
        if self.path.startswith("/api/v1/cancel/"):
            return self._json({"status": "cancelled"})
        self._json({"detail": "not found"}, 404)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class MaestroClientTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "bilder").mkdir()
        for name in ("girl1.png", "girl2.png", "key.png", "vorbild.jpg"):
            (self.tmp / "bilder" / name).write_bytes(b"\x89PNG fake")
        clip = self.tmp / "clip.mp4"
        ff.run([ff.ffmpeg(), "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=320x176:r=24",
                "-t", "1", "-pix_fmt", "yuv420p", str(clip)])
        FakeMaestro.video_bytes = clip.read_bytes()
        FakeMaestro.jobs, FakeMaestro.requests, FakeMaestro.uploads, FakeMaestro.presets = {}, [], [], []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeMaestro)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _project(self, **extra):
        cfg = {
            "maestro": {"url": self.url, "preset": "H3 Steps4", "variants": 1, "poll_seconds": 0.01},
            "girls": [{"name": "A", "image": "bilder/girl1.png", "look": "blonde"},
                      {"name": "B", "image": "bilder/girl2.png", "look": "brunette"}],
            "style_reference": "bilder/vorbild.jpg",
            "scenes": [
                {"id": "loop", "girls": True, "keyframe": "bilder/key.png", "action": "They dance."},
                {"id": "omni", "girls": [1], "action": "Close-up."},
                {"id": "crowd", "action": "Crowd jumps.", "frames": 200},
            ],
        }
        cfg.update(extra)
        path = self.tmp / "projekt.json"
        path.write_text(json.dumps(cfg))
        return load_project(path)

    def test_render_scenes_without_preset(self):
        project = self._project()
        failures = maestro.render_scenes(project)
        self.assertEqual(failures, 0)
        loop, omni, crowd = FakeMaestro.requests
        # Seamless loop: the same uploaded keyframe is first and last frame.
        self.assertEqual(loop["model_type"], "minimax_h3")
        self.assertEqual(loop["image_start"], loop["image_end"])
        self.assertEqual(loop["image_prompt_type"], "SE")
        self.assertIn("<Picture 1>", loop["prompt"])
        self.assertIn("integrated_multimodal_description: [Shot 1]", loop["prompt"])
        # H3 Turbo LoRA with 4 steps (Maestro's own Turbo checkbox would force 6).
        self.assertEqual(loop["num_inference_steps"], 4)
        self.assertEqual(loop["activated_loras"], ["minimax_h3_turbo_4step_ckpt500.safetensors"])
        self.assertEqual(loop["loras_multipliers"], "0.70")
        self.assertFalse(loop["minimax_h3_turbo_mode"])
        self.assertEqual(loop["video_length"], 175)
        self.assertEqual(loop["resolution"], "1280x704")
        # Omni: identity reference of girl B + style reference.
        self.assertEqual(omni["model_type"], "minimax_h3_ref2va")
        refs = omni["minimax_h3_references"]
        self.assertEqual([r["image_intent"] for r in refs], ["identity", "style"])
        self.assertNotIn("image_start", omni)
        self.assertIn("brunette", omni["prompt"])
        # Text only, frames snapped to 17n+5.
        self.assertEqual(crowd["video_length"], 192)
        self.assertNotIn("image_start", crowd)
        self.assertEqual(crowd["image_prompt_type"], "")
        clips = sorted(p.name for p in project.scenes_dir.glob("*.mp4"))
        self.assertEqual(clips, ["crowd__v1.mp4", "loop__v1.mp4", "omni__v1.mp4"])
        meta = json.loads((project.scenes_dir / "loop__v1.json").read_text())
        self.assertTrue(meta["loop"])
        # Second run skips finished clips.
        maestro.render_scenes(project)
        self.assertEqual(len(FakeMaestro.requests), 3)

    def test_preset_wins(self):
        FakeMaestro.presets = [{"id": "p1", "name": "H3 Steps4", "model_type": "minimax_h3",
                                "activated_loras": ["minimax_h3_turbo_4step_ckpt500.safetensors", "style.safetensors"],
                                "loras_multipliers": "0.8 0.5",
                                "params": {"num_inference_steps": 4, "guidance_scale": 1.0, "flow_shift": 5}}]
        project = self._project()
        maestro.render_scenes(project, only=["crowd"])
        (req,) = FakeMaestro.requests
        self.assertEqual(req["activated_loras"][1], "style.safetensors")
        self.assertEqual(req["loras_multipliers"], "0.8 0.5")
        self.assertEqual(req["flow_shift"], 5)


class FakeComfy(BaseHTTPRequestHandler):
    prompts: list = []
    uploads: list = []
    image_bytes = b""

    def log_message(self, *args):
        pass

    def _json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        if self.path == "/upload/image":
            name = f"up{len(self.uploads)}.png"
            self.uploads.append(name)
            return self._json({"name": name, "subfolder": "", "type": "input"})
        if self.path == "/prompt":
            self.prompts.append(json.loads(body)["prompt"])
            return self._json({"prompt_id": f"p{len(self.prompts)}"})

    def do_GET(self):
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[-1]
            return self._json({pid: {"outputs": {"9": {"images": [{"filename": "out.png", "subfolder": "",
                                                                     "type": "output"}]}}}})
        if self.path.startswith("/view?"):
            self.send_response(200)
            self.send_header("Content-Length", str(len(self.image_bytes)))
            self.end_headers()
            self.wfile.write(self.image_bytes)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class KeyframeTest(unittest.TestCase):
    def setUp(self):
        import cv2

        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "bilder").mkdir()
        img = np.zeros((64, 64, 3), np.uint8)
        img[:] = (30, 60, 200)
        ok, png = cv2.imencode(".png", img)
        FakeMaestro.image_bytes = FakeComfy.image_bytes = png.tobytes()
        for name in ("girl1.png", "girl2.png"):
            (self.tmp / "bilder" / name).write_bytes(png.tobytes())
        FakeMaestro.jobs, FakeMaestro.requests, FakeMaestro.uploads, FakeMaestro.presets = {}, [], [], []
        FakeComfy.prompts, FakeComfy.uploads = [], []
        self.servers = []
        for handler in (FakeMaestro, FakeComfy):
            srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            self.servers.append(srv)
        self.maestro_url = f"http://127.0.0.1:{self.servers[0].server_address[1]}"
        self.comfy_url = f"http://127.0.0.1:{self.servers[1].server_address[1]}"

    def tearDown(self):
        for srv in self.servers:
            srv.shutdown()
            srv.server_close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _project(self, keyframes=None):
        cfg = {
            "maestro": {"url": self.maestro_url, "preset": "", "variants": 1, "poll_seconds": 0.01},
            "keyframes": keyframes or {},
            "girls": [{"name": "A", "image": "bilder/girl1.png", "look": "blonde"},
                      {"name": "B", "image": "bilder/girl2.png", "look": "brunette"}],
            "scenes": [{"id": "dj", "girls": True, "action": "At the DJ booth."},
                       {"id": "crowd", "action": "Crowd jumps."}],
        }
        path = self.tmp / "projekt.json"
        path.write_text(json.dumps(cfg))
        return load_project(path)

    def test_maestro_keyframe_turns_scene_into_loop(self):
        from technoloop.keyframes import make_keyframes

        project = self._project()
        self.assertEqual(maestro.scene_mode(project, project["scenes"][0]), "omni")
        self.assertEqual(make_keyframes(project), 0)
        (req,) = FakeMaestro.requests  # only the girl scene needs a keyframe
        self.assertEqual(req["model_type"], "krea2_turbo_edit")
        self.assertEqual(req["image_mode"], 1)
        self.assertEqual(req["video_length"], 1)
        self.assertEqual(req["video_prompt_type"], "I")
        self.assertEqual(len(req["image_refs"]), 2)
        self.assertIn("first reference image", req["prompt"])
        target = self.tmp / "bilder" / "keyframes" / "dj.png"
        self.assertTrue(target.is_file())
        # The scene now renders as a seamless H3 loop from that keyframe.
        self.assertEqual(maestro.scene_mode(project, project["scenes"][0]), "keyframe")
        maestro.render_scenes(project, only=["dj"])
        h3 = FakeMaestro.requests[-1]
        self.assertEqual(h3["model_type"], "minimax_h3")
        self.assertEqual(h3["image_start"], h3["image_end"])
        # Second run: keyframe exists -> nothing generated.
        make_keyframes(project)
        self.assertEqual(sum(1 for r in FakeMaestro.requests if r["model_type"] == "krea2_turbo_edit"), 1)

    def test_comfyui_workflow_placeholders(self):
        from technoloop.keyframes import make_keyframes

        workflow = {
            "3": {"class_type": "KSampler", "inputs": {"seed": 5, "steps": 20}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "{{PROMPT}}, masterpiece"}},
            "10": {"class_type": "LoadImage", "inputs": {"image": "old_a.png"}},
            "11": {"class_type": "LoadImage", "inputs": {"image": "old_b.png"}},
            "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0]}},
        }
        (self.tmp / "wf.json").write_text(json.dumps(workflow))
        project = self._project({"engine": "comfyui", "comfyui_url": self.comfy_url, "comfyui_workflow": "wf.json"})
        self.assertEqual(make_keyframes(project), 0)
        (graph,) = FakeComfy.prompts
        self.assertTrue(graph["6"]["inputs"]["text"].endswith(", masterpiece"))
        self.assertIn("brunette", graph["6"]["inputs"]["text"])
        self.assertEqual([graph["10"]["inputs"]["image"], graph["11"]["inputs"]["image"]], ["up0.png", "up1.png"])
        self.assertNotEqual(graph["3"]["inputs"]["seed"], 5)
        self.assertTrue((self.tmp / "bilder" / "keyframes" / "dj.png").is_file())
        self.assertEqual(FakeMaestro.requests, [])


def _synthetic_beats(bpm: float, seconds: float, sr: int = audio.ANALYSIS_SR) -> np.ndarray:
    x = np.zeros(int(seconds * sr), np.float32)
    k = np.arange(int(0.15 * sr)) / sr
    kick = np.sin(2 * np.pi * 60 * k) * np.exp(-k * 25)
    t = 0.25
    while t < seconds - 0.2:
        p = int(t * sr)
        x[p:p + len(kick)] += kick
        t += 60.0 / bpm
    return x


class AnalysisTest(unittest.TestCase):
    def test_tempo(self):
        for bpm in (122.0, 128.0, 140.0):
            x = _synthetic_beats(bpm, 60)
            env = audio.band_envelope(x, audio.ANALYSIS_SR, 35, 130)
            period, phase, found, _conf = audio._comb_beats(audio.onset_envelope(env), audio.ANALYSIS_SR / audio.ENV_HOP)
            self.assertAlmostEqual(found, bpm, delta=0.15)
            rate = audio.ANALYSIS_SR / audio.ENV_HOP
            first = phase / rate
            d = (first - 0.25) % (60 / bpm)
            self.assertLess(min(d, 60 / bpm - d), 0.03)


    def test_free_tempo_falls_back_to_onsets(self):
        sr, rate = audio.ANALYSIS_SR, audio.ANALYSIS_SR / audio.ENV_HOP
        rng = np.random.default_rng(1)
        n = int(60 * sr)
        x = np.zeros(n)
        for _ in range(120):  # notes at random times: no steady beat
            p = int(rng.integers(0, n - sr))
            k = np.arange(sr) / sr
            x[p:p + sr] += np.sin(2 * np.pi * rng.uniform(40, 200) * k) * np.exp(-k * rng.uniform(2, 8))
        onset = audio.onset_envelope(audio.band_envelope(x.astype(np.float32), sr, 35, 130))
        self.assertLess(audio._comb_beats(onset, rate)[3], 1.8)
        peaks = audio._onset_peaks(onset, rate)
        self.assertGreater(len(peaks), 20)
        self.assertGreaterEqual(np.diff(peaks).min() / rate, 0.39)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class BuildTest(unittest.TestCase):
    def test_small_build(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            demo.make_demo(tmp)
            cfg = json.loads((tmp / "projekt.json").read_text())
            cfg["video"] = {"width": 640, "height": 360, "workers": 1, "clip_cache": 2, "encoder": "libx264"}
            (tmp / "projekt.json").write_text(json.dumps(cfg))
            project = load_project(tmp / "projekt.json")
            mix = audio.build_mix(project)
            self.assertAlmostEqual(mix.duration, 41 + 38 + 36 - 2 * 4, delta=0.5)
            analysis = audio.analyze(project, mix)
            self.assertEqual([round(b) for b in analysis.bpm], [124, 128, 132])
            clips = montage.collect_clips(project)
            segs = montage.plan_edl(project, clips, analysis, mix.timeline)
            self.assertAlmostEqual(segs[0].t0, 0.0)
            self.assertAlmostEqual(segs[-1].t1, analysis.n_frames / analysis.fps, delta=1e-6)
            for a, b in zip(segs, segs[1:]):
                self.assertAlmostEqual(a.t1, b.t0)
                self.assertNotEqual(a.clip, b.clip)
            on_beat = sum(np.min(np.abs(analysis.beats - s.t0)) < 0.02 for s in segs[1:])
            self.assertGreaterEqual(on_beat, len(segs) - 2)
            out = subprocess.run(
                [sys.executable, "-m", "technoloop", "bauen", str(tmp / "projekt.json"), "--vorschau", "6", "--ab", "0:36"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            video = tmp / "ausgabe" / "demo_techno_loop_vorschau.mp4"
            info = ff.probe(video)
            self.assertEqual((info["width"], info["height"]), (640, 360))
            self.assertAlmostEqual(info["duration"], 6.0, delta=0.15)
            self.assertTrue(info.get("has_audio"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class AppendTest(unittest.TestCase):
    """Find songs by name, append one, rebuild: the start must be reused, not re-rendered."""

    def test_append_song_reuses_rendered_start(self):
        from technoloop import cli, songs

        tmp = Path(tempfile.mkdtemp())
        try:
            demo.make_demo(tmp / "d")
            (tmp / "Downloads" / "suno").mkdir(parents=True)
            (tmp / "F").mkdir()
            music = sorted((tmp / "d" / "musik").glob("*.wav"))
            shutil.copy(music[0], tmp / "F" / "Symphonie und Odyssee.wav")
            shutil.copy(music[1], tmp / "Downloads" / "suno" / "Feuer und Eis.wav")
            shutil.copy(music[2], tmp / "Downloads" / "suno" / "Ice Storm (1).wav")
            cfg = {
                "name": "grow", "clips_folder": "d/clips",
                "song_search": ["Downloads", "Downloads/suno", "F"],
                "songs": [{"find": "symphonie und odyssee"}, {"find": "Feuer und Eis"}],
                "audio": {"crossfade_seconds": 4},
                "video": {"width": 320, "height": 180, "workers": 1, "encoder": "libx264", "chunk_seconds": 15},
            }
            config = tmp / "projekt.json"
            config.write_text(json.dumps(cfg))
            self.assertEqual(cli.main(["bauen", str(config)]), 0)
            parts_dir = tmp / "arbeitsordner" / "render" / "teile"
            first = {p.name: p.stat().st_mtime_ns for p in parts_dir.glob("*.mp4")}
            edl1 = json.loads((tmp / "arbeitsordner" / "render" / "edl.json").read_text())

            project = load_project(config)
            path, _ = songs.find_song(project, "ice storm")
            self.assertEqual(path.name, "Ice Storm (1).wav")
            self.assertEqual(songs.append_to_config(config, project, [path]), 1)
            self.assertEqual([s.title for s in load_project(config).songs()],
                             ["Symphonie und Odyssee", "Feuer und Eis", "Ice Storm"])

            self.assertEqual(cli.main(["bauen", str(config)]), 0)
            second = {p.name: p.stat().st_mtime_ns for p in parts_dir.glob("*.mp4")}
            reused = [n for n in first if second.get(n) == first[n]]
            self.assertGreaterEqual(len(reused), 2, "the unchanged start must not be rendered again")
            self.assertGreater(len(second), len(first))
            edl2 = json.loads((tmp / "arbeitsordner" / "render" / "edl.json").read_text())
            n_same = 0
            for a, b in zip(edl1["segments"], edl2["segments"]):
                if a != b:
                    break
                n_same += 1
            self.assertGreaterEqual(n_same, len(edl1["segments"]) // 2)
            info = ff.probe(tmp / "ausgabe" / "grow.mp4")
            self.assertAlmostEqual(info["duration"], 41 + 38 + 36 - 2 * 4, delta=0.5)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class ResolveExportTest(unittest.TestCase):
    def test_edl_matches_render_and_overlay_has_alpha(self):
        import re

        from technoloop import cli, resolve

        tmp = Path(tempfile.mkdtemp())
        try:
            demo.make_demo(tmp)
            cfg = json.loads((tmp / "projekt.json").read_text())
            cfg["video"] = {"width": 320, "height": 180, "workers": 1, "encoder": "libx264"}
            cfg["montage"] = {"reverse_chance": 0.5}  # make sure reverse and ping-pong runs show up
            (tmp / "projekt.json").write_text(json.dumps(cfg))
            self.assertEqual(cli.main(["resolve", str(tmp / "projekt.json")]), 0)
            out = tmp / "ausgabe" / "demo_techno_loop_resolve"
            edl = (out / "demo_techno_loop_schnitt.edl").read_text()
            clips, segments = montage.load_edl(tmp / "arbeitsordner" / "render" / "edl.json")
            fps = 24

            def frames(tc):
                h, m, s_, f = (int(x) for x in tc.split(":"))
                return ((h * 60 + m) * 60 + s_) * fps + f

            events = []
            for block in edl.split("\n\n"):  # read_text() turns the CRLF line ends into \\n
                m = re.search(r"^\d+\s+(\S+)\s+V\s+C\s+(\S+) (\S+) (\S+) (\S+)", block, re.M)
                if not m:
                    continue
                speed = re.search(r"^M2\s+\S+\s+(-?[\d.]+)", block, re.M)
                events.append((m.group(1), frames(m.group(2)), frames(m.group(4)) - 3600 * fps,
                               frames(m.group(5)) - 3600 * fps, float(speed.group(1)) if speed else fps))
            # Events tile the whole timeline without gaps.
            self.assertEqual(events[0][2], 0)
            for a, b in zip(events, events[1:]):
                self.assertEqual(a[3], b[2])
            n_frames = int(round(segments[-1].t1 * fps))
            self.assertEqual(events[-1][3], n_frames)
            self.assertTrue(any(e[4] < 0 for e in events), "expected reverse events")
            # Every record frame shows the same clip and (forward) the same source frame as the render.
            seg_i = 0
            for reel, src_in, r0, r1, speed in events:
                for r in range(r0, r1):
                    while round(segments[seg_i].t1 * fps) <= r:
                        seg_i += 1
                    seg = segments[seg_i]
                    clip = clips[seg.clip]
                    self.assertEqual(reel, resolve._reel(clip))
                    want = int(resolve.source_indices(seg, clip, np.array([r]), fps)[0])
                    if speed > 0:
                        # EDL keeps whole source frames and speeds with one decimal -> within ~1.5 frames
                        self.assertLessEqual(abs(src_in + (r - r0) * speed / fps - want), 1.5)
                    else:
                        self.assertGreaterEqual(want, src_in - 1)
            # Overlay: transparent in the middle, opaque on the speakers.
            mov = out / "demo_techno_loop_overlay_lautsprecher_titel.mov"
            raw = subprocess.run([ff.ffmpeg(), "-v", "error", "-ss", "2", "-i", str(mov), "-frames:v", "1",
                                  "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
            img = np.frombuffer(raw, np.uint8).reshape(180, 320, 4)
            self.assertEqual(img[60, 160, 3], 0)
            self.assertEqual(img[150, 30, 3], 255)
            self.assertTrue((out / "demo_techno_loop_musik.wav").is_file())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
