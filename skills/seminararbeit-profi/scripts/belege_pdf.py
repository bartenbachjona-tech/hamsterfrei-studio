#!/usr/bin/env python3
"""Quellenbelege bauen: aus Screenshots werden beschriftete Belegseiten und PDFs.

Eingabe: eine CSV-Datei (Trennzeichen ; ) mit den Spalten
    nr;kapitel;kurzbeleg;angabe;url;abgerufen;belegt;datei
  nr        z. B. 3.02
  kapitel   z. B. 3
  kurzbeleg z. B. Müller 2021, S. 12
  angabe    vollständige Angabe wie im Literaturverzeichnis
  url       Adresse der Quelle
  abgerufen TT.MM.JJJJ
  belegt    was genau der Screenshot belegt (Aussage, Zahl, Seite)
  datei     Dateiname des Screenshots im Bilderordner (png/jpg)

Ausgabe im Zielordner:
  Kapitel 3/3.02_Mueller.jpg  (Belegseiten je Kapitel)
  Belege Kapitel 3.pdf        (je Kapitel)
  Quellenbelege gesamt.pdf    (mit Übersicht vorne)
  Übersicht.txt

    python belege_pdf.py belege.csv Bilderordner/ "Quellenbelege (Stand 01.11.2026)" [--qualitaet 60]
"""
import argparse
import csv
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

A4 = (1240, 1754)  # 150 dpi
PAD = 60
GREY = (238, 238, 236)
BLUE = (26, 86, 196)
TEXT = (20, 20, 20)
SUB = (82, 81, 78)


def font(size, bold=False):
    cands = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


F_HEAD, F_TXT, F_SMALL = font(26, True), font(21), font(19)


def wrap(draw, text, fnt, width):
    lines = []
    for para in str(text).split("\n"):
        line = ""
        for word in re.split(r"(\s+)", para):
            test = line + word
            if draw.textlength(test, font=fnt) <= width:
                line = test
            else:
                if line.strip():
                    lines.append(line.rstrip())
                # sehr lange Wörter (URLs) hart umbrechen
                while draw.textlength(word, font=fnt) > width:
                    cut = len(word)
                    while cut > 1 and draw.textlength(word[:cut], font=fnt) > width:
                        cut -= 1
                    lines.append(word[:cut])
                    word = word[cut:]
                line = word.lstrip()
        lines.append(line.rstrip())
    return lines


def header_block(row, width):
    tmp = Image.new("RGB", (width, 10))
    d = ImageDraw.Draw(tmp)
    inner = width - 2 * PAD
    parts = [
        (F_HEAD, TEXT, f"Kapitel {row['kapitel']} · Beleg {row['nr']} · {row['kurzbeleg']}"),
        (F_TXT, TEXT, row.get("angabe", "")),
        (F_TXT, BLUE, row.get("url", "")),
        (F_SMALL, SUB, f"abgerufen am {row.get('abgerufen', '')}  |  Belegt: {row.get('belegt', '')}"),
    ]
    lines = []
    for fnt, col, txt in parts:
        if not str(txt).strip():
            continue
        for ln in wrap(d, txt, fnt, inner):
            lines.append((fnt, col, ln))
        lines.append((None, None, 8))
    h = PAD // 2 + sum((l[0].size + 8) if l[0] else l[2] for l in lines) + PAD // 2
    img = Image.new("RGB", (width, h), GREY)
    d = ImageDraw.Draw(img)
    y = PAD // 2
    for fnt, col, ln in lines:
        if fnt is None:
            y += ln
            continue
        d.text((PAD, y), ln, font=fnt, fill=col)
        y += fnt.size + 8
    return img


def pages_for(row, shot):
    W, H = A4
    head = header_block(row, W)
    shot = shot.convert("RGB")
    scale = (W - 2 * PAD) / shot.width
    shot = shot.resize((W - 2 * PAD, max(1, int(shot.height * scale))), Image.LANCZOS)
    pages = []
    y_src = 0
    first = True
    while y_src < shot.height or first:
        page = Image.new("RGB", A4, "white")
        y = 0
        if first:
            page.paste(head, (0, 0))
            y = head.height + 24
        else:
            d = ImageDraw.Draw(page)
            d.text((PAD, 24), f"Beleg {row['nr']} (Fortsetzung)", font=F_SMALL, fill=SUB)
            y = 70
        avail = H - y - PAD
        part = shot.crop((0, y_src, shot.width, min(shot.height, y_src + avail)))
        page.paste(part, (PAD, y))
        ImageDraw.Draw(page).rectangle([PAD - 1, y - 1, PAD + part.width, y + part.height], outline=(200, 200, 200))
        pages.append(page)
        y_src += avail - (40 if y_src + avail < shot.height else 0)  # 40 px Überlappung, damit keine Zeile zerschnitten wird
        first = False
    return pages


def overview_pages(rows, title):
    W, H = A4
    pages, page, y = [], None, 0
    d = None

    def new():
        nonlocal page, y, d
        page = Image.new("RGB", A4, "white")
        d = ImageDraw.Draw(page)
        y = PAD
        pages.append(page)

    new()
    d.text((PAD, y), title, font=font(34, True), fill=TEXT)
    y += 60
    d.text((PAD, y), f"{len(rows)} Belege · Screenshots mit Adresse und Abrufdatum", font=F_SMALL, fill=SUB)
    y += 50
    for r in rows:
        lines = wrap(d, f"{r['nr']}  {r['kurzbeleg']} – {r.get('belegt', '')}", F_SMALL, W - 2 * PAD)
        need = len(lines) * 27 + 10
        if y + need > H - PAD:
            new()
        for ln in lines:
            d.text((PAD, y), ln, font=F_SMALL, fill=TEXT)
            y += 27
        y += 10
    return pages


def safe(s):
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue")
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")[:40]


def save_pdf(pages, path, q):
    if not pages:
        return
    rgb = [p.convert("RGB") for p in pages]
    rgb[0].save(path, "PDF", save_all=True, append_images=rgb[1:], resolution=150, quality=q)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("bilder")
    ap.add_argument("ziel")
    ap.add_argument("--qualitaet", type=int, default=60)
    ap.add_argument("--titel", default="Quellenbelege")
    a = ap.parse_args()

    with open(a.csv, encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            delim = csv.Sniffer().sniff(sample, delimiters=";,\t").delimiter
        except csv.Error:
            delim = ";"
        rows = [ {k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in csv.DictReader(f, delimiter=delim)]
    pflicht = {"nr", "kapitel", "kurzbeleg", "datei"}
    if rows and not pflicht <= set(rows[0]):
        raise SystemExit(f"CSV-Spalten fehlen: {sorted(pflicht - set(rows[0]))}. Erwartet: nr;kapitel;kurzbeleg;angabe;url;abgerufen;belegt;datei")
    leer = [r.get("nr", "?") for r in rows if not r.get("datei")]
    rows = [r for r in rows if r.get("datei")]
    if leer:
        print("Zeilen ohne Screenshot-Datei übersprungen:", ", ".join(leer))
    os.makedirs(a.ziel, exist_ok=True)
    by_kap, all_pages, fehlen = {}, [], []
    for r in rows:
        p = os.path.join(a.bilder, r["datei"])
        if not os.path.exists(p):
            fehlen.append(r["datei"])
            continue
        try:
            shot = Image.open(p)
            shot.load()
        except Exception:
            fehlen.append(r["datei"] + " (nicht lesbar – z. B. HEIC vom iPhone: bitte als JPG/PNG schicken)")
            continue
        pages = pages_for(r, shot)
        kdir = os.path.join(a.ziel, f"Kapitel {r['kapitel']}")
        os.makedirs(kdir, exist_ok=True)
        for k, pg in enumerate(pages):
            suffix = f"-{k + 1}" if len(pages) > 1 else ""
            pg.save(os.path.join(kdir, f"{r['nr']}{suffix}_{safe(r['kurzbeleg'])}.jpg"), quality=a.qualitaet)
        by_kap.setdefault(r["kapitel"], []).extend(pages)
        all_pages.extend(pages)
    for kap, pages in by_kap.items():
        save_pdf(pages, os.path.join(a.ziel, f"Belege Kapitel {kap}.pdf"), a.qualitaet)
    fehl_namen = {f.split(" (")[0] for f in fehlen}
    ok_rows = [r for r in rows if r["datei"] not in fehl_namen]
    save_pdf(overview_pages(ok_rows, a.titel) + all_pages, os.path.join(a.ziel, "Quellenbelege gesamt.pdf"), a.qualitaet)
    with open(os.path.join(a.ziel, "Übersicht.txt"), "w", encoding="utf8") as f:
        for r in ok_rows:
            f.write(f"{r['nr']}\t{r['kurzbeleg']}\t{r.get('url', '')}\tabgerufen am {r.get('abgerufen', '')}\t{r.get('belegt', '')}\n")
    size = os.path.getsize(os.path.join(a.ziel, "Quellenbelege gesamt.pdf")) / 1e6
    print(f"{len(ok_rows)} Belege, {len(all_pages)} Seiten, Gesamt-PDF {size:.1f} MB → {a.ziel}")
    if size > 30:
        print("Achtung: über 30 MB. Mit --qualitaet 45 neu bauen.")
    if fehlen:
        print("Fehlende Screenshots:", ", ".join(fehlen))


if __name__ == "__main__":
    main()
