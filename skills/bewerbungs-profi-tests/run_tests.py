#!/usr/bin/env python3
"""Tests für bewerbungs-profi v3 – schreibt nur unter /tmp/bp_test3/work.
Enthält die angepassten v2-Tests + Regressionen aus Fehlerliste Runde 1 und Runde 2."""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

S = "/home/claude/hamsterfrei-studio/skills/bewerbungs-profi/scripts"
W = "/tmp/bp_test3/work"
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
check("R2 „juli 26“ im Wortlaut belegt 07/2026", "07/2026" not in o, o)
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
check("R2 Motivationssatz ohne Wortlaut → ⚠️ (kein ❌)", rc == 0 and "Genau so möchte" in o and "kein Problem" in o
      and "⚠️ [weich]" in o, o)
check("R2 Eigenschaft „zuverlässig“ ohne Wortlaut → ⚠️", "zuverlässig" in o, o)
check("Woher-Liste: belegter Satz ↔ Antwort-Nr., unbelegter ↔ ❓", "↔ deine Antwort 5" in o and "↔ ❓" in o, o)
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
d["belege"] = [{"text": "seit über einem Jahr", "woher": "Minijob seit 09/2025"}]
rc, o = fc(d, "bel.json")
check("belege ohne zitat → ❌", rc == 1 and "Beleg ohne Zitat" in o, o)
d["belege"] = [{"text": "seit über einem Jahr", "woher": "Minijob seit 09/2025, heute 11/2026", "zitat": "Kasse im Supermarkt Beispiel in Ingolstadt seit 09/2025"}]
rc, o = fc(d, "bel2.json")
check("belege mit wörtlichem Zitat → ok", rc == 0 and "Beleg ohne Zitat" not in o, o)
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
F284 = json.load(open("/tmp/bp_test3/fixtures/fall_284.json", encoding="utf8"))
rc, o = fc(copy.deepcopy(F284), "f284.json", "--woher")
check("Fall 284: ehrliche Texte aus knappen Antworten → 0 ❌", rc == 0 and not rot(o), o)
check("Fall 284: Auswahl-Antwort „a und b“ belegt Optionstext (Woher ↔ Antwort 9)", "↔ deine Antwort 9" in o, o)
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
check("Fall 284: dazugedichteter Motivationssatz (Begriffe aus der Anzeige) → ⚠️", "⚠️ [weich]" in o and "möchte" in o, o)

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
check("endcheck: Spitzname/Zahlenfolge in E-Mail gewarnt", "partymaus2007" in o and "Zahlenfolge" in o, o)
check("endcheck: echte Fremdfirma gemeldet, früherer Arbeitgeber nicht", "Müller Logistik GmbH" in o and "Supermarkt Beispiel GmbH" not in o.split("Fremde")[-1], o)
check("endcheck: Stelle unvollständig (Büromanagement fehlt)", "unvollständig" in o and "büromanagement" in o.lower(), o)
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
check("R2 Akte: Liste „im neuen Chat wieder hochladen“", "wieder hochladen" in txt and "Zeugnis_10.jpg (Zeugnis der 10. Klasse)" in txt, txt[:600])
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
    "schwierige_fragen": [{"frage": "Was ist Ihre Schwäche?", "antwort": "ich bin ungeduldig"}],
    "feedback": [{"frage": "Was ist Ihre Schwäche?", "besser": "Ich werde ungeduldig, wenn etwas lange dauert. An der Kasse plane ich mir darum feste Pausen ein."}],
    "eigene_fragen": [{"frage": "Wie sieht die Einarbeitung aus?", "gewaehlt": True}, {"frage": "Gibt es Gleitzeit?", "gewaehlt": False},
                      "Wie groß ist das Team? (Vorschlag Claude, intern)"]})
d["profil"]["beispiele"].append({"thema": "Ordnung", "situation": "", "aufgabe": "", "handlung": "", "ergebnis": ""})
Ps = speichern(d, "sp.json")
rc, o = run(f"{S}/akte.py", Ps, "--spickzettel", "--pdf", "--ausgabe", f"{W}/sp")
sp_txt = open(f"{W}/sp/Gespraech_Spickzettel_Beispiel-GmbH_AKTUELL.txt", encoding="utf8").read()
check("R2 Spickzettel: Termin | Art | Ort mit Trennzeichen", "Termin: 12.11.2026, 10:00 Uhr | Art: vor Ort | Ort: Hauptstraße 5" in sp_txt, sp_txt[:300])
check("R2 Spickzettel: Mitbring-Liste, 3 Kernbotschaften", "MITBRINGEN" in sp_txt and "Personalausweis" in sp_txt and "DEINE 3 KERNBOTSCHAFTEN" in sp_txt, sp_txt)
check("R2 Spickzettel: verbesserte Antwort aus Feedback statt alter", "plane ich mir darum feste Pausen" in sp_txt and "ich bin ungeduldig" not in sp_txt, sp_txt)
check("R2 Spickzettel: Lücke als schwierige Frage", "Was war 08/2024 – 02/2025?" in sp_txt, sp_txt)
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
check("R2 AC-Spickzettel: Übungen mit Tipp", "DEIN AUSWAHLTAG" in ac and "Postkorb: A sofort" in ac and "TIPPS FÜR DEIN AUSWAHLTAG" in ac, ac)

# ================================================================ 10 Ordner, textlib
os.makedirs(f"{W}/basis")
rc, o = run(f"{S}/ordner_anlegen.py", f"{W}/basis", "Kita-Verbund Sonnenberg gGmbH", "Erzieher/in (PiA)", AN, "--profil", P, "--zip", "--ausgabe", f"{W}/zip")
check("ordner_anlegen: Ordner + Akte + ZIP", rc == 0 and os.listdir(f"{W}/zip") and
      any(f.startswith("Bewerbungsakte_") for f in os.listdir(f"{W}/basis/Bewerbung_Kita-Verbund-Sonnenberg-gGmbH_Erzieher-in-PiA")), o)
rc, o = run(f"{S}/textlib.py", LL, "--info")
check("textlib --info: eigener LL nicht mehrspaltig", "keine Hinweise auf mehrere Spalten" in o, o[-400:])
rc, o = run(f"{S}/textlib.py", "--help")
check("textlib --help", "Text aus Word" in o, o)

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
