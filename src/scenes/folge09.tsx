import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge09 · Hamster-Test „Aushang fürs Schneeschippen“ · Hook-Test Variante A (Paar 4) · ohne Werbung · Leinwand 948×1004
// Vorher-Zettel + Person vom Studio erfunden (docs/plaene/beispiel/aushang_beispiel.txt), Nummer = Platzhalter.
// Claude-Antwort echt (docs/plaene/beispiel/aushang_claude_antwort.md). Zeiten in Props = Sekunden ab Szenenstart.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster. Zeigestab-Spitze ≈ (440, 930).
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LGREEN = "#DDF1E6";
const ORANGE = "#D9772B";
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
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.88)", whiteSpace: "nowrap" }}>{text}</div>
);

const ClaudeHead: React.FC<{ size?: number }> = ({ size = 32 }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    Claude
  </div>
);

// Vorher: krakeliger Zettel
const AltZettel: React.FC<{ fs: number; ring?: number }> = ({ fs, ring = 0 }) => (
  <div style={{ position: "relative", background: "#FBFBF4", border: `3px solid #B9B2A3`, padding: `${fs * 0.6}px ${fs * 0.6}px`, boxShadow: "4px 6px 0 rgba(58,38,24,.12)", fontFamily: HAND, color: "#3B4A8C", lineHeight: 1.25, backgroundImage: "repeating-linear-gradient(transparent 0 38px, #DCE6F2 38px 40px)" }}>
    <div style={{ position: "relative", fontSize: fs, rotate: "-2deg", whiteSpace: "nowrap" }}>
      Mache Gartenarbeit
      <br />und so.
      {ring > 0 && (
        <svg viewBox="0 0 200 80" preserveAspectRatio="none" style={{ position: "absolute", left: -18, top: -10, width: "115%", height: "125%" }}>
          <ellipse cx={100} cy={40} rx={96} ry={36} fill="none" stroke={RED} strokeWidth={4} strokeDasharray={480} strokeDashoffset={480 * (1 - ring)} strokeLinecap="round" />
        </svg>
      )}
    </div>
    <div style={{ fontSize: fs * 0.8, marginTop: fs * 0.3, rotate: "1deg", whiteSpace: "nowrap" }}>Bei Interesse melden!!!</div>
    <div style={{ fontSize: fs * 0.62, marginTop: fs * 0.3, whiteSpace: "nowrap" }}>Tel. 0123 456789 (Leonie)</div>
  </div>
);

// Nachher: Claudes Aushang (gekürzt, Inhalte aus der echten Antwort)
const Aushang: React.FC<{ width: number; fs: number; hl?: [number, number, number]; torn?: number; strips?: boolean }> = ({ width, fs, hl = [0, 0, 0], torn = 0, strips = true }) => {
  const H = (v: number): React.CSSProperties => ({ background: `rgba(255,224,138,${v})`, borderRadius: 10, padding: "0 8px", margin: "0 -8px", boxShadow: v > 0 ? `0 0 0 ${4 * v}px rgba(200,71,58,${v})` : "none" });
  return (
    <div style={{ width, background: PAPER, border: `5px solid ${INK}`, borderRadius: 8, boxShadow: "6px 8px 0 rgba(58,38,24,.14)", position: "relative" }}>
      <div style={{ padding: `${fs * 0.4}px ${fs * 0.5}px ${fs * 0.3}px`, textAlign: "center" }}>
        <div style={{ display: "inline-block", fontSize: fs * 1.9, fontWeight: 700, lineHeight: 1.0, color: INK, ...H(hl[0]) }}>
          <span style={{ color: ORANGE }}>LAUB</span> & <span style={{ color: NAVY }}>SCHNEE?</span>
        </div>
        <div style={{ fontSize: fs * 0.9, fontWeight: 600, marginTop: fs * 0.15 }}>Ich mach das für Sie!</div>
        <div style={{ fontSize: fs * 0.62, fontWeight: 600, color: MUTED, marginTop: fs * 0.2, lineHeight: 1.25 }}>Leonie, 15, wohne selbst im Lerchenfeld · Rechen & Schaufel bring ich mit</div>
        <div style={{ fontSize: fs * 0.62, fontWeight: 600, color: MUTED, lineHeight: 1.25 }}>nachmittags + samstags</div>
        <div style={{ display: "inline-block", fontSize: fs * 1.05, fontWeight: 700, color: DGREEN, marginTop: fs * 0.2, ...H(hl[1]) }}>10 € pro Stunde</div>
        <div style={{ fontSize: fs * 0.95, fontWeight: 700, color: INK, marginTop: fs * 0.1 }}>0123 456789</div>
      </div>
      {strips && (
        <div style={{ display: "flex", borderTop: `3px dashed ${INK}`, ...(hl[2] > 0 ? { boxShadow: `0 0 0 ${6 * hl[2]}px rgba(255,224,138,${hl[2]})` } : {}) }}>
          {Array.from({ length: 8 }).map((_, i) => {
            const isTorn = i === 0 && torn > 0;
            return (
              <div key={i} style={{ flex: 1, height: fs * 2.6, borderRight: i < 7 ? `2px solid ${INK}` : "none", position: "relative" }}>
                <div style={{ position: "absolute", inset: 0, background: PAPER, transformOrigin: "top center", rotate: isTorn ? `${torn * 24}deg` : "0deg", translate: isTorn ? `${-torn * 14}px ${torn * 10}px` : "0 0", border: isTorn ? `2px solid ${INK}` : "none", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <div style={{ writingMode: "vertical-rl", rotate: "180deg", fontSize: fs * 0.42, fontWeight: 700, whiteSpace: "nowrap", color: INK }}>0123 456789</div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

// ---------- 1 Hook: vorher/nachher ab Frame 0 ----------
export const SceneHook: React.FC<{ ringAt: number }> = ({ ringAt }) => {
  const { t, frame } = useT();
  const wob = Math.sin(frame / 6) * 0.08;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 14, textAlign: "center" }}>
        <div style={{ fontSize: 30, fontWeight: 700, letterSpacing: 6, color: MUTED }}>HAMSTER-TEST</div>
        <div style={{ fontSize: 66, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>Nebenjob mit 15: <span style={{ color: GREEN }}>Aushang</span></div>
      </div>
      <div style={{ position: "absolute", left: 18, top: 190, rotate: "-5deg", width: 360 }}>
        <div style={{ marginBottom: 8 }}><Stempel size={30} text="VORHER" /></div>
        <AltZettel fs={36} ring={lin(t, ringAt, 0.5)} />
      </div>
      <div style={{ position: "absolute", left: 250, top: 560, fontSize: 110, fontWeight: 700, color: GREEN, rotate: "30deg" }}>➜</div>
      <div style={{ position: "absolute", left: 398, top: 352, rotate: "2deg" }}>
        <div style={{ position: "absolute", right: 10, top: -34, zIndex: 2 }}><Stempel size={30} text="NACHHER · CLAUDE" rot={5} color={GREEN} /></div>
        <div style={{ position: "absolute", right: 14, bottom: -40, zIndex: 2 }}><Stempel size={20} text="BEISPIEL" rot={-3} /></div>
        <Aushang width={530} fs={40} torn={interpolate(t, [0.3, 1.1], [0.8, 1.9], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) + wob} />
      </div>
    </div>
  );
};

// ---------- 2 Leonie fragt, Claude fragt 8 Sachen zurück ----------
export const SceneFragen: React.FC<{ claudeAt: number }> = ({ claudeAt }) => {
  const { t, fps } = useT();
  const chips = ["Was?", "Wo?", "Wann?", "Preis?"];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26 }}><Stempel size={30} text="BEISPIEL" rot={-4} /></div>
      <div style={{ position: "absolute", left: 230, right: 30, top: 30, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "14px 22px", fontSize: 36, fontWeight: 600, lineHeight: 1.2 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 4 }}>Hamster an Claude, für Leonie (15):</div>
          „Kannst du ihren Zettel besser machen? Frag erst, was du wissen musst.“
        </div>
      </div>
      <Pop at={claudeAt} style={{ position: "absolute", left: 30, right: 40, top: 300 }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden" }}>
          <ClaudeHead size={32} />
          <div style={{ padding: "16px 26px 24px" }}>
            <div style={{ fontSize: 50, fontWeight: 700, color: NAVY }}>Erst 8 Fragen:</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginTop: 14 }}>
              {chips.map((c, i) => (
                <Pop key={c} at={claudeAt + 0.25 + i * 0.18}>
                  <div style={{ background: LGREEN, border: `5px solid ${GREEN}`, borderRadius: 30, padding: "6px 22px", fontSize: 50, fontWeight: 700, color: DGREEN }}>{c}</div>
                </Pop>
              ))}
              <Pop at={claudeAt + 1.0}>
                <div style={{ fontSize: 44, fontWeight: 700, color: MUTED, padding: "10px 6px" }}>+ 4 mehr</div>
              </Pop>
            </div>
          </div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 3 Der fertige Zettel ----------
export const SceneZettel: React.FC<{ a: number; b: number; c: number }> = ({ a, b, c }) => {
  const { t, fps } = useT();
  const k = (x: number) => (t >= x ? Math.min(1, (t - x) / 0.25) : 0);
  const cur = t >= c ? [0, 0, k(c)] : t >= b ? [0, k(b), 0] : [k(a), 0, 0];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 46, fontWeight: 700, color: MUTED }}>Claudes Zettel</div>
      <div style={{ position: "absolute", left: 130, top: 100, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <Aushang width={760} fs={52} hl={cur as [number, number, number]} />
      </div>
    </div>
  );
};

// ---------- 4 Claude streicht „morgens vor der Schule“ ----------
export const SceneStreicht: React.FC<{ strikeAt: number }> = ({ strikeAt }) => {
  const { t, fps } = useT();
  const st = lin(t, strikeAt, 0.4);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 50, fontWeight: 700, color: MUTED }}>Aber …</div>
      <div style={{ position: "absolute", left: 120, right: 30, top: 120, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "16px 24px", fontSize: 44, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 4 }}>Leonies Zeiten:</div>
          „Nachmittags und samstags, wenn's geschneit hat{" "}
          <span style={{ position: "relative", fontWeight: 700 }}>
            auch morgens vor der Schule.
            <span style={{ position: "absolute", left: -4, top: "52%", height: 10, width: `${st * 104}%`, background: RED, borderRadius: 6, rotate: "-2deg" }} />
          </span>
          “
        </div>
      </div>
      <div style={{ position: "absolute", left: 420, top: 470, opacity: fade(t, strikeAt - 0.2), scale: S(sp(t, strikeAt - 0.2, fps)) }}>
        <svg width={300} height={300} viewBox="0 0 100 100">
          <circle cx={50} cy={54} r={38} fill={PAPER} stroke={INK} strokeWidth={5} />
          <line x1={50} y1={54} x2={50} y2={28} stroke={INK} strokeWidth={5} strokeLinecap="round" />
          <line x1={50} y1={54} x2={66} y2={54} stroke={INK} strokeWidth={5} strokeLinecap="round" />
          <circle cx={24} cy={16} r={10} fill={INK} />
          <circle cx={76} cy={16} r={10} fill={INK} />
        </svg>
        <div style={{ position: "absolute", left: 40, top: 300, fontSize: 52, fontWeight: 700, color: INK, whiteSpace: "nowrap" }}>7:00 Uhr</div>
        <div style={{ position: "absolute", left: 80, top: 40, fontSize: 240, fontWeight: 700, color: RED, opacity: st, lineHeight: 1 }}>✗</div>
      </div>
      <div style={{ position: "absolute", left: 40, top: 520, fontSize: 58, fontWeight: 700, color: INK, opacity: fade(t, strikeAt + 0.1, 0.15), lineHeight: 1.15 }}>Claude lässt<br />das weg.</div>
    </div>
  );
};

// ---------- 5 Regel-Karte ----------
export const SceneRegel: React.FC<{ voll: number; unterricht: number }> = ({ voll, unterricht }) => {
  const { t, fps } = useT();
  const rows: [string, number, boolean][] = [
    ["vor dem Unterricht", unterricht, false],
    ["max. 2 Std. am Tag", unterricht + 0.5, true],
    ["nur 8–18 Uhr", unterricht + 0.8, true],
    ["Eltern einverstanden", unterricht + 1.1, true],
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 30, background: PAPER, border: `6px solid ${NAVY}`, borderRadius: 26, padding: "22px 30px", scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <div style={{ fontSize: 40, fontWeight: 700, color: GREEN }}>✓ Stimmt bei Leonie</div>
        <div style={{ fontSize: 62, fontWeight: 700, color: NAVY, lineHeight: 1.1, marginTop: 6, background: `rgba(255,224,138,${fade(t, voll)})`, borderRadius: 10, display: "inline-block", padding: "0 8px", margin: "6px -8px 0" }}>Noch voll schulpflichtig?</div>
        <div style={{ fontSize: 38, fontWeight: 600, color: MUTED, marginTop: 4 }}>Dann gilt beim Jobben gegen Geld:</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 14, marginTop: 18 }}>
          {rows.map(([txt, at, ok]) => (
            <div key={txt} style={{ opacity: fade(t, at), translate: `${(1 - fade(t, at)) * 30}px 0px`, display: "flex", alignItems: "center", gap: 18, fontSize: 52, fontWeight: 700, color: ok ? INK : RED }}>
              <span style={{ width: 60, textAlign: "center", color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span>
              {txt}
            </div>
          ))}
        </div>
        <div style={{ fontSize: 36, fontWeight: 600, color: MUTED, marginTop: 24, opacity: fade(t, unterricht + 1.3) }}>JArbSchG § 2 Abs. 3, § 5 Abs. 3 · je nach Bundesland 9 oder 10 Schuljahre</div>
      </div>
    </div>
  );
};

// ---------- 6 Der Haken: „üblich“ ohne Beleg ----------
export const SceneHaken: React.FC<{ mark: number; beleg: number }> = ({ mark, beleg }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 50, fontWeight: 700, color: MUTED }}>Der Haken</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 130, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", scale: S(sp(t, 0, fps)) }}>
        <ClaudeHead size={32} />
        <div style={{ padding: "18px 28px 26px", fontSize: 50, fontWeight: 600, lineHeight: 1.35 }}>
          „Mein Preisvorschlag: <b>10 € pro Stunde</b>.{" "}
          <span style={{ background: `rgba(255,224,138,${fade(t, mark)})`, borderRadius: 8, fontWeight: 700 }}>Das ist für Jugendliche in der Nachbarschaft üblich</span> und fair.“
        </div>
      </div>
      <Pop at={beleg} style={{ position: "absolute", left: 240, top: 620 }}>
        <Stempel size={84} rot={-6} text="OHNE BELEG" />
      </Pop>
      <div style={{ position: "absolute", left: 400, top: 800, fontSize: 40, fontWeight: 600, color: MUTED, opacity: fade(t, beleg + 0.4), whiteSpace: "nowrap" }}>Quelle? Keine genannt.</div>
    </div>
  );
};

// ---------- 7 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 20, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 54, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, zeilen) }}>5 von 5 Fehlern <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.25) }}>Regel erkannt <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.5) }}>Preis ungeprüft <span style={{ color: RED }}>✗</span></div>
      </div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar AUSHANG ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📌</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Vorlage<br />zum<br />Abschreiben</div>
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
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>AUSHANG</div>
        </div>
      </Pop>
    </div>
  );
};
