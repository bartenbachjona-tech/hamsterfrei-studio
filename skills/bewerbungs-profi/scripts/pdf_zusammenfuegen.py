#!/usr/bin/env python3
"""Bewerbungs-PDFs bauen: eine Gesamt-PDF, saubere Einzeldateien oder N Bündel (Upload-Limit).

    python3 pdf_zusammenfuegen.py ZIEL.pdf Anschreiben_….pdf Lebenslauf_….pdf Zeugnis.jpg …
    python3 pdf_zusammenfuegen.py ZIEL.pdf --profil PROFIL.json [--ordner AUSGABE]
          → aktuelles Anschreiben/Motivationsschreiben, aktueller Lebenslauf, dann profil.anlagen
    python3 pdf_zusammenfuegen.py --einzeln --profil PROFIL.json [--ausgabe ORDNER]
    python3 pdf_zusammenfuegen.py --einzeln DATEI … [--name DATEI=Bezeichnung …] [--ausgabe ORDNER]
          → jede Datei als eigene PDF mit sprechendem Namen (Bezeichnung aus profil.anlagen statt IMG_4471),
            flach im Ausgabeordner (kein Unterordner – am Handy gibt es keine Ordner) + Liste „Hochladen: …“
    python3 pdf_zusammenfuegen.py --buendeln N --profil PROFIL.json [--ordner QUELLE] [--ausgabe ORDNER]
          → Upload-Limit „max. N Dateien“: Anschreiben (bzw. Motivationsschreiben), Lebenslauf einzeln, alle
            Anlagen gebündelt (N=2: Lebenslauf + Anschreiben&Anlagen; N=1: alles in einer PDF)
- Quellen (…_AKTUELL.pdf) werden in --ordner, sonst in --ausgabe, sonst im Standard-Ausgabeordner gesucht –
  im ersten Ordner, in dem sie liegen. --ausgabe ist nur das Ziel.
- --einzeln/--buendeln im selben Ordner: die Arbeitsdateien …_AKTUELL.pdf wandern danach nach alt/ – am Handy
  liegt so nur EINE Datei je Unterlage im Ordner (die saubere zum Hochladen).

- ZIEL-Name wird genau so verwendet (Bindestriche bleiben). Nur Umlaute/Leerzeichen/Sonderzeichen werden
  ersetzt – mit klarer Meldung.
- Fehlt eine Datei oder klappt eine Umwandlung nicht: ABBRUCH ohne PDF, Exit-Code 2.
- Neuere Fassung vorhanden (…_AKTUELL bzw. höheres _vN, auch wenn der Pfad in alt/ zeigt oder nicht mehr
  existiert): die aktuelle wird genommen (mit Hinweis). --genau schaltet das ab.
- Bilder (.jpg/.png/.webp/.heic) → A4; Querformat-Fotos werden gedreht (Texterkennung, wenn vorhanden) oder auf
  eine A4-Querseite eingepasst; --drehen DATEI=90|180|270 dreht von Hand. PDF-Anlagen in anderem Format
  (Letter, Scan-Größe) werden auf A4 skaliert.
- Anlagen-Zeile im Anschreiben ≠ angehängte Anlagen: mit --profil wird das Anschreiben automatisch neu
  erzeugt (nur die Anlagen-Zeile ändert sich); sonst Exit 3 (--trotzdem baut dennoch).
- Ausgabe ohne Ordner → /mnt/user-data/outputs. Gleichnamige ältere Datei → alt/ (nichts wird überschrieben).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textlib  # noqa: E402

MAX_MB = 5
A4_PX = (1654, 2339)   # A4 bei 200 dpi
A4_PT = (595.28, 841.89)
RAND_PX = 60
HANDY_HEIC = ("HEIC-Foto (iPhone) ließ sich nicht umwandeln. So geht's: iPhone → Einstellungen → Kamera → "
              "Formate → „Maximale Kompatibilität“ (dann JPG), oder das Foto öffnen, Screenshot machen und den "
              "Screenshot hochladen. Am besten gleich mit der Notizen-App als PDF scannen (Notizen → Kamera → "
              "Dokumente scannen).")
KAMERA_NAME = re.compile(r"^(img|pxl|dsc|dcim|photo|foto|bild|image|scan|screenshot|whatsapp)[_\- ]?\d", re.I)


def pip_install(paket):
    for extra in ([], ["--break-system-packages"]):
        if subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", paket, *extra],
                          capture_output=True).returncode == 0:
            return True
    return False


def pypdf_laden():
    try:
        import pypdf
        return pypdf
    except ImportError:
        pip_install("pypdf")
        try:
            import pypdf
            return pypdf
        except ImportError:
            return None


def heic_oeffner():
    try:
        import pillow_heif
    except ImportError:
        if not pip_install("pillow-heif"):
            return False
        try:
            import pillow_heif
        except ImportError:
            return False
    pillow_heif.register_heif_opener()
    return True


def dateiname(roh):
    """Exakter Name, wenn er schon sauber ist; sonst nur Problemzeichen ersetzen (Bindestrich bleibt)."""
    stamm, ext = os.path.splitext(os.path.basename(roh))
    if re.fullmatch(r"[A-Za-z0-9_.\-]+", stamm):
        return stamm + ".pdf", None
    neu = re.sub(r"\s+", "_", textlib.translit(stamm).strip())
    neu = re.sub(r"[^A-Za-z0-9_.\-]", "", neu).strip("_-") or "Bewerbung"
    return neu + ".pdf", f"ℹ️ Dateiname angepasst (Umlaute/Leerzeichen/Sonderzeichen machen in Portalen Ärger): „{stamm}{ext}“ → „{neu}.pdf“"


def osd_drehung(img):
    """Drehwinkel per Texterkennung (tesseract --psm 0), wenn vorhanden und sicher; sonst None."""
    if not shutil.which("tesseract"):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "x.png")
        k = img.copy()
        k.thumbnail((1600, 1600))
        k.save(p)
        try:
            r = subprocess.run(["tesseract", p, "-", "--psm", "0"], capture_output=True, text=True, timeout=40)
        except Exception:
            return None
    m = re.search(r"Rotate:\s*(\d+)", r.stdout)
    c = re.search(r"Orientation confidence:\s*([\d.]+)", r.stdout)
    if m and c and float(c.group(1)) >= 2.0:
        return int(m.group(1))
    return None


def bild_a4(pfad, out, drehen=None, hinweise=None):
    from PIL import Image, ImageOps
    img = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")
    name = os.path.basename(pfad)
    if drehen:
        img = img.rotate(-int(drehen), expand=True)
    elif img.width > img.height * 1.05:
        winkel = osd_drehung(img)
        if winkel:
            img = img.rotate(-winkel, expand=True)
            if hinweise is not None:
                hinweise.append(f"↻ {name}: lag quer – um {winkel}° gedreht (Texterkennung). Bitte Seite ansehen.")
    quer = img.width > img.height * 1.05
    seite_px = (A4_PX[1], A4_PX[0]) if quer else A4_PX
    if quer and hinweise is not None and not drehen:
        hinweise.append(f"⚠️ {name}: Querformat → auf eine A4-Querseite eingepasst (groß und lesbar). Liegt der Text auf "
                        f"der Seite? Dann neu bauen mit --drehen {name}=90 (oder 270) – oder mit der Scan-App neu aufnehmen.")
    breite, hoehe = seite_px[0] - 2 * RAND_PX, seite_px[1] - 2 * RAND_PX
    f = min(breite / img.width, hoehe / img.height)
    img = img.resize((max(1, int(img.width * f)), max(1, int(img.height * f))))
    seite = Image.new("RGB", seite_px, "white")
    seite.paste(img, ((seite_px[0] - img.width) // 2, (seite_px[1] - img.height) // 2))
    seite.save(out, "PDF", resolution=200)


def pdf_auf_a4(pfad, out, pypdf):
    """Seiten, die nicht A4 sind, auf A4 (hoch/quer passend) skalieren und zentrieren. → (pfad, geändert?)"""
    r = pypdf.PdfReader(pfad)
    geaendert = False
    w = pypdf.PdfWriter()
    for pg in r.pages:
        bw, bh = float(pg.mediabox.width), float(pg.mediabox.height)
        if pg.get("/Rotate") in (90, 270):
            bw, bh = bh, bw
        quer = bw > bh
        zw, zh = (A4_PT[1], A4_PT[0]) if quer else A4_PT
        if abs(bw - zw) < 3 and abs(bh - zh) < 3:
            w.add_page(pg)
            continue
        geaendert = True
        pg.transfer_rotation_to_content()
        bw, bh = float(pg.mediabox.width), float(pg.mediabox.height)
        s = min(zw / bw, zh / bh)
        neu = pypdf.PageObject.create_blank_page(width=zw, height=zh)
        tx = (zw - bw * s) / 2 - float(pg.mediabox.left) * s
        ty = (zh - bh * s) / 2 - float(pg.mediabox.bottom) * s
        neu.merge_transformed_page(pg, pypdf.Transformation().scale(s, s).translate(tx, ty))
        w.add_page(neu)
    if not geaendert:
        return pfad, False
    with open(out, "wb") as f:
        w.write(f)
    return out, True


def als_pdf(pfad, tmp, drehen=None, hinweise=None, anlage=False):
    ext = os.path.splitext(pfad)[1].lower()
    if ext == ".pdf":
        if anlage:
            pypdf = pypdf_laden()
            if pypdf:
                try:
                    neu, geaendert = pdf_auf_a4(pfad, os.path.join(tmp, "a4_" + os.path.basename(pfad)), pypdf)
                    if geaendert and hinweise is not None:
                        hinweise.append(f"ℹ️ {os.path.basename(pfad)}: Seitenformat war nicht A4 – auf A4 skaliert.")
                    return neu, None
                except Exception as e:
                    return None, f"PDF ließ sich nicht lesen ({e}) – passwortgeschützt? Bitte neu scannen/speichern."
        return pfad, None
    if ext in (".docx", ".doc", ".odt", ".rtf", ".txt"):
        so = shutil.which("soffice") or shutil.which("libreoffice")
        if not so:
            return None, "LibreOffice fehlt – diese Datei bitte selbst als PDF speichern"
        r = subprocess.run([so, "--headless", "--convert-to", "pdf", "--outdir", tmp, pfad],
                           capture_output=True, text=True, timeout=180, env=dict(os.environ, HOME=tmp))
        out = os.path.join(tmp, os.path.splitext(os.path.basename(pfad))[0] + ".pdf")
        return (out, None) if r.returncode == 0 and os.path.isfile(out) else (None, "Umwandlung in PDF fehlgeschlagen")
    if ext in (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"):
        try:
            import PIL  # noqa: F401
        except ImportError:
            if not pip_install("pillow"):
                return None, "Pillow fehlt – Bild bitte als PDF scannen (Handy-Scan-App)"
        if ext in (".heic", ".heif") and not heic_oeffner():
            return None, HANDY_HEIC
        out = os.path.join(tmp, os.path.basename(pfad) + ".pdf")
        try:
            bild_a4(pfad, out, drehen, hinweise)
        except Exception as e:
            return None, (HANDY_HEIC if ext in (".heic", ".heif") else f"Bild ließ sich nicht öffnen ({e})")
        return out, None
    return None, f"Dateityp {ext} wird nicht unterstützt (bitte PDF, JPG oder PNG)"


def neueste(pfade, genau, hinweise):
    out = []
    for p in pfade:
        if not genau and p:
            neu, n_neu, n = textlib.neueste_version(p)
            if neu != p:
                hinweise.append(f"⚠️ {os.path.basename(p)} ist nicht (mehr) die aktuelle Fassung – genommen wird "
                                f"{os.path.basename(neu)}. Mit --genau abschalten.")
                p = neu
            elif os.path.basename(os.path.dirname(os.path.abspath(p))) == "alt":
                hinweise.append(f"⚠️ {os.path.basename(p)} liegt in alt/ (ältere Fassung).")
        out.append(p)
    return out


def quell_ordner(profil, kandidaten):
    """Erster Ordner, in dem die Unterlagen-PDFs (auch in alt/) liegen – v3-Fehler: Suche nur im Ausgabeordner."""
    kandidaten = [k for k in dict.fromkeys(kandidaten) if k]
    for k in kandidaten:
        doks, _, fehlt, _ = profil_dateien(profil, k)
        if doks and not fehlt:
            return k
    return kandidaten[0] if kandidaten else textlib.ausgabe_ordner()


def profil_dateien(profil, ordner):
    """→ (dokumente [(pfad, bezeichnung, art)], anlagen [(pfad, bezeichnung)], fehlt, d)."""
    d = textlib.lade_profil(profil)
    name = textlib.name_teile((d.get("person") or {}).get("name", ""))
    firma = textlib.safe_name((d.get("ziel") or {}).get("firma", ""), 30, "Firma")
    doks, fehlt = [], []
    if (d.get("anschreiben") or {}).get("absaetze"):
        typ = (d["anschreiben"].get("typ") or "anschreiben").capitalize()
        v = textlib.versionen(ordner, f"{typ}_{name}_{firma}", ".pdf")
        (doks.append((v[max(v)], typ, "brief")) if v else fehlt.append(f"{typ}-PDF in {ordner} (erst erzeugen)"))
    if (d.get("lebenslauf") or {}).get("abschnitte"):
        v = textlib.versionen(ordner, f"Lebenslauf_{name}", ".pdf")
        (doks.append((v[max(v)], "Lebenslauf", "lebenslauf")) if v else fehlt.append(f"Lebenslauf-PDF in {ordner} (erst erzeugen)"))
    anl = [(a.get("datei", ""), a.get("bezeichnung") or "") for a in (d.get("profil") or {}).get("anlagen") or []]
    return doks, anl, fehlt, d


def anlagen_zeile(pdf_pfad):
    try:
        t = textlib.read_pdf_text(pdf_pfad)[0]
    except RuntimeError:
        return None
    m = re.search(r"Anlagen?:\s*(.+?)(?:\n\s*\n|$)", t, re.S)
    if not m:
        return None
    return [x.strip() for x in re.sub(r"\s+", " ", m.group(1)).split(",") if x.strip()]


def anschreiben_neu(profil, ordner):
    """Anschreiben neu erzeugen (Anlagen-Zeile nachziehen). → True bei Erfolg."""
    hier = os.path.dirname(os.path.abspath(__file__))
    geraet = ((textlib.lade_profil(profil).get("meta") or {}).get("geraet") or "").lower()
    extra = [] if geraet in ("pc", "computer", "laptop", "desktop") else ["--nur-pdf"]
    r = subprocess.run([sys.executable, os.path.join(hier, "unterlagen_erstellen.py"), profil, "--nur", "anschreiben",
                        *extra, "--ausgabe", ordner], capture_output=True, text=True)
    return r.returncode == 0


def ablegen(quelle, ziel):
    """Kopiert nach ziel; gleichnamige ältere Datei → alt/…_altN.pdf. Nichts wird überschrieben."""
    if os.path.exists(ziel):
        alt = os.path.join(os.path.dirname(ziel), "alt")
        os.makedirs(alt, exist_ok=True)
        stamm = os.path.splitext(os.path.basename(ziel))[0]
        n = 1
        while os.path.exists(os.path.join(alt, f"{stamm}_alt{n}.pdf")):
            n += 1
        shutil.move(ziel, os.path.join(alt, f"{stamm}_alt{n}.pdf"))
    shutil.copy(quelle, ziel)


def zusammen(pdfs, ziel, pypdf):
    if pypdf:
        w = pypdf.PdfWriter()
        for p in pdfs:
            w.append(p)
        with open(ziel, "wb") as f:
            w.write(f)
        return len(pypdf.PdfReader(ziel).pages)
    if shutil.which("pdfunite"):
        subprocess.run(["pdfunite", *pdfs, ziel], check=True)
        return None
    print("FEHLER: Weder pypdf noch pdfunite verfügbar. Ausweg: Dateien einzeln anhängen, wenn erlaubt.")
    sys.exit(2)


def einzeln(eintraege, ausgabe, name, drehen, hinweise):
    """eintraege: [(pfad, bezeichnung, ist_anlage)] → saubere Einzel-PDFs flach in ausgabe."""
    ziel_ordner = textlib.ausgabe_ordner(ausgabe)
    os.makedirs(ziel_ordner, exist_ok=True)
    probleme, fertig, namen = [], [], set()
    with tempfile.TemporaryDirectory() as tmp:
        for i, (q, bez, anlage) in enumerate(eintraege, 1):
            if not q or not os.path.isfile(q):
                probleme.append(f"{q or '(leerer Pfad)'}: nicht gefunden")
                continue
            p, err = als_pdf(q, tmp, drehen.get(os.path.basename(q)), hinweise, anlage)
            if err:
                probleme.append(f"{os.path.basename(q)}: {err}")
                continue
            stamm = textlib.basis_und_version(os.path.splitext(os.path.basename(q))[0])[0]
            if bez:
                teil = textlib.safe_name(bez, 70).replace("-", "_")
                stamm = f"{teil}_{name}" if name and name.split("_")[-1] not in teil else teil
            elif KAMERA_NAME.match(stamm):
                stamm = f"Anlage_{i}_{name}" if name else f"Anlage_{i}"
                hinweise.append(f"⚠️ {os.path.basename(q)}: keine Bezeichnung – heißt jetzt {stamm}.pdf "
                                f"(besser: --name {os.path.basename(q)}=\"Zeugnis 10. Klasse\" oder profil.anlagen)")
            else:
                stamm = re.sub(r"[^A-Za-z0-9_.\-]", "", textlib.translit(stamm).replace(" ", "_"))
            z, n = stamm, 2
            while z in namen:
                z, n = f"{stamm}_{n}", n + 1
            namen.add(z)
            fertig.append((p, os.path.join(ziel_ordner, z + ".pdf")))
        if probleme:
            print("FEHLER – nichts erzeugt:\n" + "\n".join(f"❌ {p}" for p in probleme))
            sys.exit(2)
        for p, ziel in fertig:
            ablegen(p, ziel)
    print("✅ Fertig. 📤 Diese Dateien hochladen/anhängen (in dieser Reihenfolge):")
    for i, (_, ziel) in enumerate(fertig, 1):
        print(f"   {i}. {os.path.basename(ziel)}")
    print(f"Ordner: {ziel_ordner}")
    return [z for _, z in fertig]


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    flags = {f for f in ("--genau", "--trotzdem", "--einzeln") if f in a}
    a = [x for x in a if x not in flags]
    opts, namen_map, drehen = {}, {}, {}
    for k in ("--profil", "--ordner", "--ausgabe", "--buendeln"):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    for k, ziel in (("--name", namen_map), ("--drehen", drehen)):
        while k in a:
            i = a.index(k)
            datei, _, wert = a[i + 1].partition("=")
            ziel[os.path.basename(datei)] = wert
            del a[i:i + 2]
    hinweise = []
    d, doks, anl = None, [], []
    ordner_q = textlib.ausgabe_ordner(opts.get("--ordner") or opts.get("--ausgabe"))
    if opts.get("--profil"):
        try:
            ordner_q = quell_ordner(opts["--profil"], [opts.get("--ordner"), opts.get("--ausgabe"), textlib.ausgabe_ordner()])
            doks, anl, fehlt, d = profil_dateien(opts["--profil"], ordner_q)
        except RuntimeError as e:
            print(f"FEHLER: {e}")
            sys.exit(2)
        if fehlt:
            print("FEHLER – nichts erzeugt:\n" + "\n".join(f"❌ {f}" for f in fehlt))
            sys.exit(2)
    name = textlib.name_teile((d.get("person") or {}).get("name", "")) if d else ""

    # Anlagen-Zeile prüfen (Brief + Profil): bei Abweichung Anschreiben automatisch neu
    an = (d or {}).get("anschreiben") or {}
    zeile_soll = an.get("anlagen_zeile")
    if zeile_soll is None:
        zeile_soll = (an.get("typ") or "anschreiben") != "kurzanschreiben"
    if d and doks and doks[0][2] == "brief" and zeile_soll:
        zeile = anlagen_zeile(doks[0][0]) or []
        vorhanden = [b for p, b in anl if p and os.path.isfile(p)]
        soll = (1 if any(x[2] == "lebenslauf" for x in doks) else 0) + len(vorhanden)
        if zeile and len(zeile) != soll or (not zeile and vorhanden):
            if anschreiben_neu(opts["--profil"], ordner_q):
                doks, anl, _, d = profil_dateien(opts["--profil"], ordner_q)
                hinweise.append("🔁 Anlagen-Zeile passte nicht zu den Anlagen → Anschreiben automatisch neu erzeugt "
                                "(nur die Anlagen-Zeile hat sich geändert).")

    if "--einzeln" in flags or opts.get("--buendeln"):
        if d:
            eintraege = [(p, b, False) for p, b, _ in doks] + [(p, b, True) for p, b in anl]
        else:
            eintraege = [(p, namen_map.get(os.path.basename(p), ""), not re.match(r"(Anschreiben|Motivationsschreiben|Kurzanschreiben|Lebenslauf)_", os.path.basename(p)))
                         for p in a]
        if not eintraege:
            print("FEHLER: Keine Dateien angegeben.")
            sys.exit(2)
        eintraege = [(neueste([p], "--genau" in flags, hinweise)[0], b, an) for p, b, an in eintraege]
        if opts.get("--buendeln"):
            n = int(opts["--buendeln"])
            ziele = buendel(eintraege, n, opts.get("--ausgabe"), name, drehen, hinweise)
        else:
            ziele = einzeln(eintraege, opts.get("--ausgabe"), name, drehen, hinweise)
        # keine zwei gleichen Dateien am Handy: Arbeitsdateien im selben Ordner nach alt/
        ziel_ordner = os.path.abspath(textlib.ausgabe_ordner(opts.get("--ausgabe")))
        for p, _, anlage in eintraege:
            if not anlage and ziele and os.path.dirname(os.path.abspath(p)) == ziel_ordner and \
                    textlib.basis_und_version(os.path.splitext(os.path.basename(p))[0])[1] == textlib.N_AKTUELL:
                textlib.aktuell_archivieren(p)
        for h in hinweise:
            print(h)
        return

    if not a:
        print(__doc__)
        sys.exit(2)
    ziel_roh, quellen = a[0], a[1:]
    if not ziel_roh.lower().endswith(".pdf"):
        print(f"FEHLER: Das erste Argument muss der Name der Ziel-PDF sein (…pdf), nicht „{ziel_roh}“. "
              "Leerzeichen im Namen? Dann in Anführungszeichen setzen.")
        sys.exit(2)
    eintraege = [(p, b, False) for p, b, _ in doks] + [(p, b, True) for p, b in anl]
    eintraege += [(q, "", not re.match(r"(Anschreiben|Motivationsschreiben|Kurzanschreiben|Lebenslauf)_", os.path.basename(q)))
                  for q in quellen]
    if not eintraege:
        print("FEHLER: Keine Dateien angegeben.")
        sys.exit(2)
    eintraege = [(neueste([p], "--genau" in flags, hinweise)[0], b, an) for p, b, an in eintraege]
    ordner = os.path.dirname(ziel_roh) or textlib.ausgabe_ordner(opts.get("--ordner"))
    fname, meldung = dateiname(ziel_roh)
    if meldung:
        hinweise.insert(0, meldung)
    os.makedirs(os.path.abspath(ordner), exist_ok=True)
    zielpfad = os.path.join(ordner, fname)
    probleme, pdfs = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for q, _, anlage in eintraege:
            if not q or not os.path.isfile(q):
                probleme.append(f"{q or '(leerer Pfad)'}: nicht gefunden")
                continue
            p, err = als_pdf(q, tmp, drehen.get(os.path.basename(q)), hinweise, anlage)
            if err:
                probleme.append(f"{os.path.basename(q)}: {err}")
            else:
                pdfs.append((q, p))
        if probleme:
            print("FEHLER – keine PDF erzeugt, weil etwas fehlt:")
            for p in probleme:
                print(f"❌ {p}")
            print("Fehlende Datei hochladen lassen (oder aus der Liste nehmen), dann neu starten.")
            sys.exit(2)
        abweichung = None
        brief = [p for q, p in pdfs if re.match(r"(Anschreiben|Motivationsschreiben)_", os.path.basename(q))]
        if brief:
            zeile = anlagen_zeile(brief[0])
            angehaengt = len(pdfs) - 1
            if zeile is not None and len(zeile) != angehaengt:
                abweichung = (f"Anlagen-Zeile im Anschreiben nennt {len(zeile)} Anlage(n) ({', '.join(zeile)}), "
                              f"angehängt sind {angehaengt}. Mit --profil wird das Anschreiben automatisch angepasst; "
                              f"sonst profil.anlagen ergänzen und Anschreiben neu erzeugen.")
        if abweichung and "--trotzdem" not in flags:
            print(f"❌ {abweichung}\nKeine PDF erzeugt (mit --trotzdem trotzdem bauen).")
            sys.exit(3)
        tmpziel = os.path.join(tmp, "gesamt.pdf")
        seiten = zusammen([p for _, p in pdfs], tmpziel, pypdf_laden())
        ablegen(tmpziel, zielpfad)
    mb = os.path.getsize(zielpfad) / 1024 / 1024
    print(f"✅ PDF: {zielpfad}")
    print("Reihenfolge: " + " → ".join(os.path.basename(q) for q, _ in pdfs))
    print(f"Seiten: {seiten if seiten else '?'} | Größe: {mb:.2f} MB")
    if mb > MAX_MB:
        print(f"⚠️ Größer als {MAX_MB} MB – Scans kleiner speichern oder weniger Anlagen (nur relevante Zeugnisse).")
    if abweichung:
        print(f"⚠️ {abweichung}")
    for h in hinweise:
        print(h)


def buendel(eintraege, n, ausgabe, name, drehen, hinweise):
    """Upload-Limit „max. N Dateien“: Rezept – Briefe/Lebenslauf einzeln, Anlagen gebündelt."""
    if n < 1:
        print("FEHLER: --buendeln braucht eine Zahl ≥ 1.")
        sys.exit(2)
    brief = [e for e in eintraege if not e[2] and re.match(r"(anschreiben|motivationsschreiben|kurzanschreiben)", (e[1] or os.path.basename(e[0])).lower())]
    ll = [e for e in eintraege if not e[2] and e not in brief]
    anl = [e for e in eintraege if e[2]]
    ordner = textlib.ausgabe_ordner(ausgabe)
    os.makedirs(ordner, exist_ok=True)
    # Name des Briefs wie er ist (v3-Fehler: Motivationsschreiben hieß „Anschreiben_…“)
    wort = "Anschreiben"
    if brief:
        m = re.match(r"(anschreiben|motivationsschreiben|kurzanschreiben)", (brief[0][1] or os.path.basename(brief[0][0])).lower())
        wort = m.group(1).capitalize()
    gruppen = []
    if n == 1:
        gruppen = [("Bewerbung", brief + ll + anl)]
    elif n == 2:
        gruppen = [("Lebenslauf", ll), (f"{wort}_und_Anlagen" if brief else "Anlagen", brief + anl)]
    else:
        gruppen = [(wort, brief), ("Lebenslauf", ll), ("Anlagen", anl)]
    gruppen = [(g, e) for g, e in gruppen if e]
    pypdf = pypdf_laden()
    probleme, fertig = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for g, elem in gruppen:
            pdfs = []
            for q, _, anlage in elem:
                if not os.path.isfile(q):
                    probleme.append(f"{q}: nicht gefunden")
                    continue
                p, err = als_pdf(q, tmp, drehen.get(os.path.basename(q)), hinweise, anlage)
                (probleme.append(f"{os.path.basename(q)}: {err}") if err else pdfs.append(p))
            if probleme:
                continue
            tz = os.path.join(tmp, f"{g}.pdf")
            zusammen(pdfs, tz, pypdf)
            fertig.append((tz, os.path.join(ordner, f"{g}_{name}.pdf" if name else f"{g}.pdf")))
        if probleme:
            print("FEHLER – nichts erzeugt:\n" + "\n".join(f"❌ {p}" for p in probleme))
            sys.exit(2)
        for t, z in fertig:
            ablegen(t, z)
    print(f"✅ {len(fertig)} Datei(en) für „max. {n} Dateien“. 📤 Hochladen:")
    for i, (_, z) in enumerate(fertig, 1):
        print(f"   {i}. {os.path.basename(z)}")
    return [z for _, z in fertig]


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
