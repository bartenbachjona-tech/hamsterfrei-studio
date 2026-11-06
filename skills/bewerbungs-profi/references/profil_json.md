# Die Profil-JSON (Quelle aller Fakten) – v3 mit Wortlaut

## Inhalt
1. Grundregel: Wortlaut zuerst
2. rohtext und Bestätigungen
3. Aufbau
4. Wie du Felder füllst (Normalisieren nur mit Wortlaut)
5. Von der JSON zu den Unterlagen
6. fakten_check: Treffer behandeln

---

## 1. Grundregel: Wortlaut zuerst

Jede Antwort des Nutzers kommt **sofort und wörtlich** in `profil.rohtext` – dann erst in die Felder. `fakten_check.py` prüft die Unterlagen gegen
- den **Wortlaut** (`profil.rohtext`),
- die **Anzeige** (`ziel.anzeige_text`), die **Einladung** (`gespraech.einladung_text`), zugestimmte **Firmenfakten**,
- **Uploads mit Text** (`profil.anlagen[].datei`, `profil.quellen[]` – Zeugnisse, alter Lebenslauf; über textlib gelesen),
- `belege[]` mit wörtlichem Zitat.

**Nicht** gegen deine eigenen Profil-Felder. Was du dort „normalisierst“ (09/2018, Klasse B, B.A., 30 Std.), zählt nur, wenn es so im Wortlaut steht. Muster: `python3 "$S/unterlagen_erstellen.py" --beispiel`. Neue Sitzung ohne JSON: Muster anlegen (`mkdir -p /tmp/bewerbung`), alle Beispielwerte **leeren**.

## 2. rohtext und Bestätigungen

```json
"rohtext": [
  {"nr": 1, "frage": "Frage 1 – Kontaktdaten", "antwort": "deniz arslan weinweg 14 93049 regensburg 0176 48213307 deniz.arslan07@gmail.com"},
  {"nr": 2, "frage": "Frage 2 – Schule", "antwort": "mittlere reife 2024 realschule am donaupark 2,8"},
  {"nr": 3, "frage": "Nachfrage zu Frage 2: Zeugnis im Juli 2024?", "antwort": "ja", "bestaetigt": "Juli 2024"}
]
```
- **Auswahlfragen** (a/b/c): die Optionen mitspeichern, dann zählt der Text der gewählten Option: `{"frage": "Warum Brenner? a) Übernahme b) nah dran", "antwort": "a und b", "optionen": {"a": "Übernahme bei guten Leistungen", "b": "nah dran"}}`.
- **Wörtlich** übernehmen, auch Tippfehler/Kleinschreibung. Auch Nebenbei-Infos aus anderen Nachrichten (dann `"frage": "nebenbei"`).
- `bestaetigt` zählt nur, wenn die Antwort ein klares Ja ist („ja“, „genau“, „stimmt“ …) **und** der Wert wörtlich in deiner Frage stand. Darum fragst du mit **einem** konkreten Wert („im Juli 2024?“), nicht „meist September“.
- Uploads (alter Lebenslauf, Zeugnis als PDF) in `profil.quellen` bzw. `profil.anlagen` – ihr Text zählt als Beleg. Bilder/Scans zählen nicht automatisch: was du darauf liest, bestätigt der Nutzer (eine Frage) → rohtext.
- Alte Akte (v2) ohne rohtext: fakten_check warnt „Kein Wortlaut“ und prüft hilfsweise gegen die Felder. Neue Antworten trotzdem in rohtext.

## 3. Aufbau

| Bereich | Inhalt | Wer schreibt |
|---|---|---|
| `meta` | stand, phase, naechster_schritt, geraet, anrede_form, modus (normal/schnell), chat_plan, **fragen_gesamt** (Y), **antworten_seit_akte** | du |
| `person` | name, strasse, plz_ort, telefon, email, linkedin (nur wenn genannt), geburtsdatum (nur auf Wunsch), foto (Pfad) | Wortlaut |
| `ziel` | art, stelle (genau wie in der Anzeige), firma, kennziffer, ansprechperson, anrede, firma_adresse, link, bewerbungsweg (inkl. WhatsApp/Portal), frist, start, unterlagen_verlangt, upload_limit, muss, kann, schluesselwoerter, auswahlverfahren, anschreiben_variante, **anzeige_text** | Anzeige |
| `profil.rohtext[]` | alle Antworten im Wortlaut | Nutzer |
| `profil.bildung[]`, `stationen[]`, `luecken[]` | wie v2 | aus dem Wortlaut |
| `profil.sprachen[]`, `edv[]`, `fuehrerschein`, **`zertifikate[]`** | Staplerschein, Ersthelfer, Sprachzertifikat → `zertifikate`, nicht unter Führerschein | Wortlaut |
| **`profil.wechselgrund`**, **`abbruch_grund`**, **`motivation_fach`**, `motivation_beruf`, `motivation_firma` | in seinen Worten, kurz | Wortlaut |
| `profil.beispiele[]` | thema, stichwort, situation, aufgabe, handlung, ergebnis (leer, wenn nicht gesagt) | Wortlaut |
| `profil.hobbys[]`, `rahmen{start, stunden, verfuegbarkeit, gehalt, foto}`, `wie_aufmerksam`, `sonstiges[]` | | Wortlaut |
| **`profil.berufstest`** | code, bereiche, vorschlaege[], gewaehlt | Skript + Nutzer |
| `profil.anlagen[]`, **`profil.quellen[]`** | datei (Upload-Pfad), bezeichnung („Zeugnis 10. Klasse“) | Uploads |
| `firmenfakten[]` | fakt, quelle, zugestimmt | Recherche + Nutzer |
| `belege[]` | `{text, woher, zitat}` – nur echte Herleitung, **zitat wörtlich** aus Wortlaut/Anzeige/Upload | du |
| `lebenslauf`, `anschreiben{typ, betreff, anrede, absaetze[], gruss, anlagen_zeile}`, `formular[{feld, limit, text}]`, `email{betreff, text}` | Unterlagen-Texte | du |
| `gespraech{termin, art, ort, gespraechspartner, einladung_text, bestaetigt, mitbringen[], kernbotschaften[], selbstpraesentation[], schwierige_fragen[{frage, antwort}], eigene_fragen[{frage, gewaehlt}], feedback[{frage, besser}], ac_uebungen[]}` | Gespräch/Spickzettel | du, aus Wortlaut + Einladung |
| `status[]`, `bewerbungen[]`, `entscheidungen[]`, `naechste_schritte[]` | Verlauf | du |

## 4. Wie du Felder füllst

- **Wörtlich genug:** „Kasse gemacht, abends abgerechnet“ → `taetigkeiten: ["an der Kasse gearbeitet", "abends die Abrechnung gemacht"]`. Nicht: „Kassenverantwortung“.
- **Daten so genau wie gesagt:** „seit 2023“ bleibt „seit 2023“. „seit märz 25“ → „seit 03/2025“ ist ok (steht so im Wortlaut). „ab Dezember“ → „ab Dezember 2026“, **nicht** „01.12.2026“.
- **Dauern** nur aus dem Wortlaut oder als Rechnung aus belegten Zeiträumen; „fast drei Jahre“ bei 2 J. 11 M. ist ok, „drei Jahre“ nicht. Zahlen aus der Anzeige belegen keine Dauer über den Nutzer.
- **Stunden/Teilzeit:** nur, was er sagt („zwei Kinder“ ≠ „Teilzeit 30 Std.“ – fragen).
- **Abschlüsse:** „Bachelor Soziale Arbeit“ bleibt so; „(B.A.)“ nur, wenn er „B.A.“ sagt oder es im Zeugnis steht.
- **Beispiele vollständig:** fehlt das Ergebnis, bleibt `ergebnis` leer.
- **Anzeigentext** ganz in `ziel.anzeige_text`; Einladung ganz in `gespraech.einladung_text`.
- **Firmenfakt aus Websuche:** `firmenfakten` mit Quelle, `zugestimmt: false`. Zustimmung als **eigene** Nachricht (Konfliktregel), erst bei Ja `true`.

## 5. Von der JSON zu den Unterlagen

- Lebenslauf = `bildung` + `stationen` (+ `luecken` > ~3 Monate) + Kenntnisse (`sprachen`, `edv`, `zertifikate`, `fuehrerschein` nur wenn gefüllt) + `hobbys`.
- Anschreiben: Einstieg aus `motivation_beruf` oder einem `beispiel`; 2–3 Anforderungen aus `ziel.muss`, belegt mit `beispiele`; Firma aus `motivation_firma` oder zugestimmtem Firmenfakt. Fehlt der Firmengrund: eine Frage, sonst Absatz weglassen.
- Anlagen-Zeile baut das Skript aus `profil.anlagen` (nur vorhandene Dateien).
- Formular: `formular[]` je Feld mit `limit`; „Wie aufmerksam geworden?“ nur aus `profil.wie_aufmerksam` (immer gefragt).

## 6. fakten_check: Treffer behandeln

`python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json [Dateien…] [--woher] [--typ spickzettel]` – Exit 1 bei ❌.

| Treffer | Was tun |
|---|---|
| ❌ Monat/Datum („nur das Jahr ist im Wortlaut“) | Nur das Jahr schreiben **oder** eine Nachfrage mit einem konkreten Wert |
| ❌ Dauer „gerundet“ | Genau schreiben („seit 10/2023“, „fast drei Jahre“) oder fragen |
| ❌ Zahl/Name/Begriff | Steht es in einer Antwort? Sonst streichen oder fragen |
| ❌ Abschluss/Kürzel, Sprachniveau, Führerschein/Klasse, Link | nur vom Nutzer – sonst raus oder fragen |
| ❌ Firmenfakt | Nutzer fragen (mit Quelle) oder streichen |
| ❌ Wie aufmerksam? | Nutzer fragen (nur die Quelle muss stimmen). Nie raten |
| ❌ Beleg ohne Zitat | `zitat` wörtlich ergänzen – oder der Beleg ist keiner |
| ❌ Abgleich | Datei ist alt oder von Hand geändert → neu erzeugen |
| ⚠️ Motivation/Eigenschaft ohne Wortlaut | Satz streichen und **als Frage** stellen („Wäre Reisen für dich okay?“) |
| ⚠️ Aufwertung? / Begriff | Hat er das so gesagt? Sonst schlichter |
| ⚠️ Beispiel/Hobby ungenutzt | einbauen oder bewusst weglassen |

**Nie** einen Treffer mit `belege` „wegbelegen“, den der Nutzer nicht gesagt hat. Der Check findet nicht alles: „Jeder Satz – woher weiß ich das?“ bleibt Pflicht.
