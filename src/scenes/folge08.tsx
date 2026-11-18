import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge08 · „Wie wird dein Minijob-Lebenslauf besser?“ · Hook-Test Variante B (Paar 4) · ohne Werbung · Leinwand 948×1004
// Lebenslauf vom Studio erfunden (docs/plaene/beispiel/lebenslauf_beispiel.txt), Person fiktiv.
// Claude-Antwort echt (docs/plaene/beispiel/lebenslauf_claude_antwort.md). Zeiten in Props = Sekunden ab Szenenstart.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
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

const ClaudeHead: React.FC<{ size?: number }> = ({ size = 36 }) => (
  <div style={{ height: size * 2.2, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 26px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    Claude
  </div>
);

const Stempel: React.FC<{ size?: number; rot?: number; text?: string; color?: string }> = ({ size = 34, rot = -8, text = "BEISPIEL", color = RED }) => (
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.88)", whiteSpace: "nowrap" }}>{text}</div>
);


const DGREEN = "#1C7049";
const LGREEN = "#DDF1E6";

// Alter Lebenslauf (erfunden). marks: strike Mail/Hobbys, ring um Kiosk
const AltCV: React.FC<{ width: number; fs: number; mail?: number; kiosk?: number; hobby?: number; grund?: number }> = ({ width, fs, mail = 0, kiosk = 0, hobby = 0, grund = 0 }) => {
  const Strike: React.FC<{ v: number }> = ({ v }) => (
    <div style={{ position: "absolute", left: -4, top: "52%", height: fs * 0.16, width: `${v * 104}%`, background: RED, borderRadius: 6, rotate: "-2deg" }} />
  );
  const H: React.FC<{ children: React.ReactNode }> = ({ children }) => <div style={{ fontSize: fs * 0.9, fontWeight: 700, color: NAVY, marginTop: fs * 0.35 }}>{children}</div>;
  const L: React.FC<{ children: React.ReactNode; s?: React.CSSProperties }> = ({ children, s }) => <div style={{ position: "relative", fontSize: fs * 0.78, fontWeight: 600, lineHeight: 1.4, color: "#33415C", whiteSpace: "nowrap", ...s }}>{children}</div>;
  return (
    <div style={{ width, background: PAPER, border: `5px solid ${INK}`, borderRadius: 14, padding: `${fs * 0.5}px ${fs * 0.6}px`, boxShadow: "6px 8px 0 rgba(58,38,24,.12)", overflow: "hidden" }}>
      <div style={{ fontSize: fs * 1.15, fontWeight: 700 }}>Lebenslauf</div>
      <L>Leon Beispiel · 2008</L>
      <L>Mail: zockerkoenig2008@…{mail > 0 && <Strike v={mail} />}</L>
      <H>Schule</H>
      <L>Gymnasium, 11. Klasse</L>
      <L>Grundschule{grund > 0 && <Strike v={grund} />}</L>
      <H>Praktikum</H>
      <L>Supermarkt, 2 Wochen</L>
      <H>Sonstiges</H>
      <L>
        Schulkiosk verkauft
        {kiosk > 0 && (
          <svg viewBox="0 0 200 40" preserveAspectRatio="none" style={{ position: "absolute", left: -26, top: -10, width: "118%", height: "150%" }}>
            <ellipse cx={100} cy={20} rx={97} ry={17} fill="none" stroke={RED} strokeWidth={4} strokeDasharray={420} strokeDashoffset={420 * (1 - kiosk)} strokeLinecap="round" />
          </svg>
        )}
      </L>
      <L>Babysitten</L>
      <H>Hobbys</H>
      <L>chillen, zocken, Netflix{hobby > 0 && <Strike v={hobby} />}</L>
      <L>Fußball</L>
    </div>
  );
};

// Neuer Lebenslauf nach Claudes Fassung (gekürzt). Kiosk = erster Punkt unter „Praktische Erfahrung“.
const NeuCV: React.FC<{ width: number; fs: number; hl?: number; kioskLines?: boolean }> = ({ width, fs, hl = 1, kioskLines }) => {
  const H: React.FC<{ children: React.ReactNode }> = ({ children }) => <div style={{ fontSize: fs * 0.85, fontWeight: 700, color: NAVY, marginTop: fs * 0.3 }}>{children}</div>;
  const L: React.FC<{ children: React.ReactNode; g?: boolean }> = ({ children, g }) => (
    <div style={{ fontSize: fs * 0.74, fontWeight: 600, lineHeight: 1.4, color: g ? DGREEN : "#33415C", background: g && hl ? LGREEN : "transparent", borderRadius: 8, padding: "0 6px", margin: "0 -6px", whiteSpace: "nowrap" }}>{children}</div>
  );
  return (
    <div style={{ width, background: PAPER, border: `5px solid ${GREEN}`, borderRadius: 14, padding: `${fs * 0.5}px ${fs * 0.6}px`, boxShadow: "6px 8px 0 rgba(35,136,90,.18)", overflow: "hidden" }}>
      <div style={{ fontSize: fs * 1.1, fontWeight: 700 }}>LEBENSLAUF</div>
      <L>Leon Beispiel</L>
      <L g>E-Mail: [seriöse Adresse]</L>
      <H>Schulbildung</H>
      <L>seit [Jahr] Gymnasium, 11. Kl.</L>
      <H>Praktische Erfahrung</H>
      <L g>▸ Verkauf am Schulkiosk</L>
      {kioskLines && <L>  Kassieren, Wechselgeld …</L>}
      <L>▸ Praktikum Supermarkt</L>
      <L>▸ Babysitten</L>
      <H>Interessen</H>
      <L>Fußball</L>
      <H>Verfügbarkeit</H>
      <L g>[z. B. samstags ganztags]</L>
    </div>
  );
};

// ---------- 1 Hook: Vorher/Nachher ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { frame } = useT();
  const pulse = 1 + Math.max(0, Math.sin(frame / 5)) * 0.04;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 16, textAlign: "center", fontSize: 64, fontWeight: 700, lineHeight: 1.06, color: NAVY }}>
        Lebenslauf Minijob:<br /><span style={{ color: RED }}>5 Fehler</span>
      </div>
      <div style={{ position: "absolute", left: 14, top: 196, rotate: "-2deg" }}>
        <div style={{ position: "absolute", left: 10, top: -34, zIndex: 2 }}><Stempel size={24} text="BEISPIEL" /></div>
        <AltCV width={440} fs={36} mail={1} kiosk={1} hobby={1} grund={1} />
      </div>
      <div style={{ position: "absolute", right: 14, top: 190, rotate: "2deg" }}>
        <NeuCV width={430} fs={34} />
      </div>
      <svg width={120} height={200} viewBox="0 0 120 200" style={{ position: "absolute", left: 436, top: 447 }}>
        <path d="M18 178 C 40 120, 50 70, 74 30" fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" />
        <path d="M56 34 L78 22 L84 48" fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div style={{ position: "absolute", left: 250, top: 236, fontSize: 24, fontWeight: 700, color: PAPER, background: RED, borderRadius: 10, padding: "2px 10px", rotate: "-2deg", whiteSpace: "nowrap" }}>✗ wann kannst du?</div>
      <div style={{ position: "absolute", right: 16, top: 830, background: MARK, border: `6px solid ${INK}`, borderRadius: 24, padding: "6px 22px", fontSize: 50, whiteSpace: "nowrap", fontWeight: 700, rotate: "-3deg", scale: S(pulse) }}>
        5 von 5 gefunden <span style={{ color: DGREEN }}>✓</span>
      </div>
    </div>
  );
};

// ---------- 2 Beispiel + eingegebene Frage ----------
export const SceneBeispiel: React.FC<{ frage: number }> = ({ frage }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 150, scale: S(sp(t, 0, fps)), transformOrigin: "top left", rotate: "-1deg" }}>
        <div style={{ position: "absolute", left: 10, top: -36, zIndex: 2 }}><Stempel size={28} text="BEISPIEL" /></div>
        <AltCV width={520} fs={40} />
      </div>
      <Pop at={0.5} style={{ position: "absolute", left: 40, top: 30 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: "6px 22px", fontSize: 46, fontWeight: 700 }}>☕ Ziel: Aushilfe im Café</div>
      </Pop>
      <Pop at={frage} style={{ position: "absolute", left: 590, right: 24, top: 230 }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "16px 20px", fontSize: 34, fontWeight: 600, lineHeight: 1.2 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 6 }}>an Claude:</div>
          „Ich bewerb mich für nen Minijob als Aushilfe in einem Café. Kannst du meinen Lebenslauf besser machen?“
          <div style={{ fontSize: 28, color: MUTED, marginTop: 6 }}>+ Lebenslauf</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 3 Mail ----------
export const SceneMail: React.FC<{ neu: number }> = ({ neu }) => {
  const { t, fps } = useT();
  const strike = interpolate(t, [0.5, 1.0], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Fehler 1 · Mail</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 170, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "30px 30px", scale: S(sp(t, 0, fps)) }}>
        <div style={{ position: "relative", display: "inline-block", fontSize: 50, fontWeight: 700, color: NAVY, whiteSpace: "nowrap" }}>
          zockerkoenig2008@…
          <div style={{ position: "absolute", left: -6, top: "50%", height: 12, width: `${strike * 104}%`, background: RED, borderRadius: 6, rotate: "-2deg" }} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 440, top: 380, fontSize: 90, fontWeight: 700, color: GREEN, opacity: fade(t, neu - 0.3) }}>↓</div>
      <Pop at={neu} style={{ position: "absolute", left: 60, right: 60, top: 520 }}>
        <div style={{ background: LGREEN, border: `6px solid ${GREEN}`, borderRadius: 26, padding: "34px 30px", fontSize: 66, fontWeight: 700, color: DGREEN, textAlign: "center" }}>E-Mail:<br />[neue, seriöse Adresse]</div>
      </Pop>
      <div style={{ position: "absolute", right: 60, top: 820, fontSize: 44, fontWeight: 700, color: DGREEN, opacity: fade(t, neu + 0.3) }}>Claude ✓</div>
    </div>
  );
};

// ---------- 4 Kiosk nach vorn ----------
export const SceneKiosk: React.FC<{ cafe: number; vorn: number }> = ({ cafe, vorn }) => {
  const { t, fps } = useT();
  const move = interpolate(t, [vorn, vorn + 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Fehler 2 · versteckt</div>
      <div style={{ position: "absolute", left: 50, right: 50, top: 130, background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: "18px 26px", opacity: 1 - 0.55 * move, scale: S(sp(t, 0, fps)) }}>
        <div style={{ fontSize: 44, fontWeight: 700, color: NAVY }}>Sonstiges</div>
        <div style={{ fontSize: 56, fontWeight: 700 }}>Schulkiosk verkauft</div>
        <div style={{ fontSize: 40, fontWeight: 600, color: MUTED }}>Babysitten · Englisch gut</div>
      </div>
      <Pop at={cafe} style={{ position: "absolute", left: 470, top: 395 }}>
        <div style={{ whiteSpace: "nowrap", background: MARK, border: `5px solid ${INK}`, borderRadius: 20, padding: "6px 22px", fontSize: 50, fontWeight: 700, rotate: "4deg" }}>= Café-Arbeit ☕</div>
      </Pop>
      <div style={{ position: "absolute", left: 60, right: 60, top: 520, translate: `0px ${(1 - move) * 140}px`, opacity: move }}>
        <div style={{ background: PAPER, border: `6px solid ${GREEN}`, borderRadius: 22, padding: "16px 26px" }}>
          <div style={{ fontSize: 36, fontWeight: 600, color: MUTED }}>Schulbildung …</div>
          <div style={{ fontSize: 46, fontWeight: 700, color: NAVY }}>Praktische Erfahrung</div>
          <div style={{ fontSize: 56, fontWeight: 700, color: DGREEN, background: LGREEN, borderRadius: 10, padding: "0 10px" }}>1. Verkauf am Schulkiosk</div>
          <div style={{ fontSize: 38, fontWeight: 600, color: MUTED }}>2. Praktikum · 3. Babysitten</div>
        </div>
      </div>
      <div style={{ position: "absolute", right: 60, top: 820, fontSize: 44, fontWeight: 700, color: DGREEN, opacity: fade(t, vorn + 0.5) }}>Claude ✓</div>
    </div>
  );
};

// ---------- 5 Hobbys ----------
export const SceneHobbys: React.FC<{ raus: number; bleibt: number }> = ({ raus, bleibt }) => {
  const { t } = useT();
  const items = ["chillen", "zocken", "Netflix"];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Fehler 3 · Hobbys</div>
      {items.map((it, i) => {
        const a = raus + i * 0.12;
        const k = interpolate(t, [a, a + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return (
          <div key={it} style={{ position: "absolute", left: 60 - k * 40, top: 170 + i * 150 + k * 20, rotate: `${-k * 8}deg`, opacity: 1 - k * 0.6, whiteSpace: "nowrap", background: PAPER, border: `6px solid ${RED}`, borderRadius: 40, padding: "14px 30px", fontSize: 58, fontWeight: 700, color: RED }}>
            {it} ✗
          </div>
        );
      })}
      <Pop at={bleibt} style={{ position: "absolute", left: 330, top: 560 }}>
        <div style={{ whiteSpace: "nowrap", background: LGREEN, border: `8px solid ${GREEN}`, borderRadius: 40, padding: "16px 36px", fontSize: 70, fontWeight: 700, color: DGREEN }}>⚽ Fußball ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 6 Neuestes nach oben + Verfügbarkeit ----------
export const SceneNeu: React.FC<{ verf: number }> = ({ verf }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Fehler 4 + 5</div>
      <div style={{ position: "absolute", left: 30, top: 110, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <NeuCV width={560} fs={46} hl={0} />
      </div>
      <Pop at={0.2} style={{ position: "absolute", left: 620, top: 220 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: "8px 20px", fontSize: 46, fontWeight: 700, color: NAVY, lineHeight: 1.1 }}>↑ Neuestes<br />nach oben</div>
      </Pop>
      <Pop at={verf} style={{ position: "absolute", left: 628, top: 600 }}>
        <div style={{ whiteSpace: "nowrap", background: LGREEN, border: `6px solid ${GREEN}`, borderRadius: 24, padding: "10px 16px", fontSize: 38, fontWeight: 700, color: DGREEN, lineHeight: 1.15 }}>🕒 Wann<br />kannst du<br />arbeiten?</div>
      </Pop>
      <div style={{ position: "absolute", right: 40, top: 840, fontSize: 44, fontWeight: 700, color: DGREEN, opacity: fade(t, verf + 0.3) }}>Claude ✓</div>
    </div>
  );
};

// ---------- 7 Ausgeschmückt ----------
export const SceneDazu: React.FC<{ mark: number; nirgends: number }> = ({ mark, nirgends }) => {
  const { t, fps } = useT();
  const hl = (a: number) => interpolate(t, [a, a + 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Aber …</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 120, fontSize: 40, fontWeight: 600, color: MUTED }}>Leon schrieb nur: <span style={{ color: INK, fontWeight: 700 }}>„Hab beim Schulkiosk verkauft“</span></div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 250, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", scale: S(sp(t, 0, fps)) }}>
        <ClaudeHead size={32} />
        <div style={{ padding: "16px 26px 22px", fontSize: 46, fontWeight: 600, lineHeight: 1.35 }}>
          <div>Verkauf am Schulkiosk</div>
          <div>– Verkauf von Snacks und Getränken</div>
          <div><span style={{ background: `rgba(255,224,138,${hl(mark)})`, borderRadius: 8 }}>– Kassieren und Herausgeben von Wechselgeld</span></div>
          <div><span style={{ background: `rgba(255,224,138,${hl(mark + 0.6)})`, borderRadius: 8 }}>– Schneller, freundlicher Service auch bei großem Andrang</span></div>
        </div>
      </div>
      <Pop at={nirgends} style={{ position: "absolute", left: 300, top: 780 }}>
        <Stempel size={80} rot={-5} text="STAND NIRGENDS" />
      </Pop>
    </div>
  );
};

// ---------- 8 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 20, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 56, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, zeilen) }}>5 von 5 Fehlern <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.25) }}>Kiosk ausgeschmückt <span style={{ color: RED }}>✗</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.3), fontSize: 46, color: NAVY }}>→ streich, was nicht stimmt</div>
      </div>
    </div>
  );
};

// ---------- 9 Ende: Handy + Kommentar LEBENSLAUF ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📋</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Frage<br />+<br />Checkliste</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 230, top: 850 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>LEBENSLAUF</div>
        </div>
      </Pop>
    </div>
  );
};
