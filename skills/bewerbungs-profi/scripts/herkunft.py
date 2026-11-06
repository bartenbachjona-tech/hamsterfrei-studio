#!/usr/bin/env python3
"""Satz-Herkunft prüfen (v4): Jeder Satz mit einer Aussage über die Person braucht eine Quelle –
Antwort-Nr. + WÖRTLICHES Zitat aus dem Nutzer-Wortlaut (profil.rohtext). Claude legt die Zuordnung beim
Entwurf an (profil-JSON, Liste „herkunft“), dieses Skript prüft sie mechanisch und druckt die Woher-Liste.

    python3 herkunft.py PROFIL.json [--teil anschreiben|formular|email|whatsapp|kurzprofil] [--liste]
      → ❌/⚠️ je Satz + kompakte Woher-Liste für die Freigabe-Nachricht. Exit 1 bei ❌.
    (fakten_check.py ruft dieselbe Prüfung automatisch auf.)

Format in der Profil-JSON:
  "herkunft": [
    {"satz": "Seit September 2025 mache ich an der Kasse die Abrechnung.",
     "quellen": [{"nr": 3, "zitat": "seit 09/2025, am schichtende mach ich die abrechnung selbst"}]},
    {"satz": "In Ihrer Anzeige nennen Sie Sorgfalt.", "quellen": [{"anzeige": "Sorgfalt"}]},
    {"satz": "Mich spricht an, dass Azubis eigene Projekte betreuen.", "quellen": [{"nr": 6, "zitat": "…"},
                                                                     {"firmenfakt": "Azubis betreuen eigene Projekte"}]},
    {"satz": "Meine Cousine hat bei Ihnen gelernt.", "quellen": [{"nr": 13, "zitat": "meine cousine hat da ausbildung gemacht"}],
     "privat_ok": true}
  ]
  Kurzform: {"satz": …, "nr": 3, "zitat": "…"}. Quellen-Arten: nr+zitat (Wortlaut) · upload (Zitat aus Text-Upload,
  z. B. Zeugnis-PDF) · anzeige (Zitat aus Anzeige/Einladung) · firmenfakt (nur mit Zustimmung).

Regeln (heuristisch, mit klarer Meldung):
  1. Satz mit Aussage über die Person ohne Eintrag → ❌ „nicht schreiben, sondern fragen“.
  2. Zitat muss (normalisiert) wörtlich in der genannten Antwort stehen (bzw. in Anzeige/Upload/Firmenfakt).
  3. Der Satz darf keine Inhaltswörter/Zahlen enthalten, die weder in seinen Zitaten noch in der Liste neutraler
     Wörter (Bindewörter, „bewerben“, „Anhang“ …) stehen – sonst ❌ mit den Wörtern („täglich, lerne, schnell“).
  4. Aussagen über die Person nie nur aus der Anzeige belegen. Firmenfakt nur mit zugestimmt: true.
  5. Gesundheit, Familie, Privates nur mit "privat_ok": true (ausdrückliche Zustimmung); im Anschreiben ⚠️.
  6. Zitat aus einer unsicheren Antwort („glaub ich“) → ⚠️ erst kurz bestätigen lassen (rohtext geklaert: true).
Neutrale Sätze („Ich freue mich auf ein persönliches Gespräch.“, „Anbei sende ich …“) brauchen keine Quelle.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

NEUTRAL = set(textlib.translit(w) for w in """
ich mich mir mein meine meinen meinem meiner meines wir uns unser unsere unseren unserem unserer du dich dir dein deine
sie ihnen ihr ihre ihrem ihren ihrer ihres es er man der die das den dem des ein eine einen einem einer eines kein keine
keinen dies diese dieser dieses diesem diesen jene welche welcher welches was wer wie wo wann warum
in im am an auf aus bei beim mit nach seit von vom zu zum zur für fuer über ueber unter vor durch gegen ohne um bis ab
als neben während waehrend innerhalb außerhalb per pro je
und oder aber denn weil dass da wenn ob sowie sodass damit dabei dann noch schon jetzt heute derzeit aktuell zurzeit
bereits zudem außerdem ausserdem darum deshalb daher so hier dafür dazu davon darin dort auch nur erst zuerst danach
dadurch somit also zwar sondern sowohl weder nicht
bin bist ist sind war waren gewesen sein habe hast hat haben hatte hatten hätte werde wird werden wurde wurden worden
kann kannst können konnte konnten möchte möchten moechte will wollen würde würden soll sollte darf
mache machst macht machen gemacht arbeite arbeitet arbeiten gearbeitet tätig taetig
bewerbe bewerben bewirbt beworben bewerbung bewerbungen unterlagen lebenslauf anschreiben motivationsschreiben
zeugnis zeugnisse anhang anlage anlagen pdf datei mail e-mail email telefon telefonnummer handy rückfragen rueckfragen
erreichen erreichbar anbei sende schicke schicken senden finden beigefügt beigefuegt
stelle stellen anzeige stellenanzeige ausschreibung ausbildung ausbildungsplatz studium praktikum praktikumsplatz job
gespräch gespraech vorstellungsgespräch persönliches persoenliches persönlich kennenlernen rückmeldung rueckmeldung
nennen nennt suchen sucht steht schreiben schreibt wünschen wuenschen erwarten erwartet bieten bietet
herr frau freue freuen darauf kennenzulernen spricht anfangen anfange beginnen beginne starten starte
erste ersten zweite zweiten jahr jahre jahren monat monate monaten woche wochen uhr ab sofort
eur euro brutto jahresgehalt gehaltsvorstellung stunden std pro
""".split())
# Sätze, die ohne Quelle stehen dürfen (Formalien, Bewerbungsfloskeln ohne Aussage über die Person)
NEUTRAL_SATZ = [r"^ich freue mich\b",
                r"^(anbei|im anhang|beigefügt)\b", r"\b(im anhang|als pdf|anbei|finden sie)\b",
                r"^für (rückfragen|fragen)\b", r"^(hallo|guten tag|sehr geehrte|liebe[rs]?)\b",
                r"^(mit )?(freundlichen|viele|beste|liebe) grüße", r"\bbewerb(e|en)\b", r"\bbewerbung\b"]
ICH_RE = re.compile(r"\b(ich|mich|mir|mein\w*|wir|uns|unser\w*)\b", re.I)
PRIVAT_RE = re.compile(
    r"\b(mein|meine|meinem|meinen|meiner|unser\w*)\s+(sohn|tochter|kind\w*|vater|mutter|papa|mama|eltern|bruder|schwester|"
    r"oma|opa|großmutter|grossmutter|großvater|grossvater|cousine|cousin|tante|onkel|mann|ehemann|frau|ehefrau|partner\w*|"
    r"familie|nachbar\w*)\b|\b(knie\w*|rücken\w*|krank\w*|erkrank\w*|gesundheit\w*|operation|diagnose|therapie\w*|"
    r"depression\w*|burn-?out|behinder\w*|schwerbehinder\w*|schwanger\w*|verletz\w*|unfall|verstorben|gestorben|"
    r"todesfall|trauer\w*|scheidung|religi\w*|glaube[n]?)\b", re.I)
PERSON_ANZEIGE = re.compile(r"\b(führerschein|klasse [a-z]|volljährig|\d+ jahre alt|mindestens \d+|abgeschlossen\w*|"
                            r"mittlere reife|abitur|hochschulreife|[abc][12]|erfahrung)\b", re.I)


def kompakt(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s/.,%-]", " ", textlib.translit((s or "").lower()))).strip()


def alnum(s):
    return re.sub(r"[^a-z0-9]+", " ", textlib.translit((s or "").lower())).strip()


def stamm(w):
    w = textlib.translit(w.lower())
    if len(w) > 6 and w.startswith("ge") and w[2] not in "aeiou":
        w = w[2:]
    for suf in ("ungen", "ung", "innen", "erin", "ern", "en", "er", "es", "em", "e", "st", "t", "n", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[:-len(suf)]
    return w


SEP = ("zurueck", "durch", "nach", "weg", "aus", "ein", "auf", "mit", "vor", "ab", "an", "zu", "um")


def gedeckt(w, quell):
    """Ist das Satzwort w durch eines der Quellwörter gedeckt (Flexion, Komposita, trennbare Verben)?"""
    wt = textlib.translit(w.lower())
    if wt in quell["roh"]:
        return True
    s = stamm(wt)
    for q in quell["staemme"]:
        k = min(len(s), len(q))
        if k >= 4 and (s.startswith(q) or q.startswith(s)):
            return True
        if s == q or (len(s) == 3 and q.startswith(s) and len(q) - len(s) <= 2):
            return True       # „gut“ ↔ „gutes“
        if len(s) >= 4 and any(q.startswith(p) and q[len(p):].startswith(s) for p in SEP):
            return True       # „bildet“ ↔ „ausbilden“
    for p in SEP:             # „ausbilden“ ↔ „bildet … aus“
        if wt.startswith(p) and len(wt) - len(p) >= 4 and p in quell["roh"] and gedeckt(wt[len(p):], quell):
            return True
    if len(wt) >= 5 and any(wt in r for r in quell["roh"] if len(r) > len(wt)):
        return True          # „Lager“ steckt in „Reifenlager“
    if len(wt) >= 9:         # Kompositum aus Quellwörtern („Kassenabrechnung“)
        bedeckt = [False] * len(wt)
        for r in quell["roh"]:
            if len(r) >= 4:
                for m in re.finditer(re.escape(r[:max(4, len(r) - 2)]), wt):
                    for i in range(m.start(), min(len(wt), m.start() + len(r))):
                        bedeckt[i] = True
        if sum(bedeckt) / len(wt) >= 0.8:
            return True
    return False


def quell_index(texte):
    roh = set()
    for t in texte:
        roh |= set(re.findall(r"[a-z0-9]+", textlib.translit(textlib.normalisiere_nutzertext(t).lower())))
    belege = Monatsbelege("\n".join(textlib.normalisiere_nutzertext(t) for t in texte))
    return {"roh": roh, "staemme": {stamm(r) for r in roh if not r.isdigit()}, "zahlen": belege.zahlen,
            "monate": belege.monate}


class Monatsbelege:
    MON = {**{k: v for k, v in textlib.MONATE_NORM.items()}}

    def __init__(self, t):
        low = textlib.translit(t.lower())
        self.zahlen, self.monate = set(), set()
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
        for m in re.finditer(r"\b\d{1,2}\.(\d{1,2})\.(\d{2,4})\b", low):
            self.monate.add(int(m.group(1)))
            y = int(m.group(2))
            self.zahlen.add(str(y + 2000 if y < 100 else y))
        for w in re.findall(r"[a-z]+", low):
            if textlib.translit(w) in {textlib.translit(k) for k in self.MON}:
                self.monate.add(next(v for k, v in self.MON.items() if textlib.translit(k) == w))
        for m in re.finditer(r"\b(" + "|".join(sorted({textlib.translit(k) for k in self.MON}, key=len, reverse=True))
                             + r")\.?\s+'?(\d{2})\b", low):
            self.zahlen.add(str(2000 + int(m.group(2))))


def ist_monat(w):
    wt = textlib.translit(w.lower())
    for k, v in textlib.MONATE_NORM.items():
        if textlib.translit(k) == wt and len(wt) >= 3:
            return v
    return None


POSSESSIV_SIE = {"ihr", "ihre", "ihrem", "ihren", "ihrer", "ihres", "euer", "eure", "eurem", "euren", "eurer"}
FIRMA_NOMEN = set(textlib.translit(w) for w in "haus unternehmen betrieb firma team praxis filiale markt laden kanzlei kita "
                  "autohaus getränkemarkt büro standort geschäft klinik hotel restaurant werkstatt".split())
NEUTRAL_STAEMME = {stamm(w) for w in NEUTRAL if len(w) >= 5}
GRUSS = set(textlib.translit(w) for w in "sehr geehrte geehrter hallo guten tag liebe lieber freundlichen grüßen "
             "grüße viele beste herzliche".split())


def ist_neutral_satz(satz, erlaubt, zahlen_anzeige=()):
    low = satz.lower().strip()
    if not any(re.search(rx, low) for rx in NEUTRAL_SATZ):
        return False
    rest = [w for w in re.findall(r"[a-zäöüß0-9]+", low) if textlib.translit(w) not in NEUTRAL
            and not erlaubt_hat(textlib.translit(w), erlaubt) and textlib.translit(w) not in GRUSS
            and not (w.isdigit() and (w in zahlen_anzeige or str(int(w)) in zahlen_anzeige))]
    return not rest


def nur_formales(satz, erlaubt):
    """„ab Dezember 2026“, „01.09.2027“: nur Datum/Zahl/neutrale Wörter, keine Ich-Aussage → prüft fakten_check."""
    if ICH_RE.search(satz):
        return False
    for w in re.findall(r"[A-Za-zÄÖÜäöüß]+|\d+", satz):
        wt = textlib.translit(w.lower())
        if not (wt.isdigit() or wt in NEUTRAL or erlaubt_hat(wt, erlaubt) or ist_monat(w) or len(wt) < 3):
            return False
    return True


def saetze(text):
    out = []
    for z in (text or "").splitlines():
        z = z.strip()
        if not z:
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9„\"])", z):
            out.append(s.strip())
    return out


def texte_aus(d, teil=None):
    """→ [(teil, satz)] aller Freitexte, die eine Herkunft brauchen."""
    out = []
    an = d.get("anschreiben") or {}
    if teil in (None, "anschreiben"):
        for a in an.get("absaetze") or []:
            out += [("anschreiben", s) for s in saetze(a)]
    if teil in (None, "formular"):
        for f in d.get("formular") or []:
            if "aufmerksam" in (f.get("feld") or "").lower():
                continue          # eigene Prüfung (Quelle) in fakten_check
            out += [("formular", s) for s in saetze(f.get("text") or "")]
    if teil in (None, "email"):
        out += [("email", s) for s in saetze((d.get("email") or {}).get("text") or "")]
    if teil in (None, "whatsapp"):
        out += [("whatsapp", s) for s in saetze((d.get("whatsapp") or {}).get("text") or "")]
    if teil in (None, "kurzprofil"):
        out += [("kurzprofil", s) for s in saetze((d.get("lebenslauf") or {}).get("kurzprofil") or "")]
    return [(t, re.sub(r"\[PRÜFEN:[^\]]*\]", "", s).strip()) for t, s in out if s.strip()]


def eintraege(d):
    out = []
    for e in d.get("herkunft") or []:
        if not isinstance(e, dict) or not e.get("satz"):
            continue
        qs = list(e.get("quellen") or [])
        if e.get("zitat") or e.get("nr"):
            qs.insert(0, {"nr": e.get("nr"), "zitat": e.get("zitat", "")})
        for k in ("anzeige", "firmenfakt", "upload"):
            if e.get(k):
                qs.append({k: e[k]})
        out.append({**e, "quellen": qs})
    return out


def finde_eintrag(satz, liste):
    a = alnum(satz)
    for e in liste:
        b = alnum(e["satz"])
        if a == b or (min(len(a), len(b)) >= 20 and (a.startswith(b) or b.startswith(a))):
            return e
    for e in liste:   # Satz leicht umgestellt/gekürzt: hohe Wortüberdeckung
        wa, wb = set(a.split()), set(alnum(e["satz"]).split())
        if wa and wb and len(wa & wb) / max(len(wa), len(wb)) >= 0.85:
            return e
    return None


def ziel_woerter(d):
    z, p = d.get("ziel") or {}, d.get("person") or {}
    imm, stelle = set(), set()
    for k in ("firma", "ansprechperson", "kennziffer"):
        imm |= set(re.findall(r"[a-z0-9]+", textlib.translit(str(z.get(k) or "").lower())))
    for k in ("name", "telefon", "email", "strasse", "plz_ort"):
        imm |= set(re.findall(r"[a-z0-9]+", textlib.translit(str(p.get(k) or "").lower())))
    an = (z.get("anrede") or "") + " " + " ".join(z.get("firma_adresse") or [] if isinstance(z.get("firma_adresse"), list) else [])
    imm |= set(re.findall(r"[a-z0-9]+", textlib.translit(an.lower())))
    stelle |= set(re.findall(r"[a-z0-9]+", textlib.translit(str(z.get("stelle") or "").lower())))
    for w in list(stelle):          # Kaufmann/-frau, Mechatroniker/in → alle Formen
        if w.endswith("mann"):
            stelle |= {w[:-4] + "frau", w[:-4] + "leute"}
        elif w.endswith("frau"):
            stelle.add(w[:-4] + "mann")
        if w.endswith(("er", "ent", "ant", "eur", "ist", "ling")):
            stelle |= {w + "in", w + "innen"}
    return imm, stelle


def erlaubt_hat(wt, erlaubt):
    """Ziel-/Personenwort, auch gebeugt („Fachangestellten“ ↔ „fachangestellte“)."""
    if wt in erlaubt:
        return True
    s = stamm(wt)
    return len(s) >= 6 and any(len(e) >= 6 and (stamm(e).startswith(s) or s.startswith(stamm(e))) for e in erlaubt)


def pruefe(d, teil=None):
    """→ (befunde [(sym, teil, satz, meldung)], woher [(sym, satz, quelle_text)])"""
    eintr = {e["nr"]: e for e in textlib.rohtext_eintraege(d)}
    unklar = {e["nr"] for e in textlib.unklare_antworten(d)}
    z = d.get("ziel") or {}
    anzeige = kompakt("\n".join([z.get("anzeige_text") or "", (d.get("gespraech") or {}).get("einladung_text") or ""]))
    uploads, _ = textlib.upload_texte(d)
    upload_k = kompakt("\n".join(uploads))
    ff = {kompakt(f.get("fakt")): f for f in d.get("firmenfakten") or [] if f.get("fakt")}
    imm, stelle_w = ziel_woerter(d)
    liste = eintraege(d)
    anz_zahlen = Monatsbelege(anzeige).zahlen
    befunde, woher = [], []
    for t, satz in texte_aus(d, teil):
        erlaubt = imm | (stelle_w if re.search(r"bewerb|anzeige|stelle|platz|ausbildung als|als\b", satz, re.I) else set())
        e = finde_eintrag(satz, liste)
        if e is None:
            if ist_neutral_satz(satz, erlaubt, anz_zahlen) or nur_formales(satz, erlaubt):
                continue
            befunde.append(("❌", t, satz, "Satz ohne Quelle – nicht schreiben, sondern den Nutzer fragen "
                                          "(oder herkunft mit Antwort-Nr. + wörtlichem Zitat ergänzen)"))
            woher.append(("❓", satz, "keine Quelle → als Frage stellen"))
            continue
        nutzer_q, firma_q, q_texte, meldungen, qtext = [], [], [], [], []
        for q in e["quellen"]:
            zit = q.get("zitat") or ""
            if q.get("anzeige"):
                if kompakt(q["anzeige"]) and kompakt(q["anzeige"]) in anzeige:
                    firma_q.append(q["anzeige"])
                    q_texte.append(q["anzeige"])
                    qtext.append(f"Anzeige: „{kurz(q['anzeige'])}“")
                else:
                    meldungen.append(("❌", f"Anzeige-Zitat „{kurz(q['anzeige'])}“ steht nicht in Anzeige/Einladung"))
                continue
            if q.get("firmenfakt"):
                f = ff.get(kompakt(q["firmenfakt"])) or next((v for k, v in ff.items() if kompakt(q["firmenfakt"]) in k), None)
                if not f:
                    meldungen.append(("❌", f"Firmenfakt „{kurz(q['firmenfakt'])}“ nicht in firmenfakten"))
                elif f.get("zugestimmt") is not True:
                    meldungen.append(("❌", f"Firmenfakt „{kurz(q['firmenfakt'])}“ ohne Zustimmung des Nutzers"))
                else:
                    firma_q.append(f["fakt"])
                    q_texte.append(f["fakt"])
                    qtext.append("Firmen-Info (du: ja)")
                continue
            if q.get("upload"):
                if kompakt(q["upload"]) and kompakt(q["upload"]) in upload_k:
                    nutzer_q.append(q["upload"])
                    q_texte.append(q["upload"])
                    qtext.append(f"dein Zeugnis/Upload: „{kurz(q['upload'])}“")
                else:
                    meldungen.append(("❌", f"Upload-Zitat „{kurz(q['upload'])}“ steht in keinem Text-Upload "
                                            "(Fotos/Scans: Inhalt erst beim Nutzer bestätigen → rohtext)"))
                continue
            nr = q.get("nr")
            if not zit:
                meldungen.append(("❌", f"Quelle ohne wörtliches Zitat (Antwort {nr})"))
                continue
            kz = kompakt(zit)
            treffer = None
            if nr in eintr and (kz in kompakt(eintr[nr]["antwort"]) or kz in kompakt(textlib.normalisiere_nutzertext(eintr[nr]["antwort"]))
                                or kz in kompakt(" ".join(str(v) for v in (eintr[nr].get("optionen") or {}).values()))
                                or (eintr[nr].get("bestaetigt") and kz in kompakt(eintr[nr]["bestaetigt"]) and textlib.JA_RE.match(eintr[nr]["antwort"]))):
                treffer = nr
            else:
                for n2, e2 in eintr.items():
                    if kz and kz in kompakt(e2["antwort"]):
                        treffer = n2
                        meldungen.append(("⚠️", f"Zitat „{kurz(zit)}“ steht in Antwort {n2}, nicht in {nr} – Nummer korrigieren"))
                        break
            if treffer is None:
                meldungen.append(("❌", f"Zitat „{kurz(zit)}“ steht so in keiner Antwort (wörtlich zitieren, nicht umformulieren)"))
                continue
            if eintr[treffer].get("sensibel"):
                meldungen.append(("❌", f"Antwort {treffer} ist als sensibel markiert – nicht in Unterlagen verwenden"))
                continue
            if treffer in unklar:
                meldungen.append(("⚠️", f"Antwort {treffer} war unsicher („{kurz(eintr[treffer]['antwort'], 6)}“) – "
                                        "erst kurz mit Ja/Nein bestätigen lassen (rohtext: geklaert: true)"))
            nutzer_q.append(zit)
            q_texte.append(zit)
            qtext.append(f"deine Worte: „{kurz(zit)}“ (Nr. {treffer})")
        ich = bool(ICH_RE.search(satz))
        versucht = any(q.get("nr") or q.get("zitat") or q.get("upload") for q in e["quellen"])
        if ich and not nutzer_q and not versucht:
            meldungen.append(("❌", "Aussage über dich, aber keine Quelle aus deinen Antworten – die Anzeige "
                                    "belegt nichts über dich"))
        if ich and firma_q:
            nq = quell_index(nutzer_q)
            pa_fehl = [x for x in PERSON_ANZEIGE.findall(satz)
                       if not all(gedeckt(w, nq) for w in re.findall(r"[a-zäöüß0-9]+", x.lower()))]
            if pa_fehl:
                meldungen.append(("❌", "Personen-Fakt nur aus der Anzeige: " + ", ".join(dict.fromkeys(pa_fehl))))
        # Inhaltswörter/Zahlen ohne Deckung
        qi = quell_index(q_texte)
        fehl = []
        vorher = ""
        for w in re.findall(r"[A-Za-zÄÖÜäöüß]+|\d+", satz):
            wt = textlib.translit(w.lower())
            vor, vorher = vorher, wt
            if wt in NEUTRAL or erlaubt_hat(wt, erlaubt) or len(wt) < 3 and not wt.isdigit():
                continue
            if vor in POSSESSIV_SIE and wt in FIRMA_NOMEN:
                continue          # „Ihr Haus“, „Ihr Betrieb“ = die Zielfirma, keine Aussage über die Person
            if wt[0].isdigit():
                if {wt, str(int(wt))} & qi["zahlen"] or wt in erlaubt:
                    continue
                fehl.append(w)
                continue
            if stamm(wt) in NEUTRAL_STAEMME:
                continue
            mon = ist_monat(w)
            if mon:
                if mon in qi["monate"]:
                    continue
                fehl.append(w)
                continue
            if not gedeckt(w, qi):
                fehl.append(w)
        if fehl:
            meldungen.append(("❌", "Wörter ohne Quelle: " + ", ".join(dict.fromkeys(fehl))
                              + " – hat der Nutzer das so gesagt? Sonst streichen oder fragen"))
        if PRIVAT_RE.search(satz):
            if not e.get("privat_ok"):
                meldungen.append(("❌", f"Privates/Gesundheit/Familie („{PRIVAT_RE.search(satz).group(0)}“) nur nach "
                                        "ausdrücklicher Zustimmung (privat_ok: true)"))
            elif t == "anschreiben":
                meldungen.append(("⚠️", "Privates im Anschreiben – im Regelfall weglassen (Nutzer hat zugestimmt)"))
        for sym, m in meldungen:
            befunde.append((sym, t, satz, m))
        sym = "❌" if any(s == "❌" for s, _ in meldungen) else ("⚠️" if meldungen else "✅")
        woher.append((sym, satz, " + ".join(qtext) if qtext else "–"))
    return befunde, woher


def kurz(s, n=8):
    w = (s or "").split()
    return " ".join(w[:n]) + ("…" if len(w) > n else "")


def woher_liste(woher, max_zeilen=12):
    """Kompakte Woher-Liste für die Freigabe: Satzanfang → deine Worte."""
    zeilen = []
    for sym, satz, q in woher[:max_zeilen]:
        anfang = kurz(satz, 5)
        if sym == "❓":
            zeilen.append(f"❓ „{anfang}“ → {q}")
        else:
            zeilen.append(f"– „{anfang}“ → {q}" + ("  ⚠️" if sym == "⚠️" else "  ❌" if sym == "❌" else ""))
    return zeilen


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    teil = None
    if "--teil" in a:
        i = a.index("--teil")
        teil = a[i + 1]
        del a[i:i + 2]
    try:
        d = textlib.lade_profil(a[0])
    except RuntimeError as e:
        print(f"FEHLER: {e}")
        sys.exit(2)
    bef, woher = pruefe(d, teil)
    print("# Satz-Herkunft (v4) – jeder Satz über die Person braucht deine Worte als Quelle")
    for sym, t, satz, m in bef:
        print(f"{sym} [{t}] „{kurz(satz, 10)}“ ⟶ {m}")
    print("---")
    print("# Woher-Liste (für die Freigabe-Nachricht):")
    for z in woher_liste(woher) or ["(keine Sätze mit Aussagen über die Person)"]:
        print(z)
    rot = sum(1 for b in bef if b[0] == "❌")
    print("---")
    print(f"{rot} ❌ · {sum(1 for b in bef if b[0] == '⚠️')} ⚠️")
    sys.exit(1 if rot else 0)


if __name__ == "__main__":
    main()
