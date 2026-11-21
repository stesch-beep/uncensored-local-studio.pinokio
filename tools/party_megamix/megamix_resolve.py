#!/usr/bin/env python3
"""
Builds the Party Megamix as a 1920x1080 timeline in DaVinci Resolve from plan.json.

How to run (works in the free DaVinci Resolve too):
  1. Copy this file to the Resolve scripts folder:
       Windows: %APPDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Utility\\
       macOS:   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
  2. Set PLAN_PATH below (or the environment variable MEGAMIX_PLAN) to your plan.json.
  3. In Resolve: Workspace > Scripts > megamix_resolve
  (Resolve Studio can also run it externally: python megamix_resolve.py path\\to\\plan.json)

Tracks:
  V1 = beat-cut girls + landscapes, V2 = lipsync shots (exactly on the song),
  A1/A2 = songs alternating, so the transitions between songs can be crossfaded.
"""
import json
import os
import sys

PLAN_PATH = r""                      # e.g. r"D:\Maestro\megamix_out\plan.json"
PROJECT_NAME = "Party Megamix - Eva & Techno Girls"
TIMELINE_NAME = "Megamix 1080p"
ADD_RENDER_JOB = True                # puts a 1080p H.264 job into the render queue
START_RENDER = False                 # True = start rendering right away


def get_resolve():
    g = globals()
    if g.get("resolve"):
        return g["resolve"]
    if g.get("bmd"):
        r = g["bmd"].scriptapp("Resolve")
        if r:
            return r
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        mod = {
            "win32": r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules",
            "darwin": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules",
        }.get(sys.platform, "/opt/resolve/Developer/Scripting/Modules")
        sys.path.append(mod)
        import DaVinciResolveScript as dvr
    return dvr.scriptapp("Resolve")


def find_plan():
    for p in [PLAN_PATH, os.environ.get("MEGAMIX_PLAN", ""), *(sys.argv[1:2])]:
        if p and os.path.isfile(p):
            return p
    here = os.path.dirname(os.path.abspath(globals().get("__file__", "."))) if "__file__" in globals() else "."
    for p in (os.path.join(here, "plan.json"), os.path.join(here, "megamix_out", "plan.json")):
        if os.path.isfile(p):
            return p
    raise SystemExit("plan.json nicht gefunden – PLAN_PATH im Skript setzen.")


def main():
    plan_path = find_plan()
    plan = json.load(open(plan_path, encoding="utf-8"))
    W, H, FPS = plan.get("width", 1920), plan.get("height", 1080), plan.get("fps", 30)

    resolve = get_resolve()
    if not resolve:
        raise SystemExit("DaVinci Resolve nicht erreichbar (laeuft Resolve? Externes Scripting nur in Studio).")
    pm = resolve.GetProjectManager()
    proj = pm.CreateProject(PROJECT_NAME) or pm.LoadProject(PROJECT_NAME)
    if not proj:
        raise SystemExit("Projekt konnte nicht angelegt/geladen werden.")
    for k, v in {
        "timelineFrameRate": str(FPS), "timelinePlaybackFrameRate": str(FPS),
        "timelineResolutionWidth": str(W), "timelineResolutionHeight": str(H),
        "timelineOutputResolutionWidth": str(W), "timelineOutputResolutionHeight": str(H),
        "timelineInputResMismatchBehavior": "scaleToCrop",   # fill 16:9 frame, no black bars
    }.items():
        proj.SetSetting(k, v)

    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()
    folders = {}
    for name in ("Songs", "Girls", "Landschaften", "Lipsync"):
        folders[name] = mp.AddSubFolder(root, name) or root

    def import_into(folder, paths):
        mp.SetCurrentFolder(folder)
        items = mp.ImportMedia(sorted(set(paths))) or []
        out = {}
        for it in items:
            fp = os.path.normcase(os.path.abspath(it.GetClipProperty("File Path") or ""))
            out[fp] = it
        return out

    key = lambda p: os.path.normcase(os.path.abspath(p))
    shots = plan["shots"]
    items = {}
    items.update(import_into(folders["Songs"], [s["path"] for s in plan["songs"]]))
    for kind, folder in (("girls", "Girls"), ("landscape", "Landschaften"), ("lipsync", "Lipsync")):
        paths = [s["clip"] for s in shots if s["kind"] == kind and key(s["clip"]) not in items]
        if paths:
            items.update(import_into(folders[folder], paths))

    tl = mp.CreateEmptyTimeline(TIMELINE_NAME)
    if not tl:
        n = 2
        while not tl and n < 50:
            tl = mp.CreateEmptyTimeline(f"{TIMELINE_NAME} ({n})"); n += 1
    proj.SetCurrentTimeline(tl)
    while tl.GetTrackCount("video") < 2:
        tl.AddTrack("video")
    while tl.GetTrackCount("audio") < 2:
        tl.AddTrack("audio", "stereo")
    tl.SetTrackName("video", 1, "Girls + Landschaft")
    tl.SetTrackName("video", 2, "Lipsync")
    tl.SetTrackName("audio", 1, "Songs A")
    tl.SetTrackName("audio", 2, "Songs B")
    t0 = tl.GetStartFrame()
    fr = lambda sec: int(round(sec * FPS))

    # --- music: alternate A1/A2, each section 2 s longer so you can crossfade the seams
    infos = []
    for i, s in enumerate(plan["songs"]):
        it = items.get(key(s["path"]))
        if not it:
            print("Song fehlt im Media Pool:", s["path"]); continue
        tail = 2.0 if i < len(plan["songs"]) - 1 else 0.0
        infos.append({"mediaPoolItem": it, "startFrame": fr(s["seg_start"]),
                      "endFrame": fr(min(s["duration"], s["seg_end"] + tail)) - 1,
                      "trackIndex": 1 + (i % 2), "recordFrame": t0 + fr(s["tl_start"]), "mediaType": 2})
    # --- video
    for sh in shots:
        it = items.get(key(sh["clip"]))
        if not it:
            print("Clip fehlt im Media Pool:", sh["clip"]); continue
        src_fps = float(it.GetClipProperty("FPS") or FPS)
        a = int(round(sh["src_in"] * src_fps))
        b = max(a + 1, int(round(sh["src_out"] * src_fps)) - 1)
        infos.append({"mediaPoolItem": it, "startFrame": a, "endFrame": b,
                      "trackIndex": 2 if sh["kind"] == "lipsync" else 1,
                      "recordFrame": t0 + fr(sh["tl_in"]), "mediaType": 1})   # video only

    placed = 0
    for i in range(0, len(infos), 100):
        res = mp.AppendToTimeline(infos[i:i + 100]) or []
        placed += len(res)
    print(f"Timeline '{tl.GetName()}': {placed}/{len(infos)} Elemente gesetzt, "
          f"{plan['total_seconds']/60:.1f} min, {W}x{H} @ {FPS} fps")

    # song-change markers
    for s in plan["songs"]:
        tl.AddMarker(fr(s["tl_start"]), "Blue", s["title"], f"{s['bpm']:.1f} BPM", 1)

    if ADD_RENDER_JOB:
        out_dir = os.path.dirname(os.path.abspath(plan_path))
        proj.SetCurrentRenderFormatAndCodec("mp4", "H264")
        proj.SetRenderSettings({"SelectAllFrames": True, "TargetDir": out_dir,
                                "CustomName": "Party_Megamix_Eva_Technogirls_1080p",
                                "FormatWidth": W, "FormatHeight": H, "FrameRate": float(FPS)})
        job = proj.AddRenderJob()
        print("Render-Job angelegt:", job, "->", out_dir)
        if START_RENDER and job:
            proj.StartRendering(job)
    pm.SaveProject()
    resolve.OpenPage("edit")


main()
