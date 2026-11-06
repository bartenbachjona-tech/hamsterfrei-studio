# Phase 6: Endcheck und Abschicken

## Inhalt
1. Prüfen (Skripte + Checkliste)
2. Anlagen und eine PDF (oder Einzeldateien)
3. Weg A: E-Mail
4. Weg B: Online-Formular / Portal
5. Weg C: persönlich oder per Post
6. Nach dem Abschicken

---

## 1. Prüfen (Pflicht, auch im Schnellmodus)

```
python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json /mnt/user-data/outputs/<alle aktuellen Dateien>
python3 "$S/endcheck.py" …/Anschreiben_…_vN.pdf --typ anschreiben --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/Lebenslauf_…_vN.pdf --typ lebenslauf --profil /tmp/bewerbung/profil.json
python3 "$S/endcheck.py" …/Formular-Texte_….txt --typ formular --profil /tmp/bewerbung/profil.json
```
Ein Aufruf je Dokumenttyp. Zeig nur Befunde in einfachen Worten (❌ zuerst), behebe ❌ über die JSON + neu erzeugen. Dann die Checkliste (am Handy in 2 Nachrichten zu je 3–4 Punkten):

```
✅ Bitte kurz selbst prüfen:
1. Firma, Ansprechperson, Stelle stimmen überall
2. Daten, Noten, Zeiträume stimmen mit deinen Zeugnissen
3. Alle verlangten Unterlagen liegen bereit: …(aus der Anzeige)
4. Du kannst zu jedem Satz etwas erzählen
5. Einmal laut vorlesen (Rechtschreibung!)
```
Rechtschreibfehler sind für 44 % der Recruiter entscheidend; häufig: falscher Firmenname durch Copy-and-paste, fehlende verlangte Unterlagen, mehrere Einzeldateien.

## 2. Anlagen und eine PDF

**Anlagen:** letztes bzw. relevantes Schulzeugnis (Ausbildung: meist die letzten zwei), Abschluss-, Arbeits-, Praktikumszeugnisse, relevante Zertifikate. AT: „Dienstzeugnisse“. CH: Zeugnisse/Diplome immer beilegen. Uploads in `profil.anlagen` (datei + bezeichnung) eintragen – daraus entsteht die Anlagen-Zeile im Anschreiben. Neue Anlage später? JSON ergänzen, Anschreiben neu erzeugen.

Scans/Fotos werden **nicht** verändert, nur auf A4 eingepasst. HEIC (iPhone) wird umgewandelt; klappt das nicht, gibt das Skript eine Handy-Anleitung aus (JPG/Screenshot/Scan).

**Eine PDF** (Anschreiben → Lebenslauf → Anlagen, Richtwert < 5 MB):
```
python3 "$S/pdf_zusammenfuegen.py" Bewerbung_Vorname_Nachname_Stelle.pdf --profil /tmp/bewerbung/profil.json
```
Nimmt automatisch die **aktuellsten** Fassungen und die Anlagen aus dem Profil. Mit Einzeldateien geht's auch (`… Ziel.pdf A.pdf B.pdf Zeugnis.jpg`) – ist eine Fassung veraltet, nimmt das Skript die neueste und sagt es. **Fehlt eine Datei, bricht es ab (Exit 2)** – dann fehlende Datei hochladen lassen. Passt die Anlagen-Zeile nicht zu den angehängten Dateien: Abbruch (Exit 3) → Anschreiben neu erzeugen.

**Formular will getrennte Dateien** (oder Upload-Limit, `sonderfaelle.md` Abschnitt 7):
```
python3 "$S/pdf_zusammenfuegen.py" --einzeln …/Lebenslauf_…_v2.pdf …/Anschreiben_…_v3.pdf
```
→ saubere Namen ohne `_vN` in `outputs/versand/`. Vorher fragen, was das Formular will, sonst baust du umsonst.

## 3. Weg A: E-Mail

`email.betreff`/`email.text` in der JSON, dann `unterlagen_erstellen.py … --nur email` → `E-Mail_Bewerbung_Firma_vN.txt`; Text **auch im Chat** zeigen (zum Kopieren).
```
Betreff: Bewerbung als [Stelle genau wie in der Anzeige] (Kennziffer …)

Sehr geehrte Frau Sommer,
anbei sende ich Ihnen meine Bewerbung als [Stelle] ab [Start]. [Ein Satz aus dem Profil, wer du bist.]
Anschreiben, Lebenslauf und Zeugnisse finden Sie in einer PDF im Anhang.
Für Rückfragen erreichen Sie mich unter [Telefon aus dem Profil].

Mit freundlichen Grüßen
[Name]
```
3–5 Sätze; Anschreiben nicht doppelt hineinkopieren (außer es soll entfallen). Anleitung Schritt für Schritt (Handy: `geraet.md`): neue Mail → Betreff/Text einfügen → PDF anhängen → **Testmail an dich selbst** → senden → gesendete Mail aufheben.

## 4. Weg B: Online-Formular / Portal

- Texte vorher als Datei (Timeout-Gefahr): `formular[]` mit `feld`, `limit`, `text` → `--nur formular`. Feldtitel stehen als `=== … ===` darüber; `endcheck.py --typ formular` prüft Limits, leere Felder, „siehe Lebenslauf“, Platzhalter.
- Typische Felder: Über mich, Motivation, Eintrittstermin, Gehalt (nur Spanne, nur wenn gefragt), „Wie sind Sie auf uns aufmerksam geworden?“ – **nur mit der Antwort des Nutzers** (`profil.wie_aufmerksam`), nie raten.
- Dateien im verlangten Format (meist PDF; getrennt oder eine – wie das Formular es will, Upload-Limits beachten).
- Am Ende: Screenshot der Bestätigungsseite oder Bestätigungsmail aufheben.
- Du füllst das Formular nicht selbst aus (Ausnahme: Browser-Werkzeug verbunden und ausdrücklicher Wunsch – Passwörter gibt der Nutzer selbst ein, „Absenden“ nur nach seinem Ja).

## 5. Weg C: persönlich oder per Post

Selten (Minijob, kleine Betriebe). Persönlich: Lebenslauf ausgedruckt mitnehmen, kurz vorstellen, nach der zuständigen Person fragen, Verfügbarkeit sagen. Post nur, wenn verlangt.

## 6. Nach dem Abschicken

- JSON: `status`, `bewerbungen` (abgeschickt am, Weg, nachfassen am – ohne Gespräch etwa 2–3 Wochen später), dann `akte.py`.
- **Parallel weiterbewerben** – Ghosting ist häufig (karriere.at, AT 11/2025: 84 % schon ohne Rückmeldung).
- Fahrplan: „Zeit für einen neuen Chat? Lade dort die Akte hoch und schreib ‚Gespräch üben‘.“
