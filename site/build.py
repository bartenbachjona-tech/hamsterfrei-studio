"""Baut die öffentliche Seite nach ../../hamsterfrei-site (GitHub Pages) bzw. eine Artifact-Vorschau.
Aufruf: python3 build.py [BUY_URL]"""
import base64, html, sys, pathlib, re
HERE = pathlib.Path(__file__).parent
OUT = HERE.parent.parent / "hamsterfrei-site"
BUY = sys.argv[1] if len(sys.argv) > 1 else ""

FONTFACE = """@font-face{font-family:"Fredoka";src:url(fonts/fredoka-latin.woff2) format("woff2");font-weight:300 700;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Fredoka";src:url(fonts/fredoka-latin-ext.woff2) format("woff2");font-weight:300 700;font-display:swap;unicode-range:U+0100-024F,U+1E00-1EFF,U+20A0-20AB,U+20AD-20CF}
@font-face{font-family:"Nunito Sans";src:url(fonts/nunito-latin.woff2) format("woff2");font-weight:200 1000;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Nunito Sans";src:url(fonts/nunito-latin-ext.woff2) format("woff2");font-weight:200 1000;font-display:swap;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C4}
"""
INK='#3A2618'
THUMBS = (
 '<svg viewBox="0 0 64 64"><path d="M16 38V30a16 16 0 0 1 32 0v8" fill="none" stroke="#2B2B2E" stroke-width="5" stroke-linecap="round"/><rect x="10" y="34" width="12" height="18" rx="6" fill="#2B2B2E"/><rect x="42" y="34" width="12" height="18" rx="6" fill="#2B2B2E"/></svg>'
 '<svg viewBox="0 0 64 64"><ellipse cx="32" cy="34" rx="22" ry="16" fill="#3A3A3E"/><path d="M12 32q20 -8 40 0" fill="none" stroke="#8A8A90" stroke-width="2" stroke-dasharray="3 3"/><rect x="28" y="22" width="8" height="5" rx="2" fill="#8A8A90"/></svg>'
 '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" fill="#2B2B2E"/><circle cx="32" cy="32" r="11" fill="#55555A"/><path d="M18 22l4 3M44 40l3 3M20 42l3-2" stroke="#9A9AA0" stroke-width="2" stroke-linecap="round"/></svg>'
)
def icon(path):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+path+'</svg>'
ICONS = {
 '{{ICON_FILE}}': icon('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 11v6M9 14l3 3 3-3"/>'),
 '{{ICON_DOC}}': icon('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
 '{{ICON_CHECK}}': icon('<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>'),
 '{{ICON_USER}}': icon('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
 '{{ICON_TOGGLE}}': icon('<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="16" cy="12" r="3"/>'),
 '{{ICON_CAM}}': icon('<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="14" r="4"/>'),
}
EX = {
 '{{EX_QUESTIONS}}':'Die verkaufen sich gut! Zwei kurze Fragen: Funktioniert alles, und wie lange hält der Akku? Hast du Rechnung oder Karton, und von wo verschickst du?',
 '{{EX_ANSWER}}':'Funktioniert alles, Akku ca. 25 Stunden, keine Rechnung, Versand aus München.',
 '{{EX_RESULT_INTRO}}':'Am besten auf Kleinanzeigen. Hier ist deine Anzeige:',
 '{{EX_TITLE}}':'Sony WH-1000XM4 Noise-Cancelling Kopfhörer schwarz mit Etui',
 '{{EX_PRICE}}':'115 € VB · realistisch 100–110 € · nicht unter 90 €',
 '{{EX_TEXT}}':html.escape('Ich verkaufe meine Sony WH-1000XM4 Bluetooth-Kopfhörer mit Noise Cancelling, gebraucht in gutem Zustand.\n\n• Bei mir funktioniert alles ohne Probleme, Akku ca. 25 Stunden\n• Ohrpolster leicht abgenutzt (siehe Foto)\n• Dabei: Etui, USB-C-Kabel, Klinkenkabel\n\nVersand versichert oder Abholung in München.'),
}

def render(src, preview):
    s = src
    if preview:
        img = 'data:image/png;base64,' + base64.b64encode((HERE/'hamster.png').read_bytes()).decode()
        cut = 'data:image/png;base64,' + base64.b64encode((HERE/'hamster-cut.png').read_bytes()).decode()
    else:
        img = 'hamster.png'; cut = 'hamster-cut.png'
        # Google Fonts raus (DSGVO), lokale Schriften rein
        s = re.sub(r'<link rel="preconnect"[^>]*>\n', '', s)
        s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', s)
        s = s.replace('<style>\n', '<style>\n' + FONTFACE, 1)
    rep = dict(ICONS)
    rep['{{THUMBS}}'] = THUMBS
    rep['{{HAMSTER}}'] = img
    rep['{{HAMSTER_CUT}}'] = cut
    rep['{{BUY_ANZEIGEN}}'] = BUY or '#kaufen'
    rep['{{BUY_CLASS}}'] = '' if BUY else 'soon'
    rep['{{BUY_ATTRS}}'] = 'rel="noopener" target="_blank"' if BUY else 'aria-disabled="true"'
    rep['{{BUY_LABEL}}'] = 'Für 9,90 € kaufen' if BUY else 'Bald verfügbar'
    rep['{{IMPRESSUM}}'] = 'impressum.html'
    rep['{{DATENSCHUTZ}}'] = 'datenschutz.html'
    rep['{{AGB}}'] = 'kaufbedingungen.html'
    for k, v in rep.items(): s = s.replace(k, v)
    assert '{{' not in s, re.findall(r'{{\w+}}', s)
    return s

def wrap(body):
    return '<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<link rel="icon" href="hamster.png">\n' + body.replace('</style>\n', '</style>\n</head>\n<body>\n', 1) + '\n</body>\n</html>\n'

src = (HERE/'index.src.html').read_text()
(HERE/'index.html').write_text(render(src, True))
OUT.mkdir(exist_ok=True)
import shutil; shutil.copy(HERE/'hamster-cut.png', OUT/'hamster-cut.png')
(OUT/'index.html').write_text(wrap(render(src, False)))
# Rechtsseiten
legal_css = (HERE/'legal.css').read_text()
for name in ['impressum', 'datenschutz', 'kaufbedingungen']:
    body = (HERE/f'{name}.src.html').read_text()
    page = f'<title>{name.capitalize()} · Hamsterfrei</title>\n<style>\n{FONTFACE}{legal_css}</style>\n' + body
    (OUT/f'{name}.html').write_text(wrap(page))
print('ok', 'BUY=' + (BUY or '-'))
