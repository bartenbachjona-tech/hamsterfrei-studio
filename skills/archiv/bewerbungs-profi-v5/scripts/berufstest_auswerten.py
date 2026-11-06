#!/usr/bin/env python3
"""Wertet den Kurz-Berufstest (12 Aussagen, RIASEC) aus.

    python3 berufstest_auswerten.py 4 5 2 3 1 4 5 2 3 4 1 5
    python3 berufstest_auswerten.py "4,5,2,3,1,4,5,2,3,4,1,5"
    python3 berufstest_auswerten.py "1a 2c 3b 4a 5e 6d 7b 8c 9a 10b 11c 12d"
    python3 berufstest_auswerten.py --fragen        (zeigt die 12 Aussagen)

Antworten entweder als Zahlen 1–5 in Reihenfolge (1 = gar nicht … 5 = sehr gern) oder im
Kompakt-Format „Nummer + Buchstabe“: a = sehr gern, b = gern, c = geht so, d = eher nicht, e = gar nicht. Ausgabe: Punkte je Typ, Code aus den
2–3 stärksten Typen, Hinweise zu Gleichstand und flachem Profil.
Das Ergebnis ist ein Gesprächsanstoß, keine Diagnose.
"""
import re
import sys

# Reihenfolge und Zuordnung müssen mit references/berufstest.md übereinstimmen.
FRAGEN = [
    ("R", "Geräte, Fahrräder oder Möbel reparieren"),
    ("S", "Anderen etwas erklären"),
    ("C", "Tabellen sauber führen, Fehler finden"),
    ("I", "Tüfteln, warum etwas nicht geht"),
    ("A", "Gestalten: zeichnen, Fotos, Videos"),
    ("E", "Andere überzeugen, etwas verkaufen"),
    ("S", "Mich um Menschen kümmern"),
    ("R", "Draußen oder mit Werkzeug arbeiten"),
    ("E", "Eine Gruppe anführen, entscheiden"),
    ("I", "Knobeln mit Zahlen oder am Computer"),
    ("C", "Planen und ordnen: Termine, Abläufe"),
    ("A", "Eigene Ideen: schreiben, Musik, erfinden"),
]
TYPEN = {
    "R": "Praktisch-technisch (Realistic)",
    "I": "Forschend-analytisch (Investigative)",
    "A": "Kreativ-gestaltend (Artistic)",
    "S": "Sozial-helfend (Social)",
    "E": "Unternehmerisch-führend (Enterprising)",
    "C": "Ordnend-verwaltend (Conventional)",
}
HEXAGON = "RIASEC"  # Reihenfolge rund ums Hexagon


def abstand(a, b):
    """1 = Nachbarn (R-I, I-A, A-S, S-E, E-C, C-R), 2 = eine Ecke dazwischen,
    3 = genau gegenüber (nur R-S, I-E, A-C)."""
    d = abs(HEXAGON.index(a) - HEXAGON.index(b))
    return min(d, 6 - d)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--fragen":
        for i, (t, f) in enumerate(FRAGEN, 1):
            print(f"{i:2}. [{t}] {f}")
        return
    roh = " ".join(a).lower()
    paare = re.findall(r"(\d{1,2})\s*[:.)=-]?\s*([a-e])\b", roh)
    if paare:
        buchst = {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1}
        dic = {int(n): buchst[b] for n, b in paare}
        fehlen = [i for i in range(1, len(FRAGEN) + 1) if i not in dic]
        if fehlen:
            sys.exit(f"FEHLER: Antwort fehlt zu Aussage {', '.join(map(str, fehlen))} – bitte nachfragen.")
        werte = [dic[i] for i in range(1, len(FRAGEN) + 1)]
    else:
        werte = [int(x) for x in re.findall(r"\d", roh)]
    if len(werte) != len(FRAGEN):
        sys.exit(f"FEHLER: {len(werte)} Antworten erkannt, gebraucht werden genau {len(FRAGEN)} (je 1–5).")
    if any(w < 1 or w > 5 for w in werte):
        sys.exit("FEHLER: Jede Antwort muss zwischen 1 und 5 liegen.")
    punkte = {t: 0 for t in HEXAGON}
    for (t, _), w in zip(FRAGEN, werte):
        punkte[t] += w
    rang = sorted(HEXAGON, key=lambda t: (-punkte[t], HEXAGON.index(t)))
    print("Punkte je Typ (2–10):")
    for t in rang:
        print(f"  {t} {TYPEN[t]:<40} {punkte[t]:>2} " + "■" * punkte[t])
    code = "".join(rang[:3])
    print(f"\nCode: {code}  (stärkster Typ zuerst)")
    for wert in sorted({punkte[t] for t in rang[:3]}, reverse=True):
        gruppe = [t for t in rang if punkte[t] == wert]
        if len(gruppe) > 1:
            extra = " – auch Platz 4 ist gleichauf, diese Richtungen alle anbieten" if any(rang.index(t) >= 3 for t in gruppe) else ""
            print(f"Hinweis: Gleichstand {' = '.join(gruppe)} ({wert} Punkte), Reihenfolge im Code ist hier beliebig{extra}.")
    if punkte[rang[0]] - punkte[rang[-1]] <= 2:
        print("Hinweis: Sehr flaches Profil – Interessen sind (noch) nicht klar. Lieber über Lieblingsfächer, "
              "Praktika und Check-U weiterkommen; Vorschläge breit streuen.")
    if punkte[rang[0]] <= 5:
        print("Hinweis: Wenig Begeisterung insgesamt – nachfragen, was im Alltag Spaß macht (Hobbys, Nebenjob).")
    ab = abstand(rang[0], rang[1])
    print("Passung der Top-2: " + {
        1: "Nachbarn im Hexagon – passen gut zusammen.",
        2: "eine Ecke auseinander – gut kombinierbar, viele Berufe verbinden beides.",
        3: "genau gegenüber im Hexagon – seltener in einem Beruf vereint: Berufe suchen, die beides verbinden, oder eins priorisieren.",
    }[ab])
    print("Nächster Schritt: 3 Vorschläge aus references/berufstest.md zum Code (2-Buchstaben-Tabelle) und passend zum Abschluss; "
          "am Ende immer Check-U, BERUFENET und Berufsberatung nennen.")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
