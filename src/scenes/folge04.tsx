import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge04 · Hamster-Test „Fitnessstudio kündigen“ · Hook-Test Variante A (Paar 2) · ohne Werbung · Leinwand 948×1004
// Echte Claude-Antwort (frischer Kontext, 13.11.2026), Vertrag = Beispiel. Keine Logos, kein Studio-Name.
// Zeiten in den Props = Sekunden ab Szenenstart. Unten links (y > ~860, x < ~420) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const MARK = "#FFE08A";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const S = (v: number) => String(Math.max(0.0001, v));

const ClaudeHead: React.FC<{ right?: React.ReactNode }> = ({ right }) => (
  <div style={{ height: 80, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 28px", fontSize: 36, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);

const BeispielStempel: React.FC<{ size?: number; rot?: number }> = ({ size = 30, rot = -8 }) => (
  <div style={{ display: "inline-block", border: `5px solid ${RED}`, color: RED, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.85)" }}>BEISPIEL</div>
);

// Gezeichnete Hantel (generisch), optional mit Anhänger
const Hantel: React.FC<{ w?: number; tag?: string }> = ({ w = 340, tag }) => (
  <div style={{ position: "relative", width: w, height: w * 0.42 }}>
    <svg viewBox="0 0 200 84" width={w} height={w * 0.42}>
      <rect x={40} y={36} width={120} height={12} rx={5} fill="#9AA3AE" stroke={INK} strokeWidth={3} />
      <rect x={14} y={8} width={30} height={68} rx={8} fill={NAVY} stroke={INK} strokeWidth={3} />
      <rect x={2} y={20} width={16} height={44} rx={6} fill={NAVY} stroke={INK} strokeWidth={3} />
      <rect x={156} y={8} width={30} height={68} rx={8} fill={NAVY} stroke={INK} strokeWidth={3} />
      <rect x={182} y={20} width={16} height={44} rx={6} fill={NAVY} stroke={INK} strokeWidth={3} />
    </svg>
    {tag && (
      <div style={{ position: "absolute", left: w * 0.38, top: w * 0.27, rotate: "10deg", transformOrigin: "top left" }}>
        <div style={{ width: 4, height: 40, background: INK, marginLeft: 20 }} />
        <div style={{ background: MARK, border: `5px solid ${INK}`, borderRadius: 10, padding: "4px 14px", fontSize: 34, fontWeight: 700, whiteSpace: "nowrap" }}>✉️ {tag}</div>
      </div>
    )}
  </div>
);

// ---------- 1 Hook: Ergebnis ab Frame 0 ----------
export const SceneHook: React.FC<{ jahr: number }> = ({ jahr }) => {
  const { t, frame } = useT();
  const pulse = 1 + Math.max(0, Math.sin(frame / 5)) * 0.05;
  const strike = 1; // Durchgestrichen ab Frame 0 (Ergebnis zuerst)
  const shake = t >= jahr && t < jahr + 0.5 ? Math.sin((t - jahr) * 40) * 6 : 0;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 20, textAlign: "center", fontSize: 30, fontWeight: 700, color: GREEN, letterSpacing: 4 }}>🐹 HAMSTER-TEST</div>
      <div style={{ position: "absolute", left: 16, right: 16, top: 60, textAlign: "center", fontSize: 66, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>
        Fitnessstudio kündigen: <span style={{ color: GREEN }}>Wie schnell raus?</span>
      </div>
      {/* links: "noch 12 Monate" durchgestrichen */}
      <div style={{ position: "absolute", left: 26, top: 300, width: 340, rotate: `${-5 + shake * 0.3}deg` }}>
        <div style={{ position: "relative", background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "14px 16px", textAlign: "center" }}>
          <div style={{ fontSize: 34, fontWeight: 600, color: MUTED }}>gedacht:</div>
          <div style={{ fontSize: 56, fontWeight: 700, lineHeight: 1.1, whiteSpace: "nowrap" }}>+12 Monate</div>
          <div style={{ fontSize: 40, fontWeight: 700, color: MUTED }}>Verlängerung</div>
          <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
            <line x1={4} y1={96} x2={96} y2={6} stroke={RED} strokeWidth={4} strokeOpacity={0.85} strokeDasharray={130} strokeDashoffset={130 * (1 - strike)} strokeLinecap="round" />
          </svg>
        </div>
      </div>
      <div style={{ position: "absolute", left: 360, top: 380, fontSize: 80, fontWeight: 700, color: GREEN }}>➜</div>
      {/* rechts: Claude-Ergebnis */}
      <div style={{ position: "absolute", right: 26, top: 240, width: 470, background: PAPER, border: `6px solid ${INK}`, borderRadius: 28, overflow: "hidden", boxShadow: "0 10px 0 rgba(58,38,24,.12)" }}>
        <ClaudeHead />
        <div style={{ position: "relative", padding: "14px 10px 26px", textAlign: "center" }}>
          <div style={{ fontSize: 40, fontWeight: 600, color: MUTED, marginBottom: 14 }}>höchstens</div>
          <div style={{ fontSize: 100, fontWeight: 700, lineHeight: 1, color: "#1C7049", scale: String(pulse) }}>1 Monat</div>
          <div style={{ fontSize: 40, fontWeight: 600, color: MUTED, marginTop: 14 }}>Frist</div>
          <svg viewBox="0 0 200 100" preserveAspectRatio="none" style={{ position: "absolute", left: 6, top: 62, width: "96%", height: 140, pointerEvents: "none" }}>
            <ellipse cx={100} cy={50} rx={96} ry={46} fill="none" stroke={GREEN} strokeWidth={2.6} />
          </svg>
        </div>
      </div>
      {/* Hantel mit Kündigung, an der Zeigestab-Spitze (~440, 860) */}
      <div style={{ position: "absolute", left: 470, top: 690, rotate: `${-14 + Math.sin(frame / 6) * 4}deg` }}>
        <Hantel w={360} tag="KÜNDIGUNG" />
      </div>
      <svg width={948} height={1004} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
        <path d="M 400 960 Q 430 760 520 740" fill="none" stroke={MUTED} strokeWidth={6} strokeDasharray="14 14" strokeDashoffset={-frame * 2} strokeLinecap="round" opacity={0.7} />
      </svg>
    </div>
  );
};

// ---------- 2 Vertrag (Beispiel) ----------
export const SceneVertrag: React.FC<{ vorbei: number }> = ({ vorbei }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 70, right: 70, top: 60, background: PAPER, border: `6px solid ${INK}`, borderRadius: 18, padding: "26px 34px", scale: S(sp(t, 0.03, fps)), transformOrigin: "top center" }}>
        <div style={{ fontSize: 52, fontWeight: 700, borderBottom: `4px solid ${INK}`, paddingBottom: 10, marginBottom: 16 }}>Mitgliedsvertrag</div>
        {[
          ["Beginn", "03/2025"],
          ["Mindestlaufzeit", "12 Monate"],
          ["Beitrag", "29,99 € / Monat"],
          ["Zahlung", "Lastschrift"],
        ].map(([a, b]) => (
          <div key={a} style={{ display: "flex", justifyContent: "space-between", fontSize: 44, fontWeight: 600, lineHeight: 1.55 }}>
            <span style={{ color: MUTED }}>{a}</span>
            <span>{b}</span>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", right: 60, top: 40 }}>
        <BeispielStempel size={34} rot={7} />
      </div>
      <Pop at={vorbei} style={{ position: "absolute", left: 300, right: 50, top: 620 }}>
        <div style={{ background: "#E3F1EA", border: `6px solid ${GREEN}`, color: "#1C7049", borderRadius: 22, padding: "10px 26px", fontSize: 54, fontWeight: 700, textAlign: "center" }}>seit 03/2026 vorbei ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 3 Claude sagt: höchstens 1 Monat (Zeitstrahl) ----------
export const SceneClaude: React.FC<{ hoechstens: number }> = ({ hoechstens }) => {
  const { t, fps } = useT();
  const grow = interpolate(t, [0.1, 1.0], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const X0 = 50, X1 = 400, X2 = 640, X3 = 860;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 50, right: 50, top: 120, background: "#F1E6D3", borderRadius: 30, padding: "18px 26px", fontSize: 40, fontWeight: 600, lineHeight: 1.2, opacity: fade(t, 0) }}>
        „Du kannst dann jederzeit mit <b style={{ color: "#1C7049" }}>höchstens einem Monat Frist</b> kündigen.“
      </div>
      {/* Zeitstrahl */}
      <div style={{ position: "absolute", left: X0, top: 450, width: (X3 - X0) * grow, height: 18, background: INK, borderRadius: 9 }} />
      <div style={{ position: "absolute", left: X0, top: 390, width: X1 - X0, height: 130, background: "#D9D2C6", border: `5px solid ${INK}`, borderRadius: 16, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", fontSize: 42, fontWeight: 700, color: MUTED, lineHeight: 1.05, opacity: fade(t, 0.1) }}>Mindest-<br />laufzeit ✓</div>
      {[
        [X0 + 40, "03/25"],
        [X1, "03/26"],
        [X2, "heute"],
      ].map(([x, l]) => (
        <div key={l as string} style={{ position: "absolute", left: (x as number) - 90, width: 180, top: 540, textAlign: "center", fontSize: 56, fontWeight: 700, opacity: fade(t, 0.2) }}>{l}</div>
      ))}
      <div style={{ position: "absolute", left: X2, top: 390, width: X3 - X2 + 40, height: 130, background: "#E3F1EA", border: `6px solid ${GREEN}`, borderRadius: 16, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 52, fontWeight: 700, color: "#1C7049", scale: S(sp(t, hoechstens, fps)) }}>≤ 1 Monat</div>
      <Pop at={hoechstens + 0.3} style={{ position: "absolute", left: 400, right: 30, top: 680 }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "10px 24px", fontSize: 46, fontWeight: 700, textAlign: "center" }}>
          keine 12 Monate <span style={{ color: RED }}>Verlängerung</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 4 Nachgeprüft: § 309 Nr. 9 BGB ----------
export const SceneGesetz: React.FC<{ stimmt: number }> = ({ stimmt }) => {
  const { t, fps } = useT();
  const s = t < stimmt ? 0 : spring({ frame: (t - stimmt) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 34, fontSize: 56, fontWeight: 700 }}>🔍 Nachgeprüft</div>
      <div style={{ position: "absolute", left: 50, right: 50, top: 150, background: PAPER, border: `6px solid ${NAVY}`, borderRadius: 22, padding: "24px 30px", scale: S(sp(t, 0.05, fps)), transformOrigin: "top center" }}>
        <div style={{ fontSize: 64, fontWeight: 700, color: NAVY }}>§ 309 Nr. 9 BGB</div>
        <div style={{ fontSize: 44, fontWeight: 600, lineHeight: 1.3, marginTop: 10 }}>
          Vertrag ab <span style={{ background: MARK }}>1.3.2022</span> geschlossen:<br />nach der Mindestlaufzeit jederzeit kündbar, Frist <b>max. 1 Monat</b>
        </div>
        <div style={{ fontSize: 30, fontWeight: 600, color: MUTED, marginTop: 14 }}>Quelle: Gesetzestext</div>
      </div>
      <div style={{ position: "absolute", left: 420, top: 640, border: `12px solid ${GREEN}`, color: "#1C7049", borderRadius: 26, padding: "0 34px", fontSize: 110, fontWeight: 700, rotate: "-8deg", scale: S(s === 0 ? 0 : 2 - s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.75)" }}>STIMMT</div>
    </div>
  );
};

// ---------- 5 Brief + Lastschrift-Tipp ----------
export const SceneBrief: React.FC<{ tipp: number; gebuehren: number }> = ({ tipp, gebuehren }) => {
  const { t, fps } = useT();
  const mark = interpolate(t, [tipp, tipp + 0.6], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 60, right: 60, top: 36, background: PAPER, border: `5px solid ${INK}`, borderRadius: 10, padding: "22px 30px", lineHeight: 1.25, rotate: "-1.5deg", scale: S(sp(t, 0.03, fps)), transformOrigin: "top center" }}>
        <div style={{ fontSize: 46, fontWeight: 700, marginBottom: 14 }}>✉️ Kündigung meiner Mitgliedschaft</div>
        <div style={{ height: 14, width: "80%", background: "#E7E1D6", borderRadius: 7, marginBottom: 10 }} />
        <div style={{ height: 14, width: "62%", background: "#E7E1D6", borderRadius: 7, marginBottom: 18 }} />
        <div style={{ fontSize: 44, fontWeight: 700 }}>
          <span style={{ background: `linear-gradient(90deg, ${MARK} ${mark}%, transparent ${mark}%)` }}>„Ich widerrufe das SEPA-Lastschriftmandat mit Wirkung zum Vertragsende.“</span>
        </div>
        <div style={{ height: 14, width: "40%", background: "#E7E1D6", borderRadius: 7, marginTop: 18 }} />
      </div>
      <Pop at={tipp + 0.2} style={{ position: "absolute", left: 380, right: 40, top: 520 }}>
        <div style={{ background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "10px 24px", fontSize: 44, fontWeight: 700, lineHeight: 1.15 }}>Lastschrift erst zum Vertragsende stoppen</div>
      </Pop>
      <Pop at={gebuehren} style={{ position: "absolute", left: 420, right: 40, top: 720 }}>
        <div style={{ background: "#FDE3DF", border: `6px solid ${RED}`, color: RED, borderRadius: 22, padding: "8px 24px", fontSize: 44, fontWeight: 700 }}>sonst Rücklastschrift-Gebühren</div>
      </Pop>
    </div>
  );
};

// ---------- 6 Aber: Kündigungsbutton zu eng ----------
export const SceneButton: React.FC<{ eng: number; online: number }> = ({ eng, online }) => {
  const { t, fps } = useT();
  const s = t < eng ? 0 : spring({ frame: (t - eng) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 60, fontWeight: 700, color: RED }}>Aber: Kündigungsbutton</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 140, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden" }}>
        <ClaudeHead />
        <div style={{ padding: "18px 26px", fontSize: 42, fontWeight: 600, lineHeight: 1.25 }}>
          „<span style={{ background: MARK }}>Hast du online abgeschlossen</span>, muss das Studio … einen Button haben.“
        </div>
      </div>
      <div style={{ position: "absolute", right: 60, top: 420, border: `10px solid #D9A400`, color: "#A87C00", borderRadius: 22, padding: "0 26px", fontSize: 76, fontWeight: 700, rotate: "8deg", scale: S(s === 0 ? 0 : 2 - s), opacity: s === 0 ? 0 : 1, background: "rgba(255,248,220,.9)" }}>ZU ENG</div>
      <Pop at={online - 0.4} style={{ position: "absolute", left: 300, right: 36, top: 590 }}>
        <div style={{ background: "#E3F1EA", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "12px 22px", fontSize: 40, fontWeight: 700, color: "#1C7049", lineHeight: 1.2 }}>
          Pflicht, sobald man auf der Website Mitglied werden kann, egal wo du unterschrieben hast.
          <div style={{ fontSize: 28, color: MUTED, marginTop: 6 }}>§ 312k BGB</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 7 Urteil: GEKLAPPT ----------
export const SceneUrteil: React.FC<{ stempel: number; monat: number }> = ({ stempel, monat }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: "#1C7049", borderRadius: 30, padding: "0 40px", fontSize: 130, fontWeight: 700, letterSpacing: 5, rotate: "-6deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 40, right: 30, top: 420, display: "flex", justifyContent: "center", alignItems: "center", gap: 24, fontSize: 92, fontWeight: 700, opacity: fade(t, monat - 0.1) }}>
        <span style={{ color: "#1C7049", textAlign: "center", lineHeight: 1 }}>1 Monat<div style={{ fontSize: 36, color: MUTED }}>Frist</div></span>
        <span style={{ fontSize: 44, color: MUTED }}>statt</span>
        <span style={{ color: RED, textAlign: "center", lineHeight: 1 }}><span style={{ textDecoration: "line-through", textDecorationThickness: 6 }}>1 Jahr</span><div style={{ fontSize: 36, color: MUTED }}>Verlängerung</div></span>
      </div>
      <div style={{ position: "absolute", left: 420, right: 30, top: 600, fontSize: 44, fontWeight: 600, color: MUTED, opacity: fade(t, monat + 0.5), lineHeight: 1.25 }}>Brief ✓ · Lastschrift-Tipp ✓<br />Button-Regel: zu eng</div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar RAUS ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>✉️</div>
          <div style={{ fontSize: 54, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Der Brief<br />zum<br />Kopieren</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 360, top: 840 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 92, fontWeight: 600, color: INK, letterSpacing: 4 }}>RAUS</div>
        </div>
      </Pop>
    </div>
  );
};
