# Phase 1: Berufstest

## Inhalt
1. Welcher Weg?
2. Standard: der Block mit 12 Aussagen
3. Kurzweg (Minijob, Praktikum, Nebenjob)
4. Auswertung und 3 Vorschläge
5. Vorschlagslisten (Einzeltypen, alle 2-Buchstaben-Codes, besondere Gruppen)
6. Immer am Ende: Check-U, BERUFENET, Berufsberatung

---

## 1. Welcher Weg?

- **Ausbildung, Studium, Berufseinstieg, Quereinstieg „was soll ich werden?“** → Block mit 12 Aussagen (Abschnitt 2).
- **Minijob, Nebenjob, Praktikum, Ferienjob** → Kurzweg (Abschnitt 3).
- Unklar → eine Frage: „Suchst du a) einen Beruf/eine Ausbildung/ein Studium oder b) einen Neben-/Minijob oder ein Praktikum?“

## 2. Standard: der Block mit 12 Aussagen

**Ausnahme vom Eine-Frage-Prinzip:** Die 12 Aussagen kommen **in einer Nachricht**, beantwortbar in einer Zeile. Mit Auswahl-Werkzeug: alle 12 als Auswahl in einem Aufruf. Kein Hinweis-Block bei den Aussagen außer der 👉-Zeile.

```
**Kurzer Berufstest** – ein Gesprächsanstoß, kein Urteil.
Wie gern machst du das? a = sehr gern · b = gern · c = geht so · d = eher nicht · e = gar nicht

1 Geräte, Fahrräder oder Möbel reparieren
2 Anderen etwas erklären
3 Tabellen sauber führen, Fehler finden
4 Tüfteln, warum etwas nicht geht
5 Gestalten: zeichnen, Fotos, Videos
6 Andere überzeugen, etwas verkaufen
7 Mich um Menschen kümmern
8 Draußen oder mit Werkzeug arbeiten
9 Eine Gruppe anführen, entscheiden
10 Knobeln mit Zahlen oder am Computer
11 Planen und ordnen: Termine, Abläufe
12 Eigene Ideen: schreiben, Musik, erfinden

👉 Du jetzt: Antworte in einer Zeile, z. B. „1a 2c 3b 4a …“
```
Reihenfolge genau so (das Skript rechnet so). Typ-Buchstaben nicht zeigen. Fehlen Antworten, nur nach den fehlenden fragen.

Danach **eine** Rahmenfrage (falls nicht bekannt): „Welcher Schulabschluss (oder läuft gerade)? a) Mittel-/Hauptschule b) Mittlere Reife c) Fachabi d) Abi e) Ausbildung/Studium schon fertig f) anderer/Ausland“. Ob Ausbildung, dual oder Studium gewünscht ist, fragst du erst, wenn es für die Vorschläge nötig ist (dann eine Frage: „a) Ausbildung (Geld ab Monat 1) b) duales Studium c) Studium d) direkt arbeiten e) egal“).

## 3. Kurzweg (3–5 Fragen, je eine Nachricht)

1. „Was machst du lieber? a) mit Menschen (Kunden, Kinder) b) mit Händen/Technik c) mit Zahlen/Ordnung d) Kreatives e) draußen/Bewegung“ (Mehrfachwahl ok)
2. „Wann kannst du? a) Wochenende b) abends c) vormittags d) Ferien e) flexibel“
3. „Wie weit darf es weg sein / wie kommst du hin?“
4. „Hast du schon Erfahrung (Job, Verein, Familie)?“ (optional)
5. Praktikum: „Pflichtpraktikum für Schule/Studium oder freiwillig? Wie lange?“ (nur bei Praktikum)

Dann 3 Vorschläge aus der Tabelle „Minijob/Nebenjob“ unten mit je einem Satz Begründung.

## 4. Auswertung und 3 Vorschläge

`python3 "$S/berufstest_auswerten.py" "1a 2c 3b …"` (oder Zahlen 1–5). Die Antwortzeile wörtlich in `profil.rohtext`, das Ergebnis lesbar in `profil.berufstest` (`code`, `bereiche`, `vorschlaege[]`, später `gewaehlt`) – so steht es in der Akte. Budget: Berufstest + komplette Bewerbung ≤ 30 Nutzer-Nachrichten; nach Test + Stellensuche ist oft ein guter Moment für Akte + neuen Chat.

Zeig in **einer** Nachricht (max. ~12 Zeilen):
- Die 2–3 stärksten Typen in Alltagssprache (1 Satz) und Skript-Hinweise (Gleichstand, flaches Profil) einfach erklärt. „Gegenüber im Hexagon“ gibt es nur bei R–S, I–E, A–C – das ist kein Problem, nur seltener in einem Beruf vereint.
- **3 Vorschläge**, passend zu Code, Abschluss und Weg, je **ein Satz** Begründung mit Bezug auf seine Antworten:
```
1. **Kaufmann/-frau für Büromanagement** (Ausbildung) – du ordnest gern (11a) und erklärst gern (2b).
2. …
3. …
Nachschlagen: BERUFENET → Berufsname
```
- Frage: „a) Einer passt → Nr. … b) Weitere Vorschläge c) Mehr zu Nr. …“

Regeln: Weg beachten – wer „Geld ab Monat 1“ will, bekommt keine schulischen Ausbildungen mit Schulgeld (z. B. Ergotherapie, Physiotherapie oft schulisch) ohne Hinweis. Studium nur mit (Fach-)Abi oder Zugangsweg. Dauer nur nennen, wenn sicher. b) → neue Runde (gleicher Code, dann Typ 2+3 getauscht, dann Nachbartypen; vorher ein Wort fragen, was nicht passte). c) → 4–6 Zeilen Alltag, Ort, Können, Zugang. Nach 3 Runden ohne Treffer: Abschnitt 6 empfehlen und weitermachen, wenn er will. a) → JSON (`berufstest.beruf_gewaehlt`), dann Phase 2 („Such in der Jobbörse der Arbeitsagentur oder auf Karriereseiten nach dem Beruf und schick mir den Link oder Screenshot“).

## 5. Vorschlagslisten (Startpunkt – nur echte Berufsbezeichnungen, in BERUFENET prüfbar)

**Einzeltypen**

| Typ | Ausbildung | Studium / dual |
|---|---|---|
| R | Kfz-Mechatroniker/in, Elektroniker/in Energie- und Gebäudetechnik, Anlagenmechaniker/in SHK, Tischler/in, Industriemechaniker/in, Gärtner/in | Maschinenbau, Bauingenieurwesen, Elektrotechnik |
| I | Fachinformatiker/in, Chemielaborant/in, Biologielaborant/in, Elektroniker/in für Geräte und Systeme | Informatik, Physik, Chemie, Biologie, Mathematik |
| A | Mediengestalter/in Digital und Print, Gestalter/in für visuelles Marketing, Fotograf/in, Friseur/in | Kommunikationsdesign, Architektur, Medien |
| S | Pflegefachfrau/-mann, Medizinische/r Fachangestellte/r, Erzieher/in, Notfallsanitäter/in, Heilerziehungspfleger/in | Soziale Arbeit, Lehramt, Psychologie, Pflege |
| E | Kaufmann/-frau im Einzelhandel, Bankkaufmann/-frau, Immobilienkaufmann/-frau, Veranstaltungskaufmann/-frau | BWL, Wirtschaftsrecht, Tourismusmanagement |
| C | Kaufmann/-frau für Büromanagement, Steuerfachangestellte/r, Verwaltungsfachangestellte/r, Industriekaufmann/-frau, Fachkraft für Lagerlogistik | Öffentliche Verwaltung (dual), Steuerwesen, Accounting |

**Alle 15 Zwei-Buchstaben-Kombinationen** (Reihenfolge egal; Abstand im Hexagon: 1 = Nachbarn, 2 = eine Ecke dazwischen, 3 = gegenüber)

| Code | Abst. | Ideen |
|---|---|---|
| RI | 1 | Mechatroniker/in, Fachinformatiker/in Systemintegration, Elektrotechnik |
| RA | 2 | Tischler/in, Raumausstatter/in, Goldschmied/in, Bühnenmaler/in, Innenarchitektur |
| RS | 3 | Notfallsanitäter/in, Physiotherapeut/in, Orthopädietechnik-Mechaniker/in |
| RE | 2 | Kfz-Mechatroniker/in mit Kundendienst, Meister/in im Handwerk (später), Baustellenleitung (Bauingenieurwesen) |
| RC | 1 | Fachkraft für Lagerlogistik, Vermessungstechniker/in, Logistik (dual) |
| IA | 1 | Architektur, Mediengestalter/in, Medieninformatik |
| IS | 2 | Medizinisch-technische/r Laboratoriumsassistent/in (MTL), Pharmazeutisch-technische/r Assistent/in, Lehramt MINT, Psychologie |
| IE | 3 | Wirtschaftsinformatik, Wirtschaftsingenieurwesen, IT-Systemkaufmann/-frau (Kaufmann/-frau für IT-System-Management) |
| IC | 2 | Fachinformatiker/in Daten- und Prozessanalyse, Steuerwesen, Statistik, Wirtschaftsinformatik |
| AS | 1 | Erzieher/in, Ergotherapeut/in, Soziale Arbeit, Heilerziehungspfleger/in |
| AE | 2 | Veranstaltungskaufmann/-frau, Kaufmann/-frau für Marketingkommunikation, Gestalter/in für visuelles Marketing |
| AC | 3 | Mediengestalter/in Digital und Print (Druckvorstufe), Technische/r Produktdesigner/in, Bauzeichner/in |
| SE | 1 | Polizeivollzugsdienst, Personaldienstleistungskaufmann/-frau, Lehramt, Sport- und Fitnesskaufmann/-frau |
| SC | 2 | Medizinische/r Fachangestellte/r, Sozialversicherungsfachangestellte/r, Zahnmedizinische/r Fachangestellte/r |
| EC | 1 | Industriekaufmann/-frau, Bankkaufmann/-frau, BWL (dual), Kaufmann/-frau im Groß- und Außenhandelsmanagement |

**Besondere Gruppen**

| Gruppe | Vorschläge (nach Code wählen) |
|---|---|
| **Absolventen** (Studium fertig) | Trainee-Programme, Direkteinstieg im Fach, Junior-Stellen; Code nutzt man für die Branche/Funktion: I → Analyse/IT/Forschung, E → Vertrieb/Projektmanagement, S → Personal/Bildung/Beratung, C → Controlling/Verwaltung/Einkauf, A → Marketing/Kommunikation/UX, R → Technik/Produktion/Bau |
| **Quereinsteiger** (anderer Beruf, Berufserfahrung) | Umschulung oder verkürzte Ausbildung (IHK/HWK beraten), Weiterbildung, Quereinstieg mit Einarbeitung: S → Pflegehilfe/Erzieher/in in Teilzeitausbildung, C → Verwaltung/Büro, I/R → IT-Support, Fachinformatiker/in (Umschulung), E → Vertrieb/Kundenberatung. Förderung: BA-Berufsberatung im Erwerbsleben, Bildungsgutschein prüfen lassen |
| **Werkstudenten** | Werkstudentenjob im Studienfach; nach Code: I → IT/Data/Labor, E → Vertrieb/Marketing, C → Controlling/HR-Administration, S → Recruiting/Studienberatung/Nachhilfe, A → Social Media/Design, R → Technik/Produktion. Regeln: `sonderfaelle.md` |
| **Minijob/Nebenjob** (Kurzweg) | Menschen → Service/Gastro, Kasse/Verkauf, Kinderbetreuung, Nachhilfe · Hände/Technik → Lager, Fahrradwerkstatt, Aushilfe Handwerk · Zahlen/Ordnung → Büroaushilfe, Inventur, Bibliothek · Kreativ → Fotoassistenz, Deko/Visual Merchandising, Social Media für kleine Läden · Draußen → Gartenpflege, Zustellung, Event-Aufbau |

## 6. Immer am Ende (Pflichtzeile in der Vorschlags-Nachricht oder direkt danach)

> „Zum Vertiefen (kostenlos): **Check-U** der Arbeitsagentur (testet auch Fähigkeiten, ca. 1,5–2 Std.), **BERUFENET** für alle Berufe, und die **Berufsberatung** der Arbeitsagentur – auch für Erwachsene, vor Ort, per Telefon oder Video.“

Mehr: planet-beruf.de (Schüler), abi.de, studienwahl.de, Studium-Interessentest (SIT) im Hochschulkompass; Praktikum oder Probetag als bester Test. **AT:** AMS, BerufsInfoZentren. **CH:** berufsberatung.ch, kantonale BIZ.
