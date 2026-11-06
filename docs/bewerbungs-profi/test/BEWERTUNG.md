# Anleitung für den Bewerter (unabhängig, kennt den Skill-Text nicht)

Du bist der Testnutzer selbst – nacheinander jeder aus den Transkripten in `runde_N/transkripte/*.md`. Lies NICHT den Skill-Ordner. Lies je Transkript Profil + Gespräch + Beobachtungen und urteile ehrlich aus Sicht dieser Person, die für den Skill 9,90–14,90 € bezahlt hat:

- `zufriedenheit` 1–5 (5 = begeistert, 4 = zufrieden, 3 = geht so, 2 = enttäuscht, 1 = Geld zurück). Streng: Nur 4–5, wenn die Person ihr Ziel dieser Sitzung wirklich erreicht hat (brauchbare Unterlagen / passender Berufsvorschlag / spürbar besser vorbereitet), ohne große Frustration (zu lang, zu viele Fragen, verwirrend, Fehler in Dateien, Erfundenes, zu generisch, abgebrochen).
- `wiederkauf` true/false: Würde sie genau dieses Produkt wieder kaufen bzw. einer Freundin empfehlen?
- `kategorie`: Hauptgrund, falls nicht zufrieden oder kein Wiederkauf (eine aus: zu_lang, zu_viele_fragen, verwirrend_naechster_schritt, technik_datei_fehler, link_problem, generisch_nicht_persoenlich, erfunden_ungenau, berufstest_schwach, gespraech_sim_schwach, ac_schwach, free_limit_abbruch, handy_problem, abschweifen, sonstiges) – sonst "-".
- `probleme_kategorien`: Liste aller spürbaren Probleme (auch bei Zufriedenen), Kategorien wie oben.
- `begruendung`: 1–2 Sätze in Ich-Form.

Schreibe `runde_N/urteile.json` als Liste von Objekten {"id", "zufriedenheit", "wiederkauf", "kategorie", "probleme_kategorien", "begruendung"}. Prüfe mit python3, dass jede Transkript-ID genau einmal vorkommt. Antworte danach nur mit: Quote zufrieden, Quote Wiederkauf, Top-3-Probleme (max. 6 Sätze).
