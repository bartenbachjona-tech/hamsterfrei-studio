#!/usr/bin/env python3
"""Text aus Word (.docx), PDF, HTML und Textdateien lesen – plus gemeinsame Hilfen
(Dateinamen, Versionen, Profil-JSON laden) für die anderen Skripte.

    python3 textlib.py DATEI            → reiner Text
    python3 textlib.py DATEI --info     → Text + Layout-Befunde für den ATS-Check
                                          (.docx: Tabellen, Textfelder, Spalten sicher erkannt;
                                           .pdf: einfache Spalten-/Tabellen-Erkennung, kann sich irren)
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
AUSGABE_STD = "/mnt/user-data/outputs"

# ---------------------------------------------------------------- Dateinamen
_TRANS = {
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss", "ẞ": "SS",
    "ı": "i", "İ": "I", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ø": "o", "Ø": "O",
    "æ": "ae", "Æ": "Ae", "œ": "oe", "Œ": "Oe", "þ": "th", "Þ": "Th", "ð": "d",
}


def translit(s):
    """ć→c, ş→s, ı→i, ë→e, ß→ss, ä→ae … – nie Buchstaben einfach löschen."""
    s = "".join(_TRANS.get(ch, ch) for ch in (s or ""))
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def safe_name(s, maxlen=40, leer="unbenannt"):
    """Dateiname-Teil: transliteriert, nur A–Z/0–9/-, gekürzt nur an Wortgrenzen."""
    s = re.sub(r"[^A-Za-z0-9]+", "-", translit(s).strip()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if len(s) > maxlen:
        teile, out = s.split("-"), ""
        for t in teile:
            kand = f"{out}-{t}" if out else t
            if len(kand) > maxlen:
                break
            out = kand
        s = out or s[:maxlen]
    return s or leer


def name_teile(name):
    return "_".join(safe_name(t, 30) for t in (name or "").split() if t.strip()) or "Name"


# ---------------------------------------------------------------- Versionen
# Der Nutzer sieht immer nur EINE Datei je Unterlage: …_AKTUELL.pdf. Frühere Fassungen liegen
# intern in alt/ als …_v1, …_v2 (nichts wird gelöscht). Alte Namen …_vN im Ordner gehen auch.
AKTUELL = "AKTUELL"
N_AKTUELL = 10 ** 6
VER_RE = re.compile(r"^(?P<basis>.+?)_(?:v(?P<n>\d+)|(?P<akt>AKTUELL))$")


def basis_und_version(stamm):
    m = VER_RE.match(stamm)
    if not m:
        return stamm, 0
    return m.group("basis"), (N_AKTUELL if m.group("akt") else int(m.group("n")))


def versionen(ordner, basis, ext):
    """Alle Fassungen basis_vN.ext / basis_AKTUELL.ext im Ordner und in ordner/alt → {n: pfad}
    (AKTUELL hat die höchste Nummer)."""
    gef = {}
    for o in (os.path.join(ordner, "alt"), ordner):
        if not os.path.isdir(o):
            continue
        for f in os.listdir(o):
            s, e = os.path.splitext(f)
            if e.lower() != ext.lower():
                continue
            b, n = basis_und_version(s)
            if b == basis and n:
                gef[n] = os.path.join(o, f)
    return gef


def _naechste_alt_nr(ordner, basis, exts):
    nrs = [n for e in exts for n in versionen(ordner, basis, e) if n < N_AKTUELL]
    return (max(nrs) if nrs else 0) + 1


def neue_version(ordner, basis, ext, mitziehen=(".docx", ".pdf")):
    """Pfad für die neue aktuelle Fassung basis_AKTUELL.ext. Die bisherige AKTUELL-Fassung (und alte
    …_vN-Dateien im Ordner) wandern nach ordner/alt/ als …_vN – so liegt im Ordner genau EINE Datei je
    Unterlage. Gibt (pfad, interne_nummer) zurück. Nichts wird gelöscht oder überschrieben."""
    os.makedirs(ordner, exist_ok=True)
    exts = sorted(set(mitziehen) | {ext})
    alt = os.path.join(ordner, "alt")
    nr = _naechste_alt_nr(ordner, basis, exts)
    # alte _vN-Dateien im Hauptordner nach alt/
    for e in exts:
        for n, p in sorted(versionen(ordner, basis, e).items()):
            if os.path.dirname(os.path.abspath(p)) == os.path.abspath(ordner) and n < N_AKTUELL:
                os.makedirs(alt, exist_ok=True)
                if not os.path.exists(os.path.join(alt, os.path.basename(p))):
                    shutil.move(p, os.path.join(alt, os.path.basename(p)))
    # bisherige AKTUELL-Fassung → alt/basis_vN
    verschoben = False
    for e in exts:
        p = os.path.join(ordner, f"{basis}_{AKTUELL}{e}")
        if os.path.exists(p):
            os.makedirs(alt, exist_ok=True)
            shutil.move(p, os.path.join(alt, f"{basis}_v{nr}{e}"))
            verschoben = True
    return os.path.join(ordner, f"{basis}_{AKTUELL}{ext}"), (nr + 1 if verschoben else nr)


def neueste_version(pfad):
    """(neuester_pfad, n_neu, n_gegeben) für eine Datei mit _vN/_AKTUELL-Endung. Findet die Fassung
    auch, wenn der genannte Pfad inzwischen in alt/ liegt oder gar nicht mehr existiert."""
    ordner = os.path.dirname(os.path.abspath(pfad))
    stamm, ext = os.path.splitext(os.path.basename(pfad))
    basis, n = basis_und_version(stamm)
    such = os.path.dirname(ordner) if os.path.basename(ordner) == "alt" else ordner
    v = versionen(such, basis, ext)
    if not v:
        return pfad, n, n
    n_max = max(v)
    if n_max > n or not os.path.exists(pfad):
        return v[n_max], n_max, n
    return pfad, n, n


def version_text(n):
    return "aktuell" if n >= N_AKTUELL else f"v{n}"


def ausgabe_ordner(wunsch=None):
    if wunsch:
        return wunsch
    return AUSGABE_STD if os.path.isdir(AUSGABE_STD) else os.getcwd()


# ---------------------------------------------------------------- Profil-JSON
AKTE_START = "===== DATEN FUER CLAUDE (nicht aendern) ====="
AKTE_ENDE = "===== ENDE DATEN ====="


def lade_profil(pfad):
    """Profil-JSON aus .json, aus der Akte (.txt mit DATEN-Block) oder alter Akte (.md mit ```json)."""
    if not os.path.isfile(pfad):
        raise RuntimeError(f"Datei nicht gefunden: {pfad}")
    raw = open(pfad, encoding="utf8", errors="replace").read()
    if AKTE_START in raw:
        raw = raw.split(AKTE_START, 1)[1].split(AKTE_ENDE, 1)[0]
    elif not pfad.lower().endswith(".json"):
        bl = re.findall(r"```json\s*\n(.*?)\n```", raw, re.S)
        if bl:
            raw = bl[-1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON ungültig (Zeile {e.lineno}, Spalte {e.colno}): {e.msg}")


# ---------------------------------------------------------------- Wortlaut (v3)
JA_RE = re.compile(r"^\s*(ja|jap|jep|jo|joa|yes|genau|stimmt|passt|richtig|korrekt|ok|okay|jawohl|klar)\b", re.I)


def rohtext_eintraege(d):
    """Liste der Nutzer-Antworten im Wortlaut: profil.rohtext (Hauptquelle) bzw. d['rohtext'].
    Einträge: {"nr", "frage", "antwort", "bestaetigt"} oder einfache Strings."""
    roh = (d.get("profil") or {}).get("rohtext")
    if roh is None:
        roh = d.get("rohtext")
    out = []
    for i, e in enumerate(roh or [], 1):
        if isinstance(e, str):
            out.append({"nr": i, "frage": "", "antwort": e})
        elif isinstance(e, dict):
            out.append({"nr": e.get("nr", i), "frage": e.get("frage", ""), "antwort": e.get("antwort", "") or "",
                        "bestaetigt": e.get("bestaetigt", ""), "optionen": e.get("optionen") or {}})
    return out


def wortlaut(d):
    """Alle Nutzer-Wörter: Antworten + nur bei klarem „ja“ der bestätigte Wert, wenn er wörtlich in der Frage stand
    + bei Auswahlfragen der Text der gewählten Optionen ({"optionen": {"a": "Übernahme", …}}, Antwort „a und b“)."""
    teile = []
    for e in rohtext_eintraege(d):
        teile.append(e["antwort"])
        gewaehlt = set(re.findall(r"(?<![\w])([a-f])(?![\w])", e["antwort"].lower()))
        for k, v in (e.get("optionen") or {}).items():
            if str(k).lower() in gewaehlt:
                teile.append(str(v))
        b = e.get("bestaetigt") or ""
        if b and JA_RE.match(e["antwort"]) and translit(b.lower()) in translit((e.get("frage") or "").lower()):
            teile.append(b)
    return teile


def upload_texte(d, extra=()):
    """Texte aus Uploads (Zeugnisse, alter Lebenslauf …): profil.anlagen[].datei, profil.quellen[] + extra.
    Bilder/Scans ohne Text werden übersprungen (Hinweis)."""
    pfade = [a.get("datei", "") for a in ((d.get("profil") or {}).get("anlagen") or []) if isinstance(a, dict)]
    pfade += [q if isinstance(q, str) else q.get("datei", "") for q in ((d.get("profil") or {}).get("quellen") or [])]
    pfade += list(extra)
    texte, hinweise = [], []
    for p in dict.fromkeys(x for x in pfade if x):
        if not os.path.isfile(p):
            hinweise.append(f"Upload nicht gefunden (nicht als Beleg genutzt): {os.path.basename(p)}")
            continue
        try:
            t = read_any(p)
        except RuntimeError:
            hinweise.append(f"{os.path.basename(p)}: Bild/Scan ohne Text – Inhalt nicht maschinell als Beleg nutzbar")
            continue
        if t.strip():
            texte.append(t)
        else:
            hinweise.append(f"{os.path.basename(p)}: kein Text (Scan) – nicht als Beleg nutzbar")
    return texte, hinweise


# ---------------------------------------------------------------- Lesen
def _para_text(p):
    out = []
    for el in (x for r in p.iter(f"{W}r") for x in r.iter()):
        if el.tag == f"{W}t":
            out.append(el.text or "")
        elif el.tag == f"{W}tab":
            out.append("\t")
        elif el.tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
        elif el.tag == f"{W}noBreakHyphen":
            out.append("-")
    return "".join(out)


def read_docx(path):
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
    }
    hf = []
    for n in z.namelist():
        if re.match(r"word/(header|footer)\d*\.xml", n):
            t = " ".join(_para_text(p) for p in ET.fromstring(z.read(n)).iter(f"{W}p")).strip()
            if t:
                hf.append(t)
    info["kopf_fusszeilen_text"] = " | ".join(hf)
    return {"paragraphs": paras, "info": info}


def read_pdf_text(path, layout=False):
    try:
        import pypdf
        r = pypdf.PdfReader(path)
        if layout:
            try:
                return "\n\f".join((pg.extract_text(extraction_mode="layout") or "") for pg in r.pages), len(r.pages)
            except TypeError:
                pass
        return "\n".join((pg.extract_text() or "") for pg in r.pages), len(r.pages)
    except ImportError:
        pass
    except Exception as e:
        raise RuntimeError(f"PDF ließ sich nicht lesen ({e}). Ist sie passwortgeschützt?")
    if shutil.which("pdftotext"):
        args = ["pdftotext"] + (["-layout"] if layout else []) + [path, "-"]
        out = subprocess.run(args, capture_output=True, text=True)
        return out.stdout, (out.stdout.count("\f") or None)
    raise RuntimeError("Kein PDF-Leser verfügbar (pypdf oder pdftotext). Ausweg: Text einfügen lassen.")


DATUM_LINKS = re.compile(r"^\s*(seit\s+)?(\d{1,2}[./])?\d{2,4}(\s*[–-]\s*((\d{1,2}[./])?\d{2,4}|heute))?\s*$|:\s*$|^\s*\?\?", re.I)


def pdf_spalten_hinweis(path):
    """Einfache Erkennung: viele Zeilen mit zwei Textblöcken nebeneinander, bei denen der linke
    Block KEIN Datum/Label ist → wahrscheinlich zweispaltig oder Tabelle."""
    try:
        txt, _ = read_pdf_text(path, layout=True)
    except RuntimeError:
        return None
    zeilen = [z for z in txt.splitlines() if z.strip()]
    if len(zeilen) < 8:
        return None
    zwei, verdaechtig = 0, 0
    for z in zeilen:
        teile = [t for t in re.split(r"\s{4,}", z.strip()) if t]
        if len(teile) >= 2:
            zwei += 1
            if not DATUM_LINKS.search(teile[0]) and len(teile[0].split()) >= 1 and len(teile[1].split()) >= 2:
                verdaechtig += 1
    anteil = verdaechtig / len(zeilen)
    return {"zeilen": len(zeilen), "zweiblock": zwei, "verdaechtig": verdaechtig, "mehrspaltig": anteil > 0.25}


def read_html_text(path):
    raw = open(path, encoding="utf8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    t = html.unescape(raw)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", t)).strip()


def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        return "\n".join(p["text"] for p in read_docx(path)["paragraphs"] if p["text"].strip())
    if ext == ".pdf":
        return read_pdf_text(path)[0]
    if ext in (".html", ".htm"):
        return read_html_text(path)
    if ext == ".doc":
        raise RuntimeError("Alte .doc-Datei: bitte in Word als .docx oder PDF speichern und neu hochladen.")
    if ext in (".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"):
        raise RuntimeError("Das ist ein Bild. Claude kann es direkt ansehen (Bild im Chat), "
                           "dieses Skript liest nur Text-Dateien.")
    return open(path, encoding="utf8", errors="ignore").read()


WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüßÀ-ɏ0-9]+(?:[-'’][A-Za-zÄÖÜäöüßÀ-ɏ0-9]+)*")


def words(text):
    return WORD_RE.findall(text or "")


def main():
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    path = a[0]
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
    if "--info" in a:
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
            h = pdf_spalten_hinweis(path)
            if h and h["mehrspaltig"]:
                print(f"⚠️ Wahrscheinlich zweispaltig oder mit Tabelle ({h['verdaechtig']} von {h['zeilen']} Zeilen "
                      "mit Textblöcken nebeneinander). ATS-Risiko – einspaltige Fassung anbieten. "
                      "(Einfache Erkennung, kann sich irren: Seite als Bild ansehen.)")
            elif h:
                print("Spalten: keine Hinweise auf mehrere Spalten (einfache Erkennung; Datum links + Text rechts ist ok).")


if __name__ == "__main__":
    main()
