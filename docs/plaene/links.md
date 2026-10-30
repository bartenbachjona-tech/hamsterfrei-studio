# Freigegebene Links für DMs

Nur Links eintragen, die Jona ausdrücklich freigegeben hat. Affiliate-Links in der DM immer mit „(*Werbelink)“ kennzeichnen.

| Wort | Link | Kennzeichnung | freigegeben am |
|---|---|---|---|
| SHOP | – (noch keiner, Shopify-Affiliate noch nicht beantragt/bestätigt) | – | – |
| SEMINAR | https://bartenbachjona-tech.github.io/hamsterfrei-site/seminararbeit-profi.html (Bestellformular https://www.checkout-ds24.com/product/757079) | „Werbung: mein eigenes Produkt“ | erst aktiv nach Digistore-Freigabe |
| SKILL | https://bartenbachjona-tech.github.io/hamsterfrei-site/ (Verkaufsseite; Bestellformular https://www.checkout-ds24.com/product/757063) | „Werbung: mein eigenes Produkt“ | erst aktiv, wenn Seite online + Digistore-Freigabe |

## Verkaufsseite
- Quelle: `site/` im Studio-Repo, Build: `python3 site/build.py <DIGISTORE_LINK>` → schreibt nach ../hamsterfrei-site (öffentliches Repo, GitHub Pages).
- Adresse (sobald Pages aktiv): https://bartenbachjona-tech.github.io/hamsterfrei-site/
- Digistore24-Bestell-Link: https://www.checkout-ds24.com/product/757063 (Produkt-ID 757063).

## Digistore-Stand (30.10.2026)
- Anzeigen-Profi 757063 (9,90 €) und Seminararbeit-Profi 757079 (9,90 €, Plan 1545912; 37-€-Plan 1545910 deaktiviert; Datei-Paket 153266).
- Beide **nicht genehmigt** → Bestellformular nur mit Testzahlung.
- Verkaufsseite auf github.io wird abgelehnt (Fehler SLPDM1: Domain von anderem User belegt) → eigene Domain nötig (z. B. hamsterfrei.de), dann GitHub-Pages-Custom-Domain.
- Freigabe-Checkliste muss Jona selbst bestätigen (Testkauf, Impressum, Seriosität).

- **Bio-Link bis 10.11.2026 auf allen Kanälen: https://hamsterfrei.de/seminar** (leitet direkt auf seminararbeit-profi.html, NICHT auf die Startseite). Danach ggf. wieder hamsterfrei.de.

## Domain hamsterfrei.de (gekauft 30.10.2026 bei STRATO, Paket 10203868)
- **LIVE seit 30.10.2026 ~07:45:** STRATO A 185.199.108.153, AAAA 2606:50c0:8000::153, www folgt der Hauptdomain. CNAME-Datei im Repo, HTTPS-Zertifikat für hamsterfrei.de aktiv, http→https per Skript in jeder Seite. Offen: Häkchen „Enforce HTTPS“ in GitHub (API über Proxy gesperrt), www-Zertifikat kommt automatisch.
- Status 30.10. 00:30: „wird eingerichtet“, STRATO schickt Mail, wenn fertig (i. d. R. < 24 h).
- Danach (Jona loggt sich bei STRATO ein): DNS setzen
  - A @ → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
  - CNAME www → bartenbachjona-tech.github.io
- ERST wenn DNS auflöst: Datei `CNAME` mit `hamsterfrei.de` ins Repo hamsterfrei-site, Pages → Custom domain + „Enforce HTTPS“.
- Dann Digistore: Verkaufsseite 757063 → https://hamsterfrei.de/anzeigen-profi.html, 757079 → https://hamsterfrei.de/seminararbeit-profi.html; TikTok-Bio-Link aktualisieren.
