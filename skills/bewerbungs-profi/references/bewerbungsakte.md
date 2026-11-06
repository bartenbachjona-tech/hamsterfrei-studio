# Die Bewerbungsakte (Gedächtnis zwischen Chats)

Ein neuer Chat weiß nichts vom alten, und im Free-Plan sind Nachrichten begrenzt (Reset etwa alle 5 Stunden). Darum gibt es die **Bewerbungsakte**: eine `.txt`-Datei, die `akte.py` aus der Profil-JSON schreibt – oben lesbar (Stand, Ziel, Profil, Status, Gespräch, Bewerbungen, Entscheidungen, nächste Schritte), unten die vollständigen Daten zum Fortsetzen.

## Schreiben – automatisch und billig

```
python3 "$S/akte.py" /tmp/bewerbung/profil.json          (Handy: --pdf dazu, dann gibt es auch eine lesbare PDF)
```
→ `/mnt/user-data/outputs/Bewerbungsakte_Vorname_Nachname_JJJJ-MM-TT_HHMM.txt`. Ältere Akten im Ausgabeordner wandern nach `alt/`. Vorher `meta.phase`, `meta.naechster_schritt`, `status`, `naechste_schritte` in der JSON aktualisieren – nie die Akte von Hand schreiben.

**Wann:**
- nach **jeder Phase** (Steckbrief ok, Profil ok, Lebenslauf ok …),
- **spätestens nach ~6 Nutzerantworten** innerhalb einer Phase (Profil-Fragen, STAR-Geschichten, Übungen),
- wenn der Nutzer aufhört („danke, bis morgen“) oder der Chat lang wird.

Ein Satz reicht: „📁 Akte aktualisiert: Bewerbungsakte_…_1840.txt – speichern, im neuen Chat einfach hochladen.“ Beim ersten Mal zusätzlich: „Sie enthält deine Daten – privat speichern, nicht teilen.“

## Fahrplan in Chats (Free-Plan)

| Weg | Chat 1 | Chat 2 | Chat 3 |
|---|---|---|---|
| Stelle vorhanden | Stelle + Profil | Lebenslauf, Anschreiben, Abschicken | Gespräch/AC üben |
| Ohne Plan | Berufstest + Stelle finden | Profil + Unterlagen | Abschicken + Gespräch |
| Einladung da | Übersicht + Üben | (Runde 2 / AC-Übungen) | – |

`meta.chat_plan` speichern. An jeder Etappen-Grenze und wenn eine Phase lang wird (~20 Nachrichten im Chat): Akte speichern und **neuen Chat empfehlen**: „Starte jetzt einen neuen Chat, lade die Akte hoch und schreib ‚Weiter mit meiner Bewerbung‘. So läufst du nicht ins Nachrichtenlimit.“

## Fortsetzung

Lädt der Nutzer eine Akte hoch (`.txt`, PDF hilft nicht – die Daten stehen nur in der `.txt`; alte `.md` geht auch):
1. `python3 "$S/akte.py" --lesen /mnt/user-data/uploads/<Akte>` → schreibt `/tmp/bewerbung/profil.json` und zeigt Stand/Phase/nächsten Schritt.
2. Mehrere Akten hochgeladen? Die mit dem jüngsten Datum im Namen bzw. „Stand“ nehmen und kurz sagen, welche.
3. In **2 Zeilen** sagen, wo er steht; nächsten Schritt nennen und **direkt loslegen** (nicht alles neu fragen).
4. Fristen oder Nachfass-Daten vorbei? Das zuerst ansprechen.
5. Alte Akte (v1, ohne `profil`): fehlende Profil-Felder **nachfragen**, nicht aus den alten Texten ableiten.

## Datenschutz

Keine Ausweis-, Steuer-, Sozialversicherungs- oder Kontonummern aufnehmen. Gibt es ein Claude-Projekt, kann der Nutzer die Akte dort als Projektdatei ablegen.
