# Phase 5: Anschreiben / Kurzanschreiben / Motivationsschreiben

## Inhalt
1. Variante wählen
2. Aufbau
3. Sprache: echt statt KI-glatt
4. Beispiel schlecht → gut
5. Erzeugen, prüfen, zeigen
6. Motivationsschreiben

---

## 1. Variante wählen (`anschreiben.typ`, `ziel.anschreiben_variante`)

Laut Stepstone (700 Recruiter, 07/2025) verlangen 55 % der Unternehmen ein Anschreiben, nur 34 % halten es für entscheidend.

| Situation | `typ` |
|---|---|
| verlangt; Ausbildung, duales Studium, öffentlicher Dienst; Schweiz | `anschreiben` – max. 1 Seite, 3–4 Absätze |
| optional | `kurzanschreiben` (150–200 Wörter) oder 3–5 Sätze im Formular-/Mailfeld (`formular`/`email`) |
| Hochschule/dual verlangt „Motivationsschreiben“ | `motivationsschreiben` (Dateiname heißt dann so) |
| „ohne Anschreiben“ | keins – Risiko nennen, wenn der Nutzer eins will; er entscheidet |
| Minijob | 3–5 Sätze in Mail/Formular (oder WhatsApp, `sonderfaelle.md`) |

Nur fragen, wenn die Anzeige es offenlässt (eine Frage, Empfehlung markieren). Entscheidung in `entscheidungen`.

## 2. Aufbau

1. **Betreff:** Stellentitel genau wie in der Anzeige, ggf. Kennziffer, Start.
2. **Anrede** persönlich; ohne Namen „Sehr geehrte Damen und Herren,“ oder „Guten Tag, liebes …-Team,“. AT: Titel (Mag., Dr.).
3. **Einstieg ohne Floskel:** stärkster Bezug aus dem Profil (`motivation_beruf`, ein `beispiel`, ein Telefonat).
4. **Belege statt Behauptungen:** 2–3 Anforderungen aus `ziel.muss`/`schluesselwoerter`, je ein Beispiel aus `profil.beispiele` – mit den Details, die der Nutzer genannt hat, nicht mehr.
5. **Warum diese Firma:** `motivation_firma` oder ein `firmenfakt` mit `zugestimmt: true`. Fehlt beides: eine Frage stellen – nicht raten, nicht [PRÜFEN] mit eigenem Vorschlag.
6. **Rahmen nur, wenn verlangt:** Start, Gehalt (Spanne brutto/Jahr), bei Praktikum/Werkstudent Zeitraum, Stunden, Pflicht/freiwillig.
7. **Schluss ohne Konjunktiv:** „Ich freue mich auf ein persönliches Gespräch.“
8. Gruß, Name. **Anlagen-Zeile baut das Skript** aus `profil.anlagen` (nur vorhandene Dateien) – nicht von Hand schreiben. Zeugnisse darum **vor** dem Anschreiben einsammeln (Profil-Frage). Kommen sie später, zieht `pdf_zusammenfuegen.py --profil` die Zeile automatisch nach.
   **Kurzanschreiben: ohne Anlagen-Zeile** (es steht im Portal/in der Mail neben den Dateien). Erzwingen mit `anschreiben.anlagen_zeile: true`, unterdrücken beim vollen Anschreiben mit `false`.

## 3. Sprache: echt statt KI-glatt

Laut Stepstone (06/2025) finden 73 % der Recruiter KI-Bewerbungen weniger authentisch, 75 % sehen oft übertriebene Qualifikationen. Darum:
- Motivation, Gefühle und Eigenschaften **nur aus dem Wortlaut** (`profil.rohtext`). Keine Sätze wie „Genau so möchte ich arbeiten“, „macht mir mehr Spaß als alles andere“, „Reisen ist kein Problem“, „ich bin sehr zuverlässig“, wenn er das nicht gesagt hat. Fehlt die Basis: **nicht schreiben, sondern fragen.**
- Sprache des Nutzers (Alter, Bildungsweg). Verboten: „hiermit bewerbe ich mich“, „mit großem Interesse“, „würde mich freuen“, „teamfähig, belastbar und flexibel“, Dreier-Ketten.
- Nach dem Entwurf: „Kannst du zu jedem Satz eine kleine Geschichte erzählen?“

## 4. Beispiel schlecht → gut

**Schlecht:**
> hiermit bewerbe ich mich mit großem Interesse um einen Ausbildungsplatz in Ihrem renommierten Unternehmen. Ich bin teamfähig, belastbar und flexibel. Über eine Einladung würde ich mich sehr freuen.

**Gut** (jeder Satz steht so im Profil – Kasse seit 09/2025, Praktikum Steuerbüro, Schülerfirma mit 4 Mitschülern, Firmenfakt zugestimmt):
> Sehr geehrte Frau Sommer,
> seit September 2025 mache ich an der Kasse eines Supermarkts die Abrechnung am Schichtende selbst. Dabei habe ich gemerkt, wie gern ich Zahlen sauber abschließe.
> In Ihrer Anzeige nennen Sie Sorgfalt und Teamarbeit. Im Praktikum im Steuerbüro habe ich Belege sortiert und erfasst. In der Schülerfirma haben wir zu fünft einen Verkaufsstand geplant; ich habe die Kasse übernommen.
> Mich spricht an, dass Azubis bei Ihnen eigene Projekte betreuen.
> Ich freue mich auf ein persönliches Gespräch.

Der Firmen-Satz steht nur drin, weil die Nutzerin vorher gefragt wurde: „Laut Ihrer Karriereseite (beispiel.de/karriere) betreuen Azubis eigene Projekte – soll das rein?“ → Ja.

Danach in 2–3 Sätzen erklären, warum der Text so gebaut ist.

## 5. Zeigen, freigeben, EINMAL erzeugen

1. Absätze in `anschreiben.absaetze` (bzw. `formular`/`email`), dann `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json --woher` → 0 ❌; ⚠️ „Motivation/Eigenschaft ohne Wortlaut“ → Satz raus, als Frage stellen.
2. **Im Chat zeigen** (Computer: im Codeblock zum Kopieren) – **noch keine Datei**. Darunter die **Woher-Liste** (max. 5 Zeilen, aus der `--woher`-Ausgabe, in einfachen Worten):
   ```
   So habe ich deine Antworten verwendet:
   – „Die Abrechnung macht mir Spaß …“ ↔ deine Antwort 5: „die Abrechnung macht mir Spaß“
   – „zu fünft einen Verkaufsstand geplant“ ↔ Antwort 7
   ```
   Dann: „Klingt das nach dir? a) Ja, Datei erstellen b) Ändern: … c) lockerer/förmlicher“.
3. Nach dem Ja **einmal**: `python3 "$S/unterlagen_erstellen.py" /tmp/bewerbung/profil.json --nur anschreiben [--nur-pdf]` → `Anschreiben_…_AKTUELL.pdf` (bzw. `Motivationsschreiben_…`, `Kurzanschreiben_…`).
4. `fakten_check.py profil.json <Datei>` (Abgleich: Datei = freigegebener Text) + `endcheck.py <Datei> --typ anschreiben|kurzanschreiben|motivationsschreiben --profil profil.json`.
5. Formular-/Mailtext genauso: erst im Chat (Handy: Feld für Feld), nach dem Ja `--nur formular` bzw. `--nur email` → `.txt`. Steht „max. N Zeichen“ schon im Feldnamen, hängt das Skript es nicht doppelt an. Firmenname/Stellentitel sind in Formularfeldern und Mail **nicht** Pflicht – keine hölzernen Sätze einbauen, freigegebene Texte nicht für den Endcheck umschreiben.

## 6. Motivationsschreiben (Studium, duales Studium)

Gleiche Regeln; Schwerpunkt: Warum dieses Fach (`profil.motivation_fach`, wörtlich erfragt), was hat hingeführt (Schulfach, Projekt, Praktikum), was danach. Dual: Warum der Betrieb **und** warum das Fach (zwei Profil-Fragen). Vorgaben der Hochschule/des Betriebs (Länge, Leitfragen) gehen vor; Leitfragen, auf die er nichts gesagt hat, fragst du – nicht auffüllen.
