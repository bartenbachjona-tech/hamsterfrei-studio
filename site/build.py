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
    else:
        img = 'hamster.png'
        # Google Fonts raus (DSGVO), lokale Schriften rein
        s = re.sub(r'<link rel="preconnect"[^>]*>\n', '', s)
        s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', s)
        s = s.replace('<style>\n', '<style>\n' + FONTFACE, 1)
    rep = dict(EX)
    rep['{{HAMSTER}}'] = img
    rep['{{BUY_ANZEIGEN}}'] = BUY or '#anzeigen-profi'
    rep['{{BUY_DISABLED}}'] = '' if BUY else 'aria-disabled="true" title="Kauf-Link kommt in Kürze"'
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
(OUT/'index.html').write_text(wrap(render(src, False)))
# Rechtsseiten
legal_css = (HERE/'legal.css').read_text()
for name in ['impressum', 'datenschutz', 'kaufbedingungen']:
    body = (HERE/f'{name}.src.html').read_text()
    page = f'<title>{name.capitalize()} · Hamsterfrei</title>\n<style>\n{FONTFACE}{legal_css}</style>\n' + body
    (OUT/f'{name}.html').write_text(wrap(page))
print('ok', 'BUY=' + (BUY or '-'))
