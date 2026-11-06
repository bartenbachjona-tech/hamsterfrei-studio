# Runde 2 (Skill v2) – zusammengeführte Befunde der 8 Simulations-Agenten (41 Sitzungen)

## A. Fakten-Check (wichtigster Block)
1. **Fehlalarme in jeder Sitzung** → „erst bei 0 ❌ zeigen“ unerfüllbar, Claude „belegt“ Fehlalarme weg (Check wird ausgehöhlt):
   - Namenserkennung über Zeilenumbrüche („Grüßen⏎Name⏎Anlagen“, „Würzburg⏎Kundinnen“, Überschrift+Label).
   - Zwei großgeschriebene Substantive gelten als Name („Minuten Zeit“, „Ihren Sachen“).
   - STANDARD-Wortliste enthält Umlaute, Vergleich erst nach Transliteration → „Mit freundlichen Grüßen“ immer ❌.
   - Eigene Feldtitel der Formular-Datei („max. 1000 Zeichen“, „Frühester Eintrittstermin“) als unbelegt gemeldet.
   - Führerschein-Regel trifft „13. Klasse am Gymnasium“.
   - „Wie aufmerksam geworden?“: jedes Wort ≥ 4 Buchstaben muss im Profil stehen.
   - Recherchierter Firmenfakt löst ❌ aus, wenn seine Wörter in der Stellenbezeichnung stehen, obwohl er nicht im Text ist.
   - Akte im Ausgabeordner gerät in Sammelprüfung.
2. **Übersieht Echtes**: gerundete Dauer geht durch, wenn dieselbe Zahl irgendwo in der Anzeige steht („Drei Jahre studiert“ bei 2 J. 11 M.); weiche Motiv-/Gefühlssätze ohne Zahl/Name („genau so möchte ich arbeiten“, „mehr Spaß als alles andere“, „Reisen ist kein Problem“, „oft“, „täglich“).
3. **Profil-JSON = Beleg, aber Claude füllt sie selbst** → geratene Monate (09/2018 aus „2018“, 01.12.2026 aus „ab Dezember“, 10/2020 aus Claudes eigenem Beispiel), „(B.A.)“, „Klasse B“, „1. Ausbildungsjahr abgeschlossen“, „Teilzeit 30 Std.“ aus „zwei Kinder“ gelten als belegt. Kein Abgleich mit dem Wortlaut der Nutzerantworten.
4. Spickzettel/Akte/Gesprächsvorschläge werden nicht geprüft („8 Jahre“ statt 7,5; Claude-Fragen als „Meine Fragen“).

## B. endcheck.py
5. `kern_firma()` schneidet Rechtsformen ohne Wortgrenzen und case-insensitiv („Krankenkasse“→„krankenkas“, „Augusta“→„a usta“, „Reisen“→„rei n“) → falsches ❌ Firmenname fehlt.
6. Verlangt Firmenname + vollständigen Stellentitel in Formularfeldern und E-Mail (die eigene Mail-Vorlage hat keinen) → Claude baut hölzerne Sätze/Werbezusätze ein, ändert freigegebene Texte ohne neue Freigabe.
7. Keine Flexion bei Stellenbezeichnung („…angestellten“, „zur Medizinischen Fachangestellten“).
8. Übersieht „würde ich mich sehr freuen“ und gebeugte Floskeln; „3–5 Sätze“-Hinweis bei Mail statt Anschreiben; Fehlalarme bei gescannten Zeugnissen in `--typ gesamt`, kein Typ für Anlagen-PDFs; „Beispiel ungenutzt“ nur Stichwortvergleich.

## C. Ablauf / Regeln
9. Unterlagen-PDFs vor der Freigabe erzeugt → v2/v3 nach einer Änderung („warum v3?“). Anschreiben vor Upload der Zeugnisse → Anlagen-Zeile unvollständig.
10. Akte: zu spät gespeichert (9–16 statt ~6 Antworten); kollidiert mit „Rolle nicht unterbrechen“; nach Phase 2 fehlt noch der Name. .txt und .pdf gleichnamig → falsche hochgeladen; zwei Akten in derselben Minute gleicher Name; Uploads (Zeugnisse) im neuen Chat weg, Akte speichert nur Pfade; Wechselgrund/Berufstest im lesbaren Teil fehlen; doppelte Klammern.
11. Eine-Frage-Regel bricht, wo zwei Skill-Stellen gleichzeitig etwas verlangen („Termin bestätigt?“ + Übungsmenü; Firmengrund + Zustimmung Firmenfakt; zwei Freigaben). Zählung „Frage X von Y“ uneinheitlich (Sprünge, vor Frage 3 unklar). ➡️-Zeile fällt oft weg.
12. Gerätefrage-Zeitpunkt ungeregelt, wenn der Nutzer direkt mit Link/Einladung kommt (kostet Nachricht, nervt).
13. Schnellmodus: unklar ob Gerätefrage, Fahrplan, Firmen-Recherche, Checkliste entfallen; Pflicht-Checkliste wurde weggelassen.
14. Budget: Berufstest + komplette Bewerbung 29–32 Nachrichten; Vielfrager ohne Strategie; kurze Ein-Wort-Nutzer am Handy bekommen sehr lange Claude-Nachrichten.
15. „Wie aufmerksam geworden?“ einmal abgeleitet statt gefragt; Websuche beim Gehalt nicht genutzt; Firmen-Recherche/Zustimmung ausgelassen.

## D. Dateien / Handy / Desktop
16. `pdf_zusammenfuegen.py`: benennt Zieldatei still um (Bindestrich→Unterstrich); Querformat-Fotos verkleinert hochkant; PDF-Anlagen nicht auf A4; `--einzeln` benennt Fotos nach Dateiname (IMG_4471.pdf); bricht ab, wenn Fassung in alt/.
17. „versand/“-Ordner existiert nach Download am Handy nicht; zu viele Dateien nebeneinander.
18. „Teilen → Kopieren“ in Job-Apps kopiert nur den Link; „Strg+A“ im Browser markiert ganzen Chat; keine Desktop-Anleitung für Download/Upload.
19. Spickzettel: Termin/Art/Ort ohne Trennzeichen, leere Felder „Aufgabe:  |“, Video-Tipps auch vor Ort, keine Lücken/schwierige Fragen, keine verbesserten Antworten aus dem Feedback, Mitbring-Liste fehlt, interne Vermerke/Umgangssprache („der Gruber“) ungefiltert, kein AC-Spickzettel, Textwand.
20. `unterlagen_erstellen.py`: Zeichengrenze doppelt in Formular-Überschrift; Kurzanschreiben ohne Anlagen-Zeile (nirgends dokumentiert); Foto als eigener Block schiebt Lebenslauf ~4 cm nach unten.

## E. Fachliche Lücken
21. Profil-JSON ohne Felder: Wechselgrund, Zertifikate (Staplerschein unter Führerschein), Studienabbruch-Grund, Fach-Motivation, Rohwortlaut.
22. Fehlend: Probearbeiten; Minijob-Kenntnisse-Frage; Bewerbung per WhatsApp; Portale, die nach Upload alles nochmal eintippen lassen; Upload-Limit „max. 3 Dateien“ (Bündel-Rezept); Werkstudent: 20 h inkl. anderer Jobs, Ende mit Exmatrikulation; kurze Übungsrunde (welche 5 von 8 Fragen); Termin bestätigen; Anzeige online aber nur Firmenname; bereits beantwortete geplante Frage.

## Was gut lief
Fallback blockierter Link, Prompt-Injection erkannt, Schnellmodus „alle Fragen auf einmal“ (Unterlagen nach 11 Nachrichten), Rückfragen-Regel, Ehrlichkeit bei Lücken/Abbruch/Gesundheit, HEIC, Transliteration, Akte-Rundreise, Layouts, Postkorb in Häppchen, Budget ≤ 25 ohne Berufstest meist eingehalten.
