# Vorgaben und Formalia

Immer gilt zuerst das Merkblatt der eigenen Schule und was die Lehrkraft sagt. Die Werte hier sind übliche bayerische Vorgaben und gelten nur, wenn nichts anderes bekannt ist. Weichen sie vom Merkblatt ab, gilt das Merkblatt. Lädt der Nutzer sein Merkblatt hoch, ziehst du daraus die Werte und schreibst sie in den Arbeitsstand.

## Rechtlicher Rahmen in Bayern

Quellen: GSO § 24 (https://www.gesetze-bayern.de/Content/Document/BayGSO-24) und die Materialien auf https://www.oberstufe.bayern.de (Stand Oktober 2026). Ist eine Websuche verfügbar, prüfst du bei Bedarf, ob sich etwas geändert hat.

- **Abgabe:** spätestens am **2. Unterrichtstag im November** der Jahrgangsstufe 13. Die Herbstferien liegen davor. 2026 ist das meist Dienstag, der 10.11. Den genauen Termin nennt die Schule. Die Schule kann eine Uhrzeit festlegen. Eine Fristverlängerung gibt es nur in besonderen Fällen.
- Danach folgt ein **Prüfungsgespräch** zur Arbeit. Der Nutzer erläutert die Arbeit, fasst Ergebnisse zusammen und beantwortet Fragen. Die Details stehen in `coach.md`.
- **0 Punkte und keine Zulassung zum Abitur** drohen bei:
  - Nichtanfertigung
  - versäumter Abgabe
  - **Plagiat oder nicht selbstständiger Anfertigung**
- **Gewichtung** von schriftlicher Arbeit und Prüfungsgespräch: Bei der Lehrkraft erfragen. Früher galt 3 : 1 zur Abschlusspräsentation. Für den neuen G9-Jahrgang nennen Schulen teils andere Werte. Nichts behaupten, was nicht bestätigt ist.
- **Bewertet** werden Inhalt, Darstellung und Formalia, häufig im Verhältnis 3 : 2 : 1. Die Lehrkraft legt die Kriterien fest, oft mit einem Bewertungsbogen. Liegt er vor: hochladen lassen und danach prüfen.
- **Englisch als Leitfach:** Die Arbeit wird auf Englisch geschrieben. In anderen modernen Fremdsprachen ist die Fremdsprache oder Deutsch möglich.

## Übliche Merkblatt-Werte

| Punkt | üblich (Merkblatt prüfen!) |
|---|---|
| Umfang | ca. 10–15 DIN-A4-**Textseiten**; Deckblatt, Verzeichnisse, Anhang zählen meist nicht mit. Lehrkräfte geben oft weniger vor, etwa „ca. 10 reine Textseiten“. |
| Papier | DIN A4, einseitig |
| Ränder | links ca. 3 cm, rechts ca. 3–4 cm (Korrekturrand), oben und unten ca. 2,5 cm |
| Schrift | z. B. Arial 11 pt oder Calibri bzw. Times New Roman 12 pt |
| Zeilenabstand | 1,5-fach; Fußnoten und abgesetzte Zitate einzeilig |
| Satz | Blocksatz mit automatischer Silbentrennung |
| Fußnoten | kleiner, meist 10 pt |
| Seitenzahlen | oft zentriert in der Kopfzeile; Deckblatt (S. 1) und Inhaltsverzeichnis (S. 2) mitgezählt, aber ohne sichtbare Nummer |
| Überschriften | Dezimalgliederung 1, 1.1, 1.1.1; fett und größer; mit Abstand davor |
| Reihenfolge | Deckblatt → Inhaltsverzeichnis → Text → (Anhang) → Literaturverzeichnis → (Abbildungsverzeichnis) → **unterschriebene Erklärung als letzte nummerierte Seite** |
| Deckblatt | Vorlage der Schule verwenden (Schule, Abiturjahrgang, Leitfach, Rahmenthema, Thema, Name, Kursleitung, Abgabetermin, ggf. Felder für Bewertung) |
| Abgabe | oft Klemmmappe mit Klarsichtdeckel; ggf. zusätzlich digital |
| Internetquellen | Adresse und Abrufdatum; **Ausdruck bzw. Datei des Beitrags beilegen** → siehe `belege.md` |

**Erklärung:** Den Wortlaut nimmt man aus dem Merkblatt, mit Ort, Datum und Unterschrift. Ob und wie KI-Nutzung erwähnt wird, legt die Lehrkraft fest. Du formulierst nichts, was nicht stimmt.

## Gliederungsregeln

- Jedes Hauptkapitel hat entweder **mindestens zwei** Unterkapitel oder keins.
- Überschriften sind sachlich, ohne Fragen und ohne Wertung.
- Ob es eine Einleitung gibt, entscheidet die Lehrkraft. Manche wollen keine, viele wollen eine kurze.
- **Wertungen gehören ins Fazit.** Das Fazit beantwortet die Forschungsfrage ausdrücklich, nennt Zielkonflikte und Grenzen und endet mit einem Ausblick.

## Formalia-Check (Modus 5)

1. Prüfen:

   ```
   python scripts/formalia_check.py Arbeit.docx --soll-seiten 10-15 --schrift "Calibri 12,Arial 11" --zeilenabstand 1.5 > 05_Checks/Formalia_<Datum>.md
   ```

   Die Parameter stellst du auf die Vorgaben des Merkblatts ein. Die Wörter pro Seite liegen bei Calibri 12 / Arial 11 mit 1,5 Zeilen und üblichen Rändern bei etwa 300, als `--woerter-pro-seite` anpassbar.
2. Den Bericht lesen und für den Nutzer in eine kurze Liste übersetzen: zuerst ❌, dann ⚠️. Heuristische Treffer, etwa der Abgleich mit dem Literaturverzeichnis, selbst kontrollieren, bevor du sie meldest.
3. Korrigieren. In Word geht das zuverlässig über die Formatvorlagen. Für technische Änderungen an der .docx siehe unten. Danach den Check noch einmal laufen lassen.
4. Mit LibreOffice als PDF rendern, falls vorhanden (`soffice --headless --convert-to pdf`). Die Seiten ansehen auf allein stehende Überschriften, leere Seiten und Bilder.

## Word richtig einstellen (Anleitung für den Nutzer oder technische Umsetzung)

- **Formatvorlage „Standard“:** Schrift und Größe nach Merkblatt, Zeilenabstand 1,5 (in der XML `w:line="360" w:lineRule="auto"`), Blocksatz.
- **Silbentrennung:** Layout → Silbentrennung → Automatisch.
- **Ränder:** Layout → Seitenränder → Benutzerdefiniert. In der XML entspricht 1 cm ≈ 567 twips.
- **Überschrift 1/2:** nummeriert (Start → Liste mit mehreren Ebenen) und mit „Mit nächstem Absatz zusammenhalten“. Literaturverzeichnis und Erklärung sind Überschrift 1 **ohne Nummer**.
- **Seitenzahl:** Einfügen → Seitenzahl → Seitenanfang, zentriert. Deckblatt und Verzeichnis ohne sichtbare Nummer, über „Erste Seite anders“ oder einen eigenen Abschnitt. Die Zählung läuft trotzdem mit.
- **Fußnoten:** Referenzen → Fußnote einfügen; Fußnotentext 10 pt, einzeilig.
- **Inhaltsverzeichnis** als automatisches Feld (Referenzen → Inhaltsverzeichnis). Vor dem Drucken ins Verzeichnis klicken, F9 drücken und „Nur Seitenzahlen aktualisieren“ wählen.
- **Keine leeren Absätze** als Abstandshalter. Stattdessen „Abstand vor/nach“ nutzen.

## Technische .docx-Bearbeitung (wenn du die Datei selbst änderst)

- Nie das Original überschreiben. Arbeite an einer Kopie mit neuem Namen und lege vorher eine Sicherung an.
- Gibt es eine docx-Skill, nutze sie. Sonst so vorgehen:
  1. Entpacken.
  2. `word/document.xml` und `word/footnotes.xml` gezielt ändern.
  3. Neu packen, mit `[Content_Types].xml` zuerst.
- Text ist oft auf mehrere Runs verteilt. Ersetze darum mit eindeutigen Ankern und prüfe die Trefferzahl.
- Nach Änderungen an Fußnoten: Sind die Bezüge noch richtig? Gibt es verwaiste Fußnoten? Stimmen die „ebd.“-Ketten noch?
- Abschnittsumbrüche (`w:sectPr`) beim Löschen von Absätzen erhalten.
- Neue Bilder brauchen eine Relationship und bei .jpg einen Default-Eintrag in den Content-Types.
- Danach `formalia_check.py` laufen lassen und rendern. Liefere nie eine Datei aus, die nicht geöffnet und geprüft wurde.
