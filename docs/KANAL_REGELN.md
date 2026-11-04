# Hamsterfrei – Kanalregeln (Sicherheit, Recht, Freigabe, Konten)

Stand 04.11.2026 (Marke v2, von Jona freigegeben). Ersetzt die Fassung vom 29./30.10.2026.

## Rangfolge (bei Widersprüchen gilt die höhere Ebene)
1. **Sicherheit und Recht** in dieser Datei (Freigabe, Werbung, Minderjährige, Konten)
2. **`docs/brand/*`** (POSITIONIERUNG, STIMME, LOOK, SERIEN)
3. **`docs/STUDIO_HANDBUCH.md`** (G1–G10, gilt für alle drei Studios)
4. **`docs/AUSWERTUNG_AKTUELL.md`** (aktueller Test, Messziele)
5. **`docs/PRODUKTION.md`**, danach `KOMMENTARE_DMS.md`, `THEMEN.md`, `TRENDS.md`, `VIRAL_FORMATE.md`, `docs/plaene/*`

Widerspricht eine niedrigere Datei einer höheren, gilt die höhere, und der Widerspruch wird im nächsten Lauf in der niedrigeren Datei bereinigt. Die Prompts der geplanten Aufgaben verweisen nur auf diese Dateien und enthalten keine eigenen Detailregeln.

## Kanal (kurz, Details in docs/brand/)
- Name **Hamsterfrei**. TikTok @hamsterfrei (ehemals Jonas Privatkonto mit ca. 2.400 Followern), Instagram @hamsterfrei, YouTube-Kanal Hamsterfrei `UCBmT3RjRK5PGk-YVTdFzuDA` (Details `state/konten.md`).
- Positionierung bis 10.11. Seminararbeit-Offensive, ab 11.11. „Der Hamster probiert's aus: KI-Tricks, die dir Zeit oder Geld bringen.“ → `docs/brand/POSITIONIERUNG.md`.
- Figur, Farben, Schrift, Musik → `docs/brand/LOOK.md` (Stil nur schrittweise ändern). Stimme → `docs/brand/STIMME.md`.
- TikTok-Bio bis 10.11.: „Seminararbeit bis 10.11.? Keine Angst 🐹 Hilfe hier ⬇️“, Link hamsterfrei.de/seminar. Danach entscheidet Jona (Vorschlag in POSITIONIERUNG.md).

## Takt
- **1 Video pro Tag, Veröffentlichung 18:00 Uhr** (Europe/Berlin) auf TikTok, YouTube Shorts und Instagram Reels. Das gilt auch während der Seminar-Offensive (die frühere Planung „2 Videos pro Tag um 16:30/20:30“ in SEMINAR.md ist aufgehoben).
- Ist für heute schon ein Video terminiert oder veröffentlicht, wird kein zweites hochgeladen.
- Die Posting-Zeit ist eine spätere Testvariable (nur über AUSWERTUNG_AKTUELL), jetzt nicht ändern.

## Freigabe und Terminieren (neu ab 04.11.2026, Jonas Entscheidung)
- **Das Studio terminiert Videos selbst für 18:00** auf YouTube, TikTok und Instagram, sobald Text-Kritiker und Bild-Kritiker freigegeben haben (PRODUKTION.md). Nie sofort veröffentlichen, immer terminieren (Ausnahme Instagram-Web ohne Planungsfunktion: siehe PRODUKTION.md).
- Jona bekommt nach dem Terminieren Video, Caption und Links (SendUserMessage + PushNotification) und **kann bis 18:00 stoppen**. Schreibt er „stopp“ oder Änderungen: Termine löschen bzw. auf privat/Entwurf setzen und nichts neu terminieren, bis er antwortet.
- **AUSNAHME – Werbung für eigene Produkte:** Videos, die das eigene Produkt zeigen, nennen, bewerben oder darauf verlinken (Digistore „**Seminararbeit-Profi**“ 757079, „**Anzeigen-Profi**“ 757063, auch per „Link in Bio“-Hinweis oder Werbe-Label), werden **nur nach Jonas ausdrücklichem „ok“** zu genau diesem Video terminiert. Ohne Okay: fertig bauen, Jona schicken, nicht terminieren. Gleiches gilt für Affiliate-Werbung.
- Kein Kritiker-OK (nach 2 Runden) → nicht terminieren, im Log mit Grund, Jona melden.

## Werbung
- **Höchstens 1 von 5 Videos** enthält Werbung (gezählt über die letzten 5 veröffentlichten bzw. terminierten Videos in `state/log.md`). Gilt ab 11.11.; bis 10.11. läuft die Seminar-Offensive mit Jonas Einzel-OK pro Werbe-Video (POSITIONIERUNG.md).
- **Nie als Eröffnung:** Frame 0, Hook und die ersten Sätze zeigen Nutzen bzw. Ergebnis, nie das Produkt, nie „Link in Bio“.
- **Immer mit echtem Nutzen im Video:** Wer nichts kauft, hat trotzdem etwas gelernt bzw. kann es nachmachen.
- **Immer gekennzeichnet:** „Werbung“-Label oben links im Bild (`werbung`-Prop in Episode), Caption beginnt mit „Werbung: mein eigenes Produkt |“ (bzw. „Werbung |“ bei Affiliate), TikTok „Beitragsinhalt offenlegen → Deine Marke“, YouTube „Bezahlte Werbung = Ja“, Instagram-Hinweis in der Caption. Videos ohne Produkt/Affiliate bekommen kein Werbe-Label.
- Keine Einkommensversprechen, keine Notengarantien, kein „unentdeckbar“ (Bann-Phrasen: `docs/brand/STIMME.md`).

## Minderjährige (Publikum enthält Unter-18-Jährige)
- **Kommentar-Wort-DMs enthalten nur den Gratis-Teil** (Anleitung, Checkliste, Prompts). **Kein Kauflink und keine Kaufaufforderung an erkennbar Minderjährige.** Weil das Alter in Kommentaren meist nicht sicher erkennbar ist, gilt praktisch: **Kommentar-Wort-DMs enthalten grundsätzlich keinen Kauflink und keine Kaufaufforderung.** Fragt ein erkennbar Erwachsener ausdrücklich nach dem Produkt, geht die Antwort als Vorschlag an Jona. Details `docs/KOMMENTARE_DMS.md`.
- Der **Link in der Bio bleibt** (Verkaufsseite nennt „Claude-Konto ab 18“).
- Wird ein Claude-Weg gezeigt: Hinweis „Claude-Konto ab 18“ im Bild oder in der Caption.
- Nie zum Kauf drängen, keine künstliche Verknappung.
- **Nie „Made for Kids“** einstellen (YouTube: „Nein, nicht speziell für Kinder“; sonst fallen die Kommentare weg).

## Plattform-Sicherheit
- KI-Label an (TikTok „KI-generierter Inhalt“, YouTube „KI verwendet = Ja“, Instagram KI-Label), „KI-animiert“ in Bio bzw. Beschreibung.
- Keine Trend-Sounds, keine fremde Musik, keine fremden Logos/Produktfotos, keine fremden Skripte oder Geschichten (Handbuch G9).
- „Kommentier X“ nur mit echtem Gegenwert (gilt sonst als Engagement-Köder).

## DMs und Links
- DM-Texte stehen in `docs/plaene/<WORT>.md`. Kauflinks (eigene Produkte, Affiliate) kommen nicht in Kommentar-Wort-DMs (siehe Minderjährige). Andere Links (z. B. Gratis-Vorlage) nur, wenn Jona sie in `docs/plaene/links.md` freigegeben hat.
- Ablauf, Grenzen, Log: `docs/KOMMENTARE_DMS.md`.

## Konten strikt trennen
- Nur die Konten **hamsterfrei** (TikTok, Instagram) und den YouTube-Kanal **Hamsterfrei** benutzen. **groschenfall_yt**, **schattengast** und alle anderen Konten nie anfassen, auch nicht Jonas private Kleinanzeigen-/Vinted-Konten.
- Chrome: nur das Hamsterfrei-Profil per `select_browser` nach deviceId (PRODUKTION.md §10). deviceId `3fb31033…` = schattengast, nie. Anzeigenamen „Browser N“ wechseln, nur die deviceId zählt. Vor jeder Aktion das eingeloggte Konto prüfen; falsches Konto → Tab schließen, nichts lesen, Jona melden.
- Nichts an Kontoeinstellungen, Passwörtern oder Zahlungsdaten ändern, nie ausloggen.
