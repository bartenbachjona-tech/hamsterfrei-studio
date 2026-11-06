#!/usr/bin/env python3
"""Text aus Word (.docx), PDF, HTML und Textdateien lesen – z. B. alter Lebenslauf,
Stellenanzeige als PDF, Einladung, eigene erzeugte Unterlagen.

Nur Standardbibliothek (zipfile + xml). Für PDF wird pypdf oder pdftotext genutzt,
wenn vorhanden.

    python3 textlib.py DATEI            → reiner Text
    python3 textlib.py DATEI --info     → Text + Layout-Befunde (Tabellen, Spalten,
                                          Textfelder, Bilder, Wörter) für den ATS-Check
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


def _para_text(p):
    out = []
    for el in (x for r in p.iter(f"{W}r") for x in r.iter()):
        if el.tag == f"{W}t":
            out.append(el.text or "")
        elif el.tag in (f"{W}tab",):
            out.append("\t")
        elif el.tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
        elif el.tag == f"{W}noBreakHyphen":
            out.append("-")
    return "".join(out)


def read_docx(path):
    """Gibt dict zurück: paragraphs (Liste von {text, style, highlight}), Layout-Befunde."""
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise RuntimeError(f"{os.path.basename(path)} ist keine gültige Word-Datei (.docx). "
                           "Alte .doc-Dateien bitte in Word als .docx speichern.")
    if "word/document.xml" not in z.namelist():
        raise RuntimeError("In der Datei fehlt word/document.xml – keine Word-Datei.")
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(f"{W}body")
    styles = {}
    if "word/styles.xml" in z.namelist():
        sroot = ET.fromstring(z.read("word/styles.xml"))
        for s in sroot.findall(f"{W}style"):
            n = s.find(f"{W}name")
            styles[s.get(f"{W}styleId")] = n.get(f"{W}val") if n is not None else s.get(f"{W}styleId")
    paras = []
    for p in body.iter(f"{W}p"):
        ppr = p.find(f"{W}pPr")
        sid = None
        if ppr is not None and ppr.find(f"{W}pStyle") is not None:
            sid = ppr.find(f"{W}pStyle").get(f"{W}val")
        hl = any(h.get(f"{W}val") not in (None, "none") for h in p.iter(f"{W}highlight"))
        paras.append({"text": _para_text(p), "style": styles.get(sid, sid or "Normal"), "highlight": hl})
    cols = 1
    for c in root.iter(f"{W}cols"):
        try:
            cols = max(cols, int(c.get(f"{W}num", "1")))
        except ValueError:
            pass
    info = {
        "tabellen": len(list(body.iter(f"{W}tbl"))),
        "textfelder": len(list(root.iter(f"{W}txbxContent"))),
        "bilder": len(list(root.iter(f"{W}drawing"))) + len(list(root.iter(f"{W}pict"))),
        "spalten": cols,
        "kopf_fusszeilen_text": "",
    }
    hf = []
    for n in z.namelist():
        if re.match(r"word/(header|footer)\d*\.xml", n):
            hroot = ET.fromstring(z.read(n))
            t = " ".join(_para_text(p) for p in hroot.iter(f"{W}p")).strip()
            if t:
                hf.append(t)
    info["kopf_fusszeilen_text"] = " | ".join(hf)
    return {"paragraphs": paras, "info": info}


def read_pdf_text(path):
    try:
        import pypdf  # noqa
        r = pypdf.PdfReader(path)
        return "\n".join((pg.extract_text() or "") for pg in r.pages), len(r.pages)
    except ImportError:
        pass
    except Exception as e:
        raise RuntimeError(f"PDF ließ sich nicht lesen ({e}). Ist sie passwortgeschützt?")
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        seiten = out.stdout.count("\f") or None
        return out.stdout, seiten
    raise RuntimeError("Kein PDF-Leser verfügbar (pypdf oder pdftotext). "
                       "Ausweg: pip install pypdf oder den Text einfügen lassen.")


def read_html_text(path):
    raw = open(path, encoding="utf8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    t = html.unescape(raw)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", t)).strip()


def read_any(path):
    """Reiner Text einer Datei (docx, pdf, html, txt, md)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return "\n".join(p["text"] for p in read_docx(path)["paragraphs"] if p["text"].strip())
    if ext == ".pdf":
        return read_pdf_text(path)[0]
    if ext in (".html", ".htm"):
        return read_html_text(path)
    if ext == ".doc":
        raise RuntimeError("Alte .doc-Datei: bitte in Word als .docx oder PDF speichern und neu hochladen.")
    return open(path, encoding="utf8", errors="ignore").read()


WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüßÀ-ÿ0-9]+(?:[-'’][A-Za-zÄÖÜäöüßÀ-ÿ0-9]+)*")


def words(text):
    return WORD_RE.findall(text or "")


def main():
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    if not os.path.isfile(path):
        sys.exit(f"FEHLER: Datei nicht gefunden: {path}")
    try:
        txt = read_any(path)
    except RuntimeError as e:
        sys.exit(f"FEHLER: {e}")
    if not txt.strip():
        print("⚠️ Kein Text gefunden. Vermutlich ein Scan/Foto oder eine Grafik (z. B. aus Canva). "
              "Nichts ist geprüft. Bitte Text einfügen oder eine echte Text-PDF/Word-Datei hochladen.")
        return
    print(txt)
    if "--info" in sys.argv:
        print("\n---")
        print(f"Wörter: {len(words(txt))}")
        if path.lower().endswith(".docx"):
            i = read_docx(path)["info"]
            print(f"Tabellen: {i['tabellen']} | Textfelder: {i['textfelder']} | Bilder: {i['bilder']} | Spalten: {i['spalten']}")
            if i["kopf_fusszeilen_text"]:
                print(f"Text in Kopf-/Fußzeile: {i['kopf_fusszeilen_text'][:150]}")
            if i["tabellen"] or i["textfelder"] or i["spalten"] > 1:
                print("⚠️ ATS-Risiko: Tabellen, Textfelder oder mehrere Spalten werden von Bewerbermanagement-"
                      "Systemen oft falsch gelesen. Einspaltig neu bauen.")
        elif path.lower().endswith(".pdf"):
            seiten = read_pdf_text(path)[1]
            if seiten:
                print(f"Seiten: {seiten}")


if __name__ == "__main__":
    main()
