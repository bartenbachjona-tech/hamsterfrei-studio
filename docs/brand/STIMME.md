# Hamsterfrei – Stimme (Marke v2, Stand 04.11.2026)

Geht PRODUKTION.md vor. Sicherheit/Recht aus KANAL_REGELN geht dieser Datei vor.

## Stimme und Parameter (versioniert)
| Version | gültig ab | Voice | Modell | Takes | Hinweis |
|---|---|---|---|---|---|
| v1 | 29.10.2026 | „Hamsterfrei – Hamster“ `E6cNSOTqfEt7KnIGmkxz` | `eleven_v3` | 2 | Comic-Hamster, leicht hoch, quirlig, gut verständlich |
| **v2** | **04.11.2026** | **gleich: `E6cNSOTqfEt7KnIGmkxz`** | **`eleven_v3`** (unverändert) | **1** | Audio-Tags erlaubt (`[excited]`, `[calm]`, `[calm, warm]`), sparsam: höchstens 3 pro Skript |

- **Ab sofort genau 1 Take** (`generations_count: 1`) wegen der Credits (spart ca. 700 Credits pro Video). Den Generierungsaufruf nie wiederholen. Ist der eine Take unbrauchbar (Versprecher, falsche Betonung im Hook), wird nur der betroffene Satz einzeln neu gesprochen und angesetzt, nicht das ganze Skript. Verbrauch ins Log (`state/log.md`) eintragen.
- Die Stimme bleibt dieselbe (Wiedererkennung). Ein Modellwechsel (z. B. das bei S2 einmalig genutzte `eleven_v4`) ist eine Testvariable und läuft nur über `docs/AUSWERTUNG_AKTUELL.md`, nie nebenbei.
- Musikbett unverändert: `public/music/bett01.mp3`, ca. 10 %, sanft ein- und ausgeblendet. Keine Trend-Sounds, keine fremde Musik.

## Ton
- Der Hamster ist ein **Ausprobierer mit Meinung**: neugierig, ein bisschen frech, ehrlich enttäuscht, wenn etwas nicht klappt. Er redet wie ein älterer Mitschüler, nicht wie ein Lehrer und nicht wie ein Verkäufer.
- Du-Form, Präsens, kurze Sätze (meist unter 12 Wörtern), gesprochene Sprache.
- Nach dem Hook alle 5–8 s eine Wendung („aber …“, „deshalb …“), nicht „und dann …“ (Handbuch G3).

## Hook
- **Signatur-Einstieg „Hamster-Test:“** steckt *im* ersten Satz der Serie „Hamster-Test“ (siehe SERIEN.md), z. B. „Hamster-Test: Ich hab Claude meine Bewerbung schreiben lassen.“ Das ist das Hör-Signet (G4), kein eigenes Intro, dauert unter 0,7 s. In den anderen Serien gibt es keinen Pflichtsatz, dort trägt das Bild-Signet (LOOK.md).
- Bis 10.11. (Seminar-Folgen) wird „Hamster-Test:“ **nicht** benutzt, damit die Testvariable ab 11.11. sauber ist (siehe AUSWERTUNG_AKTUELL).
- **Kein KI-Jargon im Hook:** nicht „Agent“, „Prompt-Chaining“, „LLM“, „Workflow“, „Use Case“, „generativ“, „Skill“, „Automation“. Stattdessen das konkrete Ergebnis für dich: „Bewerbung in 2 Minuten“, „Anzeige, die in einem Tag weg war“. Der Name „Claude“ ist erlaubt.
- Der erste Satz ist nach höchstens 1,5 s verstanden (Hook-Tor 1) und enthält „du/dein“ oder eine Ich-hab-es-ausprobiert-Situation (Hook-Tor 3).
- Zahlen im Hook nur, wenn sie echt belegt sind (eigener Test, Screenshot, Quelle).

## Schluss (neu, ohne Schluss-Signal)
- **Kein Schluss-Signal**: kein „Zum Schluss“, „Am Ende des Tages“, „Das war's“, „Bis zum nächsten Mal“, kein „Folg mir für mehr“.
- Der letzte inhaltliche Satz ist die **Pointe** (das Ergebnis bzw. das ehrliche Urteil des Hamsters). Direkt danach höchstens **ein** CTA-Satz mit echtem Nutzen:
  - „Kommentier <WORT>, dann schick ich dir <konkreter Gratis-Nutzen>.“ (z. B. „die drei Prompts zum Kopieren“)
  - Bei Videos ohne Kommentar-Wort: kein CTA oder eine Frage, die Kommentare auslöst („Was soll der Hamster als Nächstes testen?“).
- Der alte Pflichtschluss „Die genaue Anleitung schick ich dir. Folg mir und kommentier WORT.“ gilt nicht mehr.
- Letztes Bild bleibt mit dem Wort stehen (Handy mit Kommentarblase, LOOK.md); das Video endet mit dem CTA, nichts danach.

## Bann-Phrasen (nie sprechen, nie als Bildtext)
- Begrüßung, Intro: „Hey Leute“, „Willkommen“, „Heute zeig ich dir …“, „In diesem Video …“
- Schluss-Signale (siehe oben), Insider-Bezüge („wie im letzten Video“)
- Hype: „Gamechanger“, „krass“, „unglaublich“, „das ändert alles“, „Geheimtipp“, „Hack“, „Gelddruckmaschine“, „passives Einkommen“, „schnell reich“
- Versprechen: „garantiert“, „100 %“, „unentdeckbar“, „besteht jeden KI-Detektor“, Notengarantien (seit 04.11. erlaubt: zeigen, dass Claude die Arbeit mit dir komplett schreibt, siehe POSITIONIERUNG), Einkommensversprechen
- Druck: „nur noch heute“, „schnell zugreifen“, „Link in Bio, bevor es weg ist“, jede Kaufaufforderung im Hook
- Fachwörter im Hook (siehe oben), „Dropshipping“ (darf nur als Gegenbegriff im Nebenjob-Check vorkommen: „nicht Dropshipping, sondern …“)

## Vorher/Nachher (Beispiele)
| Vorher (v1) | Nachher (v2) |
|---|---|
| „Heute zeig ich dir, wie du mit KI eine Anzeige schreibst.“ | „Hamster-Test: Gleiche Fotos, zwei Anzeigen. Nur eine war nach einem Tag weg.“ |
| „Mein Claude-Skill findet die alle automatisch. Link in Bio.“ (Werbung als Pointe) | Pointe = Ergebnis: „Drei davon hatte ich auch drin.“ + „Kommentier SEMINAR, dann schick ich dir die Checkliste.“ |
| „Die genaue Anleitung schick ich dir. Folg mir und kommentier SHOP.“ | „Kommentier STUNDE, dann schick ich dir meine Rechnung zum Nachrechnen.“ |

## TTS-Regeln (Handbuch G8)
- Zahlen, Euro-Beträge, Uhrzeiten, Daten, Paragrafen und Akronyme im Sprechtext **ausschreiben** („neun Euro neunzig“, „zehnter November“, „K I“ nur wenn nötig, besser „KI“ vermeiden und „Claude“ sagen). Im Untertitel per `captionMap` wieder als Ziffern zeigen (z. B. „neun Euro neunzig“ → „9,90 €“).
- **Keine Gedankenstriche „–“ oder „—“ im Sprechtext** (führen zu Aussetzern). Stattdessen Punkt oder Komma.
- Englische Wörter nur, wenn das Publikum sie so sagt (Claude, Vinted). Bei Ausspracheproblemen Lautschrift-Ersatz im Sprechtext („Klohd“ nur, wenn Claude falsch klingt; im Untertitel per captionMap korrigieren).
- Audio-Tags in eckigen Klammern werden vor Scribe/Untertiteln entfernt.
- Skript vor dem Vertonen einmal laut gegenlesen lassen (Kritiker prüft Sprechbarkeit).
