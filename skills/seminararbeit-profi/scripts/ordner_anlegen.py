#!/usr/bin/env python3
"""Legt den Seminararbeit-Ordner mit Unterordnern und Arbeitsstand an und packt ihn als ZIP.

    python ordner_anlegen.py ZIELORDNER "Thema" "Abgabe TT.MM.JJJJ" [Dateien, die einsortiert werden sollen ...]

Dateien werden nach Endung/Name einsortiert: Arbeit (*.docx mit 'arbeit' oder 'seminar'),
Merkblatt (Name enthält 'merkblatt'/'vorgabe'), Quellen (pdf), Screenshots (png/jpg).
"""
import datetime
import os
import shutil
import sys
import zipfile

STRUKTUR = [
    "01_Arbeit/Sicherungen",
    "02_Vorgaben",
    "03_Quellen",
    "04_Belege/Screenshots",
    "05_Checks",
    "06_Pruefungsgespraech",
]

ARBEITSSTAND = """# Arbeitsstand Seminararbeit

Diese Datei bei jedem neuen Chat mit hochladen. Claude aktualisiert sie am Ende jeder Sitzung.

- Thema: {thema}
- Forschungsfrage: (noch offen)
- Leitfach / Lehrkraft: (noch offen)
- Abgabe: {abgabe}
- Prüfungsgespräch: (Termin noch offen)
- Vorgaben: Umfang ?, Schrift ?, Zeilenabstand ?, Zitierweise ? (Merkblatt in 02_Vorgaben)
- KI-Regel der Lehrkraft: (noch offen)

## Gliederung
(noch offen)

## Erledigt
- {heute}: Ordner angelegt

## Offen / nächste Schritte
1. Merkblatt und bisherigen Text hochladen

## Entscheidungen (mit Datum)

## Quellen (freigegeben)
| Kurzbeleg | Art | frei zugänglich | Beleg-Screenshot |
|---|---|---|---|
"""


def sortiere(f):
    n = os.path.basename(f).lower()
    if n == "arbeitsstand.md":
        return "."
    if any(k in n for k in ("merkblatt", "vorgabe", "richtlinie", "bewertungsbogen", "korrektur", "anmerkung", "deckblatt", "vorlage")):
        return "02_Vorgaben"
    if n.endswith((".png", ".jpg", ".jpeg", ".webp", ".heic")):
        return "04_Belege/Screenshots"
    if n.endswith(".docx"):
        return "01_Arbeit"
    return "03_Quellen"


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    ziel, thema, abgabe, *dateien = sys.argv[1:]
    for s in STRUKTUR:
        os.makedirs(os.path.join(ziel, s), exist_ok=True)
    heute = datetime.date.today().strftime("%d.%m.%Y")
    stand = os.path.join(ziel, "Arbeitsstand.md")
    if not os.path.exists(stand) and not any(os.path.basename(d).lower() == "arbeitsstand.md" for d in dateien):
        with open(stand, "w", encoding="utf8") as f:
            f.write(ARBEITSSTAND.format(thema=thema, abgabe=abgabe, heute=heute))
    for d in dateien:
        if os.path.isfile(d):
            dest = os.path.join(ziel, sortiere(d), os.path.basename(d))
            if os.path.abspath(d) != os.path.abspath(dest):
                shutil.copy2(d, dest)
    out_dir = os.environ.get("AUSGABE", "/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else os.path.dirname(os.path.abspath(ziel)))
    zp = os.path.join(out_dir, os.path.basename(ziel.rstrip("/")) + ".zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(ziel):
            rel = os.path.relpath(root, os.path.dirname(os.path.abspath(ziel.rstrip("/"))))
            z.writestr(rel + "/", "")
            for f in files:
                z.write(os.path.join(root, f), os.path.join(rel, f))
    print(f"Ordner: {ziel}\nZIP: {zp}")


if __name__ == "__main__":
    main()
