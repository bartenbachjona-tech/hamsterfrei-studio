#!/usr/bin/env python3
"""Fakten-Check v5 („Fakten wörtlich, Formulierung frei“): Steht in den Unterlagen eine Behauptung, die der Nutzer NICHT gesagt hat
(und das nicht in Anzeige, Einladung oder seinen Uploads steht)? Prüft außerdem die Satz-Herkunft
(herkunft.py: jeder Satz über die Person ↔ Antwort-Nr. + wörtliches Zitat).

    python3 fakten_check.py PROFIL.json                  → prüft lebenslauf/anschreiben/formular/email der JSON
    python3 fakten_check.py PROFIL.json DATEI [DATEI …]  → zusätzlich die Dateien (.pdf/.docx/.txt) + Abgleich
                                                           Datei = freigegebener JSON-Text
    python3 fakten_check.py PROFIL.json --typ spickzettel [DATEI]  → Spickzettel (ohne Datei: aus der JSON gebaut)
    Optionen: --anzeige ANZEIGE.txt · --quelle UPLOAD.pdf (weitere Belegquellen) · --woher (Woher-Liste aus
              profil.herkunft für die Freigabe-Nachricht) · --kurz (nur ❌)

BELEGE (v3 – Wortlaut-Prinzip): NICHT die Profil-Felder, die Claude selbst füllt, sondern
  1. profil.rohtext – die Antworten des Nutzers im Wortlaut ({"nr", "frage", "antwort", "bestaetigt"}).
     „bestaetigt“ zählt nur, wenn die Antwort ein klares „ja“ ist und der Wert wörtlich in der Frage stand.
  2. Anzeige (ziel.anzeige_text, --anzeige), Einladung (gespraech.einladung_text), zugestimmte Firmenfakten
  3. Uploads mit Text (profil.anlagen[].datei, profil.quellen[], --quelle) – Zeugnisse, alter Lebenslauf
  4. belege[] mit Pflicht-Zitat {"text", "woher", "zitat"}: das Zitat muss wörtlich in 1–3 stehen UND den
     Wert tragen (jede Zahl/jedes Datum/jeder Abschluss im text muss aus dem Zitat folgen)
Normalisierungs-Wörterbuch (textlib.NORMALISIERUNG): fachabi ↔ Fachhochschulreife, fsj ↔ Freiwilliges Soziales
Jahr, papa ↔ Vater, str. ↔ Straße, B.A. ↔ Bachelor of Arts, „20h“ → 20 Std., „29-31k“ → 29.000/31.000,
Monatsnamen mit Tippfehlern, „april 25“, „märz bis august 24“, „31. August 2027“ = 31.08.2027 – ohne belege.
Lebenslauf: nur der Nutzer-Wortlaut zählt (Anzeige belegt nichts über die Person).
Dauern („drei Jahre“) zählen nur aus dem Nutzer-Wortlaut oder als Rechnung aus belegten Zeiträumen
(„10/2023 – 09/2026“ = 2 J. 11 M.); Zahlen aus der Anzeige belegen keine Dauer über den Nutzer.

Geprüft: Zahlen, Daten, Monate, Dauern (auch gerundet), Namen (zeilenweise, echte Eigennamen-Muster),
Abschlüsse/Kürzel, Sprachniveaus, Führerschein/Klasse, Links, Aufwertungen, Motivations-/Gefühlssätze ohne
Wortlaut (⚠️), [PRÜFEN] als Vorschlag, „Wie aufmerksam geworden?“ (nur die Quelle), Firmenfakten ohne
Zustimmung, Datei ≠ freigegebener Text. Ignoriert: Grußformel, Name darunter, Anlagen-Zeile, Feldtitel
„=== … (max. N Zeichen) ===“, Akte-Dateien.
❌ = ohne Beleg → Nutzer fragen oder streichen.  ⚠️ = prüfen.  Exit: 0 ohne ❌, 1 mit ❌, 2 Bedienfehler.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402
import sprachlib as SL  # noqa: E402

ERZEUGT = ("lebenslauf", "anschreiben", "formular", "email", "meta", "status")
PRUEFEN_RE = re.compile(r"\[PRÜFEN:[^\]]*\]")
HEUTE = datetime.date.today()
MONATE = {"januar": 1, "jan": 1, "jänner": 1, "februar": 2, "feb": 2, "märz": 3, "maerz": 3, "mär": 3, "april": 4,
          "apr": 4, "mai": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7, "august": 8, "aug": 8, "september": 9,
          "sept": 9, "sep": 9, "oktober": 10, "okt": 10, "november": 11, "nov": 11, "dezember": 12, "dez": 12}
MON_RE = "|".join(sorted(MONATE, key=len, reverse=True))
ZAHLWORT = {"ein": 1, "eine": 1, "einem": 1, "einen": 1, "einer": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
            "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11, "zwölf": 12,
            "fünfzehn": 15, "zwanzig": 20, "dreißig": 30, "fünfzig": 50, "hundert": 100, "tausend": 1000,
            "halb": 0.5, "halbes": 0.5, "halben": 0.5, "anderthalb": 1.5, "eineinhalb": 1.5, "zweieinhalb": 2.5,
            "zweit": 2, "dritt": 3, "viert": 4, "fünft": 5, "sechst": 6, "dutzend": 12, "beiden": 2, "beide": 2}
EINHEIT = r"(Jahre?n?|Jahr(?:es)?|Monate?n?|Monat(?:s)?|Wochen?|Tage?n?|Tag(?:es)?|Stunden?|Std\.?|Semester[n]?|Schuljahre?n?)"
EINH_NORM = [("schuljahr", "jahr"), ("jahr", "jahr"), ("monat", "monat"), ("woche", "woche"), ("tag", "tag"),
             ("stunde", "stunde"), ("std", "stunde"), ("semester", "semester")]
IN_MONATEN = {"jahr": 12, "monat": 1, "woche": 12 / 52, "semester": 6}
QUALI_RE = re.compile(r"(über|mehr als|fast|knapp|beinahe|rund|etwa|ungefähr|ca\.?|gut|insgesamt|bald)\s*$", re.I)
ABSCHLUESSE = ["abitur", "fachabitur", "fachhochschulreife", "allgemeine hochschulreife", "mittlere reife",
               "realschulabschluss", "hauptschulabschluss", "mittelschulabschluss", "qualifizierender", "quali",
               "msa", "bachelor", "master", "b.sc.", "b.a.", "m.sc.", "m.a.", "b.eng.", "m.eng.", "ll.b.", "ll.m.",
               "diplom", "staatsexamen", "magister", "meister", "techniker", "gesellenbrief", "gesellenprüfung",
               "abschlussprüfung", "promotion", "dr.", "matura", "lehrabschluss", "efz", "berufsmaturität",
               "ihk-abschluss", "ausbilderschein", "ada-schein", "ausbildungsjahr"]
NIVEAU_RE = re.compile(r"\b([ABC][12])\b|\b(Muttersprache|muttersprachlich|fließend|verhandlungssicher|Grundkenntnisse|"
                       r"Basiskenntnisse|gute Kenntnisse|sehr gute Kenntnisse|Konversationssicher)\b", re.I)
# nur echter Führerschein-Kontext: „13. Klasse am Gymnasium“ ist keiner
FUEHRERSCHEIN_RE = re.compile(r"(?i:\b(Führerschein|Fahrerlaubnis|PKW-Führerschein)\b)|(?<!\d\.\s)(?<!\d\.)\bKlasse\s+(?:BE|B96|C1E|C1|CE|AM|A1|A2|[ABCDLT])\b(?!\s+(?:am|an|der|des|im|in)\b)")
URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b[\w.+-]+@[\w-]+\.[\w.]+|\blinkedin\.com/\S+|\bxing\.com/\S+)", re.I)
AUFWERTUNG = ["geleitet", "leitung", "leitete", "projektleitung", "verantwortlich", "verantwortung", "eigenverantwortlich",
              "konzipiert", "mitkonzipiert", "entwickelt", "aufgebaut", "eingeführt", "optimiert", "gesteigert",
              "koordiniert", "geführt", "führung", "teamleitung", "filialverantwortung", "managed", "gemanagt",
              "maßgeblich", "federführend", "strategisch", "betreut", "verbessert", "ausgebildet", "eingearbeitet",
              "eingelernt", "selbstständig", "selbständig", "erfolgreich"]
FIRMEN_RE = re.compile(r"\b([A-ZÄÖÜ][\wÄÖÜäöüß&.\-]*(?:[ \t]+[A-ZÄÖÜ&][\wÄÖÜäöüß&.\-]*){0,3})[ \t]+"
                       r"(gGmbH|GmbH|AG|KG|SE|e\.\s?V\.|GbR|OHG|UG|mbH|KGaA)(?![\wÄÖÜäöüß])")
AKRONYM_RE = re.compile(r"\b([A-ZÄÖÜ]{2,}[0-9]*|[A-Z][a-z]+[A-Z][A-Za-z]+)\b")
AKRONYM_OK = {"EUR", "PDF", "IT", "EDV", "PC", "CV", "AG", "GMBH", "SE", "KG", "UG", "MS", "USB", "TV", "OK", "DE",
              "AT", "CH", "EU", "MWD", "PS", "ZB", "BZW", "CA", "UND", "WLAN", "III", "II", "IV", "HR", "KI", "AI",
              "WHATSAPP", "JPG", "PNG", "LKW", "PKW", "ABC", "STAR", "AC", "FAQ", "NR", "ID"}
QUELLEN = ["indeed", "stepstone", "linkedin", "xing", "jobbörse", "jobboerse", "arbeitsagentur", "agentur für arbeit",
           "bundesagentur", "instagram", "facebook", "tiktok", "youtube", "karriereseite", "website", "webseite",
           "homepage", "internet", "google", "messe", "jobmesse", "ausbildungsmesse", "zeitung", "aushang", "plakat",
           "freund", "freundin", "bekannt", "familie", "vater", "mutter", "eltern", "bruder", "schwester", "schule",
           "lehrer", "lehrerin", "berufsberatung", "berufsberater", "azubiyo", "ausbildung.de", "meinestadt",
           "kununu", "empfehlung", "praktikum", "glassdoor", "monster", "jobware", "kleinanzeigen", "radio", "app",
           "aubi-plus", "lehrstellenbörse", "ihk", "hwk", "uni", "hochschule", "career service", "kollege", "kollegin"]

# Wörter, die nie Eigennamen sind (bereits transliteriert verglichen – v2-Fehler: „Grüßen“ ≠ „gruessen“)
_STANDARD_ROH = """
lebenslauf kurzprofil berufserfahrung praktische erfahrung schulbildung bildung ausbildung studium kenntnisse
interessen ehrenamt praktika praktikum nebenjob minijob sprachen sprache edv muttersprache grundkenntnisse
anschreiben motivationsschreiben kurzanschreiben bewerbung bewerbungsunterlagen anlagen anlage zeugnis zeugnisse
sehr geehrte geehrter geehrtes damen herren freundlichen freundliche grüßen grüße gruß viele beste liebe lieber
hallo guten tag team ich sie ihr ihre ihnen ihrer ihres ihren ihrem euer eure euch wir uns unser unsere dabei darum
deshalb seit heute bei in im am an der die das den dem des ein eine einen einem einer gespräch vorstellungsgespräch
persönliches persönlichen einladung frage fragen stelle stellen anzeige ausbildungsplatz geboren betreff kennziffer
telefon e-mail adresse und oder sowie außerdem zudem gern gerne januar februar märz april mai juni juli august
september oktober november dezember montag dienstag mittwoch donnerstag freitag samstag sonntag
mit für von vom zum zur nach vor über unter auf aus als auch aber denn dann wenn weil dass ob wie was wer wo
mein meine meinen meinem meiner dein deine sein seine man es er jeder jede dieses diese dieser diesem diesen
jahr jahre jahren jahres monat monate monaten woche wochen tag tage tagen stunde stunden minute minuten mal prozent euro
zeit arbeit sachen sache dinge ding art teil ende anfang beginn platz weg leute menschen kunden kundinnen kunde
kollegen kolleginnen chef chefin betrieb firma unternehmen schule klasse fach fächer beruf berufe job jobs aufgabe
aufgaben erfahrung erfahrungen beispiel beispiele idee ideen grund gründe ziel ziele möglichkeit möglichkeiten
freude spaß interesse lust kontakt bereich bereiche alltag praxis theorie wissen können fähigkeit
umgang ordnung lager ware waren kasse abrechnung schicht schichten training verein mannschaft kinder kind eltern
familie freunde freizeit hobby hobbys kenntnis programm programme computer handy internet mail email
ausbildungsjahr studiengang semester abschluss note noten vorlesung vorlesungen projekt projekte gruppe gruppen
start eintritt eintrittstermin frühester frühestmöglicher motivation über mich warum wieso aufmerksam geworden
gehaltsvorstellung gehalt verfügbarkeit wochenstunden arbeitszeit bewerbungsweg unterlagen rückfragen
rückmeldung anhang gesprächspartner gesprächspartnerin ansprechpartner ansprechpartnerin hiermit sehr gut gute neue neuen erste ersten letzte letzten nächste nächsten
aushilfe aushilfen mitarbeiter mitarbeiterin praktikant praktikantin werkstudent werkstudentin azubi azubis
auszubildende auszubildender helfer helferin minijobber schülerpraktikum ferienjob nebenjob teilzeit vollzeit
haus praxis filiale markt laden geschäft kita kanzlei büro werkstatt kantine zentrale standort
zertifikate zertifikat scheine schein sonstiges sonstige weitere weiterbildung weiterbildungen führerschein software
it-kenntnisse edv-kenntnisse sprachkenntnisse fähigkeiten stärken projekte schwerpunkte tätigkeiten aufgaben
vater mutter eltern oma opa bruder schwester cousine cousin tante onkel
""".split()
STANDARD = {textlib.translit(w) for w in _STANDARD_ROH}
NOMEN_ENDUNG = re.compile(r"(ung|ungen|heit|heiten|keit|keiten|schaft|schaften|tion|tionen|tät|täten|nis|nisse|tum|ment|"
                          r"ismus|ik|ur|enz|anz|chen|lein|ling|linge|nahme|stelle|arbeit|zeit|ort|platz|raum|plan|tag|"
                          r"woche|wochen|jahr|jahre|gespräch|gespräche|aufgabe|aufgaben|bereich|kunden|kundin|kundinnen|"
                          r"leute|team|teams|ware|waren|halle|lager|dienst|beruf|berufe|fach|fächer|kasse|kurs|kurse)$")
GRUSS_RE = re.compile(r"^\s*(mit\s+)?(freundlichen|freundliche|beste[n]?|viele[n]?|herzliche[n]?|liebe[n]?|sonnige)\s+gr(ü|ue)(ß|ss)(e|en)\b", re.I)
IGNORIER_ZEILE = re.compile(r"^\s*(Anlagen?\s*:|===.*===\s*$|Betreff\s*:)", re.I)
MAXZ_RE = re.compile(r"\(?\s*max\.?\s*\d{1,3}(?:[.\s]\d{3})*\s*(Zeichen|Wörter|Worte)\s*\)?", re.I)


# ---------------------------------------------------------------- Hilfen
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


def norm(s):
    return textlib.translit((s or "").lower())


def kompakt(s):
    return re.sub(r"\s+", " ", norm(s)).strip()


def zahl(s):
    s = s.strip()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def jahr2(y):
    y = int(y)
    return y + 2000 if y < 100 else y


def monate_fmt(m):
    j, r = divmod(int(round(m)), 12)
    return (f"{j} J. " if j else "") + f"{r} M."


class Belege:
    """Belegsammlung aus einem Text: Wörter, Jahre, Monate, Tage, Zahlen, Dauern, Zeiträume."""

    def __init__(self, text, nutzer=False):
        self.text = text or ""
        self.low = norm(self.text)
        self.woerter = set(re.findall(r"[a-z0-9]+", self.low))
        self.monate, self.jahre, self.tage = set(), set(), set()
        for y, m, t in self.daten(self.text, nutzer):
            self.jahre.add(y)
            if m:
                self.monate.add((y, m))
            if t:
                self.tage.add((y, m, t))
        rest = self.ohne_daten(self.text)
        self.zahlen = {z for z in (zahl(x) for x in re.findall(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])", rest)) if z is not None}
        self.zahlen |= {float(m) for _, m in self.monate}
        for w, v in ZAHLWORT.items():
            if w not in ("ein", "eine", "einem", "einen", "einer") and re.search(rf"\b{w}\b", self.text, re.I):
                self.zahlen.add(float(v))
        self.dauern = set(d for d, _ in self.dauern_mit_pos(self.text))
        self.zeitraeume = zeitraeume(self.text)

    @staticmethod
    def daten(t, nutzer=False):
        for m in re.finditer(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b", t):
            yield jahr2(m.group(3)), int(m.group(2)), int(m.group(1))
        for m in re.finditer(r"\b(\d{1,2})\.\s*(" + MON_RE + r")\.?\s+(\d{4})\b", t, re.I):   # „31. August 2027“
            yield int(m.group(3)), MONATE[m.group(2).lower()], int(m.group(1))
        for m in re.finditer(r"\b(\d{1,2})\s*[/.]\s*(\d{4})\b", t):
            if 1 <= int(m.group(1)) <= 12:
                yield int(m.group(2)), int(m.group(1)), None
        for m in re.finditer(r"\b(" + MON_RE + r")\.?\s+(\d{4})\b", t, re.I):
            yield int(m.group(2)), MONATE[m.group(1).lower()], None
        for m in re.finditer(r"(?<![\d./])((?:19|20)\d{2})(?![\d])", t):
            yield int(m.group(1)), None, None
        if nutzer:   # Nutzer schreiben „seit märz 25“, „juli 24“, „03/25“, „ab dezember“, „märz bis august 24“
            for m in re.finditer(r"\b(" + MON_RE + r")\.?\s+'?(\d{2})\b(?![.:\d])", t, re.I):
                yield jahr2(m.group(2)), MONATE[m.group(1).lower()], None
            for m in re.finditer(r"\b(" + MON_RE + r")\.?\s*(?:bis|-|–|und)\s*(" + MON_RE + r")\.?\s+'?(\d{2}|\d{4})\b", t, re.I):
                y = jahr2(m.group(3))
                yield y, MONATE[m.group(1).lower()], None
                yield y, MONATE[m.group(2).lower()], None
            for m in re.finditer(r"\b(\d{1,2})\.\s*(" + MON_RE + r")\b(?!\.?\s*'?\d)", t, re.I):   # „zum 1. januar“
                mo = MONATE[m.group(2).lower()]
                yield (HEUTE.year if mo >= HEUTE.month else HEUTE.year + 1), mo, int(m.group(1))
            for m in re.finditer(r"(?<![\w.])(" + MON_RE + r")\b(?!\.?\s*'?\d)", t, re.I):         # Monat ohne Jahr
                vor = t[max(0, m.start() - 8):m.start()].lower()
                if re.search(r"\b(ab|im|seit|bis|zum|ende|anfang|mitte|von|und|-|–)\s*$", vor):
                    continue      # mit Präposition: unten genauer
                mo = MONATE[m.group(1).lower()]
                yield (HEUTE.year if mo >= HEUTE.month else HEUTE.year + 1), mo, None
                yield (HEUTE.year if mo <= HEUTE.month else HEUTE.year - 1), mo, None
            for m in re.finditer(r"(?<![\d./])(\d{1,2})/(\d{2})(?![\d/])", t):
                if 1 <= int(m.group(1)) <= 12:
                    yield jahr2(m.group(2)), int(m.group(1)), None
            for m in re.finditer(r"\b(ab|im|seit|bis|zum|ende|anfang|mitte)\s+(" + MON_RE + r")\b(?!\.?\s*'?\d)", t, re.I):
                mo = MONATE[m.group(2).lower()]
                y = HEUTE.year if mo >= HEUTE.month or m.group(1).lower() == "seit" else HEUTE.year + 1
                if m.group(1).lower() == "seit" and mo > HEUTE.month:
                    y = HEUTE.year - 1
                yield y, mo, None

    @staticmethod
    def ohne_daten(t):
        t = re.sub(r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b", " ", t)
        t = re.sub(r"\b\d{1,2}\.\s*(?=(?:" + MON_RE + r")\b)", " ", t, flags=re.I)
        t = re.sub(r"\b\d{1,2}\s*[/.]\s*\d{4}\b", " ", t)
        return t

    @staticmethod
    def dauern_mit_pos(t):
        wort = "|".join(sorted(ZAHLWORT, key=len, reverse=True))
        for m in re.finditer(rf"(?<![\w/.])(\d+(?:[.,]\d+)?|{wort})\s*(?:-\s*)?{EINHEIT}(?![\wäöü])", t, re.I):
            roh = m.group(1).lower()
            v = ZAHLWORT.get(roh) if roh in ZAHLWORT else zahl(roh)
            e = m.group(2).lower()
            einheit = next((n for k, n in EINH_NORM if e.startswith(k)), e)
            if v is not None:
                yield (float(v), einheit), m

    def hat_wort(self, w):
        w = norm(w)
        if not w:
            return True
        if re.search(r"(?<![a-z0-9])" + re.escape(w), self.low):
            return True
        if "-" in w or " " in w:      # „Kfz-Mechatroniker“ ↔ „kfz mechatroniker“, „U-Bahn“ ↔ „ubahn“
            dicht = re.sub(r"[\s-]+", "", w)
            if dicht in re.sub(r"[\s-]+", "", self.low) or re.sub(r"-", " ", w) in self.low:
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


def zeitraeume(t):
    """Zeiträume → Dauer in Monaten (09/2018 – 07/2024, März 2025 bis heute, seit 03/2025)."""
    out = []
    mm = r"(?:(\d{1,2})\s*/\s*(\d{4})|(" + MON_RE + r")\.?\s+(\d{4}))"
    for m in re.finditer(mm + r"\s*(?:–|-|bis)\s*(?:" + mm + r"|(heute|jetzt|laufend))", t, re.I):
        g = m.groups()
        def ym(a, b, c, d):
            if a:
                return int(b), int(a)
            if c:
                return int(d), MONATE[c.lower()]
            return None
        s = ym(*g[0:4])
        e = ym(*g[4:8]) if not g[8] else (HEUTE.year, HEUTE.month)
        if s and e:
            out.append((e[0] - s[0]) * 12 + e[1] - s[1] + 1)
    for m in re.finditer(r"\bseit\s+" + mm, t, re.I):
        g = m.groups()
        s = (int(g[1]), int(g[0])) if g[0] else (int(g[3]), MONATE[g[2].lower()])
        out.append((HEUTE.year - s[0]) * 12 + HEUTE.month - s[1])
    return [x for x in out if 0 <= x < 600]


# ---------------------------------------------------------------- Korpus
def korpus(d, anzeigen=(), quellen=(), befunde=None):
    """→ (U, A, UA, offene_firmenfakten, legacy). U = Nutzer-Wortlaut + Uploads + gültige Belege,
    A = Anzeige/Einladung/zugestimmte Firmenfakten/heutiges Datum."""
    befunde = befunde if befunde is not None else []
    z = d.get("ziel") or {}
    a_teile = [z.get("anzeige_text", "")]
    for f in anzeigen:
        a_teile.append(textlib.read_any(f))
    a_teile.append((d.get("gespraech") or {}).get("einladung_text", ""))
    offen = []
    for f in d.get("firmenfakten") or []:
        if f.get("zugestimmt") is True:
            a_teile.append(f.get("fakt", ""))
        else:
            offen.append(f.get("fakt", ""))
    a_teile.append(HEUTE.strftime("%d.%m.%Y"))
    anzeige_roh = "\n".join(a_teile)
    # Ziel-Metadaten (Firma, Stelle, Adresse …) stammen aus der Anzeige – dort gegenprüfen
    meta = []
    for k in ("firma", "stelle", "kennziffer", "ansprechperson", "anrede", "firma_adresse", "start", "frist"):
        v = z.get(k)
        meta += v if isinstance(v, list) else [v or ""]
    a_teile += meta

    legacy = not textlib.rohtext_eintraege(d)
    if legacy:
        u_teile = flach({k: v for k, v in d.items() if k not in ERZEUGT and k not in ("firmenfakten", "ziel", "belege")})
        befunde.append(("⚠️", "Profil", "Kein Wortlaut", "profil.rohtext fehlt",
                        "Prüfung nur gegen Profil-Felder (unsicher). Nutzer-Antworten im Wortlaut in profil.rohtext speichern."))
    else:
        u_teile = [SL.standardisiere(x) for x in textlib.wortlaut(d)]
    up, hinw = textlib.upload_texte(d, quellen)
    u_teile += [textlib.normalisiere_nutzertext(x) for x in up]
    for h in hinw:
        befunde.append(("ℹ️", "Uploads", "Hinweis", h, ""))
    basis = kompakt("\n".join(u_teile + [anzeige_roh]))
    for b in d.get("belege") or []:
        zit = kompakt(b.get("zitat", "")) if isinstance(b, dict) else ""
        txt = b.get("text", "") if isinstance(b, dict) else str(b)
        if not zit or zit not in basis:
            befunde.append(("❌", "belege", "Beleg ohne Zitat", txt[:60],
                            "Jeder Beleg braucht ein wörtliches Zitat aus Nutzer-Antwort, Anzeige oder Upload (zitat)."))
            continue
        fehlt = traegt_nicht(txt, b.get("zitat", ""))
        if fehlt:
            befunde.append(("❌", "belege", "Zitat trägt den Wert nicht", txt[:60],
                            "im Zitat steht nicht: " + ", ".join(fehlt) + " – Beleg gilt nicht (nicht „wegbelegen“)."))
            continue
        u_teile.append(txt)          # „woher“ ist Claudes Erklärung, kein Beleg
    if not legacy:
        alle_a = norm(anzeige_roh)
        if (z.get("anzeige_text") or "").strip():
            for k in ("firma", "stelle", "ansprechperson"):
                w = [x for x in re.findall(r"[A-Za-zÄÖÜäöüß]{4,}", z.get(k) or "") if norm(x) not in STANDARD]
                fehl = [x for x in w if norm(x)[:max(4, len(norm(x)) - 3)] not in alle_a and norm(x) not in kompakt("\n".join(u_teile))]
                if fehl:
                    befunde.append(("⚠️", "ziel", f"ziel.{k}", z.get(k), "steht so nicht in Anzeige/Nutzer-Antworten – Quelle prüfen"))
    U = Belege("\n".join(u_teile), nutzer=True)
    A = Belege("\n".join(a_teile))
    UA = Belege(U.text + "\n" + A.text, nutzer=True)
    zr_antw = [(norm(x), zeitraeume(x)) for x in u_teile]
    return U, A, UA, offen, legacy, zr_antw


def traegt_nicht(txt, zitat):
    """Was im Beleg-Text steht, aber nicht aus dem Zitat folgt (Zahlen, Daten, Dauern, Abschlüsse, Niveaus)."""
    Z = Belege(textlib.normalisiere_nutzertext(zitat), nutzer=True)
    fehl = []
    for y, mo, tg in Belege.daten(txt):
        if tg and (y, mo, tg) not in Z.tage:
            fehl.append(f"{tg:02d}.{mo:02d}.{y}")
        elif mo and not tg and (y, mo) not in Z.monate:
            fehl.append(f"{mo:02d}/{y}")
        elif not mo and y not in Z.jahre:
            fehl.append(str(y))
    comp = zeitraeume(zitat)
    for (v, e), m in Belege.dauern_mit_pos(txt):
        r = pruefe_dauer(v, e, txt[max(0, m.start() - 20):m.start()], txt, Z, Belege(""), comp)
        if r and r[0] == "❌":
            fehl.append(m.group(0))
    rest = Belege.ohne_daten(txt)
    for m in re.finditer(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])", rest):
        zz = zahl(m.group(0))
        if zz is not None and zz not in Z.zahlen and not any(v == zz for v, _ in Z.dauern) and \
                not any(v == zz for (v, _), _m in Belege.dauern_mit_pos(rest[m.start():m.end() + 12])):
            fehl.append(m.group(0))
    lt = norm(txt)
    for a in ABSCHLUESSE:
        na = norm(a)
        if re.search(r"(?<![a-z])" + re.escape(na) + (r"(?![a-z])" if not na.endswith(".") else ""), lt) and \
                not re.search(r"(?<![a-z])" + re.escape(na), Z.low):
            fehl.append(a)
    for m in NIVEAU_RE.finditer(txt):
        if not Z.hat_wort(m.group(0)):
            fehl.append(m.group(0))
    return list(dict.fromkeys(fehl))


# ---------------------------------------------------------------- Text vorbereiten
SPICK_KOPF = re.compile(r"^\s*(spickzettel|termin\b|mitbringen|deine 3 kernbotschaften|ihre 3 kernbotschaften|kernbotschaften|"
                        r"so stellst du dich vor|so stellen sie sich vor|vorstellung|schwierige fragen|fachfragen|"
                        r"deine beispiele|ihre beispiele|beispiele|deine fragen|ihre fragen|fragen an die firma|"
                        r"dein auswahltag|ihr auswahltag|die übungen|übungen|tipps)\b", re.I)
SPICK_PRUEFEN = re.compile(r"^\s*(spickzettel|termin|deine 3 kernbotschaften|ihre 3 kernbotschaften|kernbotschaften|"
                           r"so stellst du dich vor|so stellen sie sich vor|vorstellung|schwierige fragen|fachfragen|"
                           r"deine beispiele|ihre beispiele|beispiele)\b", re.I)
ORT_DATUM_RE = re.compile(r"^\s*[A-ZÄÖÜ][\wäöüß .\-]{1,40},\s*(den\s+)?\d{1,2}\.\s?\d{1,2}\.\s?\d{2,4}\s*$")


def zeilen_fuer_pruefung(t, spickzettel=False):
    """Zeilen, die geprüft werden: ohne Grußformel + Name darunter, Anlagen (auch umbrochen), Feldtitel,
    Betreff-Label, „max. N Zeichen“, Ort/Datum-Zeile des Briefs. Beim Spickzettel: nur die Fakten-Abschnitte
    (Kernbotschaften, Vorstellung, Antworten „→ …“, Beispiele) – ohne Überschriften, Fragen, Tipps, Übungen,
    Mitbring-Liste und ohne eigene Nummerierung („1.“, „•“)."""
    out, nach_gruss, skip, in_anlagen = [], 0, False, False
    for z in (t or "").splitlines():
        if spickzettel:
            if SPICK_KOPF.match(z) and (z.strip().isupper() or z.lower().startswith(("spickzettel", "termin")) or len(z.split()) <= 6):
                skip = not SPICK_PRUEFEN.match(z)
                if z.lstrip().lower().startswith(("spickzettel", "termin")):
                    out.append(re.sub(r"^\s*SPICKZETTEL\s*[–:-]\s*", "", z, flags=re.I))
                continue
            if skip:
                continue
            z = re.sub(r"^\s*(?:[1-9][.)](?!\s*" + textlib.ORDINAL_NOMEN + r")|[•\-–·▸])\s+", "", z)   # eigene Nummerierung (nicht „12. Klasse“)
            if z.strip().endswith("?") or z.strip().lower().startswith(("frage:", "f:")):
                continue          # Fragen sind keine Fakten
            z = re.sub(r"^\s*(→|antwort:)\s*", "", z, flags=re.I)
        if in_anlagen:
            if z.strip():
                continue          # umbrochene Anlagen-Zeile
            in_anlagen = False
        if ORT_DATUM_RE.match(z):
            continue              # „Ingolstadt, 07.11.2026“ – Briefdatum ist Erstellungsdatum, kein Fakt
        if GRUSS_RE.match(z):
            nach_gruss = 2
            continue
        if nach_gruss and z.strip():
            nach_gruss -= 1
            if len(z.split()) <= 4:
                continue
        if IGNORIER_ZEILE.match(z):
            if z.strip().lower().startswith("betreff"):
                out.append(re.sub(r"^\s*Betreff\s*:\s*", "", z, flags=re.I))
            elif re.match(r"^\s*Anlagen?\s*:", z, re.I):
                in_anlagen = True
            continue
        out.append(MAXZ_RE.sub(" ", z))
    return out


def saetze(text):
    for s in textlib.saetze(text):
        if len(s.split()) >= 3:
            yield s.strip()


def klausel_bei(z, pos):
    """Teilsatz (zwischen , ; : – ( )) um die Position pos."""
    a = max([z.rfind(c, 0, pos) for c in ",;:–—().\n"] + [-1]) + 1
    bs = [i for i in (z.find(c, pos) for c in ",;:–—()\n") if i >= 0]
    return z[a:min(bs) if bs else len(z)]


SPRACHEN = ["Deutsch", "Englisch", "Französisch", "Spanisch", "Italienisch", "Türkisch", "Russisch", "Polnisch", "Arabisch",
            "Kroatisch", "Serbisch", "Bosnisch", "Rumänisch", "Griechisch", "Portugiesisch", "Ukrainisch", "Albanisch",
            "Kurdisch", "Persisch", "Farsi", "Vietnamesisch", "Chinesisch", "Japanisch", "Niederländisch", "Ungarisch",
            "Tschechisch", "Bulgarisch", "Latein", "Gebärdensprache", "Tamil", "Hindi", "Urdu", "Dari", "Paschtu"]
EINSCHRAENKUNG = r"(manchmal|ab und zu|gelegentlich|selten|bisschen|bissl|bissel|etwas|ein wenig|nicht wirklich|kaum|teilweise|ab und an|so halb)"
PERSON_TITEL_RE = re.compile(r"\b(Herrn?|Frau)\s+((?:Dr\.|Prof\.|Dipl\.-?\w*\.?|Mag\.)\s*)*([A-ZÄÖÜ][\wäöüß\-]+)(\s+[A-ZÄÖÜ][\wäöüß\-]+)?")


def ohne_fremde_personen(t, A):
    """Anrede/Gesprächspartner aus Anzeige oder Einladung („Herr Dr. Huber“, „Frau Albrecht (Teamleitung)“) sind keine
    Angaben über den Nutzer → vor der Abschluss-/Titel-/Aufwertungs-Prüfung entfernen."""
    def weg(m):
        nachname = (m.group(4) or m.group(3)).strip()
        return " " if norm(nachname) in A.low or norm(m.group(3)) in A.low else m.group(0)
    t = PERSON_TITEL_RE.sub(weg, t)
    return re.sub(r"\((?:[A-ZÄÖÜ][\wäöüß\-]*)?(leitung|leiter|leiterin|teamleitung|personalleitung|ausbildungsleitung)\)", " ", t, flags=re.I)


def kontext(m, src):
    a, b = max(0, m.start() - 35), min(len(src), m.end() + 35)
    return re.sub(r"\s+", " ", src[a:b]).strip()


ICH_RE = re.compile(r"\b(ich|mich|mir|mein\w*|wir|habe|hab|bin|war)\b", re.I)


def pruefe_dauer(v, e, satz_vor, satz, U, A, computed):
    """→ None (ok) oder (sym, msg)."""
    q = QUALI_RE.search(satz_vor)
    qual = q.group(1).lower().rstrip(".") if q else ""
    claim = v * IN_MONATEN.get(e, 0) if e in IN_MONATEN else None
    vtxt = ("%g" % v).replace(".", ",")
    nah = [c for c in computed if claim is not None and abs(c - claim) <= max(6, claim * 0.25) and c != claim]
    if (v, e) in U.dauern:
        if not qual and nah and claim and claim >= 12:
            return ("⚠️", f"Nutzer sagt {vtxt} {e}(e), aus den Daten berechnet {monate_fmt(nah[0])} – genauer schreiben?")
        return None
    if claim is not None and computed:
        if qual in ("über", "mehr als", "gut") and any(c > claim for c in computed):
            return None
        if qual in ("fast", "knapp", "beinahe", "bald") and any(claim - 6 <= c < claim for c in computed):
            return None
        if qual in ("rund", "etwa", "ungefähr", "ca", "insgesamt") and any(abs(c - claim) <= 2 for c in computed):
            return None
        if not qual and claim in computed:
            return None
        if not qual and e == "jahr" and any(claim <= c < claim + 12 for c in computed):
            return None   # v5: abgerundet ist korrekt („sieben Jahre“ bei 7 J. 2 M.), aufgerundet nicht
        if nah:
            return ("❌", f"gerundet: aus den Daten berechnet {monate_fmt(nah[0])} – genau schreiben "
                          f"(„seit …“, „fast {vtxt} {e}e“) oder Nutzer fragen")
    if (v, e) in A.dauern and not ICH_RE.search(satz):
        return None   # Fakt aus der Anzeige („Die Ausbildung dauert 3 Jahre“)
    return ("❌", "Dauer so nicht vom Nutzer gesagt und nicht aus Daten berechenbar (Anzeige-Zahlen zählen hier nicht)")


DETERMINATIV_RE = re.compile(r"^(Ihr|Ihre|Ihrem|Ihren|Ihrer|Ihres|Mein|Meine|Meinem|Meinen|Meiner|Unser|Unsere|Unserem|"
                             r"Unseren|Euer|Eure|Der|Die|Das|Den|Dem|Des|Ein|Eine|Einem|Einen|Einer|Jede|Jeder|Diese|Dieser)$")
ALTER_RE = re.compile(r"(\balt\b|kind|kinder|sohn|söhne|tochter|töchter|enkel|jährig|\balter\b|lebensjahr)", re.I)


def passende_zeitraeume(zeile, K):
    """Zeiträume (in Monaten) aus derselben Zeile + aus Nutzer-Antworten, die inhaltlich zur Zeile passen."""
    out = list(zeitraeume(zeile))
    kern = {w[:6] for w in re.findall(r"[a-z]{5,}", norm(zeile)) if w not in STANDARD}
    kern |= {norm(a) for a in re.findall(r"\b[A-ZÄÖÜ]{2,5}\b", zeile)}
    for antw, zr in K.get("zr_antworten", []):
        if zr and kern & {w[:6] for w in re.findall(r"[a-z0-9]{2,}", antw)}:
            out += zr
    return sorted(set(out))


def ist_eigenname_folge(tokens):
    """Echte Eigennamen-Muster: mind. ein Token, das kein Standardwort ist und nicht wie ein normales
    Nomen endet (Minuten Zeit, Ihren Sachen, Erfahrung Kundenkontakt → keine Namen)."""
    kand = [t for t in tokens if norm(t) not in STANDARD and not NOMEN_ENDUNG.search(t.lower())]
    return kand


# ---------------------------------------------------------------- Prüfung eines Textes
def pruefe_text(name, t, K, befunde, spickzettel=False, nur_nutzer=False):
    """nur_nutzer (Lebenslauf): Belege nur aus dem Nutzer-Wortlaut/Uploads – die Anzeige belegt nichts über die Person."""
    U, A, UA, offen = K["U"], K["A"], K["UA"], K["offen"]
    if nur_nutzer:
        A, UA = Belege(""), U
    gemeldet = set()

    def add(sym, kat, was, ctx=""):
        befunde.append((sym, name, kat, was, ctx))
        gemeldet.update(norm(x) for x in re.findall(r"[A-Za-zÄÖÜäöüß]{3,}", was))

    for m in PRUEFEN_RE.finditer(t):
        inh = m.group(0).lower()
        if re.search(r"stimmt (das|es)|so ok|korrekt\?|passt (das|es)|einverstanden|oder\?|richtig\?", inh):
            add("⚠️", "[PRÜFEN] als Vorschlag", m.group(0)[:70],
                "[PRÜFEN] nur für echte Lücken. Eigene Vorschläge vorher im Chat fragen – nicht in den Text schreiben.")
    zeilen = zeilen_fuer_pruefung(PRUEFEN_RE.sub(" ", t), spickzettel)
    A_voll = K["A"]
    zeilen = [ohne_fremde_personen(z, A_voll) for z in zeilen]
    s = "\n".join(zeilen)

    # Daten
    for y, mo, tg in Belege.daten(s):
        if tg and (y, mo, tg) not in UA.tage:
            if (y, mo) in UA.monate:
                add("❌", "Datum", f"{tg:02d}.{mo:02d}.{y}", "Tag erfunden – nur der Monat ist belegt (z. B. „ab Dezember 2026“)")
            else:
                add("❌", "Datum", f"{tg:02d}.{mo:02d}.{y}", "kein Beleg")
        elif mo and not tg and (y, mo) not in UA.monate:
            nachbar = {((y * 12 + mo - 1 + dd) // 12, (y * 12 + mo - 1 + dd) % 12 + 1) for dd in (-1, 1)}
            if nachbar & UA.monate and (y, mo) in K.get("luecken_monate", set()):
                pass      # Lücke: Monate ergeben sich aus den Nachbarstationen – so gewollt
            elif nachbar & UA.monate:
                add("⚠️", "Monat", f"{mo:02d}/{y}", "aus dem Nachbarmonat abgeleitet (z. B. Lücke zwischen zwei Stationen) – passt das?")
            elif y in UA.jahre:
                add("❌", "Monat", f"{mo:02d}/{y}", f"nur das Jahr {y} ist im Wortlaut – Monat erfragen oder nur „{y}“ schreiben")
            else:
                add("❌", "Monat/Jahr", f"{mo:02d}/{y}", "kein Beleg")
        elif not mo and y not in UA.jahre:
            if y in K.get("abgel", {}):
                add("⚠️", "Jahr", str(y), f"abgeleitet aus „{K['abgel'][y]}“ – kurz bestätigen lassen (Ja/Nein)")
            else:
                add("❌", "Jahr", str(y), "kein Beleg")
    # Dauern (zeilenweise, mit Satz-Kontext). Gerechnet wird nur mit Zeiträumen derselben Zeile oder aus
    # Antworten, die zum Satz passen (v3-Fehler: „4 Semester“ gegen die Minijob-Dauer geprüft).
    gesehen_d = set()
    for z in zeilen:
        for (v, e), m in Belege.dauern_mit_pos(z):
            umfeld = z[max(0, m.start() - 30):m.end() + 15]
            if ALTER_RE.search(umfeld) and v in UA.zahlen:
                continue          # Alter („Kinder (4 und 7 Jahre)“, „3- bis 6-Jährige“) ist keine Dauer
            satz_vor = z[max(0, m.start() - 20):m.start()]
            r = pruefe_dauer(v, e, satz_vor, z, U, A, passende_zeitraeume(z, K))
            key = (v, e, r[0] if r else "")
            if r and key not in gesehen_d:
                gesehen_d.add(key)
                vtxt = ("%g" % v).replace(".", ",")
                add(r[0], "Dauer", f"{vtxt} {e}(e)", r[1] + f" ⟵ „{kontext(m, z)}“")
    # Zahlen
    rest = Belege.ohne_daten(s)
    rest = re.sub(r"\b[ABC][12]\b", " ", rest)
    rest = re.sub(r"\b(\d{1,2}):00\b", r"\1", rest)      # „9:00 Uhr“ = „9 Uhr“
    for m in re.finditer(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])", rest):
        zz = zahl(m.group(0))
        if zz is None or zz in UA.zahlen:
            continue
        if any(v == zz for v, _ in UA.dauern):
            continue
        if 1900 <= zz <= 2100 and (int(zz) in UA.jahre or int(zz) in K.get("abgel", {})):
            continue      # abgeleitete Jahre („letztes Jahr“) meldet die Datumsprüfung als ⚠️
        if any(v == zz for (v, _), _m in Belege.dauern_mit_pos(rest[max(0, m.start() - 1):m.end() + 12])):
            continue   # schon als Dauer geprüft
        add("❌", "Zahl", m.group(0), kontext(m, rest))
    wort = "|".join(w for w in ZAHLWORT if w not in ("ein", "eine", "einem", "einen", "einer", "beiden", "beide"))
    for m in re.finditer(rf"\b(?:zu\s+)?({wort})\b(?!\s*(?:-\s*)?{EINHEIT})", s, re.I):
        if float(ZAHLWORT[m.group(1).lower()]) not in UA.zahlen and not UA.hat_wort(m.group(0)):
            add("❌", "Zahlwort", m.group(0), kontext(m, s))
    # Abschlüsse / Kürzel
    low = norm(s)
    abschl_basis = U.low + "\n" + norm(K["stelle"] + " " + K["firma"])   # Stellentitel („… (B.A.)“) darf im Betreff stehen
    for a in ABSCHLUESSE:
        na = norm(a)
        m_a = re.search(r"(?<![a-z])" + re.escape(na) + (r"(?![a-z])" if not na.endswith(".") else ""), low)
        if m_a and not re.search(r"(?<![a-z])" + re.escape(na) + (r"(?![a-z])" if not na.endswith(".") else ""), abschl_basis):
            # v5: im Sie-Teilsatz aus Anzeige/zugestimmtem Firmenfakt („ab dem 2. Ausbildungsjahr betreuen Azubis bei Ihnen“)
            kl = klausel_bei(low, m_a.start())
            if not nur_nutzer and re.search(r"(?<![a-z])" + re.escape(na), A_voll.low) and \
                    re.search(r"\b(sie|ihnen|ihr\w*)\b", kl) and not SL.ICH_RE.search(kl):
                continue
            add("❌", "Abschluss", a, "Abschluss/Kürzel steht nicht im Wortlaut des Nutzers oder in seinem Zeugnis "
                                     "(die Anzeige belegt nichts über ihn)")
    # Sprachen (v5): „Deutsch (Muttersprache)“ nie ohne Nutzerangabe
    if nur_nutzer or spickzettel:
        for sp in SPRACHEN:
            for m in re.finditer(r"\b" + sp + r"\b", s):
                if not U.hat_wort(sp):
                    add("❌", "Sprache", sp, f"„{sp}“ hat der Nutzer nicht genannt – nie automatisch eintragen (auch nicht "
                                            "Deutsch als Muttersprache), Sprachen-Frage stellen")
                break
    # Sprachniveaus
    for m in NIVEAU_RE.finditer(s):
        if not U.hat_wort(m.group(0)):
            if re.match(r"(grund|basis|schul)", m.group(0), re.I):   # Abwertung („bisschen“ → Grundkenntnisse)
                add("⚠️", "Niveau", m.group(0), kontext(m, s) + " – so vorsichtig formuliert ok? (Nutzerwort lieber übernehmen)")
            else:
                add("❌", "Sprachniveau", m.group(0), kontext(m, s))
        else:
            vor = s[max(0, m.start() - 25):m.start()]
            spr = re.findall(r"\b([A-ZÄÖÜ][a-zäöüß]+(?:isch|sch))\b", vor)
            if spr and m.group(1):
                pat = norm(spr[-1])[:5] + r"\w*\W{0,4}(?:\w+\W{0,3}){0,3}" + norm(m.group(0))
                if not re.search(pat, U.low):
                    add("❌", "Sprachniveau", f"{spr[-1]} {m.group(0)}", "diese Kombination hat der Nutzer nicht gesagt")
    # Führerschein / Klasse (nur echter Kontext)
    for m in FUEHRERSCHEIN_RE.finditer(s):
        if not re.search(r"fuehrerschein|fahrerlaubnis|\blappen\b|\bb[- ]?schein\b|auto ?fahren", U.low):
            add("❌", "Führerschein", m.group(0), "Führerschein hat der Nutzer nie erwähnt")
            break
        kl = re.search(r"Klasse\s+(\w+)", m.group(0))
        x = norm(kl.group(1)) if kl else ""
        if kl and not re.search(r"(fuehrerschein|schein|lappen|fahrerlaubnis)\W{0,3}(klasse\W{0,2})?" + x + r"\b|\b" + x
                                + r"[- ]?(schein|fuehrerschein)\b|(?<![\d.] )\bklasse\W{0,2}" + x + r"\b(?! (am|an|der|des|im|in)\b)", U.low):
            add("❌", "Führerschein", m.group(0), f"„Klasse {kl.group(1)}“ steht nicht im Wortlaut – Nutzer fragen")
            break
    # URLs/E-Mail
    for m in URL_RE.finditer(s):
        u = m.group(0).rstrip(".,;)")
        if norm(u) not in UA.low:
            add("❌", "Link/E-Mail", u, "nicht vom Nutzer genannt")
    if re.search(r"\blinked\s?in\b", low) and "linkedin" not in U.low and "linkedin" not in gemeldet:
        add("❌", "Link/E-Mail", "LinkedIn", "kein LinkedIn vom Nutzer")
    # Eigennamen – zeilenweise, nie über Zeilenumbrüche
    gesehen = set()
    for z in zeilen:
        for m in FIRMEN_RE.finditer(z):
            n = " ".join(m.groups())
            if n not in gesehen and not UA.hat_wort(m.group(1)):
                gesehen.add(n)
                add("❌", "Name/Firma", n, "nicht vom Nutzer genannt und nicht in der Anzeige")
        for m in AKRONYM_RE.finditer(z):
            w = m.group(1)
            if w.upper() in AKRONYM_OK or w in gesehen:
                continue
            gesehen.add(w)
            if w.isupper() and len(w) >= 5 and w.isalpha():
                # GROSS geschriebenes Wort („ALLGEMEINE HOCHSCHULREIFE“) ist kein Kürzel → wie ein Wort prüfen
                if norm(w) not in STANDARD and not UA.hat_wort(w.lower()) and len(w) >= 12:
                    add("⚠️", "Begriff", w, kontext(m, z))
                continue
            if not UA.hat_wort(w):
                add("❌", "Name/Begriff", w, kontext(m, z))
        satzzeile = bool(re.search(r"[.!?]\s*$", z.strip()))
        for m in re.finditer(r"(?:^[ \t]*|(?<=[^.!?:\s])[ \t]+|(?<=[,;])[ \t]*)((?:Frau|Herr|Dr\.)?[ \t]*[A-ZÄÖÜ][\wäöüß\-]+(?:[ \t]+[A-ZÄÖÜ][\wäöüß\-]+)+)", z):
            folge = m.group(1).strip()
            teile = folge.split()
            if teile[0] in ("Frau", "Herr", "Dr."):
                kand = teile[1:]
            else:
                if not z[:m.start(1)].strip() and satzzeile:
                    teile = teile[1:]          # Satzanfang ist kein Name
                # nach Artikel/Possessiv folgt ein normales Nomen („Ihr Haus“, „Ihre Praxis“, „Meine Cousine“)
                teile = [x for i, x in enumerate(teile) if not (i > 0 and DETERMINATIV_RE.match(teile[i - 1]))]
                kand = ist_eigenname_folge(teile)
            fehlt = [x for x in kand if not UA.hat_wort(x) and norm(x) not in gemeldet and not SL.gedeckt(x, K["QUA"])]
            if fehlt and folge not in gesehen:
                gesehen.add(folge)
                add("❌", "Name", folge, "nicht vom Nutzer/aus der Anzeige: " + ", ".join(fehlt))
    # Aufwertungen – nur gegen den Nutzer-Wortlaut (nicht die Anzeige)
    for a in AUFWERTUNG:
        for m in re.finditer(r"\b" + re.escape(a) + r"\w*", s, re.I):
            kl = klausel_bei(s, m.start())
            if U.hat_wort(m.group(0)[:len(a)]) or SL.gedeckt(m.group(0), K["QU"]):
                break     # v5: „eingelernt“ ↔ „einlernen“, „geführt“ ↔ „ich führe“
            if A_voll.hat_wort(m.group(0)) and not SL.ICH_RE.search(kl):
                break     # Titel/Funktion aus Anzeige/Einladung („Teamleitung“), keine Angabe über den Nutzer
            add("⚠️", "Aufwertung?", m.group(0), kontext(m, s) + " – hat der Nutzer das so gesagt?")
            break
    # lange Fachbegriffe
    for m in re.finditer(r"\b[A-ZÄÖÜ][a-zäöüß]{11,}\b", s):
        w = m.group(0)
        if norm(w) in STANDARD or w in gesehen or norm(w) in gemeldet:
            continue
        gesehen.add(w)
        if not UA.hat_wort(w) and not SL.gedeckt(w, K["QU"] if nur_nutzer else K["QUA"]):
            add("⚠️", "Begriff", w, kontext(m, s))
    # Firmenfakten ohne Zustimmung: nur wenn der Fakt wirklich im Text steht (Satz-Ebene,
    # ohne die Wörter aus Stelle/Firma – v2-Fehlalarm)
    weg = set(re.findall(r"[a-z0-9]{4,}", norm(" ".join([K["stelle"], K["firma"]]))))
    for f in offen:
        kern = [x for x in dict.fromkeys(re.findall(r"[a-z0-9]{5,}", norm(f))) if x not in weg]
        if len(kern) < 2:
            continue
        for satz in saetze(s):
            ns = norm(satz)
            treffer = sum(1 for k in kern if k[:max(5, len(k) - 2)] in ns)
            if treffer >= 2 and treffer / len(kern) >= 0.6:
                add("❌", "Firmenfakt", f, "aus der Recherche, aber der Nutzer hat nicht zugestimmt")
                break
    QU = K["QU"]
    # v5: Lebenslauf-Begriffe (Tätigkeiten, Fähigkeiten) gegen den Wortlaut – ⚠️, weil Stichpunkte frei formuliert sind
    if nur_nutzer and not spickzettel and name.endswith("(JSON)"):
        for z in zeilen:
            inhalt = z.split(":", 1)[1] if re.match(r"^\s*[\wÄÖÜäöüß /-]{2,30}:", z) else z
            fehl = [w for w in SL.woerter(inhalt) if not w[0].isdigit() and len(w) >= 3 and not SL.ist_frei(w)
                    and norm(w) not in STANDARD and norm(w) not in LL_WORTE and norm(w) not in SL.MONATE
                    and not SL.gedeckt(w, QU) and norm(w) not in gemeldet]
            if fehl:
                add("⚠️", "Lebenslauf-Begriff", ", ".join(dict.fromkeys(fehl)),
                    f"nicht im Wortlaut ⟵ „{z.strip()[:70]}“ – hat der Nutzer das so gesagt? Sonst seine Worte nehmen")
    # v5: Spickzettel – Kernbotschaften, Vorstellung, Antworten, Beispiele gegen den Wortlaut (nicht Fachfragen)
    if spickzettel:
        for z in spick_faktzeilen(t):
            fehl = [w for w in SL.woerter(z) if not w[0].isdigit() and len(w) >= 3 and not SL.ist_frei(w)
                    and norm(w) not in STANDARD and norm(w) not in SL.MONATE and not SL.gedeckt(w, QU)
                    and not A_voll.hat_wort(w) and norm(w) not in gemeldet]
            if fehl:
                add("❌", "Spickzettel-Wortlaut", ", ".join(dict.fromkeys(fehl)),
                    f"nicht vom Nutzer ⟵ „{z.strip()[:70]}“ – seine Worte nehmen oder fragen")
    # v5: Einschränkung des Nutzers („b manchmal“, „sap so bisschen“) darf nicht verloren gehen
    for antw, eingeschraenkt in K.get("einschraenkungen", []):
        for z in zeilen:
            if re.search(EINSCHRAENKUNG + r"|gelegentlich|teilweise|grundkenntnis|grundlagen|einige|bei bedarf", z, re.I):
                continue
            treffer = [w for w in eingeschraenkt if any(SL.lemma(x) == w or (len(w) >= 5 and SL.lemma(x).startswith(w))
                                                        for x in SL.woerter(z))]
            if len(treffer) >= max(1, min(2, len(eingeschraenkt))):
                add("⚠️", "Einschränkung weg?", z.strip()[:60], f"Nutzer sagte „{antw}“ – im Text ohne „manchmal/etwas“?")
                break
    return s


LL_WORTE = set(norm(w) for w in """heute laufend voraussichtlich abgebrochen abschluss ohne note noten schnitt durchschnitt
leistungskurs leistungskurse wahlfach fach fächer schwerpunkt schwerpunkte grundkurs klasse jahrgangsstufe sprachen edv
kenntnisse sonstiges zertifikate führerschein interessen hobbys ehrenamt ehrenamtlich minijob aushilfe praktikum
berufserfahrung schulbildung bildung ausbildung studium projekte projekt privat familienzeit elternzeit bewerbungsphase
weiterbildung weiterbildungen schulung schulungen woche wochen stunden std monate""".split())


def spick_faktzeilen(t):
    """Zeilen aus Kernbotschaften, Vorstellung, Antworten auf schwierige Fragen und Beispielen."""
    out, aktiv = [], False
    for z in (t or "").splitlines():
        if SPICK_KOPF.match(z) and (z.strip().isupper() or len(z.split()) <= 6):
            low = z.lower()
            aktiv = bool(re.match(r"\s*(deine 3 kernbotschaften|ihre 3 kernbotschaften|kernbotschaften|so stellst du dich vor|"
                                  r"so stellen sie sich vor|vorstellung|schwierige fragen|deine beispiele|ihre beispiele|beispiele)", low))
            continue
        if not aktiv or not z.strip() or z.strip().endswith("?") or "noch offen" in z:
            continue
        zz = re.sub(r"^\s*(→|antwort:|•|-|–|·)\s*", "", z.strip(), flags=re.I)
        zz = re.sub(r"^(?:[1-9][.)])\s+(?!" + textlib.ORDINAL_NOMEN + ")", "", zz)
        out.append(zz)
    return out


def einschraenkungen(d):
    """→ [(antwort_ausschnitt, [lemmata])] für Antworten mit „manchmal“, „bisschen“ … (inkl. gewählter Option)."""
    out = []
    for e in textlib.rohtext_eintraege(d):
        if e.get("sensibel"):
            continue
        for seg in re.split(r"[.;\n]|,(?!\d)", e["antwort"]):
            m = re.search(r"\b" + EINSCHRAENKUNG + r"\b", seg, re.I)
            if not m:
                continue
            ok = lambda w: len(w) >= 3 and not SL.ist_frei(w) and not re.fullmatch(EINSCHRAENKUNG, w, re.I) and w.lower() not in ("nur",)
            vorher = [w for w in SL.woerter(seg[:m.start()]) if ok(w)][-3:]
            woerter_seg = vorher or [w for w in SL.woerter(seg[m.end():]) if ok(w)][:2]
            buchst = re.findall(r"(?<![\wäöüß])([a-f])(?![\wäöüß])", seg[:m.start()].lower() or seg.lower())
            for k, v in (e.get("optionen") or {}).items():
                if str(k).lower() in buchst:
                    woerter_seg += [w for w in SL.woerter(str(v)) if len(w) >= 3 and not SL.ist_frei(w)]
            lem = list(dict.fromkeys(SL.lemma(w) for w in woerter_seg))
            if len(lem) >= 2:      # ein einzelnes Wort („sap so bisschen“) prüfen Niveau-/Kenntnis-Regeln
                out.append((seg.strip(), lem))
    return out


# ---------------------------------------------------------------- Texte aus der JSON
def json_texte(d):
    out = {}
    lv = d.get("lebenslauf") or {}
    if lv:
        teile = [lv.get("kurzprofil", "")]
        for ab in lv.get("abschnitte", []):
            for e in ab.get("eintraege", []):
                teile += [e.get("zeitraum", ""), e.get("titel", ""), e.get("ort", "")] + list(e.get("punkte", []))
        teile += [f'{k.get("label", "")}: {k.get("wert", "")}'.strip(": ") for k in lv.get("kenntnisse", [])] + [lv.get("interessen", "")]
        out["lebenslauf"] = [x for x in teile if x]
    an = d.get("anschreiben") or {}
    if an.get("absaetze"):
        out["anschreiben"] = [x for x in [an.get("betreff", ""), an.get("anrede", "")] + an["absaetze"] if x]
    if d.get("formular"):
        out["formular"] = [f.get("text", "") for f in d["formular"] if f.get("text")]
    em = d.get("email") or {}
    if em.get("text"):
        out["email"] = [x for x in (em.get("betreff", ""), em["text"]) if x]
    wa = d.get("whatsapp") or {}
    if wa.get("text"):
        out["whatsapp"] = [wa["text"]]
    return out


def alnum(s):
    return re.sub(r"[^a-z0-9äöüß]", "", (s or "").lower())


def abgleich(datei_text, texte, name, befunde):
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
                            "fehlt in der Datei: „" + re.sub(r"\s+", " ", e)[:80] + "“ – Datei neu erzeugen (alte Fassung?)"))
    return best


def ungenutzt(d, alle_texte, befunde):
    t = norm(" ".join(alle_texte))
    for b in (d.get("profil") or {}).get("beispiele") or []:
        roh = b.get("stichwort") or " ".join(str(b.get(k, "")) for k in ("situation", "handlung"))
        kern = [w for w in re.findall(r"[a-z0-9]{4,}", norm(roh)) if w not in STANDARD][:5]
        if kern and not any(k[:max(4, len(k) - 2)] in t for k in kern):
            befunde.append(("⚠️", "Profil", "Beispiel ungenutzt", b.get("stichwort") or b.get("thema") or roh[:40],
                            "gesammeltes Beispiel kommt in keiner Unterlage vor – einbauen oder bewusst weglassen"))
    for h in (d.get("profil") or {}).get("hobbys") or []:
        kern = re.findall(r"[a-z0-9]{4,}", norm(h))[:1]
        if kern and kern[0][:max(4, len(kern[0]) - 2)] not in t:
            befunde.append(("⚠️", "Profil", "Hobby ungenutzt", h, "nicht im Lebenslauf – absichtlich?"))


def aufmerksam_check(d, U, befunde):
    """Nur die QUELLE (Portal, Person, Messe …) muss im Nutzer-Wortlaut stehen – nicht jedes Wort."""
    wa = (d.get("profil") or {}).get("wie_aufmerksam") or ""
    for f in d.get("formular") or []:
        if "aufmerksam" not in (f.get("feld") or "").lower():
            continue
        t = PRUEFEN_RE.sub(" ", f.get("text") or "").strip().rstrip(".!")
        if not t:
            continue
        nt = norm(t)
        quellen = [q for q in QUELLEN if re.search(r"(?<![a-z])" + re.escape(norm(q)), nt)]
        woerter = [w.rstrip(".,;:!") for w in re.findall(r"[A-Za-zÄÖÜäöüß][\wäöüß.\-]*", t)]
        namen = [w for w in woerter[1:] if w[0].isupper() and norm(w) not in STANDARD
                 and not NOMEN_ENDUNG.search(w.lower()) and not any(norm(q) in norm(w) for q in quellen)]
        fehl = [q for q in quellen if not U.hat_wort(q)] + [n for n in namen if not U.hat_wort(n)]
        if not quellen and not namen:
            inhalt = [w for w in re.findall(r"[a-zäöüß]{4,}", t.lower()) if norm(w) not in STANDARD]
            if not any(U.hat_wort(w) for w in inhalt):
                fehl = ["keine erkennbare Quelle"]
        if not wa or fehl:
            befunde.append(("❌", "formular", "Wie aufmerksam?", t[:60],
                            "Quelle nicht vom Nutzer gesagt (" + (", ".join(fehl) if fehl else "profil.wie_aufmerksam leer")
                            + ") – immer fragen, nie raten"))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    anzeigen, quellen = [], []
    for flag, ziel in (("--anzeige", anzeigen), ("--quelle", quellen)):
        while flag in a:
            i = a.index(flag)
            ziel.append(a[i + 1])
            del a[i:i + 2]
    typ = None
    if "--typ" in a:
        i = a.index("--typ")
        typ = a[i + 1]
        del a[i:i + 2]
    kurz, woher = "--kurz" in a, "--woher" in a
    a = [x for x in a if x not in ("--kurz", "--woher")]
    try:
        d = textlib.lade_profil(a[0])
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(2)
    for x in anzeigen + quellen + a[1:]:
        if not os.path.isfile(x):
            print(f"FEHLER: Datei nicht gefunden: {x}")
            sys.exit(2)
    befunde = []
    U, A, UA, offen, legacy, zr_antw = korpus(d, anzeigen, quellen, befunde)
    z = d.get("ziel") or {}
    abgel = {}
    for e in textlib.rohtext_eintraege(d):
        if not e.get("sensibel"):
            abgel.update(SL.abgeleitete_jahre(e["antwort"]))
    luecken_monate = set()
    for l in (d.get("profil") or {}).get("luecken") or []:
        for mo, y in re.findall(r"\b(\d{1,2})\s*/\s*(\d{4})", str(l.get("zeitraum", ""))):
            luecken_monate.add((int(y), int(mo)))
    K = {"U": U, "A": A, "UA": UA, "offen": offen, "stelle": z.get("stelle", ""), "firma": z.get("firma", ""),
         "zr_antworten": zr_antw, "QU": SL.Quelle([U.text]), "QUA": SL.Quelle([UA.text]), "abgel": {y: a for y, a in abgel.items() if y not in U.jahre},
         "luecken_monate": luecken_monate, "einschraenkungen": [] if legacy else einschraenkungen(d)}
    alle, geprueft = [], []

    if typ == "spickzettel":
        if a[1:]:
            quellen_sp = []
            for x in a[1:]:
                txt = os.path.splitext(x)[0] + ".txt"
                if not x.lower().endswith(".txt") and os.path.isfile(txt):
                    x = txt    # die .txt hat dieselben Inhalte mit sauberen Zeilen
                quellen_sp.append((os.path.basename(x), textlib.read_any(x)))
        else:
            import akte
            quellen_sp = [("Spickzettel (JSON)", akte.spickzettel_text(d))]
        for name, t in quellen_sp:
            alle.append(t)
            pruefe_text(name, t, K, befunde, spickzettel=True)
    else:
        texte = json_texte(d)
        if not texte and not a[1:]:
            print("FEHLER: In der JSON stehen noch keine Unterlagen-Texte (lebenslauf/anschreiben/formular/email).")
            sys.exit(2)
        for sek, einheiten in texte.items():
            alle.append("\n".join(einheiten))
            pruefe_text(sek + " (JSON)", "\n".join(einheiten), K, befunde, nur_nutzer=(sek == "lebenslauf"))
            geprueft.append(sek)
            # v5: Unterlagen in Standarddeutsch – Umgangssprache, Chat-Kürzel, Tippfehler früh melden (vor der Freigabe)
            for msg, vorschlag in SL.stil_befunde("\n".join(einheiten[1:] if sek == "anschreiben" else einheiten),
                                                  referenz=[z.get("anzeige_text", "")], lebenslauf=(sek == "lebenslauf")):
                befunde.append(("⚠️", sek + " (JSON)", "Stil", msg, f"Standarddeutsch: {vorschlag}"))
        for aw in (d.get("meta") or {}).get("offene_aenderungen") or []:
            if isinstance(aw, dict) and not aw.get("erledigt"):
                befunde.append(("⚠️", "Änderungswunsch", "offen", aw.get("text", "")[:70],
                                "zugesagt, aber noch nicht abgehakt – in den Text einbauen, dann erledigt: true"))
        for datei in a[1:]:
            name = os.path.basename(datei)
            if name.lower().startswith(("bewerbungsakte", "gespraech_spickzettel", "spickzettel")):
                befunde.append(("ℹ️", name, "übersprungen", "Akte/Spickzettel",
                                "nicht Teil der Unterlagen-Prüfung (Spickzettel: --typ spickzettel)"))
                continue
            try:
                dt = textlib.read_any(datei)
            except RuntimeError as e:
                befunde.append(("❌", name, "Lesen", str(e), ""))
                continue
            if not dt.strip():
                befunde.append(("ℹ️", name, "kein Text", "Scan/Bild", "Anlage – nicht geprüft"))
                continue
            if texte:
                abgleich(dt, texte, name, befunde)
            tmp = []
            alle.append(dt)
            pruefe_text(name, dt, K, tmp, nur_nutzer=name.lower().startswith("lebenslauf"))
            schon = {(b[2], b[3]) for b in befunde}
            befunde += [b for b in tmp if (b[2], b[3]) not in schon]
        aufmerksam_check(d, U, befunde)
        ungenutzt(d, alle, befunde)
        # Satz-Herkunft (v4): jeder Satz über die Person ↔ Antwort-Nr. + wörtliches Zitat (herkunft.py)
        import herkunft
        hb, woher_z = herkunft.pruefe(d)
        for sym, teil, satz, meldung in hb:
            befunde.append((sym, "Herkunft", teil, "„" + herkunft.kurz(satz, 9) + "“", meldung))
        for e in textlib.unklare_antworten(d):
            befunde.append(("ℹ️", "Wortlaut", f"unsichere Antwort Nr. {e['nr']}", f"„{herkunft.kurz(e['antwort'], 8)}“",
                            "vor der Verwendung kurz mit Ja/Nein bestätigen lassen (dann rohtext geklaert: true)"))
        if woher:
            print("# Woher-Liste (für die Freigabe-Nachricht – kompakt zeigen)")
            for zl in herkunft.woher_liste(woher_z) or ["(keine Sätze mit Aussagen über die Person)"]:
                print(zl)
            print("---")
    rot = [b for b in befunde if b[0] == "❌"]
    gelb = [b for b in befunde if b[0] == "⚠️"]
    info = [b for b in befunde if b[0] == "ℹ️"]
    print("# Fakten-Check v5 – Fakten wörtlich, Formulierung frei. Belege: Wortlaut, Anzeige/Einladung, Uploads" + (" (LEGACY ohne rohtext)" if legacy else ""))
    for sym, wo, kat, was, ctx in rot + ([] if kurz else gelb + info):
        print(f"{sym} [{wo}] {kat}: {was}" + (f"  ⟶ {ctx}" if ctx else ""))
    n_pr = sum(len(PRUEFEN_RE.findall(x)) for x in alle)   # v3-Fehler: wurde nach dem Entfernen gezählt (immer 0)
    print("---")
    print(f"{len(rot)} ❌ ohne Beleg · {len(gelb)} ⚠️ prüfen · {n_pr} offene [PRÜFEN]")
    if not rot:
        print("✅ Keine unbelegten Fakten, jeder Satz über die Person hat eine Quelle. Woher-Liste in der Freigabe zeigen.")
    print("Bei ❌: Nutzer fragen (Antwort wörtlich in profil.rohtext) oder streichen. belege nur mit wörtlichem zitat.")
    sys.exit(1 if rot else 0)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
