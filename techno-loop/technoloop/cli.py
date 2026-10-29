"""Command line: szenen (Maestro), bauen (1-hour video), demo, info."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import ConfigError, load_project


def _parse_time(value: str) -> float:
    parts = [float(p) for p in str(value).split(":")]
    seconds = 0.0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def _fmt(t: float, long: bool) -> str:
    t = int(t)
    h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if long else f"{m:02d}:{s:02d}"


def write_description(project, timeline, duration: float, path: Path) -> None:
    from .montage import song_switch_times

    long = duration >= 3600
    lines = ["Tracklist:"]
    for t, entry in zip(song_switch_times(timeline), timeline):
        lines.append(f"{_fmt(t, long)} {entry.display}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_scenes(args) -> int:
    from .maestro import render_scenes

    project = load_project(args.projekt)
    failures = render_scenes(project, only=args.nur, force=args.neu, dry_run=args.test, url=args.url)
    return 1 if failures else 0


def _prepare(project, fresh_cut: bool = False):
    from .audio import build_mix, analyze
    from .montage import collect_clips, describe, plan_edl, reusable_prefix, save_edl

    mix = build_mix(project)
    analysis = analyze(project, mix)
    clips = collect_clips(project)
    state = project.work_dir / "render"
    state.mkdir(parents=True, exist_ok=True)
    prefix = [] if fresh_cut else reusable_prefix(
        state / "edl.json", project, clips, mix.timeline, mix.crossfade, mix.end_fade)
    if prefix:
        print(f"Schnitt der ersten {_fmt(prefix[-1].t1, prefix[-1].t1 >= 3600)} bleibt wie beim letzten Mal "
              f"({len(prefix)} Schnitte), nur der Rest wird neu geplant.")
    segments = plan_edl(project, clips, analysis, mix.timeline, prefix)
    analysis.save(state / "analysis.npz")
    save_edl(state / "edl.json", clips, segments, project, mix.timeline, mix.crossfade, mix.end_fade)
    (state / "timeline.json").write_text(
        json.dumps([e.__dict__ for e in mix.timeline], indent=2, ensure_ascii=False), encoding="utf-8")
    print(describe(clips, segments))
    return mix, analysis, clips, segments, state


def cmd_build(args) -> int:
    from .render import default_workers, render_video

    project = load_project(args.projekt)
    if args.workers:
        project.data["video"]["workers"] = args.workers
    mix, analysis, clips, segments, state = _prepare(project, fresh_cut=args.neu_schneiden)
    fps = analysis.fps
    f0, f1 = 0, analysis.n_frames
    name = project["name"]
    if args.vorschau:
        f0 = int(_parse_time(args.ab) * fps) if args.ab else 0
        f1 = min(analysis.n_frames, f0 + int(float(args.vorschau) * fps))
        name += "_vorschau"
    out_dir = project.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{name}.mp4"
    if not args.vorschau:
        desc = out_dir / f"{project['name']}_youtube_beschreibung.txt"
        write_description(project, mix.timeline, mix.duration, desc)
        print(f"YouTube-Kapitel/Tracklist: {desc}")
    render_video(project, str(Path(args.projekt).resolve()), state, mix.path, out, f0, f1, default_workers(project),
                 use_cache=not args.vorschau)
    print(f"\nFERTIG: {out}")
    return 0


def cmd_resolve(args) -> int:
    from .render import default_workers
    from .resolve import export_resolve

    project = load_project(args.projekt)
    mix, analysis, clips, segments, state = _prepare(project)
    out = export_resolve(project, str(Path(args.projekt).resolve()), state, mix, clips, segments,
                         analysis.n_frames, default_workers(project))
    print(f"\nFERTIG: {out}\nAnleitung: {out / 'LIESMICH_Resolve.txt'}")
    return 0


def cmd_info(args) -> int:
    from .maestro import scene_mode

    project = load_project(args.projekt)
    print(f"Projekt: {project['name']}  (Arbeitsordner {project.work_dir})")
    songs = project.songs()
    print(f"{len(songs)} Songs:")
    for s in songs:
        print(f"    {s.display}")
    print(f"{len(project['scenes'])} Szenen:")
    for sc in project["scenes"]:
        n = len(list(project.scenes_dir.glob(f"{sc['id']}__v*.mp4"))) if project.scenes_dir.is_dir() else 0
        print(f"    {sc['id']:<22} {scene_mode(project, sc):<9} {n} Clip(s) fertig")
    return 0


def cmd_keyframes(args) -> int:
    from .keyframes import make_keyframes

    project = load_project(args.projekt)
    failures = make_keyframes(project, only=args.nur, force=args.neu, dry_run=args.test, url=args.url)
    return 1 if failures else 0


def _candidates(project, term: str | None):
    import os

    from .songs import audio_files, normalize, search_folders

    try:
        used = {os.path.normcase(str(s.path.resolve())) for s in project.songs()}
    except ConfigError:
        used = set()
    files = [p for _, p in audio_files(search_folders(project), int(project.get("song_search_depth") or 3))]
    if term:
        files = [p for p in files if normalize(term) in normalize(p.stem)]
    return files, used


def cmd_songs(args) -> int:
    import os

    project = load_project(args.projekt)
    files, used = _candidates(project, " ".join(args.suche) if args.suche else None)
    if not files:
        print("Keine Audiodateien gefunden. Ordner unter \"song_search\" in projekt.json prüfen.")
        return 1
    for i, path in enumerate(files, 1):
        mark = "  [in Playlist]" if os.path.normcase(str(path.resolve())) in used else ""
        print(f"{i:4d}  {path.name:<55} {path.parent}{mark}")
    return 0


def cmd_add_song(args) -> int:
    import os

    from .songs import append_to_config, find_song

    config_path = Path(args.projekt).resolve()
    project = load_project(config_path)
    chosen: list[Path] = []
    if args.suche:
        for term in args.suche:
            path, others = find_song(project, term)
            if not path:
                print(f"Nicht gefunden: {term}")
                continue
            print(f"Gefunden: {path}")
            for other in others:
                print(f"    (weitere Treffer: {other})")
            chosen.append(path)
    else:
        files, used = _candidates(project, None)
        files = [p for p in files if os.path.normcase(str(p.resolve())) not in used]
        if not files:
            print("Keine weiteren Songs in den Suchordnern gefunden.")
            return 1
        for i, path in enumerate(files, 1):
            print(f"{i:4d}  {path.name:<55} {path.parent}")
        answer = input("\nNummer(n) der Songs zum Anhängen (z. B. 3 oder 3,5,7), Enter = abbrechen: ").strip()
        for part in answer.replace(";", ",").split(","):
            if part.strip().isdigit() and 1 <= int(part) <= len(files):
                chosen.append(files[int(part) - 1])
    if not chosen:
        print("Nichts angehängt.")
        return 1
    added = append_to_config(config_path, project, chosen)
    songs = load_project(config_path).songs()
    print(f"\n{added} Song(s) angehängt. Playlist jetzt ({len(songs)}):")
    for i, s in enumerate(songs, 1):
        print(f"  {i:2d}. {s.display}")
    print("\nJetzt '3_video_bauen.bat' starten – die schon gerenderten Teile werden wiederverwendet.")
    return 0


def cmd_demo(args) -> int:
    from .demo import make_demo

    target = Path(args.ordner).resolve()
    make_demo(target)
    print(f"\nDemo-Projekt angelegt: {target}\nTesten mit:\n  python -m technoloop bauen \"{target / 'projekt.json'}\"")
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:  # Pinokio / piped Windows consoles default to cp1252
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(prog="technoloop", description="1-Stunden-Techno-Loop-Video aus Maestro-H3-Szenen")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("keyframes", aliases=["bilder"],
                       help="Standbilder der Girls pro Szene erzeugen (Maestro Krea 2 Identity Edit oder ComfyUI)")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.add_argument("--nur", nargs="+", help="nur diese Szenen-ids")
    p.add_argument("--neu", action="store_true", help="vorhandene Keyframes neu erzeugen")
    p.add_argument("--test", action="store_true", help="nur Prompts anzeigen")
    p.add_argument("--url", help="Maestro-Adresse (überschreibt projekt.json)")
    p.set_defaults(func=cmd_keyframes)

    p = sub.add_parser("szenen", aliases=["scenes"], help="Szenen mit Maestro (MiniMax H3) rendern")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.add_argument("--nur", nargs="+", help="nur diese Szenen-ids")
    p.add_argument("--neu", action="store_true", help="vorhandene Clips neu rendern")
    p.add_argument("--test", action="store_true", help="nur Prompts/Parameter anzeigen, nichts senden")
    p.add_argument("--url", help="Maestro-Adresse (überschreibt projekt.json)")
    p.set_defaults(func=cmd_scenes)

    p = sub.add_parser("bauen", aliases=["build"], help="Musik mischen, schneiden und das lange Video rendern")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.add_argument("--vorschau", type=float, metavar="SEKUNDEN", help="nur einen kurzen Ausschnitt rendern")
    p.add_argument("--ab", metavar="MM:SS", help="Startzeit der Vorschau")
    p.add_argument("--workers", type=int, help="parallele Render-Prozesse")
    p.add_argument("--neu-schneiden", action="store_true",
                   help="Schnitt komplett neu planen (sonst bleibt der Anfang wie beim letzten Mal)")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("resolve", help="Export für DaVinci Resolve: Schnittliste (EDL), Overlay mit Alpha, Musik-WAV")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("info", help="Songs, Szenen und fertige Clips anzeigen")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("lieder", aliases=["songs"], help="Songs in den Suchordnern auflisten")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.add_argument("--suche", nargs="+", help="nur Dateien mit diesem Namen")
    p.set_defaults(func=cmd_songs)

    p = sub.add_parser("song-dazu", aliases=["add-song"], help="Songs hinten an die Playlist anhängen")
    p.add_argument("projekt", nargs="?", default="projekt.json")
    p.add_argument("--suche", nargs="+", help="Songnamen (sonst Auswahlliste)")
    p.set_defaults(func=cmd_add_song)

    p = sub.add_parser("demo", help="Test-Projekt mit künstlicher Musik und Test-Clips anlegen")
    p.add_argument("ordner", nargs="?", default="demo")
    p.set_defaults(func=cmd_demo)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ConfigError as error:
        print(f"\nFEHLER in der Projektdatei: {error}")
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        return 130
    except Exception as error:  # surfaced plainly for non-programmers; --debug not needed
        from .ffmpeg_tools import FFmpegError
        from .maestro import MaestroError

        if isinstance(error, (FFmpegError, MaestroError, FileNotFoundError)):
            print(f"\nFEHLER: {error}")
        else:
            raise
    return 1


if __name__ == "__main__":
    sys.exit(main())
