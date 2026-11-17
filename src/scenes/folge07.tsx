import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge07 · „Ist diese Handy-Anzeige faul?“ · Hook-Test Variante B (Paar 3) · ohne Werbung · Leinwand 948×1004
// Anzeige vom Studio erfunden (docs/plaene/beispiel/handy_anzeige_beispiel.txt), kein Portal, kein Logo, Nummer geschwärzt.
// Claude-Antwort echt (docs/plaene/beispiel/handy_claude_antwort.md). Zeiten in Props = Sekunden ab Szenenstart.
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

// Gezeichnetes Handy (kein Produktfoto)
const PhoneIcon: React.FC<{ h: number; lock?: boolean }> = ({ h, lock }) => (
  <svg width={h * 0.52} height={h} viewBox="0 0 52 100">
    <rect x={2} y={2} width={48} height={96} rx={9} fill="#2A2733" stroke={INK} strokeWidth={3} />
    <rect x={6} y={8} width={40} height={84} rx={6} fill={lock ? "#3B3F55" : "#8FB3D9"} />
    <rect x={19} y={4} width={14} height={4} rx={2} fill="#111" />
    {lock && (
      <g>
        <rect x={16} y={48} width={20} height={16} rx={3} fill="#F3EBDD" />
        <path d="M20 48v-6a6 6 0 0 1 12 0v6" fill="none" stroke="#F3EBDD" strokeWidth={3.5} />
      </g>
    )}
  </svg>
);

// Anzeige (erfunden). mark: 'warn' = rot eingekreist ⚠, 'miss' = gelb gestrichelt „übersehen“
type Mark = "warn" | "miss" | undefined;
const ZEILEN = [
  { text: "Wie neu, keine Kratzer.", falle: 0 },
  { text: "Akku top.", falle: 3 },
  { text: "Bin in Spanien, nur Versand.", falle: 2 },
  { text: "Vorab: PayPal Freunde & Familie", falle: 1 },
  { text: "iCloud entferne ich nach Zahlung.", falle: 4 },
  { text: "Fotos per WhatsApp: 0176 ••••", falle: 5 },
];
const Anzeige: React.FC<{ width: number; fs: number; marks?: Record<number, Mark>; nums?: number; ring?: number }> = ({ width, fs, marks = {}, nums = 0, ring = 1 }) => (
  <div style={{ width, background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, overflow: "hidden", boxShadow: "6px 8px 0 rgba(58,38,24,.12)" }}>
    <div style={{ display: "flex", gap: fs * 0.5, padding: fs * 0.45, background: "#EEF2F8", alignItems: "center" }}>
      <PhoneIcon h={fs * 3.1} />
      <div>
        <div style={{ fontSize: fs * 1.05, fontWeight: 700, lineHeight: 1.1 }}>iPhone 13 · 128 GB<br />wie neu</div>
        <div style={{ fontSize: fs * 1.3, fontWeight: 700, color: NAVY, marginTop: 4 }}>289 € VB</div>
      </div>
    </div>
    <div style={{ padding: `${fs * 0.3}px ${fs * 0.45}px ${fs * 0.45}px` }}>
      {ZEILEN.map((z, i) => {
        const m = marks[i];
        return (
          <div key={i} style={{ position: "relative", fontSize: fs * 0.82, fontWeight: 600, lineHeight: 1.6, whiteSpace: "nowrap", color: "#33415C" }}>
            {m === "miss" && <div style={{ position: "absolute", left: -6, right: "auto", width: "60%", top: "10%", height: "80%", background: MARK, borderRadius: 6, border: `3px dashed ${MUTED}` }} />}
            {nums > 0 && z.falle > 0 && z.falle <= nums && (
              <span style={{ display: "inline-block", width: fs * 0.95, height: fs * 0.95, lineHeight: `${fs * 0.95}px`, textAlign: "center", borderRadius: fs, background: MARK, border: `3px solid ${INK}`, fontSize: fs * 0.6, fontWeight: 700, marginRight: 8, position: "relative" }}>{z.falle}</span>
            )}
            <span style={{ position: "relative", marginLeft: m === "warn" ? fs * 0.4 : 0 }}>{z.text}</span>
            {m === "warn" && (
              <svg viewBox="0 0 200 40" preserveAspectRatio="none" style={{ position: "absolute", left: -30, top: -6, width: "108%", height: "130%", pointerEvents: "none" }}>
                <ellipse cx={100} cy={20} rx={97} ry={17} fill="none" stroke={RED} strokeWidth={4} strokeDasharray={420} strokeDashoffset={420 * (1 - ring)} strokeLinecap="round" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  </div>
);

const ALLE_WARN: Record<number, Mark> = { 2: "warn", 3: "warn", 4: "warn", 5: "warn", 1: "miss" };

// ---------- 1 Hook: Ergebnis ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { frame } = useT();
  const pulse = 1 + Math.max(0, Math.sin(frame / 5)) * 0.04;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 18, textAlign: "center", fontSize: 64, fontWeight: 700, lineHeight: 1.06, color: NAVY }}>
        Fake-Anzeige erkennen:<br /><span style={{ color: RED }}>4 von 5</span>
      </div>
      <div style={{ position: "absolute", left: 16, top: 200, rotate: "-2deg" }}>
        <div style={{ position: "absolute", left: 10, top: -36, zIndex: 2 }}><Stempel size={26} text="BEISPIEL" /></div>
        <Anzeige width={680} fs={42} marks={ALLE_WARN} />
      </div>
      <div style={{ position: "absolute", right: 6, top: 730, width: 410, background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, overflow: "hidden", rotate: "3deg", scale: S(pulse), boxShadow: "0 10px 0 rgba(58,38,24,.12)" }}>
        <ClaudeHead size={34} />
        <div style={{ padding: "16px 22px 22px", fontSize: 58, fontWeight: 700, color: RED, lineHeight: 1.05 }}>Bitte nicht kaufen.</div>
      </div>
      <div style={{ position: "absolute", left: 215, top: 490, fontSize: 36, fontWeight: 700, color: INK, background: MARK, border: `3px solid ${INK}`, borderRadius: 12, padding: "0 12px", rotate: "-2deg" }}>← nicht erkannt</div>
    </div>
  );
};

// ---------- 2 Ganze Anzeige, 5 Fallen nummeriert ----------
export const SceneAnzeige: React.FC<{ fallen: number }> = ({ fallen }) => {
  const { t, fps } = useT();
  const nums = Math.min(5, Math.floor(interpolate(t, [fallen, fallen + 0.6], [0, 5.99], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 28, fontSize: 54, fontWeight: 700 }}>Meine Beispiel-Anzeige</div>
      <div style={{ position: "absolute", left: 60, top: 130, scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <Anzeige width={830} fs={48} nums={nums} />
      </div>
      <Pop at={fallen + 0.2} style={{ position: "absolute", right: 40, top: 30 }}>
        <Stempel size={48} rot={6} text="5 FALLEN" />
      </Pop>
    </div>
  );
};

// ---------- 3 Chat: Claude sagt sofort „nicht kaufen“ ----------
export const SceneChat: React.FC<{ urteil: number }> = ({ urteil }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 250, right: 36, top: 120, background: "#F1E6D3", borderRadius: "30px 30px 6px 30px", padding: "18px 24px", fontSize: 40, fontWeight: 600, lineHeight: 1.2, opacity: fade(t, 0) }}>
        Kann ich zuschlagen oder ist da was faul? <span style={{ color: MUTED }}>+ Anzeige</span>
      </div>
      <div style={{ position: "absolute", left: 36, right: 36, top: 360, background: PAPER, border: `5px solid ${INK}`, borderRadius: "30px 30px 30px 6px", padding: "26px 30px", scale: S(sp(t, urteil - 0.3, fps)), transformOrigin: "top left" }}>
        <div style={{ fontSize: 46, fontWeight: 600, color: MUTED, marginBottom: 8 }}>Kurz gesagt:</div>
        <div style={{ fontSize: 96, fontWeight: 700, color: RED, lineHeight: 1 }}>Bitte nicht kaufen.</div>
      </div>
    </div>
  );
};

// ---------- 4 PayPal Freunde & Familie ----------
export const ScenePaypal: React.FC<{ schutz: number }> = ({ schutz }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Falle 1 · Bezahlung</div>
      <div style={{ position: "absolute", left: 70, right: 70, top: 140, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "28px 34px", scale: S(sp(t, 0, fps)) }}>
        <div style={{ fontSize: 44, fontWeight: 600, color: MUTED }}>Zahlung vorab per</div>
        <div style={{ fontSize: 70, fontWeight: 700, color: NAVY, lineHeight: 1.1 }}>PayPal<br />Freunde & Familie</div>
      </div>
      <div style={{ position: "absolute", left: 470, top: 460, fontSize: 90, fontWeight: 700, color: RED, opacity: fade(t, schutz - 0.3) }}>↓</div>
      <Pop at={schutz} style={{ position: "absolute", left: 300, top: 600 }}>
        <div style={{ background: "#FDE3DF", border: `8px solid ${RED}`, borderRadius: 24, padding: "10px 34px", fontSize: 72, fontWeight: 700, color: RED, rotate: "-3deg" }}>kein Käuferschutz ⚠</div>
      </Pop>
      <div style={{ position: "absolute", right: 50, top: 820, fontSize: 40, fontWeight: 700, color: "#1C7049", opacity: fade(t, schutz + 0.4) }}>Claude ✓</div>
    </div>
  );
};

// ---------- 5 iCloud erst nach Zahlung ----------
export const SceneIcloud: React.FC<{ wertlos: number }> = ({ wertlos }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Falle 4 · Sperre</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 120, fontSize: 56, fontWeight: 700, lineHeight: 1.15 }}>„iCloud entferne ich<br />nach Zahlung.“</div>
      <div style={{ position: "absolute", left: 110, top: 330, scale: S(sp(t, 0.2, fps)) }}>
        <PhoneIcon h={460} lock />
      </div>
      <div style={{ position: "absolute", left: 400, top: 380, fontSize: 52, fontWeight: 700, color: NAVY, opacity: fade(t, 0.6) }}>Aktivierungs-<br />sperre</div>
      <Pop at={wertlos} style={{ position: "absolute", left: 380, top: 600 }}>
        <Stempel size={104} rot={-6} text="WERTLOS" />
      </Pop>
      <div style={{ position: "absolute", right: 50, top: 840, fontSize: 40, fontWeight: 700, color: "#1C7049", opacity: fade(t, wertlos + 0.4) }}>Claude ✓</div>
    </div>
  );
};

// ---------- 6 Ausland + WhatsApp ----------
export const SceneAusland: React.FC<{ whatsapp: number }> = ({ whatsapp }) => {
  const { t } = useT();
  const Chip: React.FC<{ at: number; top: number; text: React.ReactNode }> = ({ at, top, text }) => (
    <Pop at={at} style={{ position: "absolute", left: 60, right: 60, top }}>
      <div style={{ display: "flex", alignItems: "center", gap: 20, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "18px 28px", fontSize: 54, fontWeight: 700 }}>
        <span style={{ flex: 1 }}>{text}</span>
        <span style={{ color: "#1C7049", fontSize: 46 }}>Claude ✓</span>
      </div>
    </Pop>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Falle 2 + 5</div>
      <Chip at={0.4} top={170} text={<>✈️ „gerade im Ausland,<br />nur Versand“</>} />
      <Chip at={whatsapp} top={480} text={<>💬 → WhatsApp<br /><span style={{ fontSize: 40, color: MUTED }}>weg von der Plattform</span></>} />
      <div style={{ position: "absolute", left: 300, top: 760, fontSize: 64, fontWeight: 700, color: RED, opacity: fade(t, whatsapp + 0.1) }}>4 von 5 gefunden</div>
    </div>
  );
};

// ---------- 7 Akku top: nicht als Haken genannt ----------
export const SceneAkku: React.FC<{ haken: number }> = ({ haken }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Falle 3 · Akku</div>
      <div style={{ position: "absolute", left: 60, top: 140, fontSize: 92, fontWeight: 700 }}>„Akku top.“</div>
      <svg width={420} height={220} viewBox="0 0 120 60" style={{ position: "absolute", left: 80, top: 320, scale: S(sp(t, 0.1, fps)) }}>
        <rect x={3} y={6} width={100} height={48} rx={8} fill={PAPER} stroke={INK} strokeWidth={4} />
        <rect x={104} y={20} width={10} height={20} rx={3} fill={INK} />
        <text x={53} y={42} textAnchor="middle" fontSize={26} fontWeight={700} fill={MUTED} fontFamily="Fredoka">?? %</text>
      </svg>
      <div style={{ position: "absolute", left: 540, top: 360, fontSize: 48, fontWeight: 700, color: NAVY, lineHeight: 1.15, opacity: fade(t, 0.6) }}>Wie viel<br />Prozent?</div>
      <Pop at={haken} style={{ position: "absolute", left: 260, top: 640 }}>
        <div style={{ background: MARK, border: `6px dashed ${INK}`, borderRadius: 24, padding: "12px 30px", fontSize: 58, fontWeight: 700, rotate: "-2deg" }}>Claude: kein Haken ✗</div>
      </Pop>
    </div>
  );
};

// ---------- 8 Preis: Fehlalarm „Lockpreis“ ----------
export const ScenePreis: React.FC<{ lock: number; general: number }> = ({ lock, general }) => {
  const { t, fps } = useT();
  const strike = interpolate(t, [general + 0.3, general + 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, fontSize: 50, fontWeight: 700, color: MUTED }}>Und der Preis?</div>
      <div style={{ position: "absolute", left: 60, top: 130, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "18px 30px", scale: S(sp(t, 0, fps)), transformOrigin: "top left" }}>
        <div style={{ fontSize: 40, fontWeight: 600, color: MUTED }}>Anzeige</div>
        <div style={{ fontSize: 100, fontWeight: 700, color: NAVY, lineHeight: 1 }}>289 €</div>
      </div>
      <Pop at={lock} style={{ position: "absolute", left: 470, top: 170 }}>
        <div style={{ position: "relative", background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: 24, padding: "10px 28px", fontSize: 58, fontWeight: 700, color: RED, rotate: "4deg" }}>
          Claude: „Lockpreis!“
          <div style={{ position: "absolute", left: 10, top: "48%", height: 10, width: `${strike * 95}%`, background: INK, borderRadius: 5, rotate: "-4deg" }} />
        </div>
      </Pop>
      <Pop at={general} style={{ position: "absolute", left: 60, right: 60, top: 450 }}>
        <div style={{ background: "#DDF1E6", border: `6px solid ${GREEN}`, borderRadius: 26, padding: "20px 30px" }}>
          <div style={{ fontSize: 44, fontWeight: 600, color: "#1C7049" }}>generalüberholt, gleiches Modell</div>
          <div style={{ fontSize: 100, fontWeight: 700, color: "#1C7049", lineHeight: 1.05 }}>299 €</div>
          <div style={{ fontSize: 30, fontWeight: 600, color: MUTED }}>Back Market, Preisübersicht Nov. 2026</div>
        </div>
      </Pop>
      <Pop at={general + 0.9} style={{ position: "absolute", left: 250, top: 800 }}>
        <Stempel size={84} rot={-5} text="FEHLALARM" color={NAVY} />
      </Pop>
    </div>
  );
};

// ---------- 9 Urteil: GEKLAPPT ----------
export const SceneUrteil: React.FC<{ stempel: number; vier: number }> = ({ stempel, vier }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: "#1C7049", borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 30, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 58, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, vier) }}>4 von 5 Fallen <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, vier + 0.3) }}>Akku nicht erkannt <span style={{ color: RED }}>✗</span></div>
        <div style={{ opacity: fade(t, vier + 0.5) }}>Preis: Fehlalarm <span style={{ color: RED }}>✗</span></div>
      </div>
    </div>
  );
};

// ---------- 10 Ende: Handy + Kommentar CHECK ----------
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
      <Pop at={commentAt} style={{ position: "absolute", left: 360, top: 840 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "16px 34px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 88, fontWeight: 600, color: INK, letterSpacing: 4 }}>CHECK</div>
        </div>
      </Pop>
    </div>
  );
};
