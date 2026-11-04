import React from "react";
import { AbsoluteFill, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { Hamster } from "../Hamster";
import { INK, GREEN, NAVY, CREAM } from "../Scenes";
import type { Word } from "../Episode";
import wordsData from "./seminar05.words.json";

// Seminar-Offensive S1 · „Abgabe am 10. November?!“ · Produkt: Seminararbeit-Profi (eigenes Produkt → Werbung)
const fontFamily = "Fredoka";
loadFont({ family: fontFamily, url: staticFile("fonts/fredoka-latin.woff2"), weight: "300 700" });
loadFont({ family: fontFamily, url: staticFile("fonts/fredoka-latin-ext.woff2"), weight: "300 700", unicodeRange: "U+0100-024F, U+1E00-1EFF, U+20A0-20AB, U+20AD-20CF" });

const RED = "#C8473A";
const YEL = "#D9A32B";
const MUTED = "#6B5444";
const FLOOR = "#F5E7CF";

const ALL = (wordsData as { words: Word[] }).words;
const WORDS = ALL.filter((w) => w.type === "word");
const norm = (s: string) => s.toLowerCase().replace(/[^a-zäöüß0-9-]/g, "");
// Startzeit des n-ten Worts, das mit `w` beginnt (nach Wort-Index `after`)
const at = (w: string, after = 0): number => {
  const i = WORDS.findIndex((x, k) => k >= after && norm(x.text).startsWith(w));
  if (i < 0) throw new Error("Wort nicht gefunden: " + w);
  return WORDS[i].start;
};
const idx = (w: string, after = 0) => WORDS.findIndex((x, k) => k >= after && norm(x.text).startsWith(w));

// Seminar05 · „Sechs Tage, null Seiten“ (Muster S1, Jona 04.11.2026) · Werbung eigenes Produkt
const iDesh = idx("deshalb");
const M = {
  abgabe: at("abgabe"),
  nullS: at("null"),
  keine: at("keine"),
  stell: at("du"), // Schreibtisch ab „Du gibst Claude …“
  laedst: at("du"),
  thema: at("thema"),
  aber: at("aber"),
  gliederung: at("gliederung"),
  ffrage: at("forschungsfrage"),
  schreibt: at("deshalb"),
  kapitel: at("kapitel", iDesh),
  quellenS: at("quellen", iDesh),
  fn: at("fußnoten", iDesh),
  fehlen: at("dir", idx("fußnoten")),
  diagramm: at("er", idx("zahlen")),
  diagramme: at("diagramm"),
  deckblatt: at("deckblatt"),
  lit: at("literatur"),
  raender: at("seitenränder"),
  merkblatt: at("merkblatt"),
  uebt: at("und", idx("schule")),
  genau: at("genau"),
  sechs2: at("sechs", idx("genau")),
  reichen: at("reichen"),
  skill: at("der", idx("reichen")),
  link: at("den", idx("skill")),
  profil: at("profil"),
  end: WORDS[WORDS.length - 1].end,
};
// Seitenzähler im Claude-Fenster: 0 bis zur Gliederung, dann steigend bis zur Pointe
const pages = (t: number) => Math.round(interpolate(t, [M.gliederung, M.reichen], [1, 15], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })) * (t >= M.gliederung ? 1 : 0);
export const SEMINAR05_SECONDS = Math.ceil((M.end + 2.2) * 10) / 10;

// ---------- Helfer ----------
const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const pop = (t: number, start: number, fps: number) =>
  t < start ? 0 : spring({ frame: (t - start) * fps, fps, config: { damping: 13, stiffness: 170 } });
const fade = (t: number, a: number, b: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const Card: React.FC<{ show: number; style?: React.CSSProperties; children: React.ReactNode; rot?: number }> = ({ show, style, children, rot = 0 }) => (
  <div
    style={{
      position: "absolute",
      background: "#fff",
      border: `6px solid ${INK}`,
      borderRadius: 28,
      padding: "18px 30px",
      fontSize: 50,
      fontWeight: 600,
      lineHeight: 1.15,
      boxShadow: "0 18px 0 rgba(58,38,24,.12)",
      scale: String(show),
      opacity: show > 0.02 ? 1 : 0,
      rotate: `${rot}deg`,
      ...style,
    }}
  >
    {children}
  </div>
);

// Schweißtropfen
const Sweat: React.FC<{ t: number; until: number }> = ({ t, until }) => {
  if (t > until + 0.4) return null;
  const drops = [
    { x: 40, d: 0 },
    { x: 410, d: 0.35 },
    { x: 380, d: 0.8 },
    { x: 70, d: 1.15 },
  ];
  return (
    <>
      {drops.map((dr, i) => {
        const cyc = ((t + dr.d) % 1.2) / 1.2;
        const y = 60 + cyc * 160;
        const o = interpolate(cyc, [0, 0.15, 0.8, 1], [0, 1, 1, 0]) * (t > until ? 0 : 1);
        return (
          <svg key={i} viewBox="0 0 20 30" width={34} height={50} style={{ position: "absolute", left: dr.x, top: y, opacity: o }}>
            <path d="M10 1 C14 10 19 15 19 20 A9 9 0 0 1 1 20 C1 15 6 10 10 1Z" fill="#7CC4F0" stroke={INK} strokeWidth={2} />
          </svg>
        );
      })}
    </>
  );
};

// ---------- Teil 1: Panik ----------
const Panic: React.FC = () => {
  const { t, fps, frame } = useT();
  const calm = t >= M.keine;
  const shake = calm ? 0 : Math.sin(frame * 1.9) * 7;
  const talking = WORDS.some((w) => t >= w.start && t <= w.end) && frame % 6 < 3;
  const calendar = Math.max(0.85, pop(t, -0.25, fps));
  const ring = interpolate(t, [0.6, 1.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const out = calm ? interpolate(t, [M.keine, M.keine + 0.35], [1, 0], { extrapolateRight: "clamp" }) : 1;
  const calmIn = pop(t, M.keine, fps);
  const bg = calm ? "#E8F4EC" : interpolate(Math.sin(frame / 4), [-1, 1], [0, 1]) > 0.5 ? "#FDE8E4" : "#FBE1DC";
  return (
    <AbsoluteFill style={{ background: bg }}>
      {/* Kalender */}
      <div style={{ opacity: out }}>
        <div style={{ position: "absolute", left: 300, top: 150, width: 480, scale: String(calendar), rotate: `${calm ? 0 : Math.sin(frame / 3) * 2}deg` }}>
          <div style={{ background: RED, color: "#fff", border: `7px solid ${INK}`, borderBottom: "none", borderRadius: "34px 34px 0 0", textAlign: "center", fontSize: 56, fontWeight: 600, padding: "14px 0" }}>NOVEMBER</div>
          <div style={{ background: "#fff", border: `7px solid ${INK}`, borderRadius: "0 0 34px 34px", textAlign: "center", fontSize: 230, fontWeight: 700, lineHeight: 1.05, position: "relative" }}>
            10
            <svg viewBox="0 0 200 120" style={{ position: "absolute", left: 40, top: 20, width: 390, height: 240 }}>
              <ellipse cx={100} cy={60} rx={92} ry={52} fill="none" stroke={RED} strokeWidth={8} strokeDasharray={600} strokeDashoffset={600 * (1 - ring)} strokeLinecap="round" />
            </svg>
          </div>
          <div style={{ textAlign: "center", fontSize: 54, fontWeight: 600, marginTop: 18 }}>Abgabe Seminararbeit</div>
        </div>
        <Card show={Math.max(0.9, pop(t, -0.2, fps))} rot={-6} style={{ left: 40, top: 110, background: RED, color: "#fff", fontSize: 58 }}>noch 6 Tage!</Card>
        <Card show={pop(t, M.nullS - 0.15, fps)} rot={3} style={{ left: 170, top: 790, width: 740, fontSize: 46 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <svg viewBox="0 0 24 24" width={60} height={60} fill="none" stroke={NAVY} strokeWidth={2}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" /><path d="M14 3v5h5" /></svg>
            Seminararbeit.docx
          </div>
          <div style={{ marginTop: 14, height: 150, background: "#FBF7F0", border: "3px solid #E7D9C2", borderRadius: 12, padding: 16, fontSize: 40 }}>
            <span style={{ opacity: Math.floor(t * 3) % 2 ? 1 : 0 }}>|</span>
          </div>
          <div style={{ marginTop: 12, fontSize: 64, fontWeight: 700, color: RED, textAlign: "center" }}>0 Seiten 😱</div>
        </Card>
      </div>
      {/* Beruhigung */}
      {calm && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center", scale: String(calmIn) }}>
          <div style={{ fontSize: 120, fontWeight: 700, color: GREEN }}>Keine Panik.</div>
          <div style={{ fontSize: 76, fontWeight: 600, marginTop: 10 }}>Ich hab dich. 🐹</div>
        </div>
      )}
      {/* Hamster */}
      <div style={{ position: "absolute", left: 270, top: 1250, translate: `${shake}px 0px` }}>
        <div style={{ position: "relative" }}>
          <Hamster size={540} talking={talking} blink={!calm ? frame % 40 < 3 : frame % 105 < 4} pointerAngle={calm ? -10 : Math.sin(frame / 2) * 8} />
          <div style={{ position: "absolute", left: 0, top: 0 }}>
            <Sweat t={t} until={M.keine} />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Teil 2: Schreibtisch mit Bildschirm ----------
const Bubble: React.FC<{ show: number; me?: boolean; children: React.ReactNode; style?: React.CSSProperties }> = ({ show, me, children, style }) => (
  <div
    style={{
      alignSelf: me ? "flex-end" : "flex-start",
      maxWidth: "86%",
      background: me ? "#F1E6D3" : "#fff",
      border: me ? "none" : `3px solid #E7D9C2`,
      borderRadius: 22,
      padding: "14px 20px",
      fontSize: 40,
      lineHeight: 1.3,
      opacity: show,
      translate: `0px ${(1 - show) * 30}px`,
      ...style,
    }}
  >
    {children}
  </div>
);

const Typed: React.FC<{ text: string; start: number; dur: number }> = ({ text, start, dur }) => {
  const { t } = useT();
  const n = Math.floor(interpolate(t, [start, start + dur], [0, text.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <span>
      {text.slice(0, n)}
      {n < text.length && t >= start && <span style={{ opacity: Math.floor(t * 4) % 2 ? 1 : 0 }}>|</span>}
    </span>
  );
};

const Check: React.FC<{ show: number; label: string; status: "ok" | "warn" | "bad"; note: string }> = ({ show, label, status, note }) => {
  const col = status === "ok" ? GREEN : status === "warn" ? YEL : RED;
  const icon = status === "ok" ? "✓" : status === "warn" ? "!" : "✗";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 18, opacity: show, translate: `${(1 - show) * -40}px 0px`, fontSize: 38, padding: "10px 0", borderBottom: "2px solid #EFE4D2" }}>
      <div style={{ width: 46, height: 46, borderRadius: 23, background: col, color: "#fff", display: "grid", placeItems: "center", fontWeight: 700, fontSize: 30, flex: "none" }}>{icon}</div>
      <div style={{ fontWeight: 600, width: 330 }}>{label}</div>
      <div style={{ color: MUTED, fontSize: 30 }}>{note}</div>
    </div>
  );
};

// Bildschirm-Inhalt je nach Zeit
const Screen: React.FC = () => {
  const { t, fps } = useT();
  const stage =
    t < M.aber ? "thema" : t < M.schreibt ? "gliederung" : t < M.diagramm ? "schreiben" : t < M.deckblatt ? "diagramm" : t < M.uebt ? "formalia" : t < M.sechs2 ? "pruefung" : t < M.skill ? "pointe" : "ende";
  const appear = (s: number) => pop(t, s, fps);
  const f = (a: number) => fade(t, a, a + 0.35);
  const n = pages(t);
  const outline = [
    { at: M.gliederung - 0.9, l: "1  Einleitung" },
    { at: M.gliederung - 0.6, l: "2  Tourismus in Island seit 2010" },
    { at: M.gliederung - 0.3, l: "3  Folgen für den Wohnungsmarkt" },
    { at: M.gliederung, l: "4  Auswirkungen auf die Bevölkerung" },
    { at: M.gliederung + 0.3, l: "5  Fazit" },
  ];

  return (
    <AbsoluteFill style={{ background: "#FBF7F0", fontFamily, color: INK }}>
      <div style={{ height: 70, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 26px", fontSize: 28, fontWeight: 600, borderBottom: "3px solid #E7D9C2" }}>
        <div style={{ width: 18, height: 18, borderRadius: 9, background: "#E5835E" }} />
        Claude
        <span style={{ marginLeft: "auto", background: n >= 15 ? GREEN : n > 0 ? NAVY : RED, color: "#fff", borderRadius: 999, padding: "4px 18px", fontSize: 26 }}>📄 {n} {n === 1 ? "Seite" : "Seiten"}</span>
      </div>

      <div style={{ position: "absolute", left: 30, right: 30, top: 96, bottom: 30, display: "flex", flexDirection: "column", gap: 16 }}>
        {stage === "thema" && (
          <Bubble show={f(M.laedst + 0.1)} me style={{ fontSize: 46 }}>
            <Typed text="Mein Thema: Tourismus in Island. Abgabe in 6 Tagen." start={M.laedst + 0.1} dur={1.3} />
          </Bubble>
        )}
        {stage === "gliederung" && (
          <>
            <div style={{ fontSize: 44, fontWeight: 700, opacity: f(M.aber) }}>Gliederung</div>
            <div style={{ background: "#fff", border: "3px solid #E7D9C2", borderRadius: 14, padding: "14px 24px", fontSize: 32, opacity: f(M.aber + 0.3) }}>
              <span style={{ color: MUTED }}>Forschungsfrage:</span> <b>Wie verändert der Tourismus das Leben in Reykjavík?</b>
            </div>
            <div style={{ background: "#fff", border: "3px solid #E7D9C2", borderRadius: 14, padding: "10px 24px" }}>
              {outline.map((o, i) => (
                <div key={i} style={{ fontSize: 40, fontWeight: 600, padding: "8px 0", borderBottom: i < 4 ? "2px solid #EFE4D2" : "none", opacity: f(o.at), translate: `${(1 - f(o.at)) * -40}px 0px` }}>{o.l}</div>
              ))}
            </div>
            <div style={{ alignSelf: "center", fontSize: 36, fontWeight: 700, background: GREEN, color: "#fff", borderRadius: 999, padding: "8px 26px", scale: String(appear(M.ffrage)), opacity: t >= M.ffrage ? 1 : 0 }}>✓ passt zur Forschungsfrage</div>
          </>
        )}
        {stage === "schreiben" && (
          <div style={{ flex: 1, background: "#fff", border: "3px solid #E7D9C2", borderRadius: 14, padding: "26px 34px", position: "relative" }}>
            <div style={{ fontSize: 42, fontWeight: 700, opacity: f(M.schreibt) }}>4.2 Auswirkungen auf die Bevölkerung</div>
            <div style={{ fontSize: 34, lineHeight: 1.5, marginTop: 14 }}>
              <Typed text="Die Zahl der Ferienwohnungen in Reykjavík stieg zwischen 2014 und 2017 stark an." start={M.kapitel - 0.3} dur={1.6} />
              {t >= M.quellenS && <sup style={{ color: NAVY, fontWeight: 700, opacity: f(M.quellenS) }}>12</sup>}{" "}
              <Typed text="Laut Mermet betraf das vor allem die Innenstadt." start={M.quellenS + 0.2} dur={1.2} />
              {t >= M.fn && <sup style={{ color: NAVY, fontWeight: 700 }}>13</sup>}
            </div>
            <div style={{ position: "absolute", left: 34, right: 34, bottom: 22, borderTop: "2px solid #CFC2AE", paddingTop: 10, fontSize: 26, color: MUTED, opacity: f(M.fn) }}>
              <sup>12</sup> Vgl. Elíasson/Ragnarsson 2018, S. 7.&nbsp;&nbsp;<sup>13</sup> Vgl. Mermet 2019, S. 21.
            </div>
            <div style={{ position: "absolute", right: 34, bottom: 90, background: GREEN, color: "#fff", borderRadius: 999, padding: "6px 18px", fontSize: 26, fontWeight: 600, scale: String(appear(M.quellenS)), opacity: t >= M.quellenS ? 1 : 0 }}>✓ echte Quelle, Seite geprüft</div>
            <div style={{ position: "absolute", left: 34, bottom: 90, background: RED, color: "#fff", borderRadius: 14, padding: "8px 20px", fontSize: 34, fontWeight: 700, rotate: "-4deg", scale: String(appear(M.fehlen)), opacity: t >= M.fehlen ? 1 : 0 }}>Zahlen fehlen? 🤔</div>
          </div>
        )}
        {stage === "diagramm" && (
          <div style={{ flex: 1, background: "#fff", border: "3px solid #E7D9C2", borderRadius: 14, padding: "24px 34px", display: "flex", flexDirection: "column" }}>
            <div style={{ fontSize: 30, color: MUTED, marginBottom: 10, opacity: f(M.diagramm) }}>🔍 Statistik Island · Besucher pro Jahr</div>
            <div style={{ display: "flex", alignItems: "flex-end", gap: 26, height: 360, borderBottom: `4px solid ${INK}`, paddingLeft: 10 }}>
              {[0.65, 0.78, 0.97, 1.26, 1.77, 2.2, 2.32].map((v, i) => {
                const g = interpolate(t, [M.diagramm + 0.3 + i * 0.12, M.diagramm + 0.7 + i * 0.12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
                return (
                  <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end", height: "100%" }}>
                    <div style={{ fontSize: 24, color: MUTED, opacity: g }}>{v.toString().replace(".", ",")}</div>
                    <div style={{ width: "100%", height: `${(v / 2.4) * 300 * g}px`, background: i > 4 ? "#2a78d6" : "#9cc2ee", borderRadius: "8px 8px 0 0" }} />
                  </div>
                );
              })}
            </div>
            <div style={{ display: "flex", gap: 26, paddingLeft: 10, fontSize: 24, color: MUTED, marginTop: 6 }}>
              {["2012", "2013", "2014", "2015", "2016", "2017", "2018"].map((y) => <div key={y} style={{ flex: 1, textAlign: "center" }}>{y}</div>)}
            </div>
            <div style={{ fontSize: 28, fontStyle: "italic", marginTop: 18, opacity: f(M.diagramme) }}>Abbildung 2: Besucher in Island (in Mio.)</div>
            <div style={{ fontSize: 24, color: MUTED, marginTop: 4, opacity: f(M.diagramme + 0.3) }}>Achsen beschriftet · Quelle in der Fußnote · Dezimalkomma ✓</div>
          </div>
        )}
        {stage === "formalia" && (
          <>
            <div style={{ fontSize: 44, fontWeight: 700 }}>Formalia · nach Merkblatt</div>
            <div>
              <Check show={f(M.deckblatt)} label="Deckblatt" status="ok" note="Schule, Fach, Lehrkraft ✓" />
              <Check show={f(M.lit)} label="Literaturverz." status="ok" note="24 Quellen, alphabetisch" />
              <Check show={f(M.raender)} label="Seitenränder" status="ok" note="links 2,5 cm · rechts 4 cm" />
              <Check show={f(M.merkblatt)} label="Schrift / Zeilen" status="ok" note="12 pt · 1,5-zeilig" />
            </div>
            <div style={{ alignSelf: "center", marginTop: 10, fontSize: 36, fontWeight: 700, background: GREEN, color: "#fff", borderRadius: 999, padding: "8px 26px", scale: String(appear(M.merkblatt + 0.3)), opacity: t >= M.merkblatt + 0.3 ? 1 : 0 }}>📋 Merkblatt deiner Schule ✓</div>
          </>
        )}
        {stage === "pruefung" && (
          <>
            <div style={{ fontSize: 44, fontWeight: 700 }}>🎓 Probe-Prüfung</div>
            <Bubble show={f(M.uebt + 0.3)}>
              <span style={{ fontSize: 26, color: MUTED, fontWeight: 700 }}>LEHRKRAFT</span>
              <br />Auf S. 7 schreiben Sie, die Besucherzahl hat sich vervierfacht. Woher wissen Sie das?
            </Bubble>
            <Bubble show={f(M.genau)} me>
              Amtliche Statistik: 2010 rund 0,5 Mio., 2018 2,3 Mio. …
            </Bubble>
          </>
        )}
        {stage === "pointe" && (
          <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 20, textAlign: "center" }}>
            <div style={{ fontSize: 96, fontWeight: 700, scale: String(appear(M.sechs2)) }}>6 Tage?</div>
            <div style={{ fontSize: 110, fontWeight: 700, color: GREEN, scale: String(appear(M.reichen)), opacity: t >= M.reichen ? 1 : 0 }}>Reichen dir. ✓</div>
          </div>
        )}
        {stage === "ende" && (
          <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 18, textAlign: "center" }}>
            <div style={{ fontSize: 66, fontWeight: 700, scale: String(appear(M.skill)) }}>Seminararbeit-Profi</div>
            <div style={{ fontSize: 34, color: MUTED, opacity: f(M.skill + 0.4) }}>Gliederung · Kapitel · Diagramme · Formalia · Prüfung</div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

// Profil-Handy am Schluss
const Profile: React.FC = () => {
  const { t, fps, frame } = useT();
  const s = pop(t, M.link, fps);
  const glow = 0.5 + 0.5 * Math.sin(frame / 4);
  return (
    <div style={{ position: "absolute", left: 250, top: 140, width: 580, height: 940, background: "#fff", border: `10px solid ${INK}`, borderRadius: 60, scale: String(s), opacity: t >= M.link ? 1 : 0, overflow: "hidden" }}>
      <div style={{ padding: "60px 40px", textAlign: "center" }}>
        <div style={{ width: 170, height: 170, borderRadius: 85, background: "#F5E7CF", margin: "0 auto", display: "grid", placeItems: "center", overflow: "hidden", border: `5px solid ${INK}` }}>
          <div style={{ marginTop: 40 }}><Hamster size={200} talking={false} blink={false} pointerAngle={0} /></div>
        </div>
        <div style={{ fontSize: 46, fontWeight: 700, marginTop: 20 }}>@hamsterfrei</div>
        <div style={{ fontSize: 28, color: MUTED, marginTop: 8 }}>Claude-Skills, die dir Arbeit abnehmen</div>
        <div style={{ marginTop: 34, fontSize: 34, fontWeight: 700, color: "#1A56C4", border: `5px solid rgba(35,136,90,${glow})`, borderRadius: 18, padding: "14px 10px", background: "#EEF7F1" }}>🔗 Link: Seminararbeit-Profi</div>
        <div style={{ marginTop: 50, fontSize: 54, fontWeight: 700, color: GREEN, scale: String(pop(t, M.profil, fps)) }}>☝️ Link im Profil</div>
      </div>
    </div>
  );
};

const Desk: React.FC = () => {
  const { t, frame } = useT();
  const talking = WORDS.some((w) => t >= w.start && t <= w.end) && frame % 6 < 3;
  const typing = t > M.laedst && t < M.skill ? Math.sin(frame * 1.3) * 4 : 0;
  const showProfile = t >= M.link;
  return (
    <AbsoluteFill style={{ background: CREAM }}>
      {!showProfile && (
        <>
          {/* Monitor */}
          <div style={{ position: "absolute", left: 50, top: 120, width: 980, height: 820, background: INK, borderRadius: 34, padding: 22 }}>
            <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: 16, overflow: "hidden" }}>
              <Screen />
            </div>
          </div>
          <div style={{ position: "absolute", left: 470, top: 940, width: 140, height: 90, background: "#5A3F2C" }} />
          <div style={{ position: "absolute", left: 360, top: 1020, width: 360, height: 26, borderRadius: 13, background: "#5A3F2C" }} />
        </>
      )}
      {showProfile && <Profile />}
      {/* Tisch */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1560, bottom: 0, background: FLOOR, borderTop: "6px solid #EAD6B4" }} />
      {/* Hamster */}
      <div style={{ position: "absolute", left: 300, top: 1190, translate: `0px ${typing}px` }}>
        <Hamster size={500} talking={talking} blink={frame % 105 < 4} pointerAngle={showProfile ? -30 + Math.sin(frame / 5) * 6 : -6} />
      </div>
      {/* Tastatur */}
      {!showProfile && (
        <div style={{ position: "absolute", left: 250, top: 1600, width: 580, height: 90, background: "#fff", border: `6px solid ${INK}`, borderRadius: 18, display: "grid", gridTemplateColumns: "repeat(12,1fr)", gap: 6, padding: 10 }}>
          {Array.from({ length: 24 }).map((_, i) => (
            <div key={i} style={{ background: (Math.floor(frame / 3) + i * 7) % 11 === 0 && t > M.laedst && t < M.skill ? "#9DB8E0" : "#EFE4D2", borderRadius: 5 }} />
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};

// ---------- Untertitel ----------
type Chunk = { words: Word[]; start: number; end: number };
const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  let cur: Word[] = [];
  WORDS.forEach((w) => {
    cur.push(w);
    if (cur.length >= 3 || /[.,?!:]$/.test(w.text)) {
      out.push({ words: cur, start: cur[0].start, end: w.end });
      cur = [];
    }
  });
  if (cur.length) out.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end });
  return out.map((c, i) => ({ ...c, end: i < out.length - 1 ? out[i + 1].start : c.end + 1.5 }));
})();

const cap = (s: string) =>
  s
    .replace(/[„“]/g, "")
    .replace(/^Sechs$/i, "6")
    .replace(/^null$/, "0");

const Captions: React.FC<{ top: number }> = ({ top }) => {
  const { t } = useT();
  const c = CHUNKS.find((x) => t >= x.start && t < x.end);
  if (!c) return null;
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "4px 20px" }}>
      {c.words.map((w, i) => {
        const active = t >= w.start && t < w.end + 0.08;
        const label = cap(w.text);
        return (
          <span key={i} style={{ fontSize: 72, fontWeight: 700, color: active ? GREEN : INK, WebkitTextStroke: "0px", textShadow: "0 4px 0 #fff, 0 -4px 0 #fff, 4px 0 0 #fff, -4px 0 0 #fff" }}>
            {label}
          </span>
        );
      })}
    </div>
  );
};

export const Seminar05: React.FC = () => {
  const { fps } = useVideoConfig();
  const { t } = useT();
  const desk = t >= M.stell;
  const cuts = [M.keine, M.stell, M.aber, M.schreibt, M.diagramm, M.deckblatt, M.uebt, M.sechs2, M.link];
  return (
    <AbsoluteFill style={{ fontFamily, color: INK, background: CREAM }}>
      <Audio src={staticFile("folgen/seminar05.mp3")} />
      <Audio
        src={staticFile("music/bett01.mp3")}
        loop
        volume={(f) => 0.08 * interpolate(f, [0, 15, SEMINAR05_SECONDS * fps - 30, SEMINAR05_SECONDS * fps], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      />
      {cuts.map((c) => (
        <Sequence key={c} from={Math.max(0, Math.round(c * fps) - 3)} durationInFrames={12} layout="none">
          <Audio src={staticFile("sfx/whoosh.wav")} volume={0.5} />
        </Sequence>
      ))}
      <Sequence from={Math.round(M.profil * fps)} durationInFrames={10} layout="none">
        <Audio src={staticFile("sfx/ding.wav")} volume={0.7} />
      </Sequence>
      {desk ? <Desk /> : <Panic />}
      {!(t >= M.keine && t < M.stell) && <Captions top={desk ? 1060 : 1170} />}
      <div style={{ position: "absolute", left: 40, top: 40, fontSize: 30, fontWeight: 500, color: MUTED, background: "#FFFFFF", border: `3px solid ${MUTED}`, borderRadius: 14, padding: "4px 16px" }}>Werbung</div>
    </AbsoluteFill>
  );
};
