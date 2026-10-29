#!/usr/bin/env python3
"""Eine Seite aus einem Quellen-PDF als Bild ausgeben und die belegte Stelle gelb markieren.

    python pdf_markieren.py Quelle.pdf SEITE "gesuchter Wortlaut" ausgabe.png
SEITE ist die PDF-Seite (1 = erste Seite der Datei), nicht die gedruckte Seitenzahl.
Braucht pdftoppm und pdftotext (poppler). Ohne diese Programme: Screenshot selbst machen.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw


def norm(w):
    return re.sub(r"[^\wäöüß]", "", w.lower())


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    pdf, page, phrase, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    if not (shutil.which("pdftoppm") and shutil.which("pdftotext")):
        sys.exit("pdftoppm/pdftotext fehlen – bitte Screenshot der Seite selbst machen und hochladen.")
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", info)
        if m and not 1 <= page <= int(m.group(1)):
            sys.exit(f"Die PDF hat nur {m.group(1)} Seiten – Seite {page} gibt es nicht. (Gemeint ist die PDF-Seite, nicht die gedruckte Seitenzahl.)")
    tmp = tempfile.mkdtemp()
    dpi = 150
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi), "-png", pdf, os.path.join(tmp, "p")], check=True)
    png = [f for f in os.listdir(tmp) if f.endswith(".png")][0]
    img = Image.open(os.path.join(tmp, png)).convert("RGB")
    html = os.path.join(tmp, "b.html")
    subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox", pdf, html], check=True)
    raw = open(html, encoding="utf8", errors="ignore").read()
    words = [(m.group(5), *map(float, m.group(1, 2, 3, 4))) for m in re.finditer(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', raw)]
    target = [norm(w) for w in phrase.split() if norm(w)]
    # Silbentrennung am Zeilenende: "Regenera-" + "tion" → beide Kästchen markieren
    toks = [norm(w[0]) for w in words]
    for i in range(len(words) - 1):
        if words[i][0].endswith("-") and len(words[i][0]) > 2:
            joined = norm(words[i][0][:-1] + words[i + 1][0])
            toks[i] = joined
            toks[i + 1] = "\x00" + joined  # Folgeteil markieren
    # Tokens, die Folgeteil sind, beim Vergleich überspringen
    idx = [i for i, t in enumerate(toks) if not t.startswith("\x00")]
    words_f = [words[i] for i in idx]
    extra = {i: i + 1 for i in range(len(words) - 1) if toks[i + 1].startswith("\x00")}
    toks_f = [toks[i] for i in idx]
    scale = dpi / 72
    found = False
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i in range(len(toks_f) - len(target) + 1):
        if toks_f[i:i + len(target)] == target:
            boxes = []
            for j in idx[i:i + len(target)]:
                boxes.append(words[j])
                if j in extra:
                    boxes.append(words[extra[j]])
            for _, x0, y0, x1, y1 in boxes:
                d.rectangle([x0 * scale - 2, y0 * scale - 2, x1 * scale + 2, y1 * scale + 2], fill=(255, 221, 0, 110))
            found = True
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(out)
    if found:
        print("Markiert.")
    else:
        print("Wortlaut auf dieser Seite nicht gefunden – Seite ohne Markierung gespeichert. Seite oder Wortlaut prüfen.")
        sys.exit(2)


if __name__ == "__main__":
    main()
