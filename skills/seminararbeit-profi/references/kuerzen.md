# Umfang anpassen (Modus 7): Kürzen ohne Umschreiben

Viele erste Fassungen sind „viel zu lang“. Gekürzt wird so, dass das Übrige gleich oder fast gleich bleibt. Die Lehrkraft kennt oft schon Teile des Textes.

1. **Umfang richtig messen.** Mit `python scripts/formalia_check.py Arbeit.docx` bekommst du die Fließtextwörter ohne Fußnoten, Bildunterschriften und Verzeichnisse. Bei Calibri 12 bzw. Arial 11, 1,5-zeilig, entspricht eine Textseite etwa 300 Wörtern. Bei „ca. 10 reinen Textseiten“ liegt das Ziel also bei etwa 3.000 Wörtern. Ob Grafiken mitzählen, regelt das Merkblatt.
2. **Kürzungsbedarf je Kapitel** nach Gewicht verteilen. Das Hauptkapitel wird am wenigsten gekürzt, Grundlagenkapitel am meisten.
3. **Kürzungsvorschlag als markierte Kopie** erstellen, als .docx mit Änderungsfarben:
   - zu Streichendes **rot durchgestrichen**
   - Neues **grün unterstrichen**

   Dazu eine kurze Liste mit Kapitel, Wörtern vorher und nachher und den Gründen.
4. Was gestrichen wird, in dieser Reihenfolge:
   1. Meta-Sätze und Überleitungen ohne Inhalt
   2. Wertungen im Hauptteil
   3. doppelte Aussagen
   4. Zahlenkolonnen, die eine Grafik ersetzt
   5. Nebenaspekte, die die Forschungsfrage nicht braucht
   6. lange Detailbeispiele, von denen eines genügt

   Der Rest bleibt wörtlich stehen.
5. Nach der Freigabe umsetzen. Danach prüfen:
   - verwaiste Fußnoten
   - „ebd.“-Ketten
   - doppelte Leerzeichen, Punkte und leere Absätze
   - allein stehende Überschriften
   - nicht mehr zitierte Literatur, die raus muss, samt Beleg-Screenshot
   - Abbildungsnummern und Verweise
   - Inhaltsverzeichnis
6. Das Fazit darf leicht ergänzt werden, etwa um Zielkonflikte, wenn die Kürzung das nötig macht. Nur mit Freigabe.
7. `formalia_check.py` erneut ausführen und den neuen Umfang melden.

## Zu kurz? Gezielt ausbauen

1. Den Umfang messen (wie oben) und die Lücke in Wörtern pro Kapitel nennen.
2. **Lücken finden statt aufblähen.** Wo fehlt etwas, das die Forschungsfrage braucht? Typische Lücken:
   - ein fehlendes Unterkapitel, etwa Lösungsansätze, Gegenpositionen oder ein regionales Beispiel
   - Zahlen ohne Einordnung
   - Fachbegriffe ohne Erklärung
   - zu wenig Literaturarbeit („Laut …“, „… betont, dass …“)
   - eine Grafik mit Auswertung im Text
   - Fazit ohne Zielkonflikte oder Ausblick
3. Vorschlag als Liste: Kapitel, was ergänzt wird, welche Quelle (vorstellen und freigeben lassen, `quellen.md`) und ungefähre Wortzahl.
4. Umsetzen **nach der KI-Regel der Lehrkraft:**
   - Ist das Formulieren erlaubt, schreibst du einen Entwurf mit Belegen. Dazu kommt die Erklärung der Kernaussagen für das Prüfungsgespräch.
   - Ist es nicht erlaubt, lieferst du ein Stichpunkt-Gerüst mit Quellen und Seitenzahlen. Der Nutzer schreibt selbst, und du gibst danach Feedback.
5. Kein Füllstoff, also keine Wiederholungen, Floskeln oder Meta-Sätze. Lehrkräfte merken das sofort.
