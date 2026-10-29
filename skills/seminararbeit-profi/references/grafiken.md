# Grafiken (Modus 6)

## Inhaltliche Regeln (die häufigsten Kritikpunkte von Lehrkräften)

- Alles auf **Deutsch:** Achsentitel, Monate, Legende.
- **Achsen beschriften, mit Einheit,** zum Beispiel „Niederschlag (in mm)“, „Anteil am BIP (in %)“, „Jahr“.
- **Kein Titel und kein Logo im Bild.** Der Titel steht in der Beschriftung darunter: „Abbildung n: Titel“.
- **Die Quelle steht in der Fußnote zur Beschriftung,** nicht als Text unter dem Bild:
  - „Eigene Darstellung nach Statistisches Bundesamt 2025a.“
  - „Eigene Berechnung und Darstellung nach …“
- Ist eine Grafik mit KI-Hilfe erstellt und verlangt die Schule eine Kennzeichnung: Zusatz „(mithilfe von KI erstellt)“ in der Beschriftung. Die Lehrkraft fragen, ob sie das will.
- Fortlaufend nummerieren. Jede Abbildung wird im Text **vor** ihrem Erscheinen erwähnt: „(vgl. Abbildung 3)“. Nach dem Einfügen oder Löschen alle Nummern und Verweise anpassen.
- Datenprobleme offenlegen:
  - vorläufige Werte mit Sternchen und hellerer Farbe
  - fehlende oder offensichtlich falsche Werte als Lücke, mit Erklärung in der Fußnote
- Richtig runden, x,5 kaufmännisch. Pythons `round` macht das nicht.
- Fotos nur mit freier Lizenz (CC0, CC BY, CC BY-SA), zum Beispiel von Wikimedia Commons. Urheber, Datum und Lizenz in die Fußnote.
- Wo es passt, ist eine **Karte** besser als ein Foto. Klimadaten gehören in ein **Klimadiagramm.**

## Diagrammtypen

| Daten | Diagramm |
|---|---|
| Entwicklung über Zeit | Linie, evtl. mit leichter Fläche; wenige beschriftete Schlüsseljahre |
| Vergleich von Kategorien | Balken, nach Größe sortiert |
| Anteile | Balken mit % (Torten nur bei 2–4 Teilen) |
| Temperatur + Niederschlag | Klimadiagramm (Balken mm links, Linie °C rechts, Jahresmittel und -summe als Text) |
| Regionale Werte | Choroplethenkarte, 3–5 sinnvolle Klassen, keine leere Klasse in der Legende |
| Saisonalität | Balken je Monat |

## Einheitlicher Stil (matplotlib)

- Schrift: Liberation Sans bzw. Arial, dpi 300, Größe ca. 16 × 9 cm (`figsize=(6.3, 3.6)`). Speichern mit `bbox_inches="tight"`.
- Farben:
  - Text #0b0b0b, Nebentext #52514e, Gitter #d9d8d4
  - Hauptfarbe #2a78d6, hell #9cc2ee
  - Karten-Klassen #e3eefb, #9cc2ee, #1f5fae
  - Markierungen #f2b632
- Nur die untere Achse ist sichtbar, ohne Tick-Striche. Ein helles horizontales Gitter liegt hinter den Daten.
- Werte direkt an Balken oder Punkte schreiben, 7,5–9 pt, mit Dezimalkomma (`f"{v:.1f}".replace(".", ",")`).
- Karten:
  - Geodaten von Natural Earth (admin1) oder amtliche Geodaten
  - Orte mit verifizierten Koordinaten, zum Beispiel aus OpenStreetMap; den richtigen Treffer wählen
  - kleine Regionen mit Hinweislinie beschriften
  - Maßstab und Legende unter der Karte
- Ist keine Netzverbindung für Geodaten da: den Nutzer um die Datei bitten oder eine einfache Lageskizze vorschlagen.

## Ablauf

1. Daten aus der Quelle übernehmen und als Tabelle zeigen. Bei eigener Berechnung den Rechenweg angeben.
2. Diagramm rendern und **selbst ansehen.** Prüfen:
   - keine Überlappungen
   - Legende nicht abgeschnitten
   - Achsen beschriftet
   - Dezimalkomma
3. Als PNG ausgeben, mit dem Vorschlag für die Beschriftung und die Fußnote. Auf Wunsch direkt in die .docx einfügen: zentriert, ca. 14,5 cm breit, die Beschriftung darunter mit dem Bild zusammengehalten.
4. Daten und Quelle der Grafik kommen in die Belege („Grundlage Abb. n“).
