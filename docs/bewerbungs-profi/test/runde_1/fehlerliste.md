# Runde 1 – zusammengeführte Befunde der 8 Simulations-Agenten (41 Sitzungen)

## A. Inhalt / Verhalten
1. **Erfundenes/Aufgeblähtes trotz Verbot** (in fast jedem Paket): Monate ohne [PRÜFEN], Führerschein, „acht Jahre“ statt 7,5, LinkedIn-Adresse, „mitkonzipiert“, Leistungsfächer, STAR-Geschichten ausgeschmückt, Firmenfakten aus Recherche ohne Kennzeichnung, geratene Antwort auf „Wie aufmerksam geworden?“. [PRÜFEN] wird als Rechtfertigung für eigene Vorschläge missbraucht. Kein Skript erkennt das.
2. **„Eine Frage pro Nachricht“ vom Skill selbst gebrochen**: Frage 9 „Rahmen“ (Start+Foto+Hobby), Frage 4 „pro Station“, Nachhaken, Rückfrage beantworten + nächste Frage anhängen; Zählung „Frage X von Y“ verrutscht.
3. **Hinweis-Block** stört in Rollenspielen/Simulation, wird zu lang (>3 Zeilen mit Akten-Pflichtsatz), fehlt teils.
4. **Free-Plan-Limit** in ~12 von 41 Sitzungen erreicht; Skill plant keine Chat-Aufteilung, warnt nicht; Akte nur nach großen Schritten → Antworten/Feedback verloren.
5. **Schnellmodus („mach einfach“) ungeregelt**: Freigaben, Endcheck, Gesprächsvorbereitung fallen weg.
6. **Gesammelte Beispiele** (Fußball, Kapitän) landen nicht in den Unterlagen.
7. **Freigegebene Änderung kam nicht in der Datei an**; alte Version v1 statt v2 in Gesamt-PDF abgeschickt.
8. **Anlagenliste** im Anschreiben nicht mit echten Anlagen abgeglichen.
9. **Check-U/BERUFENET/Berufsberatung** nach Berufstest teils vergessen.

## B. Handy/Tablet/Anfänger
10. Gerät wird nie abgefragt; Anleitungen setzen Strg+C/Strg+P voraus; Download/Upload am Handy nicht erklärt.
11. `.md` (Akte, Spickzettel) am Handy/Windows nicht zu öffnen; Spickzettel-PDF zeigt `#`/`**`; `.docx` am Handy nutzlos.
12. Postkorb mit 10–12 Dokumenten in einer Nachricht am Handy kaum machbar (Abbruch).
13. HEIC-Fotos abgelehnt bzw. still übersprungen; Zeugnisfotos nicht A4/unbeschnitten.
14. Anzeige als Screenshot hochladen als Fallback fehlt.

## C. Skripte
15. `endcheck.py`: Warnung „E-Mail seriös?“ bei jeder Adresse; eigener/früherer Arbeitgeber als Copy-Paste-Rest; Firmenname nur exakt inkl. Rechtsform; Stelle nur erstes Wort; Formular-.txt als Lebenslauf erkannt (❌ keine E-Mail, Feldtitel als Platzhalter); Prüfungen hängen am Dateinamen; volles Anschreiben als „Kurzanschreiben“ gewertet; .txt-Formulartexte sonst ungeprüft.
16. `unterlagen_erstellen.py`: Nicht-ASCII-Buchstaben aus Dateinamen gelöscht (ć ş ë ı Ç); Firmenname nach 30 Zeichen mitten im Wort abgeschnitten; kein Dokumenttyp Motivationsschreiben; [PRÜFEN]-Zählung über ganzes JSON statt pro Dokument; [PRÜFEN] im Zeitraum verschiebt Layout; _v2-Dateien ohne klaren Hinweis, welche aktuell ist; blaue statt graue Linie unter Titel.
17. `pdf_zusammenfuegen.py`: fehlende Datei → trotzdem ✅/Exit 0; HEIC übersprungen mit ✅; Fotos nicht auf A4; Umlaut-Ersatz inkonsistent; keine Warnung, wenn ältere Version gewählt wird.
18. `berufstest_auswerten.py`: nennt S+C, I+C, A+E, I+S „eher gegensätzlich“ – falsch (gegenüber im Hexagon nur R–S, I–E, A–C).
19. `ordner_anlegen.py --nur-akte`: schreibt fest nach /mnt/user-data/outputs, keine `--ausgabe`, bricht ab/überschreibt nicht bei vorhandener Akte, erzeugt nur leere Vorlage statt aus Daten befüllter Akte.
20. `textlib.py --info` erkennt Spalten/Tabellen in PDF-Lebensläufen nicht (Behauptung in lebenslauf.md falsch).

## D. Lücken im Fachinhalt
21. Keine Berufsvorschläge für Absolventen, Quereinsteiger, Werkstudenten, Minijob; RIASEC-Tabelle ohne IS/SI u. a.; 14 Fragen zu viel für Minijob/Praktikum (Kurzweg nötig).
22. Fehlend: Wiedereinstieg, Teilzeitausbildung, Studienabbruch, Lücken-Feld, Initiativbewerbung, Anzeige offline, mitgebrachter ChatGPT-Text, ältere Bewerber (Sie/Du, Schulabschluss-Frage), private Angaben (Kinder) nur nach Rückfrage, Werkstudenten-Regeln (20 h, KV), Minijob-Grenze/Mindestlohn, PiA, Telefon-/Video-/technische Interviews, Kinderbetreuung als unzulässige Frage, AC-Einladung bestätigen mit Frist, Upload-Limits im Formular („max. 2 Dateien“), AC-Menü an Einladung anpassen.
23. Gehalt: Verweis auf Entgeltatlas, den Claude nicht abrufen kann → Websuche mit Quelle oder klare Anleitung.
24. Rechtliches: konkrete Fristen (Elternzeit) über allgemeine Einordnung hinaus.

## Was gut lief (beibehalten)
Fallback bei blockiertem Link; versteckte KI-Anweisung in Anzeige erkannt und ignoriert; Fortsetzung über Akte; PDF-Layout sauber, einspaltig, 1 Seite.
