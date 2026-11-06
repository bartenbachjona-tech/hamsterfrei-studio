#!/usr/bin/env python3
"""Erzeugt Lebenslauf und Anschreiben als Word (.docx) und, wenn möglich, als PDF.

    python3 unterlagen_erstellen.py DATEN.json [--nur lebenslauf|anschreiben] [--ausgabe ORDNER] [--kein-pdf]
    python3 unterlagen_erstellen.py Bewerbungsakte.md     (liest den json-Block aus der Akte)
    python3 unterlagen_erstellen.py --beispiel             (zeigt das Datenformat als JSON)

Ausgabe: /mnt/user-data/outputs, falls vorhanden, sonst der aktuelle Ordner.
Dateinamen: Lebenslauf_Vorname_Nachname.docx, Anschreiben_Vorname_Nachname_Firma.docx.
Vorhandene Dateien werden nie überschrieben (dann _v2, _v3 ...).
Stellen mit [PRÜFEN: ...] werden im Word-Dokument gelb markiert.

Layout: einspaltig, keine Word-Tabellen, keine Grafiken, Standard-Überschriften,
Daten per Tabstopp ausgerichtet. So können Bewerbermanagement-Systeme (ATS) es auslesen.
Benötigt python-docx (wird bei Bedarf mit pip nachinstalliert). PDF über LibreOffice.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCHRIFT = "Arial"          # überall vorhanden bzw. metrisch gleich ersetzt (Liberation Sans)
GROESSE = 11               # gut lesbar, 1 Seite für Einsteiger bleibt erreichbar
TAB_CM = 4.0               # Spalte für den Text neben dem Zeitraum (einspaltig per Tabstopp)
PRUEFEN_RE = re.compile(r"(\[PRÜFEN:[^\]]*\])")

BEISPIEL = {
    "person": {
        "name": "Lena Muster",
        "strasse": "Musterweg 1",
        "plz_ort": "85049 Ingolstadt",
        "telefon": "0151 23456789",
        "email": "lena.muster@example.de",
        "linkedin": "",
        "geburtsdatum": "",
        "foto": ""
    },
    "ziel": {
        "art": "Ausbildung",
        "stelle": "Kauffrau für Büromanagement",
        "firma": "Beispiel GmbH",
        "kennziffer": "AZ-2027-04",
        "ansprechperson": "Frau Sommer",
        "anrede": "Sehr geehrte Frau Sommer,",
        "firma_adresse": ["Beispiel GmbH", "Personalabteilung", "Frau Petra Sommer", "Hauptstraße 5", "85049 Ingolstadt"]
    },
    "lebenslauf": {
        "kurzprofil": "Organisiert und zahlenfest, Mittlere Reife 2026. Erfahrung an der Kasse und in der Schülerfirma.",
        "abschnitte": [
            {"titel": "Praktische Erfahrung", "eintraege": [
                {"zeitraum": "09/2025 – heute", "titel": "Aushilfe Kasse (Minijob)", "ort": "Supermarkt Beispiel, Ingolstadt",
                 "punkte": ["Kassenabrechnung am Schichtende selbstständig erstellt", "Kundenfragen am Infopunkt beantwortet"]},
                {"zeitraum": "03/2025", "titel": "Schülerpraktikum (2 Wochen)", "ort": "Steuerbüro Beispiel, Ingolstadt",
                 "punkte": ["Belege sortiert und in DATEV erfasst [PRÜFEN: Programmname]"]}
            ]},
            {"titel": "Schulbildung", "eintraege": [
                {"zeitraum": "09/2020 – 07/2026", "titel": "Mittlere Reife (Note 2,3)", "ort": "Realschule Beispiel, Ingolstadt",
                 "punkte": ["Wahlfach Wirtschaft, Schülerfirma: Verkaufsstand mit 4 Mitschülern organisiert"]}
            ]},
            {"titel": "Ehrenamt", "eintraege": [
                {"zeitraum": "seit 2023", "titel": "Jugendtrainerin Handball (U12)", "ort": "TSV Beispiel", "punkte": []}
            ]}
        ],
        "kenntnisse": [
            {"label": "Sprachen", "wert": "Deutsch (Muttersprache), Englisch (B1)"},
            {"label": "EDV", "wert": "Word, Excel (Formeln, Tabellen), PowerPoint"},
            {"label": "Führerschein", "wert": "Klasse B (ab 02/2027) [PRÜFEN: Datum]"}
        ],
        "interessen": "Handball (Training einer Jugendmannschaft)",
        "ort_datum_unterschrift": False
    },
    "anschreiben": {
        "betreff": "Bewerbung um einen Ausbildungsplatz als Kauffrau für Büromanagement ab 01.09.2027 (Kennziffer AZ-2027-04)",
        "anrede": "Sehr geehrte Frau Sommer,",
        "absaetze": [
            "seit einem Jahr mache ich an der Kasse eines Supermarkts die Abrechnung am Schichtende selbst. Dabei habe ich gemerkt, wie gern ich Zahlen sauber und ohne Fehler abschließe.",
            "In Ihrer Anzeige nennen Sie Sorgfalt und Teamarbeit. In meinem Praktikum im Steuerbüro habe ich Belege sortiert und erfasst. In der Schülerfirma haben wir zu fünft einen Verkaufsstand geplant; ich habe die Kasse und die Abrechnung übernommen.",
            "[PRÜFEN: Warum genau die Beispiel GmbH? Ein konkreter Grund vom Nutzer]",
            "Ich freue mich auf ein persönliches Gespräch."
        ],
        "gruss": "Mit freundlichen Grüßen",
        "anlagen": ["Lebenslauf", "Zeugnis der 9. und 10. Klasse", "Praktikumsbescheinigung"],
        "ort_datum": ""
    }
}


# ---------------------------------------------------------------- Hilfen
def ensure_docx():
    try:
        import docx  # noqa: F401
        return
    except ImportError:
        pass
    print("python-docx fehlt – installiere es mit pip ...", file=sys.stderr)
    for extra in ([], ["--break-system-packages"]):
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "python-docx", *extra],
                           capture_output=True, text=True)
        if r.returncode == 0:
            break
    try:
        import docx  # noqa: F401
    except ImportError:
        sys.exit("FEHLER: python-docx ließ sich nicht installieren (kein Internet in der Sandbox?).\n"
                 "Ausweg: den eingebauten docx-Skill nutzen und das gleiche Layout nachbauen "
                 "(einspaltig, keine Tabellen, Überschriften wie hier).")


def safe_name(s, maxlen=40):
    s = (s or "").strip()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        s = s.replace(a, b)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s[:maxlen].strip("-") or "unbenannt"


def name_teile(name):
    return "_".join(safe_name(t, 30) for t in (name or "").split() if t.strip()) or "Name"


def unique_path(ordner, basis, ext):
    p = os.path.join(ordner, f"{basis}{ext}")
    n = 2
    while os.path.exists(p):
        p = os.path.join(ordner, f"{basis}_v{n}{ext}")
        n += 1
    return p


def load_data(path):
    if not os.path.isfile(path):
        sys.exit(f"FEHLER: Datei nicht gefunden: {path}")
    raw = open(path, encoding="utf8").read()
    if path.lower().endswith(".md"):
        blocks = re.findall(r"```json\s*\n(.*?)\n```", raw, re.S)
        if not blocks:
            sys.exit("FEHLER: In der Akte steht kein ```json-Block mit den Daten. "
                     "Daten neu erfragen und als JSON übergeben.")
        raw = blocks[-1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"FEHLER: JSON ist ungültig (Zeile {e.lineno}, Spalte {e.colno}): {e.msg}")


def ort_aus(plz_ort):
    m = re.match(r"^\s*\d{4,5}\s+(.+)$", plz_ort or "")
    return (m.group(1) if m else (plz_ort or "")).strip()


def heute():
    return datetime.date.today().strftime("%d.%m.%Y")


# ---------------------------------------------------------------- Word-Bausteine
def neues_dokument(titel, autor):
    from docx import Document
    from docx.enum.text import WD_COLOR_INDEX  # noqa: F401
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    sec.left_margin, sec.right_margin = Cm(2.5), Cm(2.0)
    for sname in ("Normal", "List Bullet", "Heading 1", "Title"):
        st = doc.styles[sname]
        st.font.name = SCHRIFT
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = rpr.makeelement(qn("w:rFonts"), {})
            rpr.append(rf)
        for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(k), SCHRIFT)
        for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rf.get(qn(k)) is not None:
                del rf.attrib[qn(k)]
        st.font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Normal"].font.size = Pt(GROESSE)
    pf = doc.styles["Normal"].paragraph_format
    pf.space_after, pf.space_before, pf.line_spacing = Pt(2), Pt(0), 1.1
    h = doc.styles["Heading 1"]
    h.font.size, h.font.bold = Pt(12.5), True
    h.paragraph_format.space_before, h.paragraph_format.space_after = Pt(12), Pt(4)
    h.paragraph_format.keep_with_next = True
    _unterstrich(h.element.get_or_add_pPr())
    doc.core_properties.title = titel
    doc.core_properties.author = autor
    doc.core_properties.comments = ""
    return doc


def _unterstrich(ppr):
    from docx.oxml.ns import qn
    bdr = ppr.makeelement(qn("w:pBdr"), {})
    b = bdr.makeelement(qn("w:bottom"), {qn("w:val"): "single", qn("w:sz"): "6", qn("w:space"): "1", qn("w:color"): "808080"})
    bdr.append(b)
    ppr.append(bdr)


def text(par, inhalt, bold=False, size=None):
    """Fügt Text ein; [PRÜFEN: ...] wird gelb markiert."""
    from docx.enum.text import WD_COLOR_INDEX
    from docx.shared import Pt
    for teil in PRUEFEN_RE.split(inhalt or ""):
        if not teil:
            continue
        r = par.add_run(teil)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if PRUEFEN_RE.fullmatch(teil):
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return par


def tab_absatz(doc, links, rechts_fett, rechts_rest=""):
    from docx.shared import Cm, Pt
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Cm(TAB_CM))
    p.paragraph_format.left_indent = Cm(TAB_CM)
    p.paragraph_format.first_line_indent = Cm(-TAB_CM)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.keep_with_next = True
    text(p, (links or "") + "\t")
    text(p, rechts_fett, bold=True)
    if rechts_rest:
        text(p, rechts_rest)
    return p


def punkt(doc, inhalt):
    from docx.shared import Cm
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(TAB_CM + 0.5)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    text(p, inhalt)
    return p


# ---------------------------------------------------------------- Lebenslauf
def baue_lebenslauf(d, ordner):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    pers, lv = d.get("person", {}), d.get("lebenslauf", {})
    name = pers.get("name", "").strip()
    doc = neues_dokument("Lebenslauf " + name, name)
    foto = pers.get("foto")
    if foto and os.path.isfile(foto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run().add_picture(foto, width=Cm(3.5))
    p = doc.add_paragraph(style="Title")
    p.paragraph_format.space_after = Pt(2)
    text(p, "Lebenslauf", size=13)
    p = doc.add_paragraph()
    text(p, name, bold=True, size=18)
    kontakt = [pers.get(k, "") for k in ("strasse", "plz_ort", "telefon", "email", "linkedin")]
    p = doc.add_paragraph()
    text(p, " | ".join(k for k in kontakt if k))
    if pers.get("geburtsdatum"):
        text(doc.add_paragraph(), "Geboren am " + pers["geburtsdatum"])
    if lv.get("kurzprofil"):
        doc.add_heading("Kurzprofil", level=1)
        text(doc.add_paragraph(), lv["kurzprofil"])
    for ab in lv.get("abschnitte", []):
        if not ab.get("eintraege"):
            continue
        doc.add_heading(ab.get("titel", "Stationen"), level=1)
        for e in ab["eintraege"]:
            rest = (", " + e["ort"]) if e.get("ort") else ""
            tab_absatz(doc, e.get("zeitraum", ""), e.get("titel", ""), rest)
            for pkt in e.get("punkte", []):
                punkt(doc, pkt)
    if lv.get("kenntnisse"):
        doc.add_heading("Kenntnisse", level=1)
        for k in lv["kenntnisse"]:
            tab_absatz(doc, k.get("label", "") + ":", "", k.get("wert", ""))
    if lv.get("interessen"):
        doc.add_heading("Interessen", level=1)
        text(doc.add_paragraph(), lv["interessen"])
    if lv.get("ort_datum_unterschrift"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(24)
        text(p, f"{ort_aus(pers.get('plz_ort'))}, {heute()}")
        text(doc.add_paragraph(), name)
    pfad = unique_path(ordner, "Lebenslauf_" + name_teile(name), ".docx")
    doc.save(pfad)
    return pfad


# ---------------------------------------------------------------- Anschreiben
def baue_anschreiben(d, ordner):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    pers, ziel, an = d.get("person", {}), d.get("ziel", {}), d.get("anschreiben", {})
    name = pers.get("name", "").strip()
    doc = neues_dokument("Anschreiben " + name, name)
    absender = [name] + [pers.get(k, "") for k in ("strasse", "plz_ort", "telefon", "email")]
    for i, z in enumerate(a for a in absender if a):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        text(p, z, bold=(i == 0))
    doc.add_paragraph()
    for z in ziel.get("firma_adresse") or [ziel.get("firma", "")]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        text(p, z)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(18)
    text(p, an.get("ort_datum") or f"{ort_aus(pers.get('plz_ort'))}, {heute()}")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    text(p, an.get("betreff") or f"Bewerbung als {ziel.get('stelle', '')}", bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    text(p, an.get("anrede") or ziel.get("anrede") or "Sehr geehrte Damen und Herren,")
    for a in an.get("absaetze", []):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        text(p, a)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    text(p, an.get("gruss", "Mit freundlichen Grüßen"))
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(24)
    text(p, name)
    if an.get("anlagen"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        text(p, "Anlagen: " + ", ".join(an["anlagen"]))
    firma = safe_name(ziel.get("firma", ""), 30)
    pfad = unique_path(ordner, f"Anschreiben_{name_teile(name)}_{firma}", ".docx")
    doc.save(pfad)
    return pfad


# ---------------------------------------------------------------- PDF
def zu_pdf(docx_pfad):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None, "LibreOffice fehlt – PDF bitte in Word erstellen (Datei → Speichern unter → PDF)."
    ordner = os.path.dirname(os.path.abspath(docx_pfad))
    ziel = os.path.splitext(docx_pfad)[0] + ".pdf"
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, HOME=tmp)
        try:
            r = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, docx_pfad],
                               capture_output=True, text=True, timeout=180, env=env)
        except subprocess.TimeoutExpired:
            return None, "PDF-Umwandlung hat zu lange gedauert – PDF bitte in Word erstellen."
        erzeugt = os.path.join(tmp, os.path.splitext(os.path.basename(docx_pfad))[0] + ".pdf")
        if r.returncode != 0 or not os.path.isfile(erzeugt):
            return None, "PDF-Umwandlung fehlgeschlagen: " + (r.stderr or r.stdout).strip()[:200]
        shutil.move(erzeugt, ziel)
    return ziel, None


def pruef_luecken(d, nur):
    fehl = []
    pers = d.get("person", {})
    for k, label in (("name", "Name"), ("telefon", "Telefon"), ("email", "E-Mail"), ("plz_ort", "PLZ/Ort")):
        if not pers.get(k):
            fehl.append(label)
    if nur in (None, "anschreiben"):
        if not d.get("ziel", {}).get("firma"):
            fehl.append("Firma (ziel.firma)")
        if not d.get("anschreiben", {}).get("absaetze"):
            fehl.append("Anschreiben-Absätze")
    return fehl


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--beispiel":
        print(json.dumps(BEISPIEL, ensure_ascii=False, indent=2))
        return
    quelle = a[0]
    nur = a[a.index("--nur") + 1] if "--nur" in a else None
    if nur not in (None, "lebenslauf", "anschreiben"):
        sys.exit("FEHLER: --nur kennt nur 'lebenslauf' oder 'anschreiben'.")
    std = "/mnt/user-data/outputs" if os.path.isdir("/mnt/user-data/outputs") else os.getcwd()
    ordner = a[a.index("--ausgabe") + 1] if "--ausgabe" in a else std
    os.makedirs(ordner, exist_ok=True)
    d = load_data(quelle)
    if not d.get("person", {}).get("name"):
        sys.exit("FEHLER: person.name fehlt – ohne Namen kann ich keine Unterlagen bauen.")
    ensure_docx()
    erstellt = []
    if nur in (None, "lebenslauf"):
        erstellt.append(baue_lebenslauf(d, ordner))
    if nur in (None, "anschreiben"):
        if d.get("anschreiben", {}).get("absaetze"):
            erstellt.append(baue_anschreiben(d, ordner))
        else:
            print("Hinweis: Kein Anschreiben-Text in den Daten – Anschreiben übersprungen.")
    for p in list(erstellt):
        print(f"✅ Word: {p}")
        if "--kein-pdf" not in a:
            pdf, err = zu_pdf(p)
            print(f"✅ PDF:  {pdf}" if pdf else f"⚠️ {err}")
    fehl = pruef_luecken(d, nur)
    if fehl:
        print("⚠️ Fehlende Angaben: " + ", ".join(fehl))
    n = len(PRUEFEN_RE.findall(json.dumps(d, ensure_ascii=False)))
    if n:
        print(f"⚠️ {n} Stelle(n) mit [PRÜFEN: …] – gelb markiert, vor dem Abschicken klären.")
    print("Nächster Schritt: Dateien mit textlib.py wieder einlesen und endcheck.py laufen lassen.")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
