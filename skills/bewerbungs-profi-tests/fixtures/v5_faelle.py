"""v5-Fälle: Nutzerwortlaut (umgangssprachlich, Tippfehler) → professionelles Anschreiben (muss 0 ❌ in EINEM Lauf
ergeben) und Erfindungs-Fälle aus allen vier Fehlerlisten (müssen ❌ ergeben). Wird von run_tests.py importiert."""
import copy


def R(nr, antwort, frage=None, **kw):
    e = {"nr": nr, "frage": frage or f"Frage {nr}", "antwort": antwort}
    e.update(kw)
    return e


def S(satz, *quellen, **kw):
    qs = []
    for q in quellen:
        if isinstance(q, tuple):
            qs.append({"nr": q[0], "zitat": q[1]})
        else:
            qs.append(q)
    return dict({"satz": satz, "quellen": qs}, **kw)


# ---------------------------------------------------------------- Transkript 15 (Katrin, Praxissemester, knapp)
F15 = {
    "name": "Katrin Hollweck", "anrede_form": "sie",
    "ziel": {"stelle": "Praktikum (Praxissemester) Personalentwicklung (m/w/d) – Sommersemester 2027", "firma": "Alpenwerk Versicherung AG",
             "ansprechperson": "Herr Daniel Wörle", "anrede": "Sehr geehrter Herr Wörle,",
             "anzeige_text": "Praktikum (Praxissemester) Personalentwicklung (m/w/d) – Sommersemester 2027. Alpenwerk Versicherung AG, "
                             "München. Ihr Profil: Studium BWL oder Psychologie, Pflichtpraktikum mind. 20 Wochen, Excel und PowerPoint, "
                             "Kommunikationsstärke, Organisationstalent, gute Englischkenntnisse. Sie arbeiten an einem eigenen Projekt "
                             "im Onboarding mit. Kontakt: Herr Daniel Wörle."},
    "rohtext": [
        R(1, "Katrin Hollweck, Implerstraße 41, 81371 München, 0160 9384417, k.hollweck@gmx.de"),
        R(2, "BWL Bachelor, Hochschule München, seit 10/2024, jetzt 5. Semester"),
        R(3, "Ausbildung Hotelfachfrau Hotel Sonnenhof 2008-2011. Danach Rezeption dort bis 09/2024, ab 2017 Schichtleitung. Jetzt Wochenende Rezeption Minijob dort."),
        R(4, "a, b und c. Habe 6 Azubis betreut.", "Nachfrage: Was haben Sie an der Rezeption gemacht? a) Check-in/Check-out b) Dienstpläne c) Azubis eingearbeitet d) anderes",
          optionen={"a": "Check-in/Check-out", "b": "Dienstpläne", "c": "Azubis eingearbeitet"}),
        R(5, "Englisch gut, Excel, PowerPoint, Opera (Hotelsoftware)"),
        R(6, "Azubis einarbeiten hat mir am meisten Spaß gemacht"),
        R(7, "Weiß nicht"),
        R(8, "a) das eigene Projekt im Onboarding", "Denkanstoß: a) Was hat Sie an der Anzeige angesprochen? b) … c) …",
          optionen={"a": "Was hat Sie an der Anzeige angesprochen?"}),
        R(9, "Dienstplan für 12 Leute gemacht, Wünsche abgefragt, Konflikte geklärt"),
        R(10, "Pflichtpraktikum, 01.03.2027 bis 31.07.2027, Vollzeit. Minijob am Wochenende läuft weiter."),
        R(11, "Karriereseite")],
    "absaetze": [
        "im Hotel Sonnenhof habe ich nach meiner Ausbildung zur Hotelfachfrau an der Rezeption gearbeitet und ab 2017 die Schicht geleitet. "
        "Dabei habe ich sechs Auszubildende betreut und eingearbeitet – das hat mir am meisten Spaß gemacht. "
        "Deshalb möchte ich mein Pflichtpraktikum in der Personalentwicklung absolvieren.",
        "Seit Oktober 2024 studiere ich Betriebswirtschaftslehre (Bachelor) an der Hochschule München und bin jetzt im fünften Semester. "
        "In Ihrer Anzeige nennen Sie Organisationstalent und Kommunikationsstärke. "
        "An der Rezeption habe ich den Dienstplan für zwölf Mitarbeitende erstellt, Wünsche abgefragt und Konflikte geklärt. "
        "Ich nutze Excel und PowerPoint, und mein Englisch ist gut.",
        "In Ihrer Anzeige hat mich das eigene Projekt im Onboarding angesprochen.",
        "Mein Pflichtpraktikum kann ich vom 01.03.2027 bis 31.07.2027 in Vollzeit absolvieren. Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("im Hotel Sonnenhof habe ich nach meiner Ausbildung zur Hotelfachfrau an der Rezeption gearbeitet und ab 2017 die Schicht geleitet.",
          (3, "Ausbildung Hotelfachfrau Hotel Sonnenhof 2008-2011. Danach Rezeption dort bis 09/2024, ab 2017 Schichtleitung")),
        S("Dabei habe ich sechs Auszubildende betreut und eingearbeitet – das hat mir am meisten Spaß gemacht.",
          (4, "Habe 6 Azubis betreut"), (4, "Azubis eingearbeitet"), (6, "Azubis einarbeiten hat mir am meisten Spaß gemacht")),
        S("Deshalb möchte ich mein Pflichtpraktikum in der Personalentwicklung absolvieren.", (10, "Pflichtpraktikum"), {"anzeige": "Personalentwicklung"}),
        S("Seit Oktober 2024 studiere ich Betriebswirtschaftslehre (Bachelor) an der Hochschule München und bin jetzt im fünften Semester.",
          (2, "BWL Bachelor, Hochschule München, seit 10/2024, jetzt 5. Semester")),
        S("In Ihrer Anzeige nennen Sie Organisationstalent und Kommunikationsstärke.", {"anzeige": "Kommunikationsstärke, Organisationstalent"}),
        S("An der Rezeption habe ich den Dienstplan für zwölf Mitarbeitende erstellt, Wünsche abgefragt und Konflikte geklärt.",
          (9, "Dienstplan für 12 Leute gemacht, Wünsche abgefragt, Konflikte geklärt"), (3, "Rezeption")),
        S("Ich nutze Excel und PowerPoint, und mein Englisch ist gut.", (5, "Englisch gut, Excel, PowerPoint")),
        S("In Ihrer Anzeige hat mich das eigene Projekt im Onboarding angesprochen.", (8, "das eigene Projekt im Onboarding")),
        S("Mein Pflichtpraktikum kann ich vom 01.03.2027 bis 31.07.2027 in Vollzeit absolvieren.", (10, "Pflichtpraktikum, 01.03.2027 bis 31.07.2027, Vollzeit"))],
}

# ---------------------------------------------------------------- Transkript 72 (Mara, duales Studium, Motivationsschreiben)
F72 = {
    "name": "Mara Kessler", "typ": "motivationsschreiben",
    "ziel": {"stelle": "Duales Studium Betriebswirtschaft – Schwerpunkt Logistik (B.A.)", "firma": "Hollerith Logistik GmbH",
             "ansprechperson": "Frau Daniela Ortner", "anrede": "Sehr geehrte Frau Ortner,",
             "anzeige_text": "Duales Studium Betriebswirtschaft – Schwerpunkt Logistik (B.A.), Start 01.10.2027. Hollerith Logistik GmbH, "
                             "Regensburg. Wir erwarten: Fachabitur, gute Noten in Mathe und Englisch, Teamfähigkeit, Organisationstalent. "
                             "Bewerbung mit Motivationsschreiben über unser Portal. Kontakt: Frau Daniela Ortner."},
    "rohtext": [
        R(1, "mara kessler, am kreuzhof 7, 93055 regensburg, 0157 31846620, mara.kessler@gmx.de"),
        R(2, "fachabi wirtschaft an der fos regensburg, juli 2025, schnitt 2,6. mathe 2 englisch 3 glaub ich", geklaert=True),
        R(3, "ja hab nachgeschaut 3", "Nachfrage: Also Englisch Note 3 – stimmt das? a) Ja b) Nein", bestaetigt="Englisch Note 3"),
        R(4, "seit januar am wochenende minijob in der bäckerei schmid, verkauf und kasse. sonst nix, nach dem fachabi hab ich keinen platz bekommen"),
        R(5, "ja", "Nachfrage: Bäckerei seit Januar 2026 – stimmt das? a) Ja b) Nein", bestaetigt="Januar 2026"),
        R(10, "ich find es cool wie alles ankommt, also wie die ware vom lager in den laden kommt, sehe ich in der bäckerei wenn die lieferung kommt. und ich will studieren aber auch geld verdienen"),
        R(11, "die sind bei mir in der nähe, 20 min mit dem rad. und meine freundin macht da die ausbildung und sagt die azubis werden gut betreut"),
        R(12, "in der bäckerei mach ich samstags die vorbestellungen fertig, also die listen abarbeiten und alles in tüten mit namen packen bevor die leute kommen. hat noch nie was gefehlt glaub ich", geklaert=True)],
    "absaetze": [
        "mich interessiert, wie Waren vom Lager in den Laden gelangen. Das erlebe ich in der Bäckerei, wenn die Lieferung ankommt. "
        "Ich möchte studieren und dabei auch Geld verdienen – deshalb bewerbe ich mich um das duale Studium.",
        "Seit Januar 2026 arbeite ich am Wochenende als Aushilfe in der Bäckerei Schmid im Verkauf und an der Kasse. "
        "In Ihrer Anzeige nennen Sie Organisationstalent. "
        "Samstags bereite ich die Vorbestellungen vor: Ich arbeite die Listen ab und packe alles mit Namen in Tüten, bevor die Kundinnen und Kunden kommen.",
        "Ihr Unternehmen liegt in meiner Nähe – mit dem Rad bin ich in 20 Minuten bei Ihnen. "
        "Eine Freundin von mir macht bei Ihnen die Ausbildung und erzählt, dass die Auszubildenden gut betreut werden.",
        "Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("mich interessiert, wie Waren vom Lager in den Laden gelangen.", (10, "ich find es cool wie alles ankommt, also wie die ware vom lager in den laden kommt")),
        S("Das erlebe ich in der Bäckerei, wenn die Lieferung ankommt.", (10, "sehe ich in der bäckerei wenn die lieferung kommt")),
        S("Ich möchte studieren und dabei auch Geld verdienen – deshalb bewerbe ich mich um das duale Studium.", (10, "ich will studieren aber auch geld verdienen")),
        S("Seit Januar 2026 arbeite ich am Wochenende als Aushilfe in der Bäckerei Schmid im Verkauf und an der Kasse.",
          (4, "seit januar am wochenende minijob in der bäckerei schmid, verkauf und kasse"), (5, "Januar 2026")),
        S("In Ihrer Anzeige nennen Sie Organisationstalent.", {"anzeige": "Organisationstalent"}),
        S("Samstags bereite ich die Vorbestellungen vor: Ich arbeite die Listen ab und packe alles mit Namen in Tüten, bevor die Kundinnen und Kunden kommen.",
          (12, "in der bäckerei mach ich samstags die vorbestellungen fertig, also die listen abarbeiten und alles in tüten mit namen packen bevor die leute kommen")),
        S("Ihr Unternehmen liegt in meiner Nähe – mit dem Rad bin ich in 20 Minuten bei Ihnen.", (11, "die sind bei mir in der nähe, 20 min mit dem rad")),
        S("Eine Freundin von mir macht bei Ihnen die Ausbildung und erzählt, dass die Auszubildenden gut betreut werden.",
          (11, "meine freundin macht da die ausbildung und sagt die azubis werden gut betreut"))],
}

# ---------------------------------------------------------------- Transkript 158 (Dennis, Jobwechsel, Tippfehler)
F158 = {
    "name": "Dennis Hartl",
    "ziel": {"stelle": "Lagermitarbeiter Wareneingang (m/w/d)", "firma": "Brenner Sanitär-Großhandel GmbH",
             "ansprechperson": "Herr Tobias Wagner", "anrede": "Sehr geehrter Herr Wagner,",
             "anzeige_text": "Lagermitarbeiter Wareneingang (m/w/d). Brenner Sanitär-Großhandel GmbH, Augsburg-Lechhausen. Aufgaben: Ware "
                             "annehmen und prüfen, einlagern mit Gabelstapler, in SAP buchen, Inventur. Profil: Ausbildung Fachkraft "
                             "Lagerlogistik oder mehrjährige Lagererfahrung, Staplerschein, sorgfältige und zuverlässige Arbeitsweise. "
                             "Arbeitszeit Mo–Fr 6:00–14:30. Bewerbung per E-Mail an Herrn Tobias Wagner mit Gehaltsvorstellung."},
    "rohtext": [
        R(2, "Dennis Hartl, Lindenweg 7, 86356 Neusäß, 0171 5583920, dennis.hartl87@gmx.de"),
        R(4, "quali 2005 an der mittelschule neusäß, danach ausbildung kfz mechatroniker beim autohaus seitz in augsburg ab sept 2005 aber nach anderthalb jahren abgebrochen"),
        R(5, "märz 2007 rum. mit dem meister gings garnich und ich wollt endlich richtig geld verdienen, hab dann direkt im lager angefangen"),
        R(6, "ja", "Also bis März 2007 – stimmt das? a) Ja b) Nein", bestaetigt="März 2007"),
        R(7, "2007 bis 2014 bei spedition kögel in augsburg lagerhelfer, kommisioniert, lkws be und entladen, ab 2008 staplerfahrer. seit 2014 bei plastiwerk schwaben in gersthofen maschinenführer an spritzgussmaschinen, 3 schicht, rüsten, teile prüfen, neue leute einlernen"),
        R(8, "staplerschein seit 2008, führerschein B, sap so bisschen vom kögel noch, excel nich wirklich. deutsch halt"),
        R(9, "b, und kommisionieraufträge ausgedruckt", "Was hast du in SAP gemacht? a) Wareneingang gebucht b) Lagerplätze nachgeschaut c) anderes",
          optionen={"a": "Wareneingang gebucht", "b": "Lagerplätze nachgeschaut"}),
        R(10, "ich will raus aus der schicht, die nachtschicht macht mich echt fertig und meine kids seh ich kaum. lager hab ich beim kögel gern gemacht, da sieht man am abend was man geschafft hat"),
        R(12, "is 15 min mit auto von mir, und mo-fr nur früh. und ein kumpel von mir fährt für die, der sagt die sind korrekt"),
        R(13, "beim plastiwerk prüf ich jede stunde teile mit messschieber, wenn maß nich passt stopp ich die maschine und sag dem schichtleiter bescheid. letztes jahr hab ich so ne ganze charge mit falschen maßen gefunden bevor die raus is"),
        R(14, "hab 3 monate kündigungsfrist zum monatsende. also wenn ich ende november kündige frühstens 1. märz"),
        R(15, "ja genau", "Also ab 01.03.2027 – stimmt das? a) Ja b) Nein", bestaetigt="01.03.2027"),
        R(17, "ja passt", "Mein Vorschlag: 34.000–36.000 EUR brutto/Jahr. Passt das? a) Ja b) Andere Zahl", bestaetigt="34.000–36.000 EUR brutto/Jahr"),
        R(20, "ja", "Soll ich im Lebenslauf 05/2007 – 06/2014 schreiben? a) Ja b) Nein", bestaetigt="05/2007 – 06/2014")],
    "absaetze": [
        "seit 2014 arbeite ich als Maschinenführer an Spritzgussmaschinen bei Plastiwerk Schwaben in Gersthofen im Drei-Schicht-Betrieb. "
        "Davor war ich von Mai 2007 bis Juni 2014 bei der Spedition Kögel in Augsburg im Lager tätig, ab 2008 auch als Staplerfahrer. "
        "Dort habe ich Aufträge kommissioniert, Lkw be- und entladen und in SAP Lagerplätze nachgesehen. "
        "Die Arbeit im Lager hat mir gefallen, weil man am Abend sieht, was man geschafft hat. "
        "Ich möchte aus der Schichtarbeit heraus und wieder im Lager arbeiten.",
        "In Ihrer Anzeige nennen Sie eine sorgfältige Arbeitsweise. "
        "Im Plastiwerk prüfe ich jede Stunde Teile mit dem Messschieber. "
        "Passt ein Maß nicht, stoppe ich die Maschine und informiere den Schichtleiter. "
        "Im vergangenen Jahr habe ich auf diese Weise eine ganze Charge mit falschen Maßen entdeckt, bevor sie den Betrieb verlassen hat.",
        "Ihr Standort ist mit dem Auto in 15 Minuten erreichbar, und bei Ihnen arbeite ich von Montag bis Freitag nur in der Frühschicht.",
        "Ich kann frühestens am 1. März 2027 beginnen. Meine Gehaltsvorstellung liegt bei 34.000 bis 36.000 Euro brutto im Jahr. "
        "Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("seit 2014 arbeite ich als Maschinenführer an Spritzgussmaschinen bei Plastiwerk Schwaben in Gersthofen im Drei-Schicht-Betrieb.",
          (7, "seit 2014 bei plastiwerk schwaben in gersthofen maschinenführer an spritzgussmaschinen, 3 schicht")),
        S("Davor war ich von Mai 2007 bis Juni 2014 bei der Spedition Kögel in Augsburg im Lager tätig, ab 2008 auch als Staplerfahrer.",
          (7, "2007 bis 2014 bei spedition kögel in augsburg lagerhelfer"), (7, "ab 2008 staplerfahrer"), (20, "05/2007 – 06/2014")),
        S("Dort habe ich Aufträge kommissioniert, Lkw be- und entladen und in SAP Lagerplätze nachgesehen.",
          (7, "kommisioniert, lkws be und entladen"), (9, "kommisionieraufträge"), (9, "Lagerplätze nachgeschaut"), (8, "sap")),
        S("Die Arbeit im Lager hat mir gefallen, weil man am Abend sieht, was man geschafft hat.",
          (10, "lager hab ich beim kögel gern gemacht, da sieht man am abend was man geschafft hat")),
        S("Ich möchte aus der Schichtarbeit heraus und wieder im Lager arbeiten.", (10, "ich will raus aus der schicht"), (10, "lager")),
        S("In Ihrer Anzeige nennen Sie eine sorgfältige Arbeitsweise.", {"anzeige": "sorgfältige und zuverlässige Arbeitsweise"}),
        S("Im Plastiwerk prüfe ich jede Stunde Teile mit dem Messschieber.", (13, "beim plastiwerk prüf ich jede stunde teile mit messschieber")),
        S("Passt ein Maß nicht, stoppe ich die Maschine und informiere den Schichtleiter.",
          (13, "wenn maß nich passt stopp ich die maschine und sag dem schichtleiter bescheid")),
        S("Im vergangenen Jahr habe ich auf diese Weise eine ganze Charge mit falschen Maßen entdeckt, bevor sie den Betrieb verlassen hat.",
          (13, "letztes jahr hab ich so ne ganze charge mit falschen maßen gefunden bevor die raus is")),
        S("Ihr Standort ist mit dem Auto in 15 Minuten erreichbar, und bei Ihnen arbeite ich von Montag bis Freitag nur in der Frühschicht.",
          (12, "is 15 min mit auto von mir, und mo-fr nur früh")),
        S("Ich kann frühestens am 1. März 2027 beginnen.", (14, "frühstens 1. märz"), (15, "01.03.2027")),
        S("Meine Gehaltsvorstellung liegt bei 34.000 bis 36.000 Euro brutto im Jahr.", (17, "34.000–36.000 EUR brutto/Jahr"))],
}

# ---------------------------------------------------------------- Transkript 651 (Johanna, Ausbildung SoFa, viele Rückfragen)
F651 = {
    "name": "Johanna Weidinger",
    "ziel": {"stelle": "Ausbildung Sozialversicherungsfachangestellte/r (m/w/d) – Fachrichtung allgemeine Krankenversicherung",
             "firma": "BKK Frankenland", "ansprechperson": "Frau Katrin Albrecht", "anrede": "Sehr geehrte Frau Albrecht,",
             "anzeige_text": "Ausbildung Sozialversicherungsfachangestellte/r (m/w/d) – Fachrichtung allgemeine Krankenversicherung, Start 01.09.2027, BKK Frankenland, Fürth. Gewünscht: "
                             "gute Noten in Deutsch und Mathe, Freude am Umgang mit Menschen, Kommunikationsstärke, Sorgfalt. "
                             "Ansprechpartnerin: Frau Katrin Albrecht."},
    "firmenfakten": [{"fakt": "Azubis betreuen ab dem 2. Ausbildungsjahr eigene Versicherte im Kundencenter",
                      "quelle": "bkk-frankenland.de/karriere/ausbildung", "zugestimmt": True}],
    "rohtext": [
        R(8, "Johanna Weidinger, Sielstraße 9, 90429 Nürnberg, 0160 4417825, johanna.weidinger@t-online.de"),
        R(9, "fsj 09/2022 bis 08/2023 in der st.-anna-klinik fürth am empfang, patienten aufgenommen, versichertenkarten eingelesen, mit den krankenkassen telefoniert wenn unklar war wer zahlt. seit 10/2023 kundenservice bei stromhaus franken in nürnberg, teilzeit 25 std, am telefon kundenfragen zu abschlägen und rechnungen, adressänderungen im system. zählt das callcenter überhaupt?"),
        R(12, "im fsj hab ich gemerkt dass mich das interessiert wer was zahlt, viele patienten wussten das nicht und ich hab dann bei der kasse nachgefragt. und im callcenter erklär ich leuten gern ihre rechnung bis sie es verstehen"),
        R(13, "ehrlich gesagt weiß ichs nicht genau. vlt weil die in fürth sind und nah?", geklaert=True),
        R(14, "ja stimmt, 15 min mit der ubahn", "Also „Die BKK ist in Fürth und nah dran“ – stimmt das so? a) Ja b) Nein",
          bestaetigt="in Fürth und nah dran"),
        R(16, "im callcenter hat mal ein älterer mann angerufen der total sauer war weil sein abschlag verdoppelt wurde. ich hab ihn erst erzählen lassen, dann im system gesehen dass sein zählerstand geschätzt war, und ihm gesagt er soll ein foto vom zähler schicken. hab das an die abrechnung gegeben, eine woche später war der abschlag wieder normal und er hat nochmal angerufen und sich bedankt")],
    "absaetze": [
        "während meines Freiwilligen Sozialen Jahres am Empfang der St.-Anna-Klinik in Fürth habe ich gemerkt, dass mich die Frage interessiert, wer was bezahlt. "
        "Viele Patientinnen und Patienten wussten das nicht, und ich habe dann bei der Krankenkasse nachgefragt.",
        "Seit Oktober 2023 arbeite ich in Teilzeit im Kundenservice von Stromhaus Franken und beantworte am Telefon Fragen zu Abschlägen und Rechnungen. "
        "Ich erkläre Kundinnen und Kunden gern ihre Rechnung, bis sie sie verstehen. "
        "Einmal rief ein älterer Mann verärgert an, weil sich sein Abschlag verdoppelt hatte. "
        "Ich habe ihn zunächst erzählen lassen und dann im System gesehen, dass sein Zählerstand geschätzt war. "
        "Ich habe ihm gesagt, er solle ein Foto des Zählers schicken, und den Vorgang an die Abrechnung weitergegeben. "
        "Eine Woche später war der Abschlag wieder normal, und er rief noch einmal an, um sich zu bedanken.",
        "Ihr Standort in Fürth ist für mich mit der U-Bahn in 15 Minuten erreichbar. "
        "Laut Ihrer Karriereseite betreuen Auszubildende bei Ihnen ab dem zweiten Ausbildungsjahr eigene Versicherte im Kundencenter.",
        "Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("während meines Freiwilligen Sozialen Jahres am Empfang der St.-Anna-Klinik in Fürth habe ich gemerkt, dass mich die Frage interessiert, wer was bezahlt.",
          (9, "fsj 09/2022 bis 08/2023 in der st.-anna-klinik fürth am empfang"), (12, "im fsj hab ich gemerkt dass mich das interessiert wer was zahlt")),
        S("Viele Patientinnen und Patienten wussten das nicht, und ich habe dann bei der Krankenkasse nachgefragt.",
          (12, "viele patienten wussten das nicht und ich hab dann bei der kasse nachgefragt"), (9, "mit den krankenkassen telefoniert")),
        S("Seit Oktober 2023 arbeite ich in Teilzeit im Kundenservice von Stromhaus Franken und beantworte am Telefon Fragen zu Abschlägen und Rechnungen.",
          (9, "seit 10/2023 kundenservice bei stromhaus franken in nürnberg, teilzeit 25 std, am telefon kundenfragen zu abschlägen und rechnungen")),
        S("Ich erkläre Kundinnen und Kunden gern ihre Rechnung, bis sie sie verstehen.", (12, "erklär ich leuten gern ihre rechnung bis sie es verstehen")),
        S("Einmal rief ein älterer Mann verärgert an, weil sich sein Abschlag verdoppelt hatte.",
          (16, "hat mal ein älterer mann angerufen der total sauer war weil sein abschlag verdoppelt wurde")),
        S("Ich habe ihn zunächst erzählen lassen und dann im System gesehen, dass sein Zählerstand geschätzt war.",
          (16, "ich hab ihn erst erzählen lassen, dann im system gesehen dass sein zählerstand geschätzt war")),
        S("Ich habe ihm gesagt, er solle ein Foto des Zählers schicken, und den Vorgang an die Abrechnung weitergegeben.",
          (16, "ihm gesagt er soll ein foto vom zähler schicken. hab das an die abrechnung gegeben")),
        S("Eine Woche später war der Abschlag wieder normal, und er rief noch einmal an, um sich zu bedanken.",
          (16, "eine woche später war der abschlag wieder normal und er hat nochmal angerufen und sich bedankt")),
        S("Ihr Standort in Fürth ist für mich mit der U-Bahn in 15 Minuten erreichbar.", (14, "15 min mit der ubahn"), (13, "in fürth")),
        S("Laut Ihrer Karriereseite betreuen Auszubildende bei Ihnen ab dem zweiten Ausbildungsjahr eigene Versicherte im Kundencenter.",
          {"firmenfakt": "Azubis betreuen ab dem 2. Ausbildungsjahr eigene Versicherte im Kundencenter"})],
}

# ---------------------------------------------------------------- Transkript 976 (Andrea, Wiedereinstieg, Telegrammstil)
F976 = {
    "name": "Andrea Wimmer", "anrede_form": "sie",
    "ziel": {"stelle": "Sachbearbeiter Einkauf (m/w/d) in Teilzeit (25–30 Std./Woche)", "firma": "Brandl Verpackungen GmbH",
             "ansprechperson": "Herr Thomas Reiter", "anrede": "Sehr geehrter Herr Reiter,",
             "anzeige_text": "Sachbearbeiter Einkauf (m/w/d) in Teilzeit (25–30 Std./Woche), Brandl Verpackungen GmbH, Ergolding. "
                             "Aufgaben: Bestellungen, Lieferanten, Termine, Eingangsrechnungen, Stammdaten in SAP. Profil: kaufmännische "
                             "Ausbildung, sicher in MS Office, Zuverlässigkeit und Kommunikationsstärke. Wiedereinsteiger nach "
                             "Familienphase ausdrücklich willkommen. Bewerbung per E-Mail an Herrn Thomas Reiter."},
    "upload": "Arbeitszeugnis. Frau Andrea Wimmer war vom 01.08.2008 bis 31.03.2018 als Sachbearbeiterin im Einkauf der Weigl "
              "Elektrotechnik GmbH tätig. Zu ihren Aufgaben gehörten die Abwicklung von Bestellungen in SAP MM, die Kommunikation "
              "mit Lieferanten und die Prüfung von Eingangsrechnungen.",
    "rohtext": [
        R(1, "Andrea Wimmer, Am Mühlbach 3, 84030 Ergolding, 0171 5520873, andrea.wimmer@t-online.de"),
        R(2, "Industriekauffrau, 2008"), R(3, "Brunner Metallbau Landshut"),
        R(4, "Weigl Elektrotechnik, Einkauf, 2008 bis 2018. Bestellungen, Lieferanten, Rechnungen."),
        R(5, "Familienzeit. 3 Kinder.", "Wie soll die Zeit seit 2018 heißen? a) Familienzeit b) Elternzeit c) anders"),
        R(6, "c. b manchmal.", "Gab es bei Weigl etwas Besonderes? a) neue Lieferanten gesucht b) Preise verhandelt c) bei der SAP-Einführung mitgemacht d) nichts Besonderes",
          optionen={"a": "neue Lieferanten gesucht", "b": "Preise verhandelt", "c": "bei der SAP-Einführung mitgemacht", "d": "nichts Besonderes"}),
        R(7, "SAP MM, Excel, Word. Englisch Schule."), R(8, "Kinder sind jetzt größer. Einkauf kann ich."),
        R(9, "Nah. Teilzeit. Wiedereinsteiger willkommen."),
        R(10, "Lieferant hat mal falsch geliefert, kurz vor Produktionsstart. Hab angerufen, Ersatz am nächsten Tag organisiert. Band lief weiter."),
        R(11, "Ab 1.2.27. 25 Std, vormittags."),
        R(13, "a", "Mein Vorschlag: a) 37.000 € brutto/Jahr auf Vollzeit gerechnet b) andere Zahl",
          optionen={"a": "37.000 € brutto/Jahr auf Vollzeit gerechnet", "b": "andere Zahl"}),
        R(14, "Stepstone")],
    "absaetze": [
        "nach meiner Familienzeit möchte ich ab dem 1. Februar 2027 wieder im Einkauf arbeiten – mit 25 Stunden pro Woche am Vormittag.",
        "Ich bin Industriekauffrau und war von 2008 bis 2018 im Einkauf der Weigl Elektrotechnik GmbH tätig. "
        "Dort habe ich Bestellungen in SAP MM abgewickelt, mit Lieferanten kommuniziert und Eingangsrechnungen geprüft. "
        "Außerdem habe ich bei der Einführung von SAP MM mitgewirkt und gelegentlich Preise verhandelt.",
        "In Ihrer Anzeige nennen Sie Zuverlässigkeit und Kommunikationsstärke. "
        "Als ein Lieferant kurz vor einem Produktionsstart falsch geliefert hatte, habe ich ihn angerufen und den Ersatz für den nächsten Tag organisiert. "
        "So lief das Band weiter.",
        "Für Ihr Unternehmen spricht, dass es in meiner Nähe liegt, Teilzeit anbietet und Wiedereinsteiger willkommen heißt.",
        "Meine Gehaltsvorstellung liegt bei 37.000 Euro brutto im Jahr, auf Vollzeit gerechnet. Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("nach meiner Familienzeit möchte ich ab dem 1. Februar 2027 wieder im Einkauf arbeiten – mit 25 Stunden pro Woche am Vormittag.",
          (5, "Familienzeit"), (8, "Einkauf kann ich"), (11, "Ab 1.2.27. 25 Std, vormittags.")),
        S("Ich bin Industriekauffrau und war von 2008 bis 2018 im Einkauf der Weigl Elektrotechnik GmbH tätig.",
          (2, "Industriekauffrau, 2008"), (4, "Weigl Elektrotechnik, Einkauf, 2008 bis 2018")),
        S("Dort habe ich Bestellungen in SAP MM abgewickelt, mit Lieferanten kommuniziert und Eingangsrechnungen geprüft.",
          {"upload": "die Abwicklung von Bestellungen in SAP MM, die Kommunikation mit Lieferanten und die Prüfung von Eingangsrechnungen"},
          (4, "Bestellungen, Lieferanten, Rechnungen")),
        S("Außerdem habe ich bei der Einführung von SAP MM mitgewirkt und gelegentlich Preise verhandelt.",
          (6, "c. b manchmal."), (7, "SAP MM")),
        S("In Ihrer Anzeige nennen Sie Zuverlässigkeit und Kommunikationsstärke.", {"anzeige": "Zuverlässigkeit und Kommunikationsstärke"}),
        S("Als ein Lieferant kurz vor einem Produktionsstart falsch geliefert hatte, habe ich ihn angerufen und den Ersatz für den nächsten Tag organisiert.",
          (10, "Lieferant hat mal falsch geliefert, kurz vor Produktionsstart. Hab angerufen, Ersatz am nächsten Tag organisiert.")),
        S("So lief das Band weiter.", (10, "Band lief weiter.")),
        S("Für Ihr Unternehmen spricht, dass es in meiner Nähe liegt, Teilzeit anbietet und Wiedereinsteiger willkommen heißt.",
          (9, "Nah. Teilzeit. Wiedereinsteiger willkommen.")),
        S("Meine Gehaltsvorstellung liegt bei 37.000 Euro brutto im Jahr, auf Vollzeit gerechnet.", (13, "37.000 € brutto/Jahr auf Vollzeit gerechnet"))],
}

# ---------------------------------------------------------------- Transkript 605 (Tobias, Mechatroniker, Ein-Wort-Antworten, „a“)
F605 = {
    "name": "Tobias Gerl",
    "ziel": {"stelle": "Ausbildung zum Mechatroniker (m/w/d) 2027", "firma": "Steinberger Maschinenbau GmbH",
             "ansprechperson": "Herr Florian Zeiler", "anrede": "Sehr geehrter Herr Zeiler,",
             "anzeige_text": "Ausbildung zum Mechatroniker (m/w/d) 2027, Start 01.09.2027, Steinberger Maschinenbau GmbH, Ergolding. "
                             "Du bringst mit: guten Mittelschulabschluss oder Mittlere Reife, Interesse an Technik, Mathe und Physik, "
                             "handwerkliches Geschick, Teamfähigkeit. Bewerbung per E-Mail an Herrn Florian Zeiler."},
    "rohtext": [
        R(8, "tobias gerl, am hofgarten 9, 84028 landshut, 0152 21907735, tobi.gerl@outlook.de"),
        R(10, "2 fachabi 2025 fos landshut wirtschaft 2,9. mittlere reife 2023\n3 baumarkt seit august 25 gartenabteilung 20h\n4 nix besonderes. führerschein b\n5 schrauben macht spaß. moped selber repariert\n6 nah. 10 min mit moped"),
        R(11, "b und c. rasenmäher fertig machen für verkauf", "Was machst du im Baumarkt? a) Kunden beraten b) Ware verräumen c) Geräte/Mäher fertig machen d) anderes",
          optionen={"a": "Kunden beraten", "b": "Ware verräumen", "c": "Geräte/Mäher fertig machen"}),
        R(12, "mathe 3. physik hatte ich nicht mehr"),
        R(13, "moped kupplung selber gewechselt mit youtube, ging dann"),
        R(15, "indeed"),
        R(16, "a", "Auf den Zeugnissen lese ich: Fachabi Juli 2025, Mittlere Reife Juli 2023. Stimmt das? a) Ja b) Nein",
          bestaetigt=["Fachabi Juli 2025", "Mittlere Reife Juli 2023"])],
    "absaetze": [
        "das Schrauben macht mir Spaß: Mein Moped repariere ich selbst, und die Kupplung habe ich mithilfe von YouTube selbst gewechselt.",
        "In Ihrer Anzeige nennen Sie handwerkliches Geschick und Interesse an Technik. "
        "Seit August 2025 arbeite ich mit 20 Wochenstunden in der Gartenabteilung eines Baumarkts. "
        "Dort verräume ich Ware und mache Rasenmäher für den Verkauf fertig.",
        "Im Juli 2025 habe ich an der FOS Landshut mein Fachabitur im Bereich Wirtschaft erworben. "
        "Mit dem Moped bin ich in zehn Minuten bei Ihnen.",
        "Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("das Schrauben macht mir Spaß: Mein Moped repariere ich selbst, und die Kupplung habe ich mithilfe von YouTube selbst gewechselt.",
          (10, "schrauben macht spaß. moped selber repariert"), (13, "moped kupplung selber gewechselt mit youtube")),
        S("In Ihrer Anzeige nennen Sie handwerkliches Geschick und Interesse an Technik.", {"anzeige": "Interesse an Technik"}, {"anzeige": "handwerkliches Geschick"}),
        S("Seit August 2025 arbeite ich mit 20 Wochenstunden in der Gartenabteilung eines Baumarkts.", (10, "baumarkt seit august 25 gartenabteilung 20h")),
        S("Dort verräume ich Ware und mache Rasenmäher für den Verkauf fertig.", (11, "b und c. rasenmäher fertig machen für verkauf")),
        S("Im Juli 2025 habe ich an der FOS Landshut mein Fachabitur im Bereich Wirtschaft erworben.",
          (10, "fachabi 2025 fos landshut wirtschaft"), (16, "Fachabi Juli 2025")),
        S("Mit dem Moped bin ich in zehn Minuten bei Ihnen.", (10, "nah. 10 min mit moped"))],
}

# ---------------------------------------------------------------- Transkript 654 (Thomas, Bäcker → Qualitätssicherung)
F654 = {
    "name": "Thomas Reischl", "anrede_form": "sie",
    "ziel": {"stelle": "Mitarbeiter Qualitätssicherung (m/w/d) – Quereinstieg", "firma": "Donautal Backwaren GmbH",
             "ansprechperson": "Frau Pöllmann", "anrede": "Sehr geehrte Frau Pöllmann,",
             "anzeige_text": "Mitarbeiter Qualitätssicherung (m/w/d) – Quereinstieg, Ref. QS-2026-11, Donautal Backwaren GmbH, Neuburg an "
                             "der Donau. Tagschicht Mo–Fr. Profil: Ausbildung im Lebensmittelbereich (z. B. Bäcker/in), HACCP-Kenntnisse, "
                             "sorgfältige Arbeitsweise, Excel-Grundkenntnisse, Führerschein B. Bewerbung per E-Mail an Frau Pöllmann."},
    "rohtext": [
        R(5, "Thomas Reischl, Gerolfinger Straße 18, 85049 Ingolstadt, Tel. 0171 2290457, E-Mail thomas.reischl@t-online.de"),
        R(6, "Ausbildung zum Bäcker bei der Bäckerei Hutter in Ingolstadt von 09/2004 bis 07/2007. Seitdem dort Bäckergeselle in der Backstube, seit 2015 Schichtleiter in der Nachtschicht. Ich mache die Teigführung, plane mit der Chefin die Bestellmengen für 6 Filialen und leite 2 Azubis an. Ich führe auch die Temperatur- und Reinigungslisten für die Hygiene. Muss ich die Hauptschule auch angeben?"),
        R(7, "Staplerschein seit 2019. HACCP-Schulung jedes Jahr, letzte im März 2026. Computer: Word und Excel Grundlagen, die Bestellungen machen wir in einer Excel-Tabelle. Englisch nur Schulenglisch."),
        R(9, "Ich arbeite seit 2008 nachts und möchte endlich tagsüber arbeiten. Mit der Bäckerei selbst bin ich zufrieden."),
        R(10, "In der Backstube achte ich schon immer darauf, dass alles nach Vorschrift läuft, die Hygienelisten führe ich seit Jahren. Das würde ich gern hauptberuflich machen."),
        R(11, "Tagschicht Montag bis Freitag, nur 20 Minuten mit dem Auto, und die backen auch, da kenne ich mich aus."),
        R(12, "Einmal hatte die Kühlung im Teigraum nachts 9 statt 4 Grad. Ich habe es auf der Temperaturliste gesehen, die Teige gesperrt, die Chefin angerufen und den Kältetechniker bestellt. Es ist keine Ware an Kunden gegangen."),
        R(13, "Kündigungsfrist 3 Monate zum Monatsende, also frühestens 01.03.2027. Muss ich vorher kündigen, bevor ich mich bewerbe?"),
        R(15, "Ja", "So eintragen: 38.000–40.000 EUR brutto/Jahr? a) Ja b) Ändern", bestaetigt="38.000–40.000 EUR brutto/Jahr")],
    "absaetze": [
        "seit 2008 arbeite ich nachts in der Backstube der Bäckerei Hutter und möchte nun tagsüber arbeiten. "
        "Für die Hygiene führe ich seit Jahren die Temperatur- und Reinigungslisten und achte darauf, dass alles nach Vorschrift läuft. "
        "Diese Aufgabe möchte ich gern hauptberuflich in der Qualitätssicherung übernehmen.",
        "In Ihrer Anzeige nennen Sie HACCP-Kenntnisse und eine sorgfältige Arbeitsweise. "
        "Die HACCP-Schulung besuche ich jedes Jahr, zuletzt im März 2026. "
        "Einmal hatte die Kühlung im Teigraum nachts 9 statt 4 Grad. "
        "Ich habe es auf der Temperaturliste bemerkt, die Teige gesperrt, die Chefin angerufen und einen Kältetechniker bestellt. "
        "So ist keine Ware an Kundinnen und Kunden gegangen. "
        "Seit 2015 bin ich Schichtleiter in der Nachtschicht und leite zwei Auszubildende an.",
        "Ihr Betrieb bietet eine Tagschicht von Montag bis Freitag, ist mit dem Auto in 20 Minuten erreichbar und backt ebenfalls – damit kenne ich mich aus.",
        "Ich kann frühestens am 1. März 2027 beginnen. Meine Gehaltsvorstellung liegt bei 38.000 bis 40.000 Euro brutto im Jahr. "
        "Ich freue mich auf ein persönliches Gespräch."],
    "herkunft": [
        S("seit 2008 arbeite ich nachts in der Backstube der Bäckerei Hutter und möchte nun tagsüber arbeiten.",
          (9, "Ich arbeite seit 2008 nachts und möchte endlich tagsüber arbeiten"), (6, "Bäckerei Hutter"), (6, "Backstube")),
        S("Für die Hygiene führe ich seit Jahren die Temperatur- und Reinigungslisten und achte darauf, dass alles nach Vorschrift läuft.",
          (6, "Ich führe auch die Temperatur- und Reinigungslisten für die Hygiene"), (10, "achte ich schon immer darauf, dass alles nach Vorschrift läuft, die Hygienelisten führe ich seit Jahren")),
        S("Diese Aufgabe möchte ich gern hauptberuflich in der Qualitätssicherung übernehmen.", (10, "Das würde ich gern hauptberuflich machen.")),
        S("In Ihrer Anzeige nennen Sie HACCP-Kenntnisse und eine sorgfältige Arbeitsweise.", {"anzeige": "HACCP-Kenntnisse, sorgfältige Arbeitsweise"}),
        S("Die HACCP-Schulung besuche ich jedes Jahr, zuletzt im März 2026.", (7, "HACCP-Schulung jedes Jahr, letzte im März 2026")),
        S("Einmal hatte die Kühlung im Teigraum nachts 9 statt 4 Grad.", (12, "Einmal hatte die Kühlung im Teigraum nachts 9 statt 4 Grad.")),
        S("Ich habe es auf der Temperaturliste bemerkt, die Teige gesperrt, die Chefin angerufen und einen Kältetechniker bestellt.",
          (12, "Ich habe es auf der Temperaturliste gesehen, die Teige gesperrt, die Chefin angerufen und den Kältetechniker bestellt.")),
        S("So ist keine Ware an Kundinnen und Kunden gegangen.", (12, "Es ist keine Ware an Kunden gegangen.")),
        S("Seit 2015 bin ich Schichtleiter in der Nachtschicht und leite zwei Auszubildende an.", (6, "seit 2015 Schichtleiter in der Nachtschicht"), (6, "leite 2 Azubis an")),
        S("Ihr Betrieb bietet eine Tagschicht von Montag bis Freitag, ist mit dem Auto in 20 Minuten erreichbar und backt ebenfalls – damit kenne ich mich aus.",
          (11, "Tagschicht Montag bis Freitag, nur 20 Minuten mit dem Auto, und die backen auch, da kenne ich mich aus.")),
        S("Ich kann frühestens am 1. März 2027 beginnen.", (13, "frühestens 01.03.2027")),
        S("Meine Gehaltsvorstellung liegt bei 38.000 bis 40.000 Euro brutto im Jahr.", (15, "38.000–40.000 EUR brutto/Jahr"))],
}

EHRLICH = {"15": F15, "72": F72, "158": F158, "651": F651, "976": F976, "605": F605, "654": F654}


def profil(f, beispiel, upload_pfad=None):
    """Fall → vollständige Profil-JSON (auf Basis des Beispiels, alle Beispiel-Inhalte geleert)."""
    d = copy.deepcopy(beispiel)
    d["person"].update({"name": f["name"], "strasse": "", "plz_ort": "", "telefon": "", "email": ""})
    d["meta"]["anrede_form"] = f.get("anrede_form", "du")
    d["ziel"] = dict(d["ziel"], **f["ziel"])
    d["ziel"]["firma_adresse"] = [f["ziel"]["firma"]]
    d["ziel"]["kennziffer"] = ""
    d["profil"]["rohtext"] = copy.deepcopy(f["rohtext"])
    d["profil"].update({"beispiele": [], "hobbys": [], "anlagen": [], "quellen": [], "luecken": [], "wie_aufmerksam": ""})
    if upload_pfad:
        d["profil"]["anlagen"] = [{"datei": upload_pfad, "bezeichnung": "Arbeitszeugnis"}]
    d["firmenfakten"] = copy.deepcopy(f.get("firmenfakten", []))
    d["anschreiben"] = {"typ": f.get("typ", "anschreiben"), "betreff": "Bewerbung als " + f["ziel"]["stelle"],
                        "anrede": f["ziel"]["anrede"], "absaetze": copy.deepcopy(f["absaetze"]), "gruss": "Mit freundlichen Grüßen",
                        "ort_datum": "", "anlagen_zeile": None}
    d["herkunft"] = copy.deepcopy(f["herkunft"])
    d["lebenslauf"] = {"kurzprofil": "", "abschnitte": [], "kenntnisse": [], "interessen": ""}
    d["formular"], d["email"], d["whatsapp"] = [], {"betreff": "", "text": ""}, {"text": ""}
    d["belege"] = []
    return d


# ---------------------------------------------------------------- Erfindungs-Fälle (alle vier Fehlerlisten + Runde 4)
# (name, basisfall, absatz_neu, herkunft_eintrag, erwartete Wörter im ❌)
ERFUNDEN = [
    ("R3/500 Häufigkeit+Fähigkeit: „täglich … lerne schnell“", "158",
     "Mit SAP arbeite ich täglich und lerne neue Programme schnell.",
     S("Mit SAP arbeite ich täglich und lerne neue Programme schnell.", (8, "sap so bisschen vom kögel noch")), ["täglich", "lerne", "schnell"]),
    ("R3/530 Fähigkeit: „schwer tragen bin ich gewohnt“", "158",
     "Schwere Lasten zu tragen bin ich gewohnt.",
     S("Schwere Lasten zu tragen bin ich gewohnt.", (7, "lkws be und entladen")), ["tragen", "gewohnt"]),
    ("R3/920 Tätigkeit: „wie Waren ankommen und weitergehen“", "72",
     "Mich interessiert, wie Waren verteilt und verbucht werden.",
     S("Mich interessiert, wie Waren verteilt und verbucht werden.", (10, "ich find es cool wie alles ankommt")), ["verteilt", "verbucht"]),
    ("R3/941 Kontakt zur Firma: „am Stand kennengelernt“", "651",
     "Ihr Team habe ich bereits am Tag der offenen Tür kennengelernt.",
     S("Ihr Team habe ich bereits am Tag der offenen Tür kennengelernt.", (14, "15 min mit der ubahn")), ["kennengelernt"]),
    ("R2 Motiv ohne Quelle: „Genau so möchte ich später arbeiten“", "976",
     "Genau so möchte ich später arbeiten.", None, ["Satz ohne Quelle"]),
    ("R2 Eigenschaft: „Ich bin sehr zuverlässig“", "605",
     "Ich bin sehr zuverlässig und belastbar.",
     S("Ich bin sehr zuverlässig und belastbar.", (10, "schrauben macht spaß")), ["zuverlässig", "belastbar"]),
    ("R4 Intensität: Englisch „gut“ → „sehr gut“", "15",
     "Mein Englisch ist sehr gut.", S("Mein Englisch ist sehr gut.", (5, "Englisch gut")), ["sehr"]),
    ("R4 Gefühl: „cool“ → „begeistert mich schon immer“", "72",
     "Logistik begeistert mich schon immer.", S("Logistik begeistert mich schon immer.", (10, "ich find es cool wie alles ankommt")),
     ["begeistert", "immer"]),
    ("R4 Ich-Aussage aus Anzeige + beliebigem Zitat", "605",
     "Ich bin teamfähig, wie Sie es sich wünschen.",
     S("Ich bin teamfähig, wie Sie es sich wünschen.", {"anzeige": "Teamfähigkeit"}, (10, "nah. 10 min mit moped")), ["teamfähig"]),
    ("R4 Motiv „spricht mich an“ nur aus Firmenfakt + Ja", "651",
     "Mich spricht an, dass Auszubildende bei Ihnen eigene Versicherte betreuen.",
     S("Mich spricht an, dass Auszubildende bei Ihnen eigene Versicherte betreuen.",
       {"firmenfakt": "Azubis betreuen ab dem 2. Ausbildungsjahr eigene Versicherte im Kundencenter"}, (14, "ja stimmt")), ["spricht"]),
    ("R4 Tätigkeit aus NICHT gewählter Option („Kunden beraten“)", "605",
     "Im Baumarkt berate ich Kunden.", S("Im Baumarkt berate ich Kunden.", (11, "b und c")), ["berate"]),
    ("R4 Zahl: 7. statt 5. Semester", "15",
     "Ich bin im siebten Semester.", S("Ich bin im siebten Semester.", (2, "jetzt 5. Semester")), ["siebten"]),
    ("R4 Zahl: acht statt 6 Azubis", "15",
     "Insgesamt habe ich 8 Auszubildende betreut.", S("Insgesamt habe ich 8 Auszubildende betreut.", (4, "Habe 6 Azubis betreut")), ["8"]),
    ("R4 Synonym nur in eine Richtung: Kunden ≠ Kollegen eingearbeitet", "651",
     "Neue Kollegen habe ich im Kundenservice eingearbeitet.",
     S("Neue Kollegen habe ich im Kundenservice eingearbeitet.", (9, "kundenservice bei stromhaus franken")), ["Kollegen", "eingearbeitet"]),
    ("R4 Tippfehler-Toleranz nur für Tippfehler: „Klasse“ ≠ „Kasse“", "72",
     "In der Klasse habe ich die Vorbestellungen fertig gemacht.",
     S("In der Klasse habe ich die Vorbestellungen fertig gemacht.", (12, "in der bäckerei mach ich samstags die vorbestellungen fertig"),
       (4, "verkauf und kasse")), ["Klasse"]),
    ("R4 Ort aus der Wohnadresse („Hotel in München“)", "15",
     "Im Hotel Sonnenhof in München habe ich an der Rezeption gearbeitet.",
     S("Im Hotel Sonnenhof in München habe ich an der Rezeption gearbeitet.", (3, "Rezeption dort bis 09/2024")), ["München"]),
    ("R1 Dauer erfunden: „seit acht Jahren“", "651",
     "Seit acht Jahren arbeite ich im Kundenservice.", S("Seit acht Jahren arbeite ich im Kundenservice.", (9, "seit 10/2023 kundenservice")), ["acht"]),
    ("R4 Gesundheit: „wegen meines Rückens“ ohne Zustimmung", "158",
     "Wegen meines Rückens möchte ich nicht mehr an der Maschine stehen.",
     S("Wegen meines Rückens möchte ich nicht mehr an der Maschine stehen.", (10, "ich will raus aus der schicht")), ["Privates"]),
]
