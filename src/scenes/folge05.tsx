import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge05 · „Wie wird aus deinem Heft-Chaos ein Lernzettel?“ · Hook-Test Variante B (Paar 2) · ohne Werbung · Leinwand 948×1004
// Beispiel-Notizen erfunden, Fehler absichtlich eingebaut (docs/plaene/beispiel/lernzettel_notizen_beispiel.txt).
// Claude-Antwort echt (docs/plaene/beispiel/lernzettel_claude_antwort.md/.pdf). Zeiten in Props = Sekunden ab Szenenstart.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster. Zeigestab-Spitze ~ (440, 930).
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const MARK = "#FFE08A";
const GRID = "#DCE6F2";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const S = (v: number) => String(Math.max(0.0001, v));

const ClaudeHead: React.FC<{ right?: React.ReactNode; size?: number }> = ({ right, size = 36 }) => (
  <div style={{ height: size * 2.2, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 26px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);

const BeispielStempel: React.FC<{ size?: number; rot?: number; text?: string }> = ({ size = 34, rot = -8, text = "BEISPIEL" }) => (
  <div style={{ display: "inline-block", border: `5px solid ${RED}`, color: RED, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.85)" }}>{text}</div>
);

// Heftzettel (kariert, Handschrift-Optik). bad = Zeile mit dem eingebauten Fehler
const NOTIZEN = [
  "Zellatmung – Bio",
  "Glucose + O2 → CO2 + H2O + ATP",
  "4 Schritte??",
  "Glykolyse: im Mitochondrium",
  "Citratzyklus: Matrix, 2×",
  "Atmungskette: innere Membran",
  "gesamt 36-38 ATP ??",
  "ohne O2: Gärung, nur 2 ATP",
  "Test Do!!",
];
const BAD = 3;
const Heft: React.FC<{ width: number; fontSize: number; ring?: number; mark?: number; rot?: number }> = ({ width, fontSize, ring = 0, mark = 0, rot = 0 }) => (
  <div style={{ width, background: PAPER, backgroundImage: `linear-gradient(${GRID} 2px, transparent 2px), linear-gradient(90deg, ${GRID} 2px, transparent 2px)`, backgroundSize: `${fontSize * 0.9}px ${fontSize * 0.9}px`, border: `5px solid ${INK}`, borderRadius: 10, padding: `${fontSize * 0.5}px ${fontSize * 0.6}px`, rotate: `${rot}deg`, boxShadow: "6px 8px 0 rgba(58,38,24,.12)" }}>
    {NOTIZEN.map((l, i) => (
      <div key={i} style={{ position: "relative", fontSize: i === 0 ? fontSize * 1.15 : fontSize, fontWeight: i === 0 ? 700 : 500, color: i === 0 ? NAVY : "#33415C", lineHeight: 1.45, whiteSpace: "nowrap", fontStyle: "italic" }}>
        {i === BAD && mark > 0 && <div style={{ position: "absolute", left: -6, top: "12%", height: "76%", width: `${mark * 104}%`, background: MARK, zIndex: 0, borderRadius: 4 }} />}
        <span style={{ position: "relative" }}>{l}</span>
        {i === BAD && ring > 0 && (
          <svg viewBox="0 0 200 40" preserveAspectRatio="none" style={{ position: "absolute", left: -18, top: -10, width: "112%", height: "160%", pointerEvents: "none" }}>
            <ellipse cx={100} cy={20} rx={97} ry={17} fill="none" stroke={RED} strokeWidth={2.6} strokeDasharray={420} strokeDashoffset={420 * (1 - ring)} strokeLinecap="round" />
          </svg>
        )}
      </div>
    ))}
  </div>
);

// Claudes Lernzettel-Karte (Ausschnitt der echten Antwort)
const TAB = [
  ["Glykolyse", "Cytoplasma", "2 ATP"],
  ["Ox. Decarb.", "Matrix", "2 CO₂"],
  ["Citratzyklus", "Matrix", "2 ATP"],
  ["Atmungskette", "inn. Membran", "26–28 ATP"],
];
const Karte: React.FC<{ width: number; fs: number; rows?: number; pulse?: number }> = ({ width, fs, rows = 4, pulse = 1 }) => (
  <div style={{ width, background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, overflow: "hidden", boxShadow: "0 10px 0 rgba(58,38,24,.12)" }}>
    <ClaudeHead size={fs * 0.95} right={<span style={{ fontSize: fs * 0.8, color: MUTED }}>Lernzettel</span>} />
    <div style={{ margin: `${fs * 0.4}px ${fs * 0.4}px 0`, background: MARK, border: `4px solid ${INK}`, borderRadius: 14, padding: `${fs * 0.2}px ${fs * 0.4}px`, fontSize: fs, fontWeight: 700, lineHeight: 1.15, scale: S(pulse) }}>
      ⚠️ Korrektur:<br />Glykolyse → <span style={{ color: GREEN }}>Cytoplasma</span>
    </div>
    <div style={{ padding: `${fs * 0.35}px ${fs * 0.4}px ${fs * 0.5}px` }}>
      {TAB.map((r, i) => (
        <div key={i} style={{ display: "grid", gridTemplateColumns: "1.15fr 1.15fr 0.9fr", gap: 8, fontSize: fs * 0.66, whiteSpace: "nowrap", fontWeight: 600, lineHeight: 1.5, borderBottom: i < 3 ? `2px solid #E7D9C2` : "none", opacity: i < rows ? 1 : 0.1 }}>
          <span>{r[0]}</span>
          <span style={{ color: i === 0 ? GREEN : NAVY }}>{r[1]}</span>
          <span style={{ color: MUTED }}>{r[2]}</span>
        </div>
      ))}
    </div>
  </div>
);

// ---------- 1 Hook: Ergebnis ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { frame } = useT();
  const pulse = 1 + Math.max(0, Math.sin(frame / 5)) * 0.04;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 20, textAlign: "center", fontSize: 62, fontWeight: 700, lineHeight: 1.08, color: NAVY }}>
        Lernzettel mit KI:<br /><span style={{ color: GREEN }}>Fehler gefunden</span>
      </div>
      <div style={{ position: "absolute", left: 18, top: 205 }}>
        <div style={{ position: "absolute", left: 6, top: -40, zIndex: 2 }}>
          <BeispielStempel size={26} text="BEISPIEL-NOTIZEN" />
        </div>
        <Heft width={520} fontSize={32} ring={1} rot={-3} />
      </div>
      {/* rotes X an der Fehlerzeile */}
      <div style={{ position: "absolute", left: 540, top: 300, fontSize: 100, fontWeight: 700, color: RED, rotate: "-8deg" }}>✗</div>
      {/* Claude-Karte unten rechts, Zeigestab-Spitze (~440, 930) zeigt auf ihre Unterkante */}
      <div style={{ position: "absolute", right: 16, top: 440, rotate: "2deg" }}>
        <Karte width={520} fs={42} pulse={pulse} />
      </div>
    </div>
  );
};

// ---------- 2 Heftzettel groß, Fehler eingebaut ----------
export const SceneNotizen: React.FC<{ fehler: number }> = ({ fehler }) => {
  const { t, fps } = useT();
  const mark = interpolate(t, [fehler, fehler + 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 52, fontWeight: 700 }}>Meine Bio-Notizen</div>
      <div style={{ position: "absolute", right: 40, top: 26 }}>
        <BeispielStempel size={40} rot={6} />
      </div>
      <div style={{ position: "absolute", left: 70, top: 130, scale: S(sp(t, 0.05, fps)), transformOrigin: "top left" }}>
        <Heft width={800} fontSize={44} mark={mark} rot={-1.5} />
      </div>
      <Pop at={fehler + 0.4} style={{ position: "absolute", left: 420, top: 820 }}>
        <div style={{ background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: 22, padding: "8px 26px", fontSize: 50, fontWeight: 700, color: RED, rotate: "-3deg" }}>absichtlich falsch 🤫</div>
      </Pop>
    </div>
  );
};

// ---------- 3 Zelle: Glykolyse springt ins Cytoplasma ----------
export const SceneZelle: React.FC<{ falsch: number }> = ({ falsch }) => {
  const { t, fps } = useT();
  const k = sp(t, falsch, fps);
  // Etikett wandert vom Mitochondrium (rechts) ins Cytoplasma (links)
  const x = interpolate(k, [0, 1], [520, 150]);
  const y = interpolate(k, [0, 1], [430, 640]);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 52, fontWeight: 700 }}>Wo läuft die Glykolyse?</div>
      <svg viewBox="0 0 948 1004" style={{ position: "absolute", inset: 0 }}>
        <ellipse cx={474} cy={560} rx={420} ry={330} fill="#FCEFD9" stroke={INK} strokeWidth={8} />
        <g transform="rotate(-18 600 470)">
          <ellipse cx={600} cy={470} rx={190} ry={95} fill="#F6C9A8" stroke={INK} strokeWidth={7} />
          <path d="M440 470 q30 -60 60 0 q30 60 60 0 q30 -60 60 0 q30 60 60 0 q30 -60 60 0" fill="none" stroke={INK} strokeWidth={5} />
        </g>
        <circle cx={260} cy={420} r={70} fill="#D9D3F0" stroke={INK} strokeWidth={6} />
      </svg>
      <div style={{ position: "absolute", left: 470, top: 560, fontSize: 36, fontWeight: 700, color: MUTED }}>Mitochondrium</div>
      <div style={{ position: "absolute", left: 180, top: 720, fontSize: 46, fontWeight: 700, color: "#1C7049", opacity: fade(t, falsch + 0.1, 0.15) }}>im Cytoplasma ✓</div>
      <div style={{ position: "absolute", left: x, top: y, background: k > 0.5 ? "#DDF1E6" : "#FDE3DF", border: `6px solid ${k > 0.5 ? GREEN : RED}`, borderRadius: 20, padding: "6px 22px", fontSize: 52, fontWeight: 700, color: k > 0.5 ? "#1C7049" : RED, whiteSpace: "nowrap" }}>
        Glykolyse {k > 0.5 ? "✓" : "✗"}
      </div>
      <Pop at={falsch} style={{ position: "absolute", right: 30, top: 20 }}>
        <div style={{ border: `8px solid ${RED}`, color: RED, borderRadius: 18, padding: "0 26px", fontSize: 62, fontWeight: 700, rotate: "6deg", background: "rgba(255,255,255,.85)" }}>FALSCH</div>
      </Pop>
    </div>
  );
};

// ---------- 4 Chat: Claudes Korrektur ganz oben (wörtlich) ----------
export const SceneChat: React.FC<{ oben: number }> = ({ oben }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 300, right: 36, top: 120, background: "#F1E6D3", borderRadius: "30px 30px 6px 30px", padding: "18px 24px", fontSize: 36, fontWeight: 600, lineHeight: 1.2, opacity: fade(t, 0) }}>
        Mach mir daraus einen Lernzettel, der auf <b>eine Seite</b> passt …
      </div>
      <div style={{ position: "absolute", left: 36, right: 36, top: 330, background: PAPER, border: `5px solid ${INK}`, borderRadius: "30px 30px 30px 6px", padding: "22px 28px", scale: S(sp(t, 0.35, fps)), transformOrigin: "top left" }}>
        <div style={{ fontSize: 50, fontWeight: 700, marginBottom: 12 }}>⚠️ Vorab: zwei Korrekturen</div>
        <div style={{ position: "relative", fontSize: 46, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ position: "absolute", left: -8, right: -8, top: 0, bottom: 0, background: MARK, borderRadius: 8, opacity: fade(t, oben, 0.4) }} />
          <span style={{ position: "relative" }}>1. Die Glykolyse läuft im <b>Cytoplasma</b> ab, nicht im Mitochondrium.</span>
        </div>
      </div>
      <Pop at={oben + 0.2} style={{ position: "absolute", right: 50, top: 760 }}>
        <div style={{ background: "#DDF1E6", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "8px 26px", fontSize: 54, fontWeight: 700, color: "#1C7049" }}>Fehler gefunden ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 5 Tabelle + 5 Fragen ----------
const FRAGEN = ["4 Schritte + Ort?", "ATP & CO₂ pro Schritt?", "Wie entsteht ATP?", "Warum nur 2 ATP?", "Woher die 6 CO₂?"];
export const SceneTabelle: React.FC<{ fragen: number }> = ({ fragen }) => {
  const { t, fps } = useT();
  const rows = Math.min(4, Math.floor(interpolate(t, [0.05, 1.0], [1, 4.99], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 30, top: 24, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <Karte width={600} fs={42} rows={rows} />
      </div>
      {FRAGEN.map((f, i) => {
        const a = fragen + i * 0.18;
        return (
          <div key={i} style={{ position: "absolute", left: 250 + i * 14, top: 480 + i * 82, width: 620, background: i % 2 ? "#E4ECF7" : PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: "8px 18px", fontSize: 38, fontWeight: 700, whiteSpace: "nowrap", rotate: `${(i - 2) * 1.5}deg`, opacity: fade(t, a, 0.15), translate: `${(1 - sp(t, a, fps)) * 300}px 0px` }}>
            <span style={{ color: GREEN }}>Frage {i + 1}:</span> {f}
          </div>
        );
      })}
    </div>
  );
};

// ---------- 6 Eine Seite gewünscht – zwei gedruckt ----------
export const SceneSeiten: React.FC<{ eine: number; zwei: number }> = ({ eine, zwei }) => {
  const { t, fps } = useT();
  const Blatt: React.FC<{ n: number; at: number }> = ({ n, at }) => (
    <div style={{ position: "relative", width: 360, height: 500, background: PAPER, border: `6px solid ${INK}`, borderRadius: 10, padding: 24, scale: S(sp(t, at, fps)), boxShadow: "6px 8px 0 rgba(58,38,24,.12)" }}>
      {Array.from({ length: n === 1 ? 13 : 7 }).map((_, i) => (
        <div key={i} style={{ height: 14, margin: "14px 0", width: `${60 + ((i * 37) % 40)}%`, background: i === 0 && n === 1 ? NAVY : "#CFC6B8", borderRadius: 7 }} />
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 14, textAlign: "center", fontSize: 34, fontWeight: 700, color: MUTED }}>Seite {n}</div>
    </div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <Pop at={eine} style={{ position: "absolute", left: 40, top: 30 }}>
        <div style={{ fontSize: 58, fontWeight: 700 }}>gewünscht: <span style={{ color: GREEN }}>1 Seite</span></div>
      </Pop>
      <div style={{ position: "absolute", left: 60, top: 150, display: "flex", gap: 50 }}>
        <div style={{ position: "relative" }}><Blatt n={1} at={0.1} /></div>
        <div style={{ position: "relative" }}><Blatt n={2} at={zwei - 0.4} /></div>
      </div>
      <Pop at={zwei} style={{ position: "absolute", left: 420, top: 690 }}>
        <div style={{ border: `8px solid ${RED}`, color: RED, borderRadius: 18, padding: "0 26px", fontSize: 76, fontWeight: 700, rotate: "-5deg", background: "rgba(255,255,255,.9)" }}>2 Seiten ✗</div>
      </Pop>
      <div style={{ position: "absolute", right: 40, top: 880, fontSize: 30, fontWeight: 600, color: MUTED, opacity: fade(t, zwei + 0.3) }}>A4, Schrift 11</div>
    </div>
  );
};

// ---------- 7 Urteil: GEKLAPPT ----------
export const SceneUrteil: React.FC<{ stempel: number; fehler: number; lang: number }> = ({ stempel, fehler, lang }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: "#1C7049", borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 30, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 62, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, fehler) }}>Fehler gefunden <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, fehler + 0.3) }}>Tabelle + 5 Fragen <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, lang) }}>1 Seite <span style={{ color: RED }}>✗</span> <span style={{ fontSize: 50, color: MUTED }}>(2)</span></div>
      </div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar LERNEN ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📋</div>
          <div style={{ fontSize: 54, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Meine Frage<br />zum<br />Kopieren</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 330, top: 840 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 88, fontWeight: 600, color: INK, letterSpacing: 4 }}>LERNEN</div>
        </div>
      </Pop>
    </div>
  );
};
