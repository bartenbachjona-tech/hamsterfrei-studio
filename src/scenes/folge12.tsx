import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";
import { Hamster } from "../Hamster";

// Folge12 · Hamster-Test „Klausurwoche: drei Klausuren + Minijob“ · Einstiegs-Test E2 (Paar 1) · ohne Werbung · Leinwand 948×1004
// Woche + Person (Lea) vom Studio erfunden (docs/plaene/beispiel/klausur_woche_beispiel.txt).
// Plan = Claudes echte Antwort (docs/plaene/beispiel/klausur_claude_antwort.md). Bio-Abendportionen und Di-Bio haben in der Antwort keine Uhrzeit → nur schematisch platziert, als „20 Min.“ beschriftet.
// Zeiten in Props = Sekunden ab Szenenstart. Unten links auf der Leinwand (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LRED = "#F9DEDA";
const GREY = "#B9AFA3";
const PINK = "#F6C9D4";
const BLUE = "#6C93C9";
const YEL = "#F5C542";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const S = (v: number) => String(Math.max(0.0001, v));
const lin = (t: number, a: number, d: number) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const Stempel: React.FC<{ size?: number; rot?: number; text?: string; color?: string }> = ({ size = 34, rot = -8, text = "BEISPIEL", color = RED }) => (
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.88)", whiteSpace: "nowrap" }}>{text}</div>
);

// ---------- Wochenplan (Claudes Plan, Sa–Do) ----------
type Kind = "schicht" | "oma" | "mathe" | "bio" | "engl";
type Block = { a: number; b: number; k: Kind; label: string; open?: boolean; short?: string };
const COL: Record<Kind, [string, string]> = {
  schicht: [GREY, "#5E554C"],
  oma: [PINK, "#9C3B57"],
  mathe: [GREEN, "#FFFFFF"],
  bio: [BLUE, "#FFFFFF"],
  engl: [YEL, "#5A4300"],
};
const TAGE: { d: string; klausur?: string; blocks: Block[] }[] = [
  { d: "SA", blocks: [{ a: 6, b: 12, k: "schicht", label: "Schicht" }, { a: 14, b: 17, k: "mathe", label: "Mathe" }, { a: 19.6, b: 20.6, k: "bio", label: "🧬" }] },
  { d: "SO", blocks: [{ a: 9, b: 11.5, k: "mathe", label: "📐" }, { a: 12, b: 18, k: "oma", label: "Oma 80 🎂" }, { a: 19.6, b: 20.6, k: "bio", label: "🧬" }] },
  { d: "MO", blocks: [{ a: 14, b: 14.75, k: "mathe", label: "" }, { a: 15, b: 19, k: "schicht", label: "Schicht" }, { a: 19.5, b: 21, k: "mathe", label: "📐" }] },
  { d: "DI", klausur: "Mathe", blocks: [{ a: 15, b: 18.5, k: "engl", label: "Englisch", open: true }, { a: 19.6, b: 20.6, k: "bio", label: "🧬" }] },
  { d: "MI", klausur: "Engl.", blocks: [{ a: 13.5, b: 14.75, k: "bio", label: "🧬" }, { a: 15, b: 19, k: "schicht", label: "Schicht" }, { a: 19.5, b: 21, k: "bio", label: "🧬" }] },
  { d: "DO", klausur: "Bio", blocks: [{ a: 6.8, b: 7.8, k: "bio", label: "🧬" }] },
];

// grow(k, dayIndex) → 0..1 wie weit ein Block gezeichnet ist; hl → Zeile hervorheben
export const WeekPlan: React.FC<{ w: number; h: number; grow?: (k: Kind, day: number) => number; hl?: number; dim?: Kind[]; head?: boolean; headText?: React.ReactNode; pulse?: Kind | "klausur" | null; pv?: number }> = ({ w, h, grow = () => 1, hl = -1, dim = [], head = true, headText, pulse = null, pv = 0 }) => {
  const headH = head ? h * 0.1 : 0;
  const scaleH = h * 0.06;
  const rowsH = h - headH - scaleH;
  const rowH = rowsH / TAGE.length;
  const labW = w * 0.2;
  const X0 = labW + 6;
  const W = w - X0 - 14;
  const x = (hr: number) => X0 + ((hr - 6) / 15.5) * W;
  const fs = rowH * 0.27;
  return (
    <div style={{ position: "relative", width: w, height: h, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", boxShadow: "6px 8px 0 rgba(58,38,24,.14)" }}>
      {head && <div style={{ height: headH, background: NAVY, color: "#fff", fontSize: headH * 0.5, fontWeight: 700, display: "flex", alignItems: "center", paddingLeft: 24, letterSpacing: 1, whiteSpace: "pre" }}><span>{headText ?? "LEAS KLAUSURWOCHE"}</span></div>}
      <div style={{ position: "absolute", left: 0, top: headH, width: w, height: scaleH, borderBottom: "3px solid #E7D9C2" }}>
        {[6, 9, 12, 15, 18, 21].map((hr) => (
          <div key={hr} style={{ position: "absolute", left: x(hr) - 40, width: 80, textAlign: "center", top: scaleH * 0.12, fontSize: scaleH * 0.55, fontWeight: 600, color: MUTED }}>{hr}</div>
        ))}
      </div>
      {TAGE.map((tg, i) => {
        const top = headH + scaleH + i * rowH;
        return (
          <div key={tg.d} style={{ position: "absolute", left: 0, top, width: w, height: rowH, borderBottom: i < TAGE.length - 1 ? "3px solid #EFE4D2" : "none", background: hl === i ? "rgba(249,222,218,.8)" : "transparent" }}>
            <div style={{ position: "absolute", left: 14, top: rowH * 0.1, fontSize: rowH * 0.36, fontWeight: 700, color: INK }}>{tg.d}</div>
            {tg.klausur && (
              <div style={{ position: "absolute", left: 10, top: rowH * 0.56, fontSize: rowH * 0.2, fontWeight: 700, color: "#fff", background: RED, borderRadius: 8, padding: "1px 6px", whiteSpace: "nowrap", scale: S(pulse === "klausur" ? 1 + 0.35 * pv : 1), transformOrigin: "left center", outline: pulse === "klausur" ? `${3 + 4 * pv}px solid ${YEL}` : "none" }}>📝 {tg.klausur}</div>
            )}
            {tg.blocks.map((b, j) => {
              const g = grow(b.k, i);
              const bw = (x(b.b) - x(b.a)) * g;
              const [bg, fg] = COL[b.k];
              return (
                <div key={j} style={{ position: "absolute", left: x(b.a), top: rowH * 0.16, height: rowH * 0.68, width: Math.max(0, bw), background: b.open ? `linear-gradient(90deg, ${bg} 60%, rgba(245,197,66,0))` : bg, borderRadius: 12, overflow: "hidden", opacity: dim.includes(b.k) ? 0.3 : g > 0 ? 1 : 0, border: pulse === b.k ? `${4 + 5 * pv}px solid ${RED}` : b.k === "mathe" ? `3px solid ${DGREEN}` : "none", boxSizing: "border-box" }}>
                  <div style={{ padding: `${rowH * 0.12}px 10px`, fontSize: fs, fontWeight: 700, color: fg, whiteSpace: "nowrap" }}>{b.label}</div>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

const mathTotal = (sa: number, so: number, mo: number) => 3 * sa + 2.5 * so + 2.25 * mo; // Sa 3 h, So 2,5 h, Mo 0,75 + 1,5 h
const fmtH = (v: number) => (v >= 7.74 ? "7¾" : v.toFixed(1).replace(".", ",").replace(",0", ""));

// ---------- 0 E2-Vollbild (0–1,0 s): Ergebnis bildfüllend, Mathe-Blöcke wachsen, Zähler springt ----------
export const E2Hook: React.FC = () => {
  const { t, frame } = useT();
  const so = lin(t, 0.05, 0.22);
  const mo = lin(t, 0.22, 0.25);
  const grow = (k: Kind, d: number) => (k !== "mathe" ? 1 : d === 0 ? 1 : d === 1 ? so : d === 2 ? mo : 1);
  const total = mathTotal(1, so, mo);
  const bump = 1 + 0.12 * Math.max(0, 1 - Math.abs(t - 0.48) / 0.15);
  const pv = (Math.sin(frame / 2.5) + 1) / 2;
  return (
    <AbsoluteFill style={{ background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 196, textAlign: "center", fontSize: 32, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST · Lernplan Klausuren</div>
      <div style={{ position: "absolute", left: 15, top: 248 }}>
        <WeekPlan w={1050} h={1200} grow={grow} pulse={t < 0.8 ? "klausur" : "schicht"} pv={pv} headText={<>{"3 Klausuren + Job: "}<span style={{ color: "#8FE0B5" }}>Claudes Plan</span></>} />
      </div>
      <div style={{ position: "absolute", left: 262, top: 1468, scale: S(bump), transformOrigin: "left center", background: DGREEN, color: "#fff", borderRadius: 22, padding: "8px 26px", fontSize: 60, fontWeight: 700, boxShadow: "4px 6px 0 rgba(58,38,24,.2)", whiteSpace: "nowrap" }}>
        Mathe: {fmtH(total)} h
      </div>
      <div style={{ position: "absolute", left: 270, top: 1580 }}><Stempel size={26} text="BEISPIEL · Lea ist erfunden" rot={-2} /></div>
      <div style={{ position: "absolute", left: -20, top: 1440 }}>
        <Hamster size={300} talking={frame % 6 < 3} blink={false} pointerAngle={-6 + Math.sin(frame / 3) * 5} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- 1 Hook auf der Leinwand (ab 1,0 s): Plan + „Ein Fach kommt zu kurz“ ----------
export const SceneHook: React.FC<{ kurz: number }> = ({ kurz }) => {
  const { t, frame } = useT();
  const pulse = (Math.sin(frame / 4) + 1) / 2;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 10, textAlign: "center" }}>
        <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST · Lernplan Klausuren</div>
        <div style={{ fontSize: 56, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>3 Klausuren + Job: <span style={{ color: GREEN }}>Claudes Plan</span></div>
      </div>
      <div style={{ position: "absolute", left: 20, top: 120 }}>
        <WeekPlan w={900} h={760} hl={t >= kurz ? 3 : -1} pulse={t < 1.45 ? "schicht" : t >= 1.55 && t < 2.7 ? "oma" : t >= 3.25 && t < kurz ? "mathe" : null} pv={(Math.sin(frame / 2.5) + 1) / 2} />
      </div>
      {t < kurz && <div style={{ position: "absolute", left: 600, top: 900, background: DGREEN, color: "#fff", borderRadius: 18, padding: "6px 20px", fontSize: 44, fontWeight: 700 }}>Mathe: 7¾ h</div>}
      {t >= kurz && (
        <Pop at={kurz} style={{ position: "absolute", left: 470, top: 895 }}>
          <div style={{ fontSize: 46, fontWeight: 700, color: RED, background: LRED, border: `5px solid ${RED}`, borderRadius: 16, padding: "4px 16px", scale: S(1 + 0.05 * pulse), whiteSpace: "nowrap" }}>Ein Fach zu kurz?</div>
        </Pop>
      )}
    </div>
  );
};

// ---------- 2 Die Eingabe (echt, gekürzt) + drei Klausuren ----------
export const SceneEingabe: React.FC<{ di: number; mi: number; doo: number }> = ({ di, mi, doo }) => {
  const { t, fps } = useT();
  const k: [string, string, number][] = [["Di", "Mathe 😬", di], ["Mi", "Englisch", mi], ["Do", "Bio", doo]];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 50, top: 40 }}><Stempel size={28} text="BEISPIEL · Lea, 17, ist erfunden" rot={-1} /></div>
      <div style={{ position: "absolute", left: 90, right: 30, top: 120, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "16px 26px", fontSize: 40, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 6 }}>An Claude:</div>
          „Ich hab nächste Woche <b>drei Klausuren</b> und arbeite nebenbei. Kannst du mir einen <b>Lernplan von Samstag bis Donnerstag</b> machen? …“
          <div style={{ fontSize: 40, color: NAVY, marginTop: 10, fontWeight: 700 }}>+ Schichten Sa/Mo/Mi · Omas 80. am So</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 60, right: 40, top: 560, display: "flex", gap: 22 }}>
        {k.map(([d, f, at]) => (
          <div key={d} style={{ flex: 1, scale: S(sp(t, at, fps)), background: PAPER, border: `5px solid ${RED}`, borderRadius: 20, padding: "14px 10px", textAlign: "center" }}>
            <div style={{ fontSize: 40, fontWeight: 700, color: RED }}>📝 {d}</div>
            <div style={{ fontSize: 44, fontWeight: 700 }}>{f}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ---------- 3 Mathe nach vorn: Stunden-Balken ----------
export const SceneMathe: React.FC<{ fast: number; zitat: number }> = ({ fast, zitat }) => {
  const { t } = useT();
  const g = lin(t, fast - 0.4, 0.8);
  const bars: [string, number, string, string][] = [
    ["Mathe", 7.75, GREEN, `${fmtH(7.75 * g)} h`],
    ["Bio", 3.75, BLUE, "≈ 3¾ h"],
    ["Englisch", 0, YEL, "?"],
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 52, fontWeight: 700, color: NAVY }}>Mathe zuerst: Sa, So, Mo</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, display: "flex", flexDirection: "column", gap: 34 }}>
        {bars.map(([n, v, c, lab], i) => {
          const gg = i === 0 ? g : fade(t, 0.3 + i * 0.3);
          return (
            <div key={n} style={{ display: "flex", alignItems: "center", gap: 18, opacity: i === 0 ? 1 : gg }}>
              <div style={{ width: 230, fontSize: 48, fontWeight: 700 }}>{n}</div>
              <div style={{ height: 96, width: Math.max(14, (v / 7.75) * 480 * gg), background: c, borderRadius: 16, border: `4px solid ${INK}` }} />
              <div style={{ fontSize: 50, fontWeight: 700, color: i === 0 ? DGREEN : MUTED }}>{lab}</div>
            </div>
          );
        })}
      </div>
      <Pop at={zitat} style={{ position: "absolute", left: 40, right: 40, top: 560 }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, overflow: "hidden" }}>
          <div style={{ height: 58, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: 30, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
            <div style={{ width: 20, height: 20, borderRadius: 20, background: "#E5835E" }} />Claude
          </div>
          <div style={{ padding: "14px 24px 20px", fontSize: 42, fontWeight: 600, lineHeight: 1.3 }}>
            „Mathe kommt zuerst und bekommt die meiste Zeit, <b style={{ color: DGREEN }}>weil du da am schwächsten bist</b>.“
          </div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 4 Schichten + Oma bleiben frei ----------
export const SceneFrei: React.FC<{ frei: number; oma: number }> = ({ frei, oma }) => {
  const { t, fps } = useT();
  const item = (txt: string, bg: string, at: number) => (
    <div style={{ display: "flex", alignItems: "center", gap: 18, background: bg, border: `5px solid ${INK}`, borderRadius: 20, padding: "14px 24px", fontSize: 50, fontWeight: 700, scale: S(0.9 + 0.1 * sp(t, at, fps)) }}>
      <span style={{ flex: 1 }}>{txt}</span>
      <span style={{ opacity: fade(t, at), color: DGREEN, background: PAPER, borderRadius: 12, padding: "0 14px", border: `4px solid ${GREEN}` }}>frei ✓</span>
    </div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 54, fontWeight: 700, color: NAVY }}>Und die Schichten?</div>
      <div style={{ position: "absolute", left: 50, right: 50, top: 130, display: "flex", flexDirection: "column", gap: 22 }}>
        {item("🥐 Sa 6–12 Schicht", "#E6E1DA", frei)}
        {item("🥐 Mo 15–19 Schicht", "#E6E1DA", frei + 0.15)}
        {item("🥐 Mi 15–19 Schicht", "#E6E1DA", frei + 0.3)}
        {item("🎂 So 12–18 Oma wird 80", PINK, oma)}
      </div>
      <div style={{ position: "absolute", left: 400, top: 740, fontSize: 40, fontWeight: 600, color: MUTED, opacity: fade(t, oma + 0.4) }}>kein Lernen drin</div>
    </div>
  );
};

// ---------- 5 Bio in kleinen Portionen ----------
export const SceneBio: React.FC<{ sa: number }> = ({ sa }) => {
  const { t, fps } = useT();
  const cards: [string, string, string][] = [
    ["Sa", "20 Min.", "Karten anlegen"],
    ["So", "20 Min.", "Karten"],
    ["Di", "20 Min.", "Karten"],
    ["Mi", "13:30–14:45", "+ 19:30–21"],
    ["Do", "kurz", "überfliegen"],
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 52, fontWeight: 700, color: BLUE }}>Bio: schon ab Samstag 🧬</div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 130, display: "flex", flexWrap: "wrap", gap: 26 }}>
        {cards.map(([d, z, x], i) => {
          const a = sp(t, sa + i * 0.14, fps);
          const big = i === 3;
          return (
            <div key={d} style={{ width: big ? 560 : 272, scale: S(a), background: PAPER, border: `6px solid ${BLUE}`, borderRadius: 20, padding: "16px 20px", rotate: `${(i % 2 ? 1.5 : -1.5)}deg` }}>
              <div style={{ fontSize: 58, fontWeight: 700, color: BLUE }}>{d}</div>
              <div style={{ fontSize: 54, fontWeight: 700 }}>{z}</div>
              <div style={{ fontSize: 38, color: INK, fontWeight: 600 }}>{x}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------- 6 Der Haken: Englisch nur ein Nachmittag ----------
export const SceneEnglisch: React.FC<{ nur: number; nach: number }> = ({ nur, nach }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 54, fontWeight: 700, color: RED }}>Aber Englisch?</div>
      <div style={{ position: "absolute", left: 30, top: 110, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <WeekPlan w={888} h={520} head={false} hl={3} dim={["mathe", "bio", "schicht", "oma"]} />
      </div>
      <Pop at={nur} style={{ position: "absolute", left: 120, top: 660 }}>
        <Stempel size={64} rot={-4} text="NUR 1 NACHMITTAG" />
      </Pop>
      <div style={{ position: "absolute", left: 300, right: 30, top: 790, fontSize: 42, fontWeight: 700, color: INK, opacity: fade(t, nach), lineHeight: 1.2 }}>
        Di: erst <span style={{ color: RED }}>📝 Mathe-Klausur</span>,<br />danach Englisch lernen.
      </div>
    </div>
  );
};

// ---------- 7 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  const z: [string, boolean][] = [["Mathe zuerst", true], ["Schichten frei", true], ["Bio verteilt", true], ["Englisch zu kurz", false]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 330, right: 20, top: 400, display: "flex", flexDirection: "column", gap: 16, fontSize: 50, fontWeight: 700 }}>
        {z.map(([txt, ok], i) => (
          <div key={txt} style={{ opacity: fade(t, zeilen + i * 0.22) }}>{txt} <span style={{ color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span></div>
        ))}
      </div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar KLAUSUR ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📚</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Lernplan-<br />Frage zum<br />Kopieren</div>
          {[0, 1, 2, 3].map((i) => {
            const tt = (frame - i * 9) / fps;
            const y = interpolate(tt % 1.6, [0, 1.6], [0, -120]);
            const o = interpolate(tt % 1.6, [0, 0.2, 1.3, 1.6], [0, 1, 1, 0]);
            return (
              <svg key={i} width={50} height={50} viewBox="0 0 24 24" style={{ position: "absolute", right: 14 + (i % 2) * 24, bottom: 20, translate: `0px ${y}px`, opacity: tt < 0 ? 0 : o }}>
                <path d="M12 21s-7-4.5-9.5-9C.7 8.6 2.6 4 6.6 4c2.1 0 3.6 1.2 4.4 2.5C11.8 5.2 13.3 4 15.4 4c4 0 5.9 4.6 4.1 8-2.5 4.5-9.5 9-9.5 9z" fill="#E05A47" />
              </svg>
            );
          })}
        </div>
      </div>
      <Pop at={commentAt} style={{ position: "absolute", left: 250, top: 850 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>KLAUSUR</div>
        </div>
      </Pop>
    </div>
  );
};

// Cover (Standbild des E2-Hooks bei 0,5 s, ohne Untertitel)
export const Folge12Cover: React.FC = () => (
  <AbsoluteFill style={{ fontFamily: "Fredoka", color: INK }}>
    <E2Hook />
  </AbsoluteFill>
);
