# Die Profil-JSON (Quelle aller Fakten)

## Inhalt
1. Grundregel
2. Aufbau
3. Wie du Antworten einträgst
4. Von der JSON zu den Unterlagen
5. fakten_check: Treffer behandeln

---

## 1. Grundregel

Alles, was der Nutzer sagt (oder was in seinen Uploads/der Anzeige steht), kommt **sofort** in `/tmp/bewerbung/profil.json` – ein Feld je Fakt, möglichst in seinen Worten. Die Unterlagen-Abschnitte (`lebenslauf`, `anschreiben`, `formular`, `email`) schreibst du **nur aus diesen Feldern**. Was nicht in der JSON oder der Anzeige steht, gibt es nicht. Das vollständige Muster zeigt `python3 "$S/unterlagen_erstellen.py" --beispiel`.

Neue Sitzung ohne JSON: mit dem Muster anlegen (`mkdir -p /tmp/bewerbung`), Platzhalterwerte des Musters **leeren**, nicht übernehmen.

## 2. Aufbau

| Bereich | Inhalt | Wer schreibt |
|---|---|---|
| `meta` | stand, phase, naechster_schritt, geraet (handy/tablet/pc), anrede_form, modus (normal/schnell), chat_plan | du |
| `person` | name, strasse, plz_ort, telefon, email, linkedin (nur wenn genannt), geburtsdatum (nur auf Wunsch), foto (Pfad) | Nutzer |
| `ziel` | art, stelle (genau wie in der Anzeige), firma, kennziffer, ansprechperson, anrede, firma_adresse, link, bewerbungsweg, frist, start, unterlagen_verlangt, upload_limit, muss, kann, schluesselwoerter, auswahlverfahren, anschreiben_variante, **anzeige_text** (ganzer Text) | Anzeige |
| `profil.bildung[]` | zeitraum, abschluss, schule, note, details | Nutzer |
| `profil.stationen[]` | zeitraum, art, titel, firma, ort, taetigkeiten[], ergebnisse[] | Nutzer |
| `profil.luecken[]` | zeitraum, erklaerung (in Nutzerworten) | Nutzer |
| `profil.sprachen[]`, `edv[]`, `fuehrerschein` | nur was gesagt wurde; Führerschein leer lassen, wenn nie erwähnt | Nutzer |
| `profil.motivation_beruf`, `motivation_firma` | Originalton, kurz | Nutzer |
| `profil.beispiele[]` | thema, stichwort, situation, aufgabe, handlung, ergebnis – auch STAR-Geschichten aus Phase 7 | Nutzer |
| `profil.hobbys[]`, `rahmen{start, stunden, verfuegbarkeit, gehalt, foto}`, `wie_aufmerksam`, `sonstiges[]` | | Nutzer |
| `profil.anlagen[]` | datei (Pfad des Uploads), bezeichnung („Zeugnis 10. Klasse“) | Nutzer/Uploads |
| `firmenfakten[]` | fakt, quelle (URL/Seite), zugestimmt (true/false) | Recherche + Nutzer |
| `belege[]` | text, woher – für Abgeleitetes, z. B. `{"text": "seit über einem Jahr", "woher": "Minijob seit 09/2025, heute 11/2026"}` | du, nur mit echter Herleitung |
| `lebenslauf`, `anschreiben{typ, betreff, anrede, absaetze[], gruss}`, `formular[{feld, limit, text}]`, `email{betreff, text}` | die Unterlagen-Texte | du, aus den Feldern oben |
| `status[]`, `gespraech{termin, art, ort, star[], eigene_fragen[], selbstpraesentation[], feedback[]}`, `bewerbungen[]`, `entscheidungen[]`, `naechste_schritte[]` | Verlauf | du |

## 3. Wie du Antworten einträgst

- **Wörtlich genug:** „Kasse gemacht, abends abgerechnet“ → `taetigkeiten: ["an der Kasse gearbeitet", "abends die Abrechnung gemacht"]`. Nicht: „Kassenverantwortung“.
- **Daten so genau wie gesagt:** „seit 2023“ bleibt `"seit 2023"` – kein Monat dazuerfinden. Braucht der Lebenslauf Monate, fragst du (eine Nachfrage) oder schreibst „seit 2023“.
- **Dauern nicht runden:** „7,5 Jahre“ bleibt 7,5; im Text „seit 2018“ oder „über sieben Jahre“ nur mit Beleg.
- **Beispiele vollständig:** fehlt das Ergebnis, bleibt `ergebnis` leer – nicht ausschmücken. Bei Bedarf eine Nachfrage.
- **Hobbys/Beispiele, die du nicht nutzen willst:** trotzdem eintragen; fakten_check meldet ungenutzte – dann bewusst entscheiden (und kurz im Chat sagen, warum).
- **Anzeigentext** ganz in `ziel.anzeige_text` – so belegt er Schlüsselwörter und Firmenangaben.
- **Firmenfakt aus Websuche:** `firmenfakten` mit Quelle, `zugestimmt: false`. Im Chat: „Laut Karriereseite (Link) … – soll das ins Anschreiben? a) Ja b) Nein“. Erst bei Ja `true`.

## 4. Von der JSON zu den Unterlagen

- Lebenslauf-Einträge = `bildung` + `stationen` (+ `luecken`, wenn > ~3 Monate) – Zeiträume 1:1, Stichpunkte aus `taetigkeiten`/`ergebnisse` (sprachlich glätten ja, Inhalt dazudichten nein).
- Kenntnisse = `sprachen` + `edv` (+ `fuehrerschein` nur, wenn gefüllt).
- Interessen = `hobbys` (Auswahl: was etwas aussagt oder zur Stelle passt).
- Anschreiben: Einstieg aus `motivation_beruf` oder einem `beispiel`; 2–3 Anforderungen aus `ziel.muss`/`schluesselwoerter`, belegt mit `beispiele`; Firma aus `motivation_firma` oder zugestimmtem `firmenfakt`. Fehlt der Firmengrund: eine Frage stellen, sonst Absatz weglassen – nicht [PRÜFEN] mit eigenem Vorschlag.
- Anlagen-Zeile baut das Skript selbst aus `profil.anlagen` (nur vorhandene Dateien).
- Formular: `formular[]` je Feld mit `limit`; „Wie aufmerksam geworden?“ nur aus `profil.wie_aufmerksam`.

## 5. fakten_check: Treffer behandeln

`python3 "$S/fakten_check.py" /tmp/bewerbung/profil.json [Dateien…]` – Exit 1 bei ❌.

| Treffer | Was tun |
|---|---|
| ❌ Zahl/Datum/Monat/Dauer | Steht es so in einer Antwort? → Feld ergänzen. Abgeleitet? → `belege`. Sonst streichen oder eine Nachfrage. |
| ❌ Name/Firma/Begriff | Tippfehler/andere Schreibweise im Profil angleichen; sonst streichen. |
| ❌ Abschluss, Sprachniveau, Führerschein, Link | nur vom Nutzer – sonst raus. |
| ❌ Firmenfakt | Nutzer fragen (mit Quelle) oder streichen. |
| ❌ Wie aufmerksam? | Nutzer fragen. Nie raten. |
| ❌ Abgleich | Datei ist alt oder von Hand geändert → neu erzeugen. |
| ⚠️ Aufwertung? / Begriff | Hat er das so gesagt? Wenn nicht: schlichter formulieren. |
| ⚠️ [PRÜFEN] als Vorschlag | Vorschlag aus dem Text nehmen, im Chat fragen. |
| ⚠️ Beispiel/Hobby ungenutzt | einbauen oder bewusst weglassen. |

Erst bei **0 ❌** zeigen oder freigeben lassen. Der Check findet nicht alles: der Selbst-Check „Jeder Satz – woher weiß ich das?“ bleibt Pflicht.
