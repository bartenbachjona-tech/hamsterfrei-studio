#!/usr/bin/env python3
"""Legt den Bewerbungsordner mit Unterordnern und Bewerbungsakte an, sortiert Dateien ein.

    python3 ordner_anlegen.py BASISORDNER "Firma" "Stelle" [Dateien ...] [--zip] [--name "Vorname Nachname"]
    python3 ordner_anlegen.py --nur-akte "Firma" "Stelle" [--name "Vorname Nachname"]

BASISORDNER: der verbundene lokale Ordner (Desktop-App) oder ein Arbeitsordner in der Sandbox.
Darin entsteht Bewerbung_Firma_Stelle/ (Umlaute ersetzt, keine Leerzeichen).
Bestehende Dateien werden nie überschrieben; eine vorhandene Bewerbungsakte.md bleibt.
--zip      packt den Ordner zusätzlich als ZIP nach /mnt/user-data/outputs (Free-Plan: Download).
--nur-akte schreibt nur eine leere Bewerbungsakte.md nach /mnt/user-data/outputs (bzw. aktuellen Ordner).

Einsortiert wird nach Name/Endung: Stellenanzeige, Lebenslauf, Anschreiben, Zeugnisse/Anlagen,
Versand (Bewerbung_*.pdf, E-Mail-Text), Gespräch (Einladung, Vorbereitung).
"""
import datetime
import filecmp
import os
import re
import shutil
import sys
import zipfile

STRUKTUR = [
    "01_Stellenanzeige",
    "02_Lebenslauf",
    "03_Anschreiben",
    "04_Zeugnisse_Anlagen",
    "05_Versand",
    "06_Gespraech",
]

AKTE = """# Bewerbungsakte

> Diese Datei beim nächsten Chat einfach hochladen und schreiben: „Weiter mit meiner Bewerbung.“
> Sie enthält persönliche Daten – nicht öffentlich teilen.

**Stand:** {heute} · **Phase:** 0 Start · **Nächster Schritt:** Stelle auswerten oder Berufstest

## 1. Ziel
- Art: (Ausbildung / duales Studium / Praktikum / Werkstudent / Berufseinstieg / Jobwechsel / Minijob)
- Stelle: {stelle}
- Firma: {firma}
- Link/Quelle der Anzeige: (offen)
- Kennziffer: (offen) · Ansprechperson: (offen)
- Bewerbungsweg: (E-Mail / Online-Formular / Portal / persönlich) · Frist: (offen) · Start: (offen)
- Verlangte Unterlagen: (offen)
- Muss-Anforderungen: (offen)
- Kann-Anforderungen: (offen)
- Schlüsselwörter: (offen)
- Auswahlverfahren erwartet: (Gespräch / Online-Test / Assessment Center / unbekannt)

## 2. Profil (kurz)
- Stand heute: (offen)
- Stärken mit Beispiel: (offen)
- Motivation in eigenen Worten: (offen)
- Warum diese Firma: (offen)
- Berufstest-Code: (falls gemacht)

## 3. Status der Unterlagen
| Unterlage | Status | Datei | Offen |
|---|---|---|---|
| Lebenslauf | offen | – | – |
| Anschreiben | offen | – | – |
| Zeugnisse/Anlagen | offen | – | – |
| E-Mail-Text / Formular-Texte | offen | – | – |
| Gesamt-PDF | offen | – | – |
| Endcheck | offen | – | – |
| Abgeschickt am | – | – | – |

## 4. Gespräch
- Termin/Art: (offen)
- STAR-Geschichten: (offen)
- Eigene Fragen an die Firma: (offen)
- Feedback aus der Übung: (offen)

## 5. Alle Bewerbungen (parallel bewerben)
| Firma | Stelle | Abgeschickt | Status | Nachfassen am |
|---|---|---|---|---|
| {firma} | {stelle} | – | in Arbeit | – |

## 6. Entscheidungen (mit Datum)
- {heute}: Akte angelegt

## 7. Nächste Schritte
1. (offen)

## 8. Daten für die Unterlagen (nicht löschen – daraus baut Claude Word und PDF neu)
```json
{{}}
```
"""


def safe(s, maxlen=40):
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        s = s.replace(a, b)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s.strip()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:maxlen].strip("-") or "offen"


def sortiere(f):
    n = os.path.basename(f).lower()
    if n == "bewerbungsakte.md":
        return "."
    if any(k in n for k in ("anzeige", "stelle", "job", "ausschreibung", "karriere")):
        return "01_Stellenanzeige"
    if any(k in n for k in ("lebenslauf", "cv", "resume")):
        return "02_Lebenslauf"
    if any(k in n for k in ("anschreiben", "motivationsschreiben", "cover")):
        return "03_Anschreiben"
    if any(k in n for k in ("einladung", "gespraech", "gespräch", "interview", "assessment", "vorbereitung", "feedback")):
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


def ausgabe_ordner():
    if os.environ.get("AUSGABE"):
        return os.environ["AUSGABE"]
    return "/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else os.getcwd()


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    name = a[a.index("--name") + 1] if "--name" in a else ""
    if "--name" in a:
        i = a.index("--name")
        del a[i:i + 2]
    heute = datetime.date.today().strftime("%d.%m.%Y")
    if a[0] == "--nur-akte":
        if len(a) < 3:
            sys.exit("FEHLER: --nur-akte braucht Firma und Stelle (notfalls \"offen\").")
        firma, stelle = a[1], a[2]
        p = os.path.join(ausgabe_ordner(), "Bewerbungsakte.md")
        if os.path.exists(p):
            sys.exit(f"Akte gibt es schon: {p} – nicht überschrieben.")
        txt = AKTE.format(heute=heute, firma=firma, stelle=stelle)
        if name:
            txt = txt.replace("# Bewerbungsakte", f"# Bewerbungsakte – {name}", 1)
        open(p, "w", encoding="utf8").write(txt)
        print(f"✅ Akte: {p}")
        return
    if len(a) < 3:
        sys.exit(__doc__)
    zip_ = "--zip" in a
    a = [x for x in a if x != "--zip"]
    basis, firma, stelle, *dateien = a
    if not os.path.isdir(basis):
        sys.exit(f"FEHLER: Basisordner gibt es nicht: {basis}")
    ziel = os.path.join(basis, f"Bewerbung_{safe(firma, 30)}_{safe(stelle, 40)}")
    for s in STRUKTUR:
        os.makedirs(os.path.join(ziel, s), exist_ok=True)
    akte = os.path.join(ziel, "Bewerbungsakte.md")
    hochgeladen = [d for d in dateien if os.path.basename(d).lower() == "bewerbungsakte.md"]
    if hochgeladen and not os.path.exists(akte):
        shutil.copy2(hochgeladen[0], akte)
        print("Akte übernommen (Fortsetzung).")
    elif not os.path.exists(akte):
        txt = AKTE.format(heute=heute, firma=firma, stelle=stelle)
        if name:
            txt = txt.replace("# Bewerbungsakte", f"# Bewerbungsakte – {name}", 1)
        open(akte, "w", encoding="utf8").write(txt)
    else:
        print("Akte existiert schon – unverändert gelassen.")
    for d in dateien:
        if d in hochgeladen:
            continue
        if not os.path.isfile(d):
            print(f"⚠️ nicht gefunden: {d}")
            continue
        dest, neu = kopiere(d, os.path.join(ziel, sortiere(d)))
        print(f"  {os.path.basename(d)} → {os.path.relpath(dest, ziel)}" + ("" if neu else " (lag schon dort)"))
    print(f"✅ Ordner: {ziel}")
    if zip_:
        os.makedirs(ausgabe_ordner(), exist_ok=True)
        zp = os.path.join(ausgabe_ordner(), os.path.basename(ziel) + ".zip")
        oben = os.path.dirname(os.path.abspath(ziel))
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(ziel):
                rel = os.path.relpath(root, oben)
                z.writestr(rel + "/", "")
                for f in files:
                    z.write(os.path.join(root, f), os.path.join(rel, f))
        print(f"✅ ZIP: {zp}")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
