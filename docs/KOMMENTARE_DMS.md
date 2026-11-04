# Kommentare & DMs (alle 2 Stunden)

Stand 04.11.2026 (Marke v2). Zuerst lesen: `docs/KANAL_REGELN.md` (Rangfolge, Minderjährige, Werbung), `docs/brand/STIMME.md` (Ton, Bann-Phrasen), `docs/THEMEN.md` (welche Wörter gehören zu welcher Folge), `docs/plaene/links.md`, `state/dm_log.csv`.

## Browser
- Claude-in-Chrome-Tools in EINEM ToolSearch laden: list_connected_browsers, select_browser, tabs_context_mcp, tabs_create_mcp, navigate, find, read_page, get_page_text, computer, javascript_tool, browser_batch, tabs_close_mcp.
- Nur das Hamsterfrei-Chrome-Profil nutzen: `select_browser` mit dem Hamsterfrei-deviceId (deviceIds in PRODUKTION.md §10), und zwar dem, in dem die Kontoprüfung hamsterfrei ergibt; deviceId 3fb31033… = schattengast, nie; Anzeigenamen „Browser N“ wechseln, nur deviceId zählt. Die Profile von groschenfall und schattengast nie auswählen. Details und Kontoprüfung: PRODUKTION.md §10.
- Vor jeder Aktion prüfen, dass TikTok/Instagram/YouTube **hamsterfrei** zeigt. Falsches Konto → Tab schließen, nichts lesen, Jona melden. Nie groschenfall_yt, schattengast oder andere Konten.
- Eigene Tabs am Ende schließen. Andere Automationen nutzen Chrome ebenfalls: zügig arbeiten, keine Tabs offen lassen.

## Ablauf
1. Kommentare lesen: TikTok Studio → Kommentare (`https://www.tiktok.com/tiktokstudio/comment`) bzw. jedes Hamsterfrei-Video der letzten 14 Tage.
2. Für jeden Kommentar, der ein Kommentar-Wort enthält (Groß/Kleinschreibung egal, Tippfehler tolerieren, z. B. „shop“, „Shop 🙏“) und dessen Nutzer in `state/dm_log.csv` noch nicht mit diesem Wort `gesendet` hat:
   a) Auf den Kommentar kurz antworten (variieren, z. B. „Ist unterwegs 📩“, „Schau in deine Nachrichten 🐹“, „Hab ich dir geschickt!“).
   b) DM senden: Text aus `docs/plaene/<WORT>.md`, {name} = angezeigter Name (Vorname, wenn erkennbar, sonst Nutzername ohne @), ggf. ein kurzer Satz passend zum Kommentar. **Die DM enthält nur den Gratis-Teil (Anleitung, Checkliste, Prompts): keinen Kauflink, keine Kaufaufforderung, keinen Produkt-Hinweis** (Publikum enthält Minderjährige, KANAL_REGELN). Enthält ein DM-Plan einen `{link}` oder Produkt-Satz, diesen Teil weglassen. Andere Links (z. B. Gratis-Vorlage) nur, wenn in `links.md` freigegeben. Fragt jemand, der erkennbar erwachsen ist, ausdrücklich nach dem Produkt: nicht selbst antworten, sondern Jona mit Antwortvorschlag melden (`frage_an_jona`).
   c) Kann keine Nachricht geschickt werden (TikTok erlaubt DMs oft nur zwischen Konten, die sich gegenseitig folgen): dem Nutzer zurückfolgen und erneut versuchen. Geht es dann noch nicht: auf den Kommentar antworten „Folg mir kurz, dann kann ich dir den Plan schicken 📩“ und im Log `wartet` setzen. `wartet`-Einträge in jedem Lauf erneut versuchen (max. 3 Tage, danach `aufgegeben`).
   d) Nach dem Senden prüfen, dass die Nachricht im Chat steht. Log-Zeile schreiben.
3. Antworten auf unsere DMs (Rückfragen) lesen: einfache Danke-Nachrichten mit einem kurzen, freundlichen Satz beantworten. Echte Fragen NICHT selbst beantworten, sondern Jona mit Antwortvorschlag melden.
4. Andere Kommentare: Hasskommentare/Spam nicht beantworten. Fragen zum Thema sammeln und Jona mit Antwortvorschlag melden (nicht selbst posten). Lob darf mit einem Herz geliked werden.

## Instagram und YouTube
- Instagram (@hamsterfrei): Kommentare unter den Reels lesen; bei Kommentar-Wort genauso: kurz antworten + DM mit dem Gratis-Teil (gleiche Regeln wie TikTok, kein Kauflink) (Instagram erlaubt Nachrichtenanfragen auch ohne gegenseitiges Folgen). Gleiche Grenzen, gleiches Log (Spalte `nutzer` mit Präfix `ig:`).
- YouTube (Kanal Hamsterfrei): YouTube hat keine DMs. Bei Kommentar-Wort den Plan als **Antwort auf den Kommentar** posten (gekürzt auf die Schritte, ohne Link), Log mit Präfix `yt:`. Kommentare in YouTube Studio → Kommentare.

## Offenes Instagram-Reel (aus der Tagesproduktion)
Steht in `state/log.md` für heute „IG offen 18:00“ und ist es nach 18:00: Reel posten wie in PRODUKTION.md §10 beschrieben, **nur wenn Jona nicht gestoppt hat** (Log/Sitzung prüfen) und bei Werbung sein OK vorliegt. Danach Log auf „IG gepostet <Uhrzeit>“ setzen.

## Zahlen nebenbei (für die Auswertung)
Wort-Kommentare und gesendete DMs stehen im Log; die Auswertungsroutine überträgt sie nach `state/zahlen.md`. Hier keine Studio-Zahlen erfassen.

## Grenzen (Kontosicherheit)
- Pro Lauf höchstens 15 DMs und 20 Kommentar-Antworten, zwischen Aktionen ein paar Sekunden Pause, natürlich variierte Texte.
- Zeigt TikTok eine Warnung („zu schnell“, eingeschränkt, Captcha, Sicherheitsprüfung): sofort aufhören, nichts umgehen, kein Captcha lösen, Jona per Push melden.
- Nie Jonas private Daten nennen, keine fremden Links, nichts verkaufen oder versprechen (keine Einkommensversprechen, keine Notengarantien).

## Log `state/dm_log.csv`
Spalten: `datum;nutzer;wort;kommentar;status;notiz` – Status: gesendet / wartet / aufgegeben / frage_an_jona.
Am Ende committen und pushen.

## Meldung an Jona
Nur wenn es etwas gibt (sonst keine Push): „HAMSTERFREI: X DMs gesendet (WORT: n), Y warten auf Follow, Z Fragen an dich:“ + Fragen mit Antwortvorschlag. Die Antworten auf diese **Fragen** werden erst nach Jonas „ok“ bzw. seinen Änderungen gesendet. Gratis-Teil-DMs zu Kommentar-Wörtern brauchen kein Einzel-OK.
