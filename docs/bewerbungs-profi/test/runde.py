"""Ziehe eine Stichprobe für Runde N (geschichtet nach 'stand', ohne Wiederholung über Runden) und werte Urteile aus.
python3 runde.py ziehen N GROESSE   -> runde_N/stichprobe.json + 4 Pakete
python3 runde.py auswerten N        -> Zusammenfassung aus runde_N/urteile.json
"""
import json, random, sys, os, glob
from collections import Counter
U = json.load(open("nutzer_1000.json"))
cmd, n = sys.argv[1], int(sys.argv[2])
d = f"runde_{n}"
if cmd == "ziehen":
    size = int(sys.argv[3]); os.makedirs(d, exist_ok=True)
    used = set()
    for f in glob.glob("runde_*/stichprobe.json"):
        used |= {u["id"] for u in json.load(open(f))}
    pool = [u for u in U if u["id"] not in used]
    random.seed(100 + n)
    by = {}
    for u in pool: by.setdefault(u["stand"], []).append(u)
    share = Counter(u["stand"] for u in U)
    s = []
    for k, lst in by.items():
        s += random.sample(lst, round(size * share[k] / len(U)))
    random.shuffle(s)
    json.dump(s, open(f"{d}/stichprobe.json", "w"), ensure_ascii=False, indent=1)
    for p in range(4):
        json.dump(s[p::4], open(f"{d}/paket_{p+1}.json", "w"), ensure_ascii=False, indent=1)
    print(len(s), Counter(u["stand"] for u in s))
else:
    J = json.load(open(f"{d}/urteile.json"))
    n_ = len(J); z = sum(1 for j in J if j["zufriedenheit"] >= 4); w = sum(1 for j in J if j["wiederkauf"])
    print(f"Runde {n}: n={n_}  zufrieden {z}/{n_} = {z/n_:.0%}  wiederkauf {w}/{n_} = {w/n_:.0%}  Ø {sum(j['zufriedenheit'] for j in J)/n_:.2f}")
    print("Hauptprobleme (Kategorie):", Counter(j.get("kategorie", "-") for j in J if j["zufriedenheit"] < 4 or not j["wiederkauf"]).most_common())
    print("Alle genannten Probleme:", Counter(c for j in J for c in j.get("probleme_kategorien", [])).most_common(12))
