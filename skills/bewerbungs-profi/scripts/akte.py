#!/usr/bin/env python3
"""Bewerbungsakte schreiben und lesen – billig aus der Profil-JSON, ohne Tipparbeit.

    python3 akte.py PROFIL.json [--pdf] [--ausgabe ORDNER]
        → Bewerbungsakte_Vorname_Nachname_JJJJ-MM-TT_HHMM.txt (öffnet auf jedem Handy/PC):
          oben lesbare Zusammenfassung, unten die Daten (JSON) zum Weitermachen.
          --pdf zusätzlich als PDF (nur der lesbare Teil). Ältere Akten im Ordner → alt/.
    python3 akte.py --lesen AKTE.txt|AKTE.md [--json-nach /tmp/bewerbung/profil.json]
        → holt die JSON aus einer hochgeladenen Akte (auch alte .md mit ```json) und zeigt den Stand.
    python3 akte.py PROFIL.json --spickzettel [--pdf]
        → Gespraech_Spickzettel_Firma.txt (+ PDF) aus gespraech + profil.beispiele, ohne #/**.
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


def g(d, *pfad, std=""):
    for p in pfad:
        d = d.get(p, {}) if isinstance(d, dict) else {}
    return d if d not in ({}, None) else std


def zeile(label, wert):
    if isinstance(wert, list):
        wert = ", ".join(str(x) for x in wert if x)
    return f"{label}: {wert if wert not in ('', None) else '(offen)'}"


def lesbar(d):
    p, z, pr, m = d.get("person") or {}, d.get("ziel") or {}, d.get("profil") or {}, d.get("meta") or {}
    jetzt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    out = [f"BEWERBUNGSAKTE – {p.get('name', '')}",
           "Beim nächsten Chat diese Datei hochladen und schreiben: „Weiter mit meiner Bewerbung“.",
           "Enthält persönliche Daten – privat speichern, nicht teilen.", "",
           f"Stand: {jetzt}", zeile("Phase", m.get("phase")), zeile("Nächster Schritt", m.get("naechster_schritt")),
           zeile("Fahrplan", m.get("chat_plan")), zeile("Gerät", m.get("geraet")), "", LINIE, "ZIEL", LINIE]
    for k, lab in (("art", "Art"), ("stelle", "Stelle"), ("firma", "Firma"), ("link", "Link"), ("kennziffer", "Kennziffer"),
                   ("ansprechperson", "Ansprechperson"), ("bewerbungsweg", "Bewerbungsweg"), ("frist", "Frist"),
                   ("start", "Start"), ("unterlagen_verlangt", "Verlangte Unterlagen"), ("upload_limit", "Upload-Limit"),
                   ("muss", "Muss"), ("kann", "Kann"), ("auswahlverfahren", "Auswahlverfahren"),
                   ("anschreiben_variante", "Anschreiben-Variante")):
        out.append(zeile(lab, z.get(k)))
    out += ["", LINIE, "PROFIL (deine Angaben)", LINIE]
    for b in pr.get("bildung") or []:
        out.append(f"- Bildung: {b.get('zeitraum', '')} {b.get('abschluss', '')}, {b.get('schule', '')}"
                   + (f", Note {b['note']}" if b.get("note") else ""))
    for s in pr.get("stationen") or []:
        out.append(f"- Station: {s.get('zeitraum', '')} {s.get('titel', '')} ({s.get('art', '')}), {s.get('firma', '')}")
        for t in (s.get("taetigkeiten") or []) + (s.get("ergebnisse") or []):
            out.append(f"    · {t}")
    for l in pr.get("luecken") or []:
        out.append(f"- Lücke: {l.get('zeitraum', '')} – {l.get('erklaerung', '')}")
    if pr.get("sprachen"):
        out.append(zeile("Sprachen", [f"{s.get('sprache')} ({s.get('niveau')})" for s in pr["sprachen"]]))
    out.append(zeile("EDV", pr.get("edv")))
    if pr.get("fuehrerschein"):
        out.append(zeile("Führerschein", pr.get("fuehrerschein")))
    out.append(zeile("Warum dieser Beruf", pr.get("motivation_beruf")))
    out.append(zeile("Warum diese Firma", pr.get("motivation_firma")))
    for b in pr.get("beispiele") or []:
        out.append(f"- Beispiel ({b.get('thema', '')}): {b.get('situation', '')} → {b.get('handlung', '')} → {b.get('ergebnis', '') or '(Ergebnis offen)'}")
    out.append(zeile("Hobbys", pr.get("hobbys")))
    r = pr.get("rahmen") or {}
    out.append(zeile("Start/Verfügbarkeit", " · ".join(x for x in (r.get("start", ""), r.get("stunden", ""), r.get("verfuegbarkeit", "")) if x)))
    out.append(zeile("Foto", {True: "ja", False: "nein"}.get(r.get("foto"), "(offen)")))
    if d.get("firmenfakten"):
        out.append("Firmenfakten aus Recherche:")
        for f in d["firmenfakten"]:
            out.append(f"    · {f.get('fakt')} (Quelle: {f.get('quelle')}; im Text: {'ja' if f.get('zugestimmt') else 'nein'})")
    out += ["", LINIE, "STATUS DER UNTERLAGEN", LINIE]
    for s in d.get("status") or []:
        out.append(f"- {s.get('unterlage')}: {s.get('status')}" + (f" – {s.get('datei')}" if s.get("datei") else "")
                   + (f" – offen: {s.get('offen')}" if s.get("offen") else ""))
    gs = d.get("gespraech") or {}
    out += ["", LINIE, "GESPRÄCH / AUSWAHLTAG", LINIE, zeile("Termin/Art", " ".join(x for x in (gs.get("termin", ""), gs.get("art", "")) if x))]
    for s in gs.get("star") or []:
        out.append(f"- STAR: {s if isinstance(s, str) else s.get('kurz', s)}")
    for f in gs.get("eigene_fragen") or []:
        out.append(f"- Eigene Frage: {f}")
    for f in gs.get("feedback") or []:
        out.append(f"- Feedback: {f}")
    out += ["", LINIE, "ALLE BEWERBUNGEN", LINIE]
    for b in d.get("bewerbungen") or []:
        out.append(f"- {b.get('firma')} | {b.get('stelle')} | abgeschickt: {b.get('abgeschickt') or '–'} | "
                   f"{b.get('status')} | nachfassen: {b.get('nachfassen') or '–'}")
    out += ["", LINIE, "ENTSCHEIDUNGEN", LINIE]
    for e in d.get("entscheidungen") or []:
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


def alte_wegraeumen(ordner, praefix):
    for f in os.listdir(ordner):
        if f.startswith(praefix) and os.path.splitext(f)[1].lower() in (".txt", ".pdf", ".md"):
            alt = os.path.join(ordner, "alt")
            os.makedirs(alt, exist_ok=True)
            ziel = os.path.join(alt, f)
            if not os.path.exists(ziel):
                shutil.move(os.path.join(ordner, f), ziel)


def schreibe_akte(d, ordner, pdf=False):
    os.makedirs(ordner, exist_ok=True)
    name = textlib.name_teile((d.get("person") or {}).get("name", "")) or "Name"
    praefix = f"Bewerbungsakte_{name}"
    alte_wegraeumen(ordner, praefix)
    stempel = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    pfad = os.path.join(ordner, f"{praefix}_{stempel}.txt")
    d.setdefault("meta", {})["stand"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    les = lesbar(d)
    voll = les + "\n\n" + textlib.AKTE_START + "\n" + json.dumps(d, ensure_ascii=False, indent=1) + "\n" + textlib.AKTE_ENDE + "\n"
    open(pfad, "w", encoding="utf8").write(voll)
    ergebnis = [pfad]
    if pdf:
        p = os.path.splitext(pfad)[0] + ".pdf"
        err = txt_zu_pdf(les, p)
        ergebnis.append(p if not err else err)
    return ergebnis


def spickzettel(d, ordner, pdf=False):
    z, gs, pr = d.get("ziel") or {}, d.get("gespraech") or {}, d.get("profil") or {}
    out = [f"SPICKZETTEL – Gespräch {z.get('stelle', '')} bei {z.get('firma', '')}",
           zeile("Termin/Art/Ort", " ".join(x for x in (gs.get("termin", ""), gs.get("art", ""), gs.get("ort", "")) if x)),
           zeile("Gesprächspartner", gs.get("gespraechspartner") or z.get("ansprechperson")), "",
           "SELBSTPRÄSENTATION (heute → Weg → warum hier)"]
    out += [f"- {s}" for s in gs.get("selbstpraesentation") or ["(offen)"]]
    out += ["", "MEINE BEISPIELE (STAR)"]
    for b in pr.get("beispiele") or []:
        out.append(f"- {b.get('thema', '')}: {b.get('situation', '')} | Aufgabe: {b.get('aufgabe', '')} | "
                   f"Ich: {b.get('handlung', '')} | Ergebnis: {b.get('ergebnis', '') or '(offen)'}")
    out += ["", zeile("Warum dieser Beruf", pr.get("motivation_beruf")), zeile("Warum diese Firma", pr.get("motivation_firma")),
            "", "MEINE FRAGEN AN DIE FIRMA"]
    out += [f"- {f}" for f in gs.get("eigene_fragen") or ["(offen)"]]
    out += ["", "AM TAG", "- Weg + 10 Minuten Puffer · Unterlagen ausgedruckt · Kleidung eine Stufe formeller",
            "- Video: Technik testen, in die Kamera schauen, Handy lautlos",
            "- Am Ende fragen: Wie geht es weiter, wann höre ich von Ihnen?"]
    txt = "\n".join(out) + "\n"
    firma = textlib.safe_name(z.get("firma", ""), 30, "Firma")
    pfad, _ = textlib.neue_version(ordner, f"Gespraech_Spickzettel_{firma}", ".txt", mitziehen=(".txt", ".pdf"))
    open(pfad, "w", encoding="utf8").write(txt)
    res = [pfad]
    if pdf:
        p = os.path.splitext(pfad)[0] + ".pdf"
        err = txt_zu_pdf(txt, p)
        res.append(p if not err else err)
    return res


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
            d = textlib.lade_profil(a[1])
        except (RuntimeError, IndexError) as e:
            print(f"FEHLER: Akte nicht lesbar: {e}")
            sys.exit(2)
        ziel = opts.get("--json-nach", "/tmp/bewerbung/profil.json")
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        json.dump(d, open(ziel, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        m, z = d.get("meta") or {}, d.get("ziel") or {}
        print(f"✅ Daten übernommen → {ziel}")
        print(f"Stand: {m.get('stand', '?')} | Phase: {m.get('phase', '?')} | Nächster Schritt: {m.get('naechster_schritt', '?')}")
        print(f"Ziel: {z.get('stelle', '?')} bei {z.get('firma', '?')} | Frist: {z.get('frist', '?')}")
        if "schema" not in d:
            print("ℹ️ Alte Akte (v1): Profil-Felder fehlen – fehlende Fakten beim Nutzer nachfragen, nicht aus den Texten raten.")
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
        if a[0].endswith(".json"):   # Stand-Zeitstempel auch in der Arbeits-JSON
            json.dump(d, open(a[0], "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print("Zum Herunterladen geben. Ältere Akten nicht mehr hochladen (die neueste hat das jüngste Datum im Namen).")


if __name__ == "__main__":
    main()
