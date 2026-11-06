# Zuschauer-Test (Pflicht für JEDES Video, Jona 06.11.2026)

Vor jedem Post prüft ein simuliertes Panel aus 1.000 Zuschauern: **Schauen sie zu Ende? Gehen sie auf die Website? Würden sie kaufen? Und wenn nein – warum nicht?** Gilt für alle Hamsterfrei-Videos (mit und ohne Werbung, auch Tagesproduktion und Sonderfolgen). Ergebnis ist eine Richtgröße zum Vergleichen und Verbessern, keine Prognose – so auch an Jona melden.

## Wann
Nach dem Bild-Kritiker (PRODUKTION.md Schritt 7), vor der Checkliste (Schritt 8). Kostet keine ElevenLabs-Credits.

## Eingaben (nur das, was ein Zuschauer sieht)
- Kontaktbogen A (Hook) und B (ganzes Video) aus Schritt 7, Cover.
- Gesprochener Text mit Zeitmarken (aus `src/folgen/<folge>.words.json`) und Bildschirmtexte.
- Caption (TikTok/Instagram) und Bio-Link-Ziel.
- Wenn das Video auf eine Seite führt: Kurzfassung der Zielseite (Überschrift, Preis, „Was drin ist“, Hinweise wie „ab 18“, Widerruf) aus `site/pages/*.src.html` – so, wie der Zuschauer sie nach dem Klick sehen würde.
- NICHT: Skript-Notizen, Kritiker-Urteile, Absichten.

## Panel
- Personen: `docs/produktsim/personas.json` (50 Archetypen, gewichtet = 1.000 Zuschauer; Querschnitt des Hamsterfrei-Publikums inkl. Unter-18-Jähriger und Nicht-Zielgruppe).
- **2 Agenten** (frischer Kontext, je 25 Archetypen, `model` Standard), Auftrag wörtlich aus `docs/video_test/AUFTRAG.md`. Sie urteilen je Persona als Zuschauer in der For-You-Page bzw. aus der Suche (Szenario steht im Auftrag).
- Je Persona: `bis_ende` (0–100), `website` (0–100: Profil → Link → Seite), `kauf` (0–100; bei Videos ohne Produkt: `folgen` statt `kauf`), `grund_weg` / `grund_kein_klick` / `grund_kein_kauf` (Kategorie aus der Liste unten), `satz` (max. 12 Wörter, Ich-Form).
- Auswertung: `python3 scripts/video_panel.py docs/video_test/<folge>/` → `bericht.md` (gewichtete Quoten pro 1.000, Top-3-Gründe je Stufe, die 3 aussagekräftigsten Sätze, Vergleich mit den letzten 5 Tests aus `docs/video_test/verlauf.csv`).

## Gründe-Kategorien
`kein_bedarf` · `nicht_zielgruppe` (Alter, Bundesland, Schulart) · `hook_schwach` (weggewischt in 1–2 s) · `unklar_worum` · `unklar_was_produkt` · `werbung_misstrauen` · `preis_unbekannt_oder_zu_teuer` · `gratis_alternative` (ChatGPT etc.) · `ki_skepsis_oder_verbot` · `kein_claude_konto` · `zu_lang_langweilig` · `link_umstaendlich` · `spaeter_vielleicht` · `sonstiges`

## Entscheidung
- Ist ein Grund aus dem Video selbst behebbar (hook_schwach, unklar_worum, unklar_was_produkt, link_umstaendlich, zu_lang) und betrifft ≥ 15 % der Abspringer einer Stufe → **eine** Nachbesserungsrunde (Schnitt/Text/Overlay/Caption), danach erneut testen. Neue Vertonung nur, wenn ohne sie nicht lösbar (Credits sparen, Jona fragen bei Werbe-Videos).
- Nicht behebbare Gründe (kein_bedarf, nicht_zielgruppe) nur dokumentieren – sie sagen, ob Thema/Zielgruppe passen.
- Ergebnis (3 Zahlen + Top-Gründe) gehört in die Freigabe-Nachricht an Jona, ins Skript (`scripts/<folge>.md`, Abschnitt „Zuschauer-Test“) und in `state/log.md`.
- Nach 48 h echte Zahlen (Aufrufe, Profilaufrufe, Link-Klicks soweit sichtbar, Verkäufe) neben die Panel-Zahlen in `docs/video_test/verlauf.csv` schreiben → Kalibrierung über die Zeit.
