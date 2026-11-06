"""Hochrechnung des Testpanels auf 1.000 Personen.

50 Archetypen (personas.json) werden nach Gewicht auf 1.000 Einzelpersonen vervielfacht.
Jede Einzelperson bekommt eine individuelle Streuung (Kaufneigung ±40 %, Preise ±20 %),
damit nicht 30 identische Klone entstehen. Seed fest -> reproduzierbar.

Kalibrierung: Umfrage-Kaufabsichten sind immer viel zu hoch. Der einzige echte Wert ist
P1 Seminararbeit-Profi: 3 Verkäufe bei ca. 2.500 Videoaufrufen = 0,12 %.
Faktor k = 0,12 % / (Panel-Kaufquote P1). k gilt für alle Produkte gleich
-> "erwartete Käufe pro 1.000 Videoaufrufe" (grobe Richtgröße, keine Prognose).
"""
import json, random, statistics as st

random.seed(42)
D = "/home/claude/hamsterfrei-studio/docs/produktsim/"
pers = json.load(open(D + "personas.json"))
U = {}
for f in ("urteile_a.json", "urteile_b.json", "urteile_c.json"):
    U.update(json.load(open(D + f)))

NAMES = {
    "P1": "Seminararbeit-Profi (Referenz)", "P2": "Anzeigen-Profi", "P3": "Bewerbungs-Profi Ausbildung/Minijob",
    "P4": "Wohnungs-/WG-Bewerbungs-Profi", "P5": "Hausarbeit-/Bachelorarbeit-Profi", "P6": "Kleingewerbe-Starter",
    "P7": "Steuer-Checkliste Azubi/Studi", "P8": "Abi-Lernplan-Coach", "P9": "BAföG-Lotse", "P10": "Hochzeits-Planer",
    "F1": "CapCut Pro (Affiliate)", "F2": "Gamma (Affiliate)", "F3": "LanguageTool Premium (Affiliate)",
    "F4": "ElevenLabs (Affiliate)", "F5": "smartsteuer (Affiliate)", "F6": "Surfshark VPN (Affiliate)",
}
# Provision pro zahlendem Kunden (Schätzung aus der Affiliate-Recherche, in €)
PROV = {"F1": 15, "F2": 15, "F3": 20, "F4": 7, "F5": 20, "F6": 25}

people = [p for p in pers for _ in range(p["gewicht"])]
assert len(people) == 1000
noise_k = [random.uniform(0.6, 1.4) for _ in people]
noise_p = [random.uniform(0.8, 1.2) for _ in people]


def net_own(price):
    """Was bei Jona pro Verkauf ankommt: brutto -> netto (19 % USt) minus Digistore (7,9 % + 1 €)."""
    return price / 1.19 - (0.079 * price + 1.0)


def vw_points(rows):
    """Van Westendorp: Schnittpunkte der kumulierten Kurven (gewichtet über Einzelpersonen)."""
    grid = [x / 2 for x in range(1, 201)]  # 0,50 € .. 100 €
    n = len(rows)
    if n < 20:
        return None

    def share(idx, cmp):
        return [sum(1 for r in rows if cmp(r[idx], g)) / n for g in grid]

    too_cheap = share(0, lambda v, g: v >= g)   # fällt mit dem Preis
    cheap = share(1, lambda v, g: v >= g)
    exp = share(2, lambda v, g: v <= g)         # steigt mit dem Preis
    too_exp = share(3, lambda v, g: v <= g)

    def cross(a, b):
        for g, x, y in zip(grid, a, b):
            if y >= x:
                return g
        return None

    return {
        "PMC": cross(too_cheap, [1 - e for e in exp]),     # untere Grenze
        "OPP": cross(too_cheap, too_exp),                  # optimaler Preis
        "IDP": cross(cheap, exp),                          # indifferenter Preis
        "PME": cross([1 - c for c in cheap], too_exp),     # obere Grenze
    }


res = {}
for pid, judg in U.items():
    probs, vws, gratis, maxp = [], [], [], []
    for i, p in enumerate(people):
        j = judg[p["id"]]
        pr = min(1.0, j["kauf"] / 100 * noise_k[i])
        probs.append(pr)
        if pid.startswith("P") and j.get("vw"):
            vws.append([v * noise_p[i] for v in j["vw"]])
        if pid.startswith("F"):
            gratis.append(min(1.0, j["gratis"] / 100 * noise_k[i]))
            if j["max"]:
                maxp.append(j["max"] * noise_p[i])
    r = {"name": NAMES[pid], "panel_kaeufer": sum(probs),
         "starke_absicht": sum(1 for x in probs if x >= 0.5)}
    if vws:
        r["vw"] = vw_points(vws)
        r["median_guenstig"] = st.median(v[1] for v in vws)
        r["median_teuer"] = st.median(v[2] for v in vws)
    if pid.startswith("F"):
        r["gratis_anmeldungen"] = sum(gratis)
        r["median_max"] = st.median(maxp) if maxp else 0
    # wer kauft? Top-Segmente
    seg = {}
    for i, p in enumerate(people):
        seg[p["id"]] = seg.get(p["id"], 0) + probs[i]
    r["top_segmente"] = [(s, round(v, 1)) for s, v in sorted(seg.items(), key=lambda x: -x[1])[:3]]
    res[pid] = r

k = 0.0012 / (res["P1"]["panel_kaeufer"] / 1000)
for pid, r in res.items():
    r["kaeufe_pro_1000_aufrufe"] = r["panel_kaeufer"] / 1000 * k * 1000
    if pid.startswith("P"):
        price = (r.get("vw") or {}).get("OPP") or 9.90
        if pid in ("P1", "P2"):
            price = 9.90
        r["preis_empfehlung"] = price
        r["euro_pro_verkauf"] = net_own(price)
    else:
        r["euro_pro_verkauf"] = PROV[pid]
    r["euro_pro_1000_aufrufe"] = r["kaeufe_pro_1000_aufrufe"] * r["euro_pro_verkauf"]

json.dump({"kalibrierfaktor": k, "ergebnisse": res}, open(D + "ergebnis.json", "w"), ensure_ascii=False, indent=1)

print(f"Kalibrierfaktor k = {k:.4f} (Umfrage-Absicht -> echte Käufe)\n")
print(f"{'Produkt':40} {'Panel':>6} {'stark':>5} {'Kauf/1k':>8} {'€/Verk':>7} {'€/1k':>6}  Preis (PMC–OPP–PME)")
for pid, r in sorted(res.items(), key=lambda x: -x[1]["euro_pro_1000_aufrufe"]):
    vw = r.get("vw") or {}
    pr = f"{vw.get('PMC')}–{vw.get('OPP')}–{vw.get('PME')}" if vw else f"max/Monat Median {r.get('median_max', 0):.0f} €"
    print(f"{r['name'][:40]:40} {r['panel_kaeufer']:6.0f} {r['starke_absicht']:5d} {r['kaeufe_pro_1000_aufrufe']:8.2f} "
          f"{r['euro_pro_verkauf']:7.2f} {r['euro_pro_1000_aufrufe']:6.2f}  {pr}  {r['top_segmente']}")
