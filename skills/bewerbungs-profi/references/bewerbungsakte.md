# Die Bewerbungsakte (Gedächtnis zwischen Chats)

Ein neuer Chat weiß nichts vom alten. Im Free-Plan sind Nachrichten begrenzt (Reset etwa alle 5 Stunden). Darum führst du eine Datei **`Bewerbungsakte.md`**: Stand, Profil, Zielstelle, Status je Unterlage, nächste Schritte – plus die Daten für die Unterlagen als json-Block.

## Wann anlegen, wann aktualisieren

- **Anlegen**, sobald es um eine konkrete Stelle geht oder der Berufstest fertig ist:
  `python3 "$S/ordner_anlegen.py" --nur-akte "Firma" "Stelle" --name "Vorname Nachname"` → `/mnt/user-data/outputs/Bewerbungsakte.md`.
  (Mit lokalem Ordner legt `ordner_anlegen.py` die Akte im Bewerbungsordner an, siehe `werkzeuge.md`.)
- **Aktualisieren** nach jedem großen Schritt (Phase fertig), wenn der Nutzer aufhört („Danke, bis morgen“) oder wenn der Chat lang wird. Die Akte schreibst du direkt neu, immer unter dem gleichen Namen `Bewerbungsakte.md` (Ausnahme von „nie überschreiben“: so ist klar, welche die aktuelle ist; „Stand“ oben trägt das Datum).
- **Immer zum Download geben**, mit dem Satz:
  > „📁 Speicher dir die **Bewerbungsakte.md**. Beim nächsten Chat einfach hochladen und ‚Weiter mit meiner Bewerbung‘ schreiben – dann weiß ich alles wieder.“

## Aufbau (Pflichtteile)

1. Kopf: Name, **Stand** (Datum), **Phase** (Nummer + Name), **nächster Schritt**.
2. Ziel: Art, Stelle, Firma, Link, Kennziffer, Ansprechperson, Bewerbungsweg, Frist, Start, verlangte Unterlagen, Muss/Kann, Schlüsselwörter, erwartetes Auswahlverfahren.
3. Profil kurz: Stand, Stärken mit Beispiel, Motivation **in den Worten des Nutzers**, Warum diese Firma, Berufstest-Code.
4. Status der Unterlagen: Tabelle (Unterlage | Status: offen/Entwurf/fertig/abgeschickt | Datei | Offen, z. B. [PRÜFEN]-Punkte).
5. Gespräch: Termin/Art, STAR-Geschichten (je 1 Zeile), eigene Fragen, Feedback aus Übungen.
6. Alle Bewerbungen: Tracking-Tabelle (Firma | Stelle | abgeschickt | Status | Nachfassen am).
7. Entscheidungen mit Datum (z. B. „06.11.: Kurzanschreiben statt voll, weil optional“).
8. Nächste Schritte (nummeriert, max. 3).
9. **Daten für die Unterlagen** als ```json-Block (gleiches Format wie `unterlagen_erstellen.py --beispiel`). `unterlagen_erstellen.py Bewerbungsakte.md` liest den letzten json-Block direkt.

Die Vorlage erzeugt `ordner_anlegen.py`; halte dich an ihre Überschriften.

## Fortsetzung erkennen

Lädt der Nutzer eine `Bewerbungsakte.md` hoch:
1. Lesen, Phase und nächsten Schritt erkennen.
2. In **2 Zeilen** sagen, wo er steht: „Du bewirbst dich als Kauffrau für Büromanagement bei der Beispiel GmbH. Lebenslauf und Anschreiben sind fertig, abgeschickt am 10.11.“
3. Nächsten Schritt nennen und **direkt loslegen** (bzw. eine Frage stellen, falls eine Entscheidung nötig ist). Nicht alles neu fragen.
4. Sind seit dem Stand Fristen vergangen (Frist, Nachfass-Datum), das zuerst ansprechen.

## Datenschutz

Die Akte enthält persönliche Daten. Hinweis beim ersten Download (einmal): „Die Akte enthält deine Daten – speicher sie privat und teil sie nicht öffentlich.“ Keine Ausweis-, Steuer-, Sozialversicherungs- oder Kontonummern aufnehmen. Gibt es ein Claude-Projekt im Konto, kann der Nutzer die Akte dort als Projektdatei ablegen.
