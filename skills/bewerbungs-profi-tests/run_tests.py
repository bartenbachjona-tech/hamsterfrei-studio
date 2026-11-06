#!/usr/bin/env python3
"""Tests für bewerbungs-profi v5 – schreibt nur unter /tmp/bp_test5/work.
Start: Ordner bewerbungs-profi-tests nach /tmp/bp_test5 kopieren (fixtures/ mit fall_284.json und v5_faelle.py), dann
    python3 /tmp/bp_test5/run_tests.py
Enthält die angepassten v2–v4-Tests + Regressionen aus den Fehlerlisten Runde 1–4 und den v5-Block 16:
7 Transkript-Fälle „Nutzerwortlaut umgangssprachlich → professionelles Anschreiben“ (je EIN Lauf, 0 ❌),
18 Erfindungs-Fälle (alle ❌), Lemma/Zahlwort/Datum/Wörterbuch/Tippfehler, Satztrenner, „a“ als Ja, Stil-Check,
Spickzettel-Fehlalarme, Lebenslauf-Lücken/Zeitraum/Zukunft, offene Änderungswünsche, bearbeitbar/, Akte ohne Namen."""
import copy
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

S = "/home/claude/hamsterfrei-studio/skills/bewerbungs-profi/scripts"
W = "/tmp/bp_test5/work"
sys.path.insert(0, S)
import textlib  # noqa: E402

shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)
OUT_SNAP = sorted(os.listdir("/mnt/user-data/outputs")) if os.path.isdir("/mnt/user-data/outputs") else None
ERG = []


def run(*args, cwd=W, env=None):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd,
                       env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr


def check(name, cond, info=""):
    ERG.append((bool(cond), name))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"\n   → {str(info)[:1200]}"))


_, _o = run(f"{S}/unterlagen_erstellen.py", "--beispiel")
BSP = json.loads(_o)


def beispiel():
    return copy.deepcopy(BSP)


def speichern(d, name):
    p = os.path.join(W, name)
    json.dump(d, open(p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return p


def fc(d, name, *extra):
    return run(f"{S}/fakten_check.py", speichern(d, name), *extra)


def roh(d, nr, frage, antwort, bestaetigt=None):
    e = {"nr": nr, "frage": frage, "antwort": antwort}
    if bestaetigt:
        e["bestaetigt"] = bestaetigt
    d["profil"]["rohtext"].append(e)


def rot(o):
    return [z for z in o.splitlines() if z.startswith("❌")]


# ================================================================ 1 Dateinamen
for r_, soll in (("Petrović", "Petrovic"), ("Ayşe Şahin", "Ayse_Sahin"), ("Selin Aydın", "Selin_Aydin"),
                 ("Zoë Çelik", "Zoe_Celik"), ("Jürgen Groß", "Juergen_Gross"), ("İlkay Łukasz", "Ilkay_Lukasz")):
    check(f"Transliteration {r_}", textlib.name_teile(r_) == soll, textlib.name_teile(r_))
lang = textlib.safe_name("Kita-Verbund Sonnenberg Kinderbetreuung gemeinnützige GmbH", 30)
check("Kein Abschneiden mitten im Wort", lang == "Kita-Verbund-Sonnenberg", lang)

# ================================================================ 2 Unterlagen erstellen (AKTUELL)
os.makedirs(f"{W}/up")
from PIL import Image  # noqa: E402
Image.new("RGB", (2480, 3508), "lightgray").save(f"{W}/up/Zeugnis_10.jpg")
d = beispiel()
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"},
                          {"datei": f"{W}/up/fehlt.pdf", "bezeichnung": "Praktikumszeugnis"}]
P = speichern(d, "profil.json")
O = f"{W}/out"
rc, o = run(f"{S}/unterlagen_erstellen.py", P, "--ausgabe", O)
files = sorted(os.listdir(O))
check("Erzeugen ok, Namen …_AKTUELL", rc == 0 and "Lebenslauf_Lena_Muster_AKTUELL.pdf" in files
      and "Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf" in files, f"{files}\n{o}")
check("Fehlende Anlage gemeldet", "Anlage fehlt als Datei" in o and "Praktikumszeugnis" in o, o)
AN = f"{O}/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf"
LL = f"{O}/Lebenslauf_Lena_Muster_AKTUELL.pdf"
anl = textlib.read_any(AN)
check("Anlagen-Zeile aus echten Dateien", "Anlagen: Lebenslauf, Zeugnis der 10. Klasse" in re.sub(r"\s+", " ", anl)
      and "Praktikumszeugnis" not in anl, anl[-300:])
z = zipfile.ZipFile(f"{O}/Lebenslauf_Lena_Muster_AKTUELL.docx")
styles = z.read("word/styles.xml").decode()
h1 = re.findall(r'w:styleId="Heading1".*?</w:style>', styles, re.S)
check("Überschrift-Linie grau", h1 and "808080" in h1[0], h1[:1])
rc, o = run(f"{S}/unterlagen_erstellen.py", P, "--ausgabe", O, "--nur", "lebenslauf")
files = sorted(os.listdir(O))
check("Neue Fassung: wieder _AKTUELL, alte intern nach alt/…_v1", "Lebenslauf_Lena_Muster_AKTUELL.pdf" in files
      and not any(re.search(r"_v\d+\.", f) for f in files) and "Lebenslauf_Lena_Muster_v1.pdf" in os.listdir(f"{O}/alt"), files)
d2 = beispiel(); d2["anschreiben"]["typ"] = "motivationsschreiben"
rc, o = run(f"{S}/unterlagen_erstellen.py", speichern(d2, "mot.json"), "--ausgabe", f"{W}/out_mot", "--nur", "anschreiben", "--nur-pdf")
fm = os.listdir(f"{W}/out_mot")
check("Motivationsschreiben + --nur-pdf", "Motivationsschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf" in fm
      and not any(f.endswith(".docx") for f in fm), f"{fm}\n{o}")
rc, o = run(f"{S}/unterlagen_erstellen.py", P, "--ausgabe", O, "--nur", "formular")
FORM = f"{O}/Formular-Texte_Beispiel-GmbH_AKTUELL.txt"
ft = open(FORM, encoding="utf8").read()
check("Formular: Zeichengrenze nicht doppelt im Feldtitel", "=== Warum möchtest du zu uns? (max. 1000 Zeichen) ===" in ft
      and ft.count("max. 1000") == 1, ft[:200])
d3 = beispiel(); d3["anschreiben"]["typ"] = "kurzanschreiben"
d3["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
run(f"{S}/unterlagen_erstellen.py", speichern(d3, "kurz.json"), "--ausgabe", f"{W}/out_kurz", "--nur", "anschreiben", "--nur-pdf")
kt = textlib.read_any(f"{W}/out_kurz/Kurzanschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf")
check("Kurzanschreiben ohne Anlagen-Zeile (Regel)", "Anlagen:" not in kt, kt[-200:])
d3["anschreiben"]["anlagen_zeile"] = True
run(f"{S}/unterlagen_erstellen.py", speichern(d3, "kurz2.json"), "--ausgabe", f"{W}/out_kurz2", "--nur", "anschreiben", "--nur-pdf")
check("Kurzanschreiben: anlagen_zeile true erzwingt Zeile",
      "Anlagen:" in textlib.read_any(f"{W}/out_kurz2/Kurzanschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf"))
# Foto rechts neben dem Kopf (schwebend), Lebenslauf bleibt 1 Seite, Kopf rutscht nicht nach unten
Image.new("RGB", (900, 1200), (120, 150, 200)).save(f"{W}/up/foto.jpg")
d4 = beispiel(); d4["person"]["foto"] = f"{W}/up/foto.jpg"
run(f"{S}/unterlagen_erstellen.py", speichern(d4, "foto.json"), "--ausgabe", f"{W}/out_foto", "--nur", "lebenslauf")
docxml = zipfile.ZipFile(f"{W}/out_foto/Lebenslauf_Lena_Muster_AKTUELL.docx").read("word/document.xml").decode()
check("Foto als schwebendes Bild (wp:anchor, rechts)", "wp:anchor" in docxml and "<wp:align>right</wp:align>" in docxml
      and "wp:inline" not in docxml, docxml[:300])
subprocess.run(["pdftoppm", "-r", "40", "-png", "-f", "1", "-l", "1", f"{W}/out_foto/Lebenslauf_Lena_Muster_AKTUELL.pdf", f"{W}/foto_ll"])
png = [f for f in os.listdir(W) if f.startswith("foto_ll")]
im = Image.open(f"{W}/{png[0]}").convert("RGB")
# Name „Lena Muster“ (schwarz, fett) muss im oberen Viertel stehen → Zeile mit vielen dunklen Pixeln links oben
dunkel_y = [y for y in range(im.height // 4) if sum(1 for x in range(30, im.width // 2) if sum(im.getpixel((x, y))) < 300) > 5]
blau = [(x, y) for x in range(im.width // 2, im.width) for y in range(im.height // 3) if im.getpixel((x, y)) == (120, 150, 200)]
check("Layout als Bild: Foto rechts oben, Name bleibt oben", dunkel_y and blau and min(y for _, y in blau) < im.height // 8,
      f"dunkel {dunkel_y[:3]} blau {len(blau)}")

# ================================================================ 3 fakten_check: ehrliche Vorlagen → 0 ❌ ohne belege
B0 = beispiel()
check("Beispiel hat keine belege (keine Tricks)", B0["belege"] == [], B0["belege"])
rc, o = fc(B0, "clean.json")
check("fakten_check: ehrliches Anschreiben + Mail + Formular (JSON) → 0 ❌", rc == 0 and not rot(o), o)
d = beispiel(); d["profil"]["anlagen"] = []
Pc = speichern(d, "clean2.json")
run(f"{S}/unterlagen_erstellen.py", Pc, "--ausgabe", f"{W}/out_clean")
dateien = sorted(f"{W}/out_clean/{f}" for f in os.listdir(f"{W}/out_clean") if f.endswith((".pdf", ".txt")))
run(f"{S}/akte.py", Pc, "--ausgabe", f"{W}/out_clean")      # Akte liegt mit im Ordner
alle = sorted(f"{W}/out_clean/{f}" for f in os.listdir(f"{W}/out_clean") if f.endswith((".pdf", ".txt")))
rc, o = run(f"{S}/fakten_check.py", Pc, *alle)
check("fakten_check: erzeugte Dateien (mit Grußformel, Anlagen, Feldtiteln) → 0 ❌", rc == 0 and not rot(o), o)
check("fakten_check: Akte im Ordner wird aus Sammelprüfung ausgenommen", "Bewerbungsakte" in o and "übersprungen" in o, o)
rc, o = run(f"{S}/endcheck.py", *[x for x in dateien if "Anschreiben" in x], "--typ", "anschreiben", "--profil", Pc)
check("endcheck: ehrliches Anschreiben → 0 ❌, keine Floskel", rc == 0 and "Floskel" not in o, o)
rc, o = run(f"{S}/endcheck.py", *[x for x in dateien if "E-Mail" in x], "--typ", "email", "--profil", Pc)
check("endcheck: Mail nach Vorlage → 0 ❌, keine Firma/Stelle verlangt", rc == 0 and "Stellenbezeichnung" not in o and "kommt nicht vor" not in o, o)
rc, o = run(f"{S}/endcheck.py", *[x for x in dateien if "Formular" in x], "--typ", "formular", "--profil", Pc)
check("endcheck: Formular → 0 ❌, keine Firma/Stelle verlangt", rc == 0 and "Stellenbezeichnung" not in o and "kommt nicht vor" not in o, o)

# ================================================================ 4 fakten_check: Regressionen (Runde 1 + 2)
d = beispiel()
d["anschreiben"]["absaetze"][1] += " Dabei habe ich pro Schicht rund 250 Kunden bedient."
rc, o = fc(d, "erf.json")
check("R1 erfundene Zahl → ❌", rc == 1 and "Zahl: 250" in o, o)
# geratener Monat: Wortlaut „2018“ → JSON „09/2018“
d = beispiel()
d["profil"]["rohtext"][1]["antwort"] = "realschule beispiel 2018 bis juli 26, mittlere reife 2,3, wahlfach wirtschaft, schülerfirma"
d["profil"]["bildung"][0]["zeitraum"] = "09/2018 – 07/2026"         # Claude hat die JSON selbst „normalisiert“
d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["zeitraum"] = "09/2018 – 07/2026"
rc, o = fc(d, "monat.json")
check("R2 geratener Monat (Wortlaut 2018, JSON 09/2018) → ❌", rc == 1 and "Monat: 09/2018" in o, o)
check("R2 „juli 26“ im Wortlaut belegt 07/2026", "07/2026" not in "\n".join(z for z in o.splitlines() if "Herkunft" not in z), o)
# Bestätigung zählt nur bei klarem Ja + Wert in der Frage
d = beispiel()
d["profil"]["rohtext"][1]["antwort"] = "realschule beispiel 2018 bis juli 26, mittlere reife 2,3, wahlfach wirtschaft, schülerfirma"
roh(d, 20, "Nachfrage: Angefangen im September 2018?", "ja", "September 2018")
d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["zeitraum"] = "09/2018 – 07/2026"
rc, o = fc(d, "bestaetigt.json")
check("R2 bestätigter Monat (klares ja, Wert stand in der Frage) → ok", "09/2018" not in o, o)
d["profil"]["rohtext"][-1]["antwort"] = "weiß nicht genau"
rc, o = fc(d, "bestaetigt2.json")
check("R2 ohne klares ja zählt die Bestätigung nicht → ❌", "Monat: 09/2018" in o, o)
# Klasse B ohne Wortlaut
d = beispiel(); d["lebenslauf"]["kenntnisse"].append({"label": "Führerschein", "wert": "Klasse B"})
rc, o = fc(d, "fs.json")
check("R2 Führerschein nie erwähnt → ❌", rc == 1 and "Führerschein" in o, o)
d = beispiel(); roh(d, 20, "Hast du einen Führerschein?", "ja hab ich", "Führerschein")
d["lebenslauf"]["kenntnisse"].append({"label": "Führerschein", "wert": "Klasse B"})
rc, o = fc(d, "fsb.json")
check("R2 „Klasse B“ ohne Wortlaut (nur „Führerschein ja“) → ❌", rc == 1 and "Klasse B" in o, o)
d["profil"]["rohtext"][-1]["antwort"] = "ja, klasse b seit 2025"
rc, o = fc(d, "fsb2.json")
check("R2 „Klasse B“ im Wortlaut → ok", "Führerschein" not in o, o)
# 13. Klasse ist kein Führerschein
d = beispiel(); d["profil"]["rohtext"][1]["antwort"] += ". Jetzt bin ich in der 13. Klasse am Gymnasium"
d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["punkte"].append("13. Klasse am Gymnasium")
rc, o = fc(d, "13kl.json")
check("R2 „13. Klasse am Gymnasium“ → kein Führerschein-❌", "Führerschein" not in o and rc == 0, o)
# Dauer gerundet: Drei Jahre bei 2 J. 11 M., obwohl „3 Jahre“ in der Anzeige steht
d = beispiel(); roh(d, 20, "Studium?", "BWL an der TH Ingolstadt von 10/2023 bis 08/2026, dann abgebrochen")
d["anschreiben"]["absaetze"].insert(1, "Drei Jahre habe ich BWL studiert.")
rc, o = fc(d, "drei.json")
check("R2 „Drei Jahre“ bei 2 J. 11 M. (Anzeige nennt 3 Jahre) → ❌", rc == 1 and "Dauer" in o and "2 J. 11 M." in o, o)
d["anschreiben"]["absaetze"][1] = "Fast drei Jahre habe ich BWL studiert."
rc, o = fc(d, "drei2.json")
check("R2 „fast drei Jahre“ aus berechneter Dauer → ok", "Dauer" not in o, o)
d = beispiel(); d["anschreiben"]["absaetze"][0] = d["anschreiben"]["absaetze"][0].replace("seit September 2025", "seit acht Jahren")
rc, o = fc(d, "acht.json")
check("R1 Dauer „acht Jahre“ ohne Beleg → ❌", rc == 1 and "Dauer: 8" in o, o)
d = beispiel(); d["anschreiben"]["absaetze"].insert(1, "Die Ausbildung dauert bei Ihnen 3 Jahre.")
rc, o = fc(d, "anzdauer.json")
check("Dauer aus der Anzeige im Satz über die Stelle → ok", "Dauer" not in o, o)
# Sprachniveau, Aufwertung, Abschlusskürzel
d = beispiel(); d["lebenslauf"]["kenntnisse"][0]["wert"] = "Deutsch (Muttersprache), Englisch (C1)"
d["anschreiben"]["absaetze"][1] += " Den Stand habe ich mitkonzipiert."
rc, o = fc(d, "niv.json")
check("R1 Sprachniveau C1 erfunden → ❌", "C1" in o and rc == 1, o)
check("R1 Aufwertung „mitkonzipiert“ → ⚠️", "mitkonzipiert" in o, o)
d = beispiel(); roh(d, 20, "Studium?", "Bachelor Soziale Arbeit 2022 bis 2025")
d["lebenslauf"]["abschnitte"][1]["eintraege"].insert(0, {"zeitraum": "2022 – 2025", "titel": "Soziale Arbeit (B.A.)", "ort": "", "punkte": []})
rc, o = fc(d, "ba.json")
check("R2 Abschlusskürzel „(B.A.)“ ohne Wortlaut → ❌", rc == 1 and "b.a." in o.lower(), o)
# Weiche Erfindungen
d = beispiel()
d["anschreiben"]["absaetze"].insert(2, "Genau so möchte ich später arbeiten.")
d["anschreiben"]["absaetze"].insert(2, "Reisen ist für mich kein Problem.")
d["formular"][0]["text"] += " Ich bin sehr zuverlässig."
rc, o = fc(d, "weich.json", "--woher")
check("v4 Motivationssatz ohne Quelle → ❌ (Herkunft, nicht nur ⚠️)", rc == 1 and "Genau so möchte" in o and "kein Problem" in o
      and "Satz ohne Quelle" in o, o)
check("v4 Eigenschaft „zuverlässig“ ohne Quelle → ❌", "sehr zuverlässig" in "".join(rot(o)), o)
check("v5 Woher-Liste: belegter Satz → deine Worte (ohne interne Nr.), unbelegter → ❓", "→ deine Worte: „Die Abrechnung macht mir Spaß“" in o
      and "(Nr." not in o.split("# Fakten-Check")[0] and "❓ „Genau so möchte ich später" in o, o)
# Fehlalarme v2 (Namen)
d = beispiel()
d["anschreiben"]["absaetze"].insert(2, "Für ein Gespräch nehme ich mir gern ein paar Minuten Zeit und erledige auch mal Ihren Sachen zuliebe Extras.")
d["email"]["text"] = d["email"]["text"].replace("Mit freundlichen Grüßen\nLena Muster", "Mit freundlichen Grüßen\nLena Muster\nIngolstadt")
d["lebenslauf"]["abschnitte"][0]["eintraege"][0]["ort"] = "Supermarkt Beispiel, Ingolstadt"
rc, o = fc(d, "namen.json")
check("R2 „Minuten Zeit“, „Ihren Sachen“, Grußformel → kein Namens-❌", not [z for z in rot(o) if "Name" in z], o)
open(f"{W}/zeilen.txt", "w", encoding="utf8").write(
    "Sehr geehrte Frau Sommer,\nich wohne in Ingolstadt\nKundinnen berate ich gern.\n\nMit freundlichen Grüßen\nLena Muster\n\nAnlagen: Lebenslauf, Zeugnis der 10. Klasse\n")
rc, o = run(f"{S}/fakten_check.py", speichern(beispiel(), "zl.json"), f"{W}/zeilen.txt")
check("R2 Namen nie über Zeilenumbrüche (Ingolstadt⏎Kundinnen, Grüßen⏎Name⏎Anlagen)", not [z for z in rot(o) if "Name" in z], o)
d = beispiel(); d["anschreiben"]["absaetze"][2] = "Bei Ihnen möchte ich mit Herrn Krawczyk von der Müller Logistik GmbH arbeiten."
rc, o = fc(d, "echtname.json")
check("Echter erfundener Name/Firma → ❌", rc == 1 and ("Krawczyk" in o) and "Müller Logistik GmbH" in o, o)
# Wie aufmerksam: nur die Quelle zählt
d = beispiel(); d["formular"][2]["text"] = "Die Stelle habe ich bei Indeed entdeckt und mich gleich informiert."
d["profil"]["rohtext"][10]["antwort"] = "indeed"
d["profil"]["wie_aufmerksam"] = "Indeed"
rc, o = fc(d, "aufm.json")
check("R2 Wie aufmerksam: Quelle im Wortlaut → ok (Füllwörter egal)", "Wie aufmerksam" not in o, o)
d["formular"][2]["text"] = "Über StepStone."
rc, o = fc(d, "aufm2.json")
check("R2 Wie aufmerksam: Quelle geraten → ❌", rc == 1 and "Wie aufmerksam" in o and "stepstone" in o.lower(), o)
d["profil"]["wie_aufmerksam"] = ""
d["formular"][2]["text"] = "Über Ihre Karriereseite."
d["profil"]["rohtext"][10]["antwort"] = "karriereseite"
rc, o = fc(d, "aufm3.json")
check("Wie aufmerksam: profil.wie_aufmerksam leer → ❌ (immer fragen)", "Wie aufmerksam" in o, o)
# Firmenfakten
d = beispiel(); d["anschreiben"]["absaetze"][2] = "Mich spricht an, dass Azubis bei Ihnen eigene Projekte betreuen."
rc, o = fc(d, "ff.json")
check("R1 Firmenfakt ohne Zustimmung → ❌", rc == 1 and "Firmenfakt" in o, o)
d["firmenfakten"][0]["zugestimmt"] = True
rc, o = fc(d, "ff2.json")
check("Firmenfakt mit Zustimmung → ok", "Firmenfakt" not in o, o)
d = beispiel(); d["firmenfakten"] = [{"fakt": "Ausbildung zur Kauffrau für Büromanagement mit eigener Akademie seit 1990",
                                      "quelle": "Website", "zugestimmt": False}]
rc, o = fc(d, "ff3.json")
check("R2 Firmenfakt-Wörter nur in der Stellenbezeichnung → kein ❌", "Firmenfakt" not in o, o)
# Datum aus „ab Dezember“
d = beispiel(); d["profil"]["rohtext"][7]["antwort"] = "ab dezember"
d["formular"][1]["text"] = "01.12.2026"
d["anschreiben"]["absaetze"][3] = "Ich freue mich auf ein persönliches Gespräch."
d["email"]["text"] = d["email"]["text"].replace(" ab 01.09.2027", "")
d["anschreiben"]["betreff"] = "Bewerbung um einen Ausbildungsplatz als Kauffrau für Büromanagement (Kennziffer AZ-2027-04)"
rc, o = fc(d, "dez.json")
check("R2 „01.12.2026“ aus „ab Dezember“ → ❌ Tag erfunden", rc == 1 and "01.12.2026" in o, o)
d["formular"][1]["text"] = "ab Dezember 2026"
rc, o = fc(d, "dez2.json")
check("„ab Dezember 2026“ aus „ab dezember“ → ok", "12/2026" not in o and "Dezember" not in "".join(rot(o)), o)
# belege nur mit Zitat
d = beispiel(); d["anschreiben"]["absaetze"][1] += " Seit über einem Jahr arbeite ich an der Kasse."
d["herkunft"].append({"satz": "Seit über einem Jahr arbeite ich an der Kasse.", "nr": 3, "zitat": "an der Kasse im Supermarkt Beispiel in Ingolstadt seit 09/2025"})
d["belege"] = [{"text": "seit über einem Jahr", "woher": "Minijob seit 09/2025"}]
rc, o = fc(d, "bel.json")
check("belege ohne zitat → ❌", rc == 1 and "Beleg ohne Zitat" in o, o)
d["belege"] = [{"text": "seit über einem Jahr", "woher": "Minijob seit 09/2025, heute 11/2026", "zitat": "Kasse im Supermarkt Beispiel in Ingolstadt seit 09/2025"}]
rc, o = fc(d, "bel2.json")
check("belege mit wörtlichem Zitat → ok", rc == 0 and "Beleg ohne Zitat" not in o, o)
d["anschreiben"]["absaetze"][1] = d["anschreiben"]["absaetze"][1].replace("Seit über einem Jahr", "Seit drei Jahren")
d["herkunft"][-1]["satz"] = "Seit drei Jahren arbeite ich an der Kasse."
d["belege"] = [{"text": "seit drei Jahren", "woher": "Minijob", "zitat": "Kasse im Supermarkt Beispiel in Ingolstadt seit 09/2025"}]
rc, o = fc(d, "bel3.json")
check("v4 belege: Zitat trägt den Wert nicht („drei Jahre“ aus „seit 09/2025“) → ❌", rc == 1 and "trägt den Wert nicht" in o, o)
# Zeugnis-Text als Beleg (Upload via textlib)
open(f"{W}/up/Zeugnis_Text.txt", "w", encoding="utf8").write("Abschlusszeugnis Realschule Beispiel. Mathematik 1, Deutsch 2. Notendurchschnitt 2,3")
d = beispiel(); d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_Text.txt", "bezeichnung": "Abschlusszeugnis"}]
d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["punkte"].append("Mathematik: Note 1")
rc, o = fc(d, "zeug.json")
check("Zeugnis-Upload (Text) belegt Note → ok", rc == 0, o)
# [PRÜFEN] als Vorschlag, ungenutztes Beispiel, Abgleich
d = beispiel()
d["anschreiben"]["absaetze"][2] = "Bei Ihnen könnte ich eigene Projekte betreuen. [PRÜFEN: Stimmt das so?]"
d["profil"]["beispiele"].append({"thema": "Zuverlässigkeit", "stichwort": "Fußball", "situation": "Kapitän der B-Jugend"})
rc, o = fc(d, "pr.json")
check("R1 [PRÜFEN] als Vorschlag → ⚠️", "[PRÜFEN] als Vorschlag" in o, o)
check("R1 ungenutztes Beispiel (Fußball) → ⚠️", "Beispiel ungenutzt" in o and "Fußball" in o, o)
d = beispiel(); d["profil"]["anlagen"] = []
Pa = speichern(d, "abg.json")
run(f"{S}/unterlagen_erstellen.py", Pa, "--ausgabe", f"{W}/out_abg", "--nur", "anschreiben")
d["anschreiben"]["absaetze"][3] = "Ich freue mich darauf, Sie kennenzulernen."
speichern(d, "abg.json")
run(f"{S}/unterlagen_erstellen.py", Pa, "--ausgabe", f"{W}/out_abg2", "--nur", "anschreiben")
rc, o = run(f"{S}/fakten_check.py", Pa, f"{W}/out_abg/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf")
check("Abgleich: Datei ≠ freigegebener Text → ❌", rc == 1 and "Abgleich" in o, o)
rc, o = run(f"{S}/fakten_check.py", Pa, f"{W}/out_abg2/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf")
check("Abgleich: neue Datei = JSON → ok", "Abgleich" not in o and rc == 0, o)
# Legacy-Akte ohne rohtext
d = beispiel(); del d["profil"]["rohtext"]
rc, o = fc(d, "legacy.json")
check("v2-JSON ohne rohtext: läuft, warnt „Kein Wortlaut“", rc in (0, 1) and "Kein Wortlaut" in o and "LEGACY" in o, o)

# Realistischer Fall (Transkript 284): knappe Kleinbuchstaben-Antworten, Auswahl „a und b“, Lücke → 0 ❌
F284 = json.load(open("/tmp/bp_test5/fixtures/fall_284.json", encoding="utf8"))
rc, o = fc(copy.deepcopy(F284), "f284.json", "--woher")
check("Fall 284: ehrliche Texte aus knappen Antworten → 0 ❌", rc == 0 and not rot(o), o)
check("Fall 284: Auswahl-Antwort „a und b“ belegt Optionstext (Woher ohne Nr.)", "„Übernahme bei guten Leistungen“" in o and "(Nr. 9)" not in o, o)
check("Fall 284: Lücken-Monate aus Nachbarmonaten → nur ⚠️", "aus dem Nachbarmonat" in o, o)
check("Fall 284: „Grundkenntnisse“ aus „bisschen“ → nur ⚠️", "⚠️ [lebenslauf (JSON)] Niveau: Grundkenntnisse" in o, o)
d = copy.deepcopy(F284); d["lebenslauf"]["kenntnisse"][1]["wert"] = "Excel (sehr gute Kenntnisse)"
rc, o = fc(d, "f284b.json")
check("Fall 284: Aufwertung „sehr gute Kenntnisse“ → ❌", rc == 1 and "sehr gute Kenntnisse" in o, o)
d = copy.deepcopy(F284); d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["zeitraum"] = "09/2018 – 07/2024"
rc, o = fc(d, "f284c.json")
check("Fall 284: „09/2018“ aus „meist September“ → ❌ (Transkript-Fehler)", rc == 1 and "Monat: 09/2018" in o, o)
d = copy.deepcopy(F284); d["formular"][0]["text"] += " Bei Ihnen möchte ich das Kommissionieren mit dem Scanner richtig lernen."
rc, o = fc(d, "f284d.json")
check("Fall 284: dazugedichteter Satz (Begriffe aus der Anzeige) ohne Quelle → ❌", rc == 1 and "Kommissionieren" in "".join(rot(o)), o)
d["herkunft"].append({"satz": "Bei Ihnen möchte ich das Kommissionieren mit dem Scanner richtig lernen.",
                      "quellen": [{"anzeige": "Kommissionieren"}]})
rc, o = fc(d, "f284e.json")
check("Fall 284: Satz über die Person nur mit Anzeige-Zitat → ❌", rc == 1 and ("die Anzeige belegt nichts über dich" in o or "Wörter ohne Quelle" in o), o)

# ================================================================ 5 endcheck
rc, o = run(f"{S}/endcheck.py", AN, "--typ", "anschreiben", "--profil", P)
check("endcheck: normale E-Mail-Adresse ohne Warnung", "E-Mail lena" not in o, o)
check("endcheck: Firma erkannt", "kommt nicht vor" not in o, o)
open(f"{W}/brief.txt", "w", encoding="utf8").write(
    "Sehr geehrte Frau Sommer,\nseit 2025 arbeite ich bei der Supermarkt Beispiel GmbH an der Kasse. "
    "Davor war ich bei der Müller Logistik GmbH. Ich bewerbe mich als Kauffrau bei Beispiel.\n"
    "Mit freundlichen Grüßen\nLena Muster\npartymaus2007@web.de")
d = beispiel(); d["profil"]["stationen"][0]["firma"] = "Supermarkt Beispiel GmbH"
Pe = speichern(d, "ec.json")
rc, o = run(f"{S}/endcheck.py", f"{W}/brief.txt", "--typ", "anschreiben", "--profil", Pe)
check("endcheck: Spitzname in E-Mail gewarnt (Geburtsjahr allein ist keine Zahlenfolge)", "partymaus2007" in o and "Spitzname" in o and "Zahlenfolge" not in o, o)
check("endcheck: echte Fremdfirma gemeldet, früherer Arbeitgeber nicht", "Müller Logistik GmbH" in o and "Supermarkt Beispiel GmbH" not in o.split("Fremde")[-1], o)
check("endcheck: Stelle unvollständig (Büromanagement fehlt)", "unvollständig" in o and "büromanagement" in o.lower(), o)
open(f"{W}/brief2.txt", "w", encoding="utf8").write("Sehr geehrte Frau Sommer,\nich bin Melis.\nMit freundlichen Grüßen\nMelis Karaca\nmelis.k2007@web.de / melis.karaca1234567@web.de")
rc, o = run(f"{S}/endcheck.py", f"{W}/brief2.txt", "--typ", "anschreiben")
check("v4 endcheck: melis.k2007 ohne Warnung, lange Zahlenfolge mit Warnung", "melis.k2007@web.de:" not in o and "melis.karaca1234567" in o and "Zahlenfolge" in o, o)
for firma, txt in (("Krankenkasse Augusta", "bei der Krankenkasse Augusta in Augsburg"),
                   ("Augusta Reisen GmbH", "bei Augusta Reisen in Augsburg"),
                   ("Sparkasse Augsburg", "bei der Sparkasse Augsburg"),
                   ("AOK Bayern – Die Gesundheitskasse", "bei der AOK Bayern")):
    open(f"{W}/fa.txt", "w", encoding="utf8").write(f"Sehr geehrte Damen und Herren,\nich möchte {txt} arbeiten.\nMit freundlichen Grüßen\nLena")
    rc, o = run(f"{S}/endcheck.py", f"{W}/fa.txt", "--typ", "anschreiben", "--firma", firma)
    check(f"R2 Rechtsform-Schnitt: „{firma}“ erkannt", "kommt nicht vor" not in o, o)
import endcheck  # noqa: E402
check("kern_firma: Krankenkasse/Augusta/Reisen bleiben ganz",
      endcheck.kern_firma("Krankenkasse Augusta") == ["krankenkasse", "augusta"] and endcheck.kern_firma("Augusta Reisen GmbH") == ["augusta", "reisen"],
      endcheck.kern_firma("Krankenkasse Augusta"))
open(f"{W}/fl.txt", "w", encoding="utf8").write(
    "Sehr geehrte Damen und Herren,\nBetreff: Bewerbung als Medizinische Fachangestellte\n"
    "ich bewerbe mich um die Ausbildung zur Medizinischen Fachangestellten in Ihrer Praxis Dr. Huber.\nMit freundlichen Grüßen\nLena")
rc, o = run(f"{S}/endcheck.py", f"{W}/fl.txt", "--typ", "anschreiben", "--firma", "Praxis Dr. Huber", "--stelle", "Medizinische/r Fachangestellte/r (m/w/d)")
check("R2 Flexion der Stellenbezeichnung toleriert", "Stellenbezeichnung" not in o, o)
open(f"{W}/fl2.txt", "w", encoding="utf8").write("Sehr geehrte Damen und Herren,\nich will zur Praxis.\nÜber eine Einladung würde ich mich sehr freuen.\nMit freundlichen Grüßen\nLena")
rc, o = run(f"{S}/endcheck.py", f"{W}/fl2.txt", "--typ", "anschreiben", "--firma", "Praxis Huber")
check("R2 „würde ich mich sehr freuen“ als Floskel erkannt", "Floskel" in o and "freuen" in o, o)
open(f"{W}/fl3.txt", "w", encoding="utf8").write("Sehr geehrte Damen und Herren,\nmit großem Interesse habe ich Ihre Anzeige gelesen. Ich möchte Ihr renommiertes Unternehmen bereichern.\nMit freundlichen Grüßen\nLena")
rc, o = run(f"{S}/endcheck.py", f"{W}/fl3.txt", "--typ", "anschreiben")
check("Gebeugte Floskeln (großem Interesse, renommiertes, bereichern)", "großem Interesse" in o and "renommiertes" in o and "bereichern" in o, o)
open(f"{W}/mail.txt", "w", encoding="utf8").write("Betreff: Bewerbung\n\nSehr geehrte Frau Sommer,\nanbei meine Unterlagen.\n\nMit freundlichen Grüßen\nLena Muster")
rc, o = run(f"{S}/endcheck.py", f"{W}/mail.txt", "--typ", "email", "--firma", "Beispiel GmbH", "--stelle", "Kauffrau für Büromanagement")
check("R2 E-Mail: Firma/Stelle NICHT verlangt", rc == 0 and "kommt nicht vor" not in o and "Stellenbezeichnung" not in o, o)
open(f"{W}/Formular_x.txt", "w", encoding="utf8").write("=== Motivation (max. 50 Zeichen) ===\nIch habe die Anzeige auf [Name des Jobportals] gesehen und will unbedingt zu Ihnen.\n\n=== Eintritt ===\n\n")
rc, o = run(f"{S}/endcheck.py", f"{W}/Formular_x.txt", "--typ", "formular", "--firma", "Beispiel GmbH")
check("endcheck: Formular Limit/Platzhalter/leer, aber Firma nicht verlangt", "erlaubt 50" in o and "Platzhalter" in o and "ist leer" in o and "kommt nicht vor" not in o, o)
rc, o = run(f"{S}/endcheck.py", f"{W}/up/Zeugnis_10.jpg", "--typ", "anlage")
check("R2 Typ anlage: Zeugnis-Bild ohne Textprüfung", rc == 0 and "Kein Text" not in o and "E-Mail" not in o, o)
open(f"{W}/kurz.txt", "w").write("Sehr geehrte Damen und Herren,\n" + "Wort " * 170 + "\nMit freundlichen Grüßen")
rc, o = run(f"{S}/endcheck.py", f"{W}/kurz.txt", "--typ", "kurzanschreiben")
check("endcheck: Kurzanschreiben-Bewertung nur bei --typ kurzanschreiben", "passt als Kurzanschreiben" in o, o)

# ================================================================ 6 pdf_zusammenfuegen
import pypdf  # noqa: E402
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Bewerbung.pdf", AN, LL, f"{W}/up/gibtsnicht.pdf")
check("PDF: fehlende Datei → Exit 2, keine PDF", rc == 2 and not os.path.exists(f"{W}/pdf/Bewerbung.pdf"), o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Bewerbung Lena", "IT-Support.pdf", AN)
check("PDF: Zielname ohne .pdf → Exit 2", rc == 2, o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Bewerbung-Lena-Muster_Kauffrau.pdf", LL)
check("R2 Dateiname mit Bindestrich bleibt exakt", rc == 0 and os.path.exists(f"{W}/pdf/Bewerbung-Lena-Muster_Kauffrau.pdf"), f"{o} {os.listdir(W + '/pdf')}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Bewerbung Lena Müller.pdf", LL)
check("Problemzeichen im Namen: klare Meldung statt stiller Umbenennung", rc == 0 and "Dateiname angepasst" in o
      and os.path.exists(f"{W}/pdf/Bewerbung_Lena_Mueller.pdf"), o)
Image.new("RGB", (3000, 2000), "lightgray").save(f"{W}/up/IMG_4471.jpg")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Quer.pdf", f"{W}/up/IMG_4471.jpg")
pg = pypdf.PdfReader(f"{W}/pdf/Quer.pdf").pages[0]
w_, h_ = float(pg.mediabox.width), float(pg.mediabox.height)
check("R2 Querformat-Foto → A4-Querseite, groß (nicht klein hochkant)", rc == 0 and abs(w_ - 842) < 3 and abs(h_ - 595) < 3 and "Querformat" in o, f"{w_}x{h_} {o}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Quer2.pdf", f"{W}/up/IMG_4471.jpg", "--drehen", "IMG_4471.jpg=90")
pg = pypdf.PdfReader(f"{W}/pdf/Quer2.pdf").pages[0]
check("--drehen 90: Querfoto wird hochkant auf A4", abs(float(pg.mediabox.width) - 595) < 3, o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Foto.pdf", f"{W}/up/Zeugnis_10.jpg")
pg = pypdf.PdfReader(f"{W}/pdf/Foto.pdf").pages[0].mediabox
check("Hochkant-Foto auf A4", abs(float(pg.width) - 595.3) < 2 and abs(float(pg.height) - 842) < 2, f"{pg} {o}")
# PDF-Anlage im Letter-Format → A4
wl = pypdf.PdfWriter(); wl.add_blank_page(width=612, height=792); wl.write(open(f"{W}/up/Zertifikat_Letter.pdf", "wb"))
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Letter.pdf", f"{W}/up/Zertifikat_Letter.pdf")
pg = pypdf.PdfReader(f"{W}/pdf/Letter.pdf").pages[0].mediabox
check("R2 PDF-Anlage (Letter) auf A4 skaliert", abs(float(pg.width) - 595.3) < 2 and abs(float(pg.height) - 842) < 2, f"{pg} {o}")
import pillow_heif  # noqa: E402
pillow_heif.register_heif_opener()
Image.new("RGB", (800, 1000), "white").save(f"{W}/up/Foto.heic")
open(f"{W}/up/kaputt.heic", "wb").write(b"keinbild")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Heic.pdf", f"{W}/up/Foto.heic")
check("HEIC wird umgewandelt", rc == 0 and os.path.exists(f"{W}/pdf/Heic.pdf"), o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Heic2.pdf", f"{W}/up/kaputt.heic")
check("Kaputtes HEIC → Handy-Anleitung, Exit 2", rc == 2 and "Screenshot" in o, o)
# Fassung in alt/ bzw. gelöschter Pfad → aktuelle wird genommen
alt_ll = f"{O}/alt/Lebenslauf_Lena_Muster_v1.pdf"
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Neu.pdf", alt_ll)
check("R2 Pfad zeigt in alt/ → aktuelle Fassung genommen", rc == 0 and "Lebenslauf_Lena_Muster_AKTUELL.pdf" in o, o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Neu2.pdf", f"{O}/Lebenslauf_Lena_Muster_v2.pdf")
check("R2 Pfad existiert nicht mehr (_v2) → aktuelle Fassung statt Abbruch", rc == 0 and "AKTUELL" in o, o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/pdf/Falsch.pdf", AN, LL)
check("Anlagen-Zeile passt nicht (ohne Profil) → Exit 3", rc == 3 and "Anlagen-Zeile" in o, o)
# Profil: Anschreiben VOR dem Zeugnis-Upload erzeugt → Anlagen-Zeile wird automatisch nachgezogen
d = beispiel(); d["profil"]["anlagen"] = []
Pp = speichern(d, "pp.json")
run(f"{S}/unterlagen_erstellen.py", Pp, "--ausgabe", f"{W}/out_pp", "--nur-pdf")
d["profil"]["anlagen"] = [{"datei": f"{W}/up/IMG_4471.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
speichern(d, "pp.json")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/out_pp/Bewerbung_Lena_Muster_Kauffrau.pdf", "--profil", Pp, "--ordner", f"{W}/out_pp")
n = len(pypdf.PdfReader(f"{W}/out_pp/Bewerbung_Lena_Muster_Kauffrau.pdf").pages) if rc == 0 else 0
neu_an = textlib.read_any(f"{W}/out_pp/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf")
check("R2 Anlagen-Zeile nach späterem Upload automatisch neu (3 Seiten)", rc == 0 and n == 3 and "automatisch neu" in o
      and "Zeugnis der 10. Klasse" in neu_an, o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--einzeln", "--profil", Pp, "--ausgabe", f"{W}/out_pp")
fl = os.listdir(f"{W}/out_pp")
check("R2 --einzeln: Bezeichnung statt IMG_…, flach (kein versand/), Hochlade-Liste",
      "Zeugnis_der_10_Klasse_Lena_Muster.pdf" in fl and "Lebenslauf_Lena_Muster.pdf" in fl and "versand" not in fl
      and not any(f.startswith("IMG") for f in fl) and "hochladen" in o, f"{fl}\n{o}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--einzeln", f"{W}/up/IMG_4471.jpg", "--name", "IMG_4471.jpg=Praktikumszeugnis", "--ausgabe", f"{W}/out_ein")
check("--einzeln --name DATEI=Bezeichnung", os.listdir(f"{W}/out_ein") and "Praktikumszeugnis.pdf" in os.listdir(f"{W}/out_ein"), f"{os.listdir(W + '/out_ein')} {o}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--buendeln", "3", "--profil", Pp, "--ordner", f"{W}/out_pp", "--ausgabe", f"{W}/out_b3")
check("R2 Upload-Limit max. 3 Dateien: Anschreiben | Lebenslauf | Anlagen", rc == 0 and sorted(os.listdir(f"{W}/out_b3")) ==
      ["Anlagen_Lena_Muster.pdf", "Anschreiben_Lena_Muster.pdf", "Lebenslauf_Lena_Muster.pdf"], f"{os.listdir(W + '/out_b3')} {o}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--buendeln", "2", "--profil", Pp, "--ordner", f"{W}/out_pp", "--ausgabe", f"{W}/out_b2")
check("Upload-Limit max. 2 Dateien: Lebenslauf | Anschreiben+Anlagen", rc == 0 and len(os.listdir(f"{W}/out_b2")) == 2
      and "Anschreiben_und_Anlagen_Lena_Muster.pdf" in os.listdir(f"{W}/out_b2"), o)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/out_pp/Bewerbung_Lena_Muster_Kauffrau.pdf", "--profil", Pp, "--ordner", f"{W}/out_pp")
check("Ältere Gesamt-PDF → alt/", rc == 0 and any(f.startswith("Bewerbung_Lena_Muster_Kauffrau_alt") for f in os.listdir(f"{W}/out_pp/alt")), o)
rc, o = run(f"{S}/endcheck.py", f"{W}/out_pp/Bewerbung_Lena_Muster_Kauffrau.pdf", "--typ", "gesamt", "--profil", Pp)
check("R2 endcheck --typ gesamt mit Scan-Seite: keine Fehlalarme", rc == 0 and "Keine E-Mail" not in o and "Floskel" not in o, o)

# ================================================================ 7 Berufstest
for code, ant in (("S+C", "1e 2a 3b 4e 5e 6d 7a 8e 9d 10e 11b 12e"), ("I+C", "1e 2e 3b 4a 5e 6e 7e 8e 9e 10a 11b 12e"),
                  ("A+E", "1e 2e 3e 4e 5a 6a 7e 8e 9b 10e 11e 12a"), ("I+S", "1e 2a 3e 4a 5e 6e 7b 8e 9e 10a 11e 12e")):
    rc, o = run(f"{S}/berufstest_auswerten.py", ant)
    check(f"Berufstest {code} nicht 'gegenüber'", "gegenüber" not in o and "eine Ecke" in o, o)
rc, o = run(f"{S}/berufstest_auswerten.py", "1a 2a 3e 4e 5e 6e 7a 8a 9e 10e 11e 12e")
check("Berufstest R+S = gegenüber", "gegenüber" in o, o)

# ================================================================ 8 Akte
A = f"{W}/akte"
d = beispiel()
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
d["profil"]["wechselgrund"] = "möchte nach der Elternzeit wieder Vollzeit arbeiten"
d["profil"]["berufstest"] = {"code": "SC", "vorschlaege": ["Kauffrau für Büromanagement", "Sozialversicherungsfachangestellte"]}
d["profil"]["zertifikate"] = ["Staplerschein"]
Pk = speichern(d, "akte.json")
rc, o = run(f"{S}/akte.py", Pk, "--ausgabe", A)
rc2, o2 = run(f"{S}/akte.py", Pk, "--ausgabe", A)
akten = sorted(os.listdir(A))
txt_akten = [f for f in akten if f.endswith(".txt")]
check("R2 Akte: Sekunden im Namen, zwei Akten in derselben Minute verschieden", len(txt_akten) == 1 and
      re.search(r"_\d{4}-\d{2}-\d{2}_\d{6}(_\d+)?\.txt$", txt_akten[0]) and len(os.listdir(f"{A}/alt")) == 1
      and os.listdir(f"{A}/alt")[0] != txt_akten[0], f"{akten} {os.listdir(A + '/alt')}")
check("R2 Akte nur .txt (PDF nur auf Wunsch)", not any(f.endswith(".pdf") for f in akten), akten)
txt = open(f"{A}/{txt_akten[0]}", encoding="utf8").read()
check("R2 Akte: Liste „im neuen Chat noch einmal mit hochladen“", "noch einmal mit hochladen" in txt and "Zeugnis_10.jpg (Zeugnis der 10. Klasse)" in txt, txt[:600])
check("R2 Akte: Wechselgrund, Berufstest, Zertifikate lesbar", "Wechselgrund: möchte nach der Elternzeit" in txt
      and "BERUFSTEST" in txt and "Ergebnis (Code): SC" in txt and "Staplerschein" in txt, txt[:2500])
check("R2 Akte: keine doppelten Klammern", "(Minijob) (Minijob)" not in txt and "))" not in txt.split(textlib.AKTE_START)[0], txt[:2000])
rc, o = run(f"{S}/akte.py", Pk, "--ausgabe", f"{W}/akte_pdf", "--pdf")
fp = os.listdir(f"{W}/akte_pdf")
check("R2 Akte-PDF heißt anders als die .txt (Akte-Lesefassung_…)", any(f.startswith("Akte-Lesefassung_") and f.endswith(".pdf") for f in fp)
      and not any(f.startswith("Bewerbungsakte_") and f.endswith(".pdf") for f in fp), fp)
lesef = [f for f in fp if f.endswith(".pdf")][0]
pt = textlib.read_any(f"{W}/akte_pdf/{lesef}")
check("Akte-PDF: Umlaute korrekt, keine Daten-JSON", "Büromanagement" in pt and "DATEN FUER CLAUDE" not in pt, pt[:300])
# --lesen im neuen Chat: Anlage liegt unter neuem Upload-Pfad
os.makedirs(f"{W}/neue_uploads")
d_up = beispiel(); d_up["profil"]["anlagen"] = [{"datei": "/alt/chat/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"},
                                                 {"datei": "/alt/chat/Praktikum.pdf", "bezeichnung": "Praktikumszeugnis"}]
shutil.copy(f"{W}/up/Zeugnis_10.jpg", f"{W}/neue_uploads/Zeugnis_10.jpg")
run(f"{S}/akte.py", speichern(d_up, "akte_up.json"), "--ausgabe", f"{W}/akte_up")
akte_up = [f for f in os.listdir(f"{W}/akte_up") if f.endswith(".txt")][0]
rc, o = run(f"{S}/akte.py", "--lesen", f"{W}/akte_up/{akte_up}", "--json-nach", f"{W}/fort/profil.json", env={"BP_UPLOADS": f"{W}/neue_uploads"})
dz = json.load(open(f"{W}/fort/profil.json"))
check("Akte --lesen: Anlage im neuen Upload gefunden, fehlende genannt", rc == 0 and dz["profil"]["anlagen"][0]["datei"] == f"{W}/neue_uploads/Zeugnis_10.jpg"
      and "Praktikum.pdf" in o and "noch einmal hochladen" in o, o)
check("Akte --lesen: Roundtrip mit rohtext", dz["profil"]["rohtext"] and dz["person"]["name"] == "Lena Muster", "")
open(f"{W}/alt_akte.md", "w").write("# Bewerbungsakte\n\n```json\n" + json.dumps({"person": {"name": "Alt Nutzer"}}) + "\n```\n")
rc, o = run(f"{S}/akte.py", "--lesen", f"{W}/alt_akte.md", "--json-nach", f"{W}/fort/alt.json")
check("Akte --lesen: alte .md (v1)", rc == 0 and "Alte Akte" in o, o)
rc, o = run(f"{S}/unterlagen_erstellen.py", f"{A}/{txt_akten[0]}", "--ausgabe", f"{W}/out_akte", "--nur", "lebenslauf", "--kein-pdf")
check("Unterlagen direkt aus Akte .txt", rc == 0 and os.listdir(f"{W}/out_akte"), o)

# ================================================================ 9 Spickzettel
d = beispiel()
roh(d, 12, "Lücke?", "08/2024 bis 02/2025 hab ich einen Ausbildungsplatz gesucht und Bewerbungen geschrieben")
roh(d, 13, "Schwäche?", "ich werde ungeduldig wenn was lange dauert, an der kasse plane ich mir feste pausen ein")
d["profil"]["luecken"] = [{"zeitraum": "08/2024 – 02/2025", "erklaerung": "Ausbildungsplatz gesucht und Bewerbungen geschrieben"}]
d["gespraech"].update({
    "termin": "12.11.2026, 10:00 Uhr", "art": "vor Ort", "ort": "Hauptstraße 5, 85049 Ingolstadt", "gespraechspartner": "Frau Petra Sommer",
    "einladung_text": "Wir laden Sie am 12.11.2026 um 10:00 Uhr in die Hauptstraße 5 ein. Bitte bringen Sie Ihren Personalausweis mit.",
    "mitbringen": ["Personalausweis", "Lebenslauf ausgedruckt"],
    "kernbotschaften": ["Ich mache an der Kasse die Abrechnung am Schichtende selbst", "In der Schülerfirma haben wir zu fünft einen Verkaufsstand geplant",
                        "Ab 01.09.2027 kann ich anfangen"],
    "selbstpraesentation": ["Mittlere Reife 07/2026 an der Realschule Beispiel", "Seit 09/2025 Minijob an der Kasse"],
    "schwierige_fragen": [{"frage": "Was ist Ihre Schwäche?", "antwort": "ich bin ungeduldig",
                           "antwort_final": "Ich werde ungeduldig, wenn etwas lange dauert. An der Kasse plane ich mir darum feste Pausen ein."}],
    "feedback": [{"frage": "Was ist Ihre Schwäche?", "besser": "Ich werde ungeduldig, wenn etwas lange dauert. An der Kasse plane ich mir darum feste Pausen ein."}],
    "eigene_fragen": [{"frage": "Wie sieht die Einarbeitung aus?", "gewaehlt": True}, {"frage": "Gibt es Gleitzeit?", "gewaehlt": False},
                      "Wie groß ist das Team? (Vorschlag Claude, intern)"]})
d["profil"]["beispiele"].append({"thema": "Ordnung", "situation": "", "aufgabe": "", "handlung": "", "ergebnis": ""})
Ps = speichern(d, "sp.json")
rc, o = run(f"{S}/akte.py", Ps, "--spickzettel", "--pdf", "--ausgabe", f"{W}/sp")
sp_txt = open(f"{W}/sp/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("R2 Spickzettel: Termin | Art | Ort mit Trennzeichen", "Termin: 12.11.2026, 10:00 Uhr | Art: vor Ort | Ort: Hauptstraße 5" in sp_txt, sp_txt[:300])
check("R2 Spickzettel: Mitbring-Liste, 3 Kernbotschaften", "MITBRINGEN" in sp_txt and "Personalausweis" in sp_txt and "DEINE 3 KERNBOTSCHAFTEN" in sp_txt, sp_txt)
check("v4 Spickzettel: finale Antwort (antwort_final) statt Rohfassung, Feedback nur einmal", "plane ich mir darum feste Pausen" in sp_txt
      and "ich bin ungeduldig" not in sp_txt and sp_txt.count("feste Pausen") == 1, sp_txt)
check("v4 Spickzettel: Lücke NICHT automatisch als Frage, aber Hinweis an Claude", "Was war 08/2024" not in sp_txt
      and "profil.luecken vorhanden" in o, o)
check("R2 Spickzettel: nur gewählte eigene Fragen, keine internen Vermerke", "Einarbeitung" in sp_txt and "Gleitzeit" not in sp_txt
      and "Vorschlag Claude" not in sp_txt and "intern" not in sp_txt, sp_txt)
check("R2 Spickzettel: keine leeren Felder", "Aufgabe:  |" not in sp_txt and "(offen)" not in sp_txt and not re.search(r":\s*\|", sp_txt)
      and "Ordnung: " not in sp_txt, sp_txt)
check("R2 Spickzettel: vor Ort → keine Video-Tipps", "Kamera" not in sp_txt and "VOR ORT" in sp_txt.upper(), sp_txt)
check("Spickzettel-PDF erzeugt (sauber, ohne #/**)", os.path.exists(f"{W}/sp/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.pdf")
      and "**" not in textlib.read_any(f"{W}/sp/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.pdf"), o)
rc, o = run(f"{S}/fakten_check.py", Ps, "--typ", "spickzettel")
check("fakten_check --typ spickzettel: ehrlicher Spickzettel → 0 ❌", rc == 0, o)
d2 = copy.deepcopy(d); d2["gespraech"]["selbstpraesentation"].append("Seit 8 Jahren im Handballverein")
rc, o = fc(d2, "sp2.json", "--typ", "spickzettel")
check("R2 Spickzettel-Check findet „8 Jahre“ ohne Beleg", rc == 1 and "Dauer: 8" in o, o)
d3 = copy.deepcopy(d); d3["gespraech"]["art"] = "Assessment Center"; d3["gespraech"]["ac_uebungen"] = ["Gruppendiskussion", "Postkorb", "Interview"]
run(f"{S}/akte.py", speichern(d3, "sp3.json"), "--spickzettel", "--ausgabe", f"{W}/sp_ac")
ac = open(f"{W}/sp_ac/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("R2 AC-Spickzettel: Übungen mit Tipp, Grammatik „deinen Auswahltag“", "DEIN AUSWAHLTAG" in ac and "Postkorb: A sofort" in ac
      and "TIPPS FÜR DEINEN AUSWAHLTAG" in ac and "DEIN AUSWAHLTAG\n" not in ac.replace("DEIN AUSWAHLTAG – DIE ÜBUNGEN", ""), ac)

# ================================================================ 10 Ordner, textlib
os.makedirs(f"{W}/basis")
rc, o = run(f"{S}/ordner_anlegen.py", f"{W}/basis", "Kita-Verbund Sonnenberg gGmbH", "Erzieher/in (PiA)", AN, "--profil", P, "--zip", "--ausgabe", f"{W}/zip")
check("ordner_anlegen: Ordner + Akte + ZIP", rc == 0 and os.listdir(f"{W}/zip") and
      any(f.startswith("Bewerbungsakte_") for f in os.listdir(f"{W}/basis/Bewerbung_Kita-Verbund-Sonnenberg-gGmbH_Erzieher-in-PiA")), o)
rc, o = run(f"{S}/textlib.py", LL, "--info")
check("textlib --info: eigener LL nicht mehrspaltig", "keine Hinweise auf mehrere Spalten" in o, o[-400:])
rc, o = run(f"{S}/textlib.py", "--help")
check("textlib --help", "Text aus Word" in o, o)

# ================================================================ 12 v4 Satz-Herkunft (Transkripte 500, 530, 920, 941)
def h_profil(roh_liste, name="Lena Muster", **teile):
    d = beispiel()
    d["person"]["name"] = name
    d["profil"]["rohtext"] = [{"nr": i + 1, "frage": f"Frage {i + 1}", "antwort": a} for i, a in enumerate(roh_liste)]
    d["anschreiben"]["absaetze"] = teile.get("anschreiben", [])
    d["formular"] = [{"feld": f["feld"], "limit": 1000, "text": f["text"]} for f in teile.get("formular", [])]
    d["email"] = {"betreff": "Bewerbung", "text": teile.get("email", "")}
    d["whatsapp"] = {"text": teile.get("whatsapp", "")}
    d["herkunft"] = teile.get("herkunft", [])
    d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [], "kenntnisse": [], "interessen": ""}
    d["profil"]["beispiele"], d["profil"]["hobbys"], d["profil"]["anlagen"] = [], [], []
    d["firmenfakten"] = teile.get("firmenfakten", [])
    return d


def herk_rot(o):
    return "\n".join(z for z in rot(o) if "[Herkunft]" in z)


R500 = ["Hallo, ich hoffe Sie können mir helfen.", "Ja das stimmt. SAP kann ich aber nicht, ist das schlimm?",
        "Kerstin Albrecht, Schillerstraße 15, 86633 Neuburg an der Donau, 0160 93374512, k.albrecht@gmx.de",
        "Realschule Neuburg 2000 Mittlere Reife.",
        "seit 2003 bei Lechner. Erst Disposition bis 2012 glaube ich, dann Abrechnung/Fakturierung bis heute. Ich mache die Rechnungen für ca. 150 Kunden im Monat, Gutschriften, Mahnungen",
        "Hab im Vertrag nachgeschaut: seit 01.04.2012 Abrechnung.",
        "Office, Excel ganz gut, unser Programm heißt Soloplan CarLo, damit mach ich alles. SAP leider nicht."]
s500 = "SAP kenne ich noch nicht, arbeite aber täglich mit einer Speditionssoftware und lerne neue Programme schnell."
d = h_profil(R500, formular=[{"feld": "Ihre Motivation (max. 1.000 Zeichen)", "text": s500}],
             herkunft=[{"satz": s500, "quellen": [{"nr": 7, "zitat": "SAP leider nicht"},
                                                  {"nr": 7, "zitat": "unser Programm heißt Soloplan CarLo, damit mach ich alles"}]}])
rc, o = fc(d, "h500.json")
check("v4 Transkript 500: „täglich … lerne neue Programme schnell“ mit Claudes Zitaten → ❌ mit den Wörtern",
      rc == 1 and "täglich" in herk_rot(o) and "lerne" in herk_rot(o) and "schnell" in herk_rot(o), o)
d["herkunft"] = []
rc, o = fc(d, "h500b.json")
check("v4 Transkript 500: derselbe Satz ganz ohne Quelle → ❌ „nicht schreiben, sondern fragen“", rc == 1 and "Satz ohne Quelle" in o, o)
s500e = "SAP kann ich noch nicht. Mit unserem Programm Soloplan CarLo mache ich alles."
d = h_profil(R500, formular=[{"feld": "Ihre Motivation (max. 1.000 Zeichen)", "text": s500e}],
             herkunft=[{"satz": "SAP kann ich noch nicht.", "nr": 2, "zitat": "SAP kann ich aber nicht"},
                       {"satz": "Mit unserem Programm Soloplan CarLo mache ich alles.", "nr": 7, "zitat": "unser Programm heißt Soloplan CarLo, damit mach ich alles"}])
rc, o = fc(d, "h500e.json")
check("v4 Transkript 500: ehrliche Fassung mit wörtlichem Zitat → 0 ❌", rc == 0 and not rot(o), o)

R530 = ["https://www.getraenke-ostler.example/jobs/aushilfe mach schnell bitte, bin am handy",
        "leon brandl blücherstr 41 86165 augsburg 0176 22918450 leon.brandl@gmail.com",
        "quali 2024 mittelschule hochzoll, dann ausbildung kfz mechatroniker bei autohaus wiedemann ab september 24, im februar abgebrochen",
        "ja", "hab gemerkt dass werkstatt nich mein ding is, will lieber ins lager oder so", "a dann halt",
        "in der ausbildung reifen gewechselt, räder eingelagert im reifenlager, ölwechsel. sonst nix",
        "führerschein b. stapler nein", "ja beides ab sofort. is 10 min mit dem rad. indeed"]
s530 = "In meiner Ausbildung im Autohaus habe ich Reifen gewechselt und Räder im Reifenlager eingelagert – schwer tragen bin ich gewohnt."
wa = f"Hallo Herr Ostler, ich bin Leon Brandl und möchte mich als Aushilfe in Ihrem Getränkemarkt bewerben. {s530} Meinen Lebenslauf schicke ich als PDF mit. Viele Grüße, Leon Brandl"
herk530 = [{"satz": s530, "quellen": [{"nr": 7, "zitat": "in der ausbildung reifen gewechselt, räder eingelagert im reifenlager"},
                                      {"nr": 3, "zitat": "autohaus wiedemann"}]}]
d = h_profil(R530, name="Leon Brandl", whatsapp=wa, herkunft=herk530)
d["ziel"].update({"stelle": "Aushilfe (m/w/d) Getränkemarkt – Minijob", "firma": "Getränke Ostler", "ansprechperson": "Herr Ostler"})
rc, o = fc(d, "h530.json")
check("v4 Transkript 530: „schwer tragen bin ich gewohnt“ (WhatsApp) → ❌ schwer/tragen/gewohnt",
      rc == 1 and all(w in herk_rot(o) for w in ("schwer", "tragen", "gewohnt")), o)
check("v4 Transkript 530: Begrüßungssatz mit Name/Stelle braucht keine Quelle", "Hallo Herr Ostler" not in herk_rot(o), o)
d["whatsapp"]["text"] = wa.replace(" – schwer tragen bin ich gewohnt", "")
d["herkunft"][0]["satz"] = s530.replace(" – schwer tragen bin ich gewohnt", "")
rc, o = fc(d, "h530e.json")
check("v4 Transkript 530: ehrliche WhatsApp-Nachricht → 0 ❌", rc == 0 and not rot(o), o)

R920 = ["link", "a", "screenshots", "a", "Nele Brandstätter, Söflinger Str. 88, 89077 Ulm, 0157 31948822, nele.brandstaetter@gmx.de",
        "abi 2024 gymnasium am eselsberg ulm 2,3", "ja", "fsj kita st martin neu-ulm 09/24-08/25. seit okt 25 radwerk ulm aushilfe 20h",
        "kita: gruppe mit 3-6 jährigen, ausflüge mitgeplant. radwerk: kasse, bestellungen im warenwirtschaftssystem, versand",
        "englisch b2, französisch bisschen, excel gut, word", "will praxis und geld verdienen, nicht nur uni. wirtschaft find ich spannend",
        "radwerk, seh wie bestellen lager preise zusammenhängen. das find ich spannend",
        "nah dran, und meine cousine hat da ausbildung gemacht, sagt gutes klima"]
s920 = "Dass Sie als Familienunternehmen Fördersysteme für Logistikzentren bauen, passt zu dem, was mich im Radwerk interessiert: wie Waren ankommen und weitergehen."
ff920 = [{"fakt": "Familienunternehmen, baut Fördersysteme für Logistikzentren", "quelle": "brandl-foerdertechnik.de", "zugestimmt": True}]
d = h_profil(R920, anschreiben=[s920], firmenfakten=ff920,
             herkunft=[{"satz": s920, "quellen": [{"firmenfakt": "Familienunternehmen, baut Fördersysteme für Logistikzentren"},
                                                  {"nr": 12, "zitat": "radwerk, seh wie bestellen lager preise zusammenhängen. das find ich spannend"}]}])
rc, o = fc(d, "h920.json")
check("v4 Transkript 920: „wie Waren ankommen und weitergehen“ → ❌ (ankommen/weitergehen nicht gesagt)",
      rc == 1 and "ankommen" in herk_rot(o) and "weitergehen" in herk_rot(o), o)
ff920[0]["zugestimmt"] = False
rc, o = fc(d, "h920b.json")
check("v4 Firmenfakt ohne Zustimmung als Quelle → ❌", "ohne Zustimmung" in o, o)
s920c = "Brandl ist für mich nah dran, und meine Cousine hat bei Ihnen ihre Ausbildung gemacht – sie sagt, das Klima ist gut."
d = h_profil(R920, anschreiben=[s920c], herkunft=[{"satz": s920c, "nr": 13, "zitat": "nah dran, und meine cousine hat da ausbildung gemacht, sagt gutes klima"}])
d["ziel"]["firma"] = "Brandl Fördertechnik GmbH"
rc, o = fc(d, "h920c.json")
check("v4 Familie („meine Cousine“) ohne ausdrückliche Zustimmung → ❌", rc == 1 and "Privates/Gesundheit/Familie" in o, o)
d["herkunft"][0]["privat_ok"] = True
rc, o = fc(d, "h920d.json")
check("v4 Familie mit privat_ok → kein ❌, im Anschreiben ⚠️ „im Regelfall weglassen“", rc == 0 and "im Regelfall weglassen" in o, o)

R941 = ["hallo ich möchte mich beim autohaus brandl in landshut für eine ausbildung bewerben. ich hab aber keine anzeige oder link, nur den namen von der ausbildungsmesse. geht das überhaupt?",
        "ja ich glaub a, die frau am stand meinte büro und autos verkaufen", "a",
        "Melis Karaca, Am Mühlbach 7, 84034 Landshut, 0157 31864420, melis.k2007@web.de",
        "realschule seligenthal bis 2024 mittlere reife 2,6, dann fos wirtschaft 2 jahre, fachabi diesen sommer 2,9",
        "x", "x", "x", "x", "x", "x",
        "die frau am stand war voll nett und hat gesagt ich soll mich unbedingt bewerben. und mein papa kauft da seit jahren seine autos, der kennt die"]
s941 = "Wir haben uns auf der Ausbildungsmesse an Ihrem Stand kennengelernt."
mail941 = f"Sehr geehrte Frau Brandl,\n\nanbei sende ich Ihnen meine Bewerbung um einen Ausbildungsplatz als Automobilkauffrau ab dem 01.09.2027. {s941}\n\nMit freundlichen Grüßen\nMelis Karaca"
d = h_profil(R941, name="Melis Karaca", email=mail941, herkunft=[{"satz": s941, "quellen": [{"nr": 1, "zitat": "nur den namen von der ausbildungsmesse"},
                                                                       {"nr": 12, "zitat": "die frau am stand war voll nett"}]}])
d["ziel"].update({"stelle": "Automobilkaufmann/-frau", "firma": "Autohaus Brandl GmbH", "ansprechperson": "Frau Sabine Brandl",
                  "anzeige_text": "Wir bilden aus: Automobilkaufmann/-frau – Start 01.09.2027. Führerschein B von Vorteil. Bewerbung per E-Mail an Frau Sabine Brandl."})
rc, o = fc(d, "h941.json")
check("v4 Transkript 941: „an Ihrem Stand kennengelernt“ (Annahme) → ❌ kennengelernt", rc == 1 and "kennengelernt" in herk_rot(o), o)
s941e = "Auf der Ausbildungsmesse hat mir die Frau an Ihrem Stand gesagt, ich soll mich unbedingt bewerben."
d["email"]["text"] = mail941.replace(s941, s941e)
d["herkunft"] = [{"satz": s941e, "quellen": [{"nr": 1, "zitat": "ausbildungsmesse"},
                                             {"nr": 12, "zitat": "die frau am stand war voll nett und hat gesagt ich soll mich unbedingt bewerben"}]}]
rc, o = fc(d, "h941e.json")
check("v4 Transkript 941: ehrliche Fassung aus ihren Worten → 0 ❌", rc == 0 and not rot(o), o)
sfs = "Den Führerschein Klasse B habe ich."
d["email"]["text"] = mail941.replace(s941, sfs)
d["herkunft"] = [{"satz": sfs, "quellen": [{"anzeige": "Führerschein B von Vorteil"}]}]
rc, o = fc(d, "h941f.json")
check("v4 Personen-Fakt nur aus der Anzeige (Führerschein) → ❌", rc == 1 and ("die Anzeige belegt nichts über dich" in o or "Führerschein" in "".join(rot(o))), o)

# weitere Herkunft-Regeln
d = h_profil(["x", "englisch b2 glaub ich, excel gut"], anschreiben=["Englisch spreche ich auf B2-Niveau."],
             herkunft=[{"satz": "Englisch spreche ich auf B2-Niveau.", "nr": 2, "zitat": "englisch b2"}])
rc, o = fc(d, "hunklar.json")
check("v4 unsichere Antwort („b2 glaub ich“) → ⚠️ erst bestätigen", "unsicher" in o and "Ja/Nein" in o, o)
d["profil"]["rohtext"][1]["geklaert"] = True
rc, o = fc(d, "hunklar2.json")
check("v4 unsichere Antwort nach Bestätigung (geklaert) → kein Hinweis", "unsicher" not in o and "unsichere Antwort" not in o, o)
d = h_profil(["x", "die abrechnung macht mir spaß"], anschreiben=["Die Abrechnung macht mir großen Spaß."],
             herkunft=[{"satz": "Die Abrechnung macht mir großen Spaß.", "nr": 2, "zitat": "die abrechnung macht mir richtig spaß"}])
rc, o = fc(d, "hnichtwoertlich.json")
check("v4 Zitat nicht wörtlich (umformuliert) → ❌", rc == 1 and "steht so in keiner Antwort" in o, o)
d["herkunft"][0]["zitat"] = "die abrechnung macht mir spaß"
d["herkunft"][0]["nr"] = 1
rc, o = fc(d, "hnr.json")
check("v4 falsche Antwort-Nr. → ⚠️ Nummer korrigieren, „großen“ → ❌", "Nummer korrigieren" in o and "großen" in herk_rot(o), o)
sk = "Wegen meines Knies kann ich nicht mehr in der Werkstatt arbeiten."
d = h_profil(["x", "wegen meinem knie geht werkstatt nicht mehr"], anschreiben=[sk],
             herkunft=[{"satz": sk, "nr": 2, "zitat": "wegen meinem knie geht werkstatt nicht mehr"}])
rc, o = fc(d, "hknie.json")
check("v4 Gesundheit („Knie“) ohne ausdrückliche Zustimmung → ❌", rc == 1 and "Privates/Gesundheit/Familie" in o, o)
open(f"{W}/up/Zeugnis_Text2.txt", "w", encoding="utf8").write("Abschlusszeugnis. Mathematik: sehr gut (1). Deutsch: gut (2).")
sz = "In Mathematik hatte ich eine 1."
d = h_profil(["x"], anschreiben=[sz], herkunft=[{"satz": sz, "quellen": [{"upload": "Mathematik: sehr gut (1)"}]}])
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_Text2.txt", "bezeichnung": "Abschlusszeugnis"}]
rc, o = fc(d, "hzeug.json")
check("v4 Zeugnis als Text-Upload belegt die Note (upload-Zitat) → 0 ❌", rc == 0, o)
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis (Foto)"}]
rc, o = fc(d, "hzeug2.json")
check("v4 Zeugnis nur als Foto → Inhalt erst bestätigen lassen (❌)", rc == 1 and "erst beim Nutzer bestätigen" in o, o)
rc, o = run(f"{S}/herkunft.py", speichern(beispiel(), "hcli.json"))
check("v5 herkunft.py CLI: Beispiel 0 ❌ + Woher-Liste „Satzanfang → deine Worte“ ohne Nr.", rc == 0 and "→ deine Worte:" in o and "(Nr." not in o, o)
rc, o = run(f"{S}/fakten_check.py", speichern(beispiel(), "hwoher.json"), "--woher")
wl = [z for z in o.split("---")[0].splitlines() if z.startswith(("–", "❓"))]
check("v4 Woher-Liste kompakt: eine Zeile je Satz, Satzanfang ≤ 5 Wörter", wl and all(len(z.split("“")[0].split()) <= 7 for z in wl), wl)

# ================================================================ 13 v4 Normalisierungs-Wörterbuch: ehrliche Texte → 0 ❌ ohne belege
N = beispiel()
N["person"].update({"name": "Leon Brandl", "strasse": "Blücherstraße 41", "plz_ort": "86165 Augsburg", "telefon": "0176 22918450",
                    "email": "leon.brandl@gmail.com"})
N["profil"]["rohtext"] = [{"nr": i + 1, "frage": f"Frage {i + 1}", "antwort": a} for i, a in enumerate([
    "leon brandl blücherstr 41 86165 augsburg 0176 22918450 leon.brandl@gmail.com",
    "ABI 2024 am gym bei st. stephan augsburg, lk bio und mathe",
    "fsj kita st martin 09/24-08/25. seit okt 25 aushilfe im radwerk 15h die woche",
    "praktikum märz bis august 24 bei der stadt augsburg, akten sortiert",
    "nachhilfe in mathe seit febuar 2026",
    "englisch b2, excel gut",
    "kann ab januar anfangen",
    "gehalt so 29-31k",
    "mein papa ist kfz mechatroniker, da hab ich oft in der werkstatt geholfen",
    "zwei kinder, 4 und 7",
    "studium 31. august 2027 fertig, B.A. soziale arbeit",
    "maschinenbau th augsburg 10/2023 bis 09/2025, 4 semester",
    "indeed", "zfa ausbildung april 25 abgebrochen januar 26"])]
N["profil"]["anlagen"], N["profil"]["beispiele"], N["profil"]["hobbys"] = [], [], []
N["profil"]["wie_aufmerksam"] = "Indeed"
N["lebenslauf"] = {"kurzprofil": "", "abschnitte": [
    {"titel": "Praktische Erfahrung", "eintraege": [
        {"zeitraum": "seit 10/2025", "titel": "Aushilfe (15 Std./Woche)", "ort": "Radwerk", "punkte": []},
        {"zeitraum": "09/2024 – 08/2025", "titel": "Freiwilliges Soziales Jahr", "ort": "Kita St. Martin", "punkte": []},
        {"zeitraum": "04/2025 – 01/2026", "titel": "Ausbildung zur Zahnmedizinischen Fachangestellten (abgebrochen)", "ort": "", "punkte": []},
        {"zeitraum": "03/2024 – 08/2024", "titel": "Praktikum", "ort": "Stadt Augsburg", "punkte": ["Akten sortiert"]},
        {"zeitraum": "seit 02/2026", "titel": "Nachhilfe in Mathematik", "ort": "", "punkte": []}]},
    {"titel": "Schulbildung", "eintraege": [
        {"zeitraum": "2024", "titel": "ALLGEMEINE HOCHSCHULREIFE", "ort": "Gymnasium bei St. Stephan, Augsburg",
         "punkte": ["Leistungskurse Biologie und Mathematik"]},
        {"zeitraum": "10/2023 – 09/2025", "titel": "Maschinenbau (4 Semester)", "ort": "Technische Hochschule Augsburg", "punkte": []},
        {"zeitraum": "voraussichtlich 31.08.2027", "titel": "Bachelor of Arts Soziale Arbeit", "ort": "", "punkte": []}]},
    {"titel": "Familienzeit", "eintraege": [{"zeitraum": "", "titel": "Zwei Kinder (4 und 7 Jahre alt)", "ort": "", "punkte": []}]}],
    "kenntnisse": [{"label": "Sprachen", "wert": "Englisch (B2)"}, {"label": "Weitere Kenntnisse", "wert": "Excel"},
                   {"label": "Zertifikate", "wert": "keine"}, {"label": "Sonstiges", "wert": "Werkstatt-Erfahrung"}],
    "interessen": "", "ort_datum_unterschrift": False}
a1 = "Mein Vater ist Kfz-Mechatroniker, und ich habe oft in der Werkstatt geholfen. Ihr Haus erreiche ich mit dem Rad in 10 Minuten."
a2 = "Nach 4 Semestern Maschinenbau weiß ich, dass ich praktischer arbeiten will."
N["anschreiben"]["absaetze"] = [a1, a2, "Ich freue mich auf ein persönliches Gespräch."]
N["herkunft"] = [{"satz": "Mein Vater ist Kfz-Mechatroniker, und ich habe oft in der Werkstatt geholfen.", "privat_ok": True, "nr": 9,
                  "zitat": "mein papa ist kfz mechatroniker, da hab ich oft in der werkstatt geholfen"},
                 {"satz": "Ihr Haus erreiche ich mit dem Rad in 10 Minuten.", "nr": 16, "zitat": "10 min mit dem rad"},
                 {"satz": a2, "quellen": [{"nr": 12, "zitat": "maschinenbau th augsburg 10/2023 bis 09/2025, 4 semester"}]}]
N["profil"]["rohtext"].append({"nr": 15, "frage": "Warum?", "antwort": "weiß jetzt dass ich praktischer arbeiten will"})
N["profil"]["rohtext"].append({"nr": 16, "frage": "Warum wir?", "antwort": "10 min mit dem rad"})
N["herkunft"][2]["quellen"].append({"nr": 15, "zitat": "weiß jetzt dass ich praktischer arbeiten will"})
N["formular"] = [{"feld": "Frühester Eintritt", "limit": 50, "text": "ab Januar 2027"},
                 {"feld": "Gehaltsvorstellung", "limit": 100, "text": "29.000 – 31.000 EUR brutto im Jahr"},
                 {"feld": "Wie sind Sie auf uns aufmerksam geworden?", "limit": 100, "text": "Über Indeed."}]
N["email"] = {"betreff": "", "text": ""}
N["ziel"]["anzeige_text"] = "Ausbildung bei der Beispiel GmbH."
rc, o = fc(N, "norm.json")
check("v4 Normalisierungen (abi/ABI GROSS, gym, lk bio, fsj, 09/24, okt 25, 15h, märz bis august 24, febuar, ab januar, "
      "29-31k, papa, B.A., 31. august 2027, zfa, april 25/januar 26, Kinderalter, Kenntnis-Labels, „Ihr Haus“, "
      "Satzpunkt, Studiendauer statt Minijob) → 0 ❌ ohne belege", rc == 0 and not rot(o) and N["belege"] == [], o)
check("v4 Normalisierungen: keine Dauer-Warnung „gerundet“ gegen fremden Zeitraum", "gerundet" not in o and "berechnet" not in o, o)
open(f"{W}/norm_brief.txt", "w", encoding="utf8").write(
    "Leon Brandl | Blücherstraße 41 | 86165 Augsburg\nAugsburg, 09.11.2026\nSehr geehrte Damen und Herren,\n" + a1 + "\n"
    "Mit freundlichen Grüßen\nLeon Brandl\n\nAnlagen: Lebenslauf, Zeugnis der\n10. Klasse, Praktikumszeugnis\n")
rc, o = run(f"{S}/fakten_check.py", speichern(N, "norm2.json"), f"{W}/norm_brief.txt")
check("v4 Datei: Straße/str., Briefdatum an späterem Tag, umbrochene Anlagen-Zeile → kein ❌",
      not [z for z in rot(o) if "norm_brief" in z and "Abgleich" not in z], o)
d = copy.deepcopy(N); d["formular"][1]["text"] = "29.000 – 35.000 EUR brutto im Jahr"
rc, o = fc(d, "norm3.json")
check("v4 Normalisierung bleibt streng: 35.000 statt 31k → ❌", rc == 1 and "35.000" in o, o)
d = copy.deepcopy(N); d["lebenslauf"]["kenntnisse"][0]["wert"] = "Englisch (C1)"
rc, o = fc(d, "norm4.json")
check("v4 Normalisierung bleibt streng: C1 statt b2 → ❌", rc == 1 and "C1" in o, o)
d = copy.deepcopy(N); d["formular"][0]["text"] = "01.01.2027"
rc, o = fc(d, "norm5.json")
check("v4 „ab januar“ → „01.01.2027“ (Tag erfunden) → ❌", rc == 1 and "01.01.2027" in o, o)
d = copy.deepcopy(N); d["lebenslauf"]["abschnitte"][1]["eintraege"][0]["zeitraum"] = "06/2024"
rc, o = fc(d, "norm6.json")
check("v4 Lebenslauf: Monat nur aus der Anzeige zählt nicht (nur Wortlaut)", rc == 1 and "06/2024" in o, o)
d = copy.deepcopy(N); d["formular"][0]["text"] = "ab Januar 2027 [PRÜFEN: Tag?]"
rc, o = fc(d, "norm7.json")
check("v4 Zähler „offene [PRÜFEN]“ zählt wirklich", "1 offene [PRÜFEN]" in o, o)
check("Wörterbuch: Rückrichtung automatisch (Fachhochschulreife → fachabi)", "fachabi" in textlib.normalisiere_nutzertext("Fachhochschulreife 2022").lower())
check("Wörterbuch: Monats-Tippfehler „febuar“ → februar", "februar" in textlib.normalisiere_nutzertext("seit febuar 2026"))

# ================================================================ 14 v4 Spickzettel
SP = beispiel()
SP["meta"]["anrede_form"] = "sie"
SP["profil"]["rohtext"] += [{"nr": 12, "frage": "Über sich", "antwort": "Mittlere Reife 07/2026, seit 09/2025 Kasse, will Zahlen und Kunden"},
                            {"nr": 14, "frage": "Schwäche?", "antwort": "fehler will ich nicht, darum prüf ich lieber zweimal"},
                            {"nr": 13, "frage": "Fachfrage Skonto", "antwort": "skonto ist ein rabatt wenn man schnell zahlt, meist 2 prozent"}]
SP["gespraech"].update({
    "termin": "20.01.2027, 9:00 Uhr", "art": "Assessment Center", "ort": "Industriestraße 4, Ingolstadt", "anrede": "sie",
    "einladung_text": "Wir laden Sie zum Auswahltag am 20.01.2027 um 9 Uhr in die Industriestraße 4 ein. Ablauf: Selbstpräsentation "
                      "(5 Minuten), Gruppenaufgabe, Kurzpräsentation zu einem Fachthema, Einzelinterview. Bitte bringen Sie Ihren Personalausweis mit.",
    "mitbringen": ["Personalausweis"],
    "kernbotschaften": ["1. Seit 09/2025 mache ich an der Kasse die Abrechnung selbst", "2. Mittlere Reife 07/2026", "3. Ab 01.09.2027 kann ich anfangen"],
    "vorstellung": {"kernpunkte": ["Mittlere Reife 07/2026 an der Realschule Beispiel", "Seit 09/2025 Minijob an der Kasse"]},
    "schwierige_fragen": [{"frage": "Was ist Ihre Schwäche?", "antwort_final": "Ich schließe Zahlen gern ohne Fehler ab – darum prüfe ich lieber zweimal."},
                          {"frage": "Gruppendiskussion", "antwort_final": "Coaching: mehr zusammenfassen (Feedback: zu still)"}],
    "fachfragen": [{"frage": "Was ist Skonto?", "antwort_final": "Ein Rabatt, wenn man schnell zahlt, meist 2 Prozent."}],
    "gehalt": {"antwort_final": "[PRÜFEN: Spanne mit Quelle]"},
    "feedback": [{"frage": "Selbstpräsentation", "besser": "Er soll mehr Blickkontakt halten"}],
    "ac_uebungen": [{"typ": "", "titel": "Selbstpräsentation"}, "Gruppenaufgabe", "Kurzpräsentation zu einem Fachthema", "Einzelinterview"],
    "eigene_fragen": [{"frage": "Wie läuft die Einarbeitung?", "gewaehlt": True}]})
Psp = speichern(SP, "sp4.json")
rc, o = run(f"{S}/akte.py", Psp, "--spickzettel", "--pdf", "--ausgabe", f"{W}/sp4")
sp4 = open(f"{W}/sp4/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("v4 Spickzettel: Vorstellungsdauer aus der Einladung (5 Minuten), nicht fest 1–2", "(5 MINUTEN)" in sp4 and "1–2" not in sp4, sp4)
check("v4 Spickzettel: Sie-Form durchgehend", "SO STELLEN SIE SICH VOR" in sp4 and "IHRE 3 KERNBOTSCHAFTEN" in sp4
      and "TIPPS FÜR IHREN AUSWAHLTAG" in sp4 and not re.search(r"\b(du|dein\w*|dich|dir)\b", sp4, re.I), sp4)
zl = {z.split(":")[0].strip("• "): z for z in sp4.splitlines() if z.startswith("• ") and ":" in z}
check("v4 AC: Selbstpräsentation bekommt Vorstellungs-Tipp (nicht Fallstudie)", "heute → Weg" in zl.get("Selbstpräsentation (5 Min.)", "")
      and "Problem → Ursachen" not in zl.get("Selbstpräsentation (5 Min.)", ""), zl)
check("v4 AC: Gruppenaufgabe bekommt Gruppen-Tipp", "andere einbeziehen" in zl.get("Gruppenaufgabe", ""), zl)
check("v4 AC: Fach-Präsentation bekommt Präsentations-Tipp", "Kernaussage zuerst" in zl.get("Kurzpräsentation zu einem Fachthema", ""), zl)
check("v4 Spickzettel: Feedback/Coaching-Notizen nicht als schwierige Frage", "Coaching" not in sp4 and "Blickkontakt halten" not in sp4
      and "• Gruppendiskussion" not in sp4, sp4)
check("v4 Spickzettel: Fachfragen-Abschnitt", "FACHFRAGEN – IHRE ANTWORT" in sp4 and "Skonto" in sp4, sp4)
check("v4 Spickzettel: Gehaltsfrage offen wird angezeigt, nicht still weggelassen", "Gehaltsvorstellung" in sp4 and "noch offen" in sp4
      and "Gehaltsvorstellung" in o, f"{sp4}\n{o}")
rc2, o2 = run(f"{S}/fakten_check.py", Psp, "--typ", "spickzettel")
check("v4 fakten_check Spickzettel: eigene Nummerierung „1.“/Übungen → kein Fehlalarm (0 ❌)", rc2 == 0 and not rot(o2), o2)
rc2, o2 = run(f"{S}/fakten_check.py", Psp, "--typ", "spickzettel", f"{W}/sp4/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt")
check("v4 fakten_check Spickzettel-Datei → 0 ❌", rc2 == 0 and not rot(o2), o2)
pdf4 = f"{W}/sp4/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.pdf"
r4 = pypdf.PdfReader(pdf4)
mb = r4.pages[0].mediabox
check("v4 Spickzettel-PDF kompakt (A5, handytauglich)", abs(float(mb.width) - 419.5) < 3 and abs(float(mb.height) - 595.3) < 3, mb)
letzte = [z for z in (r4.pages[-1].extract_text() or "").splitlines() if z.strip()]
check("v4 Spickzettel-PDF: keine fast leere letzte Seite", len(r4.pages) == 1 or len(letzte) >= 6, f"{len(r4.pages)} Seiten, letzte {len(letzte)} Zeilen")
subprocess.run(["pdftoppm", "-r", "70", "-png", pdf4, f"{W}/sp4_bild"])
# Grammatik du-Form + 5-Minuten bei normalem Gespräch
d = beispiel()
d["gespraech"].update({"termin": "12.11.2026, 10:00 Uhr", "art": "vor Ort", "ort": "Hauptstraße 5",
                       "einladung_text": "Wir laden dich am 12.11.2026 um 10 Uhr ein. Bitte bereite eine kurze Vorstellung deiner Person (ca. 5 Minuten) vor.",
                       "vorstellung": {"kernpunkte": ["Seit 09/2025 Minijob an der Kasse"]}})
run(f"{S}/akte.py", speichern(d, "sp5.json"), "--spickzettel", "--ausgabe", f"{W}/sp5")
sp5 = open(f"{W}/sp5/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("v4 Spickzettel du-Form: „So stellst du dich vor (5 Minuten)“, „Tipps für dein Gespräch“", "SO STELLST DU DICH VOR (5 MINUTEN)" in sp5
      and "TIPPS FÜR DEIN GESPRÄCH" in sp5, sp5)
# v3-Daten (Strings) weiter lesbar: „Kurzpräsentation ‚Warum ich?‘“ = Selbstpräsentation
d = beispiel()
d["gespraech"].update({"art": "Auswahltag", "einladung_text": "Kurzpräsentation „Warum ich?“ (3 Min.), Gruppenaufgabe",
                       "ac_uebungen": ["Kurzpräsentation „Warum ich?“", "Gruppenaufgabe", "Fallstudie"]})
run(f"{S}/akte.py", speichern(d, "sp6.json"), "--spickzettel", "--ausgabe", f"{W}/sp6")
sp6 = open(f"{W}/sp6/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
z6 = [z for z in sp6.splitlines() if "Warum ich" in z]
check("v4 Transkript 227/233: „Kurzpräsentation ‚Warum ich?‘“ → Selbstpräsentations-Tipp, 3 Min.", z6 and "heute → Weg" in z6[0]
      and "Problem → Ursachen" not in z6[0] and "3 Min" in z6[0], sp6)
check("v4 Fallstudie behält Fallstudien-Tipp", "Fallstudie: Problem → Ursachen" in sp6, sp6)
# Probearbeiten: Ort aus der Einladung fehlt → Hinweis an Claude (Transkript 319)
d = beispiel()
d["gespraech"].update({"art": "Probearbeiten", "termin": "Sa 14.11., 13 Uhr", "ort": "Bäckerei-Café Stadler, Rosenheim",
                       "einladung_text": "Komm gern am Samstag, 14.11., um 13 Uhr zum Probearbeiten bei uns in der Filiale am Ludwigsplatz vorbei."})
rc, o = run(f"{S}/akte.py", speichern(d, "sp7.json"), "--spickzettel", "--ausgabe", f"{W}/sp7")
check("v4 Transkript 319: Ort laut Einladung fehlt im Spickzettel → Hinweis", "Ludwigsplatz" in o and "gespraech.ort" in o, o)
sp7 = open(f"{W}/sp7/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("v4 Probearbeiten-Spickzettel: Tipps fürs Probearbeiten inkl. Bezahlung klären", "TIPPS FÜR DEIN PROBEARBEITEN" in sp7 and "bezahlt" in sp7, sp7)

# ================================================================ 15 v4 Datei-Fixes
# Bündeln: Motivationsschreiben heißt so
d = beispiel(); d["anschreiben"]["typ"] = "motivationsschreiben"
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
Pm = speichern(d, "mot4.json")
run(f"{S}/unterlagen_erstellen.py", Pm, "--ausgabe", f"{W}/out_m4", "--nur-pdf")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--buendeln", "3", "--profil", Pm, "--ordner", f"{W}/out_m4", "--ausgabe", f"{W}/out_m4b")
check("v4 --buendeln 3: Motivationsschreiben heißt „Motivationsschreiben_…“", rc == 0 and "Motivationsschreiben_Lena_Muster.pdf" in os.listdir(f"{W}/out_m4b")
      and not any(f.startswith("Anschreiben") for f in os.listdir(f"{W}/out_m4b")), f"{os.listdir(W + '/out_m4b')} {o}")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--buendeln", "2", "--profil", Pm, "--ordner", f"{W}/out_m4", "--ausgabe", f"{W}/out_m4c")
check("v4 --buendeln 2: „Motivationsschreiben_und_Anlagen_…“", rc == 0 and "Motivationsschreiben_und_Anlagen_Lena_Muster.pdf" in os.listdir(f"{W}/out_m4c"), o)
# Quellen in anderem Ordner als --ausgabe (Standardordner)
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--buendeln", "3", "--profil", Pm, "--ausgabe", f"{W}/out_m4d", env={"BP_AUSGABE": f"{W}/out_m4"})
check("v4 --buendeln mit --ausgabe woanders: Quellen im Standardordner gefunden", rc == 0 and len(os.listdir(f"{W}/out_m4d")) == 3, o)
# --einzeln im selben Ordner: keine zweite Kopie neben _AKTUELL
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--einzeln", "--profil", Pm, "--ausgabe", f"{W}/out_m4")
fl = sorted(f for f in os.listdir(f"{W}/out_m4") if f.endswith(".pdf"))
check("v4 --einzeln: je Unterlage nur EINE PDF im Ordner (AKTUELL → alt/)", rc == 0 and "Lebenslauf_Lena_Muster.pdf" in fl
      and not any("_AKTUELL" in f for f in fl) and any("Lebenslauf_Lena_Muster_v" in f for f in os.listdir(f"{W}/out_m4/alt")), f"{fl}\n{o}")
run(f"{S}/unterlagen_erstellen.py", Pm, "--ausgabe", f"{W}/out_m4", "--nur", "lebenslauf", "--nur-pdf")
fl = sorted(f for f in os.listdir(f"{W}/out_m4") if f.startswith("Lebenslauf"))
check("v4 neue Lebenslauf-Fassung: alte Upload-Kopie wandert nach alt/ (keine zwei Lebensläufe)", fl == ["Lebenslauf_Lena_Muster_AKTUELL.pdf"], fl)
# Dateiname nicht mitten im Sinn abgeschnitten
check("v4 safe_name endet nie auf „fuer“", not textlib.safe_name("IHK-Prüfungszeugnis Kauffrau für Bürokommunikation", 34).endswith("fuer"),
      textlib.safe_name("IHK-Prüfungszeugnis Kauffrau für Bürokommunikation", 34))
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--einzeln", f"{W}/up/IMG_4471.jpg", "--name", "IMG_4471.jpg=IHK-Prüfungszeugnis Kauffrau für Bürokommunikation", "--ausgabe", f"{W}/out_lang")
check("v4 --einzeln: langer Name vollständig (Transkript 500)", "IHK_Pruefungszeugnis_Kauffrau_fuer_Buerokommunikation.pdf" in os.listdir(f"{W}/out_lang"), os.listdir(f"{W}/out_lang"))
# Tausenderpunkt im Feldnamen
d = beispiel(); d["formular"][0]["feld"] = "Ihre Motivation (max. 1.000 Zeichen)"
run(f"{S}/unterlagen_erstellen.py", speichern(d, "tsd.json"), "--ausgabe", f"{W}/out_tsd", "--nur", "formular")
ft = open(f"{W}/out_tsd/Formular-Texte_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("v4 Zeichengrenze „max. 1.000“ nicht doppelt", "=== Ihre Motivation (max. 1.000 Zeichen) ===" in ft and ft.count("1.000") == 1
      and "max. 1000" not in ft, ft[:200])
open(f"{W}/Formular_t.txt", "w", encoding="utf8").write("=== Motivation (max. 1.000 Zeichen) ===\n" + "x" * 1100 + "\n")
rc, o = run(f"{S}/endcheck.py", f"{W}/Formular_t.txt", "--typ", "formular")
check("v4 endcheck liest „max. 1.000 Zeichen“", "erlaubt 1.000" in o, o)
# Kennziffer im Betreff nicht umbrechen
d = beispiel(); d["ziel"]["kennziffer"] = "DS-BWL-2027-03"
d["anschreiben"]["betreff"] = "Bewerbung für das Duale Studium BWL – Industrie (B.A.) 2027 mit Start am 01.10.2027, Kennziffer DS-BWL-2027-03"
run(f"{S}/unterlagen_erstellen.py", speichern(d, "kz.json"), "--ausgabe", f"{W}/out_kz", "--nur", "anschreiben")
dx = zipfile.ZipFile(f"{W}/out_kz/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.docx").read("word/document.xml").decode()
check("v4 Kennziffer mit geschütztem Bindestrich (w:noBreakHyphen)", dx.count("<w:noBreakHyphen/>") == 3, dx.count("noBreakHyphen"))
kz_txt = subprocess.run(["pdftotext", "-layout", f"{W}/out_kz/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf", "-"], capture_output=True, text=True).stdout
check("v4 Kennziffer im PDF auf einer Zeile", re.search(r"DS.BWL.2027.03", kz_txt), kz_txt[:900])
subprocess.run(["pdftoppm", "-r", "70", "-png", "-f", "1", "-l", "1", f"{W}/out_kz/Anschreiben_Lena_Muster_Beispiel-GmbH_AKTUELL.pdf", f"{W}/kz_bild"])
open(f"{W}/st.txt", "w", encoding="utf8").write("Sehr geehrte Frau Rauch,\nBewerbung für das Duale Studium BWL – Industrie (B.A.) bei Brandl.\nMit freundlichen Grüßen\nNele")
rc, o = run(f"{S}/endcheck.py", f"{W}/st.txt", "--typ", "anschreiben", "--firma", "Brandl Fördertechnik GmbH", "--stelle", "Duales Studium BWL – Industrie (B.A.) Start 2027 (m/w/d)")
check("v4 endcheck: „Start“/Jahr im Stellentitel muss nicht in den Betreff", "start" not in o.lower() and "Stellenbezeichnung" not in o, o)
# Akte: Reupload-Liste ohne Duplikate, Lücke mit „grund“, Station ohne Doppelklammer
d = beispiel()
d["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
d["profil"]["quellen"] = [f"{W}/up/Zeugnis_10.jpg"]
d["profil"]["luecken"] = [{"zeitraum": "08/2024 – 02/2025", "grund": "Ausbildungsplatz gesucht"}]
d["profil"]["stationen"][0].update({"titel": "Aushilfe", "art": "Aushilfe (20 Std./Woche)"})
rc, o = run(f"{S}/akte.py", speichern(d, "ak4.json"), "--ausgabe", f"{W}/ak4")
ak4 = open(f"{W}/ak4/" + [f for f in os.listdir(f"{W}/ak4") if f.endswith(".txt")][0], encoding="utf8").read()
lesbar4 = ak4.split(textlib.AKTE_START)[0]
check("v4 Akte: Reupload-Liste ohne Duplikate", lesbar4.count("Zeugnis_10.jpg") == 1 and o.count("Zeugnis_10.jpg") == 1, lesbar4[:500] + o)
check("v4 Akte: Lücke mit „grund“ statt „erklaerung“ wird angezeigt", "Lücke: 08/2024 – 02/2025 – Ausbildungsplatz gesucht" in lesbar4, lesbar4)
check("v4 Akte: keine Doppelklammer „Aushilfe (Aushilfe (…))“", "Aushilfe (Aushilfe" not in lesbar4 and "Aushilfe (20 Std./Woche)" in lesbar4, lesbar4)
# akte --lesen: umbenannte Akte „Bewerbungsakte (1).txt“ und Re-Upload „image(1).jpg“ (gleicher Inhalt)
os.makedirs(f"{W}/up_neu")
Image.new("RGB", (800, 1100), (200, 180, 160)).save(f"{W}/up/IMG_2041.jpg")
d = beispiel(); d["profil"]["anlagen"] = [{"datei": f"{W}/up/IMG_2041.jpg", "bezeichnung": "Zeugnis FOS"}]
run(f"{S}/akte.py", speichern(d, "ak5.json"), "--ausgabe", f"{W}/ak5")
akte5 = [f for f in os.listdir(f"{W}/ak5") if f.endswith(".txt")][0]
shutil.copy(f"{W}/ak5/{akte5}", f"{W}/up_neu/Bewerbungsakte (1).txt")
shutil.copy(f"{W}/up/IMG_2041.jpg", f"{W}/up_neu/image(1).jpg")
os.remove(f"{W}/up/IMG_2041.jpg")
rc, o = run(f"{S}/akte.py", "--lesen", f"{W}/up_neu/Bewerbungsakte_gibts_nicht.txt", "--json-nach", f"{W}/fort5/profil.json", env={"BP_UPLOADS": f"{W}/up_neu"})
d5 = json.load(open(f"{W}/fort5/profil.json")) if rc == 0 else {}
check("v4 akte --lesen: umbenannte Akte „Bewerbungsakte (1).txt“ gefunden", rc == 0 and "Bewerbungsakte (1).txt" in o, o)
check("v4 akte --lesen: Zeugnis als „image(1).jpg“ (gleicher Inhalt) zugeordnet", rc == 0 and d5["profil"]["anlagen"][0]["datei"].endswith("image(1).jpg")
      and "noch einmal hochladen" not in o, o)
# WhatsApp als eigener Typ
d = beispiel(); d["whatsapp"] = {"text": "Hallo Frau Sommer, ich bin Lena Muster und bewerbe mich um den Ausbildungsplatz als Kauffrau für Büromanagement. Meinen Lebenslauf schicke ich als PDF mit. Viele Grüße, Lena Muster"}
Pw = speichern(d, "wa.json")
rc, o = run(f"{S}/unterlagen_erstellen.py", Pw, "--ausgabe", f"{W}/out_wa", "--nur", "whatsapp")
check("v4 WhatsApp-Text als eigener Typ (WhatsApp-Text_…_AKTUELL.txt, kein Feldtitel)", rc == 0 and os.listdir(f"{W}/out_wa") == ["WhatsApp-Text_Beispiel-GmbH_AKTUELL.txt"]
      and "===" not in open(f"{W}/out_wa/WhatsApp-Text_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read(), f"{os.listdir(W + '/out_wa')} {o}")
rc, o = run(f"{S}/endcheck.py", f"{W}/out_wa/WhatsApp-Text_Beispiel-GmbH_AKTUELL.txt", "--typ", "whatsapp", "--profil", Pw)
check("v4 endcheck --typ whatsapp: kurze ehrliche Nachricht → 0 ❌, keine Firma/Stelle verlangt", rc == 0 and "kommt nicht vor" not in o and "Stellenbezeichnung" not in o, o)
rc, o = run(f"{S}/fakten_check.py", Pw)
check("v4 fakten_check prüft WhatsApp-Text mit (neutraler Text → 0 ❌)", rc == 0, o)
# Lebenslauf-PDF als Bild (für die Sichtprüfung)
subprocess.run(["pdftoppm", "-r", "70", "-png", "-f", "1", "-l", "1", LL, f"{W}/ll_bild"])
check("Lebenslauf- und Spickzettel-PNG für die Sichtprüfung erzeugt", any(f.startswith("ll_bild") for f in os.listdir(W))
      and any(f.startswith("sp4_bild") for f in os.listdir(W)), os.listdir(W))

# ================================================================ 16 v5: Fakten wörtlich, Formulierung frei
sys.path.insert(0, "/tmp/bp_test5/fixtures")
import v5_faelle as V5  # noqa: E402
import sprachlib  # noqa: E402
up976 = f"{W}/up/Arbeitszeugnis_Weigl.txt"
open(up976, "w", encoding="utf8").write(V5.F976["upload"])
# 16a: 7 Transkript-Fälle (umgangssprachlicher Wortlaut → professionelles Anschreiben) – je EIN Lauf, 0 ❌
for k, f in V5.EHRLICH.items():
    d = V5.profil(f, beispiel(), up976 if "upload" in f else None)
    rc, o = fc(d, f"v5_ehrlich_{k}.json", "--woher")
    check(f"v5 Transkript {k}: professionelles Anschreiben aus Umgangssprache → 0 ❌ in einem Lauf", rc == 0 and not rot(o), o)
    check(f"v5 Transkript {k}: Woher-Liste ohne interne Nummern", "(Nr." not in o.split("# Fakten-Check")[0]
          and ("Ihre Worte" if f.get("anrede_form") == "sie" else "deine Worte") in o, o[:600])
    check(f"v5 Transkript {k}: kein Stil-⚠️ im professionellen Text", "Stil" not in o, [z for z in o.splitlines() if "Stil" in z])
# Anschreiben aus Fall 158 als PDF: endcheck ohne Stil-Befund, Seite als Bild
d158 = V5.profil(V5.F158, beispiel())
d158["person"].update({"strasse": "Lindenweg 7", "plz_ort": "86356 Neusäß", "telefon": "0171 5583920", "email": "dennis.hartl87@gmx.de"})
P158 = speichern(d158, "v5_158_datei.json")
rc, o = run(f"{S}/unterlagen_erstellen.py", P158, "--ausgabe", f"{W}/out_v5", "--nur", "anschreiben")
AN158 = f"{W}/out_v5/" + [f for f in os.listdir(f"{W}/out_v5") if f.startswith("Anschreiben") and f.endswith(".pdf")][0]
rc, o = run(f"{S}/fakten_check.py", P158, AN158)
check("v5 Fall 158 als PDF: fakten_check mit Datei → 0 ❌ (Abgleich ok)", rc == 0 and not rot(o), o)
rc, o = run(f"{S}/endcheck.py", AN158, "--typ", "anschreiben", "--profil", P158)
check("v5 Fall 158 als PDF: endcheck 0 ❌, kein Stil-⚠️, 1 Seite", rc == 0 and "Stil:" not in o and "Seitenzahl: 1" in o, o)
subprocess.run(["pdftoppm", "-r", "60", "-png", "-f", "1", "-l", "1", AN158, f"{W}/v5_an158_bild"])

# 16b: Erfindungen aus allen vier Fehlerlisten werden gefunden
for i, (name, basis, satz, herk, erwartet) in enumerate(V5.ERFUNDEN):
    f = V5.EHRLICH[basis]
    d = V5.profil(f, beispiel(), up976 if "upload" in f else None)
    d["anschreiben"]["absaetze"].insert(1, satz)
    if herk:
        d["herkunft"].append(herk)
    rc, o = fc(d, f"v5_erf_{i}.json")
    check(f"v5 Erfindung erkannt: {name}", rc == 1 and all(any(e in z for z in rot(o)) for e in erwartet), "\n".join(rot(o)) or o)
check("v5 mind. 10 Erfindungs- und 6 Umgangssprache-Fälle", len(V5.ERFUNDEN) >= 10 and len(V5.EHRLICH) >= 6, "")

# 16c: Bausteine – Lemma, Partizip, trennbare Verben, Zahlwörter, Daten, Wörterbuch, Tippfehler
Q = sprachlib.Quelle(["azubis einarbeiten hat spaß gemacht, kommisioniert, sag dem chef bescheid, 15 min mit der ubahn, "
                      "ab 1.2.27, jetzt 5. semester, schichtleitung, er hat angerufen"])
for w in ("eingearbeitet", "Auszubildende", "kommissioniert", "informiere", "U-Bahn", "geleitet"):
    check(f"v5 Deckung: „{w}“ aus dem Wortlaut erkannt", sprachlib.gedeckt(w, Q), w)
for w in ("Kollegen", "täglich", "begeistert", "verhandelt", "Klasse"):
    check(f"v5 Deckung: „{w}“ ist NICHT gedeckt", not sprachlib.gedeckt(w, Q), w)
check("v5 Zahlwort „fünften“ ↔ „5.“", sprachlib.zahl_gedeckt("fünften", Q) == "ja" and sprachlib.zahl_gedeckt("siebten", Q) == "nein")
check("v5 Datum „01.02.2027“ ↔ „1.2.27“", sprachlib.zahl_gedeckt("01.02.2027", Q) == "ja" and sprachlib.zahl_gedeckt("01.03.2027", Q) == "nein")
check("v5 Umgangssprache-Wörterbuch ≥ 60 Einträge (red, seh, find, hab, nix, was, ubahn, sa, so, kumpel, mega, cool, bissl, kfz, azubi)",
      len(sprachlib.UMGANGSSPRACHE) >= 60 and all(k in sprachlib.UMGANGSSPRACHE for k in
      ("red", "seh", "find", "hab", "nix", "was", "ubahn", "sa", "so", "kumpel", "mega", "cool", "bissl", "kfz", "azubi")),
      len(sprachlib.UMGANGSSPRACHE))
check("v5 „sa und so“ → samstags/sonntags, „mo-fr“ → montags bis freitags",
      "samstags" in sprachlib.standardisiere("nur sa und so") and "montag" in sprachlib.standardisiere("mo-fr früh")
      and "sonntag" not in sprachlib.standardisiere("das war so gut"))
check("v5 Levenshtein ≤ 2 nur ab 6 Zeichen", sprachlib.gedeckt("frühestens", sprachlib.Quelle(["frühstens"]))
      and not sprachlib.gedeckt("Kasse", sprachlib.Quelle(["klasse"])))
# Satztrenner (gemeinsam für herkunft, fakten_check, akte)
for t, n_ in (("Ich bin im 5. Semester. Danach Praktikum.", 2), ("Anfangen kann ich am 1. März 2027.", 1),
              ("Herr Dr. Huber wartet z. B. in Raum 2.14. Dann geht es los.", 2), ("Ab dem 2. Ausbildungsjahr betreuen Azubis Kunden.", 1),
              ("Ich war in der 12. Klasse. Das war 2019. Danach kam die Lehre.", 3), ("Kurzpräsentation „Warum ich?“ (3 Min.), Gruppenaufgabe", 1)):
    check(f"v5 Satztrenner: „{t[:40]}…“ → {n_} Satz/Sätze", len(textlib.saetze(t)) == n_, textlib.saetze(t))

# 16d: Bestätigungen „a“, Liste, Wortreihenfolge
check("v5 „a“ / „1a“ / „a passt“ auf „a) Ja b) Nein“ = Ja", all(textlib.ist_ja({"antwort": a_, "frage": "Stimmt das? a) Ja b) Nein"})
                                                               for a_ in ("a", "1a", "a passt", "A)")) and not textlib.ist_ja(
    {"antwort": "a und c", "frage": "a) Kasse b) Lager c) Büro"}))
check("v5 bestätigter Wert ohne zusammenhängende Zeichenfolge („Deutsch ist deine Muttersprache?“)",
      textlib.bestaetigte_werte({"antwort": "ja", "frage": "Deutsch ist deine Muttersprache – stimmt das?", "bestaetigt": "Deutsch Muttersprache"})
      == ["Deutsch Muttersprache"])
d = V5.profil(V5.F605, beispiel())
d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [{"titel": "Schulbildung", "eintraege": [
    {"zeitraum": "07/2025", "titel": "Fachabitur Wirtschaft (Note 2,9)", "ort": "FOS Landshut", "punkte": []},
    {"zeitraum": "07/2023", "titel": "Mittlere Reife", "ort": "", "punkte": []}]}], "kenntnisse": [{"label": "Sonstiges", "wert": "Führerschein Klasse B"}], "interessen": ""}
rc, o = fc(d, "v5_a_ja.json")
check("v5 Transkript 605: Monate aus Bestätigung mit „a“ (zwei Werte) → 0 ❌ im Lebenslauf", rc == 0 and "07/2023" not in "".join(rot(o)), o)

# 16e: Deutsch-Muttersprache nie ohne Angabe; Titel aus Anzeige; Vorlagensätze; Privates
d = V5.profil(V5.F605, beispiel())
d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [{"titel": "Schulbildung", "eintraege": [
    {"zeitraum": "2025", "titel": "Fachabitur", "ort": "FOS Landshut", "punkte": []}]}],
    "kenntnisse": [{"label": "Sprachen", "wert": "Deutsch (Muttersprache), Englisch"}], "interessen": ""}
rc, o = fc(d, "v5_deutsch.json")
check("v5 „Deutsch (Muttersprache)“ ohne Nutzerangabe → ❌ (Transkripte 72/158/423/976)", rc == 1 and "Sprache: Deutsch" in o and "Englisch" in o, o)
d = V5.profil(V5.F654, beispiel())
d["ziel"]["ansprechperson"] = "Frau Dr. Anna Pöllmann"
d["ziel"]["anzeige_text"] += " Ihre Ansprechpartnerin: Frau Dr. Anna Pöllmann (Teamleitung Qualitätssicherung)."
d["anschreiben"]["anrede"] = "Sehr geehrte Frau Dr. Pöllmann,"
rc, o = fc(d, "v5_titel.json")
check("v5 Titel/Funktion aus der Anzeige („Dr.“) in der Anrede → kein ❌", rc == 0 and "dr." not in "".join(rot(o)).lower(), o)
d = V5.profil(V5.F976, beispiel(), up976)
d["email"] = {"betreff": "Bewerbung als Sachbearbeiterin Einkauf in Teilzeit",
              "text": "Sehr geehrter Herr Reiter,\n\nanbei sende ich Ihnen meine Bewerbung als Sachbearbeiterin Einkauf in Teilzeit ab dem 01.02.2027.\n"
                      "Anschreiben, Lebenslauf und Arbeitszeugnis finden Sie in einer PDF im Anhang.\n"
                      "Für Rückfragen erreichen Sie mich unter 0171 5520873.\n\nMit freundlichen Grüßen\nAndrea Wimmer"}
d["person"]["telefon"] = "0171 5520873"
rc, o = fc(d, "v5_mail976.json")
check("v5 Transkript 976: Mail-Vorlage (Arbeitszeugnis, Starttermin) ohne herkunft → 0 ❌", rc == 0 and not rot(o), o)
d["email"]["text"] = d["email"]["text"].replace("Anschreiben, Lebenslauf und Arbeitszeugnis", "Anschreiben, Lebenslauf und meine letzten zwei Zeugnisse")
rc, o = fc(d, "v5_mail605.json")
check("v5 Transkript 605: „… meine letzten zwei Zeugnisse finden Sie …“ → neutral, 0 ❌", rc == 0, o)
d["email"]["text"] = d["email"]["text"].replace("Für Rückfragen", "Ich arbeite täglich mit SAP. Für Rückfragen")
rc, o = fc(d, "v5_mail_erf.json")
check("v5 Vorlage + eigene Behauptung („täglich mit SAP“) → ❌", rc == 1 and "täglich" in "".join(rot(o)), o)
for satz, privat in (("Bei der Krankenkasse habe ich nachgefragt.", False), ("Nach meiner Elternzeit möchte ich wieder arbeiten.", True),
                     ("Bis 16 Uhr kann ich arbeiten, weil ich danach mein Kind aus der Kita abhole.", True)):
    d = V5.profil(V5.F651, beispiel())
    d["anschreiben"]["absaetze"] = [satz]
    d["herkunft"] = [V5.S(satz, (12, "ich hab dann bei der kasse nachgefragt"))]
    d["profil"]["rohtext"].append(V5.R(30, "nach der elternzeit will ich wieder arbeiten, bis 16 uhr weil ich mein kind aus der kita abhole, kasse nachgefragt"))
    d["herkunft"][0]["quellen"].append({"nr": 30, "zitat": "nach der elternzeit"})
    rc, o = fc(d, "v5_privat.json")
    check(f"v5 Privat-Erkennung: „{satz[:35]}…“ → {'❌ Privates' if privat else 'kein Privat-❌'}",
          ("Privates" in o) == privat, o)
# abgeleitete Jahreszahl („letztes Jahr“) → nur ⚠️
d = V5.profil(V5.F158, beispiel())
d["anschreiben"]["absaetze"][1] = d["anschreiben"]["absaetze"][1].replace("Im vergangenen Jahr", f"Im Jahr {datetime.date.today().year - 1}")
for h in d["herkunft"]:
    h["satz"] = h["satz"].replace("Im vergangenen Jahr", f"Im Jahr {datetime.date.today().year - 1}")
rc, o = fc(d, "v5_abgeleitet.json")
check("v5 Jahr aus „letztes jahr“ abgeleitet → ⚠️ bestätigen, kein ❌", rc == 0 and "abgeleitet" in o, o)

# 16f: Lebenslauf – Kfz-Mechatroniker, Dauer abgerundet, eingelernt, Einschränkung, Lücke, Zeitraum, Zukunft
d = V5.profil(V5.F158, beispiel())
d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [{"titel": "Berufserfahrung", "eintraege": [
    {"zeitraum": "05/2007 – 06/2014", "titel": "Lagerhelfer, ab 2008 Staplerfahrer", "ort": "Spedition Kögel, Augsburg",
     "punkte": ["Waren kommissioniert, Lkw be- und entladen", "Neue Mitarbeitende eingelernt"]}]},
    {"titel": "Ausbildung", "eintraege": [{"zeitraum": "09/2005 – 03/2007", "titel": "Ausbildung zum Kfz-Mechatroniker (ohne Abschluss)",
                                           "ort": "Autohaus Seitz, Augsburg", "punkte": []}]}],
    "kenntnisse": [{"label": "Sprachen", "wert": "Deutsch"}], "interessen": ""}
d["anschreiben"]["absaetze"][0] += " Sieben Jahre war ich bei der Spedition Kögel."
d["herkunft"].append(V5.S("Sieben Jahre war ich bei der Spedition Kögel.", (20, "05/2007 – 06/2014"), (7, "spedition kögel")))
rc, o = fc(d, "v5_ll158.json")
check("v5 „Kfz-Mechatroniker“ (Nutzer: „kfz mechatroniker“) → kein Name-❌", "Mechatroniker" not in "".join(rot(o)), o)
check("v5 „Sieben Jahre“ bei 7 J. 2 M. (abgerundet) → ok", "Dauer" not in "".join(rot(o)), o)
check("v5 „eingelernt“ aus „einlernen“ → keine Aufwertungs-⚠️", "eingelernt" not in o, o)
d["anschreiben"]["absaetze"][0] = d["anschreiben"]["absaetze"][0].replace("Sieben Jahre", "Acht Jahre")
d["herkunft"][-1]["satz"] = "Acht Jahre war ich bei der Spedition Kögel."
rc, o = fc(d, "v5_ll158b.json")
check("v5 „Acht Jahre“ bei 7 J. 2 M. (aufgerundet) → ❌", rc == 1 and "Dauer" in o, o)
d = V5.profil(V5.F976, beispiel(), up976)
d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [{"titel": "Berufserfahrung", "eintraege": [
    {"zeitraum": "08/2008 – 03/2018", "titel": "Sachbearbeiterin Einkauf", "ort": "Weigl Elektrotechnik GmbH",
     "punkte": ["Preise mit Lieferanten verhandelt", "Kunden am Telefon beraten"]}]}], "kenntnisse": [], "interessen": ""}
rc, o = fc(d, "v5_ll976.json")
check("v5 Transkript 976: „Preise verhandelt“ ohne „manchmal“ → ⚠️ Einschränkung weg", "Einschränkung weg" in o, o)
check("v5 Lebenslauf-Tätigkeit nie gesagt („Kunden … beraten“) → ⚠️ Lebenslauf-Begriff", "Lebenslauf-Begriff" in o and "beraten" in o, o)
# Lücke automatisch, langer Zeitraum, Zukunft
d = V5.profil(V5.F72, beispiel())
d["person"].update({"plz_ort": "93055 Regensburg", "telefon": "0157 31846620", "email": "mara.kessler@gmx.de"})
d["profil"]["luecken"] = [{"zeitraum": "08/2025 – 12/2025", "bezeichnung": "Bewerbungsphase", "grund": "Pflege in der Familie"}]
d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [
    {"titel": "Praktische Erfahrung", "eintraege": [{"zeitraum": "seit 01/2026", "titel": "Aushilfe Verkauf und Kasse (Minijob)", "ort": "Bäckerei Schmid", "punkte": []}]},
    {"titel": "Schulbildung", "eintraege": [{"zeitraum": "07/2025", "titel": "Fachhochschulreife Wirtschaft", "ort": "FOS Regensburg", "punkte": []}]},
    {"titel": "Weiterbildung", "eintraege": [{"zeitraum": "jährlich, zuletzt 03/2026", "titel": "HACCP-Schulung", "ort": "", "punkte": []},
                                             {"zeitraum": "10/2026 – 07/2029", "titel": "Duales Studium", "ort": "", "punkte": []}]}],
    "kenntnisse": [], "interessen": ""}
Pl = speichern(d, "v5_luecke.json")
rc, o = run(f"{S}/unterlagen_erstellen.py", Pl, "--ausgabe", f"{W}/out_v5ll", "--nur", "lebenslauf")
llt = textlib.read_any(f"{W}/out_v5ll/Lebenslauf_Mara_Kessler_AKTUELL.pdf")
check("v5 Lücke aus profil.luecken automatisch im Lebenslauf (Bezeichnung, nicht der private Grund)",
      "Bewerbungsphase" in llt and "Pflege" not in llt and llt.index("seit 01/2026") < llt.index("Bewerbungsphase") < llt.index("Schulbildung"), llt)
check("v5 langer Zeitraum gekürzt + Hinweis, Rest als Notiz", "zu lang für die Datumsspalte" in o and "zuletzt 03/2026" in llt and "jährlich" in llt, o)
check("v5 Enddatum in der Zukunft → Hinweis „voraussichtlich“", "voraussichtlich" in o, o)
rc, o = run(f"{S}/endcheck.py", f"{W}/out_v5ll/Lebenslauf_Mara_Kessler_AKTUELL.pdf", "--typ", "lebenslauf", "--profil", Pl)
check("v5 endcheck --profil: Zeitraum zu lang + Zukunft gemeldet", "zu lang für die Datumsspalte" in o and "Zukunft" in o, o)
spalte = [p_["text"].split("\t")[0] for p_ in textlib.read_docx(f"{W}/out_v5ll/Lebenslauf_Mara_Kessler_AKTUELL.docx")["paragraphs"]
          if "\t" in p_["text"]]
check("v5 Datumsspalte bleibt schmal (kein Zeitraum > 17 Zeichen vor dem Tab)", spalte and all(len(x) <= 17 for x in spalte)
      and "zuletzt 03/2026" in spalte, spalte)
subprocess.run(["pdftoppm", "-r", "60", "-png", "-f", "1", "-l", "1", f"{W}/out_v5ll/Lebenslauf_Mara_Kessler_AKTUELL.pdf", f"{W}/v5_ll_bild"])

# 16g: Stil-Check im endcheck
open(f"{W}/umgang.txt", "w", encoding="utf8").write(
    "Sehr geehrte Frau Ortner,\nich red gern mit Leuten und find Logistik mega spannend. Mit der Ubahn bin ich in 15 Minuten da. "
    "Mein Kumpel arbeitet bei Ihnen. Sa und So kann ich nix machen, vlt am Abend. Ich habe kommisioniert und die die Listen geprüft.\n"
    "Mit freundlichen Grüßen\nMara Kessler\nmara.kessler@gmx.de")
rc, o = run(f"{S}/endcheck.py", f"{W}/umgang.txt", "--typ", "anschreiben", "--firma", "Hollerith Logistik GmbH")
for wort, vorschlag in (("red", "rede"), ("find", "finde"), ("mega", "sehr"), ("Ubahn", "U-Bahn"), ("Kumpel", "Freund"), ("nix", "nichts"),
                        ("vlt", "vielleicht"), ("kommisioniert", "kommissioniert"), ("Sa und So", "samstags"), ("die die", "die")):
    check(f"v5 endcheck Stil: „{wort}“ → ⚠️ mit Vorschlag „{vorschlag}“", any(wort in z and vorschlag in z for z in o.splitlines() if z.startswith("⚠️")), o)
open(f"{W}/standard.txt", "w", encoding="utf8").write(
    "Sehr geehrte Frau Ortner,\nmich interessiert, wie Waren vom Lager in den Laden gelangen. Mit der U-Bahn bin ich in 15 Minuten bei Ihnen. "
    "Samstags und sonntags arbeite ich in der Bäckerei. Bis 4 Grad muss die Kühlung halten. Die Halt­estelle liegt nah.\n"
    "Mit freundlichen Grüßen\nMara Kessler\nmara.kessler@gmx.de")
rc, o = run(f"{S}/endcheck.py", f"{W}/standard.txt", "--typ", "anschreiben", "--firma", "Hollerith Logistik GmbH")
check("v5 endcheck Stil: Standarddeutsch → kein Stil-⚠️ („4 Grad“, „Samstags“)", "Stil:" not in o, o)
open(f"{W}/quer.txt", "w", encoding="utf8").write("Betreff: Bewerbung als Mitarbeiter Qualitätssicherung (m/w/d)\nSehr geehrte Frau Pöllmann,\n"
                                                  "ich bin Bäcker.\nMit freundlichen Grüßen\nThomas Reischl\nthomas.reischl@t-online.de")
rc, o = run(f"{S}/endcheck.py", f"{W}/quer.txt", "--typ", "anschreiben", "--firma", "Donautal Backwaren GmbH",
            "--stelle", "Mitarbeiter Qualitätssicherung (m/w/d) – Quereinstieg")
check("v5 endcheck: „Quereinstieg“ muss nicht in den Betreff", "Stellenbezeichnung" not in o, o)
open(f"{W}/kurz2.txt", "w").write("Sehr geehrte Damen und Herren,\n" + "Wort " * 210 + "\nMit freundlichen Grüßen")
rc, o = run(f"{S}/endcheck.py", f"{W}/kurz2.txt", "--typ", "kurzanschreiben")
check("v5 Kurzanschreiben: Grenze und Meldung einheitlich 150–200 Wörter", "150–200" in o and "Wörter ab der Anrede" in o, o)

# 16h: Spickzettel-Fehlalarme (Transkripte 72, 651) und Kernbotschaften gegen den Wortlaut
SP5 = V5.profil(V5.F72, beispiel())
SP5["profil"]["rohtext"].append(V5.R(30, "hab die listen angeboten"))
SP5["profil"]["luecken"] = [{"zeitraum": "08/2025 – 12/2025", "bezeichnung": "Bewerbungsphase"}]
SP5["gespraech"].update({
    "termin": "11.02.2027, 8:30 Uhr", "art": "Assessment Center", "ort": "Schulungszentrum Hafenstraße 18", "gespraechspartner": "Frau Dr. Ortner (Ausbildungsleitung)",
    "einladung_text": "Wir laden dich zum Auswahltag am 11.02.2027 um 8:30 Uhr ins Schulungszentrum Hafenstraße 18 ein, Raum 2.14. "
                      "Ablauf: Kurzpräsentation „Warum ich?“ (3 Min.), Gruppenübung (30 Min.), Postkorb (45 Min.). "
                      "Bitte bring deinen Personalausweis mit. Bitte bestätige deine Teilnahme bis 22.01.2027.",
    "kernbotschaften": ["Samstags bereite ich in der Bäckerei die Vorbestellungen vor", "Ich habe die Listen angeboten",
                        "In der 12. Klasse hatte ich Wirtschaft"],
    "schwierige_fragen": [{"frage": "Was hast du zwischen Fachabi und Januar gemacht?", "antwort_final": "Ich habe mich beworben und keinen Platz bekommen."}],
    "ac_uebungen": ["Kurzpräsentation „Warum ich?“", "Gruppenübung", "Postkorb"],
    "mitbringen": ["Personalausweis", "Kugelschreiber", "Lebenslauf ausgedruckt", "Zeugnisse in Kopie", "Etwas zu trinken", "Notizblock", "Uhr"]})
SP5["profil"]["rohtext"].append(V5.R(31, "in der 12. klasse hatte ich wirtschaft, beworben und keinen platz bekommen"))
Psp5 = speichern(SP5, "v5_sp.json")
rc, o = run(f"{S}/akte.py", Psp5, "--spickzettel", "--pdf", "--ausgabe", f"{W}/sp_v5")
sp_v5 = open(f"{W}/sp_v5/Gespraech_Spickzettel_Hollerith-Logistik-GmbH_AKTUELL.txt", encoding="utf8").read()
check("v5 Spickzettel: Bestätigungsfrist (22.01.) ist kein Termin-Fehlalarm", "22.01" not in o, o)
check("v5 Spickzettel: „Raum 2.14“ ist kein Datum", "2.14" not in o, o)
check("v5 Spickzettel: „Bitte bring …“ ist kein Ort", "„bring" not in o and "Ort laut Einladung" not in o, o)
check("v5 Spickzettel: Lücken-Frage ohne Wort „Lücke“ erkannt", "profil.luecken vorhanden" not in o, o)
check("v5 Spickzettel: Vorstellungsdauer 3 Min. (nicht 30 Min. der Gruppenübung)", "(3 MINUTEN)" in sp_v5 or "(3 Min.)" in sp_v5
      and "30 Min" not in [z for z in sp_v5.splitlines() if "Warum ich" in z][0], sp_v5)
check("v5 Spickzettel: „12. Klasse“ bleibt erhalten", "12. Klasse" in sp_v5, sp_v5)
rc, o = run(f"{S}/fakten_check.py", Psp5, "--typ", "spickzettel")
check("v5 Spickzettel: Kernbotschaft „angeboten“ gegen Wortlaut ok, Titel „Dr.“/„Ausbildungsleitung“ aus Einladung kein ❌",
      "angeboten" not in "".join(rot(o)) and "dr." not in "".join(rot(o)).lower() and "Ausbildungsleitung" not in o, o)
SP5b = copy.deepcopy(SP5); SP5b["gespraech"]["kernbotschaften"][1] = "Ich habe die Listen selbst eingeschickt"
rc, o = fc(SP5b, "v5_sp_b.json", "--typ", "spickzettel")
check("v5 Spickzettel: Kernbotschaft „eingeschickt“ (Nutzer sagte „angeboten“) → ❌", rc == 1 and "eingeschickt" in "".join(rot(o)), o)
SP5c = copy.deepcopy(SP5); SP5c["gespraech"]["kernbotschaften"][1] = "Ich habe die Lieferscheine digital erfasst"
rc, o = fc(SP5c, "v5_sp_c.json", "--typ", "spickzettel")
check("v5 Spickzettel: erfundene Kernbotschaft („Lieferscheine digital erfasst“) → ❌", rc == 1 and "Spickzettel-Wortlaut" in o, o)
r5 = pypdf.PdfReader(f"{W}/sp_v5/Gespraech_Spickzettel_Hollerith-Logistik-GmbH_AKTUELL.pdf")
letzte5 = [z for z in (r5.pages[-1].extract_text() or "").splitlines() if z.strip()]
check("v5 Spickzettel-PDF A5: keine fast leere Seite 2 trotz langer Mitbring-Liste", len(r5.pages) == 1 or len(letzte5) >= 6,
      f"{len(r5.pages)} Seiten, letzte {len(letzte5)} Zeilen")
subprocess.run(["pdftoppm", "-r", "70", "-png", f"{W}/sp_v5/Gespraech_Spickzettel_Hollerith-Logistik-GmbH_AKTUELL.pdf", f"{W}/v5_sp_bild"])

# 16i: zugesagte Änderungen, Dateien (bearbeitbar/), Akte ohne Namen, akte --lesen mit Ordner
d = V5.profil(V5.F72, beispiel())
d["person"].update({"plz_ort": "93055 Regensburg", "telefon": "0157 31846620", "email": "mara.kessler@gmx.de"})
d["meta"]["offene_aenderungen"] = [{"text": "Organisationstalent-Satz vor das Beispiel", "unterlage": "anschreiben", "erledigt": False}]
Pae = speichern(d, "v5_aenderung.json")
rc, o = run(f"{S}/unterlagen_erstellen.py", Pae, "--ausgabe", f"{W}/out_ae", "--nur", "anschreiben")
check("v5 Transkript 72: offene zugesagte Änderung → kein Erzeugen (Exit 3)", rc == 3 and "Organisationstalent" in o
      and not os.path.isdir(f"{W}/out_ae") or not os.listdir(f"{W}/out_ae"), o)
rc, o = fc(d, "v5_aenderung2.json")
check("v5 fakten_check meldet offenen Änderungswunsch (⚠️)", "Änderungswunsch" in o, o)
rc, o = run(f"{S}/akte.py", Pae, "--ausgabe", f"{W}/ak_ae")
akae = open(f"{W}/ak_ae/" + [f for f in os.listdir(f"{W}/ak_ae") if f.endswith(".txt")][0], encoding="utf8").read()
check("v5 Akte listet offene Änderungen", "Zugesagte Änderungen (noch offen): Organisationstalent" in akae, akae[:800])
d["meta"]["offene_aenderungen"][0]["erledigt"] = True
speichern(d, "v5_aenderung.json")
rc, o = run(f"{S}/unterlagen_erstellen.py", Pae, "--ausgabe", f"{W}/out_ae", "--nur", "anschreiben")
check("v5 nach dem Abhaken wird erzeugt", rc == 0 and any(f.startswith("Motivationsschreiben") for f in os.listdir(f"{W}/out_ae")), o)
dd = beispiel(); dd["profil"]["anlagen"] = [{"datei": f"{W}/up/Zeugnis_10.jpg", "bezeichnung": "Zeugnis der 10. Klasse"}]
Pdx = speichern(dd, "v5_docx.json")
run(f"{S}/unterlagen_erstellen.py", Pdx, "--ausgabe", f"{W}/out_dx")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", "--einzeln", "--profil", Pdx, "--ausgabe", f"{W}/out_dx")
fl = sorted(f for f in os.listdir(f"{W}/out_dx") if os.path.isfile(os.path.join(f"{W}/out_dx", f)))
check("v5 --einzeln: Word-Fassungen in bearbeitbar/, je Unterlage genau EINE Datei im Ordner",
      rc == 0 and not any(f.endswith(".docx") for f in fl) and os.path.isdir(f"{W}/out_dx/bearbeitbar")
      and len([f for f in fl if f.startswith("Lebenslauf")]) == 1 and len([f for f in fl if f.startswith("Anschreiben")]) == 1, f"{fl}\n{o}")
run(f"{S}/unterlagen_erstellen.py", Pdx, "--ausgabe", f"{W}/out_dx2")
rc, o = run(f"{S}/pdf_zusammenfuegen.py", f"{W}/out_dx2/Bewerbung_Lena_Muster.pdf", "--profil", Pdx, "--ordner", f"{W}/out_dx2")
check("v5 Gesamt-PDF mit --profil: .docx wandern nach bearbeitbar/", rc == 0 and not any(f.endswith(".docx") for f in os.listdir(f"{W}/out_dx2"))
      and "bearbeitbar" in o, f"{os.listdir(W + '/out_dx2')}\n{o}")
run(f"{S}/unterlagen_erstellen.py", Pdx, "--ausgabe", f"{W}/out_dx", "--nur", "lebenslauf")
check("v5 neue Fassung nach bearbeitbar/: alte Word-Fassung wandert nach alt/ (keine Doppelten)",
      not os.path.exists(f"{W}/out_dx/bearbeitbar/Lebenslauf_Lena_Muster_AKTUELL.docx")
      and os.path.exists(f"{W}/out_dx/Lebenslauf_Lena_Muster_AKTUELL.docx"), os.listdir(f"{W}/out_dx"))
dn = beispiel(); dn["person"]["name"] = ""
rc, o = run(f"{S}/akte.py", speichern(dn, "v5_ohne_name.json"), "--ausgabe", f"{W}/ak_nn")
check("v5 Akte schon vor dem Namen (nach dem Berufstest): Bewerbungsakte_<Datum>.txt", rc == 0 and any(
    re.match(r"Bewerbungsakte_\d{4}-\d{2}-\d{2}_\d{6}\.txt", f) for f in os.listdir(f"{W}/ak_nn")), os.listdir(f"{W}/ak_nn"))
os.makedirs(f"{W}/up_v5")
Image.new("RGB", (700, 900), (90, 120, 150)).save(f"{W}/up/IMG_5555.jpg")
dz5 = beispiel(); dz5["profil"]["anlagen"] = [{"datei": f"{W}/up/IMG_5555.jpg", "bezeichnung": "Zeugnis Fachabi"}]
run(f"{S}/akte.py", speichern(dz5, "v5_lesen.json"), "--ausgabe", f"{W}/ak_l5")
shutil.copy(f"{W}/ak_l5/" + [f for f in os.listdir(f"{W}/ak_l5") if f.endswith(".txt")][0], f"{W}/up_v5/Bewerbungsakte (1).txt")
shutil.copy(f"{W}/up/IMG_5555.jpg", f"{W}/up_v5/image.jpg")
os.remove(f"{W}/up/IMG_5555.jpg")
rc, o = run(f"{S}/akte.py", "--lesen", f"{W}/up_v5", "--json-nach", f"{W}/fort_v5/profil.json", env={"BP_UPLOADS": f"{W}/gibts_nicht"})
check("v5 akte --lesen ORDNER: Uploads im angegebenen Ordner gefunden + 🔗-Meldung bei anderem Namen",
      rc == 0 and "image.jpg" in json.load(open(f"{W}/fort_v5/profil.json"))["profil"]["anlagen"][0]["datei"] and "🔗" in o, o)

# 16j: Skill-Texte v5
skill5 = open("/home/claude/hamsterfrei-studio/skills/bewerbungs-profi/SKILL.md", encoding="utf8").read()
check("v5 SKILL.md: Kernprinzip + Standarddeutsch + Budgets (Minijob ≤ 12, AC ≤ 40) oben",
      "Fakten wörtlich, Formulierung frei" in skill5 and "Standarddeutsch" in skill5 and "≤ 12" in skill5 and "≤ 40" in skill5
      and skill5.index("Fakten wörtlich") < skill5.index("Kurzpfade"), "")
ref = "/home/claude/hamsterfrei-studio/skills/bewerbungs-profi/references/"
lies = lambda f: open(ref + f, encoding="utf8").read()  # noqa: E731
check("v5 Fachliches: Zweiradmechatroniker + Tier-Berufe im Berufstest", "Zweiradmechatroniker" in lies("berufstest.md") and "Tierpfleger" in lies("berufstest.md"), "")
check("v5 Fachliches: „Wir duzen uns“ + Werkstudent über 30 (mit Quelle)", "Wir duzen uns" in lies("sonderfaelle.md")
      and "Werkstudent über 30" in lies("sonderfaelle.md") and "Verbraucherzentrale" in lies("sonderfaelle.md"), "")
check("v5 Ablauf: Liste direkt, nie „nur noch eine Frage“, Chatwechsel nur wenn nötig, Rollenspiel zurückholen",
      "direkt als Liste" in lies("interview_fragen.md") and "nur noch eine Frage" in lies("interview_fragen.md")
      and "nur, wenn nötig" in lies("bewerbungsakte.md") and "Abschweifen" in lies("gespraech.md"), "")
check("v5 Mail-Vorlage neutral + bearbeitbar/ in abschicken.md", "brauchen **keine** `herkunft`" in lies("abschicken.md") and "bearbeitbar/" in lies("abschicken.md"), "")

# ================================================================ 11 Skill-Dateien
SK = "/home/claude/hamsterfrei-studio/skills/bewerbungs-profi"
skill = open(f"{SK}/SKILL.md", encoding="utf8").read()
n_zeilen = skill.count("\n") + 1
check(f"SKILL.md ≤ ~200 Zeilen ({n_zeilen})", n_zeilen <= 205, n_zeilen)
fm = re.match(r"---\nname: (.+)\ndescription: \"(.+?)\"\n---", skill, re.S)
check("Frontmatter: name = Ordner, description ≤ 1024, keine < >", fm and fm.group(1) == "bewerbungs-profi"
      and len(fm.group(2)) <= 1024 and "<" not in fm.group(2), fm.group(2)[:80] if fm else skill[:200])
for ref in re.findall(r"`references/([a-z_]+\.md)`", skill):
    check(f"Referenz vorhanden: {ref}", os.path.exists(f"{SK}/references/{ref}"), ref)
alle_md = {f: open(os.path.join(r, f), encoding="utf8").read() for r, _, fs in os.walk(SK) for f in fs if f.endswith(".md") and f != "CHANGELOG.md"}
check("v4 SKILL.md: Satz-Herkunft, Kurzpfade, keine Gerätefrage, kritische Regeln oben",
      "herkunft" in skill and "Kurzpfade" in skill and "keine Gerätefrage" in skill
      and skill.index("kritischen Regeln") < skill.index("Kurzpfade") < skill.index("Wann welche Datei"), "")
check("v4 Keine Gerätefrage mehr in den Anleitungen", not any("Womit bist du gerade hier" in t for t in alle_md.values()), "")
check("v4 KV-Werkstudent richtiggestellt (bis 30, 14-Semester-Grenze seit 2020 weg, mit Quelle)",
      "seit 01.01.2020 nicht mehr" in alle_md["sonderfaelle.md"] and "30 wird" in alle_md["sonderfaelle.md"] and "Barmer" in alle_md["sonderfaelle.md"], "")
check("v4 Pflicht-Checkliste in EINEM Teil", "in **einem** Teil" in alle_md["abschicken.md"] and "2 Nachrichten zu je" not in alle_md["abschicken.md"], "")
check("v4 Postkorb max. 6 Dokumente in 2 Häppchen, abbrechbar", "Höchstens 6 Dokumente" in alle_md["assessment_center.md"]
      and "abbrechbar" in alle_md["assessment_center.md"], "")
for skript in set(re.findall(r"`([a-z_]+\.py)", skill + "".join(alle_md.values()))):
    check(f"Skript vorhanden: {skript}", os.path.exists(f"{SK}/scripts/{skript}"), skript)
check("Keine Verweise auf versand/-Ordner mehr", not any("versand/" in open(os.path.join(r, f), encoding="utf8").read()
      for r, _, fs in os.walk(SK) for f in fs if f.endswith((".md", ".py")) and f != "CHANGELOG.md"), "")
for f in os.listdir(f"{SK}/scripts"):
    if f.endswith(".py"):
        rc, o = run("-m", "py_compile", f"{SK}/scripts/{f}")
        check(f"py_compile {f}", rc == 0, o)

# ================================================================ Abschluss
if OUT_SNAP is not None:
    check("Nichts nach /mnt/user-data/outputs geschrieben", sorted(os.listdir("/mnt/user-data/outputs")) == OUT_SNAP, "")
ok = sum(1 for e, _ in ERG if e)
print(f"\n=== {ok}/{len(ERG)} Tests bestanden ===")
sys.exit(0 if ok == len(ERG) else 1)
