# Werkzeuge, Speichern und kostenloses Claude

Der Skill funktioniert **mit dem kostenlosen Claude**. Voraussetzung: In den Einstellungen ist „Code-Ausführung und Dateierstellung“ (bzw. „Dateien erstellen und bearbeiten“) eingeschaltet. Prüfe still, welche Werkzeuge da sind, und sag dem Nutzer nur, was für ihn wichtig ist. Fehlt die Code-Ausführung ganz: Texte im Chat liefern und erklären, wie man die Einstellung einschaltet.

| Funktion | Kostenloses Claude | Mit Extras |
|---|---|---|
| Anzeige-Link lesen | ✅ oft; sonst Text einfügen oder PDF hochladen | – |
| Firmen-Recherche | ✅ wenn Websuche an ist; sonst fragt der Nutzer selbst nach | – |
| Lebenslauf, Anschreiben (.docx + .pdf) | ✅ zum Download | direkt im lokalen Ordner |
| Gesamt-PDF, E-Mail-/Formular-Texte | ✅ zum Download | direkt im lokalen Ordner |
| Gespräch/AC üben | ✅ Text; Sprachmodus/Diktat, falls die App ihn bietet | – |
| Weitermachen in neuem Chat | ✅ `Bewerbungsakte.md` hochladen | Claude-Projekt mit Akte als Datei |
| Bewerbungsordner | ✅ optional als ZIP | Ordner `Bewerbung_Firma_Stelle` auf dem Rechner |

## Die Skripte (immer ausführen, nicht nachbauen)

| Skript | Zweck |
|---|---|
| `berufstest_auswerten.py 4 5 2 …` | RIASEC-Code aus den 12 Antworten (`--fragen` zeigt die Aussagen) |
| `textlib.py Datei [--info]` | Text aus .docx/.pdf/.html/.txt; `--info` zeigt Tabellen, Spalten, Textfelder (ATS-Risiko) |
| `unterlagen_erstellen.py daten.json [--nur lebenslauf/anschreiben] [--ausgabe Ordner] [--kein-pdf]` | Lebenslauf + Anschreiben als .docx und .pdf; liest auch `Bewerbungsakte.md`; `--beispiel` zeigt das Datenformat |
| `endcheck.py Dateien --firma "…" --stelle "…"` | Selbstcheck: [PRÜFEN], Platzhalter, Floskeln, Länge, Seiten, Firmenname, ATS, Dateiname, Größe |
| `pdf_zusammenfuegen.py Ziel.pdf Dateien…` | Anschreiben + Lebenslauf + Anlagen zu einer PDF (docx/jpg werden umgewandelt) |
| `ordner_anlegen.py Basis "Firma" "Stelle" [Dateien] [--zip]` | Bewerbungsordner + Akte; `--nur-akte` für den Free-Plan |

Abhängigkeiten: Standardbibliothek; `python-docx` (wird bei Bedarf per pip nachinstalliert), für PDF LibreOffice (`soffice`), zum Zusammenfügen `pypdf` (pip-Fallback) oder `pdfunite`, für Bilder Pillow. Fehlt etwas und ist keine Installation möglich: `.docx` liefern und erklären, wie man in Word „Speichern unter → PDF“ macht; ersatzweise den eingebauten docx-Skill nutzen. Die Skripte melden Fehler auf Deutsch – lies die Meldung und erklär sie dem Nutzer in einem Satz.

## Speichern ohne Ordnerzugriff (Free-Plan, Standard)

- Alles, was der Nutzer bekommen soll, kommt nach **`/mnt/user-data/outputs/`** – sonst sieht er es nicht.
- **Klare Dateinamen** ohne Umlaute/Leerzeichen: `Lebenslauf_Vorname_Nachname.docx/.pdf`, `Anschreiben_Vorname_Nachname_Firma.docx/.pdf`, `Bewerbung_Vorname_Nachname_Stelle.pdf`, `E-Mail_Bewerbung_Firma.txt`, `Formular-Texte_Firma.txt`, `Gespraech_Vorbereitung_Firma.md`, `Bewerbungsakte.md`.
- Neue Fassungen bekommen `_v2`, `_v3` (die Skripte machen das automatisch). Nur die Akte behält immer ihren Namen.
- Nach jeder Datei sagen, was der Nutzer damit tut: „Lade beide herunter und speicher sie in einem Ordner ‚Bewerbung Beispiel GmbH‘ auf deinem Handy/PC.“
- Optional am Ende: alles als ZIP mit Ordnerstruktur (`ordner_anlegen.py /tmp "Firma" "Stelle" Dateien… --zip`).

## Speichern mit lokalem Ordner (bezahlte Pläne, Desktop-App mit verbundenem Ordner)

Erkennst du einen verbundenen Ordner (Datei-Werkzeuge für den Rechner des Nutzers):
1. Kurz fragen: „Soll ich deinen Bewerbungsordner direkt in [Ordnername] anlegen? a) Ja (Empfohlen) b) Nein, nur Downloads“.
2. Kannst du dort Befehle ausführen: `python3 "$S/ordner_anlegen.py" "<verbundener Ordner>" "Firma" "Stelle" [Dateien] --name "Vorname Nachname"`. Kannst du dort nur Dateien schreiben: den Ordner in der Sandbox bauen (gleiches Skript) und die Dateien in den verbundenen Ordner kopieren.
3. Struktur:
```
Bewerbung_Firma_Stelle/
├── Bewerbungsakte.md          ← Stand, Profil, Status, nächste Schritte
├── 01_Stellenanzeige/         ← Anzeige als PDF/Text, Steckbrief
├── 02_Lebenslauf/
├── 03_Anschreiben/
├── 04_Zeugnisse_Anlagen/
├── 05_Versand/                ← Gesamt-PDF, E-Mail-/Formular-Texte, Bestätigung
└── 06_Gespraech/              ← Einladung, Vorbereitung, Übungs-Feedback
```
4. Erzeugte Dateien mit `--ausgabe "<Ordner>/02_Lebenslauf"` usw. direkt an die richtige Stelle schreiben.
5. Nichts löschen, nichts überschreiben (außer der Akte). Hat der Nutzer eine Datei inzwischen selbst geändert, erst nachfragen. Ist eine Datei in Word geöffnet, kann das Speichern scheitern – dann um Schließen bitten.

## Nachrichtenlimit und lange Chats

- Pro Chat ein großer Schritt (z. B. Berufstest, Unterlagen, Gesprächstraining).
- Lange Ergebnisse als Datei, im Chat nur Kurzfassung. Skript-Ausgaben nicht vollständig in den Chat kopieren.
- Wird der Chat lang: Akte aktualisieren, herunterladen lassen, neuen Chat empfehlen.

## Fragen-Stil (Kurzfassung)

Eine Frage pro Nachricht, „Frage X von Y“, Optionen a/b/c oder Beispielantworten, Empfehlung markiert. Gibt es ein Auswahl-Werkzeug (z. B. AskUserQuestion), nutze es. Sagt der Nutzer „mach einfach“: die empfohlene Option nehmen und oben sagen, welche.
