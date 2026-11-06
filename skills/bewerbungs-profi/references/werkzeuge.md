# Werkzeuge, Speichern und kostenloses Claude

Der Skill funktioniert mit dem **kostenlosen Claude**, wenn „Code-Ausführung und Dateierstellung“ (bzw. „Dateien erstellen und bearbeiten“) eingeschaltet ist. Prüfe still, welche Werkzeuge da sind; sag dem Nutzer nur, was für ihn wichtig ist. Fehlt die Code-Ausführung: Texte im Chat liefern und erklären, wie man die Einstellung einschaltet (Einstellungen → Funktionen).

| Funktion | Kostenlos | Mit Extras |
|---|---|---|
| Anzeige-Link lesen | oft; sonst Screenshot, Text oder PDF | – |
| Firmen-Recherche, aktuelle Zahlen | wenn Websuche an ist | – |
| Lebenslauf, Anschreiben (.pdf + .docx) | Download | direkt im lokalen Ordner |
| Gesamt-PDF, E-Mail-/Formular-Texte | Download | lokaler Ordner |
| Gespräch/AC üben | Text, Diktat/Sprachmodus | – |
| Weitermachen | Akte (.txt) hochladen | Claude-Projekt mit Akte |

## Die Skripte (immer ausführen, nicht nachbauen)

| Skript | Zweck |
|---|---|
| `fakten_check.py PROFIL.json [Dateien] [--woher] [--typ spickzettel] [--anzeige x.txt] [--quelle upload.pdf]` | **Pflicht vor jeder Freigabe**: prüft gegen Nutzer-Wortlaut (mit Normalisierungs-Wörterbuch), Anzeige, Einladung, Uploads – nicht gegen Claudes JSON-Werte. Zahlen, Daten, Monate, Dauern (nur gegen passende Zeiträume), Namen, Kürzel, Niveaus, Führerschein, Links, „Wie aufmerksam“, Firmenfakten, belege (Zitat muss den Wert tragen), Datei = freigegebener Text **und die Satz-Herkunft** (herkunft.py). `--woher` druckt die Woher-Liste. Lebenslauf nur gegen den Wortlaut. Exit 1 bei ❌ |
| `herkunft.py PROFIL.json [--teil anschreiben/formular/email/whatsapp/kurzprofil]` | Satz-Herkunft allein prüfen + Woher-Liste (läuft in fakten_check automatisch mit). v5: prüft nur Behauptungs-Bausteine – Formulierung frei |
| `sprachlib.py "Text"` | Hilfsmodul (Lemma, Umgangssprache → Standard, Synonyme, Tippfehler-Toleranz, Stil-Check, Satztrenner in textlib); zum Ausprobieren: Stil-Befunde eines Texts |
| `unterlagen_erstellen.py PROFIL.json [--nur lebenslauf/anschreiben/formular/email/whatsapp] [--nur-pdf] [--ausgabe O]` | Unterlagen aus der JSON – **erst nach der Freigabe**; Lücken aus `profil.luecken` automatisch; Exit 3 bei offenen Änderungswünschen; `…_AKTUELL`, frühere intern in `alt/`; alte Upload-Kopien wandern mit; Anlagen-Zeile automatisch; Kennziffer im Betreff ohne Umbruch; `--beispiel` zeigt das Format (inkl. herkunft) |
| `endcheck.py Dateien --typ T [--profil P]` | Form/Stil inkl. **Stil-Check** (Umgangssprache, Chat-Kürzel, Tippfehler, „Sa und So“, doppelte Wörter → ⚠️ mit Vorschlag); mit `--profil` auch Zeitraum zu lang/Enddatum in der Zukunft. Typ: lebenslauf, anschreiben, motivationsschreiben, kurzanschreiben, formular, email, whatsapp, gesamt, anlage. Firma/Stelle nur im Brief (ohne „Start“/Jahr), gebeugte Floskeln, Zeichengrenzen auch „1.000“ |
| `pdf_zusammenfuegen.py Ziel.pdf --profil P` · `--einzeln --profil P` · `--buendeln N --profil P [--ordner Q] [--ausgabe O]` | Gesamt-PDF, saubere Einzeldateien (Arbeitsdateien danach in `alt/`, Word-Fassungen in `bearbeitbar/` – eine Datei je Unterlage), Bündel (Motivationsschreiben heißt so); Quellen in `--ordner`/`--ausgabe`/Standard gesucht; Querformat drehen, A4; Exit 2 bei fehlender Datei |
| `akte.py PROFIL.json [--pdf]` · `--lesen AKTE\|ORDNER` · `--spickzettel [--pdf] [--a4]` | Akte schreiben/lesen (findet umbenannte Akten und Re-Uploads); Spickzettel kompakt A5, Du/Sie, Hinweise an Claude |
| `berufstest_auswerten.py "1a 2c …"` | RIASEC-Code (`--fragen` zeigt die Aussagen) |
| `textlib.py Datei [--info]` | Text aus .docx/.pdf/.html/.txt; `--info`: Layout-Befunde |
| `ordner_anlegen.py Basis "Firma" "Stelle" [Dateien] [--profil P] [--zip] [--ausgabe O]` | Bewerbungsordner mit Akte (lokaler Ordner oder ZIP) |

Abhängigkeiten: Standardbibliothek; `python-docx`, `pypdf`, `pillow`, `pillow-heif` werden bei Bedarf per pip nachinstalliert; PDF über LibreOffice (`soffice`). Fehlt etwas und keine Installation möglich: `.docx` liefern und „Speichern unter → PDF“ erklären bzw. den eingebauten docx-Skill nutzen. Fehlermeldungen sind deutsch – in einem Satz erklären.

## Speichern ohne Ordnerzugriff (Free-Plan, Standard)

- Alles für den Nutzer nach **`/mnt/user-data/outputs/`**; Arbeits-JSON in `/tmp/bewerbung/`.
- Namen ohne Umlaute/Sonderzeichen (die Skripte transliterieren: ć→c, ş→s, ı→i, ë→e, ä→ae, ß→ss), flach, ohne Unterordner: Arbeitsdateien `Lebenslauf_Vorname_Nachname_AKTUELL.pdf`, `Anschreiben_…_Firma_AKTUELL.pdf`, `Formular-Texte_Firma_AKTUELL.txt`, `E-Mail_Bewerbung_Firma_AKTUELL.txt`, `Gespraech_Spickzettel_Firma_AKTUELL.txt/.pdf`; zum Versand `Bewerbung_Vorname_Nachname_Stelle.pdf` bzw. `Lebenslauf_Vorname_Nachname.pdf` usw.; Akte `Bewerbungsakte_Vorname_Nachname_Datum_HHMMSS.txt`.
- **Genau eine Datei je Unterlage** (`…_AKTUELL`) im Ausgabeordner; frühere intern in `alt/` – nicht erwähnen. Dateien erst **nach der Freigabe** erzeugen, nicht „zur Ansicht“.
- Nach jeder Datei sagen, was der Nutzer tut (Handy: `geraet.md`).
- Optional am Ende: alles als ZIP (`ordner_anlegen.py /tmp "Firma" "Stelle" Dateien… --profil P --zip`).

## Speichern mit lokalem Ordner (Desktop-App, bezahlte Pläne)

1. Kurz fragen: „Soll ich deinen Bewerbungsordner direkt in [Ordner] anlegen? a) Ja (Empfohlen) b) Nein, nur Downloads“.
2. Befehle dort möglich: `python3 "$S/ordner_anlegen.py" "<Ordner>" "Firma" "Stelle" [Dateien] --profil /tmp/bewerbung/profil.json`. Nur Dateien schreibbar: in der Sandbox bauen und kopieren.
3. Struktur: `Bewerbung_Firma_Stelle/` mit Akte, `01_Stellenanzeige`, `02_Lebenslauf`, `03_Anschreiben`, `04_Zeugnisse_Anlagen`, `05_Versand`, `06_Gespraech`.
4. Erzeugte Dateien mit `--ausgabe "<Ordner>/02_Lebenslauf"` usw. direkt hineinschreiben.
5. Nichts löschen oder überschreiben. Hat der Nutzer eine Datei selbst geändert: erst nachfragen. Datei in Word geöffnet: um Schließen bitten.

## Nachrichtenlimit

- Fahrplan in Chats (`bewerbungsakte.md`), Akte nach jeder Phase und alle ~6 Antworten.
- Lange Ergebnisse als Datei, im Chat nur Kurzfassung; Skript-Ausgaben nie komplett in den Chat kopieren.
- Ziel: Profil → fertige Unterlagen in ≤ ~25 Nutzer-Nachrichten (Minijob ≤ 10), alles inkl. Gespräch ≤ 35.
