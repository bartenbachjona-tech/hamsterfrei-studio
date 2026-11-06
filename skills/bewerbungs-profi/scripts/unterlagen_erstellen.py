#!/usr/bin/env python3
"""Erzeugt Lebenslauf, Anschreiben/Motivationsschreiben/Kurzanschreiben, Formular- und
E-Mail-Texte – NUR aus der Profil-JSON (bzw. der Akte mit DATEN-Block).

    python3 unterlagen_erstellen.py PROFIL.json [--nur lebenslauf|anschreiben|formular|email]
                                    [--ausgabe ORDNER] [--nur-pdf] [--kein-pdf]
    python3 unterlagen_erstellen.py Bewerbungsakte_….txt   (liest den DATEN-Block)
    python3 unterlagen_erstellen.py --beispiel              (zeigt das Datenformat)

Ausgabe: /mnt/user-data/outputs (falls vorhanden), sonst aktueller Ordner.
Versionen: Der Nutzer sieht nur …_AKTUELL.pdf – genau EINE Datei je Unterlage. Frühere Fassungen
wandern intern nach alt/ (…_v1, …_v2; nichts wird gelöscht). Erst NACH der Freigabe im Chat erzeugen.
--nur-pdf: nur PDF ausgeben (Handy), .docx bleibt in alt/word/ als Sicherung.
Anlagen-Zeile im Anschreiben: automatisch aus profil.anlagen (nur Dateien, die es gibt) +
„Lebenslauf“. Kurzanschreiben: ohne Anlagen-Zeile (anschreiben.anlagen_zeile: true erzwingt sie).
Formular: Steht „max. N Zeichen“ schon im Feldnamen, wird es nicht doppelt angehängt.
Foto (person.foto): schwebend rechts neben dem Kopf, 3,5 × 4,5 cm. Stellen mit [PRÜFEN: …] werden gelb markiert und pro Dokument gezählt.
Layout: einspaltig, keine Tabellen/Grafiken, Tabstopp, Arial 11, A4 (ATS-lesbar).
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

SCHRIFT = "Arial"
GROESSE = 11
TAB_CM = 4.0
GRAU = "808080"
PRUEFEN_RE = re.compile(r"(\[PRÜFEN:[^\]]*\])")
TYPEN = {"anschreiben": "Anschreiben", "motivationsschreiben": "Motivationsschreiben",
         "kurzanschreiben": "Kurzanschreiben"}

BEISPIEL = {
    "schema": "bewerbungs-profi/3",
    "meta": {"stand": "06.11.2026", "phase": "4 Lebenslauf", "naechster_schritt": "Lebenslauf freigeben",
             "geraet": "handy", "anrede_form": "du", "modus": "normal", "fragen_gesamt": 10, "antworten_seit_akte": 0,
             "chat_plan": "Chat 1: Stelle + Profil · Chat 2: Unterlagen + Abschicken · Chat 3: Gespräch"},
    "person": {"name": "Lena Muster", "strasse": "Musterweg 1", "plz_ort": "85049 Ingolstadt",
               "telefon": "0151 23456789", "email": "lena.muster@example.de", "linkedin": "",
               "geburtsdatum": "", "foto": ""},
    "ziel": {"art": "Ausbildung", "stelle": "Kauffrau für Büromanagement", "firma": "Beispiel GmbH",
             "kennziffer": "AZ-2027-04", "ansprechperson": "Frau Petra Sommer", "anrede": "Sehr geehrte Frau Sommer,",
             "firma_adresse": ["Beispiel GmbH", "Personalabteilung", "Frau Petra Sommer", "Hauptstraße 5", "85049 Ingolstadt"],
             "link": "", "bewerbungsweg": "E-Mail", "frist": "31.01.2027", "start": "01.09.2027",
             "unterlagen_verlangt": ["Anschreiben", "Lebenslauf", "letzte zwei Zeugnisse"],
             "muss": ["Mittlere Reife"], "kann": ["Excel"], "schluesselwoerter": ["Sorgfalt", "Teamarbeit"],
             "auswahlverfahren": "Gespräch", "anschreiben_variante": "anschreiben", "upload_limit": "",
             "anzeige_text": "Ausbildung Kauffrau für Büromanagement (m/w/d) ab 01.09.2027 bei der Beispiel GmbH, "
                             "Hauptstraße 5, 85049 Ingolstadt. Kennziffer AZ-2027-04. Ansprechpartnerin: Frau Petra Sommer, "
                             "Personalabteilung. Dein Profil: Mittlere Reife, Sorgfalt, Teamarbeit, Excel von Vorteil. "
                             "Die Ausbildung dauert 3 Jahre. Bewerbung per E-Mail an ausbildung@beispiel.de mit Anschreiben, "
                             "Lebenslauf und den letzten zwei Zeugnissen bis 31.01.2027."},
    "profil": {
        "rohtext": [
            {"nr": 1, "frage": "Frage 1 – Kontaktdaten", "antwort": "Lena Muster, Musterweg 1, 85049 Ingolstadt, 0151 23456789, lena.muster@example.de"},
            {"nr": 2, "frage": "Frage 2 – Schule", "antwort": "Realschule Beispiel in Ingolstadt, 09/2020 bis 07/2026, Mittlere Reife mit 2,3. Wahlfach Wirtschaft, Schülerfirma"},
            {"nr": 3, "frage": "Frage 3 – Stationen", "antwort": "Minijob an der Kasse im Supermarkt Beispiel in Ingolstadt seit 09/2025, am Schichtende mach ich die Abrechnung selbst und beantworte Kundenfragen am Infopunkt. Schülerpraktikum im Steuerbüro Beispiel 03/2025, 2 Wochen, Belege sortiert und erfasst. Seit 2023 Jugendtrainerin Handball U12 beim TSV Beispiel"},
            {"nr": 4, "frage": "Frage 4 – Kenntnisse", "antwort": "Deutsch Muttersprache, Englisch B1, Word, Excel mit Formeln und Tabellen, PowerPoint"},
            {"nr": 5, "frage": "Frage 5 – Warum dieser Beruf?", "antwort": "Ich schließe Zahlen gern sauber und ohne Fehler ab, das merk ich an der Kasse. Die Abrechnung macht mir Spaß"},
            {"nr": 6, "frage": "Frage 6 – Warum diese Firma?", "antwort": "ihr bildet viele Azubis aus und ich bin mit dem Bus in 15 Minuten da"},
            {"nr": 7, "frage": "Frage 7 – Beispiel Teamarbeit", "antwort": "Schülerfirma, wir haben zu fünft einen Verkaufsstand geplant, ich hab die Kasse und die Abrechnung übernommen"},
            {"nr": 8, "frage": "Frage 8 – Start", "antwort": "ab 01.09.2027 passt"},
            {"nr": 9, "frage": "Frage 9 – Foto", "antwort": "nein"},
            {"nr": 10, "frage": "Frage 10 – Hobbys", "antwort": "Handball, ich trainiere die U12"},
            {"nr": 11, "frage": "Frage 11 – Wie aufmerksam geworden?", "antwort": "auf eurer Karriereseite, mein Lehrer hat sie mir gezeigt"}],
        "quellen": [],
        "bildung": [{"zeitraum": "09/2020 – 07/2026", "abschluss": "Mittlere Reife", "schule": "Realschule Beispiel, Ingolstadt",
                     "note": "2,3", "details": "Wahlfach Wirtschaft, Schülerfirma"}],
        "stationen": [
            {"zeitraum": "09/2025 – heute", "art": "Minijob", "titel": "Aushilfe Kasse", "firma": "Supermarkt Beispiel", "ort": "Ingolstadt",
             "taetigkeiten": ["Kassenabrechnung am Schichtende selbst gemacht", "Kundenfragen am Infopunkt beantwortet"], "ergebnisse": []},
            {"zeitraum": "03/2025, 2 Wochen", "art": "Schülerpraktikum", "titel": "Schülerpraktikum", "firma": "Steuerbüro Beispiel",
             "ort": "Ingolstadt", "taetigkeiten": ["Belege sortiert und erfasst"], "ergebnisse": []},
            {"zeitraum": "seit 2023", "art": "Ehrenamt", "titel": "Jugendtrainerin Handball (U12)", "firma": "TSV Beispiel",
             "ort": "", "taetigkeiten": [], "ergebnisse": []}],
        "luecken": [],
        "sprachen": [{"sprache": "Deutsch", "niveau": "Muttersprache"}, {"sprache": "Englisch", "niveau": "B1"}],
        "edv": ["Word", "Excel (Formeln, Tabellen)", "PowerPoint"],
        "fuehrerschein": "", "zertifikate": [],
        "wechselgrund": "", "abbruch_grund": "", "motivation_fach": "",
        "motivation_beruf": "Ich schließe Zahlen gern sauber und ohne Fehler ab (Kasse). Abrechnung macht Spaß.",
        "motivation_firma": "bildet viele Azubis aus; mit dem Bus 15 Minuten",
        "beispiele": [{"thema": "Teamarbeit", "stichwort": "Schülerfirma",
                       "situation": "Schülerfirma, Verkaufsstand", "aufgabe": "Stand zu fünft planen",
                       "handlung": "Kasse und Abrechnung übernommen", "ergebnis": ""}],
        "hobbys": ["Handball (Trainerin U12)"],
        "rahmen": {"start": "01.09.2027", "stunden": "", "verfuegbarkeit": "", "gehalt": "", "foto": False},
        "wie_aufmerksam": "Karriereseite, Hinweis vom Lehrer",
        "berufstest": {},
        "sonstiges": [],
        "anlagen": [{"datei": "/mnt/user-data/uploads/Zeugnis_10.pdf", "bezeichnung": "Zeugnis der 10. Klasse"}]
    },
    "firmenfakten": [{"fakt": "Azubis betreuen eigene Projekte", "quelle": "Karriereseite beispiel.de/karriere", "zugestimmt": False}],
    "belege": [],
    "lebenslauf": {
        "kurzprofil": "",
        "abschnitte": [
            {"titel": "Praktische Erfahrung", "eintraege": [
                {"zeitraum": "09/2025 – heute", "titel": "Aushilfe Kasse (Minijob)", "ort": "Supermarkt Beispiel, Ingolstadt",
                 "punkte": ["Kassenabrechnung am Schichtende selbst gemacht", "Kundenfragen am Infopunkt beantwortet"]},
                {"zeitraum": "03/2025", "titel": "Schülerpraktikum (2 Wochen)", "ort": "Steuerbüro Beispiel, Ingolstadt",
                 "punkte": ["Belege sortiert und erfasst"]}]},
            {"titel": "Schulbildung", "eintraege": [
                {"zeitraum": "09/2020 – 07/2026", "titel": "Mittlere Reife (Note 2,3)", "ort": "Realschule Beispiel, Ingolstadt",
                 "punkte": ["Wahlfach Wirtschaft, Schülerfirma: Verkaufsstand zu fünft geplant"]}]},
            {"titel": "Ehrenamt", "eintraege": [
                {"zeitraum": "seit 2023", "titel": "Jugendtrainerin Handball (U12)", "ort": "TSV Beispiel", "punkte": []}]}],
        "kenntnisse": [{"label": "Sprachen", "wert": "Deutsch (Muttersprache), Englisch (B1)"},
                       {"label": "EDV", "wert": "Word, Excel (Formeln, Tabellen), PowerPoint"}],
        "interessen": "Handball (Trainerin der U12)",
        "ort_datum_unterschrift": False},
    "anschreiben": {
        "typ": "anschreiben",
        "betreff": "Bewerbung um einen Ausbildungsplatz als Kauffrau für Büromanagement ab 01.09.2027 (Kennziffer AZ-2027-04)",
        "anrede": "Sehr geehrte Frau Sommer,",
        "absaetze": [
            "seit September 2025 mache ich an der Kasse eines Supermarkts die Abrechnung am Schichtende selbst. Die Abrechnung macht mir Spaß, weil ich Zahlen gern sauber und ohne Fehler abschließe.",
            "In Ihrer Anzeige nennen Sie Sorgfalt und Teamarbeit. In meinem Praktikum im Steuerbüro habe ich Belege sortiert und erfasst. In der Schülerfirma haben wir zu fünft einen Verkaufsstand geplant; ich habe die Kasse und die Abrechnung übernommen.",
            "Für die Beispiel GmbH spricht für mich, dass Sie viele Azubis ausbilden und ich Sie mit dem Bus in 15 Minuten erreiche.",
            "Ab dem 01.09.2027 kann ich bei Ihnen anfangen. Ich freue mich auf ein persönliches Gespräch."],
        "gruss": "Mit freundlichen Grüßen", "ort_datum": "", "anlagen_zeile": None},
    "formular": [
        {"feld": "Warum möchtest du zu uns? (max. 1000 Zeichen)", "limit": 1000,
         "text": "An der Kasse mache ich am Schichtende die Abrechnung selbst und merke dabei, dass ich Zahlen gern sauber abschließe. Sie bilden viele Azubis aus, und ich erreiche Sie mit dem Bus in 15 Minuten."},
        {"feld": "Frühester Eintrittstermin", "limit": 50, "text": "01.09.2027"},
        {"feld": "Wie sind Sie auf uns aufmerksam geworden?", "limit": 200,
         "text": "Über Ihre Karriereseite – mein Lehrer hat mich darauf hingewiesen."}],
    "email": {"betreff": "Bewerbung als Kauffrau für Büromanagement (Kennziffer AZ-2027-04)",
              "text": "Sehr geehrte Frau Sommer,\n\nanbei sende ich Ihnen meine Bewerbung um einen Ausbildungsplatz als Kauffrau für Büromanagement ab 01.09.2027. Im Juli 2026 habe ich meine Mittlere Reife an der Realschule Beispiel gemacht.\nAnschreiben, Lebenslauf und Zeugnis finden Sie in einer PDF im Anhang.\nFür Rückfragen erreichen Sie mich unter 0151 23456789.\n\nMit freundlichen Grüßen\nLena Muster"},
    "status": [{"unterlage": "Lebenslauf", "status": "Entwurf", "datei": "", "offen": ""}],
    "gespraech": {"termin": "", "art": "", "ort": "", "gespraechspartner": "", "einladung_text": "", "bestaetigt": False,
                  "mitbringen": [], "kernbotschaften": [], "selbstpraesentation": [], "schwierige_fragen": [],
                  "star": [], "eigene_fragen": [], "feedback": [], "ac_uebungen": []},
    "bewerbungen": [{"firma": "Beispiel GmbH", "stelle": "Kauffrau für Büromanagement", "abgeschickt": "", "status": "in Arbeit", "nachfassen": ""}],
    "entscheidungen": [{"datum": "06.11.2026", "text": "Volles Anschreiben, weil verlangt"}],
    "naechste_schritte": ["Lebenslauf freigeben", "Anschreiben"]
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
        if subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "python-docx", *extra],
                          capture_output=True, text=True).returncode == 0:
            break
    try:
        import docx  # noqa: F401
    except ImportError:
        sys.exit("FEHLER: python-docx ließ sich nicht installieren (kein Internet in der Sandbox?).\n"
                 "Ausweg: den eingebauten docx-Skill nutzen und das gleiche Layout nachbauen "
                 "(einspaltig, keine Tabellen, Überschriften wie hier).")


def ort_aus(plz_ort):
    m = re.match(r"^\s*\d{4,5}\s+(.+)$", plz_ort or "")
    return (m.group(1) if m else (plz_ort or "")).strip()


def heute():
    return datetime.date.today().strftime("%d.%m.%Y")


def zaehle_pruefen(*texte):
    return sum(len(PRUEFEN_RE.findall(t or "")) for t in texte)


# ---------------------------------------------------------------- Word-Bausteine
def _rahmen_grau(ppr):
    """Untere Linie grau (ersetzt auch die blaue Linie der Vorlage)."""
    from docx.oxml.ns import qn
    for alt in ppr.findall(qn("w:pBdr")):
        ppr.remove(alt)
    bdr = ppr.makeelement(qn("w:pBdr"), {})
    bdr.append(bdr.makeelement(qn("w:bottom"), {qn("w:val"): "single", qn("w:sz"): "6",
                                                 qn("w:space"): "1", qn("w:color"): GRAU}))
    ppr.append(bdr)


def neues_dokument(titel, autor):
    from docx import Document
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
    _rahmen_grau(h.element.get_or_add_pPr())
    t = doc.styles["Title"]
    t.font.size = Pt(13)
    _rahmen_grau(t.element.get_or_add_pPr())
    doc.core_properties.title = titel
    doc.core_properties.author = autor
    doc.core_properties.comments = ""
    return doc


def text(par, inhalt, bold=False, size=None):
    from docx.enum.text import WD_COLOR_INDEX
    from docx.shared import Pt
    for teil in PRUEFEN_RE.split(inhalt or ""):
        if not teil:
            continue
        r = par.add_run(teil)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if PRUEFEN_RE.fullmatch(teil) or teil == "??":
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
    for i, teil in enumerate(re.split(r"(\?\?)", links or "")):
        if teil:
            text(p, teil)
    text(p, "\t")
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


def notiz(doc, inhalt):
    from docx.shared import Cm
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(TAB_CM)
    text(p, inhalt)
    return p


def zeitraum_aufteilen(z):
    """[PRÜFEN] im Zeitraum sprengt die 4-cm-Spalte → in der Spalte nur „??“, Notiz darunter."""
    notizen = list(dict.fromkeys(PRUEFEN_RE.findall(z or "")))   # gleiche Notiz nur einmal
    if not notizen:
        return z, []
    kurz = re.sub(r"\s{2,}", " ", PRUEFEN_RE.sub("??", z)).strip()
    return kurz, notizen


FOTO_B_CM, FOTO_H_CM = 3.5, 4.5


def foto_rechts(par, pfad):
    """Bewerbungsfoto als schwebendes Bild (wp:anchor) rechts oben am Seitenrand, Text fließt links daneben.
    Hochformat 3,5 × 4,5 cm (zugeschnitten, nicht verzerrt)."""
    from docx.oxml.ns import qn
    from docx.shared import Cm
    from PIL import Image, ImageOps
    import copy
    import tempfile as _tf
    img = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")
    ziel = FOTO_B_CM / FOTO_H_CM
    w, h = img.size
    if w / h > ziel:                     # zu breit → seitlich zuschneiden
        nw = int(h * ziel)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:                                # zu hoch → oben/unten zuschneiden
        nh = int(w / ziel)
        img = img.crop((0, (h - nh) // 3, w, (h - nh) // 3 + nh))
    tmp = _tf.NamedTemporaryFile(suffix=".jpg", delete=False).name
    img.save(tmp, "JPEG", quality=90)
    run = par.add_run()
    run.add_picture(tmp, width=Cm(FOTO_B_CM), height=Cm(FOTO_H_CM))
    inline = run._r.find(qn("w:drawing")).find(qn("wp:inline"))
    emu_b, emu_h = int(Cm(FOTO_B_CM)), int(Cm(FOTO_H_CM))
    A = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    xml = (f'<wp:anchor xmlns:wp="{A}" distT="0" distB="0" distL="114300" distR="0" simplePos="0" relativeHeight="251659264" '
           f'behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0">'
           f'<wp:simplePos x="0" y="0"/>'
           f'<wp:positionH relativeFrom="margin"><wp:align>right</wp:align></wp:positionH>'
           f'<wp:positionV relativeFrom="paragraph"><wp:posOffset>0</wp:posOffset></wp:positionV>'
           f'<wp:extent cx="{emu_b}" cy="{emu_h}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
           f'<wp:wrapSquare wrapText="left"/></wp:anchor>')
    from lxml import etree
    anchor = etree.fromstring(xml)
    for tag in ("wp:docPr", "wp:cNvGraphicFramePr"):
        el = inline.find(qn(tag))
        if el is not None:
            anchor.append(copy.deepcopy(el))
    anchor.append(copy.deepcopy(inline.find(qn("a:graphic"))))
    inline.getparent().replace(inline, anchor)
    try:
        os.unlink(tmp)
    except OSError:
        pass


# ---------------------------------------------------------------- Lebenslauf
def baue_lebenslauf(d, ordner):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    pers, lv = d.get("person", {}), d.get("lebenslauf", {})
    name = pers.get("name", "").strip()
    doc = neues_dokument("Lebenslauf " + name, name)
    pruefen = 0
    foto = pers.get("foto")
    p = doc.add_paragraph(style="Title")
    p.paragraph_format.space_after = Pt(2)
    text(p, "Lebenslauf", size=13)
    if foto and os.path.isfile(foto):
        foto_rechts(p, foto)          # schwebend rechts neben Name/Kontakt – schiebt nichts nach unten
    elif foto:
        print(f"⚠️ Foto nicht gefunden: {foto} – Lebenslauf ohne Foto erstellt.")
    text(doc.add_paragraph(), name, bold=True, size=18)
    kontakt = [pers.get(k, "") for k in ("strasse", "plz_ort", "telefon", "email", "linkedin")]
    text(doc.add_paragraph(), " | ".join(k for k in kontakt if k))
    pruefen += zaehle_pruefen(*kontakt)
    if pers.get("geburtsdatum"):
        text(doc.add_paragraph(), "Geboren am " + pers["geburtsdatum"])
    if lv.get("kurzprofil"):
        doc.add_heading("Kurzprofil", level=1)
        text(doc.add_paragraph(), lv["kurzprofil"])
        pruefen += zaehle_pruefen(lv["kurzprofil"])
    for ab in lv.get("abschnitte", []):
        if not ab.get("eintraege"):
            continue
        doc.add_heading(ab.get("titel", "Stationen"), level=1)
        for e in ab["eintraege"]:
            zr, notizen = zeitraum_aufteilen(e.get("zeitraum", ""))
            rest = (", " + e["ort"]) if e.get("ort") else ""
            tab_absatz(doc, zr, e.get("titel", ""), rest)
            for pkt in e.get("punkte", []):
                punkt(doc, pkt)
            for n in notizen:
                notiz(doc, n)
            pruefen += zaehle_pruefen(e.get("zeitraum"), e.get("titel"), e.get("ort"), *e.get("punkte", []))
    if lv.get("kenntnisse"):
        doc.add_heading("Kenntnisse", level=1)
        for k in lv["kenntnisse"]:
            tab_absatz(doc, k.get("label", "") + ":", "", k.get("wert", ""))
            pruefen += zaehle_pruefen(k.get("label"), k.get("wert"))
    if lv.get("interessen"):
        doc.add_heading("Interessen", level=1)
        text(doc.add_paragraph(), lv["interessen"])
        pruefen += zaehle_pruefen(lv["interessen"])
    if lv.get("ort_datum_unterschrift"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(24)
        text(p, f"{ort_aus(pers.get('plz_ort'))}, {heute()}")
        text(doc.add_paragraph(), name)
    pfad, n = textlib.neue_version(ordner, "Lebenslauf_" + textlib.name_teile(name), ".docx")
    doc.save(pfad)
    return pfad, pruefen


# ---------------------------------------------------------------- Anlagen
def anlagen_liste(d):
    """Anlagen-Zeile aus tatsächlich vorhandenen Dateien. Gibt (liste, hinweise) zurück."""
    hinweise, liste = [], []
    if d.get("lebenslauf", {}).get("abschnitte"):
        liste.append("Lebenslauf")
    prof = d.get("profil", {}).get("anlagen")
    if prof is not None:
        for a in prof:
            datei, bez = a.get("datei", ""), a.get("bezeichnung") or os.path.basename(a.get("datei", ""))
            if datei and os.path.isfile(datei):
                liste.append(bez)
            else:
                hinweise.append(f"Anlage fehlt als Datei, nicht aufgeführt: {bez} ({datei or 'kein Pfad'})")
    elif d.get("anschreiben", {}).get("anlagen"):
        liste = list(d["anschreiben"]["anlagen"])
        hinweise.append("Anlagen-Zeile von Hand (anschreiben.anlagen) – nicht mit Dateien abgeglichen. "
                        "Besser profil.anlagen mit Dateipfaden füllen.")
    return liste, hinweise


# ---------------------------------------------------------------- Anschreiben
def baue_anschreiben(d, ordner):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    pers, ziel, an = d.get("person", {}), d.get("ziel", {}), d.get("anschreiben", {})
    typ = (an.get("typ") or ziel.get("anschreiben_variante") or "anschreiben").lower()
    if typ not in TYPEN:
        typ = "anschreiben"
    wort = TYPEN[typ]
    name = pers.get("name", "").strip()
    doc = neues_dokument(f"{wort} {name}", name)
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
    betreff = an.get("betreff") or f"Bewerbung als {ziel.get('stelle', '')}"
    text(p, betreff, bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    anrede = an.get("anrede") or ziel.get("anrede") or "Sehr geehrte Damen und Herren,"
    text(p, anrede)
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
    anl, hinw = anlagen_liste(d)
    # Regel: Kurzanschreiben ohne Anlagen-Zeile (die Dateien stehen ohnehin im Portal/der Mail);
    # anschreiben.anlagen_zeile: true erzwingt sie, false unterdrückt sie auch beim vollen Anschreiben.
    zeile_an = an.get("anlagen_zeile")
    if zeile_an is None:
        zeile_an = typ != "kurzanschreiben"
    if anl and zeile_an:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        text(p, "Anlagen: " + ", ".join(anl))
    pruefen = zaehle_pruefen(betreff, anrede, *an.get("absaetze", []))
    firma = textlib.safe_name(ziel.get("firma", ""), 30, "Firma")
    pfad, n = textlib.neue_version(ordner, f"{wort}_{textlib.name_teile(name)}_{firma}", ".docx")
    doc.save(pfad)
    return pfad, pruefen, hinw


# ---------------------------------------------------------------- Formular / E-Mail (.txt)
def baue_formular(d, ordner):
    felder = d.get("formular") or []
    zeilen, pruefen, warn = [], 0, []
    for f in felder:
        lim = f.get("limit")
        feld = (f.get("feld") or "Feld").strip()
        schon = re.search(r"max\.?\s*\d+\s*(Zeichen|Wörter|Worte)", feld, re.I)
        if schon and lim:   # Grenze steht schon im Feldtitel → nicht doppelt; die Zahl im Titel muss passen
            feld = re.sub(r"\s*\(?\s*max\.?\s*\d+\s*(Zeichen|Wörter|Worte)\s*\)?", "", feld, flags=re.I).strip()
        kopf = f"=== {feld}" + (f" (max. {lim} Zeichen)" if lim else (f" ({schon.group(0)})" if schon else "")) + " ==="
        t = (f.get("text") or "").strip()
        zeilen += [kopf, t, ""]
        pruefen += zaehle_pruefen(t)
        if lim and len(t) > int(lim):
            warn.append(f"Feld „{f.get('feld')}“: {len(t)} Zeichen, erlaubt {lim} – kürzen.")
    firma = textlib.safe_name(d.get("ziel", {}).get("firma", ""), 30, "Firma")
    pfad, _ = textlib.neue_version(ordner, f"Formular-Texte_{firma}", ".txt", mitziehen=(".txt",))
    open(pfad, "w", encoding="utf8").write("\n".join(zeilen).rstrip() + "\n")
    return pfad, pruefen, warn


def baue_email(d, ordner):
    e = d.get("email") or {}
    inhalt = f"Betreff: {e.get('betreff', '')}\n\n{(e.get('text') or '').strip()}\n"
    firma = textlib.safe_name(d.get("ziel", {}).get("firma", ""), 30, "Firma")
    pfad, _ = textlib.neue_version(ordner, f"E-Mail_Bewerbung_{firma}", ".txt", mitziehen=(".txt",))
    open(pfad, "w", encoding="utf8").write(inhalt)
    return pfad, zaehle_pruefen(inhalt), []


# ---------------------------------------------------------------- PDF
def zu_pdf(docx_pfad):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None, "LibreOffice fehlt – PDF bitte in Word erstellen (Datei → Speichern unter → PDF)."
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
    if nur in (None, "anschreiben") and d.get("anschreiben", {}).get("absaetze") and not d.get("ziel", {}).get("firma"):
        fehl.append("Firma (ziel.firma)")
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
    if nur in TYPEN:
        nur = "anschreiben"
    if nur not in (None, "lebenslauf", "anschreiben", "formular", "email"):
        sys.exit("FEHLER: --nur kennt lebenslauf, anschreiben (bzw. motivationsschreiben/kurzanschreiben), formular, email.")
    ordner = textlib.ausgabe_ordner(a[a.index("--ausgabe") + 1] if "--ausgabe" in a else None)
    os.makedirs(ordner, exist_ok=True)
    try:
        d = textlib.lade_profil(quelle)
    except RuntimeError as e:
        sys.exit(f"FEHLER: {e}")
    if not d.get("person", {}).get("name"):
        sys.exit("FEHLER: person.name fehlt – ohne Namen kann ich keine Unterlagen bauen.")
    nur_pdf, kein_pdf = "--nur-pdf" in a, "--kein-pdf" in a
    erstellt, warn = [], []          # (pfad, pruefen, ist_docx)
    if nur in (None, "lebenslauf") and d.get("lebenslauf", {}).get("abschnitte"):
        ensure_docx()
        p, n = baue_lebenslauf(d, ordner)
        erstellt.append((p, n, True))
    if nur in (None, "anschreiben"):
        if d.get("anschreiben", {}).get("absaetze"):
            ensure_docx()
            p, n, h = baue_anschreiben(d, ordner)
            erstellt.append((p, n, True))
            warn += h
        elif nur == "anschreiben":
            print("Hinweis: Kein Anschreiben-Text in den Daten – übersprungen.")
    if nur in (None, "formular") and d.get("formular"):
        p, n, h = baue_formular(d, ordner)
        erstellt.append((p, n, False))
        warn += h
    if nur in (None, "email") and (d.get("email") or {}).get("text"):
        p, n, h = baue_email(d, ordner)
        erstellt.append((p, n, False))
    if not erstellt:
        sys.exit("FEHLER: Nichts erzeugt – in der JSON fehlen lebenslauf/anschreiben/formular/email.")
    fehler = 0
    for p, n, ist_docx in erstellt:
        zeile = ""
        if ist_docx and not kein_pdf:
            pdf, err = zu_pdf(p)
            if pdf:
                if nur_pdf:
                    sich = os.path.join(ordner, "alt", "word")
                    os.makedirs(sich, exist_ok=True)
                    shutil.move(p, os.path.join(sich, os.path.basename(p)))
                    print(f"✅ PDF:  {pdf}")
                else:
                    print(f"✅ Word: {p}\n✅ PDF:  {pdf}")
            else:
                fehler += 1
                print(f"✅ Word: {p}\n⚠️ {err}")
        else:
            print(f"✅ {'Word' if ist_docx else 'Text'}: {p}")
        if n:
            zeile = f"   ⚠️ {n} offene [PRÜFEN: …]-Stelle(n) in diesem Dokument (gelb markiert)."
        print(zeile or "   ✅ keine [PRÜFEN]-Stellen in diesem Dokument.")
    for w in warn:
        print(f"⚠️ {w}")
    fehl = pruef_luecken(d, nur)
    if fehl:
        print("⚠️ Fehlende Angaben: " + ", ".join(fehl))
    if os.path.isdir(os.path.join(ordner, "alt")):
        print("📌 Für den Nutzer gilt nur …_AKTUELL. Frühere Fassungen liegen intern in alt/ – nicht erwähnen, nicht anbieten.")
    print("Nächster Schritt: fakten_check.py PROFIL.json <Dateien> – Treffer belegen, streichen oder nachfragen.")
    sys.exit(1 if fehler and not erstellt else 0)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
