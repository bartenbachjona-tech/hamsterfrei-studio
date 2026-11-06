# Phase 4: Lebenslauf (tabellarisch, einspaltig, maschinenlesbar)

## Inhalt
1. Regeln für den Inhalt
2. Regeln für das Layout (ATS)
3. Daten als JSON
4. Erzeugen, prüfen, zeigen
5. Änderungswünsche

---

## 1. Regeln für den Inhalt

**Aufbau (in dieser Reihenfolge):**
1. Kopf: Name, Adresse, Telefon, seriöse E-Mail (vorname.nachname@…), optional LinkedIn. Ist die E-Mail-Adresse unseriös („partygirl03@…“), freundlich eine neue empfehlen.
2. Optional **Kurzprofil** (2–3 Zeilen): wer, was kann ich, was will ich – nur mit Fakten aus Phase 3.
3. **Berufserfahrung / Praktische Erfahrung** – **antichronologisch** (neueste zuerst).
4. **Ausbildung / Studium / Schulbildung**.
5. Praktika, Nebenjobs, **Ehrenamt** (eigener Abschnitt oder bei 3).
6. **Kenntnisse:** Sprachen mit Niveau (A1–C2), EDV konkret benannt, Führerschein.
7. Optional **Interessen** – nur, wenn sie etwas aussagen oder zur Stelle passen (Vereinstrainer, Gaming-Turniere organisieren). „Lesen, Freunde treffen“ weglassen.

Bei Einsteigern ohne Berufserfahrung darf „Schulbildung“ vor „Praktische Erfahrung“ stehen.

**Länge:** Schüler und Einsteiger **1 Seite**, mit Berufserfahrung höchstens 2 Seiten.

**Stichpunkte: Ergebnis statt Aufgabe**, 2–4 pro Station, aktive Verben:
- schwach: „zuständig für Kasse“
- gut: „Kassenabrechnung für 3 Filialen übernommen“ (nur wenn es so war!)

**Schlüsselwörter** aus der Anzeige im gleichen Wortlaut verwenden – nur, wo sie zutreffen.

**Lücken** über ~3 Monate kurz und ehrlich benennen, z. B. „Berufliche Orientierung“, „Pflege eines Angehörigen“, „Reise/Sprachkurs“, „Jobsuche, parallel Online-Kurs X“. Krankheitsdiagnosen muss niemand nennen.

**Foto:** freiwillig (AGG). Wenn gewünscht, Pfad im JSON unter `person.foto` – das Skript setzt es rechts oben (3,5 cm breit).

**Datum und Unterschrift:** bei Online-Bewerbungen nicht nötig, aber nicht falsch (`ort_datum_unterschrift`).

**Geburtsdatum:** freiwillig, nur auf Wunsch.

**Nichts erfinden:** Zeiträume, Noten, Niveaus, Titel nur vom Nutzer. Unklares als `[PRÜFEN: …]` – das Skript markiert es gelb.

## 2. Regeln für das Layout (ATS)

Viele Firmen lesen Lebensläufe maschinell aus (Bewerbermanagement-Systeme, ATS). Laut Indeed-Umfrage (10/2026, 300 HR-Verantwortliche) nutzen 42 % KI oder Software zur Vorauswahl; 11 % geben zu, dass aussortierte Bewerbungen kein Mensch mehr sieht. Darum:
- **einspaltig**, keine Word-Tabellen, keine Textspalten, keine Icons, Skill-Balken oder Grafiken
- gängige Schrift, Standard-Überschriften („Berufserfahrung“, „Ausbildung“, „Kenntnisse“)
- Abkürzungen ausschreiben, „EUR“ statt „€“
- PDF aus Word erzeugen, nicht als Canva-Grafik

`unterlagen_erstellen.py` hält das automatisch ein (Tabstopp statt Tabelle, Arial 11, A4). Hat der Nutzer einen eigenen, z. B. zweispaltigen Canva-Lebenslauf: `textlib.py --info` zeigt das Risiko; ehrlich erklären und die einspaltige Fassung anbieten. Er entscheidet.

## 3. Daten als JSON

Das Format zeigt `python3 "$S/unterlagen_erstellen.py" --beispiel`. Kurz:

```json
{
  "person": {"name": "", "strasse": "", "plz_ort": "", "telefon": "", "email": "", "linkedin": "", "geburtsdatum": "", "foto": ""},
  "ziel": {"art": "", "stelle": "", "firma": "", "kennziffer": "", "ansprechperson": "", "anrede": "", "firma_adresse": ["Zeile 1", "Zeile 2"]},
  "lebenslauf": {
    "kurzprofil": "",
    "abschnitte": [
      {"titel": "Praktische Erfahrung", "eintraege": [
        {"zeitraum": "09/2025 – heute", "titel": "Aushilfe Kasse (Minijob)", "ort": "Firma, Ort", "punkte": ["…"]}
      ]}
    ],
    "kenntnisse": [{"label": "Sprachen", "wert": "Deutsch (Muttersprache), Englisch (B1)"}],
    "interessen": "",
    "ort_datum_unterschrift": false
  },
  "anschreiben": {"betreff": "", "anrede": "", "absaetze": ["…"], "gruss": "Mit freundlichen Grüßen", "anlagen": ["Lebenslauf"], "ort_datum": ""}
}
```
- Zeiträume einheitlich `MM/JJJJ – MM/JJJJ` oder `seit MM/JJJJ`.
- Abschnitte ohne Einträge werden weggelassen.
- Die JSON-Daten kommen auch in die Akte (json-Block in Abschnitt 8), damit man in einem neuen Chat neu erzeugen kann.

## 4. Erzeugen, prüfen, zeigen

1. JSON nach `/tmp/bewerbung.json` schreiben (Arbeitsdatei, nicht zum Download).
2. Führe aus: `python3 "$S/unterlagen_erstellen.py" /tmp/bewerbung.json --nur lebenslauf`
   → `Lebenslauf_Vorname_Nachname.docx` und `.pdf` in `/mnt/user-data/outputs/` (bei vorhandener Datei automatisch `_v2`).
   Kein python-docx und keine Installation möglich? Dann mit dem eingebauten docx-Skill das gleiche Layout bauen.
3. **Wieder einlesen:** `python3 "$S/textlib.py" /mnt/user-data/outputs/Lebenslauf_….docx --info` – stimmt alles, keine Tabellen?
4. `python3 "$S/endcheck.py" /mnt/user-data/outputs/Lebenslauf_….pdf` – Seitenzahl, offene [PRÜFEN].
5. Wenn möglich, PDF-Seite als Bild ansehen (z. B. `pdftoppm -r 60 -png`), um das Layout zu prüfen.
6. Im Chat **nicht** den ganzen Lebenslauf wiederholen. Zeig: 3–5 Zeilen Zusammenfassung, offene [PRÜFEN]-Stellen als Liste, Dateien.

Dann: „Schau dir die Datei an. Passt alles? a) Ja b) Ändern: …“

## 5. Änderungswünsche

- Kleine Änderungen: JSON anpassen, neu erzeugen (neue Version `_v2`), alte Fassung bleibt.
- Nutzer will etwas Übertriebenes oder Erfundenes: freundlich ablehnen, ehrliche Alternative formulieren.
- Nutzer bearbeitet in Word selbst weiter: völlig okay. Hinweis: PDF in Word über „Speichern unter → PDF“ erzeugen, nicht drucken-als-Bild.
