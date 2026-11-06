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
AUSGABE_STD = os.environ.get("BP_AUSGABE", "/mnt/user-data/outputs")   # BP_AUSGABE nur für Tests

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
        # nie mit „fuer“, „der“, „und“ … enden („Kauffrau-fuer“ wirkt abgeschnitten)
        teile = out.split("-") if out else []
        while len(teile) > 1 and teile[-1].lower() in _FUELLWORT:
            teile.pop()
        s = "-".join(teile) or s[:maxlen]
    return s or leer


_FUELLWORT = {"fuer", "der", "die", "das", "den", "dem", "des", "und", "im", "in", "zur", "zum", "von", "vom", "mit",
              "bei", "am", "an", "als", "auf", "aus", "nach", "oder", "fur", "a", "the", "of"}


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


def aktuell_archivieren(pfad):
    """Arbeitsdatei …_AKTUELL.pdf nach alt/…_vN verschieben (z. B. nachdem --einzeln die saubere Upload-Datei
    gebaut hat) – so liegt am Handy nur EINE Datei je Unterlage im Ordner. → neuer Pfad oder None."""
    ordner = os.path.dirname(os.path.abspath(pfad))
    stamm, ext = os.path.splitext(os.path.basename(pfad))
    basis, n = basis_und_version(stamm)
    if n != N_AKTUELL or not os.path.isfile(pfad) or os.path.basename(ordner) == "alt":
        return None
    nr = _naechste_alt_nr(ordner, basis, (".pdf", ".docx", ".txt"))
    alt = os.path.join(ordner, "alt")
    os.makedirs(alt, exist_ok=True)
    ziel = os.path.join(alt, f"{basis}_v{nr}{ext}")
    shutil.move(pfad, ziel)
    return ziel


def versandkopien_weg(ordner, wort, name):
    """Neue Fassung erzeugt → alte saubere Upload-Kopien (Lebenslauf_Vorname_Nachname.pdf,
    Anschreiben_und_Anlagen_….pdf aus --einzeln/--buendeln) nach alt/, damit keine veraltete Datei neben der
    neuen liegt. → Liste der verschobenen Dateinamen."""
    weg = []
    if not os.path.isdir(ordner):
        return weg
    muster = re.compile(rf"^{re.escape(wort)}(_und_Anlagen)?_{re.escape(name)}(_\d+)?\.pdf$")
    for f in os.listdir(ordner):
        if muster.match(f):
            alt = os.path.join(ordner, "alt")
            os.makedirs(alt, exist_ok=True)
            stamm, n = os.path.splitext(f)[0], 1
            while os.path.exists(os.path.join(alt, f"{stamm}_alt{n}.pdf")):
                n += 1
            shutil.move(os.path.join(ordner, f), os.path.join(alt, f"{stamm}_alt{n}.pdf"))
            weg.append(f)
    return weg


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


# ---------------------------------------------------------------- Normalisierungs-Wörterbuch (v4)
# Was Nutzer schreiben („fachabi“, „fsj“, „papa“, „str.“, „20h“, „febuar“) und was in den Unterlagen steht.
# Gilt in BEIDE Richtungen: steht die Kurzform im Wortlaut, ist die Langform belegt – und umgekehrt.
# Nur echte Gleichbedeutungen – keine Aufwertungen (aus „bisschen“ wird hier kein „gute Kenntnisse“).
NORMALISIERUNG = {
    "abi": ["abitur", "allgemeine hochschulreife"],
    "abitur": ["allgemeine hochschulreife", "abi"],
    "allgemeine hochschulreife": ["abitur", "abi"],
    "fachabi": ["fachabitur", "fachhochschulreife"],
    "fachabitur": ["fachhochschulreife", "fachabi"],
    "fachhochschulreife": ["fachabitur", "fachabi"],
    "fhr": ["fachhochschulreife"],
    "quali": ["qualifizierender mittelschulabschluss", "qualifizierender abschluss der mittelschule", "qualifizierender hauptschulabschluss"],
    "qualifizierender mittelschulabschluss": ["quali"],
    "msa": ["mittlerer schulabschluss", "mittlere reife"],
    "m10": ["mittlerer schulabschluss", "mittlere reife"],
    "mittlere reife": ["mittlerer schulabschluss", "realschulabschluss", "msa"],
    "realschulabschluss": ["mittlere reife", "mittlerer schulabschluss"],
    "mittlerer schulabschluss": ["mittlere reife", "msa", "realschulabschluss"],
    "fsj": ["freiwilliges soziales jahr"], "freiwilliges soziales jahr": ["fsj"],
    "föj": ["freiwilliges ökologisches jahr"], "foej": ["freiwilliges ökologisches jahr"],
    "bfd": ["bundesfreiwilligendienst"], "bufdi": ["bundesfreiwilligendienst"], "bundesfreiwilligendienst": ["bfd"],
    "zfa": ["zahnmedizinische fachangestellte", "zahnmedizinischer fachangestellter"],
    "mfa": ["medizinische fachangestellte", "medizinischer fachangestellter"],
    "kfz": ["kraftfahrzeug"], "pkw": ["personenkraftwagen"], "lkw": ["lastkraftwagen"],
    "bio": ["biologie"], "mathe": ["mathematik"], "reli": ["religion"], "geo": ["geographie", "geografie"],
    "info": ["informatik"], "chemie": ["chemie"], "physik": ["physik"], "wirtschaft": ["wirtschaft"],
    "engl": ["englisch"], "franz": ["französisch"], "frz": ["französisch"], "span": ["spanisch"],
    "lk": ["leistungskurs"], "gk": ["grundkurs"], "ag": ["arbeitsgemeinschaft"],
    "fos": ["fachoberschule"], "bos": ["berufsoberschule"], "gym": ["gymnasium"], "gymi": ["gymnasium"],
    "rs": ["realschule"], "ms": ["mittelschule"], "gs": ["grundschule"], "bs": ["berufsschule"],
    "fh": ["fachhochschule", "hochschule"], "th": ["technische hochschule", "hochschule"],
    "uni": ["universität", "hochschule"], "tu": ["technische universität", "universität"],
    "hochschule": ["fachhochschule", "technische hochschule"],
    "bwl": ["betriebswirtschaftslehre", "betriebswirtschaft"], "vwl": ["volkswirtschaftslehre"],
    "wiwi": ["wirtschaftswissenschaften"], "wing": ["wirtschaftsingenieurwesen"],
    "azubi": ["auszubildende", "auszubildender", "ausbildung"], "praxissemester": ["praktikum"],
    "b.a.": ["bachelor of arts"], "bachelor of arts": ["b.a."], "b.sc.": ["bachelor of science"],
    "bachelor of science": ["b.sc."], "b.eng.": ["bachelor of engineering"], "bachelor of engineering": ["b.eng."],
    "m.a.": ["master of arts"], "master of arts": ["m.a."], "m.sc.": ["master of science"], "master of science": ["m.sc."],
    "ll.b.": ["bachelor of laws"], "bachelor of laws": ["ll.b."],
    "papa": ["vater"], "papi": ["vater"], "mama": ["mutter"], "mami": ["mutter"], "vater": ["papa"], "mutter": ["mama"],
    "oma": ["großmutter"], "opa": ["großvater"], "bro": ["bruder"], "sis": ["schwester"],
    "lappen": ["führerschein"], "b-schein": ["führerschein klasse b"], "autoführerschein": ["führerschein klasse b"],
    "str.": ["straße"], "str": ["straße"], "straße": ["str."], "strasse": ["straße"],
    "pl.": ["platz"], "nr.": ["nummer"], "hbf": ["hauptbahnhof"], "min": ["minuten"], "min.": ["minuten"],
    "std": ["stunden"], "std.": ["stunden"], "km": ["kilometer"], "ca.": ["etwa", "circa"],
    "ehrenamtlich": ["ehrenamt"], "ehrenamt": ["ehrenamtlich"],
    "minijob": ["aushilfe", "geringfügige beschäftigung"], "aushilfe": ["aushilfskraft"],
    "nebenjob": ["aushilfe"], "werkstudi": ["werkstudent", "werkstudentin"],
    "office": ["word", "excel", "powerpoint", "ms office", "microsoft office"],
    "ms office": ["microsoft office", "word", "excel", "powerpoint"],
    "pc": ["computer"], "laptop": ["computer"], "erste hilfe": ["ersthelfer"], "ersthelfer": ["erste hilfe"],
}
# Rückrichtung automatisch: steht die Langform im Wortlaut, ist auch die Kurzform belegt
for _k, _werte in list(NORMALISIERUNG.items()):
    for _v in _werte:
        NORMALISIERUNG.setdefault(_v, [])
        if _k not in NORMALISIERUNG[_v]:
            NORMALISIERUNG[_v].append(_k)
# Monatsnamen inkl. typischer Tippfehler
MONATE_NORM = {
    "januar": 1, "jänner": 1, "janur": 1, "januat": 1, "jan": 1, "februar": 2, "febuar": 2, "februrar": 2, "feburar": 2,
    "feber": 2, "febr": 2, "feb": 2, "märz": 3, "maerz": 3, "marz": 3, "mär": 3, "mrz": 3, "april": 4, "apirl": 4,
    "apr": 4, "mai": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7, "august": 8, "augsut": 8, "aug": 8,
    "september": 9, "septemer": 9, "spetember": 9, "sept": 9, "sep": 9, "oktober": 10, "oktbober": 10, "okt": 10,
    "november": 11, "novmber": 11, "nov": 11, "dezember": 12, "dezemer": 12, "dez": 12}


def normalisiere_nutzertext(t):
    """Nutzer-Wortlaut → Wortlaut + Ergänzungszeilen aus dem Wörterbuch (Kurz-/Langformen, Tippfehler bei
    Monaten, „20h“ → „20 Stunden“, „29-31k“ → „29.000 31.000“). Das Original bleibt vollständig erhalten."""
    t = t or ""
    low = t.lower()
    extra = []
    for k, werte in NORMALISIERUNG.items():
        if re.search(r"(?<![\wäöüß])" + re.escape(k) + (r"(?![\wäöüß])" if k[-1].isalnum() else ""), low):
            extra += werte
    for m in re.finditer(r"(?<![\w.,])(\d{1,3})\s*(?:h|std\.?|stunden?)(?![\wäöü])(?:\s*(?:/|pro|die|in der)\s*(?:woche|wo|w)\b)?", low):
        extra.append(f"{m.group(1)} Stunden")
        if re.search(r"/\s*w|woche|pro wo", m.group(0)):
            extra.append(f"{m.group(1)} Stunden pro Woche {m.group(1)} Std./Woche")
    for m in re.finditer(r"(?<![\w.,])(\d{1,3})(?:[.,](\d))?\s*(?:-|–|bis)?\s*(\d{1,3})?(?:[.,](\d))?\s*k\b", low):
        for zahl, nach in ((m.group(1), m.group(2)), (m.group(3), m.group(4))):
            if zahl:
                wert = int(zahl) * 1000 + (int(nach) * 100 if nach else 0)
                extra.append(f"{wert:,}".replace(",", "."))
    woerter = set(re.findall(r"[a-zäöüß]+", low))
    ersatz = {}
    for w in woerter:
        if w in MONATE_NORM:
            if w not in _MONAT_STANDARD:
                ersatz[w] = _MONAT_STANDARD_NAME[MONATE_NORM[w]]
        elif len(w) >= 6:
            for mon, nr in _MONAT_STANDARD_NAME.items():
                if len(nr) >= 6 and _ein_fehler(w, nr):
                    ersatz[w] = nr
                    break
    if ersatz:
        neu = low
        for w, n in ersatz.items():
            neu = re.sub(r"(?<![a-zäöüß])" + re.escape(w) + r"(?![a-zäöüß])", n, neu)
        extra.append(neu)
    if not extra:
        return t
    return t + "\n" + "\n".join(dict.fromkeys(extra))


_MONAT_STANDARD_NAME = {1: "januar", 2: "februar", 3: "märz", 4: "april", 5: "mai", 6: "juni", 7: "juli", 8: "august",
                        9: "september", 10: "oktober", 11: "november", 12: "dezember"}
_MONAT_STANDARD = set(_MONAT_STANDARD_NAME.values()) | {"jan", "feb", "apr", "jun", "jul", "aug", "sep", "sept", "okt",
                                                        "nov", "dez", "jänner", "maerz", "mär"}


def _ein_fehler(a, b):
    """Levenshtein-Abstand ≤ 1 (für Tippfehler in Monatsnamen)."""
    if a == b or abs(len(a) - len(b)) > 1:
        return a == b
    if len(a) == len(b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        return len(diff) == 1 or (len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]])
    k, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:i] + l[i + 1:] == k for i in range(len(l)))


# ---------------------------------------------------------------- Wortlaut (v3)
JA_RE = re.compile(r"^\s*(ja|jap|jep|jo|joa|yes|genau|stimmt|passt|richtig|korrekt|ok|okay|jawohl|klar|👍)", re.I)


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
                        "bestaetigt": e.get("bestaetigt", ""), "optionen": e.get("optionen") or {},
                        "geklaert": e.get("geklaert", False), "sensibel": e.get("sensibel", False)})
    return out


def unklare_antworten(d):
    """Antworten mit „glaub schon“, „b2 glaub ich“, „vielleicht“ …, die noch nicht per Ja/Nein geklärt sind."""
    out = []
    for e in rohtext_eintraege(d):
        a = e["antwort"]
        if e.get("geklaert") or e.get("sensibel") or len(a) > 160:
            continue
        if re.search(r"(glaub|vielleicht|ungefähr|irgendwie|oder so|denk schon|müsste|keine ahnung|weiß nicht genau)", a, re.I):
            out.append(e)
    return out


def wortlaut(d):
    """Alle Nutzer-Wörter: Antworten + nur bei klarem „ja“ der bestätigte Wert, wenn er wörtlich in der Frage stand
    + bei Auswahlfragen der Text der gewählten Optionen ({"optionen": {"a": "Übernahme", …}}, Antwort „a und b“)."""
    teile = []
    for e in rohtext_eintraege(d):
        if e.get("sensibel"):
            continue          # sensible Details (Todesfall, Diagnose …) sind kein Beleg für Unterlagen
        teile.append(normalisiere_nutzertext(e["antwort"]))
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
