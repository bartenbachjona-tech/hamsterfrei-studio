# Changelog – bewerbungs-profi

## v3 (06.11.2026) – nach Testrunde 2 (41 Sitzungen, Fehlerliste 1–22)

### Wortlaut-Prinzip gegen Erfundenes (Fehler 2, 3)
- Neu: `profil.rohtext` – jede Nutzer-Antwort wörtlich (`nr`, `frage`, `antwort`, optional `bestaetigt`). Eine Bestätigung zählt nur bei klarem „ja“ und wenn genau dieser Wert in der Frage stand.
- `fakten_check.py` prüft jetzt gegen Wortlaut + Anzeige + Einladung + Upload-Texte (Zeugnisse, alter Lebenslauf über textlib) + zugestimmte Firmenfakten – **nicht** mehr gegen Claudes eigene Profil-Felder. Normalisierte Werte (Monat aus „2018“, „Klasse B“, „(B.A.)“, Stunden) ohne Wortlaut → ❌. „01.12.2026“ aus „ab Dezember“ → ❌ (Tag erfunden).
- Dauern werden gegen die aus Zeiträumen berechnete Dauer geprüft („Drei Jahre“ bei 2 J. 11 M. → ❌ „gerundet“; „fast drei Jahre“ ok). Zahlen aus der Anzeige belegen keine Dauer über den Nutzer.
- `belege` nur noch mit Pflicht-`zitat` (muss wörtlich in Wortlaut/Anzeige/Upload stehen).
- v2-Akten ohne rohtext laufen weiter (Hinweis „Kein Wortlaut“).

### Weiche Erfindungen (Fehler 2)
- Motivations-/Gefühls-/Eigenschaftssätze (möchte, Spaß, begeistert, genau so, schon immer, leidenschaftlich, oft, täglich, kein Problem, zuverlässig …) ohne Wortlaut-Stütze → ⚠️.
- `fakten_check.py --woher` liefert die **Woher-Liste** (Satz ↔ Antwort-Nr.) für die Freigabe-Nachricht (max. 5 Zeilen). Sätze ohne Basis werden gefragt, nicht geschrieben.

### Fehlalarme abgeschafft (Fehler 1)
- Zeilenweise Prüfung (nie über Zeilenumbrüche); Grußformel + Name, Anlagen-Zeile, Betreff-Label, Feldtitel `=== … ===`, „max. N Zeichen“ werden ignoriert; Standardwörter nach gleicher Normalisierung („Grüßen“).
- Namen nur bei echten Eigennamen-Mustern (Liste häufiger Nomen/Funktions-/Maßwörter, Nomen-Endungen, Satzanfänge): „Minuten Zeit“, „Ihren Sachen“, „Aushilfe Kasse“ sind keine Namen mehr.
- Führerschein-Regel nur im echten Kontext („13. Klasse am Gymnasium“ ist keiner).
- „Wie aufmerksam geworden?“: geprüft wird nur die Quelle (Portal/Person/Messe).
- Firmenfakt-❌ nur, wenn der Fakt wirklich im Satz steht (Wörter der Stellenbezeichnung zählen nicht).
- Akte/Spickzettel aus Sammelprüfungen ausgenommen; eigener Modus `--typ spickzettel` (Überschriften, Fragen, Tipps/Mitbring-Liste ausgenommen).
- Ergebnis: Das ehrliche Beispiel (Anschreiben + Mail + Formular + Lebenslauf, auch als Dateien) hat 0 ❌ ohne `belege`.

### endcheck.py (Fehler 5–8)
- Rechtsformen nur als ganzes Wort in genauer Schreibweise („Krankenkasse“, „Augusta“, „Reisen“, „Sparkasse“ bleiben ganz).
- Stellenbezeichnung mit Flexions-Toleranz („zur Medizinischen Fachangestellten“).
- Firma und Stellentitel nur noch im Anschreiben/Motivations-/Kurzanschreiben verlangt, nicht in Formular und E-Mail.
- Floskeln als Muster inkl. gebeugter Formen und Konjunktiv-Schluss („würde ich mich sehr freuen“, „mit großem Interesse“, „renommiertes“, „bereichern“).
- Hinweise je Typ; neue Typen `anlage` (Zeugnis-Scan: nur Format/Größe) und `gesamt` ohne Stil-Fehlalarme.

### Ablauf (Fehler 9–11)
- Erst Text im Chat → Freigabe → **einmal** Dateien erzeugen. Der Nutzer sieht nur `…_AKTUELL.pdf`; frühere Fassungen liegen intern in `alt/…_vN` („warum v3?“ entfällt).
- Zeugnisse werden in der Profil-Phase eingesammelt; kommen sie später, zieht `pdf_zusammenfuegen.py --profil` die Anlagen-Zeile automatisch nach.
- Akte: früh (sobald der Name da ist), nach jeder Phase und ~6 Antworten, nie mitten in Übungen; nur `.txt` (PDF auf Wunsch als `Akte-Lesefassung_…`); Name mit Sekunden + Laufnummer; Liste „im neuen Chat wieder hochladen“; Wechselgrund, Abbruchgrund, Zertifikate, Berufstest lesbar; keine doppelten Klammern. `--lesen` findet Anlagen unter den neuen Uploads.
- Ein Anliegen pro Nachricht mit **Konfliktregel**; feste Zählregel (Y ab der ersten Profilfrage, übersprungene Fragen senken Y mit Hinweis); ➡️-Zeile Pflicht außer in Übungen.

### Gerät, Schnellmodus, Budget (Fehler 12–14, 17, 18)
- Gerätefrage erst, wenn Dateien/Anleitungen nötig sind (oder aus Hinweisen abgeleitet).
- Schnellmodus als Tabelle: entfällt (Fahrplan, Erklärungen, Firmen-Recherche optional) / bleibt (Gerätefrage bei Dateien, Fakten-Check, Woher-Liste, Freigabe, Pflicht-Checkliste kompakt, Endcheck, Akte). Vielfrager-Strategie; Budget mit Berufstest ≤ 30.
- Handy: Anzeigen aus Job-Apps per 1–3 Screenshots; flache Dateinamen, kein `versand/`-Ordner, immer „diese Datei hochladen“. Desktop: Kopier-Button am Codeblock bzw. `.txt` statt „Strg+A“; Download/Upload-Anleitung.

### Skripte (Fehler 16, 19, 20)
- `pdf_zusammenfuegen.py`: exakter Zielname (Bindestrich bleibt, sonst klare Meldung); Querformat-Fotos drehen (Texterkennung, falls vorhanden; `--drehen D=90`) oder auf A4-Querseite einpassen; PDF-Anlagen auf A4 skaliert; `--einzeln` mit Bezeichnung statt `IMG_…`, flach + Hochlade-Liste; findet Fassungen in `alt/` bzw. gelöschte Pfade; neu `--buendeln N` für „max. N Dateien“.
- `akte.py --spickzettel` neu: Termin | Art | Ort, Mitbring-Liste, 3 Kernbotschaften, Vorstellung, schwierige Fragen mit den verbesserten Antworten (inkl. Lücken/Abbruch/Wechsel), Beispiele, nur gewählte eigene Fragen, Tipps je Präsenz/Video/Telefon/Probearbeiten/AC; AC-Variante; keine leeren Felder/internen Vermerke; saubere PDF mit Überschriften.
- `unterlagen_erstellen.py`: Zeichengrenze im Feldtitel nicht doppelt; Foto schwebend rechts neben dem Kopf (3,5 × 4,5 cm, zugeschnitten); Kurzanschreiben-Regel (ohne Anlagen-Zeile, `anlagen_zeile` steuert); v3-Beispiel mit rohtext.

### Fachliches (Fehler 15, 21, 22)
- Neue Felder: `wechselgrund`, `zertifikate`, `abbruch_grund`, `motivation_fach`, `berufstest`, `quellen`, `gespraech.{einladung_text, bestaetigt, mitbringen, kernbotschaften, schwierige_fragen, eigene_fragen[gewaehlt], feedback[besser], ac_uebungen}`, `meta.{fragen_gesamt, antworten_seit_akte}`.
- „Wie aufmerksam geworden?“ ist feste Profilfrage; Minijob mit Kenntnisse-Frage; Werkstudent: 20 Std. inkl. anderer Jobs, Ende mit Exmatrikulation; Probearbeiten; Bewerbung per WhatsApp; Portale mit Neu-Eintippen; Termin bestätigen als eigener Schritt; kurze Übungsrunde = festgelegte 5 Fragen; Gehalt immer per Websuche mit Quelle, wenn verfügbar.

## v2 (06.11.2026) – nach Testrunde 1 (41 Sitzungen, Fehlerliste 1–24)

### Nichts erfinden, technisch abgesichert (Fehler 1, 6)
- Neu: **Profil-JSON** (`/tmp/bewerbung/profil.json`, `references/profil_json.md`) mit einem Feld je Fakt, auch für Beispiele/STAR-Geschichten, Lücken, Hobbys, „Wie aufmerksam geworden“, Anlagen, Firmenfakten (mit Quelle + Zustimmung) und Belege. Unterlagen entstehen nur aus dieser JSON und der Anzeige.
- Neu: **`fakten_check.py`** findet in Lebenslauf, Anschreiben, Formular- und Mailtext alles ohne Beleg: Zahlen, Monate/Jahre/Tage, Dauern (auch „acht Jahre“), Eigennamen, Abschlüsse, Sprachniveaus, Führerschein, Links/LinkedIn, Firmenfakten ohne Zustimmung, geratenes „Wie aufmerksam“. Dazu Warnungen bei Aufwertungen („mitkonzipiert“, „geleitet“), [PRÜFEN] als eigenem Vorschlag und ungenutzten Beispielen/Hobbys. Prüft außerdem, ob eine Datei dem freigegebenen Text entspricht. Pflicht vor jeder Freigabe; Exit 1 bei ❌.
- Regeln: [PRÜFEN] nur für echte Lücken; Selbst-Check „Jeder Satz – woher weiß ich das?“; Firmenfakten im Chat mit Quelle, im Text nur mit Zustimmung. Das Beispiel-Anschreiben zeigt kein [PRÜFEN]-Vorschlagsmuster mehr.

### Gesprächsführung (2, 3, 5)
- Eine Frage pro Nachricht konsequent: Rahmen-Frage aufgeteilt (Start / Foto / Hobbys einzeln), keine „pro Station“-Serie mehr, Minijob-Fragen getrennt. Rückfrage → beantworten und **dieselbe** Frage wiederholen; „Frage X von Y“ steht nach Frage 3 fest, Nachfragen zählen nicht.
- Hinweis-Block höchstens 2 Zeilen; entfällt in Rollenspielen, Simulationen und Testaufgaben.
- Schnellmodus definiert: was entfallen darf und was nie (Fakten-Check, Freigabe vor dem Absenden, Abgleich Datei = Text, Endcheck, Akte).
- Ziel: komplette Bewerbung (Profil → Unterlagen) in ≤ ~25 Nutzer-Nachrichten (Nachrichten-Budget in SKILL.md, ~10 Profil-Fragen).
- Berufstest: 12 sehr kurze Aussagen als **ein Block** („1a 2c 3b …“ oder Auswahl-Werkzeug); Kurzweg mit 3–5 Fragen für Minijob/Praktikum; danach 3 Vorschläge mit je 1 Satz Begründung. Check-U/BERUFENET/Berufsberatung als Pflichtzeile (9).
- Gespräch/AC: eine kompakte Übersicht (≤ 12 Zeilen) oder ein Spickzettel-PDF, dann direkt üben.

### Free-Plan, Handy, Anfänger (4, 10–14)
- Fahrplan in Chats am Start; Akte nach jeder Phase **und** spätestens alle ~6 Antworten, per Skript; proaktiv „neuen Chat starten, Akte hochladen“.
- Neu: **`akte.py`**: Akte als `.txt` (öffnet überall, mit eingebetteter JSON), optional als PDF; `--lesen` zum Fortsetzen (auch alte `.md`); `--spickzettel` ohne Markdown-Zeichen. Datum + Uhrzeit im Namen, ältere nach `alt/`.
- Neu: `references/geraet.md`. Das Gerät wird früh abgefragt. Am Handy gibt es immer PDF (`--nur-pdf`), keine Strg-Tasten, Anzeige per Screenshot oder „Teilen → Kopieren“, Download/Upload für iPhone und Android erklärt, Postkorb und Checklisten in Häppchen (höchstens 3–4 pro Nachricht).

### Skripte (7, 8, 13, 15–20)
- `unterlagen_erstellen.py`: Dateinamen mit Transliteration (ć→c, ş→s, ı→i, ë→e, ß→ss, Umlaute→ae/oe/ue); Kürzen nur an Wortgrenzen; Typen Motivationsschreiben/Kurzanschreiben; Formular- und Mail-Texte (`--nur formular|email`); [PRÜFEN]-Zählung pro Dokument; [PRÜFEN] im Zeitraum → „??“ in der Spalte + Notiz darunter; graue statt blauer Titellinie; Versionen `_vN`, im Ausgabeordner genau eine aktuelle Fassung, ältere in `alt/`; Anlagen-Zeile automatisch aus den vorhandenen Dateien (`profil.anlagen`); `--nur-pdf`.
- `pdf_zusammenfuegen.py`: Abbruch mit Exit 2 bei fehlender Datei/fehlgeschlagener Umwandlung (keine halbe PDF); nimmt automatisch die neueste Fassung (mit Hinweis, `--genau` schaltet das ab); HEIC über pillow-heif, sonst klare Handy-Anleitung; Fotos auf A4 eingepasst (EXIF-Drehung); Anlagen-Zeile gegen die angehängten Dateien geprüft (Exit 3); `--profil` stellt alles automatisch zusammen; `--einzeln` erzeugt saubere Einzeldateien für Formulare.
- `endcheck.py`: Dokumenttyp per `--typ` statt Dateiname; `--profil`; E-Mail-Warnung nur bei echten Problemen (Spitzname, Zahlenfolge ≥ 3, Jugendsprache, Name fehlt); frühere Arbeitgeber/Schulen aus dem Profil gelten nicht als Fremdfirma; Firmenvergleich unscharf ohne Rechtsform; ganze Stellenbezeichnung; Formular-.txt richtig geprüft (Feldtitel `=== … ===`, Zeichenlimits, leere Felder, „siehe Lebenslauf“, Platzhalter); Kurzanschreiben-Bewertung nur bei `--typ kurzanschreiben`; Exit 1 bei ❌.
- `berufstest_auswerten.py`: Hexagon-Abstand korrekt (gegenüber nur R–S, I–E, A–C; „eine Ecke dazwischen“ für S+C, I+C, A+E, I+S …); Kompakt-Eingabe „1a 2c …“; kürzere Aussagen.
- `ordner_anlegen.py`: `--ausgabe`, Akte aus der JSON (über akte.py), keine leere Vorlage mehr; `--nur-akte` braucht `--profil`.
- `textlib.py`: gemeinsame Hilfen (Transliteration, Versionen, Profil laden); `--info` erkennt Spalten/Tabellen in PDFs grob (als Hinweis gekennzeichnet); `--help` funktioniert.

### Fachinhalt (21–24)
- Berufstest: Vorschläge für alle 15 Zwei-Buchstaben-Codes sowie für Absolventen, Quereinsteiger, Werkstudenten und Minijob/Nebenjob; Hinweis auf schulische Ausbildungen mit Schulgeld.
- Neu: `references/sonderfaelle.md` zu Mindestlohn und Minijob-Grenze 2026/2027 mit Quelle und Stand, Praktikum und Mindestlohn, Werkstudenten-Regeln (20 Std., Versicherung), Lücke, Wiedereinstieg, Studienabbruch, Initiativbewerbung, Teilzeitausbildung, PiA, Anzeige offline, mitgebrachtem ChatGPT-Text, älteren Bewerbern (Sie/Du, keine Schulnoten), privaten Angaben nur auf Wunsch und Upload-/Zeichenlimits.
- Gespräch: Einladung bestätigen; Telefon-, Video- und technisches Interview; Frage nach der Kinderbetreuung als unzulässig. AC: Menü an die Einladung angepasst, Einladung mit Frist bestätigen.
- Gehalt: Websuche mit Quelle oder eine Anleitung für den Entgeltatlas (Claude kann ihn nicht abrufen). Rechtliches nur allgemein, keine Einzelfall-Fristen.

### Beibehalten
Fallback bei blockiertem Link, Anzeige als Daten (Schutz vor Prompt-Injection), Fortsetzung über die Akte, einspaltiges ATS-Layout auf 1 Seite.

## v1 (06.11.2026)
Erste Fassung: 9 Phasen, 6 Skripte, Akte als `.md`.
