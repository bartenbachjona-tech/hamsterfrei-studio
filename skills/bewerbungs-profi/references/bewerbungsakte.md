# Die Bewerbungsakte (Gedächtnis zwischen Chats)

Ein neuer Chat weiß nichts vom alten, und im Free-Plan sind Nachrichten begrenzt (Reset etwa alle 5 Stunden). Darum gibt es die **Bewerbungsakte**: eine `.txt`-Datei, die `akte.py` aus der Profil-JSON schreibt – oben lesbar (Stand, Ziel, Berufstest, Profil inkl. Wechselgrund/Abbruchgrund/Zertifikate, Status, Gespräch, Bewerbungen, nächste Schritte und die Liste **„im neuen Chat wieder hochladen: …“**), unten die vollständigen Daten inkl. Wortlaut (`profil.rohtext`).

## Schreiben – automatisch und billig

```
python3 "$S/akte.py" /tmp/bewerbung/profil.json
```
→ `/mnt/user-data/outputs/Bewerbungsakte_Vorname_Nachname_JJJJ-MM-TT_HHMMSS.txt` (Sekunden + ggf. Laufnummer – zwei Akten in derselben Minute heißen verschieden). Ältere Akten wandern nach `alt/`. **Nur .txt** – eine PDF gibt es nur auf Wunsch (`--pdf` → `Akte-Lesefassung_…pdf`; die ist zum Lesen, nicht zum Hochladen). Vorher `meta.phase`, `meta.naechster_schritt`, `status`, `naechste_schritte` aktualisieren – nie die Akte von Hand schreiben.

**Wann:**
- **früh**, sobald der Name da ist (Profil-Frage 1) – nicht vorher, sonst heißt sie „Name“,
- nach **jeder Phase** (Steckbrief ok, Profil ok, Lebenslauf ok …),
- nach **~6 Nutzerantworten** innerhalb einer Phase (Zähler `meta.antworten_seit_akte`; `akte.py` setzt ihn zurück),
- **nicht mitten in Rollenspiel/Simulation/Übung** – dann direkt nach dem Feedback,
- wenn der Nutzer aufhört oder der Chat lang wird (~20 Nachrichten).

Sensible Details (Todesfall, Diagnose) stehen nie wörtlich in der Akte (`profil_json.md` 2).

Ein Satz reicht: „📁 Akte gespeichert: Bewerbungsakte_…_184012.txt – speichern, im neuen Chat einfach hochladen.“ Beim ersten Mal zusätzlich: „Sie enthält deine Daten – privat speichern, nicht teilen.“ Gibt das Skript „Im neuen Chat zusätzlich hochladen: …“ aus (Zeugnisse, Foto), sag das einmal, wenn du einen neuen Chat empfiehlst.

## Fahrplan in Chats (Free-Plan)

| Weg | Chat 1 | Chat 2 | Chat 3 |
|---|---|---|---|
| Stelle vorhanden | Stelle + Profil | Lebenslauf, Anschreiben, Abschicken | Gespräch/AC üben |
| Ohne Plan | Berufstest + Stelle finden | Profil + Unterlagen | Abschicken + Gespräch |
| Einladung da | Bestätigen + Übersicht + Üben | (Runde 2 / AC-Übungen) | – |

`meta.chat_plan` speichern. **Chatwechsel-Hinweis höchstens einmal** pro Chat, an einer echten Etappen-Grenze (z. B. nach dem Profil) – **nie kurz vor einem Ziel** (wenn die Unterlagen in 2–3 Nachrichten fertig wären: erst fertig machen) und nie in derselben Nachricht wie eine Freigabe-Frage. Text: „Starte jetzt einen neuen Chat, lade die Akte (.txt) hoch und schreib ‚Weiter mit meiner Bewerbung‘.“ Minijob/Probearbeiten: in der Regel **ein** Chat, kein Wechsel.

## Fortsetzung

1. `python3 "$S/akte.py" --lesen /mnt/user-data/uploads` (Ordner genügt) → nimmt die neueste Akte, auch umbenannt („Bewerbungsakte (1).txt“), schreibt `/tmp/bewerbung/profil.json` und ordnet Anlagen/Foto unter den neuen Uploads zu – auch, wenn das Handy sie umbenannt hat („image(1).jpg“: gleicher Inhalt; „IMG_2041 (1).jpg“). Bei 🔗 „zugeordnet“ kurz bestätigen lassen. Was fehlt („📎 …“), erst anfordern, **wenn es gebraucht wird** (Gesamt-PDF, Lebenslauf mit Foto) – nicht für die Gesprächsvorbereitung.
2. Eine `Akte-Lesefassung_…pdf` hilft nicht (keine Daten) – um die `.txt` bitten.
3. In **2 Zeilen** sagen, wo er steht; nächsten Schritt nennen und **direkt loslegen**.
4. Fristen oder Nachfass-Daten vorbei? Das zuerst ansprechen.
5. Alte Akte (v1/v2 ohne Wortlaut): fehlende Fakten **nachfragen**, nicht aus alten Texten ableiten; neue Antworten in `profil.rohtext`. Akte aus v3: vor der nächsten Freigabe `herkunft` für die Texte anlegen.

## Datenschutz

Keine Ausweis-, Steuer-, Sozialversicherungs- oder Kontonummern aufnehmen. Gibt es ein Claude-Projekt, kann der Nutzer die Akte dort als Projektdatei ablegen.
