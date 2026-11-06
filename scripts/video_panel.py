"""Auswertung Zuschauer-Test: python3 scripts/video_panel.py docs/video_test/<folge>/  -> bericht.md + Zeile in verlauf.csv"""
import json, sys, glob, os, csv
from collections import Counter
d = sys.argv[1].rstrip("/")
folge = os.path.basename(d)
pers = {p["id"]: p for p in json.load(open("docs/produktsim/personas.json"))}
U = {}
for f in sorted(glob.glob(f"{d}/urteile_*.json")):
    U.update(json.load(open(f)))
fehlt = set(pers) - set(U)
if fehlt:
    sys.exit(f"Fehlende Archetypen: {sorted(fehlt)}")
W = sum(p["gewicht"] for p in pers.values())
def q(key):
    return sum(pers[i]["gewicht"] * U[i].get(key, 0) / 100 for i in pers) / W * 1000
dritte = "kauf" if any("kauf" in u for u in U.values()) else "folgen"
r = {"bis_ende": q("bis_ende"), "website": q("website"), dritte: q(dritte)}
def gruende(key, weg):
    c = Counter()
    for i, u in U.items():
        g = u.get(key, "-")
        if g and g != "-":
            c[g] += pers[i]["gewicht"] * (1 - u.get(weg, 0) / 100)
    tot = sum(c.values()) or 1
    return [(g, round(100 * v / tot)) for g, v in c.most_common(3)]
G = {"Wegwischen": gruende("grund_weg", "bis_ende"), "Kein Website-Klick": gruende("grund_kein_klick", "website"),
     "Kein Kauf" if dritte == "kauf" else "Kein Folgen": gruende("grund_kein_kauf", dritte)}
top = sorted(pers, key=lambda i: -pers[i]["gewicht"] * (U[i].get("website", 0) + 1))[:3]
lines = [f"# Zuschauer-Test {folge}", "", "Simuliertes Panel (50 gewichtete Archetypen = 1.000 Zuschauer). Richtgröße zum Vergleichen, keine Prognose.", "",
         f"- Schauen bis zum Ende: **{r['bis_ende']:.0f} von 1.000**",
         f"- Gehen auf die Website: **{r['website']:.0f} von 1.000**",
         f"- {'Würden kaufen' if dritte == 'kauf' else 'Würden folgen'}: **{r[dritte]:.0f} von 1.000**", ""]
for k, v in G.items():
    lines.append(f"**{k} – Top-Gründe:** " + ", ".join(f"{g} ({p} %)" for g, p in v))
lines += ["", "**Stimmen:**"] + [f"- {pers[i]['persona'][:60]}…: „{U[i].get('satz', '')}“" for i in top]
vf = "docs/video_test/verlauf.csv"
alt = list(csv.reader(open(vf))) if os.path.exists(vf) else [["folge", "bis_ende", "website", "kauf_oder_folgen", "echt_aufrufe_48h", "echt_klicks", "echt_kaeufe"]]
alt = [z for z in alt if z[0] != folge]
alt.append([folge, f"{r['bis_ende']:.0f}", f"{r['website']:.0f}", f"{r[dritte]:.0f}", "", "", ""])
csv.writer(open(vf, "w", newline="")).writerows(alt)
if len(alt) > 2:
    lines += ["", "**Vergleich letzte Tests (bis_ende / website / kauf|folgen pro 1.000):**"] + [f"- {z[0]}: {z[1]} / {z[2]} / {z[3]}" for z in alt[-6:-1]]
open(f"{d}/bericht.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
