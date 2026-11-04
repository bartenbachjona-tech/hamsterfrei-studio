# Hamsterfrei – Auswertung aktuell (Stand 04.11.2026, Marke v2)

Geht PRODUKTION.md vor, steht unter KANAL_REGELN, `docs/brand/*` und STUDIO_HANDBUCH. Die Auswertungsroutine (geplante Aufgabe, alle 2 Tage, wie bei Groschenfall/Schattengast; muss noch angelegt werden) aktualisiert diese Datei und `state/zahlen.md`. Befunde werden als konkrete Regeländerung in `docs/brand/*` bzw. hier eingetragen, nicht nur ins Log (Handbuch G7).

## Befund
- **Es gibt bisher keine Zahlen.** Belegt sind nur: erste Version von Folge 01 hatte 10 Aufrufe (29.10.), bei den letzten Videos „Ø 5–7 s, Absprung nach 0:01“ (scripts/seminar03.md). `state/dm_log.csv` ist leer (0 DMs), Verkäufe nicht dokumentiert.
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

## Messziele (vorläufig; nach Erfassung der Basiswerte konkretisieren)
| Kennzahl | Plattform | Basiswert | Ziel nach 10 Videos ab 11.11. |
|---|---|---|---|
| Ø Wiedergabedauer | TikTok | offen (zuletzt ca. 5–7 s) | ≥ Basis + 50 % (Richtwert ≥ 10 s) |
| „Ganz angesehen“ % | TikTok | offen | ≥ Basis × 2 |
| Halterate nach 3 s | TikTok (falls sichtbar) | offen | ≥ 50 % |
| Angesehen % (vs. Weiterwischen) | YouTube | offen | ≥ 60 % |
| Ø angesehener Anteil | YouTube | offen | ≥ 70 % |
| Follower-Wachstum / 7 Tage | je Plattform | offen | positiv, Ziel festlegen nach Basis |
| Kommentare mit Kommentar-Wort | alle | offen | ≥ 1 pro Video mit Wort |
| Gesendete DMs | TikTok/IG | 0 | jede Wort-Anfrage innerhalb von 2 h beantwortet |
| Verkäufe | Digistore | offen | nur beobachten, kein Ziel (kein Werbekanal) |

## Laufender Test
- **Bis 10.11.:** kein Test. Seminar-Offensive mit Handbuch-Regeln. Nur Basiswerte und Erwartungen sammeln.
- **Testvariable 1 (ab 11.11., 10 Videos):** **Ergebnis-Hook „Hamster-Test“** (SERIEN.md (a): Signatur-Satz „Hamster-Test:“ + echtes Ergebnis als Schlüsselbild) **gegen den bisherigen Hook** (Anleitungs- bzw. Frage-Hook wie Folge 01/S2: erster Satz = erster Schritt oder Frage, startle + Text-Hook).
  - Verteilung: abwechselnd (gerade/ungerade Folge), Themen zufällig verteilt, Länge und Musik gleich.
  - Bewertung: TikTok und YouTube getrennt; Hauptmaß TikTok Ø Wiedergabe und „ganz angesehen“, YouTube „angesehen %“.
  - Entscheidung nach 10 Videos hier eintragen; Gewinner wird Standard in STIMME.md/SERIEN.md.
- Erst danach: Figur-Ausbau (LOOK.md), Länge, Posting-Zeit, Karussell – je eine Variable pro 10 Videos.
- Ausreißer (≥ 3× Median) lösen innerhalb von 48 h ein Folgevideo aus, ändern aber nicht die Testvariable (Handbuch G6).

## Offene Frage für Jona
- **Ist das geerbte Privatkonto (TikTok @hamsterfrei, ca. 2.400 themenfremde Follower) die richtige Basis?** Themenfremde Follower reagieren schlecht auf die ersten Ausspielungen und können die Ø-Werte drücken. Optionen: (1) weiter so und nur beobachten, ob die Follower-Demografie kippt; (2) neues TikTok-Konto starten und das alte ruhen lassen. Die Basiswerte (Follower-Demografie, Traffic aus „Folge ich“ vs. For You) sollen die Entscheidung stützen. Antwort hier eintragen.
