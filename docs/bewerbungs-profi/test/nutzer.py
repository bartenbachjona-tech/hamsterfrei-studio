"""1.000 simulierte Testnutzer für den Bewerbungs-Profi (gewichtete Zufallsauswahl, Seed fest)."""
import json, random
random.seed(7)
ZIEL = [("Ausbildung", 26), ("Duales Studium", 12), ("Praktikum/Werkstudent", 12), ("Berufseinstieg nach Studium", 14),
        ("Jobwechsel", 20), ("Minijob/Nebenjob", 10), ("Wiedereinstieg nach Pause", 6)]
STAND = [("weiß noch nicht, was ich machen will", 25), ("habe einen Favoriten/eine konkrete Stelle", 55), ("Unterlagen schon abgeschickt, Gespräch/AC steht an", 20)]
KI = [("noch nie KI benutzt", 15), ("nur ChatGPT ein paar Mal", 50), ("nutzt KI regelmäßig", 30), ("Claude-Erfahren", 5)]
EIGEN = [("antwortet sehr knapp", 25), ("schweift gern ab", 15), ("ungeduldig, will schnell Ergebnis", 20), ("unsicher, braucht Ermutigung", 20),
         ("gründlich, viele Rückfragen", 10), ("Tippfehler, umgangssprachlich", 10)]
LINK = [("Link funktioniert", 50), ("Link blockiert (Portal-Sperre)", 30), ("hat keinen Link, nur Firmenname", 20)]
GERAET = [("Laptop", 55), ("nur Handy", 35), ("Tablet", 10)]
LUECKE = [("lückenloser Lebenslauf", 60), ("Lücke im Lebenslauf", 25), ("Abbruch Ausbildung/Studium", 15)]
def pick(lst): return random.choices([x for x, _ in lst], [w for _, w in lst])[0]
users = []
for i in range(1000):
    z = pick(ZIEL)
    alter = random.randint(18, 22) if z in ("Ausbildung", "Duales Studium", "Minijob/Nebenjob") else random.randint(20, 45)
    stand = pick(STAND)
    ac = z in ("Duales Studium", "Berufseinstieg nach Studium") and random.random() < 0.6 or random.random() < 0.15
    users.append({"id": i + 1, "alter": alter, "ziel": z, "stand": stand, "ki": pick(KI), "eigenart": pick(EIGEN),
                  "link": pick(LINK), "geraet": pick(GERAET), "lebenslauf": pick(LUECKE), "assessment_center": bool(ac)})
json.dump(users, open("nutzer_1000.json", "w"), ensure_ascii=False, indent=0)
from collections import Counter
for k in ("ziel", "stand", "ki", "eigenart", "link", "geraet"):
    print(k, Counter(u[k] for u in users).most_common())
