import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";
import { Hamster } from "../Hamster";

// Folge16 · Hamster-Test „Neun Euro mit siebzehn – erlaubt?“ · Serie (a) · Einstiegs-Test E2 (Paar 3, E2 zuerst) · ohne Werbung
// Claude-Antwort wörtlich gekürzt aus docs/plaene/beispiel/lohn_claude_antwort.md. Werte: Bundesregierung Mindestlohn-FAQ (Stand 2026).
// Zeiten in Props = Sekunden ab Szenenstart. Unten links auf der Leinwand (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LRED = "#F9DEDA";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const slam = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 9, stiffness: 240 } }));
const S = (v: number) => String(Math.max(0.0001, v));

const Stempel: React.FC<{ size?: number; rot?: number; text: string; color?: string; s?: number }> = ({ size = 34, rot = -8, text, color = RED, s = 1 }) => (
  <div style={{ display: "inline-block", border: `${Math.round(size / 6)}px solid ${color}`, color, borderRadius: 14, padding: "0 18px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.9)", whiteSpace: "nowrap", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1 }}>{text}</div>
);

const ClaudeHead: React.FC<{ size?: number; title?: string }> = ({ size = 32, title = "Claude" }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    {title}
  </div>
);

const M: React.FC<{ children: React.ReactNode; v?: number; c?: "g" | "r" }> = ({ children, v = 0, c = "g" }) => {
  const bg = c === "g" ? `rgba(205,235,217,${v})` : `rgba(249,222,218,${v})`;
  return <span style={{ background: v > 0 ? bg : "transparent", color: v > 0.5 ? (c === "g" ? DGREEN : RED) : "inherit", borderRadius: 8, padding: "0 4px", fontWeight: v > 0.5 ? 700 : "inherit" }}>{children}</span>;
};

// Claudes Antwort (gekürzt, wörtlich)
const Antwort: React.FC<{ w: number; fs: number; ja?: number; par?: number; head?: number }> = ({ w, fs, ja = 1, par = 0, head = 28 }) => (
  <div style={{ width: w, background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden", boxShadow: "6px 8px 0 rgba(58,38,24,.14)" }}>
    <ClaudeHead size={head} title="Claude" />
    <div style={{ padding: `${fs * 0.35}px ${fs * 0.5}px`, fontSize: fs, lineHeight: 1.25, color: "#1E2430" }}>
      <div>Kurz gesagt: <M v={ja}>Ja, das ist erlaubt.</M></div>
      <div style={{ marginTop: fs * 0.3, fontSize: fs * 0.82 }}>Er gilt nicht für Jugendliche unter 18 ohne abgeschlossene Berufsausbildung (<M v={par}>§ 22 Mindestlohngesetz</M>).</div>
    </div>
  </div>
);

const Lohn: React.FC<{ fs: number; stamp: number }> = ({ fs, stamp }) => (
  <div style={{ position: "relative", display: "inline-block", whiteSpace: "nowrap", background: "#FFF0C2", border: `6px solid ${NAVY}`, borderRadius: 26, padding: `${fs * 0.08}px ${fs * 0.3}px` }}>
    <div style={{ fontSize: fs * 0.26, fontWeight: 700, color: MUTED, letterSpacing: 2 }}>MINDESTLOHN 2026</div>
    <div style={{ fontSize: fs, fontWeight: 700, color: NAVY, lineHeight: 1 }}>13,90 €</div>
    <div style={{ position: "absolute", right: -fs * 0.05, top: fs * 1.0 }}>
      <Stempel size={fs * 0.42} rot={-12} text="ERST AB 18" s={stamp} />
    </div>
  </div>
);

// ---------- 0 E2-Hook (Vollbild 1080×1920, 0–1,0 s) ----------
export const E2Hook: React.FC = () => {
  const { t, frame, fps } = useT();
  const st = slam(t, 0.15, fps);
  // Hamster stößt mit dem Zeigestab zum Stempel, wenn er landet
  const jab = interpolate(t, [0, 0.12, 0.2, 0.45], [30, 5, 14, 10], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center" }}>
        <div style={{ fontSize: 34, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST · Minijob mit 17</div>
        <div style={{ fontSize: 80, fontWeight: 700, lineHeight: 1.05, color: NAVY, whiteSpace: "nowrap" }}>Mit 17: <span style={{ color: RED }}>kein Mindestlohn?</span></div>
      </div>
      <div style={{ position: "absolute", left: 30, top: 295, rotate: "-1deg" }}>
        <Antwort w={1020} fs={64} ja={fade(t, 0.02, 0.15)} par={fade(t, 0.3, 0.2)} head={38} />
      </div>
      <div style={{ position: "absolute", left: 40, top: 860 }}>
        <Lohn fs={255} stamp={st} />
      </div>
      <div style={{ position: "absolute", left: 300, top: 1400, rotate: "-3deg", background: PAPER, border: `4px solid ${INK}`, borderRadius: 16, padding: "6px 18px", fontSize: 44, fontWeight: 700 }}>9 €/Std. mit 17?</div>
      <div style={{ position: "absolute", left: 10, top: 1450 }}>
        <Hamster size={260} talking={frame % 6 < 3} blink={false} pointerAngle={jab} />
      </div>
      <div style={{ position: "absolute", left: 230, top: 1330, fontSize: 70, fontWeight: 700, color: RED, opacity: st > 0 ? 1 - fade(t, 0.5, 0.3) : 0, rotate: "15deg" }}>!</div>
    </AbsoluteFill>
  );
};

// ---------- 0b Hook auf der Leinwand (ab 1,0 s) ----------
export const SceneHook: React.FC = () => (
  <div style={{ position: "absolute", inset: 0, background: CREAM }}>
    <div style={{ position: "absolute", left: 0, right: 0, top: 14, textAlign: "center" }}>
      <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST · Minijob mit 17</div>
      <div style={{ fontSize: 62, fontWeight: 700, lineHeight: 1.05, color: NAVY, whiteSpace: "nowrap" }}>Mit 17: <span style={{ color: RED }}>kein Mindestlohn?</span></div>
    </div>
    <div style={{ position: "absolute", left: 24, top: 130 }}>
      <Antwort w={900} fs={48} ja={1} par={1} />
    </div>
    <div style={{ position: "absolute", left: 300, top: 540 }}>
      <Lohn fs={140} stamp={1} />
    </div>
  </div>
);

// ---------- 1 Die Frage an Claude ----------
export const SceneFrage: React.FC<{ neun: number }> = ({ neun }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 58, fontWeight: 700, color: NAVY }}>HAMSTER-TEST</div>
      <div style={{ position: "absolute", left: 40, top: 100, fontSize: 40, fontWeight: 600, color: MUTED }}>Ich hab Claude gefragt:</div>
      <div style={{ position: "absolute", left: 110, right: 30, top: 180, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "16px 28px", fontSize: 50, fontWeight: 600, lineHeight: 1.25 }}>
          „Ich bin 17 und hab einen Minijob in einem Café angeboten bekommen. Die zahlen <M v={fade(t, neun)} c="r">neun Euro die Stunde</M>. Ist das überhaupt erlaubt?“
        </div>
        <div style={{ marginTop: 12, textAlign: "right", fontSize: 30, fontWeight: 700, color: MUTED }}>Beispielfrage · keine echte Person</div>
      </div>
      <Pop at={neun + 0.3} style={{ position: "absolute", left: 420, top: 700 }}>
        <div style={{ fontSize: 120, fontWeight: 700, color: RED }}>9 € ?</div>
      </Pop>
    </div>
  );
};

// ---------- 2 Claude sagt Ja + § 22 (Nahaufnahme) ----------
export const SceneJa: React.FC<{ par: number; unter: number }> = ({ par, unter }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF7F1" }}>
      <div style={{ position: "absolute", left: 40, top: 24, display: "flex", alignItems: "center", gap: 14, fontSize: 44, fontWeight: 600, color: MUTED }}>
        <div style={{ width: 26, height: 26, borderRadius: 20, background: "#E5835E" }} /> Claude sagt:
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 110, scale: S(sp(t, 0.4, fps)), transformOrigin: "top left", fontSize: 96, fontWeight: 700, color: DGREEN, lineHeight: 1, whiteSpace: "nowrap" }}>„Ja, das ist erlaubt.“</div>
      <Pop at={par} style={{ position: "absolute", left: 40, top: 270 }}>
        <div style={{ background: PAPER, border: `6px solid ${GREEN}`, borderRadius: 22, padding: "6px 30px", fontSize: 96, fontWeight: 700, color: DGREEN }}>§ 22 <span style={{ fontSize: 52, color: INK }}>Mindestlohngesetz</span></div>
      </Pop>
      <Pop at={unter} style={{ position: "absolute", left: 30, right: 30, top: 500 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: "16px 24px", fontSize: 58, fontWeight: 700, lineHeight: 1.2, textAlign: "center" }}>
          unter 18 <span style={{ color: GREEN }}>+</span> ohne abgeschlossene Ausbildung<br /><span style={{ color: RED, fontSize: 72 }}>= kein Mindestlohn</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 3 Im Gesetz nachgelesen ----------
export const SceneGesetz: React.FC<{ stimmt: number }> = ({ stimmt }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#F4F1EA" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 56, fontWeight: 700, color: MUTED }}>Im Gesetz nachgelesen:</div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 120, scale: S(sp(t, 0, fps)), transformOrigin: "top center", background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: "22px 30px", fontSize: 54, lineHeight: 1.3, color: "#222" }}>
        <div style={{ fontWeight: 700, fontSize: 60, color: NAVY }}>§ 22 Abs. 2 Mindestlohngesetz</div>
        <div style={{ marginTop: 12, fontWeight: 600 }}>Jugendliche unter 18 <M v={fade(t, 0.4)}>ohne abgeschlossene Berufsausbildung</M> gelten nicht als Arbeitnehmer im Sinne dieses Gesetzes.</div>
        <div style={{ marginTop: 10, fontSize: 32, color: MUTED }}>(sinngemäß gekürzt, mit § 2 JArbSchG)</div>
      </div>
      <div style={{ position: "absolute", left: 400, top: 700 }}>
        <Stempel size={100} rot={-8} text="STIMMT ✓" color={GREEN} s={slam(t, stimmt, fps)} />
      </div>
    </div>
  );
};

// ---------- 4 Ab dem 18. Geburtstag ----------
export const SceneAchtzehn: React.FC<{ lohn: number; jan: number }> = ({ lohn, jan }) => {
  const { t, fps, frame } = useT();
  const flame = 1 + Math.sin(frame / 2) * 0.12;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FFF4E0" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 54, fontWeight: 700, color: NAVY }}>Ab dem 18. Geburtstag:</div>
      {/* Kuchen */}
      <svg width={300} height={300} viewBox="0 0 300 300" style={{ position: "absolute", left: 40, top: 130, scale: S(sp(t, 0, fps)) }}>
        <rect x={40} y={150} width={220} height={110} rx={18} fill="#F7C9D6" stroke={INK} strokeWidth={6} />
        <path d="M40 180 Q75 205 110 180 T180 180 T260 180" fill="none" stroke={PAPER} strokeWidth={10} />
        <rect x={135} y={80} width={30} height={72} rx={6} fill={GREEN} stroke={INK} strokeWidth={5} />
        <ellipse cx={150} cy={64} rx={12 * flame} ry={20 * flame} fill="#F6A623" stroke={INK} strokeWidth={3} />
        <text x={150} y={240} textAnchor="middle" fontSize={64} fontWeight={700} fill={INK} fontFamily="Fredoka">18</text>
      </svg>
      <div style={{ position: "absolute", left: 380, top: 150, display: "flex", alignItems: "center", gap: 20, opacity: fade(t, lohn - 0.6) }}>
        <div style={{ fontSize: 90, fontWeight: 700, color: RED, textDecoration: "line-through" }}>9 €</div>
        <div style={{ fontSize: 80, fontWeight: 700, color: INK }}>→</div>
      </div>
      <Pop at={lohn} style={{ position: "absolute", left: 360, top: 280 }}>
        <div style={{ background: "#CDEBD9", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "4px 24px" }}>
          <div style={{ fontSize: 32, fontWeight: 700, color: DGREEN }}>mindestens</div>
          <div style={{ fontSize: 120, fontWeight: 700, color: DGREEN, lineHeight: 1 }}>13,90 €</div>
        </div>
      </Pop>
      <Pop at={jan} style={{ position: "absolute", left: 360, top: 560 }}>
        <div style={{ background: PAPER, border: `5px solid ${NAVY}`, borderRadius: 20, padding: "8px 24px", fontSize: 56, fontWeight: 700, color: NAVY }}>ab 1.1.2027: <span style={{ color: GREEN }}>14,60 €</span></div>
      </Pop>
      <div style={{ position: "absolute", left: 360, right: 20, top: 690, fontSize: 38, fontWeight: 600, color: MUTED, opacity: fade(t, jan + 0.3) }}>Quelle: Bundesregierung, Mindestlohn-FAQ 2026</div>
    </div>
  );
};

// ---------- 5 Lücke: sittenwidrig ----------
export const SceneLuecke: React.FC<{ sitten: number }> = ({ sitten }) => {
  const { t, fps } = useT();
  const w = fade(t, sitten, 0.2);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 58, fontWeight: 700, color: RED }}>Was Claude nicht sagt:</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, scale: S(sp(t, 0.9, fps)), transformOrigin: "top left", background: LRED, border: `6px solid ${RED}`, borderRadius: 24, padding: "30px 34px", fontSize: 76, fontWeight: 700, lineHeight: 1.2, color: INK }}>
        Auch mit 17 darf dein Lohn nicht{" "}
        <span style={{ background: `rgba(255,255,255,${w})`, color: w > 0.5 ? RED : INK, border: `${w > 0.5 ? 5 : 0}px solid ${RED}`, borderRadius: 10, padding: "0 8px" }}>sittenwidrig niedrig</span>{" "}
        sein.
      </div>
      <div style={{ position: "absolute", left: 360, right: 30, top: 600, fontSize: 52, fontWeight: 700, color: RED, opacity: fade(t, sitten + 0.4) }}>§ 138 BGB (Lohnwucher)<br />fehlt in Claudes Antwort ✗</div>
    </div>
  );
};

// ---------- 6 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number; fair: number }> = ({ stempel, zeilen, fair }) => {
  const { t, fps } = useT();
  const z: [string, boolean][] = [["§ 22 richtig", true], ["ab 18: mind. 13,90 €", true], ["„sittenwidrig“ fehlt", false]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 30, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <Stempel size={100} rot={-6} text="GEKLAPPT" color={GREEN} s={slam(t, stempel, fps)} />
      </div>
      <div style={{ position: "absolute", left: 300, right: 10, top: 380, display: "flex", flexDirection: "column", gap: 18, fontSize: 52, whiteSpace: "nowrap", fontWeight: 700 }}>
        {z.map(([txt, ok], i) => (
          <div key={txt} style={{ opacity: fade(t, zeilen + i * 0.15, 0.15), color: ok ? INK : RED, background: ok ? "transparent" : LRED, borderRadius: 12, padding: "0 8px", width: "fit-content" }}>{txt} <span style={{ color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span></div>
        ))}
      </div>
      <Pop at={fair} style={{ position: "absolute", left: 300, right: 10, top: 680 }}>
        <div style={{ fontSize: 56, fontWeight: 700, color: NAVY }}>erlaubt ≠ fair</div>
        <div style={{ fontSize: 46, fontWeight: 700, color: GREEN }}>→ frag nach mehr Geld</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Ende: Handy + Kommentar LOHN ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 440, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 18, padding: 18 }}>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>5 Fragen<br />vor dem<br />ersten<br />Minijob</div>
          <div style={{ background: "#CDEBD9", border: `4px solid ${GREEN}`, borderRadius: 16, padding: "8px 14px", fontSize: 40, fontWeight: 700, color: DGREEN, textAlign: "center", lineHeight: 1.2 }}>Lohn · Zeiten<br />Vertrag · Urlaub<br />krank</div>
          <div style={{ fontSize: 28, fontWeight: 600, color: MUTED, textAlign: "center" }}>keine Rechtsberatung<br />Claude-Konto ab 18</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 300, top: 850 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>LOHN</div>
        </div>
      </Pop>
    </div>
  );
};
