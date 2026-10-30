# Hamsterfrei – Kanalregeln (gehen immer vor)

Stand 29.10.2026, alles von Jona festgelegt.

## Kanal
- Name: **Hamsterfrei**. TikTok: @hamsterfrei (ehemals Jonas Konto mit ca. 2.400 Followern). Instagram: neues Konto (wird von Jona angelegt, noch offen).
- Maskottchen: gezeichneter Hamster mit gelockerter Büro-Krawatte (navy mit grünen Streifen), Zeigestab in der Hand, steht vor einer Leinwand. Alles, was erklärt wird, läuft auf der Leinwand. Komponente: `src/Hamster.tsx`, Layout: `src/Episode.tsx`. Stil nie ändern.
- Stimme: ElevenLabs „Hamsterfrei – Hamster“, Voice-ID `E6cNSOTqfEt7KnIGmkxz`, Modell `eleven_v3`. Comic-Hamster, leicht hoch, quirlig, gut verständlich.
- Musik: dezentes, eigenes ElevenLabs-Musikbett (Ukulele/Marimba, ruhig, ohne Gesang) unter jedem Video, Lautstärke ca. 10 %, sanft ein-/ausgeblendet. Datei `public/music/bett01.mp3`, Standard in `Episode`. Keine Trend-Sounds oder fremde Musik.
- Geld: primär Affiliate-Links + E-Mail-Liste. Später Nebenprodukt Anzeigen-Automation (Vinted/Kleinanzeigen/eBay).

## Ausrichtung (ab 30.10.2026, von Jona entschieden)
- Look, Stimme, Musik bleiben unverändert. Inhaltlich: **„Der Hamster nimmt dir mit KI Arbeit ab“** (Schule, Uni, Alltag, Verkaufen).
- **Bis 10.11.2026: Seminararbeit-Offensive hat Vorrang** (siehe `docs/plaene/SEMINAR.md`). TikTok-Bio bis 10.11.: „Seminararbeit bis 10.11.? Keine Angst 🐹 Hilfe hier ⬇️“, Link hamsterfrei.de/seminar. Danach entscheidet Jona über neue Bio (Varianten: „Ich nehm dir Arbeit ab 🐹 KI-Hilfe für Seminararbeit & Alltag ⬇️“ / „Weniger Stress, mehr frei 🐹 Claude-Skills für Schule & Alltag ⬇️“).
- Publikum sind auch Unter-18-Jährige: nie zum Kauf drängen, Produktseite nennt „Claude-Konto ab 18“.
- Nebenbei-Business-Videos (Format 1 unten) nur noch gelegentlich, nicht mehr Kern.

## Format 1 (ab jetzt nur gelegentlich): Der Hamster erklärt ein kleines Nebenbei-Business
- Kleine, unscheinbare Side Hustles. KEINE Gründergeschichten, keine „der hat Millionen gemacht“-Storys.
- Startet direkt mit der Anleitung („Such dir auf AliExpress …“), Schritt für Schritt, 45–55 s.
- **Immer konkret:** ein echtes, greifbares Beispiel, das gerade viral/aktuell ist („Zum Beispiel …“), und dieses Beispiel wird auf der Leinwand gezeigt. Tools (z. B. Shopify, Canva, Etsy, Printify, Vinted) werden Schritt für Schritt nachgebaut gezeigt, damit man sieht: ist einfach.
- Dropshipping darf gezeigt, aber nicht beim Namen genannt werden. Fachbegriffe vermeiden.
- Videos dürfen nicht wie Werbung anfangen. Kein „Haken“-Teil im Video. Kein gesprochener Satz über Werbelinks.
- Ende: „Die genaue Anleitung schick ich dir. Folg mir und kommentier WORT.“ Letztes Bild bleibt mit dem Wort (SHOP-Kommentarblase auf Handy).
- Folgen mit Affiliate-Tool: kleines „Werbung“-Label oben links im Bild + „Werbung |“ am Anfang der Caption. Auf TikTok „Beitragsinhalt offenlegen → Deine Marke“ und „KI-generierter Inhalt“ einschalten.
- Kein großer Titeltext im Video, Titel nur in Caption/Cover.

## Format 2 (später)
Zeigen, was jemand konkret macht und wie es funktioniert. Noch nicht produzieren.

## Ablauf und Freigabe
- Täglich ein Video, **Veröffentlichung 18:00 Uhr** (Europe/Berlin).
- **Jedes Video geht erst nach Jonas ausdrücklichem „ok“ online** (Freigabe in der Sitzung der Tagesproduktion). Ohne Okay wird nichts veröffentlicht.
- DMs: persönlicher Plan als Text (siehe `docs/plaene/`). Solange es keinen Affiliate-Link/keine Hamsterfrei-Seite gibt: **kein Link** in der DM. Sobald Jona einen Affiliate-Link freigibt, wird er in `docs/plaene/links.md` eingetragen und mit Kennzeichnung (*Werbelink) angehängt.

## Konten strikt trennen
- Nur das TikTok-Konto **hamsterfrei** benutzen. **groschenfall_yt** und **schattengast** und alle anderen Konten nie anfassen.
- Chrome: nur das Hamsterfrei-Profil (dem Hamsterfrei-deviceId, siehe PRODUKTION.md §6; deviceId 3fb31033… = schattengast, nie; Anzeigenamen „Browser N“ wechseln, nur deviceId zählt) per `select_browser` wählen. Die Chrome-Profile von groschenfall und schattengast nie auswählen. Vor jeder Aktion das eingeloggte Konto prüfen; falsches Konto → Tab schließen, nichts lesen, Jona melden.
- Nichts an Kontoeinstellungen, Passwörtern oder Zahlungsdaten ändern, nie ausloggen.
