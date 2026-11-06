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

- Alter Lebenslauf hochgeladen → `textlib.py … --info`, Pfad in `profil.quellen` (sein Text gilt als Beleg), dann **eine** Frage: „Ich habe übernommen: … (3–5 Zeilen). Stimmt das noch, und was ist neu?“ Fragen 2–4 entfallen meist.
- Akte vorhanden → JSON nehmen, nichts doppelt fragen.
- Anzeige sagt schon etwas (z. B. Start 01.09.) → nicht fragen, nur bestätigen lassen, wenn es den Nutzer betrifft.
- Nie nach Ausweis, Steuer-ID, SV- oder Kontonummer fragen.

Einmal sagen: „Jetzt kommen ca. 10 kurze Fragen. Stichworte reichen. ‚Weiß nicht‘ ist okay.“ (Wer will, bekommt sie als Liste auf einmal – höchstens 5 pro Nachricht.)

## 2. Format und Zählung

```
**Frage 4 von 10 – Kenntnisse**
Welche Sprachen und Programme kannst du – und wie gut?
Beispiele: „Englisch B1, Türkisch Muttersprache“ · „Excel Grundlagen, Canva“

➡️ Als Nächstes: noch 6 Fragen, dann baue ich deinen Lebenslauf.
👉 Du jetzt: Antworte in Stichworten.
```
**Zählregel (fest):**
- **Y steht ab der ersten Profilfrage** fest: Plane die Fragen vorher (Standardliste + Anpassungen aus Abschnitt 4) und speichere Y in `meta.fragen_gesamt`. Vor Frage 1 gibt es keine Zählung.
- **Schon beantwortet** (Upload, Akte, Nebenbei-Antwort)? Frage überspringen, **Y um 1 senken** und es in einem Halbsatz sagen: „(Frage 6 entfällt – hast du schon gesagt; jetzt 9 Fragen.)“ Die Nummern laufen ohne Lücke weiter.
- **Nachfragen** (Lücke, fehlender Monat, unklares Niveau) tragen die Nummer der Ausgangsfrage: „**Nachfrage zu Frage 3** – …“, zählen nicht.
- Kommt ein **neues Thema** dazu (z. B. Lücke erkannt, Wechselgrund nötig), wird es eine Nachfrage zur passenden Frage – Y ändert sich nicht.
- Pro Nachricht **ein** Anliegen. Nicht anhängen: „Und hast du ein Foto?“.
- **Jede Antwort sofort wörtlich in `profil.rohtext`**, dann in die Felder (`profil_json.md`).
- Akte nach ~6 Antworten (`meta.antworten_seit_akte`), ein Satz.

## 3. Die Standardfragen

| Nr | Frage (ein Thema) | Beispiele | → JSON |
|---|---|---|---|
| 1 | **Kontaktdaten** als Block (Name zuerst – dann heißt die Akte richtig) | „Lena Muster, Musterweg 1, 85049 Ingolstadt, 0151 …, lena.muster@…“ | person |
| 2 | **Schule/Abschluss**: höchster (oder laufender) mit Monat/Jahr, Schule | „Realschule Ingolstadt, Mittlere Reife 07/2026“ | profil.bildung |
| 3 | **Stationen**: Jobs, Praktika, Ehrenamt, Verein – je mit Monat/Jahr und was du gemacht hast | „Minijob Kasse seit 09/2025, abends abgerechnet“ | profil.stationen |
| 4 | **Kenntnisse**: Sprachen mit Niveau, Programme, Scheine/Zertifikate | „Englisch B1, Excel, Staplerschein“ | sprachen, edv, zertifikate |
| 5 | **Warum dieser Beruf?** ein echter Grund | „Ich mag Zahlen“ | motivation_beruf |
| 6 | **Warum diese Firma?** ein Grund | „nah dran“, „bilden viel aus“ | motivation_firma |
| 7 | **Ein Beispiel für [Soft Skill aus der Anzeige]**: was war los, was hast *du* getan, was kam raus? | „Schülerfirma, zu fünft Stand geplant, ich Kasse“ | profil.beispiele |
| 8 | **Ab wann kannst du anfangen?** (Minijob/Werkstudent: Tage/Stunden) | „ab 01.09.“, „Fr+Sa abends“ | rahmen |
| 9 | **Wie bist du auf die Stelle aufmerksam geworden?** (immer – Formulare fragen es oft, nie raten) | „Indeed“, „Karriereseite“, „Tipp von meiner Tante“ | wie_aufmerksam |
| 10 | **Zeugnisse jetzt hochladen** (die die Anzeige verlangt; Handy: Scan-App) – damit die Anlagen-Zeile gleich stimmt | „Zeugnis 10. Klasse“ | profil.anlagen |
| (11) | **Foto?** a) ja, habe eins b) nein · **Hobbys** – nur wenn sinnvoll, sonst weglassen | | rahmen.foto, hobbys |

Nur bei Bedarf (zählt in Y): **Note** (wenn verlangt oder gut) · **Lücke** > 3 Monate (als Nachfrage) · **Führerschein** (nur wenn Anzeige/Beruf ihn braucht) · **Gehaltsvorstellung** (nur wenn verlangt). Foto: freiwillig (AGG), in AT/CH üblicher.

## 4. Anpassen nach Ziel

- **Ausbildung (Schüler):** Frage 2 mit Lieblingsfach (nur wenn passend); Frage 3 auch Schülerpraktikum, Verein, Schülerfirma, Familie.
- **Duales Studium/Studium:** Frage 2 mit Hochschulzugang. Motivationsschreiben: Frage 5 doppelt – **Warum dieses Fach?** (`motivation_fach`) **und** Warum der Betrieb (zwei Fragen).
- **Praktikum/Werkstudent:** Frage 2 = Studiengang + Semester; Frage 8 = Zeitraum, Stunden/Woche **inkl. anderer Jobs**, Ende (spätestens mit der Exmatrikulation), Pflicht- oder freiwilliges Praktikum (`sonderfaelle.md`).
- **Berufseinstieg/Jobwechsel:** Frage 3 mit Ergebnissen und Verantwortung (nur echte); zusätzlich **Wechselgrund** (sachlich, `wechselgrund`). Keine Schulnoten-Fragen.
- **Studien-/Ausbildungsabbruch:** zusätzlich **Grund** in seinen Worten (`abbruch_grund`), sachlich, nach vorn.
- **Minijob (≈ 6 Fragen):** 1 Kontakt · 2 Schule/Stand · 3 Erfahrung · **4 Kenntnisse kurz** (Kasse, Sprachen, Führerschein nur wenn relevant – eine Frage) · 8 Verfügbarkeit · 6 Warum hier (ein Satz) · 9 Wie aufmerksam. Frage 7 nur, wenn die Anzeige einen Soft Skill betont.
- **Ältere/erfahrene Bewerber:** `sonderfaelle.md` Abschnitt 5.

## 5. Nachfragen und Rückfragen

- **Rückfrage des Nutzers** („Was heißt B1?“): kurz beantworten, **dieselbe Frage noch einmal** stellen. Keine neue Frage anhängen.
- **„Weiß nicht“** bei 5/6: drei Denkanstöße als Optionen („a) Was hat dich an der Anzeige angesprochen? b) Was machst du gern, das dazu passt? c) Wen kennst du, der das macht?“) – die Antwort schreibt der Nutzer.
- **„Keine Erfahrung“:** nach Schule, Verein, Familie, Hobby, Nachbarschaftshilfe fragen.
- **Unklare Daten** (Monat, Niveau, Ergebnis): **eine** Nachfrage mit **einem** konkreten Vorschlag („Juli 2024?“) – sonst so lassen, wie gesagt („seit 2023“), oder [PRÜFEN: Monat?]. Nie selbst einen Monat ergänzen.
- **Übertreibungen bremsen:** aus „Kasse gemacht“ wird keine „Filialverantwortung“. Kurz begründen (Gespräch, § 123 BGB).
- **Gefälschtes** (Zeugnis, Abschluss, Referenz): freundlich ablehnen, Alternative nennen.

## 6. Abschluss: Profil bestätigen

Kurzprofil (max. 8 Zeilen: Stand, Stationen, Stärken mit Beispiel, Motivation, Start) – **nur Dinge aus seinen Antworten** – und „Passt das? a) Ja, bau den Lebenslauf b) Ändern: …“. Bei Ja: Akte speichern (`akte.py`), dann Phase 4. Im Fahrplan ist hier oft das Ende von Chat 1.
