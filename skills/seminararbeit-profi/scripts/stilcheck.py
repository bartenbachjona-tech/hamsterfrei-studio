#!/usr/bin/env python3
"""Stil-Check für eine Seminararbeit.

Findet Floskeln, die nach KI klingen, Wertungen außerhalb des Fazits, Meta-Sätze,
leere Allgemeinplätze und misst, wie stark die Satzlängen schwanken.
Das ist KEIN KI-Detektor und beweist nichts über die Urheberschaft.
Es zeigt Stellen, die Lehrkräfte typischerweise anstreichen.

    python stilcheck.py Arbeit.docx [--vergleich eigener_alter_text.txt] > stil_bericht.md

--vergleich: ein Text, den man nachweislich selbst geschrieben hat (z. B. ein altes
Referat). Dann werden die Messwerte nebeneinander gestellt.
"""
import argparse
import re
import statistics

from textlib import body_paragraphs, read_any, read_docx, sentences, words

FLOSKELN = [
    r"darüber hinaus", r"spielt eine (zentrale|entscheidende|wichtige|wesentliche|bedeutende) rolle",
    r"von (zentraler|entscheidender|großer|besonderer) bedeutung", r"maßgeblich", r"vielfältig\w*",
    r"faszinierend\w*", r"einzigartig\w*", r"fluch und segen", r"zusammenfassend lässt sich",
    r"lässt sich (festhalten|feststellen|sagen)", r"es (ist|bleibt) (wichtig|festzuhalten|zu beachten)",
    r"(insgesamt|letztlich|somit) zeigt sich", r"spannungsfeld", r"im hinblick auf",
    r"in diesem zusammenhang", r"essenziell\w*", r"unerlässlich\w*", r"bemerkenswert\w*",
    r"eindrucksvoll\w*", r"schlüsselrolle", r"tiefgreifend\w*", r"facettenreich\w*",
    r"komplexe[sn]? zusammenspiel", r"nicht zuletzt", r"gilt es zu", r"stellt .{0,30} dar,? (wie|dass)",
    r"wirft .{0,20}fragen auf", r"vor diesem hintergrund", r"im spannungsfeld", r"zunehmend an bedeutung",
    r"einen wichtigen beitrag", r"ein zentrales element", r"ganzheitlich\w*", r"nahtlos\w*",
    r"\bim kern\b", r"ebenso wichtig", r"nicht nur\b.{0,80}\bsondern auch",
]
WERTUNG = [
    r"herausragend\w*", r"überraschend\w*", r"erstaunlich\w*", r"gewaltig\w*", r"enorm\w*",
    r"dramatisch\w*", r"\bleider\b", r"glücklicherweise", r"hervorragend\w*", r"beeindruckend\w*",
    r"unglaublich\w*", r"katastrophal\w*", r"perfekt\w*", r"\bideal(e[nrs]?)?\b", r"erschreckend\w*", r"zu recht\b", r"bedenklich\w*", r"großartig\w*", r"alleinstellungsmerkmal\w*",
    r"verheerend\w*", r"schockierend\w*", r"wunderschön\w*", r"atemberaubend\w*", r"zum glück",
    r"bedauerlich\w*", r"erfreulich\w*", r"besorgniserregend\w*", r"das zeigt,? wie",
]
META = [
    r"(dieses|in diesem|im folgenden|im nächsten) kapitel", r"im folgenden", r"diese arbeit",
    r"in dieser arbeit", r"soll (gezeigt|untersucht|dargestellt|erläutert) werden",
    r"wird (nun|im folgenden) (gezeigt|untersucht|dargestellt|erläutert)", r"wie (bereits )?(oben )?erwähnt",
]
LEER = [
    r"trägt (wesentlich|entscheidend|maßgeblich) (zu|bei)", r"eine (wichtige|große|zentrale) rolle",
    r"vielfältige (herausforderungen|auswirkungen|gründe)", r"in vielerlei hinsicht",
    r"auf verschiedenen ebenen", r"in hohem maße", r"in gewisser weise", r"gewissermaßen",
]


def find(patterns, text):
    hits = []
    for p in patterns:
        if not p.startswith("\\b"):
            p = r"\b" + p
        for m in re.finditer(p, text, re.I):
            hits.append(m.group(0))
    return hits


def metrics(text):
    sents = [s for s in sentences(text) if len(words(s)) >= 3]
    lens = [len(words(s)) for s in sents]
    w = sum(lens) or 1
    if len(lens) < 3:
        return None
    mean = statistics.mean(lens)
    sd = statistics.pstdev(lens)
    # Wechsel zwischen aufeinanderfolgenden Sätzen
    jumps = statistics.mean(abs(a - b) for a, b in zip(lens, lens[1:]))
    floskeln = len(find(FLOSKELN, text))
    dashes = len(re.findall(r"\s[–—]\s", text))
    dreier = len(re.findall(r"\b\w+, \w+(?: \w+)? und \w+\b", text))
    return {
        "Sätze": len(lens),
        "Wörter": w,
        "Satzlänge Mittel": round(mean, 1),
        "Satzlänge Streuung (SD)": round(sd, 1),
        "Schwankung (SD/Mittel)": round(sd / mean, 2),
        "Sprung von Satz zu Satz": round(jumps, 1),
        "Floskeln je 1.000 Wörter": round(floskeln * 1000 / w, 1),
        "Gedankenstriche je 1.000 Wörter": round(dashes * 1000 / w, 1),
        "Dreierlisten je 1.000 Wörter": round(dreier * 1000 / w, 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--vergleich")
    a = ap.parse_args()

    if a.datei.lower().endswith(".docx"):
        doc = read_docx(a.datei)
        blocks = [(kap or "Text", p["text"]) for kap, _, p in body_paragraphs(doc)]
    else:
        blocks = [("Text", t) for t in read_any(a.datei).split("\n") if t.strip()]

    funde = []  # (art, kapitel, fund, satz)
    in_fazit = False
    for kap, text in blocks:
        k = (kap or "").strip()
        hauptnr = re.match(r"^(\d+)", k)
        if re.search(r"(?i)\b(fazit|schluss|bewertung|resümee|zusammenfassung)\b", k):
            in_fazit = True
            fazit_nr = hauptnr.group(1) if hauptnr else None
        elif in_fazit and hauptnr and fazit_nr and hauptnr.group(1) != fazit_nr:
            in_fazit = False
        fazit = in_fazit
        einleitung = bool(re.search(r"(?i)einleitung", k))
        for s in sentences(text):
            for art, pats in (("Floskel", FLOSKELN), ("Meta-Satz", [] if einleitung else META), ("Leerformel", LEER)):
                for h in find(pats, s):
                    funde.append((art, kap, h, s))
            if not fazit:
                for h in find(WERTUNG, s):
                    funde.append(("Wertung außerhalb des Fazits", kap, h, s))
            if len(words(s)) > 38:
                funde.append(("Sehr langer Satz", kap, f"{len(words(s))} Wörter", s))

    gesamt = "\n".join(t for _, t in blocks)
    m = metrics(gesamt)

    print("# Stil-Check\n")
    print("Kein Werkzeug kann beweisen, wer einen Text geschrieben hat. Dieser Check zeigt Stellen, "
          "die sachlicher, konkreter oder eigener werden können. Inhalt nur mit Beleg ändern.\n")
    if m:
        print("## Messwerte\n")
        vm = metrics(read_any(a.vergleich, nur_hauptteil=False)) if a.vergleich else None
        if vm:
            print("| Wert | Arbeit | Vergleichstext (selbst geschrieben) |\n|---|---|---|")
            for k in m:
                print(f"| {k} | {m[k]} | {vm.get(k, '–')} |")
        else:
            print("| Wert | Arbeit |\n|---|---|")
            for k, v in m.items():
                print(f"| {k} | {v} |")
        print("\nSo liest man das: Menschliche Sachtexte haben meist eine größere Schwankung der Satzlänge "
              "und mehr Sprünge von Satz zu Satz. Sehr gleichmäßige Sätze, viele Floskeln, Gedankenstrich-Einschübe "
              "und Dreierlisten wirken glatt. Feste Grenzwerte gibt es nicht; am aussagekräftigsten ist der "
              "Vergleich mit einem eigenen, älteren Text (Option --vergleich).\n")
    by_art = {}
    for f in funde:
        by_art.setdefault(f[0], []).append(f)
    print(f"## Fundstellen ({len(funde)})\n")
    for art in ("Wertung außerhalb des Fazits", "Meta-Satz", "Leerformel", "Floskel", "Sehr langer Satz"):
        items = by_art.get(art, [])
        if not items:
            continue
        print(f"### {art} ({len(items)})\n")
        for _, kap, h, s in items[:60]:
            s2 = s if len(s) < 220 else s[:217] + "…"
            print(f"- **{h}** · {kap}: „{s2}“")
        print()
    if not funde:
        print("Keine typischen Fundstellen.\n")


if __name__ == "__main__":
    main()
