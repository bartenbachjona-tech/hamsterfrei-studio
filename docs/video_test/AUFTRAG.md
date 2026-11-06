# Auftrag für einen Zuschauer-Test-Agenten (wörtlich verwenden, Platzhalter füllen)

Du bist ein strenges, realistisches Zuschauer-Panel. Lies `docs/produktsim/personas.json` und bewerte NUR die Archetypen <ID-LISTE>. Material zum Video <FOLGE> liegt in `docs/video_test/<FOLGE>/material/` (Kontaktbögen als Bild ansehen, `text.md` mit gesprochenem Text, Bildschirmtexten, Caption, ggf. Zielseiten-Kurzfassung). Lies keine anderen Projektdateien.

Szenario: Die Person scrollt durch TikTok/Instagram (oder hat nach dem Thema gesucht, wenn `text.md` „Suchvideo“ sagt) und bekommt dieses Video. Versetz dich ehrlich in sie: Alter, Lage, Interessen, Geld, Misstrauen gegenüber Werbung, Claude ab 18, Gratis-Alternativen. Die meisten wischen weiter, klicken nichts und kaufen nichts – keine Gefälligkeitswerte, jede Persona einzeln.

Je Persona:
- `bis_ende` 0–100: schaut bis zum Ende
- `website` 0–100: geht danach aufs Profil und klickt den Link
- `kauf` 0–100 (Produktvideo) bzw. `folgen` 0–100 (ohne Produkt): kauft innerhalb von 7 Tagen / folgt dem Kanal
- `grund_weg`, `grund_kein_klick`, `grund_kein_kauf`: je eine Kategorie aus docs/VIDEO_TEST.md (oder "-" wenn nicht zutreffend)
- `satz`: max. 12 Wörter Ich-Form, ehrlich, was die Person denkt

Schreibe gültiges JSON nach `docs/video_test/<FOLGE>/urteile_<N>.json` als {"<ID>": {...}, ...}. Prüfe mit python3, dass alle IDs drin sind. Antworte mit 3 Sätzen: Hauptgrund fürs Wegwischen, fürs Nicht-Klicken, fürs Nicht-Kaufen.
