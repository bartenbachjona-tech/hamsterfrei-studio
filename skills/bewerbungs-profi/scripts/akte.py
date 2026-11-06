#!/usr/bin/env python3
"""Bewerbungsakte schreiben und lesen – billig aus der Profil-JSON, ohne Tipparbeit.

    python3 akte.py PROFIL.json [--pdf] [--ausgabe ORDNER]
        → Bewerbungsakte_Vorname_Nachname_JJJJ-MM-TT_HHMMSS.txt (eindeutig, öffnet auf jedem Handy/PC):
          oben lesbar (inkl. „im neuen Chat wieder hochladen: …“), unten die Daten zum Weitermachen.
          Nur .txt hochladen! --pdf (nur auf Wunsch) erzeugt zusätzlich Akte-Lesefassung_….pdf
          (anderer Name, damit niemand die PDF statt der .txt hochlädt). Ältere Akten im Ordner → alt/.
    python3 akte.py --lesen AKTE.txt|AKTE.md [--json-nach /tmp/bewerbung/profil.json]
        → holt die JSON aus einer hochgeladenen Akte (auch v1/v2), sucht Anlagen in den neuen Uploads
          und sagt, was noch einmal hochgeladen werden muss.
    python3 akte.py PROFIL.json --spickzettel [--pdf]
        → Gespraech_Spickzettel_Firma_AKTUELL.txt (+ PDF): Termin | Art | Ort, Mitbring-Liste,
          3 Kernbotschaften, Vorstellung, schwierige Fragen mit den VERBESSERTEN Antworten, Beispiele,
          nur die gewählten eigenen Fragen, Tipps passend zu Präsenz/Video/Telefon bzw. Auswahltag (AC).
          Leere Felder und interne Vermerke werden weggelassen. Vorher: fakten_check.py … --typ spickzettel
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
INTERN_RE = re.compile(r"(\(?vorschlag\s+claude|\bintern\b|\bnotiz\s*:|\btodo\b|\[PRÜFEN|\bclaude\b|nicht in unterlagen)", re.I)


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
    if art and art.lower() not in titel.lower():
        titel = f"{titel} ({art})" if titel else art
    teile = [s.get("zeitraum", ""), titel]
    ort = ", ".join(x for x in (s.get("firma", ""), s.get("ort", "")) if x)
    return " ".join(x for x in teile if x) + (f", {ort}" if ort else "")


def wieder_hochladen(d):
    pr = d.get("profil") or {}
    liste = []
    for a in pr.get("anlagen") or []:
        if a.get("datei"):
            liste.append(f"{os.path.basename(a['datei'])} ({a.get('bezeichnung') or 'Anlage'})")
    if (d.get("person") or {}).get("foto"):
        liste.append(f"{os.path.basename(d['person']['foto'])} (Bewerbungsfoto)")
    for q in pr.get("quellen") or []:
        p = q if isinstance(q, str) else q.get("datei", "")
        if p:
            liste.append(f"{os.path.basename(p)} (Upload)")
    return liste


def lesbar(d):
    p, z, pr, m = d.get("person") or {}, d.get("ziel") or {}, d.get("profil") or {}, d.get("meta") or {}
    jetzt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    out = [f"BEWERBUNGSAKTE – {p.get('name', '') or '(Name noch offen)'}",
           "Im neuen Chat DIESE .txt-Datei hochladen und schreiben: „Weiter mit meiner Bewerbung“.",
           "Enthält persönliche Daten – privat speichern, nicht teilen.", ""]
    hoch = wieder_hochladen(d)
    if hoch:
        out.append("Im neuen Chat zusätzlich wieder hochladen (Uploads bleiben nicht erhalten):")
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
    for l in pr.get("luecken") or []:
        out.append(f"- Lücke: {l.get('zeitraum', '')} – {l.get('erklaerung', '')}")
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
    meta["antworten_seit_akte"] = 0
    d.setdefault("schema", "bewerbungs-profi/3")
    les = lesbar(d)
    voll = les + "\n\n" + textlib.AKTE_START + "\n" + json.dumps(d, ensure_ascii=False, indent=1) + "\n" + textlib.AKTE_ENDE + "\n"
    open(pfad, "w", encoding="utf8").write(voll)
    ergebnis = [pfad]
    if pdf:
        p = os.path.join(ordner, os.path.basename(pfad).replace(praefix, lese, 1).replace(".txt", ".pdf"))
        err = txt_zu_pdf(les, p)
        ergebnis.append(p if not err else err)
    return ergebnis


# ---------------------------------------------------------------- Spickzettel
TIPPS = {
    "praesenz": ["10 Minuten vor der Zeit da sein, Weg vorher prüfen",
                 "Kleidung eine Stufe formeller als im Betrieb üblich",
                 "Handy lautlos, Blickkontakt, ruhig ausreden lassen",
                 "Am Ende fragen: Wie geht es weiter, wann höre ich von Ihnen?"],
    "video": ["Link, Kamera, Ton und Akku 30 Minuten vorher testen",
              "Licht von vorn, ruhiger Hintergrund, Kamera auf Augenhöhe",
              "In die Kamera schauen, Benachrichtigungen aus",
              "Telefonnummer für Technikprobleme bereithalten"],
    "telefon": ["Ruhiger Ort, gutes Netz, Handy geladen",
                "Lebenslauf und diesen Zettel vor dir, Stift bereit",
                "Im Stehen sprechen und lächeln – man hört es",
                "Namen der Gesprächspartner notieren"],
    "ac": ["Pünktlich, ausgeschlafen, etwas zu essen und trinken dabei",
           "In Gruppenübungen andere einbeziehen und zusammenfassen",
           "Jede Entscheidung kurz begründen",
           "Auch Pausen gehören dazu – freundlich und echt bleiben"],
    "probearbeit": ["Bequeme, passende Kleidung und Schuhe (nach Vorgabe)",
                    "Fragen stellen, wenn etwas unklar ist – das wirkt gut",
                    "Pünktlich sein und mit anpacken",
                    "Am Ende nach Rückmeldung und nächstem Schritt fragen"],
}
MITBRINGEN = {
    "praesenz": ["Lebenslauf und Anschreiben ausgedruckt", "Zeugnisse (Kopien)", "Stift und Notizzettel"],
    "video": ["Zugangslink und Passwort", "Ladekabel", "Notizzettel und Glas Wasser"],
    "telefon": ["Lebenslauf und Anzeige", "Notizzettel und Stift"],
    "ac": ["Einladung", "Lebenslauf ausgedruckt", "Stift, Notizblock, Uhr", "Verpflegung"],
    "probearbeit": ["Passende Kleidung/Schuhe", "Einladung", "Getränk"],
}
AC_TIPP = {
    "selbstpräsentation": "frei sprechen: heute → Weg → warum hier, Zeit einhalten",
    "gruppendiskussion": "Position beziehen, andere einbeziehen, am Ende zusammenfassen",
    "postkorb": "A sofort / B planen oder delegieren / C später – jede Entscheidung begründen",
    "rollenspiel": "zuhören, ruhig bleiben, konkrete Lösung zusagen",
    "fallstudie": "Problem → Ursachen → Optionen → Empfehlung",
    "präsentation": "Problem → Ursachen → Optionen → Empfehlung, Zeit einhalten",
    "interview": "wie ein Vorstellungsgespräch – deine Beispiele nutzen",
    "test": "ruhig bleiben, bei schweren Aufgaben weiter und später zurück",
}


def art_schluessel(gs, z):
    a = textlib.translit(f"{gs.get('art', '')} {z.get('auswahlverfahren', '') if not gs.get('art') else ''}".lower())
    if re.search(r"assessment|\bac\b|auswahltag|auswahlverfahren", a):
        return "ac", "Auswahltag"
    if "probe" in a:
        return "probearbeit", "Probearbeiten"
    if "video" in a or "teams" in a or "zoom" in a or "online" in a:
        return "video", "Videogespräch"
    if "telefon" in a:
        return "telefon", "Telefoninterview"
    return "praesenz", "Gespräch vor Ort"


def sauber(liste):
    out = []
    for x in liste or []:
        t = x if isinstance(x, str) else (x.get("frage") or x.get("text") or "")
        if isinstance(x, dict) and x.get("gewaehlt") is False:
            continue
        t = (t or "").strip()
        if t and not INTERN_RE.search(t):
            out.append(t)
    return out


def spickzettel_teile(d):
    """→ [(Überschrift oder None, [Zeilen])] ohne leere Abschnitte."""
    z, gs, pr = d.get("ziel") or {}, d.get("gespraech") or {}, d.get("profil") or {}
    schl, art_name = art_schluessel(gs, z)
    teile = []
    kopf = [f"SPICKZETTEL – {' · '.join(x for x in (z.get('stelle', ''), z.get('firma', '')) if x)}"]
    kz = " | ".join(f"{lab}: {v}" for lab, v in (("Termin", gs.get("termin")), ("Art", gs.get("art") or art_name),
                                                   ("Ort", gs.get("ort"))) if v)
    kopf.append(kz)
    if gs.get("gespraechspartner") or z.get("ansprechperson"):
        kopf.append(f"Gesprächspartner: {gs.get('gespraechspartner') or z.get('ansprechperson')}")
    teile.append((None, kopf))
    teile.append(("Mitbringen", [f"- {x}" for x in (sauber(gs.get("mitbringen")) or MITBRINGEN[schl])]))
    kb = sauber(gs.get("kernbotschaften"))[:3]
    if kb:
        teile.append(("Deine 3 Kernbotschaften", [f"{i}. {x}" for i, x in enumerate(kb, 1)]))
    sp = sauber(gs.get("selbstpraesentation"))
    if sp:
        teile.append(("So stellst du dich vor (1–2 Minuten)", [f"- {x}" for x in sp]))
    # Schwierige Fragen: verbesserte Antwort aus dem Feedback hat Vorrang
    besser = {}
    for f in gs.get("feedback") or []:
        if isinstance(f, dict) and f.get("frage") and f.get("besser") and not INTERN_RE.search(f["besser"]):
            besser[textlib.translit(f["frage"].lower())] = f["besser"]
    sf = []
    gesehen = set()
    for q in gs.get("schwierige_fragen") or []:
        if not isinstance(q, dict) or not q.get("frage"):
            continue
        k = textlib.translit(q["frage"].lower())
        antwort = besser.pop(k, None) or q.get("antwort", "")
        if antwort and not INTERN_RE.search(antwort):
            sf += [f"- {q['frage']}", f"  → {antwort}"]
            gesehen.add(k)
    for k, antwort in besser.items():
        frage = next(f["frage"] for f in gs.get("feedback") if isinstance(f, dict) and textlib.translit(f.get("frage", "").lower()) == k)
        sf += [f"- {frage}", f"  → {antwort}"]
    abgedeckt = " ".join(sf)
    for l in pr.get("luecken") or []:
        if l.get("zeitraum") and l.get("erklaerung") and l["zeitraum"] not in abgedeckt:
            sf += [f"- Was war {l['zeitraum']}?", f"  → {l['erklaerung']}"]
    if pr.get("abbruch_grund") and "abbruch" not in abgedeckt.lower():
        sf += ["- Warum haben Sie abgebrochen?", f"  → {pr['abbruch_grund']}"]
    if pr.get("wechselgrund") and "wechsel" not in abgedeckt.lower():
        sf += ["- Warum möchten Sie wechseln?", f"  → {pr['wechselgrund']}"]
    if sf:
        teile.append(("Schwierige Fragen – deine Antwort", sf))
    bsp = []
    for b in pr.get("beispiele") or []:
        st = " → ".join(x for x in (b.get("situation", ""), ("Ich: " + b["handlung"]) if b.get("handlung") else "",
                                    ("Ergebnis: " + b["ergebnis"]) if b.get("ergebnis") else "") if x)
        if st and not INTERN_RE.search(st):
            bsp.append(f"- {b.get('thema') + ': ' if b.get('thema') else ''}{st}")
    if bsp:
        teile.append(("Deine Beispiele", bsp))
    ef = sauber(gs.get("eigene_fragen"))
    if ef:
        teile.append(("Deine Fragen an die Firma", [f"- {x}" for x in ef]))
    if schl == "ac":
        ue = sauber(gs.get("ac_uebungen")) or []
        zeilen = []
        for u in ue:
            tipp = next((t for k, t in AC_TIPP.items() if k in u.lower()), "")
            zeilen.append(f"- {u}" + (f": {tipp}" if tipp else ""))
        if zeilen:
            teile.append(("Dein Auswahltag", zeilen))
    teile.append((f"Tipps für dein {art_name}", [f"- {x}" for x in TIPPS[schl]]))
    return teile


def spickzettel_text(d):
    out = []
    for kopf, zeilen in spickzettel_teile(d):
        if kopf:
            out += ["", kopf.upper()]
        out += [z for z in zeilen if z]
    return "\n".join(out).strip() + "\n"


def spickzettel_pdf(d, pdf_ziel):
    """Saubere PDF: Überschriften fett mit grauer Linie, Arial, A4 (über Word + LibreOffice)."""
    try:
        import unterlagen_erstellen as ue
        ue.ensure_docx()
        from docx.shared import Pt
        doc = ue.neues_dokument("Spickzettel", "")
        for kopf, zeilen in spickzettel_teile(d):
            if kopf:
                doc.add_heading(kopf, level=1)
            for i, zl in enumerate(zeilen):
                if not zl:
                    continue
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(1)
                ue.text(p, zl, bold=(kopf is None and i == 0), size=(14 if kopf is None and i == 0 else None))
        tmpd = tempfile.mkdtemp()
        docx = os.path.join(tmpd, os.path.splitext(os.path.basename(pdf_ziel))[0] + ".docx")
        doc.save(docx)
        pdf, err = ue.zu_pdf(docx)
        if err:
            return err
        shutil.move(pdf, pdf_ziel)
        return None
    except SystemExit as e:
        return str(e)


def spickzettel(d, ordner, pdf=False):
    z = d.get("ziel") or {}
    txt = spickzettel_text(d)
    firma = textlib.safe_name(z.get("firma", ""), 30, "Firma")
    pfad, _ = textlib.neue_version(ordner, f"Gespraech_Spickzettel_{firma}", ".txt", mitziehen=(".txt", ".pdf"))
    open(pfad, "w", encoding="utf8").write(txt)
    res = [pfad]
    if pdf:
        p = os.path.splitext(pfad)[0] + ".pdf"
        err = spickzettel_pdf(d, p)
        res.append(p if not err else err)
    return res


def lesen(akte, ziel):
    d = textlib.lade_profil(akte)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    fehlen = []
    pr = d.get("profil") or {}
    for a in pr.get("anlagen") or []:
        p = a.get("datei", "")
        if p and not os.path.isfile(p):
            neu = os.path.join(UPLOADS, os.path.basename(p))
            if os.path.isfile(neu):
                a["datei"] = neu
            else:
                fehlen.append(f"{os.path.basename(p)} ({a.get('bezeichnung') or 'Anlage'})")
    foto = (d.get("person") or {}).get("foto")
    if foto and not os.path.isfile(foto):
        neu = os.path.join(UPLOADS, os.path.basename(foto))
        if os.path.isfile(neu):
            d["person"]["foto"] = neu
        else:
            fehlen.append(f"{os.path.basename(foto)} (Bewerbungsfoto)")
    json.dump(d, open(ziel, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    m, z = d.get("meta") or {}, d.get("ziel") or {}
    print(f"✅ Daten übernommen → {ziel}")
    print(f"Stand: {m.get('stand', '?')} | Phase: {m.get('phase', '?')} | Nächster Schritt: {m.get('naechster_schritt', '?')}")
    print(f"Ziel: {z.get('stelle', '?')} bei {z.get('firma', '?')} | Frist: {z.get('frist', '?')}")
    if fehlen:
        print("📎 Bitte noch einmal hochladen (erst nötig für Anlagen/Gesamt-PDF): " + "; ".join(fehlen))
    if "schema" not in d:
        print("ℹ️ Alte Akte (v1): Profil-Felder fehlen – fehlende Fakten beim Nutzer nachfragen, nicht aus den Texten raten.")
    elif not textlib.rohtext_eintraege(d):
        print("ℹ️ Akte ohne Wortlaut (v2): fakten_check prüft gegen Profil-Felder (unsicher). Neue Antworten in profil.rohtext.")


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
            lesen(a[1], opts.get("--json-nach", "/tmp/bewerbung/profil.json"))
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
    res = spickzettel(d, ordner, "--pdf" in a) if "--spickzettel" in a else schreibe_akte(d, ordner, "--pdf" in a)
    for r in res:
        print(("✅ " if os.path.isfile(r) else "⚠️ ") + r)
    if "--spickzettel" not in a:
        if a[0].endswith(".json"):   # Stand + Zähler auch in der Arbeits-JSON
            json.dump(d, open(a[0], "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("Zum Herunterladen geben: NUR die .txt ist zum Weitermachen (die neueste Uhrzeit im Namen gilt).")
        hoch = wieder_hochladen(d)
        if hoch:
            print("Im neuen Chat zusätzlich hochladen: " + "; ".join(hoch))


if __name__ == "__main__":
    main()
