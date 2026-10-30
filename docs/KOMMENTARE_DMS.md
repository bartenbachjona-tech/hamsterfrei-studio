# Kommentare & DMs (alle 2 Stunden)

Zuerst lesen: `docs/KANAL_REGELN.md`, `docs/THEMEN.md` (welche Wörter gehören zu welcher Folge), `docs/plaene/links.md`, `state/dm_log.csv`.

## Browser
- Claude-in-Chrome-Tools in EINEM ToolSearch laden: list_connected_browsers, select_browser, tabs_context_mcp, tabs_create_mcp, navigate, find, read_page, get_page_text, computer, javascript_tool, browser_batch, tabs_close_mcp.
- Nur das Hamsterfrei-Chrome-Profil nutzen: `select_browser` mit deviceId `2d7e7af3-dde1-4461-93af-738582ea1b9c` („Browser 1“, Google-Konto bartenbach.jona@gmail.com). Die Profile von groschenfall und schattengast nie auswählen. Details und Kontoprüfung: PRODUKTION.md §6.
- Vor jeder Aktion prüfen, dass TikTok/Instagram/YouTube **hamsterfrei** zeigt. Falsches Konto → Tab schließen, nichts lesen, Jona melden. Nie groschenfall_yt, schattengast oder andere Konten.
- Eigene Tabs am Ende schließen. Andere Automationen nutzen Chrome ebenfalls: zügig arbeiten, keine Tabs offen lassen.

## Ablauf
1. Kommentare lesen: TikTok Studio → Kommentare (`https://www.tiktok.com/tiktokstudio/comment`) bzw. jedes Hamsterfrei-Video der letzten 14 Tage.
2. Für jeden Kommentar, der ein Kommentar-Wort enthält (Groß/Kleinschreibung egal, Tippfehler tolerieren, z. B. „shop“, „Shop 🙏“) und dessen Nutzer in `state/dm_log.csv` noch nicht mit diesem Wort `gesendet` hat:
   a) Auf den Kommentar kurz antworten (variieren, z. B. „Ist unterwegs 📩“, „Schau in deine Nachrichten 🐹“, „Hab ich dir geschickt!“).
   b) DM senden: Text aus `docs/plaene/<WORT>.md`, {name} = angezeigter Name (Vorname, wenn erkennbar, sonst Nutzername ohne @), ggf. ein kurzer Satz passend zum Kommentar. Link nur, wenn in `links.md` freigegeben, dann mit „(*Werbelink)“.
   c) Kann keine Nachricht geschickt werden (TikTok erlaubt DMs oft nur zwischen Konten, die sich gegenseitig folgen): dem Nutzer zurückfolgen und erneut versuchen. Geht es dann noch nicht: auf den Kommentar antworten „Folg mir kurz, dann kann ich dir den Plan schicken 📩“ und im Log `wartet` setzen. `wartet`-Einträge in jedem Lauf erneut versuchen (max. 3 Tage, danach `aufgegeben`).
   d) Nach dem Senden prüfen, dass die Nachricht im Chat steht. Log-Zeile schreiben.
3. Antworten auf unsere DMs (Rückfragen) lesen: einfache Danke-Nachrichten mit einem kurzen, freundlichen Satz beantworten. Echte Fragen NICHT selbst beantworten, sondern Jona mit Antwortvorschlag melden.
4. Andere Kommentare: Hasskommentare/Spam nicht beantworten. Fragen zum Thema sammeln und Jona mit Antwortvorschlag melden (nicht selbst posten). Lob darf mit einem Herz geliked werden.

## Instagram und YouTube
- Instagram (@hamsterfrei): Kommentare unter den Reels lesen; bei Kommentar-Wort genauso: kurz antworten + DM mit dem Plan (Instagram erlaubt Nachrichtenanfragen auch ohne gegenseitiges Folgen). Gleiche Grenzen, gleiches Log (Spalte `nutzer` mit Präfix `ig:`).
- YouTube (Kanal Hamsterfrei): YouTube hat keine DMs. Bei Kommentar-Wort den Plan als **Antwort auf den Kommentar** posten (gekürzt auf die Schritte, ohne Link), Log mit Präfix `yt:`. Kommentare in YouTube Studio → Kommentare.

## Grenzen (Kontosicherheit)
- Pro Lauf höchstens 15 DMs und 20 Kommentar-Antworten, zwischen Aktionen ein paar Sekunden Pause, natürlich variierte Texte.
- Zeigt TikTok eine Warnung („zu schnell“, eingeschränkt, Captcha, Sicherheitsprüfung): sofort aufhören, nichts umgehen, kein Captcha lösen, Jona per Push melden.
- Nie Jonas private Daten nennen, keine fremden Links, nichts verkaufen oder versprechen (keine Einkommensversprechen).

## Log `state/dm_log.csv`
Spalten: `datum;nutzer;wort;kommentar;status;notiz` – Status: gesendet / wartet / aufgegeben / frage_an_jona.
Am Ende committen und pushen.

## Meldung an Jona
Nur wenn es etwas gibt (sonst keine Push): „HAMSTERFREI: X DMs gesendet (WORT: n), Y warten auf Follow, Z Fragen an dich:“ + Fragen mit Antwortvorschlag. Er antwortet in der Sitzung mit „ok“ oder Änderungen; erst dann senden.
