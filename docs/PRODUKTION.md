# Tagesproduktion (läuft täglich mittags, Studio terminiert selbst für 18:00)

Stand 04.11.2026 (Marke v2). Zuerst lesen, in dieser Rangfolge: `docs/KANAL_REGELN.md` → `docs/brand/POSITIONIERUNG.md`, `STIMME.md`, `LOOK.md`, `SERIEN.md` → `docs/STUDIO_HANDBUCH.md` → `docs/AUSWERTUNG_AKTUELL.md` → diese Datei. Dazu `docs/THEMEN.md`, `state/log.md`. Bei Widerspruch gilt die höhere Datei (KANAL_REGELN, Rangfolge).

## 1. Vorbereitung
- Repo klonen bzw. `git pull`, dann `npm ci --loglevel=error` (dauert ein paar Minuten).
- Prüfen, ob für heute schon eine Folge terminiert/veröffentlicht ist (`state/log.md`). Wenn ja: nichts Neues bauen, nur melden (1 Video pro Tag).
- **Werbe-Quote prüfen** (ab 11.11.): Sind unter den letzten 4 Videos im Log schon eines mit Werbung, wird heute kein Werbe-Video gebaut (höchstens 1 von 5).
- Nächste Folge: bis 10.11. oberste Zeile mit Status `offen` in `docs/THEMEN.md` (Seminar-Offensive). Ab 11.11.: Idee aus einer Kernserie (`docs/brand/SERIEN.md`, 80 %) oder ein Experiment (20 %); Themen aus THEMEN.md werden dabei in eine Serie umgebaut. Testvariable aus AUSWERTUNG_AKTUELL beachten (welcher Hook-Typ ist heute dran?). Nummer NN zweistellig.

## 2. Idee → Pointe → Schlüsselbild → Hook (Handbuch G3, G1, G2)
Reihenfolge ist Pflicht, alles in `scripts/folgeNN.md` notieren:
1. **Pointe zuerst (G3):** Was ist das Ergebnis bzw. das Urteil am Ende? Ein Satz.
2. **Schlüsselbild (G1):** Frame 0 nach LOOK.md: Hamster tut etwas Absurd-Konkretes + echtes Ergebnis/Bildschirm auf der Leinwand. Hell, konkret, in 1 s verständlich. **Ohne starkes Schlüsselbild wird die Idee verworfen** (nächste Idee; Trichter: ≥ 3 Ideen prüfen, Ausschlusskriterien aus SERIEN.md).
3. **Hook-Paket (G2):** Hook in **mindestens 2 der 6 Hook-Formate** schreiben (Experimenter, Teacher, Contrarian, Magician, Investigator, Fortune Teller), die mit dem größten Kontrast zum Schlüsselbild wählen. Paket = Schlüsselbild + Text-Overlay (≤ 6 Wörter) + gesprochener Hook (1–2 Sätze) + Ton + TikTok-Cover. Signatur „Hamster-Test:“ nur in Serie (a) und erst ab 11.11. (STIMME.md).

## 3. Skript (30–50 s gesprochen, ca. 70–120 Wörter)
- **Echt machen:** Ergebnis selbst erzeugen (z. B. Claude-Antwort in dieser Sitzung, als Beispiel markiert) oder per WebSearch belegen (realistische Preise, Quelle + Datum im Skript). Zahlen nie erfinden; lieber ohne Zahl als mit falscher.
- Nach dem Hook alle 5–8 s eine Wendung („aber …“, „deshalb …“). Kontext tröpfchenweise.
- Ton, Bann-Phrasen, TTS-Regeln, Schluss: `docs/brand/STIMME.md` (kein Schluss-Signal; letzter Satz = Pointe, danach höchstens ein CTA-Satz mit echtem Nutzen). Der alte Pflichtschluss „Die genaue Anleitung schick ich dir …“ gilt nicht mehr.
- Werbung: nur wenn das Thema es trägt und die Quote es erlaubt; nie im Hook, Nutzen auch ohne Kauf (KANAL_REGELN).
- Untertitel-Mapping über `captionMap` (z. B. „neun Euro neunzig“ → „9,90 €“).
- **Erwartung (G7)** ins Skript und später ins Log: Aufrufe nach 48 h und Ø Wiedergabe (TikTok), Basis = Median aus `state/zahlen.md` (solange leer: „keine Basis“ notieren).
- Skript speichern: `scripts/folgeNN.md` (Serie/Experiment, Hook-Typ laut Testvariable, Pointe, Schlüsselbild, beide Hook-Varianten, Sprechtext, Szenenplan, Overlay, Cover, Caption, Wort, Werbung ja/nein, Quellen, Erwartung).

## 4. Text-Kritiker (Agent `model: "fable"`, frischer Kontext)
Sieht nur: Skript, `docs/brand/*`, `docs/STUDIO_HANDBUCH.md`, KANAL_REGELN, AUSWERTUNG_AKTUELL. Ist kein fable-Agent verfügbar: Selbstprüfung nach derselben Rubrik, im Skript als „Selbstprüfung“ markieren.

**Harte Hook-Tore (alle ja, sonst sofort überarbeiten, Handbuch G2):**
1. Kein Delay: Thema in ≤ 1,5 s klar, kein Füllsatz.
2. Klarheit: einfache Wörter, aktiv, **kein KI-Jargon** (STIMME.md-Liste).
3. Relevanz: „du/dein“ oder Ich-hab's-ausprobiert + echte Situation aus dem Alltag der Zielgruppe.
4. Kontrast: A (was man glaubt) gegen B (was rauskam) erkennbar.
5. Alignment: Schlüsselbild, Overlay, Hook-Satz und Ton sagen dasselbe; funktioniert stumm.

**Rubrik (je 1–10):**
| # | Kriterium | 10 = |
|---|---|---|
| 1 | Schlüsselbild | Hamster tut etwas Absurd-Konkretes + echtes Ergebnis, in 1 s klar (LOOK.md) |
| 2 | Hook | Format bewusst gewählt, ≥ 2 Varianten geschrieben, größter Kontrast |
| 3 | Ergebnis statt Erklärung | Ergebnis kommt zuerst, Anleitung nur so viel wie nötig |
| 4 | Ehrlichkeit/Belege | jede Zahl und jede Ergebnis-Behauptung belegt, Schwäche gezeigt |
| 5 | Spannungsbogen | alle 5–8 s neue Information/Wendung, kein Füllsatz, Pointe am Ende |
| 6 | Stimme | Du-Form, kurze Sätze, keine Bann-Phrase, kein Schluss-Signal, TTS-tauglich (keine Gedankenstriche, Zahlen ausgeschrieben) |
| 7 | Sicherheit/Werbung | KANAL_REGELN erfüllt: keine Werbe-Eröffnung, Kennzeichnung, Quote, Minderjährige, kein Abschreib-/Einkommensversprechen |
| 8 | Serien-Treue | passt zum Bauplan der Serie bzw. ist als Experiment markiert; Testvariable eingehalten |

**Bestehen:** Ø ≥ 8,0, keine Note unter 6, **Kriterien 1, 4 und 7 ≥ 8**. Max. 2 Überarbeitungsrunden, sonst Idee verwerfen und nächste nehmen. Noten und übernommene Korrekturen ins Skript. Kommt dieselbe Korrektur dreimal vor, als feste Regel in `docs/brand/*` eintragen (G7).

## 5. Stimme (1 Take)
- ElevenLabs-Connector: `creative_create_flow`, dann `creative_generate_speech` mit voice_id `E6cNSOTqfEt7KnIGmkxz`, Modell `eleven_v3`, Text = Sprechtext, **`generations_count: 1`** (STIMME.md). Mit `creative_get_flow_run_status` pollen. Nie einen Generierungsaufruf wiederholen (kostet doppelt, ca. 700 Credits pro Take). Unbrauchbarer Satz → nur diesen Satz einzeln neu sprechen.
- Audio-URL per curl laden (storage.googleapis.com ist erreichbar) nach `public/folgen/folgeNN.mp3`.
- Wort-Zeitstempel: Take per `creative_add_flow_asset_node` anpinnen und `creative_transcribe_audio` (Scribe) mit connect_from darauf; Ergebnis als `src/folgen/folgeNN.words.json` im Format `{ "words": [{text,start,end,type}] }` speichern (Audio-Tag-Wörter `[…]` entfernen).
- Dauer messen (ffprobe). totalSeconds = Audiodauer + ca. 1,8 s. Erstes Wort möglichst ≤ 0,3 s.
- Credits-Fehler: sofort stoppen, Jona melden (SendUserMessage + PushNotification), nicht auf andere Stimmen ausweichen. Verbrauch ins Log.

## 6. Video (Remotion)
- `src/folgen/folgeNN.tsx` nach dem Muster der letzten Folge: `<Episode audio words scenes totalSeconds dingAt werbung captionMap startle? />`. In `src/Root.tsx` die Composition `FolgeNN` ergänzen. `werbung` nur bei Produkt-/Affiliate-Werbung auf `true` (Default in Episode ist `true` → bei Nicht-Werbung ausdrücklich `werbung={false}` setzen).
- Szenen für die Leinwand (948×1004 px) in `src/scenes/folgeNN.tsx`; vorhandene Bausteine aus `src/Scenes.tsx`, `src/ScenesV2.tsx` wiederverwenden. Farben/Schrift/Figur nach LOOK.md. Bewährte Bausteine nicht ändern, sondern kopieren.
- Frame 0 = Schlüsselbild aus Schritt 2 (nie leer, nie ein Einblenden aus Leer). Szenenwechsel und Einblendungen auf die Wort-Zeitstempel legen; pro Beat ein neues Element (Shot-Variation, LOOK.md).
- Endbild nach LOOK.md (Handy mit Kommentarblase bei Kommentar-Wort, `dingAt` ≈ Zeitpunkt des Worts; sonst Pointe groß).
- Cover/Titelbild: Standbild des Schlüsselbilds mit Overlay (LOOK.md), als PNG.
- `npx tsc --noEmit`, dann Standbilder (`npx remotion still FolgeNN --frame=…`) bei **Frame 0, 0,5 s, 1 s, 2 s** und je Szene einmal: nichts überlappt, Untertitel passen, Hamster verdeckt nichts, Text lesbar.
- Rendern: `npx remotion render FolgeNN out/hamsterfrei-folgeNN.mp4`.

## 7. Bild-Kritiker am Kontaktbogen (Pflicht, frischer Kontext, Handbuch G8)
- Kontaktbögen per ffmpeg (hstack) aus dem fertigen Video: **Bogen A = Hook** (Frame 0, 0,5 s, 1 s, 2 s), **Bogen B = ganzes Video** (7–8 Frames gleichmäßig + Endbild). Dazu das Cover.
- Kritiker (Agent `model: "fable"`) sieht nur Kontaktbögen, Cover, `docs/brand/*` und das Handbuch, nicht das Skript. Er prüft:
  - **Stumm-Test** (Bogen A): Ist ohne Ton klar, worum es geht? (ja/knapp/nein)
  - Schlüsselbild nach LOOK.md: Hamster tut etwas Konkretes + echtes Ergebnis sichtbar; startle allein = durchgefallen.
  - Hamster unverändert (gleiche Figur, Krawatte, Farben), kein großer Titeltext, kein Logo/Intro, Werbe-Label nur bei Werbung und nicht über dem Schlüsselbild.
  - Jede Einstellung in 1 s erkennbar, keine zwei gleichen Einstellungen ohne neue Information hintereinander, Text auf dem Handy lesbar.
  - Cover = gleiche Aussage wie der Hook.
- Urteil **pass / nachbessern** mit Note; Freigabe ab 8/10. Max. 2 Runden, sonst nicht terminieren (Log + Jona melden).

## 7b. Zuschauer-Test (Pflicht, docs/VIDEO_TEST.md)
- Material nach `docs/video_test/<folge>/material/` (Kontaktbögen, Cover, `text.md` mit gesprochenem Text, Bildschirmtexten, Caption, ggf. Zielseiten-Kurzfassung).
- 2 Agenten mit dem Auftrag aus `docs/video_test/AUFTRAG.md` (Archetypen 1–25 bzw. 26–50 aus `docs/produktsim/personas.json`), dann `python3 scripts/video_panel.py docs/video_test/<folge>/`.
- Behebbarer Hauptgrund (≥ 15 % der Abspringer einer Stufe) → eine Nachbesserungsrunde, erneut testen. Ergebnis (bis Ende / Website / Kauf bzw. Folgen pro 1.000 + Top-Gründe) ins Skript, ins Log und in die Nachricht an Jona.

## 8. Checkliste vor dem Terminieren (Handbuch G10)
Alle Punkte aus Handbuch G10 abhaken und im Skript vermerken (Schlüsselbild, Hook-Tore, ≥ 2 Hook-Varianten, Pointe zuerst, Signatur ohne Intro/Schluss-Signal, Serie/Experiment, Testvariable, Cover, Erwartung, Sicherheit). Zusätzlich: Werbung ja/nein korrekt (Label, Caption, Quote), „Claude-Konto ab 18“, wenn ein Claude-Weg gezeigt wird.

## 9. Terminieren bzw. Freigabe
- **Video ohne Werbung:** nach Freigabe von Text- und Bild-Kritiker **selbst für heute 18:00 terminieren** (Schritt 10). Danach Jona informieren (SendUserFile mit eindeutigem Dateinamen, z. B. `hamsterfrei-folgeNN-<wort>.mp4`, nie denselben Namen wiederverwenden; SendUserMessage + PushNotification): „HAMSTERFREI Folge NN (<Thema>) ist für 18:00 terminiert (TikTok, YouTube, Instagram). Schreib ‚stopp‘, wenn sie nicht raus soll.“ + Caption + Links.
- **Video mit Werbung (eigenes Produkt oder Affiliate):** nicht terminieren, bevor Jona zu genau diesem Video ausdrücklich „ok“ schreibt. Video + Caption schicken: „HAMSTERFREI Folge NN (<Thema>) ist WERBUNG für <Produkt>. Antworte ‚ok‘, dann terminiere ich sie für 18:00 – oder schreib Änderungen.“ Kommt das OK bis 17:30, terminieren; sonst bleibt das Video liegen (Log „wartet auf OK“), heute nichts anderes nachschieben.
- **Stopp von Jona** (jederzeit vor 18:00): Termine auf allen drei Plattformen löschen bzw. auf privat/Entwurf setzen, Log „gestoppt“, nichts neu terminieren, bis er antwortet.
- Spätstart: Ist die Folge nach 17:30 erst fertig, für morgen 18:00 terminieren (falls morgen noch frei).
- `docs/plaene/<WORT>.md` als DM-Plan anlegen (nur Gratis-Teil, kein Kauflink; Link-Regeln: KOMMENTARE_DMS.md).

## 10. Terminieren in Chrome
- Chrome über die Claude-in-Chrome-Tools. In EINEM ToolSearch laden: list_connected_browsers, select_browser, tabs_context_mcp, tabs_create_mcp, navigate, find, read_page, computer, file_upload, javascript_tool, get_page_text, tabs_close_mcp, browser_batch.
- **Hamsterfrei-Chrome = deviceId `2d7e7af3-dde1-4461-93af-738582ea1b9c`** (geklärt 30.10. 13:35: TikTok @hamsterfrei, YouTube Studio Kanal Hamsterfrei UCBmT3RjRK5PGk-YVTdFzuDA, Instagram hamsterfrei, Digistore, STRATO). `93e4a890-9262-4c31-b12b-8deb51641c1f` zeigte groschenfall → nie benutzen. `3fb31033-7664-45bc-9b00-7ffb5fb04b01` = schattengast → nie, nicht einmal zum Nachschauen. Die Anzeigenamen „Browser 1/2/3“ wechseln bei jedem Neustart, nur die deviceId zählt. Mit `select_browser` gezielt per deviceId wählen (nicht switch_browser). Fehlt das Profil in `list_connected_browsers` oder ergibt die Kontoprüfung nicht hamsterfrei: nichts tun, Jona per Push melden.
- **Kontoprüfung vor jeder Aktion:** `fetch('https://www.tiktok.com/passport/web/account/info/?aid=1988').then(r=>r.json())` → username muss `hamsterfrei` sein (falls JS blockiert: tiktok.com/profile muss auf /@hamsterfrei leiten); YouTube Studio #entity-name = Hamsterfrei. Anderes Konto (groschenfall_yt, schattengast, …): sofort Tab schließen, nichts lesen oder klicken, Jona melden.
- **TikTok:** `https://www.tiktok.com/tiktokstudio/upload` → versteckten Video-File-Input per find suchen → `file_upload` mit dem Pfad im Arbeitsverzeichnis (Pfad aus /home/claude/…; /mnt/user-data/outputs wird abgelehnt). Popup „Automatische Inhaltsprüfungen“ mit „Abbrechen“ schließen. Beschreibung leeren, Caption eintippen (beginnt bei Werbung mit „Werbung: mein eigenes Produkt |“), Hashtags anhängen, Escape. Cover aus Schritt 6 setzen, falls möglich. „Mehr anzeigen“: Beitragsinhalt offenlegen → „Deine Marke“ (nur bei Werbung), „KI-generierter Inhalt“ an (Dialog „Aktivieren“). „Wann veröffentlichen“ → **„Zeitplan“ auf 18:00** (heute bzw. Spätstart morgen). Vor dem Klick auf „Planen“ Screenshot prüfen (Caption, Schalter, Zeit). Danach in Studio → Beiträge prüfen, dass der Beitrag geplant ist.
- **YouTube Shorts:** studio.youtube.com, Kanal-ID `UCBmT3RjRK5PGk-YVTdFzuDA` prüfen (Name „Hamsterfrei“). `…/channel/UCBmT3RjRK5PGk-YVTdFzuDA/videos/upload?d=ud` → File-Input → Titel (Hook-Satz, kurz, mit „#shorts“), Beschreibung (bei Werbung „Werbung: mein eigenes Produkt | …“; bei Kommentar-Wort „Kommentier <WORT>, dann antworte ich dir mit <Gratis-Nutzen> 🐹“; „KI-animiert.“ + Hashtags). **„Nein, nicht speziell für Kinder“** (nie Made for Kids). „Mehr anzeigen“ → Bezahlte Werbung = Ja (nur bei Werbung), KI verwendet = Ja. Weiter ×3 → „Veröffentlichungszeitpunkt festlegen“ → 18:00. Link notieren.
- **Instagram Reel:** Instagram-Web kann nicht planen. Zuerst versuchen, über die Meta Business Suite (business.facebook.com, nur wenn dort das Konto hamsterfrei verbunden ist und keine neue Anmeldung nötig ist) für 18:00 zu planen. Geht das nicht: im Log „IG offen 18:00“ eintragen; der erste Lauf von „Kommentare & DMs“ nach 18:00 postet das Reel (instagram.com → „Erstellen“ → File-Input → Seitenverhältnis „Original“ → Weiter → Weiter → Caption wie TikTok + KI-Label an → Teilen), **aber nur, wenn Jona nicht gestoppt hat** (und bei Werbung sein OK vorliegt). Datei dafür im Repo-Ordner `out/` bzw. Pfad im Log angeben.
- Danach: `docs/THEMEN.md` Status setzen (`terminiert <Datum> 18:00`), `state/log.md` Eintrag (Datum, Folge, Serie/Experiment, Hook-Typ, Wort, Werbung ja/nein, Beispiel + Quelle, Kritiker-Noten, Erwartung 48 h, Termine + Links, Credits). Committen, pushen.

## Nie still abbrechen
Scheitert etwas (Credits, Render, Kritiker, Chrome nicht erreichbar, falsches Konto), Jona per Push melden, was fehlt, und im Log festhalten.
