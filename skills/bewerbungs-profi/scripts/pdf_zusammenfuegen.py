#!/usr/bin/env python3
"""Fügt Anschreiben, Lebenslauf und Anlagen zu EINER PDF zusammen (Reihenfolge = Reihenfolge der Argumente).

    python3 pdf_zusammenfuegen.py ZIEL.pdf Anschreiben.pdf Lebenslauf.pdf Zeugnis.jpg Praktikum.docx ...

- .docx/.odt werden vorher mit LibreOffice in PDF umgewandelt (falls vorhanden).
- .jpg/.png (z. B. abfotografierte Zeugnisse) werden mit Pillow in PDF umgewandelt (falls vorhanden).
- ZIEL ohne Ordner → /mnt/user-data/outputs (falls vorhanden). Umlaute/Leerzeichen im Namen werden ersetzt.
- Bestehende Datei wird nicht überschrieben (_v2, _v3 ...).
- Meldet Seitenzahl und Größe; Richtwert unter 5 MB.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

MAX_MB = 5  # Richtwert für E-Mail-Anhänge; Vorgaben der Anzeige gehen vor


def safe(name):
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        name = name.replace(a, b)
    stem, ext = os.path.splitext(name)
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("_")
    return (stem or "Bewerbung") + (ext or ".pdf")


def unique(p):
    if not os.path.exists(p):
        return p
    s, e = os.path.splitext(p)
    n = 2
    while os.path.exists(f"{s}_v{n}{e}"):
        n += 1
    return f"{s}_v{n}{e}"


def pypdf_laden():
    try:
        import pypdf
        return pypdf
    except ImportError:
        for extra in ([], ["--break-system-packages"]):
            if subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "pypdf", *extra],
                              capture_output=True).returncode == 0:
                break
        try:
            import pypdf
            return pypdf
        except ImportError:
            return None


def als_pdf(pfad, tmp):
    ext = os.path.splitext(pfad)[1].lower()
    if ext == ".pdf":
        return pfad, None
    if ext in (".docx", ".doc", ".odt", ".rtf"):
        so = shutil.which("soffice") or shutil.which("libreoffice")
        if not so:
            return None, "LibreOffice fehlt – diese Datei bitte selbst als PDF speichern"
        r = subprocess.run([so, "--headless", "--convert-to", "pdf", "--outdir", tmp, pfad],
                           capture_output=True, text=True, timeout=180, env=dict(os.environ, HOME=tmp))
        out = os.path.join(tmp, os.path.splitext(os.path.basename(pfad))[0] + ".pdf")
        return (out, None) if r.returncode == 0 and os.path.isfile(out) else (None, "Umwandlung fehlgeschlagen")
    if ext in (".jpg", ".jpeg", ".png", ".webp"):
        try:
            from PIL import Image
        except ImportError:
            return None, "Pillow fehlt – Bild bitte als PDF scannen (z. B. Handy-Scan-App)"
        out = os.path.join(tmp, os.path.basename(pfad) + ".pdf")
        img = Image.open(pfad).convert("RGB")
        img.thumbnail((1654, 2339))  # A4 bei 200 dpi: lesbar, hält die Datei klein
        img.save(out, "PDF", resolution=200)
        return out, None
    return None, f"Dateityp {ext} wird nicht unterstützt (.heic bitte als JPG senden)"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ziel, quellen = sys.argv[1], sys.argv[2:]
    if not os.path.dirname(ziel):
        base = "/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else os.getcwd()
        ziel = os.path.join(base, safe(ziel))
    else:
        ziel = os.path.join(os.path.dirname(ziel), safe(os.path.basename(ziel)))
    os.makedirs(os.path.dirname(os.path.abspath(ziel)), exist_ok=True)
    ziel = unique(ziel)
    with tempfile.TemporaryDirectory() as tmp:
        pdfs, probleme = [], []
        for q in quellen:
            if not os.path.isfile(q):
                probleme.append(f"{q}: nicht gefunden")
                continue
            p, err = als_pdf(q, tmp)
            if err:
                probleme.append(f"{os.path.basename(q)}: {err}")
            else:
                pdfs.append((q, p))
        if not pdfs:
            sys.exit("FEHLER: Keine Datei ließ sich verwenden.\n" + "\n".join(probleme))
        pypdf = pypdf_laden()
        if pypdf:
            w = pypdf.PdfWriter()
            for _, p in pdfs:
                w.append(p)
            with open(ziel, "wb") as f:
                w.write(f)
            seiten = len(pypdf.PdfReader(ziel).pages)
        elif shutil.which("pdfunite"):
            subprocess.run(["pdfunite", *[p for _, p in pdfs], ziel], check=True)
            seiten = None
        else:
            sys.exit("FEHLER: Weder pypdf noch pdfunite verfügbar. Ausweg: Dateien einzeln anhängen, "
                     "wenn die Anzeige das erlaubt.")
    mb = os.path.getsize(ziel) / 1024 / 1024
    print(f"✅ PDF: {ziel}")
    print("Reihenfolge: " + " → ".join(os.path.basename(q) for q, _ in pdfs))
    print(f"Seiten: {seiten if seiten else '?'} | Größe: {mb:.2f} MB")
    if mb > MAX_MB:
        print(f"⚠️ Größer als {MAX_MB} MB – Scans kleiner speichern oder weniger Anlagen (nur relevante Zeugnisse).")
    for p in probleme:
        print(f"⚠️ {p}")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
