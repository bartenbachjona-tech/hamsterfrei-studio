# Phase 3: Persönliche Fragen (Profil)

Ziel: alle Fakten für die Unterlagen **vom Nutzer**, in die Profil-JSON (`profil_json.md`). Eine Frage = ein Thema pro Nachricht. ~10 Fragen, damit die ganze Bewerbung in ~25 Nachrichten passt.

## Inhalt
1. Vorher: was schon da ist
2. Format und Zählung
3. Die Standardfragen
4. Anpassen nach Ziel
5. Nachfragen und Rückfragen
6. Abschluss: Profil bestätigen

---

## 1. Vorher: was schon da ist

- Alter Lebenslauf hochgeladen → `textlib.py … --info`, Daten in die JSON, dann **eine** Frage: „Ich habe übernommen: … (3–5 Zeilen). Stimmt das noch, und was ist neu?“ Fragen 1–4 entfallen meist.
- Akte vorhanden → JSON nehmen, nichts doppelt fragen.
- Anzeige sagt schon etwas (z. B. Start 01.09.) → nicht fragen, nur bestätigen lassen, wenn es den Nutzer betrifft.
- Zeugnisse müssen nicht hochgeladen werden (außer für die Gesamt-PDF). Nie nach Ausweis, Steuer-ID, SV- oder Kontonummer fragen.

Einmal sagen: „Jetzt kommen ca. 10 kurze Fragen. Stichworte reichen. ‚Weiß nicht‘ ist okay.“ (Wer will, bekommt sie als Liste auf einmal – höchstens 5 pro Nachricht.)

## 2. Format und Zählung

```
**Frage 4 von 10 – Kenntnisse**
Welche Sprachen und Programme kannst du – und wie gut?
Beispiele: „Englisch B1, Türkisch Muttersprache“ · „Excel Grundlagen, Canva“

➡️ Als Nächstes: noch 6 Fragen, dann baue ich deinen Lebenslauf.
👉 Du jetzt: Antworte in Stichworten.
```
- **Y** steht nach Frage 3 (Stationen) fest und ändert sich danach nicht. Kommt eine Lücke oder ein fehlendes Detail dazu: „**Nachfrage zu Frage 3** – …“ (zählt nicht als neue Nummer).
- Pro Nachricht **ein** Fragezeichen-Thema. Nicht anhängen: „Und hast du ein Foto?“.

## 3. Die Standardfragen

| Nr | Frage (ein Thema) | Beispiele | → JSON |
|---|---|---|---|
| 1 | **Kontaktdaten** als Block, so wie sie oben im Lebenslauf stehen sollen | „Lena Muster, Musterweg 1, 85049 Ingolstadt, 0151 …, lena.muster@…“ | person |
| 2 | **Schule/Abschluss**: höchster (oder laufender) mit Monat/Jahr, Schule | „Realschule Ingolstadt, Mittlere Reife 07/2026“ | profil.bildung |
| 3 | **Stationen**: Jobs, Praktika, Ehrenamt, Verein – je mit Monat/Jahr und was du dort gemacht hast | „Minijob Kasse seit 09/2025, abends abgerechnet“ | profil.stationen |
| 4 | **Kenntnisse**: Sprachen mit Niveau, Programme | „Englisch B1, Excel“ | profil.sprachen, edv |
| 5 | **Warum dieser Beruf?** ein echter Grund | „Ich mag Zahlen“ | motivation_beruf |
| 6 | **Warum diese Firma?** ein Grund oder Fakt | „nah dran“, „bilden viel aus“ | motivation_firma |
| 7 | **Ein Beispiel für [Soft Skill aus der Anzeige]**: was war los, was hast *du* getan, was kam raus? | „Schülerfirma, zu fünft Stand geplant, ich Kasse“ | profil.beispiele |
| 8 | **Ab wann kannst du anfangen?** (Minijob/Werkstudent: Tage/Stunden) | „ab 01.09.“, „Fr+Sa abends“ | rahmen.start/verfuegbarkeit |
| 9 | **Foto im Lebenslauf?** a) ja, habe eins b) nein (Empfohlen, wenn kein gutes vorhanden) | | rahmen.foto |
| 10 | **Hobbys/Freizeit**, die etwas über dich sagen | „Handballtrainerin U12“ | profil.hobbys |

Nur bei Bedarf (als eigene Frage, zählt in Y): **Note** (wenn die Anzeige sie verlangt oder sie gut ist) · **Lücke** > 3 Monate (erkennst du an den Daten) · **Führerschein** (nur wenn Anzeige/Beruf ihn braucht) · **Gehaltsvorstellung** (nur wenn verlangt) · **Wie bist du auf die Stelle aufmerksam geworden?** (nur wenn das Formular fragt – nie raten).

Zu Frage 9 (ein Satz): Foto ist freiwillig, seit dem AGG (2006) darf es niemand verlangen; wenn, dann professionell und aktuell. In AT/CH üblicher.

## 4. Anpassen nach Ziel

- **Ausbildung (Schüler):** Frage 2 mit Lieblingsfach (nur wenn passend); Frage 3 auch Schülerpraktikum, Verein, Schülerfirma, Familie.
- **Duales Studium:** Frage 2 mit Hochschulzugang (Abi/Fachabi). Bei Motivationsschreiben Frage 5 doppelt: Fach **und** Betrieb (zwei Fragen).
- **Praktikum/Werkstudent:** Frage 2 = Studiengang + Semester; Frage 8 = Zeitraum, Stunden/Woche, Pflicht- oder freiwilliges Praktikum (`sonderfaelle.md`).
- **Berufseinstieg/Jobwechsel:** Frage 3 mit Ergebnissen und Verantwortung (nur echte); zusätzlich **Wechselgrund** (sachlich). Keine Schulnoten-Fragen.
- **Minijob (≈ 6 Fragen):** 1 Kontakt · 2 Schule/Stand · 3 Erfahrung · 8 Verfügbarkeit · 5 Warum hier (ein Satz) · 10 Hobbys (optional). Frage 7 nur, wenn die Anzeige einen Soft Skill betont.
- **Ältere/erfahrene Bewerber:** `sonderfaelle.md` Abschnitt 5.

## 5. Nachfragen und Rückfragen

- **Rückfrage des Nutzers** („Was heißt B1?“): kurz beantworten, **dieselbe Frage noch einmal** stellen. Keine neue Frage anhängen.
- **„Weiß nicht“** bei 5/6: drei Denkanstöße als Optionen („a) Was hat dich an der Anzeige angesprochen? b) Was machst du gern, das dazu passt? c) Wen kennst du, der das macht?“) – die Antwort schreibt der Nutzer.
- **„Keine Erfahrung“:** nach Schule, Verein, Familie, Hobby, Nachbarschaftshilfe fragen.
- **Unklare Daten** (Monat, Niveau, Ergebnis): **eine** Nachfrage; sonst so lassen, wie gesagt („seit 2023“), oder [PRÜFEN: Monat?].
- **Übertreibungen bremsen:** aus „Kasse gemacht“ wird keine „Filialverantwortung“. Kurz begründen (Gespräch, § 123 BGB).
- **Gefälschtes** (Zeugnis, Abschluss, Referenz): freundlich ablehnen, Alternative nennen.

## 6. Abschluss: Profil bestätigen

Kurzprofil (max. 8 Zeilen: Stand, Stationen, Stärken mit Beispiel, Motivation, Start) und „Passt das? a) Ja, bau den Lebenslauf b) Ändern: …“. Bei Ja: Akte speichern (`akte.py`), dann Phase 4. Im Fahrplan ist hier oft das Ende von Chat 1.
