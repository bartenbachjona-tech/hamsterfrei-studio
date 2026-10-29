#!/usr/bin/env python3
"""Gemeinsame Hilfsfunktionen: Word-, PDF-, Text- und HTML-Dateien einlesen.

Nur Standardbibliothek (zipfile + xml). pypdf bzw. pdftotext werden genutzt,
wenn sie vorhanden sind.

Als Programm aufgerufen, gibt es die Arbeit als nummerierte Übersicht aus
(Kapitel, Absatznummer, Text, Fußnoten), damit man Stellen eindeutig benennen kann:
    python textlib.py Arbeit.docx > arbeit_uebersicht.md
"""
import html
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TWIP_PER_CM = 566.93

STOP_HEADINGS = re.compile(
    r"^(\d+(\.\d+)*\.?\s*)?(literatur|quellen|bibliograph|abbildungsverzeichnis|tabellenverzeichnis|"
    r"anhang|erklärung|eidesstattliche|selbstständigkeitserklärung|selbständigkeitserklärung)",
    re.I,
)
SKIP_HEADINGS = re.compile(r"^(inhaltsverzeichnis|inhalt|gliederung)\s*$", re.I)
PSEUDO_NUM = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+[A-ZÄÖÜa-zäöü]")
PSEUDO_WORD = re.compile(r"^(inhaltsverzeichnis|inhalt|einleitung|fazit|schluss|literaturverzeichnis|quellenverzeichnis|quellen|literatur|abbildungsverzeichnis|anhang|erklärung|eidesstattliche erklärung|selbstständigkeitserklärung)\b", re.I)
CAPTION_RE = re.compile(r"^(abbildung|abb\.|tabelle|tab\.|grafik|diagramm|karte)\s*\d+\s*[:.]", re.I)


# ---------------------------------------------------------------- Word
def _style_map(z):
    names, based, ppr, rpr = {}, {}, {}, {}
    defaults = {"font": None, "size": None}
    if "word/styles.xml" not in z.namelist():
        return names, based, ppr, rpr, defaults
    root = ET.fromstring(z.read("word/styles.xml"))
    dd = root.find(f"{W}docDefaults")
    if dd is not None:
        r = dd.find(f"{W}rPrDefault/{W}rPr")
        if r is not None:
            defaults.update(_rpr_info(r))
        p = dd.find(f"{W}pPrDefault/{W}pPr")
        if p is not None:
            defaults.update(_ppr_info(p))
    for s in root.findall(f"{W}style"):
        sid = s.get(f"{W}styleId")
        if s.get(f"{W}type") == "paragraph" and s.get(f"{W}default") in ("1", "true"):
            defaults["para_style"] = sid
        n = s.find(f"{W}name")
        names[sid] = n.get(f"{W}val") if n is not None else sid
        b = s.find(f"{W}basedOn")
        if b is not None:
            based[sid] = b.get(f"{W}val")
        p = s.find(f"{W}pPr")
        if p is not None:
            ppr[sid] = _ppr_info(p)
        r = s.find(f"{W}rPr")
        if r is not None:
            rpr[sid] = _rpr_info(r)
    return names, based, ppr, rpr, defaults


def _rpr_info(r):
    out = {}
    f = r.find(f"{W}rFonts")
    if f is not None:
        out["font"] = f.get(f"{W}ascii") or f.get(f"{W}hAnsi") or f.get(f"{W}asciiTheme")
    sz = r.find(f"{W}sz")
    if sz is not None and sz.get(f"{W}val"):
        out["size"] = int(sz.get(f"{W}val")) / 2
    return out


def _ppr_info(p):
    out = {}
    sp = p.find(f"{W}spacing")
    if sp is not None and sp.get(f"{W}line"):
        rule = sp.get(f"{W}lineRule", "auto")
        if rule == "auto":
            out["line"] = round(int(sp.get(f"{W}line")) / 240, 2)
        else:
            out["line"] = f"{int(sp.get(f'{W}line')) / 20:.0f} pt ({rule})"
    jc = p.find(f"{W}jc")
    if jc is not None:
        out["jc"] = jc.get(f"{W}val")
    if p.find(f"{W}keepNext") is not None:
        out["keepNext"] = True
    ol = p.find(f"{W}outlineLvl")
    if ol is not None:
        out["outline"] = int(ol.get(f"{W}val"))
    if p.find(f"{W}numPr") is not None:
        out["numbered"] = True
    return out


def _resolve(sid, table, based, key, depth=0):
    while sid and depth < 20:
        if sid in table and key in table[sid]:
            return table[sid][key]
        sid = based.get(sid)
        depth += 1
    return None


def _para_text(p):
    parts, refs = [], []
    for el in p.iter():
        tag = el.tag
        if tag == f"{W}t":
            parts.append(el.text or "")
        elif tag == f"{W}tab":
            parts.append(" ")
        elif tag in (f"{W}br", f"{W}cr"):
            parts.append(" ")
        elif tag == f"{W}noBreakHyphen":
            parts.append("-")
        elif tag == f"{W}footnoteReference":
            fid = el.get(f"{W}id")
            refs.append((fid, len("".join(parts))))
            parts.append(f"⁣FN{fid}⁣")
    return "".join(parts), refs


def _theme_fonts(z):
    out = {}
    for n in z.namelist():
        if n.startswith("word/theme/") and n.endswith(".xml"):
            x = z.read(n).decode("utf8", "ignore")
            for kind in ("major", "minor"):
                m = re.search(rf"<a:{kind}Font>\s*<a:latin typeface=\"([^\"]+)\"", x)
                if m:
                    out[kind] = m.group(1)
            break
    return out


def _font_name(f, theme):
    if f and f.lower().startswith("minor"):
        return theme.get("minor", f)
    if f and f.lower().startswith("major"):
        return theme.get("major", f)
    return f


def read_docx(path):
    """Liest eine .docx-Datei. Gibt ein dict mit Absätzen, Fußnoten und Layout zurück."""
    z = zipfile.ZipFile(path)
    names, based, sppr, srpr, defaults = _style_map(z)
    theme = _theme_fonts(z)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(f"{W}body")

    footnotes = {}
    if "word/footnotes.xml" in z.namelist():
        froot = ET.fromstring(z.read("word/footnotes.xml"))
        for fn in froot.findall(f"{W}footnote"):
            if fn.get(f"{W}type") in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            txt = " ".join(_para_text(p)[0] for p in fn.findall(f".//{W}p"))
            footnotes[fn.get(f"{W}id")] = re.sub(r"\s+", " ", txt).strip()

    paragraphs = []
    images = 0
    for p in body.iter(f"{W}p"):
        text_marked, refs = _para_text(p)
        ppr = p.find(f"{W}pPr")
        sid = None
        direct = {}
        if ppr is not None:
            ps = ppr.find(f"{W}pStyle")
            if ps is not None:
                sid = ps.get(f"{W}val")
            direct = _ppr_info(ppr)
        sid = sid or defaults.get("para_style") or "Normal"
        sname = names.get(sid, sid)
        line = direct.get("line", _resolve(sid, sppr, based, "line") or defaults.get("line", 1.0))
        jc = direct.get("jc", _resolve(sid, sppr, based, "jc") or "left")
        outline = direct.get("outline", _resolve(sid, sppr, based, "outline"))
        keep = direct.get("keepNext", _resolve(sid, sppr, based, "keepNext") or False)
        numbered = direct.get("numbered") or _resolve(sid, sppr, based, "numbered") or False
        # Schrift: häufigste Schrift/Größe der Runs
        fonts, sizes = {}, {}
        bold_chars = all_chars = 0
        for r in p.findall(f"{W}r"):
            t = "".join((x.text or "") for x in r.findall(f"{W}t"))
            if not t.strip():
                continue
            all_chars += len(t)
            rp = r.find(f"{W}rPr")
            if rp is not None and rp.find(f"{W}b") is not None and rp.find(f"{W}b").get(f"{W}val", "true") not in ("0", "false"):
                bold_chars += len(t)
            rinfo = _rpr_info(rp) if rp is not None else {}
            f = _font_name(rinfo.get("font") or _resolve(sid, srpr, based, "font") or defaults.get("font"), theme)
            s = rinfo.get("size") or _resolve(sid, srpr, based, "size") or defaults.get("size") or 10
            fonts[f] = fonts.get(f, 0) + len(t)
            sizes[s] = sizes.get(s, 0) + len(t)
        if p.find(f".//{W}drawing") is not None or p.find(f".//{W}pict") is not None:
            images += 1
            has_img = True
        else:
            has_img = False
        is_heading = (
            sname.lower().startswith(("heading", "überschrift", "title", "titel"))
            or outline is not None
        )
        level = None
        plain = re.sub(r"\u2063FN\d+\u2063", "", text_marked).strip()
        if not is_heading and plain and len(plain) < 100 and not plain.endswith((".", ":", ",", ";")) and not re.search(r"\d\s*$", plain) and not sname.lower().startswith(("toc", "verzeichnis")):
            bold = all_chars and bold_chars / all_chars > 0.6
            if (PSEUDO_NUM.match(plain) and (bold or len(plain) < 70)) or (PSEUDO_WORD.match(plain) and (bold or len(plain) < 40)):
                is_heading = True
                m = PSEUDO_NUM.match(plain)
                level = (m.group(1).count(".") + 1) if m else 1
                sname = sname + " (als Überschrift erkannt)"
        if is_heading and level is None:
            m = re.search(r"(\d)", sname)
            level = int(m.group(1)) if m else (outline + 1 if outline is not None else 1)
        paragraphs.append(
            {
                "text_marked": text_marked,
                "text": re.sub(r"⁣FN\d+⁣", "", text_marked),
                "refs": [r[0] for r in refs],
                "style": sname,
                "heading": is_heading,
                "level": level,
                "numbered": bool(numbered),
                "line": line,
                "jc": jc,
                "keepNext": keep,
                "fonts": fonts,
                "sizes": sizes,
                "image": has_img,
                "toc": sname.lower().startswith(("toc", "verzeichnis")),
            }
        )

    margins = None
    sect = body.find(f"{W}sectPr")
    if sect is not None:
        pm = sect.find(f"{W}pgMar")
        if pm is not None:
            margins = {
                k: round(int(pm.get(f"{W}{k}", "0")) / TWIP_PER_CM, 2)
                for k in ("top", "bottom", "left", "right")
            }
    headers = []
    for n in z.namelist():
        if re.match(r"word/header\d*\.xml", n):
            x = z.read(n).decode("utf8", "ignore")
            has_page = bool(re.search(r"PAGE\b", x))
            centered = 'w:val="center"' in x
            headers.append({"datei": n, "seitenzahl": has_page, "zentriert": centered})
    footers = []
    for n in z.namelist():
        if re.match(r"word/footer\d*\.xml", n):
            x = z.read(n).decode("utf8", "ignore")
            footers.append({"datei": n, "seitenzahl": bool(re.search(r"PAGE\b", x))})
    hyph = False
    if "word/settings.xml" in z.namelist():
        hyph = b"autoHyphenation" in z.read("word/settings.xml")
    fn_nr = {}
    for p in paragraphs:
        for fid in p["refs"]:
            if fid not in fn_nr:
                fn_nr[fid] = len(fn_nr) + 1
    return {
        "fn_nr": fn_nr,
        "paragraphs": paragraphs,
        "footnotes": footnotes,
        "margins": margins,
        "headers": headers,
        "footers": footers,
        "autoHyphenation": hyph,
        "images": images,
    }


def chapters(doc):
    """Teilt die Absätze in Hauptteil (mit Kapitel) und Rest. Gibt Liste (kapitel, absatz) zurück."""
    out = []
    current = None
    started = False
    stopped = False
    for i, p in enumerate(doc["paragraphs"]):
        t = p["text"].strip()
        if p["heading"] and t:
            if SKIP_HEADINGS.match(t):
                continue
            if STOP_HEADINGS.match(t):
                stopped = True
            elif not stopped:
                started = True
                current = t
            continue
        if not started or stopped or p["toc"]:
            continue
        out.append((current, i, p))
    doc["struktur_erkannt"] = bool(out)
    if not out:
        # Keine Gliederung erkannt: alle Absätze bis zum Literaturverzeichnis nehmen
        for i, p in enumerate(doc["paragraphs"]):
            t = p["text"].strip()
            if p["heading"] and STOP_HEADINGS.match(t):
                break
            if not p["toc"]:
                out.append(("Text (Gliederung nicht erkannt)", i, p))
    return out


def body_paragraphs(doc):
    """Fließtext-Absätze des Hauptteils ohne Bildunterschriften und leere Zeilen."""
    res = []
    for kap, i, p in chapters(doc):
        t = p["text"].strip()
        if not t or CAPTION_RE.match(t):
            continue
        res.append((kap, i, p))
    return res


# ---------------------------------------------------------------- andere Formate
def read_pdf_text(path):
    try:
        import pypdf  # noqa

        r = pypdf.PdfReader(path)
        return "\n".join((pg.extract_text() or "") for pg in r.pages)
    except Exception:
        pass
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        return out.stdout
    raise RuntimeError("Kein PDF-Leser verfügbar (pypdf oder pdftotext).")


def read_html_text(path):
    raw = open(path, encoding="utf8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return html.unescape(raw)


def read_any(path, nur_hauptteil=True):
    """Gibt den reinen Text einer Datei zurück.
    docx: mit nur_hauptteil=True nur der Fließtext des Hauptteils (für die eigene Arbeit),
    sonst alle Absätze (für Quellen und Vergleichstexte)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        doc = read_docx(path)
        if nur_hauptteil:
            return "\n".join(p["text"] for _, _, p in body_paragraphs(doc))
        return "\n".join(p["text"] for p in doc["paragraphs"] if p["text"].strip())
    if ext == ".pdf":
        return read_pdf_text(path)
    if ext in (".html", ".htm"):
        return read_html_text(path)
    return open(path, encoding="utf8", errors="ignore").read()


SENT_SPLIT = re.compile(r"(?<=[.!?])[\"“”»]?\s+(?=[A-ZÄÖÜ„\"\d])")
ABBR = re.compile(r"\b(z\.\s?B|u\.\s?a|d\.\s?h|bzw|vgl|ca|Nr|Abb|S|Mio|Mrd|etc|ggf|evtl|usw|Jh|bspw|o\.\s?J|o\.\s?O|ebd|Kap|Jg|Dr|Prof|St)\.")


def sentences(text):
    protected = ABBR.sub(lambda m: m.group(0).replace(".", "§"), text)
    parts = SENT_SPLIT.split(protected)
    return [s.replace("§", ".").strip() for s in parts if s.strip()]


WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüßÀ-ÿĀ-žÞþÐð0-9]+(?:[-'’][A-Za-zÄÖÜäöüßÀ-ÿ0-9]+)*")


def words(text):
    return WORD_RE.findall(text)


# ---------------------------------------------------------------- CLI
def main():
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    if not path.lower().endswith(".docx"):
        print(read_any(path))
        return
    doc = read_docx(path)
    kap_last = None
    n = 0
    for kap, i, p in chapters(doc):
        if kap != kap_last:
            print(f"\n## {kap}\n")
            kap_last = kap
            n = 0
        t = p["text_marked"].strip()
        if not t:
            continue
        n += 1
        t = re.sub(r"⁣FN(\d+)⁣", lambda m: f"[^{doc['fn_nr'].get(m.group(1), m.group(1))}]", t)
        print(f"[{n}] {t}\n")
        for fid in p["refs"]:
            print(f"    [^{doc['fn_nr'].get(fid, fid)}]: {doc['footnotes'].get(fid, '')}")
        if p["refs"]:
            print()
    wc = sum(len(words(p['text'])) for _, _, p in body_paragraphs(doc))
    print(f"\n---\nFließtext-Wörter im Hauptteil (ohne Fußnoten, Bildunterschriften, Verzeichnisse): {wc}")


if __name__ == "__main__":
    main()
