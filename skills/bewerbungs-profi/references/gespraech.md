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

Einladung bekommen und `gespraech.bestaetigt` ist nicht `true`? Dann ist das die **erste und einzige** Sache dieser Nachricht: Einladung ganz in `gespraech.einladung_text`, Termin/Art/Ort/Gesprächspartner in `gespraech`, dann eine kurze Bestätigungs-Mail (3 Sätze: Dank, Termin bestätigen, ggf. eine Frage zu Ablauf/Ort/Mitbringen) im Chat zum Kopieren und:
„Hast du sie abgeschickt? a) Ja b) Mach ich später“. Frist der Einladung beachten, sonst innerhalb von 1–2 Tagen. **Erst in der nächsten Nachricht** Übersicht und Übungsangebot (Konfliktregel).

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
Dann: „Wollen wir üben? a) Ja, kurze Runde – 5 Fragen (Empfohlen am Handy) b) Ja, volle Runde – 8 Fragen c) Erst den Spickzettel“.

**Spickzettel** (`akte.py … --spickzettel [--pdf]`) – gegliedert, kurz, sachlich, ohne leere Felder und ohne interne Vermerke:
`Termin | Art | Ort` · Mitbringen (aus der Einladung, sonst passend zur Art) · **3 Kernbotschaften** (`gespraech.kernbotschaften`, je ein Satz aus seinen Antworten) · Vorstellung · **Schwierige Fragen mit Antwort** (`schwierige_fragen`; Lücken, Abbruch, Wechselgrund kommen automatisch dazu; nach dem Üben gilt die **verbesserte** Fassung aus `feedback[].besser`) · Beispiele · **nur die eigenen Fragen, die der Nutzer gewählt hat** (`eigene_fragen[{frage, gewaehlt: true}]`) · Tipps passend zu Präsenz/Video/Telefon/Probearbeiten/AC.
Schreib die Felder in sachlicher Sprache („Frau Gruber“, nicht „der Gruber“). Vorher `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json --typ spickzettel` → 0 ❌ (z. B. keine „8 Jahre“ bei 7,5).

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
- **Probearbeiten / Probetag (5a):** üblich in Handwerk, Gastro, Pflege, Kita, Handel. Klären (eine Frage, falls nicht in der Einladung): Dauer, Kleidung/Schuhe, was mitbringen, Bezahlung. Hinweis: Ein kurzes unbezahltes „Einfühlungsverhältnis“ (meist wenige Tage, ohne Arbeitspflicht) ist üblich; wird richtig mitgearbeitet, steht in der Regel Lohn zu – bei Unsicherheit allgemein einordnen und auf Beratung (Gewerkschaft, IHK/HWK) verweisen. Tipps: pünktlich, mit anpacken, Fragen stellen, am Ende nach Rückmeldung fragen. Spickzettel mit `gespraech.art = "Probearbeiten"`.
- **Technisches/Fach-Interview** (IT, Technik, Labor, Handwerk): Fachfragen zu Muss-Anforderungen der Anzeige, oft eine kleine Aufgabe (Code, Rechnung, Fehlersuche). Üben: 3–4 Fachfragen zu den Schlüsselwörtern, **laut denken** („Ich würde zuerst … prüfen, weil …“), Nichtwissen ehrlich sagen und den Lösungsweg zeigen. Keine Fakten über die echte Firmentechnik erfinden.

## 6. Üben: Simulation

Kurz ankündigen (2 Sätze): „Ich bin jetzt [Frau Sommer] von [Firma]. Eine Frage nach der anderen – antworte wie im echten Gespräch (gern per Diktat/Sprachmodus). ‚Stopp‘ beendet, ‚Tipp‘ gibt einen Hinweis.“

- **Eine Frage pro Nachricht**, „Frage 3 von 8“ (bzw. „von 5“), in der Rolle, kurze Reaktionen. **Kein Hinweis-Block, kein Feedback** während der Runde (außer bei „Tipp“).
- **Volle Runde 8 Fragen**, passend zu Stelle und Lebenslauf: 1 Über sich · 2 Warum dieser Beruf/diese Stelle · 3 Warum wir · 4 konkrete Station oder Lücke/Wechsel · 5 Verhaltensfrage zu einer Muss-Anforderung (STAR) · 6 Stärken/Schwächen · 7 fachlich/situativ (bei Azubis einfach) · 8 Stressfrage oder Rahmen, dann „Haben Sie Fragen an uns?“ (antworte plausibel, **ohne** Fakten über die echte Firma zu erfinden).
- **Kurze Runde = genau diese 5:** 1 Über sich · 2 Warum diese Stelle/Firma · 4 Station/Lücke/Wechsel · 5 Verhaltensfrage (STAR) · 6 Stärken/Schwächen – dann „Haben Sie Fragen an uns?“.
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
Verbesserungen nur mit Fakten des Nutzers; keine Noten, keine Garantie. Die verbesserte Antwort je Frage als `gespraech.feedback[{frage, besser}]` speichern (landet so im Spickzettel), dann `akte.py`. Runde 2: andere Fragen, Vergleich zu Runde 1. Im Feedback keine gerundeten Dauern („seit 2010“ statt „12 Jahre“).
