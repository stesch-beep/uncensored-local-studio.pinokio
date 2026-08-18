# CLAUDE – Recherchepaket & Rangliste – Video 07

**Thema:** 10 ChatGPT-Plugins/Apps, die dein Leben erleichtern – mit echten Beispielen
**Arbeitstitel:** „Diese 10 ChatGPT-Plugins sparen dir jede Woche Stunden"
**Kanal:** STX AI CREATOR LAB
**Stand der Recherche:** 18.08.2026
**Rolle:** Rechercheur, Faktenprüfer, Demo-Designer (kein Upload, kein fertiges Video)

> **Wichtiger Zielkonflikt vorab (EINSCHÄTZUNG):** Alle geprüften offiziellen OpenAI-Quellen stimmen darin überein, dass „Apps in ChatGPT" **außerhalb** des EWR, der Schweiz und des UK ausgerollt sind und die Verfügbarkeit **in Deutschland bislang nicht bestätigt** ist. Damit ist die im Briefing zentrale Anforderung „Verfügbarkeit für Nutzer in Deutschland" für die meisten Kandidaten **NICHT BELEGT**. Das prägt die gesamte Bewertung und die Rangliste. Siehe Kapitel 2, 6, 7, 10.

---

## 1. Management-Zusammenfassung

**Kernbefund:** Das ursprünglich als „ChatGPT-Plugins" geplante Video-Thema trifft auf eine veränderte Produktrealität. OpenAI hat die Terminologie mehrfach umgebaut. Am 09.07.2026 wurde laut OpenAI-Entwicklerdokumentation das „App-Verzeichnis" in ein **„Plugin-Verzeichnis"** überführt. Der Begriff **„Plugin"** ist damit heute wieder der offizielle Oberbegriff – allerdings mit völlig anderer Bedeutung als 2023. Ein Plugin ist heute ein installierbares Bündel, das **Apps** (Integrationen zu externen Diensten, technisch über MCP-Server, früher „Connectors") und/oder **Skills** (wiederverwendbare Arbeitsanweisungen) und **App-Templates** enthalten kann.

**Zweite Kernbotschaft:** Das größte Risiko für dieses Video ist **nicht** die Funktion, sondern die **Deutschland-/EWR-Verfügbarkeit**. Nach den geprüften OpenAI-Quellen sind Apps in ChatGPT für eingeloggte Nutzer **außerhalb** von EWR, Schweiz und UK verfügbar; ein EU-Rollout wird angekündigt, ist aber (Stand 18.08.2026) nicht als abgeschlossen belegt. Konsequenz: Fast jede „ist verfügbar"-Aussage muss im Video als **regional eingeschränkt / im deutschen Konto zu prüfen** gekennzeichnet werden.

**Belegte, demonstrierbare Kandidaten (Integration nachweisbar):** Google Drive, Notion, Canva, Adobe (Express/Photoshop/Acrobat als Plugin), Figma, HeyGen, vidIQ, Semrush, GitHub, Hugging Face, Cloudflare (via eigenem MCP-Server), Monday.com, Asana, Box, SharePoint, Outlook, Google Calendar/Gmail. Die **Deutschland-Verfügbarkeit** ist bei praktisch allen **nicht** primärquellenbelegt.

**Empfehlung (EINSCHÄTZUNG):** Video nicht als „Top 10 in Deutschland verfügbar" positionieren, sondern als **„Die 10 stärksten ChatGPT-Apps/Plugins – und wie du prüfst, ob sie in deinem Konto laufen"**. So bleibt das Video ehrlich, auch wenn einzelne Apps im deutschen Konto (noch) fehlen. Zwei bis drei Plätze sollten mit **„PLATZ NOCH OFFEN – Verfügbarkeit im deutschen Konto nicht belegt"** gekennzeichnet werden, bis Codex sie live geprüft hat.

**Zählung:**
- BELEGT (Integration existiert, Primärquelle vorhanden): **11**
- TEILWEISE BELEGT (Integration/Verfügbarkeit teils unklar, EU-Frage offen, oder nur MCP statt nativer App): **6**
- NICHT BELEGT (keine native ChatGPT-Integration nachweisbar): **1** (vidIQ = Grenzfall, siehe unten; als BELEGT geführt)

---

## 2. Stand und verwendete Terminologie

**Frage:** Was heißt am 18.08.2026 offiziell was – Plugin, App, Connector, Skill, Template?

Nach den geprüften OpenAI-Entwickler- und Hilfeseiten gilt folgendes Bild (jede Aussage quellenbelegt in Kapitel 12):

- **Plugin** = Oberbegriff und **Paket**, das Menschen in ChatGPT und Codex „entdecken, installieren, teilen und veröffentlichen". Ein Plugin kann Skills, Apps und App-Templates enthalten. Seit **09.07.2026** ist das „App-Verzeichnis" das **„Plugin-Verzeichnis"**. → Quelle: developers.openai.com/plugins/concepts/plugins; help.openai.com/…/20001256.
- **App** = die eigentliche **Integration** zu externen Daten und Aktionen (früher „Connector"). Apps „verbinden ChatGPT oder Codex mit externen Daten und Aktionen". Technisch von **MCP-Servern** gestützt, optional mit eigener ChatGPT-Oberfläche. → developers.openai.com/plugins/concepts/plugins.
- **Connector** = **älterer/paralleler Begriff für „App"**. Die OpenAI-Hilfeseite trägt bis heute die URL „…connectors-in-chatgpt", zeigt aber den Titel „Apps in ChatGPT". **Widerspruch/Uneinheitlichkeit:** OpenAI verwendet „App" und „Connector" nebeneinander; in Admin-/Business-Kontexten und bei „Apps mit Sync" taucht „Connector" weiter auf. → help.openai.com/…/11487775.
- **Skill** = **Ordner mit Anweisungen und Ressourcen** (`SKILL.md` plus optionale Skripte/Templates), der ChatGPT/Codex einen **wiederholbaren Arbeitsablauf** beibringt. Ein Skill liefert die Ablauflogik; der MCP-Server/die App liefert Daten, Auth und Aktionen. Skills können auch **ohne** Live-Datenzugriff laufen. → developers.openai.com/plugins/concepts/skills.
- **App-Template / Template** = vordefinierte, in ein Plugin-Listing aufnehmbare Vorlage. In der Doku als Bestandteil eines Plugin-Listings genannt („ein Plugin-Listing kann eine oder mehrere Apps, Skills und App-Templates enthalten"). Eine eigenständige, ausführliche Template-Definition liegt in den geprüften Seiten **nicht** vor → als **TEILWEISE BELEGT** kennzeichnen. → developers.openai.com/plugins.

**Widerspruch ausdrücklich dargestellt:** Es existieren **zwei Sprachwelten parallel**: (a) Verbraucher-/Consumer-Sicht = „Apps in ChatGPT" (seit Herbst 2025, Apps SDK); (b) neuere Paket-/Plugin-Sicht = „Plugins in ChatGPT und Codex" (Verzeichnis-Umbenennung 09.07.2026). Der Begriff **„Connector"** ist die dritte, ältere Ebene, primär in Business/Enterprise und bei „Apps mit Sync". **Für das Video:** Begriffe nicht als Synonyme verkaufen, sondern die Hierarchie zeigen: **Plugin (Paket) → enthält Apps/Connectors (Verbindung) + Skills (Ablauf) + Templates (Vorlage)**.

*(Terminologie-Erklärung bewusst unter 250 Wörter im Fließtext gehalten; Aufzählung dient der Präzision.)*

**Hinweis auf mögliche Änderungen:** Terminologie und Verzeichnisstruktur haben sich 2025→2026 mehrfach geändert. Alles unten kann sich nach dem 18.08.2026 erneut ändern. Vor Veröffentlichung erneut prüfen.

---

## 3. Quellen- und Prüfmethodik

- **Priorität 1:** Offizielle OpenAI-Seiten (help.openai.com, developers.openai.com, openai.com) für alle Aussagen über ChatGPT-Produkte.
- **Priorität 2:** Offizielle Anbieter-Doku/Produktseiten (z. B. canva.com, adobe.com/helpx, figma.com/help, heygen.com, semrush.com, vidiq.com, huggingface.co, developers.cloudflare.com, support.monday.com, asana.com) für Anbieter-Funktionen.
- **Nicht als Hauptbeleg:** News, Blogs, Foren, Reddit, YouTube (nur als Suchhinweis genutzt).
- **Trennung:** FAKT (quellenbelegt) / EINSCHÄTZUNG (eigene Schlussfolgerung) / EMPFEHLUNG sind sichtbar getrennt.
- **Live-Test:** Es wurde **kein** Live-Test in einem ChatGPT-Konto durchgeführt. Alle Funktionsaussagen sind daher **NICHT LIVE GETESTET** und müssen von Codex im echten deutschen Konto verifiziert werden.
- **Technische Einschränkung dieser Recherche:** Mehrere OpenAI-Hilfeseiten lieferten beim direkten Abruf HTTP 403 (Bot-Schutz). In diesen Fällen wurden die **von der Suchmaschine gelieferten offiziellen Auszüge derselben offiziellen URL** verwendet und als solche gekennzeichnet. Codex sollte diese Seiten im Browser gegenprüfen.
- **Grenzen eingehalten:** Keine Konten verbunden, keine Drittanbieter autorisiert, kein Abo/Test gestartet, keine externe Aktion, keine Unteragenten. Max. Quellen- und Suchbudget beachtet.

---

## 4. Kandidatenübersicht (Tabelle)

| # | Produkt | Anbieter | Art | Status Integration | DE-Verfügbarkeit | Schreiben/Erstellen? |
|---|---------|----------|-----|--------------------|------------------|----------------------|
| 1 | Google Drive (App mit Sync) | Google/OpenAI | App/Connector | BELEGT | NICHT BELEGT (EWR offen) | Lesen; Erstellen via Docs-Actions TEILWEISE |
| 2 | Notion (App mit Sync) | Notion Labs | App (MCP) | BELEGT | NICHT BELEGT | Lesen; Schreiben lt. Anbieter möglich (TEILW.) |
| 3 | Canva | Canva | App | BELEGT | NICHT BELEGT (EU/China ausgeschlossen) | Erstellen/Bearbeiten JA; Export NUR in Canva |
| 4 | Adobe (Express/Photoshop/Acrobat) | Adobe | Plugin | BELEGT | TEILWEISE (global lt. Adobe) | Erstellen/Bearbeiten JA |
| 5 | vidIQ | vidIQ | App | BELEGT | NICHT BELEGT | Nur Lesen (read-only) |
| 6 | GitHub | GitHub/OpenAI | App/Connector | BELEGT | TEILWEISE (global f. Plus/Pro/Team lt. OpenAI) | Nur Lesen |
| 7 | Hugging Face | Hugging Face | MCP-Server | BELEGT (MCP) | TEILWEISE | Lesen; Schreiben nur mit Extra-Tools |
| 8 | Cloudflare | Cloudflare | MCP-Server | BELEGT (MCP) | TEILWEISE (Pro/Business nötig) | je nach Server |
| 9 | HeyGen | HeyGen | App | BELEGT | NICHT BELEGT | Erstellt Videos (in HeyGen-Konto) |
| 10 | Semrush | Semrush | App | BELEGT | NICHT BELEGT | Nur Lesen; „Reporting" an Drittziele |
| E1 | Figma | Figma | App | BELEGT | NICHT BELEGT (EU ausgeschlossen) | Erstellen (FigJam/Slides) |
| E2 | Monday.com | monday.com | App (MCP) | TEILWEISE | NICHT BELEGT | lt. Anbieter Lesen+Schreiben (TEILW.) |
| E3 | Asana | Asana | App mit Sync | TEILWEISE | NICHT BELEGT | Sync = Lesen belegt; Schreiben TEILW. |
| E4 | Box | Box/OpenAI | Connector | BELEGT (gelistet) | NICHT BELEGT | Lesen |
| E5 | SharePoint | Microsoft/OpenAI | App mit Sync | BELEGT | TEILWEISE (US/EU/JP Sync) | Lesen |
| E6 | Outlook | Microsoft/OpenAI | App | BELEGT | NICHT BELEGT | Lesen (Business/Ent.) |
| E7 | Google Calendar/Gmail | Google/OpenAI | App | BELEGT | NICHT BELEGT | Lesen |
| E8 | Teams | Microsoft/OpenAI | App | BELEGT | NICHT BELEGT | Lesen |

*Legende: „NICHT BELEGT" bei DE-Verfügbarkeit heißt: keine Primärquelle bestätigt die Nutzbarkeit im deutschen (EWR-)Konto; oft sogar EWR ausdrücklich ausgeschlossen.*

---

## 5. Einzelprüfung aller Kandidaten (Untersuchungskarten)

> Jede Karte: Alle Funktions- und Verfügbarkeitsaussagen sind **NICHT LIVE GETESTET**. „Erstellen/Verändern/Senden/Löschen" wird nur bejaht, wenn eine Quelle es ausdrücklich nennt.

### Karte 1 — Google Drive (App mit Sync)
- **Produktname:** Google Drive App (mit Sync) in ChatGPT
- **Anbieter:** Google / OpenAI
- **Status:** BELEGT (Integration); DE-Verfügbarkeit NICHT BELEGT
- **Quelle:** help.openai.com/en/articles/10948259 (Self-Service Setup); help.openai.com/en/articles/10847137 (Apps mit Sync) — **Abruf 18.08.2026**
- **Fähigkeiten in ChatGPT:** Drive-Inhalte indexieren/durchsuchen; Docs/Sheets/Slides als „Google-Drive-Actions" vereinheitlicht; Dateien im Chat via @-Mention referenzieren.
- **Liest:** Google Docs, Sheets, Slides, Dateien im Drive (nach Autorisierung „see and download all your Google Drive files").
- **Erstellt:** Docs-Actions können lt. OpenAI Aktionen ausführen → **Erstellen TEILWEISE BELEGT**, nicht live geprüft.
- **Verändert / Sendet / Löscht:** **NICHT BELEGT** — nicht behaupten.
- **Berechtigungen:** OAuth-Freigabe „sehen und herunterladen aller Drive-Dateien" (weitreichend!).
- **ChatGPT-Tarif nötig:** Für Sync-Connector teils Workspace/Business; Self-Service für Plus/Pro genannt. **Im deutschen Konto prüfen.**
- **Drittanbieter-Konto kostenpflichtig?** Nein (Google-Konto genügt).
- **Region/Wohnsitz:** EWR-Verfügbarkeit NICHT BELEGT.
- **Unternehmen/Admin:** Sync teils nur Google **Workspace**, nicht privates Drive (laut Auszug). Admin kann Apps sperren.
- **Workspace-Richtlinien:** Admin-Freigabe kann nötig sein.
- **Demo-Fall (Video):** Öffentlich/synthetisch befüllten Drive-Ordner „Angebote 2026" durchsuchen und zusammenfassen.
- **Demo-Prompt (DE):** siehe Kapitel 7, Platz 4.
- **Erwartetes Ergebnis:** Kurze Übersicht + Fundstellen der Testdateien.
- **Verifikation durch Codex:** Test-Ordner mit 3 Dummy-Dokumenten anlegen, Prompt ausführen, prüfen ob Inhalte korrekt zitiert werden.
- **Datenschutz-Warnung:** Voller Lesezugriff auf **alle** Drive-Dateien – nur mit Testkonto/Testordner demonstrieren.
- **Größte Einschränkung:** Weitreichende Leseberechtigung; privates vs. Workspace-Drive.
- **Grund für möglichen Ausschluss:** DE-Verfügbarkeit unklar.

### Karte 2 — Notion (App mit Sync)
- **Produktname:** Notion App mit Sync (MCP: `https://mcp.notion.com/mcp`)
- **Anbieter:** Notion Labs
- **Status:** BELEGT (Integration); DE-Verfügbarkeit NICHT BELEGT
- **Quelle:** help.openai.com/en/articles/12532955 (Notion synced connector); notion.com/help/notion-mcp — **Abruf 18.08.2026**
- **Fähigkeiten:** Fragen an Notion-Workspaces/Seiten stellen; lesen. Notion beschreibt MCP als „read from and write to your Notion pages".
- **Liest:** Notion-Seiten/Datenbanken.
- **Erstellt/Verändert:** Notion-Doku nennt **Schreiben** → **TEILWEISE BELEGT** (Anbieterquelle, nicht live in ChatGPT geprüft; im Video als „lt. Anbieter, live prüfen" kennzeichnen).
- **Sendet/Löscht:** NICHT BELEGT.
- **Berechtigungen:** OAuth-Freigabe des Notion-Workspace.
- **ChatGPT-Tarif:** nicht eindeutig; im dt. Konto prüfen. **Notion-Konto:** kostenloses genügt.
- **Region:** EWR NICHT BELEGT. **Admin/Workspace:** Notion-Admin kann MCP sperren.
- **Demo-Fall:** Synthetisches Projekt-Wiki durchsuchen und Statusbericht erzeugen.
- **Demo-Prompt:** Kapitel 7, Platz 6.
- **Erwartetes Ergebnis:** Zusammenfassung + offene Aufgaben.
- **Verifikation:** Test-Workspace mit Dummy-Seiten; Prompt lesen lassen; Schreiben nur mit vorheriger Bestätigung testen.
- **Warnung:** Schreibzugriff möglich – Demo strikt read-only halten, Schreiben nur mit Bestätigung.
- **Größte Einschränkung:** Schreib-Umfang in ChatGPT nicht live belegt.
- **Ausschlussgrund:** DE-Verfügbarkeit.

### Karte 3 — Canva
- **Produktname:** Canva App für ChatGPT
- **Anbieter:** Canva
- **Status:** BELEGT; DE-Verfügbarkeit **ausdrücklich eingeschränkt** (EU/China ausgeschlossen) → für DE **NICHT BELEGT/negativ**
- **Quelle:** canva.com/help/chatgpt-templates; canva.com/apps/tc_chatgpt/chatgpt — **Abruf 18.08.2026**
- **Fähigkeiten:** Designs beschreiben → Canva schlägt Designs vor; erstellen, bearbeiten, Vorschau in ChatGPT.
- **Liest:** Prompt-Eingaben; Canva-Vorlagen.
- **Erstellt/Verändert:** **JA** (Design erstellen, Text ändern) — Anbieterquelle.
- **Sendet:** NICHT BELEGT. **Löscht:** NICHT BELEGT.
- **Export/Markenkit:** **NUR in Canva selbst**, nicht in ChatGPT (Quelle nennt Einschränkung).
- **Berechtigungen:** Canva-Konto verbinden.
- **ChatGPT-Tarif:** kostenlose & bezahlte Personal-Konten (lt. Canva). **Canva-Konto:** kostenlos nutzbar; Premium-Features (Magic Resize, Brand Kit) **nicht** in ChatGPT.
- **Region:** **„not yet accessible in China or the EU"** → Deutschland betroffen.
- **Demo-Fall:** Social-Media-Grafik aus Textbriefing erzeugen.
- **Demo-Prompt:** Kapitel 7, Platz 3.
- **Erwartetes Ergebnis:** Design-Vorschläge/Grafik-Entwurf.
- **Verifikation:** Im dt. Konto prüfen, ob Canva **überhaupt** erscheint (wahrscheinlich EU-gesperrt).
- **Warnung:** EU-Sperre – im deutschen Konto evtl. gar nicht sichtbar.
- **Größte Einschränkung:** EU nicht verfügbar.
- **Ausschlussgrund:** EU-Ausschluss → für „in Deutschland" ungeeignet, außer als „kommt evtl."-Ausblick.

### Karte 4 — Adobe (Express / Photoshop / Acrobat / Firefly)
- **Produktname:** Adobe Plugin für ChatGPT (bündelt Express, Photoshop, Acrobat, Firefly u. a.)
- **Anbieter:** Adobe
- **Status:** BELEGT; DE-Verfügbarkeit TEILWEISE (Adobe-Blog nennt „globally … on ChatGPT web and app")
- **Quelle:** helpx.adobe.com/express/web/add-ons-and-integrations/chatgpt-integration-with-express.html; blog.adobe.com/…2026/08/06 (Adobe für ChatGPT); adobe.com/products/firefly/adobe-for-chatgpt.html — **Abruf 18.08.2026**
- **Fähigkeiten:** Vorlagen suchen, Text hinzufügen, Bilder tauschen, Hintergrundfarbe ändern, Animationen anwenden; >70 Pro-Tools laut Adobe.
- **Liest:** Prompt + verbundenes Adobe-Konto.
- **Erstellt/Verändert:** **JA** (Designs, Bildbearbeitung).
- **Sendet/Löscht:** NICHT BELEGT.
- **Berechtigungen:** Adobe-Express-Login (viele Funktionen laut Adobe „ohne Login").
- **ChatGPT-Tarif:** nicht spezifiziert. **Adobe-Konto:** kostenlos für Basis; Premium für mehr.
- **Region:** Adobe sagt „global" — **Widerspruch** zur OpenAI-Regel (Apps außerhalb EWR). Für DE als „laut Adobe global, im dt. Konto verifizieren" kennzeichnen.
- **Admin/Workspace:** Plugin-Installation kann Admin-gesteuert sein.
- **Demo-Fall:** Aus Briefing ein Thumbnail/Poster entwerfen.
- **Demo-Prompt:** Kapitel 7, Platz 2.
- **Erwartetes Ergebnis:** Design-Entwurf, in Adobe Express weiter bearbeitbar.
- **Verifikation:** Plugin im dt. Konto suchen/installieren-Dialog aufnehmen; Testdesign erzeugen.
- **Warnung:** Verbindet Adobe-Konto; nur Testdaten verwenden.
- **Größte Einschränkung:** „Feinschliff/Export" teils nur in Adobe Express.
- **Ausschlussgrund:** Keiner zwingend, **wenn** DE-Verfügbarkeit live bestätigt.

### Karte 5 — vidIQ
- **Produktname:** vidIQ App für ChatGPT (YouTube-Analytics)
- **Anbieter:** vidIQ
- **Status:** BELEGT; DE-Verfügbarkeit NICHT BELEGT
- **Quelle:** vidiq.com/chatgpt/; support.vidiq.com/en/articles/15082430 (vidIQ MCP) — **Abruf 18.08.2026**
- **Fähigkeiten:** Kanaldaten, Top-Videos, Wettbewerber, Keyword-Recherche, Trends, Transkripte lesen.
- **Liest:** YouTube-/Kanaldaten (real-time).
- **Erstellt/Verändert/Sendet:** **Nein — read-only** (Anbieter: „cannot post videos, change settings, or modify anything on YouTube"; einzige Ausnahme: Wettbewerber-Watchlist).
- **Löscht:** Nein.
- **Berechtigungen:** vidIQ-Login; nutzt vidIQ-Credits.
- **ChatGPT-Tarif:** nicht spezifiziert. **vidIQ-Konto:** Plan bestimmt Datenumfang; kostenloses Konto möglich.
- **Region:** nicht spezifiziert; als Personal-App EWR-Frage offen.
- **Demo-Fall (ideal für den Kanal!):** Öffentliche YouTube-Nische analysieren, Titel-/Thumbnail-Ideen.
- **Demo-Prompt:** Kapitel 7, Platz 5.
- **Erwartetes Ergebnis:** Keyword-/Trend-Liste, Titelvorschläge.
- **Verifikation:** Mit eigenem Kanal oder öffentlichen Daten prüfen; read-only bestätigen.
- **Warnung:** Verbindet YouTube-Analytics – nur eigenen/öffentlichen Kanal.
- **Größte Einschränkung:** Nur Lesen (das ist hier ein Vorteil für Datenschutz).
- **Ausschlussgrund:** DE-Verfügbarkeit nicht belegt.

### Karte 6 — GitHub
- **Produktname:** GitHub App/Connector für ChatGPT (Deep Research + Sync/Chat)
- **Anbieter:** GitHub / OpenAI
- **Status:** BELEGT; DE-Verfügbarkeit TEILWEISE (OpenAI: „global to Plus/Pro/Team, including EEA, Switzerland and UK")
- **Quelle:** help.openai.com/en/articles/11145903 (Connecting GitHub to ChatGPT Deep Research) — **Abruf 18.08.2026**
- **Fähigkeiten:** Repos, Code, README, Docs lesen und durchsuchen; Deep Research; Sync-Index für Enterprise.
- **Liest:** Verbundene Repositories (Code/Commits/PRs bei Sync).
- **Erstellt/Verändert/Sendet/Löscht:** **Nein — nur Lesen** (OpenAI: „only lets you read from your repositories").
- **Berechtigungen:** GitHub-App autorisieren, Repos auswählen.
- **ChatGPT-Tarif:** Plus/Pro/Team (Beta); Enterprise/Edu global. **GitHub-Konto:** kostenloses genügt (öffentliche Repos).
- **Region:** **ausdrücklich auch EEA/CH/UK** genannt → **einer der wenigen DE-tauglichen Kandidaten** (verifizieren).
- **Admin:** Org kann App-Zugriff steuern; privater Repo-Scope teils fehleranfällig (Community-Hinweis, kein Hauptbeleg).
- **Demo-Fall:** Öffentliches Repo zusammenfassen (z. B. „Erkläre die Struktur dieses Open-Source-Projekts").
- **Demo-Prompt:** Kapitel 7, Platz 8.
- **Erwartetes Ergebnis:** Struktur-/Funktionsübersicht mit Dateiverweisen.
- **Verifikation:** Öffentliches Repo verbinden, Prompt ausführen, Lesezugriff bestätigen.
- **Warnung:** Nur Lesen – trotzdem nur nicht-vertrauliche Repos verbinden.
- **Größte Einschränkung:** Keine Schreibfunktion.
- **Ausschlussgrund:** Keiner (DE-tauglichster Kandidat).

### Karte 7 — Hugging Face
- **Produktname:** Hugging Face MCP Server
- **Anbieter:** Hugging Face
- **Status:** BELEGT (als MCP-Server, ChatGPT ausdrücklich als Client genannt); DE-Verfügbarkeit TEILWEISE (MCP-Server, keine EU-Sperre dokumentiert; aber ChatGPT-MCP-Nutzung setzt passenden Tarif voraus)
- **Quelle:** huggingface.co/docs/hub/hf-mcp-server; huggingface.co/settings/mcp — **Abruf 18.08.2026**
- **Fähigkeiten:** Modelle, Datasets, Spaces, Papers suchen/erkunden; Doku-Suche; Community-Tools (Gradio Spaces); Jobs/Sandboxes.
- **Liest:** Hub-Ressourcen (Model Cards, Datasets etc.).
- **Erstellt/Verändert:** **Nur mit zusätzlich aktivierten Tools** („Contribute Repos": Repos erstellen/Dateien schreiben) → **TEILWEISE BELEGT**, standardmäßig aus.
- **Sendet/Löscht:** NICHT BELEGT.
- **Berechtigungen:** HF-Login/Token; anonym eingeschränkt.
- **ChatGPT-Tarif:** MCP-Connector in ChatGPT setzt i. d. R. Pro/Business voraus (siehe Cloudflare-Karte). **HF-Konto:** kostenlos.
- **Region:** keine EU-Sperre dokumentiert.
- **Demo-Fall (perfekt für KI-Kanal):** Zwei öffentliche Model Cards vergleichen.
- **Demo-Prompt:** Kapitel 7, Platz 7.
- **Erwartetes Ergebnis:** Vergleich (Parameter, Lizenz, Einsatz).
- **Verifikation:** Als ChatGPT-Connector einrichten; Suche testen; Schreib-Tools ausgeschaltet lassen.
- **Warnung:** Schreib-Tools (Repo-Erstellung) nur bewusst aktivieren.
- **Größte Einschränkung:** In ChatGPT als manueller MCP-Connector (Tarifabhängig), keine 1-Klick-App im Verzeichnis belegt.
- **Ausschlussgrund:** MCP-Einrichtung evtl. zu technisch für Einsteiger.

### Karte 8 — Cloudflare
- **Produktname:** Cloudflare Remote MCP Server(s) (z. B. Docs-MCP, DEX-MCP)
- **Anbieter:** Cloudflare
- **Status:** BELEGT (als MCP-Server); DE-Verfügbarkeit TEILWEISE (Tarifbindung)
- **Quelle:** developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/; developers.cloudflare.com/cloudflare-one/insights/dex/dex-mcp-server/ — **Abruf 18.08.2026**
- **Fähigkeiten:** Je nach Server – Doku-Suche, Konfigurationen abfragen, DEX-Insights etc.
- **Liest:** Cloudflare-Ressourcen/Doku (serverabhängig).
- **Erstellt/Verändert/Löscht:** Serverabhängig – **pauschal NICHT BELEGT**; nur konkreten Server prüfen.
- **Berechtigungen:** OAuth zum jeweiligen MCP-Server.
- **ChatGPT-Tarif:** **Cloudflare-Doku sagt ausdrücklich: ChatGPT Pro oder Business nötig; Free/Plus unterstützen keine MCP-Server.** Wichtiger Beleg für MCP-Tarifbindung generell.
- **Region:** keine EU-Sperre dokumentiert; Tarifhürde bleibt.
- **Demo-Fall:** Cloudflare-Doku per natürlicher Sprache durchsuchen (Docs-MCP).
- **Demo-Prompt:** Kapitel 7 (Reserve/optional).
- **Erwartetes Ergebnis:** Passende Doku-Antwort mit Quellen.
- **Verifikation:** Nur mit Pro/Business testbar; Connector-URL eintragen.
- **Warnung:** Nur öffentliche Doku-Server für Demo; produktive Server nicht anfassen.
- **Größte Einschränkung:** Pro/Business-Pflicht → für Einsteiger-Video schwächer.
- **Ausschlussgrund:** Zu technisch + Tarifhürde → **Kandidat für „PLATZ NOCH OFFEN"**.

### Karte 9 — HeyGen
- **Produktname:** HeyGen App für ChatGPT (Video Agent)
- **Anbieter:** HeyGen
- **Status:** BELEGT; DE-Verfügbarkeit NICHT BELEGT
- **Quelle:** heygen.com/chatgpt-app; heygen.com/integrations/chatgpt — **Abruf 18.08.2026**
- **Fähigkeiten:** Aus Prompt/Skript fertiges Video (Avatar, B-Roll, Voiceover) im Chat erzeugen; konversationell verfeinern.
- **Liest:** Prompt/Thread-Kontext.
- **Erstellt:** **JA — Videos** (im HeyGen-Konto, Credits).
- **Verändert:** Video im Chat anpassen (Länge/Visuals/Ton).
- **Sendet/Veröffentlicht/Löscht:** NICHT BELEGT (kein Auto-Publish dokumentiert).
- **Berechtigungen:** Kostenloses HeyGen-Konto; verbraucht Credits.
- **ChatGPT-Tarif:** nicht spezifiziert. **HeyGen-Konto:** kostenlos mit Start-Credits; mehr = kostenpflichtig.
- **Region:** nicht spezifiziert.
- **Demo-Fall:** Kurzes Erklär-Video aus synthetischem Skript.
- **Demo-Prompt:** Kapitel 7, Platz 1 (Alternativ).
- **Erwartetes Ergebnis:** Fertiges Kurzvideo in der Chat-Vorschau.
- **Verifikation:** Testkonto, kurzes Dummy-Skript, Credit-Verbrauch beachten.
- **Warnung:** Keine echten Personen/Stimmen ohne Einwilligung; Credits kosten Geld.
- **Größte Einschränkung:** Credit-Kosten; Avatar-Rechte.
- **Ausschlussgrund:** DE-Verfügbarkeit + Kostenaspekt.

### Karte 10 — Semrush
- **Produktname:** Semrush App für ChatGPT
- **Anbieter:** Semrush
- **Status:** BELEGT; DE-Verfügbarkeit NICHT BELEGT
- **Quelle:** semrush.com/news/439260 (Launch, 17.12.2025); semrush.com/mcp/ — **Abruf 18.08.2026**
- **Fähigkeiten:** Live-Semrush-Daten (Traffic, Rankings, Sichtbarkeit); Content-Briefs, Keyword-Cluster, Gap-Analysen; Reporting.
- **Liest:** Semrush-Daten.
- **Erstellt:** Content-Briefs/Outlines (Text im Chat).
- **Verändert/Löscht:** NICHT BELEGT. **„Reporting" an Google Docs/Notion/Slack/E-Mail:** nur als Feature genannt → **externe Sende-Funktion NICHT ohne Live-Test behaupten**; im Demo strikt vermeiden.
- **Berechtigungen:** Semrush-Login (@Semrush im Prompt taggen).
- **ChatGPT-Tarif:** lt. Semrush Enterprise/EDU/Business/Pro/Plus. **Semrush-Konto:** kostenpflichtig (Pro/Business/Enterprise).
- **Region:** nicht spezifiziert.
- **Demo-Fall:** Öffentliche Domain-Sichtbarkeit abfragen, Content-Brief erstellen.
- **Demo-Prompt:** Kapitel 7, Platz 9.
- **Erwartetes Ergebnis:** Keyword-Cluster + Brief.
- **Verifikation:** Mit Semrush-Konto; Reporting-Funktion NICHT auslösen.
- **Warnung:** „Reporting an E-Mail/Slack" ist eine Sende-Aktion – im Video nicht demonstrieren.
- **Größte Einschränkung:** Kostenpflichtiges Semrush-Konto nötig.
- **Ausschlussgrund:** DE-Verfügbarkeit + Kostenhürde.

### Ersatzkandidaten (Kurzkarten)

**E1 Figma** — BELEGT; **EU ausdrücklich ausgeschlossen** („not available in the EU"). Kann FigJam-Diagramme & Figma-Slides erstellen; andere Figma-Produkte nicht. Für DE damit **negativ** (nur Ausblick). Quelle: help.figma.com/…/35326636109975. **Abruf 18.08.2026**

**E2 Monday.com** — TEILWEISE; via MCP mit ChatGPT verbindbar (support.monday.com/…/29491695661458), lt. Anbieter Lesen+Schreiben (Items/Boards); in ChatGPT nicht live belegt. DE NICHT BELEGT. **Abruf 18.08.2026**

**E3 Asana** — TEILWEISE; „Asana App mit Sync" bei OpenAI gelistet (help.openai.com/…/12628359), „Asana for ChatGPT coming soon"; Schreiben (Projekte anlegen) angekündigt, nicht live belegt. **Abruf 18.08.2026**

**E4 Box** — BELEGT als unterstützter Connector (Google Drive, SharePoint, Dropbox, Box). Lesen. DE NICHT BELEGT. Quelle: help.openai.com/…/11487775. **Abruf 18.08.2026**

**E5 SharePoint** — BELEGT; „App mit Sync" für OneDrive/SharePoint; Sync unterstützt Datenresidenz US/EU/JP (→ EU-Region grundsätzlich vorgesehen, Verfügbarkeit im konkreten dt. Konto prüfen). Lesen. Quelle: help.openai.com/…/12143177. **Abruf 18.08.2026**

**E6 Outlook** — BELEGT; E-Mail/Kalender durchsuchbar; Business/Enterprise/Edu. Lesen. DE NICHT BELEGT. Quelle: help.openai.com/…/12512241. **Abruf 18.08.2026**

**E7 Google Calendar/Gmail** — BELEGT; für Business/Enterprise/Edu, automatische Referenzierung. Lesen. Quelle: help.openai.com/…/11487775. **Abruf 18.08.2026**

**E8 Teams** — BELEGT; durchsuchbar per Chat + Deep Research; Business/Enterprise. Lesen. Quelle: help.openai.com/…/12552368. **Abruf 18.08.2026**

---

## 6. Bewertungsmatrix (0–10 je Kategorie)

Kategorien: (1) Zeitersparnis (2) Einsteiger-Verständlichkeit (3) Sichtbares Ergebnis (4) Alltagstauglichkeit (5) Berechtigungs-Transparenz (6) Datenschutz/Sicherheit (7) DE-Verfügbarkeit (8) YouTube-Demo-Stärke.

> **Regel angewandt:** Fehlende Quelle, unbestätigte DE-Verfügbarkeit oder unklare Berechtigung = deutlicher Abzug (v. a. Kategorie 7). Bekanntheit gibt **keine** Punkte.

| Kandidat | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Summe | Quellenlage | Live-Test |
|----------|---|---|---|---|---|---|---|---|-------|-------------|-----------|
| GitHub | 8 | 6 | 7 | 7 | 9 | 8 | **7** | 7 | **59** | BELEGT | offen |
| Hugging Face | 7 | 5 | 7 | 6 | 8 | 8 | **6** | 8 | **55** | BELEGT | offen |
| Adobe (Express) | 8 | 8 | 9 | 8 | 6 | 6 | **5** | 9 | **59** | BELEGT | offen |
| vidIQ | 8 | 7 | 7 | 8 | 8 | 9 | **4** | 9 | **60** | BELEGT | offen |
| Google Drive | 9 | 8 | 7 | 9 | 4 | 4 | **4** | 7 | **52** | BELEGT | offen |
| Notion | 8 | 7 | 7 | 8 | 5 | 5 | **4** | 7 | **51** | BELEGT | offen |
| HeyGen | 9 | 7 | 10 | 7 | 6 | 5 | **4** | 10 | **58** | BELEGT | offen |
| Semrush | 8 | 5 | 7 | 6 | 6 | 6 | **4** | 7 | **49** | BELEGT | offen |
| Canva | 8 | 9 | 9 | 8 | 6 | 6 | **2** | 9 | **57** | BELEGT (EU-Sperre) | offen |
| Figma | 7 | 7 | 8 | 6 | 6 | 6 | **1** | 7 | **48** | BELEGT (EU-Sperre) | offen |
| Cloudflare | 6 | 3 | 5 | 5 | 7 | 7 | **4** | 4 | **41** | BELEGT (MCP) | offen |
| Monday.com | 7 | 6 | 6 | 7 | 5 | 5 | **3** | 6 | **45** | TEILW. | offen |
| Asana | 7 | 6 | 6 | 7 | 5 | 5 | **3** | 6 | **45** | TEILW. | offen |
| SharePoint | 7 | 6 | 6 | 7 | 5 | 5 | **5** | 5 | **46** | BELEGT | offen |

**Begründungs-Kurzform (EINSCHÄTZUNG):**
- **vidIQ** führt trotz DE-Unsicherheit, weil read-only (Top-Datenschutz), extrem passend zum Kanal und stark demonstrierbar.
- **GitHub/Adobe** gleichauf: GitHub durch belegte EWR-Verfügbarkeit + Transparenz; Adobe durch visuelles Ergebnis.
- **Canva/Figma** stark im Ergebnis, aber **EU-Sperre** drückt Kategorie 7 hart nach unten.
- **Cloudflare** verliert durch Technik-Hürde und Pro/Business-Pflicht.

---

## 7. Finale / vorläufige Top 10 (Countdown)

> **Wichtig:** Da für die meisten Kandidaten die **Deutschland-Verfügbarkeit NICHT BELEGT** ist, ist dies eine **vorläufige** Rangliste. Reihenfolge folgt der Matrix, gewichtet für ein Einsteiger-Video (sichtbares Ergebnis + Datenschutz + DE-Chance). **Zwei Plätze sind bewusst offen.** Alle Prompts: read-only, keine externen Aktionen, Bestätigung vor jeder Schreibaktion.

### Platz 10 — SharePoint / Box (Dokumenten-Connector) — *TEILWEISE / vorläufig*
- **Hook (8–12 s):** „Deine Firmendokumente durchsuchen, ohne sie zu öffnen – geht das wirklich?"
- **Problem:** Wichtige Infos verstreut in vielen Dateien.
- **Demo:** In ChatGPT den SharePoint/Box-Connector zeigen, synthetischen Ordner durchsuchen.
- **Prompt (DE):** `Durchsuche meinen verbundenen Testordner „Handbuch-Demo" und fasse die drei wichtigsten Regeln in Stichpunkten zusammen. Nutze nur die dort vorhandenen Dateien. Wenn eine Information fehlt, sage es ausdrücklich und erfinde nichts.`
- **Erwartetes Ergebnis:** Stichpunktliste mit Dateiverweisen.
- **Vorher-Nachher:** Manuelles Durchklicken → 1 Prompt.
- **Zeitersparnis:** ~15–20 Min./Suche.
- **Einschränkung:** Business/Enterprise, Admin-Freigabe; DE-Konto prüfen.
- **Berechtigung:** Lesezugriff auf gewählte Sites/Ordner.
- **Sicherheitshinweis:** Nur Testordner, keine echten Firmendaten.
- **Einblendung (≤8 Wörter):** „Nur Lesen – Admin muss freigeben."
- **Platzierungsgrund:** Nützlich, aber Business-lastig und wenig „wow".

### Platz 9 — Semrush — *vorläufig*
- **Hook:** „SEO-Daten direkt im Chat – ohne 20 Tabs."
- **Problem:** SEO-Recherche ist zeitraubend.
- **Demo:** `@Semrush` taggen, öffentliche Domain analysieren.
- **Prompt (DE):** `@Semrush Zeige mir für die öffentliche Domain example.com die Top-5-Keywords und die Sichtbarkeitsentwicklung der letzten Monate. Erstelle daraus einen kurzen Content-Brief mit fünf Themenideen. Sende oder veröffentliche nichts – gib alles nur hier im Chat aus.`
- **Erwartetes Ergebnis:** Keyword-Liste + 5 Content-Ideen.
- **Vorher-Nachher:** Manuelle Tool-Recherche → Sekunden.
- **Zeitersparnis:** ~30 Min./Brief.
- **Einschränkung:** Kostenpflichtiges Semrush-Konto; DE-Verfügbarkeit offen.
- **Berechtigung:** Semrush-Login (Lesen).
- **Sicherheitshinweis:** „Reporting an E-Mail/Slack" NICHT auslösen.
- **Einblendung:** „Braucht bezahltes Semrush-Konto."
- **Platzierungsgrund:** Stark, aber Kosten + kein visuelles Wow.

### Platz 8 — GitHub — *belegt, DE-tauglichster Kandidat*
- **Hook:** „Ein fremdes Code-Projekt in 60 Sekunden verstehen."
- **Problem:** Große Repos sind unübersichtlich.
- **Demo:** Öffentliches Repo verbinden, Struktur erklären lassen.
- **Prompt (DE):** `Ich habe ein öffentliches GitHub-Repository verbunden. Erkläre mir in einfachen Worten, was dieses Projekt macht, wie die Ordnerstruktur aufgebaut ist und wo ich anfangen sollte zu lesen. Verweise auf konkrete Dateien. Ändere nichts – nur lesen.`
- **Erwartetes Ergebnis:** Verständliche Projektübersicht mit Dateiverweisen.
- **Vorher-Nachher:** Stundenlanges Einlesen → 1 Antwort.
- **Zeitersparnis:** 1–2 Std. beim Einarbeiten.
- **Einschränkung:** Nur Lesen; Plus/Pro/Team (lt. OpenAI auch EWR).
- **Berechtigung:** Repo-Lesezugriff.
- **Sicherheitshinweis:** Nur nicht-vertrauliche Repos verbinden.
- **Einblendung:** „Nur Lesen, auch in Europa (prüfen)."
- **Platzierungsgrund:** Belegte EWR-Verfügbarkeit + Transparenz, aber Nische.

### Platz 7 — Hugging Face — *belegt, ideal für KI-Publikum*
- **Hook:** „Zwei KI-Modelle vergleichen – ohne selbst zu suchen."
- **Problem:** Model Cards sind technisch und verstreut.
- **Demo:** HF-MCP-Connector, zwei öffentliche Modelle vergleichen.
- **Prompt (DE):** `Vergleiche zwei öffentliche Modelle auf Hugging Face anhand ihrer Model Cards: Parametergröße, Lizenz, typische Einsatzzwecke und bekannte Einschränkungen. Stelle das als Tabelle dar und nenne die Quell-Links. Nur lesen, nichts erstellen.`
- **Erwartetes Ergebnis:** Vergleichstabelle mit Links.
- **Vorher-Nachher:** Zwei Tabs lesen → 1 Tabelle.
- **Zeitersparnis:** ~15 Min./Vergleich.
- **Einschränkung:** MCP-Einrichtung (technisch); Schreib-Tools separat.
- **Berechtigung:** HF-Login (Lesen).
- **Sicherheitshinweis:** Schreib-Tools („Contribute Repos") ausgeschaltet lassen.
- **Einblendung:** „Standard nur Lesen."
- **Platzierungsgrund:** Perfekt fürs Publikum, aber Setup-Hürde.

### Platz 6 — Notion — *belegt, DE offen*
- **Hook:** „Dein ganzes Wissens-Wiki auf eine Frage antworten lassen."
- **Problem:** Notizen und Projekte unübersichtlich.
- **Demo:** Test-Workspace durchsuchen, Statusbericht erzeugen.
- **Prompt (DE):** `Durchsuche meinen verbundenen Notion-Test-Workspace „Projekt Demo" und erstelle einen kurzen Statusbericht: erledigte Aufgaben, offene Aufgaben, nächste Schritte. Nur lesen. Bevor du irgendetwas in Notion änderst oder anlegst, frage mich zuerst.`
- **Erwartetes Ergebnis:** Statusbericht (Text).
- **Vorher-Nachher:** Seiten durchklicken → 1 Bericht.
- **Zeitersparnis:** ~20 Min./Woche.
- **Einschränkung:** Schreiben lt. Anbieter möglich → bewusst read-only halten; DE offen.
- **Berechtigung:** Notion-Workspace (OAuth).
- **Sicherheitshinweis:** Schreibzugriff möglich – Bestätigung erzwingen.
- **Einblendung:** „Kann auch schreiben – Vorsicht."
- **Platzierungsgrund:** Sehr nützlich, aber Berechtigungsbreite + DE offen.

### Platz 5 — vidIQ — *belegt, Kanal-Match, read-only*
- **Hook:** „YouTube-Ideen, die auf echten Daten beruhen."
- **Problem:** Titel/Themen aus dem Bauch heraus.
- **Demo:** Öffentliche Nische analysieren, Titel-/Thumbnail-Ideen.
- **Prompt (DE):** `Analysiere mit vidIQ die YouTube-Nische „KI-Tools für Anfänger": nenne fünf gefragte Themen, passende Keywords und je einen Titelvorschlag. Nur lesen – ändere nichts an einem Kanal. Markiere Annahmen ausdrücklich.`
- **Erwartetes Ergebnis:** 5 Themen + Keywords + Titel.
- **Vorher-Nachher:** Raten → datenbasiert.
- **Zeitersparnis:** ~30–45 Min./Recherche.
- **Einschränkung:** DE-Verfügbarkeit offen; vidIQ-Plan bestimmt Datenumfang.
- **Berechtigung:** vidIQ-Login (nur Lesen).
- **Sicherheitshinweis:** Read-only – kann nichts auf YouTube ändern (Anbieter-Aussage).
- **Einblendung:** „Nur Lesen – sicher für YouTube."
- **Platzierungsgrund:** Datenschutzfreundlich + starke Demo; DE offen hält es auf 5.

### Platz 4 — Google Drive — *belegt, Alltagsheld, DE offen*
- **Hook:** „Frag deine Dateien, statt sie zu suchen."
- **Problem:** Dokumente verstreut, Suche mühsam.
- **Demo:** Test-Ordner durchsuchen, zusammenfassen.
- **Prompt (DE):** `Durchsuche meinen verbundenen Test-Ordner „Angebote-Demo" in Google Drive und vergleiche die drei enthaltenen Beispiel-Angebote nach Preis und Leistung. Nur lesen. Erstelle oder ändere keine Datei. Wenn Angaben fehlen, sage es klar.`
- **Erwartetes Ergebnis:** Vergleichstabelle der Testdateien.
- **Vorher-Nachher:** Dateien öffnen → 1 Vergleich.
- **Zeitersparnis:** ~20–30 Min./Vorgang.
- **Einschränkung:** Weitreichender Lesezugriff; privates vs. Workspace-Drive; DE offen.
- **Berechtigung:** „Alle Drive-Dateien sehen/herunterladen" (breit!).
- **Sicherheitshinweis:** Voller Lesezugriff – nur Testordner nutzen.
- **Einblendung:** „Sieht ALLE Drive-Dateien."
- **Platzierungsgrund:** Höchste Alltagstauglichkeit, aber Berechtigungsbreite senkt Datenschutz.

### Platz 3 — Canva — *belegt, ABER EU-Sperre → als Ausblick*
- **Hook:** „Aus einem Satz ein fertiges Design."
- **Problem:** Grafiken kosten Zeit/Design-Skill.
- **Demo:** Aus Briefing Social-Grafik erzeugen (falls im Konto sichtbar).
- **Prompt (DE):** `Erstelle mit Canva einen Entwurf für einen quadratischen Social-Media-Post zum Thema „Kostenloser Webinar-Termin am Freitag". Stil: modern, freundlich, Blautöne. Zeige mir Design-Vorschläge. Veröffentliche oder versende nichts.`
- **Erwartetes Ergebnis:** Design-Vorschläge/Entwurf.
- **Vorher-Nachher:** Editor-Arbeit → 1 Prompt.
- **Zeitersparnis:** ~20–30 Min./Grafik.
- **Einschränkung:** **In der EU laut Canva nicht verfügbar**; Export/Brand Kit nur in Canva.
- **Berechtigung:** Canva-Konto.
- **Sicherheitshinweis:** EU-Sperre – im dt. Konto evtl. nicht sichtbar.
- **Einblendung:** „In EU evtl. (noch) gesperrt."
- **Platzierungsgrund:** Stärkstes visuelles Wow – **nur als „kommt evtl." zeigen**, sonst Platz offen lassen.

### Platz 2 — Adobe (Express) — *belegt, laut Adobe global*
- **Hook:** „Design-Profi-Werkzeuge – direkt im Chat."
- **Problem:** Professionelle Grafiken ohne Adobe-Kenntnisse.
- **Demo:** Aus Briefing ein Thumbnail/Poster entwerfen.
- **Prompt (DE):** `Erstelle mit Adobe Express einen Entwurf für ein YouTube-Thumbnail zum Thema „10 ChatGPT-Apps". Große, gut lesbare Schrift, kräftige Farben, Platz für ein Gesicht rechts. Zeige mir einen Entwurf. Nichts veröffentlichen.`
- **Erwartetes Ergebnis:** Thumbnail-Entwurf, in Express weiter bearbeitbar.
- **Vorher-Nachher:** Design-Software → 1 Prompt.
- **Zeitersparnis:** ~30 Min./Design.
- **Einschränkung:** Feinschliff/Export teils nur in Adobe Express; DE live prüfen.
- **Berechtigung:** Adobe-Login (viele Funktionen ohne Login lt. Adobe).
- **Sicherheitshinweis:** Nur Testinhalte; Konto-Verbindung bewusst.
- **Einblendung:** „Laut Adobe weltweit verfügbar."
- **Platzierungsgrund:** Visuelles Wow + Adobe nennt globale Verfügbarkeit → bester „sicherer" Show-Kandidat.

### Platz 1 — PLATZ NOCH OFFEN (Live-Test entscheidet) — *empfohlen: HeyGen ODER GitHub*
- **Begründung:** Platz 1 darf erst nach Live-Test im deutschen Konto fixiert werden. **Zwei Optionen:**
  - **HeyGen** = größtes „Wow" (fertiges Video im Chat), aber Credits + DE offen.
  - **GitHub** = einzige Integration mit **belegter** EWR-Verfügbarkeit (ehrlichster Platz 1 für ein DE-Video).
- **Empfehlung (EINSCHÄTZUNG):** Wenn HeyGen im dt. Konto läuft → **HeyGen** auf 1 (Show-Effekt). Wenn nicht → **GitHub** auf 1 (Verlässlichkeit).
- **HeyGen-Prompt (DE):** `Erstelle mit HeyGen ein 20-Sekunden-Erklärvideo aus diesem synthetischen Skript: „Willkommen bei STX AI CREATOR LAB. Heute zeige ich dir zehn ChatGPT-Apps, die dir Zeit sparen." Wähle einen neutralen Avatar. Zeige mir das Ergebnis zur Prüfung. Veröffentliche nichts.`
- **Erwartetes Ergebnis:** Kurzvideo in der Chat-Vorschau.
- **Einblendung:** „Fertiges Video – kostet Credits."
- **Sicherheitshinweis:** Keine echten Personen/Stimmen; Credits kosten Geld.

> **Kennzeichnung offener Plätze:** Platz 1 = **PLATZ NOCH OFFEN – Verfügbarkeit/Show-Test im deutschen Konto entscheidet.** Zusätzlich sollte einer der Business-Plätze (10) als **PLATZ NOCH OFFEN** geführt werden, falls SharePoint/Box im dt. Konto nicht erscheint.

---

## 8. Drei Short-Konzepte

### Short 1 — „Plugin, App oder Connector? Der 45-Sekunden-Klartext" *(Pflicht: Begriffe erklären)*
- **Titel:** Plugin vs. App vs. Connector – endlich verständlich
- **Hook (1 Satz):** „Alle sagen ‚ChatGPT-Plugin' – aber das stimmt so nicht mehr."
- **Ablauf (30–45 s):** (0–8 s) Hook + drei Kärtchen einblenden. (8–25 s) Hierarchie animieren: Plugin = Paket → enthält App/Connector (Verbindung) + Skill (Ablauf). (25–40 s) Screenshot Plugin-Verzeichnis. (40–45 s) CTA.
- **Bildschirmaktion:** ChatGPT-Einstellungen → „Plugins/Apps" öffnen.
- **Kerntext (gesprochen):** „Ein Plugin ist das Paket. Darin steckt eine App – früher Connector genannt –, die ChatGPT mit einem Dienst verbindet. Und ein Skill, der ChatGPT den Ablauf beibringt. Merke: Plugin ist die Schachtel, App ist die Verbindung."
- **Einblendungen:** „Plugin = Paket" / „App = Verbindung" / „Skill = Ablauf".
- **CTA:** „Folge für die Top 10."

### Short 2 — „Diese eine Berechtigung solltest du NIE blind erlauben" *(Pflicht: Berechtigungs-Warnung)*
- **Titel:** Stopp! Bevor du auf „Erlauben" klickst
- **Hook:** „Google Drive in ChatGPT will ‚alle Dateien sehen' – wirklich alle."
- **Ablauf (30–45 s):** (0–8 s) Hook + Berechtigungsdialog. (8–30 s) Lesen vs. Schreiben/Senden/Löschen erklären. (30–45 s) Regel: erst Testordner.
- **Bildschirmaktion:** OAuth-Berechtigungsdialog (synthetisch/Testkonto).
- **Kerntext:** „Prüfe immer: Darf die App nur lesen – oder auch ändern, senden, löschen? Gib nur frei, was du wirklich brauchst. Und teste zuerst mit einem leeren Ordner."
- **Einblendungen:** „Lesen ≠ Löschen" / „Nur nötige Rechte" / „Erst mit Testdaten".
- **CTA:** „Teilen, bevor's jemand blind klickt."

### Short 3 — „Ein Satz → fertige Grafik (Vorher/Nachher)" *(Pflicht: Vorher-Nachher)*
- **Titel:** Von 0 auf Design in 20 Sekunden
- **Hook:** „Ein Satz eingetippt – und ChatGPT baut das Design."
- **Ablauf (30–45 s):** (0–6 s) leere Leinwand (Vorher). (6–30 s) Prompt tippen → Adobe/Canva-Entwurf erscheint. (30–45 s) Split „Vorher/Nachher".
- **Bildschirmaktion:** Adobe-Express-/Canva-Demo-Prompt live.
- **Kerntext:** „Kein Design-Programm, kein Vorwissen. Ein Satz genügt, und du bekommst einen fertigen Entwurf, den du nur noch anpasst."
- **Einblendungen:** „Vorher: leer" / „Nachher: fertig" / „In EU: verfügbarkeit prüfen".
- **CTA:** „Welches Tool zuerst? Kommentier's!"

---

## 9. Sicherheitsanleitung für Zuschauer

1. **Herausgeber prüfen:** Ist die App/das Plugin offiziell vom Anbieter (nicht ein Nachbau)?
2. **Produktseite + Datenschutz lesen:** Offizielle Seite und Datenschutzerklärung des Anbieters kontrollieren.
3. **Nur nötige Rechte:** Keine breiten Berechtigungen „auf Vorrat" freigeben.
4. **Erst Testdaten:** Mit synthetischen/öffentlichen Daten starten, nie mit echten.
5. **Zugriffsarten unterscheiden:** Lesen ≠ Schreiben ≠ Senden ≠ Löschen bewusst trennen.
6. **Unternehmensdaten:** Interne Richtlinien & Admin-Vorgaben beachten.
7. **Menschliche Bestätigung:** Vor jeder externen Aktion (senden, veröffentlichen, ändern) selbst bestätigen.
8. **Verbindungen trennen:** Nicht mehr genutzte Apps in den Einstellungen entfernen.
9. **Keine sensiblen Daten:** Keine Passwörter, Bank-, Gesundheits-, Personal- oder Kundendaten in Demos.
10. **Am Installationstag neu prüfen:** Verfügbarkeit, Tarif und Berechtigungen ändern sich – vor Nutzung erneut checken.

---

## 10. Ausschlüsse und offene Punkte

- **EU-/DE-Verfügbarkeit ist der Hauptvorbehalt.** OpenAI: Apps außerhalb EWR/CH/UK; EU-Rollout angekündigt, nicht als abgeschlossen belegt. → Fast alle „verfügbar"-Aussagen sind für DE **NICHT BELEGT**.
- **Canva & Figma:** EU **ausdrücklich ausgeschlossen** (Anbieterquellen) → für ein DE-Video nur als Ausblick.
- **Cloudflare, Hugging Face:** In ChatGPT als **manueller MCP-Connector**; Cloudflare-Doku belegt: **MCP-Connector braucht ChatGPT Pro/Business** (Free/Plus nicht). → Einsteiger-Hürde.
- **Schreib-/Sende-/Löschfunktionen:** Nur Canva/Adobe (erstellen/bearbeiten) und HeyGen (Video erstellen) sind belegt. Notion/Monday/Asana nennen Schreiben nur **anbieterseitig** → im Video **nicht** als „funktioniert in ChatGPT" behaupten. Semrush-„Reporting" (E-Mail/Slack) ist eine **Sende-Aktion** → nicht demonstrieren.
- **Google Drive Sync:** Auszug nennt Einschränkung „nur Workspace-Drive, nicht privat" für Sync → live prüfen.
- **Terminologie kann sich erneut ändern** (Verzeichnis-Umbau 07/2026).
- **Nicht behauptbar (ohne Live-Test):** dass eine App im **deutschen** Konto vollständig funktioniert; dass Schreib-/Sende-Funktionen aktiv sind; dass eine sichtbare Schaltfläche = funktionierende Funktion.

---

## 11. Live-Test-Checkliste für Codex (im echten deutschen Konto)

Für **jede** App vor der Aufnahme:
1. Erscheint die App/das Plugin im deutschen Konto im Verzeichnis? (Ja/Nein + Screenshot)
2. Welcher ChatGPT-Tarif ist aktiv? Funktioniert die App darin?
3. Berechtigungsdialog aufnehmen (welche Rechte werden verlangt?).
4. Demo-Prompt (aus Kap. 7) ausführen, Ergebnis screenshotten.
5. Bestätigen: Wird nur **gelesen**? Keine externe Aktion ausgelöst?
6. Bei Schreib-Apps (Canva/Adobe/HeyGen): Ergebnis erzeugt? Wo landet es (nur Konto, kein Auto-Publish)?
7. Prüfen: privates vs. Workspace-/Business-Konto nötig?
8. Datum des Tests notieren (Verfügbarkeit ändert sich).

**Priorität Live-Test (zwingend):** GitHub (EWR belegt), Adobe Express, vidIQ, Google Drive, Notion, HeyGen. **Danach:** Semrush, Hugging Face, SharePoint. **Nur falls sichtbar:** Canva, Figma (EU-Sperre erwartet).

---

## 12. Quellenverzeichnis (Abruf jeweils 18.08.2026)

**OpenAI (Produkt/Terminologie):**
1. Apps in ChatGPT — https://help.openai.com/en/articles/11487775-connectors-in-chatgpt
2. Plugins in ChatGPT and Codex — https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex
3. Plugin-Architektur (Definitionen) — https://developers.openai.com/plugins/concepts/plugins
4. Skills (Definition) — https://developers.openai.com/plugins/concepts/skills
5. Plugins (Übersicht/Verzeichnis) — https://developers.openai.com/plugins
6. Apps mit Sync — https://help.openai.com/en/articles/10847137-chatgpt-synced-connectors
7. Google Drive App (Self-Service Setup) — https://help.openai.com/en/articles/10948259-google-drive-app-with-sync-self-service-setup
8. Notion synced connector — https://help.openai.com/en/articles/12532955-notion-synced-connector
9. GitHub in ChatGPT (Deep Research) — https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt-deep-research
10. SharePoint app — https://help.openai.com/en/articles/12143177-sharepoint-connectors-on-chatgpt
11. Outlook app — https://help.openai.com/en/articles/12512241-outlook-email-and-calendar-app-for-chatgpt
12. Microsoft Teams app — https://help.openai.com/en/articles/12552368-microsoft-teams-connector-for-chatgpt
13. Asana synced connector — https://help.openai.com/en/articles/12628359-asana-synced-connector
14. Admin controls/security — https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-for-plugins-and-apps
15. Introducing apps in ChatGPT — https://openai.com/index/introducing-apps-in-chatgpt/

**Anbieter:**
16. Canva – ChatGPT-Integration — https://www.canva.com/help/chatgpt-templates/
17. Adobe Express in ChatGPT — https://helpx.adobe.com/express/web/add-ons-and-integrations/chatgpt-integration-with-express.html
18. Adobe für ChatGPT (Blog) — https://blog.adobe.com/en/publish/2026/08/06/introducing-adobe-chatgpt-create-edit-get-work-done-all-in-chatgpt
19. Figma mit ChatGPT — https://help.figma.com/hc/en-us/articles/35326636109975-Use-ChatGPT-with-Figma
20. vidIQ ChatGPT App — https://vidiq.com/chatgpt/
21. HeyGen ChatGPT App — https://www.heygen.com/chatgpt-app
22. Semrush Launch (17.12.2025) — https://www.semrush.com/news/439260-semrush-launches-official-app-in-chatgpt-offering-users-direct-access-to-semrush-data/
23. Hugging Face MCP Server — https://huggingface.co/docs/hub/hf-mcp-server
24. Cloudflare eigene MCP-Server — https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/
25. Cloudflare DEX MCP (ChatGPT-Verbindung, Pro/Business) — https://developers.cloudflare.com/cloudflare-one/insights/dex/dex-mcp-server/
26. Monday.com MCP mit ChatGPT — https://support.monday.com/hc/en-us/articles/29491695661458-Connect-monday-MCP-with-ChatGPT
27. Notion MCP — https://www.notion.com/help/notion-mcp

*(Hinweis: Bei den OpenAI-Hilfeseiten lieferte der direkte Serverabruf teils HTTP 403; verwendet wurden die offiziellen Auszüge derselben URLs. Codex sollte im Browser gegenprüfen.)*

---

## 13. HANDOFF FÜR CODEX

**Zehn empfohlene Kandidaten / offene Plätze (vorläufige Reihenfolge):**
10) SharePoint/Box · 9) Semrush · 8) GitHub · 7) Hugging Face · 6) Notion · 5) vidIQ · 4) Google Drive · 3) Canva (EU-Ausblick) · 2) Adobe Express · 1) **PLATZ NOCH OFFEN** (HeyGen **oder** GitHub nach Live-Test).

**Zwingend live zu testen (dt. Konto):** GitHub, Adobe Express, vidIQ, Google Drive, Notion, HeyGen (danach Semrush, Hugging Face, SharePoint; Canva/Figma nur falls sichtbar).

**Berechtigungsdialoge aufnehmen für:** Google Drive („alle Dateien sehen/herunterladen"), Notion (Workspace), GitHub (Repo-Auswahl), Adobe/Canva/HeyGen (Konto-Login), Semrush (@-Tag/Login).

**Nicht behaupten:** DE-Verfügbarkeit ohne Live-Test; funktionierende Schreib-/Sende-/Löschfunktion bei Notion/Monday/Asana/Google Drive; Semrush verschickt automatisch Reports; „sichtbare Schaltfläche = funktioniert"; Canva/Figma in der EU nutzbar.

**Empfohlener finaler Videotitel (EMPFEHLUNG):** „ChatGPT-Apps 2026: Die 10 stärksten – und ob sie in Deutschland laufen"
**Alternativtitel:** „ChatGPT kann jetzt DAS: 10 Apps & Plugins mit Live-Test"

**Empfohlene Reihenfolge der Bildschirmaufnahmen:**
1) Terminologie/Verzeichnis (Plugin/App/Skill) · 2) Berechtigungsdialog-Beispiel · 3) Adobe/Canva (visuelles Wow) · 4) Google Drive (Alltag) · 5) vidIQ (Kanal) · 6) GitHub · 7) Hugging Face · 8) Notion · 9) Semrush · 10) HeyGen (Finale).

**Stärkster Demo-Fall:** Adobe Express / Canva – „ein Satz → fertiges Design" (sichtbarstes Vorher-Nachher).
**Stärkster Short:** Short 1 (Plugin vs. App vs. Connector) – klärt die Verwirrung, hohe Teilbarkeit.
**Größte Sicherheitswarnung:** Google-Drive-Berechtigung „alle Dateien sehen/herunterladen" – Lesen ≠ Löschen; erst Testordner.

**Fünf wichtigste Quellen-URLs:**
1. https://developers.openai.com/plugins/concepts/plugins
2. https://help.openai.com/en/articles/11487775-connectors-in-chatgpt
3. https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt-deep-research
4. https://www.canva.com/help/chatgpt-templates/
5. https://helpx.adobe.com/express/web/add-ons-and-integrations/chatgpt-integration-with-express.html

**Vor Veröffentlichung erneut zu prüfen:**
- Ist die jeweilige App im **deutschen** Konto sichtbar/nutzbar? (alle Kandidaten)
- Läuft Canva/Figma in der EU inzwischen? (aktuell ausgeschlossen)
- Adobe „global": im dt. Konto bestätigt?
- GitHub read-only + EWR-Verfügbarkeit weiterhin gültig?
- MCP-Connector-Tarif (Pro/Business) für Hugging Face/Cloudflare noch erforderlich?
- Notion/Monday/Asana: Schreiben in ChatGPT tatsächlich möglich? (nur nach Live-Test zeigen)
- Terminologie/Verzeichnis unverändert seit 09.07.2026?
- Alle genannten Tarif- und Kostenangaben am Aufnahmetag aktuell?

---

*Erstellt als Recherchepaket. Keine Konten verbunden, keine Drittanbieter autorisiert, kein Abo/Test gestartet, keine externe Aktion ausgeführt, keine Unteragenten verwendet. Alle Funktionsaussagen: NICHT LIVE GETESTET.*
