# Runde 3 (Skill v3): 83 % zufrieden, 96 % Wiederkauf (n=48) – Befunde für v4

Unzufrieden (Note 3): 135 (35 Nachrichten, Postkorb-Abbruch, doppelt sagen), 227/233 (Spickzettel-Fehler, 2 Anschreiben am Handy, Fallstudien-Tipp bei Präsentation), 319 (Probearbeiten: 👍-Bestätigung ignoriert, 5 Fragen zu viel), 500 (erfunden „täglich … lerne schnell“), 530 (Minijob: zu viele Fragen, Checkliste in 2 Teilen, „schwer tragen bin ich gewohnt“ erfunden), 920 (> 40 Nachrichten, erfundener Satz), 941 (erfunden „am Stand kennengelernt“).

## 1. Weiche Erfindungen (19×) – Ansatz ändern
- fakten_check lässt Sätze durch, wenn genug Wörter irgendwo im Wortlaut stehen; Marker-Liste fängt „passt zu mir“, „ist mir wichtig“, „finde ich spannend“, „lerne schnell“, „verbindet genau …“, „Privat habe ich …“, „Wir haben uns … kennengelernt“ nicht.
- `--woher` meist leer oder falsch zugeordnet (Block-Antworten, Satzanfänge, Kontaktdaten). Unbrauchbar.
- Personen-Fakten aus der ANZEIGE (Klasse B, mind. 18) gelten als Beleg für den Nutzer. Inhalte aus Zeugnis-Fotos ungeprüft übernommen. Gesundheitsangabe („wegen meines Knies“) unkommentiert ins Anschreiben.
- Claude erfindet Gegenmaßnahmen bei Schwächen (Spickzettel), Kennenlern-Situationen, Häufigkeiten.
→ v4: **Satz-Herkunft durch Claude statt Skript**: Jeder Satz im Anschreiben/Motivationstext/Mail/Formularfreitext bekommt beim Entwurf intern eine Quelle (Antwort-Nr. + Zitat ODER Anzeige-Zitat für Firmenbezug). Freigabe-Nachricht zeigt die Woher-Liste kompakt für alle Sätze mit Aussagen über die Person (Motivation, Eigenschaften, Erlebnisse, Häufigkeiten). Satz ohne Quelle = nicht schreiben, sondern als Frage. Skript `woher` nur als Format-Hilfe (nimmt Claudes Zuordnung als JSON an und prüft, ob jedes Zitat wörtlich im Rohtext steht). Personen-Fakten nie aus Anzeige belegen. Zeugnis-Inhalte nur mit Nachfrage. Gesundheit/Privates nur nach ausdrücklicher Zustimmung, im Anschreiben i. d. R. nicht.

## 2. Fehlalarme fakten_check (alle Pakete) → Normalisierungs-Wörterbuch
abi/fachabi/quali/msa/m10/mittlere reife, fsj/bfd/zfa/mfa/kfz/bio/…, str./straße, Monatsnamen inkl. Tippfehler (febuar), „april 25“→04/2025, „märz bis august 24“, „januar 26“, „ab Januar“→nächstes Vorkommen (Skill erlaubt es, Skript meldet ❌ – Widerspruch), „15h/20h“→Std., „31. August 2027“↔„31.08.2027“, „29-31k“, papa→Vater, Großschreibung (ALLGEMEINE HOCHSCHULREIFE), B.A.↔Bachelor of Arts; Kinderalter („4 und 7“) keine Dauer; Kenntnis-Labels (Zertifikate, Sprachen, Scheine, Sonstiges, Weitere Kenntnisse) keine Namen; „Ihr Haus“; Satzpunkt am Feldende; umbrochene Anlagen-Zeile; Briefdatum an späterem Tag; eigene Nummerierung im Spickzettel; Übungsfragen; Dauer-Prüfung mit falschem Zeitraum (Minijob statt Studium). `belege` muss die Aussage tragen (Zitat ↔ Wert), nicht nur irgendwo vorkommen. Zähler „offene [PRÜFEN]“ immer 0.

## 3. Spickzettel (`akte.py --spickzettel`) – häufigster Dateifehler
Vorstellungsdauer fest „1–2 Minuten“ (Einladung sagt 3/5) → aus Einladung übernehmen; verbesserte Antworten/Feedback/AC-Übungen/Wechselgrund als „schwierige Frage“ (doppelt); interne Notizen in 3. Person/Coaching-Vermerke; Fallstudien-Tipp bei Selbstpräsentation; Gruppenaufgabe ohne Tipp; „Tipps für dein Auswahltag“; immer Du (auch bei Sie); Seite 2 fast leer; kein Abschnitt Fachfragen; Gehaltsfrage mit [PRÜFEN] still weggelassen; A4 am Handy zu klein (Handy-Format A5/kompakt oder Text im Chat). → Klare Datenstruktur: `vorstellung{dauer_min, kernpunkte}`, `schwierige_fragen[{frage, antwort_final}]`, `eigene_fragen`, `mitbringen`, `fachfragen`, `ac_uebungen[{typ, tipp}]`, `anrede: du|sie`.

## 4. Dateien
`--buendeln` benennt Motivationsschreiben „Anschreiben_…“; `--einzeln` legt zweite Kopien neben _AKTUELL (am Handy 2 gleiche Dateien); Dateinamen mitten im Wort gekürzt; Zeichengrenze doppelt bei Tausenderpunkt („1.500“); `pdf_zusammenfuegen` sucht Quellen im falschen Ordner bei abweichendem --ausgabe/--ordner; Kennziffer im Betreff am Bindestrich umbrochen; endcheck „im Stellentitel fehlt ‚start‘“; Akte-Reupload-Liste doppelt; `akte.py --lesen` erkennt umbenannte Handy-Re-Uploads nicht; `luecken[].erklaerung` undokumentiert (mit `grund` bleibt Lücke leer); kein WhatsApp-Typ (läuft als „Formular-Texte“).

## 5. Länge / Fragen (zu_lang 17×, zu_viele_fragen 12×)
- **Gerätefrage kostet Extra-Runden** → abschaffen: immer PDF liefern (+ .docx dazu), Bedienhinweise kurz für beide; nur fragen, wenn Nutzer Probleme meldet.
- Minijob/Probearbeiten-Pfad zu lang (> 20 Runden) → Kurzpfad: max. 5 Fragen, Unterlagen in ≤ 10 Nachrichten; Probearbeiten-Vorbereitung = 1 Übersicht + 2 Fragen.
- Bereits gegebene Antworten (👍-Bestätigung, Kurzweg-Antworten, „ja glaub schon“) erkennen, nicht nochmal fragen; unklare Antworten („glaub schon“, „b2 glaub ich“) kurz bestätigen lassen.
- Pflicht-Checkliste in EINEM Teil (max. 6 Zeilen).
- Postkorb: max. 6 Dokumente in 2 Häppchen; AC-Übung abbrechbar mit Kurzfeedback.
- Gesamtbudget inkl. Gespräch/AC: ≤ 35 Nachrichten; Chatwechsel-Hinweis nur einmal, nicht kurz vor Ziel.
- Hinweis-Block: bei ≤ 3-Zeilen-Nachfragen nur 👉-Zeile erlaubt (Regel anpassen statt dauernd verletzen); „≤ 8 Zeilen am Handy“ ersetzen durch „so kurz wie möglich, große Blöcke als Datei/Code-Block“.
- Nie zwei Anliegen: Freigabe + Angebot, Profil-Freigabe + Chatwechsel trennen.

## 6. Fachliches
`sonderfaelle.md`: studentische KV für Werkstudenten nur bis 30 bzw. 14. Fachsemester (richtigstellen, mit Quelle). Karriereseite = Anzeige? (ja, wenn Stellenbeschreibung). Hörensagen über Firma nicht als Fakt. Unbekannte Bewerbungs-Mailadresse, telefonische Einladung (keine Bestätigungs-Mail-Pflicht), persönlich abgeben, WhatsApp-Gerätewechsel, private Projekte im Lebenslauf, sensible Details (Todesfall) nicht wörtlich in Akte; Online-Formular: Felder vorab erfragen; KI-Hinweis in Anzeige vs. Regel 8 (Nutzer entscheidet ehrlich, ob KI-Hilfe angegeben wird).
