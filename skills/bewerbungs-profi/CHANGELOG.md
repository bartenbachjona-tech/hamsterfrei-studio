# Changelog – bewerbungs-profi

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
