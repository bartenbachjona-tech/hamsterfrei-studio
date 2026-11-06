#!/usr/bin/env python3
"""Wertet den Kurz-Berufstest (12 Aussagen, RIASEC) aus.

    python3 berufstest_auswerten.py 4 5 2 3 1 4 5 2 3 4 1 5
    python3 berufstest_auswerten.py "4,5,2,3,1,4,5,2,3,4,1,5"
    python3 berufstest_auswerten.py --fragen        (zeigt die 12 Aussagen)

Jede Antwort ist 1–5 (1 = macht mir keinen Spaß … 5 = mache ich sehr gern),
in der Reihenfolge der Fragen 1–12. Ausgabe: Punkte je Typ, Code aus den
2–3 stärksten Typen, Hinweise zu Gleichstand und flachem Profil.
Das Ergebnis ist ein Gesprächsanstoß, keine Diagnose.
"""
import re
import sys

# Reihenfolge und Zuordnung müssen mit references/berufstest.md übereinstimmen.
FRAGEN = [
    ("R", "Ein Fahrrad, ein Gerät oder ein Möbelstück reparieren oder zusammenbauen"),
    ("S", "Jemandem etwas erklären, bis er es wirklich verstanden hat"),
    ("C", "Eine Tabelle sauber führen und Fehler darin finden"),
    ("I", "Herausfinden, warum etwas nicht funktioniert – tüfteln, recherchieren, testen"),
    ("A", "Etwas gestalten: zeichnen, fotografieren, Videos schneiden oder dekorieren"),
    ("E", "Andere von einer Idee überzeugen oder etwas verkaufen"),
    ("S", "Mich um Menschen kümmern, z. B. Kinder, Ältere, Kranke oder Kunden"),
    ("R", "Draußen oder mit Werkzeug und Maschinen körperlich arbeiten"),
    ("E", "Eine Gruppe anführen, Entscheidungen treffen und Verantwortung übernehmen"),
    ("I", "Mit Zahlen, Experimenten oder am Computer knifflige Aufgaben lösen"),
    ("C", "Dinge planen und ordnen: Termine, Lager, Unterlagen oder Abläufe"),
    ("A", "Eigene Ideen entwickeln: schreiben, Musik machen oder Neues erfinden"),
]
TYPEN = {
    "R": "Praktisch-technisch (Realistic)",
    "I": "Forschend-analytisch (Investigative)",
    "A": "Kreativ-gestaltend (Artistic)",
    "S": "Sozial-helfend (Social)",
    "E": "Unternehmerisch-führend (Enterprising)",
    "C": "Ordnend-verwaltend (Conventional)",
}
HEXAGON = "RIASEC"  # Nachbarn im Hexagon passen besser zusammen


def nachbarn(a, b):
    i, j = HEXAGON.index(a), HEXAGON.index(b)
    return abs(i - j) in (1, 5)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "--fragen":
        for i, (t, f) in enumerate(FRAGEN, 1):
            print(f"{i:2}. [{t}] {f}")
        return
    werte = [int(x) for x in re.findall(r"\d", " ".join(a))]
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
    print("Passung der Top-2: " + ("Nachbarn im Hexagon – passen gut zusammen."
                                    if nachbarn(rang[0], rang[1]) else "eher gegensätzlich – Berufe suchen, die beides verbinden, oder eins priorisieren."))
    print("Nächster Schritt: Vorschläge aus references/berufstest.md zum Code und passend zum Abschluss.")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
