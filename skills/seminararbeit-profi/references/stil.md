# Schreiben und Überarbeiten (Modus 3)

## Ablauf pro Kapitel

1. Kurz klären: Welche Frage beantwortet das Kapitel, und wie zahlt es auf die Forschungsfrage ein?
2. Quellen recherchieren, vorstellen und freigeben lassen (`quellen.md`).
3. Den Inhalt als **Stichpunkt-Gerüst** vorschlagen: Aussage, Beleg und geplante Grafik. Der Nutzer gibt frei oder ändert.
4. Ausformulieren, nur so weit, wie die KI-Regel der Lehrkraft es erlaubt. Ist das Formulieren durch KI nicht erlaubt, schreibt der Nutzer selbst. Du gibst dann Feedback und Korrekturvorschläge, schreibst aber nichts neu.
5. Belegen: Nach jeder belegten Aussage eine Fußnote setzen (`zitieren.md`).
6. Die Stilregeln unten anwenden und `scripts/stilcheck.py` laufen lassen.
7. Dem Nutzer die 2–3 wichtigsten Aussagen des Kapitels in einfachen Worten erklären. Er soll sie für das Prüfungsgespräch verstehen.

Ist ein Kapitel nur teilweise vorhanden, überarbeitest du den Text nach den Regeln in `SKILL.md`: Vorschlag vor Änderung, so wenig wie möglich ändern.

## Der richtige Ton

Das Vorbild ist ein sachlicher Fachtext auf Schulniveau. Wenn die Lehrkraft eine Beispielarbeit hergibt, ist diese das Vorbild.
- sachlich und klar, mittellange Sätze mit wechselnder Länge
- Fachbegriffe beim ersten Auftreten kurz erklären: „Geysire, also heiße Quellen, die in Abständen Wasser ausstoßen“
- konkrete Zahlen mit Beleg statt Adjektiven
- präzise Angaben: „rund 290 km von Grönland“ statt „nahe Grönland“
- Zahlenkolonnen gehören in eine Grafik. Im Text steht dann „(vgl. Abbildung 2)“.
- deutsche Zahlschreibweise:
  - 2,3 Mio.
  - 103.000 km²
  - 8,8 % mit Leerzeichen vor dem Prozentzeichen
  - Bereiche mit Halbgeviertstrich: 2010–2025
- typografische Anführungszeichen „…“

## Was Lehrkräfte typischerweise anstreichen

| Randbemerkung | Bedeutung | Lösung |
|---|---|---|
| „Quelle?“ / „Woher weiß man das?“ | Beleg fehlt oder die Aussage geht über die Quelle hinaus | Beleg ergänzen oder die Aussage abschwächen |
| „Aussage?“ / „Inhalt?“ | Allgemeinplatz ohne Gehalt, z. B. „trägt wesentlich zur Stabilisierung bei“ | konkrete Zahl oder Tatsache einsetzen, sonst streichen |
| „W“ / „Wertung“ | Bewertung außerhalb des Fazits | sachlich formulieren oder ins Fazit verschieben |
| „A“ / „Ausdruck“, „Bz“ / „Bezug“ | unklare Wortwahl oder unklarer Bezug | präzise formulieren |
| „überflüssig“ | Meta-Satz wie „Dieses Kapitel stellt … vor“ | streichen |
| „ungenau“ | vage Angabe | konkrete Zahl, Ort oder Zeit |
| „visualisieren!“ / „Graphik?“ | Zahlen im Fließtext | Diagramm, Tabelle oder Karte |
| „Seitenumbruch!“ | Überschrift allein am Seitenende, leere Absätze | „Mit nächstem Absatz zusammenhalten“, leere Absätze löschen |
| „Das wäre ein großes Thema!“ | Nebenaspekt nur angerissen | vertiefen, wenn er für die Forschungsfrage wichtig ist, sonst knapp halten |
| „Z“ / „Zit.“ | Zitierfehler | Schema aus `zitieren.md` |

Lädt der Nutzer Fotos von Korrekturen hoch, entzifferst du jede Randbemerkung. Unsicheres markierst du als unsicher. Jede Bemerkung ordnest du einer konkreten Korrektur zu.

## Regeln für einen sachlichen, eigenen Stil

- **Keine Wertungen im Hauptteil.** Beispiele: „herausragend“, „überraschend“, „gewaltig“, „dramatisch“, „leider“, „beeindruckend“, „Das zeigt, wie …“
- **Keine Meta-Sätze:** „Im Folgenden …“, „Dieses Kapitel …“, „Diese Arbeit …“
- **Keine Floskeln:**
  - „darüber hinaus“
  - „spielt eine zentrale Rolle“
  - „maßgeblich“
  - „vielfältig“
  - „Fluch und Segen“
  - „zusammenfassend lässt sich festhalten“
  - „Spannungsfeld“
  - „nicht nur …, sondern auch …“ in Serie
- **Keine Muster:** Dreierlisten in jedem Absatz, Gedankenstrich-Einschübe, gleich lange Sätze, glatte Übergänge ohne Inhalt
- Konkrete Details sind besser als allgemeine Überleitungen.

Muss ein Text nach einem Detektor-Ergebnis überarbeitet werden: nur so viel ändern, wie für einen natürlichen, sachlichen Stil nötig ist, und **inhaltlich nichts**. Der Zweck ist ein besserer Text, nicht das Verschleiern unerlaubter KI-Nutzung. Mehr dazu in `endcheck.md`.
