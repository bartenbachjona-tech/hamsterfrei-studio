#!/usr/bin/env python3
"""Satz-Herkunft prüfen (v5: „Fakten wörtlich, Formulierung frei“). Jeder Satz mit einer Aussage über die Person
braucht eine Quelle – Antwort-Nr. + Zitat aus dem Nutzer-Wortlaut (profil.rohtext). Claude legt die Zuordnung beim
Entwurf an (Liste „herkunft“), dieses Skript prüft sie und druckt die Woher-Liste.

    python3 herkunft.py PROFIL.json [--teil anschreiben|formular|email|whatsapp|kurzprofil]
      → ❌/⚠️ je Satz + kompakte Woher-Liste für die Freigabe-Nachricht. Exit 1 bei ❌.
    (fakten_check.py ruft dieselbe Prüfung automatisch auf.)

Format in der Profil-JSON:
  "herkunft": [
    {"satz": "Seit September 2025 erstelle ich an der Kasse die Abrechnung.",
     "quellen": [{"nr": 3, "zitat": "seit 09/2025, am schichtende mach ich die abrechnung selbst"}]},
    {"satz": "In Ihrer Anzeige nennen Sie Sorgfalt.", "quellen": [{"anzeige": "Sorgfalt"}]},
    {"satz": "Anbei sende ich Ihnen meine Bewerbung …", "vorlage": true},
    {"satz": "Meine Cousine hat bei Ihnen gelernt.", "nr": 13, "zitat": "meine cousine hat da ausbildung gemacht",
     "privat_ok": true}]
  Quellen-Arten: nr+zitat (Wortlaut) · upload (Text-Upload, z. B. Zeugnis-PDF) · anzeige (Anzeige/Einladung) ·
  firmenfakt (nur mit Zustimmung). „…“ im Zitat erlaubt (Teile in der Reihenfolge der Antwort).

Was geprüft wird (v5) – nur BEHAUPTUNGS-BAUSTEINE, die Formulierung ist frei:
  Zahlen, Daten, Dauern, Eigennamen, Abschlüsse/Zertifikate/Niveaus, Tätigkeiten und Fähigkeiten, Häufigkeit und
  Intensität (täglich, immer, schnell, sehr …), Gefühle und Motive (Spaß, spannend, spricht mich an …), Kontakt zur
  Firma (kennengelernt …). Jeder solche Baustein muss in den Quellen des Satzes stehen – erkannt werden Beugung,
  Partizip II, trennbare Verben, Komposita-Teilwörter, Zahlwörter („fünften“ ↔ „5.“), Daten („1.2.27“ ↔ „1. Februar
  2027“), Umgangssprache („red“ → reden, „nix“ → nichts, „ubahn“ → U-Bahn, „leute“ → Kunden, „bescheid sagen“ →
  informieren) und Tippfehler (Levenshtein ≤ 2 ab 6 Zeichen). Funktions- und Stilwörter sind frei (sprachlib.FREI).
  Bestätigte Werte („Januar 2026?“ → „ja“/„a“) gelten überall als Nutzerangabe.
Weitere Regeln: Satz ohne Eintrag → ❌ „nicht schreiben, sondern fragen“. Zitat muss in der Antwort stehen.
  In Ich-Teilsätzen zählen nur Nutzer-Quellen (Anzeige/Firmenfakt belegen nichts über die Person).
  Gesundheit/Familie/Privates nur mit privat_ok (im Anschreiben ⚠️). Unsichere Antwort → ⚠️ bis geklaert.
  Vorlagensätze (Mail: „Anbei sende ich Ihnen …“, „… finden Sie in einer PDF im Anhang“) sind neutral.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402
import sprachlib as SL  # noqa: E402

# Sätze, die ohne Quelle stehen dürfen (Formalien, Mail-Vorlagen aus abschicken.md)
NEUTRAL_SATZ = [r"^ich freue mich\b", r"^(anbei|im anhang|beigefügt)\b", r"\b(im anhang|als pdf|anbei|finden sie)\b",
                r"^für (rückfragen|fragen)\b", r"^(hallo|guten tag|sehr geehrte[rn]?|liebe[rs]?)\b",
                r"^(mit )?(freundlichen|viele|beste|liebe) grüße", r"\bbewerb(e|en)\b", r"\bbewerbung\b",
                r"^(meinen|den) lebenslauf\b", r"\bschicke ich\b", r"\berreichen sie mich\b"]
UNTERLAGEN_WORTE = set(SL.n(w) for w in """lebenslauf anschreiben motivationsschreiben zeugnis zeugnisse arbeitszeugnis
arbeitszeugnisse abiturzeugnis abschlusszeugnis notenspiegel nachweis nachweise bescheinigung bescheinigungen zertifikat
zertifikate unterlagen anlagen dokumente schulzeugnis schulzeugnisse halbjahreszeugnis jahreszeugnis zwischenzeugnis
praktikumszeugnis gesellenbrief letzten zwei drei beiden vollständigen mitgeschickt""".split())
PRIVAT_RE = re.compile(
    r"\b(mein|meine|meinem|meinen|meiner|unser\w*)\s+(sohn|tochter|kind\w*|vater|mutter|papa|mama|eltern|bruder|schwester|"
    r"oma|opa|großmutter|grossmutter|großvater|grossvater|cousine|cousin|tante|onkel|mann|ehemann|frau|ehefrau|partner\w*|"
    r"familie|nachbar\w*)\b|\b(knie\w*|rücken\w*|krank(?!en(kasse|kassen|haus|häuser|versicher\w*|pfleg\w*|geld|schein))\w*|"
    r"erkrank\w*|gesundheit\w*|operation|diagnose|therapie\w*|depression\w*|burn-?out|behinder\w*|schwerbehinder\w*|"
    r"schwanger\w*|verletz\w*|unfall|verstorben|gestorben|todesfall|trauer\w*|scheidung|religi\w*|elternzeit|"
    r"mutterschutz|kinderbetreuung|kitaplatz|kita-platz)\b|\b(kita|kindergarten|krippe|hort)\b(?=[^.]*\b(abhol\w*|bring\w*|"
    r"schließt|platz|betreuung|öffnungszeit\w*)\b)", re.I)
POSSESSIV_SIE = {"ihr", "ihre", "ihrem", "ihren", "ihrer", "ihres", "euer", "eure", "eurem", "euren", "eurer"}
FIRMA_NOMEN = set(SL.n(w) for w in "haus unternehmen betrieb firma team praxis filiale markt laden kanzlei kita autohaus "
                  "getränkemarkt büro standort geschäft klinik hotel restaurant werkstatt kasse".split())
RECHTSFORM = {"gmbh", "ag", "kg", "ggmbh", "mbh", "se", "ohg", "gbr", "ug", "ev", "eg", "kgaa", "co"}


def kompakt(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s/.,%-]", " ", textlib.translit((s or "").lower()))).strip()


def alnum(s):
    return re.sub(r"[^a-z0-9]+", " ", textlib.translit((s or "").lower())).strip()


def _dicht(s):
    return re.sub(r"[^a-z0-9]+", "", textlib.translit((s or "").lower()))


def zitat_in(zitat, text):
    """Zitat steht (normalisiert: Groß/klein, Satzzeichen, Leerzeichen, Bindestriche) im Text; „…“ trennt Teile."""
    t = _dicht(text)
    pos = 0
    for teil in re.split(r"\s*(?:…|\.\.\.)\s*", zitat or ""):
        d = _dicht(teil)
        if not d:
            continue
        i = t.find(d, pos)
        if i < 0:
            return False
        pos = i + len(d)
    return bool(_dicht(zitat))


def texte_aus(d, teil=None):
    """→ [(teil, satz)] aller Freitexte, die eine Herkunft brauchen."""
    out = []
    an = d.get("anschreiben") or {}
    if teil in (None, "anschreiben"):
        for a in an.get("absaetze") or []:
            out += [("anschreiben", s) for s in textlib.saetze(a)]
    if teil in (None, "formular"):
        for f in d.get("formular") or []:
            if "aufmerksam" in (f.get("feld") or "").lower():
                continue          # eigene Prüfung (Quelle) in fakten_check
            out += [("formular", s) for s in textlib.saetze(f.get("text") or "")]
    if teil in (None, "email"):
        out += [("email", s) for s in textlib.saetze((d.get("email") or {}).get("text") or "")]
    if teil in (None, "whatsapp"):
        out += [("whatsapp", s) for s in textlib.saetze((d.get("whatsapp") or {}).get("text") or "")]
    if teil in (None, "kurzprofil"):
        out += [("kurzprofil", s) for s in textlib.saetze((d.get("lebenslauf") or {}).get("kurzprofil") or "")]
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
    imm, stelle = set(RECHTSFORM), set()
    for k in ("firma", "ansprechperson", "kennziffer"):
        imm |= set(re.findall(r"[a-z0-9]+", textlib.translit(str(z.get(k) or "").lower())))
    for k in ("name", "telefon", "email"):          # v5: Wohnort/Straße NICHT frei (Hotel „in München“ erfunden)
        imm |= set(re.findall(r"[a-z0-9]+", textlib.translit(str(p.get(k) or "").lower())))
    an = " ".join(z.get("firma_adresse") or [] if isinstance(z.get("firma_adresse"), list) else [])   # nicht die Anrede („Sehr“)
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
    if wt in erlaubt:
        return True
    s = SL.lemma(wt)
    return len(s) >= 4 and any(len(e) >= 4 and (SL.lemma(e) == s or SL.lemma(e).startswith(s) or s.startswith(SL.lemma(e)))
                               for e in erlaubt)


def ist_vorlage_satz(satz, erlaubt, Q_alle, anlagen_w):
    """Mail-/Brief-Vorlage: neutrales Muster und nur Unterlagen-/Stellen-/Firmenwörter + belegte Zahlen/Daten."""
    low = satz.lower().strip()
    if not any(re.search(rx, low) for rx in NEUTRAL_SATZ):
        return False
    for w in SL.woerter(satz):
        wt = SL.n(w)
        if wt in erlaubt:
            continue              # Telefonnummer, Name, Firma, Kennziffer
        if w[0].isdigit() or SL.ist_zahlwort(w) or wt in SL.MONATE:
            if w[0].isdigit() or SL.ist_zahlwort(w):
                if SL.zahl_gedeckt(w, Q_alle) == "nein":
                    return False
            elif SL.MONATE[wt] not in Q_alle.monate:
                return False
            continue
        if len(wt) < 3 or SL.ist_frei(w) or wt in UNTERLAGEN_WORTE or wt in anlagen_w or erlaubt_hat(wt, erlaubt):
            continue
        if wt in {"freue", "freuen", "persoenliches", "gespraech", "rueckfragen", "erreichen", "unter", "jederzeit",
                  "schicke", "mit", "gern", "gerne", "vorstellungsgespraech", "einladung", "sehr", "beste", "besten",
                  "herzliche", "herzlichen", "liebe", "lieber", "viele"}:
            continue
        return False
    return True


def nur_formales(satz, erlaubt, Q_alle):
    """„ab Dezember 2026“, „01.09.2027“: nur Datum/Zahl/neutrale Wörter, keine Ich-Aussage → Zahlen belegt?"""
    if SL.ICH_RE.search(satz):
        return False
    for w in SL.woerter(satz):
        wt = SL.n(w)
        if w[0].isdigit():
            if SL.zahl_gedeckt(w, Q_alle) == "nein":
                return False
            continue
        if not (SL.ist_frei(w) or erlaubt_hat(wt, erlaubt) or wt in SL.MONATE or len(wt) < 3):
            return False
    return True


def klauseln(satz):
    """Satz → Teilsätze (an , ; : – — ( ) getrennt; „7,5“ und „2.14“ bleiben ganz)."""
    teile = re.split(r"(?<!\d),(?!\d)|;|:|\s[–—-]\s|\(|\)", satz)
    return [t for t in teile if t and t.strip()]


def stelle_erlaubt(satz):
    return bool(re.search(r"bewerb|anzeige|stelle|platz|möcht|moecht|will|wollen|wünsch|anfang|beginn|start|absolvier|"
                          r"\bals\b|ausbildung|studium|praktikum|interess|bei ihnen", satz, re.I))


def pruefe(d, teil=None):
    """→ (befunde [(sym, teil, satz, meldung)], woher [(sym, satz, quelle_text)])"""
    roh = textlib.rohtext_eintraege(d)
    eintr = {e["nr"]: e for e in roh}
    unklar = {e["nr"] for e in textlib.unklare_antworten(d)}
    z = d.get("ziel") or {}
    anzeige_roh = "\n".join([z.get("anzeige_text") or "", (d.get("gespraech") or {}).get("einladung_text") or ""])
    uploads, _ = textlib.upload_texte(d)
    upload_roh = "\n".join(uploads)
    ff = {kompakt(f.get("fakt")): f for f in d.get("firmenfakten") or [] if f.get("fakt")}
    imm, stelle_w = ziel_woerter(d)
    liste = eintraege(d)
    # global: bestätigte Werte (zählen überall), Wortlaut + Uploads + Anzeige (für Vorlagensätze/Zahlen)
    bestaetigt = [w for e in roh if not e.get("sensibel") for w in textlib.bestaetigte_werte(e)]
    alle_nutzer = textlib.wortlaut(d) + uploads
    Q_alle = SL.Quelle(alle_nutzer + [anzeige_roh, (d.get("ziel") or {}).get("start") or ""])
    anlagen_w = set()
    for a in (d.get("profil") or {}).get("anlagen") or []:
        anlagen_w |= {SL.n(w) for w in SL.woerter(a.get("bezeichnung") or "")}
    abgel = {}
    for e in roh:
        if not e.get("sensibel"):
            abgel.update(SL.abgeleitete_jahre(e["antwort"]))
    du = "Ihre" if ((d.get("meta") or {}).get("anrede_form") or "").lower().startswith("s") else "deine"
    befunde, woher = [], []
    for t, satz in texte_aus(d, teil):
        erlaubt = imm | (stelle_w if stelle_erlaubt(satz) else set())
        e = finde_eintrag(satz, liste)
        if e is not None and e.get("vorlage"):
            if ist_vorlage_satz(satz, erlaubt | set(SL.n(w) for w in SL.woerter(" ".join(bestaetigt))), Q_alle, anlagen_w) \
                    or nur_formales(satz, erlaubt, Q_alle):
                continue
            befunde.append(("❌", t, satz, "als Vorlage markiert, enthält aber eine Aussage über die Person – Quelle angeben"))
            woher.append(("❌", satz, "Vorlage mit eigener Aussage"))
            continue
        if e is None:
            if ist_vorlage_satz(satz, erlaubt, Q_alle, anlagen_w) or nur_formales(satz, erlaubt, Q_alle):
                continue
            befunde.append(("❌", t, satz, "Satz ohne Quelle – nicht schreiben, sondern den Nutzer fragen "
                                          "(oder herkunft mit Antwort-Nr. + Zitat ergänzen)"))
            woher.append(("❓", satz, "keine Quelle → als Frage stellen"))
            continue
        nutzer_t, firma_t, meldungen, qtext, nutzer_zit = [], [], [], [], []
        hat_nutzerquelle = False
        for q in e["quellen"]:
            zit = q.get("zitat") or ""
            if q.get("anzeige"):
                if zitat_in(q["anzeige"], anzeige_roh):
                    firma_t.append(q["anzeige"])
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
                    firma_t.append(f["fakt"])
                    qtext.append("Firmen-Info (zugestimmt)")
                continue
            if q.get("upload"):
                hat_nutzerquelle = True
                if zitat_in(q["upload"], upload_roh):
                    nutzer_t.append(q["upload"])
                    nutzer_t += [u for u in uploads if zitat_in(q["upload"], u)]
                    qtext.append(f"{du.capitalize()} Zeugnis/Upload: „{kurz(q['upload'])}“")
                else:
                    meldungen.append(("❌", f"Upload-Zitat „{kurz(q['upload'])}“ steht in keinem Text-Upload "
                                            "(Fotos/Scans: Inhalt erst beim Nutzer bestätigen → rohtext)"))
                continue
            nr = q.get("nr")
            hat_nutzerquelle = True
            if not zit and nr not in eintr:
                meldungen.append(("❌", f"Quelle ohne Zitat (Antwort {nr})"))
                continue
            treffer = None
            if nr in eintr:
                en = eintr[nr]
                quelltexte = [en["antwort"], textlib.normalisiere_nutzertext(en["antwort"])] + textlib.gewaehlte_optionen(en) \
                    + textlib.bestaetigte_werte(en)
                if not zit or any(zitat_in(zit, x) for x in quelltexte):
                    treffer = nr
            if treffer is None and zit:
                for n2, e2 in eintr.items():
                    if zitat_in(zit, e2["antwort"]) or any(zitat_in(zit, x) for x in textlib.bestaetigte_werte(e2)):
                        treffer = n2
                        if nr is not None:
                            meldungen.append(("⚠️", f"Zitat „{kurz(zit)}“ steht in Antwort {n2}, nicht in {nr} – Nummer korrigieren"))
                        break
            if treffer is None:
                meldungen.append(("❌", f"Zitat „{kurz(zit)}“ steht so in keiner Antwort (aus der Antwort kopieren, nicht umformulieren)"))
                continue
            en = eintr[treffer]
            if en.get("sensibel"):
                meldungen.append(("❌", f"Antwort {treffer} ist als sensibel markiert – nicht in Unterlagen verwenden"))
                continue
            if treffer in unklar:
                meldungen.append(("⚠️", f"Antwort {treffer} war unsicher („{kurz(en['antwort'], 6)}“) – "
                                        "erst kurz mit Ja/Nein bestätigen lassen (rohtext: geklaert: true)"))
            nutzer_t += [zit, en["antwort"]] + textlib.gewaehlte_optionen(en) + textlib.bestaetigte_werte(en)
            nutzer_zit.append(f"„{kurz(zit or en['antwort'])}“")
        if nutzer_zit:
            qtext.insert(0, f"{du} Worte: " + " + ".join(dict.fromkeys(nutzer_zit)))
        ich_satz = bool(SL.ICH_RE.search(satz))
        if ich_satz and not hat_nutzerquelle:
            meldungen.append(("❌", "Aussage über die Person, aber keine Quelle aus ihren Antworten – die Anzeige "
                                    "belegt nichts über dich"))
        QN = SL.Quelle(nutzer_t + bestaetigt, abgel)
        QF = SL.Quelle(firma_t)
        fehl, abgeleitet, nur_firma = [], [], []
        # trennbares Motiv-Verb „spricht … an“ / „sprach mich an“ = Gefühl/Motiv → muss vom Nutzer kommen
        if re.search(r"\b(spricht|sprechen|sprach|sprachen)\b[^.,;:]*\ban\b|\b(anspricht|angesprochen|ansprechen)\b", satz, re.I) \
                and not SL.gedeckt("anspricht", QN) and not SL.gedeckt("angesprochen", QN):
            fehl.append("spricht … an")
        for kl in klauseln(satz):
            sie_kl = bool(SL.SIE_RE.search(kl)) and not SL.ICH_RE.search(kl)
            pm = re.search(r"\b(vor|an|aus|ein|auf|ab|mit|zu|weiter|zurück|fest|nach|fertig|kennen|her|hin)\W*$", kl.strip())
            partikel = SL.n(pm.group(1)) if pm else ""
            firma_ok = sie_kl or not ich_satz
            vorher = ""
            toks = SL.woerter(kl)
            for i, w in enumerate(toks):
                wt = SL.n(w)
                vor, vorher = vorher, wt
                if w[0].isdigit() or SL.ist_zahlwort(w):
                    r = SL.zahl_gedeckt(w, QN)
                    if r == "ja" or wt in erlaubt or (firma_ok and SL.zahl_gedeckt(w, QF) == "ja"):
                        continue
                    if w[0].isdigit() and re.fullmatch(r"\d{1,2}", w) and i + 1 < len(toks) and SL.n(toks[i + 1]) in SL.MONATE \
                            and _tag_belegt(w, toks[i + 1], QN):
                        continue
                    (abgeleitet if r == "abgeleitet" else fehl).append(w)
                    continue
                if len(wt) < 3 or SL.ist_frei(w) or erlaubt_hat(wt, erlaubt):
                    continue
                if vor in POSSESSIV_SIE and wt in FIRMA_NOMEN:
                    continue          # „Ihr Haus“, „Ihr Betrieb“ = die Zielfirma
                if wt in SL.MONATE:
                    if SL.MONATE[wt] in QN.monate or (firma_ok and SL.MONATE[wt] in QF.monate):
                        continue
                    fehl.append(w)
                    continue
                if SL.gedeckt(w, QN) or (partikel and SL.gedeckt(partikel + SL.lemma(w), QN)):
                    continue          # „bereite … vor“ ↔ „fertig machen/vorbereiten“, „rief … an“ ↔ „angerufen“
                if SL.gedeckt(w, QF):
                    if firma_ok:
                        continue
                    nur_firma.append(w)
                    continue
                fehl.append(w)
        if nur_firma:
            meldungen.append(("❌", "In einem Ich-Teilsatz nur aus Anzeige/Firmen-Info belegt: " + ", ".join(dict.fromkeys(nur_firma))
                              + " – die Anzeige belegt nichts über die Person. Nutzer fragen"))
        if fehl:
            meldungen.append(("❌", "Wörter ohne Quelle: " + ", ".join(dict.fromkeys(fehl))
                              + " – hat der Nutzer das gesagt? Sonst streichen oder fragen"))
        if abgeleitet:
            meldungen.append(("⚠️", "Zahl nur abgeleitet (" + ", ".join(f"{x} aus „{QN.abgeleitet.get(x, '')}“" for x in dict.fromkeys(abgeleitet))
                              + ") – kurz bestätigen lassen"))
        if PRIVAT_RE.search(satz):
            if not e.get("privat_ok"):
                meldungen.append(("❌", f"Privates/Gesundheit/Familie („{PRIVAT_RE.search(satz).group(0)}“) nur nach "
                                        "ausdrücklicher Zustimmung (privat_ok: true)"))
            elif t == "anschreiben":
                meldungen.append(("⚠️", "Privates im Anschreiben – im Regelfall weglassen (Nutzer hat zugestimmt)"))
        for sym, m in meldungen:
            befunde.append((sym, t, satz, m))
        sym = "❌" if any(s == "❌" for s, _ in meldungen) else ("⚠️" if meldungen else "✅")
        woher.append((sym, satz, " + ".join(dict.fromkeys(qtext)) if qtext else "–"))
    return befunde, woher


def _tag_belegt(tag, monat, Q):
    """„1. Februar“ ↔ Quelle „1.2.27“ / „01.02.2027“ / „zum 1. februar“."""
    mo = SL.MONATE.get(SL.n(monat))
    return bool(mo and re.search(rf"(?<!\d)0?{int(tag)}\.\s*0?{mo}\.", Q.text)) or \
        bool(re.search(rf"(?<!\d)0?{int(tag)}\.\s*{SL.n(monat)}", SL.n(Q.text)))


def kurz(s, n=8):
    w = (s or "").split()
    return " ".join(w[:n]) + ("…" if len(w) > n else "")


def woher_liste(woher, max_zeilen=12):
    """Kompakte Woher-Liste für die Freigabe: Satzanfang → deine Worte (ohne interne Nummern)."""
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
    print("# Satz-Herkunft (v5) – Fakten wörtlich, Formulierung frei")
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
