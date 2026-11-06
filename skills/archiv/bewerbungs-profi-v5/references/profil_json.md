# Die Profil-JSON (Quelle aller Fakten) – v5: Fakten wörtlich, Formulierung frei

## Inhalt
1. Grundregel: Wortlaut zuerst
2. rohtext, Bestätigungen, unsichere und sensible Antworten
3. Aufbau
4. Wie du Felder füllst (Normalisierungs-Wörterbuch)
5. Satz-Herkunft (`herkunft`)
6. Von der JSON zu den Unterlagen
7. fakten_check: Treffer behandeln

---

## 1. Grundregel: Wortlaut zuerst

Jede Antwort des Nutzers kommt **sofort und wörtlich** in `profil.rohtext` – dann erst in die Felder. `fakten_check.py` prüft die Unterlagen gegen
- den **Wortlaut** (`profil.rohtext`),
- die **Anzeige** (`ziel.anzeige_text`), die **Einladung** (`gespraech.einladung_text`), zugestimmte **Firmenfakten**,
- **Uploads mit Text** (`profil.anlagen[].datei`, `profil.quellen[]` – Zeugnisse, alter Lebenslauf; über textlib gelesen),
- `belege[]` mit wörtlichem Zitat, das den Wert trägt,
- und die **Satz-Herkunft** (`herkunft`, Abschnitt 5) für alle Freitexte.

**v5-Prinzip:** Jede *Behauptung* (Zahl, Datum, Dauer, Name, Abschluss/Niveau, Tätigkeit/Fähigkeit, Häufigkeit/Intensität, Gefühl/Motiv, Kontakt zur Firma) kommt vom Nutzer. Die *Formulierung* ist frei und muss sauberes Standarddeutsch sein: „seh ich“ → „sehe ich“, „nix“ → „nichts“, „ubahn“ → „U-Bahn“, „Kumpel“ → „ein Bekannter“, „Sa und So“ → „samstags und sonntags“, „bescheid sagen“ → „informieren“, „leute“ → „Kundinnen und Kunden“, Tippfehler korrigieren. Das Skript erkennt diese Umformungen (Lemma, Wörterbuch, Tippfehler-Toleranz) – du brauchst dafür keine Rückfrage und keine `belege`.

Im **Lebenslauf** zählt nur der Wortlaut (+ Uploads) – die Anzeige belegt nichts über die Person. **Nicht** gegen deine eigenen Profil-Felder. Was du dort „normalisierst“ (09/2018, Klasse B, B.A., 30 Std.), zählt nur, wenn es so im Wortlaut steht. Muster: `python3 "$S/unterlagen_erstellen.py" --beispiel`. Neue Sitzung ohne JSON: Muster anlegen (`mkdir -p /tmp/bewerbung`), alle Beispielwerte **leeren**.

## 2. rohtext, Bestätigungen, unsichere und sensible Antworten

```json
"rohtext": [
  {"nr": 1, "frage": "Frage 1 – Kontaktdaten", "antwort": "deniz arslan weinweg 14 93049 regensburg 0176 48213307 deniz.arslan07@gmail.com"},
  {"nr": 2, "frage": "Frage 2 – Schule", "antwort": "mittlere reife 2024 realschule am donaupark 2,8"},
  {"nr": 3, "frage": "Nachfrage zu Frage 2: Zeugnis im Juli 2024?", "antwort": "ja", "bestaetigt": "Juli 2024"}
]
```
- **Auswahlfragen** (a/b/c): die Optionen mitspeichern, dann zählt der Text der gewählten Option automatisch (auch als Zitat): `{"frage": "Warum Brenner? a) Übernahme b) nah dran", "antwort": "a und b", "optionen": {"a": "Übernahme bei guten Leistungen", "b": "nah dran"}}`. Nicht gewählte Optionen zählen nie.
- **Wörtlich** übernehmen, auch Tippfehler/Kleinschreibung. Auch Nebenbei-Infos aus anderen Nachrichten (dann `"frage": "nebenbei"`).
- `bestaetigt` zählt, wenn die Antwort ein klares Ja ist („ja“, „genau“, „stimmt“, „👍“ – **und „a“, „1a“, „a passt“, wenn a) „Ja“ war**) und die Teile des Werts in deiner Frage standen (Reihenfolge egal: „Deutsch Muttersprache“ ↔ „Deutsch ist deine Muttersprache?“). Mehrere Werte als Liste: `"bestaetigt": ["Juli 2025", "Juli 2023"]`. **Bestätigte Werte gelten überall** – in fakten_check und in jedem `herkunft`-Satz (Zitat = der Wert). Frag mit konkreten Werten („im Juli 2024?“), nicht „meist September“.
- **Abgeleitete Zeitangaben** („letztes Jahr“, „letzten Sommer“ → 2025/2026) sind nur ⚠️ – einmal mit dem Jahr bestätigen lassen, dann `bestaetigt`.
- **Unsichere Antworten** („b2 glaub ich“, „ja glaub schon“, „oder so“): `fakten_check` meldet ℹ️, `herkunft` ⚠️. Eine Ja/Nein-Rückfrage, Antwort als neuer Eintrag, beim alten `"geklaert": true`.
- **Schickt der Nutzer dein Beispiel zurück** („Excel gut, SAP MM, Englisch B2“ – genau wie in deiner Frage): wie unsicher behandeln, kurz bestätigen lassen.
- **Sensibles** (Todesfall, Diagnose, Trennung): nicht wörtlich speichern. `{"nr": 9, "frage": "…", "antwort": "familiärer Grund (Details nicht gespeichert)", "sensibel": true}` – zählt nie als Beleg.
- Uploads (alter Lebenslauf, Zeugnis als PDF) in `profil.quellen` bzw. `profil.anlagen` – ihr Text zählt als Beleg. Bilder/Scans zählen nicht automatisch: was du darauf liest, bestätigt der Nutzer (eine Frage) → rohtext.
- Alte Akte (v2) ohne rohtext: fakten_check warnt „Kein Wortlaut“ und prüft hilfsweise gegen die Felder. Neue Antworten trotzdem in rohtext.

## 3. Aufbau

| Bereich | Inhalt | Wer schreibt |
|---|---|---|
| `meta` | stand, phase, naechster_schritt, geraet, anrede_form, modus (normal/schnell), chat_plan, **fragen_gesamt** (Y), **antworten_seit_akte**, **offene_aenderungen[{text, unterlage, erledigt}]** | du |
| `person` | name, strasse, plz_ort, telefon, email, linkedin (nur wenn genannt), geburtsdatum (nur auf Wunsch), foto (Pfad) | Wortlaut |
| `ziel` | art, stelle (genau wie in der Anzeige), firma, kennziffer, ansprechperson, anrede, firma_adresse, link, bewerbungsweg (inkl. WhatsApp/Portal), frist, start, unterlagen_verlangt, upload_limit, muss, kann, schluesselwoerter, auswahlverfahren, anschreiben_variante, **anzeige_text** | Anzeige |
| `profil.rohtext[]` | alle Antworten im Wortlaut | Nutzer |
| `profil.bildung[]`, `stationen[]`, `luecken[]` | `stationen[{zeitraum, art (Minijob/Praktikum/Ehrenamt), titel (Tätigkeit), firma, ort, taetigkeiten[], ergebnisse[]}]` · `luecken[{zeitraum, bezeichnung, grund, im_lebenslauf}]` – `bezeichnung` („Bewerbungsphase“) kommt automatisch in den Lebenslauf, `grund` bleibt privat | aus dem Wortlaut |
| `profil.sprachen[]`, `edv[]`, `fuehrerschein`, **`zertifikate[]`** | Staplerschein, Ersthelfer, Sprachzertifikat → `zertifikate`, nicht unter Führerschein | Wortlaut |
| **`profil.wechselgrund`**, **`abbruch_grund`**, **`motivation_fach`**, `motivation_beruf`, `motivation_firma` | in seinen Worten, kurz | Wortlaut |
| `profil.beispiele[]` | thema, stichwort, situation, aufgabe, handlung, ergebnis (leer, wenn nicht gesagt) | Wortlaut |
| `profil.hobbys[]`, `rahmen{start, stunden, verfuegbarkeit, gehalt, foto}`, `wie_aufmerksam`, `sonstiges[]` | | Wortlaut |
| **`profil.berufstest`** | code, bereiche, vorschlaege[], gewaehlt | Skript + Nutzer |
| `profil.anlagen[]`, **`profil.quellen[]`** | datei (Upload-Pfad), bezeichnung („Zeugnis 10. Klasse“) | Uploads |
| `firmenfakten[]` | fakt, quelle, zugestimmt | Recherche + Nutzer |
| `belege[]` | `{text, woher, zitat}` – nur echte Herleitung; das **zitat** muss wörtlich vorkommen **und** den Wert tragen (jede Zahl/jedes Datum/jeder Abschluss im `text` steht im Zitat oder folgt daraus) | du |
| **`herkunft[]`** | `{satz, quellen[{nr, zitat} \| {anzeige} \| {firmenfakt} \| {upload}], privat_ok, vorlage}` – Abschnitt 5 | du, beim Entwurf |
| `lebenslauf`, `anschreiben{typ, betreff, anrede, absaetze[], gruss, anlagen_zeile}`, `formular[{feld, limit, text}]`, `email{betreff, text}`, **`whatsapp{text}`** | Unterlagen-Texte | du |
| `gespraech{termin, art, ort, gespraechspartner, einladung_text, bestaetigt, anrede (du/sie), mitbringen[], kernbotschaften[], vorstellung{dauer_min, kernpunkte[]}, schwierige_fragen[{frage, antwort_final}], fachfragen[{frage, antwort_final}], gehalt{antwort_final}, eigene_fragen[{frage, gewaehlt}], ac_uebungen[{typ, titel, dauer_min}], feedback[] (intern)}` | Gespräch/Spickzettel (`gespraech.md` 3) | du, aus Wortlaut + Einladung |
| `status[]`, `bewerbungen[]`, `entscheidungen[]`, `naechste_schritte[]` | Verlauf | du |

## 4. Wie du Felder füllst

**Normalisierungs-Wörterbuch** (`textlib.NORMALISIERUNG`, beide Richtungen): abi/ABI ↔ Abitur/Allgemeine Hochschulreife · fachabi ↔ Fachhochschulreife · quali, msa, m10, mittlere reife · fsj, föj, bfd · zfa, mfa, kfz · bio, mathe, lk, gk · fos, bos, gym, rs, th, fh, uni · bwl · B.A. ↔ Bachelor of Arts (B.Sc., B.Eng., M.A. …) · papa ↔ Vater, mama ↔ Mutter · str. ↔ Straße · „20h“/„15 std“ → 20 Std. (/Woche) · „29-31k“ → 29.000/31.000 · min → Minuten · Monatsnamen mit Tippfehlern („febuar“) · „april 25“ → 04/2025 · „märz bis august 24“ → 03/2024–08/2024 · „31. August 2027“ = 31.08.2027 · „ab januar“ → nächster Januar · Alter („Kinder 4 und 7“) ist keine Dauer. Diese Normalisierungen darfst du ohne `belege` schreiben. **Nicht** im Wörterbuch (fragen!): Aufwertungen („bisschen“ → „gute Kenntnisse“), geratene Monate/Tage, Niveaus.

- **Wörtlich genug:** „Kasse gemacht, abends abgerechnet“ → `taetigkeiten: ["an der Kasse gearbeitet", "abends die Abrechnung gemacht"]`. Nicht: „Kassenverantwortung“.
- **Daten so genau wie gesagt:** „seit 2023“ bleibt „seit 2023“. „seit märz 25“ → „seit 03/2025“ ist ok (steht so im Wortlaut). „ab Dezember“ → „ab Dezember 2026“, **nicht** „01.12.2026“.
- **Dauern** nur aus dem Wortlaut oder als Rechnung aus belegten Zeiträumen; „fast drei Jahre“ bei 2 J. 11 M. ist ok, „drei Jahre“ nicht. Zahlen aus der Anzeige belegen keine Dauer über den Nutzer.
- **Stunden/Teilzeit:** nur, was er sagt („zwei Kinder“ ≠ „Teilzeit 30 Std.“ – fragen).
- **Abschlüsse:** „Bachelor Soziale Arbeit“ bleibt so; „(B.A.)“ nur, wenn er „B.A.“ sagt oder es im Zeugnis steht.
- **Beispiele vollständig:** fehlt das Ergebnis, bleibt `ergebnis` leer.
- **Anzeigentext** ganz in `ziel.anzeige_text`; Einladung ganz in `gespraech.einladung_text`.
- **Firmenfakt aus Websuche:** `firmenfakten` mit Quelle, `zugestimmt: false`. Zustimmung als **eigene** Nachricht, erst bei Ja `true`. Hörensagen des Nutzers („Cousine sagt, gutes Klima“) bleibt seine Aussage, kein Firmenfakt.

## 5. Satz-Herkunft (`herkunft`)

Beim **Entwurf** jedes Freitexts (Anschreiben, Motivationsschreiben, Mail, Formular-Freitext, WhatsApp, Kurzprofil) schreibst du zu jedem Satz mit einer Aussage über die Person die Quelle dazu:
```json
"herkunft": [
 {"satz": "Seit März 2025 arbeite ich als Minijobber im Getränkelager.",
  "quellen": [{"nr": 4, "zitat": "minijob getränke hofmann seit märz 25 lager"}, {"nr": 8, "zitat": "im getränkelager"}]},
 {"satz": "In Ihrer Anzeige nennen Sie Sorgfalt.", "quellen": [{"anzeige": "Sorgfalt"}]},
 {"satz": "Meine Cousine hat bei Ihnen gelernt.", "nr": 13, "zitat": "meine cousine hat da ausbildung gemacht", "privat_ok": true}
]
```
- `satz` = der Satz genau wie im Text. `zitat` = Ausschnitt aus der Antwort (Groß/klein, Satzzeichen egal; „…“ für Auslassungen). Mehrere Quellen pro Satz sind normal; Belege sind Zitat **und** die ganze zitierte Antwort (inkl. gewählter Optionen, bestätigter Werte).
- Das Skript prüft nur **Behauptungs-Bausteine**: Zahlen/Daten (auch „fünften“ ↔ „5.“, „1. Februar 2027“ ↔ „1.2.27“), Namen, Abschlüsse, Tätigkeiten, Fähigkeiten, Häufigkeit/Intensität (täglich, immer, schnell, sehr), Gefühle/Motive (Spaß, spannend, „spricht mich an“), Kontakt zur Firma (kennengelernt). Erkannt werden Beugung, Partizip, trennbare Verben, Komposita, Umgangssprache, Synonyme in eine Richtung („leute“ → Kunden, nicht umgekehrt Kunden → Kollegen) und Tippfehler. Funktions- und Stilwörter sind frei. Fehlt ein Baustein → ❌ „Wörter ohne Quelle: …“.
- In **Ich-Teilsätzen** zählen nur Nutzer-Quellen; Anzeige/Firmen-Info nur im Teilsatz über die Firma („…, dass Azubis bei Ihnen …“). Ein „ja“ zu einem Firmenfakt ist **kein** Motiv – „Mich spricht an, dass …“ nur, wenn er es so (oder „finde ich gut/spannend“) gesagt hat; sonst „Laut Ihrer Karriereseite …“.
- Neutrale Sätze brauchen keinen Eintrag („Ich freue mich auf ein persönliches Gespräch.“, Gruß, Name, reine Datumsangaben) – auch die **Mail-Vorlagen** aus `abschicken.md` („anbei sende ich Ihnen meine Bewerbung als … ab …“, „Anschreiben, Lebenslauf und Zeugnisse finden Sie in einer PDF im Anhang“, „Für Rückfragen erreichen Sie mich unter …“). Vorlage mit eigenem Zusatz: `{"satz": …, "vorlage": true}` – dann prüft das Skript nur Zahlen/Daten.
- Quellen-Arten: `nr`+`zitat` (Wortlaut) · `upload` (Zitat aus Text-PDF/Word, z. B. Zeugnis) · `anzeige` (Anzeige/Einladung – nur für Firmenbezug) · `firmenfakt` (nur mit `zugestimmt: true`).
- Ich-Satz nur mit Anzeige-Quelle → ❌. Zeugnis-Foto → erst Rückfrage, Antwort ins rohtext, dann zitieren. Gesundheit/Familie/Privates → nur mit `privat_ok: true` nach ausdrücklichem Ja; im Anschreiben ⚠️ (im Regelfall weglassen).
- `fakten_check.py … --woher` (oder `herkunft.py PROFIL.json`) druckt die **Woher-Liste** für die Freigabe: `– „Satzanfang…“ → deine Worte: „…“` (ohne interne Nummern; Sie-Form: „Ihre Worte“).

## 6. Von der JSON zu den Unterlagen

- Lebenslauf = `bildung` + `stationen` (+ `luecken` > ~3 Monate) + Kenntnisse (`sprachen`, `edv`, `zertifikate`, `fuehrerschein` nur wenn gefüllt) + `hobbys`.
- Anschreiben: Einstieg aus `motivation_beruf` oder einem `beispiel`; 2–3 Anforderungen aus `ziel.muss`, belegt mit `beispiele`; Firma aus `motivation_firma` oder zugestimmtem Firmenfakt. Fehlt der Firmengrund: eine Frage, sonst Absatz weglassen.
- Anlagen-Zeile baut das Skript aus `profil.anlagen` (nur vorhandene Dateien).
- Formular: `formular[]` je Feld mit `limit`; „Wie aufmerksam geworden?“ nur aus `profil.wie_aufmerksam` (immer gefragt).

## 7. fakten_check: Treffer behandeln

`python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json [Dateien…] [--woher] [--typ spickzettel]` – Exit 1 bei ❌.

| Treffer | Was tun |
|---|---|
| ❌ Monat/Datum („nur das Jahr ist im Wortlaut“) | Nur das Jahr schreiben **oder** eine Nachfrage mit einem konkreten Wert |
| ❌ Dauer „gerundet“ | Genau schreiben („seit 10/2023“, „fast drei Jahre“) oder fragen |
| ❌ Zahl/Name/Begriff | Steht es in einer Antwort? Sonst streichen oder fragen |
| ❌ Abschluss/Kürzel, Sprachniveau, Führerschein/Klasse, Link | nur vom Nutzer – sonst raus oder fragen |
| ❌ Firmenfakt | Nutzer fragen (mit Quelle) oder streichen |
| ❌ Wie aufmerksam? | Nutzer fragen (nur die Quelle muss stimmen). Nie raten |
| ❌ Beleg ohne Zitat / Zitat trägt den Wert nicht | Der Wert steht nicht im Zitat → Nutzer fragen; ein Beleg ist keiner |
| ❌ Herkunft: Satz ohne Quelle | Satz streichen und **als kurze Frage** stellen – oder Eintrag mit Nr. + Zitat ergänzen, wenn er es gesagt hat |
| ❌ Herkunft: Wörter ohne Quelle | Diese Wörter hat er nicht gesagt → streichen/ersetzen durch seine Worte oder fragen |
| ❌ Herkunft: Zitat steht in keiner Antwort | wörtlich zitieren (nicht glätten) |
| ❌ Privates/Gesundheit/Familie | vorher ausdrücklich fragen („Soll das mit deinem Knie rein? Ich rate eher ab.“) |
| ℹ️/⚠️ unsichere Antwort | Ja/Nein-Rückfrage, dann `geklaert: true` |
| ❌ Abgleich | Datei ist alt oder von Hand geändert → neu erzeugen |
| ❌ Sprache | „Deutsch“/„Englisch“ nicht genannt → Sprachen-Frage, nie automatisch eintragen |
| ❌ Spickzettel-Wortlaut | Kernbotschaft/Antwort mit Wörtern, die er nicht gesagt hat → seine Worte nehmen |
| ⚠️ Aufwertung? / Begriff / Lebenslauf-Begriff | Hat er das so gesagt? Sonst seine Worte nehmen |
| ⚠️ Einschränkung weg? | Er sagte „manchmal“/„bisschen“ – im Text mitnehmen („gelegentlich“) |
| ⚠️ Stil | Umgangssprache, Chat-Kürzel, Tippfehler → Standarddeutsch (Vorschlag steht dabei) |
| ⚠️ Jahr abgeleitet | aus „letztes Jahr“ – Jahr kurz bestätigen lassen |
| ⚠️ Änderungswunsch offen | zugesagte Änderung einbauen, dann `erledigt: true` |
| ⚠️ Beispiel/Hobby ungenutzt | einbauen oder bewusst weglassen |

**Nie** einen Treffer mit `belege` „wegbelegen“, den der Nutzer nicht gesagt hat. Der Check ist heuristisch: Deine `herkunft` ehrlich anzulegen bleibt Pflicht.
