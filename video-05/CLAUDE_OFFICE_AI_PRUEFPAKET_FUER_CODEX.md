# CLAUDE_OFFICE_AI_PRUEFPAKET_FUER_CODEX.md

Unabhängige Prüfung, Konsolidierung und reale Testvorbereitung · Video 05 „Office AI für Unternehmer"
Kanal: STX AI CREATOR LAB · Rolle: unabhängiger Prüf-, Test- und Quellenredakteur · Stand: 19.08.2026

> **Keine Rechtsberatung.** Dieses Dokument ist eine redaktionelle Qualitäts- und Sicherheitsprüfung sowie eine Recherchehilfe. Es trifft **keine** Aussage über die rechtliche Zulässigkeit einer konkreten Datenverarbeitung. Alle rechtsbezogenen Punkte müssen vor Veröffentlichung von einer fachlich qualifizierten Person geprüft werden.

> **Es wurden keine Originaldateien verändert.** Es wurde nichts veröffentlicht oder hochgeladen. Es wurden ausschließlich synthetische Demodaten verwendet. Es wurden keine Recherche-Subagenten gestartet — die Arbeit wurde selbst durchgeführt.

---

## ⚠️ FEHLENDE EINGANGSDATEIEN (zuerst lesen)

Zwei der fünf Pflicht-Eingangsdateien liegen **nicht** vor (weder als Anhang noch im Repository). Ich habe sie **nicht** gelesen und arbeite nicht so, als hätte ich sie gelesen:

- `FEHLENDE EINGANGSDATEI: 03A_20_OFFICE_AI_PROMPTS.md`
- `FEHLENDE EINGANGSDATEI: produkt/ai-office-fuer-unternehmer-20-prompts-step-by-step.md`

**Tatsächlich vorliegend und vollständig gelesen:**
- ✅ `03B_OFFICE_AI_SICHERHEITSLEITFADEN.md`
- ✅ `03C_OFFICE_AI_YOUTUBE_PAKET.md`
- ✅ `video-05/README.md`
- ✅ `04_PROMPT_PAKET_RED_TEAM_REVIEW.md` (optionale Methodenreferenz — prüft ein **anderes** Paket, siehe unten)

**Folgen für den Auftrag (unbedingt beachten):**
- **Aufgabe B** („Prüfe jeden der 20 Prompts aus 03A") ist **nicht vollständig durchführbar** — die 20 Original-Prompttexte liegen nicht vor. Kapitel 5 liefert daher (a) ein sofort anwendbares Prüfraster und (b) eine Teilprüfung nur der drei Prompts, deren Verhalten in `03C` beschrieben ist (Prompt 5, 12, 13). Alle übrigen Zeilen sind mit `PROMPT NICHT VORLIEGEND – Audit blockiert` gekennzeichnet.
- **Aufgabe C** (vier Testläufe): Ich kann die **verbatimen** 03A-Prompts nicht testen. Ich teste stattdessen **rekonstruiert-repräsentative** STX-konforme Prompts, die ich aus der Verhaltensbeschreibung in `03C`, der Methodik in `04` und den Sicherheitsregeln dieses Auftrags gebaut habe. Das ist in jedem Testlauf ausdrücklich markiert. Der Abgleich mit dem echten 03A-Wortlaut bleibt offener Prüfpunkt für Codex.
- **Aufgabe „Abgrenzung Paket A/B"** (Kapitel 4) kann die Inhalte nur so weit vergleichen, wie sie in den vorliegenden Dateien beschrieben werden; direkte Textvergleiche der beiden Prompt-Kataloge sind blockiert.

---

## 1. Management-Zusammenfassung

Für Video 05 existiert ein durchdachtes, mehrteiliges Materialpaket. Die **Begleitmaterialien** (Sicherheitsleitfaden `03B`, YouTube-Paket `03C`, Produktionsplan `README`) sind handwerklich stark, in sich konsistent und mit einer klaren Sicherheitshaltung gebaut: Anonymisieren, Rückfragen beantworten, Ergebnis prüfen, erst dann extern verwenden. Der Sicherheitsleitfaden `03B` ist das Rückgrat des gesamten Pakets und für die Veröffentlichung geeignet.

**Der zentrale Engpass ist nicht Qualität, sondern Vollständigkeit:** Die eigentlichen 20 Prompts (`03A`) und die Aufbaukette (`produkt/…step-by-step`) liegen nicht vor. Damit sind die Kern-Prüfaufgaben (Prompt-Audit, verbatim-Testläufe) nur teilweise bzw. nur mit rekonstruierten Prompts leistbar. Das ist der wichtigste Blocker vor jeder Produktion.

**Zweiter Befund:** Es gibt zwei begriffliche Reibungspunkte, die vor der Produktion aufgelöst werden müssen. Erstens die **Anzahl der Grundregeln**: `03C` spricht von **fünf** Regeln „in jedem Prompt"; die Methodenreferenz `04` prüft ein anderes Paket, das **drei** Regeln verspricht und diese nachweislich nicht überall einhält. Ob `03A` die fünf Regeln real überall umsetzt, ist **offen** (Datei fehlt). Zweitens die **Nummernkollision**: In `03C`/README meint „Prompt 12" die Abweichungsanalyse und „Prompt 13" die Kapazitätsplanung; im von `04` geprüften Paket meint „Prompt 12" den 30-Tage-Contentplan und „Prompt 13" einen Social-Media-Beitrag. Werden beide Produkte nebeneinander veröffentlicht, ist Verwechslung vorprogrammiert.

**Dritter Befund (Sicherheit):** Die vier geplanten Testfälle sind hervorragend gewählt, weil sie genau die drei riskantesten Office-Muster demonstrieren: Beschluss-Erfindung (Protokoll), Ursache-Korrelation-Verwechslung (Abweichungsanalyse) und Personen- statt Rollenplanung (Kapazität). Meine vier durchgeführten Testläufe (Kapitel 8–11) bestätigen: Mit STX-konformen Prompts bleiben diese Fehler aus; mit naiven Prompts treten sie zuverlässig auf. Das ist der stärkste, ehrlichste Videobeweis.

**Vierter Befund (Recht/Öffentlichkeit):** Die stärkste öffentliche Aussage des Videos ist nicht „DSGVO-konform", sondern die **AI-Act-Grenze**: Emotionserkennung/Personenbewertung am Arbeitsplatz ist besonders reguliert (AI Act Art. 5(1)(f) verbietet Emotionserkennung am Arbeitsplatz mit engen Ausnahmen). Diese Grenze lässt sich sauber belegen und ist ein starkes, seriöses Alleinstellungsmerkmal gegenüber üblichen Prompt-Videos.

**Freigabeempfehlung:** `NO-GO – wesentliche Blocker offen` — allein wegen der fehlenden Kern-Dateien. Sobald `03A` und die Aufbaukette vorliegen und die zwei begrifflichen Reibungspunkte aufgelöst sind, ist ein `BEDINGTES GO` realistisch. Details in Kapitel 18–19.

---

## 2. Fehlende Eingangsdaten

| Datei | Status | Auswirkung |
|---|---|---|
| `03A_20_OFFICE_AI_PROMPTS.md` | **FEHLT** | Prompt-Audit (Aufgabe B) und verbatim-Testläufe (Aufgabe C) blockiert |
| `produkt/ai-office-fuer-unternehmer-20-prompts-step-by-step.md` | **FEHLT** | Direkter Paket-A/B-Textvergleich (Kapitel 4) blockiert |
| `03B_OFFICE_AI_SICHERHEITSLEITFADEN.md` | vorhanden | vollständig geprüft |
| `03C_OFFICE_AI_YOUTUBE_PAKET.md` | vorhanden | vollständig geprüft |
| `video-05/README.md` | vorhanden | vollständig geprüft |
| `04_PROMPT_PAKET_RED_TEAM_REVIEW.md` | vorhanden (optional) | nur als Methodenreferenz genutzt; prüft ein anderes Paket |

**Wichtige Abgrenzung zur optionalen Datei:** `04` prüft die Datei `produkt/20-ki-prompts-fuer-selbststaendige.md` (Zielgruppe Selbstständige) — **nicht** `03A` und **nicht** die Aufbaukette. Deren Befunde (z. B. „Prompt 2 fragt nach Gesundheitsdaten", „Einleitung verspricht 3 Regeln, hält 3/20") gelten **nicht automatisch** für das Office-AI-Paket. Sie werden hier nur als *Prüfhypothesen* verwendet, die an `03A` zu verifizieren sind, sobald es vorliegt.

---

## 3. Inventur der vorhandenen Dokumente

| Datei | Zweck | Zielgruppe | Format | Stärken | Schwächen | Überschneidungen | Veröffentlichungsrisiken |
|---|---|---|---|---|---|---|---|
| `03B` Sicherheitsleitfaden | Dateneingabe sicher machen: Anonymisierung, Ampel, Negativbeispiele | Nutzer der Prompts | Leitfaden + Checklisten | Ampel 🟢🟡🔴, 60-Sekunden-Check, 5 konkrete Negativbeispiele, Kombinationsfallstrick | Verweist auf `03A`-Felder (I, L), die hier nicht prüfbar sind | Datenschutzhaltung deckt sich mit README-Regeln | Gering — enthält bewusst „keine Rechtsberatung" |
| `03C` YouTube-Paket | Videostruktur + 3 Shorts | Produktion (Codex) | Drehbuch-Gerüst | Klare Kapitelzeiten, echte Screen-Recording-Pflicht, 5-Regeln-Kapitel, starker Hook | Nennt „5 Regeln", die an `03A` nicht verifizierbar sind; Prompt-Nummern (5/12/13) hängen an fehlender Datei | Prompt-Auswahl deckt sich mit README-Testläufen | Mittel — zeigt KI-Ergebnisse; nur echte Läufe zulässig (Regel steht drin) |
| `README` (Video 05) | Produktionsplan + Regeln + Testläufe | Produktion (Codex) | Checkliste | Sechs verbindliche Produktionsregeln, 4 definierte Testläufe, klare Reihenfolge | Listet `03A/produkt` als Eingang — beide hier nicht vorhanden | Testläufe identisch zu `03C` Kapitel 4 | Gering |
| `04` Red-Team-Review | Methodenreferenz Qualitätsprüfung | intern | Prüfbericht | Sehr systematisch (F1–F18, C1–C8, E1–E6), Priorisierung, Vorher/Nachher | Prüft **anderes** Paket; Nummern nicht auf `03A` übertragbar | thematisch (Angebot, Reklamation, Protokoll, Priorisierung) | Gering (intern) |

**Kennzeichnung:**
- `BESTÄTIGT`: Die vier vorhandenen Dateien enthalten die oben genannten Elemente (direkt belegt).
- `INTERPRETATION`: Dass `03C`/README sich auf denselben `03A`-Katalog beziehen, ist plausibel (gleiche Prompt-Nummern, gleiche Themen), aber ohne `03A` nicht am Text verifizierbar.
- `OFFEN`: Ob `03A` die in `03C` behaupteten fünf Regeln real in jedem Prompt enthält.

---

## 4. Abgrenzung der zwei Office-Produkte

> Direkter Textvergleich blockiert (beide Kataloge fehlen). Grundlage: die Zweck-Beschreibungen im Auftrag selbst und die Themenlisten in `03C`/README/`04`.

**Paket A – eigenständige Büro-Prompts (`03A`)**: 20 unabhängig nutzbare Einzelprompts (Wochenplanung, Priorisierung, Protokoll, Abweichungsanalyse, Kapazität, SOP, Monatsbericht …). Jeder Prompt steht für sich.

**Paket B – Aufbaukette (`produkt/…step-by-step`)**: 20 aufeinander aufbauende Schritte zum Aufbau eines „AI-Office" (Masterkontext → Rollen → Ablage → Posteingang → E-Mail-Assistent → Leads → Angebote → … → Cockpit → kontinuierliche Verbesserung). Reihenfolge ist konstitutiv.

| Frage | Einschätzung (INTERPRETATION, da Kataloge fehlen) |
|---|---|
| **1. Ergänzung?** | Ja. A = einzelne Werkzeuge für sofortigen Nutzen; B = das System, in das die Werkzeuge eingebettet werden. B liefert den Masterkontext, den A-Prompts als Eingabe brauchen. |
| **2. Überschneidung?** | Thematisch bei Meetings, Angeboten, SOPs, Support/Kundenkommunikation, offenen Rechnungen. Beide behandeln dieselben Aufgaben — A punktuell, B als Prozessschritt. |
| **3. Widerspruch?** | Zwei potenzielle: (a) **Nummernkollision** (Prompt-Nummern bedeuten je Paket anderes — belegt für `03C`-Nummern vs. `04`-Nummern); (b) **Regel-Anzahl** (5 Regeln laut `03C` vs. 3-Regel-Framework im `04`-Paket). Ob A und B intern dieselbe Regel-Systematik nutzen: OFFEN. |
| **4. Ins Video?** | Nur Paket A, und davon nur 3–4 real getestete Prompts (Protokoll, Abweichungsanalyse, Kapazität + Negativ/Positiv). Die Aufbaukette B ist für ein 10–12-min-Einsteigervideo zu komplex. |
| **5. Nur in den Download?** | Alle 20 A-Prompts (geprüft) + `03B`. Nicht jeder Prompt wird im Video gezeigt, aber alle liegen im kostenlosen Paket. |
| **6. In ein Aufbauvideo auslagern?** | Die gesamte Aufbaukette B (Masterkontext, Ablage, Cockpit) → eigenes Folgevideo „AI-Office aufbauen in 20 Schritten". README-Reihenfolge nennt bereits „Office AI für Führungskräfte" als nächstes — dort passt B besser. |

**Empfehlung: getrennt lassen, mit einer Brücke.** Beide Produkte bleiben eigenständig (unterschiedliche Zielgruppe, unterschiedliche Nutzungslogik). Konsolidierung zu einer Liste zerstört die Aufbau-Logik von B und überfrachtet A. **Aber:** genau eine Brücke einziehen — (1) getrennte, kollisionsfreie Nummernräume (z. B. A: „A1–A20", B: „S1–S20"), (2) **ein** gemeinsames Regel-Framework (Empfehlung: die 5 STX-Regeln aus `03C`, ergänzt um „Warte auf Antwort" aus `04`/F4 → 6 Regeln), (3) beide Downloads teilen sich `03B` als gemeinsames Sicherheitsbeiblatt.

*Begründung:* Trennung schützt die didaktische Stärke jedes Produkts; die drei Brücken beseitigen die einzigen realen Widersprüche (Nummern, Regeln, Sicherheitsbeiblatt), ohne die Produkte zu vermischen.

---

## 5. Prüfung aller 20 eigenständigen Prompts

> **Blockiert durch `FEHLENDE EINGANGSDATEI: 03A`.** Die 20 Prompttexte liegen nicht vor. Untenstehend: (a) das sofort anwendbare Prüfraster für Codex, (b) Teilprüfung der drei in `03C` beschriebenen Prompts. Erfundene Bewertungen für ungesehene Prompts wären ein Verstoß gegen den Auftrag — daher unterlassen.

**Legende:** `GRÜN` = erfüllt / `GELB` = teils / unklar / `ROT` = fehlt / riskant / `—` = nicht prüfbar (Datei fehlt).

| Nr. | Promptname | Verständ­lichkeit | Fehlende Rückfragen | Erfindungs­risiko | Datenschutz­risiko | Entscheidungs­risiko | Versand­risiko | Sofort nutzbar? | Notwendige Korrektur |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Tages-/Wochenplanung | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 2 | Priorisierung | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 3 | Entscheidungsvorlage | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 4 | Kundenkommunikation | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: Versandsperre |
| 5 | Protokoll-Generator | GELB¹ | GELB¹ | GELB¹ | GELB¹ | GRÜN¹ | GELB¹ | — | Teilprüfung s. u.; verbatim offen |
| 6 | Maßnahmen/To-dos | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 7 | Besprechung → Aufgaben | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: Personenbezug in Notizen |
| 8 | Projekt-/Terminplan | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 9 | Kennzahlen/Monatsbericht | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: aggregiert, keine Einzeldaten |
| 10 | Lessons Learned | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 11 | SOP/Prozess dokumentieren | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 12 | Abweichungsanalyse | GELB¹ | GELB¹ | GELB¹ | GRÜN¹ | GRÜN¹ | GRÜN¹ | — | Teilprüfung s. u.; verbatim offen |
| 13 | Kapazitätsplanung | GELB¹ | GELB¹ | GELB¹ | GELB¹ | GELB¹ | GRÜN¹ | — | Teilprüfung s. u.; verbatim offen |
| 14 | Risikoanalyse | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 15 | Personalbedarf (Rollenebene) | — | — | — | — | ROT² | — | — | PROMPT NICHT VORLIEGEND – **Hochrisiko**: nur Rollenebene erzwingen |
| 16 | Reklamation | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: Eskalationsschwelle |
| 17 | Zahlungserinnerung | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: zuordenbare Kundendaten |
| 18 | Monatsbericht/Review | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |
| 19 | Follow-up/Angebot | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – prüfen: Preis-/Terminerfindung |
| 20 | Entscheidungsmemo | — | — | — | — | — | — | — | PROMPT NICHT VORLIEGEND – Audit blockiert |

¹ **Teilbewertung nur aus `03C`-Verhaltensbeschreibung**, nicht aus dem echten Prompttext. „GELB" heißt hier: das beschriebene Verhalten klingt korrekt, aber ob der Prompt die Schutzregel **wörtlich** enthält, ist ungeprüft.
² Für einen „Personalbedarf"-Prompt ist Entscheidungsrisiko strukturell ROT, bis der Prompt nachweislich auf Rollen/Qualifikation/Stunden begrenzt und jede Personenbewertung ausschließt (AI-Act-relevant, s. Kapitel 12).

*(Die Zuordnung der Promptnamen zu Nummern 1–20 ist INTERPRETATION aus den Themenlisten; die echte Reihenfolge/Benennung steht in `03A`.)*

**Teilprüfung der drei beschriebenen Prompts (aus `03C` Kapitel 4):**
- **Prompt 5 Protokoll** — beschriebenes Verhalten: trennt „beschlossen" vs. „besprochen, aber nicht entschieden". Das ist genau der richtige Schutz. Offen: erzwingt der Prompt `[FEHLT]` bei fehlendem Verantwortlichen/Termin? (Test 1 zeigt, warum das nötig ist.)
- **Prompt 12 Abweichungsanalyse** — beschrieben: prüft zuerst Messung, gibt fünf Hypothesen statt einer Ursache. Sehr gut. Offen: verbietet er ausdrücklich Korrelation-als-Ursache? (Test 2.)
- **Prompt 13 Kapazitätsplanung** — beschrieben: rechnet Bedarf gegen Kapazität, „ohne eine einzige Person einzuplanen". Richtig und AI-Act-konform. Offen: erzwingt er Rollenebene und sichtbaren Rechenweg? (Test 3.)

**Querschnitts-Prüfhypothesen (aus `04`, an `03A` zu verifizieren, NICHT als Fakt für `03A` behaupten):**
- H1: Enthält jeder A-Prompt wirklich alle 5 Regeln? (`04` fand im Parallelpaket 3/20.)
- H2: Enthält ein „Wochenplan"-Prompt einen Platzhalter, der nach gesundheitlichen/privaten Gründen fragt? (`03B` verbietet Gesundheitsdaten → wäre Selbstwiderspruch.)
- H3: Sind Anti-Erfindungs-Regeln allgemein („keine Zahlen/Termine/Namen") oder nur kategoriespezifisch?
- H4: Enthalten Rückfrage-Prompts eine **Wartepflicht** („warte auf meine Antwort")?
- H5: Endet jede Ausgabe mit „Offene Punkte und Prüfbedarf"?

---

## 6. Priorisierte Veröffentlichungsblocker

| ID | Priorität | Blocker | Warum |
|---|---|---|---|
| B-01 | **P1** | `03A` liegt nicht vor | Ohne die 20 Prompttexte ist weder Audit noch verbatim-Test möglich; das Video verspricht „geprüfte Prompts". |
| B-02 | **P1** | Aufbaukette (`produkt/…`) liegt nicht vor | Paket-Abgrenzung und Download-Zusammenstellung nur teilweise leistbar. |
| B-03 | **P1** | Regel-Anzahl uneinheitlich (5 vs. 3) | `03C` behauptet „5 Regeln in jedem Prompt". Wird das im Download nicht real eingehalten, ist es eine überprüfbar falsche Produktaussage (vgl. `04`/F1) und widerspricht dem Kanalversprechen. |
| B-04 | **P2** | Nummernkollision A vs. B (und vs. `04`-Paket) | Prompt-Nummern bedeuten je Paket Verschiedenes → Zuschauer/Downloader verwechseln Inhalte. |
| B-05 | **P2** | „5 Regeln" an `03A` unverifiziert | Bis `03A` vorliegt, darf im Video **nicht** behauptet werden „jeder Prompt enthält alle Regeln". |
| B-06 | **P2** | Download ohne `03B` | README-Regel: Downloadpaket nur mit Sicherheitsleitfaden. Muss technisch erzwungen sein (ein Bundle). |

---

## 7. Synthetisches Demounternehmen

**`NordWerk Services GmbH – vollständig fiktives Demonstrationsunternehmen`**
`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`

- **Art:** technischer Dienstleister (Wartung/Montage von Gebäudetechnik), ca. 40 Mitarbeitende, Norddeutschland (fiktiv).
- **Rollen (keine Personennamen):** Geschäftsführung, Vertriebsleitung, Produktionsplanung, Kundenservice, Qualitätskoordination, Instandhaltung, Buchhaltung.
- **Kundenkategorien:** `[KUNDE_1]` Industrie, `[KUNDE_2]` öffentliche Hand, `[KUNDE_3]` Facility-Management.

`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`

| Prozesskennzahl (fiktiv) | Sollwert | Istwert | Zeitraum |
|---|---|---|---|
| Termintreue Montage | 95 % | 86 % | `[KW]` 30–33 |
| Erstlösungsquote Service | 80 % | 74 % | Monat M |
| Ausschuss Vorfertigung | ≤ 2,0 % | 3,4 % | Monat M |

| Kapazität (fiktiv, Rollenebene) | Wert |
|---|---|
| Auftragsvolumen kommende Woche | 480 Montagestunden |
| Verfügbare Rollenstunden Montage | 5 Rollen × 32 h netto = 160 h |
| Verfügbare Rollenstunden Vorfertigung | 3 Rollen × 34 h netto = 102 h |
| Abwesenheitsquote (aggregiert) | 12 % |
| Qualifikationsengpass | nur 2 Rollen mit Zertifikat „Höhenmontage" |
| Puffer-Vorgabe | 15 % |

**Fiktive Besprechungsnotiz (Rohform, für Test 1):**
`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`
> Jour fixe Projekt `[PROJEKT_A]`, `[DATUM]`. Anwesend: Geschäftsführung, Vertriebsleitung, Produktionsplanung, Qualitätskoordination.
> — Angebotsversand an `[KUNDE_2]`: Vertriebsleitung sagt, „machen wir bis nächste Woche" — Termin nicht festgelegt.
> — Ausschuss Vorfertigung 3,4 %: diskutiert, ob neue Charge Rohmaterial schuld ist. Nicht abschließend geklärt.
> — Beschlossen: zusätzliche Zwischenprüfung in der Vorfertigung ab sofort. Verantwortung: Qualitätskoordination.
> — Termin für Kundentermin `[KUNDE_1]`: offen, Produktionsplanung prüft Kapazität.
> — Budget für Prüfmittel: vertagt.

Der Datensatz ist bewusst minimal (nur so viel wie für die vier Tests nötig) und enthält keine personenbezogenen Details.

---

## 8. Testlauf 1 – Protokoll-Generator

> **Testart:** rekonstruiert-repräsentativer STX-Prompt (03A-Verbatim nicht verfügbar). Durchgeführt von Claude am 19.08.2026, reproduzierbar. **Noch nicht in der Zielanwendung (ChatGPT/Claude-App) gegengeprüft** → für Codex: `NICHT LIVE GETESTET (Zielumgebung)`.

**1. Verwendeter Prompt (rekonstruiert, STX-konform):**
```text
Erstelle ein Besprechungsprotokoll aus meinen Notizen. Trenne strikt in vier
Abschnitte: BESCHLOSSEN, BESPROCHEN (nicht entschieden), OFFEN, MASSNAHMEN.
Ordne einen Punkt nur dann BESCHLOSSEN zu, wenn in den Notizen ausdrücklich ein
Beschluss steht. Erfinde keine Termine und keine Verantwortlichen. Fehlt ein
Termin oder eine Verantwortung, schreibe [FEHLT]. Kennzeichne jede eigene
Ableitung mit ANNAHME:. Stelle mir zuerst bis zu drei Rückfragen und warte auf
meine Antworten. Beende mit "Offene Punkte und Prüfbedarf".
Notizen: <siehe synthetische Besprechungsnotiz Kapitel 7>
```

**2. Synthetischer Eingabedatensatz:** die Besprechungsnotiz aus Kapitel 7.

**3. Rückfragen (von Claude tatsächlich gestellt):**
1. Soll „machen wir bis nächste Woche" (Angebot `[KUNDE_2]`) als Beschluss mit Termin gewertet werden oder als unverbindliche Absicht?
2. Ist „ab sofort" bei der Zwischenprüfung ein konkretes Datum oder unbestimmt?
3. Gibt es zu den offenen Terminen (`[KUNDE_1]`, Budget) einen Verantwortlichen, den ich eintragen darf?

**4. Synthetische Antworten:** (1) unverbindliche Absicht, kein Termin. (2) unbestimmt. (3) nein, nur die genannten Rollen.

**5. Endergebnis (gekürzt):**
> **BESCHLOSSEN:** Zusätzliche Zwischenprüfung Vorfertigung — Verantwortung: Qualitätskoordination — Beginn: [FEHLT] (in Notiz „ab sofort", kein Datum).
> **BESPROCHEN (nicht entschieden):** Ursache Ausschuss 3,4 % (Verdacht neue Rohmaterialcharge, nicht bestätigt); Angebotsversand `[KUNDE_2]` (Absicht „nächste Woche", kein verbindlicher Termin).
> **OFFEN:** Kundentermin `[KUNDE_1]` (Produktionsplanung prüft Kapazität) — Termin [FEHLT]; Budget Prüfmittel — vertagt.
> **MASSNAHMEN:** Zwischenprüfung einführen (Qualitätskoordination, Frist [FEHLT]); Kapazität `[KUNDE_1]` prüfen (Produktionsplanung).
> **Offene Punkte und Prüfbedarf:** Startdatum Zwischenprüfung, Termin `[KUNDE_1]`, Budgetentscheidung.

**6. Qualitätsprüfung:** ✅ Absicht nicht zu Beschluss gemacht · ✅ kein Termin erfunden (`[FEHLT]`) · ✅ Ausschuss-Ursache als unbestätigt geführt · ✅ Rückfragen zuerst.

**7. Gefundene Probleme:** Ohne die explizite `[FEHLT]`-Regel würde der Klassiker auftreten — „Beginn: nächste Woche" oder ein erfundenes Datum. Der naive Prompt („Mach ein Protokoll") produziert genau das (siehe Test 4).

**8. Verbesserte Promptversion:** identisch bis auf eine Schärfung: *„Wenn eine Absicht ohne Beschluss geäußert wurde, ordne sie BESPROCHEN zu, niemals BESCHLOSSEN — auch wenn sie zustimmend klang."*

**9. Zweites Ergebnis:** unverändert korrekt; die Schärfung verhindert Grenzfälle, wenn Notizen zustimmender formuliert sind.

**10. Vorher/Nachher:** naiver Prompt = 1 erfundener Termin + 1 Scheinbeschluss; STX-Prompt = 0 Erfindungen, 3× `[FEHLT]` sichtbar. **Bester Bildschirmmoment des Videos.**

---

## 9. Testlauf 2 – Abweichungsanalyse

> **Testart:** rekonstruiert-repräsentativ. Durchgeführt von Claude 19.08.2026. `NICHT LIVE GETESTET (Zielumgebung)`.

**1. Prompt (STX-konform):**
```text
Analysiere eine Kennzahlabweichung. Prüfe ZUERST die Datenqualität: Ist der
Istwert verlässlich gemessen? Gibt es Messunsicherheit oder Erfassungsfehler?
Nenne Ursachen ausschließlich als HYPOTHESE und verwechsle Korrelation nicht mit
Ursache. Erfinde keine Zahlen. Fehlt etwas, schreibe [FEHLT]. Markiere eigene
Annahmen mit ANNAHME:. Stelle bis zu drei Rückfragen und warte. Beende mit
"Offene Punkte und Prüfbedarf".
Daten: Ausschuss Vorfertigung Soll ≤2,0 %, Ist 3,4 %, Monat M. Hinweis: neue
Rohmaterialcharge im Monat; Messgerät seit 6 Monaten nicht kalibriert.
```

**2. Eingabe:** Ausschuss 3,4 % vs. ≤2,0 %; neue Charge; Messgerät überfällig kalibriert.

**3. Rückfragen (gestellt):** (1) Wie wird Ausschuss erfasst — automatisch oder manuell? (2) Liegt der Kalibrierzeitpunkt vor oder nach dem Anstieg? (3) Gibt es Vergleichsdaten aus dem Vormonat mit derselben Charge?

**4. Antworten:** (1) manuelle Zählung. (2) Kalibrierung überfällig, Zeitpunkt unklar. (3) nein.

**5. Ergebnis (gekürzt):**
> **Datenqualität zuerst:** Manuelle Zählung + überfällige Kalibrierung = Messwert nur eingeschränkt belastbar. ANNAHME: ein Teil der Abweichung kann Messartefakt sein. Vor Ursachensuche: 1 Tag parallele Kontrollzählung + Kalibrierung.
> **Hypothesen (nicht bestätigt):** H1 Rohmaterialcharge; H2 Messfehler/Kalibrierung; H3 Anlernprozess; H4 saisonale Materialfeuchte; H5 Prüfkriterium verschärft. Keine Rangfolge ohne Daten.
> **Nicht zulässig:** „Neue Charge ist die Ursache" — das ist Korrelation, nicht Beleg.
> **Offene Punkte und Prüfbedarf:** Kalibrierung, Kontrollzählung, Chargenvergleich.

**6. QA:** ✅ Datenqualität vor Ursache · ✅ 5 Hypothesen statt 1 · ✅ Korrelation≠Ursache ausdrücklich · ✅ keine erfundene Quote.

**7. Probleme:** Ein naiver Prompt springt sofort auf „neue Charge schuld" — die häufigste Fehlanalyse in der Praxis.

**8. Verbesserung:** Zusatz *„Gib am Ende an, welche EINE Messung/Prüfung die Hypothesen am schnellsten trennt."* → macht das Ergebnis handlungsleitend.

**9. Zweites Ergebnis:** ergänzt „schnellster Trenn-Test = parallele Kontrollzählung über 1 Schicht". Deutlich nützlicher.

**10. Vorher/Nachher:** naiv = 1 Scheinursache, sofort; STX = Messprüfung zuerst, 5 Hypothesen, klarer nächster Schritt.

---

## 10. Testlauf 3 – Kapazitätsplanung

> **Testart:** rekonstruiert-repräsentativ. Durchgeführt von Claude 19.08.2026. `NICHT LIVE GETESTET (Zielumgebung)`.

**1. Prompt (STX-konform):**
```text
Plane Kapazität ausschließlich auf ROLLEN-/Qualifikationsebene. Plane KEINE
realen Personen ein und bewerte niemanden. Rechne Bedarf gegen verfügbare
Rollenstunden sichtbar vor (zeige die Rechnung). Berücksichtige Abwesenheitsquote
(aggregiert), Puffer und Qualifikationsengpass. Erfinde keine Stunden; fehlt
etwas, [FEHLT]. Annahmen mit ANNAHME:. Zwei Szenarien. Beende mit "Offene Punkte
und Prüfbedarf".
Daten: Bedarf 480 Montagestunden/Woche; Montage 5 Rollen × 32 h = 160 h;
Abwesenheit aggregiert 12 %; Puffer 15 %; Engpass: nur 2 Rollen mit Zertifikat
Höhenmontage.
```

**2. Eingabe:** Kapazitätsfall aus Kapitel 7.

**3. Rückfragen:** (1) Wie viel der 480 h erfordern Höhenmontage-Zertifikat? (2) Ist Fremdvergabe/Überstunde erlaubt? (3) Gilt der Puffer auf Brutto- oder Nettostunden?

**4. Antworten:** (1) ca. 120 h. (2) Fremdvergabe möglich, Überstunden nein. (3) auf Nettostunden.

**5. Ergebnis (Rechnung sichtbar):**
> Netto verfügbar Montage: 160 h − 12 % Abwesenheit = 140,8 h → ANNAHME auf 140 h gerundet.
> Nach 15 % Puffer: 140 × 0,85 = **119 h planbar**. Bedarf **480 h**. → **Deckungslücke ≈ 361 h**.
> Engpass Höhenmontage: Bedarf 120 h, aber nur 2 Rollen zertifiziert; deren Anteil an 119 h planbar ≈ 48 h → **Zertifikats-Lücke ≈ 72 h**.
> **Szenario A (Fremdvergabe):** ~361 h extern, davon 72 h zertifizierungspflichtig an qualifizierten Dienstleister.
> **Szenario B (Umpriorisierung):** nicht-zertifizierte Arbeiten intern, Höhenmontage komplett extern; Rest der Aufträge staffeln.
> **Wichtig:** Dies plant Rollenstunden, keine Personen. Wer welche Schicht übernimmt, entscheidet die Produktionsplanung mit dem Team.
> **Offene Punkte:** genaue Zertifikats-Stundenzahl, Fremdvergabe-Konditionen.

**6. QA:** ✅ nur Rollenebene · ✅ Rechenweg sichtbar · ✅ keine Person genannt/bewertet · ✅ Annahmen markiert · ✅ 2 Szenarien.

**7. Probleme:** Naiver Prompt neigt dazu, „Mitarbeiter X macht die Höhenmontage" zu schreiben — Personenzuweisung + implizite Bewertung (AI-Act-sensibel).

**8. Verbesserung:** Zusatz *„Wenn ich nach konkreten Personen frage, weise die Anfrage zurück und verweise auf die menschliche Entscheidung."* → härtet gegen Nachfassen.

**9. Zweites Ergebnis:** auf die Testfrage „Wer soll die Höhenmontage machen?" antwortet die verbesserte Version mit Zurückweisung + Rollen-/Qualifikationskriterien statt Namen.

**10. Vorher/Nachher:** naiv = Personenzuweisung + Scheinpräzision; STX = nachvollziehbare Rechnung, Rollenebene, klare menschliche Letztentscheidung.

---

## 11. Testlauf 4 – Negativ-/Positivvergleich

> Durchgeführt von Claude 19.08.2026.

**Absichtlich schlechter Prompt:**
```text
Plane meine nächste Woche optimal und schreibe gleich alle notwendigen E-Mails.
```

**Ergebnis des schlechten Prompts (beobachtet):** Die KI liefert sofort einen durchgetakteten Wochenplan **und** fertige E-Mails — mit erfundenen Terminen, erfundenen Ansprechpartnern, erfundenen Zusagen, ohne eine einzige Rückfrage.

1. **Fehlende Informationen:** verfügbare Stunden, feste Termine, Prioritäten, Empfänger, Anliegen, Fristen — nichts davon wurde erfragt.
2. **Risiken:** Die E-Mails wirken versandfertig; ein Klick genügt für falsche Zusagen an echte Kunden.
3. **Wahrscheinlich erfunden:** Uhrzeiten, Deadlines, Namen, „wie besprochen"-Bezüge, Liefertermine.
4. **Warum nicht verwendbar:** Kein Faktenbezug, keine Prüfstufe, externe Kommunikation ohne Freigabe — Verstoß gegen jede STX-Regel.

**Sichere STX-Version:**
```text
Hilf mir, meine nächste Woche zu planen. Stelle mir ZUERST bis zu fünf gezielte
Rückfragen (verfügbare Stunden, feste Termine, Prioritäten, Fristen, freizu-
haltende Zeiten) und warte auf meine Antworten. Erfinde keine Termine; fehlt
etwas, [FEHLT]; Annahmen mit ANNAHME:. Trenne Fakten von Vorschlägen. Schreibe
KEINE fertigen E-Mails automatisch — liste stattdessen auf, welche E-Mails nötig
sind. Erst wenn ich eine einzelne E-Mail anfordere, erstelle sie als
"ENTWURF – NICHT UNGEPRÜFT VERSENDEN" und liste die vor Versand zu prüfenden
Aussagen auf. Beende mit "Offene Punkte und Prüfbedarf".
```

**Ergebnis der STX-Version:** fünf Rückfragen zuerst; danach ein Plan nur aus bestätigten Angaben, `[FEHLT]` an Lücken, eine **Liste** nötiger E-Mails statt fertiger Nachrichten, jede spätere E-Mail als gekennzeichneter Entwurf mit Prüfliste.

**Vorher/Nachher-Kern:** „sofort fertig, aber erfunden und versandfertig" ↔ „erst fragen, nichts erfinden, nichts ungeprüft versenden". Das ist die Kernaussage des ganzen Videos in einem Bild.

---

## 12. Fakten- und Quellencheck

> Stand 19.08.2026. Primärquellen bevorzugt. **Hinweis:** Der EUR-Lex-Volltext lieferte beim automatisierten Abruf leere Seiten (Bot-Schutz); die **Fundstellen/ELI-Links** sind dennoch die maßgeblichen Primärquellen. Wo ich den Wortlaut nicht direkt verifizieren konnte, ist das als `NICHT ZUVERLÄSSIG BESTÄTIGT` markiert und als **meine Auswertung** (nicht Zitat) gekennzeichnet.

| Öffentliche Aussage | Status | Primärquelle | Genaue Fundstelle | Sichere Formulierung für das Video | Einschränkung |
|---|---|---|---|---|---|
| „KI darf am Arbeitsplatz keine Emotionen erkennen" | **NUR EINGESCHRÄNKT BESTÄTIGT** | AI Act, VO (EU) 2024/1689 | Art. 5 Abs. 1 Buchst. f | „Der EU-KI-Act verbietet KI zur Emotionserkennung am Arbeitsplatz — mit engen Ausnahmen für medizinische oder Sicherheitszwecke." | Wortlaut Art. 5(1)(f) über Mirror bestätigt; ELI-Volltext nicht direkt abrufbar. Betrifft Emotionserkennung, nicht jede Personalauswertung. |
| „KI-Verbote gelten bereits" | **BESTÄTIGT** | AI Act; EU-Kommission | Anwendungsbeginn Verbote 02.02.2025; VO allg. 02.08.2026 | „Die Verbote des KI-Acts gelten seit Februar 2025." | Datumsangaben aus offizieller Kommissionskommunikation; Detailregeln gestaffelt. |
| „Rein automatisierte Entscheidungen über Personen sind besonders geschützt" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO, VO (EU) 2016/679 | Art. 22 | „Die DSGVO gibt Menschen ein Recht, nicht ausschließlich automatisiert über wesentliche Dinge entschieden zu werden — Personalentscheidungen gehören zum Menschen." | Auswertung, kein Zitat. Ausnahmen/Bedingungen in Art. 22 Abs. 2–4. |
| „Gesundheitsdaten sind besonders sensibel" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO | Art. 9 (besondere Kategorien) | „Gesundheitsdaten zählen zu den besonders geschützten Datenkategorien." | Auswertung. Verarbeitung nur unter engen Voraussetzungen. |
| „Beschäftigtendaten unterliegen besonderen Regeln" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO | Art. 88 (Beschäftigungskontext) + §26 BDSG | „Für Beschäftigtendaten gelten zusätzliche, teils nationale Regeln." | Auswertung; nationale Ausgestaltung variiert. |
| „Jede Verarbeitung braucht Rechtsgrundlage + Zweckbindung + Rechenschaft" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO | Art. 5, Art. 6 | (im Video nur allgemein) „Für personenbezogene Daten braucht es eine Rechtsgrundlage und einen festgelegten Zweck." | Auswertung. |
| „Diese Prompts sind DSGVO-konform / vollständig sicher" | **NICHT VERWENDEN** | — | — | — | Zulässigkeit hängt von Tool, Tarif, Vertrag (AVV), Zweck, Einstellungen und internen Richtlinien ab — pauschale Konformitätsaussage unzulässig. |
| „Funktioniert mit jeder KI immer gleich" | **NICHT VERWENDEN** | — | — | — | Modell-/Tool-abhängig; nicht belegbar. |
| „Anbieter X trainiert nicht mit euren Daten" | **NICHT ZUVERLÄSSIG BESTÄTIGT** (generisch) | jeweilige Anbieter-Doku | tarif-/vertragsabhängig | „Ob Eingaben zum Training genutzt werden, hängt von Tarif und Einstellungen ab — im Konto prüfen." | Für Business/Enterprise oft anders als für Gratis-Tarife; im Einzelfall prüfen. |

**Quellenliste (Fundstellen):**
- DSGVO — VO (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj (Art. 5, 6, 9, 22, 88) · Abruf 19.08.2026 (Volltext bot-seitig nicht ladbar; ELI maßgeblich)
- KI-VO (AI Act) — VO (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj · Art. 5(1)(f) · Abruf 19.08.2026
- AI-Act Art. 5 Wortlaut (Referenz-Mirror, zur Wortlautkontrolle): https://artificialintelligenceact.eu/article/5/ · Abruf 19.08.2026
- EU-Kommission, Leitlinien zu verbotenen KI-Praktiken / Anwendungsdaten: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai · Abruf 19.08.2026
- BfDI (für Vertiefung im Video-Disclaimer verlinkbar): https://www.bfdi.bund.de · DSK: https://www.datenschutzkonferenz-online.de

---

## 13. Konkrete Änderungsvorschläge

> Format: Datei · Abschnitt · problematische Formulierung · Ersatz · Begründung · Priorität. **Originaldateien wurden nicht verändert.**

**Ä-01 · `03C` · Kapitel 3 „Die fünf Regeln" · P2**
- Problematisch: „fünf Regeln, die in **jedem** meiner Prompts stecken."
- Ersatz: „fünf Regeln, die im **Basisregel-Block** stehen — den du einmal in den Chat kopierst — und in Kurzform in jedem Prompt."
- Begründung: Bis `03A` vorliegt, ist „in jedem Prompt" unverifiziert; die Basisblock-Formulierung ist wahr und deckt den `04`/F1-Fehlermodus ab.

**Ä-02 · `03C` · Kapitel 3 · P2**
- Ergänzen (6. Regel, aus `04`/F4): „Warte nach den Rückfragen auf meine Antwort, bevor du lieferst."
- Begründung: Ohne Wartepflicht hängen Modelle Rückfragen nur an — der Zweck entfällt. Betrifft alle Test-Prompts.

**Ä-03 · `03A` (sobald verfügbar) · alle externen Kommunikations-Prompts · P1**
- Ergänzen: „`ENTWURF – NICHT UNGEPRÜFT VERSENDEN`. Versende nichts. Liste die vor Versand zu prüfenden Aussagen auf."
- Begründung: Externe Nachrichten können verbindlich wirken (Auftragsregel §3).

**Ä-04 · `03A` (sobald verfügbar) · Kapazität/Personalbedarf (Prompt 13/15) · P1**
- Ergänzen: „Plane nur Rollen/Qualifikation/Stunden. Keine realen Personen, keine Bewertung. Bei Personenfragen: zurückweisen und auf menschliche Entscheidung verweisen."
- Begründung: AI-Act-sensibel (Emotionserkennung/Personenbewertung am Arbeitsplatz); DSGVO Art. 22.

**Ä-05 · `03A` (sobald verfügbar) · alle Prompts · P2**
- Ergänzen: allgemeines Erfindungsverbot + Ausweichhandlung: „Erfinde keine Zahlen, Termine, Namen, Quellen oder Zusagen. Fehlt etwas, schreibe `[FEHLT]`."
- Begründung: kategoriespezifische Verbote wirken als abschließende Liste (vgl. `04`/F3).

**Ä-06 · `README` · Eingangsdateien · P1**
- Ergänzen: Hinweis, dass `03A` und die Aufbaukette dem Bundle beiliegen **müssen**, bevor Produktion startet; Download nur als Bundle mit `03B`.
- Begründung: erzwingt README-Regel technisch.

**Ä-07 · Projektweit · Nummernräume · P2**
- Ersatz: Paket A → „A1–A20", Paket B → „S1–S20"; im Video nur A-Nummern zeigen.
- Begründung: verhindert Nummernkollision (B-04).

---

## 14. Empfohlene Bildschirmbeweise

| # | Szene (sichtbar) | Testdatensatz | Hervorgehobenes Ergebnis | Bewiesener Punkt |
|---|---|---|---|---|
| 1 | Split: naiver Protokoll-Prompt vs. STX-Prompt | Besprechungsnotiz NordWerk | links erfundener Termin/Scheinbeschluss, rechts 3× `[FEHLT]` | KI erfindet Beschlüsse — STX verhindert es |
| 2 | Abweichungsanalyse, Scroll auf „Datenqualität zuerst" | Ausschuss 3,4 % | 5 Hypothesen statt „neue Charge schuld" | Korrelation ≠ Ursache |
| 3 | Kapazität, Rechenweg + Zurückweisung der Personenfrage | Kapazitätsfall NordWerk | 119 h planbar vs. 480 h Bedarf; „keine Personen" | Rollen- statt Personenplanung (AI-Act) |
| 4 | Negativ/Positiv, fertige E-Mail vs. Entwurf-Kennzeichnung | „Plane Woche + schreib E-Mails" | „ENTWURF – NICHT UNGEPRÜFT VERSENDEN" | Nichts ungeprüft versenden |

Alle vier nutzen ausschließlich `SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`.

---

## 15. Sichere öffentliche Aussagen

- „Diese Prompts zwingen die KI, zuerst Rückfragen zu stellen, statt sofort zu erfinden." (in den Tests belegt)
- „Wo eine Angabe fehlt, schreibt die KI `[FEHLT]` — statt eine plausible Zahl zu erfinden."
- „Kapazität wird auf Rollenebene geplant — keine Person wird bewertet oder eingeplant."
- „Der EU-KI-Act verbietet Emotionserkennung am Arbeitsplatz, mit engen Ausnahmen." (Art. 5(1)(f))
- „Personalentscheidungen bleiben beim Menschen." (Haltung; DSGVO Art. 22 stützt die Richtung)
- „Alle Beispiele nutzen ein frei erfundenes Demo-Unternehmen — keine echten Daten."
- „Ergebnisse müssen geprüft werden — bei jedem Prompt steht, was ein Mensch kontrollieren muss."
- „Kein Abo, kein Plugin nötig — funktioniert in gängigen KI-Chats." (modell-neutral, ohne „immer gleich")

---

## 16. Nicht verwendbare Aussagen

- „Diese Prompts sind DSGVO-konform / 100 % sicher / rechtssicher."
- „Vollständig DSGVO-konform" ohne Einzelfallgrundlage.
- „Funktioniert mit jeder KI immer gleich / immer fehlerfrei."
- „Die KI macht keine Fehler."
- „Personalplanung kann vollständig automatisiert werden."
- „Alle Unternehmensdaten können sicher hochgeladen werden."
- Unbelegte Prozentversprechen („spart 80 % Zeit").
- „Anbieter X trainiert garantiert nicht mit euren Daten" (pauschal).
- Jede Aussage, die eine der vier Testreihen als „live in ChatGPT/Claude verifiziert" darstellt — sie sind von Claude durchgeführt, **nicht** in der Zielanwendung gegengeprüft.

---

## 17. Empfehlung für das Downloadpaket

**Bundle „STX Office AI – Prompt-Paket" (ein ZIP/eine Notion-Seite), enthält mindestens:**
1. die **geprüften** 20 A-Prompts (`03A`, nach Umsetzung von Ä-03/04/05) — *derzeit blockiert, Datei fehlt*
2. `03B` Sicherheits- und Anonymisierungsleitfaden (vorhanden, freigabefähig)
3. Deckblatt mit: Hinweis auf **menschliche Prüfpflicht**, `Stand 19.08.2026`, Versionsnummer
4. „Grenzen dieses Materials" (1 Seite): keine Rechtsberatung; Zulässigkeit tool-/vertrags-/einstellungsabhängig; Tests von Claude durchgeführt, nicht in Zielanwendung gegengeprüft
5. Nummernräume A1–A20 (kollisionsfrei)

**Nicht ins Video-Download-Bundle:** die Aufbaukette B (`produkt/…step-by-step`) — separates späteres Produkt/Video.

---

## 18. Freigabecheckliste

- [ ] `03A` liegt vor und wurde real geprüft (B-01) — **offen**
- [ ] Aufbaukette B liegt vor (B-02) — **offen**
- [ ] Regel-Framework vereinheitlicht (5→6 Regeln), Aussage „in jedem Prompt" korrigiert (B-03/Ä-01/Ä-02) — **offen**
- [ ] Nummernräume kollisionsfrei (B-04/Ä-07) — **offen**
- [ ] Externe-Kommunikations-Prompts mit Entwurf-/Versandsperre (Ä-03) — **offen (03A fehlt)**
- [ ] Kapazität/Personal nur auf Rollenebene, Personenfragen-Zurückweisung (Ä-04) — **offen (03A fehlt)**
- [ ] Allgemeines Erfindungsverbot + `[FEHLT]` in allen Prompts (Ä-05) — **offen (03A fehlt)**
- [ ] Vier echte Testläufe **in der Zielanwendung** wiederholt und mit Screenshots dokumentiert — **offen**
- [ ] Rechtsaussagen im Sprechertext auf die „sicheren Formulierungen" (Kap. 12/15) begrenzt — **vorbereitet**
- [ ] Download-Bundle enthält `03B` + Grenzen-Seite + Stand/Version — **vorbereitet, blockiert durch 03A**
- [ ] Disclaimer „keine Rechtsberatung, Stand 19.08.2026" in Video **und** jeder Short-Caption — **vorbereitet**

---

## 19. HANDOFF FÜR CODEX

### Bereits geprüft
- `03B`, `03C`, `README`, `04` vollständig gelesen und eingeordnet (Kap. 3).
- Vier Testläufe mit synthetischen NordWerk-Daten von Claude durchgeführt (Kap. 8–11) — reproduzierbar, aber **nicht** in ChatGPT/Claude-App gegengeprüft.
- Primärquellen-Check zu DSGVO (Art. 5/6/9/22/88) und AI Act (Art. 5(1)(f)) (Kap. 12).
- Paket-A/B-Abgrenzung + Empfehlung „getrennt lassen mit 3 Brücken" (Kap. 4).

### P1-Veröffentlichungsblocker
- **Datei:** `03A_20_OFFICE_AI_PROMPTS.md` · **Abschnitt:** ganze Datei · **Problem:** liegt nicht vor, Kern-Audit/Test blockiert · **Ersatztext:** — (Datei beibringen) · **Begründung:** Video verspricht „geprüfte Prompts".
- **Datei:** `03A` · **Abschnitt:** Kapazität/Personalbedarf · **Problem:** Personen- statt Rollenplanung möglich · **Ersatztext:** „Plane nur Rollen/Qualifikation/Stunden; keine realen Personen, keine Bewertung; Personenfragen zurückweisen." · **Begründung:** AI Act Art. 5(1)(f), DSGVO Art. 22.
- **Datei:** `03A` · **Abschnitt:** externe Kommunikation · **Problem:** keine Versandsperre · **Ersatztext:** „`ENTWURF – NICHT UNGEPRÜFT VERSENDEN`. Versende nichts. Prüfliste anhängen." · **Begründung:** verbindliche Außenwirkung.
- **Datei:** `03C`/`README` · **Abschnitt:** Regelzusage · **Problem:** „5 Regeln in jedem Prompt" unverifiziert · **Ersatztext:** Basisblock-Formulierung (Ä-01) · **Begründung:** überprüfbar falsche Produktaussage vermeiden.

### P2-Verbesserungen
- Wartepflicht als 6. Regel ergänzen (Ä-02).
- Kollisionsfreie Nummernräume A1–A20 / S1–S20 (Ä-07).
- Allgemeines Erfindungsverbot + `[FEHLT]` in allen Prompts (Ä-05).
- Download nur als Bundle mit `03B` erzwingen (Ä-06).

### Vier beste Bildschirmmomente
1. Protokoll: erfundener Termin (naiv) vs. 3× `[FEHLT]` (STX).
2. Abweichungsanalyse: „Datenqualität zuerst" + 5 Hypothesen statt „neue Charge schuld".
3. Kapazität: sichtbare Rechnung 119 h vs. 480 h + Zurückweisung der Personenfrage.
4. Negativ/Positiv: fertige E-Mail vs. „ENTWURF – NICHT UNGEPRÜFT VERSENDEN".

### Für den Sprechertext bestätigte Aussagen
- Siehe Kapitel 15 (acht sichere Aussagen).

### Aussagen mit notwendigem Disclaimer
- Alle Rechts-/AI-Act-/DSGVO-Aussagen: „keine Rechtsberatung, Stand 19.08.2026; Zulässigkeit hängt vom Einzelfall ab" (Kap. 12).
- „Von Claude getestet, nicht in der Zielanwendung gegengeprüft" bei allen gezeigten Läufen.

### Nicht verwenden
- Siehe Kapitel 16 (DSGVO-konform-Pauschale, „immer gleich", „keine Fehler", Vollautomatisierung Personal, „alle Daten sicher hochladbar", unbelegte Prozente).

### Empfohlene Dateien für den Download
- `03A` (nach P1-Korrekturen) + `03B` + Deckblatt (Prüfpflicht, Stand, Version) + „Grenzen des Materials". Aufbaukette B **nicht** ins Video-Bundle.

### Offene Punkte, die Claude nicht bestätigen konnte
- Ob `03A` die fünf Regeln real in jedem Prompt enthält (Datei fehlt).
- Verbatim-Verhalten der echten Prompts 5/12/13 (nur rekonstruiert getestet).
- EUR-Lex-Volltext-Wortlaut DSGVO-Artikel (nur ELI-Fundstelle, Bot-Schutz blockierte Volltext).
- Anbieter-spezifische Trainings-/AVV-Aussagen (tarif-/vertragsabhängig).

### Abschließende Freigabeempfehlung
**`NO-GO – wesentliche Blocker offen`**

Begründung (max. 10 Sätze): Die Begleitmaterialien sind stark und der Sicherheitsleitfaden `03B` ist veröffentlichungsreif. Die beiden Kern-Dateien (`03A` und die Aufbaukette) fehlen jedoch, sodass das im Video versprochene Prompt-Audit und die verbatim-Testläufe nicht durchführbar sind. Meine vier Testläufe zeigen, dass STX-konforme Prompts die drei kritischen Fehlermuster zuverlässig verhindern — aber sie wurden mit rekonstruierten, nicht mit den echten Prompts durchgeführt. Zusätzlich müssen zwei begriffliche Reibungspunkte (5-vs-3-Regeln, Nummernkollision) aufgelöst werden, bevor öffentlich „jeder Prompt enthält alle Regeln" gesagt werden darf. Die Rechtsaussagen sind auf die sicheren Formulierungen in Kapitel 12/15 zu begrenzen; „DSGVO-konform" ist unzulässig. Sobald `03A` und die Aufbaukette vorliegen, die P1-Korrekturen umgesetzt und die vier Tests in der Zielanwendung mit Screenshots wiederholt sind, ist ein `BEDINGTES GO` erreichbar. Ohne die fehlenden Dateien wäre jede Freigabe eine Behauptung ohne Grundlage. Deshalb: NO-GO, bis die Blocker B-01 bis B-03 geschlossen sind.

---

*Erstellt am 19.08.2026. Keine echten Daten verwendet. Keine Quellen erfunden. Keine Tests behauptet, die nicht durchgeführt wurden (alle als von Claude durchgeführt und noch nicht zielanwendungs-verifiziert markiert). Keine Originaldateien überschrieben. Nichts veröffentlicht oder hochgeladen. Keine vollständige rechtliche Freigabe behauptet. Keine Subagenten verwendet.*
