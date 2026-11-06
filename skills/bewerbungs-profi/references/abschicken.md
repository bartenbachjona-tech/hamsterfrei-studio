# Phase 6: Endcheck und Abschicken

## Inhalt
1. Endcheck (Skript + Checkliste)
2. Anlagen und eine PDF
3. Weg A: per E-Mail
4. Weg B: Online-Formular / Portal
5. Weg C: persönlich oder per Post
6. Nach dem Abschicken

---

## 1. Endcheck (Skript + Checkliste)

Führe aus:
```
python3 "$S/endcheck.py" /mnt/user-data/outputs/Anschreiben_….pdf /mnt/user-data/outputs/Lebenslauf_….pdf --firma "Firma" --stelle "Stelle"
```
Zeig nur die Befunde (❌ zuerst) in einfachen Worten und behebe ❌ gemeinsam mit dem Nutzer. Dann die Checkliste – als **eine** Nachricht zum Abhaken, der Nutzer antwortet z. B. „alles ok“ oder „4 fehlt“:

```
✅ Endcheck – bitte kurz selbst prüfen:
1. Firmenname, Ansprechperson und Stelle stimmen überall (Betreff, Anrede, Text)
2. Alle [PRÜFEN]-Stellen sind geklärt (gelb markiert = noch offen)
3. Daten, Noten, Zeiträume stimmen mit deinen Zeugnissen überein
4. Alle verlangten Unterlagen liegen bereit: …(aus der Anzeige)
5. E-Mail-Adresse ist seriös, Telefonnummer stimmt
6. Du kannst zu jedem Satz etwas erzählen
7. Einmal laut vorlesen oder von jemandem lesen lassen (Rechtschreibung!)
```
Rechtschreibfehler sind für 44 % der Recruiter entscheidend; häufige Fehler sind falscher Firmenname durch Copy-and-paste, generische Texte, zu lange Unterlagen, mehrere Einzeldateien, fehlende verlangte Unterlagen.

## 2. Anlagen und eine PDF

**Anlagen:** das letzte bzw. relevante Schulzeugnis (bei Ausbildung meist die letzten zwei), Abschlusszeugnisse, Arbeits- und Praktikumszeugnisse, relevante Zertifikate. Keine Seminarbescheinigungen von vor 10 Jahren. AT: „Dienstzeugnisse“. CH: Zeugnisse und Diplome immer beilegen.

Zeugnisse hat der Nutzer meist auf Papier → er scannt sie (Handy-Scan-App oder Kopierer, als PDF oder JPG) und lädt sie hoch. Sie werden **nicht** verändert.

**Eine PDF-Datei** in der Reihenfolge Anschreiben → Lebenslauf → Anlagen, unter ~5 MB (Richtwert, Vorgabe der Anzeige geht vor):
```
python3 "$S/pdf_zusammenfuegen.py" Bewerbung_Vorname_Nachname_Stelle.pdf \
  /mnt/user-data/outputs/Anschreiben_….pdf /mnt/user-data/outputs/Lebenslauf_….pdf /mnt/user-data/uploads/Zeugnis.pdf
```
Dateiname ohne Umlaute und Leerzeichen (das Skript ersetzt sie). Ohne Anlagen-Uploads: Gesamt-PDF aus Anschreiben + Lebenslauf bauen und erklären, wie der Nutzer Zeugnisse später anhängt – oder ob das Formular sie einzeln will.

Verlangt das Formular **getrennte Dateien**, dann getrennt hochladen – die Anzeige gilt.

## 3. Weg A: per E-Mail

E-Mail-Text als Datei `E-Mail_Bewerbung_Firma.txt` ausgeben **und** im Chat zeigen (zum Kopieren):

```
Betreff: Bewerbung als [Stelle genau wie in der Anzeige] (Kennziffer …)

Sehr geehrte Frau Sommer,

anbei sende ich Ihnen meine Bewerbung als [Stelle] ab [Start]. [Ein Satz, wer du bist,
z. B. „Ich mache gerade meine Mittlere Reife und arbeite nebenbei an der Kasse.“]
Anschreiben, Lebenslauf und Zeugnisse finden Sie in einer PDF-Datei im Anhang.
Für Rückfragen erreichen Sie mich unter 0151 ….

Mit freundlichen Grüßen
Lena Muster
```
Regeln: 3–5 Sätze; den Anschreiben-Text **nicht** doppelt in die Mail kopieren (Ausnahme: das Anschreiben soll ganz entfallen, dann kommt das Kurzanschreiben in die Mail).

Schritt für Schritt für Anfänger (eine Nachricht, nummeriert):
1. E-Mail-Programm öffnen, neue Mail an die Adresse aus der Anzeige.
2. Betreff und Text aus der Datei einfügen.
3. PDF anhängen (Büroklammer-Symbol).
4. **Erst eine Testmail an dich selbst schicken** – kommt der Anhang an, öffnet er sich?
5. Dann an die Firma senden. Gesendete Mail aufheben.

## 4. Weg B: Online-Formular / Portal

- Texte **vorher** in einer Datei schreiben (Timeout-Gefahr) – du lieferst sie als `Formular-Texte_Firma.txt`, Feld für Feld beschriftet.
- Pflichtfelder vollständig ausfüllen, Felder **nicht** mit „siehe Lebenslauf“ füllen. Zeichenlimits beachten (frag nach, wenn ein Feld ein Limit zeigt, und kürze passend).
- Dateien im verlangten Format hochladen (meist PDF; getrennt oder eine Datei – wie das Formular es will).
- Am Ende: **Screenshot der Bestätigungsseite** machen oder Bestätigungsmail aufheben.
- Typische Felder, die du vorbereitest: Kurzprofil/„Über mich“, Motivation, Eintrittstermin, Gehaltsvorstellung (nur Spanne, nur wenn gefragt), „Wie sind Sie auf uns aufmerksam geworden?“.
- Du kannst das Formular nicht selbst ausfüllen oder absenden (außer ein Browser-Werkzeug ist verbunden und der Nutzer will das ausdrücklich – dann gibt er Passwörter selbst ein, und du klickst nie selbst auf „Absenden“, ohne dass er es bestätigt).

## 5. Weg C: persönlich oder per Post

Selten, eher bei Minijob oder kleinen Betrieben. Persönlich: Lebenslauf ausgedruckt mitnehmen, kurz vorstellen („Ich habe gesehen, dass Sie eine Aushilfe suchen …“), nach der zuständigen Person fragen, Verfügbarkeit sagen. Per Post nur, wenn ausdrücklich verlangt.

## 6. Nach dem Abschicken

- Akte aktualisieren: „Abgeschickt am …“, Weg, Nachfass-Datum (ohne Gespräch nach etwa 2–3 Wochen nachfragen, falls keine Frist genannt).
- **Parallel weiterbewerben** – Ghosting ist häufig (laut karriere.at, AT 11/2025: 84 % haben schon keine Rückmeldung bekommen). Tracking-Tabelle in der Akte (Abschnitt 5) führen.
- Fragen: „Möchtest du dich schon mal aufs Vorstellungsgespräch vorbereiten? Je früher, desto entspannter.“ → Phase 7.
