import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge11 · Hamster-Test „Morgen-Briefing aus Notiz-Chaos“ · Hook-Test Variante A (Paar 5) · ohne Werbung · Leinwand 948×1004
// Notizen + Person (Tim) vom Studio erfunden (docs/plaene/beispiel/morgen_notizen_beispiel.txt).
// Claude-Antwort echt (docs/plaene/beispiel/morgen_claude_antwort.md), Reihenfolge der Karte = Claudes echte Reihenfolge.
// Zeiten in Props = Sekunden ab Szenenstart. Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LGREEN = "#DDF1E6";
const LRED = "#F9DEDA";
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

const ClaudeHead: React.FC<{ size?: number; title?: string }> = ({ size = 32, title = "Claude" }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    {title}
  </div>
);

// Vorher: Handy-Notiz (9 Zeilen wörtlich aus dem Beispiel)
const NOTIZ = [
  "mo 1.+2. bio, 3. mathe test!!!",
  "sportzeug 5./6. sport",
  "zettel klassenfahrt unterschr.",
  "bus 7:12 fällt aus",
  "schicht supermarkt 16-19",
  "fußball training 18:30",
  "mama di geburtstag, geschenk??",
  "deutsch buch bis kap 6 (mi)",
  "handy laden!!",
];
const Notiz: React.FC<{ fs: number; wob?: number }> = ({ fs, wob = 0 }) => (
  <div style={{ background: "#FFF6B8", border: `4px solid #C9B55A`, borderRadius: 14, padding: `${fs * 0.5}px ${fs * 0.55}px`, boxShadow: "4px 6px 0 rgba(58,38,24,.12)", fontFamily: HAND, color: "#3B4A8C", lineHeight: 1.28 }}>
    <div style={{ fontSize: fs * 0.8, fontWeight: 700, color: MUTED, marginBottom: fs * 0.15 }}>Notizen</div>
    {NOTIZ.map((z, i) => (
      <div key={i} style={{ fontSize: fs, whiteSpace: "nowrap", rotate: `${(i % 2 ? 1 : -1) * (0.8 + wob)}deg` }}>{z}</div>
    ))}
  </div>
);

// Nachher: Claudes Briefing-Karte (echte Reihenfolge, gekürzt)
const PUNKTE: [string, string][] = [
  ["🌙", "Heute Abend: Handy, Zettel, Sportzeug"],
  ["🚌", "Bus 7:12 fällt aus: früher los"],
  ["📐", "3. Std: Mathetest Kap. 4"],
  ["🎁", "Geschenk für Mama bis 16 Uhr"],
];
const Karte: React.FC<{ width: number; fs: number; show?: number[]; konflikt?: number; pulse?: number; hl?: number }> = ({ width, fs, show = [1, 1, 1, 1], konflikt = 1, pulse = 0, hl = -1 }) => (
  <div style={{ width, background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden", boxShadow: "6px 8px 0 rgba(58,38,24,.14)" }}>
    <div style={{ background: NAVY, color: "#fff", fontSize: fs * 1.15, fontWeight: 700, padding: `${fs * 0.2}px ${fs * 0.6}px`, letterSpacing: 2 }}>MONTAG</div>
    <div style={{ padding: `${fs * 0.35}px ${fs * 0.45}px`, display: "flex", flexDirection: "column", gap: fs * 0.28 }}>
      {PUNKTE.map(([ic, txt], i) => (
        <div key={i} style={{ display: "flex", gap: fs * 0.3, alignItems: "flex-start", fontSize: fs, fontWeight: 600, lineHeight: 1.15, opacity: show[i], translate: `${(1 - show[i]) * 30}px 0px`, background: hl === i ? "rgba(255,224,138,1)" : "transparent", borderRadius: 10, padding: "0 6px", margin: "0 -6px" }}>
          <span style={{ color: MUTED, fontWeight: 700, minWidth: fs * 0.6 }}>{i + 1}</span>
          <span>{ic}</span>
          <span>{txt}</span>
        </div>
      ))}
      <div style={{ opacity: konflikt, display: "flex", gap: fs * 0.3, alignItems: "center", fontSize: fs * 1.05, fontWeight: 700, color: RED, background: LRED, border: `${4 + pulse * 3}px solid ${RED}`, borderRadius: 14, padding: `${fs * 0.15}px ${fs * 0.3}px` }}>
        <span style={{ color: MUTED, minWidth: fs * 0.6 }}>5</span>
        <span>⚠ Schicht 16–19 ↔ Training 18:30</span>
      </div>
    </div>
  </div>
);

// ---------- 1 Hook: Notiz-Chaos → Briefing ab Frame 0 ----------
export const SceneHook: React.FC = () => {
  const { t, frame } = useT();
  const pulse = (Math.sin(frame / 4) + 1) / 2;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 12, textAlign: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST · Schule organisieren</div>
        <div style={{ fontSize: 62, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>9 Notizen <span style={{ color: GREEN }}>→ 1 Morgen-Briefing</span></div>
      </div>
      <div style={{ position: "absolute", left: 14, top: 150, rotate: "-4deg", width: 330 }}>
        <div style={{ marginBottom: 6 }}><Stempel size={28} text="VORHER" /></div>
        <Notiz fs={23} wob={Math.sin(frame / 5) * 0.6} />
      </div>
      <div style={{ position: "absolute", left: 326, top: 300, fontSize: 90, fontWeight: 700, color: GREEN }}>➜</div>
      <div style={{ position: "absolute", left: 410, top: 190, rotate: "1.5deg", scale: S(1 + 0.06 * lin(t, 1.8, 0.8)), transformOrigin: "bottom center" }}>
        <div style={{ position: "absolute", right: 8, top: -34, zIndex: 2 }}><Stempel size={26} text="NACHHER · CLAUDE" rot={4} color={GREEN} /></div>
        <Karte width={520} fs={33} pulse={pulse} />
        <div style={{ position: "absolute", right: 10, bottom: -42 }}><Stempel size={20} text="BEISPIEL" rot={-3} /></div>
      </div>
      <div style={{ position: "absolute", left: 340, top: 770, fontSize: 40, fontWeight: 700, color: RED, scale: S(1 + 0.05 * pulse), rotate: "-3deg", whiteSpace: "nowrap" }}>⬆ Claude merkt den Konflikt!</div>
      <div style={{ position: "absolute", left: 0, top: 0, opacity: t < 0 ? 0 : 1 }} />
    </div>
  );
};

// ---------- 2 Die Eingabe (echt, gekürzt) ----------
export const SceneEingabe: React.FC = () => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26 }}><Stempel size={28} text="BEISPIEL · Hamster tippt Tims Notizen ein" rot={-3} /></div>
      <div style={{ position: "absolute", left: 120, right: 30, top: 140, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "18px 26px", fontSize: 44, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ fontSize: 30, color: MUTED, marginBottom: 6 }}>An Claude:</div>
          „Kannst du mir aus meinen Notizen ein kurzes <b>Morgen-Briefing für Montag</b> machen? … Höchstens fünf Punkte.“
        </div>
      </div>
      <Pop at={0.7} style={{ position: "absolute", left: 470, top: 560, rotate: "3deg" }}>
        <div style={{ background: "#FFF6B8", border: `4px solid #C9B55A`, borderRadius: 14, padding: "14px 26px", fontFamily: HAND, color: "#3B4A8C", fontSize: 56, lineHeight: 1.25 }}>
          + 9 Notiz-Zeilen
        </div>
      </Pop>
      <div style={{ position: "absolute", left: 470, top: 790, fontSize: 52, fontWeight: 700, color: NAVY, opacity: fade(t, 1.2) }}>Tim, 17 · Montag</div>
    </div>
  );
};

// ---------- 3 Karte baut sich auf: Bus, dann Mathetest ----------
export const SceneKarte: React.FC<{ bus: number; mathe: number }> = ({ bus, mathe }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 46, fontWeight: 700, color: MUTED }}>Claude sortiert nach Uhrzeit</div>
      <div style={{ position: "absolute", left: 60, top: 110, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <Karte width={830} fs={46} show={[0.35, fade(t, bus), fade(t, mathe), 0]} konflikt={0} hl={t >= mathe ? 2 : t >= bus ? 1 : -1} />
      </div>
    </div>
  );
};

// ---------- 4 Schon am Abend vorher ----------
export const SceneAbend: React.FC = () => {
  const { t, fps } = useT();
  const items = ["Zettel unterschreiben", "Sportzeug einpacken", "Handy laden"];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#E9ECF6" }}>
      <div style={{ position: "absolute", left: 50, top: 40, display: "flex", alignItems: "center", gap: 20, scale: S(sp(t, 0, fps)), transformOrigin: "left center" }}>
        <div style={{ fontSize: 110 }}>🌙</div>
        <div style={{ fontSize: 66, fontWeight: 700, color: NAVY, lineHeight: 1.05 }}>Schon am<br />Abend vorher</div>
      </div>
      <div style={{ position: "absolute", left: 80, right: 60, top: 330, display: "flex", flexDirection: "column", gap: 26 }}>
        {items.map((x, i) => (
          <div key={x} style={{ opacity: fade(t, 0.3 + i * 0.35), translate: `${(1 - fade(t, 0.3 + i * 0.35)) * 40}px 0px`, display: "flex", alignItems: "center", gap: 22, background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: "14px 26px", fontSize: 56, fontWeight: 700 }}>
            <span style={{ color: GREEN }}>✓</span>{x}
          </div>
        ))}
      </div>
    </div>
  );
};

// ---------- 5 Der Konflikt: Zeitleiste 16–19 Uhr ----------
export const SceneKonflikt: React.FC<{ warn: number; training: number; zitat: number }> = ({ warn, training, zitat }) => {
  const { t } = useT();
  const X0 = 90, W = 780; // 15:30 .. 19:30 Uhr
  const x = (h: number) => X0 + ((h - 15.5) / 4) * W;
  const schicht = lin(t, warn, 0.6);
  const tr = lin(t, training, 0.5);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 52, fontWeight: 700, color: RED, opacity: fade(t, 0) }}>Aber dann warnt Claude:</div>
      <div style={{ position: "absolute", left: 40, top: 100, fontSize: 40, fontWeight: 700, color: MUTED }}>Montag</div>
      {[16, 17, 18, 19].map((h) => (
        <div key={h} style={{ position: "absolute", left: x(h) - 50, width: 100, top: 160, textAlign: "center", fontSize: 44, fontWeight: 700, color: INK }}>
          {h}:00
          <div style={{ position: "absolute", left: 48, top: 50, width: 4, height: 330, background: "#E2D6C2" }} />
        </div>
      ))}
      <div style={{ position: "absolute", left: x(16), top: 240, height: 110, width: (x(19) - x(16)) * schicht, background: LGREEN, border: `5px solid ${GREEN}`, borderRadius: 18, overflow: "hidden" }}>
        <div style={{ padding: "18px 22px", fontSize: 48, fontWeight: 700, color: DGREEN, whiteSpace: "nowrap" }}>🛒 Schicht 16–19</div>
      </div>
      <div style={{ position: "absolute", left: x(18.5), top: 380, height: 110, width: (x(19.5) - x(18.5)) * tr, background: "#FCE3CF", border: `5px solid #D9772B`, borderRadius: 18, overflow: "hidden" }}>
        <div style={{ padding: "18px 16px", fontSize: 44, fontWeight: 700, color: "#9A4C12", whiteSpace: "nowrap" }}>⚽ 18:30</div>
      </div>
      <div style={{ position: "absolute", left: x(18.5), top: 230, width: x(19) - x(18.5), height: 270, opacity: tr, background: "repeating-linear-gradient(45deg, rgba(200,71,58,.35) 0 14px, transparent 14px 28px)", border: `5px solid ${RED}`, borderRadius: 10 }} />
      <Pop at={training + 0.5} style={{ position: "absolute", left: 470, top: 510 }}>
        <div style={{ fontSize: 64, fontWeight: 700, color: RED, whiteSpace: "nowrap" }}>⚠ passt nicht</div>
      </Pop>
      <Pop at={zitat} style={{ position: "absolute", left: 40, right: 40, top: 620 }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, overflow: "hidden" }}>
          <ClaudeHead size={28} />
          <div style={{ padding: "14px 24px 20px", fontSize: 40, fontWeight: 600, lineHeight: 1.3 }}>
            „<b style={{ color: RED }}>Achtung, Terminkonflikt:</b> Deine Schicht geht von 16 bis 19 Uhr, das Training beginnt aber schon um 18:30.“
          </div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 6 Geschenk vor der Schicht ----------
export const SceneGeschenk: React.FC<{ vor: number }> = ({ vor }) => {
  const { t, fps } = useT();
  const steps: [string, string, string][] = [
    ["🏫", "Schule", NAVY],
    ["🎁", "Geschenk bis 16 Uhr", GREEN],
    ["🛒", "Schicht 16–19", MUTED],
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 30, textAlign: "center", fontSize: 58, fontWeight: 700, color: NAVY }}>Geschenk für Mama?</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 120, textAlign: "center", fontSize: 150, scale: S(sp(t, 0, fps)) }}>🎁</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", fontSize: 60, fontWeight: 700, color: GREEN, opacity: fade(t, vor) }}>nur vor 16 Uhr!</div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 420, display: "flex", flexDirection: "column", gap: 22 }}>
        {steps.map(([ic, txt, c], i) => {
          const on = i === 1 ? fade(t, vor) : fade(t, 0.2 + i * 0.15);
          return (
            <div key={txt} style={{ opacity: on, display: "flex", alignItems: "center", gap: 22, background: i === 1 ? LGREEN : PAPER, border: `${i === 1 ? 7 : 4}px solid ${i === 1 ? GREEN : INK}`, borderRadius: 20, padding: "12px 26px", fontSize: 54, fontWeight: 700, color: c, scale: i === 1 ? S(0.9 + 0.1 * sp(t, vor, fps)) : "1" }}>
              <span>{ic}</span>{txt}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------- 7 Der Haken: Dienstagabend doppelt belegt ----------
export const SceneHaken: React.FC<{ buch: number; geb: number }> = ({ buch, geb }) => {
  const { t, fps } = useT();
  const tag = (name: string, inner: React.ReactNode, hl = false) => (
    <div style={{ flex: hl ? 2.4 : 1, background: PAPER, border: `${hl ? 7 : 4}px solid ${hl ? RED : INK}`, borderRadius: 20, overflow: "hidden", minHeight: 430 }}>
      <div style={{ background: hl ? RED : "#E7D9C2", color: hl ? "#fff" : INK, fontSize: 40, fontWeight: 700, padding: "8px 16px", textAlign: "center" }}>{name}</div>
      <div style={{ padding: 14, display: "flex", flexDirection: "column", gap: 14 }}>{inner}</div>
    </div>
  );
  const chip = (txt: string, bg: string, a: number) => (
    <div style={{ opacity: a, scale: S(a), background: bg, borderRadius: 14, padding: "12px 14px", fontSize: 42, fontWeight: 700, lineHeight: 1.15 }}>{txt}</div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 52, fontWeight: 700, color: MUTED }}>Der Haken</div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 120, display: "flex", gap: 16, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        {tag("Mo", chip("🛒 Schicht", LGREEN, 1))}
        {tag("Di abend", <>
          {chip("📖 Deutschbuch lesen", "#DCE6F2", sp(t, buch, fps))}
          {chip("🎂 Mama hat Geburtstag", "#FCE3CF", sp(t, geb, fps))}
        </>, true)}
        {tag("Mi", chip("Abgabe Kap. 6", "#EEE", 1))}
      </div>
      <Pop at={geb + 0.35} style={{ position: "absolute", left: 180, top: 600 }}>
        <Stempel size={70} rot={-5} text="DOPPELT BELEGT" />
      </Pop>
      <div style={{ position: "absolute", left: 400, top: 740, fontSize: 36, fontWeight: 600, color: MUTED, opacity: fade(t, geb + 0.7), lineHeight: 1.2 }}>Stand beides in<br />Tims Notizen.</div>
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
      <div style={{ position: "absolute", left: 300, right: 20, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 52, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, zeilen) }}>5 Punkte <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.25) }}>Konflikt erkannt <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, zeilen + 0.5) }}>Dienstagabend doppelt <span style={{ color: RED }}>✗</span></div>
      </div>
    </div>
  );
};

// ---------- 9 Ende: Handy + Kommentar MORGEN ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>🌙</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Briefing-<br />Frage zum<br />Kopieren</div>
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
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>MORGEN</div>
        </div>
      </Pop>
    </div>
  );
};
