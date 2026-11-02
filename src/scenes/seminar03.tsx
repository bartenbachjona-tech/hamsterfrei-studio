import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";
import { Hamster } from "../Hamster";

// Seminar-Offensive S2 · „Prüfungsgespräch: Wofür hast du KI benutzt?“ · Leinwand 948×1004
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFDF8";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));

// Sprechblase der Lehrkraft (Schwanz unten links)
const Bubble: React.FC<{ label?: string; size?: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ label = "LEHRKRAFT", size = 64, style, children }) => (
  <div style={{ position: "absolute", ...style }}>
    <div style={{ position: "relative", background: "#fff", border: `7px solid ${INK}`, borderRadius: 40, padding: "26px 38px 30px", boxShadow: "0 14px 0 rgba(58,38,24,.12)" }}>
      <div style={{ fontSize: 30, fontWeight: 700, color: NAVY, letterSpacing: 2 }}>🧑‍🏫 {label}</div>
      <div style={{ fontSize: size, fontWeight: 700, lineHeight: 1.12, marginTop: 6 }}>{children}</div>
      <svg width={90} height={70} viewBox="0 0 90 70" style={{ position: "absolute", left: 70, bottom: -62 }}>
        <path d="M4 0 L30 64 L70 0" fill="#fff" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <rect x={0} y={-8} width={90} height={9} fill="#fff" />
      </svg>
    </div>
  </div>
);

const Num: React.FC<{ n: number; title: string }> = ({ n, title }) => {
  const { t, fps } = useT();
  const s = Math.max(0.6, sp(t, -0.1, fps));
  return (
    <div style={{ position: "absolute", left: 40, top: 36, display: "flex", alignItems: "center", gap: 22, scale: String(s), transformOrigin: "left center" }}>
      <div style={{ width: 110, height: 110, borderRadius: 55, background: RED, color: "#fff", border: `6px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 72, fontWeight: 700 }}>{n}</div>
      <div style={{ fontSize: 50, fontWeight: 700, color: MUTED }}>{title}</div>
    </div>
  );
};

const Badge: React.FC<{ ok?: boolean; at: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ ok = true, at, style, children }) => (
  <Pop at={at} style={{ position: "absolute", ...style }}>
    <div style={{ display: "inline-flex", alignItems: "center", gap: 14, background: ok ? GREEN : RED, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 30px", fontSize: 42, fontWeight: 600, whiteSpace: "nowrap" }}>
      {children}
    </div>
  </Pop>
);

const Lines: React.FC<{ n: number; w?: number[] }> = ({ n, w = [100, 92, 96, 70] }) => (
  <>
    {Array.from({ length: n }).map((_, i) => (
      <div key={i} style={{ height: 14, width: `${w[i % w.length]}%`, background: "#E6DACA", borderRadius: 7, marginTop: 16 }} />
    ))}
  </>
);

// ---------- Hook: steht ab Frame 0, bewegt sich ab Frame 0 ----------
export const SceneHook: React.FC<{ frage: number; pg: number }> = ({ frage, pg }) => {
  const { t, frame, fps } = useT();
  const wob = Math.sin(frame / 3) * 2.2; // Blase wackelt sofort
  const pulse = 1 + 0.035 * Math.sin(frame / 4);
  const shake = frame < 18 ? Math.sin(frame * 2.2) * (18 - frame) * 0.9 : 0;
  const stamp = t < pg ? 0 : spring({ frame: (t - pg) * fps, fps, config: { damping: 9, stiffness: 200 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      <div style={{ position: "absolute", left: 30, right: 30, top: 40, rotate: `${-2 + wob}deg`, scale: String(pulse), translate: `${shake}px 0px` }}>
        <Bubble size={104} style={{ position: "relative" }}>„Wofür hast du KI benutzt?“</Bubble>
      </div>
      {["?", "?", "?"].map((q, i) => (
        <div key={i} style={{ position: "absolute", right: 40 + i * 70, top: 470 + Math.sin(frame / 5 + i * 2) * 14, fontSize: 90 + i * 10, fontWeight: 700, color: i === 1 ? RED : NAVY, rotate: `${(i - 1) * 14}deg` }}>{q}</div>
      ))}
      <div style={{ position: "absolute", left: 50, top: 600, right: 50, fontSize: 76, fontWeight: 700, lineHeight: 1.1, color: INK }}>
        Mit <span style={{ color: RED, background: "#FFE7B0", borderRadius: 12, padding: "0 10px" }}>DIESER</span> Frage
        <br />musst du rechnen.
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 815, display: "flex", justifyContent: "center", scale: String(stamp ? 2 - stamp : 0), opacity: stamp ? 1 : 0, rotate: "-6deg" }}>
        <div style={{ border: `8px solid ${RED}`, color: RED, borderRadius: 18, padding: "6px 24px", fontSize: 60, fontWeight: 700, background: "rgba(255,255,255,.9)" }}>PRÜFUNGSGESPRÄCH</div>
      </div>
      {t >= frage && t < pg && <div style={{ position: "absolute", left: 60, top: 840, fontSize: 54, fontWeight: 700, color: MUTED, opacity: fade(t, frage) }}>👇</div>}
    </div>
  );
};

// ---------- Kultusministerium: KI-Gebrauch ist Gesprächsthema ----------
export const SceneKMS: React.FC<{ km: number; ki: number; thema: number }> = ({ km, ki, thema }) => {
  const { t, fps } = useT();
  const rows = ["Fachliche Kompetenz", "Arbeitsprozess", "KI-Gebrauch", "Konkrete Passagen", "Ergebnisse"];
  const s = Math.max(0.85, sp(t, -0.1, fps));
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 90, right: 90, top: 50, height: 880, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "36px 44px", scale: String(s), boxShadow: "0 16px 0 rgba(58,38,24,.12)" }}>
        <div style={{ fontSize: 30, color: MUTED, fontWeight: 700, letterSpacing: 1 }}>SCHREIBEN VOM 02.02.2026</div>
        <div style={{ fontSize: 50, fontWeight: 700, marginTop: 6, opacity: Math.max(0.35, fade(t, km - 0.1)) }}>🏛️ Kultusministerium</div>
        <div style={{ fontSize: 36, fontWeight: 600, color: MUTED, marginTop: 8 }}>Prüfungsgespräch · Fragen zu …</div>
        {rows.map((r, i) => {
          const isKI = r === "KI-Gebrauch";
          const on = isKI && t >= ki;
          return (
            <div key={r} style={{ marginTop: 18, fontSize: 44, fontWeight: on ? 700 : 500, padding: "12px 20px", borderRadius: 14, background: on ? "#FFE27A" : "#F3EBDD", color: on ? INK : MUTED, scale: on ? String(1 + 0.06 * sp(t, ki, fps)) : "1", opacity: fade(t, 0.1 + i * 0.12, 0.2), border: on ? `5px solid ${INK}` : "5px solid transparent" }}>
              {on ? "👉 " : ""}
              {r}
            </div>
          );
        })}
      </div>
      <Badge ok={false} at={thema} style={{ left: 170, top: 880 }}>KI-Gebrauch = eigenes Thema</Badge>
    </div>
  );
};

// ---------- Rahmen: max. 25 Minuten, optional Kurzvortrag ----------
export const SceneDauer: React.FC<{ min: number; vortrag: number }> = ({ min, vortrag }) => {
  const { t, fps } = useT();
  const p = interpolate(t, [min, min + 1.4], [0, 0.83], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const R = 170;
  const C = 2 * Math.PI * R;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 60, display: "flex", justifyContent: "center", scale: String(Math.max(0.8, sp(t, -0.1, fps))) }}>
        <svg width={420} height={420} viewBox="0 0 420 420">
          <circle cx={210} cy={210} r={R} fill="#fff" stroke={INK} strokeWidth={10} />
          <circle cx={210} cy={210} r={R - 24} fill="none" stroke={RED} strokeWidth={34} strokeDasharray={`${C} ${C}`} strokeDashoffset={C * (1 - p)} transform="rotate(-90 210 210)" opacity={0.9} />
          <text x={210} y={232} textAnchor="middle" fontSize={84} fontWeight={700} fill={INK} fontFamily="Fredoka">{t >= min ? "25" : ""}</text>
          <text x={210} y={290} textAnchor="middle" fontSize={40} fontWeight={600} fill={MUTED} fontFamily="Fredoka">{t >= min ? "Min." : ""}</text>
        </svg>
      </div>
      <Pop at={min} style={{ position: "absolute", left: 0, right: 0, top: 500, textAlign: "center" }}>
        <div style={{ fontSize: 80, fontWeight: 700 }}>höchstens 25 Minuten</div>
      </Pop>
      <Pop at={vortrag} style={{ position: "absolute", left: 90, right: 90, top: 660 }}>
        <div style={{ background: "#EEF7F1", border: `6px solid ${GREEN}`, borderRadius: 26, padding: "22px 30px", textAlign: "center", rotate: "-2deg" }}>
          <div style={{ fontSize: 34, fontWeight: 700, color: GREEN }}>OPTIONAL · DAVOR</div>
          <div style={{ fontSize: 56, fontWeight: 700, marginTop: 4 }}>🎤 Kurzvortrag ≤ 5 Min.</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- „4 Fragen – vorher überlegen“ ----------
export const SceneVier: React.FC<{ vier: number }> = ({ vier }) => {
  const { t, frame, fps } = useT();
  const s = Math.max(0.75, sp(t, -0.1, fps)) * (t >= vier ? 1 + 0.15 * Math.max(0, 1 - (t - vier) * 3) : 1);
  return (
    <div style={{ position: "absolute", inset: 0, background: NAVY }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 120, textAlign: "center", color: "#fff", fontSize: 70, fontWeight: 700, opacity: Math.max(0.4, fade(t, 0)) }}>Überleg dir vorher:</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 260, textAlign: "center", color: "#FFE27A", fontSize: 300, fontWeight: 700, lineHeight: 1, scale: String(s ? s : 0.001), rotate: `${Math.sin(frame / 5) * 3}deg` }}>4</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 600, textAlign: "center", color: "#fff", fontSize: 110, fontWeight: 700 }}>Fragen</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 790, display: "flex", justifyContent: "center", gap: 30 }}>
        {[0, 1, 2, 3].map((i) => (
          <div key={i} style={{ width: 80, height: 80, borderRadius: 40, background: "#fff", color: NAVY, display: "grid", placeItems: "center", fontSize: 50, fontWeight: 700, scale: String(sp(t, 0.3 + i * 0.25, fps)) }}>{i + 1}</div>
        ))}
      </div>
    </div>
  );
};

// ---------- Frage 1: Forschungsfrage ----------
export const SceneF1: React.FC<{ bubble: number; idee: number }> = ({ bubble, idee }) => {
  const { t, frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={1} title="Thema & Frage" />
      <Pop at={bubble} style={{ position: "absolute", left: 40, right: 40, top: 190 }}>
        <Bubble size={70} style={{ position: "relative" }}>„Wie bist du auf deine Forschungsfrage gekommen?“</Bubble>
      </Pop>
      <Pop at={idee} style={{ position: "absolute", left: 0, right: 0, top: 640, display: "flex", justifyContent: "center", gap: 60, alignItems: "center" }}>
        <div style={{ fontSize: 170, translate: `0px ${Math.sin(frame / 5) * 10}px` }}>💡</div>
        <div style={{ fontSize: 50, fontWeight: 700, color: GREEN, lineHeight: 1.2, opacity: fade(t, idee + 0.4) }}>Deine echte<br />Geschichte</div>
      </Pop>
    </div>
  );
};

// ---------- Frage 2: Passage auf Seite 12 ----------
export const SceneF2: React.FC<{ seite: number; worte: number; wer: number }> = ({ seite, worte, wer }) => {
  const { t, fps } = useT();
  const hl = fade(t, seite, 0.5);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={2} title="Eine Stelle erklären" />
      <div style={{ position: "absolute", left: 70, width: 520, top: 180, height: 600, background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: "28px 34px", rotate: "-2deg", scale: String(Math.max(0.8, sp(t, -0.1, fps))) }}>
        <Lines n={3} />
        <div style={{ marginTop: 22, height: 120, borderRadius: 10, background: `rgba(255,226,122,${hl})`, border: `5px solid rgba(200,71,58,${hl})`, padding: "6px 10px" }}>
          <Lines n={3} w={[96, 100, 80]} />
        </div>
        <Lines n={4} w={[100, 90, 94, 60]} />
        <div style={{ position: "absolute", bottom: 20, left: 0, right: 0, textAlign: "center", fontSize: 40, fontWeight: 700, color: MUTED }}>– 12 –</div>
      </div>
      <Pop at={seite} style={{ position: "absolute", right: 50, top: 230 }}>
        <div style={{ background: RED, color: "#fff", border: `6px solid ${INK}`, borderRadius: 24, padding: "14px 28px", fontSize: 64, fontWeight: 700, rotate: "6deg" }}>S. 12</div>
      </Pop>
      <Pop at={worte} style={{ position: "absolute", right: 40, top: 420, width: 340 }}>
        <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: 26, padding: "18px 22px", fontSize: 46, fontWeight: 700, lineHeight: 1.15, textAlign: "center" }}>🗣️ in eigenen Worten</div>
      </Pop>
      <Badge ok={false} at={wer} style={{ left: 60, top: 840 }}>🤔 Wer hat das geschrieben?</Badge>
    </div>
  );
};

// ---------- Frage 3: KI-Gebrauch + Prüfen ----------
export const SceneF3: React.FC<{ ki: number; geprueft: number }> = ({ ki, geprueft }) => {
  const { t, frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={3} title="KI-Gebrauch" />
      <Pop at={ki} style={{ position: "absolute", left: 40, right: 40, top: 190 }}>
        <Bubble size={70} style={{ position: "relative" }}>„Wofür hast du KI benutzt?“</Bubble>
      </Pop>
      <Pop at={geprueft} style={{ position: "absolute", left: 40, right: 40, top: 590 }}>
        <Bubble size={66} style={{ position: "relative" }}>„Und wie hast du die Ergebnisse geprüft?“</Bubble>
      </Pop>
      {t >= geprueft + 0.5 && (
        <div style={{ position: "absolute", right: 60, top: 820, fontSize: 130, rotate: `${Math.sin(frame / 4) * 10}deg`, opacity: fade(t, geprueft + 0.5) }}>🔍</div>
      )}
    </div>
  );
};

// ---------- Frage 4: Rückblick ----------
export const SceneF4: React.FC<{ bubble: number }> = ({ bubble }) => {
  const { frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={4} title="Rückblick" />
      <Pop at={bubble} style={{ position: "absolute", left: 40, right: 40, top: 190 }}>
        <Bubble size={76} style={{ position: "relative" }}>„Was würdest du heute anders machen?“</Bubble>
      </Pop>
      {["⏰ Zeitplan", "📚 Quellen", "🧪 Methode"].map((x, i) => (
        <Pop key={x} at={bubble + 0.5 + i * 0.35} style={{ position: "absolute", left: 90 + i * 70, top: 600 + i * 120 }}>
          <div style={{ background: i === 1 ? "#FFE27A" : "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 34px", fontSize: 54, fontWeight: 700, rotate: `${(i - 1) * 4 + Math.sin(frame / 6 + i) * 2}deg` }}>{x}</div>
        </Pop>
      ))}
    </div>
  );
};

// ---------- Schluss: Fragenkatalog + Probe-Prüfung + Link im Profil ----------
export const SceneSkill: React.FC<{ katalog: number; probe: number; link: number }> = ({ katalog, probe, link }) => {
  const { t, fps, frame } = useT();
  if (t >= link) {
    const s = sp(t, link, fps);
    const glow = 0.5 + 0.5 * Math.sin(frame / 4);
    return (
      <div style={{ position: "absolute", inset: 0, background: CREAM }}>
        <div style={{ position: "absolute", left: 214, top: 50, width: 520, height: 880, background: "#fff", border: `10px solid ${INK}`, borderRadius: 56, scale: String(s), overflow: "hidden" }}>
          <div style={{ padding: "54px 36px", textAlign: "center" }}>
            <div style={{ width: 160, height: 160, borderRadius: 80, background: "#F5E7CF", margin: "0 auto", overflow: "hidden", border: `5px solid ${INK}` }}>
              <div style={{ marginTop: 36, marginLeft: -12 }}>
                <Hamster size={190} talking={false} blink={false} pointerAngle={0} />
              </div>
            </div>
            <div style={{ fontSize: 44, fontWeight: 700, marginTop: 18 }}>@hamsterfrei</div>
            <div style={{ fontSize: 28, color: MUTED, marginTop: 10, lineHeight: 1.3 }}>Seminararbeit bis 10.11.?<br />Keine Angst 🐹</div>
            <div style={{ marginTop: 34, fontSize: 32, fontWeight: 700, color: "#1A56C4", border: `5px solid rgba(35,136,90,${glow})`, borderRadius: 18, padding: "14px 8px", background: "#EEF7F1" }}>🔗 hamsterfrei.de/seminar</div>
            <div style={{ marginTop: 60, fontSize: 58, fontWeight: 700, color: GREEN, scale: String(sp(t, link + 0.3, fps)) }}>☝️ Link im Profil</div>
          </div>
        </div>
      </div>
    );
  }
  const exam = t >= probe;
  const fragen = ["Wie bist du auf … gekommen?", "S. 12: Erklär das …", "Wofür KI? Wie geprüft?", "Woher stammt die Zahl …?"];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ height: 90, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 34px", fontSize: 36, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
        <div style={{ width: 22, height: 22, borderRadius: 11, background: "#E5835E" }} />
        Claude
        <span style={{ marginLeft: "auto", background: GREEN, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>Skill: Seminararbeit-Profi</span>
      </div>
      {!exam ? (
        <div style={{ padding: "30px 50px" }}>
          <div style={{ fontSize: 34, color: MUTED, fontWeight: 600 }}>📄 deine Arbeit →</div>
          <div style={{ fontSize: 56, fontWeight: 700, marginBottom: 10, opacity: Math.max(0.3, fade(t, katalog - 0.2)) }}>Fragenkatalog</div>
          {fragen.map((x, i) => {
            const a = katalog - 1.4 + i * 0.35;
            return (
              <div key={x} style={{ display: "flex", alignItems: "center", gap: 20, fontSize: 42, padding: "16px 0", borderBottom: "3px solid #EFE4D2", opacity: fade(t, a, 0.2), translate: `${(1 - fade(t, a, 0.2)) * -40}px 0px` }}>
                <div style={{ width: 54, height: 54, borderRadius: 27, background: NAVY, color: "#fff", display: "grid", placeItems: "center", fontWeight: 700, fontSize: 32, flex: "none" }}>{i + 1}</div>
                <div style={{ fontWeight: 600 }}>{x}</div>
              </div>
            );
          })}
        </div>
      ) : (
        <div style={{ padding: "34px 50px", display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ fontSize: 56, fontWeight: 700, opacity: fade(t, probe) }}>🎓 Probe-Prüfung</div>
          <div style={{ alignSelf: "flex-start", maxWidth: "88%", background: "#fff", border: "4px solid #E7D9C2", borderRadius: 24, padding: "18px 26px", fontSize: 42, lineHeight: 1.3, opacity: fade(t, probe + 0.15) }}>
            <span style={{ fontSize: 28, color: MUTED, fontWeight: 700 }}>LEHRKRAFT (geübt)</span>
            <br />Wofür hast du KI benutzt?
          </div>
          <div style={{ alignSelf: "flex-end", maxWidth: "80%", background: "#F1E6D3", borderRadius: 24, padding: "18px 26px", fontSize: 42, lineHeight: 1.3, opacity: fade(t, probe + 0.5) }}>
            Für die Gliederung. Jede Zahl hab ich nachgeschlagen …
          </div>
        </div>
      )}
    </div>
  );
};
