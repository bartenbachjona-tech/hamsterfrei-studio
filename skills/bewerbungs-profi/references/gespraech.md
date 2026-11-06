# Phase 7 + 8: Vorstellungsgespräch vorbereiten und üben

## Inhalt
0. Termin bestätigen (eigener Schritt)
1. Gespräch, Probearbeiten oder Assessment Center?
2. Was du brauchst
3. Die kompakte Übersicht (eine Nachricht) + Spickzettel
4. Hintergrundwissen (nur bei Rückfragen)
5. Telefon-, Video-, technisches Interview
6. Üben: Simulation
7. Feedback und zweite Runde

---

## 0. Termin bestätigen (eigener Schritt)

Einladung ganz in `gespraech.einladung_text`, Termin/Art/**Ort genau wie in der Einladung** („Filiale am Ludwigsplatz“)/Gesprächspartner in `gespraech`.
- **Schon zugesagt** („hab mit 👍 geantwortet“, „hab angerufen“, „passt, komme“) → `bestaetigt: true`, **keine** zweite Bestätigungsrunde; direkt weiter mit der Übersicht. Nur wenn die Einladung eine schriftliche Bestätigung verlangt, einen Satz zum Kopieren anbieten.
- **Telefonische Einladung:** keine Bestätigungs-Mail nötig; nur Termin, Ort, Ansprechperson notieren lassen (eine Frage, falls etwas fehlt).
- **Noch nicht zugesagt:** eine Nachricht nur dafür: kurze Bestätigung (3 Sätze, Codeblock) + „Abgeschickt? a) Ja b) Später“. Frist beachten. Erst danach Übersicht und Übungsangebot.

## 1. Gespräch, Probearbeiten oder Assessment Center?

Anzeige, Akte, Einladung lesen. „Assessment Center“, „Auswahltag“, „Einstellungstest“, „Online-Test“, „Gruppenübung“ → `assessment_center.md` (das Einzelinterview dort mit Abschnitt 6). „Probearbeiten“, „Probetag“, „Schnuppertag“ → Abschnitt 5a. Unklar → **eine** Frage: „Was steht in deiner Einladung? a) Vorstellungsgespräch b) Auswahltag/AC c) Probearbeiten d) Telefon/Video e) noch keine Einladung“.

## 2. Was du brauchst

Aus Akte/JSON: Stelle, Unterlagen, `profil.beispiele`. Fehlt etwas: höchstens eine Frage (Termin/Art). Ohne Unterlagen geht es auch – dann Werdegang kurz erfragen (eine Frage).

## 3. Die kompakte Übersicht (EINE Nachricht, max. ~12 Zeilen) – dann direkt üben

```
🎯 Dein Gespräch in Kürze
1. Begrüßung, Smalltalk – kurz, freundlich, Blickkontakt
2. Firma stellt sich vor – zuhören, 1–2 Notizen
3. „Erzählen Sie von sich“ – 1–2 Min.: heute → Weg → warum hier
4. Fragen zu Lebenslauf/Motivation – deine Beispiele aus dem Profil
5. Verhaltensfragen („Erzählen Sie von einer Situation …“) – STAR: Situation, Aufgabe, was DU getan hast, Ergebnis
6. Deine Fragen (2–3) – z. B. erste Wochen, Team, wie es weitergeht
7. Abschluss – fragen, wann du Rückmeldung bekommst
Verhalten: 10 Min. Puffer, eine Stufe schicker als üblich, Stichpunkte statt auswendig, bei Blackout durchatmen und nachfragen.
Unzulässig (z. B. Schwangerschaft, Kinderwunsch, Kinderbetreuung, Religion): freundlich nachfragen, worum es geht – du musst nicht antworten.
```
Dann: „Wollen wir üben? a) Ja, kurze Runde – 5 Fragen (Empfohlen) b) Volle Runde – 8 Fragen c) Erst den Spickzettel“. Die „1–2 Min.“ in Punkt 3 durch die Dauer aus der Einladung ersetzen.

### Spickzettel (`akte.py PROFIL --spickzettel --pdf`)

Klare Datenstruktur in `gespraech` – das Skript baut daraus eine **kompakte A5-PDF** (am Handy lesbar, keine fast leere Seite 2; `--a4` zum Drucken) und eine `.txt`:

| Feld | Inhalt |
|---|---|
| `anrede` | `du` oder `sie` (siezt der Nutzer → `sie`; alle Überschriften passen sich an) |
| `kernbotschaften[]` | 3 Sätze aus seinen Antworten, **ohne** eigene Nummerierung |
| `vorstellung{dauer_min, kernpunkte[]}` | Dauer **aus der Einladung** (3/5 Min.); fehlt sie, liest das Skript die Einladung, sonst 1–2 Min. |
| `schwierige_fragen[{frage, antwort_final}]` | **nur echte Fragen** mit der **finalen** Antwort in seinen Worten (Ich-Form). Kein Feedback, keine Übungsnamen, keine Notizen, kein Rohtext von Wechsel-/Abbruchgrund – die schreibst du als fertige Antwort aus. Lücke/Abbruch/Wechsel nicht automatisch: das Skript erinnert dich. |
| `fachfragen[{frage, antwort_final}]` | 2–3 Fachfragen zur Stelle mit seiner Antwort |
| `gehalt{antwort_final}` | Spanne mit Quelle; offen (`[PRÜFEN]`) → steht als „noch offen – vor dem Termin klären“ drauf, **nie still weg** |
| `eigene_fragen[{frage, gewaehlt}]` | nur die gewählten |
| `mitbringen[]` | aus der Einladung (sonst Standard je Art) |
| `ac_uebungen[{typ, titel, dauer_min}]` | `typ`: selbstpraesentation · praesentation · fallstudie · gruppe · postkorb · rollenspiel · interview · test → passender Tipp (Selbstpräsentation ≠ Fallstudie) |
| `feedback[]` | **intern**, nie auf dem Spickzettel |

Das Skript meldet dir: Ort/Termin ≠ Einladung, offene Gehaltsfrage, Antworten mit internem Vermerk oder in 3. Person. Vorher `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json --typ spickzettel` → 0 ❌. Nach dem Erzeugen die PDF als Bild ansehen.

Neue STAR-Geschichten, die beim Üben entstehen, **wörtlich** in `profil.rohtext` und dann in `profil.beispiele`. **Akte nicht mitten in der Übung**, sondern direkt nach dem Feedback.

## 4. Hintergrundwissen (nur, wenn der Nutzer fragt)

- **Dauer:** meist 30–60 Min., beim dualen Studium bis 2 Std.
- **Typische Fragen:** über sich · warum dieser Beruf · warum wir · Stärken/Schwächen (Schwäche echt + was man dagegen tut) · Erfolg/Fehler · in 3–5 Jahren · Wechselgrund · Kritik · was wissen Sie über uns · Gehalt · Fragen an uns. Azubis: Lieblingsfach, Praktika, Lücken.
- **Stressfragen** („Warum gerade Sie?“, Schweigen): sachlich, kurz Zeit nehmen.
- **Gehalt:** Spanne brutto/Jahr mit Quelle (`nach_dem_gespraech.md`).
- **Unzulässige Fragen (DE, allgemein, keine Rechtsberatung):** Schwangerschaft/Familienplanung, Kinderwunsch, **Kinderbetreuung/„Wer passt auf die Kinder auf?“** (in der Regel unzulässig, diskriminierend), Heirat/Partnerschaft, sexuelle Orientierung, Religion (Ausnahme kirchliche Arbeitgeber), Partei/Gewerkschaft, ethnische Herkunft, ausgeheilte Krankheiten, in der Regel Schwerbehinderung; nach der EU-Entgelttransparenzrichtlinie das bisherige Gehalt (Umsetzung in DE noch offen, Stand 26.06.2026 – bei Websuche aktuell prüfen). Zulässig: tätigkeitsrelevante Krankheiten, Vorstrafen mit Bezug zur Stelle, Qualifikationen. Auf unzulässige Fragen darf man ausweichen oder die Unwahrheit sagen. Bei Diskriminierung: Antidiskriminierungsstelle des Bundes; Ansprüche nach AGG haben kurze Fristen – darum zügig beraten lassen.

## 5. Telefon-, Video-, technisches Interview, Probearbeiten

- **Telefon:** ruhiger Ort, im Stehen sprechen, lächeln, Lebenslauf und Notizen vor sich, Namen notieren. Oft kürzer und eine Vorauswahl – Selbstpräsentation in 1 Minute.
- **Video:** Technik vorher testen (Link, Kamera, Ton, Akku/Strom, WLAN), helles Licht von vorn, ruhiger Hintergrund, Kamera auf Augenhöhe (Handy auf Stapel Bücher, quer), **in die Kamera schauen**, Benachrichtigungen aus, Telefonnummer für Technikprobleme bereit. Kleidung wie vor Ort.
- **Zeitversetztes Video** (Fragen aufzeichnen): selten; Antworten wie im Gespräch, auf die Zeit achten.
- **Probearbeiten / Probetag (5a) – Kurzpfad:** üblich in Handwerk, Gastro, Pflege, Kita, Handel. **Eine** Übersicht (≤ 10 Zeilen: Datum, Uhrzeit, Ort laut Einladung, Kleidung, 3 Tipps, Bezahlung in einem Satz), dann „Zwei kurze Übungsfragen? a) Ja b) Nein, passt“ – **max. 2 Fragen** (z. B. „Warum bei uns?“, „Was machst du bei einer langen Schlange?“). Bezahlung: Ein kurzes unbezahltes „Einfühlungsverhältnis“ (wenige Tage, ohne Arbeitspflicht) ist üblich; wird richtig mitgearbeitet, steht in der Regel Lohn zu – allgemein einordnen, Beratung (Gewerkschaft, IHK/HWK) nennen. Spickzettel nur auf Wunsch (`gespraech.art = "Probearbeiten"`).
- **Technisches/Fach-Interview** (IT, Technik, Labor, Handwerk): Fachfragen zu Muss-Anforderungen der Anzeige, oft eine kleine Aufgabe (Code, Rechnung, Fehlersuche). Üben: 3–4 Fachfragen zu den Schlüsselwörtern, **laut denken** („Ich würde zuerst … prüfen, weil …“), Nichtwissen ehrlich sagen und den Lösungsweg zeigen. Keine Fakten über die echte Firmentechnik erfinden.

## 6. Üben: Simulation

Kurz ankündigen (2 Sätze): „Ich bin jetzt [Frau Sommer] von [Firma]. Eine Frage nach der anderen – antworte wie im echten Gespräch (gern per Diktat/Sprachmodus). ‚Stopp‘ beendet, ‚Tipp‘ gibt einen Hinweis.“

- **Eine Frage pro Nachricht**, „Frage 3 von 8“ (bzw. „von 5“), in der Rolle, kurze Reaktionen. **Kein Hinweis-Block, kein Feedback** während der Runde (außer bei „Tipp“).
- **Volle Runde 8 Fragen**, passend zu Stelle und Lebenslauf: 1 Über sich · 2 Warum dieser Beruf/diese Stelle · 3 Warum wir · 4 konkrete Station oder Lücke/Wechsel · 5 Verhaltensfrage zu einer Muss-Anforderung (STAR) · 6 Stärken/Schwächen · 7 fachlich/situativ (bei Azubis einfach) · 8 Stressfrage oder Rahmen, dann „Haben Sie Fragen an uns?“ (antworte plausibel, **ohne** Fakten über die echte Firma zu erfinden).
- **Kurze Runde = genau diese 5:** 1 Über sich · 2 Warum diese Stelle/Firma · 4 Station/Lücke/Wechsel · 5 Verhaltensfrage (STAR) · 6 Stärken/Schwächen – dann „Haben Sie Fragen an uns?“. Minijob/Probearbeiten: 2 Fragen.
- **„stopp“, „reicht“, „fertig“** beendet sofort: aus der Rolle, **Kurzfeedback** (1 Stärke, 1 Tipp, je 1 Satz), dann **eine** Frage (z. B. Spickzettel ja/nein). Beantworte Zusatzfragen („und bezahlt?“) kurz in derselben Nachricht.
- Optional nach Absprache: eine unzulässige Frage einbauen (vorher ankündigen).
- Ein-Wort-Antwort: einmal in der Rolle nachhaken.
- Am Handy/Free-Plan: die kurze Runde empfehlen.

## 7. Feedback und zweite Runde

Nach der letzten Frage aus der Rolle gehen, **eine** Nachricht:
```
🎯 Feedback
💪 Stark: Frage 2 – echter Grund mit Beispiel (Kasse/Abrechnung).
🔧 Besser: Frage 1 – zu lang. Heute → Weg → warum hier, ca. 1 Min. So mit DEINEN Fakten: „…“
🔧 Frage 6 – Schwäche ohne Gegenmaßnahme: ergänzen, was du tust.
📋 1 🟡 2 🟢 3 🔴 4 🟢 5 🟡 6 🔴 7 🟢 8 🟡
➡️ Als Nächstes: Runde 2 oder nur die roten Fragen.
👉 Du jetzt: „Runde 2“, „nur die roten“ oder „fertig“.
```
Verbesserungen nur mit Fakten des Nutzers – **keine erfundenen Gegenmaßnahmen** zu Schwächen („…was du dagegen tust“ fragen statt ausdenken). Übernimmt er eine Verbesserung („passt so“), trägst du sie als `schwierige_fragen[{frage, antwort_final}]` ein; `feedback` bleibt intern. Dann `akte.py`. Runde 2: andere Fragen. Keine gerundeten Dauern („seit 2010“ statt „12 Jahre“).
