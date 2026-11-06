#!/usr/bin/env python3
"""Bewerbungsakte schreiben und lesen – billig aus der Profil-JSON, ohne Tipparbeit.

    python3 akte.py PROFIL.json [--pdf] [--ausgabe ORDNER]
        → Bewerbungsakte_Vorname_Nachname_JJJJ-MM-TT_HHMMSS.txt (eindeutig, öffnet auf jedem Handy/PC):
          oben lesbar (inkl. „im neuen Chat wieder hochladen: …“), unten die Daten zum Weitermachen.
          Nur .txt hochladen! --pdf (nur auf Wunsch) erzeugt zusätzlich Akte-Lesefassung_….pdf
          (anderer Name, damit niemand die PDF statt der .txt hochlädt). Ältere Akten im Ordner → alt/.
    python3 akte.py --lesen AKTE.txt|ORDNER [--json-nach /tmp/bewerbung/profil.json]
        → holt die JSON aus einer hochgeladenen Akte (auch v1–v3; auch umbenannt wie „Bewerbungsakte (1).txt“ –
          ohne Pfad wird die neueste Akte in den Uploads genommen), ordnet Anlagen in den neuen Uploads zu
          (gleicher Name, gleicher Inhalt, „IMG_2041 (1).jpg“) und sagt, was noch einmal hochgeladen werden muss.
    python3 akte.py PROFIL.json --spickzettel [--pdf] [--a4]
        → Gespraech_Spickzettel_Firma_AKTUELL.txt (+ PDF, Standard kompakt A5 fürs Handy, --a4 zum Drucken):
          Termin | Art | Ort, Kernbotschaften, Vorstellung (Dauer aus der Einladung), schwierige Fragen NUR mit
          antwort_final, Fachfragen, Beispiele, gewählte eigene Fragen, AC-Übungen mit typpassendem Tipp,
          Mitbring-Liste, Tipps; Du- oder Sie-Form (gespraech.anrede). Feedback/Notizen bleiben intern.
          Gibt Hinweise für Claude aus (Ort/Termin ≠ Einladung, offene Gehaltsfrage …).
          Vorher: fakten_check.py … --typ spickzettel
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

LINIE = "-" * 60
UPLOADS = os.environ.get("BP_UPLOADS", "/mnt/user-data/uploads")


def zeile(label, wert):
    if isinstance(wert, list):
        wert = ", ".join(str(x) for x in wert if x)
    return f"{label}: {wert if wert not in ('', None) else '(offen)'}"


def zeile_wenn(out, label, wert):
    if isinstance(wert, list):
        wert = ", ".join(str(x) for x in wert if x)
    if wert not in ("", None):
        out.append(f"{label}: {wert}")


def station_text(s):
    titel, art = s.get("titel", ""), s.get("art", "")
    if art and titel and titel.lower() in art.lower():
        titel = art                     # „Aushilfe“ + „Aushilfe (20 Std./Woche)“ → nicht doppelt klammern
    elif art and art.lower() not in titel.lower():
        titel = f"{titel} ({art})" if titel else art
    teile = [s.get("zeitraum", ""), titel]
    ort = ", ".join(x for x in (s.get("firma", ""), s.get("ort", "")) if x)
    return " ".join(x for x in teile if x) + (f", {ort}" if ort else "")


def wieder_hochladen(d):
    """Liste der Dateien, die im neuen Chat wieder hochgeladen werden müssen – jede Datei nur einmal."""
    pr = d.get("profil") or {}
    liste, gesehen = [], set()

    def dazu(pfad, bez):
        b = os.path.basename(pfad or "")
        if b and b.lower() not in gesehen:
            gesehen.add(b.lower())
            liste.append(f"{b} ({bez})")
    for a in pr.get("anlagen") or []:
        dazu(a.get("datei"), a.get("bezeichnung") or "Anlage")
    if (d.get("person") or {}).get("foto"):
        dazu(d["person"]["foto"], "Bewerbungsfoto")
    for q in pr.get("quellen") or []:
        dazu(q if isinstance(q, str) else q.get("datei", ""), "Upload")
    return liste


def lesbar(d):
    p, z, pr, m = d.get("person") or {}, d.get("ziel") or {}, d.get("profil") or {}, d.get("meta") or {}
    jetzt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    out = [f"BEWERBUNGSAKTE – {p.get('name', '') or '(Name noch offen)'}",
           "Im neuen Chat DIESE .txt-Datei hochladen und schreiben: „Weiter mit meiner Bewerbung“.",
           "Enthält persönliche Daten – privat speichern, nicht teilen.", ""]
    hoch = wieder_hochladen(d)
    if hoch:
        out.append("Im neuen Chat diese Dateien bitte noch einmal mit hochladen (ein neuer Chat sieht alte Uploads nicht):")
        out += [f"  - {h}" for h in hoch]
        out.append("Lebenslauf und Anschreiben baut Claude aus dieser Akte neu – die musst du nicht hochladen.")
        out.append("")
    out += [f"Stand: {jetzt}", zeile("Phase", m.get("phase")), zeile("Nächster Schritt", m.get("naechster_schritt"))]
    zeile_wenn(out, "Fahrplan", m.get("chat_plan"))
    zeile_wenn(out, "Gerät", m.get("geraet"))
    out += ["", LINIE, "ZIEL", LINIE]
    for k, lab in (("art", "Art"), ("stelle", "Stelle"), ("firma", "Firma"), ("link", "Link"), ("kennziffer", "Kennziffer"),
                   ("ansprechperson", "Ansprechperson"), ("bewerbungsweg", "Bewerbungsweg"), ("frist", "Frist"),
                   ("start", "Start"), ("unterlagen_verlangt", "Verlangte Unterlagen"), ("upload_limit", "Upload-Limit"),
                   ("muss", "Muss"), ("kann", "Kann"), ("auswahlverfahren", "Auswahlverfahren"),
                   ("anschreiben_variante", "Anschreiben-Variante")):
        zeile_wenn(out, lab, z.get(k))
    bt = pr.get("berufstest") or {}
    if bt:
        out += ["", LINIE, "BERUFSTEST", LINIE]
        zeile_wenn(out, "Ergebnis (Code)", bt.get("code"))
        zeile_wenn(out, "Stärkste Bereiche", bt.get("bereiche") or bt.get("punkte"))
        zeile_wenn(out, "Vorschläge", bt.get("vorschlaege"))
        zeile_wenn(out, "Gewählt", bt.get("gewaehlt"))
    out += ["", LINIE, "PROFIL (deine Angaben)", LINIE]
    for b in pr.get("bildung") or []:
        out.append(f"- Bildung: {b.get('zeitraum', '')} {b.get('abschluss', '')}, {b.get('schule', '')}".replace(" ,", ",")
                   + (f", Note {b['note']}" if b.get("note") else ""))
    for s in pr.get("stationen") or []:
        out.append(f"- Station: {station_text(s)}")
        for t in (s.get("taetigkeiten") or []) + (s.get("ergebnisse") or []):
            out.append(f"    · {t}")
    for l in pr.get("luecken") or []:   # Feld heißt „erklaerung“ („grund“ geht auch)
        out.append(f"- Lücke: {l.get('zeitraum', '')} – {l.get('erklaerung') or l.get('grund') or '(Erklärung offen)'}")
    if pr.get("sprachen"):
        out.append(zeile("Sprachen", [f"{s.get('sprache')} ({s.get('niveau')})" if s.get("niveau") else s.get("sprache")
                                      for s in pr["sprachen"]]))
    zeile_wenn(out, "EDV", pr.get("edv"))
    zeile_wenn(out, "Führerschein", pr.get("fuehrerschein"))
    zeile_wenn(out, "Zertifikate/Scheine", pr.get("zertifikate"))
    zeile_wenn(out, "Wechselgrund", pr.get("wechselgrund"))
    zeile_wenn(out, "Grund Studien-/Ausbildungsabbruch", pr.get("abbruch_grund"))
    zeile_wenn(out, "Warum dieses Fach", pr.get("motivation_fach"))
    out.append(zeile("Warum dieser Beruf", pr.get("motivation_beruf")))
    out.append(zeile("Warum diese Firma", pr.get("motivation_firma")))
    for b in pr.get("beispiele") or []:
        out.append(f"- Beispiel ({b.get('thema', '')}): {b.get('situation', '')} → {b.get('handlung', '')} → "
                   f"{b.get('ergebnis', '') or '(Ergebnis offen)'}")
    zeile_wenn(out, "Hobbys", pr.get("hobbys"))
    r = pr.get("rahmen") or {}
    zeile_wenn(out, "Start/Verfügbarkeit", " · ".join(x for x in (r.get("start", ""), r.get("stunden", ""), r.get("verfuegbarkeit", "")) if x))
    out.append(zeile("Foto", {True: "ja", False: "nein"}.get(r.get("foto"), "(offen)")))
    zeile_wenn(out, "Wie auf die Stelle aufmerksam", pr.get("wie_aufmerksam"))
    if d.get("firmenfakten"):
        out.append("Firmenfakten aus Recherche:")
        for f in d["firmenfakten"]:
            out.append(f"    · {f.get('fakt')} (Quelle: {f.get('quelle')}; im Text: {'ja' if f.get('zugestimmt') else 'nein'})")
    out += ["", LINIE, "STATUS DER UNTERLAGEN", LINIE]
    for s in d.get("status") or []:
        out.append(f"- {s.get('unterlage')}: {s.get('status')}" + (f" – {s.get('datei')}" if s.get("datei") else "")
                   + (f" – offen: {s.get('offen')}" if s.get("offen") else ""))
    gs = d.get("gespraech") or {}
    if any(gs.get(k) for k in ("termin", "art", "star", "eigene_fragen", "feedback")):
        out += ["", LINIE, "GESPRÄCH / AUSWAHLTAG", LINIE]
        zeile_wenn(out, "Termin | Art | Ort", " | ".join(x for x in (gs.get("termin", ""), gs.get("art", ""), gs.get("ort", "")) if x))
        if gs.get("termin"):
            out.append(f"Termin bestätigt: {'ja' if gs.get('bestaetigt') else 'noch nicht'}")
        for f in gs.get("feedback") or []:
            out.append(f"- Feedback: {f if isinstance(f, str) else (f.get('frage', '') + ': ' + (f.get('besser') or f.get('kurz', '')))}")
    if d.get("bewerbungen"):
        out += ["", LINIE, "ALLE BEWERBUNGEN", LINIE]
        for b in d["bewerbungen"]:
            out.append(f"- {b.get('firma')} | {b.get('stelle')} | abgeschickt: {b.get('abgeschickt') or '–'} | "
                       f"{b.get('status')} | nachfassen: {b.get('nachfassen') or '–'}")
    if d.get("entscheidungen"):
        out += ["", LINIE, "ENTSCHEIDUNGEN", LINIE]
        for e in d["entscheidungen"]:
            out.append(f"- {e.get('datum', '')}: {e.get('text', '')}" if isinstance(e, dict) else f"- {e}")
    out += ["", LINIE, "NÄCHSTE SCHRITTE", LINIE]
    for i, s in enumerate((d.get("naechste_schritte") or [])[:3], 1):
        out.append(f"{i}. {s}")
    return "\n".join(out) + "\n"


def txt_zu_pdf(txt, pdf_ziel):
    so = shutil.which("soffice") or shutil.which("libreoffice")
    if not so:
        return "LibreOffice fehlt – keine PDF (die .txt reicht)."
    with tempfile.TemporaryDirectory() as tmp:
        quelle = os.path.join(tmp, os.path.splitext(os.path.basename(pdf_ziel))[0] + ".txt")
        open(quelle, "w", encoding="utf8").write(txt)
        r = subprocess.run([so, "--headless", "--infilter=Text (encoded):UTF8,LF,Liberation Sans,de-DE",
                            "--convert-to", "pdf", "--outdir", tmp, quelle],
                           capture_output=True, text=True, timeout=180, env=dict(os.environ, HOME=tmp))
        erzeugt = os.path.splitext(quelle)[0] + ".pdf"
        if r.returncode != 0 or not os.path.isfile(erzeugt):
            return "PDF-Umwandlung fehlgeschlagen (die .txt reicht)."
        shutil.move(erzeugt, pdf_ziel)
    return None


def alte_wegraeumen(ordner, praefixe):
    for f in os.listdir(ordner):
        if f.startswith(praefixe) and os.path.splitext(f)[1].lower() in (".txt", ".pdf", ".md"):
            alt = os.path.join(ordner, "alt")
            os.makedirs(alt, exist_ok=True)
            ziel = os.path.join(alt, f)
            if not os.path.exists(ziel):
                shutil.move(os.path.join(ordner, f), ziel)


def schreibe_akte(d, ordner, pdf=False):
    os.makedirs(ordner, exist_ok=True)
    name = textlib.name_teile((d.get("person") or {}).get("name", "")) or "Name"
    praefix = f"Bewerbungsakte_{name}"
    lese = f"Akte-Lesefassung_{name}"
    alte_wegraeumen(ordner, (praefix, lese))
    stempel = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    pfad, n = os.path.join(ordner, f"{praefix}_{stempel}.txt"), 2
    while os.path.exists(pfad) or os.path.exists(os.path.join(ordner, "alt", os.path.basename(pfad))):
        pfad, n = os.path.join(ordner, f"{praefix}_{stempel}_{n}.txt"), n + 1
    meta = d.setdefault("meta", {})
    meta["stand"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    for a in (d.get("profil") or {}).get("anlagen") or []:     # Fingerabdruck: Re-Upload unter anderem Namen erkennen
        if a.get("datei") and os.path.isfile(a["datei"]):
            a["sha1"], a["bytes"] = datei_hash(a["datei"]), os.path.getsize(a["datei"])
    foto = (d.get("person") or {}).get("foto")
    if foto and os.path.isfile(foto):
        d["person"]["foto_sha1"] = datei_hash(foto)
    meta["antworten_seit_akte"] = 0
    d["schema"] = "bewerbungs-profi/4"
    les = lesbar(d)
    voll = les + "\n\n" + textlib.AKTE_START + "\n" + json.dumps(d, ensure_ascii=False, indent=1) + "\n" + textlib.AKTE_ENDE + "\n"
    open(pfad, "w", encoding="utf8").write(voll)
    ergebnis = [pfad]
    if pdf:
        p = os.path.join(ordner, os.path.basename(pfad).replace(praefix, lese, 1).replace(".txt", ".pdf"))
        err = txt_zu_pdf(les, p)
        ergebnis.append(p if not err else err)
    return ergebnis


# ---------------------------------------------------------------- Spickzettel (v4)
# Datenstruktur (gespraech): anrede du|sie · vorstellung{dauer_min, kernpunkte[]} · kernbotschaften[] ·
# schwierige_fragen[{frage, antwort_final}] · fachfragen[{frage, antwort_final}] · eigene_fragen[{frage, gewaehlt}] ·
# mitbringen[] · ac_uebungen[{typ, titel, dauer_min, tipp}] · gehalt{antwort_final}. feedback bleibt INTERN.
TIPPS = {
    "praesenz": ["10 Minuten vor der Zeit da sein, Weg vorher prüfen",
                 "Kleidung eine Stufe formeller als im Betrieb üblich",
                 "Handy lautlos, Blickkontakt, ausreden lassen",
                 "Am Ende fragen: Wie geht es weiter, wann höre ich von Ihnen?"],
    "video": ["Link, Kamera, Ton und Akku 30 Minuten vorher testen",
              "Licht von vorn, ruhiger Hintergrund, Kamera auf Augenhöhe",
              "In die Kamera schauen, Benachrichtigungen aus",
              "Telefonnummer für Technikprobleme bereithalten"],
    "telefon": ["Ruhiger Ort, gutes Netz, Akku voll",
                "Lebenslauf, dieser Zettel und ein Stift griffbereit",
                "Im Stehen sprechen und lächeln – man hört es",
                "Namen der Gesprächspartner notieren"],
    "ac": ["Pünktlich, ausgeschlafen, etwas zu essen und zu trinken dabei",
           "Jede Entscheidung kurz begründen",
           "Auch Pausen und Mittagessen gehören dazu – freundlich und echt bleiben"],
    "probearbeit": ["Pünktlich sein, Kleidung und Schuhe wie in der Einladung",
                    "Mit anpacken, nachfragen, wenn etwas unklar ist",
                    "Vorher klären: Wird das Probearbeiten bezahlt?",
                    "Am Ende nach Rückmeldung und nächstem Schritt fragen"],
}
MITBRINGEN = {
    "praesenz": ["Lebenslauf und Anschreiben ausgedruckt", "Zeugnisse (Kopien)", "Stift und Notizzettel"],
    "video": ["Zugangslink", "Ladekabel", "Notizzettel und Glas Wasser"],
    "telefon": ["Lebenslauf und Anzeige", "Notizzettel und Stift"],
    "ac": ["Einladung", "Lebenslauf ausgedruckt", "Stift, Notizblock, Uhr", "Verpflegung"],
    "probearbeit": ["Passende Kleidung und Schuhe", "Einladung", "Getränk"],
}
AC_TYPEN = [   # Reihenfolge zählt: Selbstpräsentation vor Präsentation, Fallstudie vor Präsentation
    ("selbstpraesentation", r"selbst\s*präsentation|selbstpraesentation|selbstvorstellung|vorstellungsrunde|stell\w* (dich|sich) vor|"
                            r"warum ich|über mich|ueber mich|mein weg|meine person|pitch|elevator"),
    ("fallstudie", r"fall\s*studie|fallstudie|case|fallaufgabe|analyse"),
    ("gruppe", r"gruppen\s*diskussion|gruppendiskussion|gruppen\s*aufgabe|gruppenaufgabe|gruppenübung|gruppenuebung|teamaufgabe|"
               r"teamübung|teamuebung|gruppenarbeit|diskussion"),
    ("postkorb", r"postkorb|in-?box|e-?mail-übung|priorisier"),
    ("rollenspiel", r"rollen\s*spiel|rollenspiel|kundengespräch|kundengespraech|mitarbeitergespräch|konfliktgespräch"),
    ("praesentation", r"präsentation|praesentation|vortrag|referat"),
    ("interview", r"interview|einzelgespräch|einzelgespraech|gespräch|gespraech"),
    ("test", r"test|aufgaben|rechnen|logik|konzentration|wissen"),
]
AC_TIPP = {
    "selbstpraesentation": "frei sprechen: heute → Weg → warum hier; Zeit einhalten, Blick in die Runde",
    "praesentation": "Kernaussage zuerst → 2–3 Punkte mit Beispiel → kurzes Fazit; Zeit einhalten",
    "fallstudie": "Problem → Ursachen → Optionen → Empfehlung, Zahlen kurz nachrechnen",
    "gruppe": "Position beziehen, andere einbeziehen (mit Namen), Zeit im Blick, am Ende zusammenfassen",
    "postkorb": "A sofort / B planen oder delegieren / C später – jede Entscheidung begründen",
    "rollenspiel": "zuhören, ruhig bleiben, konkrete Lösung zusagen",
    "interview": "wie ein Vorstellungsgespräch – deine Beispiele nutzen",
    "test": "ruhig bleiben, schwere Aufgaben überspringen und später zurück",
}
INTERN_RE = re.compile(r"(\(?vorschlag\s+claude|\bintern\b|\bnotiz\s*:|\btodo\b|\bclaude\b|nicht in unterlagen|\bnutzer(in)?\b|"
                       r"\bbewerber(in)?\b|coaching|\bfeedback\s*:|verbesser(t|ung)\s*:)", re.I)
DRITTE_PERSON = re.compile(r"\b(er|sie) (hat|ist|war|will|möchte|sagt|findet|soll|hätte|wollte|freut|kann)\b|\bsich gefreut hat\b")


def art_schluessel(gs, z):
    a = textlib.translit(f"{gs.get('art', '')} {z.get('auswahlverfahren', '') if not gs.get('art') else ''}".lower())
    if re.search(r"assessment|\bac\b|auswahltag|auswahlverfahren", a):
        return "ac", "Auswahltag"
    if "probe" in a or "schnupper" in a:
        return "probearbeit", "Probearbeiten"
    if "video" in a or "teams" in a or "zoom" in a or "online" in a:
        return "video", "Videogespräch"
    if "telefon" in a:
        return "telefon", "Telefoninterview"
    return "praesenz", "Gespräch vor Ort"


TIPPS_KOPF = {  # grammatisch passend (v3-Fehler: „Tipps für dein Auswahltag“)
    "du": {"ac": "Tipps für deinen Auswahltag", "praesenz": "Tipps für dein Gespräch", "video": "Tipps für dein Videogespräch",
           "telefon": "Tipps für dein Telefoninterview", "probearbeit": "Tipps für dein Probearbeiten"},
    "sie": {"ac": "Tipps für Ihren Auswahltag", "praesenz": "Tipps für Ihr Gespräch", "video": "Tipps für Ihr Videogespräch",
            "telefon": "Tipps für Ihr Telefoninterview", "probearbeit": "Tipps für Ihr Probearbeiten"},
}
KOPF = {
    "du": {"kern": "Deine 3 Kernbotschaften", "vor": "So stellst du dich vor", "schwer": "Schwierige Fragen – deine Antwort",
           "fach": "Fachfragen – deine Antwort", "bsp": "Deine Beispiele", "eigen": "Deine Fragen an die Firma",
           "ac": "Dein Auswahltag – die Übungen", "mit": "Mitbringen", "offen": "noch offen – vor dem Termin klären",
           "beispiele_nutzen": "deine Beispiele nutzen"},
    "sie": {"kern": "Ihre 3 Kernbotschaften", "vor": "So stellen Sie sich vor", "schwer": "Schwierige Fragen – Ihre Antwort",
            "fach": "Fachfragen – Ihre Antwort", "bsp": "Ihre Beispiele", "eigen": "Ihre Fragen an die Firma",
            "ac": "Ihr Auswahltag – die Übungen", "mit": "Mitbringen", "offen": "noch offen – vor dem Termin klären",
            "beispiele_nutzen": "Ihre Beispiele nutzen"},
}


def anrede_form(d):
    gs, m = d.get("gespraech") or {}, d.get("meta") or {}
    a = (gs.get("anrede") or m.get("anrede_form") or "du").lower()
    return "sie" if a.startswith("s") else "du"


def ac_typ(u):
    if isinstance(u, dict) and u.get("typ"):
        t = textlib.translit(u["typ"].lower())
        t = {"gruppendiskussion": "gruppe", "gruppenaufgabe": "gruppe", "gruppenuebung": "gruppe",
             "selbstpraesentation": "selbstpraesentation", "praesentation": "praesentation"}.get(t, t)
        if t in AC_TIPP:
            return t
    txt = (u.get("titel") or u.get("typ") or "") if isinstance(u, dict) else str(u)
    low = txt.lower()
    for typ, rx in AC_TYPEN:
        if re.search(rx, low):
            if typ == "praesentation" and re.search(r"\b(ich|mich|mir|mein\w*|selbst)\b|warum ich|über mich", low):
                return "selbstpraesentation"
            return typ
    return ""


def einladung_minuten(text, schl=r"vorstell|präsent|praesent|stell\w* (dich|sich)|über (dich|sich)|warum ich|selbst"):
    """Vorstellungsdauer aus der Einladung („Kurzpräsentation (3 Min.)“, „stellen Sie sich 5 Minuten vor“)."""
    for satz in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ])|\n", text or ""):   # „(ca. 5 Minuten)“ nicht zerschneiden
        if re.search(schl, satz, re.I):
            m = re.search(r"(\d{1,2})\s*(?:[-–]|bis)\s*(\d{1,2})\s*(?:min|minuten)\b|(\d{1,2})\s*(?:min|minuten)\b", satz, re.I)
            if m:
                return f"{m.group(1)}–{m.group(2)}" if m.group(1) else m.group(3)
    return None


def antwort_von(q):
    return (q.get("antwort_final") or q.get("antwort") or "").strip() if isinstance(q, dict) else ""


def sauber(liste):
    out = []
    for x in liste or []:
        t = x if isinstance(x, str) else (x.get("frage") or x.get("text") or "")
        if isinstance(x, dict) and x.get("gewaehlt") is False:
            continue
        t = re.sub(r"^\s*(?:\d{1,2}[.)]|[•\-–·])\s+", "", (t or "").strip())   # eigene Nummerierung weg (Aufzählung macht das Skript)
        if t and not INTERN_RE.search(t):
            out.append(t)
    return out


def spickzettel_daten(d):
    """→ (teile [(Überschrift oder None, [Zeilen])], hinweise_fuer_claude [str]). Leere Abschnitte fallen weg."""
    z, gs, pr = d.get("ziel") or {}, d.get("gespraech") or {}, d.get("profil") or {}
    schl, art_name = art_schluessel(gs, z)
    f = anrede_form(d)
    K = KOPF[f]
    hinweise, teile = [], []
    kopf = [f"SPICKZETTEL – {' · '.join(x for x in (z.get('stelle', ''), z.get('firma', '')) if x)}"]
    kz = " | ".join(f"{lab}: {v}" for lab, v in (("Termin", gs.get("termin")), ("Art", gs.get("art") or art_name),
                                                   ("Ort", gs.get("ort"))) if v)
    if kz:
        kopf.append(kz)
    if gs.get("gespraechspartner") or z.get("ansprechperson"):
        kopf.append(f"Gesprächspartner: {gs.get('gespraechspartner') or z.get('ansprechperson')}")
    teile.append((None, kopf))
    hinweise += einladung_abgleich(gs)
    # Kernbotschaften
    kb = sauber(gs.get("kernbotschaften"))[:3]
    if kb:
        teile.append((K["kern"], [f"• {x}" for x in kb]))
    # Vorstellung – Dauer aus der Einladung, nie fest „1–2 Minuten“
    vs = gs.get("vorstellung") or {}
    punkte = sauber(vs.get("kernpunkte") if isinstance(vs, dict) else None) or sauber(gs.get("selbstpraesentation"))
    dauer = (vs.get("dauer_min") if isinstance(vs, dict) else None) or einladung_minuten(gs.get("einladung_text"))
    if not dauer:
        dauer = "1" if schl in ("telefon", "probearbeit") else "1–2"
        if re.search(r"präsentation|vorstell|stell\w* (dich|sich)", gs.get("einladung_text") or "", re.I):
            hinweise.append("⚠️ Einladung erwähnt eine Vorstellung/Präsentation, aber keine Dauer gefunden – "
                            "gespraech.vorstellung.dauer_min setzen.")
    if punkte:
        teile.append((f"{K['vor']} ({dauer} Minuten)" if str(dauer) != "1" else f"{K['vor']} (1 Minute)",
                      [f"• {x}" for x in punkte]))
    # Schwierige Fragen: NUR echte Fragen mit finaler Antwort (kein Feedback, keine Notizen, kein Rohtext)
    sf, offen = [], []
    for q in gs.get("schwierige_fragen") or []:
        if not isinstance(q, dict) or not q.get("frage"):
            continue
        ant = antwort_von(q)
        if not ant:
            hinweise.append(f"⚠️ Schwierige Frage ohne antwort_final weggelassen: „{q['frage']}“")
            continue
        if "[PRÜFEN" in ant or "[PRUEFEN" in ant:
            offen.append(q["frage"])
            sf += [f"• {q['frage']}", f"  → {K['offen']}"]
            continue
        if INTERN_RE.search(ant):
            hinweise.append(f"⚠️ Antwort zu „{q['frage']}“ enthält einen internen Vermerk – weggelassen. "
                            "Nur die finale Antwort in den Worten des Nutzers eintragen.")
            continue
        if DRITTE_PERSON.search(ant):
            hinweise.append(f"⚠️ Antwort zu „{q['frage']}“ klingt nach Notiz in 3. Person – in Ich-Form umschreiben?")
        sf += [f"• {q['frage']}", f"  → {ant}"]
    # Gehalt nie still weglassen
    geh = gs.get("gehalt")
    geh_ant = antwort_von(geh) if isinstance(geh, dict) else (geh or "")
    geh_thema = re.search(r"gehalt", " ".join([str(z.get("unterlagen_verlangt") or ""), z.get("anzeige_text") or "",
                                                 gs.get("einladung_text") or ""]), re.I)
    if not any(re.search(r"gehalt|verdien", x, re.I) for x in sf):
        if geh_ant and "[PRÜFEN" not in geh_ant:
            sf += ["• Was ist Ihre Gehaltsvorstellung?", f"  → {geh_ant}"]
        elif geh_ant or geh_thema or (pr.get("rahmen") or {}).get("gehalt"):
            sf += ["• Was ist Ihre Gehaltsvorstellung?", f"  → {K['offen']} (Spanne mit Quelle)"]
            offen.append("Gehaltsvorstellung")
    if offen:
        hinweise.append("⚠️ Noch offen (steht so auf dem Spickzettel): " + "; ".join(offen) + " – mit dem Nutzer klären.")
    if sf:
        teile.append((K["schwer"], sf))
    if any(pr.get(k) for k in ("luecken", "abbruch_grund", "wechselgrund")):
        abgedeckt = " ".join(sf).lower()
        for k, wort in (("luecken", "lücke|war .*20\\d\\d|zeit nach"), ("abbruch_grund", "abbruch|abgebrochen"),
                        ("wechselgrund", "wechsel")):
            if pr.get(k) and not re.search(wort, abgedeckt):
                hinweise.append(f"ℹ️ profil.{k} vorhanden, aber keine schwierige Frage dazu – als "
                                "schwierige_fragen[{frage, antwort_final}] in seinen Worten ergänzen?")
    # Fachfragen
    ff = []
    for q in gs.get("fachfragen") or []:
        if isinstance(q, dict) and q.get("frage") and antwort_von(q) and not INTERN_RE.search(antwort_von(q)):
            ff += [f"• {q['frage']}", f"  → {antwort_von(q)}"]
    if ff:
        teile.append((K["fach"], ff))
    # Beispiele (max. 3, nur vollständige)
    bsp = []
    for b in pr.get("beispiele") or []:
        st = " → ".join(x for x in (b.get("situation", ""), b.get("handlung", ""), b.get("ergebnis", "")) if x)
        if b.get("handlung") and not INTERN_RE.search(st):
            bsp.append(f"• {b.get('thema') + ': ' if b.get('thema') else ''}{st}")
    if bsp:
        teile.append((K["bsp"], bsp[:3]))
    ef = sauber(gs.get("eigene_fragen"))
    if ef:
        teile.append((K["eigen"], [f"• {x}" for x in ef[:3]]))
    if schl == "ac":
        zeilen = []
        for u in gs.get("ac_uebungen") or []:
            titel = (u.get("titel") or u.get("typ") or "") if isinstance(u, dict) else str(u)
            if not titel or INTERN_RE.search(titel):
                continue
            typ = ac_typ(u)
            dm = (u.get("dauer_min") if isinstance(u, dict) else None) or einladung_minuten(titel, r".") or \
                (dauer if typ == "selbstpraesentation" and str(dauer) != "1–2" else None)
            tipp = (u.get("tipp") if isinstance(u, dict) else None) or AC_TIPP.get(typ, "")
            if f == "sie":
                tipp = tipp.replace("deine Beispiele", "Ihre Beispiele")
            if not typ:
                hinweise.append(f"ℹ️ Übung „{titel}“ ohne passenden Tipp – gespraech.ac_uebungen[].typ setzen.")
            zeilen.append(f"• {titel}" + (f" ({dm} Min.)" if dm and str(dm) not in titel else "") + (f": {tipp}" if tipp else ""))
        if zeilen:
            teile.append((K["ac"], zeilen))
    mit = sauber(gs.get("mitbringen")) or MITBRINGEN[schl]
    teile.append((K["mit"], [f"• {x}" for x in mit]))
    teile.append((TIPPS_KOPF[f][schl], [f"• {x}" for x in TIPPS[schl]]))
    if gs.get("feedback"):
        hinweise.append("ℹ️ gespraech.feedback ist intern und steht nicht auf dem Spickzettel – verbesserte Antworten "
                        "als antwort_final in schwierige_fragen eintragen.")
    return teile, hinweise


def spickzettel_teile(d):
    return spickzettel_daten(d)[0]


def einladung_abgleich(gs):
    """Ort/Termin des Spickzettels gegen die Einladung prüfen (v3: „Filiale am Ludwigsplatz“ fehlte)."""
    e = gs.get("einladung_text") or ""
    if not e:
        return []
    out = []
    kopf = textlib.translit(f"{gs.get('termin', '')} {gs.get('ort', '')}".lower())
    for m in re.finditer(r"\b(\d{1,2})\.(\d{1,2})\.(?:\d{2,4})?", e):
        tag, mon = int(m.group(1)), int(m.group(2))
        if not re.search(rf"\b0?{tag}\.0?{mon}\.", kopf):
            out.append(f"⚠️ Einladung nennt den {m.group(0)} – steht nicht in gespraech.termin.")
            break
    for m in re.finditer(r"\b(\d{1,2})(?::(\d{2}))?\s*Uhr", e):
        if not re.search(rf"\b0?{m.group(1)}(:|\s*uhr|\.)", kopf):
            out.append(f"⚠️ Einladung nennt {m.group(0)} – Uhrzeit fehlt in gespraech.termin.")
            break
    for m in re.finditer(r"(?:(?:filiale|standort|praxis|büro|gebäude|haus|eingang|raum)\s+(?:am|an der|im|in der)\s+|"
                         r"\b)([A-ZÄÖÜ][\wäöüß\-]*(?:straße|strasse|str\.|platz|weg|allee|ring|gasse|markt|ufer|damm)\b(?:\s*\d+\w?)?)", e, re.I):
        ort = m.group(1)
        if textlib.translit(ort.lower().split()[0])[:6] not in kopf:
            out.append(f"⚠️ Ort laut Einladung: „{ort}“ – fehlt in gespraech.ort.")
            break
    return out


def spickzettel_text(d):
    out = []
    for kopf, zeilen in spickzettel_teile(d):
        if kopf:
            out += ["", kopf.upper()]
        out += [z for z in zeilen if z]
    return "\n".join(out).strip() + "\n"


def spickzettel_pdf(d, pdf_ziel, format_="kompakt"):
    """Saubere PDF. Standard „kompakt“: A5 (am Handy ohne Zoomen lesbar), 1 Seite angestrebt – wird es knapp
    länger, rückt das Skript enger zusammen statt eine fast leere Seite 2 zu erzeugen. „a4“: zum Ausdrucken."""
    try:
        import unterlagen_erstellen as ue
        ue.ensure_docx()
        from docx.shared import Cm, Pt
        teile = spickzettel_teile(d)
        stufen = [(11, 3, 9), (10.5, 2, 7), (10, 1, 5), (9.5, 0, 4)] if format_ == "kompakt" else [(11, 2, 10), (10, 1, 6)]
        for groesse, abstand, kopf_vor in stufen:
            doc = ue.neues_dokument("Spickzettel", "")
            sec = doc.sections[0]
            if format_ == "kompakt":
                sec.page_width, sec.page_height = Cm(14.8), Cm(21.0)
                sec.left_margin = sec.right_margin = Cm(1.2)
                sec.top_margin = sec.bottom_margin = Cm(1.1)
            doc.styles["Normal"].font.size = Pt(groesse)
            h = doc.styles["Heading 1"]
            h.font.size = Pt(groesse + 1)
            h.paragraph_format.space_before, h.paragraph_format.space_after = Pt(kopf_vor), Pt(2)
            for kopf, zeilen in teile:
                if kopf:
                    doc.add_heading(kopf, level=1)
                for i, zl in enumerate(zeilen):
                    if not zl:
                        continue
                    p = doc.add_paragraph()
                    p.paragraph_format.space_after = Pt(abstand)
                    if zl.startswith("  → "):
                        p.paragraph_format.left_indent = Cm(0.5)
                    ue.text(p, zl.strip(), bold=(kopf is None and i == 0), size=(groesse + 2 if kopf is None and i == 0 else None))
            tmpd = tempfile.mkdtemp()
            docx = os.path.join(tmpd, os.path.splitext(os.path.basename(pdf_ziel))[0] + ".docx")
            doc.save(docx)
            pdf, err = ue.zu_pdf(docx)
            if err:
                return err
            seiten, letzte = pdf_seiten_fuellung(pdf)
            if seiten <= 1 or letzte >= 6 or (groesse, abstand, kopf_vor) == stufen[-1]:
                shutil.move(pdf, pdf_ziel)
                return None
        return None
    except SystemExit as e:
        return str(e)


def pdf_seiten_fuellung(pdf):
    """→ (Seitenzahl, Textzeilen auf der letzten Seite)."""
    try:
        import pypdf
        r = pypdf.PdfReader(pdf)
        letzte = r.pages[-1].extract_text() or ""
        return len(r.pages), len([z for z in letzte.splitlines() if z.strip()])
    except Exception:
        return 1, 99


def spickzettel(d, ordner, pdf=False, format_="kompakt"):
    z = d.get("ziel") or {}
    teile, hinweise = spickzettel_daten(d)
    txt = spickzettel_text(d)
    firma = textlib.safe_name(z.get("firma", ""), 30, "Firma")
    pfad, _ = textlib.neue_version(ordner, f"Gespraech_Spickzettel_{firma}", ".txt", mitziehen=(".txt", ".pdf"))
    open(pfad, "w", encoding="utf8").write(txt)
    res = [pfad]
    if pdf:
        p = os.path.splitext(pfad)[0] + ".pdf"
        err = spickzettel_pdf(d, p, format_)
        res.append(p if not err else err)
    return res, hinweise


def datei_hash(pfad):
    import hashlib
    h = hashlib.sha1()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def _stamm_ohne_kopie(name):
    """„IMG_2041 (1).jpg“, „image(1).jpg“, „Zeugnis-1.pdf“ → „img_2041“, „image“, „zeugnis“."""
    st = os.path.splitext(name)[0].lower()
    return re.sub(r"\s*(\(\d+\)|[-_ ]\d{1,2}|[-_ ]kopie|[-_ ]copy)$", "", st).strip()


def akte_finden(pfad):
    """Akte auch finden, wenn das Handy sie umbenannt hat („Bewerbungsakte (1).txt“, „Akte.txt“, Ordner)."""
    if pfad and os.path.isfile(pfad):
        return pfad
    ordner = pfad if pfad and os.path.isdir(pfad) else UPLOADS
    kand = []
    for f in os.listdir(ordner) if os.path.isdir(ordner) else []:
        p = os.path.join(ordner, f)
        if os.path.isfile(p) and f.lower().endswith((".txt", ".md")):
            try:
                if textlib.AKTE_START in open(p, encoding="utf8", errors="ignore").read():
                    kand.append(p)
            except OSError:
                pass
    if not kand:
        raise RuntimeError(f"Keine Bewerbungsakte (.txt mit Datenblock) gefunden: {pfad}")

    def stand(p):
        try:
            st = (textlib.lade_profil(p).get("meta") or {}).get("stand", "")
            return datetime.datetime.strptime(st[:19], "%d.%m.%Y %H:%M:%S") if len(st) >= 19 else \
                datetime.datetime.strptime(st[:16], "%d.%m.%Y %H:%M")
        except (ValueError, RuntimeError):
            return datetime.datetime.fromtimestamp(os.path.getmtime(p))
    return max(kand, key=stand)


def lesen(akte, ziel):
    akte = akte_finden(akte)
    d = textlib.lade_profil(akte)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    fehlen, zugeordnet = [], []
    pr = d.get("profil") or {}
    uploads = [os.path.join(UPLOADS, f) for f in (os.listdir(UPLOADS) if os.path.isdir(UPLOADS) else [])
               if os.path.isfile(os.path.join(UPLOADS, f)) and os.path.abspath(os.path.join(UPLOADS, f)) != os.path.abspath(akte)
               and not f.lower().endswith((".txt", ".md", ".json"))]
    vergeben = set()
    hashes = {}

    def h(p):
        if p not in hashes:
            hashes[p] = datei_hash(p)
        return hashes[p]

    def suche(alt_pfad, sha1=None):
        b = os.path.basename(alt_pfad or "")
        frei = [u for u in uploads if u not in vergeben]
        for u in frei:                                  # 1. gleicher Name
            if os.path.basename(u) == b:
                return u, None
        if sha1:                                        # 2. gleicher Inhalt (umbenannt beim Re-Upload)
            for u in frei:
                if h(u) == sha1:
                    return u, None
        for u in frei:                                  # 3. Kopie-Endung „ (1)“
            if _stamm_ohne_kopie(os.path.basename(u)) == _stamm_ohne_kopie(b):
                return u, None
        return None, None
    offen_anl = []
    for a in pr.get("anlagen") or []:
        p = a.get("datei", "")
        if p and not os.path.isfile(p):
            neu, _ = suche(p, a.get("sha1"))
            if neu:
                a["datei"] = neu
                vergeben.add(neu)
            else:
                offen_anl.append(a)
    foto = (d.get("person") or {}).get("foto")
    if foto and not os.path.isfile(foto):
        neu, _ = suche(foto, d["person"].get("foto_sha1"))
        if neu:
            d["person"]["foto"] = neu
            vergeben.add(neu)
        else:
            fehlen.append(f"{os.path.basename(foto)} (Bewerbungsfoto)")
    frei = [u for u in uploads if u not in vergeben]
    if len(offen_anl) == 1 and len(frei) == 1:          # 4. genau eine fehlt, genau eine neue Datei → zuordnen, bestätigen lassen
        a = offen_anl.pop()
        zugeordnet.append(f"{os.path.basename(frei[0])} → {a.get('bezeichnung') or os.path.basename(a.get('datei', ''))}")
        a["datei"] = frei[0]
    for a in offen_anl:
        fehlen.append(f"{os.path.basename(a.get('datei', ''))} ({a.get('bezeichnung') or 'Anlage'})")
    json.dump(d, open(ziel, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    m, z = d.get("meta") or {}, d.get("ziel") or {}
    print(f"✅ Daten übernommen aus {os.path.basename(akte)} → {ziel}")
    print(f"Stand: {m.get('stand', '?')} | Phase: {m.get('phase', '?')} | Nächster Schritt: {m.get('naechster_schritt', '?')}")
    print(f"Ziel: {z.get('stelle', '?')} bei {z.get('firma', '?')} | Frist: {z.get('frist', '?')}")
    for zg in zugeordnet:
        print(f"🔗 Neue Datei zugeordnet (Name war anders): {zg} – kurz mit dem Nutzer bestätigen.")
    if fehlen:
        print("📎 Erst nötig für Anlagen/Gesamt-PDF – dann bitte noch einmal hochladen: " + "; ".join(fehlen))
    if "schema" not in d:
        print("ℹ️ Alte Akte (v1): Profil-Felder fehlen – fehlende Fakten beim Nutzer nachfragen, nicht aus den Texten raten.")
    elif not textlib.rohtext_eintraege(d):
        print("ℹ️ Akte ohne Wortlaut (v2): fakten_check prüft gegen Profil-Felder (unsicher). Neue Antworten in profil.rohtext.")
    elif d.get("schema") == "bewerbungs-profi/3" and (d.get("anschreiben") or d.get("formular") or d.get("email")) \
            and not d.get("herkunft"):
        print("ℹ️ Akte aus v3: Texte haben noch keine Satz-Herkunft – vor der nächsten Freigabe profil-JSON „herkunft“ ergänzen.")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    opts = {}
    for k in ("--ausgabe", "--json-nach"):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    if a[0] == "--lesen":
        try:
            lesen(a[1] if len(a) > 1 else UPLOADS, opts.get("--json-nach", "/tmp/bewerbung/profil.json"))
        except (RuntimeError, IndexError) as e:
            print(f"FEHLER: Akte nicht lesbar: {e}")
            sys.exit(2)
        return
    try:
        d = textlib.lade_profil(a[0])
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(2)
    ordner = textlib.ausgabe_ordner(opts.get("--ausgabe"))
    if "--spickzettel" in a:
        res, hinweise = spickzettel(d, ordner, "--pdf" in a, "a4" if "--a4" in a else "kompakt")
    else:
        res, hinweise = schreibe_akte(d, ordner, "--pdf" in a), []
    for r in res:
        print(("✅ " if os.path.isfile(r) else "⚠️ ") + r)
    for h in hinweise:
        print(h)
    if "--spickzettel" not in a:
        if a[0].endswith(".json"):   # Stand + Zähler auch in der Arbeits-JSON
            json.dump(d, open(a[0], "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("Zum Herunterladen geben: NUR die .txt ist zum Weitermachen (die neueste Uhrzeit im Namen gilt).")
        hoch = wieder_hochladen(d)
        if hoch:
            print("Im neuen Chat zusätzlich hochladen: " + "; ".join(hoch))


if __name__ == "__main__":
    main()
