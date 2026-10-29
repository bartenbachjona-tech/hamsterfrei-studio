# Masterplan: Maskottchen-Kanal + Automatisierungs-Plattform (Stand 29.10.2026)

## Hintergrund zum Gründer (Jona)
- Sitzt in Deutschland (Bayern), hat ein Unternehmen angemeldet (Rechtsform unklar, vermutlich Einzelunternehmen).
- Betreibt seit ca. Mitte Oktober 2026 zwei automatisierte Faceless-Kanäle: "Groschenfall" (Geld/Verbraucherwissen, Shorts + lange Videos) und "Schattengast" (animierte Creepy Stories, Shorts). Beide haben noch keine nennenswerten Zahlen, taugen also nicht als Beweis.
- Die bestehende Pipeline läuft nachts auf seinem PC: Claude schreibt Skripte, ein zweites Claude-Modell ist Kritiker, ElevenLabs (Creator-Plan) macht Stimme und Musik, Bilder per KI, Schnitt mit Remotion, Posting über Buffer (Free). Er ist kein Entwickler, Claude schreibt den Code.
- Budget unbekannt, vermutlich klein (Privatperson/Gründer).

## Ursprüngliche Idee von Jona
Social-Media-Account (TikTok, Instagram, YouTube) mit stark wiedererkennbarem Maskottchen, das Business-Ideen vorstellt und erklärt, wie man sie mit seiner Website automatisiert umsetzt. Website: Kunden kaufen monatliches Abo mit Credits, wählen Nische, Design, Stimme, verbinden TikTok/Insta/YouTube, dann laufen Faceless-Shorts automatisch. Später weitere automatisierbare Geschäftsmodelle (z. B. Makler-Akquise). Hohe Marge gewünscht. Jonas ursprüngliche Ideen, die bereits verworfen wurden: (1) ein Claude-Max-Abo für alle Kunden nutzen – nicht erlaubt laut Anthropic-Bedingungen, daher Claude API; (2) "Geld machen als richtig easy darstellen" – verworfen wegen UWG, Plattformregeln, Churn.

## Kurzfassung
Wir verkaufen fertige, automatisch gepostete Videos im Abo, kein Einkommensversprechen. Der Maskottchen-Kanal ist Vertrieb und Beweis zugleich, weil er selbst komplett mit der Plattform produziert wird.
Kernprinzipien: Output statt Versprechen; eigenes Produkt nutzen; jeder Kundenkanal sieht anders aus (YouTube "inauthentic content"-Policy gegen Massenware); alles legal über offizielle APIs mit Geschäftsplänen; erst Geld, dann Ausbau.

## Beweis-Problem
Vier Beweisquellen: (1) Maskottchen-Kanal selbst, mit Plattform produziert, wöchentlich echte Zahlen (Build in Public); (2) Output statt Einnahmen versprechen ("30 fertige Videos, 0 Minuten Schnitt"); (3) 10 Beta-Kunden zu reduziertem Preis, Zahlen zeigen dürfen; (4) 3–5 eigene Testkanäle in verschiedenen Nischen. Nie: erfundene Einnahmen.

## Produkt (MVP)
Ablauf: Konto + Plan (Stripe) → Nische (6–8 getestete) → Design (Bildstil, Farben, Schrift, Untertitel; pro Kunde variiert) → Stimme (deutsche ElevenLabs-Stimmen) → Konten verbinden → Rhythmus → Wochen-Themenplan freigeben (Pflicht, auto-Freigabe nach 24h möglich) → Produktion, Dashboard, Posting.
MVP: Auswahl, Themenplan, Produktion (Skript, Kritiker, Stimme, Bilder, Untertitel, Musik, Schnitt), Auto-Posting auf 3 Plattformen, Dashboard, KI-Kennzeichnung.
Später: Stimmenklon, Statistiken, lange Videos, mehrere Kanäle, weitere Module.

## Maskottchen und Kanal
Figur: eigene Erfindung, markenfähig (DPMA), wenige Formen, 2–3 Farben, konsistent in KI-Bildern, Referenzblatt, feste Persönlichkeit (neugierig, ehrlich, frech, kein Angeber), eigene Stimme.
Formate: "Idee der Woche" (Reichweite), "Ehrliche Zahlen" (Vertrauen), "So geht's" (Kauf), "Mythos-Check" (Abgrenzung).
Funnel: Video → Link im Profil → Landingpage mit Beispielen und echten Zahlen → kostenloser Test (3 Gratis-Videos ohne Posting) → Abo.

## Technik
Website/Dashboard Next.js, Login/DB Supabase, Stripe Billing, Worker mit Warteschlange auf eigenem Server, Remotion-Rendering, Cloud-Speicher, Claude API, ElevenLabs API, Bild-API. Posting: zuerst Drittdienst mit bereits TikTok-geprüfter App (z. B. Blotato oder Ayrshare), später eigene geprüfte Apps (TikTok Content Posting API Audit – unaudited = nur privat, max 5 Nutzer/24h; YouTube Data API Quota + OAuth-Verifizierung; Meta App Review).

## Kosten und Preise (Annahmen)
Regel: Credit-Preis ≥ 3× Kosten pro Short. Annahme 0,50 € Kosten pro Short (ungemessen).
Starter 59 €/30 Credits/1 Kanal (1,97 €/Short, ~75 % Rohmarge); Pro 99 €/60/1 (1,65 €, ~70 %); Business 179 €/120/3 Kanäle (1,49 €, ~66 %).
Regeln: Credits verfallen (max 1 Monat Übertrag), Zusatzpakete teurer, Extras eigene Credits, Tageslimits pro Kunde, Jahresabo mit 2 Monaten Rabatt.

## Recht (Checkliste)
Rechtsform (UG statt Einzelunternehmen?), Impressum, AGB (keine Einnahmengarantie), Datenschutz + AVV mit allen Anbietern (USA-Transfer), Kündigungsbutton §312k BGB, Widerruf + Zustimmung vorzeitiger Leistungsbeginn, Bruttopreise, UWG, KI-Kennzeichnung (Plattformen + EU AI Act Art. 50), Anbieterbedingungen (Claude API, ElevenLabs kommerziell), Haftung für Kundeninhalte, DPMA-Marke.

## Risiken
Churn wegen ausbleibendem Wachstum (größtes Risiko); YouTube-Massenware-Einstufung; TikTok-Audit; API-Preise; Kostenexplosion durch Fehler; Sperren von Kundenkonten; Konkurrenz (AutoShorts, FacelessVideos u. a.); Jona allein als Engpass.

## Fahrplan
Phase 0 Fundament (~3 Wo): Name, Maskottchen, Rechtsform, Rechtstexte, Landingpage mit Warteliste. Tor 1: Name, Figur, Rechtstexte fertig.
Phase 1 Kanal + Pipeline (~6–8 Wo): Maskottchen-Kanal täglich, 3–5 Testkanäle, Pipeline auf Server, Posting-Dienst. Tor 2: 300 Wartelisten-Einträge + Pipeline stabil.
Phase 2 Bezahlte Beta (~8 Wo): 10 Testkunden reduziert, Kosten messen, Fallstudien. Tor 3: Kosten gemessen, 7/10 bleiben.
Phase 3 Plattform v1 (~8–12 Wo): Selbstbedienung, Stripe-Credits, Launch, eigene API-Prüfungen. Tor 4: 50 zahlende Kunden, Marge > 60 %.
Phase 4: weitere Module (Makler).
Umsteuern: Warteliste < 100 nach 8 Wochen; Kosten > 1/3 Creditpreis; > 3/10 Beta-Kündigungen im 1. Monat.

## Offene Entscheidungen
Name, Maskottchen-Typ, Rechtsform, Budget 3 Monate, Startnischen, Posting-Dienst, Zeit pro Woche, Groschenfall/Schattengast weiter oder pausieren.
