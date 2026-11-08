# Hamsterfrei – Auswertung aktuell (Stand 08.11.2026, Marke v2)

Geht PRODUKTION.md vor, steht unter KANAL_REGELN, `docs/brand/*` und STUDIO_HANDBUCH. Die Auswertungsroutine (geplante Aufgabe, alle 2 Tage, wie bei Groschenfall/Schattengast; muss noch angelegt werden) aktualisiert diese Datei und `state/zahlen.md`. Befunde werden als konkrete Regeländerung in `docs/brand/*` bzw. hier eingetragen, nicht nur ins Log (Handbuch G7).

## Befund
- (Stand 04.11., überholt durch Erhebungen 06.11./08.11.) Es gab keine Zahlen. Belegt sind nur: erste Version von Folge 01 hatte 10 Aufrufe (29.10.), bei den letzten Videos „Ø 5–7 s, Absprung nach 0:01“ (scripts/seminar03.md). `state/dm_log.csv` ist leer (0 DMs), Verkäufe nicht dokumentiert.
- Ohne Basiswerte ist jeder Test blind. Deshalb kommt **Messen vor Figur-Ausbau** (LOOK.md).

## Aufgabe 1 der Auswertungsroutine: Basiswerte erfassen (sofort)
Für **alle bisherigen Videos** (Folge 01, S1 „Seminararbeit bis 10.11.?“, Video 2 „5 Fehler“, S2 „Prüfungsgespräch“ und alles, was bis zum Lauf dazukommt) in `state/zahlen.md` eintragen, Plattformen getrennt:
- **TikTok Studio** (tiktok.com/tiktokstudio → Analysen bzw. Beitrag → Analysen): Aufrufe, Ø Wiedergabedauer, „ganz angesehen“ in %, Halterate nach 3 s (falls sichtbar), Likes, Kommentare, Shares, Speicherungen, neue Follower durch das Video, Traffic-Quellen (For You/Suche/Profil).
- **YouTube Studio** (Kanal `UCBmT3RjRK5PGk-YVTdFzuDA`): Aufrufe, „Weiterwischen vs. Ansehen“ (angesehen %), Ø Wiedergabedauer, Ø angesehener Anteil, Abos durch das Video.
- **Instagram** (Reel → Insights; nur wenn Creator-/Profi-Konto aktiv, sonst „nicht verfügbar“ notieren): Aufrufe, Ø Wiedergabe, Shares, Speicherungen, Follower.
- Konto-Ebene je Plattform: Follower gesamt, Follower-Veränderung letzte 7 Tage; bei TikTok zusätzlich Follower-Demografie (Alter, Land), falls sichtbar.
- Funnel: Kommentare mit Kommentar-Wort, gesendete DMs (`state/dm_log.csv`), Verkäufe Digistore 757079/757063 (nur wenn Jona Zugriff gibt; nur Anzahl, keine Kundendaten).
- Dann **Median** je Plattform und **Erwartung** für das nächste Video eintragen (Handbuch G7).
- Zugriff nur über das Hamsterfrei-Chrome-Profil (KANAL_REGELN, Konten). Nichts in den Studios ändern.


## Erhebung 06.11.2026 01:10 (TikTok Studio, manuell)
| Video | veröff. | Aufrufe | Ø Wiedergabe | ganz angesehen | Für dich | Suche |
|---|---|---|---|---|---|---|
| S1 „Seminararbeit bis 10.11.? Keine Angst“ | 30.10. | 656 | 10,3 s | 4,3 % | 38,8 % | **53,5 %** |
| 5 Fehler | 30.10. | 281 | – | – | – | – |
| S2 „Wofür hast du KI benutzt?“ | 02.11. | 273 | 5,9 s | 2,1 % | 86,4 % | 4,4 % |
| S5 „6 Tage, 0 Seiten“ | 04.11. | 307 | 4,7 s | 1,3 % | 87,9 % | 7,0 % |
| S5-2 „Noch 5 Tage: Literaturverzeichnis“ | 05.11. | 240 | 3,2 s | 1,2 % | 98,8 % | 0,8 % |
- **Befund:** Für-dich-Ausspielung bleibt bei ~250–300 hängen (Absprung bei 0:01 bei allen). **S1 wächst über die TikTok-Suche** (Suchbegriffe: „w seminar quellen“, „seminararbeit ki“, „seminararbeit mit claude“, „w seminar“, „seminar arbeit ki kostenlos“). Suche = Zuschauer mit Absicht, Ø 10 s.
- **Folgerung:** Bis 10.11. Suchbegriffe gezielt in Bildschirmtext (Frame 0), Caption-Anfang und Sprechtext packen (z. B. „Seminararbeit mit KI“, „W-Seminar Quellen“). Funnel: 0 Wort-Kommentare; Verkäufe nicht geprüft (Digistore-Login).

## Erhebung 08.11.2026 ~17:20–17:40 (alle drei Plattformen, Details state/zahlen.md)
- **TikTok:** S1 1.285 Aufrufe (verdoppelt seit 06.11., 52,5 % Suche, Ø 10,47 s, 4,8 % ganz) = einziger Ausreißer (4,4× Median 295). Alle anderen 256–351, Ø 3,4–5,8 s, Absprung bei 0:01. Konto 7 T: −2 Follower.
- **YouTube:** S2 Prüfungsgespräch 698 (Shorts-Feed 95 %), S1 441; Rest 16–223. „Bis zum Ende“ Median 36 %. 0 Abos.
- **Instagram:** S1 1.875, S2 380, Rest 104–157. Keine Insights (kein Creator-Konto). S5-2 nie gepostet.
- **Funnel:** 0 Wort-Kommentare, 0 DMs; Verkäufe nicht messbar (Digistore nicht eingeloggt).
- **07.11. und 08.11.: kein Video** (Soll 1/Tag) → Jona gemeldet.

## Befunde 08.11. (nach Kritiker-Runde, gelten als Regeln)
1. **Suchleiste in Frame 0 (S7) widerlegt:** 3,7 s < 4 s (eigene Regel ausgelöst), Suche nur 7,3 %. Suchbegriffe bleiben in Caption/Sprechtext, aber eine nachgezeichnete Suchleiste ist kein Schlüsselbild. Das eigentliche Problem bleibt der **Absprung bei 0:01 bei allen Videos** → genau das prüft der Hook-Test ab 11.11.
2. **S1 ist ein Such-Akkumulator, kein FYP-Treffer** (wächst über 9 Tage, beworben). Ein Deadline-„Teil 2“ kurz vor dem 10.11. kann nicht mehr ranken → **kein S1-Follow-up**. Such-Ausreißer bekommen künftig ein Folgevideo auf **dasselbe Keyword**, keine Deadline-Variante.
3. **Werbung verzerrt die Basis:** 5 von 7 TikTok-Videos sind beworben. Basis und Test nur innerhalb gleicher Werbe-Klasse vergleichen.
4. **Verfehlte Erwartung → Pflicht:** Verfehlt ein Video seine Erwartung, steht im Log eine schriftliche Ursache und genau eine Änderung fürs nächste Video. S5-2 (256 / 3,37 s statt 300–800 / 6–9 s): vermutete Ursache = Frame 0 zeigt das Problem (Notizzettel), nicht das fertige Ergebnis → nächstes Video zeigt in Frame 0 das fertige Ergebnis.

## Messregeln (ab 08.11.)
- Jedes Video wird bei **48 h und 7 T** in state/zahlen.md protokolliert (alle Metriken); verglichen werden nur gleich alte Werte.
- **Ausreißer** = ≥ 3× Median der Plattform **und** ≥ 500 Aufrufe **und** innerhalb von 48 h erkannt. Dann Folgevideo in 48 h (G6).
- Aufrufe sind **kein Ziel**, nur Kontext.

## Messziele (Stand 08.11.2026)
| Kennzahl | Plattform | Basis 08.11. | Ziel nach 10 Test-Videos |
|---|---|---|---|
| Ø Wiedergabedauer (48 h) | TikTok | FYP-Videos 4,53 s | ≥ 6,0 s |
| „Ganz angesehen“ % (48 h) | TikTok | 1,7 % | ≥ 3 % |
| „Bis zum Ende angesehen“ % | YouTube | Median 36 % | ≥ 40 % (nur bei gleicher Länge vergleichbar) |
| Wort-Kommentare pro Video mit Kommentar-Wort | TikTok + IG | 0 | ≥ 1 |
| Verkäufe je Plattform zuordenbar | Digistore | nicht messbar | Tracking aktiv (Jona) |
Gestrichen (Kritiker 08.11.): Follower Δ 7 T (Rauschen ±2 auf totem Konto), Suchanteil ≥ 20 % (gilt nur fürs Seminar-Thema).

## Testdesign ab 11.11. (EIN Test: Hook), Fassung 08.11.
- Ergebnis-Hook „Hamster-Test“ (A) vs. bisheriger Hook (B), **abwechselnd A/B/A/B** über 10 Videos = 5 Paare an aufeinanderfolgenden Tagen.
- **Alle 10 Videos gleich lang (30–35 s, im Rahmen von SERIEN.md) und alle ohne Werbung**; Werbe-Videos laufen in dieser Zeit nicht oder zählen nicht zum Test.
- **Entscheidung:** A gewinnt, wenn A in **≥ 4 von 5 Paaren** sowohl bei TikTok Ø Wiedergabe als auch bei „ganz angesehen“ (je 48 h) vorne liegt. Sonst bleibt B Standard. (Die alte Regel „+1,5 s im Mittel“ ist bei n = 5 und ~300 Aufrufen Rauschen.)
- **Ausfalltag:** Fehlt ein Tag, wird das angefangene Paar neu begonnen; zwei Ausfalltage im Test → Test neu starten. Deshalb startet der Test erst, wenn mindestens 3 Test-Videos fertig sind.
- Erwartung nächstes FYP-Video (G7): 230–350 Aufrufe/48 h, Ø 4–5 s.
- **S2-Follow-up (YouTube-Ausreißer 698):** Prüfungsgespräch-Video am **10.11.** (Abgabe heute → jetzt kommt die Prüfung), also vor dem Teststart, als Follow-up markiert. Mit Werbung nur nach Jonas OK.

## Offene Messpunkte (nächster Lauf)
- 7-T-Werte für S5-2 und S7; 48-h-Werte für jedes neue Video.
- Herkunft der Verkäufe unklar → Jona: Digistore im Hamsterfrei-Chrome einloggen und getrennte Links/Coupons bzw. UTM je Plattform.

## Laufender Test
- **Bis 10.11.:** kein Test. Seminar-Offensive mit Handbuch-Regeln. Nur Basiswerte und Erwartungen sammeln.
- **Testvariable 1 (ab 11.11., 10 Videos):** **Ergebnis-Hook „Hamster-Test“** (SERIEN.md (a): Signatur-Satz „Hamster-Test:“ + echtes Ergebnis als Schlüsselbild) **gegen den bisherigen Hook** (Anleitungs- bzw. Frage-Hook wie Folge 01/S2: erster Satz = erster Schritt oder Frage, startle + Text-Hook).
  - Verteilung: abwechselnd (gerade/ungerade Folge), Themen zufällig verteilt, Länge und Musik gleich.
  - Bewertung: TikTok und YouTube getrennt; Hauptmaß TikTok Ø Wiedergabe und „ganz angesehen“, YouTube „angesehen %“.
  - Entscheidung nach 10 Videos hier eintragen; Gewinner wird Standard in STIMME.md/SERIEN.md.
- Erst danach: Figur-Ausbau (LOOK.md), Länge, Posting-Zeit, Karussell – je eine Variable pro 10 Videos.
- Ausreißer (≥ 3× Median und ≥ 500 Aufrufe) lösen innerhalb von 48 h ein Folgevideo aus, ändern aber nicht die Testvariable (Handbuch G6).

## Offene Frage für Jona
- **Ist das geerbte Privatkonto (TikTok @hamsterfrei, ca. 2.400 themenfremde Follower) die richtige Basis?** Themenfremde Follower reagieren schlecht auf die ersten Ausspielungen und können die Ø-Werte drücken. Optionen: (1) weiter so und nur beobachten, ob die Follower-Demografie kippt; (2) neues TikTok-Konto starten und das alte ruhen lassen. Die Basiswerte (Follower-Demografie, Traffic aus „Folge ich“ vs. For You) sollen die Entscheidung stützen. Antwort hier eintragen.
- **Zahlen 08.11. (TikTok Studio):** Die 2.400 geerbten Follower liefern praktisch nichts: Traffic „Gefolgt“ <0,1 % bei allen Videos, 0 % Follower unter den Zuschauern (S1, S5-2, S7), Netto −2 in 7 Tagen. Follower = 57 % Männer, nur 52,8 % DE (40 % „Anderes“); Zuschauer = ~70 % Frauen, 18–24, 80–90 % DE. **Empfehlung des Studios:** Konto behalten (Suche funktioniert, S1 rankt), die alten Follower als irrelevant behandeln. 250–300 FYP-Aufrufe sind Kaltstart-Normal; ein Neukonto würde daran nichts ändern. Neustart nur erwägen, wenn der DE-Anteil der Zuschauer unter 70 % fällt. Entscheidung: Jona.
