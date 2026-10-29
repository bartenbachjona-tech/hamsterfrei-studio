#!/usr/bin/env python3
"""Formalia-Check für eine Seminararbeit (.docx).

Prüft Layout, Umfang, Fußnoten, Zitate, Abbildungen und den Abgleich
Fußnoten <-> Literaturverzeichnis. Gibt einen Bericht als Markdown aus.

    python formalia_check.py Arbeit.docx [--woerter-pro-seite 300] [--soll-seiten 10-15]
        [--schrift "Calibri 12,Arial 11"] [--zeilenabstand 1.5] > formalia_bericht.md

Alles ist eine Prüfhilfe. Maßgeblich sind Merkblatt und Lehrkraft.
"""
import argparse
import re
import sys
from collections import Counter, defaultdict

from textlib import STOP_HEADINGS, CAPTION_RE, body_paragraphs, chapters, read_docx, words

QUOTE_RE = re.compile(r"[„\"»]([^“\"«]{3,}?)[“\"«]")
CITE_RE = re.compile(
    r"((?:[A-ZÀ-ÖØ-ÞĀ-Ž][\wÄÖÜäöüßðþæøáéíóúý\-]+\s){0,3}[A-ZÀ-ÖØ-ÞĀ-Ž][\wÄÖÜäöüßðþæøáéíóúý\-]+(?:\s?/\s?[A-ZÀ-ÖØ-ÞĀ-Ž][\wÄÖÜäöüßðþæøáéíóúý\-]+)*(?:\s+u\.\s?a\.)?)"
    r"(?:\s+\([^)]*\))?\s+(\d{4}[a-z]?|o\.\s?J\.[a-z]?)"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--woerter-pro-seite", type=int, default=300)
    ap.add_argument("--soll-seiten", default="10-15")
    ap.add_argument("--schrift", default="Calibri 12,Arial 11")
    ap.add_argument("--zeilenabstand", type=float, default=1.5)
    a = ap.parse_args()

    doc = read_docx(a.docx)
    paras = doc["paragraphs"]
    fns = doc["footnotes"]
    nr = lambda fid: doc["fn_nr"].get(fid, fid)
    probleme, hinweise, ok = [], [], []

    # ---------------- Umfang
    body = body_paragraphs(doc)
    wc = sum(len(words(p["text"])) for _, _, p in body)
    if wc == 0:
        print("# Formalia-Check\n\n❌ **Kein Fließtext erkannt.** Die Datei ist leer, oder der Text steht in Textfeldern bzw. Tabellen. Nichts ist geprüft. Bitte die Arbeit als normale Word-Datei (.docx) hochladen.")
        return
    if not doc.get("struktur_erkannt", True):
        probleme.append("**Gliederung nicht erkannt:** Die Überschriften sind keine Formatvorlagen („Überschrift 1/2“) und auch nicht als nummerierte Zeilen erkennbar. Geprüft wurde deshalb der ganze Text. Empfehlung: Überschriften in Word als „Überschrift 1“ bzw. „Überschrift 2“ formatieren, dann klappt auch das automatische Inhaltsverzeichnis.")
    pseudo = [p["text"] for p in doc["paragraphs"] if "(als Überschrift erkannt)" in p["style"]]
    if pseudo:
        hinweise.append(f"{len(pseudo)} Überschrift(en) sind nur fett bzw. per Hand nummeriert, keine Formatvorlage (z. B. „{pseudo[0][:50]}“). Für ein automatisches Inhaltsverzeichnis in Word als „Überschrift 1/2“ formatieren.")
    seiten = wc / a.woerter_pro_seite
    lo, hi = [float(x) for x in a.soll_seiten.split("-")]
    zeile = f"Fließtext im Hauptteil: **{wc} Wörter ≈ {seiten:.1f} reine Textseiten** (bei {a.woerter_pro_seite} Wörtern je Seite)."
    if seiten > hi:
        probleme.append(zeile + f" Das liegt über der Vorgabe von {a.soll_seiten} Seiten. Kürzen nötig: etwa {int(wc - hi * a.woerter_pro_seite)} Wörter.")
    elif seiten < lo:
        hinweise.append(zeile + f" Das liegt unter {a.soll_seiten} Seiten.")
    else:
        ok.append(zeile)

    # ---------------- Layout
    m = doc["margins"]
    if m:
        ok_m = f"Ränder: oben {m['top']} cm, unten {m['bottom']} cm, links {m['left']} cm, rechts {m['right']} cm."
        (hinweise if (m["left"] < 2.4 or m["right"] < 2.4) else ok).append(
            ok_m + (" Häufige Vorgabe: links ca. 3 cm, rechts ca. 3–4 cm, oben/unten ca. 2,5 cm. Mit dem Merkblatt vergleichen." if (m["left"] < 2.4 or m["right"] < 2.4) else " Mit dem Merkblatt vergleichen.")
        )
    fonts, sizes, lines, jcs = Counter(), Counter(), Counter(), Counter()
    for _, _, p in body:
        n = len(p["text"])
        for f, c in p["fonts"].items():
            fonts[f] += c
        for s, c in p["sizes"].items():
            sizes[s] += c
        lines[str(p["line"])] += n
        jcs[p["jc"]] += n
    total = sum(lines.values()) or 1

    def share(counter):
        t = sum(counter.values()) or 1
        return ", ".join(f"{k} ({v * 100 / t:.0f} %)" for k, v in counter.most_common(3))

    erlaubt = [x.strip() for x in a.schrift.split(",")]
    haupt_f = fonts.most_common(1)[0][0] if fonts else None
    haupt_s = sizes.most_common(1)[0][0] if sizes else None
    kombi = f"{haupt_f} {haupt_s:g}" if haupt_f and haupt_s else "unbekannt"
    if kombi in erlaubt:
        ok.append(f"Schrift im Fließtext: {share(fonts)}; Größe: {share(sizes)} pt.")
    else:
        hinweise.append(f"Schrift im Fließtext: {share(fonts)}; Größe: {share(sizes)} pt. Erwartet: {a.schrift}. Steht „None“ da, kommt die Schrift aus dem Design; in Word nachsehen.")
    if len(fonts) > 1 and fonts.most_common(2)[1][1] / (sum(fonts.values()) or 1) > 0.05:
        probleme.append(f"Mehrere Schriften im Fließtext gemischt: {share(fonts)}.")
    soll_line = str(a.zeilenabstand if a.zeilenabstand != int(a.zeilenabstand) else int(a.zeilenabstand))
    falsch = sum(v for k, v in lines.items() if k not in (soll_line, str(a.zeilenabstand)))
    if falsch / total > 0.05:
        probleme.append(f"Zeilenabstand im Fließtext: {share(lines)}. Vorgabe: {a.zeilenabstand}-fach.")
    else:
        ok.append(f"Zeilenabstand {a.zeilenabstand}-fach im Fließtext.")
    if jcs.get("both", 0) / total < 0.9:
        hinweise.append(f"Ausrichtung: {share(jcs)}. Meist ist Blocksatz („both“) vorgegeben.")
    else:
        ok.append("Blocksatz im Fließtext.")
    if not doc["autoHyphenation"]:
        hinweise.append("Automatische Silbentrennung ist aus (Layout → Silbentrennung → Automatisch). Bei Blocksatz sonst große Lücken.")
    else:
        ok.append("Automatische Silbentrennung an.")
    if any(h["seitenzahl"] for h in doc["headers"]):
        ok.append("Seitenzahl in der Kopfzeile gefunden" + (" (zentriert)." if any(h["seitenzahl"] and h["zentriert"] for h in doc["headers"]) else ". Ausrichtung prüfen."))
    elif any(f["seitenzahl"] for f in doc["footers"]):
        hinweise.append("Seitenzahl steht in der Fußzeile. Viele Merkblätter wollen sie oben in der Mitte.")
    else:
        probleme.append("Keine Seitenzahl gefunden.")

    # ---------------- Überschriften, leere Absätze
    heads = [p for p in paras if p["heading"] and p["text"].strip()]
    nonum = [p["text"] for p in heads if not p["numbered"] and not re.match(r"^\d+(\.\d+)*\.?\s", p["text"]) and not STOP_HEADINGS.match(p["text"]) and not re.match(r"(?i)^(inhalt|fazit|einleitung|schluss)", p["text"])]
    if nonum:
        hinweise.append("Überschriften ohne erkennbare Nummer: " + "; ".join(nonum[:6]))
    nokeep = [p["text"] for p in heads if not p["keepNext"]]
    if nokeep:
        hinweise.append(f"{len(nokeep)} Überschrift(en) ohne „Mit nächstem Absatz zusammenhalten“ – Gefahr: Überschrift allein am Seitenende. Beispiele: " + "; ".join(nokeep[:4]))
    empty = 0
    for _, i, p in chapters(doc):
        if not p["text"].strip() and not p["image"]:
            empty += 1
    if empty:
        probleme.append(f"{empty} leere Absätze im Hauptteil (als Abstandshalter). Entfernen und Abstände über „Abstand vor/nach“ lösen.")
    # Unterkapitel-Regel
    lvl1 = defaultdict(int)
    cur = None
    for p in heads:
        if STOP_HEADINGS.match(p["text"]):
            break
        if p["level"] == 1:
            cur = p["text"]
            lvl1[cur] += 0
        elif p["level"] == 2 and cur:
            lvl1[cur] += 1
    einzeln = [k for k, v in lvl1.items() if v == 1]
    if einzeln:
        probleme.append("Kapitel mit nur EINEM Unterkapitel (entweder mind. zwei oder keins): " + "; ".join(einzeln))

    # ---------------- Fußnoten
    order = []  # (fid, kapitel, absatztext)
    for kap, i, p in chapters(doc):
        for fid in p["refs"]:
            order.append((fid, kap, p))
    # Fußnoten in Bildunterschriften zählen mit
    fn_probleme = []
    stellung = Counter()
    for fid, kap, p in order:
        t = fns.get(fid, "")
        if not t:
            fn_probleme.append(f"Fußnote {nr(fid)} ist leer.")
            continue
        if not t.rstrip().endswith("."):
            fn_probleme.append(f"Fußnote {nr(fid)} endet nicht mit Punkt: „{t[:80]}“")
        if re.match(r"vgl\.", t):
            fn_probleme.append(f"Fußnote {nr(fid)} beginnt mit kleinem „vgl.“ → „Vgl.“")
        mk = p["text_marked"]
        mpos = mk.find(f"⁣FN{fid}⁣")
        before = mk[:mpos].rstrip()[-1:] if mpos > 0 else ""
        after = mk[mpos + len(f"⁣FN{fid}⁣"):][:1]
        if before in ".,;:!?“\"":
            stellung["nach dem Satzzeichen"] += 1
        elif after in (".", ",", ";", ":"):
            stellung["vor dem Satzzeichen"] += 1
    if len(stellung) > 1:
        fn_probleme.append(f"Fußnotenzeichen uneinheitlich: {dict(stellung)}. Einheitlich machen (meist nach dem Satzzeichen).")
    # ebd.-Ketten
    prev_kap = None
    for idx, (fid, kap, p) in enumerate(order):
        t = fns.get(fid, "")
        if re.search(r"\bebd\.", t, re.I):
            if idx == 0:
                fn_probleme.append(f"Fußnote {nr(fid)}: „ebd.“ in der ersten Fußnote.")
            elif kap != prev_kap:
                fn_probleme.append(f"Fußnote {nr(fid)}: „ebd.“ direkt nach einem Kapitelwechsel ({kap}). Hier den vollen Kurzbeleg nennen.")
            elif ";" in fns.get(order[idx - 1][0], ""):
                fn_probleme.append(f"Fußnote {nr(fid)}: „ebd.“ nach einer Fußnote mit mehreren Quellen. Unklar, welche gemeint ist; vollen Kurzbeleg nennen.")
            elif CAPTION_RE.match(order[idx - 1][2]["text"].strip()):
                fn_probleme.append(f"Fußnote {nr(fid)}: „ebd.“ nach einer Bildunterschrift-Fußnote. Prüfen, ob wirklich dieselbe Quelle gemeint ist.")
        prev_kap = kap
    # Zitate vs. Vgl.
    zit_probleme = []
    n_quotes = 0
    for kap, i, p in body:
        mk = p["text_marked"]
        for q in QUOTE_RE.finditer(mk):
            n_quotes += 1
            rest = mk[q.end():]
            m2 = re.search(r"⁣FN(\d+)⁣", rest)
            if not m2 or len(rest[: m2.start()]) > 160:
                zit_probleme.append(f"Zitat ohne nahe Fußnote ({kap}): „{q.group(1)[:70]}“")
                continue
            ft = fns.get(m2.group(1), "")
            if ft.startswith(("Vgl", "vgl")):
                zit_probleme.append(f"Wörtliches Zitat, aber Fußnote {nr(m2.group(1))} beginnt mit „Vgl.“ ({kap}): „{q.group(1)[:60]}“ – bei wörtlichen Zitaten ohne „Vgl.“")
    # Fußnoten ohne Seitenangabe (nur Hinweis)
    ohne_seite = [fid for fid, _, _ in order if fns.get(fid) and not re.search(r"\b(S\.|Kap\.|Abs\.|Tab|Tabelle|o\.\s?S\.|ebd\.|URL|http|eigene)", fns[fid]) and CITE_RE.search(fns[fid])]
    if ohne_seite:
        hinweise.append(f"{len(ohne_seite)} Fußnote(n) ohne Seiten- oder Kapitelangabe (bei Webseiten ohne Seiten ist das normal): Nr. " + ", ".join(str(nr(x)) for x in ohne_seite[:15]))

    # Prozentzeichen ohne Leerzeichen
    pz = [m.group(0) for _, _, p in body for m in re.finditer(r"\d%", p["text"])]
    if pz:
        hinweise.append(f"{len(pz)}× Prozentzeichen ohne Leerzeichen (z. B. „{pz[0]}“). Deutsche Schreibweise: „8,8 %“.")

    # ---------------- Literaturverzeichnis-Abgleich
    lit = []
    in_lit = False
    for p in paras:
        t = p["text"].strip()
        if p["heading"] and t:
            in_lit = bool(re.match(r"(?i)^(\d+\.?\s*)?(literatur|quellen)", t))
            continue
        if in_lit and t:
            lit.append(t)
    zitiert = Counter()
    for fid, _, _ in order:
        for name, jahr in CITE_RE.findall(fns.get(fid, "")):
            name = re.sub(r"^(Vgl\.?|Eigene|Darstellung|Berechnung|Stand|Nach|Und|Abbildung)\s+", "", name.strip())
            name = re.sub(r"^(nach|und)\s+", "", name)
            if name.lower() in ("vgl", "ebd", "abbildung", "eigene", "stand", "darstellung", "nach", "berechnung"):
                continue
            zitiert[(name.split("/")[0].replace(" u. a.", "").strip(), jahr.replace(" ", ""))] += 1
    fehlt_im_lit = []
    for (name, jahr), c in zitiert.items():
        hit = any(e.startswith(name) and (jahr.rstrip("abcdefg") in e.replace(" ", "")) for e in lit)
        if not hit:
            hit = any(name in e and jahr.rstrip("abcdefg") in e.replace(" ", "") for e in lit)
        if not hit:
            fehlt_im_lit.append(f"{name} {jahr}")
    nie_zitiert = []
    for e in lit:
        first = re.split(r"[,:/(]", e)[0].strip()
        if not first or len(first) < 2:
            continue
        if not any(n == first or first.startswith(n) or n.startswith(first) for (n, _) in zitiert):
            nie_zitiert.append(e[:90])
    if not lit:
        probleme.append("Kein Literaturverzeichnis gefunden (Überschrift „Literaturverzeichnis“ oder „Quellen…“).")
    else:
        alpha = [re.sub(r"[^a-zäöüß]", "", e.lower())[:12] for e in lit]
        if alpha != sorted(alpha):
            hinweise.append("Literaturverzeichnis ist evtl. nicht alphabetisch sortiert.")
        ok.append(f"Literaturverzeichnis: {len(lit)} Einträge; {len(zitiert)} verschiedene Kurzbelege in Fußnoten.")
        if fehlt_im_lit:
            probleme.append("In Fußnoten zitiert, im Literaturverzeichnis nicht gefunden (Heuristik, bitte prüfen): " + "; ".join(fehlt_im_lit[:20]))
        if nie_zitiert:
            hinweise.append("Im Literaturverzeichnis, aber in keiner Fußnote erkannt (Heuristik): " + " | ".join(nie_zitiert[:12]))
        no_date = [e[:70] for e in lit if re.search(r"https?://|www\.", e) and not re.search(r"(?i)abgerufen|abruf|zugriff", e)]
        if no_date:
            probleme.append(f"{len(no_date)} Internetquelle(n) ohne Abrufdatum: " + " | ".join(no_date[:6]))

    # ---------------- Abbildungen
    caps = [p["text"].strip() for p in paras if CAPTION_RE.match(p["text"].strip())]
    nums = [int(re.search(r"\d+", c).group()) for c in caps if c.lower().startswith(("abbildung", "abb"))]
    if nums and nums != list(range(1, len(nums) + 1)):
        probleme.append(f"Abbildungsnummern nicht fortlaufend: {nums}")
    alltext = " ".join(p["text"] for _, _, p in body)
    for n in nums:
        if not re.search(rf"(Abbildung|Abb\.)\s*{n}\b", alltext):
            hinweise.append(f"Abbildung {n} wird im Fließtext nicht erwähnt (z. B. „vgl. Abbildung {n}“).")
    if doc["images"] and not caps:
        hinweise.append(f"{doc['images']} Bild(er), aber keine Beschriftung „Abbildung n: …“ gefunden.")
    if caps:
        ok.append(f"{len(caps)} Bildunterschrift(en) gefunden.")

    # ---------------- Ausgabe
    print("# Formalia-Check\n")
    print(f"Datei: `{a.docx}`  ")
    print(f"Fußnoten: {len(order)} · wörtliche Zitate im Text: {n_quotes} · Abbildungen: {doc['images']}\n")
    print("Maßgeblich sind Merkblatt und Lehrkraft. Dieser Check ist eine Prüfhilfe.\n")
    sec = [("❌ Zu korrigieren", probleme + fn_probleme + zit_probleme), ("⚠️ Prüfen", hinweise), ("✅ In Ordnung", ok)]
    for title, items in sec:
        print(f"## {title} ({len(items)})\n")
        for it in items:
            print(f"- {it}")
        print()


if __name__ == "__main__":
    main()
