# Phase 7 + 8: Vorstellungsgespräch vorbereiten und üben

## Inhalt
1. Gespräch oder Assessment Center?
2. Was du brauchst
3. Die kompakte Übersicht (eine Nachricht) + Spickzettel
4. Hintergrundwissen (nur bei Rückfragen)
5. Telefon-, Video-, technisches Interview
6. Üben: Simulation
7. Feedback und zweite Runde

---

## 1. Gespräch oder Assessment Center?

Anzeige, Akte, Einladung lesen. Wörter wie „Assessment Center“, „Auswahltag“, „Einstellungstest“, „Online-Test“, „Gruppenübung“ → `assessment_center.md` (das Einzelinterview dort übst du mit Abschnitt 6). Unklar → **eine** Frage: „Was steht in deiner Einladung? a) Vorstellungsgespräch b) Auswahltag/AC c) Online-Test d) Telefon/Video e) noch keine Einladung“.

**Einladung bekommen?** Zuerst: Termin innerhalb von 1–2 Tagen bestätigen (kurze Mail anbieten: Dank, Termin bestätigen, ggf. Frage zu Ablauf/Ort). Termin, Art, Ort, Gesprächspartner in `gespraech`.

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
Dann sofort: „Wollen wir üben? a) Ja, jetzt (Empfohlen) b) Erst den Spickzettel als PDF“. Spickzettel: `gespraech.selbstpraesentation`, `eigene_fragen` füllen, dann `python3 "$S/akte.py" /tmp/bewerbung/profil.json --spickzettel --pdf` (ohne #/**, öffnet überall).

Neue STAR-Geschichten, die beim Üben entstehen, **sofort** in `profil.beispiele` – und alle ~6 Antworten Akte speichern.

## 4. Hintergrundwissen (nur, wenn der Nutzer fragt)

- **Dauer:** meist 30–60 Min., beim dualen Studium bis 2 Std.
- **Typische Fragen:** über sich · warum dieser Beruf · warum wir · Stärken/Schwächen (Schwäche echt + was man dagegen tut) · Erfolg/Fehler · in 3–5 Jahren · Wechselgrund · Kritik · was wissen Sie über uns · Gehalt · Fragen an uns. Azubis: Lieblingsfach, Praktika, Lücken.
- **Stressfragen** („Warum gerade Sie?“, Schweigen): sachlich, kurz Zeit nehmen.
- **Gehalt:** Spanne brutto/Jahr mit Quelle (`nach_dem_gespraech.md`).
- **Unzulässige Fragen (DE, allgemein, keine Rechtsberatung):** Schwangerschaft/Familienplanung, Kinderwunsch, **Kinderbetreuung/„Wer passt auf die Kinder auf?“** (in der Regel unzulässig, diskriminierend), Heirat/Partnerschaft, sexuelle Orientierung, Religion (Ausnahme kirchliche Arbeitgeber), Partei/Gewerkschaft, ethnische Herkunft, ausgeheilte Krankheiten, in der Regel Schwerbehinderung; nach der EU-Entgelttransparenzrichtlinie das bisherige Gehalt (Umsetzung in DE noch offen, Stand 26.06.2026 – bei Websuche aktuell prüfen). Zulässig: tätigkeitsrelevante Krankheiten, Vorstrafen mit Bezug zur Stelle, Qualifikationen. Auf unzulässige Fragen darf man ausweichen oder die Unwahrheit sagen. Bei Diskriminierung: Antidiskriminierungsstelle des Bundes; Ansprüche nach AGG haben kurze Fristen – darum zügig beraten lassen.

## 5. Telefon-, Video-, technisches Interview

- **Telefon:** ruhiger Ort, im Stehen sprechen, lächeln, Lebenslauf und Notizen vor sich, Namen notieren. Oft kürzer und eine Vorauswahl – Selbstpräsentation in 1 Minute.
- **Video:** Technik vorher testen (Link, Kamera, Ton, Akku/Strom, WLAN), helles Licht von vorn, ruhiger Hintergrund, Kamera auf Augenhöhe (Handy auf Stapel Bücher, quer), **in die Kamera schauen**, Benachrichtigungen aus, Telefonnummer für Technikprobleme bereit. Kleidung wie vor Ort.
- **Zeitversetztes Video** (Fragen aufzeichnen): selten; Antworten wie im Gespräch, auf die Zeit achten.
- **Technisches/Fach-Interview** (IT, Technik, Labor, Handwerk): Fachfragen zu Muss-Anforderungen der Anzeige, oft eine kleine Aufgabe (Code, Rechnung, Fehlersuche). Üben: 3–4 Fachfragen zu den Schlüsselwörtern, **laut denken** („Ich würde zuerst … prüfen, weil …“), Nichtwissen ehrlich sagen und den Lösungsweg zeigen. Keine Fakten über die echte Firmentechnik erfinden.

## 6. Üben: Simulation

Kurz ankündigen (2 Sätze): „Ich bin jetzt [Frau Sommer] von [Firma]. Eine Frage nach der anderen – antworte wie im echten Gespräch (gern per Diktat/Sprachmodus). ‚Stopp‘ beendet, ‚Tipp‘ gibt einen Hinweis.“

- **Eine Frage pro Nachricht**, „Frage 3 von 8“, in der Rolle, kurze Reaktionen. **Kein Hinweis-Block, kein Feedback** während der Runde (außer bei „Tipp“).
- **Standardrunde 8 Fragen**, passend zu Stelle und Lebenslauf: 1 Über sich · 2 Warum dieser Beruf/diese Stelle · 3 Warum wir · 4 konkrete Station oder Lücke/Wechsel · 5 Verhaltensfrage zu einer Muss-Anforderung (STAR) · 6 Stärken/Schwächen · 7 fachlich/situativ (bei Azubis einfach) · 8 Stressfrage oder Rahmen, dann „Haben Sie Fragen an uns?“ (antworte plausibel, **ohne** Fakten über die echte Firma zu erfinden).
- Optional nach Absprache: eine unzulässige Frage einbauen (vorher ankündigen).
- Ein-Wort-Antwort: einmal in der Rolle nachhaken.
- Am Handy/Free-Plan: kürzere Runde (5 Fragen) anbieten.

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
Verbesserungen nur mit Fakten des Nutzers; keine Noten, keine Garantie. Runde 2: andere Fragen, Vergleich zu Runde 1. Feedback-Kurzform in `gespraech.feedback`, dann `akte.py`.
