#!/usr/bin/env python3
"""Endcheck für Bewerbungsunterlagen (Form und Stil – Fakten prüft fakten_check.py).

    python3 endcheck.py DATEI [DATEI …] --typ TYP [--firma "Beispiel GmbH"] [--stelle "Kauffrau …"]
                        [--profil PROFIL.json]

TYP: lebenslauf | anschreiben | motivationsschreiben | kurzanschreiben | formular | email | whatsapp | gesamt | anlage
     (gilt für alle Dateien des Aufrufs; ein Aufruf pro Dokumenttyp. Ohne --typ wird am INHALT geraten.)
     anlage = Zeugnis/Zertifikat (Scan/PDF): nur Format, Größe, Seiten – keine Textprüfung.
     gesamt = fertige Gesamt-PDF: [PRÜFEN], Platzhalter, Größe, Seiten – keine Stil-/Firmenprüfung (Scans!).
Firmenname und Stellenbezeichnung werden NUR in Anschreiben/Motivationsschreiben/Kurzanschreiben verlangt –
nicht in Formularfeldern, E-Mail oder WhatsApp (dort nur Warnung bei fremden Firmennamen). Wörter wie „Start“,
„ab“, Jahreszahlen oder „Vollzeit“ im Stellentitel muss der Betreff nicht wiederholen.
whatsapp = kurze Nachricht: 2–6 Sätze, Gruß + voller Name, keine Emoji-Ketten, Lebenslauf als PDF erwähnt.
--profil liefert Name, Firma, Stelle und frühere Arbeitgeber/Schulen (die sind kein Copy-and-paste-Rest).

v5 Stil-Check (alle Text-Typen): Umgangssprache („nix“, „mega“, „Kumpel“, „Ubahn“), Chat-Kürzel („vlt“, „lol“),
Tippfehler (Liste + Abgleich mit der Anzeige: „kommisioniert“ ↔ „Kommissionieren“), „Sa und So“/„Mo-Fr“, doppelte
Wörter, wiederholte Satzteile → ⚠️ mit Standard-Vorschlag. Unterlagen stehen in Standarddeutsch.
Mit --profil zusätzlich: Lebenslauf-Zeitraum zu lang für die Datumsspalte, Enddatum in der Zukunft ohne „voraussichtlich“.

Prüft u. a.: offene [PRÜFEN], Platzhalter, Floskeln, Konjunktiv, Länge, Seiten, Firmenname
(unscharf, ohne Rechtsform), ganze Stellenbezeichnung, fremde Firmennamen, Anrede, ATS-Layout,
E-Mail-Adresse (nur echte Probleme), Formular-Felder mit Zeichenlimit, Dateiname, Größe.
❌ = vor dem Abschicken beheben, ⚠️ = prüfen, ✅ = in Ordnung. Exit-Code 1 bei ❌.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402
import sprachlib  # noqa: E402

MAX_MB = 5
ANSCHR_MAX_WORTE = 420
KURZ_MIN, KURZ_MAX = 150, 200
TYPEN = ("lebenslauf", "anschreiben", "motivationsschreiben", "kurzanschreiben", "formular", "email", "whatsapp", "gesamt", "anlage")
BRIEF = ("anschreiben", "motivationsschreiben", "kurzanschreiben")

FLOSKELN = [   # (Regex, Anzeige) – auch gebeugte Formen und Konjunktiv-Schluss
    (r"hiermit\s+bewerbe\s+ich\s+mich", "hiermit bewerbe ich mich"), (r"\bhiermit\b", "hiermit"),
    (r"mit\s+gro(ß|ss)(em|er|en)\s+interesse", "mit großem Interesse"),
    (r"mit\s+gro(ß|ss)(er|en)\s+freude", "mit großer Freude"),
    (r"hat\s+mich\s+(sofort|direkt|sehr)\s+angesprochen", "hat mich sofort angesprochen"),
    (r"teamf(ä|ae)hig\w*\s*,\s*belastbar", "teamfähig, belastbar"), (r"belastbar\w*\s+und\s+flexibel", "belastbar und flexibel"),
    (r"w(ü|ue)rde(n)?\s+(ich\s+)?(mich|uns)\b[^.!?]{0,60}\bfreuen", "würde mich … freuen"),
    (r"(ü|ue)ber\s+eine\s+(positive\s+)?(r(ü|ue)ckmeldung|einladung)[^.!?]{0,60}w(ü|ue)rde", "über eine Einladung würde …"),
    (r"(der|die)\s+perfekte\s+(kandidat|kandidatin|besetzung)", "der/die perfekte Kandidat(in)"),
    (r"schnelllebigen\s+welt", "in einer schnelllebigen Welt"), (r"leidenschaft\s+f(ü|ue)r", "Leidenschaft für"),
    (r"renommiert(e|en|es|em|er)?\s+(unternehmen|firma|haus)", "Ihr renommiertes Unternehmen"),
    (r"ich\s+bin\s+(fest\s+)?(davon\s+)?(ü|ue)berzeugt,?\s+dass\s+ich", "ich bin überzeugt, dass ich"),
    (r"wertvoll(e|en|er)?\s+beitrag", "wertvoller Beitrag"), (r"dynamisch(e|en|es)?\s+team", "dynamisches Team"),
    (r"bereicher(n|ung)", "bereichern"), (r"mehrwert", "Mehrwert"),
]
KONJUNKTIV = re.compile(r"\b(würde|würden|hätte|hätten|könnte|könnten|möchte gerne|wäre)\b", re.I)
PLATZHALTER = re.compile(r"(\[(?!PRÜFEN)[^\]\n]{1,60}\]|\bXXX+\b|\bMusterfirma\b|\bLorem ipsum\b|\bFirma XY\b|\bHerr/Frau\b|_{4,}|\.\.\.\s*$)", re.I | re.M)
PRUEFEN = re.compile(r"\[PRÜFEN:[^\]]*\]")
# Rechtsformen nur als eigenes Wort und in genauer Schreibweise (v2: „Krankenkasse“ → „krankenkas“, „Augusta“ → „a usta“)
RECHTSFORM = re.compile(r"(?<![\wÄÖÜäöüß])(gGmbH|GmbH\s*&\s*Co\.?\s*KG|GmbH|AG\s*&\s*Co\.?\s*KG|AG|KGaA|KG|SE|e\.\s?V\.|eG|GbR|OHG|"
                        r"UG(?:\s*\(haftungsbeschränkt\))?|mbH|Holding)(?![\wÄÖÜäöüß])")
FIRMEN = re.compile(r"\b([A-ZÄÖÜ][\wÄÖÜäöüß&.\-]*(?:[ \t]+[A-ZÄÖÜ&][\wÄÖÜäöüß&.\-]*){0,3})[ \t]+(gGmbH|GmbH|AG|KG|SE|e\.\s?V\.|GbR|OHG|UG|KGaA)(?![\wÄÖÜäöüß])")
STANDARD_UEBERSCHRIFTEN = re.compile(r"(berufserfahrung|praktische erfahrung|praktika|ausbildung|schulbildung|bildung|studium)", re.I)
MAIL_RE = re.compile(r"\b([\w.+-]+)@([\w-]+\.[\w.]+)")
MAIL_PROBLEM = ["party", "sexy", "hot", "cool", "gangster", "babe", "baby", "maus", "mausi", "schatz", "hase", "prinz",
                "princess", "prinzessin", "killer", "lol", "crazy", "boss", "king", "queen", "swag", "girl", "boy",
                "love", "dark", "devil", "angel", "bunny", "gamer", "zocker", "chiller", "styler", "suess", "süß",
                "engel", "teufel", "bad", "xx", "420", "1337", "69", "drunk", "beer", "bier", "bitch", "thug", "ninja"]
FELD_KOPF = re.compile(r"^===\s*(.+?)\s*(?:\(max\.?\s*(\d{1,3}(?:[.\s]\d{3})+|\d+)\s*Zeichen\))?\s*===\s*$", re.M)
STELLE_META = {"start", "beginn", "ab", "bis", "zum", "jahr", "befristet", "unbefristet", "vollzeit", "teilzeit", "standort",
               "kennziffer", "stellen", "plaetze", "platz", "minijob", "basis", "deutschlandweit", "remote", "hybrid",
               "quereinstieg", "quereinsteiger", "quereinsteigerin", "wiedereinstieg", "wiedereinsteiger", "sommersemester",
               "wintersemester", "sose", "wise", "ref", "referenznummer"}


def kern_firma(s):
    s = RECHTSFORM.sub(" ", s or "")
    s = textlib.translit(s.lower())
    return [w for w in re.findall(r"[a-z0-9]+", s) if w not in ("und", "co", "der", "die", "das")]


def firma_im_text(firma, txt):
    kern = kern_firma(firma)
    if not kern:
        return "leer"
    t = set(re.findall(r"[a-z0-9]+", textlib.translit(txt.lower())))
    if all(k in t for k in kern):
        return "voll"
    if kern[0] in t:
        return "kurz"
    return "fehlt"


def stelle_kern(stelle):
    s = re.sub(r"\((?:m|w|d|f|x|div|gn)(?:\s*/\s*(?:m|w|d|f|x|div))*\)|\b[mwd]\s*/\s*[mwd](\s*/\s*[mwd])?\b", " ", stelle or "", flags=re.I)
    s = re.sub(r"/-?\s*(frau|mann|in|innen|r|e)\b|\*in(nen)?\b|:in(nen)?\b|\(in\)", "", s, flags=re.I)
    return [w for w in re.findall(r"[a-zäöüß0-9]{3,}", s.lower()) if w not in ("und", "für", "der", "die", "das", "als", "zum", "zur", "ausbildung")
            and textlib.translit(w) not in STELLE_META and not w.isdigit()]


def stamm(w):
    """Flexions-Toleranz: „Medizinische Fachangestellte“ = „Medizinischen Fachangestellten“."""
    w = textlib.translit(w.lower())
    return w[:max(4, len(w) - 3)] if len(w) > 5 else w


def stelle_fehlt(stelle, txt):
    woerter = set(re.findall(r"[a-z0-9]+", textlib.translit(txt.lower())))
    return [k for k in stelle_kern(stelle) if not any(x.startswith(stamm(k)) for x in woerter)]


def art_raten(txt):
    if FELD_KOPF.search(txt):
        return "formular"
    if re.match(r"\s*Betreff:", txt):
        return "email"
    if re.search(r"(sehr geehrte|mit freundlichen grüßen)", txt, re.I):
        return "anschreiben"
    return "lebenslauf"


def profil_infos(pfad):
    if not pfad:
        return {}
    d = textlib.lade_profil(pfad)
    pr = d.get("profil") or {}
    eigene = []
    for st in pr.get("stationen") or []:
        eigene += [st.get("firma", ""), st.get("ort", "")]
    for b in pr.get("bildung") or []:
        eigene.append(b.get("schule", ""))
    for e in ((d.get("lebenslauf") or {}).get("abschnitte") or []):
        for x in e.get("eintraege", []):
            eigene.append(x.get("ort", ""))
    return {"name": (d.get("person") or {}).get("name", ""), "firma": (d.get("ziel") or {}).get("firma", ""),
            "anzeige": (d.get("ziel") or {}).get("anzeige_text", ""),
            "zeitraeume": [e.get("zeitraum", "") for ab in ((d.get("lebenslauf") or {}).get("abschnitte") or [])
                           for e in ab.get("eintraege", [])],
            "stelle": (d.get("ziel") or {}).get("stelle", ""), "eigene": [e for e in eigene if e],
            "variante": (d.get("ziel") or {}).get("anschreiben_variante", ""),
            "bewerbungsweg": (d.get("ziel") or {}).get("bewerbungsweg", "")}


def mail_check(mails, name):
    out = []
    teile = [textlib.translit(t.lower()) for t in (name or "").split() if len(t) > 1]
    for lokal, dom in mails:
        l = textlib.translit(lokal.lower())
        gruende = []
        zahlen = re.findall(r"\d{3,}", l)
        if any(not re.fullmatch(r"(19|20)\d\d", z) for z in zahlen):   # Geburtsjahr („melis.k2007“) ist normal
            gruende.append("Zahlenfolge")
        tr = [w for w in MAIL_PROBLEM if w in re.split(r"[._\-+0-9]+", l) or (len(w) >= 4 and w in l)]
        if tr:
            gruende.append("Spitzname/Jugendsprache („" + tr[0] + "“)")
        if teile and not any(t in l for t in teile):
            gruende.append("enthält deinen Namen nicht")
        if gruende:
            out.append(f"⚠️ E-Mail {lokal}@{dom}: " + ", ".join(gruende) + " – für Bewerbungen besser vorname.nachname@…")
    return out


def pruefe_anlage(pfad, add):
    ext = os.path.splitext(pfad)[1].lower()
    mb = os.path.getsize(pfad) / 1024 / 1024
    if ext not in (".pdf", ".jpg", ".jpeg", ".png"):
        add("⚠️", f"Format {ext}: Portale wollen meist PDF (oder JPG/PNG). pdf_zusammenfuegen.py --einzeln wandelt um.")
    if mb > MAX_MB:
        add("⚠️", f"{mb:.1f} MB – zu groß für viele Portale (Richtwert < {MAX_MB} MB). Scan mit geringerer Auflösung.")
    if ext == ".pdf":
        try:
            seiten = textlib.read_pdf_text(pfad)[1]
            add("✅", f"PDF lesbar, {seiten or '?'} Seite(n), {mb:.2f} MB.")
        except RuntimeError as e:
            add("❌", f"PDF nicht lesbar: {e}")
    else:
        add("✅", f"Bilddatei, {mb:.2f} MB (für Portale am besten als PDF: pdf_zusammenfuegen.py --einzeln).")


def pruefe(pfad, typ=None, firma=None, stelle=None, info=None):
    info = info or {}
    befunde = []

    def add(sym, msg):
        befunde.append(f"{sym} {msg}")

    name = os.path.basename(pfad)
    if typ == "anlage":
        pruefe_anlage(pfad, add)
        return befunde, typ
    try:
        txt = textlib.read_any(pfad)
    except RuntimeError as e:
        return [f"❌ Nicht lesbar: {e}"], typ
    if not txt.strip():
        if typ == "gesamt":
            return ["⚠️ Kein Text gefunden – besteht die PDF nur aus Scans? Anschreiben/Lebenslauf müssen Text-PDFs sein."], typ
        return ["❌ Kein Text gefunden (Scan oder Grafik?). Nichts ist geprüft. ATS können so etwas nicht lesen."], typ
    geraten = typ is None
    art = typ or art_raten(txt)
    if geraten:
        add("ℹ️", f"Typ am Inhalt geraten: {art} (besser --typ angeben)")
    low = txt.lower()
    firma = firma or info.get("firma")
    stelle = stelle or info.get("stelle")

    n = PRUEFEN.findall(txt)
    if n:
        add("❌", f"{len(n)} offene [PRÜFEN: …]-Stelle(n): " + "; ".join(re.sub(r"\s+", " ", m)[:60] for m in n[:4]))
    ph_txt = FELD_KOPF.sub("", txt) if art == "formular" else txt
    ph = [p if isinstance(p, str) else p[0] for p in PLATZHALTER.findall(ph_txt)]
    ph = [p for p in ph if p.strip()]
    if ph:
        add("❌", "Platzhalter gefunden: " + ", ".join(sorted(set(ph))[:5]))
    if re.search(r"[^A-Za-z0-9_.\-]", name):
        add("⚠️", f"Dateiname „{name}“ enthält Umlaute, Sonderzeichen oder Leerzeichen – besser {textlib.safe_name(os.path.splitext(name)[0], 60)}{os.path.splitext(name)[1]}")
    if re.search(r"_(v\d+|AKTUELL)\.\w+$", name) and art not in ("formular", "email"):
        add("ℹ️", "Arbeitsdatei (…_AKTUELL). Zum Hochladen/Anhängen: Gesamt-PDF oder pdf_zusammenfuegen.py --einzeln (saubere Namen).")
    mb = os.path.getsize(pfad) / 1024 / 1024
    if mb > MAX_MB:
        add("⚠️", f"Datei ist {mb:.1f} MB groß (Richtwert unter {MAX_MB} MB, Vorgabe der Anzeige geht vor).")
    if art == "gesamt":
        if pfad.lower().endswith(".pdf"):
            seiten = textlib.read_pdf_text(pfad)[1]
            add("✅", f"Gesamt-PDF: {seiten or '?'} Seiten, {mb:.2f} MB.")
        if info.get("name") and not all(t.lower() in low for t in info["name"].split()[:1]):
            add("⚠️", "Dein Name kommt im Text nicht vor – ist das die richtige Datei?")
        if not any(b.startswith(("❌", "⚠️")) for b in befunde):
            add("✅", "Keine Auffälligkeiten (Stil/Fakten: Einzeldokumente prüfen).")
        return befunde, art
    mails = MAIL_RE.findall(txt)
    for m in mail_check(sorted(set(mails)), info.get("name")):
        befunde.append(m)
    if not mails and art in ("lebenslauf", "anschreiben", "motivationsschreiben"):
        add("❌", "Keine E-Mail-Adresse gefunden.")
    if pfad.lower().endswith(".pdf"):
        seiten = textlib.read_pdf_text(pfad)[1]
        if seiten:
            if art in BRIEF and seiten > 1:
                add("❌", f"{art.capitalize()} hat {seiten} Seiten – höchstens 1 Seite.")
            elif art == "lebenslauf" and seiten > 2:
                add("❌", f"Lebenslauf hat {seiten} Seiten – höchstens 2 (Einsteiger: 1).")
            elif art == "lebenslauf" and seiten == 2:
                add("⚠️", "Lebenslauf hat 2 Seiten – für Schüler/Einsteiger ist 1 Seite das Ziel.")
            else:
                add("✅", f"Seitenzahl: {seiten}")
        if art == "lebenslauf":
            h = textlib.pdf_spalten_hinweis(pfad)
            if h and h["mehrspaltig"]:
                add("⚠️", "Wahrscheinlich zweispaltig/Tabelle (einfache Erkennung) – ATS-Risiko, Seite als Bild ansehen.")
    if pfad.lower().endswith(".docx"):
        i = textlib.read_docx(pfad)["info"]
        if i["tabellen"] or i["textfelder"] or i["spalten"] > 1:
            add("⚠️", f"ATS-Risiko: {i['tabellen']} Tabelle(n), {i['textfelder']} Textfeld(er), {i['spalten']} Spalte(n).")
        else:
            add("✅", "Layout einspaltig, keine Tabellen oder Textfelder (ATS-freundlich).")

    # Firma / fremde Firmen
    if firma and art != "lebenslauf":
        if art in BRIEF:
            f = firma_im_text(firma, txt)
            if f == "fehlt":
                add("❌", f"Firmenname „{firma}“ kommt nicht vor (auch nicht ohne Rechtsform).")
            elif f == "kurz":
                add("✅", f"Firma als Kurzform erwähnt („{kern_firma(firma)[0]}“).")
        kern_ziel = set(kern_firma(firma))
        eigene = [set(kern_firma(e)) for e in info.get("eigene", [])]
        fremde = set()
        for m in FIRMEN.findall(txt):
            k = set(kern_firma(" ".join(m)))
            if not k or k & kern_ziel:
                continue
            if any(k & e for e in eigene):
                continue
            fremde.add(" ".join(m).strip())
        if fremde:
            add("⚠️", "Fremde Firmennamen im Text – Copy-and-paste-Rest? " + ", ".join(sorted(fremde)[:4]))
    # Stellenbezeichnung: nur im Brief (Betreff), mit Flexions-Toleranz
    if stelle and art in BRIEF:
        kern = stelle_kern(stelle)
        fehlt = stelle_fehlt(stelle, txt)
        if kern and len(fehlt) == len(kern):
            add("⚠️", f"Stellenbezeichnung „{stelle}“ nicht gefunden – im Betreff genau wie in der Anzeige nennen.")
        elif fehlt:
            add("⚠️", f"Stellenbezeichnung unvollständig – es fehlt: {', '.join(fehlt)} (genau wie in der Anzeige: „{stelle}“).")

    if art in BRIEF:
        worte = len(textlib.words(txt))
        if art == "kurzanschreiben":
            rumpf = len(textlib.words(re.sub(r"(?is)^.*?(sehr geehrte|guten tag|hallo|liebe[sr]? )", r"\1", txt)))
            if rumpf < KURZ_MIN or rumpf > KURZ_MAX:     # Text ab der Anrede (Kopf/Adressen zählen nicht)
                add("⚠️", f"{rumpf} Wörter ab der Anrede – Kurzanschreiben: {KURZ_MIN}–{KURZ_MAX} Wörter.")
            else:
                add("✅", f"{worte} Wörter – passt als Kurzanschreiben.")
        elif worte > ANSCHR_MAX_WORTE:
            add("❌", f"{worte} Wörter – zu lang für eine Seite. Kürzen (3–4 Absätze).")
        else:
            add("✅", f"{worte} Wörter.")
        if not re.search(r"(sehr geehrte|guten tag|hallo|liebe[sr]? )", low):
            add("⚠️", "Keine Anrede gefunden.")
        saetze = [x for x in re.split(r"(?<=[.!?])\s+", txt) if len(x.split()) > 3]
        ich = sum(1 for x in saetze if x.strip().startswith("Ich "))
        if saetze and ich / len(saetze) > 0.4:
            add("⚠️", f"{ich} von {len(saetze)} Sätzen beginnen mit „Ich“ – Satzanfänge variieren.")
    if art == "whatsapp":
        saetze_w = [x for x in re.split(r"(?<=[.!?])\s+", txt.strip()) if len(x.split()) >= 2]
        if len(saetze_w) > 7:
            add("⚠️", f"{len(saetze_w)} Sätze – per WhatsApp reichen 2–6 kurze Sätze (Lebenslauf hängt als PDF dran).")
        if info.get("name") and info["name"].split()[-1].lower() not in low:
            add("⚠️", "Voller Name fehlt am Ende (Gruß + Vor- und Nachname).")
        if len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", txt)) > 2:
            add("⚠️", "Mehrere Emojis – bei Bewerbungen höchstens eins.")
        if not re.search(r"lebenslauf", low):
            add("ℹ️", "Lebenslauf nicht erwähnt – als PDF mitschicken (Büroklammer → Dokument).")
    if art in BRIEF + ("formular", "email", "whatsapp"):
        gef = []
        for rx, label in FLOSKELN:
            if re.search(rx, low) and label not in gef:
                gef.append(label)
        if "hiermit bewerbe ich mich" in gef and "hiermit" in gef:
            gef.remove("hiermit")
        if gef:
            add("⚠️", "Floskeln, die Personaler oft als KI-/Standardtext lesen: " + ", ".join(f"„{g}“" for g in gef))
        k = [x for x in KONJUNKTIV.findall(txt)]
        if len(k) >= 2:
            add("⚠️", f"{len(k)}× Konjunktiv ({', '.join(sorted(set(x.lower() for x in k)))}) – direkter schreiben.")
    if art == "formular":
        felder = list(FELD_KOPF.finditer(txt))
        if not felder:
            add("⚠️", "Keine Feld-Überschriften (=== Feld ===) gefunden – Datei mit unterlagen_erstellen.py --nur formular bauen.")
        for i, m in enumerate(felder):
            ende = felder[i + 1].start() if i + 1 < len(felder) else len(txt)
            inhalt = txt[m.end():ende].strip()
            if not inhalt:
                add("❌", f"Feld „{m.group(1)}“ ist leer.")
            elif m.group(2) and len(inhalt) > int(re.sub(r"\D", "", m.group(2))):
                add("❌", f"Feld „{m.group(1)}“: {len(inhalt)} Zeichen, erlaubt {m.group(2)}.")
            if re.search(r"siehe (lebenslauf|anlage|anhang)", inhalt, re.I):
                add("❌", f"Feld „{m.group(1)}“: „siehe Lebenslauf“ – Feld richtig ausfüllen.")
    if art == "email":
        worte = len(textlib.words(txt))
        mail_ist_anschreiben = "mail" in (info.get("variante") or "").lower()
        if worte > 140 and not mail_ist_anschreiben:
            add("⚠️", f"E-Mail hat {worte} Wörter – in der Mail reichen 3–5 Sätze (das Anschreiben hängt als PDF an).")
        if not re.search(r"(sehr geehrte|guten tag|hallo|liebe[sr]? )", low):
            add("⚠️", "E-Mail ohne Anrede.")
    if art in BRIEF + ("formular", "email", "whatsapp", "lebenslauf"):
        for msg, vorschlag in sprachlib.stil_befunde(txt, referenz=[info.get("anzeige", "")], lebenslauf=(art == "lebenslauf")):
            add("⚠️", f"Stil: {msg} → {vorschlag}")
    if art == "lebenslauf":
        for zr in info.get("zeitraeume") or []:
            if len(zr) > 17:
                add("⚠️", f"Zeitraum „{zr}“ ist zu lang für die Datumsspalte (max. ~17 Zeichen) – kürzen; der Rest gehört "
                          "unter den Titel (unterlagen_erstellen.py setzt ihn als Notiz darunter).")
            for mo, jahr in re.findall(r"(?:–|-|bis)\s*(\d{1,2})/(\d{4})", zr):
                if (int(jahr), int(mo)) > (datetime.date.today().year, datetime.date.today().month) and \
                        not re.search(r"voraussichtlich|geplant|bis vorauss", zr, re.I):
                    add("⚠️", f"Enddatum {mo}/{jahr} liegt in der Zukunft – „voraussichtlich“ davor schreiben oder „seit …“.")
        if "€" in txt:
            add("⚠️", "„€“ gefunden – für ATS besser „EUR“ schreiben.")
        if not STANDARD_UEBERSCHRIFTEN.search(txt):
            add("⚠️", "Keine Standard-Überschrift wie „Berufserfahrung“, „Ausbildung“ oder „Schulbildung“ gefunden.")
    if not any(b.startswith(("❌", "⚠️")) for b in befunde):
        add("✅", "Keine Auffälligkeiten.")
    return befunde, art


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    opts = {}
    for k in ("--firma", "--stelle", "--typ", "--profil"):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    typ = opts.get("--typ")
    if typ and typ not in TYPEN:
        print(f"FEHLER: --typ kennt {', '.join(TYPEN)}")
        sys.exit(2)
    try:
        info = profil_infos(opts.get("--profil"))
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(2)
    if typ == "kurzanschreiben" and info.get("variante") and info["variante"] != "kurzanschreiben":
        print(f"ℹ️ Laut Profil ist die Variante „{info['variante']}“ – geprüft wird trotzdem als Kurzanschreiben.")
    fehler = 0
    for d in a:
        if not os.path.isfile(d):
            print(f"❌ Datei nicht gefunden: {d}")
            fehler += 1
            continue
        bef, art = pruefe(d, typ, opts.get("--firma"), opts.get("--stelle"), info)
        print(f"\n## {os.path.basename(d)} ({art or '?'})")
        for b in bef:
            print(b)
        fehler += sum(1 for b in bef if b.startswith("❌"))
    print(f"\n---\n{'❌ ' + str(fehler) + ' Punkt(e) vor dem Abschicken beheben.' if fehler else '✅ Keine ❌-Befunde.'}"
          "\nFakten prüft fakten_check.py. Rechtschreibung trotzdem selbst lesen – laut oder von einer zweiten Person.")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
