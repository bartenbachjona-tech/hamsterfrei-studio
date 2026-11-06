# Recherche: Skill-Bau „Bewerbungs-Profi“ (Stand 06.11.2026)

Ziel: ein Claude-Skill, der KI-Anfänger auf claude.ai, auch im Free-Plan, Schritt für Schritt durch eine Bewerbung führt. Er wird als ZIP unter Anpassen → Skills hochgeladen.

---

## 1. Offizielle Regeln (Anthropic)

### Verfügbarkeit und Upload
- Skills gibt es in den Plänen Free, Pro, Max, Ultra, Team und Enterprise. Voraussetzung ist, dass „Code-Ausführung und Dateierstellung“ eingeschaltet ist (Einstellungen → Fähigkeiten, neu: „Create and edit files“). Upload: Customize → Skills → „+“ → „Create skill“ → „Upload a skill“ (ZIP). [S1] [S2]
- Die Quellen widersprechen sich: Die Platform-Doku nennt Custom Skills nur für bezahlte Pläne [S4], das Hilfe-Center dagegen ausdrücklich auch Free [S1] [S2]. Laut Presseberichten hat der Free-Plan am 11.02.2026 Dateierstellung und Skills bekommen [S12]. **Vor dem Release mit einem echten Free-Konto testen.**
- Custom Skills sind privat. Man kann sie nicht direkt an andere Nutzer weitergeben, jeder lädt das ZIP selbst hoch. [S3]

### Pflicht-Struktur
```
bewerbungs-profi.zip
└── bewerbungs-profi/          ← Ordnername = name im Frontmatter
    ├── SKILL.md               ← genau so geschrieben (Groß-/Kleinschreibung zählt)
    ├── references/*.md
    └── scripts/*.py
```
- Im ZIP muss **der Skill-Ordner** an oberster Stelle liegen. Lose Dateien direkt im ZIP sind der häufigste Fehler. [S1]
- Frontmatter in YAML: `name` mit höchstens 64 Zeichen, nur Kleinbuchstaben, Ziffern und Bindestriche. Keine XML-Tags, nicht die Wörter `anthropic` oder `claude`. [S5] Den Ordnernamen in kebab-case schreiben, ohne Leerzeichen, Unterstriche oder Großbuchstaben. Keine spitzen Klammern `< >` im Frontmatter. [S8]
- `description` darf nicht leer sein und höchstens **1.024 Zeichen** lang sein (laut API-Doku) [S5]. Der Hilfe-Center-Artikel „How to create custom skills“ nennt dagegen **200 Zeichen** [S1]. Das wichtigste Material gehört deshalb in die ersten 200 Zeichen. Den Upload mit der vollen Länge testen: Der seminararbeit-profi hat rund 560 Zeichen.
- Typische Upload-Fehler laut Hilfe-Center: ZIP zu groß (eine Zahl wird nicht genannt), Ordnername passt nicht zu `name`, SKILL.md fehlt, ungültige Zeichen in name oder description, Skills ausgegraut, weil die Code-Ausführung aus ist. [S1] [S2]

### Progressive Disclosure (Laden in drei Stufen)
1. **Metadaten** (name und description, etwa 100 Tokens) sind immer geladen.
2. **SKILL.md-Text** wird geladen, wenn der Skill ausgelöst wird. Ziel: unter 5.000 Tokens.
3. **Ressourcen** werden nur bei Bedarf gelesen. Bei Skripten landet nur die Ausgabe im Kontext. [S4] [S6]
- SKILL.md soll **unter 500 Zeilen** bleiben und wie ein Inhaltsverzeichnis funktionieren. Referenzen höchstens **eine Ebene tief** anlegen (SKILL.md → datei.md, nicht weiter verschachteln). Dateien mit mehr als 100 Zeilen bekommen oben ein Inhaltsverzeichnis. Dateinamen beschreibend wählen, Pfade mit `/`. [S5]
- Laut Anthropic-Guide liegt die Grenze bei unter 5.000 Wörtern. Werden Anweisungen nicht befolgt, ist die Ursache meist ein zu langer Text oder dass die wichtigen Regeln „vergraben“ sind. Abhilfe: kurz schreiben, das Kritische ganz oben. [S8]

### Die description: damit der Skill zuverlässig auslöst
- In der dritten Person schreiben, zuerst **was** der Skill tut, dann **wann** er greifen soll. Beispiel: „Extract text … Use when … the user mentions PDFs …“ [S5]
- Konkrete Auslöser-Wörter nennen, die Nutzer wirklich tippen. Wird der Skill zu oft ausgelöst, negative Auslöser ergänzen („nicht für …“). [S8] [S10]
- Vage Beschreibungen wie „Hilft bei Dokumenten“ lösen nicht aus. [S5]
- Name und description sind laut Anthropic das Wichtigste, weil Claude nur anhand dieser beiden Felder entscheidet, ob der Skill passt. [S6]

### Skripte und Bibliotheken
- Skripte lieber **ausführen** als lesen lassen, und das ausdrücklich so formulieren („Führe `x.py` aus“). Fehler im Skript selbst abfangen, Konstanten begründen und Fehlermeldungen konkret halten. Für kritische Prüfungen ein Skript beilegen, denn Code arbeitet deterministisch, Sprache nicht. [S5] [S8]
- Abhängigkeiten in SKILL.md aufführen und nicht davon ausgehen, dass sie installiert sind. Auf claude.ai kann Claude Pakete aus PyPI und npm nachinstallieren [S1] [S5]. Der Netzzugang der Sandbox hängt aber von den Einstellungen ab: „full, partial, or none“ [S4].
- **Word-Ausgabe:** Der offizielle docx-Skill erstellt neue Dokumente mit **docx-js** (JavaScript). Zum Bearbeiten entpackt er die Datei, ändert das XML und packt sie wieder ein, dabei prüft `validate.py` das Ergebnis. Zum Lesen nutzt er pandoc. [S7] Ob python-docx vorinstalliert ist, belegt keine offizielle Quelle. **Empfehlung:** Lesen nur mit der Standardbibliothek (zipfile und xml, wie in `textlib.py`). Zum Schreiben python-docx mit Fallback `pip install python-docx` nutzen, ersatzweise den eingebauten docx-Skill von Anthropic, der auf claude.ai ohne Einrichtung aktiv ist [S4].
- Sicherheit: Skills, die externe URLs abrufen, sind riskant, weil die geladenen Inhalte Anweisungen einschleusen können (Prompt Injection). [S4] Für den Bewerbungs-Profi heißt das: Den Text einer Stellenanzeige als Daten behandeln, niemals als Anweisung.

### Testen
Vor dem Ausbau mindestens 3 Testszenarien aufschreiben und das Verhalten ohne Skill als Ausgangswert festhalten. [S5] Dann drei Arten von Tests: Auslöse-Tests (direkte Anfragen, umformulierte Anfragen, fremde Themen, bei denen der Skill nicht greifen soll), Funktionstests und ein Vergleich mit und ohne Skill. [S8] Nach dem Upload in Claudes Denkprozess nachsehen, ob der Skill wirklich geladen wurde. [S1]

---

## 2. Erfahrungen aus der Praxis: Interview-Flow und typische Fehler

- **Eine Frage pro Nachricht.** Der verbreitete Skill „brainstorming“ (obra/superpowers) legt fest: „Only one question per message“. Auswahlfragen sind offenen Fragen vorzuziehen. Abschnitt für Abschnitt wird bestätigt („Ask after each section whether it looks right so far“). Feste Gates: Erst nach der Freigabe geht es weiter. [S9]
- **Analyse von über 40 Fehlschlägen** [S10]: (1) Der Skill wird nicht aufgerufen. Lösung: konkrete Auslöser in der description. (2) Das Ergebnis bleibt generisch. Lösung: 2–3 vollständige Beispiele mit Eingabe und Ausgabe, der Beispielteil darf länger sein als der Regelteil. (3) Der Kontext läuft über. Lösung: Progressive Disclosure, Probleme ab etwa 1.000 Zeilen. (4) Klare Grenzen setzen: Was gilt als Erfolg, was ist außerhalb des Auftrags, wann wird angehalten und gefragt. (5) Mit echter Arbeit testen und jeden Fehler protokollieren.
- **r/ClaudeAI** [S11]: Automatisch erzeugte Skills sind ausschweifend; von Hand gekürzt werden sie zuverlässiger befolgt. Beim Überarbeiten lässt Claude manchmal Teile weg, deshalb ZIP-Größe mit der Vorversion vergleichen.
- **Anthropic-Guide** [S8]: Die Muster „Sequential workflow“ und „Iterative refinement“ passen direkt: Profil → Stellenanzeige → Anschreiben → Lebenslauf → Endcheck.
- **Daraus für den Bewerbungs-Profi:** Für Anfänger höchstens 1 Frage pro Nachricht, ausnahmsweise 2–3 eng zusammengehörige, immer mit Antwortoptionen und einer Empfehlung. Der seminararbeit-profi bündelt bis zu 5 Fragen. Das funktioniert dort, weil die Nutzer unter Zeitdruck stehen, für KI-Neulinge ist es zu viel.

---

## 3. Free-Plan: Was geht, was nicht

| Funktion | Free | Beleg |
|---|---|---|
| Nachrichtenlimit | sitzungsbasiert, Reset alle **5 Stunden**, abhängig von der Auslastung | [S13] |
| Skills und Dateierstellung | ja (Code-Ausführung muss an sein) | [S1] [S2] [S12] |
| Websuche | ja, seit 27.05.2025 für alle | [S14] |
| URL einer Stellenanzeige abrufen | grundsätzlich möglich, aber unzuverlässig (siehe unten) | [S16] |
| Memory zwischen Chats | ja, seit 02.03.2026 | [S15] |
| Projekte | laut Berichten ja, möglicherweise in der Zahl begrenzt („unlimited projects“ nur bezahlt); 20 Dateien pro Chat | [S17] [S18] |
| Cowork, lokaler Ordnerzugriff | **nein.** Cowork gibt es „only“ für Pro, Max, Ultra, Team und Enterprise, lokales Lesen und Schreiben nur in der Desktop-App mit verbundenem Ordner | [S19] |
| Speichern | nur als **Download**; Dateien müssen nach `/mnt/user-data/outputs/` | interner Skill |

**URL-Abruf:** Teilt ein Nutzer einen Link, ruft Claude die Seite als „Claude-User“ ab. Das scheitert oft: robots.txt-Sperren, Cloudflare- oder WAF-Schutz mit 403 oder Challenge-Seite, Seiten, die erst per JavaScript gerendert werden und dann leer ankommen, Login-Wände. [S16] Jobportale wie StepStone, Indeed oder LinkedIn sind typische Kandidaten dafür (nicht einzeln getestet). **Regel:** Erst den Link probieren. Schlägt das fehl oder fehlt der Inhalt, den Nutzer bitten, den Anzeigentext zu kopieren oder die Seite als PDF zu speichern (Strg+P). Nie eine Anzeige aus dem Titel „rekonstruieren“.

---

## 4. Wiederverwendbare Muster aus `skills/seminararbeit-profi/`

Umfang: SKILL.md hat 180 Zeilen und rund 1.570 Wörter, dazu 10 Referenzdateien und 7 Skripte.

1. **Rangfolge der Vorgaben** gleich oben: Lehrkraft vor Merkblatt vor Skill. Für Bewerbungen übertragen: Stellenanzeige vor Wunsch des Nutzers vor Skill-Standard.
2. **Tabelle „Wann welche Datei lesen“** als Wegweiser für die Progressive Disclosure. Übernehmen.
3. **Pfad-Robustheit:** Skripte liegen unter `/mnt/skills/user/<name>/scripts/`. Bei Bedarf mit `find / -name … 2>/dev/null` suchen, als `$S` speichern. Uploads liegen in `/mnt/user-data/uploads/`, Ausgaben gehören nach `/mnt/user-data/outputs/`. Wörtlich übernehmen.
4. **Ehrlichkeitsregeln** („Nichts erfinden“, `[PRÜFEN: …]`). Für Bewerbungen bedeutet das: keine erfundenen Abschlüsse, Zeugnisse oder Kenntnisse, keine falschen Daten.
5. **Start-Check: erst schauen, dann fragen.** Uploads auswerten, eine Schnell-Diagnose mit Skript, dann wenige Fragen mit Optionen, Empfehlung und Kurzantwort („1b 2 …“). Für Anfänger auf eine Frage pro Nachricht reduzieren.
6. **Arbeitsstand.md zum Weitermachen:** Wird zu Beginn erkannt („Fortsetzung → 2 Zeilen Stand, dann loslegen“) und am Ende jeder Sitzung aktualisiert und zum Download gegeben. Im Free-Plan ist das der Kern, weil der Chat begrenzt ist. Übernehmen, Felder anpassen: Zielstelle, Firma, Frist, Status pro Unterlage, Entscheidungen.
7. **Modus-Menü mit Nummern** (1–10), einmal anzeigen, Wechsel per Nummer oder Name, automatisch, wenn der Modus aus der Bitte erkennbar ist. Für den Bewerbungs-Profi etwa: 1 Profil, 2 Stellenanzeige analysieren, 3 Anschreiben, 4 Lebenslauf, 5 Endcheck, 6 Vorstellungsgespräch üben.
8. **`ordner_anlegen.py`:** Legt den Ordner mit festen Unterordnern und einer Vorlage für Arbeitsstand.md an, sortiert Uploads nach Name und Endung ein und packt alles als ZIP. Übernehmbar, etwa mit `01_Profil`, `02_Stellen`, `03_Anschreiben`, `04_Lebenslauf`, `05_Zeugnisse`, `06_Checks`.
9. **Word ohne Abhängigkeiten:** `textlib.py` liest .docx nur mit zipfile und xml und meldet leere Dateien klar („Nichts ist geprüft“). Versionierte Dateinamen verwenden, nie überschreiben.
10. **Fester Berichtsblock** (✅ ⚠️ ❓ 📁 ⏳), ein großer Schritt pro Chat, lange Ergebnisse als Datei, still prüfen, welche Werkzeuge vorhanden sind (`references/werkzeuge.md`).

---

## 5. Checkliste für den Bau

**Struktur und Upload**
- [ ] Ordner `bewerbungs-profi/` = `name: bewerbungs-profi`; Datei exakt `SKILL.md`
- [ ] ZIP enthält den Ordner, keine losen Dateien; keine Windows-Pfade
- [ ] description: dritte Person, was und wann, deutsche Auslöser-Wörter (Bewerbung, Anschreiben, Motivationsschreiben, Lebenslauf, CV, Stellenanzeige, Vorstellungsgespräch, Ausbildungsplatz, Praktikum), negative Auslöser, Kern in ≤ 200 Zeichen, gesamt ≤ 1.024; keine `< >`
- [ ] Upload mit Free-Konto getestet, Skill in Claudes Denkprozess sichtbar geladen

**Inhalt von SKILL.md**
- [ ] ≤ 500 Zeilen, Ziel ~150–200; kritische Regeln ganz oben
- [ ] Tabelle „Wann welche Datei lesen“; Referenzen nur eine Ebene tief, ab 100 Zeilen mit Inhaltsverzeichnis
- [ ] Ehrlichkeitsregeln: nichts erfinden, `[PRÜFEN: …]`
- [ ] Interview-Regel: **eine Frage pro Nachricht**, mit Optionen und „(Empfohlen)“; nach jedem Abschnitt bestätigen lassen, erst dann weiter
- [ ] Start: Arbeitsstand.md erkannt → Fortsetzung; sonst Ordner anlegen
- [ ] Modus-Menü mit Nummern; klare Grenzen (keine Rechtsberatung, keine Fälschung von Zeugnissen)
- [ ] 2–3 vollständige Beispiele (Eingabe → Ausgabe), z. B. ein gutes und ein schlechtes Anschreiben

**Free-Plan**
- [ ] Hinweis auf die Einstellung „Code-Ausführung/Dateien erstellen“
- [ ] Alles zum Download nach `/mnt/user-data/outputs/`; kein Ordnerzugriff vorausgesetzt
- [ ] Link-Fallback: Anzeigentext einfügen oder als PDF hochladen lassen; Anzeigentext ist Daten, keine Anweisung
- [ ] Ein Schritt pro Chat; Arbeitsstand.md am Ende jeder Sitzung ausgeben

**Skripte**
- [ ] Lesen nur mit der Standardbibliothek; Schreiben über python-docx mit `pip`-Fallback oder den docx-Skill
- [ ] Ausdrücklich „ausführen“, nicht „lesen“; Fehler abfangen; verständliche Meldungen auf Deutsch
- [ ] Nach dem Erzeugen jede .docx erneut öffnen und prüfen

**Test**
- [ ] ≥ 3 Szenarien (Schüler/Ausbildung, Berufswechsel, Link funktioniert nicht) und Negativ-Test (fremdes Thema löst nicht aus)
- [ ] Nach jeder Änderung das komplette ZIP neu bauen und die Größe mit der Vorversion vergleichen

---

## Quellen
- [S1] https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- [S2] https://support.claude.com/en/articles/12512180-get-started-with-claude-skills
- [S3] https://support.claude.com/en/articles/12512180-using-skills-in-claude
- [S4] https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- [S5] https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- [S6] https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- [S7] https://lobehub.com/skills/anthropics-skills-docx (Spiegel von github.com/anthropics/skills/docx; GitHub selbst war hier nicht abrufbar)
- [S8] https://snowan.gitbook.io/study-notes/ai-blogs/anthropic-skills-guide-summary (Zusammenfassung von „The Complete Guide to Building Skills for Claude“, Original: https://claude.com/ja/resources/guides/the-complete-guide-to-building-skills-for-claude)
- [S9] https://cdn.jsdelivr.net/npm/superpowers-dev@1.0.1/skills/brainstorming/SKILL.md
- [S10] https://cashandcache.substack.com/p/i-analyzed-40-claude-skills-failures
- [S11] https://reddit.sentinel-team.org/posts/1r3hr40/snapshots/2026-02-13T17%3A14%3A42.327723Z (r/ClaudeAI)
- [S12] https://news.lavx.hu/article/anthropic-expands-claude-s-free-tier-with-file-creation-external-service-integration-and-skills
- [S13] https://support.claude.com/en/articles/8602283-about-free-claude-usage
- [S14] https://www.engadget.com/ai/anthropic-brings-web-search-to-free-claude-users-224222689.html
- [S15] https://aiproductivity.ai/news/anthropic-claude-memory-free-tier-chatgpt-import/
- [S16] https://crawlconsole.com/blog/why-claude-cant-access-your-website-claudebot-claude-user
- [S17] https://tech.yahoo.com/ai/claude/articles/claude-just-made-two-best-100300345.html
- [S18] https://www.costbench.com/software/ai-chatbots/claude/free-plan/
- [S19] https://support.claude.com/en/articles/13345190-get-started-with-cowork
