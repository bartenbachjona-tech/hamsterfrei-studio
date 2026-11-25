import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge14 · Vorher/Nachher „Winterjacken-Anzeige“ · Serie (b) · Einstiegs-Test E1 (Paar 2) · ohne Werbung · Leinwand 948×1004
// Emma + Jacke vom Studio erfunden (docs/plaene/beispiel/jacke_beispiel.txt).
// Nachher = wörtliche Claude-Antwort (docs/plaene/beispiel/jacke_claude_antwort.md), gekürzt nur durch Weglassen.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LRED = "#F9DEDA";
const LGREEN = "#CDEBD9";
const GREY = "#9AA0A8";
const HAND = "'Comic Sans MS', 'Fredoka', cursive";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));
const S = (v: number) => String(Math.max(0.0001, v));

const Stempel: React.FC<{ size?: number; rot?: number; text?: string; color?: string }> = ({ size = 34, rot = -8, text = "BEISPIEL", color = RED }) => (
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.92)", whiteSpace: "nowrap" }}>{text}</div>
);

const ClaudeHead: React.FC<{ size?: number; title?: string }> = ({ size = 32, title = "Claude" }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    {title}
  </div>
);

// Gezeichnete schwarze Winterjacke mit Kapuze + Fellrand, optional heller Fleck am rechten Ärmel
const Jacke: React.FC<{ w: number; fleck?: number; grau?: boolean }> = ({ w, fleck = 0, grau = false }) => {
  const body = grau ? "#5B5F66" : "#22242A";
  return (
    <svg width={w} height={w} viewBox="0 0 100 100">
      <path d="M30 26 Q50 6 70 26 L72 34 Q50 24 28 34 Z" fill={grau ? "#8A8278" : "#B9A58C"} />
      <path d="M28 32 Q50 22 72 32 L86 52 L84 88 L74 88 L72 58 L70 92 L30 92 L28 58 L26 88 L16 88 L14 52 Z" fill={body} />
      <path d="M50 30 L50 92" stroke="#7D838C" strokeWidth={1.6} />
      <circle cx={50} cy={20} r={0} />
      {fleck > 0 && <ellipse cx={79} cy={83} rx={3.6 * fleck} ry={2.6 * fleck} fill="#E9E2D2" />}
    </svg>
  );
};

// ---------- Anzeigen-Karten ----------
const Vorher: React.FC<{ w: number; fs: number }> = ({ w, fs }) => (
  <div style={{ width: w, background: "#ECEDEF", border: `4px solid ${GREY}`, borderRadius: 18, padding: fs * 0.5, color: "#555A61" }}>
    <div style={{ background: "#D8DADE", borderRadius: 12, display: "flex", justifyContent: "center", padding: fs * 0.3 }}><Jacke w={w * 0.55} grau /></div>
    <div style={{ fontSize: fs * 1.15, fontWeight: 700, marginTop: fs * 0.4, color: "#3E434A" }}>Winterjacke</div>
    <div style={{ fontSize: fs, marginTop: fs * 0.25 }}>Jacke, gut erhalten, VB</div>
  </div>
);

const Nachher: React.FC<{ w: number; fs: number; hlTitel?: number[]; hlMangel?: number; hlPreis?: number; waschen?: number; kompakt?: boolean }> = ({ w, fs, hlTitel = [0, 0, 0, 0], hlMangel = 0, hlPreis = 0, waschen = 0, kompakt = false }) => {
  const mk = (txt: string, v: number) => (
    <span style={{ background: v > 0 ? `rgba(205,235,217,${v})` : "transparent", color: v > 0.5 ? DGREEN : "inherit", borderRadius: 6, padding: "0 3px" }}>{txt}</span>
  );
  return (
    <div style={{ width: w, background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: fs * 0.45, boxShadow: "6px 8px 0 rgba(58,38,24,.14)", color: "#1E2430" }}>
      <div style={{ fontSize: fs * 1.12, fontWeight: 700, lineHeight: 1.15 }}>
        {mk("Schwarze", hlTitel[0])} {mk("Damen", hlTitel[1])}-Winterjacke {mk("Gr. M", hlTitel[2])} mit {mk("Kapuze", hlTitel[3])} und abnehmbarem Kunstfell
      </div>
      {!kompakt && <div style={{ fontSize: fs * 0.62, color: "#4B5260", lineHeight: 1.3, marginTop: fs * 0.25 }}>
        Kapuze mit Kunstfellrand, abnehmbar · Innen warm gefüttert · Reißverschluss funktioniert · Zwei Winter getragen
      </div>}
      {kompakt && <div style={{ fontSize: fs * 0.78, color: "#4B5260", marginTop: fs * 0.2, fontWeight: 600 }}>warm gefüttert · 2 Winter getragen</div>}
      <div style={{ marginTop: fs * 0.3, fontSize: fs * 0.86, fontWeight: 600, lineHeight: 1.25, background: hlMangel > 0 ? `rgba(255,240,194,${hlMangel})` : "transparent", border: `${hlMangel > 0 ? 4 : 0}px solid ${GREEN}`, borderRadius: 10, padding: hlMangel > 0 ? "2px 8px" : 0 }}>
        <b style={{ color: RED }}>Mangel:</b> kleiner heller Fleck am rechten Ärmel, der {waschen > 0 ? <span style={{ background: `rgba(249,222,218,${waschen})`, color: waschen > 0.5 ? RED : "inherit", textDecoration: waschen > 0.5 ? "line-through" : "none", textDecorationThickness: 4, borderRadius: 6, padding: "0 3px" }}>beim Waschen</span> : "beim Waschen"} nicht rausgeht (siehe Foto)
      </div>
      {!kompakt && <div style={{ fontSize: fs * 0.58, color: "#4B5260", marginTop: fs * 0.2 }}>Abholung in Würzburg oder Versand. Wer sich schnell meldet, hat gute Chancen.</div>}
      <div style={{ marginTop: fs * 0.25, fontSize: fs * 1.05, fontWeight: 700, display: "inline-block", background: hlPreis > 0 ? `rgba(205,235,217,${hlPreis})` : "transparent", borderRadius: 10, padding: "0 8px" }}>
        Preis: <span style={{ color: NAVY }}>___ € VB</span>
      </div>
    </div>
  );
};

// ---------- 0 Hook (E1): Split Vorher/Nachher ab Frame 0 ----------
export const SceneHook: React.FC<{ fast: number; links: number; rechts: number }> = ({ fast, links, rechts }) => {
  const { t } = useT();
  const q = fade(t, fast, 0.2);
  const L = t >= links && t < rechts ? fade(t, links, 0.15) : 0;
  const R = fade(t, rechts, 0.15);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 12, textAlign: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 700, letterSpacing: 4, color: MUTED }}>VORHER / NACHHER</div>
        <div style={{ fontSize: 72, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>Eine Zeile <span style={{ color: GREEN }}>vs. Claude</span></div>
      </div>
      <div style={{ position: "absolute", left: 22, top: 200, rotate: "-2deg" }}>
        <div style={{ fontSize: 34, fontWeight: 700, color: GREY, marginBottom: 6 }}>VORHER</div>
        <div style={{ outline: L ? `8px solid ${RED}` : "none", outlineOffset: 6, borderRadius: 20 }}><Vorher w={300} fs={34} /></div>
      </div>
      <div style={{ position: "absolute", left: 345, top: 150, rotate: "1deg" }}>
        <div style={{ fontSize: 34, fontWeight: 700, color: GREEN, marginBottom: 6 }}>NACHHER · Claude</div>
        <div style={{ outline: R ? `8px solid ${GREEN}` : "none", outlineOffset: 6, borderRadius: 20 }}><Nachher w={570} fs={43} kompakt /></div>
        <div style={{ position: "absolute", right: -6, top: -12 }}><Stempel size={22} text="BEISPIEL" rot={4} /></div>
      </div>
      <div style={{ position: "absolute", left: 590, top: 445, opacity: q, scale: S(0.6 + 0.4 * q), fontSize: 110, fontWeight: 700, color: RED }}>?</div>
    </div>
  );
};

// ---------- 1 Titel ----------
export const SceneTitel: React.FC<{ a: number[] }> = ({ a }) => {
  const { t, fps } = useT();
  const v = a.map((x) => fade(t, x, 0.2));
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 60, fontWeight: 700, color: NAVY }}>1 · Titel</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 140, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: "24px 30px", fontSize: 74, fontWeight: 700, lineHeight: 1.18, color: "#1E2430" }}>
          {["Schwarze", "Damen-", "Winterjacke", "Gr. M", "mit", "Kapuze"].map((w, i) => {
            const idx = [0, 1, -1, 2, -1, 3][i];
            const on = idx >= 0 ? v[idx] : 0;
            return <span key={w} style={{ background: on ? `rgba(205,235,217,${on})` : "transparent", color: on > 0.5 ? DGREEN : "inherit", borderRadius: 10, padding: "0 6px", marginRight: 10 }}>{w}</span>;
          })}
          <span style={{ color: "#8A8F98", fontSize: 52 }}> und abnehmbarem Kunstfell</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 420, top: 640, display: "flex", alignItems: "center", gap: 18, opacity: fade(t, a[3] + 0.6), background: PAPER, border: `4px solid ${GREY}`, borderRadius: 40, padding: "12px 26px", fontSize: 44, color: "#4B5260" }}>
        🔍 <span>damen winterjacke m</span>
      </div>
    </div>
  );
};

// ---------- 2 Fleck als Mangel ----------
export const SceneFleck: React.FC<{ mangel: number }> = ({ mangel }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 60, fontWeight: 700, color: NAVY }}>2 · Der Fleck</div>
      <div style={{ position: "absolute", left: 40, top: 120, scale: S(sp(t, 0, fps)) }}>
        <div style={{ background: "#ECEDEF", borderRadius: 24, border: `5px solid ${INK}`, padding: 10 }}><Jacke w={360} fleck={1.3} /></div>
        <div style={{ position: "absolute", left: 255, top: 255, width: 110, height: 110, borderRadius: 60, border: `11px solid ${RED}` }} />
      </div>
      <div style={{ position: "absolute", left: 440, top: 150, right: 30, opacity: fade(t, 0.3), fontFamily: HAND, fontSize: 52, fontWeight: 700, color: "#2E3F8F", lineHeight: 1.25 }}>
        Emmas Notiz:<br />„am rechten ärmel unten kleiner heller fleck geht nicht raus“
      </div>
      <Pop at={mangel} style={{ position: "absolute", left: 40, right: 40, top: 560 }}>
        <div style={{ background: "#FFF0C2", border: `6px solid ${GREEN}`, borderRadius: 20, padding: "16px 24px", fontSize: 50, fontWeight: 700, lineHeight: 1.25 }}>
          <span style={{ color: RED }}>Mangel:</span> kleiner heller Fleck am rechten Ärmel <span style={{ color: GREEN }}>✓ ehrlich drin</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 3 Preis: Lücke + Rückfrage ----------
export const ScenePreis: React.FC<{ frage: number }> = ({ frage }) => {
  const { t, fps } = useT();
  const blink = Math.floor(t * 2.5) % 2 === 0 ? 1 : 0.35;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 60, fontWeight: 700, color: NAVY }}>3 · Der Preis</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 150, display: "flex", justifyContent: "center", scale: S(sp(t, 0, fps)) }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "20px 50px", fontSize: 120, fontWeight: 700, color: "#1E2430" }}>
          <span style={{ opacity: blink, color: NAVY }}>___</span> € VB
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center", fontSize: 54, fontWeight: 700, color: GREEN, opacity: fade(t, 1.3) }}>kein Preis geraten</div>
      <Pop at={frage} style={{ position: "absolute", left: 300, right: 24, top: 480 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={30} />
          <div style={{ padding: "14px 22px 18px", fontSize: 52, fontWeight: 600, lineHeight: 1.2 }}>„Wie viel willst du haben?“</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 4 Haken: „beim Waschen“ erfunden ----------
export const SceneErfunden: React.FC<{ waschen: number; notiz: number }> = ({ waschen, notiz }) => {
  const { t, fps } = useT();
  const w = fade(t, waschen, 0.2);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 58, fontWeight: 700, color: RED }}>Aber: 2 Wörter erfunden</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={30} title="Claude · Anzeige" />
          <div style={{ padding: "16px 24px 20px", fontSize: 54, fontWeight: 600, lineHeight: 1.3 }}>
            „… kleiner heller Fleck, der{" "}
            <span style={{ background: `rgba(249,222,218,${w})`, color: w > 0.5 ? RED : INK, border: `${w > 0.5 ? 5 : 0}px solid ${RED}`, borderRadius: 10, padding: "0 6px", fontWeight: 700 }}>beim Waschen</span>{" "}
            nicht rausgeht (siehe Foto)“
          </div>
        </div>
      </div>
      <Pop at={notiz} style={{ position: "absolute", left: 330, right: 30, top: 560 }}>
        <div style={{ background: "#FFFDF5", border: `4px solid ${INK}`, borderRadius: 16, padding: "14px 22px", fontFamily: HAND, color: "#2E3F8F", fontSize: 44, lineHeight: 1.3, rotate: "-1.5deg" }}>
          Emmas Notiz: „…fleck geht nicht raus“<br />
          <span style={{ fontFamily: "Fredoka", fontWeight: 700, color: RED }}>Waschen? ✗ stand nirgends</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 5 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  const z: [string, boolean][] = [["Titel mit Suchwörtern", true], ["Fleck ehrlich drin", true], ["Preis nicht geraten", true], ["„beim Waschen“ erfunden", false]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 118, fontWeight: 700, letterSpacing: 4, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)", whiteSpace: "nowrap" }}>VIEL BESSER</div>
      </div>
      <div style={{ position: "absolute", left: 250, right: 10, top: 410, display: "flex", flexDirection: "column", gap: 20, fontSize: 52, whiteSpace: "nowrap", fontWeight: 700 }}>
        {z.map(([txt, ok], i) => (
          <div key={txt} style={{ opacity: fade(t, zeilen + i * 0.22), color: ok ? INK : RED, background: ok ? "transparent" : LRED, borderRadius: 12, padding: "0 8px" }}>{txt} <span style={{ color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span></div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 250, right: 10, top: 760, fontSize: 46, fontWeight: 700, color: NAVY, opacity: fade(t, zeilen + 1.4) }}>→ jeden Satz gegenlesen</div>
    </div>
  );
};

// ---------- 6 Ende: Handy + Kommentar JACKE ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <Jacke w={170} />
          <div style={{ fontSize: 58, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Die Frage<br />zum<br />Kopieren</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 270, top: 850 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>JACKE</div>
        </div>
      </Pop>
    </div>
  );
};

export { LGREEN };
