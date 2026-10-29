"""Render the scene pool through Maestro's local REST API (MiniMax H3)."""

from __future__ import annotations

import json
import mimetypes
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zlib
from pathlib import Path

from .config import ConfigError, Project

TERMINAL = {"completed", "failed", "cancelled"}


class MaestroError(RuntimeError):
    pass


class MaestroClient:
    def __init__(self, url: str, timeout: float = 60.0):
        self.url = url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, *, body: bytes | None = None, headers: dict | None = None):
        req = urllib.request.Request(self.url + path, data=body, method=method, headers=headers or {})
        try:
            return urllib.request.urlopen(req, timeout=self.timeout)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")
            try:
                detail = json.loads(detail).get("detail", detail)
            except (ValueError, AttributeError):
                pass
            raise MaestroError(f"Maestro {method} {path} -> HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            raise MaestroError(
                f"Maestro ist unter {self.url} nicht erreichbar ({error}). Starte Maestro in Pinokio und "
                "trage die Adresse aus 'Open Web UI' in projekt.json unter maestro.url ein."
            ) from error

    def get_json(self, path: str):
        with self._request("GET", path) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def post_json(self, path: str, payload: dict):
        data = json.dumps(payload).encode("utf-8")
        with self._request("POST", path, body=data, headers={"Content-Type": "application/json"}) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")

    def upload(self, file_path: Path) -> str:
        boundary = uuid.uuid4().hex
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        head = (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file_path.name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
        body = head + file_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
        with self._request(
            "POST", "/api/v1/upload", body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        ) as resp:
            return json.loads(resp.read().decode("utf-8"))["path"]

    def download(self, filename: str, dest: Path) -> None:
        quoted = urllib.parse.quote(filename.replace("\\", "/").split("/")[-1])
        tmp = dest.with_suffix(dest.suffix + ".part")
        with self._request("GET", f"/api/v1/file/{quoted}") as resp, open(tmp, "wb") as out:
            while chunk := resp.read(1 << 20):
                out.write(chunk)
        tmp.replace(dest)


def _looks_like_maestro(url: str) -> bool:
    client = MaestroClient(url, timeout=2.0)
    try:
        return "presets" in client.get_json("/api/v1/presets") and bool(client.get_json("/api/v1/defaults/minimax_h3"))
    except Exception:
        return False


def connect(url: str | None) -> MaestroClient:
    """Use the configured address; if it is 'auto' or unreachable, look for Maestro on local ports."""
    if url and url != "auto" and _looks_like_maestro(url):
        return MaestroClient(url)
    # Pinokio hands out ports from 42000 upwards; also try common defaults.
    for port in [*range(42000, 42300), 7860, 7861, 8000, 8080]:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.05):
                pass
        except OSError:
            continue
        candidate = f"http://127.0.0.1:{port}"
        if _looks_like_maestro(candidate):
            if url and url != "auto":
                print(f"Maestro nicht unter {url}, aber unter {candidate} gefunden.")
            else:
                print(f"Maestro gefunden: {candidate}")
            return MaestroClient(candidate)
    raise MaestroError(
        f"Maestro ist nicht erreichbar ({url or 'auto'}). Starte Maestro in Pinokio und trage die Adresse aus "
        "'Open Web UI' in projekt.json unter maestro.url ein."
    )


# ── prompts ─────────────────────────────────────────────────────────────────

def _cast(project: Project, scene: dict) -> list[dict]:
    girls = project["girls"] or []
    wanted = scene.get("girls", False)
    if wanted is True:
        return list(girls)
    if isinstance(wanted, list):
        picked = []
        for item in wanted:
            if isinstance(item, int) and 0 <= item < len(girls):
                picked.append(girls[item])
            else:
                picked += [g for g in girls if str(g.get("name", "")).lower() == str(item).lower()]
        return picked
    return []


def _cast_sentence(cast: list[dict]) -> str:
    if not cast:
        return ""
    looks = [g.get("look") or g.get("description") or "a stylish techno DJ" for g in cast]
    if len(looks) == 1:
        return f"The DJ is a woman, {looks[0]}."
    if len(looks) == 2:
        return f"Two women DJs: on the left a woman, {looks[0]}; on the right a woman, {looks[1]}."
    return "Women DJs: " + "; ".join(f"a woman, {look}" for look in looks) + "."


def scene_mode(project: Project, scene: dict) -> str:
    mode = scene.get("mode", "auto")
    if mode != "auto":
        return mode
    keyframe = project.path(scene.get("keyframe"))
    if keyframe and keyframe.is_file():
        return "keyframe"
    if any((p := project.path(g.get("image"))) and p.is_file() for g in _cast(project, scene)):
        return "omni"
    return "text"


def build_prompt(project: Project, scene: dict, mode: str, loop: bool) -> str:
    if scene.get("prompt"):
        return scene["prompt"]
    style = project["style"].strip().rstrip(".")
    action = scene.get("action", "").strip()
    cast = _cast_sentence(_cast(project, scene))
    silence = (
        "Nobody speaks or sings; every mouth stays closed or smiling and the audio contains no human voice."
        if _cast(project, scene) else ""
    )
    looping = (
        "The motion is cyclic: by the final frame everyone and the camera return exactly to the opening pose "
        "and composition." if loop else ""
    )
    description = " ".join(x for x in (f"{style}.", cast, action, looping, silence) if x)
    if mode == "omni":
        return description
    lines = []
    if mode == "keyframe":
        lines += [
            "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.",
            "",
        ]
    lines += [
        f"integrated_multimodal_description: [Shot 1] {description}",
        f"overall_soundscape: {project['soundscape']}",
        f"non_diegetic_music: {project['music']}",
    ]
    return "\n".join(lines)


def snap_frames(frames: int) -> int:
    """H3's video VAE accepts 17*n+5 frames between 124 and 345."""
    frames = max(124, min(345, int(frames)))
    n = round((frames - 5) / 17)
    return 17 * n + 5


# ── request assembly ────────────────────────────────────────────────────────

def _find_preset(client: MaestroClient, name: str) -> dict | None:
    if not name:
        return None
    try:
        presets = client.get_json("/api/v1/presets").get("presets", [])
    except MaestroError:
        return None
    wanted = name.strip().lower().replace(" ", "")
    for preset in presets:
        if str(preset.get("name", "")).strip().lower().replace(" ", "") == wanted:
            return preset
    return None


def _lora_settings(mcfg: dict, preset: dict | None) -> tuple[list[str], str, int]:
    if preset:
        params = preset.get("params") or {}
        loras = list(preset.get("activated_loras") or params.get("activated_loras") or [])
        mult = preset.get("loras_multipliers") or params.get("loras_multipliers") or ""
        mult = " ".join(str(m) for m in mult) if isinstance(mult, list) else str(mult)
        steps = int(params.get("num_inference_steps") or mcfg["steps"])
        if params.get("minimax_h3_turbo_mode") and not any("turbo" in str(l).lower() for l in loras):
            # Maestro's Turbo checkbox adds the LoRA at submit time but also forces 6 steps.
            # Add the LoRA explicitly instead, so the preset's own step count is kept.
            tokens = mult.split()
            tokens += ["1.00"] * (len(loras) - len(tokens))
            loras.append(mcfg["turbo_lora"])
            mult = " ".join(tokens[: len(loras) - 1] + [f"{float(mcfg['turbo_strength']):.2f}"])
        return loras, mult.strip(), steps
    if mcfg.get("turbo", True):
        return [mcfg["turbo_lora"]], f"{float(mcfg['turbo_strength']):.2f}", int(mcfg["steps"])
    return [], "", int(mcfg["steps"])


def assemble_request(
    project: Project,
    scene: dict,
    *,
    mode: str,
    defaults: dict,
    preset: dict | None,
    seed: int,
    keyframe_path: str | None,
    references: list[dict] | None,
) -> dict:
    mcfg = project["maestro"]
    loop = bool(scene.get("loop", True)) and mode == "keyframe"
    body = {k: v for k, v in (defaults or {}).items() if not isinstance(v, (bytes, bytearray))}
    if preset:
        body.update({k: v for k, v in (preset.get("params") or {}).items() if not k.startswith("image_")})
    loras, multipliers, steps = _lora_settings(mcfg, preset)
    body.update({
        "model_type": mcfg["omni_model"] if mode == "omni" else mcfg["model"],
        "prompt": build_prompt(project, scene, mode, loop),
        "resolution": scene.get("resolution") or mcfg["resolution"],
        "video_length": snap_frames(scene.get("frames") or mcfg["frames"]),
        "num_inference_steps": steps,
        "activated_loras": loras,
        "loras_multipliers": multipliers,
        "seed": int(seed),
        "image_mode": 0,
        "image_prompt_type": "",
        "minimax_h3_turbo_mode": False,
        "minimax_h3_window_storyboard": False,
        "generation_mode": "video",
    })
    if mcfg.get("workspace"):
        body["workspace"] = mcfg["workspace"]
    for key in ("image_start", "image_end", "minimax_h3_references"):
        body.pop(key, None)
    if mode == "keyframe":
        body["image_start"] = keyframe_path
        body["image_prompt_type"] = "S"
        body["input_video_strength"] = 1.0
        if loop:
            # Same picture as first AND last frame -> the clip ends where it began.
            body["image_end"] = keyframe_path
            body["image_prompt_type"] = "SE"
    elif mode == "omni":
        body["minimax_h3_references"] = references or []
        body["minimax_h3_reference_detail"] = "match"
    body.update(mcfg.get("extra_params") or {})
    body.update(scene.get("extra_params") or {})
    return body


# ── job execution ───────────────────────────────────────────────────────────

def _print_progress(label: str, status: dict) -> None:
    pct = status.get("progress") or 0
    step, total = status.get("step") or 0, status.get("total_steps") or 0
    steps = f" Schritt {step}/{total}" if total else ""
    msg = (status.get("message") or status.get("phase") or "")[:60]
    sys.stdout.write(f"\r  {label}: {status.get('status')} {pct:>3}%{steps}  {msg:<60}")
    sys.stdout.flush()


def run_job(client: MaestroClient, body: dict, label: str, *, poll: float, timeout_s: float) -> dict:
    job = client.post_json("/api/v1/generate", body)
    job_id = job.get("job_id") or job.get("id")
    if not job_id:
        raise MaestroError(f"Maestro hat keine job_id geliefert: {job}")
    started = time.time()
    try:
        while True:
            status = client.get_json(f"/api/v1/status/{job_id}")
            _print_progress(label, status)
            if status.get("status") in TERMINAL:
                print()
                return status
            if time.time() - started > timeout_s:
                client.post_json(f"/api/v1/cancel/{job_id}", {})
                raise MaestroError(f"Zeitlimit überschritten ({timeout_s / 60:.0f} min).")
            time.sleep(poll)
    except KeyboardInterrupt:
        print("\n  Abbruch – breche den Maestro-Job ab …")
        try:
            client.post_json(f"/api/v1/cancel/{job_id}", {})
        except MaestroError:
            pass
        raise


def scene_seed(project: Project, scene_id: str, variant: int) -> int:
    return zlib.crc32(f"{project['seed']}:{scene_id}:{variant}".encode()) & 0x7FFFFFFF


def render_scenes(project: Project, *, only: list[str] | None = None, force: bool = False,
                  dry_run: bool = False, url: str | None = None) -> int:
    mcfg = project["maestro"]
    scenes = [s for s in project["scenes"] if not s.get("skip")]
    if only:
        scenes = [s for s in scenes if s["id"] in only]
        if not scenes:
            raise ConfigError(f"Keine Szene mit id {', '.join(only)} gefunden.")
    if not scenes:
        raise ConfigError("In projekt.json sind keine Szenen eingetragen.")
    out_dir = project.scenes_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    client = MaestroClient(url or mcfg["url"]) if dry_run else connect(url or mcfg["url"])
    preset = None if dry_run else _find_preset(client, mcfg.get("preset", ""))
    if preset:
        print(f"Maestro-Preset '{preset.get('name')}' gefunden – Schritte/LoRAs kommen aus dem Preset.")
    elif mcfg.get("preset") and not dry_run:
        print(f"Preset '{mcfg['preset']}' nicht in Maestro gefunden – nutze H3 Turbo mit {mcfg['steps']} Schritten.")

    defaults_cache: dict[str, dict] = {}
    uploads: dict[Path, str] = {}

    def defaults_for(model: str) -> dict:
        if dry_run:
            return {}
        if model not in defaults_cache:
            try:
                defaults_cache[model] = client.get_json(f"/api/v1/defaults/{urllib.parse.quote(model)}")
            except MaestroError as error:
                raise MaestroError(
                    f"Modell '{model}' ist in Maestro nicht verfügbar. Aktiviere 'MiniMax H3' in den Maestro-"
                    f"Einstellungen (Model visibility) oder passe maestro.model an. ({error})"
                ) from error
        return defaults_cache[model]

    def upload(local: Path) -> str:
        if dry_run:
            return str(local)
        if local not in uploads:
            uploads[local] = client.upload(local)
        return uploads[local]

    jobs = []
    for scene in scenes:
        for variant in range(1, int(scene.get("variants") or mcfg["variants"]) + 1):
            jobs.append((scene, variant))

    failures = 0
    for index, (scene, variant) in enumerate(jobs, 1):
        target = out_dir / f"{scene['id']}__v{variant}.mp4"
        label = f"[{index}/{len(jobs)}] {scene['id']} v{variant}"
        if target.exists() and not force:
            print(f"  {label}: schon vorhanden – übersprungen")
            continue
        mode = scene_mode(project, scene)
        if mode == "text" and _cast(project, scene) and variant == 1:
            print(f"  Hinweis: '{scene['id']}' hat weder Keyframe noch Girl-Bilder – die Girls entstehen nur aus "
                  "der Beschreibung und sehen in jedem Clip etwas anders aus.")
        keyframe_path = None
        references = None
        if mode == "keyframe":
            local = project.path(scene["keyframe"])
            if not local or not local.is_file():
                raise ConfigError(f"Keyframe für Szene '{scene['id']}' fehlt: {scene.get('keyframe')}")
            keyframe_path = upload(local)
        elif mode == "omni":
            references = []
            for girl in _cast(project, scene):
                img = project.path(girl.get("image"))
                if img and img.is_file():
                    look = girl.get("look") or girl.get("description") or ""
                    role = f"{girl.get('name', 'DJ')}, {look}".strip(", ")
                    references.append({"type": "image", "path": upload(img), "role": role, "image_intent": "identity"})
            style_ref = project.path(scene.get("style_reference") or project.get("style_reference"))
            if style_ref and style_ref.is_file():
                references.append({
                    "type": "image", "path": upload(style_ref),
                    "role": "the festival stage, lighting and colour palette", "image_intent": "style",
                })
            if not references:
                raise ConfigError(f"Szene '{scene['id']}' (omni) braucht Bilder der Girls (girls[].image).")
        model = mcfg["omni_model"] if mode == "omni" else mcfg["model"]
        seed = scene_seed(project, scene["id"], variant)
        body = assemble_request(
            project, scene, mode=mode, defaults=defaults_for(model), preset=preset,
            seed=seed, keyframe_path=keyframe_path, references=references,
        )
        meta = {
            "scene": scene["id"], "variant": variant, "mode": mode,
            "loop": bool(body.get("image_end")), "seed": seed,
            "frames": body["video_length"], "steps": body["num_inference_steps"],
            "model_type": body["model_type"], "prompt": body["prompt"],
            "tags": scene.get("tags") or (["girls"] if _cast(project, scene) else []),
        }
        if dry_run:
            print(f"\n{label} ({mode}, {body['model_type']}, {body['video_length']} Frames, "
                  f"{body['num_inference_steps']} Schritte, LoRAs {body['activated_loras']} @ {body['loras_multipliers']})")
            if variant == 1:
                print("  " + body["prompt"].replace("\n", "\n  "))
            continue
        print(f"{label}: sende an Maestro ({mode}, {body['video_length']} Frames, {body['num_inference_steps']} Schritte)")
        started = time.time()
        try:
            status = run_job(
                client, body, label,
                poll=float(mcfg["poll_seconds"]), timeout_s=float(mcfg["timeout_minutes"]) * 60,
            )
            if status.get("status") != "completed":
                hint = ""
                if status.get("oom_info"):
                    hint = " (GPU-Speicher voll: frames in projekt.json z.B. auf 124 senken)"
                raise MaestroError(f"Job {status.get('status')}: {status.get('error') or status.get('message')}{hint}")
            videos = [f for f in status.get("output_files") or [] if Path(f).suffix.lower() in {".mp4", ".webm", ".mov", ".mkv"}]
            if not videos:
                raise MaestroError(f"Job fertig, aber kein Video in output_files: {status.get('output_files')}")
            client.download(videos[-1], target)
            target.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"  gespeichert: {target.name} ({(time.time() - started) / 60:.1f} min)")
        except MaestroError as error:
            failures += 1
            print(f"  FEHLER {label}: {error}")
            if "nicht erreichbar" in str(error):
                raise
    done = len(list(out_dir.glob("*.mp4")))
    print(f"\nFertig: {done} Clips in {out_dir}" + (f", {failures} Fehler" if failures else ""))
    return failures
