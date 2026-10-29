# Techno Loop – 1-Stunden-Musikvideo aus wenigen KI-Szenen

Baut ein langes YouTube-Musikvideo (Ziel: ca. 60 Minuten / ca. 15 Songs) im Stil großer Festival-Bühnen
(riesige Schildkröten-Bühne, Crowd mit erhobenen Händen, Laser, blau/rotes Licht), mit deinen
**zwei Techno-Girls** als DJs, **Lautsprechern, deren Membranen im Takt des Basses springen**,
und Songs, deren **Titel immer eingeblendet** sind. Song 1 ist **„Symphonie und Odyssee“**;
weitere Songs werden einfach **hinten angebaut** – dabei wird nur der neue Teil gerendert.

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

- **Maestro** in Pinokio, am besten aktuell (3.x, in Pinokio „Update“): Modelle *H3 Fused 4-Step – Frames*,
  *H3 Fused 4-Step – References* und *Qwen Image 2.1* in den Maestro-Einstellungen sichtbar schalten.
  Beim ersten Mal lädt Maestro die Gewichte automatisch (viele GB, dauert einmalig).
  Ältere Maestro-Versionen gehen auch: dann nimmt das Tool automatisch H3 *First / Last* + Turbo-LoRA und
  Krea 2 für die Keyframes.
- **Python 3.10+** (python.org, oder das Python aus Pinokio wird automatisch genommen)
- **ffmpeg** – am besten `winget install Gyan.FFmpeg` (dann wird die RTX 5080 per **NVENC** zum Kodieren benutzt).
  Ohne ffmpeg im PATH wird ein mitinstalliertes ffmpeg benutzt; fehlt dort NVENC, wird automatisch auf CPU (x264) umgeschaltet.
- RAM: pro Render-Prozess ca. 2 GB (Standard: 3 Prozesse).

## Einrichtung (einmalig)

1. `setup.bat` doppelklicken. Legt `.venv`, `projekt.json`, `musik\` und `bilder\` an.
2. **Songs**: In `projekt.json` steht schon die Playlist:
   ```json
   "songs": [
     {"find": "Symphonie und Odyssee"},
     {"find": "Accordion Rave Bounce 153"},
     {"find": "Tubular Bells of Berlin"},
     {"find": "Ocarina of the Underground"},
     {"find": ["Didgeridoo", "Digeridoo", "Diggeridoo", "Didjeridoo", "Didgeridu", "Didjeridu"]}
   ]
   ```
   Eine Liste bei `find` = verschiedene Schreibweisen, die erste passende Datei wird genommen.
   Ist ein Song noch nicht heruntergeladen, wird er mit einem Hinweis übersprungen und kommt automatisch
   dazu, sobald die Datei im Suchordner liegt.
   `find` sucht die Datei (WAV/MP3/FLAC, Groß/Klein, Umlaute und `_` egal) in den Ordnern unter
   `"song_search"`: `musik\`, `Downloads`, `Downloads\suno`, `C:\Download`, `C:\Download\suno` und
   `F:\Pinokio Projekt Fire und ice` (bis 3 Ordner tief). Der Fundort wird in
   `arbeitsordner\song_fundorte.json` gemerkt. Liegt der Song woanders, den Ordner in `song_search`
   ergänzen oder direkt `{"file": "F:/…/Symphonie und Odyssee.wav"}` eintragen.
   Der angezeigte Titel kommt aus den Datei-Tags oder dem Dateinamen (`01 - Künstler - Titel.wav`;
   ein angehängtes „ (1)“ von Suno-Downloads wird weggelassen). Künstler für alle Songs ohne eigenen:
   `"default_artist"`. Titel/Künstler pro Song festlegen: `{"find": "…", "title": "…", "artist": "…"}`.
3. **Bilder** nach `bilder\`:
   - `girl1.png`, `girl2.png` – je ein gutes Bild deiner beiden Girls (für Identität/Wiedererkennung).
   - optional `vorbild.jpg` – z. B. das Pinterest-Bild als Stil-Referenz (Bühne, Licht, Farben).
   - Keyframes (Standbild pro Szene mit den Girls) macht Schritt 0 automatisch nach `bilder\keyframes\<id>.png`.
     Eigene Bilder kannst du dort auch einfach ablegen (Dateiname = Szenen-id), dann werden sie benutzt.
4. In `projekt.json` die `look`-Beschreibung der Girls anpassen (Haare, Outfit) – die steht in jedem Prompt.

## Ablauf

| Schritt | Datei | Was passiert |
|---|---|---|
| Test (optional) | `demo_test.bat` | Testlauf ohne Maestro mit künstlicher Musik – prüft ffmpeg/NVENC und den ganzen Ablauf |
| 0 | `0_keyframes_erstellen.bat` | Standbild pro Girl-Szene aus `girl1.png` + `girl2.png` (Maestro: Qwen Image 2.1) → `bilder\keyframes\` |
| 1 | `1_szenen_rendern.bat` | Schickt alle Szenen an Maestro (MiniMax H3), wartet, lädt die Clips nach `arbeitsordner\szenen\` |
| 2 | `2_vorschau.bat` | Rendert 2 Minuten ab Minute 5 → `ausgabe\..._vorschau.mp4` zum Prüfen |
| 3 | `3_video_bauen.bat` | Rendert das komplette Video → `ausgabe\techno_girls_1h.mp4` + `..._youtube_beschreibung.txt` |
| 4 | `4_song_anhaengen.bat` | Listet alle Songs aus den Suchordnern (z. B. `C:\Download\suno`), du wählst per Nummer → danach wieder Schritt 3 |
| 5 (optional) | `5_resolve_export.bat` | Export für **DaVinci Resolve** (siehe „Andere Programme“) |

**Maestro muss bei Schritt 1 laufen.** Die Adresse wird automatisch gesucht (`"url": "auto"`).
Klappt das nicht, die Adresse aus Maestros *Open Web UI* in `projekt.json` eintragen, z. B. `"url": "http://127.0.0.1:42003"`.

Nützliche Optionen (an die .bat anhängen oder in der Konsole):

```
1_szenen_rendern.bat --test                  nur Prompts/Parameter anzeigen, nichts rendern
1_szenen_rendern.bat --nur dj_pult pyro_drop nur diese Szenen
1_szenen_rendern.bat --neu --nur dj_pult     vorhandene Clips dieser Szene neu rendern
2_vorschau.bat --ab 30:00                    Vorschau ab Minute 30
3_video_bauen.bat --workers 4                mehr parallele Render-Prozesse
3_video_bauen.bat --neu-schneiden            Schnitt komplett neu würfeln (sonst bleibt der Anfang gleich)
4_song_anhaengen.bat --suche "Feuer und Eis" Song direkt per Name anhängen
```

## Songs anbauen

1. `4_song_anhaengen.bat` – zeigt alle WAV/MP3 aus den Suchordnern (die schon benutzten sind markiert).
   Nummer(n) eingeben, z. B. `3` oder `3,7,12` – die Songs kommen in dieser Reihenfolge **hinten** an die Playlist.
2. `3_video_bauen.bat` – das Tool merkt sich den Schnitt und alle fertig gerenderten Teile
   (`arbeitsordner\render\teile`, je ca. 2 Minuten). Neu gerendert wird nur ab dem Übergang in den
   neuen Song (plus der eine Teil, in dem vorher das Ende ausgeblendet wurde). Der Anfang des Videos
   bleibt Bild für Bild gleich, neue Szenen-Clips tauchen erst im neuen Teil auf.

Die Videolänge ergibt sich aus den Songs (`"duration_minutes": 0`). Die Songnummer wird ohne
Gesamtzahl eingeblendet („NOW PLAYING · 03“), damit sich frühere Teile beim Anbauen nicht ändern
(`"titles": {"show_total": true}` zeigt „03 / 15“, dann rendert ein neuer Song aber alles neu).

Songs ohne festen Beat (z. B. orchestrale Stücke) erkennt das Tool automatisch und schneidet dort auf
die stärksten Akzente statt auf ein Beat-Raster.

Gefällt dir ein Clip nicht: einfach die MP4 in `arbeitsordner\szenen\` löschen und Schritt 1 erneut starten –
fertige Clips werden übersprungen. Eigene fertige Clips (z. B. direkt in Maestro erzeugt) kannst du in
einen Ordner legen und unter `"clips_folder"` eintragen; Dateinamen mit `loop` gelten als nahtlose Loops.

## Keyframes der Girls (Schritt 0)

Für jede Szene mit Girls erzeugt `0_keyframes_erstellen.bat` ein Standbild, in dem beide (oder eins) aus
deinen Fotos in der Szene stehen – mit **Qwen Image 2.1** in Maestro (bis zu 10 Referenzbilder, behält
Gesichter, Haare und Outfits; 40 Schritte, schneller: `"model": "qwen_image_21_7B_turbo"` mit 8 Schritten).
Ohne Qwen Image 2.1 nimmt das Tool automatisch Krea 2 Turbo Identity Edit. Mit `"candidates": 2` entsteht zusätzlich `<id>__alt2.png`;
gefällt dir die Variante besser, einfach umbenennen. Unpassendes Bild löschen → beim nächsten Start neu.
Szenen mit Keyframe rendert H3 mit diesem Bild als erstem **und** letztem Frame → nahtloser Loop, und die
Girls sehen in allen Clips gleich aus.

> **Lizenz beachten:** Laut Maestro steht Qwen Image 2.1 unter der *Qwen Research License* – nur für nicht-
> kommerzielle Nutzung. Ist dein YouTube-Kanal monetarisiert, gilt das als kommerziell: dann
> `"model": "krea2_turbo_edit"` nehmen oder die Lizenz bei Qwen klären.

Lieber **ComfyUI** (z. B. mit deinem eigenen Girl-LoRA oder PuLID/FaceID)? Workflow in ComfyUI öffnen,
ins positive Prompt-Feld `{{PROMPT}}` schreiben, mit **Export (API)** speichern und eintragen:
```json
"keyframes": {"engine": "comfyui", "comfyui_url": "http://127.0.0.1:8188", "comfyui_workflow": "bilder/girls_workflow_api.json"}
```
Die beiden ersten `LoadImage`-Knoten bekommen `girl1.png` / `girl2.png` (oder Platzhalter `{{IMAGE1}}`, `{{IMAGE2}}`),
`seed` wird pro Szene gesetzt (oder `{{SEED}}`), Größe über `{{WIDTH}}`/`{{HEIGHT}}`.

## Wie „H3 Steps4“ benutzt wird

- Standard ist **H3 Fused 4-Step** (`minimax_h3_fused_turbo`, für Omni-Szenen `minimax_h3_ref2va_fused_turbo`):
  Turbo steckt schon im Modell, **4 Schritte**, Start- und Endbild werden unterstützt. Eine extra Turbo-LoRA
  lehnt Maestro bei diesen Modellen ab – das Tool lässt sie deshalb weg.
- Gibt es in Maestro ein gespeichertes **Preset mit dem Namen aus `maestro.preset`** (Standard: `H3 Steps4`),
  übernimmt das Tool dessen **Schritte, LoRAs und Parameter** (Turbo-LoRAs werden beim Fused-Modell entfernt).
- Kennt dein Maestro das Fused-Modell nicht (ältere Version), nimmt das Tool automatisch H3 *First / Last* mit der
  **Turbo-LoRA** `minimax_h3_turbo_4step_ckpt500.safetensors`, 4 Schritte, Stärke `0.70`.
- Auflösung `1280x704` (H3-720p), `175` Frames (7,3 s @ 24 fps). H3 akzeptiert nur 17·n+5 Frames (124, 141, …, 243);
  das Tool rundet passend. Mit 16 GB VRAM passt das in ein H3-Fenster.

## Szenen (projekt.json → `scenes`)

```json
{
  "id": "dj_pult",
  "girls": true,                         // true = beide, [0] = Girl 1, [1] = Girl 2, weglassen = ohne Girls
  "keyframe": "bilder/eigenes_bild.png",   // optional, sonst bilder/keyframes/dj_pult.png
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
| audio | `duration_minutes` | 0 | 0 = so lang wie die Songs; sonst Mindestlänge (Songs werden wiederholt – nicht zum Anbauen) |
| audio | `crossfade_seconds` | 6 | Überblendung zwischen Songs |
| audio | `target_lufs` | -14 | YouTube-Lautheit, alle Songs gleich laut |
| video | `width`/`height`/`fps` | 1920/1080/24 | 24 fps = H3-Bildrate (kein Ruckeln) |
| video | `codec` | h264 | `hevc` oder `av1` gehen mit der RTX 5080 auch |
| video | `workers` | 3 | parallele Render-Prozesse |
| video | `chunk_seconds` | 120 | Länge der zwischengespeicherten Teile |
| montage | `cut_beats_high` / `cut_beats_low` | [4,8,8,16] / [8,16,16,32] | Schnittlängen in Beats (Drop / Breakdown) |
| montage | `zoom_range`, `speed_range`, `mirror`, `reverse_chance` | | Variationen pro Einstellung |
| montage | `bass_zoom`, `light_pump`, `flash_chance` | 0.02, 0.12, 0.12 | wie stark das Bild zur Kick pumpt |
| speakers | `size`, `positions`, `excursion` | 0.40, links+rechts unten, 0.085 | Größe, Position, Membranhub |
| speakers | `led_colors` | cyan, rot | LED-Ringe |
| speakers | `image` + `cone` | – | eigenes Lautsprecher-PNG, `cone` = [x, y, radius] der Membran (relativ) |
| resolve | `overlay_codec` | png | `png`, `qtrle`, `prores4444`, `vp9` oder `keins` |
| titles | `position` | bottom-center | auch `top-left`, `bottom-left`, `top-center` |
| titles | `intro_card`, `label`, `accent`, `watermark` | | große Titel-Einblendung pro Song, Texte/Farbe, Kanalname |

## Andere Programme

Maestro bleibt der Generator für die Video-Clips (H3). Die anderen Programme passen so dazu:

- **ComfyUI**: als Keyframe-Generator direkt eingebunden (siehe oben). **Fooocus**: Bilder dort erzeugen und
  als `bilder\keyframes\<szenen-id>.png` speichern – werden automatisch benutzt.
- **MiniMax H3 Studio** oder **ComfyUI-H3-Workflows**: fertige Clips dort erzeugen und in einen Ordner legen,
  der unter `"clips_folder"` steht (Dateiname mit `loop`, wenn Anfang = Ende).
- **Blender / Unreal Engine**: z. B. einen echten 3D-Lautsprecher rendern (Frontansicht, PNG mit Transparenz)
  und als `speakers.image` + `speakers.cone` eintragen; oder eigene Bühnen-Clips nach `clips_folder`.
- **DaVinci Resolve**: `5_resolve_export.bat` legt `ausgabe\<name>_resolve\` an:
  - `…_schnitt.edl` – alle Schnitte als Timeline (mit Tempo/Rückwärts), verweist auf deine Szenen-Clips,
  - `…_overlay_lautsprecher_titel.mov` – Lautsprecher + Titel mit Transparenz für Spur V2,
  - `…_musik.wav` – der Mix für A1, plus `LIESMICH_Resolve.txt` mit den Klicks in Resolve.
  Zoom, Spiegeln, Farblooks und Blitze der Automatik stecken nicht im EDL – die machst du in Resolve selbst.
  Das Overlay als PNG-MOV ist groß (ca. 20 GB pro Stunde bei 1080p); kleiner geht mit
  `"resolve": {"overlay_codec": "vp9"}` (WebM, ob Resolve es liest, hängt von der Version ab),
  ganz ohne Overlay: `"keins"`. Für den reinen Feinschliff kannst du auch einfach das fertige MP4 importieren.

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
