# Changelog – bewerbungs-profi

## v4 (06.11.2026) – nach Testrunde 3 (48 Sitzungen, 83 % zufrieden; Fehlerliste 1–6, Transkripte 135, 227, 233, 319, 500, 530, 920, 941)

### Satz-Herkunft statt Marker-Liste (Fehler 1)
- Neu: Claude legt beim Entwurf von Anschreiben, Motivationsschreiben, Mail, Formular-Freitext und WhatsApp-Text für **jeden Satz über die Person** einen Eintrag in `herkunft` an (Antwort-Nr. + wörtliches Zitat; Firmenbezug: Anzeige-Zitat oder zugestimmter Firmenfakt).
- Neu: `herkunft.py` (läuft in `fakten_check.py` automatisch mit): Zitat muss wörtlich in der Antwort stehen; der Satz darf keine Inhaltswörter/Zahlen enthalten, die weder im Zitat noch in der Liste neutraler Wörter stehen (Beugung, Komposita, trennbare Verben, Kaufmann/-frau werden erkannt). Meldung nennt die Wörter („Wörter ohne Quelle: täglich, lerne, schnell“).
- Satz ohne Quelle → ❌ „nicht schreiben, sondern fragen“. Personen-Fakten nie aus der Anzeige; Zeugnis-Fotos erst nach Rückfrage; Gesundheit/Familie/Privates nur mit `privat_ok` (im Anschreiben ⚠️); unsichere Antworten („b2 glaub ich“) → ⚠️ bis `geklaert`; sensible Antworten (`sensibel`) zählen nie.
- `--woher` druckt jetzt die kompakte Woher-Liste aus `herkunft` („Satzanfang → deine Worte: … (Nr. 3)“); die alte Wort-Zuordnung und die Marker-Liste sind entfernt.
- Regressionen: die erfundenen Sätze aus 500 („täglich … lerne neue Programme schnell“), 530 („schwer tragen bin ich gewohnt“), 920 („wie Waren ankommen und weitergehen“) und 941 („an Ihrem Stand kennengelernt“) werden abgelehnt; die ehrlichen Fassungen gehen durch.

### Normalisierungs-Wörterbuch, keine Fehlalarme (Fehler 2)
- `textlib.NORMALISIERUNG` (beide Richtungen): abi, fachabi, quali, msa, m10, mittlere reife, fsj/föj/bfd, zfa/mfa/kfz, bio/mathe/lk, fos/bos/gym/th/fh/uni, bwl, B.A. ↔ Bachelor of Arts (B.Sc., B.Eng., M.A. …), papa/mama, str., min, „20h“ → Std., „29-31k“ → 29.000/31.000, Monatsnamen mit Tippfehlern („febuar“).
- Daten: „april 25“, „märz bis august 24“, „31. August 2027“ = 31.08.2027, Monat ohne Jahr (nächstes/letztes Vorkommen), „zum 1. januar“, „9:00 Uhr“ = „9 Uhr“.
- Kein Fehlalarm mehr für GROSS geschriebene Abschlüsse, Kinderalter („4 und 7 Jahre“), Kenntnis-Labels („Zertifikate:“, „Weitere Kenntnisse:“), „Ihr Haus“/„Ihre Praxis“, Satzpunkt am Feldende, umbrochene Anlagen-Zeile, Briefdatum eines späteren Tages, eigene Nummerierung und Übungen im Spickzettel. Dauern werden nur noch gegen passende Zeiträume gerechnet (nicht „4 Semester“ gegen den Minijob).
- Lebenslauf wird nur gegen den Nutzer-Wortlaut geprüft (Anzeige belegt nichts über die Person).
- `belege` gilt nur, wenn das Zitat den Wert trägt („drei Jahre“ aus „seit 09/2025“ → ❌); `woher` ist kein Beleg mehr.
- Zähler „offene [PRÜFEN]“ zählt wieder (war immer 0).
- Ziel erreicht: ehrliche Texte mit allen Normalisierungen → 0 ❌ ohne `belege` (Test).

### Spickzettel neu (Fehler 3)
- Datenstruktur: `anrede` du|sie, `vorstellung{dauer_min, kernpunkte}`, `schwierige_fragen[{frage, antwort_final}]`, `fachfragen`, `gehalt`, `eigene_fragen`, `mitbringen`, `ac_uebungen[{typ, titel, dauer_min}]`; `feedback` bleibt intern.
- Vorstellungsdauer aus der Einladung (3/5 Min.); nur echte Fragen mit finaler Antwort (kein Feedback, keine Notizen, kein Wechselgrund-Rohtext, keine Übungsnamen); Lücke/Abbruch/Wechsel nur als Hinweis an Claude.
- AC-Tipps je Typ: Selbstpräsentation („Warum ich?“, „Mein Weg …“) ≠ Fallstudie; Präsentation, Gruppenaufgabe/-diskussion, Postkorb, Rollenspiel, Interview, Test.
- Grammatik („Tipps für deinen Auswahltag“), Sie-Form durchgehend, Gehaltsfrage nie still weg („noch offen – vor dem Termin klären“), Abschnitt Fachfragen.
- PDF kompakt in A5 (am Handy ohne Zoomen lesbar), rückt zusammen statt fast leerer Seite 2; `--a4` zum Drucken. Hinweise an Claude: Ort/Termin ≠ Einladung („Filiale am Ludwigsplatz“), offene Gehaltsfrage, 3.-Person-Notizen.

### Dateien (Fehler 4)
- `--buendeln`: Motivationsschreiben heißt „Motivationsschreiben_…“ (bzw. „…_und_Anlagen“). Quellen werden in `--ordner`, `--ausgabe` und im Standardordner gesucht.
- `--einzeln`: Arbeitsdateien `…_AKTUELL.pdf` wandern danach nach `alt/` – keine zwei gleichen Dateien am Handy; neue Fassung schiebt alte Upload-Kopien nach `alt/`.
- Dateinamen bis 70 Zeichen, nie auf „fuer/der/und“ endend. „max. 1.000 Zeichen“ nicht doppelt (Formular + endcheck). Kennziffer im Betreff mit geschütztem Bindestrich (kein Umbruch).
- endcheck: „Start“, Jahreszahlen, „Vollzeit“ im Stellentitel müssen nicht in den Betreff; Geburtsjahr in der E-Mail ist keine „Zahlenfolge“; neuer Typ `whatsapp`.
- Neu: `whatsapp.text` → `--nur whatsapp` → `WhatsApp-Text_Firma_AKTUELL.txt`.
- Akte: Reupload-Liste ohne Duplikate, Lücke mit `erklaerung` oder `grund`, keine Doppelklammer „Aushilfe (Aushilfe (…))“; `--lesen` findet umbenannte Akten („Bewerbungsakte (1).txt“, auch nur Ordner angeben) und Re-Uploads unter neuem Namen (gleicher Inhalt per Fingerabdruck, „IMG_2041 (1).jpg“, einzige neue Datei).

### Länge, Fragen, Ablauf (Fehler 5)
- **Gerätefrage abgeschafft:** immer PDF (+ .docx), zwei Bedienzeilen für Handy und PC; ausführlich nur bei Problemen. Link blockiert: beide Wege in einer Nachricht.
- **Kurzpfade:** Minijob/Nebenjob max. 5 Profilfragen, Unterlagen ≤ 10 Nachrichten; Probearbeiten = 1 Übersicht (≤ 10 Zeilen) + max. 2 Übungsfragen. Gesamtbudget inkl. Gespräch/AC ≤ 35.
- Schon gegebene Antworten (👍, „passt“, Kurzweg, Nebenbei) zählen; unklare Antworten und zurückgeschickte Beispielwerte → eine Ja/Nein-Rückfrage.
- Pflicht-Checkliste in einem Teil (≤ 6 Zeilen). Postkorb max. 6 Dokumente in 2 Häppchen; jede Übung mit „stopp“ abbrechbar → Kurzfeedback. Gruppendiskussion max. 5 Runden.
- Hinweis-Block: bei kurzen Rückfragen nur 👉; keine starre 8-Zeilen-Grenze, lange Inhalte als Codeblock/Datei. Nie zwei Anliegen (Freigabe + Angebot, Freigabe + Chatwechsel). Chatwechsel-Hinweis einmal und nicht kurz vor einem Ziel.
- SKILL.md neu gegliedert (146 Zeilen): kritische Regeln oben, Kurzpfade, Bedienung, Beispiele (Woher-Liste, Satz ohne Quelle, 👍, Probearbeiten).

### Fachliches (Fehler 6)
- Werkstudent-KV richtiggestellt: Familienversicherung bis 25, studentische KV bis Ende des Semesters, in dem man 30 wird; die 14-Fachsemester-Grenze gilt seit 01.01.2020 nicht mehr (Quellen: Barmer, Stand 22.09.2026; sozialversicherung-kompetent.de).
- Karriereseite = Anzeige, wenn sie die Stelle beschreibt; Hörensagen über die Firma nur als Aussage des Nutzers; unbekannte Bewerbungs-Mailadresse nicht raten; telefonische Einladung ohne Bestätigungs-Mail-Pflicht; persönlich abgeben; WhatsApp-Gerätewechsel; private Projekte im Lebenslauf; sensible Details nicht wörtlich in die Akte; Online-Formular: Felder vorab per Screenshot; KI-Hinweis der Firma ≠ Prompt-Injection (Nutzer entscheidet ehrlich); keine unbelegten Gehaltseinschätzungen; Online-Test nach dem Abschicken anbieten; Arbeitszeugnis nachträglich anfordern.

### Tests
- Testsuite 165 → 253 Tests (`bewerbungs-profi-tests/run_tests.py`, schreibt nur unter `/tmp/bp_test4/`), inkl. Sichtprüfung von Lebenslauf-, Anschreiben- und Spickzettel-PDF als Bild.

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
