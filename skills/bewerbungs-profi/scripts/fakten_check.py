#!/usr/bin/env python3
"""Fakten-Check: Steht in den Unterlagen etwas, das NICHT aus der Profil-JSON oder der Anzeige stammt?

    python3 fakten_check.py PROFIL.json                  → prüft lebenslauf/anschreiben/formular/email in der JSON
    python3 fakten_check.py PROFIL.json DATEI [DATEI …]  → prüft zusätzlich die Dateien (.pdf/.docx/.txt)
                                                           und gleicht sie mit dem freigegebenen JSON-Text ab
    Optionen: --anzeige ANZEIGE.txt (weitere Belegquelle)  --kurz (nur ❌)

Belegquellen (Korpus): alles in der JSON AUSSER den erzeugten Texten (lebenslauf, anschreiben,
formular, email, meta, status) – also person, ziel (inkl. anzeige_text), profil, belege, gespraech,
berufstest – plus Firmenfakten mit "zugestimmt": true, plus --anzeige-Dateien und das heutige Datum.

Geprüft wird: Zahlen, Jahres-/Monats-/Tagesangaben, Dauern (auch „acht Jahre“), Eigennamen
(Firmen mit Rechtsform, Abkürzungen, Namensfolgen), Abschlüsse, Sprachniveaus, Führerschein,
URLs/E-Mail/LinkedIn, aufwertende Wörter („geleitet“, „verantwortlich“ …), lange Fachbegriffe,
[PRÜFEN]-Missbrauch für eigene Vorschläge, „Wie aufmerksam geworden?“ ohne Beleg,
gesammelte Beispiele/Hobbys, die nirgends vorkommen, und Datei ≠ freigegebener Text.

❌ = ohne Beleg: belegen (Feld in profil/belege ergänzen), streichen oder den Nutzer fragen.
⚠️ = kurz prüfen.  Exit-Code: 0 ohne ❌, 1 mit ❌, 2 bei Bedienfehler.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

ERZEUGT = ("lebenslauf", "anschreiben", "formular", "email", "meta", "status")
PRUEFEN_RE = re.compile(r"\[PRÜFEN:[^\]]*\]")
MONATE = {"januar": 1, "jan": 1, "februar": 2, "feb": 2, "märz": 3, "maerz": 3, "mär": 3, "april": 4, "apr": 4,
          "mai": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7, "august": 8, "aug": 8, "september": 9, "sept": 9,
          "sep": 9, "oktober": 10, "okt": 10, "november": 11, "nov": 11, "dezember": 12, "dez": 12}
ZAHLWORT = {"ein": 1, "eine": 1, "einem": 1, "einen": 1, "einer": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
            "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11, "zwölf": 12,
            "fünfzehn": 15, "zwanzig": 20, "dreißig": 30, "fünfzig": 50, "hundert": 100, "tausend": 1000,
            "halb": 0.5, "halbes": 0.5, "halben": 0.5, "anderthalb": 1.5, "eineinhalb": 1.5, "zweieinhalb": 2.5,
            "zweit": 2, "dritt": 3, "viert": 4, "fünft": 5, "sechst": 6, "dutzend": 12, "beiden": 2, "beide": 2}
EINHEIT = r"(Jahre?n?|Jahr(?:es)?|Monate?n?|Monat(?:s)?|Wochen?|Tage?n?|Tag(?:es)?|Stunden?|Std\.?|Semester[n]?|Schuljahre?n?)"
EINH_NORM = [("jahr", "jahr"), ("schuljahr", "jahr"), ("monat", "monat"), ("woche", "woche"), ("tag", "tag"),
             ("stunde", "stunde"), ("std", "stunde"), ("semester", "semester")]
ABSCHLUESSE = ["abitur", "fachabitur", "fachhochschulreife", "allgemeine hochschulreife", "mittlere reife",
               "realschulabschluss", "hauptschulabschluss", "mittelschulabschluss", "qualifizierender", "quali",
               "msa", "bachelor", "master", "b.sc", "b.a.", "m.sc", "m.a.", "diplom", "staatsexamen", "magister",
               "meister", "techniker", "gesellenbrief", "gesellenprüfung", "abschlussprüfung", "promotion", "dr.",
               "matura", "lehrabschluss", "efz", "berufsmaturität", "ihk-abschluss", "ausbilderschein", "ada-schein"]
NIVEAU_RE = re.compile(r"\b([ABC][12])\b|\b(Muttersprache|muttersprachlich|fließend|verhandlungssicher|Grundkenntnisse|"
                       r"Basiskenntnisse|gute Kenntnisse|sehr gute Kenntnisse|Konversationssicher)\b", re.I)
FUEHRERSCHEIN_RE = re.compile(r"\b(Führerschein|Fahrerlaubnis|Klasse\s+(?:B|BE|C1|C|CE|AM|A1|A2|A|L|T)\b|PKW-Führerschein)", re.I)
URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b[\w.+-]+@[\w-]+\.[\w.]+|\blinkedin\.com/\S+|\bxing\.com/\S+)", re.I)
AUFWERTUNG = ["geleitet", "leitung", "leitete", "projektleitung", "verantwortlich", "verantwortung", "eigenverantwortlich",
              "konzipiert", "mitkonzipiert", "entwickelt", "aufgebaut", "eingeführt", "optimiert", "gesteigert",
              "koordiniert", "geführt", "führung", "teamleitung", "filialverantwortung", "managed", "gemanagt",
              "maßgeblich", "federführend", "strategisch", "betreut", "verbessert", "ausgebildet", "eingearbeitet",
              "eingelernt", "selbstständig", "selbständig", "erfolgreich"]
FIRMEN_RE = re.compile(r"\b([A-ZÄÖÜ][\wÄÖÜäöüß&.\-]*(?:\s+[A-ZÄÖÜ&][\wÄÖÜäöüß&.\-]*){0,3})\s+"
                       r"(gGmbH|GmbH|AG|KG|SE|e\.\s?V\.|GbR|OHG|UG|mbH|KGaA)\b")
AKRONYM_RE = re.compile(r"\b([A-ZÄÖÜ]{2,}[0-9]*|[A-Z][a-z]+[A-Z][A-Za-z]+)\b")
AKRONYM_OK = {"EUR", "PDF", "IT", "EDV", "PC", "CV", "AG", "GMBH", "SE", "KG", "UG", "MS", "USB", "TV", "OK", "DE",
              "AT", "CH", "EU", "MWD", "PS", "ZB", "BZW", "CA", "UND", "WLAN", "III", "II", "IV"}
STANDARD = set("""
lebenslauf kurzprofil berufserfahrung praktische erfahrung schulbildung bildung ausbildung studium kenntnisse
interessen ehrenamt praktika praktikum nebenjob minijob sprachen sprache edv muttersprache grundkenntnisse
anschreiben motivationsschreiben bewerbung bewerbungsunterlagen anlagen anlage zeugnis zeugnisse
sehr geehrte geehrter damen herren freundlichen grüßen mit gruß hallo liebe lieber guten tag team
ich sie ihr ihre ihnen ihrer ihres ihren wir uns dabei darum deshalb seit heute bei in im am an der die das
gespräch vorstellungsgespräch persönliches einladung frage fragen stelle stellen anzeige ausbildungsplatz
geboren am betreff kennziffer telefon e-mail adresse und oder sowie außerdem zudem gern gerne
januar februar märz april mai juni juli august september oktober november dezember
""".split())


# ---------------------------------------------------------------- Korpus
def flach(obj, aus=()):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in aus:
                continue
            out += flach(v)
    elif isinstance(obj, list):
        for v in obj:
            out += flach(v)
    elif isinstance(obj, (str, int, float)) and not isinstance(obj, bool):
        out.append(str(obj))
    return out


def korpus(d, anzeigen):
    teile = flach({k: v for k, v in d.items() if k not in ERZEUGT and k != "firmenfakten"})
    offen = []
    for f in d.get("firmenfakten") or []:
        if f.get("zugestimmt") is True:
            teile += flach(f)
        else:
            offen.append(f.get("fakt", ""))
    for a in anzeigen:
        teile.append(textlib.read_any(a))
    teile.append(datetime.date.today().strftime("%d.%m.%Y"))
    return "\n".join(teile), offen


def norm(s):
    return textlib.translit((s or "").lower())


def zahl(s):
    s = s.strip()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


class Belege:
    def __init__(self, text):
        self.text = text
        self.low = norm(text)
        self.woerter = set(re.findall(r"[a-z0-9]+", self.low))
        self.monate, self.jahre, self.tage = set(), set(), set()
        for y, m, t in self._daten(text):
            self.jahre.add(y)
            if m:
                self.monate.add((y, m))
            if t:
                self.tage.add((y, m, t))
        rest = self._ohne_daten(text)
        self.zahlen = {z for z in (zahl(x) for x in re.findall(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])", rest)) if z is not None}
        self.zahlen |= set(range(1, 13)) & {m for _, m in self.monate}
        for w, v in ZAHLWORT.items():
            if re.search(rf"\b{w}\b", text, re.I) and w not in ("ein", "eine", "einem", "einen", "einer"):
                self.zahlen.add(float(v))
        self.dauern = set(self._dauern(text))

    @staticmethod
    def _daten(t):
        for m in re.finditer(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b", t):
            y = int(m.group(3)); y += 2000 if y < 100 else 0
            yield y, int(m.group(2)), int(m.group(1))
        for m in re.finditer(r"\b(\d{1,2})\s*[/.]\s*(\d{4})\b", t):
            if 1 <= int(m.group(1)) <= 12:
                yield int(m.group(2)), int(m.group(1)), None
        for m in re.finditer(r"\b(" + "|".join(MONATE) + r")\.?\s+(\d{4})\b", t, re.I):
            yield int(m.group(2)), MONATE[m.group(1).lower()], None
        for m in re.finditer(r"(?<![\d./])((?:19|20)\d{2})(?![\d])", t):
            yield int(m.group(1)), None, None

    @staticmethod
    def _ohne_daten(t):
        t = re.sub(r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b", " ", t)
        t = re.sub(r"\b\d{1,2}\s*[/.]\s*\d{4}\b", " ", t)
        return t

    @staticmethod
    def _dauern(t):
        wort = "|".join(sorted(ZAHLWORT, key=len, reverse=True))
        for m in re.finditer(rf"(?<![\w])(\d+(?:[.,]\d+)?|{wort})\s*(?:-\s*)?{EINHEIT}", t, re.I):
            roh = m.group(1).lower()
            v = ZAHLWORT.get(roh) if roh in ZAHLWORT else zahl(roh)
            e = m.group(2).lower()
            einheit = next((n for k, n in EINH_NORM if e.startswith(k)), e)
            if v is not None:
                yield (float(v), einheit)

    def hat_wort(self, w):
        w = norm(w)
        if not w:
            return True
        if w in self.low:
            return True
        if len(w) >= 6 and any(x.startswith(w[:max(5, len(w) - 3)]) for x in self.woerter):
            return True
        return self._kompositum(w)

    def _kompositum(self, w):
        if len(w) < 9:
            return False
        bedeckt = [False] * len(w)
        for x in self.woerter:
            if len(x) >= 4:
                for m in re.finditer(re.escape(x[:max(4, len(x) - 2)]), w):
                    for i in range(m.start(), min(len(w), m.start() + len(x))):
                        bedeckt[i] = True
        return sum(bedeckt) / len(w) >= 0.8


# ---------------------------------------------------------------- Prüfung eines Textes
def saetze_ohne_pruefen(t):
    return PRUEFEN_RE.sub(" ", t)


def pruefe_text(name, t, B, offen_fakten, befunde):
    gemeldet = set()

    def add(sym, kat, was, ctx=""):
        befunde.append((sym, name, kat, was, ctx))
        gemeldet.update(norm(x) for x in re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", was))

    def kontext(m, src):
        a, b = max(0, m.start() - 35), min(len(src), m.end() + 35)
        return re.sub(r"\s+", " ", src[a:b]).strip()

    # [PRÜFEN]-Missbrauch
    for m in PRUEFEN_RE.finditer(t):
        inh = m.group(0).lower()
        if re.search(r"stimmt (das|es)|so ok|korrekt\?|passt (das|es)|einverstanden|oder\?|richtig\?", inh):
            add("⚠️", "[PRÜFEN] als Vorschlag", m.group(0)[:70],
                "[PRÜFEN] nur für echte Lücken. Eigene Vorschläge vorher im Chat fragen – nicht in den Text schreiben.")
    s = saetze_ohne_pruefen(t)

    # Daten
    for y, mo, tg in Belege._daten(s):
        if tg and (y, mo, tg) not in B.tage:
            if (y, mo) in B.monate:
                add("⚠️", "Datum", f"{tg:02d}.{mo:02d}.{y}", "Tag ist nicht belegt (nur Monat bekannt)")
            else:
                add("❌", "Datum", f"{tg:02d}.{mo:02d}.{y}", "kein Beleg")
        elif mo and not tg and (y, mo) not in B.monate:
            if y in B.jahre:
                add("❌", "Monat", f"{mo:02d}/{y}", f"nur das Jahr {y} ist belegt – Monat erfragen oder weglassen")
            else:
                add("❌", "Monat/Jahr", f"{mo:02d}/{y}", "kein Beleg")
        elif not mo and y not in B.jahre:
            add("❌", "Jahr", str(y), "kein Beleg")
    # Dauern
    for v, e in set(Belege._dauern(s)):
        if (v, e) not in B.dauern:
            vtxt = ("%g" % v).replace(".", ",")
            add("❌", "Dauer", f"{vtxt} {e}(e)", "Dauer so nicht belegt (nicht runden, nicht hochrechnen)")
    # Zahlen
    rest = Belege._ohne_daten(s)
    rest = re.sub(r"\b[ABC][12]\b", " ", rest)
    for m in re.finditer(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])", rest):
        z = zahl(m.group(0))
        if z is None or z in B.zahlen:
            continue
        if any(v == z for v, _ in B.dauern):
            continue
        if 1900 <= z <= 2100 and int(z) in B.jahre:
            continue
        add("❌", "Zahl", m.group(0), kontext(m, rest))
    wort = "|".join(w for w in ZAHLWORT if w not in ("ein", "eine", "einem", "einen", "einer", "beiden", "beide"))
    for m in re.finditer(rf"\b(?:zu\s+)?({wort})\b", s, re.I):
        if float(ZAHLWORT[m.group(1).lower()]) not in B.zahlen and not B.hat_wort(m.group(0)):
            add("❌", "Zahlwort", m.group(0), kontext(m, s))
    # Abschlüsse
    low = norm(s)
    for a in ABSCHLUESSE:
        if re.search(r"(?<![a-z])" + re.escape(norm(a)) + r"(?![a-z])", low) and norm(a) not in B.low:
            add("❌", "Abschluss", a, "Abschluss steht nicht im Profil")
    # Sprachniveaus
    for m in NIVEAU_RE.finditer(s):
        if not B.hat_wort(m.group(0)):
            add("❌", "Sprachniveau", m.group(0), kontext(m, s))
        else:
            vor = s[max(0, m.start() - 25):m.start()]
            spr = re.findall(r"\b([A-ZÄÖÜ][a-zäöüß]+(?:isch|sch))\b", vor)
            if spr and m.group(1):
                pat = norm(spr[-1])[:5] + r"\w*\W{0,4}(?:\w+\W{0,3}){0,3}" + norm(m.group(0))
                if not re.search(pat, B.low):
                    add("❌", "Sprachniveau", f"{spr[-1]} {m.group(0)}", "diese Kombination steht nicht im Profil")
    # Führerschein
    for m in FUEHRERSCHEIN_RE.finditer(s):
        if not re.search(r"fuehrerschein|fahrerlaubnis|klasse (b|be|c1?|ce|am|a[12]?|l|t)\b", B.low):
            add("❌", "Führerschein", m.group(0), "Führerschein nicht im Profil")
            break
    # URLs/E-Mail
    for m in URL_RE.finditer(s):
        u = m.group(0).rstrip(".,;)")
        if norm(u) not in B.low:
            add("❌", "Link/E-Mail", u, "nicht im Profil")
    if re.search(r"\blinked\s?in\b", low) and "linkedin" not in B.low and "linkedin" not in gemeldet:
        add("❌", "Link/E-Mail", "LinkedIn", "kein LinkedIn im Profil")
    # Eigennamen
    gesehen = set()
    for m in FIRMEN_RE.finditer(s):
        n = " ".join(m.groups())
        if n not in gesehen and not B.hat_wort(m.group(1)):
            gesehen.add(n)
            add("❌", "Name/Firma", n, "nicht im Profil und nicht in der Anzeige")
    for m in AKRONYM_RE.finditer(s):
        w = m.group(1)
        if w.upper() in AKRONYM_OK or w in gesehen:
            continue
        gesehen.add(w)
        if not B.hat_wort(w):
            add("❌", "Name/Begriff", w, kontext(m, s))
    for m in re.finditer(r"(?<![.!?:]\s)(?<!^)\b([A-ZÄÖÜ][\wäöüß\-]+(?:\s+[A-ZÄÖÜ][\wäöüß\-]+)+)", s, re.M):
        folge = m.group(1)
        teile = [x for x in folge.split() if norm(x) not in STANDARD]
        fehlt = [x for x in teile if not B.hat_wort(x) and norm(x) not in gemeldet]
        if fehlt and folge not in gesehen:
            gesehen.add(folge)
            add("❌", "Name", folge, "Teil ohne Beleg: " + ", ".join(fehlt))
    # Aufwertungen
    for a in AUFWERTUNG:
        for m in re.finditer(r"\b" + re.escape(a) + r"\w*", s, re.I):
            if not B.hat_wort(m.group(0)[:len(a)]):
                add("⚠️", "Aufwertung?", m.group(0), kontext(m, s) + " – hat der Nutzer das so gesagt?")
            break
    # lange Fachbegriffe
    for m in re.finditer(r"\b[A-ZÄÖÜ][a-zäöüß]{11,}\b", s):
        w = m.group(0)
        if norm(w) in STANDARD or w in gesehen or norm(w) in gemeldet:
            continue
        gesehen.add(w)
        if not B.hat_wort(w):
            add("⚠️", "Begriff", w, kontext(m, s))
    # Firmenfakten ohne Zustimmung
    for f in offen_fakten:
        kern = [x for x in re.findall(r"[a-zäöüß]{5,}", (f or "").lower())][:4]
        if kern and sum(1 for k in kern if k in s.lower()) >= max(2, len(kern) - 1):
            add("❌", "Firmenfakt", f, "aus der Recherche, aber der Nutzer hat nicht zugestimmt")


# ---------------------------------------------------------------- Texte aus der JSON
def json_texte(d):
    out = {}
    lv = d.get("lebenslauf") or {}
    if lv:
        teile = [lv.get("kurzprofil", "")]
        for ab in lv.get("abschnitte", []):
            for e in ab.get("eintraege", []):
                teile += [e.get("zeitraum", ""), e.get("titel", ""), e.get("ort", "")] + list(e.get("punkte", []))
        teile += [f'{k.get("label", "")} {k.get("wert", "")}'.strip() for k in lv.get("kenntnisse", [])] + [lv.get("interessen", "")]
        out["lebenslauf"] = [x for x in teile if x]
    an = d.get("anschreiben") or {}
    if an.get("absaetze"):
        out["anschreiben"] = [x for x in [an.get("betreff", ""), an.get("anrede", "")] + an["absaetze"] if x]
    if d.get("formular"):
        out["formular"] = [f.get("text", "") for f in d["formular"] if f.get("text")]
    em = d.get("email") or {}
    if em.get("text"):
        out["email"] = [x for x in (em.get("betreff", ""), em["text"]) if x]
    return out


def alnum(s):
    return re.sub(r"[^a-z0-9äöüß]", "", (s or "").lower())


def abgleich(datei_text, texte, name, befunde):
    """Datei = freigegebener JSON-Text? Wählt den passendsten Abschnitt."""
    dt = alnum(datei_text)
    best, best_q, best_fehl = None, -1, []
    for sek, einheiten in texte.items():
        einh = [e for e in einheiten if "[PRÜFEN" not in e and len(alnum(e)) >= 4]
        if not einh:
            continue
        fehl = [e for e in einh if alnum(e) not in dt]
        q = 1 - len(fehl) / len(einh)
        if q > best_q:
            best, best_q, best_fehl = sek, q, fehl
    if best is None or best_q < 0.3:
        befunde.append(("⚠️", name, "Abgleich", "kein passender Abschnitt in der JSON",
                        "Datei wurde wohl nicht aus der Profil-JSON erzeugt – neu erzeugen."))
    elif best_fehl:
        for e in best_fehl[:5]:
            befunde.append(("❌", name, "Abgleich", f"weicht vom freigegebenen Text ({best}) ab",
                            "fehlt in der Datei: „" + re.sub(r"\s+", " ", e)[:80] + "“ – Datei neu erzeugen (alte Version?)"))
    return best


def ungenutzt(d, alle_texte, befunde):
    t = norm(" ".join(alle_texte))
    for b in (d.get("profil") or {}).get("beispiele") or []:
        stich = b.get("stichwort") or b.get("situation") or b.get("thema") or ""
        kern = re.findall(r"[a-z0-9]{4,}", norm(stich))[:2]
        if kern and not any(k in t for k in kern):
            befunde.append(("⚠️", "Profil", "Beispiel ungenutzt", stich or b.get("thema", "?"),
                            "gesammeltes Beispiel kommt in keiner Unterlage vor – einbauen oder bewusst weglassen"))
    for h in (d.get("profil") or {}).get("hobbys") or []:
        kern = re.findall(r"[a-z0-9äöüß]{4,}", norm(h))[:1]
        if kern and kern[0] not in t:
            befunde.append(("⚠️", "Profil", "Hobby ungenutzt", h, "nicht im Lebenslauf – absichtlich?"))


def aufmerksam_check(d, B, befunde):
    for f in d.get("formular") or []:
        if "aufmerksam" in (f.get("feld") or "").lower():
            t = saetze_ohne_pruefen(f.get("text") or "")
            woerter = [w for w in re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", t) if norm(w) not in STANDARD]
            fehl = [w for w in woerter if not B.hat_wort(w)]
            if t.strip() and (not (d.get("profil") or {}).get("wie_aufmerksam") or fehl):
                befunde.append(("❌", "formular", "Wie aufmerksam?", t.strip()[:60],
                                "nicht vom Nutzer gesagt – fragen (profil.wie_aufmerksam), nie raten"))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    anzeigen = []
    while "--anzeige" in a:
        i = a.index("--anzeige")
        anzeigen.append(a[i + 1])
        del a[i:i + 2]
    kurz = "--kurz" in a
    a = [x for x in a if x != "--kurz"]
    try:
        d = textlib.lade_profil(a[0])
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(2)
    for x in anzeigen + a[1:]:
        if not os.path.isfile(x):
            print(f"FEHLER: Datei nicht gefunden: {x}")
            sys.exit(2)
    kt, offen = korpus(d, anzeigen)
    B = Belege(kt)
    befunde = []
    texte = json_texte(d)
    if not texte and not a[1:]:
        print("FEHLER: In der JSON stehen noch keine Unterlagen-Texte (lebenslauf/anschreiben/formular/email).")
        sys.exit(2)
    for sek, einheiten in texte.items():
        pruefe_text(sek + " (JSON)", "\n".join(einheiten), B, offen, befunde)
    alle = ["\n".join(v) for v in texte.values()]
    for datei in a[1:]:
        try:
            dt = textlib.read_any(datei)
        except RuntimeError as e:
            befunde.append(("❌", os.path.basename(datei), "Lesen", str(e), ""))
            continue
        name = os.path.basename(datei)
        if texte:
            abgleich(dt, texte, name, befunde)
        tmp = []
        pruefe_text(name, dt, B, offen, tmp)
        # Treffer, die schon im JSON-Text gemeldet wurden, nicht doppelt zeigen
        schon = {(b[2], b[3]) for b in befunde}
        befunde += [b for b in tmp if (b[2], b[3]) not in schon]
        alle.append(dt)
    aufmerksam_check(d, B, befunde)
    ungenutzt(d, alle, befunde)
    rot = [b for b in befunde if b[0] == "❌"]
    gelb = [b for b in befunde if b[0] == "⚠️"]
    print("# Fakten-Check – jeder Treffer: belegen, streichen oder den Nutzer fragen")
    for sym, wo, kat, was, ctx in rot + ([] if kurz else gelb):
        print(f"{sym} [{wo}] {kat}: {was}" + (f"  ⟶ {ctx}" if ctx else ""))
    n_pr = sum(len(PRUEFEN_RE.findall(x)) for x in alle)
    print("---")
    print(f"{len(rot)} ❌ ohne Beleg · {len(gelb)} ⚠️ prüfen · {n_pr} offene [PRÜFEN]")
    if not rot:
        print("✅ Keine unbelegten harten Fakten gefunden. Trotzdem Selbst-Check: Jeder Satz – woher weiß ich das?")
    print("Belegen = Fakt vom Nutzer in profil/… eintragen oder unter belege [{text, woher}] begründen.")
    sys.exit(1 if rot else 0)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
