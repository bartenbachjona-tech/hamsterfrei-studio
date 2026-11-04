# Hamsterfrei – Look (Marke v2, Stand 04.11.2026)

Geht PRODUKTION.md vor. Sicherheit/Recht aus KANAL_REGELN geht dieser Datei vor.

## Was bleibt (Wiedererkennung)
- **Figur:** gezeichneter Hamster mit gelockerter Büro-Krawatte (navy mit grünen Streifen), Zeigestab, vor einer Leinwand (948×1004 px), auf der alles Gezeigte läuft. Fell `#E9A24E`, Outline `#3A2618`. Code: `src/Hamster.tsx`, Layout `src/Episode.tsx` (inkl. Prop `startle`), Ausschnitt `src/HamsterCut.tsx`.
- **Farben** (aus `src/Scenes.tsx`): INK `#3A2618`, GREEN `#23885A`, NAVY `#24426B`, CREAM `#FFF8EC`. Krawattenfarben (Navy + Grün) sind der Kanal-Farbcode: Text-Overlays und Markierungen in diesen Farben.
- **Schrift:** Fredoka (lokal in `public/fonts`).
- **Optik:** flach, freundlich, Vektor. Keine Fotos echter Personen, keine fremden Logos oder Produktfotos (Tool-Namen als Text sind ok, echte Bildschirm-Ergebnisse als eigene Nachzeichnung oder echter Screenshot ohne fremde Personendaten).
- **Ton-Signet:** Ding (`public/sfx/ding.wav`) beim Kommentar-Wort; Musikbett `bett01.mp3`.
- Untertitel wie bisher in `Episode` (mit `captionMap`).

## Sperre gelockert: „Stil nie ändern“ → „nur schrittweise ändern“
Die alte Regel „Stil nie ändern“ ist mit Marke v2 aufgehoben (Jonas Freigabe 04.11.2026). Neu gilt:
- Änderungen an Figur und Look **nur schrittweise**: immer nur ein Baustein auf einmal, Proportionen, Farben und Krawatte bleiben gleich.
- Neue Teile entstehen **als Code-Bausteine** (Remotion-Komponenten), nie generiert. Änderungen an bewährten Bausteinen nur in einer Kopie, und es wird festgehalten, was gleich bleiben muss (Handbuch G8).
- Ein Look-Baustein ist keine Testvariable neben der laufenden. Er kommt erst, wenn AUSWERTUNG_AKTUELL ihn als nächsten Schritt freigibt.

### Geplante Erweiterung (erst NACH dem Start der Auswertung: Zahlen zuerst)
Reihenfolge laut Marke v2: **zuerst Messung und Auswertung aufsetzen** (`docs/AUSWERTUNG_AKTUELL.md`, `state/zahlen.md`), dann die Figur ausbauen. Freigabe für den Bau gibt der erste Auswertungslauf mit Basiswerten.
- **6 Posen:** staunen, triumphieren, verzweifeln, schlafen, rennen, tippen.
- **Requisiten:** Laptop, Laufrad, Geldbündel.
- Umsetzung später als Props bzw. Varianten von `Hamster.tsx` (z. B. `pose="staunen"`, `prop="laptop"`) in einer Kopie; bis dahin wird nur mit dem vorhandenen Hamster (inkl. `startle`) gearbeitet.
- Bauplan pro Baustein: Standbild an Frame 0/0,5 s/1 s → Bild-Kritiker prüft „Gleicher Hamster? In 1 s erkennbar, was er tut?“ → erst dann in Folgen einsetzen.

## Frame 0 (Handbuch G1, Pflicht)
Frame 0 besteht aus zwei Dingen gleichzeitig:
1. **Der Hamster tut etwas Absurd-Konkretes, das die Aussage zeigt** (Magician-Prinzip). Beispiele: wirft das Laufrad aus dem Fenster (Nebenjob-Check „raus aus dem Hamsterrad“), schläft auf einem Stapel Bewerbungen, hält zwei Anzeigen hoch und eine ist mit „VERKAUFT“ gestempelt. Solange es die Posen noch nicht gibt: mit vorhandenen Mitteln (startle, Zeigestab, Requisit auf der Leinwand) eine konkrete Handlung zeigen.
2. **Schlüsselbild = echtes Ergebnis bzw. echter Bildschirm** auf der Leinwand: die fertige Anzeige, die Claude-Antwort, der Vorher/Nachher-Vergleich, die Stundenlohn-Rechnung. Groß genug, dass man es in 1 s erkennt.

- **„startle“ allein reicht nicht.** Ein hochschreckender Hamster vor leerer oder abstrakter Leinwand fällt durch.
- Frame 0 ist hell, nie leer, nie schwarz. Kein Titeltext-Block, kein Logo, keine Begrüßung.
- Text-Overlay höchstens 6 Wörter, stützt das Bild (Handbuch G2). Das Overlay ist kein großer Titel, sondern eine Zeile über dem Schlüsselbild.
- Das Signet (Hamster mit Krawatte) darf das Schlüsselbild nie verdecken.
- Das „Werbung“-Label oben links erscheint nur in Werbe-Videos (KANAL_REGELN) und darf das Schlüsselbild nicht verdecken. Werbe-Videos dürfen aber nicht mit Werbung *beginnen*: Frame 0 zeigt das Ergebnis, nie das Produkt.

## Shot-Variation (gegen „inauthentic content“, Handbuch G9)
- Pro Beat ein neues Element oder eine neue Ansicht auf der Leinwand (Nah auf Ergebnis, ganze Leinwand, Split-Screen, Handy-Ansicht, Chat-Ansicht).
- Folgen einer Serie variieren Setting, Szenenfolge und Requisiten. Keine zwei Folgen mit identischer Szenenfolge hintereinander.

## Endbild
- Handy mit Kommentarblase „<WORT>“ (SceneVideos-Prinzip), bleibt bis zum Ende; Ding auf das Wort (`dingAt`).
- Ohne Kommentar-Wort: letztes Bild = Pointe (Ergebnis groß) mit dem Hamster, kein Abspann.

## TikTok-Cover / Titelbild (Teil des Hook-Pakets)
- Cover = Schlüsselbild + Text-Overlay (≤ 6 Wörter) + Hamster, gleiche Aussage wie der Hook. Bei „Hamster-Test“ steht „HAMSTER-TEST“ klein als Serien-Kennung oben.
