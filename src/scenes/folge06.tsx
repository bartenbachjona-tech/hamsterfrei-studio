import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge06 · Hamster-Test „5 Mittagessen für 20 €“ · Hook-Test Variante A (Paar 3) · ohne Werbung · Leinwand 948×1004
// Claude-Antwort echt (docs/plaene/beispiel/mittagessen_claude_antwort.md), Preise geprüft auf aldi-sued.de (15.11.2026).
// Zeiten in Props = Sekunden ab Szenenstart. Unten links (y > ~860, x < ~380) frei lassen: Hamster. Zeigestab-Spitze ~ (440, 930).
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

const ClaudeHead: React.FC<{ right?: React.ReactNode; size?: number }> = ({ right, size = 36 }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 22px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);

// Claudes Einkaufszettel (echte Antwort, 16 Artikel)
const ZETTEL: [string, string][] = [
  ["Reis 1 kg", "1,39"], ["Nudeln 500 g", "0,99"], ["Rote Linsen", "1,49"], ["Kidneybohnen", "0,75"],
  ["Mais", "0,79"], ["Pass. Tomaten", "0,65"], ["Kokosmilch", "1,19"], ["Paprika 3er", "1,99"],
  ["Zwiebeln 1 kg", "1,19"], ["Möhren 1 kg", "0,99"], ["Gurke", "0,69"], ["Eier 6er", "1,69"],
  ["Wraps", "1,39"], ["Feta 200 g", "1,39"], ["Currypulver", "0,99"], ["Paprikapulver", "0,79"],
];
const Zettel: React.FC<{ width: number; fs: number; rows?: number; ring?: number; sumScale?: number }> = ({ width, fs, rows = 16, ring = 1, sumScale = 1 }) => (
  <div style={{ width, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, overflow: "hidden", boxShadow: "0 10px 0 rgba(58,38,24,.12)" }}>
    <ClaudeHead size={fs * 1.05} right={<span style={{ fontSize: fs * 0.85, color: MUTED }}>Aldi-Zettel</span>} />
    <div style={{ padding: `${fs * 0.35}px ${fs * 0.6}px 0`, columnCount: 2, columnGap: fs }}>
      {ZETTEL.map(([a, p], i) => (
        <div key={i} style={{ display: "flex", justifyContent: "space-between", fontSize: fs * 0.72, fontWeight: 600, lineHeight: 1.42, whiteSpace: "nowrap", opacity: i < rows ? 1 : 0, breakInside: "avoid" }}>
          <span>{a}</span><span style={{ color: MUTED }}>{p}</span>
        </div>
      ))}
    </div>
    <div style={{ position: "relative", margin: `${fs * 0.3}px auto ${fs * 0.5}px`, width: "fit-content", fontSize: fs * 1.6 * sumScale, fontWeight: 700, color: INK, padding: "0 20px" }}>
      Summe <span style={{ color: GREEN }}>18,36 €</span>
      <svg viewBox="0 0 200 60" preserveAspectRatio="none" style={{ position: "absolute", left: -14, top: -8, width: "112%", height: "130%" }}>
        <ellipse cx={100} cy={30} rx={96} ry={26} fill="none" stroke={GREEN} strokeWidth={3.2} strokeDasharray={460} strokeDashoffset={460 * (1 - ring)} strokeLinecap="round" />
      </svg>
    </div>
  </div>
);

// Brotdose (eigene Zeichnung)
const Dose: React.FC<{ tag: string; label?: string; w?: number; color?: string }> = ({ tag, label, w = 170, color = "#9BD3B5" }) => (
  <div style={{ width: w, height: w * 0.52, background: color, border: `5px solid ${INK}`, borderRadius: 16, position: "relative", display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
    <div style={{ position: "absolute", top: -12, left: 14, right: 14, height: 14, background: "#F3EBDD", border: `4px solid ${INK}`, borderRadius: 8 }} />
    <div style={{ fontSize: w * 0.2, fontWeight: 700, lineHeight: 1 }}>{tag}</div>
    {label && <div style={{ fontSize: w * 0.13, fontWeight: 600, lineHeight: 1.1, marginTop: 4 }}>{label}</div>}
  </div>
);

const Schein: React.FC<{ size?: number; rot?: number }> = ({ size = 1, rot = 0 }) => (
  <div style={{ width: 160 * size, height: 84 * size, background: "#B9D8E8", border: `5px solid ${INK}`, borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 46 * size, fontWeight: 700, color: NAVY, rotate: `${rot}deg` }}>20 €</div>
);

const DOSEN_FARBEN = ["#F2B48F", "#F5D27A", "#9BD3B5", "#B9C7EE", "#F2A7A7"];

// ---------- 1 Hook: Ergebnis ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { frame } = useT();
  const wobble = Math.sin(frame / 6) * 3;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 14, textAlign: "center" }}>
        <div style={{ fontSize: 30, fontWeight: 700, letterSpacing: 6, color: MUTED }}>HAMSTER-TEST</div>
        <div style={{ fontSize: 64, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>Meal Prep: <span style={{ color: GREEN }}>5 Essen, 20 €</span></div>
      </div>
      {/* Turm aus 5 Brotdosen auf der Zeigestab-Spitze (~440, 930) */}
      <div style={{ position: "absolute", left: 300, top: 470, width: 230, display: "flex", flexDirection: "column-reverse", alignItems: "center", gap: 6, rotate: `${wobble}deg`, transformOrigin: "50% 100%", height: 460 }}>
        {["Mo", "Di", "Mi", "Do", "Fr"].map((d, i) => (
          <div key={d} style={{ translate: `${(i % 2 ? 1 : -1) * i * 4}px 0px` }}><Dose tag={d} w={160} color={DOSEN_FARBEN[i]} /></div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 230, top: 420, rotate: "-12deg" }}><Schein size={0.8} /></div>
      {/* Claudes Zettel rechts, Summe groß */}
      <div style={{ position: "absolute", right: 14, top: 170, rotate: "2deg" }}>
        <Zettel width={430} fs={30} sumScale={1.1} />
      </div>
    </div>
  );
};

// ---------- 2 Zettel groß, Summe ----------
export const SceneZettel: React.FC<{ summe: number }> = ({ summe }) => {
  const { t, fps } = useT();
  const rows = Math.min(16, Math.floor(interpolate(t, [0.05, 1.1], [1, 16.99], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const ring = interpolate(t, [summe, summe + 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 30, right: 30, top: 24, background: "#F1E6D3", borderRadius: "26px 26px 6px 26px", padding: "12px 20px", fontSize: 34, fontWeight: 600, opacity: fade(t, 0) }}>
        „20 € · 5 Mittagessen · Einkaufszettel für Aldi“
      </div>
      <div style={{ position: "absolute", left: 40, top: 130, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <Zettel width={868} fs={44} rows={rows} ring={ring} sumScale={1 + 0.15 * ring} />
      </div>
      <Pop at={summe + 0.5} style={{ position: "absolute", right: 50, top: 860 }}>
        <div style={{ background: "#DDF1E6", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "6px 24px", fontSize: 50, fontWeight: 700, color: "#1C7049" }}>16 Sachen ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 3 Trick: Reste weiterverkochen ----------
export const SceneTrick: React.FC<{ reste: number; chili: number; nudeln: number }> = ({ reste, chili, nudeln }) => {
  const { t, fps } = useT();
  const Arrow: React.FC<{ at: number }> = ({ at }) => (
    <div style={{ fontSize: 90, fontWeight: 700, color: GREEN, opacity: fade(t, at), translate: `${(1 - sp(t, at, fps)) * -40}px 0px` }}>→</div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Pop at={reste} style={{ position: "absolute", left: 0, right: 0, top: 30, display: "flex", justifyContent: "center" }}>
        <div style={{ fontSize: 76, fontWeight: 700 }}>Der Trick: <span style={{ background: MARK, padding: "0 14px", borderRadius: 12 }}>Reste</span></div>
      </Pop>
      <div style={{ position: "absolute", left: 60, top: 200, display: "flex", alignItems: "center", gap: 26, opacity: fade(t, 0, 0.2) }}>
        <Dose tag="Mo" label="Chili" w={300} color={DOSEN_FARBEN[0]} />
        <Arrow at={chili} />
        <div style={{ opacity: fade(t, chili + 0.2), scale: S(sp(t, chili + 0.2, fps)) }}><Dose tag="Di" label="Burrito" w={300} color={DOSEN_FARBEN[1]} /></div>
      </div>
      <div style={{ position: "absolute", left: 60, top: 470, display: "flex", alignItems: "center", gap: 26, opacity: fade(t, 0.15, 0.2) }}>
        <Dose tag="Do" label="Nudelsalat" w={300} color={DOSEN_FARBEN[3]} />
        <Arrow at={nudeln} />
        <div style={{ opacity: fade(t, nudeln + 0.2), scale: S(sp(t, nudeln + 0.2, fps)) }}><Dose tag="Fr" label="Frittata" w={300} color={DOSEN_FARBEN[4]} /></div>
      </div>
      <div style={{ position: "absolute", right: 60, top: 740, opacity: fade(t, nudeln + 0.8) }}>
        <Dose tag="Mi" label="Linsen-Curry" w={220} color={DOSEN_FARBEN[2]} />
      </div>
    </div>
  );
};

// ---------- 4 Nachgeprüft ----------
export const ScenePruefen: React.FC<{ aldi: number }> = ({ aldi }) => {
  const { t, fps } = useT();
  const k = sp(t, 0, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 40, textAlign: "center", fontSize: 78, fontWeight: 700 }}>Stimmen die Preise?</div>
      <div style={{ position: "absolute", left: 90, top: 210, rotate: "-3deg", opacity: 0.55 }}>
        <Zettel width={470} fs={28} />
      </div>
      {/* Lupe */}
      <svg viewBox="0 0 200 200" style={{ position: "absolute", left: 340, top: 300, width: 360, height: 360, scale: S(k) }}>
        <circle cx={80} cy={80} r={60} fill="rgba(255,255,255,.55)" stroke={INK} strokeWidth={12} />
        <line x1={125} y1={125} x2={185} y2={185} stroke={INK} strokeWidth={22} strokeLinecap="round" />
      </svg>
      <Pop at={aldi} style={{ position: "absolute", left: 420, top: 660 }}>
        <div style={{ background: PAPER, border: `6px solid ${NAVY}`, borderRadius: 22, padding: "12px 26px", fontSize: 44, fontWeight: 700, color: NAVY, lineHeight: 1.2, rotate: "2deg" }}>
          Nachgeprüft<br /><span style={{ color: INK }}>aldi-sued.de</span><br /><span style={{ fontSize: 34, color: MUTED }}>15.11.2026</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 5 Elf Preise: +0,50 € ----------
const VERGL: [string, string, string][] = [
  ["Reis", "1,39", "1,39"], ["Nudeln", "0,99", "0,69"], ["Linsen", "1,49", "1,29"], ["Kidneyb.", "0,75", "0,69"],
  ["Mais", "0,79", "0,89"], ["Tomaten", "0,65", "0,65"], ["Kokosm.", "1,19", "1,19"], ["Eier", "1,69", "2,29"],
  ["Wraps", "1,39", "1,59"], ["Feta", "1,39", "1,59"], ["Paprikap.", "0,79", "0,75"],
];
export const SceneElf: React.FC<{ summe: number }> = ({ summe }) => {
  const { t } = useT();
  const rows = Math.min(11, Math.floor(interpolate(t, [0.05, 1.3], [1, 11.99], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 20, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "10px 26px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr 1fr 0.7fr", fontSize: 34, fontWeight: 700, color: MUTED, borderBottom: `3px solid #E7D9C2` }}>
          <span>11 Preise</span><span>Claude</span><span>echt</span><span />
        </div>
        {VERGL.map(([a, c, e], i) => {
          const diff = c !== e;
          return (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr 1fr 0.7fr", fontSize: 38, fontWeight: 600, lineHeight: 1.32, opacity: i < rows ? 1 : 0, background: a === "Eier" ? MARK : "transparent", borderRadius: 8 }}>
              <span>{a}</span><span style={{ color: MUTED }}>{c}</span><span style={{ color: diff ? NAVY : INK, fontWeight: 700 }}>{e}</span><span style={{ color: diff ? NAVY : GREEN, fontSize: diff ? 28 : 38 }}>{diff ? (parseFloat(e.replace(",", ".")) - parseFloat(c.replace(",", ".")) > 0 ? "+" : "−") + Math.abs(parseFloat(e.replace(",", ".")) - parseFloat(c.replace(",", "."))).toFixed(2).replace(".", ",") : "="}</span>
            </div>
          );
        })}
      </div>
      <Pop at={summe} style={{ position: "absolute", left: 300, right: 30, top: 830 }}>
        <div style={{ background: "#DDF1E6", border: `6px solid ${GREEN}`, borderRadius: 22, padding: "6px 20px", fontSize: 48, fontWeight: 700, color: "#1C7049", textAlign: "center" }}>zusammen nur +0,50 €</div>
      </Pop>
    </div>
  );
};

// ---------- 6 Haken: Eier ----------
export const SceneEier: React.FC<{ echt: number; claude: number }> = ({ echt, claude }) => {
  const { t, fps } = useT();
  const strike = interpolate(t, [claude, claude + 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 76, fontWeight: 700 }}>Der Haken: <span style={{ color: RED }}>Eier</span></div>
      {/* Eierkarton */}
      <svg viewBox="0 0 400 200" style={{ position: "absolute", left: 174, top: 160, width: 600, height: 300, scale: S(sp(t, 0, fps)) }}>
                {[0, 1, 2, 3, 4, 5].map((i) => (
          <ellipse key={i} cx={75 + (i % 3) * 125} cy={i > 2 ? 135 : 95} rx={42} ry={50} fill="#FFF3DD" stroke={INK} strokeWidth={5} />
        ))}
        <rect x={10} y={120} width={380} height={70} rx={14} fill="#D9C3A2" stroke={INK} strokeWidth={6} />
      </svg>
      <div style={{ position: "absolute", left: 80, top: 520, fontSize: 70, fontWeight: 700, color: MUTED, opacity: fade(t, 0.2) }}>
        <span style={{ position: "relative" }}>Claude 1,69 €
          <div style={{ position: "absolute", left: -6, top: "50%", height: 8, width: `${strike * 104}%`, background: RED, borderRadius: 4 }} />
        </span>
      </div>
      <Pop at={echt} style={{ position: "absolute", left: 80, top: 640 }}>
        <div style={{ fontSize: 96, fontWeight: 700, color: RED }}>echt 2,29 €</div>
      </Pop>
      <Pop at={claude + 0.6} style={{ position: "absolute", right: 50, top: 820 }}>
        <div style={{ border: `7px solid ${RED}`, color: RED, borderRadius: 18, padding: "0 22px", fontSize: 64, fontWeight: 700, rotate: "-6deg", background: "rgba(255,255,255,.9)" }}>+36 %</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Gemüse: nicht online ----------
const GEMUESE: [string, string][] = [["🫑", "Paprika"], ["🧅", "Zwiebeln"], ["🥕", "Möhren"], ["🥒", "Gurke"], ["🍛", "Curry"]];
export const SceneGemuese: React.FC<{ geschaetzt: number }> = ({ geschaetzt }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 66, fontWeight: 700 }}>Nicht online <span style={{ color: MUTED }}>❓</span></div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 170, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 26 }}>
        {GEMUESE.map(([e, n], i) => (
          <div key={n} style={{ width: 260, height: 230, background: PAPER, border: `5px dashed ${MUTED}`, borderRadius: 22, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", scale: S(sp(t, i * 0.12, fps)) }}>
            <div style={{ fontSize: 100 }}>{e}</div>
            <div style={{ fontSize: 40, fontWeight: 700 }}>{n} <span style={{ color: MUTED }}>?</span></div>
          </div>
        ))}
      </div>
      <Pop at={geschaetzt} style={{ position: "absolute", left: 400, top: 800 }}>
        <div style={{ background: MARK, border: `6px solid ${INK}`, borderRadius: 22, padding: "6px 24px", fontSize: 54, fontWeight: 700 }}>bleibt geschätzt</div>
      </Pop>
    </div>
  );
};

// ---------- 8 Urteil: GEKLAPPT ----------
export const SceneUrteil: React.FC<{ stempel: number; summe: number; reis: number }> = ({ stempel, summe, reis }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: "#1C7049", borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 30, top: 420, display: "flex", flexDirection: "column", gap: 14, fontSize: 60, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, summe) }}>≈ 18,86 € <span style={{ color: GREEN }}>&lt; 20 €</span></div>
        <div style={{ opacity: fade(t, summe + 0.3), fontSize: 52, color: NAVY }}>5 Preise geschätzt</div>
        <div style={{ opacity: fade(t, reis) }}>+ Reis übrig 🍚</div>
      </div>
    </div>
  );
};

// ---------- 9 Ende: Handy + Kommentar ZETTEL ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>🧾</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Einkaufs-<br />zettel<br />+ 5 Rezepte</div>
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
          <div style={{ fontSize: 88, fontWeight: 600, color: INK, letterSpacing: 4 }}>ZETTEL</div>
        </div>
      </Pop>
    </div>
  );
};
