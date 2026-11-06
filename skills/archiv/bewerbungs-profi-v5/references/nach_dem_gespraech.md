# Phase 9: Nach dem Gespräch – Nachfassen, Zusage, Absage, Gehalt

## 1. Nachfassen

- **Dankes-Mail** 1–2 Tage nach dem Gespräch: kurz, greift einen konkreten Punkt auf – den Punkt liefert der Nutzer („Worüber habt ihr gesprochen, das dir gefallen hat?“).
- **Nachfragen**, wenn die genannte Frist vorbei ist oder nach **1–2 Wochen** ohne Frist; nach Bewerbung ohne Gespräch nach etwa **2–3 Wochen**.
- Entwürfe im Chat zum Kopieren, 3–5 Sätze, Betreff mit Stelle und Gesprächsdatum.

```
Betreff: Nachfrage zu meiner Bewerbung als [Stelle] – Gespräch am [Datum]

Sehr geehrte Frau Sommer,
vielen Dank noch einmal für das Gespräch am [Datum]. Sie hatten eine Rückmeldung bis [Datum] erwähnt –
gibt es schon einen Stand? Ich bin weiterhin sehr interessiert an der Stelle.
Mit freundlichen Grüßen
[Name]
```

**Ghosting normalisieren:** Laut karriere.at (AT, 11/2025, 1.077 Jobsuchende) haben 84 % schon keine Rückmeldung bekommen. „Das liegt meistens nicht an dir.“ Parallel weiterbewerben, `bewerbungen` in der JSON pflegen.

## 2. Zusage

- Schriftliche Bestätigung abwarten, bevor man anderen absagt.
- Vertrag in Ruhe lesen (Vergütung, Probezeit, Arbeitszeit, Urlaub, Beginn). Rechtliches nur allgemein einordnen; Fragen zu Fristen, Klauseln, Elternzeit, Kündigung → Gewerkschaft, IHK/HWK (bei Ausbildung), Arbeitnehmerkammer, Anwalt. **Keine Rechtsberatung, keine Fristen für den Einzelfall ausrechnen.**
- Ausbildung: Der Betrieb lässt den Vertrag bei IHK/HWK eintragen.
- Anderen fair und zügig absagen – kurze Absage-Mail anbieten.

## 3. Gehalt und Geld

- **Mindestausbildungsvergütung (BBiG):** Beginn 2026: 724 €/Monat im 1. Jahr (2.–4. Jahr ≈ 854 / 977 / 1.014 €). Beginn 2027: 764 / 902 / 1.031 / 1.070 € (BIBB, PM 07.10.2026). Tarifverträge gehen vor.
- Mindestlohn, Minijob-Grenze, Praktikum, Werkstudent: `sonderfaelle.md` Abschnitt 1.
- **Einstiegsgehalt einschätzen:** Den BA-Entgeltatlas kannst du **nicht** selbst abrufen (interaktive Seite). Darum:
  1. Gehaltsangabe in der Anzeige (Pflicht in AT, in DE durch die EU-Entgelttransparenz künftig häufiger).
  2. **Ist Websuche an, nutze sie immer** (nicht aus dem Gedächtnis): Tarifvertrag der Branche (z. B. TVöD, IG Metall, Handel) oder seriöse Gehaltsangaben suchen und **mit Quelle (Link) und Stand** nennen; Jobportal-Zahlen als grobe Orientierung kennzeichnen. Beispiel: „Laut [Quelle] (Stand 05/2026) liegt TVöD SuE S 14 Stufe 1 bei … € brutto/Monat.“
  3. Ohne Websuche oder zum Selbstprüfen – Anleitung für den Nutzer: „Such im Browser ‚Entgeltatlas Arbeitsagentur‘ → Beruf eingeben → Region und Alter wählen → du siehst den Median (mittleres Gehalt).“
  Nie eine Zahl ohne Quelle nennen – auch keine unbelegten Einschätzungen („Tarif liegt eher oben“). Eine Spanne, die du vorschlägst, als **Vorschlag** kennzeichnen; in die Unterlagen kommt nur, was der Nutzer bestätigt.
- **Verhandeln:** Spanne im Bruttojahresgehalt, mit Quelle und Qualifikation begründen, unteren Wert realistisch; Benefits mitdenken. Bei Ausbildung wird selten verhandelt.
- **AT:** Lehrlingsentschädigung laut Kollektivvertrag; Gehalt in Anzeigen Pflicht. **CH:** kein gesetzlicher Lehrlingslohn auf Bundesebene, Branchenempfehlungen.

## 4. Absage

- Nicht persönlich nehmen: Oft entscheiden Kontingente, interne Kandidaten, Kleinigkeiten.
- Optional höflich um Feedback bitten (kein Anspruch) – Entwurf anbieten.
- **Mini-Auswertung** (eine Frage): „Wo kam die Absage? a) nach den Unterlagen b) nach dem Test c) nach dem Gespräch d) keine Antwort“ → a) Unterlagen gegen die Anzeige prüfen · b) Testtraining (`assessment_center.md`) · c) Gespräch üben, Fokus auf schwache Antworten · d) nachfassen, parallel weiter.
- Häufen sich Absagen: Unterlagen prüfen lassen (BA-Berufsberatung, Jobcenter, Career Service), Zielauswahl überdenken. Ehrlich: Berufseinsteiger suchen derzeit oft 9–15 Monate (t3n, 09/2026).

Zum Schluss: JSON (`bewerbungen`, `status`, `naechste_schritte`) aktualisieren, `akte.py`, und anbieten: „Gleiches Profil, neue Stelle – schick mir den Link.“ Für die neue Stelle bleibt `profil` gleich; `ziel`, `anschreiben`, `formular`, `email`, `firmenfakten` werden neu befüllt.
