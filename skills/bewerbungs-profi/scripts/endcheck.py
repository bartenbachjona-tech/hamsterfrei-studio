#!/usr/bin/env python3
"""Endcheck für Bewerbungsunterlagen (Selbstcheck, ersetzt kein Korrekturlesen).

    python3 endcheck.py DATEI [DATEI ...] [--firma "Beispiel GmbH"] [--stelle "Kauffrau ..."]

Erkennt Anschreiben/Lebenslauf am Dateinamen (sonst am Inhalt). Prüft u. a.:
offene [PRÜFEN: ...]-Stellen, Platzhalter, Floskeln und Konjunktiv, Länge,
falscher Firmenname (Copy-and-paste), Anrede, ATS-Risiken (Tabellen, Spalten,
Textfelder), Seitenzahl, Dateiname (Umlaute, Leerzeichen), Dateigröße.
❌ = vor dem Abschicken beheben, ⚠️ = prüfen, ✅ = in Ordnung.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

MAX_MB = 5            # Richtwert für E-Mail-Anhänge; Vorgaben der Anzeige gehen vor
ANSCHR_MAX_WORTE = 420  # darüber wird eine Seite mit Briefkopf meist voll
KURZ_MIN, KURZ_MAX = 150, 200

FLOSKELN = [
    "hiermit bewerbe ich mich", "hiermit", "mit großem interesse", "mit großer freude",
    "hat mich sofort angesprochen", "teamfähig, belastbar", "belastbar und flexibel",
    "über eine einladung zu einem vorstellungsgespräch würde ich mich", "würde mich freuen",
    "würde mich sehr freuen", "ich bin der perfekte kandidat", "die perfekte kandidatin",
    "in einer schnelllebigen welt", "leidenschaft für",
]
KONJUNKTIV = re.compile(r"\b(würde|würden|hätte|hätten|könnte|könnten|möchte gerne)\b", re.I)
PLATZHALTER = re.compile(r"(\[(?!PRÜFEN)[^\]\n]{1,40}\]|\bXXX+\b|\bMusterfirma\b|\bLorem ipsum\b|\bFirma XY\b|\bHerr/Frau\b)", re.I)
PRUEFEN = re.compile(r"\[PRÜFEN:[^\]]*\]")
FIRMEN = re.compile(r"\b([A-ZÄÖÜ][\wÄÖÜäöüß&.\-]*(?:\s+[A-ZÄÖÜ&][\wÄÖÜäöüß&.\-]*){0,3})\s+(GmbH|AG|KG|SE|e\.\s?V\.|GbR|OHG|UG)\b")
STANDARD_UEBERSCHRIFTEN = re.compile(r"(berufserfahrung|praktische erfahrung|praktika|ausbildung|schulbildung|bildung|studium)", re.I)


def art_von(pfad, txt):
    n = os.path.basename(pfad).lower()
    if "anschreiben" in n or "motivationsschreiben" in n:
        return "anschreiben"
    if "lebenslauf" in n or "cv" in n:
        return "lebenslauf"
    if "bewerbung" in n:
        return "gesamt"
    return "anschreiben" if re.search(r"(sehr geehrte|mit freundlichen grüßen)", txt, re.I) else "lebenslauf"


def pruefe(pfad, firma=None, stelle=None):
    befunde = []
    def add(sym, msg):
        befunde.append(f"{sym} {msg}")

    name = os.path.basename(pfad)
    try:
        txt = textlib.read_any(pfad)
    except RuntimeError as e:
        return [f"❌ Nicht lesbar: {e}"], None
    if not txt.strip():
        return ["❌ Kein Text gefunden (Scan oder Grafik?). Nichts ist geprüft. ATS können so etwas nicht lesen."], None
    art = art_von(pfad, txt)
    low = txt.lower()

    # Allgemein
    n = len(PRUEFEN.findall(txt))
    if n:
        add("❌", f"{n} offene [PRÜFEN: …]-Stelle(n): " + "; ".join(m[:60] for m in PRUEFEN.findall(txt)[:3]))
    ph = PLATZHALTER.findall(txt)
    if ph:
        add("❌", "Platzhalter gefunden: " + ", ".join(sorted(set(p if isinstance(p, str) else p[0] for p in ph))[:5]))
    if re.search(r"[äöüÄÖÜß ]", name):
        add("⚠️", f"Dateiname „{name}“ enthält Umlaute oder Leerzeichen – besser z. B. Bewerbung_Vorname_Nachname_Stelle.pdf")
    mb = os.path.getsize(pfad) / 1024 / 1024
    if mb > MAX_MB:
        add("⚠️", f"Datei ist {mb:.1f} MB groß (Richtwert unter {MAX_MB} MB, Vorgabe der Anzeige geht vor).")
    mails = sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", txt)))
    if mails:
        add("⚠️", "E-Mail-Adresse seriös? (ideal: vorname.nachname@…): " + ", ".join(mails[:3]))
    elif art in ("lebenslauf", "anschreiben"):
        add("❌", "Keine E-Mail-Adresse gefunden.")
    if pfad.lower().endswith(".pdf"):
        seiten = textlib.read_pdf_text(pfad)[1]
        if seiten:
            if art == "anschreiben" and seiten > 1:
                add("❌", f"Anschreiben hat {seiten} Seiten – höchstens 1 Seite.")
            elif art == "lebenslauf" and seiten > 2:
                add("❌", f"Lebenslauf hat {seiten} Seiten – höchstens 2 (Einsteiger: 1).")
            elif art == "lebenslauf" and seiten == 2:
                add("⚠️", "Lebenslauf hat 2 Seiten – für Schüler/Einsteiger ist 1 Seite das Ziel.")
            else:
                add("✅", f"Seitenzahl: {seiten}")
    if pfad.lower().endswith(".docx"):
        info = textlib.read_docx(pfad)["info"]
        if info["tabellen"] or info["textfelder"] or info["spalten"] > 1:
            add("⚠️", f"ATS-Risiko: {info['tabellen']} Tabelle(n), {info['textfelder']} Textfeld(er), "
                      f"{info['spalten']} Spalte(n) – einspaltig ohne Tabellen ist sicherer.")
        else:
            add("✅", "Layout einspaltig, keine Tabellen oder Textfelder (ATS-freundlich).")

    if firma and art != "lebenslauf":
        if firma.lower() not in low:
            add("❌", f"Firmenname „{firma}“ kommt nicht vor.")
        fremde = {" ".join(m).strip() for m in FIRMEN.findall(txt)}
        fremde = {f for f in fremde if firma.lower().split()[0] not in f.lower()}
        if fremde:
            add("⚠️", "Andere Firmennamen im Text – Copy-and-paste-Rest? " + ", ".join(sorted(fremde)[:4]))
    if stelle and art == "anschreiben" and stelle.lower().split()[0] not in low:
        add("⚠️", f"Stellenbezeichnung „{stelle}“ nicht gefunden – im Betreff genau wie in der Anzeige nennen.")

    if art == "anschreiben":
        worte = len(textlib.words(txt))
        if worte > ANSCHR_MAX_WORTE:
            add("❌", f"{worte} Wörter – zu lang für eine Seite. Kürzen (3–4 Absätze).")
        elif KURZ_MIN <= worte <= KURZ_MAX:
            add("✅", f"{worte} Wörter – passt als Kurzanschreiben.")
        else:
            add("✅", f"{worte} Wörter.")
        gef = [f for f in FLOSKELN if f in low]
        gef = [f for f in gef if not any(f != g and f in g for g in gef)]
        if gef:
            add("⚠️", "Floskeln, die Personaler oft als KI-/Standardtext lesen: " + ", ".join(f"„{g}“" for g in gef[:5]))
        k = KONJUNKTIV.findall(txt)
        if len(k) >= 2:
            add("⚠️", f"{len(k)}× Konjunktiv ({', '.join(sorted(set(x.lower() for x in k)))}) – direkter schreiben: „Ich freue mich …“")
        if not re.search(r"(sehr geehrte|guten tag|hallo|liebe[sr]? )", low):
            add("⚠️", "Keine Anrede gefunden.")
        saetze = [s for s in re.split(r"(?<=[.!?])\s+", txt) if len(s.split()) > 3]
        ich = sum(1 for s in saetze if s.strip().startswith("Ich "))
        if saetze and ich / len(saetze) > 0.4:
            add("⚠️", f"{ich} von {len(saetze)} Sätzen beginnen mit „Ich“ – Satzanfänge variieren.")
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
        sys.exit(__doc__)
    firma = a[a.index("--firma") + 1] if "--firma" in a else None
    stelle = a[a.index("--stelle") + 1] if "--stelle" in a else None
    skip = {firma, stelle, "--firma", "--stelle"}
    dateien = [x for x in a if x not in skip]
    fehler = 0
    for d in dateien:
        if not os.path.isfile(d):
            print(f"❌ Datei nicht gefunden: {d}")
            fehler += 1
            continue
        bef, art = pruefe(d, firma, stelle)
        print(f"\n## {os.path.basename(d)} ({art or '?'})")
        for b in bef:
            print(b)
        fehler += sum(1 for b in bef if b.startswith("❌"))
    print(f"\n---\n{'❌ ' + str(fehler) + ' Punkt(e) vor dem Abschicken beheben.' if fehler else '✅ Keine ❌-Befunde.'}"
          "\nSelbstcheck: Rechtschreibung, Daten und Inhalte trotzdem selbst lesen – am besten laut oder von einer zweiten Person.")


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
