# Folge 13 · Hamster-Test „Notenrechner aus einem Satz“ (Composition Folge13)

- Datum: 24.11.2026, Termin 18:00 · Phase 2 · **Kernserie (a) „Hamster-Test“**, Feld Schule/Zeit. Rohstoff T25.
- **Testvariable (AUSWERTUNG_AKTUELL, Testdesign ab 23.11.): Einstiegs-Test, Variante E1, Paar 1** (E2 = Folge12 am 23.11., Los 23.11.). Frame 0 nach LOOK.md: Hamster (startle, Zeigestab) + echtes Ergebnis auf der Leinwand, Overlay ≤ 6 Wörter, normales Episode-Layout (keine Vollbild-Ebene). Hook-Satz im Paar gleich gebaut wie F12 (Experimenter: Situation + „Ich hab Claude … lassen.“ + offene Frage). Ziel 30–35 s, ohne Werbung, Musik gleich. N/K: K.
- **Thema:** kein Los nötig: T25 ist das einzige offene Thema, das ohne Jona bzw. echte Messdaten produzierbar ist (T8 braucht ein echtes Foto, T19 Jonas Rätsel-Test, T23/T24 Jonas Daten, T11/T15/T18/T21 warten). Im Log so vermerkt.
- **Werbung: NEIN.** Quote: letzte 5 (F12, F11, F10, F09, F08) ohne Werbung.
- Kommentar-Wort: **SCHNITT** → DM mit dem Satz zum Kopieren + Mini-Check (docs/plaene/SCHNITT.md), kein Kauflink.
- Suchbegriff: „Notenrechner“ / „Notendurchschnitt berechnen“ in Caption-Zeile 1 und klein im Bild.
- Ideen-Trichter (≥ 3): (1) T25 Notenrechner ✓ (echtes Artefakt, nachgerechnet, echte Schwäche); (2) T8 Verkaufsfoto (braucht echtes Foto) → raus; (3) T19 Zahlenschloss (Jona muss spielen) → raus.
- Ausschluss-Check SERIEN (a): echtes Ergebnis ✓ (frischer Kontext 24.11., schnitt_rechner_claude.html, per Playwright mit Beispielnoten getestet), kostenlos/DE ✓, keine Schularbeit schreiben lassen ✓ (Werkzeug), keine Daten Dritter ✓ (Ben erfunden, „BEISPIEL“), Zahlen aus Test + Handrechnung ✓, Aufgabe neu in den letzten 10 ✓.

## 1. Pointe zuerst (G3)
Aus einem einzigen Satz baut Claude einen funktionierenden Notenrechner. Von Hand nachgerechnet stimmt alles (Mathe 3,20, Bio ohne Schulaufgabe 2,50, gesamt 2,53). **Haken:** Im Gesamtschnitt zählt jedes Fach gleich, Bio mit zwei mündlichen Noten wiegt so viel wie Mathe. Urteil **GEKLAPPT – nur sind alle Fächer gleich schwer.**

## 2. Schlüsselbild Frame 0 (G1, E1)
Leinwand: der Rechner (Nachzeichnung von Claudes echtem Rechner, gleiche Werte und Namen): oben groß „Gesamtschnitt 2,53“, darunter Fach-Kärtchen Deutsch 2,25 · Mathematik 3,20 · Englisch 2,17 · Biologie 2,50. Klein „BEISPIEL · Nachzeichnung“. Keine Bewegung am Ergebnis vor Ende des startle (E1). Hamster (startle) zeigt mit dem Zeigestab auf die Leinwand. (R1-Korrektur 1: Haken + Sprechblase gestrichen, Haken erst in Szene 3.) Overlay oben: **„1 Satz → Notenrechner“**, klein „HAMSTER-TEST · Notenrechner Halbjahr“.

## 3. Hook-Varianten (G2, ≥ 2 Formate)
1. **Experimenter (gewählt, gleich gebaut wie F12: Dreier-Situation + „Ich hab Claude … lassen.“ + Teaser auf den Haken):** „Zwölf Noten, vier Fächer, ein Satz. Ich hab Claude einen Notenrechner bauen lassen. Ein Fach zählt dabei zu viel.“ (12 = 3 + 3 + 4 + 2 Noten) – A: „ein Satz reicht nie für ein Programm“ gegen B: fertiger Rechner im Bild. (R1: zuerst „Ein Satz, mehr nicht. … Aber rechnet der richtig?“ – nicht gleich gebaut wie F12.)
2. Fortune Teller: „Im Februar willst du wissen, wie dein Halbjahr steht. Den Rechner baust du dir heute mit einem Satz.“ – weniger Kontrast, Thema später klar.
3. Investigator: „Dieser Notenrechner rechnet richtig. Trotzdem stimmt ein Teil nicht so, wie du denkst.“ – verrät den Haken zu früh.
Gewählt: 1 (Paar-Regel: Hook-Satz-Typ wie F12; größter Kontrast).

## 4. Sprechtext (eleven_v3, 1 Take, ~85 Wörter)
[excited] Zwölf Noten, vier Fächer, ein Satz. Ich hab Claude einen Notenrechner bauen lassen. Ein Fach zählt dabei zu viel.
Mein Satz: Schulaufgaben doppelt, mündliche Noten einfach.
Bens Mathe: Schulaufgaben vier und drei, mündlich eine Zwei.
Rechner: drei Komma zwei. Von Hand: auch drei Komma zwei.
Bio ohne Schulaufgabe klappt auch.
Gesamt zwei Komma fünf drei. Stimmt.
Aber jedes Fach zählt gleich. Bio mit zwei mündlichen Noten wiegt so viel wie Mathe.
[calm] Urteil: Geklappt. Nur sind alle Fächer gleich schwer.
Kommentier Schnitt, dann schick ich dir den Satz zum Kopieren.

Untertitel: Zahlwörter per captionMap als Ziffern („Zwölf“ → „12“, „vier“ → „4“ …); „drei Komma zwei“ und „zwei Komma fünf drei“ werden in der words.json zu je einem Untertitel-Wort „3,20“ bzw. „2,53“ zusammengezogen; „Schnitt,“ → „SCHNITT,“.

## 5. Szenenplan (Leinwand 948×1004)
0. Hook bis „zu viel.“: Rechner (Schlüsselbild); bei „Ein Fach zählt dabei zu viel“ wird das Biologie-Kärtchen kurz hervorgehoben.
1. „Mein Satz …“: Chat-Blase mit dem echten Satz, „doppelt“ und „einfach“ grün markiert, Rechner fliegt als Antwort-Kärtchen ein.
2. „Bens Mathe …“: Mathe-Karte im Rechner-Look, Chips SA 4 · 3, mündlich 2 poppen nacheinander; Stempel „BEISPIEL · Ben ist erfunden“.
3. „Der Rechner sagt …“: links Rechner-Badge 3,20, rechts karierter Zettel mit Handrechnung (4·2 + 3·2 + 2) ÷ 5 = 3,20, Haken.
4. „Bio …“: Bio-Karte „Schulaufgaben: noch keine“, Badge 2,50 ✓.
5. „Gesamtschnitt …“: große 2,53, Zettel „von Hand 2,53 ✓“.
6. „Aber jedes Fach …“: Waage, links Bio (2 mündliche), rechts Mathe (2 Schulaufgaben + 1 mündlich), Waage im Gleichgewicht, rot „Bio zählt wie Mathe“, klein „hier trotzdem 2,53“, Zitat Claude „jedes Fach zählt also gleich viel“.
7. Urteil: Stempel GEKLAPPT, „Doppelt zählen ✓ · Ohne Schulaufgabe ✓ · Gesamt richtig ✓ · Fächer gleich schwer ✗“.
8. CTA: Handy „Satz zum Kopieren“ + Kommentarblase „SCHNITT“ + Ding.

## 6. Echtes Beispiel
- Eingabe, Beispielnoten, Handrechnung, Prüfpunkte: docs/plaene/beispiel/schnitt_beispiel.txt
- Claude-Antwort, Rechner-Datei, Testergebnis: docs/plaene/beispiel/schnitt_claude_antwort.md, schnitt_rechner_claude.html

## 7. Quellen
- Keine externen Zahlen. Alle Werte aus dem Playwright-Test des echten Rechners und der Handrechnung. Gewichtung „Schulaufgabe doppelt“ ist Bens Wunsch, keine Regel (in Caption „deine Gewichtung“).

## 8. Overlay, Cover, Caption
- Overlay Frame 0: „1 Satz → Notenrechner“ + klein „HAMSTER-TEST · Notenrechner Halbjahr“.
- Cover: Frame 0 (Standard).
- **Caption (TikTok):** Notenrechner fürs Halbjahr mit Claude, aus einem einzigen Satz 🐹 Hamster-Test: Schulaufgaben doppelt, mündliche Noten einfach. Ich hab Bens Noten eingetippt und von Hand nachgerechnet: Mathe 3,20, Bio ohne Schulaufgabe 2,50, gesamt 2,53, alles stimmt. Haken: Im Gesamtschnitt zählt jedes Fach gleich viel. Kommentier SCHNITT, dann schick ich dir den Satz zum Kopieren. Ben und seine Noten sind erfunden (Beispiel). Gewichtung nach deinen eigenen Regeln anpassen. Claude-Konto ab 18. KI-animiert. #notenrechner #notendurchschnitt #schule #claude #hamstertest
- **YouTube-Titel:** Notenrechner aus einem Satz: rechnet Claude richtig? Hamster-Test #shorts
- **YouTube-Beschreibung:** Hamster-Test: Ein Satz an Claude, und ich hab einen Notenrechner fürs Halbjahr. Schulaufgaben doppelt, mündliche Noten einfach, von Hand nachgerechnet: Mathe 3,20, gesamt 2,53, stimmt. Haken: Jedes Fach zählt im Gesamtschnitt gleich. Kommentier SCHNITT, dann antworte ich dir mit dem Satz zum Kopieren 🐹 Person und Noten erfunden. Claude-Konto ab 18. KI-animiert. #notenrechner #shorts

## 9. Erwartung (G7, unbeworben, E1)
- TikTok 400–750 Aufrufe/48 h, Ø 3,5–4,5 s (E1), ganz 1–2,5 %. YouTube 20–100. Instagram pausiert (Auswertung 23.11.), nicht gepostet.

## 10. Text-Kritiker (fable, frischer Kontext, 24.11.)
- R1: Tore 1–4 ja (1 knapp), **Tor 5 nein** (Haken in Frame 0 beantwortet die Hook-Frage vorab). Rubrik **7**/8/9/9/8/9/9/**6** → Ø 8,1, Krit. 1 < 8 → **überarbeiten**. Gründe: Frame 0 überladen + E2-Merkmal (Haken bewegt sich am Ergebnis), 98 Wörter zu lang, Hook nicht wie F12 gebaut. Belege alle korrekt.
- Übernommen: Korrekturen 1–6 (Frame 0 entschlackt, Hook „Zwölf Noten, vier Fächer, ein Satz …“, Alter raus, Nachrechnen/Mitte gestrafft, Waage „Bio zählt wie Mathe / hier trotzdem 2,53“). Abweichung: „Ein Fach zählt dabei zu viel“ statt „wiegt zu viel“ (passt zur Pointe „zählt gleich“).
- R2 (Abgleich durch Studio wie F07–F12): alle Korrekturen umgesetzt, ~85 Wörter, jede Zahl deckt sich mit schnitt_claude_antwort.md, Frame 0 ohne E2-Merkmal → **freigegeben**.

## 11. Produktion 24.11.2026
- Stimme: Flow idZ0QGkgpeqyoM79NSdg, Generation jaN5xvMgdMBVNi6N9FiG, 1 Take eleven_v3, **582 Credits**, 33,0 s, unbearbeitet, erstes Wort „Zwölf“ bei 0,07 s. Scribe 0 Credits (src/folgen/folge13.words.json; „drei Komma zwei“ → „3,20“, „zwei Komma fünf drei“ → „2,53“ als Untertitel-Wort). Video **34,9 s**. Kontostand nicht abgefragt.
- E1-Umsetzung: normales `Episode` mit `startle`, Rechner ab Frame 0 auf der Leinwand, keine Bewegung am Ergebnis bis 4,2 s (Biologie-Markierung + „zählt Bio zu viel?“).
- Bild-Kritiker (fable, frischer Kontext): R1 **pass 8/10**, Stumm-Test ja (Spannung knapp). Übernommen: Frage „zählt Bio zu viel?“ größer (ab 4,2 s), Auftragstext größer, Waage ohne Mini-Notiz + Claude-Zitat größer, Urteils-Checkliste größer, Kennung nur „HAMSTER-TEST“; Untertitel „3,2.“ → „3,20.“. Nicht umgesetzt: Zeigestab-Richtung (fester Code-Baustein Hamster, LOOK.md: nur schrittweise ändern). Inhaltlich „GEKLAPPT trotz ✗“ bleibt (5/5 Prüfpunkte, Haken ändert Bens Ergebnis nicht).
- Zuschauer-Test: **134 bis Ende / 11 Website / 18 folgen pro 1.000** (Wegwischen kein_bedarf 49 %, nicht_zielgruppe 44 %, zu_lang 7 % – nicht behebbar bzw. < 15 %). Niedrigster Wert seit F08: Panel bemängelt „Schulaufgaben“ = bayerisch, Q12/13 rechnet in Punkten, Notenrechner-Apps gratis.
- G10: Schlüsselbild ✓ (E1), Hook-Tore ✓, 3 Hook-Varianten ✓, Pointe zuerst ✓, Signatur (Serienname in Bild/Titel/Caption) ✓, Serie (a) ✓, Testvariable E1/Paar 1 ✓ (34,9 s, Hook gleich gebaut wie F12), Cover ✓ (Frame 0), Erwartung ✓, Sicherheit ✓ (keine Werbung, Person erfunden, Claude ab 18, KI-Label), Zuschauer-Test ✓.
- Datei out/hamsterfrei-folge13-schnitt.mp4 (nicht im Repo), Cover out/cover-folge13.png.
- Termine (Wiederholversuch 15:30, Chrome 2d7e7af3…, Konto hamsterfrei per Account-Info / #entity-name Hamsterfrei geprüft): TikTok geplant **24.11. 18:00** https://www.tiktok.com/@hamsterfrei/video/7711746350081117462 (KI-Label an, keine Offenlegung) · YouTube Short geplant **24.11. 18:00** https://youtube.com/shorts/vzD4JNUGqxY (nicht für Kinder, KI = Ja, keine bezahlte Werbung) · Instagram pausiert (Auswertung 23.11.), nicht gepostet. Cover: Standard (Frame 0).
