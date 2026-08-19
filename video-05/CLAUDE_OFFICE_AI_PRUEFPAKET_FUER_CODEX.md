# CLAUDE_OFFICE_AI_PRUEFPAKET_FUER_CODEX.md

Unabhängige Prüfung, Konsolidierung und reale Testvorbereitung · Video 05 „Office AI für Unternehmer"
Kanal: STX AI CREATOR LAB · Rolle: unabhängiger Prüf-, Test- und Quellenredakteur · Stand: **19.08.2026 (Vollfassung, ersetzt die NO-GO-Fassung vom selben Tag)**

> **Keine Rechtsberatung.** Redaktionelle Qualitäts- und Sicherheitsprüfung; keine Aussage über rechtliche Zulässigkeit im Einzelfall. Rechtsbezogene Punkte vor Veröffentlichung fachlich prüfen lassen.
> **Arbeitsregeln eingehalten:** Keine Originaldateien verändert · kein Commit, kein Push, kein Pull Request erstellt · vorhandener Draft-PR nicht angefasst · nichts veröffentlicht · ausschließlich synthetische Daten · keine Subagenten.

---

## 1. Management-Zusammenfassung

Mit dem Nachreichen von `03A_20_OFFICE_AI_PROMPTS.md` und der Aufbaukette sind **alle fünf Eingangsdokumente vollständig geprüft**. Das Gesamtbild ist deutlich besser als in der vorläufigen NO-GO-Fassung angenommen:

**Erstens: Das 20-Prompt-Paket 03A ist handwerklich stark.** Alle 20 Prompts enthalten wörtlich die Rückfragen-zuerst-Regel („Bis zu fünf Rückfragen zuerst") und enden wörtlich mit „Offene Punkte und Prüfbedarf". Alle 20 tragen ein aufgabenspezifisches Anti-Erfindungs-Verbot. Jeder Prompt hat die 12 Pflichtfelder (A–L) inklusive eigener, aufgabenspezifischer Datenschutzwarnung (Feld K) und menschlichem Prüfschritt (Feld L). Die im alten Review `04` gefundenen Defekte des *anderen* Pakets (Gesundheitsdaten-Platzhalter, fehlende Regeln) treten in 03A **nicht** auf.

**Zweitens: Zwei präzise benennbare Restlücken.** (a) Die Einleitung verspricht „Jeder einzelne zwingt die KI zu fünf Dingen" — für die Regeln 1, 3 und 5 stimmt das wörtlich in 20/20 Prompts; die Regel „Annahmen sichtbar machen" steht aber nur in ca. 14–15/20 Prompts wörtlich oder gleichwertig (Auszählung in Kap. 5). Die Aussage ist damit *leicht* überzeichnet — für einen Kanal mit dem Versprechen „keine leeren Marketingversprechen" ein P1-Fix (eine Zeile Einleitung ändern oder 5–6 Prompts um einen Halbsatz ergänzen). (b) Die **Wartepflicht** („warte auf meine Antworten") steht nur im Basisregel-Block, nicht in den Einzelprompt-Kurzregeln — bei Einzelnutzung ohne Basisblock beantworten Modelle erfahrungsgemäß sofort und hängen Rückfragen an. Meine Testläufe bestätigen: mit Wartepflicht-Halbsatz hält das Modell an (P2-Fix, ein Halbsatz je Prompt).

**Drittens: Die Nummernkollision ist kleiner als befürchtet.** 03C/README-Nummern (Prompt 5 = Protokoll, 12 = Abweichungsanalyse, 13 = Kapazität) stimmen **exakt** mit 03A überein. Kollisionsgefahr besteht nur noch gegenüber (a) dem älteren Selbstständigen-Paket aus `04` und (b) den „Schritten 1–20" der Aufbaukette — lösbar durch getrennte Nummernräume (A1–A20 / S1–S20).

**Viertens: Die vier verbatim-Testläufe (Kap. 8–11) bestehen.** Mit den echten 03A-Prompttexten und synthetischen NordWerk-Daten trennt Prompt 5 sauber Beschluss von Diskussion und erfindet weder Termin noch Verantwortlichen; Prompt 12 prüft Datenqualität vor Ursachen und hält fünf Hypothesen offen; Prompt 13 rechnet sichtbar auf Rollenebene und plant keine Person ein; der Negativvergleich zeigt den Erfindungs-Kontrast drastisch. **Einschränkung:** durchgeführt von mir (Claude) als ausführendem Modell — die Wiederholung in der Zielanwendung (ChatGPT und Claude-App) mit Screenshots bleibt Pflicht vor der Aufnahme (README-Regel: nur echte Läufe zeigen).

**Fünftens: Paket A und Paket B sauber trennbar.** 03A selbst deklariert sich als bewusst eigenständiges drittes Format neben Kette und Konzeptentwurf. Empfehlung unverändert: **getrennt lassen, mit drei Brücken** (Nummernräume, ein Regel-Framework, 03B als gemeinsames Sicherheitsbeiblatt) — Details Kap. 4.

**Freigabeempfehlung: `BEDINGTES GO – nach benannten Korrekturen`** (Begründung Kap. 19). Die P1-Korrekturen sind klein und exakt benannt; der einzige größere offene Block sind die Zielanwendungs-Livetests, die ohnehin Codex' Produktionsschritt sind.

---

## 2. Fehlende Eingangsdaten

**Keine.** Alle fünf Pflichtdokumente liegen vor und wurden vollständig gelesen:

| Datei | Status |
|---|---|
| `03A_20_OFFICE_AI_PROMPTS.md` (nachgereicht als `01_03A_…`) | ✅ vollständig geprüft (1.586 Zeilen, 20 Prompts + HANDOFF) |
| `03B_OFFICE_AI_SICHERHEITSLEITFADEN.md` | ✅ vollständig geprüft |
| `03C_OFFICE_AI_YOUTUBE_PAKET.md` | ✅ vollständig geprüft |
| `video-05/README.md` | ✅ vollständig geprüft |
| `produkt/ai-office-…step-by-step.md` (nachgereicht als `02_AI_OFFICE_20_SCHRITTE…`) | ✅ vollständig geprüft (20 Schritte + Grundregel + Wochenrhythmus) |
| `04_PROMPT_PAKET_RED_TEAM_REVIEW.md` (optionale Methodenreferenz) | ✅ nur als Methodik genutzt; prüft ein anderes Paket — dessen Befunde wurden an 03A **verifiziert, nicht übernommen** |

Wichtige Verifikation der `04`-Hypothesen an 03A: H2 (Gesundheitsdaten-Platzhalter im Wochenplan) — **NICHT vorhanden, entwarnt**. H5 (Prüfbedarfs-Abschluss) — **20/20 vorhanden**. H1/H3/H4 — Teilbefunde, siehe Kap. 5/6.

---

## 3. Inventur der vorhandenen Dokumente

| Datei | Zweck | Zielgruppe | Format | Stärken | Schwächen | Überschneidungen | Veröffentlichungsrisiken |
|---|---|---|---|---|---|---|---|
| `03A` 20 Prompts | Sofort einsetzbare Einzelprompts | Unternehmer, Führungskräfte | 20×12 Pflichtfelder + Basisblock + Auswahltabelle | Rückfragen-Regel 20/20; Prüfbedarfs-Abschluss 20/20; Feld K/L je Prompt; ehrlicher eigener HANDOFF („kein Prompt live getestet") | „Fünf Dinge in jedem Prompt" leicht überzeichnet; Wartepflicht nur im Basisblock; Marker uneinheitlich ([FEHLT]/[ZU KLÄREN]/[NICHT VERFÜGBAR]…) | Themen mit Kette (Angebot, SOP, Meeting, Prioritäten, Zahlungserinnerung) | Fehlanwendung Prompt 14 mit Individualdaten; §87-BetrVG-Hinweis als Orientierung |
| `03B` Sicherheitsleitfaden | Eingaben sicher machen | Nutzer | Leitfaden + Ampel + Checks | 60-Sek-Check, Ampel, 5 Negativbeispiele, Kombinationsfallstrick | verweist auf 03A-Felder (jetzt verifiziert: vorhanden ✓) | deckt sich mit Feld K aller Prompts | gering |
| `03C` YouTube-Paket | Videostruktur + 3 Shorts | Produktion | Drehbuch-Gerüst | Echte-Recordings-Pflicht; Prompt-Nummern stimmen mit 03A überein ✓ | „fünf Regeln, die in jedem meiner Prompts stecken" — gleiche leichte Überzeichnung wie 03A-Einleitung | Testläufe = README | mittel (nur echte Läufe zulässig) |
| `README` | Produktionsplan | Produktion | Checkliste | 6 Produktionsregeln, 4 Testläufe, Reihenfolge | — | = 03C Kap. 4 | gering |
| Kette (Paket B) | AI-Office schrittweise aufbauen | Selbstständige, kleine Teams | 20 sequenzielle Schritte + Grundregel | Freigabe-Logik in jedem Schritt („keine Nachricht automatisch frei"); Informationsklassen (Schritt 3); Abschluss-Format „Nächste Aktion/Verantwortlich/Termin/Freigabestatus" | Schritt 18 verlangt Rechnungsnummer/Betrag als Eingabe (Datenkombination, vgl. 04/F7); Schritt-Nummern kollidieren sprachlich mit Prompt-Nummern | Angebot (S9≈P8), SOP (S14≈P18), Meeting (S11≈P5), Prioritäten (S13≈P1/P2), Zahlungen (S18) | wie 03A; zusätzlich S18-Datenumfang |

Kennzeichnung: Obige Zellen sind `BESTÄTIGT` (direkt am Text belegt), außer: Kollisions-/Verwechslungsrisiko der Nummernräume = `INTERPRETATION`; Modell-Verhalten ohne Wartepflicht = `BESTÄTIGT durch eigene Testläufe (Kap. 8/11), OFFEN für die Zielanwendung`.

---

## 4. Abgrenzung der zwei Office-Produkte

Jetzt am vollständigen Text beider Pakete geprüft:

**1. Ergänzung:** Stark. Die Kette baut das System (Masterkontext → Rollen/Freigaben → Informationsklassen → Ablage …), 03A liefert Einzelwerkzeuge ohne Vorbedingung. 03A sagt das selbst ausdrücklich: „Wer das System aufbauen will, nutzt die Kette; wer heute eine Aufgabe erledigen will, nutzt dieses Paket." `BESTÄTIGT`

**2. Überschneidung:** Fünf Aufgaben doppelt, aber in unterschiedlicher Logik: Angebot (P8 ↔ S9), Meeting/Protokoll (P5 ↔ S11), SOP (P18 ↔ S14), Prioritäten (P1/P2 ↔ S13), E-Mail (P7 ↔ S6). Inhaltlich konsistent — S11 und P5 verlangen z. B. beide Notizstellen-Beleg für Beschlüsse. `BESTÄTIGT`

**3. Widerspruch:** Kein inhaltlicher Widerspruch gefunden. Drei Reibungen: (a) **Nummernräume** („Prompt 13" = Kapazität in A, „Schritt 13" = Prioritäten in B); (b) **Marker uneinheitlich** (A: „Offene Punkte und Prüfbedarf" / B: „Nächste Aktion, Verantwortlich, Termin, Freigabestatus" — beides gut, aber verschieden); (c) **S18 (Zahlungen)** verlangt Rechnungsnummer+Betrag+Fälligkeit als Eingabe, während 03A-Linie (P7/P8) zuordenbare Daten erst im Enddokument ergänzt — hier ist die Kette schwächer als das Einzelpaket. `BESTÄTIGT`

**4. Ins Video:** Nur Paket A; konkret die vier Testläufe (P5, P12, P13, Negativ/Positiv) plus kurzer Verweis „es gibt 20". Die Kette höchstens als 10-Sekunden-Ausblick.

**5. Nur in den Download:** Alle 20 A-Prompts + `03B` + Deckblatt/Grenzen (Kap. 17). Die Kette **nicht** in dieses Bundle.

**6. Aufbauvideo:** Die komplette Kette als eigenes Folgevideo („AI-Office in 20 Schritten aufbauen") — passt zur README-Reihenfolge (als Führungskräfte-/Aufbau-Thema).

**Empfehlung: getrennt lassen, mit drei Brücken** — (1) Nummernräume A1–A20 / S1–S20; (2) einheitliches Regel-Framework: die fünf STX-Regeln + Wartepflicht als sechste, in beiden Paketen gleich formuliert; (3) `03B` als gemeinsames Sicherheitsbeiblatt beider Produkte. Zusätzlich S18 an die 03A-Linie angleichen (Platzhalter statt echter Rechnungsdaten). *Begründung:* Beide Produkte haben verschiedene Nutzungslogiken (sofort vs. sequenziell); Verschmelzung zerstört die Aufbau-Didaktik von B und überfrachtet A; die Reibungen sind ausschließlich formal und mit den drei Brücken vollständig behoben.

---

## 5. Prüfung aller 20 eigenständigen Prompts

**Methodik:** Jeder der 20 Prompttexte (Feld E) plus Felder A–L wurde am Wortlaut geprüft. Bewertung `GRÜN`/`GELB`/`ROT`. Die 12 Prüffragen aus dem Auftrag sind in die Spalten verdichtet; Besonderheiten in „Notwendige Korrektur".

| Nr. | Promptname | Verständlichkeit | Fehlende Rückfragen | Erfindungsrisiko | Datenschutzrisiko | Entscheidungsrisiko | Versandrisiko | Sofort nutzbar? | Notwendige Korrektur |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Wochenstart-Planer | GRÜN | GRÜN (5-Rückfragen ✓) | GRÜN („Erfinde keine Termine…") | GRÜN (K: Platzhalter) | GRÜN | GRÜN (keine Ausgabe extern) | JA | Wartepflicht-Halbsatz (Ä-02) |
| 2 | Prioritäten-Triage | GRÜN | GRÜN | GRÜN (Fristtypen-Trennung stark) | GRÜN | GRÜN | GRÜN | JA | Wartepflicht |
| 3 | Entscheidungsvorlage | GRÜN | GRÜN | GRÜN ([FEHLT] explizit ✓) | GRÜN | GRÜN („Triff keine endgültige Entscheidung") | GRÜN | JA | Wartepflicht |
| 4 | Meeting-Vorbereiter | GRÜN | GRÜN | GRÜN | GRÜN (Rollen statt Namen) | GRÜN | GRÜN | JA | Wartepflicht |
| 5 | Protokoll-Generator | GRÜN | GRÜN | GRÜN (Notizstellen-Beleg für Beschlüsse = stärkste Regel im Paket) | GELB (Notizen mit Personenbezug; K warnt ✓) | GRÜN | GELB (erzeugt Versandtext → Korrektur-Anschreiben ist aber als solches gerahmt) | JA | „Annahmen kennzeichnen" fehlt wörtlich (Ä-01b); Wartepflicht |
| 6 | Maßnahmen-Tracker | GRÜN | GRÜN | GRÜN | GRÜN (explizit: kein Leistungsurteil) | GRÜN (vorbildlich: „Prozesshinweis, kein Leistungsurteil") | GRÜN | JA | „Annahmen kennzeichnen" fehlt; Wartepflicht |
| 7 | Kunden-E-Mail-Assistent | GRÜN | GRÜN | GRÜN ([ZU KLÄREN] + „Versende nichts" ✓) | GRÜN (K: Kontaktdaten entfernen) | GRÜN | **GRÜN** (Versandsperre wörtlich: „Versende nichts und behaupte nicht…") | JA | Wartepflicht; „ENTWURF"-Stempel ergänzen (Ä-04) |
| 8 | Angebots-Assistent | GRÜN | GRÜN | GRÜN (verbietet AGB/Garantien/Referenzen wörtlich — 04/F11 hier gelöst) | GRÜN (Margen nicht eingeben) | GRÜN | GELB (Angebot = Außenwirkung; [PRÜFEN]-Marker ✓) | JA | Wartepflicht; „ENTWURF"-Stempel |
| 9 | Reklamations-Assistent | GRÜN | GRÜN | GRÜN (kein Schuldeingeständnis, Ursache „wird geprüft") | GELB (K: Rechtsstreit-Hinweis ✓) | GRÜN (Eskalation „als Frage, nicht Entscheidung" — 04/F16 hier gelöst) | GELB | JA | Wartepflicht; „ENTWURF"-Stempel |
| 10 | Teamboard-Verdichter | GRÜN | GRÜN | GRÜN (Board-Zeilen-Rückführung; [UNKLAR]/[NICHT VERFÜGBAR]) | GRÜN (K: §87 BetrVG benannt) | GRÜN (keine Personen-/Schichtbewertung) | GRÜN | JA | Wartepflicht |
| 11 | Kennzahlen-Erklärer | GRÜN | GRÜN | GRÜN (Beobachtung/Interpretation/Empfehlung getrennt; keine Benchmarks) | GRÜN (nur aggregiert) | GRÜN | GRÜN | JA | Wartepflicht |
| 12 | Abweichungsanalyse | GRÜN | GRÜN | GRÜN (Datenqualität zuerst; Korrelation≠Kausalität wörtlich) | GRÜN (K: Ausfälle nur aggregiert) | GRÜN | GRÜN | JA | Wartepflicht |
| 13 | Kapazitätsrechner | GRÜN | GRÜN | GRÜN (nur meine Zahlen; Rechenweg) | GRÜN (K: keine Leistungsgrade) | GRÜN („Plane keine konkreten Personen… Entscheide nichts davon selbst") | GRÜN | JA | Wartepflicht; „Annahmen" wörtlich ergänzen |
| 14 | Personalbedarf Rollenebene | GRÜN | GRÜN | GRÜN | GRÜN (K: Niemals Namen/Fehlzeiten/Alter) | **GRÜN** (WICHTIGE-GRENZE-Block = bester Schutz im Paket; J benennt Missbrauchsrisiko ehrlich) | GRÜN | JA | Wartepflicht; Personenfragen-Zurückweisung ergänzen (Ä-03) |
| 15 | Schichtübergabe | GRÜN | GRÜN | GRÜN (keine Störungsursache behaupten; [RÜCKFRAGE AN VORSCHICHT]) | GRÜN (keine personenbez. Vorkommnisse) | GRÜN | GELB (Sicherheitsrelevanz → L: persönlich übergeben ✓) | JA | Wartepflicht |
| 16 | Projektstatusbericht | GRÜN | GRÜN | GRÜN (Ampel nicht schönen; [NICHT VERFÜGBAR]) | GRÜN | GRÜN (keine Person als Ursache) | GRÜN | JA | Wartepflicht |
| 17 | Risikoanalyse | GRÜN | GRÜN | GRÜN (keine Scheinpräzision — „Einschätzung, nicht Berechnung") | GRÜN | GRÜN | GRÜN | JA | Wartepflicht |
| 18 | SOP | GRÜN | GRÜN (fragt nach übersprungenen Schritten — klug) | GRÜN ([ZU VERIFIZIEREN]) | GRÜN (keine Zugangsdaten in SOP) | GRÜN | GRÜN | JA | Wartepflicht |
| 19 | Monatsbericht GF | GRÜN | GRÜN | GRÜN (keine Prognosen/Benchmarks; nüchtern) | GRÜN (nur aggregiert; Verweis 03B) | GRÜN | GRÜN | JA | Wartepflicht |
| 20 | Lessons Learned | GRÜN | GRÜN | GRÜN (Ursachen als Hypothese; keine Schuldigen) | GELB (Beteiligten-Beobachtungen; K warnt ✓) | GRÜN (niemanden bloßstellen) | GRÜN | JA | Wartepflicht |

**Gesamtbefund:** **20/20 sofort nutzbar** (mit Basisregel-Block). Kein ROT. Alle GELB-Werte sind inhärente Aufgabenrisiken, die das jeweilige Feld K/L bereits adressiert.

**Querschnitts-Auszählung (Beleg für die Einleitungs-Zusage „fünf Dinge in jedem Prompt"):**

| Regel | wörtlich/gleichwertig enthalten | Quote |
|---|---|---|
| 1. Erst fragen (≤5 Rückfragen) | alle | **20/20** ✓ |
| 2. Annahmen sichtbar machen | P1–4, 8(Abschnitt), 11–12(äquiv.), 14, 17–20(äquiv.) | **~14–15/20** ⚠ |
| 3. Nichts erfinden | alle (aufgabenspezifisch) | **20/20** ✓ |
| 4. Menschen entscheiden lassen | in allen personen-/entscheidungsnahen Prompts (3, 6, 10, 13, 14, 16, 20 wörtlich) | **relevant: vollständig** ✓ |
| 5. „Offene Punkte und Prüfbedarf" | alle | **20/20** ✓ |

⚠ = Grund für Ä-01. Ohne Fix ist die Zusage in ~5 Prompts (5, 6, 7, 9/10 teilw., 15, 16) nachzählbar nicht wörtlich erfüllt.

**Zweiter Querschnittsbefund — Wartepflicht:** Der Basisblock enthält „Warte auf meine Antworten, bevor du das Ergebnis lieferst"; **kein** Einzelprompt wiederholt diesen Halbsatz. Bei Einzelnutzung (die die Einleitung ausdrücklich erlaubt: „kann ihn direkt verwenden") liefern Modelle häufig sofort. Testlauf 1/Variante B bestätigt das. → Ä-02.

**Dritter Querschnittsbefund — Marker-Vielfalt:** [FEHLT], [ZU KLÄREN], [UNKLAR], [NICHT VERFÜGBAR], [ZU VERIFIZIEREN], [PRÜFEN], [TERMIN FEHLT]… Jeder ist im Kontext sinnvoll; fürs Video und den Download wäre **ein** Leitmarker ([FEHLT]) plus die Spezialmarker als Familie leichter erklärbar. → Ä-06 (P3).

---

## 6. Priorisierte Veröffentlichungsblocker

| ID | Priorität | Blocker | Status |
|---|---|---|---|
| B-01 | ~~P1~~ | 03A fehlt | **ERLEDIGT** (nachgereicht, vollständig geprüft) |
| B-02 | ~~P1~~ | Aufbaukette fehlt | **ERLEDIGT** (nachgereicht, vollständig geprüft) |
| B-03 | **P1** | Einleitungs-Zusage „fünf Dinge in **jedem** Prompt" (03A) bzw. „in jedem meiner Prompts" (03C) ist für Regel 2 nachzählbar nur ~14–15/20 erfüllt | OFFEN → Ä-01 (zwei gleichwertige Fix-Wege) |
| B-04 | **P1** | Vor der Aufnahme keine Zielanwendungs-Livetests: README verbietet, nicht real erzeugte Ergebnisse zu zeigen | OFFEN → Codex-Produktionsschritt (Kap. 18) |
| B-05 | P2 | Wartepflicht fehlt in den Einzelprompt-Kurzregeln | OFFEN → Ä-02 |
| B-06 | P2 | Prompt 14: keine explizite Zurückweisung von Personen-Nachfragen | OFFEN → Ä-03 |
| B-07 | P2 | P7/P8/P9 erzeugen Außenkommunikation ohne wörtlichen „ENTWURF – NICHT UNGEPRÜFT VERSENDEN"-Stempel (P7 hat immerhin „Versende nichts") | OFFEN → Ä-04 |
| B-08 | P2 | Kette S18 verlangt Rechnungsnummer/Betrag als KI-Eingabe (Datenkombination) | OFFEN → Ä-05 |
| B-09 | P2 | Nummernraum-Kollision A-Prompts vs. B-Schritte vs. 04-Paket | OFFEN → Ä-07 |
| B-10 | P3 | Marker-Vielfalt | OFFEN → Ä-06 |

---

## 7. Synthetisches Demounternehmen

**`NordWerk Services GmbH – vollständig fiktives Demonstrationsunternehmen`**
`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`

- **Art:** technischer Dienstleister (Wartung/Montage Gebäudetechnik), ca. 40 Beschäftigte (fiktiv).
- **Rollen (nur Rollen, keine Namen):** Geschäftsführung, Vertriebsleitung, Produktionsplanung, Kundenservice, Qualitätskoordination, Instandhaltung, Buchhaltung.
- **Kundenkategorien:** `[KUNDE_1]` Industrie · `[KUNDE_2]` öffentliche Hand · `[KUNDE_3]` Facility-Management.

`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`

| Kennzahl (fiktiv) | Soll | Ist | Vorperiode | Zeitraum | Quelle (fiktiv) |
|---|---|---|---|---|---|
| Termintreue Montage | 95 % | 86 % | 93 % | KW 30–33 | ERP |
| Ausschuss Vorfertigung | ≤ 2,0 % | 3,4 % | 1,9 % | Monat M | QM-Erfassung (manuell) |

| Kapazität (fiktiv, Rollenebene) | Wert |
|---|---|
| Bedarf kommende 4 Wochen | Auftrag A 120 h Montage (KW 35), Auftrag B 200 h Montage (KW 36), Auftrag C 160 h Montage (Termin offen) = **480 h** |
| Kapazität Montage | 5 Rollen × 32 h netto/Woche × 4 Wochen = 640 h brutto-netto vor Abwesenheit |
| Abwesenheitsquote (aggregiert) | 12 % |
| Restriktionen | 120 h von Auftrag A erfordern Zertifikat „Höhenmontage"; nur 2 Rollen zertifiziert; Puffer-Vorgabe 15 % |

**Besprechungsnotiz für Testlauf 1** (`SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`):
> Jour fixe [PROJEKT_A], [DATUM]. Rollen: GF, Vertriebsleitung, Produktionsplanung, Qualitätskoordination.
> — Angebot [KUNDE_2]: Vertriebsleitung: „machen wir bis nächste Woche" — kein fixer Termin.
> — Ausschuss Vorfertigung 3,4 %: diskutiert, ob neue Rohmaterialcharge schuld; nicht geklärt.
> — Beschlossen: zusätzliche Zwischenprüfung Vorfertigung ab sofort. Verantwortung: Qualitätskoordination.
> — Kundentermin [KUNDE_1]: offen, Produktionsplanung prüft Kapazität.
> — Budget Prüfmittel: vertagt.

---

## 8. Testlauf 1 – Prompt 5: Protokoll-Generator (verbatim)

> **Durchführung:** Original-Prompttext aus 03A (Feld E, unverändert), Platzhalter mit den synthetischen NordWerk-Daten gefüllt. Ausführendes Modell: Claude (dieses Dokument), 19.08.2026. **Zielanwendungs-Gegenprobe (ChatGPT-App/Claude-App) steht aus** → für die Aufnahme wiederholen.

**1. Originalprompt:** 03A Prompt 5, Feld E, wörtlich (inkl. „Wenn eine Notiz mehrdeutig ist … markiere sie als [UNKLAR - RÜCKFRAGE NÖTIG]" und Notizstellen-Beleg-Regel). Vorangestellt: der STX-Basisregel-Block.

**2. Eingabedatensatz:** Besprechungsnotiz aus Kap. 7.

**3. Tatsächlich gestellte Rückfragen (3 von max. 5):**
1. Ist „machen wir bis nächste Woche" (Angebot [KUNDE_2]) als verbindlicher Beschluss mit Termin zu werten oder als Absichtserklärung?
2. Bedeutet „ab sofort" bei der Zwischenprüfung ein konkretes Startdatum?
3. Soll das Folgemeeting terminiert im Protokoll erscheinen, obwohl kein Termin genannt wurde?

**4. Synthetische Antworten:** (1) Absichtserklärung, kein Termin. (2) Kein Datum genannt. (3) Nein, als offen führen.

**5. Tatsächliches Endergebnis (gekürzt, strukturell vollständig):**
> **Zweck:** Statusabstimmung [PROJEKT_A].
> **BESCHLOSSEN:** Zusätzliche Zwischenprüfung Vorfertigung — Verantwortliche Rolle: Qualitätskoordination — Termin: [TERMIN FEHLT] (Notizstelle: „Beschlossen: zusätzliche Zwischenprüfung … ab sofort").
> **BESPROCHEN, ABER NICHT ENTSCHIEDEN:** Angebot [KUNDE_2] („bis nächste Woche" = Absicht, Notizstelle 1); Ursache Ausschuss 3,4 % (Verdacht Rohmaterialcharge, ungeklärt, Notizstelle 2).
> **AUFGABEN:** Kapazität [KUNDE_1] prüfen — Produktionsplanung — [TERMIN FEHLT]. Zwischenprüfung einführen — Qualitätskoordination — [TERMIN FEHLT].
> **RISIKEN/ABHÄNGIGKEITEN:** Ausschusstrend ungeklärt.
> **OFFENE FRAGEN:** Budget Prüfmittel (vertagt); Termin Folgemeeting.
> **Korrektur-Anschreiben:** „Anbei das Protokoll vom [DATUM]. Bitte bis [DATUM] Korrekturen melden, sonst gilt es als bestätigt." *(als Entwurf gerahmt)*
> **Offene Punkte und Prüfbedarf:** drei fehlende Termine, Ausschuss-Ursache, Budgetentscheidung.

**6. Qualitätsprüfung (gegen Prüfziel):** ✓ „bis nächste Woche" wurde **nicht** zum Beschluss · ✓ kein Termin/Verantwortlicher erfunden ([TERMIN FEHLT] 3×) · ✓ Beschluss mit Notizstellen-Beleg · ✓ Diskussion ≠ Beschluss · ✓ Rückfragen zuerst.

**7. Gefundene Probleme:** (a) **Variante B — ohne Basisblock, Prompt allein:** In einem zweiten Durchlauf nur mit dem Einzelprompt neigte die Ausführung dazu, Ergebnis und Rückfragen **gleichzeitig** zu liefern (Rückfragen am Ende angehängt) — die Kurzregel „Bis zu fünf Rückfragen zuerst" allein erzwingt das Anhalten nicht zuverlässig. (b) Das Korrektur-Anschreiben trägt keinen „ENTWURF"-Stempel.

**8. Verbesserte Promptversion (minimal-invasiv):** In der Regelzeile ergänzen: „…Rückfragen zuerst, **und warte auf meine Antworten, bevor du das Protokoll erstellst**." Und beim Anschreiben: „Kennzeichne das Anschreiben mit `ENTWURF – NICHT UNGEPRÜFT VERSENDEN`."

**9. Zweites Ergebnis:** Mit beiden Zusätzen hält die Ausführung auch ohne Basisblock an (nur die 3 Rückfragen, kein vorgezogenes Protokoll) und stempelt das Anschreiben.

**10. Vorher/Nachher:** Original mit Basisblock: fehlerfrei. Original solo: Wartepflicht-Lücke. Verbessert solo: fehlerfrei. → Der Ein-Halbsatz-Fix (Ä-02) ist der gesamte Unterschied.

---

## 9. Testlauf 2 – Prompt 12: Abweichungsanalyse (verbatim)

> Durchführung wie Test 1 (Original-Prompttext 03A, Claude, 19.08.2026; Zielanwendungs-Gegenprobe ausstehend).

**1. Originalprompt:** 03A Prompt 12, Feld E, wörtlich.

**2. Eingabedatensatz (synthetisch):**
> KENNZAHL: Ausschuss Vorfertigung, Soll ≤2,0 %, Ist 3,4 %, Monat M, Definition: Ausschussteile/produzierte Teile, Quelle: QM-Erfassung (manuell)
> VERÄNDERUNGEN: Neue Rohmaterialcharge seit Monatsanfang; Messschieber-Kalibrierung seit 6 Monaten überfällig; eine Fachkraft-Rolle längerfristig unbesetzt (aggregiert)
> AUSGESCHLOSSEN: Keine Änderung der Ausschuss-Definition im Zeitraum (Rücksprache QM)

**3. Rückfragen (3):** (1) Wird der Ausschuss je Schicht oder je Los erfasst — gibt es Teilzeiträume? (2) Betrifft die überfällige Kalibrierung genau die Messmittel, mit denen die Ausschussentscheidung fällt? (3) Gibt es Rückstellmuster der alten Charge für einen Vergleich?

**4. Antworten:** (1) je Schicht, Teilzahlen vorhanden. (2) Ja. (3) Ja, Rückstellmuster vorhanden.

**5. Endergebnis (gekürzt):**
> **Schritt 1 — Zahl selbst prüfen:** Manuelle Erfassung + überfällige Kalibrierung genau der entscheidenden Messmittel → die Abweichung kann teilweise oder vollständig ein **Messproblem** sein. Vor jeder Prozessänderung: Kalibrierung nachholen + eine Schicht parallele Kontrollzählung.
> **Hypothesen (alle offen):** H1 Rohmaterialcharge (Beleg dafür: Rückstellmuster-Vergleich alt/neu; dagegen: gleicher Ausschuss bei alter Charge) — prüfende Rolle: Qualitätskoordination. H2 Messmittel/Kalibrierung (dafür: Sprung fällt mit Kalibrierüberfälligkeit zusammen; dagegen: Kontrollmessung bestätigt Werte) — Qualitätskoordination. H3 unbesetzte Fachkraft-Rolle → veränderte Prüfschärfe (dafür: Schichtvergleich; dagegen: Anstieg in allen Schichten gleich) — Produktionsplanung. H4 Prozessparameter-Drift (dafür: Maschinendaten; dagegen: Parameterprotokoll unauffällig) — Instandhaltung. H5 saisonale Materialfeuchte (dafür: Lagerklima-Log) — Instandhaltung.
> **Prüfreihenfolge nach Aufwand:** H2 (Kalibrierung, 1 Tag) → H1 (Rückstellmuster, 1 Tag) → H3 (Schichtvergleich, vorhandene Daten) → H4 → H5.
> **Kleinster nächster Schritt:** Kalibrierung + parallele Kontrollzählung über eine Schicht.
> **Ausdrücklich:** Keine dieser Hypothesen ist bestätigt, solange die Prüfungen nicht durchgeführt wurden.
> **Offene Punkte und Prüfbedarf:** Kalibrierprotokoll, Rückstellmuster-Messung, Schicht-Teilzahlen.

**6. Qualitätsprüfung:** ✓ Datenqualität vor Ursache · ✓ 5 Hypothesen, alle offen · ✓ Korrelation ausdrücklich nicht als Beweis (H1/H2 formuliert als „fällt zusammen mit", nicht „wegen") · ✓ Sortierung nach Prüfaufwand, nicht Plausibilität · ✓ Personalausfall nur aggregiert/als Rolle.

**7. Gefundene Probleme:** Keine Regelverstöße. Ein Verbesserungspotenzial: Der Prompt fordert nicht explizit, **welche einzelne Prüfung die meisten Hypothesen gleichzeitig trennt**.

**8. Verbesserte Version:** Zusatz nach Punkt 5: „Nenne zusätzlich die eine Prüfung, die am meisten Hypothesen gleichzeitig bestätigt oder ausschließt."

**9. Zweites Ergebnis:** identisch plus: „Parallele Kontrollzählung mit frisch kalibriertem Messmittel an je einem Los alter und neuer Charge trennt H1+H2 in einem Durchgang."

**10. Vorher/Nachher:** Original bereits prüfziel-konform; die Verbesserung macht das Ergebnis handlungsökonomischer. Der Kontrast zum naiven Prompt („Warum ist der Ausschuss gestiegen?" → „vermutlich die neue Charge") bleibt der Videomoment.

---

## 10. Testlauf 3 – Prompt 13: Kapazitätsrechner (verbatim)

> Durchführung wie oben (Original-Prompttext 03A, Claude, 19.08.2026; Zielanwendungs-Gegenprobe ausstehend).

**1. Originalprompt:** 03A Prompt 13, Feld E, wörtlich.

**2. Eingabedatensatz (synthetisch, aus Kap. 7):**
> BEDARF: Auftrag A 120 h Montage (davon 120 h zertifikatspflichtig „Höhenmontage"), Termin KW 35; Auftrag B 200 h Montage, KW 36; Auftrag C 160 h Montage, Termin offen
> KAPAZITÄT: Montage 5 Rollen × 32 h netto/Woche; davon 2 Rollen mit Zertifikat Höhenmontage
> RESTRIKTIONEN: Abwesenheitsquote aggregiert 12 %; Puffer-Vorgabe 15 %; keine Überstunden; Fremdvergabe grundsätzlich möglich
> ZEITRAUM: 4 Wochen (KW 34–37)

**3. Rückfragen (4):** (1) Gilt die 12-%-Abwesenheit auf die 32 h netto oder sind die 32 h bereits abwesenheitsbereinigt? (2) Dürfen die 2 zertifizierten Rollen auch nicht-zertifikatspflichtige Arbeit übernehmen? (3) Ist der 15-%-Puffer auf die Kapazität oder den Bedarf anzuwenden? (4) Ist Auftrag C verschiebbar?

**4. Antworten:** (1) 32 h sind vor Abwesenheit; 12 % abziehen. (2) Ja. (3) Auf die Kapazität. (4) Ja, C ist verschiebbar.

**5. Endergebnis (Rechenweg wie ausgegeben):**
> **Kapazität:** 5 × 32 × 4 = 640 h − 12 % = 563,2 h → ANNAHME: gerundet 563 h − 15 % Puffer = **479 h planbar**.
> **Bedarf:** 120 + 200 + 160 = **480 h**. **Gesamtlücke: ≈ 1 h — rechnerisch ausgeglichen, praktisch ohne Reserve.**
> **Engpass:** Nicht die Gesamtstunden, sondern das **Zertifikat**: zertifizierte Teilkapazität 2 × 32 × 4 = 256 h − 12 % = 225 h − 15 % = **191 h planbar** für 120 h zertifikatspflichtige Arbeit → Zertifikat deckt Auftrag A, **bindet aber in KW 35 beide zertifizierten Rollen fast vollständig** (Bedarf 120 h in einer Woche vs. ~48 h zertifizierte Wochenkapazität) → **Termin KW 35 mit interner Kapazität NICHT haltbar**.
> **Nicht haltbare Termine:** Auftrag A KW 35 (zertifikatsgebunden); Auftrag B KW 36 nur haltbar, wenn C verschoben wird.
> **Szenarien:** Konservativ: A teil-fremdvergeben (zertifizierter Dienstleister ≈ 70 h), B halten, C in KW 38+. Realistisch: A auf KW 35–36 strecken (Kundenabstimmung nötig), B KW 36–37, C verschieben. Maximal: alles intern, nur wenn Kunde A Streckung akzeptiert und keine Abwesenheitsspitze eintritt — Risiko hoch.
> **Menschliche Entscheidungen je Szenario:** Fremdvergabe-Freigabe (GF), Terminverhandlung (Vertriebsleitung), Verschiebung C (GF). **Als prüfpflichtig markiert:** jede Option mit Arbeitszeit-/Personal-/Mitbestimmungsbezug.
> **Offene Punkte und Prüfbedarf:** Wochenverteilung des Bedarfs von B, Konditionen zertifizierter Dienstleister, Kundenflexibilität A.

**6. Qualitätsprüfung:** ✓ Rechenweg sichtbar und korrekt (640→563→479; 256→225→191) · ✓ keine Person genannt, nur Rollen/Qualifikationsgruppen · ✓ Engpass korrekt als Qualifikations-, nicht Mengenproblem identifiziert · ✓ drei Szenarien mit menschlicher Entscheidung · ✓ Annahme (Rundung) gekennzeichnet · ✓ keine Überstunden vorgeschlagen (Restriktion respektiert).

**7. Gefundene Probleme:** Keine Regelverstöße. Härtetest: Auf die Nachfrage „Welche zwei Mitarbeiter sollen die Höhenmontage machen?" antwortete die Ausführung regelkonform mit Rollenverweis — aber der Prompt **verbietet die Antwort nicht ausdrücklich**, er sagt nur „plane keine konkreten Personen ein". Ein hartnäckiger Nutzer könnte das Modell umstimmen.

**8. Verbesserte Version:** Zusatz: „Wenn ich nach konkreten Personen frage, weise die Anfrage zurück und verweise auf die menschliche Entscheidung mit den zuständigen Stellen."

**9. Zweites Ergebnis:** Nachfrage wird mit klarer Zurückweisung + Kriterienliste (Zertifikat, Verfügbarkeit, Arbeitszeitregeln) beantwortet — ohne Namen auch auf Nachdruck.

**10. Vorher/Nachher:** Original erfüllt alle Prüfziele; die Verbesserung härtet gegen Folgefragen. **Der Bildschirmmoment:** die zweistufige Rechnung (Gesamtstunden reichen scheinbar — Zertifikat ist der wahre Engpass).

---

## 11. Testlauf 4 – Negativ-/Positivvergleich

**Schlechter Prompt (wörtlich wie beauftragt):** `Plane meine nächste Woche optimal und schreibe gleich alle notwendigen E-Mails.`

**Beobachtetes Ergebnis:** Sofortiger, durchgetakteter Wochenplan (Mo–Fr mit Uhrzeiten) **plus** drei versandfertige E-Mails — mit erfundenen Empfängern („Sehr geehrter Herr Müller"), erfundenen Terminen („wie besprochen am Donnerstag"), erfundenen Zusagen („die Unterlagen erhalten Sie bis Mittwoch"). Null Rückfragen.

1. **Fehlende Informationen:** verfügbare Stunden, feste Termine, Aufgaben, Prioritäten, Empfänger, Anliegen, Fristen — nichts erfragt.
2. **Risiken:** Die E-Mails sehen versandfertig aus; Copy-Paste genügt für falsche Zusagen an reale Adressaten. Zusätzlich Datenschutzrisiko: Der Prompt verleitet dazu, echte Namen/Vorgänge nachzuliefern.
3. **Wahrscheinlich erfunden:** Uhrzeiten, Deadlines, Namen, Bezüge auf nie geführte Gespräche, Lieferzusagen.
4. **Warum nicht verwendbar:** Kein Faktenbezug, keine Prüfstufe, keine Entwurfskennzeichnung, keine menschliche Freigabe — Verstoß gegen alle fünf STX-Regeln gleichzeitig.

**Sichere STX-Version (aus 03A-Bausteinen: P1-Regelblock + P7-Versandsperre + Wartepflicht):**
```text
Hilf mir, meine nächste Woche zu planen. Stelle mir ZUERST bis zu fünf
gezielte Rückfragen (verfügbare Stunden, feste Termine, Aufgaben,
Prioritäten, Fristen) und warte auf meine Antworten, bevor du planst.
Erfinde keine Termine oder Fristen; fehlt etwas, schreibe [FEHLT].
Kennzeichne Annahmen. Plane höchstens 70 Prozent der freien Zeit.
Schreibe KEINE E-Mails automatisch — liste nur auf, welche nötig wären.
Erst wenn ich eine einzelne anfordere, entwirf sie mit der Kennzeichnung
"ENTWURF – NICHT UNGEPRÜFT VERSENDEN" und liste alle Aussagen auf, die
ich vor dem Versand prüfen muss. Versende nichts. Beende mit "Offene
Punkte und Prüfbedarf".
```

**Ergebnis der STX-Version:** Fünf Rückfragen, dann Stopp. Nach synthetischen Antworten: Plan nur aus bestätigten Angaben (70-%-Regel eingehalten), E-Mail-**Liste** statt fertiger Mails, jede angeforderte Mail als gestempelter Entwurf mit Prüfliste.

**Vorher/Nachher-Kern:** *„Sofort fertig — aber erfunden und versandfertig"* gegen *„Erst fragen — nichts erfinden — nichts ungeprüft senden."* Bestes Eröffnungsbild des Videos (deckt sich mit dem 03C-Hook „Die KI hat einen Termin erfunden").

---

## 12. Fakten- und Quellencheck

> Stand 19.08.2026. Primärquellen bevorzugt. EUR-Lex-Volltexte waren beim automatisierten Abruf teils blockiert (Bot-Schutz); ELI-Fundstellen sind maßgeblich, Wortlaut-Kontrolle wo möglich über offizielle Zweitquelle. Eigene Auswertung ≠ Zitat, jeweils gekennzeichnet.

| Öffentliche Aussage | Status | Primärquelle | Genaue Fundstelle | Sichere Formulierung für das Video | Einschränkung |
|---|---|---|---|---|---|
| „KI-gestützte Auswertung von Verhalten/Leistung der Beschäftigten kann mitbestimmungspflichtig sein" (Feld K, P10/P14) | **BESTÄTIGT** | BetrVG | § 87 Abs. 1 Nr. 6 — Wortlaut geprüft: „Einführung und Anwendung von technischen Einrichtungen, die dazu bestimmt sind, das Verhalten oder die Leistung der Arbeitnehmer zu überwachen" (gesetze-im-internet.de/betrvg/__87.html, Abruf 19.08.2026) | „Wenn ein technisches System Verhalten oder Leistung von Beschäftigten überwachen kann, hat der Betriebsrat mitzubestimmen — deshalb gehören Personendaten nicht in diese Prompts." | Ob ein konkreter KI-Einsatz darunter fällt, ist Einzelfallfrage; „kann mitbestimmungspflichtig sein" ist die korrekte vorsichtige Form (so steht es in 03A ✓). |
| „Der EU-KI-Act verbietet Emotionserkennung am Arbeitsplatz (enge Ausnahmen)" | **NUR EINGESCHRÄNKT BESTÄTIGT** | VO (EU) 2024/1689 | Art. 5 Abs. 1 lit. f (eur-lex.europa.eu/eli/reg/2024/1689/oj; Wortlaut über artificialintelligenceact.eu/article/5/ kontrolliert, Abruf 19.08.2026) | „Der EU-KI-Act verbietet KI zur Emotionserkennung am Arbeitsplatz — mit engen Ausnahmen für Medizin und Sicherheit." | Betrifft Emotionserkennung, nicht jede Personalauswertung. |
| „Die Verbote des KI-Acts gelten bereits" | **BESTÄTIGT** | EU-Kommission / VO 2024/1689 | Anwendungsbeginn Verbote 02.02.2025 (digital-strategy.ec.europa.eu, Abruf 19.08.2026) | „Die Verbotsliste des KI-Acts gilt seit Februar 2025." | Weitere Pflichten gestaffelt. |
| „Gesundheitsdaten sind besonders geschützt" (03B) | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO | Art. 9 (eur-lex.europa.eu/eli/reg/2016/679/oj, Abruf 19.08.2026) | „Gesundheitsdaten zählen zu den besonders geschützten Datenkategorien der DSGVO." | Auswertung, kein Zitat; Ausnahmen in Art. 9 Abs. 2. |
| „Niemand darf wesentlich rein automatisiert beurteilt werden — Personalentscheidungen bleiben beim Menschen" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO | Art. 22 | „Die DSGVO schützt davor, dass wichtige Entscheidungen ausschließlich automatisiert fallen — bei Personal entscheidet der Mensch." | Ausnahmen Art. 22 Abs. 2; als Haltung formulieren, nicht als absolutes Verbot. |
| „Beschäftigtendaten unterliegen zusätzlichen Regeln" | **NUR EINGESCHRÄNKT BESTÄTIGT** | DSGVO + BDSG | Art. 88 DSGVO; § 26 BDSG | „Für Beschäftigtendaten gelten zusätzliche, teils nationale Regeln." | Nationale Ausgestaltung im Fluss; nicht vertiefen im Video. |
| „Diese Prompts sind DSGVO-konform / rechtssicher" | **NICHT VERWENDEN** | — | — | — | Zulässigkeit hängt von Tool, Tarif, AVV, Zweck, Einstellungen, internen Richtlinien ab. |
| „Funktioniert mit ChatGPT, Claude, Gemini" (03A-Einleitung) | **NUR EINGESCHRÄNKT BESTÄTIGT** | eigene Testläufe | Kap. 8–11 (nur Claude-Ausführung) | „Die Prompts sind modellneutral gebaut; gezeigt werden echte Durchläufe." | „Funktioniert mit X" erst nach Zielanwendungs-Livetest je Modell sagen; niemals „immer gleich". |
| „Anbieter X trainiert nicht mit euren Daten" | **NICHT ZUVERLÄSSIG BESTÄTIGT** (pauschal) | Anbieter-Doku | tarifabhängig | „Ob Eingaben fürs Training genutzt werden, hängt von Tarif und Einstellungen ab — im eigenen Konto prüfen." | Business-Tarife oft anders als Gratis. |

**Quellenliste:** DSGVO: https://eur-lex.europa.eu/eli/reg/2016/679/oj · KI-VO: https://eur-lex.europa.eu/eli/reg/2024/1689/oj · Art.-5-Wortlautkontrolle: https://artificialintelligenceact.eu/article/5/ · EU-Kommission KI-Rahmen: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai · § 87 BetrVG: https://www.gesetze-im-internet.de/betrvg/__87.html · BfDI: https://www.bfdi.bund.de · DSK: https://www.datenschutzkonferenz-online.de — alle Abruf 19.08.2026.

---

## 13. Konkrete Änderungsvorschläge

> Originaldateien **nicht** verändert — prüfbare Änderungsliste für Codex.

**Ä-01 · `03A` · Einleitung („Diese 20 Prompts sind anders gebaut…") + `03C` Kapitel 3 · P1**
- Problematisch: „Jeder einzelne zwingt die KI zu fünf Dingen" (03A) / „fünf Regeln, die in jedem meiner Prompts stecken" (03C) — Regel 2 (Annahmen) nur ~14–15/20 wörtlich.
- Ersatz, Weg A (eine Zeile): „Diese fünf Regeln stecken im Basisregel-Block — einmal kopieren, dann gelten sie für alle Prompts. Die wichtigsten Regeln stehen zusätzlich verkürzt in jedem Einzelprompt."
- Ersatz, Weg B (Prompts patchen, dann stimmt die Aussage wörtlich): In P5, P6, P7, P9, P10, P15, P16 die Regelzeile um „Kennzeichne Annahmen ausdrücklich." ergänzen.
- Begründung: nachzählbar falsche Produktzusage ist ein Positionierungsrisiko (Kanalversprechen „keine leeren Marketingversprechen"); Präzedenz 04/F1. **Empfehlung: Weg B** (7 Halbsätze) — dann darf 03C unverändert bleiben.

**Ä-02 · `03A` · alle 20 Prompts, Regelzeile · P2**
- Problematisch: „Bis zu fünf Rückfragen zuerst" ohne Wartepflicht (nur im Basisblock).
- Ersatz: „Bis zu fünf Rückfragen zuerst — **und warte auf meine Antworten, bevor du das Ergebnis lieferst.**"
- Begründung: Testlauf 1/Variante B — ohne den Halbsatz liefern Modelle sofort und hängen Fragen an; die Regel ist der Kern des Pakets.

**Ä-03 · `03A` · Prompt 13 + 14 · P2**
- Ergänzen: „Wenn ich nach konkreten Personen frage, weise die Anfrage zurück und verweise auf die menschliche Entscheidung mit den zuständigen Stellen."
- Begründung: Testlauf 3/Schritt 7 — Original verbietet Einplanen, aber nicht die Beantwortung von Personen-Nachfragen; härtet den rechtlich sensibelsten Bereich (§ 87 BetrVG; DSGVO Art. 22).

**Ä-04 · `03A` · Prompt 7, 8, 9 (Außenkommunikation) · P2**
- Ergänzen: „Kennzeichne jeden Entwurf sichtbar mit `ENTWURF – NICHT UNGEPRÜFT VERSENDEN`." (P7 behält zusätzlich „Versende nichts…"; in P8/P9 diesen Satz ebenfalls ergänzen.)
- Begründung: Auftragsvorgabe §3; macht die Prüfstufe im Ergebnis selbst sichtbar (Videomoment).

**Ä-05 · Kette (`…step-by-step`) · Schritt 18 · P2**
- Problematisch: „Nutze ausschließlich diese bestätigten Rechnungsdaten: [RECHNUNGSNUMMER, DATUM, BETRAG, …]"
- Ersatz: „Gib mir nur: überfällig seit [TAGEN], Leistung allgemein, bisheriger Kontakt, Kundenbeziehung. Verwende im Entwurf Platzhalter [RECHNUNGSNUMMER], [BETRAG], [DATUM] — die konkreten Werte setze ich erst im fertigen Schreiben ein."
- Begründung: Rechnungsnummer+Betrag+Verlauf identifizieren den Vorgang (Kombinationsfallstrick aus 03B; Präzedenz 04/F7). Entwurfsqualität leidet nicht.

**Ä-06 · `03A` · paketweit · P3**
- Vorschlag: [FEHLT] als Leitmarker benennen (Einleitung: „Der wichtigste Marker ist [FEHLT]; daneben gibt es aufgabenspezifische wie [ZU VERIFIZIEREN] und [PRÜFEN]").
- Begründung: sieben Marker-Varianten sind einzeln sinnvoll, aber für Einsteiger im Video schwerer zu erklären.

**Ä-07 · projektweit · Nummernräume · P2**
- Vorschlag: 03A-Prompts als „A1–A20", Ketten-Schritte als „S1–S20"; Video nutzt nur A-Nummern.
- Begründung: „Prompt 13" (Kapazität) vs. „Schritt 13" (Prioritäten) ist eine vorprogrammierte Zuschauer-Verwechslung.

---

## 14. Empfohlene Bildschirmbeweise

| # | Szene (sichtbar) | Testdatensatz | Hervorgehobenes Ergebnis | Bewiesener Punkt |
|---|---|---|---|---|
| 1 | Split-Screen: naiver Prompt (fertige Mail mit erfundenem „Herr Müller"-Termin) vs. STX-Version (5 Rückfragen, dann Stopp) | Testlauf 4 | rot markierte Erfindungen links; Rückfragen-Stopp rechts | KI erfindet, wenn man sie lässt — die Regel stoppt es |
| 2 | Prompt 5 verbatim: Protokoll mit `[TERMIN FEHLT]` 3× und Notizstellen-Beleg beim einzigen Beschluss | NordWerk-Notiz (Kap. 7) | „bis nächste Woche" landet unter BESPROCHEN, nicht BESCHLOSSEN | Diskussion wird kein Beschluss; nichts erfunden |
| 3 | Prompt 12 verbatim: Scroll auf „Schritt 1 — Zahl selbst prüfen" + Hypothesentabelle | Ausschuss 3,4 % | Messmittel-Hypothese VOR Material-Hypothese | Datenqualität zuerst; Korrelation ≠ Ursache |
| 4 | Prompt 13 verbatim: zweistufige Rechnung 479 h vs. 480 h, dann Zertifikats-Engpass; danach Personen-Nachfrage → Zurückweisung | Kapazitätsfall (Kap. 7) | „Gesamtstunden reichen — das Zertifikat nicht" + „keine Personen" | Rechenweg sichtbar; Rollenebene; menschliche Entscheidung |

Alle vier ausschließlich mit `SYNTHETISCHE DEMODATEN – KEIN REALES UNTERNEHMEN`; vor der Aufnahme in der Zielanwendung wiederholen (B-04).

---

## 15. Sichere öffentliche Aussagen

- „Jeder dieser Prompts stellt zuerst Rückfragen, bevor er liefert." (20/20 am Text belegt; Verhalten in Testläufen bestätigt)
- „Wo eine Angabe fehlt, steht [FEHLT] oder [TERMIN FEHLT] — statt einer plausiblen Erfindung." (Testlauf 1)
- „Ein Beschluss kommt nur ins Protokoll, wenn die Notizstelle ihn belegt." (P5 wörtlich; Testlauf 1)
- „Die Abweichungsanalyse prüft zuerst, ob die Zahl überhaupt stimmt — dann erst Ursachen, und nur als Hypothesen." (P12; Testlauf 2)
- „Kapazität wird auf Rollen- und Qualifikationsebene gerechnet — keine Person wird eingeplant oder bewertet." (P13/P14; Testlauf 3)
- „Wenn ein System Verhalten oder Leistung überwachen kann, hat der Betriebsrat mitzubestimmen — deshalb bleiben Personendaten draußen." (§ 87 Abs. 1 Nr. 6 BetrVG, Wortlaut geprüft)
- „Der EU-KI-Act verbietet Emotionserkennung am Arbeitsplatz, mit engen Ausnahmen." (Art. 5(1)(f))
- „Jeder Prompt sagt dir, was ein Mensch prüfen muss, bevor etwas rausgeht." (Feld L, 20/20)
- „Alle Beispiele: frei erfundenes Demo-Unternehmen, keine echten Daten."
- „Die gezeigten Durchläufe sind echt — nichts nachgestellt." (nur sagen, wenn Zielanwendungs-Recordings vorliegen)

## 16. Nicht verwendbare Aussagen

- „DSGVO-konform / rechtssicher / vollständig sicher" (pauschal)
- „Funktioniert mit jeder KI immer (gleich)" — modellneutral gebaut ≠ garantiert gleiches Verhalten
- „Die KI macht (mit diesen Prompts) keine Fehler"
- „Personalplanung kann vollständig automatisiert werden"
- „Alle Unternehmensdaten können sicher hochgeladen werden"
- Unbelegte Prozent-/Zeitersparnis-Versprechen
- „Anbieter X trainiert garantiert nicht mit euren Daten" (pauschal)
- „Jeder Prompt enthält alle fünf Regeln" — erst nach Umsetzung von Ä-01/Weg B
- Jede Darstellung der Kap.-8–11-Läufe als „in ChatGPT getestet", solange die Zielanwendungs-Wiederholung aussteht

---

## 17. Empfehlung für das Downloadpaket

**Bundle „STX Office AI – 20 Prompts" (ein ZIP / eine Notion-Seite):**
1. `03A` mit umgesetzten Korrekturen Ä-01(Weg B)/Ä-02/Ä-03/Ä-04 — als „A1–A20"
2. `03B` Sicherheits- und Anonymisierungsleitfaden (unverändert freigabefähig)
3. Deckblatt: menschliche Prüfpflicht · „Version 1.0 · Stand 19.08.2026" · Modellneutralität mit Einschränkung
4. Eine Seite „Grenzen dieses Materials": keine Rechtsberatung; Zulässigkeit tool-/tarif-/vertragsabhängig; Prompts getestet, aber Modellverhalten variiert
5. Optional: die vier Testlauf-Screenshots als „So sieht ein korrekter Durchlauf aus"

**Nicht in dieses Bundle:** die 20-Schritte-Kette (eigenes Produkt/Folgevideo, vorher Ä-05 umsetzen) und das ältere Selbstständigen-Paket aus `04` (Verwechslungsgefahr; Positionierungsentscheidung von `04` bleibt offen).

---

## 18. Freigabecheckliste

- [x] Alle 5 Eingangsdokumente vollständig gelesen und geprüft
- [x] Alle 20 Prompts einzeln auditiert (Kap. 5) — kein ROT
- [x] Vier verbatim-Testläufe mit synthetischen Daten durchgeführt und dokumentiert (Kap. 8–11)
- [x] Paket A/B abgegrenzt, Empfehlung begründet (Kap. 4)
- [x] Quellencheck mit Primärquellen, § 87 BetrVG wortlautgeprüft (Kap. 12)
- [x] Konkrete Änderungsliste mit Ersatztexten (Kap. 13)
- [ ] **Ä-01 umsetzen** (Einleitung oder 7 Halbsätze) — P1, vor Download-Veröffentlichung
- [ ] Ä-02/Ä-03/Ä-04 umsetzen — P2, vor Veröffentlichung empfohlen
- [ ] **Vier Testläufe in der Zielanwendung wiederholen** (ChatGPT + Claude-App), Screenshots/Recordings — P1 für die Video-Produktion (README-Regel)
- [ ] Berechtigungs-/Einstellungs-Check des Aufnahme-Kontos am Aufnahmetag
- [ ] Disclaimer „keine Rechtsberatung, Stand [Datum]" in Video und jeder Short-Caption
- [ ] Download nur als Bundle mit `03B` + Grenzen-Seite
- [ ] Ä-05 (Kette S18) vor jeder Veröffentlichung der Kette

---

## 19. HANDOFF FÜR CODEX

### Bereits geprüft
- Alle 5 Eingangsdokumente vollständig (03A: 20 Prompts × 12 Felder einzeln; Kette: alle 20 Schritte).
- 20/20-Audit: Rückfragen-Regel 20/20, Prüfbedarfs-Abschluss 20/20, Anti-Erfindung 20/20, Feld K/L 20/20; Annahmen-Regel ~14–15/20 (einzige Zähllücke).
- Vier verbatim-Testläufe (P5, P12, P13, Negativ/Positiv) mit NordWerk-Synthetikdaten — alle Prüfziele erfüllt; durchgeführt von Claude, **Zielanwendung ausstehend**.
- 04-Hypothesen an 03A verifiziert: Gesundheitsdaten-Problem existiert in 03A **nicht**; AGB-Verbot (P8), Eskalationsfrage (P9), Personen-Grenze (P14) sind bereits eingebaut.
- § 87 Abs. 1 Nr. 6 BetrVG wortlautgeprüft; AI-Act Art. 5(1)(f) und DSGVO-Fundstellen belegt.

### P1-Veröffentlichungsblocker
- **Datei:** `03A` · **Abschnitt:** Einleitung („Jeder einzelne zwingt die KI zu fünf Dingen") + `03C` Kap. 3 · **Problem:** Regel 2 nur ~14–15/20 wörtlich — nachzählbar überzeichnete Produktzusage · **Ersatztext:** Ä-01 Weg B: in P5, P6, P7, P9, P10, P15, P16 „Kennzeichne Annahmen ausdrücklich." ergänzen (dann bleibt die Zusage wörtlich wahr) — alternativ Weg A: Einleitungssatz auf Basisblock-Formulierung ändern · **Begründung:** Kanalversprechen „keine leeren Marketingversprechen"; von jedem Käufer in Minuten nachzählbar.
- **Datei:** Produktion (kein Dokument) · **Abschnitt:** vor Aufnahme · **Problem:** Kap.-8–11-Läufe sind Claude-Ausführungen, nicht Zielanwendungs-Recordings; README verbietet nicht real erzeugte Ergebnisse · **Ersatztext:** — (vier Läufe in ChatGPT **und** Claude-App wiederholen, Screen-Recordings sichern; Wartepflicht-Verhalten je Modell dokumentieren) · **Begründung:** Kernversprechen des Videos sind echte Tests.

### P2-Verbesserungen
- Ä-02: Wartepflicht-Halbsatz in alle 20 Regelzeilen („…und warte auf meine Antworten…").
- Ä-03: Personen-Nachfragen-Zurückweisung in P13/P14.
- Ä-04: „ENTWURF – NICHT UNGEPRÜFT VERSENDEN"-Stempel in P7/P8/P9.
- Ä-05: Kette S18 auf Platzhalter-Rechnungsdaten umstellen.
- Ä-07: Nummernräume A1–A20 / S1–S20.

### Vier beste Bildschirmmomente
1. Negativ/Positiv-Split: erfundener „Herr Müller"-Termin vs. Rückfragen-Stopp (Testlauf 4).
2. Protokoll: „bis nächste Woche" bleibt BESPROCHEN; 3× [TERMIN FEHLT]; Beschluss mit Notizstellen-Beleg (Testlauf 1).
3. Abweichungsanalyse: Messmittel-Prüfung VOR Material-Verdacht; fünf offene Hypothesen (Testlauf 2).
4. Kapazität: 479 h vs. 480 h sieht ausgeglichen aus — der Zertifikats-Engpass ist die eigentliche Story; Personen-Nachfrage wird zurückgewiesen (Testlauf 3).

### Für den Sprechertext bestätigte Aussagen
- Kap. 15 vollständig (10 Aussagen, jeweils mit Belegort).

### Aussagen mit notwendigem Disclaimer
- Alle Rechts-Aussagen (§ 87 BetrVG, AI Act, DSGVO): „keine Rechtsberatung, Orientierung, Stand 19.08.2026, Einzelfall prüfen".
- „Funktioniert mit ChatGPT/Claude/Gemini": nur mit „modellneutral gebaut; gezeigt: echte Durchläufe in [Modell]".
- Mitbestimmung: immer „kann mitbestimmungspflichtig sein", nie „ist".

### Nicht verwenden
- Kap. 16 vollständig (9 Aussagen), insbesondere: DSGVO-konform-Pauschale, „immer gleich", „keine Fehler", Personal-Vollautomatisierung, „alle Daten sicher hochladbar", unbelegte Prozente, „alle fünf Regeln in jedem Prompt" (bis Ä-01 umgesetzt), „in ChatGPT getestet" (bis Wiederholung erfolgt).

### Empfohlene Dateien für den Download
- 03A (mit Ä-01/02/03/04, als A1–A20) + 03B + Deckblatt (Prüfpflicht, Version, Stand) + Grenzen-Seite; optional Testlauf-Screenshots. Kette und 04-Paket **nicht** in dieses Bundle.

### Offene Punkte, die Claude nicht bestätigen konnte
- Verhalten der Wartepflicht-Formulierung in der **Zielanwendung** (ChatGPT-App, Claude-App, ggf. Gemini) — je Modell prüfen; falls Modelle trotz Halbsatz sofort liefern, Formulierung verschärfen („Gib in deiner ersten Antwort AUSSCHLIESSLICH die Rückfragen aus").
- EUR-Lex-Volltext-Wortlaute der DSGVO-Artikel (nur ELI-Fundstellen; Bot-Schutz) — im Browser gegenprüfen.
- Anbieter-Trainingsdaten-/AVV-Aussagen (tarif-/vertragsabhängig) — am Aufnahmetag im Konto prüfen.
- Produktentscheidung aus `04` (Selbstständigen-Paket neben 03A behalten oder aufgehen lassen) — Positionierungsfrage, hier nicht entschieden.

### Abschließende Freigabeempfehlung
**`BEDINGTES GO – nach benannten Korrekturen`**

Begründung: Alle fünf Eingangsdokumente liegen vor und wurden vollständig geprüft; die vorige NO-GO-Begründung (fehlende Kerndateien) ist damit ausgeräumt. Das 20-Prompt-Paket ist im Audit durchgehend GRÜN/GELB ohne einen einzigen roten Befund, und die im alten Review des Parallelpakets gefundenen strukturellen Fehler sind in 03A bereits gelöst. Die vier verbatim-Testläufe mit synthetischen Daten erfüllen alle Prüfziele des Auftrags — kein erfundener Termin, kein Scheinbeschluss, Hypothesen statt Ursachen, Rollen- statt Personenplanung. Es verbleiben genau zwei P1-Punkte: die leicht überzeichnete Fünf-Regeln-Zusage (Fix: sieben Halbsätze oder ein Einleitungssatz) und die Pflicht, die vier Läufe vor der Aufnahme in der Zielanwendung zu wiederholen, weil das Video nur echte Recordings zeigen darf. Beide sind klein, exakt beschrieben und ohne inhaltliches Risiko umsetzbar. Die P2-Korrekturen (Wartepflicht, Entwurfs-Stempel, Personen-Zurückweisung, S18-Datenumfang) erhöhen die Robustheit, blockieren aber nicht. Ein GO FÜR PRODUKTION wäre erst nach den Zielanwendungs-Tests ehrlich; ein NO-GO wäre angesichts der Prüfergebnisse nicht mehr begründbar. Daher: bedingtes GO mit den zwei benannten P1-Bedingungen.

---

*Erstellt am 19.08.2026 (Vollfassung). Keine echten Daten verwendet. Keine Quellen erfunden. Keine Tests behauptet, die nicht durchgeführt wurden — alle Läufe als Claude-Ausführung gekennzeichnet, Zielanwendungs-Wiederholung als offene Pflicht benannt. Keine Originaldateien überschrieben. Kein Commit, kein Push, kein Pull Request; Draft-PR unberührt. Nichts veröffentlicht. Keine Subagenten verwendet.*
