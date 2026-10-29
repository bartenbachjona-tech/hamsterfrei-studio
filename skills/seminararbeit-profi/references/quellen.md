# Quellen finden, bewerten und prüfen (Modus 2)

## Was als wissenschaftlich gilt (in dieser Reihenfolge bevorzugen)

1. **Fachaufsätze mit Peer-Review.** Viele sind frei zugänglich (Open Access), zum Beispiel bei MDPI, Springer Open, Frontiers, PLOS, über DOAJ oder Google Scholar mit dem Filter „PDF“.
2. **Amtliche Statistik:** Statistisches Bundesamt (Destatis), Bayerisches Landesamt für Statistik, Eurostat, nationale Statistikämter. Dazu den Tabellencode und den Stand notieren.
3. **Berichte von Behörden und Organisationen:** Ministerien, Umweltbundesamt, OECD, UN, WHO, EU-Parlament, Zentralbanken (Arbeitspapiere), Forschungsinstitute.
4. **Fachbücher.** Viele Lehrkräfte verlangen **mindestens ein Buch.** Ein gekauftes E-Book zählt meist, das kurz bestätigen lassen. Verlags-Leseproben sind möglich und werden im Literaturverzeichnis als „Leseprobe“ gekennzeichnet.
5. **Fachportale und Bundeszentralen:** bpb, Max-Planck-Institute, Universitätsseiten. Sie sind gut für den Einstieg, als Beleg aber nur ergänzend.
6. **Presse** nur in Ausnahmefällen, für aktuelle Ereignisse oder als Stimmungsbild.

Nicht verwenden:
- Wikipedia als Beleg. Als Einstieg ist sie in Ordnung, die Quellen am Ende des Artikels führen weiter.
- Blogs, Foren, Firmen-Werbung
- KI-Antworten als Quelle
- Quellen, die man nicht selbst einsehen kann, etwa hinter einer Bezahlschranke, wenn nur der Abstract sichtbar ist

## Ablauf

1. **Suchen.** Ist eine Websuche verfügbar, suchst du gezielt, auch auf Englisch, und bevorzugst Primärquellen. Ohne Websuche bittest du den Nutzer, PDFs oder Links hochzuladen. Er kann auch die Literaturliste seiner Lehrkraft schicken.
2. **Vorstellen**, als Tabelle mit diesen Spalten:
   - Nr
   - Kurzbeleg (Autor Jahr)
   - Art
   - Warum wissenschaftlich?
   - Belegt was?
   - Frei zugänglich?
   - Empfehlung
3. **Freigabe holen,** zum Beispiel: „Welche nehmen wir? (Empfohlen: 1, 3, 4)“. Nur freigegebene Quellen verwenden und sie in `Arbeitsstand.md` eintragen.
4. **Belegen,** sobald eine Quelle benutzt wird. Gleich die Abrufdaten notieren und an den Screenshot denken (siehe `belege.md`).

## Aussagen prüfen (für jede belegte Aussage)

1. Die Stelle im Original finden: Seite, Tabellenzeile oder Kapitel.
2. **Zahlen exakt übernehmen und richtig runden,** mit deutschem Dezimalkomma. x,5 wird kaufmännisch aufgerundet. Achtung: Pythons `round` rundet 64,5 auf 64 ab. Bei eigener Berechnung selbst nachrechnen und das Ergebnis dokumentieren.
3. **Seitenzahl:** Es zählt die gedruckte Seitenzahl, nicht die PDF-Seite. Bei Folien ohne Seitenzahl gilt die PDF-Seite.
4. **Nicht stärker formulieren als die Quelle.** Typische Fehler:
   - ein „oft“, das nicht in der Quelle steht
   - „deutlich“ statt nur „höher“
   - „die Bank“ statt „zwei Ökonomen der Bank“
   - ein Zusammenhang, den der Autor selbst nicht zieht
5. **Abweichungen zwischen Quellen offenlegen.** Die zitierte Quelle bestimmt den Wert. Ein Hinweis in die Fußnote, wenn es nötig ist.
6. **Offensichtliche Fehler** in Quellen, etwa Tippfehler in Tabellen, nicht stillschweigend korrigieren. Stattdessen in der Fußnote erklären.

Bei vielen Fußnoten die Prüfung nach Quellen gruppieren. Kannst du Hilfsagenten starten, verteile die Gruppen. Jeder Agent bekommt die Liste „Fußnote | Satz | Beleg“ und meldet zeilenweise OK, PROBLEM oder NICHT PRÜFBAR, immer mit dem wörtlichen Quellenbeleg. Die Ergebnisse bewertest du danach selbst und korrigierst nur echte Fehler.

## Praktische Zugänge

- **PDFs:** Text mit `pdftotext -layout` oder pypdf lesen. Für den Beleg die Seite mit `scripts/pdf_markieren.py` gelb markieren.
- **Statistik-Datenbanken** (Destatis GENESIS, PxWeb-Systeme):
  - Variablen wählen, Tabelle anzeigen, Screenshot als Beleg.
  - Tabellencode und „Stand“ notieren.
- **E-Books (Kindle im Browser):** Volltextsuche nutzen, Position notieren, Screenshot machen. Anmerkungen am Kapitelende enthalten oft die gesuchten Fakten.
- **Excel-Dateien von Behörden:** einlesen und die Werte als Tabelle zeigen. Im Beleg festhalten: „unverändert ausgelesen am …“.
- **Bibliothek:** Über die Stadt- oder Unibibliothek gibt es oft kostenlose E-Book-Ausleihe, etwa über Onleihe oder Springer-Zugänge.
