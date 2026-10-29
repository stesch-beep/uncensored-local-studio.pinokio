"""Finding songs on the PC (Downloads, Suno folder, project drives) and growing the playlist.

A playlist entry can be a path, {"file": ...} or {"find": "Symphonie und Odyssee"}.
"find" entries are matched by name in the search folders; the first match is
pinned in arbeitsordner/song_fundorte.json so later builds (and appended songs)
always use the same file.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path

from .config import AUDIO_EXTENSIONS, ConfigError, Project, Song, parse_song_name

SKIP_DIRS = {"$recycle.bin", "system volume information", "node_modules", ".git", "env", "venv", ".venv",
             "site-packages", "__pycache__", "windows", "program files", "program files (x86)"}


def normalize(text: str) -> str:
    text = str(text).lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", text)


def search_folders(project: Project, extra: str | None = None) -> list[Path]:
    out: list[Path] = []
    for value in ([extra] if extra else []) + list(project.get("song_search") or []):
        p = project.path(value)
        if p and p.is_dir() and p.resolve() not in [q.resolve() for q in out]:
            out.append(p)
    return out


def audio_files(folders: list[Path], depth: int) -> list[tuple[int, Path]]:
    """(folder rank, file) for every audio file up to `depth` levels below each folder."""
    seen: set[str] = set()
    found: list[tuple[int, Path]] = []
    for rank, root in enumerate(folders):
        base_depth = len(root.parts)
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            here = Path(dirpath)
            if len(here.parts) - base_depth >= depth:
                dirnames[:] = []
            dirnames[:] = [d for d in dirnames if d.lower() not in SKIP_DIRS and not d.startswith(".")]
            for name in filenames:
                path = here / name
                if path.suffix.lower() in AUDIO_EXTENSIONS:
                    key = os.path.normcase(str(path.resolve()))
                    if key not in seen:
                        seen.add(key)
                        found.append((rank, path))
            if len(found) > 20000:
                return found
    return found


def find_song(project: Project, term, folder: str | None = None) -> tuple[Path | None, list[Path]]:
    """Best match for a name (or the first of several alternative spellings that matches)."""
    if isinstance(term, (list, tuple)):
        for alternative in term:
            found, others = find_song(project, alternative, folder)
            if found:
                return found, others
        return None, []
    wanted = normalize(term)
    depth = int(project.get("song_search_depth") or 3)
    matches = []
    for rank, path in audio_files(search_folders(project, folder), depth):
        name = normalize(path.stem)
        if wanted and wanted in name:
            exact = 0 if name == wanted else 1
            matches.append(((exact, path.suffix.lower() != ".wav", rank, len(name)), path))
    matches.sort(key=lambda m: m[0])
    paths = [p for _, p in matches]
    return (paths[0] if paths else None), paths[1:6]


_warned: set[str] = set()


def _lock_file(project: Project) -> Path:
    return project.work_dir / "song_fundorte.json"


def _entry_key(entry: dict) -> str:
    return json.dumps({"find": entry.get("find"), "folder": entry.get("folder")}, sort_keys=True)


def resolve_playlist(project: Project) -> list[Song]:
    entries = project.get("songs") or []
    lock_path = _lock_file(project)
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.is_file() else {}
    changed = False
    default_artist = project.get("default_artist") or ""
    songs: list[Song] = []
    missing: list[str] = []
    seen: set[str] = set()

    def add(path: Path, entry: dict) -> None:
        key = os.path.normcase(str(path.resolve()))
        if key in seen:  # e.g. a song named by "find" that is also in an "all_in" folder
            return
        seen.add(key)
        title, artist = parse_song_name(path)
        songs.append(Song(
            path, entry.get("title") or title, entry.get("artist", artist or default_artist),
            explicit=bool(entry.get("title")),
        ))

    for entry in entries:
        if isinstance(entry, str):
            entry = {"file": entry}
        if entry.get("skip"):
            continue
        if entry.get("all_in"):
            # Every song in a folder. The order is pinned on first use; files added later go to the end,
            # so appending songs leaves the start of the video unchanged.
            folder = project.path(entry["all_in"])
            if not folder or not folder.is_dir():
                missing.append(f"Ordner {entry['all_in']}")
                continue
            key = json.dumps({"all_in": entry["all_in"]})
            pinned = [Path(p) for p in lock.get(key, []) if Path(p).is_file()]
            present = sorted((p for p in folder.iterdir() if p.suffix.lower() in AUDIO_EXTENSIONS),
                             key=lambda p: p.name.lower())
            known = {os.path.normcase(str(p.resolve())) for p in pinned}
            new = [p for p in present if os.path.normcase(str(p.resolve())) not in known]
            if new:
                print(f"  {len(new)} Song(s) aus {folder} " + ("dazu." if pinned else "gefunden."))
                lock[key] = [str(p) for p in pinned + new]
                changed = True
            for path in pinned + new:
                add(path, {})
            continue
        path = project.path(entry.get("file"))
        if entry.get("find"):
            key = _entry_key(entry)
            pinned = Path(lock[key]) if key in lock else None
            if pinned and pinned.is_file():
                path = pinned
            else:
                path, others = find_song(project, entry["find"], entry.get("folder"))
                label = entry["find"] if isinstance(entry["find"], str) else " / ".join(entry["find"])
                if not path:
                    # Not downloaded yet: skip it for now, it joins the video once the file is there.
                    missing.append(label)
                    continue
                print(f"  Song '{label}' gefunden: {path}")
                for other in others:
                    print(f"      (weitere Treffer: {other})")
                lock[key] = str(path)
                changed = True
        if not path or not path.is_file():
            raise ConfigError(f"Song nicht gefunden: {entry.get('file') or entry.get('find')}")
        add(path, entry)
    new_missing = [m for m in missing if m not in _warned]
    if new_missing:
        folders = ", ".join(str(p) for p in search_folders(project)) or "keine"
        for label in new_missing:
            print(f"  HINWEIS: Song '{label}' noch nicht gefunden – wird übersprungen, bis die Datei da ist.")
        print(f"     (gesucht in: {folders})")
        _warned.update(new_missing)
    if changed:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False), encoding="utf-8")
    if not songs:
        folder = project.path(project.get("songs_folder"))
        if folder and folder.is_dir():
            for path in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
                if path.suffix.lower() in AUDIO_EXTENSIONS:
                    title, artist = parse_song_name(path)
                    songs.append(Song(path, title, artist or default_artist))
    if not songs and missing:
        raise ConfigError(
            f"Keiner der Songs gefunden ({', '.join(missing)}). WAV/MP3 in einen der Suchordner legen "
            "(z. B. C:/Download/suno) oder den Ordner unter \"song_search\" ergänzen."
        )
    if not songs:
        raise ConfigError(
            "Keine Songs gefunden. Trage sie in projekt.json unter \"songs\" ein (z. B. {\"find\": \"Songname\"}) "
            f"oder lege Dateien in den Ordner '{project.get('songs_folder')}'."
        )
    return songs


def append_to_config(config_path: Path, project: Project, new_files: list[Path]) -> int:
    """Append songs to projekt.json (everything else stays as it is)."""
    raw = json.loads(config_path.read_text(encoding="utf-8-sig"))
    try:
        current = project.songs()
    except ConfigError:
        current = []
    entries = list(raw.get("songs") or [])
    if not entries:
        # The playlist so far came from songs_folder: keep those songs in front.
        entries = [{"file": str(s.path)} for s in current]
    existing = {os.path.normcase(str(s.path.resolve())) for s in current}
    added = 0
    for path in new_files:
        key = os.path.normcase(str(path.resolve()))
        if key in existing:
            print(f"  schon in der Playlist: {path.name}")
            continue
        entries.append({"file": str(path)})
        existing.add(key)
        added += 1
    raw["songs"] = entries
    config_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added
