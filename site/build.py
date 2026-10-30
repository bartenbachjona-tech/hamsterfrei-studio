"""Baut die öffentliche Seite (mehrseitig) nach ../../hamsterfrei-site (GitHub Pages)
und eine Vorschau nach site/_preview (für das Artifact).

Aufruf: python3 build.py
Preise und Kauf-Links stehen unten in PRODUCTS. Leerer Link = Button „Bald verfügbar“.
"""
import html, pathlib, re, shutil

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent.parent / "hamsterfrei-site"
PREVIEW = HERE / "_preview"

PRODUCTS = {
    "anzeigen": {"price": "9,90 €", "buy": "https://www.checkout-ds24.com/product/757063"},
    "seminar": {"price": "9,90 €", "buy": "https://www.checkout-ds24.com/product/757079"},
}
PAGE_PRODUCT = {"anzeigen-profi": "anzeigen", "seminararbeit-profi": "seminar"}
NAV = [("start", "index.html", "Alle Skills"), ("seminar", "seminararbeit-profi.html", "Seminararbeit"), ("anzeigen", "anzeigen-profi.html", "Anzeigen")]

FONTFACE = """@font-face{font-family:"Fredoka";src:url(fonts/fredoka-latin.woff2) format("woff2");font-weight:300 700;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Fredoka";src:url(fonts/fredoka-latin-ext.woff2) format("woff2");font-weight:300 700;font-display:swap;unicode-range:U+0100-024F,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:"Nunito Sans";src:url(fonts/nunito-latin.woff2) format("woff2");font-weight:200 1000;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Nunito Sans";src:url(fonts/nunito-latin-ext.woff2) format("woff2");font-weight:200 1000;font-display:swap;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C4}
"""
THUMBS = (
 '<svg viewBox="0 0 64 64"><path d="M16 38V30a16 16 0 0 1 32 0v8" fill="none" stroke="#2B2B2E" stroke-width="5" stroke-linecap="round"/><rect x="10" y="34" width="12" height="18" rx="6" fill="#2B2B2E"/><rect x="42" y="34" width="12" height="18" rx="6" fill="#2B2B2E"/></svg>'
 '<svg viewBox="0 0 64 64"><ellipse cx="32" cy="34" rx="22" ry="16" fill="#3A3A3E"/><path d="M12 32q20 -8 40 0" fill="none" stroke="#8A8A90" stroke-width="2" stroke-dasharray="3 3"/><rect x="28" y="22" width="8" height="5" rx="2" fill="#8A8A90"/></svg>'
 '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" fill="#2B2B2E"/><circle cx="32" cy="32" r="11" fill="#55555A"/><path d="M18 22l4 3M44 40l3 3M20 42l3-2" stroke="#9A9AA0" stroke-width="2" stroke-linecap="round"/></svg>'
)


def icon(path):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + '</svg>'


ICONS = {
 '{{ICON_FILE}}': icon('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 11v6M9 14l3 3 3-3"/>'),
 '{{ICON_DOC}}': icon('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
 '{{ICON_CHECK}}': icon('<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>'),
 '{{ICON_USER}}': icon('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
 '{{ICON_TOGGLE}}': icon('<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="16" cy="12" r="3"/>'),
 '{{ICON_CAM}}': icon('<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="14" r="4"/>'),
 '{{ICON_CLOCK}}': icon('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 '{{ICON_CAP}}': icon('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/>'),
 '{{ICON_TAG}}': icon('<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>'),
 '{{ICON_PLUS}}': icon('<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'),
}

CSS = (HERE / "site.base.css").read_text() + (HERE / "site.extra.css").read_text()
LEGAL_CSS = (HERE / "legal.css").read_text()

FOOTER = """<footer class="wrap">
  <nav aria-label="Rechtliches"><a href="index.html">Alle Skills</a><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a><a href="kaufbedingungen.html">Kaufbedingungen</a></nav>
  <p>© 2026 Hamsterfrei · Folg dem Hamster auf <a href="https://www.tiktok.com/@hamsterfrei" rel="noopener" target="_blank">TikTok</a>, <a href="https://www.instagram.com/hamsterfrei/" rel="noopener" target="_blank">Instagram</a> und <a href="https://www.youtube.com/channel/UCBmT3RjRK5PGk-YVTdFzuDA" rel="noopener" target="_blank">YouTube</a>. Claude ist eine Marke von Anthropic; Hamsterfrei ist nicht mit Anthropic verbunden.</p>
</footer>"""

BAR_JS = """<script>
(function(){
  var bar=document.getElementById('bar'), box=document.getElementById('kaufen');
  if(!('IntersectionObserver' in window)||!bar||!box) return;
  new IntersectionObserver(function(e){ bar.classList.toggle('show', !e[0].isIntersecting && e[0].boundingClientRect.top<0); }).observe(box);
})();
</script>"""


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>' for key, href, label in NAV
    )
    return (f'<header class="wrap top"><a class="brand" href="index.html" aria-label="Hamsterfrei – Startseite">'
            f'<img src="hamster.png" alt=""><b>Hamster<span>frei</span></b></a><nav aria-label="Skills">{links}</nav></header>')


def price_html(p):
    return p.replace(" ", "&nbsp;")


def fill(s, product):
    rep = dict(ICONS)
    rep["{{THUMBS}}"] = THUMBS
    rep["{{HAMSTER}}"] = "hamster.png"
    rep["{{HAMSTER_CUT}}"] = "hamster-cut.png"
    rep["{{PRICE_ANZEIGEN}}"] = price_html(PRODUCTS["anzeigen"]["price"])
    rep["{{PRICE_SEMINAR}}"] = price_html(PRODUCTS["seminar"]["price"])
    if product:
        pr = PRODUCTS[product]
        rep["{{PRICE}}"] = price_html(pr["price"])
        rep["{{BUY_URL}}"] = pr["buy"] or "#kaufen"
        rep["{{BUY_CLASS}}"] = "" if pr["buy"] else "soon"
        rep["{{BUY_ATTRS}}"] = 'rel="noopener" target="_blank"' if pr["buy"] else 'aria-disabled="true"'
        rep["{{BUY_LABEL}}"] = f'Für {pr["price"]} kaufen' if pr["buy"] else "Bald verfügbar"
    for k, v in rep.items():
        s = s.replace(k, v)
    assert "{{" not in s, re.findall(r"{{\w+}}", s)
    return s


def doc(title, desc, css, body):
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<script>if(location.protocol==="http:"&&/hamsterfrei\\.de$/.test(location.hostname))location.replace("https://hamsterfrei.de"+location.pathname+location.search+location.hash)</script>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n'
            '<link rel="icon" href="hamster.png">\n'
            f'<style>\n{FONTFACE}{css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')


def build_pages():
    pages = {}
    for src in sorted((HERE / "pages").glob("*.src.html")):
        name = src.name.replace(".src.html", "")
        raw = src.read_text()
        m = re.match(r"<!--meta\n(.*?)\n-->\n", raw, re.S)
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
        body = raw[m.end():]
        product = PAGE_PRODUCT.get(name)
        full = header(meta["nav"]) + "\n" + fill(body, product) + "\n" + FOOTER + ("\n" + BAR_JS if 'id="bar"' in body else "")
        pages[f"{name}.html"] = doc(meta["title"], meta["description"], CSS, full)
    for name in ["impressum", "datenschutz", "kaufbedingungen"]:
        body = (HERE / f"{name}.src.html").read_text().replace('href="index.html">← Zurück zu Hamsterfrei', 'href="index.html">← Zurück zu Hamsterfrei')
        pages[f"{name}.html"] = doc(f"{name.capitalize()} · Hamsterfrei", "Hamsterfrei – " + name.capitalize(), LEGAL_CSS, body)
    return pages


def write(target, pages):
    target.mkdir(exist_ok=True)
    (target / "fonts").mkdir(exist_ok=True)
    for f in (OUT / "fonts").glob("*.woff2") if target != OUT else []:
        shutil.copy(f, target / "fonts" / f.name)
    for img in ["hamster.png", "hamster-cut.png"]:
        shutil.copy(HERE / img, target / img)
    for n, c in pages.items():
        (target / n).write_text(c)


pages = build_pages()
write(OUT, pages)
write(PREVIEW, pages)
print("ok:", ", ".join(pages), "| Kauf-Links:", {k: (v["buy"] or "–") for k, v in PRODUCTS.items()})
