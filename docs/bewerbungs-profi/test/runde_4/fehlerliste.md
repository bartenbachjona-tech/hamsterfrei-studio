# Runde 4 (Skill v4): 87,5 % zufrieden, 94 % Wiederkauf (n=48) – Befunde für v5

## Hauptursache: Wortlaut-Prüfung zu wörtlich → Texte umgangssprachlich/hölzern (22×)
- herkunft.py verlangt fast jedes Inhaltswort im Nutzerwortlaut → „seh ich“, „Ich red gern“, „mega Spaß“, „find ich toll“, „Kumpel“, „nix“, „Ubahn“, „Sa und So“, „Kfz Mechatroniker“, Tippfehler des Nutzers landen in Anschreiben; korrektes Deutsch („U-Bahn“, „nichts“, „samstags“, „zwei“, „abgeräumt“, „eingearbeitet“, „kommissioniert“) wird abgelehnt; 3–4 Prüfrunden je Text; Angaben fallen weg („5. Semester“, „7. Klasse“, „Dr.“).
- **v5-Prinzip: Fakten wörtlich, Formulierung frei.** Geprüft werden nur Behauptungen (Zahlen, Daten, Dauern, Namen, Abschlüsse, Tätigkeiten/Fähigkeiten, Häufigkeiten/Intensitäten wie täglich/immer/schnell/sehr gut, Gefühle/Motive, Kontakte zur Firma) – mit Lemmatisierung, Kompositum-/Partizip-Erkennung, Zahlwörtern, Synonym-/Umgangssprache-Wörterbuch (red→reden, seh→sehen, nix→nichts, ubahn→U-Bahn, sa→samstags, kumpel→Freund, cool/mega→gern/sehr nur als Stil, Tippfehler-Toleranz Levenshtein ≤ 2 für Wörter ≥ 6 Zeichen). Funktions-/Stilwörter frei. Ziel: Standarddeutsch in Unterlagen ist Pflicht.
- **Neuer Stil-Check im endcheck:** Umgangssprache/Chat-Kürzel/Tippfehler in Unterlagen → ⚠️ mit Vorschlag (Liste), Grammatik-Grundcheck (Verbzweitstellung grob, doppelte Wörter).
- Satztrenner: Ordinalzahlen (1. Februar, 5. Semester, 12. Klasse), Abkürzungen (Dr., St., ca., z. B., Nr., Str.), Raumnummern (2.14) nie als Satzende; Spickzettel darf „12.“ nicht verlieren.

## Bestätigungen & Belege
- Antwort „a“ / „1a“ / „a passt“ auf „a) Ja b) Nein“ = Ja; bestätigte Werte zählen in herkunft UND fakten_check automatisch (Zitat = bestätigter Wert), ohne Doku-Lücke.
- Titel/Funktionen aus Anzeige/Einladung (Dr., Leitung, Teamleitung) in Anrede/Spickzettel sind keine Nutzerangaben → kein ❌.
- Anzeigen-Anforderung + beliebiges Nutzerzitat darf keine Ich-Aussage belegen (Lücke schließen).
- Abgeleitete Zeitangaben („letztes Frühjahr“ → 2026) als Normalisierung mit Bestätigung, sonst ⚠️.
- „Krankenkassen“ (Tätigkeit) ≠ Gesundheit; Kita/Elternzeit als privat erkennen.
- Mail-Vorlagen aus abschicken.md müssen ohne Herkunft-Einträge durchgehen (Vorlagensätze als neutral markieren).
- „Deutsch (Muttersprache)“ nie ohne Nutzerangabe (5/6 Lebensläufe!) → Sprachen-Frage Pflicht oder Feld leer.

## Dateien
- `--einzeln`/`--buendeln`: .docx-Arbeitsdateien nicht neben die Versand-PDFs legen (eigener Unterordner „bearbeitbar“ bzw. .docx nur auf Wunsch) → am Handy genau EINE Datei je Unterlage.
- Spickzettel: „30 Min.“ der Gruppenübung ≠ Vorstellungsdauer; „Raum 2.14“ ≠ Datum; „bring“ ≠ Ort (Straßen-Regex mit Wortgrenzen/Großschreibung); Bestätigungsfrist ≠ Termin; Lücken-/Wechselgrund-Frage-Erkennung ohne Wort „Lücke“; fast leere Seite 2 (Mitbring-Liste) vermeiden; Kernbotschaften gegen Wortlaut prüfen („eingeschickt“ vs. „angeboten“).
- Lebenslauf: Lücken aus profil.luecken automatisch; langer Zeitraum-Text bricht Datumsspalte (umbrechen/kürzen + endcheck-Warnung); Enddatum in der Zukunft → Hinweis.
- Endcheck: Betreff nicht „auch Quereinstieg“ verlangen; Kurzanschreiben 150–200 Wörter konsistent.
- Zugesagte Änderungen: offene Änderungswünsche in Akte/JSON führen, vor dem Erzeugen abhaken (72 vergessen).

## Ablauf / Budget (10×)
- Nie „nur noch eine Frage“ sagen, wenn es nicht stimmt (423 Abbruch).
- Listen-Modus für knappe/ungeduldige Nutzer direkt anbieten (nicht erst nach Ja fragen).
- Chatwechsel-Hinweis nur, wenn nötig (lange Sitzung/Limit absehbar), nicht nach Frage 1 oder kurz vor Ziel; Akte ab Berufstest-Ergebnis erlaubt (Name später ergänzen).
- Minijob-Budget realistisch ≤ 12, AC-Pfad ≤ 40; Minijob: eine Freigabe für Text+Lebenslauf erlaubt; Checkliste 3 Zeilen.
- Woher-Liste ohne interne Nummern („Nr. 7“) – nur „deine Worte: …“.
- Kontaktfrage fragt E-Mail mit; Portal-Felder im Schnellmodus nur bei Formular-Bewerbung erfragen.

## Fachliches
Tier-Berufe, Zweiradmechatroniker in Vorschlagslisten; „Wir duzen uns“-Regel (Anschreiben trotzdem höflich-neutral, Du nur wenn Firma ausdrücklich duzt); Werkstudent > 30; Abschweifen im Rollenspiel kurz zurückholen.
