# Party Megamix – Eva & Techno Girls (DaVinci Resolve, 1920×1080)

Baut aus allen Maestro-Clips automatisch einen ~30-Minuten-Partymegamix mit 20–30 Songs
und schneidet ihn als 1080p-Timeline in **DaVinci Resolve**.

## Was das Tool macht

1. **Clips bewerten** – durchsucht `Maestro/app/outputs` (rekursiv) und bewertet jeden Clip nach
   Schärfe, Farbe, Belichtung, Bewegung, Auflösung, Gesichtern und dem Maestro-Prompt
   (Eva/Techno werden bevorzugt). Fast identische Clips werden aussortiert.
2. **Sortieren** – Girls-Clips vs. Landschaften (Berge, Seen, Gebirge, Wald …, über Prompt/Dateiname).
3. **Songs analysieren** – BPM (auf 0,01 genau), Beat-Raster und energiereichster Abschnitt
   (auf 8-Takt-Phrasen) jeder Single. *Gebirgsrauschen* ist immer dabei und kommt als Finale,
   der Rest wird nach Tempo sortiert (DJ-Reihenfolge).
4. **Lipsync** – Clips, die Maestro mit einem Song erzeugt hat, werden über ihre Tonspur
   (bzw. Maestro-Metadaten) exakt an der richtigen Songstelle gefunden und framegenau
   darübergelegt. Songabschnitte werden bevorzugt so gewählt, dass Lipsync-Clips hineinfallen.
5. **Beat-Schnitt** – alle anderen Stellen werden im Takt (1/2/4 Takte) mit den besten Girls-Clips
   geschnitten, jeder 4. Schnitt ist eine Landschaft.
6. **Ausgabe** – `plan.json`, `review.html` (Kontaktbogen aller Schnitte zum Prüfen) und
   optional ein fertiges 1080p-MP4 via ffmpeg.

## Schritt 1 – Analyse & Plan (auf deinem PC)

```bash
pip install numpy "opencv-python<5"
```

```bash
python megamix.py --clips "D:\Pinokio\api\Maestro.git\app\outputs" --music "D:\Musik\Singles" --out "D:\Megamix" --minutes 30 --songs 25
```

Wichtige Optionen:

| Option | Bedeutung |
|---|---|
| `--songs 25` | Anzahl Songs (20–30) |
| `--must gebirgsrauschen` | Songs, die sicher rein müssen (Teil des Dateinamens) |
| `--focus eva techno` | bevorzugte Begriffe in Prompt/Dateiname |
| `--landscape-every 4` | jeder N-te Schnitt eine Landschaft (0 = aus) |
| `--render` | zusätzlich fertiges 1080p-MP4 mit ffmpeg |

Danach `review.html` öffnen und die Auswahl ansehen.

## Schritt 2 – Timeline in DaVinci Resolve bauen

1. `megamix_resolve.py` kopieren nach
   `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\`
2. Im Skript oben `PLAN_PATH = r"D:\Megamix\plan.json"` eintragen.
3. Resolve öffnen → **Workspace → Scripts → megamix_resolve**.

Ergebnis: Projekt *Party Megamix – Eva & Techno Girls*, Timeline 1920×1080 @ 30 fps,
Clips füllen das Bild (Scale to crop), Marker bei jedem Songwechsel, Render-Job (H.264 1080p)
in der Render-Queue.

- **V1** Girls + Landschaften im Beat, **V2** Lipsync-Clips
- **A1/A2** Songs abwechselnd, jeweils 2 s länger → an jedem Übergang einfach eine
  Crossfade-Blende ziehen

Läuft mit der kostenlosen Resolve-Version (über das Scripts-Menü). Mit Resolve Studio geht auch
`python megamix_resolve.py D:\Megamix\plan.json` von außen.
