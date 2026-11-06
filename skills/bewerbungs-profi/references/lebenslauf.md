# Phase 4: Lebenslauf (tabellarisch, einspaltig, maschinenlesbar)

## Inhalt
1. Regeln für den Inhalt
2. Regeln für das Layout (ATS)
3. Aus der Profil-JSON bauen
4. Erzeugen, prüfen, zeigen
5. Änderungswünsche und Versionen

---

## 1. Regeln für den Inhalt

**Aufbau:** 1. Kopf (Name, Adresse, Telefon, seriöse E-Mail, LinkedIn nur wenn genannt) · 2. optional Kurzprofil (2–3 Zeilen, nur Fakten aus dem Profil) · 3. Berufserfahrung/Praktische Erfahrung **antichronologisch** · 4. Ausbildung/Studium/Schulbildung · 5. Praktika, Nebenjobs, Ehrenamt · 6. Kenntnisse (Sprachen mit Niveau, EDV konkret, Führerschein **nur wenn im Profil**) · 7. optional Interessen (was etwas aussagt). Einsteiger ohne Erfahrung: Schulbildung zuerst.

**Länge:** Schüler/Einsteiger 1 Seite, mit Berufserfahrung höchstens 2.

**Stichpunkte:** 2–4 pro Station, aktive Verben, Ergebnis statt Aufgabe – **aber nur, was der Nutzer gesagt hat**. Aus `taetigkeiten`/`ergebnisse` sprachlich glätten ja, neue Inhalte, Zahlen, Rollen nein.

**Schlüsselwörter** aus der Anzeige im gleichen Wortlaut – nur, wo sie zutreffen.

**Zeiträume** exakt wie im Profil. Nur Jahr bekannt → „2023 – 2024“ oder „seit 2023“, kein ausgedachter Monat. Lücken > ~3 Monate: `profil.luecken` als eigene Zeile, kurz und ehrlich (`sonderfaelle.md`).

**Foto** freiwillig (AGG), Pfad in `person.foto` (rechts oben, 3,5 cm). **Geburtsdatum** nur auf Wunsch. **Datum/Unterschrift** online nicht nötig (`ort_datum_unterschrift`).

**E-Mail:** Ist sie unseriös (Spitzname, lange Zahlenfolge, Jugendsprache), freundlich eine neue vorname.nachname@… empfehlen. Eine normale Adresse nicht beanstanden.

## 2. Regeln für das Layout (ATS)

Laut Indeed-Umfrage (10/2026, 300 HR-Verantwortliche) nutzen 42 % KI oder Software zur Vorauswahl. Darum einspaltig, keine Tabellen/Textspalten/Icons/Skill-Balken, Standard-Überschriften, „EUR“ statt „€“, PDF aus Word statt Canva-Grafik. `unterlagen_erstellen.py` hält das ein (Tabstopp statt Tabelle, Arial 11, A4, graue Linien).

Eigener (z. B. zweispaltiger Canva-)Lebenslauf: `textlib.py Datei --info`. Bei **.docx** erkennt es Tabellen, Textfelder und Spalten sicher; bei **.pdf** nur grob (Textblöcke nebeneinander) – im Zweifel die Seite als Bild ansehen. Risiko ehrlich erklären, einspaltige Fassung anbieten; er entscheidet.

## 3. Aus der Profil-JSON bauen

Format: `python3 "$S/unterlagen_erstellen.py" --beispiel` (Abschnitt `lebenslauf`):
```json
"lebenslauf": {"kurzprofil": "", "abschnitte": [
  {"titel": "Praktische Erfahrung", "eintraege": [
    {"zeitraum": "09/2025 – heute", "titel": "Aushilfe Kasse (Minijob)", "ort": "Supermarkt Beispiel, Ingolstadt", "punkte": ["…"]}]}],
 "kenntnisse": [{"label": "Sprachen", "wert": "Deutsch (Muttersprache), Englisch (B1)"}],
 "interessen": "", "ort_datum_unterschrift": false}
```
Zuordnung: `profil.stationen` → Erfahrung/Ehrenamt, `profil.bildung` → Schulbildung, `sprachen`+`edv`(+`fuehrerschein`) → Kenntnisse, `hobbys` → Interessen (`profil_json.md`, Abschnitt 4). Zeiträume `MM/JJJJ – MM/JJJJ` oder `seit MM/JJJJ` – aber nur, wenn der Monat bekannt ist. [PRÜFEN] im Zeitraum ist ok: das Skript setzt „??“ in die Datumsspalte und die Notiz darunter (Layout bleibt gerade).

## 4. Erzeugen, prüfen, zeigen

1. `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json` → 0 ❌.
2. `python3 "$S/unterlagen_erstellen.py" /tmp/bewerbung/profil.json --nur lebenslauf` (Handy: `--nur-pdf`) → `Lebenslauf_Vorname_Nachname_vN.pdf` (+ .docx).
3. `python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json /mnt/user-data/outputs/Lebenslauf_…_vN.pdf` (Abgleich) und `python3 "$S/endcheck.py" … --typ lebenslauf --profil /tmp/bewerbung/profil.json`.
4. Wenn möglich: `pdftoppm -r 60 -png …pdf /tmp/ll` und das Bild ansehen.
5. Im Chat: 3–5 Zeilen Zusammenfassung, offene [PRÜFEN] als Liste, „📁 Aktuell: Lebenslauf_…_vN.pdf“. Dann „Passt alles? a) Ja b) Ändern: …“.

Kein python-docx/keine Installation: eingebauter docx-Skill, gleiches Layout, Texte 1:1 aus der JSON.

## 5. Änderungswünsche und Versionen

- Änderung → **JSON** ändern → neu erzeugen (→ `_v2`). Ältere Fassung liegt danach in `alt/`; im Chat sagen: „Aktuell ist v2 – lösch die alte.“ Nie die Datei selbst umschreiben.
- Wunsch nach Übertriebenem/Erfundenem: freundlich ablehnen, ehrliche Alternative.
- Nutzer bearbeitet in Word selbst weiter: okay; dann hochladen lassen, `fakten_check.py` mit der Datei laufen lassen (zeigt Abweichungen), JSON nachziehen.
