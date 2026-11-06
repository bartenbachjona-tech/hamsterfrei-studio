#!/usr/bin/env python3
"""Fügt Anschreiben, Lebenslauf und Anlagen zu EINER PDF zusammen (Reihenfolge = Argumente).

    python3 pdf_zusammenfuegen.py ZIEL.pdf Anschreiben_v2.pdf Lebenslauf_v3.pdf Zeugnis.jpg …
    python3 pdf_zusammenfuegen.py ZIEL.pdf --profil PROFIL.json [--ordner AUSGABE]
          → nimmt automatisch: aktuelles Anschreiben/Motivationsschreiben, aktuellen Lebenslauf,
            dann profil.anlagen (Dateien) in dieser Reihenfolge
    python3 pdf_zusammenfuegen.py --einzeln Datei … [--ausgabe ORDNER]
          → jede Datei als eigene PDF mit sauberem Namen (ohne _vN) nach versand/ (für Formulare,
            die getrennte Dateien wollen)

- Fehlt eine Datei oder klappt eine Umwandlung nicht: ABBRUCH ohne PDF, Exit-Code 2.
- Gibt es eine neuere Fassung (_vN höher, auch aus alt/), wird automatisch die neueste genommen (mit Hinweis).
  --genau schaltet das ab.
- .docx/.odt → PDF per LibreOffice. .jpg/.png/.webp/.heic → auf A4 eingepasst (Pillow; HEIC über
  pillow-heif, wird bei Bedarf per pip installiert).
- Prüft die Zeile „Anlagen: …“ im Anschreiben gegen die wirklich angehängten Dateien (Exit-Code 3 bei
  Abweichung; --trotzdem erzeugt die PDF dennoch).
- ZIEL ohne Ordner → /mnt/user-data/outputs. Ältere Fassung des Ziels → alt/ (nichts wird überschrieben).
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
A4_PX = (1654, 2339)   # A4 bei 200 dpi – lesbar, Datei bleibt klein
RAND_PX = 60
HANDY_HEIC = ("HEIC-Foto (iPhone) ließ sich nicht umwandeln. So geht's: iPhone → Einstellungen → Kamera → "
              "Formate → „Maximale Kompatibilität“ (dann JPG), oder das Foto öffnen, Screenshot machen und den "
              "Screenshot hochladen. Am besten gleich mit der Notizen-App als PDF scannen (Notizen → Kamera → "
              "Dokumente scannen).")


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


def bild_a4(pfad, out):
    from PIL import Image, ImageOps
    img = Image.open(pfad)
    img = ImageOps.exif_transpose(img).convert("RGB")
    breite, hoehe = A4_PX[0] - 2 * RAND_PX, A4_PX[1] - 2 * RAND_PX
    img.thumbnail((breite, hoehe))
    if img.width < breite * 0.5 and img.height < hoehe * 0.5:
        f = min(breite / img.width, hoehe / img.height)
        img = img.resize((int(img.width * f), int(img.height * f)))
    seite = Image.new("RGB", A4_PX, "white")
    seite.paste(img, ((A4_PX[0] - img.width) // 2, (A4_PX[1] - img.height) // 2))
    seite.save(out, "PDF", resolution=200)


def als_pdf(pfad, tmp):
    ext = os.path.splitext(pfad)[1].lower()
    if ext == ".pdf":
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
            bild_a4(pfad, out)
        except Exception as e:
            return None, (HANDY_HEIC if ext in (".heic", ".heif") else f"Bild ließ sich nicht öffnen ({e})")
        return out, None
    return None, f"Dateityp {ext} wird nicht unterstützt (bitte PDF, JPG oder PNG)"


def neueste(pfade, genau, hinweise):
    out = []
    for p in pfade:
        if not genau and os.path.isfile(p):
            neu, n_neu, n = textlib.neueste_version(p)
            if neu != p:
                hinweise.append(f"⚠️ {os.path.basename(p)} ist nicht aktuell – genommen wird die neueste Fassung "
                                f"{os.path.basename(neu)} (v{n_neu}). Mit --genau abschalten.")
                p = neu
            elif os.path.basename(os.path.dirname(os.path.abspath(p))) == "alt":
                hinweise.append(f"⚠️ {os.path.basename(p)} liegt in alt/ (ältere Fassung).")
        out.append(p)
    return out


def aus_profil(profil, ordner):
    d = textlib.lade_profil(profil)
    name = textlib.name_teile((d.get("person") or {}).get("name", ""))
    firma = textlib.safe_name((d.get("ziel") or {}).get("firma", ""), 30, "Firma")
    liste, fehlt = [], []
    if (d.get("anschreiben") or {}).get("absaetze"):
        typ = (d["anschreiben"].get("typ") or "anschreiben").capitalize()
        v = textlib.versionen(ordner, f"{typ}_{name}_{firma}", ".pdf")
        (liste.append(v[max(v)]) if v else fehlt.append(f"{typ}-PDF in {ordner}"))
    if (d.get("lebenslauf") or {}).get("abschnitte"):
        v = textlib.versionen(ordner, f"Lebenslauf_{name}", ".pdf")
        (liste.append(v[max(v)]) if v else fehlt.append(f"Lebenslauf-PDF in {ordner}"))
    for a in (d.get("profil") or {}).get("anlagen") or []:
        liste.append(a.get("datei", ""))
    return liste, fehlt


def anlagen_zeile(pdf_pfad):
    try:
        t = textlib.read_pdf_text(pdf_pfad)[0]
    except RuntimeError:
        return None
    m = re.search(r"Anlagen?:\s*(.+?)(?:\n\s*\n|$)", t, re.S)
    if not m:
        return None
    return [x.strip() for x in re.sub(r"\s+", " ", m.group(1)).split(",") if x.strip()]


def einzeln(dateien, ausgabe):
    ziel_ordner = os.path.join(textlib.ausgabe_ordner(ausgabe), "versand")
    os.makedirs(ziel_ordner, exist_ok=True)
    probleme, hinweise = [], []
    dateien = neueste(dateien, False, hinweise)
    with tempfile.TemporaryDirectory() as tmp:
        fertig = []
        for q in dateien:
            if not os.path.isfile(q):
                probleme.append(f"{q}: nicht gefunden")
                continue
            p, err = als_pdf(q, tmp)
            if err:
                probleme.append(f"{os.path.basename(q)}: {err}")
                continue
            stamm = textlib.basis_und_version(os.path.splitext(os.path.basename(q))[0])[0]
            ziel = os.path.join(ziel_ordner, textlib.safe_name(stamm, 80).replace("-", "_") + ".pdf")
            fertig.append((p, ziel))
        if probleme:
            print("FEHLER – nichts erzeugt:\n" + "\n".join(f"❌ {p}" for p in probleme))
            sys.exit(2)
        for p, ziel in fertig:
            if os.path.exists(ziel):
                alt = os.path.join(ziel_ordner, "alt")
                os.makedirs(alt, exist_ok=True)
                stamm = os.path.splitext(os.path.basename(ziel))[0]
                n = 1
                while os.path.exists(os.path.join(alt, f"{stamm}_alt{n}.pdf")):
                    n += 1
                shutil.move(ziel, os.path.join(alt, f"{stamm}_alt{n}.pdf"))
            shutil.copy(p, ziel)
            print(f"✅ {ziel}")
    for h in hinweise:
        print(h)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    flags = {f for f in ("--genau", "--trotzdem") if f in a}
    a = [x for x in a if x not in flags]
    opts = {}
    for k in ("--profil", "--ordner", "--ausgabe"):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    if a and a[0] == "--einzeln":
        einzeln(a[1:], opts.get("--ausgabe"))
        return
    if not a:
        print(__doc__)
        sys.exit(2)
    ziel, quellen = a[0], a[1:]
    if not ziel.lower().endswith(".pdf"):
        print(f"FEHLER: Das erste Argument muss der Name der Ziel-PDF sein (…pdf), nicht „{ziel}“. "
              "Leerzeichen im Namen? Dann in Anführungszeichen setzen.")
        sys.exit(2)
    hinweise, probleme = [], []
    if opts.get("--profil"):
        try:
            liste, fehlt = aus_profil(opts["--profil"], textlib.ausgabe_ordner(opts.get("--ordner")))
        except RuntimeError as e:
            print(f"FEHLER: {e}")
            sys.exit(2)
        probleme += [f"{f}: nicht gefunden" for f in fehlt]
        quellen = liste + quellen
    if not quellen:
        print("FEHLER: Keine Dateien angegeben.")
        sys.exit(2)
    quellen = neueste(quellen, "--genau" in flags, hinweise)
    ordner = os.path.dirname(ziel) or textlib.ausgabe_ordner(opts.get("--ordner"))
    stamm = textlib.safe_name(os.path.splitext(os.path.basename(ziel))[0], 80).replace("-", "_")
    os.makedirs(os.path.abspath(ordner), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        pdfs = []
        for q in quellen:
            if not q or not os.path.isfile(q):
                probleme.append(f"{q or '(leerer Pfad)'}: nicht gefunden")
                continue
            p, err = als_pdf(q, tmp)
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
        # Anlagen-Zeile prüfen
        abweichung = None
        brief = [p for q, p in pdfs if re.match(r"(Anschreiben|Motivationsschreiben)_", os.path.basename(q))]
        if brief:
            zeile = anlagen_zeile(brief[0])
            angehaengt = len(pdfs) - 1
            if zeile is not None and len(zeile) != angehaengt:
                abweichung = (f"Anlagen-Zeile im Anschreiben nennt {len(zeile)} Anlage(n) ({', '.join(zeile)}), "
                              f"angehängt sind {angehaengt}. Anschreiben neu erzeugen (profil.anlagen) oder Dateien ergänzen.")
        if abweichung and "--trotzdem" not in flags:
            print(f"❌ {abweichung}\nKeine PDF erzeugt (mit --trotzdem trotzdem bauen).")
            sys.exit(3)
        pypdf = pypdf_laden()
        zielpfad = os.path.join(ordner, stamm + ".pdf")
        if os.path.exists(zielpfad):
            alt = os.path.join(ordner, "alt")
            os.makedirs(alt, exist_ok=True)
            n = 1
            while os.path.exists(os.path.join(alt, f"{stamm}_v{n}.pdf")):
                n += 1
            shutil.move(zielpfad, os.path.join(alt, f"{stamm}_v{n}.pdf"))
            hinweise.append(f"Ältere Gesamt-PDF nach alt/{stamm}_v{n}.pdf verschoben.")
        if pypdf:
            w = pypdf.PdfWriter()
            for _, p in pdfs:
                w.append(p)
            with open(zielpfad, "wb") as f:
                w.write(f)
            seiten = len(pypdf.PdfReader(zielpfad).pages)
        elif shutil.which("pdfunite"):
            subprocess.run(["pdfunite", *[p for _, p in pdfs], zielpfad], check=True)
            seiten = None
        else:
            print("FEHLER: Weder pypdf noch pdfunite verfügbar. Ausweg: Dateien einzeln anhängen, wenn erlaubt.")
            sys.exit(2)
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


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except Exception:
        pass
    main()
