#!/usr/bin/env python3
"""Endcheck für Bewerbungsunterlagen (Form und Stil – Fakten prüft fakten_check.py).

    python3 endcheck.py DATEI [DATEI …] --typ TYP [--firma "Beispiel GmbH"] [--stelle "Kauffrau …"]
                        [--profil PROFIL.json]

TYP: lebenslauf | anschreiben | motivationsschreiben | kurzanschreiben | formular | email | gesamt
     (gilt für alle Dateien des Aufrufs; ein Aufruf pro Dokumenttyp. Ohne --typ wird am INHALT geraten.)
--profil liefert Name, Firma, Stelle und frühere Arbeitgeber/Schulen (die sind kein Copy-and-paste-Rest).

Prüft u. a.: offene [PRÜFEN], Platzhalter, Floskeln, Konjunktiv, Länge, Seiten, Firmenname
(unscharf, ohne Rechtsform), ganze Stellenbezeichnung, fremde Firmennamen, Anrede, ATS-Layout,
E-Mail-Adresse (nur echte Probleme), Formular-Felder mit Zeichenlimit, Dateiname, Größe.
❌ = vor dem Abschicken beheben, ⚠️ = prüfen, ✅ = in Ordnung. Exit-Code 1 bei ❌.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

MAX_MB = 5
ANSCHR_MAX_WORTE = 420
KURZ_MIN, KURZ_MAX = 150, 200
TYPEN = ("lebenslauf", "anschreiben", "motivationsschreiben", "kurzanschreiben", "formular", "email", "gesamt")
BRIEF = ("anschreiben", "motivationsschreiben", "kurzanschreiben")

FLOSKELN = [
    "hiermit bewerbe ich mich", "hiermit", "mit großem interesse", "mit großer freude",
    "hat mich sofort angesprochen", "teamfähig, belastbar", "belastbar und flexibel",
    "über eine einladung zu einem vorstellungsgespräch würde ich mich", "würde mich freuen",
    "würde mich sehr freuen", "ich bin der perfekte kandidat", "die perfekte kandidatin",
    "in einer schnelllebigen welt", "leidenschaft für", "ihr renommiertes unternehmen",
    "ich bin überzeugt, dass ich", "wertvoller beitrag", "dynamisches team",
]
KONJUNKTIV = re.compile(r"\b(würde|würden|hätte|hätten|könnte|könnten|möchte gerne)\b", re.I)
PLATZHALTER = re.compile(r"(\[(?!PRÜFEN)[^\]\n]{1,60}\]|\bXXX+\b|\bMusterfirma\b|\bLorem ipsum\b|\bFirma XY\b|\bHerr/Frau\b|_{4,}|\.\.\.\s*$)", re.I | re.M)
PRUEFEN = re.compile(r"\[PRÜFEN:[^\]]*\]")
RECHTSFORM = r"(gGmbH|GmbH\s*&\s*Co\.?\s*KG|GmbH|AG\s*&\s*Co\.?\s*KG|AG|KGaA|KG|SE|e\.\s?V\.|GbR|OHG|UG(?:\s*\(haftungsbeschränkt\))?|mbH|Holding|Gruppe)"
FIRMEN = re.compile(r"\b([A-ZÄÖÜ][\wÄÖÜäöüß&.\-]*(?:\s+[A-ZÄÖÜ&][\wÄÖÜäöüß&.\-]*){0,3})\s+(gGmbH|GmbH|AG|KG|SE|e\.\s?V\.|GbR|OHG|UG|KGaA)\b")
STANDARD_UEBERSCHRIFTEN = re.compile(r"(berufserfahrung|praktische erfahrung|praktika|ausbildung|schulbildung|bildung|studium)", re.I)
MAIL_RE = re.compile(r"\b([\w.+-]+)@([\w-]+\.[\w.]+)")
MAIL_PROBLEM = ["party", "sexy", "hot", "cool", "gangster", "babe", "baby", "maus", "mausi", "schatz", "hase", "prinz",
                "princess", "prinzessin", "killer", "lol", "crazy", "boss", "king", "queen", "swag", "girl", "boy",
                "love", "dark", "devil", "angel", "bunny", "gamer", "zocker", "chiller", "styler", "suess", "süß",
                "engel", "teufel", "bad", "xx", "420", "1337", "69", "drunk", "beer", "bier", "bitch", "thug", "ninja"]
FELD_KOPF = re.compile(r"^===\s*(.+?)\s*(?:\(max\.?\s*(\d+)\s*Zeichen\))?\s*===\s*$", re.M)


def kern_firma(s):
    s = re.sub(RECHTSFORM, " ", s or "", flags=re.I)
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
    return [w for w in re.findall(r"[a-zäöüß0-9]{3,}", s.lower()) if w not in ("und", "für", "der", "die", "das", "als", "zum", "zur")]


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
            "stelle": (d.get("ziel") or {}).get("stelle", ""), "eigene": [e for e in eigene if e],
            "variante": (d.get("ziel") or {}).get("anschreiben_variante", "")}


def mail_check(mails, name):
    out = []
    teile = [textlib.translit(t.lower()) for t in (name or "").split() if len(t) > 1]
    for lokal, dom in mails:
        l = textlib.translit(lokal.lower())
        gruende = []
        if re.search(r"\d{3,}", l):
            gruende.append("Zahlenfolge")
        tr = [w for w in MAIL_PROBLEM if w in re.split(r"[._\-+0-9]+", l) or (len(w) >= 4 and w in l)]
        if tr:
            gruende.append("Spitzname/Jugendsprache („" + tr[0] + "“)")
        if teile and not any(t in l for t in teile):
            gruende.append("enthält deinen Namen nicht")
        if gruende:
            out.append(f"⚠️ E-Mail {lokal}@{dom}: " + ", ".join(gruende) + " – für Bewerbungen besser vorname.nachname@…")
    return out


def pruefe(pfad, typ=None, firma=None, stelle=None, info=None):
    info = info or {}
    befunde = []

    def add(sym, msg):
        befunde.append(f"{sym} {msg}")

    name = os.path.basename(pfad)
    try:
        txt = textlib.read_any(pfad)
    except RuntimeError as e:
        return [f"❌ Nicht lesbar: {e}"], typ
    if not txt.strip():
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
    if art == "formular":
        ph_txt = FELD_KOPF.sub("", txt)
    else:
        ph_txt = txt
    ph = [p if isinstance(p, str) else p[0] for p in PLATZHALTER.findall(ph_txt)]
    ph = [p for p in ph if p.strip()]
    if ph:
        add("❌", "Platzhalter gefunden: " + ", ".join(sorted(set(ph))[:5]))
    if re.search(r"[^A-Za-z0-9_.\-]", name):
        add("⚠️", f"Dateiname „{name}“ enthält Umlaute, Sonderzeichen oder Leerzeichen – besser {textlib.safe_name(os.path.splitext(name)[0], 60)}{os.path.splitext(name)[1]}")
    if re.search(r"_v\d+\.\w+$", name) and art not in ("formular", "email"):
        add("ℹ️", "Arbeitsfassung (_vN im Namen). Für den Versand: pdf_zusammenfuegen.py (Gesamt-PDF oder --einzeln).")
    mb = os.path.getsize(pfad) / 1024 / 1024
    if mb > MAX_MB:
        add("⚠️", f"Datei ist {mb:.1f} MB groß (Richtwert unter {MAX_MB} MB, Vorgabe der Anzeige geht vor).")
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

    if firma and art != "lebenslauf":
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
    if stelle and art in BRIEF + ("email", "formular"):
        kern = stelle_kern(stelle)
        t = textlib.translit(low)
        fehlt = [w for w in kern if textlib.translit(w) not in t]
        if fehlt and len(fehlt) == len(kern):
            add("⚠️", f"Stellenbezeichnung „{stelle}“ nicht gefunden – im Betreff genau wie in der Anzeige nennen.")
        elif fehlt:
            add("⚠️", f"Stellenbezeichnung unvollständig – es fehlt: {', '.join(fehlt)} (genau wie in der Anzeige: „{stelle}“).")

    if art in BRIEF:
        worte = len(textlib.words(txt))
        if art == "kurzanschreiben":
            if worte < KURZ_MIN - 30 or worte > KURZ_MAX + 40:
                add("⚠️", f"{worte} Wörter – Kurzanschreiben hat meist {KURZ_MIN}–{KURZ_MAX}.")
            else:
                add("✅", f"{worte} Wörter – passt als Kurzanschreiben.")
        elif worte > ANSCHR_MAX_WORTE:
            add("❌", f"{worte} Wörter – zu lang für eine Seite. Kürzen (3–4 Absätze).")
        else:
            add("✅", f"{worte} Wörter.")
        if not re.search(r"(sehr geehrte|guten tag|hallo|liebe[sr]? )", low):
            add("⚠️", "Keine Anrede gefunden.")
        saetze = [s for s in re.split(r"(?<=[.!?])\s+", txt) if len(s.split()) > 3]
        ich = sum(1 for s in saetze if s.strip().startswith("Ich "))
        if saetze and ich / len(saetze) > 0.4:
            add("⚠️", f"{ich} von {len(saetze)} Sätzen beginnen mit „Ich“ – Satzanfänge variieren.")
    if art in BRIEF + ("formular", "email"):
        gef = [f for f in FLOSKELN if f in low]
        gef = [f for f in gef if not any(f != g and f in g for g in gef)]
        if gef:
            add("⚠️", "Floskeln, die Personaler oft als KI-/Standardtext lesen: " + ", ".join(f"„{g}“" for g in gef))
        k = KONJUNKTIV.findall(txt)
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
            elif m.group(2) and len(inhalt) > int(m.group(2)):
                add("❌", f"Feld „{m.group(1)}“: {len(inhalt)} Zeichen, erlaubt {m.group(2)}.")
            if re.search(r"siehe (lebenslauf|anlage|anhang)", inhalt, re.I):
                add("❌", f"Feld „{m.group(1)}“: „siehe Lebenslauf“ – Feld richtig ausfüllen.")
    if art == "email":
        worte = len(textlib.words(txt))
        if worte > 140:
            add("⚠️", f"E-Mail hat {worte} Wörter – 3–5 Sätze reichen (Anschreiben nicht doppelt in die Mail).")
    if art == "lebenslauf":
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
