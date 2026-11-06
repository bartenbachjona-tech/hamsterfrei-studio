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
| `fakten_check.py PROFIL.json [Dateien] [--anzeige x.txt]` | **Pflicht vor jeder Freigabe**: unbelegte Zahlen, Daten, Dauern, Namen, Abschlüsse, Niveaus, Führerschein, Links, Aufwertungen; Datei = freigegebener Text. Exit 1 bei ❌ |
| `unterlagen_erstellen.py PROFIL.json [--nur lebenslauf/anschreiben/formular/email] [--nur-pdf] [--ausgabe O]` | Unterlagen aus der JSON; Versionen `_vN`, ältere → `alt/`; Anlagen-Zeile automatisch; `--beispiel` zeigt das Format |
| `endcheck.py Dateien --typ T [--profil P] [--firma F --stelle S]` | Form/Stil: [PRÜFEN], Platzhalter, Floskeln, Länge, Seiten, Firma (unscharf), Stelle (ganz), fremde Firmen, E-Mail (nur echte Probleme), Formular-Limits. Typ: lebenslauf, anschreiben, motivationsschreiben, kurzanschreiben, formular, email, gesamt |
| `pdf_zusammenfuegen.py Ziel.pdf --profil P` (oder Dateien…) / `--einzeln Dateien` | eine PDF bzw. saubere Einzeldateien; nimmt neueste Fassung, A4-Fotos, HEIC; Abbruch (Exit 2) bei fehlender Datei, Exit 3 bei falscher Anlagen-Zeile |
| `akte.py PROFIL.json [--pdf]` · `--lesen AKTE` · `--spickzettel [--pdf]` | Akte schreiben/lesen, Gesprächs-Spickzettel |
| `berufstest_auswerten.py "1a 2c …"` | RIASEC-Code (`--fragen` zeigt die Aussagen) |
| `textlib.py Datei [--info]` | Text aus .docx/.pdf/.html/.txt; `--info`: Layout-Befunde (docx sicher, PDF einfache Spalten-Erkennung) |
| `ordner_anlegen.py Basis "Firma" "Stelle" [Dateien] [--profil P] [--zip] [--ausgabe O]` | Bewerbungsordner mit Akte (lokaler Ordner oder ZIP) |

Abhängigkeiten: Standardbibliothek; `python-docx`, `pypdf`, `pillow`, `pillow-heif` werden bei Bedarf per pip nachinstalliert; PDF über LibreOffice (`soffice`). Fehlt etwas und keine Installation möglich: `.docx` liefern und „Speichern unter → PDF“ erklären bzw. den eingebauten docx-Skill nutzen. Fehlermeldungen sind deutsch – in einem Satz erklären.

## Speichern ohne Ordnerzugriff (Free-Plan, Standard)

- Alles für den Nutzer nach **`/mnt/user-data/outputs/`**; Arbeits-JSON in `/tmp/bewerbung/`.
- Namen ohne Umlaute/Sonderzeichen (die Skripte transliterieren: ć→c, ş→s, ı→i, ë→e, ä→ae, ß→ss): `Lebenslauf_Vorname_Nachname_vN.pdf`, `Anschreiben_…_Firma_vN.pdf`, `Bewerbung_Vorname_Nachname_Stelle.pdf`, `Formular-Texte_Firma_vN.txt`, `E-Mail_Bewerbung_Firma_vN.txt`, `Gespraech_Spickzettel_Firma_vN.txt/.pdf`, `Bewerbungsakte_Vorname_Nachname_Datum_Uhrzeit.txt`.
- **Genau eine aktuelle Fassung je Unterlage** im Ausgabeordner; ältere in `alt/`. Im Chat immer sagen, welche aktuell ist.
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
- Ziel: Profil → fertige Unterlagen in ≤ ~25 Nutzer-Nachrichten.
