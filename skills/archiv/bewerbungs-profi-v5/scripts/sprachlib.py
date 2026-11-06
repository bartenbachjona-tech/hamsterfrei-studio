#!/usr/bin/env python3
"""Sprach-Hilfen für v5 „Fakten wörtlich, Formulierung frei“ (von herkunft.py, fakten_check.py, endcheck.py genutzt).

- lemma(): einfache deutsche Stammform (Partizip II, trennbare Verben, starke Verben, Endungen)
- UMGANGSSPRACHE: Nutzerwort → Standardformen (red → reden, nix → nichts, ubahn → U-Bahn, sa/so → samstags/sonntags …)
- DECKT: gerichtete Synonyme (Nutzerwort deckt Standardwort: „leute“ → Kunden, „bescheid sagen“ → informieren)
- FREI: Funktions- und Stilwörter – dürfen ohne Quelle stehen. Alles andere ist ein Behauptungs-Baustein
  (Tätigkeit, Fähigkeit, Häufigkeit/Intensität, Gefühl/Motiv, Eigenname, Abschluss, Zahl, Kontakt zur Firma).
- Quelle + gedeckt(): Deckungsprüfung mit Lemma, Komposita-Teilwort, Zahlwörtern, Datums-Normalisierung und
  Tippfehler-Toleranz (Levenshtein ≤ 2 bei Wörtern ab 6 Zeichen).
- stil_befunde(): Umgangssprache, Chat-Kürzel, Tippfehler, „Sa und So“, doppelte Wörter → ⚠️ mit Vorschlag.

    python3 sprachlib.py "Text"   → Stil-Befunde + Lemmata (zum Ausprobieren)
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

HEUTE = datetime.date.today()


def n(w):
    return textlib.translit((w or "").lower())


# ---------------------------------------------------------------- Umgangssprache → Standard (≥ 60 Einträge)
UMGANGSSPRACHE = {
    "red": ["rede", "reden"], "seh": ["sehe", "sehen"], "find": ["finde", "finden"], "hab": ["habe", "haben"],
    "habs": ["habe es"], "mach": ["mache", "machen"], "mach's": ["mache es"], "geh": ["gehe", "gehen"],
    "komm": ["komme", "kommen"], "sag": ["sage", "sagen"], "frag": ["frage", "fragen"], "prüf": ["prüfe", "prüfen"],
    "stopp": ["stoppe", "stoppen"], "erklär": ["erkläre", "erklären"], "arbeit": ["arbeite"], "kann's": ["kann es"],
    "nix": ["nichts"], "nüscht": ["nichts"], "nich": ["nicht"], "net": ["nicht"], "ned": ["nicht"], "is": ["ist"],
    "isses": ["ist es"], "gings": ["ging es"], "garnich": ["gar nicht"], "garnicht": ["gar nicht"], "wollt": ["wollte"],
    "was": ["etwas"], "ne": ["eine"], "nen": ["einen"], "nem": ["einem"], "ner": ["einer"], "grad": ["gerade"],
    "bissl": ["etwas", "ein wenig"], "bissel": ["etwas", "ein wenig"], "bisschen": ["etwas", "ein wenig"],
    "bisserl": ["etwas"], "mega": ["sehr"], "voll": ["sehr"], "total": ["sehr", "völlig"], "krass": ["sehr"],
    "echt": ["wirklich", "sehr"], "richtig": ["sehr"], "cool": ["gern", "gut"], "toll": ["gern", "gut"],
    "super": ["gern", "sehr gut"], "geil": ["gern", "gut"], "nice": ["gut"], "okay": ["in ordnung"], "ok": ["in ordnung"],
    "jo": ["ja"], "jap": ["ja"], "jep": ["ja"], "nö": ["nein"], "nee": ["nein"], "vlt": ["vielleicht"],
    "vllt": ["vielleicht"], "evtl": ["eventuell"], "zb": ["zum beispiel"], "kumpel": ["freund", "bekannter"],
    "kumpels": ["freunde", "bekannte"], "kids": ["kinder"], "papa": ["vater"], "mama": ["mutter"], "chef": ["vorgesetzter"],
    "chefin": ["vorgesetzte"], "azubi": ["auszubildende", "auszubildender"], "azubis": ["auszubildende"],
    "kfz": ["kraftfahrzeug", "kfz-"], "ubahn": ["u-bahn"], "sbahn": ["s-bahn"], "tram": ["straßenbahn"],
    "selber": ["selbst"], "nochmal": ["noch einmal"], "nochma": ["noch einmal"], "mal": ["einmal"], "raus": ["heraus", "hinaus"],
    "rein": ["herein", "hinein"], "rüber": ["herüber", "hinüber"], "runter": ["herunter", "hinunter"], "rum": ["herum"],
    "drauf": ["darauf"], "drin": ["darin"], "drüber": ["darüber"], "dran": ["daran"], "sauer": ["verärgert", "wütend"],
    "schaffen": ["arbeiten"], "jobben": ["arbeiten"], "job": ["stelle", "tätigkeit", "arbeit"], "checken": ["verstehen", "prüfen"],
    "kapiert": ["verstanden"], "quatschen": ["sprechen", "reden"], "frühstens": ["frühestens"], "spätstens": ["spätestens"],
    "kommisioniert": ["kommissioniert"], "kommisionieren": ["kommissionieren"], "letztes": ["vergangenes"],
    "dauernd": ["ständig"], "eh": ["ohnehin"], "halt": [], "ziemlich": ["recht"], "bestimmt": ["sicher"],
    "mo": ["montag", "montags"], "di": ["dienstag", "dienstags"], "mi": ["mittwoch", "mittwochs"],
    "do": ["donnerstag", "donnerstags"], "fr": ["freitag", "freitags"], "sa": ["samstag", "samstags", "wochenende"],
    "so": ["sonntag", "sonntags", "wochenende"], "we": ["wochenende"], "wochenende": ["samstags", "sonntags"],
    "lkw": ["lastkraftwagen", "lkw"], "lkws": ["lkw", "lastkraftwagen"], "pkw": ["personenkraftwagen", "pkw"],
}
# Wochentag-Kürzel nur in eindeutigen Mustern („sa und so“, „mo-fr“) ersetzen – „so“ ist sonst ein normales Wort
_TAGE = {"mo": "montag", "di": "dienstag", "mi": "mittwoch", "do": "donnerstag", "fr": "freitag", "sa": "samstag", "so": "sonntag"}
TAG_MUSTER = re.compile(r"(?<![a-zäöüß])(mo|di|mi|do|fr|sa|so)\.?\s*(und|&|,|/|-|–|bis)\s*(mo|di|mi|do|fr|sa|so)\.?(?![a-zäöüß])", re.I)
NUR_IM_TAGMUSTER = {"mo", "di", "mi", "do", "fr", "sa", "so", "was", "rein", "mal", "richtig", "echt", "voll", "total", "ne",
                    "halt", "is", "job", "schaffen", "bestimmt", "ziemlich", "letztes", "eh"}

# ---------------------------------------------------------------- gerichtete Synonyme: Nutzerwort deckt Standardwort
# Schlüssel und Werte als Lemma-Anfänge. Nur Gleichbedeutendes / neutrale Umschreibung – keine Aufwertung.
_DECKT_ROH = {
    "leute": "kunden kundin kundschaft menschen personen gaeste mitarbeiter mitarbeitende kollegen kollegin patienten",
    "kunde": "kundschaft kundin", "patient": "patientin", "kollege": "kollegin", "kumpel": "freund bekannt",
    "chef": "vorgesetzt inhaber", "chefin": "vorgesetzt inhaberin", "mann": "kunde herr anrufer", "frau": "kundin dame",
    "mach": "erstell erledig durchfuehr anfertig absolvier uebernehm vorbereit fertigstell",
    "fertigmach": "vorbereit fertigstell", "mitmach": "mitwirk beteilig", "sag": "erzaehl bericht mitteil informier meld",
    "bescheid": "informier meld benachrichtig", "seh": "erleb beobacht bemerk mitbekomm erkenn feststell",
    "schau": "seh nachseh", "nachschau": "nachseh", "find": "entdeck feststell bemerk", "gefund": "entdeck feststell",
    "merk": "bemerk feststell erkenn", "komm": "gelang ankomm eintreff", "zahl": "bezahl", "telefonier": "anruf telefon",
    "cool": "gern spass freude gefall interess spannend ansprech reiz mag", "toll": "gern spass freude gefall interess spannend ansprech",
    "super": "gern spass freude gefall interess spannend", "mega": "sehr", "geil": "gern spass gefall",
    "gern": "gern spass freude gefall mag", "spass": "gern freude gefall", "freude": "gern spass gefall",
    "mag": "gern gefall", "spannend": "interess ansprech reiz gern", "interess": "spannend ansprech reiz",
    "ansprech": "interess reiz", "sauer": "veraerger wuetend aufgebracht", "manchmal": "gelegentlich teilweise",
    "bisschen": "etwas wenig grundlag", "einlern": "einarbeit anlern", "anlern": "einarbeit einlern", "einarbeit": "einlern anlern",
    "verraeum": "einraeum einsortier", "frag": "beantwort auskunft", "kundenfrag": "beantwort auskunft",
    "erklaer": "erlaeuter", "stopp": "anhalt", "raus": "heraus hinaus verlass wechsel", "weg": "wechsel",
    "geholf": "unterstuetz mitgeholf", "helf": "unterstuetz", "abgebroch": "beend", "kenn": "auskenn vertraut",
    "nah": "naehe erreichbar", "naehe": "nah", "frueh": "fruehschicht morgen", "studier": "studium", "studium": "studier",
    "bwl": "betriebswirt", "verdien": "verdienst", "pack": "verpack", "kasse": "kassier", "gepackt": "verpack",
    "schicht": "schichtarbeit schichtbetrieb", "ware": "waren artikel", "lieferung": "liefer", "nochmal": "erneut",
    "erst": "zunaechst", "letzt": "zuletzt vergang", "vorschrift": "vorgab regel", "fehl": "fehler",
}

# ---------------------------------------------------------------- frei: Funktions- und Stilwörter
FREI = set(n(w) for w in """
ich mich mir mein meine meinen meinem meiner meines wir uns unser unsere unseren unserem unserer du dich dir dein deine
deinen deinem deiner sie ihnen ihr ihre ihrem ihren ihrer ihres es er ihm ihn sein seine seinen seinem seiner man
der die das den dem des ein eine einen einem einer eines kein keine keinen keinem keiner dies diese dieser dieses diesem
diesen jene jener welche welcher welches welchen was wer wen wem wie wo wann warum wobei wofür womit woran wodurch
in im am an auf aus bei beim mit nach seit von vom zu zum zur für über unter vor vorm durch gegen ohne um bis ab als
neben während innerhalb außerhalb per pro je laut gemäß samt sowie mithilfe hilfe statt anstatt trotz wegen dank
und oder aber denn weil dass da wenn ob sodass damit dabei dann noch schon jetzt heute derzeit aktuell zurzeit nun
bereits zudem außerdem darum deshalb daher deswegen so hier dafür dazu davon darin darauf daran dort dorthin auch nur
erst zuerst zunächst danach davor seitdem dadurch somit also zwar sondern sowohl weder nicht nichts etwas viel mehr
zuletzt später früher damals inzwischen mittlerweile wieder zurück einmal insgesamt gleichzeitig zugleich ebenfalls
ebenso jeweils bisher stattdessen trotzdem allerdings jedoch eben gerade nämlich sogar überhaupt bzw beziehungsweise
etwa rund circa ca zirka weiterhin hin her hinaus heraus herein hinein dahin daher wie weise art beispiel beispielsweise
bin bist ist sind war warst waren gewesen sein habe hast hat haben hatte hatten hätte hätten werde wirst wird werden
wurde wurden worden würde würden kann kannst können konnte konnten möchte möchten möchtest will willst wollen wollte
soll sollte sollten solle darf dürfen muss müssen musste lasse lassen ließ gelassen
mache machst macht machen gemacht tue tun tat getan arbeite arbeitest arbeitet arbeiten arbeitete gearbeitet tätig
gebe gibt geben gab gegeben liege liegt liegen lag gelegen gehe geht gehen ging gegangen komme kommt kommen kam gekommen
stehe steht stehen stand gestanden bleibe bleibt bleiben blieb geblieben heiße heißt heißen hieß nenne nennt nennen
nannte genannt suche sucht suchen bietet bieten bieten bietest biete angeboten erwarten erwartet wünschen wünscht
wünsche schreiben schreibt beschreiben beschrieben finden finde findet gefunden fand sehen sieht nutze nutzt nutzen
genutzt verwende verwenden verwendet umgehen spricht sprechen für dafür arbeit arbeits anbieten anbietet angeboten
bietet erreichen erreiche erreichbar erreicht entfernt gelegen
bewerbe bewerben bewirbt beworben bewerbung bewerbungen unterlagen lebenslauf anschreiben motivationsschreiben
zeugnis zeugnisse anhang anlage anlagen pdf datei mail e-mail email telefon telefonnummer handy rückfragen rückfrage
anbei sende sendet senden schicke schicken schickt beigefügt
stelle stellen anzeige stellenanzeige ausschreibung ausbildung ausbildungsplatz ausbildungsjahr studium studiere
studiert studieren praktikum praktikumsplatz pflichtpraktikum praxissemester semester job tätigkeit tätigkeiten
gespräch gespräche vorstellungsgespräch persönliches persönlichen persönlich kennenzulernen rückmeldung einladung
herr herrn frau damen herren freue freuen freut darauf darüber anfangen anfange beginnen beginne starten starte start
absolvieren absolviere absolviert erworben erwerben abschluss besuche besucht besuchen teilnehmen teilgenommen
jahr jahre jahren jahres monat monate monaten monats woche wochen tag tage tagen stunde stunden uhr minute minuten
std eur euro brutto netto jahresgehalt gehaltsvorstellung gehalt vollzeit teilzeit wochenstunden pro
betrieb betriebs unternehmen unternehmens firma firmen haus team teams standort standorte filiale bereich bereiche
abteilung aufgabe aufgaben vorgang fall sache anliegen thema themen weg wege frage fragen ziel grund gründe
karriereseite webseite website internetseite homepage seite
erfahrung erfahrungen alltag praxis zeit ende anfang beginn rahmen möglichkeit chance richtung schritt
mehrere einige andere anderen anderer weitere weiteren erste ersten zweite zweiten dritte letzte letzten nächste
nächsten neue neuen neuer eigene eigenen eigener ganze ganzen ganz gesamte gesamten verschiedene verschiedenen
somit genauso folgende folgenden jedoch also geehrte geehrter hallo guten freundlichen grüßen grüße gruß viele vielen
""".split())
FREI_LEMMA = set()   # wird unten gefüllt: leichte Verben in jeder Form frei (bieten, liegen, geben, gehen, kommen, stehen …)
# Bewusst NICHT frei (Behauptungs-Bausteine): gern, gut, sehr, schnell, immer, oft, täglich, regelmäßig, jeden,
# selbstständig, zuverlässig, sorgfältig, spricht … an, begeistert, Spaß, Freude, kennengelernt, gelernt …
SIE_RE = re.compile(r"\b(Sie|Ihnen|Ihr|Ihre|Ihrem|Ihren|Ihrer|Ihres|euch|eure|euer|Anzeige|Stellenanzeige|Karriereseite|"
                    r"Ausschreibung|Website|Webseite)\b")
ICH_RE = re.compile(r"\b(ich|mich|mir|mein\w*|wir|uns|unser\w*)\b", re.I)

# Partizip-ähnliche Nomen, die nicht als „ge-“-Partizip zerlegt werden dürfen
GE_NOMEN = set(n(w) for w in "gehalt gebiet gesicht geschäft gericht gewicht gesundheit gesetz gelände gerät geräte "
               "gemüse getränk getränke gepäck gebäude geschichte gefahr gefühl gedanke geduld gelegenheit gemeinde "
               "geselle gesellen gesellenbrief generation genau gerne gesamt geschwister gewinn gewerbe".split())
SEP = ("zurueck", "weiter", "heraus", "hinaus", "herein", "hinein", "kennen", "fertig", "durch", "nach", "fest", "frei",
       "voll", "wieder", "weg", "aus", "ein", "auf", "mit", "vor", "ab", "an", "zu", "um", "hin", "her", "los", "nach")
HARMLOSE_PARTIKEL = ("weiter", "mit", "nach", "hin", "her", "an", "zurueck", "wieder")
STARK = {  # Präteritum/Partizip starker Verben → Stamm des Infinitivs
    "rief": "ruf", "riefen": "ruf", "ging": "geh", "gingen": "geh", "kam": "komm", "kamen": "komm", "sah": "seh",
    "sahen": "seh", "fand": "find", "fanden": "find", "half": "helf", "geholfen": "helf", "sprach": "sprech",
    "gesprochen": "sprech", "nahm": "nehm", "genommen": "nehm", "gab": "geb", "lief": "lauf", "liefen": "lauf",
    "schrieb": "schreib", "geschrieben": "schreib", "trug": "trag", "getragen": "trag", "hielt": "halt", "blieb": "bleib",
    "stand": "steh", "wusste": "wiss", "wussten": "wiss", "gewusst": "wiss", "brachte": "bring", "gebracht": "bring",
    "dachte": "denk", "gedacht": "denk", "tat": "tu", "getan": "tu", "bat": "bitt", "gebeten": "bitt", "las": "les",
    "gelesen": "les", "lag": "lieg", "stieg": "steig", "zog": "zieh", "gezogen": "zieh", "fuhr": "fahr",
    "gefahren": "fahr", "fiel": "fall", "ließ": "lass", "liess": "lass", "begann": "beginn",
    "begonnen": "beginn", "verstand": "versteh", "verstanden": "versteh", "bekam": "bekomm", "bekommen": "bekomm",
    "gefunden": "find", "gesehen": "seh", "gekommen": "komm", "gegangen": "geh", "gerufen": "ruf", "angerufen": "anruf",
    "rief_an": "anruf", "gewesen": "sein", "kannte": "kenn", "gekannt": "kenn", "nannte": "nenn", "genannt": "nenn",
    "gesungen": "sing", "geworfen": "werf", "warf": "werf", "hob": "heb", "gehoben": "heb", "wuchs": "wachs",
    "gegeben": "geb", "geblieben": "bleib", "gestanden": "steh", "getroffen": "treff", "traf": "treff", "geworden": "werd",
    "gewonnen": "gewinn", "gelegen": "lieg", "gesessen": "sitz", "saß": "sitz", "gelaufen": "lauf", "geschlossen": "schließ",
    "geschloss": "schließ", "gestiegen": "steig", "geschnitten": "schneid", "gebacken": "back", "geschienen": "schein",
    "gestorben": "sterb", "gewaschen": "wasch", "gefangen": "fang", "gehalten": "halt",
    "abgeschlossen": "abschließ", "angefangen": "anfang", "aufgenommen": "aufnehm", "teilgenommen": "teilnehm",
    "unternommen": "unternehm", "mitgenommen": "mitnehm", "angeboten": "anbiet", "geboten": "biet", "verboten": "verbiet",
}
ZAHLWORT = {"null": 0, "ein": 1, "eins": 1, "eine": 1, "einen": 1, "einem": 1, "einer": 1, "zwei": 2, "drei": 3, "vier": 4,
            "fuenf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11, "zwoelf": 12, "dreizehn": 13,
            "vierzehn": 14, "fuenfzehn": 15, "sechzehn": 16, "siebzehn": 17, "achtzehn": 18, "neunzehn": 19, "zwanzig": 20,
            "dreissig": 30, "vierzig": 40, "fuenfzig": 50, "hundert": 100, "tausend": 1000, "dutzend": 12,
            "erste": 1, "erster": 1, "ersten": 1, "erstes": 1, "zweite": 2, "zweiten": 2, "zweiter": 2, "dritte": 3,
            "dritten": 3, "vierte": 4, "vierten": 4, "fuenfte": 5, "fuenften": 5, "sechste": 6, "sechsten": 6,
            "siebte": 7, "siebten": 7, "achte": 8, "achten": 8, "neunte": 9, "neunten": 9, "zehnte": 10, "zehnten": 10,
            "elfte": 11, "elften": 11, "zwoelfte": 12, "zwoelften": 12, "dreizehnte": 13, "dreizehnten": 13,
            "beide": 2, "beiden": 2, "zweimal": 2, "dreimal": 3, "anderthalb": 1.5, "eineinhalb": 1.5, "zweieinhalb": 2.5,
            "halb": 0.5, "halbes": 0.5, "halben": 0.5}
ZAHLWORT_IMMER_ZAHL = {k for k in ZAHLWORT if k not in ("ein", "eine", "einen", "einem", "einer", "erste", "erster",
                                                        "ersten", "erstes", "beide", "beiden")}
MONATE = {n(k): v for k, v in textlib.MONATE_NORM.items() if len(k) >= 3}
WOCHENTAGE = {"montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"}


def lemma(w):
    """Einfache Stammform: translit, klein, Umgangssprache, starke Verben, Partizip II (auch trennbar), Endungen."""
    w = n(w).strip("-'’")
    if w in STARK:
        return STARK[w]
    if len(w) > 5 and w not in GE_NOMEN:
        for p in SEP:   # trennbares Partizip: ein-ge-arbeitet → einarbeitet
            if w.startswith(p + "ge") and len(w) - len(p) - 2 >= 3 and re.search(r"(t|et|en|n)$", w):
                rest = w[len(p) + 2:]
                w = p + STARK.get("ge" + rest, rest)
                break
        else:
            if w.startswith("ge") and len(w) >= 6 and re.search(r"(t|et)$", w):
                w = w[2:]          # ge-arbeitet, ge-öffnet (starke Partizipien stehen in STARK)
    for suf in ("ungen", "ung", "heiten", "heit", "keiten", "keit", "erinnen", "innen", "ieren", "ierte", "iert",
                "eten", "etet", "ete", "ern", "enden", "ende", "end", "est", "en", "er", "es", "em", "et", "st", "t", "e",
                "n", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)]
    return w


def lemma_varianten(w):
    """Lemma + Variante ohne „ge“-Zerlegung (gestaltet/gestalten, gehört/gehören, gefallen)."""
    v = {lemma(w)}
    x = n(w).strip("-'’")
    if x.startswith("ge") and x not in STARK:
        for suf in ("ten", "tet", "en", "et", "t", "e", "n"):
            if x.endswith(suf) and len(x) - len(suf) >= 4:
                v.add(x[:-len(suf)])
                break
    return v


def levenshtein(a, b, grenze=3):
    if abs(len(a) - len(b)) > grenze:
        return grenze + 1
    vor = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        akt = [i]
        for j, cb in enumerate(b, 1):
            akt.append(min(vor[j] + 1, akt[j - 1] + 1, vor[j - 1] + (ca != cb)))
        if min(akt) > grenze:
            return grenze + 1
        vor = akt
    return vor[-1]


def _deckt_tabelle():
    t = {}
    for k, v in _DECKT_ROH.items():
        t.setdefault(lemma(k), set()).update(lemma(x) for x in v.split())
    return t


DECKT = _deckt_tabelle()
FREI_LEMMA.update(lemma(w) for w in "bieten anbieten liegen geben gehen kommen stehen machen tun arbeiten nutzen verwenden "
                  "bleiben heißen nennen erreichen beginnen anfangen starten absolvieren besuchen bewerben schicken senden".split())
WORT_RE = re.compile(r"[A-Za-zÄÖÜäöüßÀ-ɏ]+(?:[-'’][A-Za-zÄÖÜäöüßÀ-ɏ]+)*|\d+(?:[.,]\d+)*")


def woerter(text):
    return WORT_RE.findall(text or "")


def standardisiere(text):
    """Nutzertext → Original + Standardformen (Umgangssprache, Wochentag-Kürzel, Bindestrich-Varianten)."""
    low = (text or "").lower()
    extra = []
    for m in TAG_MUSTER.finditer(low):
        a, b = m.group(1).lower(), m.group(3).lower()
        extra += [_TAGE[a], _TAGE[a] + "s", _TAGE[b], _TAGE[b] + "s", "bis"]
        if {a, b} == {"sa", "so"}:
            extra += ["wochenende"]
    for w in set(re.findall(r"[a-zäöüß']+", low)):
        if w in UMGANGSSPRACHE and w not in NUR_IM_TAGMUSTER:
            extra += UMGANGSSPRACHE[w]
    for w in set(re.findall(r"[a-zäöüß]+(?:-[a-zäöüß]+)+", low)):
        extra.append(w.replace("-", ""))          # u-bahn ↔ ubahn, kfz-mechatroniker ↔ kfzmechatroniker
        extra += w.split("-")
    return text + ("\n" + " ".join(extra) if extra else "")


# ---------------------------------------------------------------- relative Zeitangaben („letztes Frühjahr“)
def abgeleitete_jahre(text, heute=None):
    """→ {jahr: ausdruck} aus „letztes Jahr“, „letzten Sommer“, „dieses Jahr“, „vor zwei Jahren“ … (nur ⚠️-Basis)."""
    h = heute or HEUTE
    low = n(text)
    out = {}
    for m in re.finditer(r"\b(letzte[snm]?|vergangene[snm]?|vorige[snm]?)\s+jahr", low):
        out[h.year - 1] = m.group(0)
    for m in re.finditer(r"\b(dieses|diesem|heuer)\s*(jahr)?\b", low):
        if m.group(1) == "heuer" or m.group(2):
            out[h.year] = m.group(0)
    for m in re.finditer(r"\b(naechste[snm]?|kommende[snm]?)\s+jahr", low):
        out[h.year + 1] = m.group(0)
    jz = {"fruehling": 4, "fruehjahr": 4, "sommer": 7, "herbst": 10, "winter": 1}
    for m in re.finditer(r"\b(letzte[snm]?|vergangene[snm]?|vorige[snm]?|diese[snm]?)\s+(fruehling|fruehjahr|sommer|herbst|winter)", low):
        mon = jz[m.group(2)]
        if m.group(1).startswith("dies"):
            out[h.year] = m.group(0)
        else:
            out[h.year if mon < h.month else h.year - 1] = m.group(0)
            if m.group(2) == "winter":
                out[h.year - 1] = m.group(0)
    for m in re.finditer(r"\bvor\s+(\w+)\s+jahren?\b", low):
        z = ZAHLWORT.get(m.group(1)) if not m.group(1).isdigit() else int(m.group(1))
        if isinstance(z, (int, float)) and z >= 1:
            out[h.year - int(z)] = m.group(0)
    return out


# ---------------------------------------------------------------- Quelle (Belegtexte eines Satzes)
class Quelle:
    def __init__(self, texte, abgeleitet=None):
        roh = "\n".join(standardisiere(textlib.normalisiere_nutzertext(t)) for t in texte if t)
        self.text = roh
        ws = [n(w) for w in woerter(roh) if not w[0].isdigit()]
        self.roh = set(ws)
        self.ohne_bindestrich = {w.replace("-", "") for w in self.roh}
        for w in list(self.roh):
            if "-" in w:
                self.roh.update(w.split("-"))
        self.lemmata = {v for w in self.roh if len(w) >= 2 for v in lemma_varianten(w)}
        self.deckt = set()
        for le in self.lemmata:
            for k, v in DECKT.items():
                if le == k or (len(k) >= 4 and le.startswith(k)):
                    self.deckt |= v
        self.zahlen, self.monate = set(), set()
        low = n(roh)
        for m in re.finditer(r"\d+(?:[.,]\d+)*", low):
            z = m.group(0)
            self.zahlen.add(z.replace(".", "").replace(",", "."))
            for teil in re.split(r"[.,/]", z):
                if teil:
                    self.zahlen.add(str(int(teil)))
        for m in re.finditer(r"\b(\d{1,2})\s*[/.]\s*(\d{2,4})\b", low):
            if 1 <= int(m.group(1)) <= 12:
                self.monate.add(int(m.group(1)))
                y = int(m.group(2))
                self.zahlen.add(str(y + 2000 if y < 100 else y))
        for m in re.finditer(r"\b(\d{1,2})\.(\d{1,2})\.(\d{2,4})?", low):
            if 1 <= int(m.group(2)) <= 12:
                self.monate.add(int(m.group(2)))
            if m.group(3):
                y = int(m.group(3))
                self.zahlen.add(str(y + 2000 if y < 100 else y))
        for w in self.roh:
            if w in MONATE:
                self.monate.add(MONATE[w])
            if w in ZAHLWORT and w in ZAHLWORT_IMMER_ZAHL:
                v = ZAHLWORT[w]
                self.zahlen.add(str(int(v)) if float(v).is_integer() else str(v))
        for m in re.finditer(r"\b(" + "|".join(sorted(MONATE, key=len, reverse=True)) + r")\.?\s+'?(\d{2})\b", low):
            self.zahlen.add(str(2000 + int(m.group(2))))
        self.abgeleitet = {str(j): a for j, a in (abgeleitet or {}).items()}
        self.verteil = bool(re.search(r"\b(montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag|morgen|abend|nacht|"
                                      r"mittag|woche|stunde|monat|jahr|tag)s\b|taeglich|woechentlich|jede[nrsm]?\b", low))


def ist_frei(w):
    return n(w) in FREI


def gedeckt(w, Q):
    """Ist das Satzwort w durch die Quelle Q gedeckt? (Lemma, Synonym, Kompositum, Tippfehler)"""
    wt = n(w)
    if wt in Q.roh or wt.replace("-", "") in Q.ohne_bindestrich:
        return True
    if "-" in wt:
        return all(gedeckt(t, Q) or ist_frei(t) or len(t) < 3 or (ist_zahlwort(t) and zahl_gedeckt(t, Q) == "ja")
                   for t in wt.split("-") if t)
    if wt in ("jeden", "jede", "jedes", "jedem", "jeder") and Q.verteil:
        return True
    varianten = lemma_varianten(wt)
    if varianten & Q.lemmata or varianten & Q.deckt or varianten & FREI_LEMMA:
        return True
    s = lemma(wt)
    for q in Q.lemmata:
        if len(s) >= 4 and len(q) >= len(s) + 3 and q.endswith(s):
            return True       # Kompositum-Kopf: „Schichtleitung“ deckt „leiten/geleitet“, „Krankenkassen“ deckt „Kasse“
        k = min(len(s), len(q))
        if k >= 4 and (s.startswith(q) or q.startswith(s)) and abs(len(s) - len(q)) <= max(3, k // 2):
            return True
        if k >= 6 and _gemeinsam(s, q) >= 6:
            return True       # kommuniziert ↔ Kommunikation, abgewickelt ↔ Abwicklung
        if len(s) >= 4 and any(q.startswith(p) and q[len(p):].startswith(s) for p in SEP):
            return True       # „bildet“ ↔ „ausbilden“, „rief … an“ ↔ „angerufen“
    for p in SEP:                 # „ausbilden“ ↔ „bildet … aus“ (Partikel steht getrennt in der Quelle)
        if s.startswith(p) and len(s) - len(p) >= 3 and p in Q.roh and gedeckt(s[len(p):], Q):
            return True
    for p in HARMLOSE_PARTIKEL:   # weiter-gegeben ↔ gegeben, mit-geholfen ↔ geholfen
        if s.startswith(p) and len(s) - len(p) >= 3 and (s[len(p):] in Q.lemmata):
            return True
    for d in Q.deckt:
        if len(d) >= 4 and s.startswith(d):
            return True
    if len(wt) >= 5 and any(wt in r for r in Q.roh if len(r) > len(wt)):
        return True           # „Lager“ steckt in „Reifenlager“
    if len(wt) >= 8:          # Kompositum aus Quell- und Stilwörtern („Schichtarbeit“, „Kassenabrechnung“)
        bedeckt = [False] * len(wt)
        for r in list(Q.roh) + [x for x in FREI if len(x) >= 4]:
            if len(r) >= 4:
                for m in re.finditer(re.escape(r[:max(4, len(r) - 2)]), wt):
                    for i in range(m.start(), min(len(wt), m.start() + len(r))):
                        bedeckt[i] = True
        if sum(bedeckt) / len(wt) >= 0.8 and any(r in wt for r in Q.roh if len(r) >= 4):
            return True
    if len(wt) >= 6 and wt not in MONATE and wt not in ZAHLWORT and lemma(wt) not in WOCHENTAGE:
        for r in Q.roh:       # Tippfehler-Toleranz (Nutzer „kommisioniert“ ↔ „kommissioniert“)
            if len(r) >= 6 and r[0] == wt[0] and r not in MONATE and levenshtein(wt, r, 2) <= 2:
                return True
    return False


def _gemeinsam(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i


def zahl_gedeckt(tok, Q):
    t = n(tok)
    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{2,4})?", t)
    if m:                     # Datum „01.09.2027“ ↔ „1.9.27“, „1. September 2027“, bestätigt „01.09.2027“
        teile = [str(int(m.group(1))), str(int(m.group(2)))] + ([str(int(m.group(3)) + (2000 if int(m.group(3)) < 100 else 0))]
                                                              if m.group(3) else [])
        ok = all(x in Q.zahlen for x in teile) and int(m.group(2)) in Q.monate
        return "ja" if ok else "nein"
    if t in ZAHLWORT:
        v = ZAHLWORT[t]
        t = str(int(v)) if float(v).is_integer() else str(v)
    t = t.replace(".", "").replace(",", ".") if re.fullmatch(r"\d{1,3}(\.\d{3})+", t) else t.replace(",", ".")
    try:
        kand = {t, str(int(float(t)))}
    except ValueError:
        kand = {t}
    if kand & Q.zahlen:
        return "ja"
    if kand & set(Q.abgeleitet):
        return "abgeleitet"
    return "nein"


def ist_zahlwort(tok):
    return n(tok) in ZAHLWORT_IMMER_ZAHL or (n(tok) in ZAHLWORT and re.match(r"(erste|zweite|dritte)", n(tok)) is None
                                             and n(tok) not in ("ein", "eine", "einen", "einem", "einer", "beide", "beiden"))


# ---------------------------------------------------------------- Stil-Check (endcheck, fakten_check)
STIL_UMGANG = {   # Wort in Unterlagen → Vorschlag
    "nix": "nichts", "nich": "nicht", "net": "nicht", "is": "ist", "hab": "habe", "mach": "mache", "red": "rede",
    "seh": "sehe", "find": "finde", "sag": "sage", "geh": "gehe", "komm": "komme", "kumpel": "Freund/Bekannter",
    "mega": "sehr", "cool": "gut/interessant", "geil": "sehr gut", "krass": "sehr", "bissl": "etwas", "bissel": "etwas",
    "bisschen": "etwas", "garnich": "gar nicht", "garnicht": "gar nicht", "gings": "ging es", "ne": "eine", "nen": "einen",
    "nem": "einem", "grad": "gerade", "halt": "(streichen)", "eh": "(streichen)", "kids": "Kinder", "papa": "Vater",
    "mama": "Mutter", "azubi": "Auszubildende(r)", "azubis": "Auszubildende",
    "ubahn": "U-Bahn", "sbahn": "S-Bahn", "selber": "selbst", "nochmal": "noch einmal", "jo": "ja", "nö": "nein",
    "nee": "nein", "okay": "in Ordnung", "ok": "in Ordnung", "frühstens": "frühestens", "kommisioniert": "kommissioniert",
    "sauer": "verärgert", "jobben": "arbeiten", "quatschen": "sprechen", "checken": "verstehen/prüfen",
    "kapiert": "verstanden", "rum": "herum", "raus": "heraus/hinaus", "rein": "hinein/herein", "drauf": "darauf",
    "drin": "darin", "wollt": "wollte", "total": "sehr/völlig", "voll": "sehr", "echt": "wirklich", "kfz": "Kfz",
}
STIL_CHAT = {"lol": "", "vlt": "vielleicht", "vllt": "vielleicht", "mfg": "Mit freundlichen Grüßen", "lg": "Liebe Grüße",
             "vg": "Viele Grüße", "idk": "", "omg": "", "btw": "übrigens", "thx": "danke", "pls": "bitte", "plz": "bitte",
             "sry": "Entschuldigung", "zb": "z. B.", "usw": "usw.", "bzw": "bzw.", "ka": "keine Ahnung", "xd": "", "hdl": ""}
TYPO = {"frühstens": "frühestens", "kommisioniert": "kommissioniert", "kommisionieren": "kommissionieren",
        "wiederrum": "wiederum", "standart": "Standard", "nähmlich": "nämlich", "vorraus": "voraus",
        "entgültig": "endgültig", "addresse": "Adresse", "packet": "Paket", "agressiv": "aggressiv", "maschiene": "Maschine",
        "interresse": "Interesse", "reperatur": "Reparatur", "ingeneur": "Ingenieur", "seperat": "separat",
        "rythmus": "Rhythmus", "tollerant": "tolerant", "selbstständigkeit": None, "zuverlässlich": "zuverlässig",
        "bewerbe mich hiermit": None, "garnich": "gar nicht", "gesundheitlich": None, "vieleicht": "vielleicht",
        "wiedersprechen": "widersprechen", "endgültig": None, "dilletantisch": "dilettantisch", "lieferrant": "Lieferant",
        "lieferranten": "Lieferanten", "inventhur": "Inventur", "kassieren": None, "projekte": None,
        "erfahrungn": "Erfahrungen", "intressiert": "interessiert", "interresiert": "interessiert", "orginal": "Original",
        "tschüss": None, "febuar": "Februar", "januar": None, "dezemer": "Dezember", "abwechslungsreich": None,
        "zuverlässigkeit": None, "organisatorisch": None, "mechatroniker": None, "kaufmänisch": "kaufmännisch",
        "bürokommunikation": None, "freundlichkeit": None, "hilfbereit": "hilfsbereit", "verantwortungsvol": "verantwortungsvoll"}
TYPO = {k: v for k, v in TYPO.items() if v}
TAGE_KURZ = re.compile(r"(?<![\wÄÖÜäöüß])(Mo|Di|Mi|Do|Fr|Sa|So)\.?\s*(und|&|,|/|-|–|bis)\s*(Mo|Di|Mi|Do|Fr|Sa|So)\.?(?![\wÄÖÜäöüß])")


def stil_befunde(text, referenz=(), lebenslauf=False):
    """→ [(meldung, vorschlag)] für Unterlagen-Text. referenz: korrekt geschriebene Wörter (Anzeige …) für die
    Tippfehler-Erkennung („kommisioniert“ ↔ Anzeige „Kommissionieren“)."""
    out = []
    zeilen = [z for z in (text or "").splitlines()
              if not re.match(r"^\s*(mit freundlichen|viele grüße|beste grüße|liebe grüße|betreff|anlagen?\s*:|===)", z, re.I)]
    t = "\n".join(zeilen)
    gesehen = set()
    ref = {}
    for w in woerter(" ".join(referenz)):
        if len(w) >= 6 and not w[0].isdigit():
            ref.setdefault(lemma(w), w)
    for m in re.finditer(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*", t):
        w = m.group(0)
        lw = w.lower()
        if lw in gesehen:
            continue
        if lw in STIL_UMGANG:
            if lw in ("halt", "voll", "total", "echt", "rein", "raus") and not _umgang_kontext(lw, t, m):
                continue
            if w[0].isupper() and lw not in NOMEN_UMGANG and not _satzanfang(t, m.start()):
                continue          # „4 Grad“, „Halt“, „Total“ als Nomen/Satzanfang
            if lw == "kfz" and w != "kfz":
                continue
            if lw in ("ok", "okay") and lebenslauf:
                continue
            gesehen.add(lw)
            out.append((f"Umgangssprache „{w}“", STIL_UMGANG[lw]))
        elif lw in STIL_CHAT and (lw not in ("bzw", "usw") or not t[m.end():m.end() + 1] == "."):
            if lw in ("bzw", "usw") and t[m.end():m.end() + 1] == ".":
                continue
            gesehen.add(lw)
            out.append((f"Chat-Kürzel „{w}“", STIL_CHAT[lw] or "(streichen)"))
        elif lw in TYPO:
            gesehen.add(lw)
            out.append((f"Tippfehler „{w}“", TYPO[lw]))
        elif len(lw) >= 7 and ref:
            le = lemma(lw)
            if le not in ref and lw not in {x.lower() for x in ref.values()}:
                for rl, rw in ref.items():
                    if rl[:1] == le[:1] and levenshtein(le, rl, 1) == 1 and abs(len(le) - len(rl)) <= 1 \
                            and not le.startswith(rl) and not rl.startswith(le) and _gemeinsam(le, rl) >= 3:
                        gesehen.add(lw)
                        out.append((f"Tippfehler? „{w}“", f"wie in der Anzeige: {rw}"))
                        break
    for m in TAGE_KURZ.finditer(t):
        out.append((f"Abkürzung „{m.group(0)}“", "Wochentage ausschreiben („samstags und sonntags“, „montags bis freitags“)"))
    for m in re.finditer(r"\b([A-Za-zÄÖÜäöüß]{2,})\s+\1\b", t, re.I):
        if m.group(1).lower() in ("sie", "es", "ihr") or re.search(r",\s*$", t[:m.start()]):
            continue      # „bis sie sie verstehen“, „…, die die Ware bringen“
        out.append((f"doppeltes Wort „{m.group(0)}“", m.group(1)))
    satzliste = [re.sub(r"\W+", " ", s.lower()).strip() for s in textlib.saetze(t)]
    teile = {}
    for s in satzliste:
        for tl in re.split(r"\s(?:und|aber|denn|weil)\s", s):
            if len(tl.split()) >= 5:
                teile[tl] = teile.get(tl, 0) + 1
    for tl, k in teile.items():
        if k > 1:
            out.append((f"Wiederholung „{' '.join(tl.split()[:7])}…“ ({k}×)", "einmal reicht"))
    for s in textlib.saetze(t):
        if re.match(r"^[a-zäöü]", s) and not re.match(r"^(z\. ?b\.|bzw\.|ca\.|u\. ?a\.)", s):
            vor = t[:t.find(s)].rstrip()
            if vor.endswith((".", "!", "?")):
                out.append((f"Satzanfang klein „{' '.join(s.split()[:3])}…“", "groß schreiben"))
    return out


NOMEN_UMGANG = {"kumpel", "kids", "azubi", "azubis", "papa", "mama", "ubahn", "sbahn", "kfz", "nix"}


def _satzanfang(t, pos):
    vor = t[:pos].rstrip()
    return not vor or vor.endswith((".", "!", "?", ":", "\n"))


def _umgang_kontext(w, t, m):
    nach = t[m.end():m.end() + 25].lower()
    vor = t[max(0, m.start() - 20):m.start()].lower()
    if w == "halt":
        return not re.match(r"\s*(en|e|t|ung)", nach) and not re.search(r"\b(ein|der|den|zum|kein)\s*$", vor)
    if w in ("voll", "total", "echt"):
        return bool(re.match(r"\s+(gut|nett|cool|toll|spannend|wichtig|gern|schön|super|interessant|anstrengend|stressig|sauer)", nach))
    if w in ("rein", "raus"):
        return not re.match(r"\s*(e|en|er|es|em)\b", nach)
    return True


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    t = " ".join(a)
    for msg, vor in stil_befunde(t):
        print(f"⚠️ {msg} → {vor}")
    print("Lemmata:", ", ".join(f"{w}→{lemma(w)}" for w in woerter(t) if not w[0].isdigit()))


if __name__ == "__main__":
    main()
