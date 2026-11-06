# Bedienung: Handy, Tablet oder Computer (ohne Gerätefrage)

## Grundsatz (v4)

**Keine Gerätefrage mehr** – sie hat in Tests Extra-Runden gekostet. Stattdessen:
- **Immer PDF** liefern (`unterlagen_erstellen.py …` erzeugt PDF + .docx; `--nur-pdf` nur, wenn der Nutzer sicher am Handy ist, z. B. Hochformat-Screenshot oder „bin am Handy“ → `meta.geraet`).
- Unter jede Datei **zwei Zeilen** für beide Geräte:
  ```
  📁 Lebenslauf_Lena_Muster_AKTUELL.pdf
  📱 Handy: antippen → Teilen/Herunterladen → speichern · 💻 PC: anklicken → Herunterladen
  ```
- Texte zum Kopieren in einen **Codeblock** (PC: Kopier-Knopf oben rechts; Handy: lange drücken → Kopieren). Nie „Strg+A“ (markiert den ganzen Chat).
- **Ausführlich** (Abschnitte unten) nur, wenn der Nutzer ein Problem meldet („finde die Datei nicht“, „kann nicht hochladen“, „zwei Dateien?“).
- Link blockiert: beide Wege in **einer** Nachricht: „Mach 1–3 Screenshots von der Anzeige (Handy) **oder** markiere den Anzeigentext und füge ihn hier ein / Drucken → Als PDF speichern (PC).“

## Dateien – was der Nutzer sieht

- Flache, eindeutige Dateinamen, keine Unterordner. Je Unterlage **eine** Datei: `…_AKTUELL.pdf`. Nach `pdf_zusammenfuegen.py --einzeln` gibt es nur noch die sauberen Upload-Namen (`Lebenslauf_Lena_Muster.pdf`) – die Arbeitsdateien wandern intern nach `alt/`.
- Immer genau sagen, **welche Datei** hochzuladen/anzuhängen ist („📤 Lebenslauf_Lena_Muster.pdf und Zeugnis_der_10_Klasse_Lena_Muster.pdf“).
- Mehrere Downloads, gleicher Name: Handys hängen „(1)“ an – die zuletzt geladene gilt, ältere löschen.

## Hilfe bei Problemen (nur auf Nachfrage)

**iPhone (Claude-App):** Speichern: Datei antippen → Teilen-Symbol (Quadrat mit Pfeil) → „In Dateien sichern“. Hochladen: „+“ bzw. Büroklammer → „Datei“ (oder „Fotos“).
**Android (Claude-App):** Speichern: Datei antippen → „Herunterladen“ (App „Dateien“ → „Downloads“). Hochladen: „+“ → „Dateien“ → „Downloads“.
**Computer:** Datei anklicken → „Herunterladen“ (Ordner „Downloads“). Hochladen: Büroklammer/„+“ oder Datei ins Chatfenster ziehen. Mac: „Cmd“ statt „Strg“.

- **Anzeige aus Job-Apps** (Indeed, StepStone …): „Teilen“ kopiert meist nur den Link → 1–3 Screenshots der ganzen Anzeige oder Anzeige im Browser öffnen. Zeitung/Aushang: Foto.
- **Zeugnisse:** Scan-Funktion (iPhone: Notizen-App → Kamera → „Dokumente scannen“; Android: Google Drive → „+“ → „Scannen“). Fotos gehen auch (JPG; HEIC wird umgewandelt). Quer fotografiert: das Skript dreht/passt ein.
- **Handy nur Ansicht, Word geht nicht:** PDF reicht für fast alle Portale.

## E-Mail am Handy (wenn er fragt)

1. Mail-App öffnen, neue Mail an die Adresse aus der Anzeige (unbekannt? nicht raten – in der Anzeige/auf der Karriereseite nachsehen oder anrufen).
2. Betreff und Text: im Chat lange drücken → Kopieren → einfügen.
3. Anhang: Büroklammer → „Datei“ → die genannte PDF aus „Dateien“/„Downloads“.
4. **Erst an dich selbst schicken** und prüfen, ob der Anhang aufgeht – dann an die Firma.

## WhatsApp und Gerätewechsel

Der Lebenslauf muss auf dem Gerät liegen, auf dem WhatsApp läuft. Hat er die PDF am Laptop: WhatsApp Web/Desktop nutzen oder die PDF an sich selbst mailen und am Handy speichern. Als **Dokument** schicken (Büroklammer → Dokument), nicht als Foto.
