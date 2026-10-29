#!/usr/bin/env python3
"""Plagiats-Selbstcheck: vergleicht die Arbeit mit den eigenen Quellentexten.

Findet (1) wortgleiche Passagen ab N Wörtern, die NICHT als Zitat in „…“ stehen, und
(2) Sätze, die zu nah an einem Quellensatz formuliert sind (umgestellte Wörter, gleiche Struktur).
Verglichen wird nur mit den Quellen, die du angibst (PDF, DOCX, TXT, HTML). Eine Datenbank
wie bei Turnitin gibt es hier nicht – Quellen, die nicht im Ordner liegen, werden nicht erkannt.

    python plagiat_check.py Arbeit.docx Quellenordner/ [--n 7] [--nah 0.55] > plagiat_bericht.md
"""
import argparse
import os
import re
import sys
from collections import defaultdict

from textlib import read_any, sentences, words

STOP = set("""der die das den dem des ein eine einer eines einem einen und oder aber in im ins an am auf aus bei mit nach
von vom zu zum zur für über unter vor hinter neben zwischen durch gegen ohne um als wie so auch nur noch schon sehr mehr
ist sind war waren wird werden wurde wurden hat haben hatte hatten sein seine ihr ihre es sich nicht kein keine dass daß
the a an and or of to in on at for with by from is are was were be been this that these those it its as not""".split())


def norm_tokens(text):
    return [w.lower().replace("’", "'") for w in words(text)]


def quoted_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"[„\"»“][^„“\"»«]{2,}?[“\"«”]", text)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arbeit")
    ap.add_argument("quellen", nargs="+", help="Ordner oder Dateien")
    ap.add_argument("--n", type=int, default=7, help="Mindestlänge wortgleicher Passagen")
    ap.add_argument("--nah", type=float, default=0.55, help="Ähnlichkeitsschwelle für zu nahe Sätze (0–1)")
    a = ap.parse_args()

    files = []
    for q in a.quellen:
        if os.path.isdir(q):
            for root, _, fs in os.walk(q):
                files += [os.path.join(root, f) for f in fs if f.lower().endswith((".pdf", ".docx", ".txt", ".md", ".html", ".htm"))]
        else:
            files.append(q)
    if not files:
        sys.exit("Keine Quellendateien gefunden.")

    arbeit = read_any(a.arbeit)
    if len(words(arbeit)) < 50:
        sys.exit("❌ In der Arbeit wurde kaum Text erkannt. Nichts geprüft. Bitte die Arbeit als normale .docx hochladen.")
    # Tokens der Arbeit mit Zeichenposition, um Zitate zu erkennen
    toks = [(m.group(0).lower().replace("’", "'"), m.start()) for m in re.finditer(r"[A-Za-zÄÖÜäöüßÀ-ÿĀ-žÞþÐð0-9]+(?:[-'’][A-Za-zÄÖÜäöüßÀ-ÿ0-9]+)*", arbeit)]
    qs = quoted_spans(arbeit)

    def in_quote(pos):
        return any(s <= pos <= e for s, e in qs)

    n = a.n
    src_texts, index = {}, defaultdict(set)
    for f in files:
        try:
            t = read_any(f, nur_hauptteil=False)
            if len(words(t)) < 30:
                print(f"> ⚠️ `{os.path.basename(f)}`: kaum Text lesbar (z. B. eingescanntes PDF). Diese Quelle wurde NICHT verglichen.\n")
                continue
        except Exception as e:
            print(f"<!-- {f}: nicht lesbar ({e}) -->")
            continue
        name = os.path.basename(f)
        src_texts[name] = t
        st = norm_tokens(t)
        for i in range(len(st) - n + 1):
            index[tuple(st[i:i + n])].add(name)

    words_only = [w for w, _ in toks]
    hit = [None] * len(words_only)
    for i in range(len(words_only) - n + 1):
        g = tuple(words_only[i:i + n])
        if g in index:
            src = sorted(index[g])[0]
            for k in range(i, i + n):
                hit[k] = src
    runs = []
    i = 0
    while i < len(hit):
        if hit[i]:
            j = i
            while j < len(hit) and hit[j] == hit[i]:
                j += 1
            start, end = toks[i][1], toks[j - 1][1] + len(toks[j - 1][0])
            runs.append((hit[i], j - i, arbeit[start:end], in_quote(start) and in_quote(end - 1)))
            i = j
        else:
            i += 1

    # zu nahe Sätze
    src_sents = []
    for name, t in src_texts.items():
        for s in sentences(t):
            cw = {w for w in norm_tokens(s) if w not in STOP and len(w) > 2}
            if len(cw) >= 6:
                src_sents.append((name, s, cw))
    inv = defaultdict(list)
    for idx, (_, _, cw) in enumerate(src_sents):
        for w in cw:
            inv[w].append(idx)
    nah = []
    for s in sentences(arbeit):
        if re.search(r"[„\"»]", s):
            continue
        cw = {w for w in norm_tokens(s) if w not in STOP and len(w) > 2}
        if len(cw) < 6:
            continue
        cand = defaultdict(int)
        for w in cw:
            for idx in inv.get(w, ()):
                cand[idx] += 1
        best, bscore = None, 0
        for idx, c in cand.items():
            score = c / len(cw | src_sents[idx][2])
            if score > bscore:
                best, bscore = idx, score
        if best is not None and bscore >= a.nah:
            nah.append((bscore, s, src_sents[best][0], src_sents[best][1]))

    total_words = len(words_only) or 1
    unmarked = [r for r in runs if not r[3]]
    marked = [r for r in runs if r[3]]
    share = sum(r[1] for r in unmarked) * 100 / total_words

    print("# Plagiats-Selbstcheck\n")
    print(f"Arbeit: `{os.path.basename(a.arbeit)}` · {total_words} Wörter · verglichen mit {len(src_texts)} Quelle(n)\n")
    print("Grenze: Verglichen wird nur mit diesen Quellen. Für alles andere gibt es keine Garantie.\n")
    print(f"## Wortgleiche Passagen ohne Anführungszeichen ({len(unmarked)}, ≈ {share:.1f} % des Textes)\n")
    if not unmarked:
        print("Keine gefunden. ✅\n")
    for src, ln, txt, _ in sorted(unmarked, key=lambda r: -r[1]):
        print(f"- **{ln} Wörter** aus `{src}`: „{txt[:300]}“  \n  → Entweder als wörtliches Zitat in „…“ mit Fußnote (ohne „Vgl.“) oder in eigenen Worten neu formulieren (mit „Vgl.“).")
    print(f"\n## Zu nah am Original formuliert ({len(nah)})\n")
    if not nah:
        print("Keine gefunden. ✅\n")
    for score, s, src, ss in sorted(nah, reverse=True)[:40]:
        print(f"- Ähnlichkeit {score:.0%} · `{src}`  \n  Arbeit: „{s[:250]}“  \n  Quelle: „{ss[:250]}“  \n  → Satzbau und Wortwahl stärker ändern; Beleg mit „Vgl.“ muss stehen.")
    # Wörtliche Zitate vollständig prüfen
    def nz(t):
        t = re.sub(r"-\s*\n\s*", "", t)  # Silbentrennung am Zeilenende
        return " ".join(norm_tokens(t))
    src_norm = {n: nz(t) for n, t in src_texts.items()}
    ok_q, bad_q = [], []
    for m in re.finditer(r"[„\"»“]([^„“\"»«”]{12,}?)[“\"«”]", arbeit):
        q = m.group(1)
        parts = [nz(x) for x in re.split(r"\(…\)|\[…\]|\(\.\.\.\)|\[\.\.\.\]|…", q) if len(norm_tokens(x)) >= 2]
        if not parts or len(norm_tokens(q)) < 4:
            continue
        hit = [n for n, t in src_norm.items() if all(pt in t for pt in parts)]
        (ok_q if hit else bad_q).append((q, hit))
    print(f"\n## Wörtliche Zitate im Abgleich ({len(ok_q)} ✅, {len(bad_q)} ⚠️)\n")
    for q, hit in bad_q:
        print(f"- ⚠️ „{q[:200]}“ – **in keiner hochgeladenen Quelle wortgleich gefunden.** Entweder weicht der Wortlaut ab (Tippfehler, andere Formulierung) oder die Quelle fehlt hier. Mit dem Original vergleichen.")
    for q, hit in ok_q:
        print(f"- ✅ „{q[:120]}“ – stimmt wortgleich mit `{hit[0]}` überein")
    if not ok_q and not bad_q:
        print("Keine wörtlichen Zitate (ab 4 Wörtern) gefunden.")


if __name__ == "__main__":
    main()
