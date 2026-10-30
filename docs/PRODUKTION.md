# Tagesproduktion (läuft täglich mittags, Veröffentlichung 18:00 nach Jonas Okay)

Zuerst lesen: `docs/KANAL_REGELN.md` (geht immer vor), `docs/THEMEN.md`, `state/log.md`.

## 1. Vorbereitung
- Repo klonen bzw. `git pull`, dann `npm ci --loglevel=error` (dauert ein paar Minuten).
- Prüfen, ob für heute schon eine Folge produziert/geplant ist (`state/log.md`). Wenn ja: nichts Neues bauen, nur melden.
- Nächste Folge = oberste Zeile mit Status `offen` in `docs/THEMEN.md`. Nummer NN zweistellig.

## 2. Skript (45–55 s gesprochen, ca. 110–130 Wörter)
- Rahmen aus dem Doc „Hamsterfrei Masterplan“, Tab „Skripte Format 1“ (Claude Docs, Doc-ID 516e17f8-914a-464f-a8a6-ebea8190249a) bzw. THEMEN.md.
- **Konkret machen:** per WebSearch ein echtes, aktuelles Beispiel finden (was gerade auf TikTok/Etsy/Vinted läuft, mit realistischen Preisen; Quelle im Log notieren). Satz „Zum Beispiel …“ einbauen. Zahlen nie erfinden; lieber „ein paar Euro“ als falsche Zahl.
- Das Tool Schritt für Schritt benennen (wie Folge 1: Konto anlegen → Name → Design → Produkt mit Bildern, Titel, Preis → live).
- Erster Satz = erster Schritt der Anleitung. Kein Haken, kein Werbe-Satz, kein Fachbegriff, „Dropshipping“ nie sagen.
- Schluss exakt: „Die genaue Anleitung schick ich dir. Folg mir und kommentier <WORT>.“
- Zahlen im Sprechtext ausschreiben (TTS), Untertitel-Mapping über `captionMap` (z. B. „neunundzwanzig“ → „29,90 €“).
- Kritiker: einen Agenten (model "fable") das Skript gegen KANAL_REGELN prüfen lassen (konkret genug? klingt es nach Werbung? stimmt jede Zahl?). Danach entscheiden.
- Skript speichern: `scripts/folgeNN.md` (Sprechtext, Szenenplan, Caption, Wort, Werbung ja/nein, Quellen).

## 3. Stimme
- ElevenLabs-Connector: `creative_create_flow`, dann `creative_generate_speech` mit voice_id `E6cNSOTqfEt7KnIGmkxz`, Modell `eleven_v3`, Text = Sprechtext (generations_count Standard = 2 Takes). Mit `creative_get_flow_run_status` pollen. Nie einen Generierungsaufruf wiederholen (kostet doppelt, ca. 750 Credits pro Take).
- Besseren Take wählen (deutlich, Tempo, keine Versprecher), Audio-URL aus dem Ergebnis per curl laden (storage.googleapis.com ist erreichbar) nach `public/folgen/folgeNN.mp3`.
- Wort-Zeitstempel: Take per `creative_add_flow_asset_node` anpinnen und `creative_transcribe_audio` (Scribe) mit connect_from darauf; Ergebnis als `src/folgen/folgeNN.words.json` im Format `{ "words": [{text,start,end,type}] }` speichern.
- Dauer messen (ffprobe). totalSeconds = Audiodauer + ca. 1,8 s.

## 4. Video (Remotion)
- `src/folgen/folgeNN.tsx` nach dem Muster von `folge01.tsx`: `<Episode audio words scenes totalSeconds dingAt werbung captionMap />`. In `src/Root.tsx` die Composition `FolgeNN` ergänzen.
- Szenen für die Leinwand (948×1004 px) neu bauen, in einer eigenen Datei `src/scenes/folgeNN.tsx`; vorhandene Bausteine aus `src/Scenes.tsx`, `src/ScenesV2.tsx` wiederverwenden (Pop, Lamp, Browserfenster aus SceneShopify, SceneFlow, SceneVideos mit Kommentar-Wort). Farben/Schrift aus Scenes.tsx (INK, GREEN, NAVY, CREAM, Fredoka). Flache, freundliche Vektor-Optik wie Folge 1, keine Fotos von echten Personen, keine fremden Logos/Marken nachzeichnen (Tool-Namen als Text ist ok).
- Szenenwechsel und Einblendungen auf die Wort-Zeitstempel legen (Sekunden ab Szenenstart).
- Letzte Szene: Handy mit Kommentarblase „<WORT>“ (SceneVideos-Prinzip), bleibt bis zum Ende stehen; `dingAt` ≈ Zeitpunkt des Worts.
- Werbung-Label nur, wenn ein Affiliate-Tool vorkommt.
- `npx tsc --noEmit`, dann Standbilder an 6–8 Zeitpunkten (`npx remotion still FolgeNN --frame=…`) ansehen: nichts überlappt, Untertitel passen in die Box, Hamster verdeckt nichts, Text lesbar. Fehler beheben.
- Rendern: `npx remotion render FolgeNN out/hamsterfrei-folgeNN.mp4`. Aus dem fertigen Video eine Kontaktbogen-Grafik (7 Frames nebeneinander, ffmpeg hstack) machen und ansehen.

## 5. Freigabe durch Jona
- Video per SendUserFile schicken (Dateiname eindeutig, z. B. `hamsterfrei-folgeNN-<wort>.mp4`, nie denselben Namen wiederverwenden) + Caption + DM-Plan-Entwurf.
- SendUserMessage + PushNotification: „HAMSTERFREI Folge NN bereit (<Thema>). Antworte ‚ok‘, dann geht sie um 18:00 raus – oder schreib Änderungen.“
- `docs/plaene/<WORT>.md` als Entwurf anlegen (Aufbau wie SHOP.md: 6–8 konkrete Schritte inkl. Pflichtzeug wie Gewerbe/Impressum/Steuern/Produktsicherheit, kein Link).
- Committen und pushen (Stand „wartet auf Freigabe“ in `state/log.md`).
- **Ohne Jonas „ok“ in dieser Sitzung wird nichts veröffentlicht.** Änderungswünsche umsetzen, neu rendern, neu schicken.

## 6. Veröffentlichen (nur nach „ok“)
- Chrome über die Claude-in-Chrome-Tools. In EINEM ToolSearch laden: list_connected_browsers, select_browser, tabs_context_mcp, tabs_create_mcp, navigate, find, read_page, computer, file_upload, javascript_tool, get_page_text, tabs_close_mcp, browser_batch.
- **Seit 30.10.2026 hat Jona drei getrennte Chrome-Profile:** Hamsterfrei (Google-Konto bartenbach.jona@gmail.com) ist deviceId `2d7e7af3-dde1-4461-93af-738582ea1b9c` ODER `93e4a890-9262-4c31-b12b-8deb51641c1f`, noch nicht endgültig geklärt. **deviceId `3fb31033-7664-45bc-9b00-7ffb5fb04b01` ist schattengast und wird nie ausgewählt.** ACHTUNG: Die Anzeigenamen „Browser 1/2/3“ wechseln bei jedem Neustart – nur nach deviceId gehen! Benutzt wird nur der der beiden, in dem die Kontoprüfung `hamsterfrei` ergibt; stand 30.10. 01:35 zeigten beide noch groschenfall_yt. Die beiden anderen Profile gehören groschenfall bzw. schattengast und werden **nie** ausgewählt, nicht einmal zum Nachschauen. Mit `select_browser` gezielt per deviceId wählen (nicht switch_browser). Fehlt es in `list_connected_browsers` oder hat sich die Zuordnung geändert: nichts tun, Jona per Push melden.
- Danach trotzdem immer das Konto prüfen (unten). Zeigt TikTok/Instagram/YouTube dort ein anderes Konto als hamsterfrei: sofort Tab schließen, nichts lesen oder klicken, Jona melden.
- Browser wählen, in dem TikTok das Konto **hamsterfrei** zeigt: `fetch('https://www.tiktok.com/passport/web/account/info/?aid=1988').then(r=>r.json())` → username muss `hamsterfrei` sein. Falls JS blockiert: tiktok.com/profile öffnen und auf @hamsterfrei prüfen. Ein Browser mit groschenfall_yt oder schattengast wird nie benutzt.
- `https://www.tiktok.com/tiktokstudio/upload` → versteckten Video-File-Input per find suchen → `file_upload` mit dem Pfad im Arbeitsverzeichnis (Pfad aus /home/claude/…; /mnt/user-data/outputs wird abgelehnt).
- Popup „Automatische Inhaltsprüfungen“ mit „Abbrechen“ schließen.
- Beschreibung leeren, Caption eintippen (beginnt mit „Werbung |“ bei Affiliate-Folgen), Hashtags anhängen, Escape.
- „Mehr anzeigen“: Beitragsinhalt offenlegen → „Deine Marke“ (nur bei Werbung), „KI-generierter Inhalt“ an (Dialog „Aktivieren“).
- „Wann veröffentlichen“: Ist es vor 17:50 → „Zeitplan“ auf heute 18:00. Danach → „Jetzt“.
- Vor dem Klick auf Veröffentlichen/Planen Screenshot prüfen (Caption, Schalter, Zeit). Danach in Studio → Beiträge prüfen, dass der Beitrag da ist.
- `docs/THEMEN.md` Status setzen, `docs/plaene/<WORT>.md` final, `state/log.md` Eintrag (Datum, Folge, Wort, Beispiel + Quelle, Uhrzeit, Link). Committen, pushen. Jona kurz melden.
- **YouTube Shorts** (gleiche Freigabe, gleiche Uhrzeit): studio.youtube.com, Kanal-ID `UCBmT3RjRK5PGk-YVTdFzuDA` prüfen (Name „Hamsterfrei“). `…/channel/UCBmT3RjRK5PGk-YVTdFzuDA/videos/upload?d=ud` → File-Input → Titel (kurz, mit „#shorts“), Beschreibung („Werbung | …“ + „Kommentier <WORT>, dann antworte ich dir mit dem Plan 🐹“ + Hashtags). „Nein, nicht speziell für Kinder“. „Mehr anzeigen“ → Bezahlte Werbung = Ja (bei Werbung), KI verwendet = Ja. Weiter ×3 → Sichtbarkeit: vor 17:50 „Veröffentlichungszeitpunkt festlegen“ heute 18:00, sonst „Öffentlich“. Link notieren.
- **Instagram Reel** (gleiche Freigabe): instagram.com → „Erstellen“ → File-Input im Dialog → Zuschneiden: Seitenverhältnis „Original“ → Weiter → Weiter → Caption („Werbung | … Kommentier <WORT> und ich schick dir den Plan per DM 🐹“ + Hashtags), KI-Label an → Teilen. Instagram-Web kann nicht planen: um 18:00 posten (bzw. nach dem Okay, wenn es schon später ist).

## Nie still abbrechen
Scheitert etwas (Credits, Render, Chrome nicht erreichbar, falsches Konto), Jona per Push melden, was fehlt.
