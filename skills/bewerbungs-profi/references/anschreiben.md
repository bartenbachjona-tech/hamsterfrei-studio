# Phase 5: Anschreiben / Motivationsschreiben

## Inhalt
1. Brauche ich überhaupt eins? (Variante wählen)
2. Aufbau
3. Sprache: echt statt KI-glatt
4. Beispiel schlecht → gut
5. Erzeugen, prüfen, zeigen
6. Motivationsschreiben (Studium, duales Studium)

---

## 1. Brauche ich überhaupt eins? (Variante wählen)

Zahlen zur Einordnung (Jobportale, eigenes Interesse beachten): Laut Stepstone (700 Recruiter, 07/2025) verlangen 55 % der Unternehmen ein Anschreiben, aber nur 34 % halten es für entscheidend. Laut Indeed (10/2026) haben 35 % der HR-Verantwortlichen höchstens eine Minute pro Bewerbung.

| Situation | Variante |
|---|---|
| Anschreiben verlangt; Ausbildung, duales Studium, öffentlicher Dienst; Schweiz | **Vollständig**, max. 1 Seite, 3–4 Absätze |
| Anschreiben optional | **Kurzanschreiben** ca. 150–200 Wörter, oder 3–5 Sätze im Formular-/E-Mail-Feld |
| „ohne Anschreiben“ verlangt | **keins** schicken – auch wenn der Nutzer gern eins hätte (Risiko kurz erklären, er entscheidet) |
| Minijob | 3–5 Sätze in der Mail/im Formular reichen meist |

Frag nur, wenn es aus der Anzeige nicht klar ist (eine Frage, Empfehlung markieren).

## 2. Aufbau

1. **Betreff** mit Stellentitel genau wie in der Anzeige, ggf. Kennziffer und Starttermin.
2. **Persönliche Anrede** („Sehr geehrte Frau Sommer,“). Ohne Namen: „Sehr geehrte Damen und Herren,“ oder „Guten Tag, liebes …-Team,“. AT: akademische Titel (Mag., Dr.) in der Anrede.
3. **Einstieg ohne Floskel** – gleich der stärkste Bezug: ein konkreter Anlass, eine Erfahrung, die zur Kernanforderung passt, oder ein Telefonat („Danke für das Gespräch am …“). Nach der Anrede klein weiterschreiben.
4. **Belege statt Behauptungen:** 2–3 Anforderungen aus der Anzeige, je ein Beispiel (Situation, Handlung, Ergebnis) aus Phase 3. „Teamfähig“ allein überzeugt nicht; „Im Schülerfirma-Projekt habe ich mit 4 anderen den Verkaufsstand organisiert“ schon.
5. **Warum diese Firma:** ein konkreter Fakt (aus Frage 7 bzw. Recherche), kein Lob von der Startseite.
6. **Rahmen nur, wenn verlangt:** Eintrittstermin, Gehaltsvorstellung als Spanne in EUR brutto/Jahr. Praktikum/Werkstudent: Zeitraum, Stunden, Pflicht-/freiwilliges Praktikum.
7. **Schluss ohne Konjunktiv:** „Ich freue mich auf ein persönliches Gespräch.“ statt „würde mich freuen“.
8. Gruß, Name, ggf. „Anlagen: …“.

Länge: höchstens 1 Seite, 3–4 Absätze, aktive Verben, Ich-Sätze bewusst variieren.

## 3. Sprache: echt statt KI-glatt

Laut Stepstone (700 Recruiter, 06/2025) nutzen rund 2 von 3 Bewerbenden KI; 73 % der Recruiter finden solche Bewerbungen weniger authentisch, 75 % sehen oft übertriebene Qualifikationen. Typische KI-Muster: austauschbare Floskeln, gleiche Satzbaumuster, Buzzwords, „unnatürliche Perfektion“, Konjunktiv-Häufung, aufgeblähte Rollen.

Darum:
- **Motivation und Beispiele kommen vom Nutzer** (Phase 3). Fehlt etwas: nachfragen oder `[PRÜFEN: …]` – nie selbst ausdenken.
- In der Sprache des Nutzers schreiben (Alter, Bildungsweg). Ein 17-jähriger Realschüler klingt anders als eine Werkstudentin im Master.
- Verboten: „hiermit bewerbe ich mich“, „mit großem Interesse“, „würde mich freuen“, „teamfähig, belastbar und flexibel“, gleichförmige Dreier-Aufzählungen.
- Jeder Satz muss im Gespräch erklärbar sein. Am Ende den Nutzer fragen: „Kannst du zu jedem Satz eine kleine Geschichte erzählen?“
- Kein Copy-and-paste zwischen Bewerbungen: Firmenname, Ansprechperson, Stelle bei jeder Bewerbung neu prüfen (`endcheck.py --firma`).

## 4. Beispiel schlecht → gut

**Schlecht** (generisch, Floskeln, Konjunktiv, Behauptungen ohne Beleg):
> Sehr geehrte Damen und Herren,
> hiermit bewerbe ich mich mit großem Interesse um einen Ausbildungsplatz in Ihrem renommierten Unternehmen. Ich bin teamfähig, belastbar und flexibel und bringe eine hohe Leidenschaft für kaufmännische Tätigkeiten mit. Über eine Einladung zu einem Vorstellungsgespräch würde ich mich sehr freuen.

**Gut** (aus echten Nutzer-Antworten gebaut, konkret, direkt):
> Sehr geehrte Frau Sommer,
> seit einem Jahr mache ich an der Kasse eines Supermarkts die Abrechnung am Schichtende selbst. Dabei habe ich gemerkt, wie gern ich Zahlen sauber und ohne Fehler abschließe.
> In Ihrer Anzeige nennen Sie Sorgfalt und Teamarbeit. In meinem Praktikum im Steuerbüro habe ich Belege sortiert und erfasst. In der Schülerfirma haben wir zu fünft einen Verkaufsstand geplant; ich habe die Kasse übernommen.
> Bei Ihnen reizt mich, dass Azubis laut Ihrer Karriereseite eigene Projekte betreuen. [PRÜFEN: Stimmt das so? Quelle: Karriereseite]
> Ich freue mich auf ein persönliches Gespräch.

Erklär dem Nutzer nach dem Entwurf in 2–3 Sätzen, warum der Text so gebaut ist – er muss ihn im Gespräch vertreten.

## 5. Erzeugen, prüfen, zeigen

1. Entwurf **erst im Chat zeigen** (der Text ist kurz genug) und fragen: „Klingt das nach dir? a) Ja b) Ändern: … c) Ganz anders: lockerer/förmlicher“.
2. Nach dem Ja: Absätze in den JSON-Block (`anschreiben.absaetze`), dann ausführen:
   `python3 "$S/unterlagen_erstellen.py" /tmp/bewerbung.json --nur anschreiben`
   → `Anschreiben_Vorname_Nachname_Firma.docx` und `.pdf`.
3. Prüfen: `python3 "$S/endcheck.py" /mnt/user-data/outputs/Anschreiben_….pdf --firma "…" --stelle "…"`. ❌ beheben, ⚠️ mit dem Nutzer kurz besprechen.
4. Kurzanschreiben / Formular-Text: als Textdatei `Kurzanschreiben_Firma.txt` ausgeben (für Copy-and-paste ins Formular) und im Chat zeigen. Zeichenlimit des Formulars erfragen, falls bekannt.

## 6. Motivationsschreiben (Studium, duales Studium)

Wird statt oder zusätzlich zum Anschreiben verlangt. Gleiche Regeln, aber Schwerpunkt: Warum dieses Fach/dieser Studiengang, was hat dich hingeführt (Schulfach, Projekt, Praktikum), was willst du danach. Beim dualen Studium beides: Warum der Betrieb **und** warum das Studienfach. Vorgaben der Hochschule bzw. des Betriebs (Länge, Fragen) gehen vor.
