# Quellenbelege mit Screenshots (Modus 8)

Merkblätter verlangen bei Internetquellen die Adresse, das Abrufdatum und einen **Ausdruck oder eine Datei** des Beitrags. Mit sauberen Belegen zeigt man außerdem im Prüfungsgespräch, dass man jede Quelle wirklich gelesen hat. Jeder Beleg zeigt die URL, das Abrufdatum und die belegte Stelle.

## Schritt 1: Beleg-Liste erstellen (immer)

1. Mit `python scripts/textlib.py Arbeit.docx` alle Fußnoten je Kapitel auslesen.
2. Daraus eine To-do-Liste als `04_Belege/belege.csv` bauen. Trennzeichen ist das Semikolon. Spalten:
   `nr;kapitel;kurzbeleg;angabe;url;abgerufen;belegt;datei`
   - eine Zeile pro **belegter Stelle** (nicht pro Quelle); Nummer `Kapitel.laufend`, zum Beispiel `3.04`
   - `belegt`: was genau gezeigt wird, zum Beispiel „Zahl 2,3 Mio. (S. 7, Tab. 2)“ oder „Zitat S. 12“
   - `datei`: Dateiname des Screenshots, zum Beispiel `3.04_Mueller.png`
3. Zeige dem Nutzer die Liste: welche Seite er öffnen und was er auf dem Screenshot sichtbar machen soll. Dazu gehören die Adresszeile mit URL, die Textstelle und bei PDFs die Seitenzahl.

## Schritt 2: Screenshots besorgen (drei Wege)

**A) Kostenloses Claude, der Nutzer macht die Screenshots.**
- Am PC: Windows `Win + Umschalt + S`, Mac `Cmd + Umschalt + 4`. Am Handy die übliche Screenshot-Funktion.
- Die Adresszeile soll sichtbar sein. Die Stelle kann vorher markiert werden.
- Die Dateien benennt er wie in der Liste und lädt sie hier hoch, auch mehrere auf einmal.

**B) Für PDF-Quellen, die hochgeladen sind:** Die Seite selbst rendern und die Stelle gelb markieren:

```
python scripts/pdf_markieren.py Quelle.pdf PDF-SEITE "exakter Wortlaut" 04_Belege/Screenshots/3.04_Mueller.png
```

Dazu ein Bild vom Impressum bzw. der Titelseite der Quelle, damit Titel, Autor und Jahr belegt sind.

**C) Browser-Modus (optional).** Nur wenn ein Browser-Werkzeug verfügbar ist, etwa Claude in Chrome oder der Browser der Desktop-App:
- Du öffnest jede URL selbst, scrollst zur Stelle, markierst sie falls möglich und machst den Screenshot. Bei Kindle wird mit echten Klicks umgeblättert.
- Seiten mit Login öffnet der Nutzer selbst und meldet sich selbst an. Du gibst keine Passwörter ein.
- Cookie-Banner werden abgelehnt.

Die Wege lassen sich mischen. Ohne Browser-Werkzeug nie so tun, als wären Screenshots gemacht worden.

## Schritt 3: Beleg-PDFs bauen

```
python scripts/belege_pdf.py 04_Belege/belege.csv 04_Belege/Screenshots "04_Belege/Quellenbelege (Stand TT.MM.JJJJ)" --titel "Quellenbelege – <Thema>"
```

Ergebnis:
- je Kapitel ein Ordner mit beschrifteten Belegseiten
- je Kapitel eine PDF
- eine **Gesamt-PDF** mit Übersicht vorne
- `Übersicht.txt`

Jeder Beleg hat einen grauen Kopf mit Kapitel, Nummer, Kurzbeleg, vollständiger Angabe, URL (blau) und „abgerufen am | Belegt: …“. Lange Screenshots werden auf mehrere Seiten verteilt.

Danach:
- Die Gesamt-PDF stichprobenartig ansehen.
- Ist die Gesamt-PDF größer als 30 MB, mit `--qualitaet 45` neu bauen.
- Fehlende Screenshots meldet das Skript. Diese an den Nutzer zurückgeben.

## Sonderfälle

- **E-Book:** Screenshot mit Kindle-Position, Seitenhintergrund weiß. Dazu das Impressum mit ISBN und DOI.
- **Statistik-Tabellen:** Screenshot der gefilterten Tabelle mit Tabellencode und Stand. Bei eigener Berechnung kommt eine eigene Seite „Eigene Berechnung“ mit den Rechenwerten dazu.
- **Grafiken:** Beleg der Datengrundlage, „Grundlage Abb. n“.
- **Bücher ohne Online-Fassung:** Ein Ausdruck ist meist nicht verlangt. Auf Wunsch ein Foto von Titelseite und Impressum.

## Bei Änderungen der Arbeit

- Belege nachziehen: Neue Quellen kommen dazu, gestrichene fliegen raus, Nummern und Seitenangaben werden angepasst.
- Neue Fassung in einen **neuen Ordner mit Datum** speichern. Den Nutzer darauf hinweisen, dass er den alten Ordner selbst löscht.
- Für die Abgabe: ausdrucken, oder als PDF auf einen USB-Stick bzw. in die digitale Abgabe. Das sagt das Merkblatt.
