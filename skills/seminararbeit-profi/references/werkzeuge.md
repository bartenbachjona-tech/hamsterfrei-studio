# Werkzeuge, Ordner und kostenloses Claude

Der Skill funktioniert **mit dem kostenlosen Claude.** Voraussetzung ist, dass in den Einstellungen „Code-Ausführung und Dateierstellung“ bzw. „Dateien erstellen und bearbeiten“ eingeschaltet ist. Alles Weitere ist optional und wird nur genutzt, wenn es da ist. Prüfe still, welche Werkzeuge verfügbar sind, und sag dem Nutzer nur, was für ihn relevant ist.

| Funktion | Kostenloses Claude | Mit Extras |
|---|---|---|
| Arbeit lesen, prüfen, verbessern | ✅ Datei hochladen | – |
| Formalia-, Plagiats-, Stil-Check | ✅ Skripte | – |
| Neue Word-Fassung, Grafiken, Beleg-PDFs | ✅ zum Download | direkt im Ordner (Desktop-App) |
| Quellen suchen | ✅ wenn Websuche an ist; sonst lädt der Nutzer Quellen hoch | – |
| Screenshots als Belege | ✅ Nutzer macht sie, Claude baut die Beleg-PDF | automatisch über Browser-Werkzeug |
| Ordner bearbeiten | ✅ fertiger Ordner als ZIP | direkt im Ordner auf dem Rechner |
| Prüfungsgespräch üben | ✅ Text; Sprachmodus, falls die App ihn bietet | – |
| Gedächtnis zwischen Chats | ✅ `Arbeitsstand.md` hochladen | Claude-Projekt mit Dateien |

## Der Seminararbeit-Ordner

Beim Start legst du ihn an:

```
python scripts/ordner_anlegen.py Seminararbeit "<Thema>" "<Abgabedatum>" [hochgeladene Dateien …]
```

Die Dateien werden einsortiert, und der Ordner kommt als ZIP zum Download.

```
Seminararbeit/
├── Arbeitsstand.md            ← bei jedem neuen Chat hochladen
├── 01_Arbeit/                 ← aktuelle Fassung, Sicherungen/
├── 02_Vorgaben/               ← Merkblatt, Bewertungsbogen, Korrektur-Fotos
├── 03_Quellen/                ← PDFs, Texte (für den Plagiats-Check)
├── 04_Belege/                 ← belege.csv, Screenshots/, Beleg-PDFs mit Datum
├── 05_Checks/                 ← Formalia-, Stil-, Plagiats-, Endcheck-Berichte mit Datum
└── 06_Pruefungsgespraech/     ← Landkarte, Fragenkatalog, Kurzvortrag, Probe-Protokolle
```

**Ohne Ordnerzugriff (Standard):** Du gibst jede neue oder geänderte Datei zum Download, mit Zielordner. Ein Beispiel: „Speichere das in 05_Checks.“ Nach größeren Schritten gibst du optional den ganzen Ordner neu als ZIP aus.

**Mit Ordnerzugriff** (Desktop-App mit verbundenem Ordner):
- Arbeite direkt dort.
- Vor dem Überschreiben vergleichen, ob der Nutzer die Datei inzwischen selbst geändert hat. Wenn ja, erst zusammenführen.
- Immer eine Sicherung nach `01_Arbeit/Sicherungen` legen.
- Ist eine Datei in Word geöffnet, wird das Speichern blockiert. Den Nutzer dann bitten, Word zu schließen.
- Nicht löschen. Alte Fassungen bleiben, der Nutzer räumt selbst auf.

## Nachrichtenlimit und lange Chats

Beim kostenlosen Claude sind die Nachrichten begrenzt, und sehr lange Chats werden langsam. Darum:
- **Ein Chat pro großem Schritt,** zum Beispiel Kapitel 3 überarbeiten, Endcheck oder Probe-Prüfung.
- Am Ende jedes Schritts `Arbeitsstand.md` aktualisieren und zum Download geben.
- Große Dateien nicht mehrfach in den Chat kopieren. Mit den Skripten arbeiten und nur die Ergebnisse zeigen.
- Gibt es Claude-Projekte im Konto, dann ein Projekt „Seminararbeit“ empfehlen, mit Merkblatt, Arbeitsstand und aktueller Fassung als Projektdateien.

## Rückfragen-Stil

- Höchstens 5 Fragen auf einmal, nummeriert, mit Optionen und Empfehlung.
- Erst prüfen, ob die Antwort schon in den Dateien steht.
- Gibt es ein Werkzeug für Auswahlfragen, nutze es.
- Ist der Nutzer nicht erreichbar oder sagt „mach einfach“: die empfohlene Option nehmen und oben in der Antwort sagen, welche.
