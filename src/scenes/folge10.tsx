import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge10 · „Steht auf deiner Referat-Folie zu viel?“ · Hook-Test Variante B (Paar 5) · ohne Werbung · Leinwand 948×1004
// Folie vom Studio erfunden (docs/plaene/beispiel/referat_folie_beispiel.txt), 7 Sätze.
// Claude-Antwort echt (docs/plaene/beispiel/referat_folie_claude_antwort.md). Zeiten in Props = Sekunden ab Szenenstart.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LGREEN = "#DDF1E6";
const HAND = "'Comic Sans MS', 'Fredoka', cursive";

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
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.9)", whiteSpace: "nowrap" }}>{text}</div>
);

const ClaudeHead: React.FC<{ size?: number }> = ({ size = 32 }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    Claude
  </div>
);

const SAETZE = [
  "Die Sonne erwärmt das Wasser in Meeren, Seen und Flüssen, wodurch es verdunstet und als unsichtbarer Wasserdampf in die Luft aufsteigt.",
  "Auch Pflanzen geben über ihre Blätter Wasser an die Luft ab.",
  "In größerer Höhe ist es kälter, deshalb kühlt der Wasserdampf ab und kondensiert zu winzigen Tröpfchen, aus denen Wolken entstehen.",
  "Wenn die Tröpfchen in den Wolken zusammenstoßen und zu groß und zu schwer werden, fallen sie als Niederschlag, also als Regen, Schnee oder Hagel, wieder auf die Erde.",
  "Ein Teil des Wassers versickert im Boden und wird zu Grundwasser, ein anderer Teil fließt über Bäche und Flüsse zurück ins Meer.",
  "Dort beginnt der Kreislauf wieder von vorne.",
  "Insgesamt geht dabei kein Wasser verloren, es wechselt nur ständig seinen Zustand und seinen Ort.",
];

// Präsentationsfolie 16:9 (eigene Zeichnung, keine Marken-Software)
const Folie: React.FC<{ w: number; children: React.ReactNode; tint?: string }> = ({ w, children, tint = PAPER }) => (
  <div style={{ width: w, height: w * 0.5625, background: tint, border: `5px solid ${INK}`, borderRadius: 10, boxShadow: "6px 8px 0 rgba(58,38,24,.14)", overflow: "hidden", position: "relative" }}>
    <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: w * 0.018, background: NAVY }} />
    {children}
  </div>
);

const AltFolie: React.FC<{ w: number; fs: number }> = ({ w, fs }) => (
  <Folie w={w}>
    <div style={{ padding: `${w * 0.035}px ${w * 0.04}px` }}>
      <div style={{ fontSize: fs * 2.1, fontWeight: 700, color: NAVY, lineHeight: 1.1 }}>Der Wasserkreislauf</div>
      <div style={{ fontSize: fs, lineHeight: 1.18, color: "#555", marginTop: fs * 0.4, textAlign: "justify" }}>{SAETZE.join(" ")}</div>
    </div>
  </Folie>
);

const NeuFolie: React.FC<{ w: number; fs: number; shown?: number[]; plus?: number }> = ({ w, fs, shown = [1, 1, 1], plus = 0 }) => {
  const words: [string, string][] = [["Verdunstung", NAVY], ["Kondensation", GREEN], ["Niederschlag", NAVY]];
  return (
    <Folie w={w}>
      <div style={{ padding: `${w * 0.04}px ${w * 0.05}px` }}>
        <div style={{ fontSize: fs * 0.62, fontWeight: 700, color: MUTED, letterSpacing: 2 }}>DER WASSERKREISLAUF</div>
        <div style={{ display: "flex", flexDirection: "column", gap: fs * 0.12, marginTop: fs * 0.2 }}>
          {words.map(([wd, c], i) => (
            <div key={wd} style={{ fontSize: fs, fontWeight: 700, color: c, lineHeight: 1.05, opacity: shown[i], translate: `${(1 - shown[i]) * 40}px 0px` }}>{wd}</div>
          ))}
          {plus > 0 && (
            <div style={{ fontFamily: HAND, fontSize: fs * 0.95, fontWeight: 700, color: DGREEN, rotate: "-3deg", opacity: plus, lineHeight: 1.05 }}>+ Versickern <span style={{ fontSize: fs * 0.75, color: RED }}>← Tipp</span></div>
          )}
        </div>
      </div>
    </Folie>
  );
};

const Karte: React.FC<{ w: number; fs: number }> = ({ w, fs }) => (
  <div style={{ width: w, background: "#FFFBEA", border: `4px solid ${INK}`, borderRadius: 8, padding: fs * 0.5, rotate: "4deg", boxShadow: "4px 6px 0 rgba(58,38,24,.14)", backgroundImage: "repeating-linear-gradient(transparent 0 22px, #E8DCB8 22px 24px)" }}>
    <div style={{ fontSize: fs, fontWeight: 700, color: MUTED }}>Sprechkarte</div>
    {[0.9, 0.7, 0.85, 0.6, 0.8].map((x, i) => (
      <div key={i} style={{ height: fs * 0.36, width: `${x * 100}%`, background: "#C9BCA4", borderRadius: 4, marginTop: fs * 0.3 }} />
    ))}
  </div>
);

// ---------- 1 Hook: Textwand vs. 3 Wörter, ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { t } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 18, textAlign: "center", fontSize: 52, fontWeight: 700, lineHeight: 1.05, color: NAVY, whiteSpace: "nowrap" }}>
        Referat-Folie: <span style={{ color: RED }}>7 Sätze</span>, <span style={{ color: GREEN }}>3 Wörter</span>
      </div>
      <div style={{ position: "absolute", left: 20, top: 150, rotate: "-4deg" }}>
        <AltFolie w={520} fs={13.5} />
        <div style={{ position: "absolute", left: 20, bottom: -40 }}><Stempel size={34} text="VORHER: 7 SÄTZE" rot={6} /></div>
      </div>
      <div style={{ position: "absolute", left: 560, top: 420, fontSize: 100, fontWeight: 700, color: GREEN, rotate: "30deg" }}>➜</div>
      <div style={{ position: "absolute", left: 352, top: 560, rotate: "2deg", scale: S(1 + 0.02 * Math.sin(t * 4) + 0.06 * fade(t, 3.4, 0.3) * (1 - fade(t, 5.1, 0.3))) }}>
        <NeuFolie w={570} fs={64} />
        <svg viewBox="0 0 200 100" preserveAspectRatio="none" style={{ position: "absolute", left: -24, top: 78, width: 440, height: 250, opacity: t > 3.4 ? 1 : 0 }}>
          <ellipse cx={100} cy={52} rx={96} ry={46} fill="none" stroke={GREEN} strokeWidth={4} strokeDasharray={460} strokeDashoffset={460 * (1 - lin(t, 3.4, 0.5))} strokeLinecap="round" />
        </svg>
        <div style={{ position: "absolute", left: 10, top: -34 }}><Stempel size={30} text="NACHHER · CLAUDE" rot={-4} color={GREEN} /></div>
        <div style={{ position: "absolute", right: -16, bottom: -46 }}><Stempel size={20} text="BEISPIEL" rot={-3} /></div>
      </div>
      <div style={{ position: "absolute", left: 700, top: 270, scale: S(1 + 0.25 * fade(t, 5.1, 0.3)), transformOrigin: "top right" }}>
        <Karte w={220} fs={26} />
        <div style={{ position: "absolute", left: -20, top: -12, right: -20, bottom: -12, border: `6px solid ${GREEN}`, borderRadius: 20, opacity: fade(t, 5.1, 0.2) }} />
      </div>
    </div>
  );
};

// ---------- 2 Beispiel: alte Folie groß + Frage ----------
export const SceneBeispiel: React.FC<{ zaehl: number }> = ({ zaehl }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 30, top: 26, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <AltFolie w={888} fs={23} />
        <div style={{ position: "absolute", left: 14, bottom: -30 }}><Stempel size={30} text="BEISPIEL" rot={-4} /></div>
      </div>
      <Pop at={zaehl} style={{ position: "absolute", right: 30, top: 420 }}>
        <div style={{ background: RED, color: PAPER, borderRadius: 24, padding: "8px 28px", fontSize: 64, fontWeight: 700, rotate: "4deg" }}>7 Sätze!</div>
      </Pop>
      <div style={{ position: "absolute", left: 140, right: 30, top: 560, opacity: fade(t, 0.2), scale: S(sp(t, 0.2, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "14px 22px", fontSize: 44, fontWeight: 600, lineHeight: 1.2 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 4 }}>An Claude:</div>
          „Kürz meine Folie. Höchstens drei Stichworte, der Rest kommt auf meine Sprechkarte. Schreib nichts Neues dazu.“
        </div>
      </div>
    </div>
  );
};

// ---------- 3 Die drei Wörter ----------
export const SceneDrei: React.FC<{ w1: number; w2: number; w3: number }> = ({ w1, w2, w3 }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 48, fontWeight: 700, color: MUTED }}>Claudes Folie</div>
      <div style={{ position: "absolute", left: 30, top: 120, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <NeuFolie w={888} fs={104} shown={[fade(t, w1), fade(t, w2), fade(t, w3)]} />
      </div>
      <div style={{ position: "absolute", left: 420, top: 680, fontSize: 56, fontWeight: 700, color: GREEN, opacity: fade(t, w3 + 0.5) }}>3 Wörter ✓</div>
    </div>
  );
};

// ---------- 4 Sprechkarte ----------
export const SceneKarte: React.FC<{ ok: number }> = ({ ok }) => {
  const { t, fps } = useT();
  const blocks: [string, string[]][] = [
    ["1. Verdunstung", ["Sonne erwärmt das Wasser …", "Pflanzen geben Wasser ab …"]],
    ["2. Kondensation", ["Wasserdampf kühlt ab …", "Tröpfchen, daraus Wolken …"]],
    ["3. Niederschlag", ["Regen, Schnee oder Hagel …", "versickert … zurück ins Meer …"]],
    ["Schluss", ["Es geht kein Wasser verloren."]],
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 50, right: 50, top: 30, background: "#FFFBEA", border: `6px solid ${INK}`, borderRadius: 16, padding: "18px 30px", rotate: "-1.5deg", scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <div style={{ fontSize: 46, fontWeight: 700, color: MUTED }}>Sprechkarte</div>
        {blocks.map(([h, ls], i) => (
          <div key={h} style={{ marginTop: 10, opacity: fade(t, 0.15 + i * 0.2) }}>
            <div style={{ fontSize: 42, fontWeight: 700, color: i === 3 ? GREEN : NAVY }}>{h}</div>
            {ls.map((l) => (
              <div key={l} style={{ fontSize: 38, fontWeight: 600, color: INK, lineHeight: 1.2 }}>• {l}</div>
            ))}
          </div>
        ))}
      </div>
      <Pop at={ok} style={{ position: "absolute", left: 380, top: 820 }}>
        <div style={{ background: LGREEN, border: `5px solid ${GREEN}`, borderRadius: 30, padding: "6px 26px", fontSize: 50, fontWeight: 700, color: DGREEN, whiteSpace: "nowrap" }}>Nichts erfunden ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 5 Claude sagt es selbst ----------
export const SceneZitat: React.FC<{ mark: number }> = ({ mark }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 52, fontWeight: 700, color: MUTED }}>Aber …</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", scale: S(sp(t, 0, fps)) }}>
        <ClaudeHead size={32} />
        <div style={{ padding: "18px 28px 26px", fontSize: 50, fontWeight: 600, lineHeight: 1.35 }}>
          „<span style={{ background: `rgba(255,224,138,${fade(t, mark)})`, borderRadius: 8, fontWeight: 700 }}>Das Versickern und das Zurückfließen ins Meer stehen nur auf der Sprechkarte</span>, damit die Folie bei drei Stichworten bleibt.“
        </div>
      </div>
      <Pop at={mark + 0.6} style={{ position: "absolute", left: 160, top: 640 }}>
        <Stempel size={56} rot={-5} text="NUR AUF DER KARTE" />
      </Pop>
    </div>
  );
};

// ---------- 6 Kreis offen ----------
export const SceneKreis: React.FC<{ luecke: number }> = ({ luecke }) => {
  const { t, fps } = useT();
  const R = 300;
  const cx = 474, cy = 470;
  const st: [string, number, string][] = [
    ["Verdunstung", -150, NAVY],
    ["Kondensation", -30, GREEN],
    ["Niederschlag", 60, NAVY],
    ["Versickern\n+ ins Meer", 150, RED],
  ];
  const g = lin(t, luecke, 0.4);
  const arc = (a1: number, a2: number) => {
    const r1 = (a1 * Math.PI) / 180, r2 = (a2 * Math.PI) / 180;
    return `M ${cx + R * Math.cos(r1)} ${cy + R * Math.sin(r1)} A ${R} ${R} 0 0 1 ${cx + R * Math.cos(r2)} ${cy + R * Math.sin(r2)}`;
  };
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 20, textAlign: "center", fontSize: 54, fontWeight: 700, color: INK }}>
        Auf der Folie: <span style={{ color: RED, opacity: fade(t, luecke) }}>kein Kreis mehr</span>
      </div>
      <svg width={948} height={1004} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d={arc(-150, 60)} stroke={GREEN} strokeWidth={16} fill="none" strokeLinecap="round" opacity={sp(t, 0, fps)} />
        <path d={arc(60, 210)} stroke={RED} strokeWidth={12} fill="none" strokeDasharray="22 22" opacity={1 - 0.75 * g} />
      </svg>
      {st.map(([n, a, c], i) => {
        const r = (a * Math.PI) / 180;
        const x = cx + R * Math.cos(r), y = cy + R * Math.sin(r);
        const miss = i === 3;
        return (
          <div key={n} style={{ position: "absolute", left: x - 150, top: y - 50, width: 300, textAlign: "center", opacity: miss ? 1 - 0.55 * g : fade(t, 0.1 + i * 0.15) }}>
            <div style={{ display: "inline-block", background: miss ? "#FBE3E0" : PAPER, border: `5px ${miss ? "dashed" : "solid"} ${c}`, borderRadius: 22, padding: "6px 16px", fontSize: 48, fontWeight: 700, color: c, whiteSpace: "pre-line", lineHeight: 1.1 }}>{n}</div>
          </div>
        );
      })}
      <Pop at={luecke + 0.2} style={{ position: "absolute", left: 120, top: 640 }}>
        <div style={{ fontSize: 120, fontWeight: 700, color: RED, lineHeight: 1 }}>✗</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; plus: number; zeilen: number }> = ({ stempel, plus, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 26, textAlign: "center", fontSize: 46, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 100, display: "flex", justifyContent: "center", zIndex: 2 }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 118, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.75)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 290, top: 330, rotate: "2deg" }}>
        <NeuFolie w={620} fs={46} plus={fade(t, plus, 0.3)} />
      </div>
      <div style={{ position: "absolute", left: 300, top: 690, display: "flex", flexDirection: "column", gap: 8, fontSize: 56, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, zeilen) }}>Nichts verloren <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.25) }}>Nichts erfunden <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.5) }}>Kreis offen <span style={{ color: RED }}>✗</span></div>
      </div>
      <div style={{ position: "absolute", left: 300, top: 910, fontSize: 48, fontWeight: 700, color: NAVY, opacity: fade(t, 3.2) }}>Die Folie zeigt, du redest.</div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar REFERAT ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📋</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Frage<br />zum<br />Kopieren</div>
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
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>REFERAT</div>
        </div>
      </Pop>
    </div>
  );
};
