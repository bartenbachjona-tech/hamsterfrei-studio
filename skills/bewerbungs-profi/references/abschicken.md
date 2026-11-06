# Phase 6: Endcheck und Abschicken

## Inhalt
1. Prüfen (Skripte + Pflicht-Checkliste)
2. Anlagen: eine PDF, Einzeldateien oder Bündel
3. Weg A: E-Mail
4. Weg B: Online-Formular / Portal
5. Weg C: WhatsApp, persönlich oder per Post
6. Nach dem Abschicken

---

## 1. Prüfen (Pflicht, auch im Schnellmodus)

```
python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json /mnt/user-data/outputs/<aktuelle Unterlagen>
python3 "$S/endcheck.py" …/Anschreiben_…_AKTUELL.pdf --typ anschreiben --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/Lebenslauf_…_AKTUELL.pdf --typ lebenslauf --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/Formular-Texte_…_AKTUELL.txt --typ formular --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/E-Mail_Bewerbung_…_AKTUELL.txt --typ email --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/WhatsApp-Text_…_AKTUELL.txt --typ whatsapp --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" /mnt/user-data/uploads/Zeugnis.jpg --typ anlage          (Zeugnisse: nur Format/Größe)
python3 "$S/endcheck.py" …/Bewerbung_Vorname_Nachname_Stelle.pdf --typ gesamt     (fertige Gesamt-PDF)
```
Ein Aufruf je Dokumenttyp. Akte und Spickzettel prüft der Sammel-Check nicht mit (Spickzettel: `fakten_check.py … --typ spickzettel`; `endcheck` hat keinen Spickzettel-Typ). Firmenname und Stellentitel verlangt `endcheck` nur im Anschreiben/Motivationsschreiben – Formular und Mail bleiben, wie sie freigegeben wurden. ❌ beheben über JSON + neu erzeugen (nach Freigabe der Änderung im Chat).

**Pflicht-Checkliste** – immer in **einem** Teil (≤ 6 Zeilen, auch am Handy und im Schnellmodus; **Minijob: 3 Zeilen** – Name/Firma stimmt, Daten = Zeugnisse, Lebenslauf dabei), als Codeblock:
```
✅ Kurz selbst prüfen, dann abschicken:
1. Firma, Ansprechperson, Stelle stimmen
2. Daten, Noten, Zeiträume = deine Zeugnisse
3. Alles dabei: …(aus der Anzeige)
4. Zu jedem Satz kannst du etwas erzählen – einmal laut vorlesen
```
Dazu **eine** Frage („Alles geprüft? a) Ja, abgeschickt b) Mir ist was aufgefallen: …“). Keine zweite Checklisten-Nachricht.

## 2. Anlagen: eine PDF, Einzeldateien oder Bündel

**Anlagen** (meist schon in der Profil-Phase hochgeladen): letztes bzw. relevantes Schulzeugnis (Ausbildung: meist die letzten zwei), Abschluss-, Arbeits-, Praktikumszeugnisse, relevante Zertifikate. AT: „Dienstzeugnisse“. CH: Zeugnisse/Diplome immer. In `profil.anlagen` (datei + bezeichnung). Scans/Fotos werden nicht verändert, nur auf A4 gebracht; Querformat-Fotos werden gedreht (wenn erkennbar) oder auf eine A4-Querseite eingepasst; PDF-Anlagen in anderen Formaten auf A4 skaliert. Liegt der Text auf der Seite: `--drehen Datei.jpg=90` (oder 270) – oder neu scannen. Seite als Bild ansehen.

**Eine PDF** (Anschreiben → Lebenslauf → Anlagen, Richtwert < 5 MB):
```
python3 "$S/pdf_zusammenfuegen.py" Bewerbung_Vorname_Nachname_Stelle.pdf --profil /tmp/bewerbung/profil.json
```
Nimmt automatisch die aktuellen Fassungen (`…_AKTUELL`, auch wenn ein alter Pfad genannt wird) und die Anlagen aus dem Profil. Der Zielname wird **genau so** verwendet; nur Umlaute/Leerzeichen werden ersetzt – mit Meldung. Passt die Anlagen-Zeile nicht zu den Anlagen (Zeugnis kam später), wird das Anschreiben automatisch neu erzeugt (nur diese Zeile ändert sich) – sag das in einem Satz. **Fehlt eine Datei: Abbruch (Exit 2)** → Upload erbitten.

**Formular will getrennte Dateien:**
```
python3 "$S/pdf_zusammenfuegen.py" --einzeln --profil /tmp/bewerbung/profil.json
```
→ saubere Namen **flach im Ausgabeordner**: `Anschreiben_Vorname_Nachname.pdf` (bzw. `Motivationsschreiben_…`), `Lebenslauf_…pdf`, `Zeugnis_der_10_Klasse_…pdf` (Bezeichnung vollständig statt `IMG_4471`). Die Arbeitsdateien `…_AKTUELL.pdf` wandern dabei nach `alt/` – am Handy liegt **je Unterlage genau eine** Datei. Das Skript listet „📤 Diese Dateien hochladen“ – genau diese Liste dem Nutzer geben. Ohne Profil: `--einzeln Datei … --name IMG_4471.jpg="Zeugnis 10. Klasse"`. Erzeugst du danach eine Unterlage neu, wandert die alte Upload-Datei automatisch nach `alt/` – dann `--einzeln` erneut.

**Upload-Limit „max. N Dateien“** (`ziel.upload_limit`) – Rezept:
```
python3 "$S/pdf_zusammenfuegen.py" --buendeln N --profil /tmp/bewerbung/profil.json
```
N ≥ 3: Anschreiben (bzw. Motivationsschreiben) | Lebenslauf | alle Anlagen in einer PDF · N = 2: Lebenslauf | Anschreiben + Anlagen · N = 1: alles in einer PDF. Größenlimit pro Datei beachten (Scans kleiner). Quellen sucht das Skript in `--ordner`, sonst `--ausgabe`, sonst im Standardordner. Vorher klären, was das Formular genau will – sonst baust du umsonst.

## 3. Weg A: E-Mail

Text erst **im Chat** zeigen (Computer: Codeblock zum Kopieren), Freigabe, dann `email.betreff`/`email.text` in die JSON und `unterlagen_erstellen.py … --nur email` → `E-Mail_Bewerbung_Firma_AKTUELL.txt`.
```
Betreff: Bewerbung als [Stelle genau wie in der Anzeige] (Kennziffer …)

Sehr geehrte Frau Sommer,
anbei sende ich Ihnen meine Bewerbung als [Stelle] ab [Start]. [Ein Satz aus seinen Antworten, wer er ist.]
Anschreiben, Lebenslauf und Zeugnisse finden Sie in einer PDF im Anhang.
Für Rückfragen erreichen Sie mich unter [Telefon aus dem Profil].

Mit freundlichen Grüßen
[Name]
```
3–5 Sätze; Anschreiben nicht doppelt hineinkopieren (außer es soll entfallen). Die Vorlagensätze (anbei …, … finden Sie in einer PDF im Anhang, Für Rückfragen …) sind neutral und brauchen **keine** `herkunft` – auch mit „Arbeitszeugnis“, „letzten zwei Zeugnisse“ oder dem Starttermin. Die Mail wird **vor** dem Erzeugen freigegeben (nicht erst mit der Gesamt-PDF zeigen). Jeder eigene Satz über die Person braucht seine `herkunft` (z. B. „über die Ausbildungsmesse“ nur, wenn er das so gesagt hat). **Bewerbungsadresse unbekannt:** nicht raten – Anzeige/Karriereseite/Impressum prüfen lassen oder anrufen. Anleitung (`geraet.md`): neue Mail → Betreff/Text einfügen → PDF anhängen → **Testmail an dich selbst** → senden.

## 4. Weg B: Online-Formular / Portal

- **Felder vorab erfragen:** „Welche Felder hat das Formular? Mach einen Screenshot der Felder (mit Zeichengrenzen).“ – dann nur diese Texte bauen.
- Texte vorher als Datei und im Chat (Timeout-Gefahr): `formular[]` mit `feld`, `limit`, `text` → `--nur formular`. Feldtitel stehen als `=== … (max. N Zeichen) ===` darüber.
- Typische Felder: Über mich, Motivation, Eintrittstermin, Gehalt (nur Spanne, nur wenn gefragt), „Wie sind Sie auf uns aufmerksam geworden?“ – **immer aus seiner Antwort** (`profil.wie_aufmerksam`, in der Profil-Phase gefragt).
- **Schnellmodus:** Portal-Felder (Gehalt, Eintritt, „Wie aufmerksam“) nur erfragen, wenn wirklich per Formular beworben wird.
- **Portale, die nach dem Upload alles noch einmal eintippen lassen** (Lebenslauf-Felder, Stationen, Daten): Felder sind oft vorausgefüllt und falsch zugeordnet. Sag das vorher. Gib die Stationen als kurze Liste im Chat (Zeitraum · Titel · Firma · 1 Zeile Tätigkeit) zum Abtippen/Kopieren; Daten exakt wie im Lebenslauf; Pflichtfelder nie mit „siehe Lebenslauf“.
- Dateien im verlangten Format (meist PDF; getrennt, eine oder Bündel – Abschnitt 2).
- Am Ende: Screenshot der Bestätigungsseite oder Bestätigungsmail aufheben.
- Du füllst das Formular nicht selbst aus (Ausnahme: Browser-Werkzeug verbunden und ausdrücklicher Wunsch – Passwörter gibt der Nutzer selbst ein, „Absenden“ nur nach seinem Ja).

## 5. Weg C: WhatsApp, persönlich oder per Post

- **WhatsApp** (Minijob, Gastro, Handwerk – nur wenn die Anzeige es anbietet): `whatsapp.text` (3–4 Sätze: wer, welche Stelle, ab wann/wie viele Stunden, Lebenslauf als PDF), mit Gruß und vollem Namen, kein Emoji-Feuerwerk. Herkunft wie beim Anschreiben. Nach der Freigabe `--nur whatsapp` → `WhatsApp-Text_Firma_AKTUELL.txt`, `endcheck --typ whatsapp`. Lebenslauf als **Dokument** schicken (Büroklammer → Dokument), nicht als Foto; liegt die PDF auf einem anderen Gerät: WhatsApp Web oder an sich selbst mailen (`geraet.md`). Im Chat den Text **direkt über** der Anleitung zeigen (nicht „siehe oben“).
- **Persönlich abgeben:** Lebenslauf (und ggf. Anschreiben) ausgedruckt in einer Klarsichthülle/Mappe, zu ruhiger Zeit hingehen (nicht zur Stoßzeit), nach der zuständigen Person fragen, 2–3 Sätze sagen (wer, welche Stelle, ab wann/wann verfügbar), Telefonnummer dalassen. Kurzen Satz vorher im Chat üben.
- **Post** nur, wenn verlangt.

## 6. Nach dem Abschicken

- JSON: `status`, `bewerbungen` (abgeschickt am, Weg, nachfassen am – ohne Gespräch etwa 2–3 Wochen später), dann `akte.py`.
- **Parallel weiterbewerben** – Ghosting ist häufig (karriere.at, AT 11/2025: 84 % schon ohne Rückmeldung).
- **Online-Test angekündigt?** Einmal anbieten, 5 Übungsaufgaben zu machen (`assessment_center.md` 4) – als eigene Nachricht, nicht mit der Abschicken-Bestätigung zusammen. **AC/Auswahltag angekündigt, aber noch keine Einladung:** einmal eine kurze AC-Übersicht anbieten (Zeit bis zum Termin nutzen), sonst „Einladung da → neuer Chat, Akte hochladen“.
- **Dateien am Handy:** Nach `--einzeln`/`--buendeln`/Gesamt-PDF (mit `--profil`) liegen die Word-Fassungen in `bearbeitbar/` – im Ordner bleibt je Unterlage **eine** Datei zum Hochladen. Die .docx nur auf Wunsch anbieten.
- Fahrplan (nur, wenn noch nicht gesagt): „Wenn die Einladung kommt: neuer Chat, Akte hochladen, ‚Gespräch üben‘ schreiben.“
