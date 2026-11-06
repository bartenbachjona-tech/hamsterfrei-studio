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
| Minijob | 3–5 Sätze in Mail/Formular oder WhatsApp (`whatsapp.text`, `abschicken.md` 5) |

Nur fragen, wenn die Anzeige es offenlässt (eine Frage, Empfehlung markieren). Entscheidung in `entscheidungen`.

## 2. Aufbau

1. **Betreff:** Stellentitel genau wie in der Anzeige, ggf. Kennziffer, Start.
2. **Anrede** persönlich; ohne Namen „Sehr geehrte Damen und Herren,“ oder „Guten Tag, liebes …-Team,“. AT: Titel (Mag., Dr.).
3. **Einstieg ohne Floskel:** stärkster Bezug aus dem Profil (`motivation_beruf`, ein `beispiel`, ein Telefonat).
4. **Belege statt Behauptungen:** 2–3 Anforderungen aus `ziel.muss`/`schluesselwoerter`, je ein Beispiel aus `profil.beispiele` – mit den Details, die der Nutzer genannt hat, nicht mehr.
5. **Warum diese Firma:** `motivation_firma` oder ein `firmenfakt` mit `zugestimmt: true`. Fehlt beides: eine Frage stellen – nicht raten, nicht [PRÜFEN] mit eigenem Vorschlag. Keine Kennenlern-Szenen erfinden („Wir haben uns am Stand kennengelernt“) – nur, was er erzählt hat.
6. **Rahmen nur, wenn verlangt:** Start, Gehalt (Spanne brutto/Jahr), bei Praktikum/Werkstudent Zeitraum, Stunden, Pflicht/freiwillig.
7. **Schluss ohne Konjunktiv:** „Ich freue mich auf ein persönliches Gespräch.“
8. Gruß, Name. **Anlagen-Zeile baut das Skript** aus `profil.anlagen` (nur vorhandene Dateien) – nicht von Hand schreiben. Zeugnisse darum **vor** dem Anschreiben einsammeln (Profil-Frage). Kommen sie später, zieht `pdf_zusammenfuegen.py --profil` die Zeile automatisch nach.
   **Kurzanschreiben: ohne Anlagen-Zeile** (es steht im Portal/in der Mail neben den Dateien). Erzwingen mit `anschreiben.anlagen_zeile: true`, unterdrücken beim vollen Anschreiben mit `false`.

## 3. Sprache: echt statt KI-glatt

Laut Stepstone (06/2025) finden 73 % der Recruiter KI-Bewerbungen weniger authentisch, 75 % sehen oft übertriebene Qualifikationen. Darum:
- Motivation, Gefühle, Eigenschaften, Häufigkeiten **nur aus dem Wortlaut** – jeder Satz bekommt beim Entwurf seinen `herkunft`-Eintrag (`profil_json.md` 5). Typische Erfindungen aus Tests: „täglich“, „lerne neue Programme schnell“, „passt zu mir“, „ist mir wichtig“, „finde ich spannend“ (wenn er es nicht sagte), „schwer tragen bin ich gewohnt“, „Privat habe ich …“, Gegenmaßnahmen zu Schwächen. Fehlt die Basis: **nicht schreiben, sondern fragen.**
- Gesundheit/Familie („wegen meines Knies“, „meine Kinder“) nur nach ausdrücklichem Ja (`privat_ok`) – und im Anschreiben im Regelfall gar nicht; besser sachlich nach vorn („Ich möchte ins Lager wechseln“).
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

Danach höchstens 1–2 Sätze, warum der Text so gebaut ist (nicht im Kurzpfad).

## 5. Zeigen, freigeben, EINMAL erzeugen

1. Absätze in `anschreiben.absaetze` (bzw. `formular`/`email`/`whatsapp`) **und** für jeden Satz über die Person den `herkunft`-Eintrag. Dann `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json --woher` → 0 ❌. ❌ „Satz ohne Quelle“/„Wörter ohne Quelle“ → Satz raus oder seine Worte nehmen; fehlt eine Info: **erst die Frage** (eigene Nachricht), dann der Entwurf.
2. **Im Chat zeigen** (Codeblock zum Kopieren) – **noch keine Datei**. Darunter die **Woher-Liste** aus der `--woher`-Ausgabe, kompakt (eine Zeile je Satz über die Person, Satzanfang → seine Worte):
   ```
   Woher:
   – „Seit September 2025 mache…“ → deine Worte: „seit 09/2025 … abrechnung selbst“ (Nr. 3)
   – „In der Schülerfirma haben wir…“ → deine Worte: „zu fünft einen verkaufsstand geplant“ (Nr. 7)
   – „In Ihrer Anzeige nennen Sie…“ → Anzeige: „Sorgfalt, Teamarbeit“
   ```
   Am Handy höchstens 6 Zeilen; bei mehr Sätzen die Liste als Codeblock. Dann: „Passt das so? a) Ja, PDF erstellen b) Ändern: …“ – **kein** Angebot und kein Chatwechsel in derselben Nachricht.
3. Nach dem Ja **einmal**: `python3 "$S/unterlagen_erstellen.py" /tmp/bewerbung/profil.json --nur anschreiben [--nur-pdf]` → `Anschreiben_…_AKTUELL.pdf` (bzw. `Motivationsschreiben_…`, `Kurzanschreiben_…`).
4. `fakten_check.py profil.json <Datei>` (Abgleich: Datei = freigegebener Text) + `endcheck.py <Datei> --typ anschreiben|kurzanschreiben|motivationsschreiben --profil profil.json`.
5. Formular-/Mail-/WhatsApp-Text genauso: erst im Chat, nach dem Ja `--nur formular` / `--nur email` / `--nur whatsapp` → `.txt`. Steht „max. N Zeichen“ (auch „1.000“) schon im Feldnamen, hängt das Skript es nicht doppelt an. Firmenname/Stellentitel sind dort **nicht** Pflicht – keine hölzernen Sätze einbauen.

## 6. Motivationsschreiben (Studium, duales Studium)

Gleiche Regeln; Schwerpunkt: Warum dieses Fach (`profil.motivation_fach`, wörtlich erfragt), was hat hingeführt (Schulfach, Projekt, Praktikum), was danach. Dual: Warum der Betrieb **und** warum das Fach (zwei Profil-Fragen). Vorgaben der Hochschule/des Betriebs (Länge, Leitfragen) gehen vor; Leitfragen, auf die er nichts gesagt hat, fragst du – nicht auffüllen.
