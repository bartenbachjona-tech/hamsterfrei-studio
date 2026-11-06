# Phase 1: Berufstest (für alle, die noch nicht wissen, was sie machen wollen)

## Inhalt
1. Einstieg und Ablauf
2. Die 14 Fragen (12 Interessen + 2 Rahmenfragen)
3. Auswertung
4. Vorschläge machen – so lange, bis etwas passt
5. Vorschlagsliste nach Typ
6. Ergänzende Angebote (Check-U, BERUFENET, Berufsberatung)

---

## 1. Einstieg und Ablauf

Modell: RIASEC (Holland-Code). Sechs Interessentypen: **R** praktisch-technisch, **I** forschend, **A** kreativ, **S** sozial, **E** unternehmerisch, **C** ordnend-verwaltend. Ergebnis ist ein Code aus den 2–3 stärksten Typen, z. B. „SEC“. Nachbarn im Hexagon (R-I, I-A, A-S, S-E, E-C, C-R) passen besser zusammen als Gegenüberliegende.

Sag vorher in 2 Sätzen:
> „Ich stelle dir 14 kurze Fragen, eine nach der anderen. Du antwortest jeweils nur mit einer Zahl von 1 bis 5 – dauert etwa 5 Minuten.“
> „Das ist ein Gesprächsanstoß, kein Urteil. Am Ende bekommst du konkrete Berufsvorschläge.“

Biete einmal an: „Wenn du schneller sein willst, kann ich dir alle 12 Aussagen auf einmal schicken.“ (spart Nachrichten im Free-Plan)

## 2. Die 14 Fragen

Skala bei jeder Interessen-Frage gleich, immer mit anzeigen:
`1 = macht mir keinen Spaß · 2 = eher nicht · 3 = geht so · 4 = gern · 5 = sehr gern`

Reihenfolge **genau so** (das Skript `berufstest_auswerten.py` rechnet in dieser Reihenfolge):

| Nr | Aussage: „Wie gern würdest du …“ | Typ |
|---|---|---|
| 1 | ein Fahrrad, ein Gerät oder ein Möbelstück reparieren oder zusammenbauen | R |
| 2 | jemandem etwas erklären, bis er es wirklich verstanden hat | S |
| 3 | eine Tabelle sauber führen und Fehler darin finden | C |
| 4 | herausfinden, warum etwas nicht funktioniert – tüfteln, recherchieren, testen | I |
| 5 | etwas gestalten: zeichnen, fotografieren, Videos schneiden oder dekorieren | A |
| 6 | andere von einer Idee überzeugen oder etwas verkaufen | E |
| 7 | dich um Menschen kümmern, z. B. Kinder, Ältere, Kranke oder Kunden | S |
| 8 | draußen oder mit Werkzeug und Maschinen körperlich arbeiten | R |
| 9 | eine Gruppe anführen, Entscheidungen treffen und Verantwortung übernehmen | E |
| 10 | mit Zahlen, Experimenten oder am Computer knifflige Aufgaben lösen | I |
| 11 | Dinge planen und ordnen: Termine, Lager, Unterlagen oder Abläufe | C |
| 12 | eigene Ideen entwickeln: schreiben, Musik machen oder Neues erfinden | A |

Den Typ-Buchstaben **nicht** anzeigen (beeinflusst die Antwort).

**Frage 13 von 14 – Abschluss:** „Welchen Schulabschluss hast du (oder machst du gerade)?“
a) Mittelschule/Hauptschule b) Mittlere Reife/Realschule c) Fachabitur d) Abitur e) schon eine Ausbildung oder ein Studium abgeschlossen f) anderer / aus dem Ausland

**Frage 14 von 14 – Weg:** „Was passt gerade am besten zu dir?“
a) Ausbildung (Geld ab dem ersten Monat) b) duales Studium (Betrieb + Hochschule, Geld ab Tag 1) c) Studium d) direkt arbeiten / Job wechseln e) weiß ich nicht

Optional danach (nur wenn hilfreich, je eine Nachricht): Lieblings- und Hassfächer; Region bzw. Umzug ja/nein.

## 3. Auswertung

Führe aus:
```
python3 "$S/berufstest_auswerten.py" 4 5 2 3 1 4 5 2 3 4 1 5
```
Zeig dem Nutzer: seine 2–3 stärksten Typen in Alltagssprache (nicht nur Buchstaben), einen Satz, was das bedeutet, und Hinweise des Skripts (Gleichstand, flaches Profil) in einfachen Worten. Interessen allein reichen nicht – Fähigkeiten, Noten und Rahmen (Ort, Abschluss, Geld) gehören dazu.

## 4. Vorschläge machen – so lange, bis etwas passt

Pro Runde **3 Vorschläge**, passend zu Code **und** Abschluss und Weg (Studium nur mit (Fach-)Abitur bzw. Zugang prüfen; wer schon einen Abschluss hat: Weiterbildung, Quereinstieg, Umschulung nennen). Je Vorschlag genau dieses Format:

```
1. **Kaufmann/-frau für Büromanagement** (Ausbildung, 3 Jahre)
   Warum: Du ordnest gern (Frage 11: 5) und erklärst gern (Frage 2: 4) – hier planst du Abläufe und hast viel Kontakt.
   Nachschlagen: BERUFENET → „Kaufmann/-frau für Büromanagement“
```
Dauer nur nennen, wenn du sie sicher weißt, sonst weglassen.

Danach fragen (eine Frage):
> „Klingt einer davon spannend? a) Ja, Nr. … → dann schauen wir nach Stellen b) Mehr dazu erzählen (Nr. …) c) Nicht das Richtige – zeig mir andere“

- **c)** → nächste Runde mit anderen Vorschlägen: erst weitere zum gleichen Code, dann Typ 2+3 in anderer Reihenfolge, dann Nachbartypen. Vorher kurz fragen, was nicht gepasst hat (ein Wort reicht) und das berücksichtigen.
- **b)** → in 4–6 Zeilen: typischer Alltag, wo man arbeitet, was man können sollte, Zugang; dann wieder die Frage.
- Nach 3 Runden ohne Treffer: freundlich die Ergänzungen aus Abschnitt 6 empfehlen **und** weitermachen, wenn der Nutzer möchte. Nie aufgeben, nie drängen.
- **a)** → kurz festhalten (Akte: Berufstest-Code, gewählter Beruf), dann Phase 2: „Hast du schon eine konkrete Stelle? Wenn nicht: Such auf der Jobbörse der Arbeitsagentur oder auf der Karriereseite einer Firma in deiner Nähe nach dem Beruf und schick mir den Link.“

Mit Websuche: Gib auf Wunsch 2–3 echte Suchwege (Jobbörse der BA, Karriereseiten) – keine erfundenen Stellen, keine erfundenen Gehälter.

## 5. Vorschlagsliste nach Typ (Startpunkt, in BERUFENET prüfen)

| Typ | Ausbildung (Beispiele) | Studium / dual (Beispiele) |
|---|---|---|
| R | Kfz-Mechatroniker/in, Elektroniker/in für Energie- und Gebäudetechnik, Anlagenmechaniker/in SHK, Tischler/in, Industriemechaniker/in, Gärtner/in | Maschinenbau, Bauingenieurwesen, Elektrotechnik, Agrarwissenschaften |
| I | Fachinformatiker/in, Chemielaborant/in, Biologielaborant/in, Elektroniker/in für Geräte und Systeme | Informatik, Physik, Chemie, Biologie, Mathematik, Medizin |
| A | Mediengestalter/in Digital und Print, Gestalter/in für visuelles Marketing, Fotograf/in, Friseur/in, Goldschmied/in | Kommunikationsdesign, Architektur, Medien, Germanistik |
| S | Pflegefachfrau/-mann, Medizinische/r Fachangestellte/r, Erzieher/in, Notfallsanitäter/in, Heilerziehungspfleger/in | Soziale Arbeit, Lehramt, Psychologie, Pflege, Physiotherapie |
| E | Kaufmann/-frau im Einzelhandel, Bankkaufmann/-frau, Immobilienkaufmann/-frau, Kaufmann/-frau für Versicherungen und Finanzanlagen, Veranstaltungskaufmann/-frau | BWL, Wirtschaftsrecht, Tourismusmanagement, Jura |
| C | Kaufmann/-frau für Büromanagement, Steuerfachangestellte/r, Verwaltungsfachangestellte/r, Industriekaufmann/-frau, Fachkraft für Lagerlogistik | Öffentliche Verwaltung (dual), Steuerwesen, Wirtschaftsinformatik, Accounting |

Kombinationen, die zwei Typen verbinden:

| Code | Ideen |
|---|---|
| RI / IR | Mechatroniker/in, Fachinformatiker/in Systemintegration, Elektrotechnik |
| RC / CR | Fachkraft für Lagerlogistik, Vermessungstechniker/in, Logistik (dual) |
| IC / CI | Fachinformatiker/in, Wirtschaftsinformatik, Steuerwesen |
| IA / AI | Architektur, Mediengestalter/in, Medieninformatik |
| AS / SA | Erzieher/in, Ergotherapeut/in, Soziale Arbeit mit Medienschwerpunkt |
| SE / ES | Polizeivollzugsdienst, Personaldienstleistungskaufmann/-frau, Lehramt |
| SC / CS | Medizinische/r Fachangestellte/r, Sozialversicherungsfachangestellte/r |
| EC / CE | Industriekaufmann/-frau, Bankkaufmann/-frau, BWL (dual) |
| AE / EA | Veranstaltungskaufmann/-frau, Kaufmann/-frau für Marketingkommunikation |
| RS / SR | Notfallsanitäter/in, Physiotherapeut/in, Gärtner/in im Therapiebereich |

Diese Liste ist ein Startpunkt. Ergänze aus deinem Wissen, aber nur echte Berufsbezeichnungen, die man in BERUFENET findet.

## 6. Ergänzende Angebote (immer am Ende nennen)

- **Check-U** (Bundesagentur für Arbeit, kostenlos): vier Module, zusammen ca. 105 Minuten (Fähigkeiten ~65, Soziale Kompetenzen ~15, Interessen ~15, Berufliche Vorlieben ~10). Die Top-Vorschläge erscheinen erst nach „Fähigkeiten“ und „Soziale Kompetenzen“. Ergebnis als PDF für die Beratung, Konto zum Speichern nötig.
- **BERUFENET**: alle Berufsbilder mit Tätigkeiten, Zugang, Verdienst. Für Schüler: **planet-beruf.de**; Abiturienten: **abi.de**, **studienwahl.de**; Studium-Interessentest (SIT) im Hochschulkompass.
- **Berufsberatung der BA**: kostenlos, auch für Erwachsene („Berufsberatung im Erwerbsleben“), vor Ort, per Telefon oder Video. Check-U-PDF mitbringen.
- **Praktikum oder Probetag**: der beste Test, ob ein Beruf passt.
- **AT:** AMS (Berufsinformation, BerufsInfoZentren). **CH:** berufsberatung.ch und die kantonalen BIZ.
