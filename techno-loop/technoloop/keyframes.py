"""Scene keyframes with the two girls, generated from their reference photos.

Default engine: Maestro's "Qwen Image 2.1" (up to ten reference images;
older Maestro versions fall back to "Krea 2 Turbo Identity Edit"). Alternative: any ComfyUI workflow exported in
API format with placeholders ({{PROMPT}}, {{IMAGE1}}, {{IMAGE2}}, {{SEED}},
{{WIDTH}}, {{HEIGHT}}).

A saved keyframe becomes the first AND last frame of the scene's H3 clip.
"""

from __future__ import annotations

import copy
import json
import time
import urllib.parse
import uuid
from pathlib import Path

from .config import ConfigError, Project
from .maestro import (MaestroClient, MaestroError, _cast, _looks_like_comfyui, connect, find_local,
                      free_comfyui_vram, keyframe_path_for, release_maestro_vram, run_job, scene_seed)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def keyframe_prompt(project: Project, scene: dict) -> str:
    if scene.get("keyframe_prompt"):
        return scene["keyframe_prompt"]
    cast = _cast(project, scene)
    looks = [g.get("look") or g.get("description") or "" for g in cast]
    if len(cast) >= 2:
        who = (f"The woman from image 1 (the first reference image) stands on the left ({looks[0]}), "
               f"the woman from image 2 (the second reference image) on the right ({looks[1]}).")
    else:
        who = f"The woman from image 1 (the reference image) ({looks[0]})."
    action = scene.get("action", "").strip()
    return (
        f"{who} {action} {project['style'].strip().rstrip('.')}. "
        "Keep both faces, hairstyles and outfits exactly as in the reference images. "
        "Photorealistic single frame of a live concert video, sharp focus, wide 16:9 composition, "
        "the women clearly visible."
    ).replace("  ", " ")


def scenes_needing_keyframes(project: Project, only=None, force=False) -> list[tuple[dict, Path]]:
    out = []
    for scene in project["scenes"]:
        if scene.get("skip") or (only and scene["id"] not in only):
            continue
        if not any((p := project.path(g.get("image"))) and p.is_file() for g in _cast(project, scene)):
            continue
        target = keyframe_path_for(project, scene)
        if target is None:
            continue
        if target.is_file() and not force:
            print(f"  {scene['id']}: Keyframe vorhanden ({target.name}) – übersprungen")
            continue
        out.append((scene, target))
    return out


def _girl_images(project: Project, scene: dict) -> list[Path]:
    imgs = []
    for girl in _cast(project, scene):
        p = project.path(girl.get("image"))
        if p and p.is_file():
            imgs.append(p)
    return imgs[:2]


def _save_image(data: bytes, suffix: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if suffix.lower() == target.suffix.lower():
        target.write_bytes(data)
        return
    import cv2
    import numpy as np

    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise MaestroError("Das erzeugte Bild ist nicht lesbar.")
    cv2.imwrite(str(target), img)


# ── Maestro ─────────────────────────────────────────────────────────────────

def _maestro_keyframe(client: MaestroClient, project: Project, scene: dict, images: list[Path],
                      defaults: dict, seed: int, uploads: dict) -> tuple[bytes, str]:
    kcfg = project["keyframes"]
    refs = []
    for img in images:
        if img not in uploads:
            uploads[img] = client.upload(img)
        refs.append(uploads[img])
    body = {k: v for k, v in (defaults or {}).items() if not isinstance(v, (bytes, bytearray))}
    for key in ("image_start", "image_end", "video_guide", "image_guide", "video_source"):
        body.pop(key, None)
    body.update({
        "model_type": kcfg["model"],
        "prompt": keyframe_prompt(project, scene),
        "image_refs": refs,
        # "I" = all reference images are people (Krea 2 Edit); the model's own default letters stay otherwise.
        "video_prompt_type": kcfg.get("video_prompt_type", "I"),
        "image_mode": 1,
        "video_length": 1,
        "batch_size": 1,
        "resolution": kcfg["resolution"],
        "seed": int(seed),
        "generation_mode": "image",
    })
    if int(kcfg.get("steps") or 0) > 0:
        body["num_inference_steps"] = int(kcfg["steps"])
    if project["maestro"].get("workspace"):
        body["workspace"] = project["maestro"]["workspace"]
    body.update(kcfg.get("extra_params") or {})
    body.update(scene.get("keyframe_params") or {})
    status = run_job(client, body, f"Keyframe {scene['id']}", poll=float(project["maestro"]["poll_seconds"]),
                     timeout_s=float(project["maestro"]["timeout_minutes"]) * 60)
    if status.get("status") != "completed":
        raise MaestroError(f"Job {status.get('status')}: {status.get('error') or status.get('message')}")
    files = [f for f in status.get("output_files") or [] if Path(f).suffix.lower() in IMAGE_EXTENSIONS]
    if not files:
        raise MaestroError(f"Job fertig, aber kein Bild in output_files: {status.get('output_files')}")
    tmp = Path(project.work_dir) / "cache" / f"kf_{uuid.uuid4().hex[:8]}{Path(files[-1]).suffix}"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    client.download(files[-1], tmp)
    data = tmp.read_bytes()
    tmp.unlink(missing_ok=True)
    return data, Path(files[-1]).suffix


# ── ComfyUI ─────────────────────────────────────────────────────────────────

class ComfyClient(MaestroClient):
    """Same small HTTP helper, ComfyUI endpoints."""

    def upload_image(self, path: Path) -> str:
        boundary = uuid.uuid4().hex
        parts = [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n".encode() + path.read_bytes() + b"\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n".encode(),
            f"--{boundary}--\r\n".encode(),
        ]
        with self._request("POST", "/upload/image", body=b"".join(parts),
                           headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return f"{data['subfolder']}/{data['name']}" if data.get("subfolder") else data["name"]


def fill_workflow(workflow: dict, values: dict) -> dict:
    """Replace {{NAME}} placeholders; fall back to LoadImage order / seed inputs when absent."""
    wf = copy.deepcopy(workflow)
    found = set()

    def sub(value):
        if isinstance(value, str):
            for name, v in values.items():
                token = "{{" + name + "}}"
                if value == token:
                    found.add(name)
                    return v
                if token in value:
                    found.add(name)
                    value = value.replace(token, str(v))
            return value
        if isinstance(value, list):
            return [sub(v) for v in value]
        if isinstance(value, dict):
            return {k: sub(v) for k, v in value.items()}
        return value

    wf = sub(wf)
    nodes = sorted(wf.items(), key=lambda kv: _node_order(kv[0]))
    if "IMAGE1" not in found:
        loaders = [n for _, n in nodes if n.get("class_type") == "LoadImage"]
        for node, key in zip(loaders, ("IMAGE1", "IMAGE2")):
            if key in values:
                node["inputs"]["image"] = values[key]
    if "SEED" not in found:
        for _, node in nodes:
            for name in ("seed", "noise_seed"):
                if isinstance(node.get("inputs", {}).get(name), int):
                    node["inputs"][name] = values["SEED"]
    if "PROMPT" not in found and not _set_positive_prompt(wf, values["PROMPT"]):
        raise ConfigError(
            "Im ComfyUI-Workflow wurde kein Prompt-Feld gefunden. Schreibe {{PROMPT}} in das positive "
            "Prompt-Feld und exportiere den Workflow erneut mit 'Export (API)'."
        )
    return wf


def _node_order(node_id) -> tuple:
    """'12' < '470' < '470:3' (flattened subgraph ids from ComfyUI's API export)."""
    parts = []
    for part in str(node_id).split(":"):
        parts.append(int(part) if part.isdigit() else 0)
    return tuple(parts)


def _set_positive_prompt(wf: dict, prompt: str) -> bool:
    """Find the positive prompt of an unmodified exported workflow: walk upstream from every
    'positive' input (sampler / guider) to the first node with a text field."""
    text_keys = ("text", "prompt", "text_g", "positive_prompt")
    starts = [n["inputs"]["positive"] for n in wf.values()
              if isinstance(n.get("inputs", {}).get("positive"), list)]
    done = False
    for link in starts:
        queue, seen = [str(link[0])], set()
        while queue:
            nid = queue.pop(0)
            if nid in seen or nid not in wf:
                continue
            seen.add(nid)
            inputs = wf[nid].get("inputs", {})
            key = next((k for k in text_keys if isinstance(inputs.get(k), str)), None)
            if key:
                inputs[key] = prompt
                done = True
                break
            queue += [str(v[0]) for v in inputs.values() if isinstance(v, list) and len(v) == 2]
    if done:
        return True
    for _, node in sorted(wf.items(), key=lambda kv: _node_order(kv[0])):
        if "TextEncode" in str(node.get("class_type")):
            inputs = node.get("inputs", {})
            key = next((k for k in text_keys if isinstance(inputs.get(k), str)), None)
            if key:
                inputs[key] = prompt
                return True
    return False


def _comfy_keyframe(client: ComfyClient, project: Project, scene: dict, images: list[Path],
                    workflow: dict, seed: int, uploads: dict) -> tuple[bytes, str]:
    kcfg = project["keyframes"]
    w, _, h = kcfg["resolution"].partition("x")
    values = {"PROMPT": keyframe_prompt(project, scene), "SEED": int(seed), "WIDTH": int(w), "HEIGHT": int(h)}
    for k, img in enumerate(images, 1):
        if img not in uploads:
            uploads[img] = client.upload_image(img)
        values[f"IMAGE{k}"] = uploads[img]
    if len(images) == 1:
        values["IMAGE2"] = values["IMAGE1"]
    graph = fill_workflow(workflow, values)
    prompt_id = client.post_json("/prompt", {"prompt": graph, "client_id": uuid.uuid4().hex})["prompt_id"]
    started = time.time()
    timeout = float(project["maestro"]["timeout_minutes"]) * 60
    while True:
        hist = client.get_json(f"/history/{prompt_id}").get(prompt_id)
        if hist and hist.get("outputs"):
            break
        if hist and (hist.get("status") or {}).get("status_str") == "error":
            raise MaestroError(f"ComfyUI-Fehler: {json.dumps(hist.get('status'))[:400]}")
        if time.time() - started > timeout:
            raise MaestroError("ComfyUI: Zeitlimit überschritten.")
        print(f"\r  Keyframe {scene['id']}: ComfyUI rechnet … {int(time.time() - started)}s", end="", flush=True)
        time.sleep(float(project["maestro"]["poll_seconds"]))
    print()
    for node_out in hist["outputs"].values():
        for img in node_out.get("images") or []:
            if img.get("type", "output") == "output":
                q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""),
                                            "type": img.get("type", "output")})
                with client._request("GET", f"/view?{q}") as resp:
                    return resp.read(), Path(img["filename"]).suffix
    raise MaestroError("ComfyUI hat kein Ausgabebild geliefert (fehlt ein SaveImage-Knoten?).")


# ── command ─────────────────────────────────────────────────────────────────

def make_keyframes(project: Project, *, only=None, force=False, dry_run=False, url=None) -> int:
    kcfg = project["keyframes"]
    todo = scenes_needing_keyframes(project, only, force)
    if not todo:
        print("Keine Keyframes zu erstellen (Szenen mit Girls brauchen girls[].image; vorhandene werden übersprungen).")
        return 0
    engine = kcfg.get("engine", "maestro")
    if dry_run:
        for scene, target in todo:
            imgs = ", ".join(p.name for p in _girl_images(project, scene))
            print(f"\n{scene['id']} → {target}  ({engine}, {kcfg['model'] if engine == 'maestro' else 'Workflow'}, Referenzen: {imgs})")
            print("  " + keyframe_prompt(project, scene))
        return 0
    uploads: dict = {}
    if engine == "comfyui":
        wf_path = project.path(kcfg.get("comfyui_workflow"))
        if not wf_path or not wf_path.is_file():
            raise ConfigError("keyframes.comfyui_workflow: Pfad zur Workflow-Datei (API-Format) fehlt.")
        workflow = json.loads(wf_path.read_text(encoding="utf-8"))
        comfy_url = find_local(_looks_like_comfyui, kcfg.get("comfyui_url"))
        if not comfy_url:
            raise MaestroError("ComfyUI nicht gefunden – in Pinokio starten oder keyframes.comfyui_url eintragen.")
        print(f"ComfyUI: {comfy_url}")
        release_maestro_vram(project)
        client = ComfyClient(comfy_url)
    else:
        client = connect(url or project["maestro"]["url"])
        free_comfyui_vram(project)
        defaults = None
        for model in [kcfg["model"]] + ([kcfg["fallback_model"]] if kcfg.get("fallback_model") else []):
            try:
                defaults = client.get_json(f"/api/v1/defaults/{urllib.parse.quote(model)}")
            except MaestroError:
                continue
            if model != kcfg["model"]:
                print(f"Bildmodell '{kcfg['model']}' gibt es in diesem Maestro nicht – nehme '{model}'.")
                kcfg = dict(kcfg, model=model)
                project.data["keyframes"] = kcfg
            break
        if defaults is None:
            raise MaestroError(
                f"Bildmodell '{kcfg['model']}' ist in Maestro nicht verfügbar – Maestro aktualisieren, das Modell "
                "in den Einstellungen sichtbar schalten oder keyframes.model ändern."
            )
    failures = 0
    for index, (scene, target) in enumerate(todo, 1):
        images = _girl_images(project, scene)
        for cand in range(1, int(kcfg.get("candidates") or 1) + 1):
            out = target if cand == 1 else target.with_name(f"{target.stem}__alt{cand}{target.suffix}")
            seed = scene_seed(project, f"keyframe:{scene['id']}", cand)
            print(f"[{index}/{len(todo)}] Keyframe {scene['id']}" + (f" (Variante {cand})" if cand > 1 else ""))
            started = time.time()
            try:
                if engine == "comfyui":
                    data, suffix = _comfy_keyframe(client, project, scene, images, workflow, seed, uploads)
                else:
                    data, suffix = _maestro_keyframe(client, project, scene, images, defaults, seed, uploads)
                _save_image(data, suffix, out)
                print(f"  gespeichert: {out} ({(time.time() - started) / 60:.1f} min)")
            except MaestroError as error:
                failures += 1
                print(f"  FEHLER: {error}")
                if "nicht erreichbar" in str(error):
                    raise
    if engine == "comfyui":
        try:  # hand the VRAM back for the H3 renders in Maestro
            client.post_json("/free", {"unload_models": True, "free_memory": True})
        except MaestroError:
            pass
    print("\nKeyframes fertig. Prüfe die Bilder – unpassende löschen oder durch eine __alt-Variante ersetzen, "
          "dann '1_szenen_rendern.bat'. Szenen mit Keyframe werden als nahtlose Loops gerendert.")
    return failures
