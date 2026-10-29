# Techno Loop – 1-Stunden-Musikvideo aus wenigen KI-Szenen

Baut ein ca. 60 Minuten langes YouTube-Video im Stil großer Festival-Bühnen (riesige
Schildkröten-Bühne, Crowd mit erhobenen Händen, Laser, blau/rotes Licht), mit deinen
**zwei Techno-Girls** als DJs, **Lautsprechern, deren Membranen im Takt des Basses springen**,
und **ca. 15 Songs**, deren **Titel immer eingeblendet** sind.

Du generierst dafür **keine Stunde Videomaterial**, sondern nur etwa **10 Szenen × 2 Varianten
à ~7 Sekunden** mit **Maestro** und **MiniMax H3 (Turbo, 4 Schritte)** auf deiner RTX 5080.
Das Tool schneidet daraus eine Stunde, die nicht nach Dauerschleife aussieht.

```
 Maestro + H3 Turbo (4 Steps)          Techno Loop (dieses Tool)
 ┌──────────────────────────┐         ┌──────────────────────────────────────────┐
 │ 10 Szenen × 2 Varianten  │  MP4s   │ 15 Songs → Mix mit Crossfades, -14 LUFS  │
 │ je 175 Frames (7,3 s)    ├────────►│ Beat-/Bass-Analyse                       │
 │ 1280×704, Keyframe-Loops │         │ Schnitt auf den Beat, hunderte Schnitte  │
 └──────────────────────────┘         │ + pumpende Lautsprecher + Songtitel      │
                                      │ → 1080p-MP4 (NVENC) + YouTube-Kapitel    │
                                      └──────────────────────────────────────────┘
```

## Warum man die Schleife nicht merkt

- **Musik wiederholt sich nicht** – 15 echte Songs mit Crossfades (die Musik ist das, was man wirklich bemerken würde).
- **Jeder Schnitt sitzt auf dem Beat**: in Drops alle 1–2 Takte, in Breakdowns alle 4–8 Takte, beim Songwechsel ein Blitz-Schnitt.
- **Keine Einstellung zweimal hintereinander**, keine Szene direkt nach sich selbst, selten benutzte Clips werden bevorzugt.
- **Jede Verwendung eines Clips ist anders**: anderer Startpunkt, Tempo 92–108 %, teils rückwärts, gespiegelt, langsamer Zoom/Schwenk, eine von 6 Farbstimmungen.
- **Licht und Bild pumpen mit der Kickdrum** (leichter Zoom + Helligkeit), Blitz-Übergänge, Filmkorn und Vignette verbinden die Clips.
- **Nahtlose Loop-Clips**: Hat eine Szene ein Keyframe-Bild, bekommt H3 dasselbe Bild als **ersten und letzten Frame** – der Clip endet exakt dort, wo er beginnt.

Die Lautsprecher sind **kein KI-Video**, sondern werden passend zur echten Musik gerendert:
Die Bass-Hüllkurve (35–130 Hz) treibt ein gedämpftes Feder-Modell → die Membran springt bei jeder
Kick nach vorn, federt zurück, die Staubschutzkappe bewegt sich mit, der LED-Ring leuchtet mit
dem Bass, der Hochtöner zittert mit den Hi-Hats.

## Voraussetzungen

- **Maestro** in Pinokio (Version mit **MiniMax H3**, ab v1.6.5), Modell *H3 First / Last – Pruned* und
  *H3 Omni – Pruned* in den Maestro-Einstellungen sichtbar. Beim ersten Clip lädt Maestro die
  H3-Gewichte und die Turbo-LoRA automatisch (viele GB, dauert einmalig).
- **Python 3.10+** (python.org, oder das Python aus Pinokio wird automatisch genommen)
- **ffmpeg** – am besten `winget install Gyan.FFmpeg` (dann wird die RTX 5080 per **NVENC** zum Kodieren benutzt).
  Ohne ffmpeg im PATH wird ein mitinstalliertes ffmpeg benutzt; fehlt dort NVENC, wird automatisch auf CPU (x264) umgeschaltet.
- RAM: pro Render-Prozess ca. 2 GB (Standard: 3 Prozesse).

## Einrichtung (einmalig)

1. `setup.bat` doppelklicken. Legt `.venv`, `projekt.json`, `musik\` und `bilder\` an.
2. **Songs** nach `musik\` kopieren. Der Titel kommt aus den MP3-Tags oder aus dem Dateinamen:
   `01 - Künstler - Songtitel.mp3` → „KÜNSTLER / SONGTITEL“. Reihenfolge = alphabetisch nach Dateiname
   (oder `"shuffle": true`). Alternativ in `projekt.json` unter `"songs"` explizit eintragen:
   ```json
   "songs": [{"file": "musik/track1.mp3", "artist": "Nova & Mila", "title": "Turtle Stage"}]
   ```
3. **Bilder** nach `bilder\`:
   - `girl1.png`, `girl2.png` – je ein gutes Bild deiner beiden Girls (für Identität/Wiedererkennung).
   - optional `vorbild.jpg` – z. B. das Pinterest-Bild als Stil-Referenz (Bühne, Licht, Farben).
   - optional Keyframes, z. B. `keyframe_dj_pult.png` – ein fertiges Standbild der Szene mit beiden Girls
     (in Maestro im Bild-Modus erstellt, z. B. mit Qwen Image Edit / Flux Klein aus den beiden Girl-Fotos).
4. In `projekt.json` die `look`-Beschreibung der Girls anpassen (Haare, Outfit) – die steht in jedem Prompt.

## Ablauf

| Schritt | Datei | Was passiert |
|---|---|---|
| 0 (optional) | `demo_test.bat` | Testlauf ohne Maestro mit künstlicher Musik – prüft ffmpeg/NVENC und den ganzen Ablauf |
| 1 | `1_szenen_rendern.bat` | Schickt alle Szenen an Maestro (MiniMax H3), wartet, lädt die Clips nach `arbeitsordner\szenen\` |
| 2 | `2_vorschau.bat` | Rendert 2 Minuten ab Minute 5 → `ausgabe\..._vorschau.mp4` zum Prüfen |
| 3 | `3_video_bauen.bat` | Rendert das komplette Video → `ausgabe\techno_girls_1h.mp4` + `..._youtube_beschreibung.txt` |

**Maestro muss bei Schritt 1 laufen.** Die Adresse wird automatisch gesucht (`"url": "auto"`).
Klappt das nicht, die Adresse aus Maestros *Open Web UI* in `projekt.json` eintragen, z. B. `"url": "http://127.0.0.1:42003"`.

Nützliche Optionen (an die .bat anhängen oder in der Konsole):

```
1_szenen_rendern.bat --test                  nur Prompts/Parameter anzeigen, nichts rendern
1_szenen_rendern.bat --nur dj_pult pyro_drop nur diese Szenen
1_szenen_rendern.bat --neu --nur dj_pult     vorhandene Clips dieser Szene neu rendern
2_vorschau.bat --ab 30:00                    Vorschau ab Minute 30
3_video_bauen.bat --workers 4                mehr parallele Render-Prozesse
```

Gefällt dir ein Clip nicht: einfach die MP4 in `arbeitsordner\szenen\` löschen und Schritt 1 erneut starten –
fertige Clips werden übersprungen. Eigene fertige Clips (z. B. direkt in Maestro erzeugt) kannst du in
einen Ordner legen und unter `"clips_folder"` eintragen; Dateinamen mit `loop` gelten als nahtlose Loops.

## Wie „H3 Steps4“ benutzt wird

- Gibt es in Maestro ein gespeichertes **Preset mit dem Namen aus `maestro.preset`** (Standard: `H3 Steps4`),
  übernimmt das Tool dessen **Schritte, LoRAs und Parameter**.
- Sonst: H3 mit der **Turbo-LoRA** `minimax_h3_turbo_4step_ckpt500.safetensors`, **4 Schritte**, Stärke `0.70`
  (`maestro.steps`, `maestro.turbo_strength`). Maestros eigener Turbo-Haken nimmt immer 6 Schritte –
  deshalb gibt das Tool die LoRA direkt mit 4 Schritten an.
- Auflösung `1280x704` (H3-720p), `175` Frames (7,3 s @ 24 fps). H3 akzeptiert nur 17·n+5 Frames (124, 141, …, 243);
  das Tool rundet passend. Mit 16 GB VRAM passt das in ein H3-Fenster.

## Szenen (projekt.json → `scenes`)

```json
{
  "id": "dj_pult",
  "girls": true,                         // true = beide, [0] = Girl 1, [1] = Girl 2, weglassen = ohne Girls
  "keyframe": "bilder/keyframe_dj_pult.png",
  "tags": ["girls"],
  "action": "Behind a huge glowing DJ booth ... The camera slowly pushes in."
}
```

(Die `//`-Kommentare dienen nur der Erklärung – JSON erlaubt keine Kommentare.)

Modus wird automatisch gewählt:

| vorhanden | H3-Modell | Ergebnis |
|---|---|---|
| `keyframe`-Bild | First / Last (`minimax_h3`) | Keyframe = erster **und** letzter Frame → **nahtloser Loop** |
| nur Girl-Bilder | Omni Reference (`minimax_h3_ref2va`) | Girls werden aus den Bildern wiedererkannt (+ `vorbild.jpg` als Stil) |
| nichts | First / Last, nur Text | Szenen ohne Girls (Crowd, Laser, Bühne) |

Prompts am besten auf Englisch. Das Tool baut daraus H3s Prompt-Format (Context-IR) inklusive
„niemand spricht“, damit H3 keine Lippenbewegungen erfindet. Der Ton von H3 wird verworfen.
Weitere Szenen-Optionen: `frames`, `variants`, `weight` (wie oft sie vorkommt), `reverse_ok`, `mirror_ok`,
`loop`, `prompt` (kompletter eigener Prompt), `extra_params` (wird direkt an Maestro durchgereicht), `skip`.

## Wichtige Einstellungen

| Bereich | Schlüssel | Standard | Bedeutung |
|---|---|---|---|
| audio | `duration_minutes` | 60 | Mindestlänge; ist die Playlist kürzer, werden Songs wiederholt |
| audio | `crossfade_seconds` | 6 | Überblendung zwischen Songs |
| audio | `target_lufs` | -14 | YouTube-Lautheit, alle Songs gleich laut |
| video | `width`/`height`/`fps` | 1920/1080/24 | 24 fps = H3-Bildrate (kein Ruckeln) |
| video | `codec` | h264 | `hevc` oder `av1` gehen mit der RTX 5080 auch |
| video | `workers` | 3 | parallele Render-Prozesse |
| montage | `cut_beats_high` / `cut_beats_low` | [4,8,8,16] / [8,16,16,32] | Schnittlängen in Beats (Drop / Breakdown) |
| montage | `zoom_range`, `speed_range`, `mirror`, `reverse_chance` | | Variationen pro Einstellung |
| montage | `bass_zoom`, `light_pump`, `flash_chance` | 0.02, 0.12, 0.12 | wie stark das Bild zur Kick pumpt |
| speakers | `size`, `positions`, `excursion` | 0.40, links+rechts unten, 0.085 | Größe, Position, Membranhub |
| speakers | `led_colors` | cyan, rot | LED-Ringe |
| speakers | `image` + `cone` | – | eigenes Lautsprecher-PNG, `cone` = [x, y, radius] der Membran (relativ) |
| titles | `position` | bottom-center | auch `top-left`, `bottom-left`, `top-center` |
| titles | `intro_card`, `label`, `accent`, `watermark` | | große Titel-Einblendung pro Song, Texte/Farbe, Kanalname |

## YouTube

- `ausgabe\..._youtube_beschreibung.txt` enthält die **Tracklist mit Zeitstempeln** – in die Videobeschreibung
  kopieren, dann erzeugt YouTube automatisch Kapitel.
- Tipp: Für bessere YouTube-Qualität kann man in `1440p` (`2560x1440`) rendern – YouTube vergibt dafür eine höhere Bitrate.
- Du brauchst die **Rechte an den Songs** (eigene Tracks oder lizenziert), sonst greift Content ID.

## Fehlerbehebung

- **„Maestro ist nicht erreichbar“** – Maestro in Pinokio starten, Adresse aus *Open Web UI* in `maestro.url` eintragen.
- **GPU-Speicher voll (OOM)** – `maestro.frames` auf `124` senken oder `resolution` auf `"864x480"`.
- **Preset nicht gefunden** – Name in `maestro.preset` muss genau dem Preset-Namen in Maestro entsprechen (Groß/Klein egal).
- **Girls sehen in jedem Clip anders aus** – `girls[].image` angeben (Omni) oder Keyframes mit beiden Girls verwenden.
- **Zu langsam / zu viel RAM** – `video.workers` anpassen, `video.clip_cache` (Clips pro Prozess im RAM, Standard 4).
- **Encoder-Fehler** – `video.encoder` auf `"libx264"` setzen.

## Für Entwickler

```
python -m technoloop szenen|bauen|info|demo [projekt.json]
python -m unittest discover -s tests
```

Module: `maestro.py` (Maestro-REST-API: `/api/v1/upload`, `/generate`, `/status`, `/file`, `/presets`),
`audio.py` (Mix + Beat/Bass-Analyse, nur numpy), `montage.py` (Schnittplan), `speakers.py`, `titles.py`,
`render.py` (Frame-Renderer, parallele Teil-Encodes, Zusammenfügen ohne Neukodierung).
