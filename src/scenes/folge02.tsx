import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge02 · Hamster-Test „Was ist meine alte Switch noch wert?“ · ohne Werbung · Leinwand 948×1004
// Zeiten in den Props sind Sekunden ab Szenenstart. Konsole generisch gezeichnet (keine Marke, kein Logo).
const RED = "#C8473A";
const YEL = "#D9A32B";
const MUTED = "#6B5444";
const SAND = "#F5EAD7";
const PAPER = "#FFFFFF";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const S = (v: number) => String(Math.max(0.0001, v));

const ClaudeHead: React.FC<{ right?: React.ReactNode }> = ({ right }) => (
  <div style={{ height: 90, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 34px", fontSize: 38, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
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

// Generische Handheld-Konsole (Navy/Grün, Kanal-Farben), optional mit Kratzern
export const Konsole: React.FC<{ w?: number; kratzer?: boolean }> = ({ w = 360, kratzer = false }) => {
  const h = w * 0.45;
  const side = w * 0.17;
  return (
    <div style={{ position: "relative", width: w, height: h }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: side, height: h, background: NAVY, border: `5px solid ${INK}`, borderRadius: `${h * 0.4}px 8px 8px ${h * 0.4}px` }}>
        <div style={{ position: "absolute", left: side * 0.28, top: h * 0.22, width: side * 0.38, height: side * 0.38, borderRadius: 99, background: INK }} />
      </div>
      <div style={{ position: "absolute", left: side - 4, top: 0, width: w - 2 * side + 8, height: h, background: "#2F2A33", border: `5px solid ${INK}` }}>
        <div style={{ position: "absolute", inset: 10, background: "#BFD9E8", borderRadius: 4, overflow: "hidden" }}>
          {kratzer && (
            <svg viewBox="0 0 100 60" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
              <path d="M12 10 L40 28 M55 8 L80 22 M30 45 L62 52" stroke="#fff" strokeWidth={1.6} strokeLinecap="round" />
            </svg>
          )}
        </div>
      </div>
      <div style={{ position: "absolute", right: 0, top: 0, width: side, height: h, background: GREEN, border: `5px solid ${INK}`, borderRadius: `8px ${h * 0.4}px ${h * 0.4}px 8px` }}>
        <div style={{ position: "absolute", right: side * 0.28, top: h * 0.55, width: side * 0.38, height: side * 0.38, borderRadius: 99, background: INK }} />
      </div>
    </div>
  );
};

const Preisschild: React.FC<{ text: string; rot?: number }> = ({ text, rot = -10 }) => (
  <div style={{ display: "inline-flex", alignItems: "center", gap: 12, background: "#FFE9A8", border: `5px solid ${INK}`, borderRadius: "14px 30px 30px 14px", padding: "6px 22px 6px 14px", fontSize: 46, fontWeight: 700, rotate: `${rot}deg`, whiteSpace: "nowrap" }}>
    <div style={{ width: 16, height: 16, borderRadius: 8, background: CREAM, border: `4px solid ${INK}` }} />
    {text}
  </div>
);

// ---------- 1 Hook: Claude-Antwort, Preis ✓, Begründung ? (ab Frame 0) ----------
export const SceneHook: React.FC<{ passt: number; nicht: number }> = ({ passt, nicht }) => {
  const { t, frame, fps } = useT();
  const ring = 1;
  const okPulse = t >= passt && t < passt + 0.5 ? 1 + Math.sin((t - passt) * 12) * 0.12 : 1;
  const q = t < nicht ? 0.75 : 0.75 + 0.25 * sp(t, nicht, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 22, textAlign: "center", fontSize: 30, fontWeight: 700, color: GREEN, letterSpacing: 4 }}>🐹 HAMSTER-TEST</div>
      <div style={{ position: "absolute", left: 20, right: 20, top: 64, textAlign: "center", fontSize: 72, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>
        Switch verkaufen: Was ist sie <span style={{ color: RED }}>wert?</span>
      </div>
      {/* Claude-Antwort-Karte */}
      <div style={{ position: "absolute", left: 36, right: 36, top: 250, background: PAPER, border: `6px solid ${INK}`, borderRadius: 30, overflow: "hidden", boxShadow: "0 12px 0 rgba(58,38,24,.12)" }}>
        <ClaudeHead />
        <div style={{ padding: "18px 34px 44px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <div style={{ fontSize: 44, fontWeight: 600, color: MUTED }}>Empfehlung:</div>
            <div style={{ fontSize: 92, fontWeight: 700 }}>150 € VB</div>
            <div style={{ fontSize: 84, color: GREEN, scale: String(okPulse), marginLeft: 6 }}>✓</div>
          </div>
          <div style={{ position: "relative", marginTop: 26, display: "flex", alignItems: "center", gap: 46 }}>
            <div style={{ fontSize: 44, fontWeight: 600, lineHeight: 1.15, paddingLeft: 34, whiteSpace: "nowrap" }}>„Händler … ab etwa 115–130 €“</div>
            <div style={{ fontSize: 120, fontWeight: 700, color: RED, lineHeight: 0.9, scale: String(q), rotate: `${Math.sin(frame / 4) * 6}deg` }}>?</div>
            <svg viewBox="0 0 200 80" preserveAspectRatio="none" style={{ position: "absolute", left: -30, top: -44, width: 700, height: 150, pointerEvents: "none" }}>
              <ellipse cx={100} cy={40} rx={97} ry={37} fill="none" stroke={RED} strokeWidth={2.2} strokeDasharray={480} strokeDashoffset={480 * (1 - ring)} strokeLinecap="round" />
            </svg>
          </div>
        </div>
      </div>
      {/* Hook-Aussage als Bildtext (erscheint mit dem Satz) */}
      <div style={{ position: "absolute", left: 40, top: 690, display: "flex", gap: 18, fontSize: 50, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, passt - 0.1), background: "#E3F1EA", border: `5px solid ${GREEN}`, color: "#1C7049", borderRadius: 18, padding: "4px 20px" }}>Preis ✓</div>
        <div style={{ opacity: fade(t, nicht - 0.1), background: "#FDE3DF", border: `5px solid ${RED}`, color: RED, borderRadius: 18, padding: "4px 20px" }}>Begründung ✗</div>
      </div>
      {/* Konsole mit Preisschild, rechts unten (Hamster steht links) */}
      <div style={{ position: "absolute", right: 60, top: 812 }}>
        <Konsole w={380} kratzer />
        <div style={{ position: "absolute", left: -175, top: 10 }}>
          <Preisschild text="150 € VB" />
        </div>
      </div>
    </div>
  );
};

// ---------- 2 Meine Frage (Chat) ----------
export const SceneFrage: React.FC = () => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", right: 40, left: 90, top: 150, background: "#F1E6D3", borderRadius: 34, padding: "26px 36px", fontSize: 54, fontWeight: 700, lineHeight: 1.18 }}>
        <Typed text="Alte Switch (2020), Dock, beide Controller, Kratzer am Display, kein Karton. Was kann ich verlangen?" start={0.05} dur={2.2} />
      </div>
      <div style={{ position: "absolute", right: 70, top: 640, scale: S(sp(t, 0.3, fps)) }}>
        <Konsole w={440} kratzer />
        <div style={{ position: "absolute", right: 0, top: 215, fontSize: 46, fontWeight: 700, color: RED, whiteSpace: "nowrap" }}>mit Kratzern · ohne Karton</div>
      </div>
    </div>
  );
};

// ---------- 3 Claudes Preis ----------
export const ScenePreis: React.FC<{ unter: number }> = ({ unter }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 0, right: 0, top: 230, display: "flex", flexDirection: "column", alignItems: "center", gap: 44 }}>
        <div style={{ fontSize: 64, fontWeight: 700, color: MUTED }}>Claude sagt:</div>
        <div style={{ scale: S(sp(t, 0.05, fps)), background: PAPER, border: `8px solid ${INK}`, borderRadius: 36, padding: "20px 60px", fontSize: 170, fontWeight: 700, lineHeight: 1 }}>150 € <span style={{ fontSize: 100 }}>VB</span></div>
        <div style={{ scale: S(sp(t, unter, fps)), background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: 24, padding: "12px 40px", fontSize: 84, fontWeight: 700, color: RED }}>nicht unter 120 €</div>
      </div>
    </div>
  );
};

// ---------- 4 Kleinanzeigen-Angebote heute ----------
const ANZ = [
  { p: 100, l: "100 €" },
  { p: 150, l: "150 € VB" },
  { p: 160, l: "160 € VB" },
  { p: 200, l: "200 €" },
];
export const SceneMarkt: React.FC<{ passt: number }> = ({ passt }) => {
  const { t, fps } = useT();
  const x = (p: number) => 60 + ((p - 90) / 120) * 760;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 36, fontSize: 54, fontWeight: 700, lineHeight: 1.1 }}>Kleinanzeigen heute: ähnliche Switches</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 160, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22 }}>
        {ANZ.map((a, i) => (
          <div key={a.l} style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: "16px 20px", display: "flex", alignItems: "center", gap: 18, scale: S(sp(t, 0.05 + i * 0.15, fps)) }}>
            <Konsole w={150} />
            <div style={{ fontSize: 50, fontWeight: 700, color: NAVY, whiteSpace: "nowrap" }}>{a.l}</div>
          </div>
        ))}
      </div>
      {/* Preisskala */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 520, height: 200 }}>
        <div style={{ position: "absolute", left: x(100), width: x(200) - x(100), top: 70, height: 30, background: "#BFD0E6", borderRadius: 15, border: `4px solid ${NAVY}` }} />
        {[100, 200].map((p) => (
          <div key={p} style={{ position: "absolute", left: x(p) - 60, width: 120, top: 112, textAlign: "center", fontSize: 52, fontWeight: 700, color: NAVY, whiteSpace: "nowrap" }}>{p} €</div>
        ))}
        <div style={{ position: "absolute", left: x(150) - 80, width: 160, top: 0, textAlign: "center", opacity: fade(t, 0.8) }}>
          <div style={{ fontSize: 40, fontWeight: 700, color: "#E5835E" }}>Claude</div>
          <div style={{ margin: "0 auto", width: 0, height: 0, borderLeft: "22px solid transparent", borderRight: "22px solid transparent", borderTop: `34px solid #E5835E` }} />
        </div>
      </div>
      <Pop at={passt} style={{ position: "absolute", left: 0, right: 0, top: 690, display: "flex", justifyContent: "center" }}>
        <div style={{ background: "#E3F1EA", border: `6px solid ${GREEN}`, borderRadius: 24, padding: "8px 40px", fontSize: 76, fontWeight: 700, color: "#1C7049" }}>passt ✓</div>
      </Pop>
      <div style={{ position: "absolute", right: 40, bottom: 34, fontSize: 28, fontWeight: 600, color: MUTED }}>Angebotspreise 11.11.2026, ohne Spiele · keine Verkaufspreise</div>
    </div>
  );
};

// ---------- 5 Aber: Claudes Begründung ----------
export const SceneAber: React.FC<{ mark: number }> = ({ mark }) => {
  const { t } = useT();
  const w = interpolate(t, [mark, mark + 0.6], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, fontSize: 64, fontWeight: 700, color: RED }}>Aber …</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 260, background: PAPER, border: `6px solid ${INK}`, borderRadius: "34px 34px 34px 8px", padding: "28px 36px", fontSize: 66, fontWeight: 700, lineHeight: 1.2 }}>
        „Händler verkaufen aufbereitete Geräte schon ab{" "}
        <span style={{ backgroundImage: "linear-gradient(#FFE08A,#FFE08A)", backgroundRepeat: "no-repeat", backgroundSize: `${w}% 100%` }}>etwa 115–130 €</span>.“
      </div>
      <div style={{ position: "absolute", left: 40, top: 720, fontSize: 40, fontWeight: 700, color: MUTED, opacity: fade(t, mark + 0.4) }}>Quelle: 🔗 netzwelt.de</div>
    </div>
  );
};

// ---------- 6 Quelle geöffnet: Händler-Tabelle ----------
const ROWS = [
  { m: "Switch Lite", p: "116,95 €", lite: true },
  { m: "Switch (V1)", p: "146,95 €" },
  { m: "Switch (V2)", p: "156,95 €" },
];
export const SceneQuelle: React.FC<{ lite: number; normal: number }> = ({ lite, normal }) => {
  const { t } = useT();
  const ring = interpolate(t, [lite, lite + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 34, fontSize: 52, fontWeight: 700 }}>🔗 Quelle geöffnet</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden" }}>
        <div style={{ background: SAND, padding: "12px 28px", fontSize: 34, fontWeight: 700, color: MUTED }}>Händler, aufbereitet · netzwelt.de, 12.10.2026</div>
        {ROWS.map((r, i) => (
          <div key={r.m} style={{ position: "relative", display: "flex", justifyContent: "space-between", padding: "22px 34px", borderTop: i ? "4px solid #EFE4D2" : "none", fontSize: 64, fontWeight: 700, background: !r.lite && t >= normal ? "#E3F1EA" : "transparent", opacity: r.lite ? 1 : fade(t, 0.2 + i * 0.1) }}>
            <span>{r.m}</span>
            <span style={{ color: r.lite ? RED : NAVY }}>{r.p}</span>
            {r.lite && (
              <svg viewBox="0 0 200 60" preserveAspectRatio="none" style={{ position: "absolute", left: 6, top: 2, width: 856, height: 104, pointerEvents: "none" }}>
                <ellipse cx={100} cy={30} rx={97} ry={27} fill="none" stroke={RED} strokeWidth={2.4} strokeDasharray={420} strokeDashoffset={420 * (1 - ring)} strokeLinecap="round" />
              </svg>
            )}
          </div>
        ))}
      </div>
      <Pop at={lite + 0.3} style={{ position: "absolute", left: 300, top: 600 }}>
        <div style={{ background: RED, color: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "10px 30px", fontSize: 56, fontWeight: 700, rotate: "-4deg" }}>⬆ DAS war die Lite</div>
      </Pop>
      <Pop at={normal} style={{ position: "absolute", left: 300, top: 760 }}>
        <div style={{ background: "#E3F1EA", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "8px 28px", fontSize: 52, fontWeight: 700, color: "#1C7049" }}>normale: ab 147 €</div>
      </Pop>
      <div style={{ position: "absolute", left: 0, right: 0, top: 900, textAlign: "center", fontSize: 30, fontWeight: 600, color: MUTED }}>Preise mit Gutschein, Angebot vom 12.10.2026</div>
    </div>
  );
};

// ---------- 7 Urteil: HALB ----------
export const SceneUrteil: React.FC<{ stempel: number; klick: number }> = ({ stempel, klick }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 40, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${YEL}`, color: "#A87A12", borderRadius: 30, padding: "0 60px", fontSize: 220, fontWeight: 700, letterSpacing: 10, rotate: "-8deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>HALB</div>
      </div>
      <div style={{ position: "absolute", left: 120, right: 120, top: 470, display: "flex", flexDirection: "column", gap: 22, fontSize: 84, fontWeight: 700, opacity: fade(t, stempel + 0.3) }}>
        <div>Preis <span style={{ color: GREEN }}>✓</span></div>
        <div>Begründung <span style={{ color: RED }}>✗</span></div>
      </div>
      <Pop at={klick} style={{ position: "absolute", left: 0, right: 0, top: 760, display: "flex", justifyContent: "center" }}>
        <div style={{ background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "12px 38px", fontSize: 64, fontWeight: 700 }}>🔗 Quelle selbst anklicken</div>
      </Pop>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar SWITCH ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📋</div>
          <div style={{ fontSize: 54, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Meine Frage<br />zum<br />Kopieren<br /><span style={{ fontSize: 42, color: GREEN }}>+ 3 Anzeigen-<br />Tipps</span></div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 300, top: 840 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 92, fontWeight: 600, color: INK, letterSpacing: 4 }}>SWITCH</div>
        </div>
      </Pop>
    </div>
  );
};
