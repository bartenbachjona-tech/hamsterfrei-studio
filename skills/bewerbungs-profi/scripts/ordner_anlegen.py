#!/usr/bin/env python3
"""Legt den Bewerbungsordner mit Unterordnern an, schreibt die Akte aus der Profil-JSON und
sortiert Dateien ein (für verbundene lokale Ordner oder als ZIP zum Download).

    python3 ordner_anlegen.py BASISORDNER "Firma" "Stelle" [Dateien …] [--profil PROFIL.json]
                              [--zip] [--ausgabe ORDNER]

BASISORDNER: verbundener lokaler Ordner (Desktop-App) oder Arbeitsordner in der Sandbox (z. B. /tmp).
Darin entsteht Bewerbung_Firma_Stelle/ (Umlaute/Sonderzeichen transliteriert, keine Leerzeichen).
--profil   schreibt die Bewerbungsakte (befüllt aus der JSON, über akte.py) in den Ordner;
           ältere Akten wandern dort nach alt/.
--zip      packt den Ordner zusätzlich als ZIP nach --ausgabe (Standard /mnt/user-data/outputs).
Bestehende Dateien werden nie überschrieben (gleiche Datei → übersprungen, sonst _v2 …).

Nur die Akte (Free-Plan): akte.py PROFIL.json  (früher: --nur-akte, wird weitergeleitet).
"""
import filecmp
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import akte  # noqa: E402
import textlib  # noqa: E402

STRUKTUR = ["01_Stellenanzeige", "02_Lebenslauf", "03_Anschreiben", "04_Zeugnisse_Anlagen", "05_Versand", "06_Gespraech"]


def sortiere(f):
    n = os.path.basename(f).lower()
    if n.startswith("bewerbungsakte"):
        return "."
    if any(k in n for k in ("anzeige", "stelle", "job", "ausschreibung", "karriere")):
        return "01_Stellenanzeige"
    if any(k in n for k in ("lebenslauf", "cv", "resume")):
        return "02_Lebenslauf"
    if any(k in n for k in ("anschreiben", "motivationsschreiben", "kurzanschreiben", "cover")):
        return "03_Anschreiben"
    if any(k in n for k in ("einladung", "gespraech", "gespräch", "interview", "assessment", "vorbereitung", "feedback", "spickzettel")):
        return "06_Gespraech"
    if any(k in n for k in ("bewerbung_", "e-mail", "email", "mail", "bestaetigung", "bestätigung", "formular")):
        return "05_Versand"
    return "04_Zeugnisse_Anlagen"


def kopiere(src, ordner):
    dest = os.path.join(ordner, os.path.basename(src))
    if os.path.abspath(src) == os.path.abspath(dest):
        return dest, False
    if os.path.exists(dest) and filecmp.cmp(src, dest, shallow=False):
        return dest, False
    if os.path.exists(dest):
        s, e = os.path.splitext(dest)
        n = 2
        while os.path.exists(f"{s}_v{n}{e}"):
            n += 1
        dest = f"{s}_v{n}{e}"
    shutil.copy2(src, dest)
    return dest, True


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    opts = {}
    for k in ("--profil", "--ausgabe", "--name"):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    if a[0] == "--nur-akte":
        if not opts.get("--profil"):
            print("FEHLER: Die Akte wird jetzt aus der Profil-JSON gebaut: akte.py PROFIL.json [--ausgabe ORDNER] "
                  "(oder hier --nur-akte --profil PROFIL.json).")
            sys.exit(2)
        d = textlib.lade_profil(opts["--profil"])
        for r in akte.schreibe_akte(d, textlib.ausgabe_ordner(opts.get("--ausgabe"))):
            print(f"✅ Akte: {r}")
        return
    zip_ = "--zip" in a
    a = [x for x in a if x != "--zip"]
    if len(a) < 3:
        print(__doc__)
        sys.exit(2)
    basis, firma, stelle, *dateien = a
    if not os.path.isdir(basis):
        print(f"FEHLER: Basisordner gibt es nicht: {basis}")
        sys.exit(2)
    ziel = os.path.join(basis, f"Bewerbung_{textlib.safe_name(firma, 30, 'offen')}_{textlib.safe_name(stelle, 40, 'offen')}")
    for s in STRUKTUR:
        os.makedirs(os.path.join(ziel, s), exist_ok=True)
    if opts.get("--profil"):
        try:
            d = textlib.lade_profil(opts["--profil"])
        except RuntimeError as e:
            print(f"FEHLER: {e}")
            sys.exit(2)
        for r in akte.schreibe_akte(d, ziel):
            print(f"✅ Akte: {os.path.relpath(r, ziel)}")
    fehlt = 0
    for d_ in dateien:
        if not os.path.isfile(d_):
            print(f"❌ nicht gefunden: {d_}")
            fehlt += 1
            continue
        dest, neu = kopiere(d_, os.path.join(ziel, sortiere(d_)))
        print(f"  {os.path.basename(d_)} → {os.path.relpath(dest, ziel)}" + ("" if neu else " (lag schon dort)"))
    print(f"✅ Ordner: {ziel}")
    if zip_:
        aus = textlib.ausgabe_ordner(opts.get("--ausgabe"))
        os.makedirs(aus, exist_ok=True)
        zp = os.path.join(aus, os.path.basename(ziel) + ".zip")
        oben = os.path.dirname(os.path.abspath(ziel))
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(ziel):
                rel = os.path.relpath(root, oben)
                z.writestr(rel + "/", "")
                for f in files:
                    z.write(os.path.join(root, f), os.path.join(rel, f))
        print(f"✅ ZIP: {zp}")
    sys.exit(2 if fehlt else 0)


if __name__ == "__main__":
    main()
