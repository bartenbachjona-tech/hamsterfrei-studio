# Endcheck vor der Abgabe (Modus 9)

Der Endcheck ist eine **Diagnose.** Erst prüfen, dann eine priorisierte Liste zeigen, dann nach Freigabe abarbeiten. Bei Zeitdruck gehen Plagiatsrisiken vor Belegen, Belege vor Formalia und Formalia vor Stil.

## 1. Plagiats-Selbstcheck

Der Nutzer lädt die Quellen hoch, die er als Datei hat (PDF, Text, gespeicherte Webseiten). Die Ergebnisse kommen nach `03_Quellen`.

```
python scripts/plagiat_check.py Arbeit.docx 03_Quellen/ > 05_Checks/Plagiat_<Datum>.md
```

Der Check findet:
- **wortgleiche Passagen** ab 7 Wörtern **ohne** Anführungszeichen. Sie müssen entweder als Zitat in „…“ stehen (Fußnote ohne „Vgl.“) oder neu formuliert werden (mit „Vgl.“).
- **zu nah formulierte Sätze,** also umgestellte Wörter mit gleicher Struktur. Diese Sätze mit eigenem Satzbau neu schreiben, der Beleg bleibt.
- **korrekt markierte Zitate,** bei denen der Wortlaut zur Quelle passt.

Zusätzlich prüfen:
- Hat jede Aussage mit Zahl oder fremdem Gedanken eine Fußnote? Steht bei jeder Paraphrase ein „Vgl.“?
- Stimmt jedes wörtliche Zitat Zeichen für Zeichen mit der Quelle überein?
- Ist das Literaturverzeichnis deckungsgleich mit den Fußnoten? (`formalia_check.py`)

**Grenze, ehrlich gesagt:** Der Check vergleicht nur mit den Quellen, die vorliegen. Eine Datenbank wie Turnitin gibt es hier nicht. Will der Nutzer zusätzlich einen externen Plagiatsprüfer nutzen, meldet er sich dort selbst an. Ergebnisse solcher Dienste sind Hinweise und keine Urteile. Treffer bei Allgemeinwissen, Fachbegriffen oder korrekt zitierten Stellen sind normal.

## 2. Stil-Check

```
python scripts/stilcheck.py Arbeit.docx [--vergleich eigener_alter_text.docx] > 05_Checks/Stil_<Datum>.md
```

Der Check zeigt:
- Floskeln
- Wertungen außerhalb des Fazits
- Meta-Sätze
- Leerformeln
- sehr lange Sätze
- die Schwankung der Satzlängen

Mit `--vergleich` nimmt er einen eigenen, nachweislich selbst geschriebenen Text als Maßstab, zum Beispiel ein altes Referat.

Wichtig für die Kommunikation:
- **Kein Werkzeug kann sicher erkennen, ob ein Text von einer KI stammt.** KI-Detektoren irren oft, besonders bei sachlichen deutschen Texten. Selbst Texte von vor 2020 werden teils als „KI“ markiert.
- Nutzt der Nutzer einen Detektor (er loggt sich selbst ein): immer eine **Gegenprobe** mit einem eigenen, alten Text oder einem Lexikontext von vor 2020 machen und beide Ergebnisse dokumentieren.
- Der Sinn dieses Checks ist ein **sachlicher, eigener Stil**, denn Floskeln und Wertungen kosten Punkte. Es geht nicht darum, verbotene KI-Nutzung zu verschleiern. Ist die KI-Nutzung erlaubt und kennzeichnungspflichtig, wird sie gekennzeichnet.
- Überarbeiten heißt: nur so viel ändern, wie nötig ist, und **inhaltlich nichts.**
- Die beste Absicherung bleibt:
  - erlaubte und ehrlich angegebene KI-Nutzung
  - jede Aussage belegt
  - der Nutzer kann alles im Prüfungsgespräch erklären → Modus 10

Liegen **keine Quellen** vor, gibt es keinen Plagiats-Check. Dann klar sagen: „Plagiats-Check nicht gemacht – keine Quellen hochgeladen.“ Nie ein ✅ ohne Prüfung.

## 3. Formalia-Check

`python scripts/formalia_check.py Arbeit.docx …` (Einstellungen siehe `formalia.md`). Danach rendern und die Seiten ansehen.

## 4. Inhalt-Check (selbst lesen)

- Wird die Forschungsfrage im Fazit **ausdrücklich** beantwortet?
- Zahlt jedes Kapitel erkennbar auf die Frage ein? Sind die Schwerpunkte richtig gewichtet?
- Stehen Wertungen nur im Fazit? Steht im Hauptteil kein Allgemeinplatz, wo eine Zahl stehen könnte?
- Werden Gegenpositionen oder Grenzen genannt?
- Gibt es zu jeder Grafik einen Verweis im Text? Sind die Grafiken auf Deutsch, beschriftet und mit Quelle versehen?

## 5. Ergebnis

Eine Datei `05_Checks/Endcheck_<Datum>.md` und eine Zusammenfassung im Chat:

```
Endcheck – Stand <Datum>
🔴 Muss vor Abgabe: … (Anzahl, mit Fundstellen)
🟡 Sollte: …
🟢 Passt: …
Vorschlag: Ich behebe jetzt 🔴 1–4 automatisch (nur Formales), für 5–6 brauche ich deine Entscheidung. Okay?
```

## Checkliste vor der Abgabe

- [ ] Deckblatt der Schule mit allen Daten
- [ ] Inhaltsverzeichnis aktualisiert (F9) und Seitenzahlen stimmen
- [ ] Umfang laut Vorgabe
- [ ] Formalia: Schrift, Zeilenabstand, Blocksatz und Silbentrennung, Ränder, Seitenzahlen, Fußnotengröße
- [ ] Jede Abbildung nummeriert, im Text erwähnt, mit Quelle in der Fußnote
- [ ] Fußnoten einheitlich: Punkt am Ende, „Vgl.“ richtig, ebd.-Ketten, Stellung des Zeichens
- [ ] Zitate wörtlich geprüft
- [ ] Literaturverzeichnis vollständig, alphabetisch, mit Abrufdaten, deckungsgleich mit den Fußnoten
- [ ] Quellenbelege aktuell (PDF und Ordner), für die Abgabe vorbereitet
- [ ] Plagiats- und Stil-Check dokumentiert
- [ ] KI-Nutzung so angegeben, wie es die Lehrkraft verlangt. **Die Erklärung passt zur tatsächlichen Nutzung**, also kein „ohne fremde Hilfe“, wenn KI benutzt wurde und die Lehrkraft eine Angabe verlangt.
- [ ] Erklärung als letzte nummerierte Seite, unterschrieben
- [ ] Sicherung der Endfassung und PDF zum Drucken
- [ ] Prüfungsgespräch vorbereitet (Modus 10)
