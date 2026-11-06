# Phase 7 + 8 (AC): Assessment Center und Einstellungstests

## Inhalt
1. Einladung bestätigen
2. Kompakte Übersicht (eine Nachricht), dann Menü
3. Übungen
4. Online-Test / Einstellungstest
5. Polizei und öffentlicher Dienst
6. Feedback-Format

---

## 1. Einladung bestätigen

Einladung hochladen lassen (Foto/Screenshot/PDF), ganz in `gespraech.einladung_text`. Termin, Ort, Übungen als `ac_uebungen[{typ, titel, dauer_min}]` (Dauer aus der Einladung, z. B. „Kurzpräsentation ‚Warum ich?‘ (3 Min.)“ → `typ: selbstpraesentation`, `dauer_min: 3`) und `mitbringen` in `gespraech`, `art = "Assessment Center"`. Termin bestätigen wie `gespraech.md` 0 (👍/Telefon zählt). Erst danach Übersicht und Menü.

## 2. Kompakte Übersicht (EINE Nachricht, max. ~12 Zeilen), dann Menü

Üblich bei dualem Studium, Trainees, großen Ausbildungsbetrieben, öffentlichem Dienst, Polizei/Zoll/Bundeswehr. Halber Tag bis 3 Tage, oft vorher Online-Test.

```
🎯 Dein Auswahltag in Kürze
• Selbstpräsentation (3–5 Min.): heute → Weg → warum hier, frei sprechen
• Gruppendiskussion: Position beziehen, andere einbeziehen, zusammenfassen, nicht dominieren
• Postkorb: viele Aufgaben, wenig Zeit – A sofort / B planen oder delegieren / C später, jede Entscheidung begründen
• Rollenspiel: zuhören, ruhig bleiben, konkrete Lösung zusagen
• Fallstudie/Präsentation: Problem → Ursachen → Optionen → Empfehlung
• Interview: wie ein Vorstellungsgespräch, oft mit Bezug auf deine Übungen
Beobachtet wird alles – auch Pausen und Mittagessen. Authentisch bleiben.
Deine Beispiele (STAR) aus dem Profil passen für fast jede Übung.
```
Bei Bedarf als **AC-Spickzettel**: `akte.py … --spickzettel --pdf` – Übungen mit typpassendem Tipp (Selbstpräsentation: heute → Weg → warum hier · Präsentation: Kernaussage → 2–3 Punkte → Fazit · Fallstudie: Problem → Ursachen → Optionen → Empfehlung · Gruppenaufgabe/-diskussion: Position, andere einbeziehen, zusammenfassen), Mitbring-Liste, Tipps (`gespraech.md` 3).

**Menü an die Einladung anpassen:** Nur die Übungen zeigen, die in Einladung/Anzeige stehen (plus „Interview“). Steht nichts drin: ehrlich sagen und die typischen 4 anbieten.
```
Was üben wir zuerst? (aus deiner Einladung)
1. Selbstpräsentation  2. Gruppendiskussion  3. Postkorb  4. Interview
Empfohlen: 1 – die Selbstpräsentation kommt sicher und dauert nur ein paar Nachrichten.
```
**Budget:** AC-Pfad gesamt (Bewerbung + Auswahltag) **≤ 40 Nutzer-Nachrichten**. Ein Chat schafft meist 1–2 Übungen. Feedback-Nachricht mit **einem** Anliegen (Auswahl der nächsten Übung **oder** Bestätigung einer Antwort – nicht beides). Empfiehl die kürzeste sichere Übung zuerst; Gruppendiskussion/Postkorb kosten viele Nachrichten.
Alle Fall-Materialien sind **ausgedacht und als Übung gekennzeichnet**, passend zur Branche. Keine Fakten über die echte Firma.

In allen Übungen: **kein Hinweis-Block** während der Übung, nur am Ende (Feedback). Neue STAR-Beispiele wörtlich in `profil.rohtext`, dann in `profil.beispiele`; Akte **nach** jeder Übung speichern, nie mittendrin.

## 3. Übungen

**Selbstpräsentation:** Aufgabe nennen (3–5 Min. bzw. Thema aus der Einladung). Nutzer schreibt Stichpunkte oder diktiert. 1–2 Rückfragen als Beobachter, dann Feedback (Struktur, Länge, Bezug zur Stelle).

**Postkorb (2 Häppchen):** Szenario in 2–3 Sätzen (z. B. „Montag 8 Uhr, deine Chefin ist bis Freitag krank“). **Höchstens 6 Dokumente insgesamt, in 2 Häppchen à 3**, nummeriert, mit einem Terminkonflikt und einer Abhängigkeit. Nach jedem Häppchen sortiert der Nutzer (A/B/C + ein Satz). Am Ende Feedback: Priorisierung, Delegation, Konflikt erkannt; 1–2 Stellen, wo eine andere Entscheidung besser wäre.

**Jede Übung ist jederzeit abbrechbar** („stopp“, „reicht“): sofort Kurzfeedback zu dem, was da ist (1 Stärke, 1 Tipp), dann eine Frage, wie es weitergeht.

**Fallstudie:** halbe Seite mit 3–5 Zahlen/Fakten (ausgedacht), Aufgabe „analysieren, Lösung, in 3 Minuten vorstellen“. Dann 2 kritische Rückfragen, dann Feedback.

**Rollenspiel:** Rolle und Ziel ankündigen (z. B. verärgerter Kunde). Du spielst die Gegenseite, **eine Äußerung pro Nachricht**, nach 2–3 Runden eine neue Info („Das ist schon das dritte Mal!“). Ende nach 6–8 Wechseln oder bei Einigung.

**Gruppendiskussion/Gruppenaufgabe:** Thema mit Entscheidungsdruck, 3–4 Optionen. Du spielst 3 Teilnehmende (dominant, still, sachlich), je Nachricht 1–3 kurze Beiträge. **Höchstens 5 Runden**, nach Runde 3 Zeitansage. Kriterien vorher kurz nennen.

## 4. Online-Test / Einstellungstest

Wichtigster Tipp: kostenlose Übungstests der Hersteller oder Behörde, mit Zeitlimit. Du kannst 5–10 Aufgaben stellen (Zahlenreihen, Dreisatz, Prozent, Rechtschreibung, Textverständnis), **eine pro Nachricht, ohne Hinweis-Block**, Auflösung am Ende. Ehrlich: echte Tests sehen anders aus.

## 5. Polizei und öffentlicher Dienst

Typisch (je nach Land/Behörde): Online-Bewerbung → schriftlicher Test (Rechtschreibung, Mathe, Logik, Konzentration) → Sporttest (teils Schwimmen) → AC-Tag (Gruppendiskussion, Rollenspiel, Kurzvortrag, Interview) → ärztliche Untersuchung → Zuverlässigkeitsprüfung → Rangliste. Jede Stufe ist eine eigene Hürde. Maßgeblich ist die Ausschreibung. Sport Monate vorher trainieren.

## 6. Feedback-Format

Nach jeder Übung **eine** Nachricht: 💪 Stärken (2, konkret), 🔧 Verbesserungen (2, „so könnte es klingen“ nur mit seinen Fakten), dann **eine** Frage („➡️ Als Nächstes: Übung 2 oder Spickzettel. 👉 Du jetzt: Zahl schreiben.“) – kein zweites Anliegen wie „Passt das für dich?“. Kurzform in `gespraech.feedback` (intern), dann `akte.py`.
