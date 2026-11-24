# Claude-Antwort Notenrechner (frischer Kontext, 24.11.2026 ~13:10, Studio-Sitzung, Agent nur mit Schreibzugriff, eine Antwort ohne Nachbesserung)

## Eingabe (wörtlich, ein Satz)
„Bau mir einen Notenrechner fürs Halbjahr, in den ich pro Fach meine Noten eintrage, wobei Schulaufgaben doppelt und mündliche Noten einfach zählen, und der mir den Schnitt pro Fach und insgesamt anzeigt.“

## Ergebnis
- Rechner als eine HTML-Datei: `docs/plaene/beispiel/schnitt_rechner_claude.html` (unverändert).
- Chat-Text (wörtlich, gekürzt um die Bedienliste): „Hier ist dein Notenrechner fürs Halbjahr! … Zum Gesamtschnitt: Er ist der Durchschnitt aus deinen Fachschnitten, **jedes Fach zählt also gleich viel.** Wenn bei euch manche Fächer stärker zählen sollen, zum Beispiel Hauptfächer doppelt, oder wenn du Tendenznoten wie 2+ oder 3- eintragen willst, sag Bescheid, dann baue ich das ein.“
- Vorbelegt: Deutsch, Mathematik, Englisch, Biologie, Geschichte; Noten per Knopf 1–6; zeigt die Rechnung pro Fach; speichert im Browser.

## Test mit den Beispielnoten (Playwright, 24.11.2026, Knöpfe geklickt)
| Fach | Rechner | Handrechnung |
|---|---|---|
| Deutsch (SA 2 · m 3, 2) | 2,25 | 9/4 = 2,25 ✓ |
| Mathematik (SA 4, 3 · m 2) | 3,20 | 16/5 = 3,20 ✓ |
| Englisch (SA 3, 2 · m 2, 1) | 2,17 | 13/6 = 2,17 ✓ |
| Biologie (keine SA · m 2, 3) | 2,50 | 5/2 = 2,50 ✓ |
| Geschichte (leer) | – (übersprungen) | ✓ |
| **Gesamt** | **2,53** („befriedigend“, 4 Fächer) | 2,53 ✓ |

## Auswertung gegen die vorher notierten Prüfpunkte
1. ✓ Schulaufgaben zählen doppelt (Mathe 3,20, nicht 3,00).
2. ✓ Fach ohne Schulaufgabe (Bio) → 2,50.
3. ✓ Fächer hinzufügen/löschen.
4. ✓ Gesamt 2,53 = Handrechnung.
5. ✓ Nur Knöpfe 1–6, leeres Fach wird übersprungen.
- **Schwäche (echt, von Claude selbst genannt):** Im Gesamtschnitt zählt jedes Fach gleich. Bio mit zwei mündlichen Noten wiegt so viel wie Mathe mit zwei Schulaufgaben. Keine Tendenznoten (2+, 3-).
- Urteil: GEKLAPPT (5/5), Haken: alle Fächer gleich schwer.
