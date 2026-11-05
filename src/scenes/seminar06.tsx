import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Seminar06 · S5-Countdown Teil 2 „Noch fünf Tage: Literaturverzeichnis“ · Leinwand 948×1004 · keine Werbung
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFDF8";
const YEL = "#FFE27A";
const CLAUDE = "#D97757"; // nur Farbfläche, kein Logo

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));

// Rohnotizen (Beispiel)
const NOTES = [
  "destatis.de/…/PD26_120_461",
  "zfk d-ticket belebt nahverkehr",
  "Buch Canzler, Mobilität",
  "vdv pressezitat sept 2025",
  "tiktok über d-ticket??",
];

// Fertiges Verzeichnis (echte, geprüfte Quellen, Abruf 05.11.2026)
const LIT = [{ a: "Canzler, W. / Knie, A.:", b: "Die digitale Mobilitätsrevolution. München: oekom 2016." }];
const WEB = [
  { a: "Statistisches Bundesamt:", b: "Fahrgastzahlen nahezu unverändert. PM Nr. 120, 08.04.2026.", abruf: "(Abruf: 05.11.2026)" },
  { a: "VDV:", b: "Pressezitat „Gewissheit bis 2030“, 18.09.2025.", abruf: "(Abruf: 05.11.2026)" },
  { a: "Walk, J.:", b: "Deutschlandticket belebt den Nahverkehr. ZfK, 20.09.2024.", abruf: "(Abruf: 05.11.2026)" },
];

const Calendar: React.FC<{ style?: React.CSSProperties; scale?: number }> = ({ style, scale = 1 }) => (
  <div style={{ position: "absolute", width: 230, background: "#fff", border: `6px solid ${INK}`, borderRadius: 22, overflow: "hidden", scale: String(scale), ...style }}>
    <div style={{ background: RED, color: "#fff", fontSize: 30, fontWeight: 700, textAlign: "center", padding: "4px 0" }}>ABGABE</div>
    <div style={{ fontSize: 40, fontWeight: 700, textAlign: "center", lineHeight: 1.1, padding: "6px 0" }}>
      noch <span style={{ color: RED, fontSize: 64 }}>5</span> Tage
    </div>
  </div>
);

// Fertige Liste als Karte (Form muss in 1 s lesbar sein: Überschriften + Zeilen + Haken)
const ListCard: React.FC<{ style?: React.CSSProperties; size?: number; showWarn?: boolean; abrufGreen?: boolean; az?: boolean; t?: number }> = ({ style, size = 30, showWarn = true, abrufGreen = true, az = false }) => (
  <div style={{ position: "absolute", background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, padding: "20px 26px", boxShadow: "0 14px 0 rgba(58,38,24,.12)", ...style }}>
    <div style={{ fontSize: size * 1.25, fontWeight: 700, display: "flex", alignItems: "center", gap: 12 }}>
      Literaturverzeichnis
      {az && <span style={{ marginLeft: "auto", fontSize: size, background: GREEN, color: "#fff", borderRadius: 10, padding: "2px 12px", border: `3px solid ${INK}` }}>A→Z</span>}
    </div>
    <div style={{ fontSize: size * 0.85, fontWeight: 700, color: NAVY, marginTop: size * 0.4 }}>LITERATUR</div>
    {LIT.map((e) => (
      <div key={e.a} style={{ fontSize: size, lineHeight: 1.2, marginTop: 4 }}>
        <b>{e.a}</b> {e.b}
      </div>
    ))}
    <div style={{ fontSize: size * 0.85, fontWeight: 700, color: NAVY, marginTop: size * 0.5 }}>INTERNETQUELLEN</div>
    {WEB.map((e) => (
      <div key={e.a} style={{ fontSize: size, lineHeight: 1.2, marginTop: 6 }}>
        <b>{e.a}</b> {e.b} <span style={{ color: abrufGreen ? GREEN : INK, fontWeight: 600 }}>{e.abruf}</span>
      </div>
    ))}
    {showWarn && (
      <div style={{ fontSize: size, lineHeight: 1.2, marginTop: 10, background: YEL, borderRadius: 10, padding: "4px 10px", border: `3px solid ${INK}` }}>
        ⚠ „TikTok übers Deutschlandticket“: nicht gefunden, Link nachtragen
      </div>
    )}
  </div>
);

// ---------- 1 Hook: Split-Screen ab Frame 0 (Runde 2: 3 Zettel, Zeigestab tippt auf Zettel, Ring zeichnet sich, Haken ploppt) ----------
const HOOK_NOTES = [
  { n: "zfk d-ticket belebt nahverkehr", x: 20, y: 40, r: -7 },
  { n: "Buch Canzler, Mobilität", x: 50, y: 250, r: 5 },
  { n: "tiktok über d-ticket??", x: 120, y: 450, r: -4 },
];
export const SceneHook: React.FC<{ haufen: number }> = ({ haufen }) => {
  const { t, frame, fps } = useT();
  const wob = t >= haufen && t < haufen + 0.9 ? 1 : 0.35;
  const ring = interpolate(t, [0, 0.6], [0.35, 1], { extrapolateRight: "clamp" });
  const tap = 1 + 0.12 * Math.abs(Math.sin(frame / 5));
  const check = t < 1 ? 0 : sp(t, 1, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 22, textAlign: "center", fontSize: 44, fontWeight: 700 }}>
        Link-Chaos <span style={{ color: GREEN }}>→ Literaturverzeichnis</span>
      </div>
      {/* links: Zettel-Haufen */}
      <div style={{ position: "absolute", left: 10, top: 110, width: 400, height: 640 }}>
        {HOOK_NOTES.map((h, i) => (
          <div key={h.n} style={{ position: "absolute", left: h.x, top: h.y, width: 300, background: YEL, border: `5px solid ${INK}`, borderRadius: 12, padding: "16px 18px", fontSize: 38, fontWeight: 600, lineHeight: 1.15, rotate: `${h.r + Math.sin(frame / 3 + i) * 3 * wob}deg`, boxShadow: "0 8px 0 rgba(58,38,24,.15)" }}>
            {h.n}
          </div>
        ))}
        <svg width={420} height={660} style={{ position: "absolute", left: -10, top: -10 }}>
          <ellipse cx={205} cy={330} rx={195} ry={315} fill="none" stroke={RED} strokeWidth={8} strokeDasharray={1600} strokeDashoffset={1600 * (1 - ring)} strokeLinecap="round" transform="rotate(-4 205 330)" />
        </svg>
      </div>
      {/* Zeigestab-Tipp auf den Zettel */}
      <svg width={948} height={1004} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d="M 440 935 C 420 880, 380 800, 330 700" stroke={RED} strokeWidth={10} fill="none" strokeLinecap="round" strokeDasharray="24 16" />
      </svg>
      <div style={{ position: "absolute", left: 270, top: 640, width: 110, height: 110, borderRadius: 55, border: `8px solid ${RED}`, scale: String(tap) }} />
      {/* Pfeil */}
      <svg width={110} height={110} viewBox="0 0 120 120" style={{ position: "absolute", left: 400, top: 380 }}>
        <path d="M10 60 H95 M70 30 L100 60 L70 90" stroke={GREEN} strokeWidth={16} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {/* rechts: fertige Liste, größer */}
      <ListCard style={{ left: 500, right: 16, top: 100 }} size={25} showWarn={false} />
      <div style={{ position: "absolute", left: 800, top: 720, width: 110, height: 110, borderRadius: 55, background: GREEN, border: `6px solid ${INK}`, color: "#fff", fontSize: 74, fontWeight: 700, display: "grid", placeItems: "center", scale: String(check), opacity: t < 1 ? 0 : 1 }}>✓</div>
      <Calendar style={{ left: 560, top: 800, rotate: `${-5 + Math.sin(frame / 6) * 2}deg` }} />
    </div>
  );
};

// ---------- 2 Chat: alles reinkopieren ----------
export const SceneChat: React.FC<{ canzler: number }> = ({ canzler }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 30, display: "inline-block", background: YEL, border: `4px solid ${INK}`, borderRadius: 12, padding: "2px 16px", fontSize: 30, fontWeight: 700 }}>BEISPIEL</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 100, display: "flex", alignItems: "center", gap: 14, fontSize: 34, fontWeight: 700, color: MUTED }}>
        <div style={{ width: 40, height: 40, borderRadius: 12, background: CLAUDE, border: `4px solid ${INK}` }} />
        Claude · Neuer Chat
      </div>
      <div style={{ position: "absolute", left: 90, right: 40, top: 170, background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: "36px 36px 8px 36px", padding: "26px 32px", scale: String(Math.max(0.7, sp(t, -0.1, fps))) }}>
        <div style={{ fontSize: 42, fontWeight: 700, marginBottom: 14 }}>Mach mir daraus mein Literaturverzeichnis:</div>
        {NOTES.map((n, i) => {
          const hi = i === 2 && t >= canzler;
          return (
            <div key={n} style={{ fontSize: 38, fontWeight: 500, lineHeight: 1.25, marginTop: 8, opacity: fade(t, 0.2 + i * 0.25, 0.2), background: hi ? GREEN : "transparent", borderRadius: 10, padding: "2px 10px" }}>
              • {n}
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, textAlign: "center", fontSize: 46, fontWeight: 700, color: GREEN, opacity: fade(t, canzler) }}>
        Halbe Notizen reichen
      </div>
    </div>
  );
};

// ---------- 3 Merkblatt dazu ----------
export const SceneMerkblatt: React.FC = () => {
  const { t, fps } = useT();
  const s = sp(t, 0.05, fps);
  const y = interpolate(s, [0, 1], [500, 0]);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF3FA" }}>
      <div style={{ position: "absolute", left: 200, top: 120, width: 548, height: 680, background: "#fff", border: `7px solid ${INK}`, borderRadius: 24, translate: `0px ${y}px`, rotate: "-3deg", padding: "36px 40px", boxShadow: "0 18px 0 rgba(58,38,24,.12)" }}>
        <div style={{ fontSize: 30, fontWeight: 700, color: "#fff", background: RED, display: "inline-block", borderRadius: 10, padding: "2px 14px" }}>PDF</div>
        <div style={{ fontSize: 58, fontWeight: 700, marginTop: 20, lineHeight: 1.1 }}>Merkblatt Seminararbeit</div>
        {["Zitierweise", "Literaturverzeichnis", "Seitenränder", "Schrift & Abstand"].map((x, i) => (
          <div key={x} style={{ fontSize: 40, fontWeight: 500, marginTop: 22, color: MUTED, display: "flex", gap: 14, opacity: fade(t, 0.3 + i * 0.15, 0.2) }}>
            <span style={{ color: GREEN }}>✓</span> {x}
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, textAlign: "center", fontSize: 50, fontWeight: 700, opacity: fade(t, 0.4) }}>
        + Merkblatt deiner Schule
      </div>
    </div>
  );
};

// ---------- 4 Ein Eintrag, Felder markiert ----------
const FIELDS = [
  { k: "Autor", v: "Canzler, Weert / Knie, Andreas:", c: "#FFD7CF" },
  { k: "Titel", v: "Die digitale Mobilitätsrevolution.", c: "#DDF3E6" },
  { k: "Verlag", v: "München: oekom", c: "#DCE6F5" },
  { k: "Jahr", v: "2016.", c: YEL },
];
export const SceneEintrag: React.FC<{ marks: number[]; format: number }> = ({ marks, format }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 40, display: "flex", alignItems: "center", gap: 14, fontSize: 34, fontWeight: 700, color: MUTED }}>
        <div style={{ width: 40, height: 40, borderRadius: 12, background: CLAUDE, border: `4px solid ${INK}` }} />
        Claude
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 110, background: "#fff", border: `6px solid ${INK}`, borderRadius: 30, padding: "26px 30px", fontSize: 30, color: MUTED, fontWeight: 600 }}>
        Notiz: <span style={{ background: YEL, borderRadius: 8, padding: "0 8px", color: INK }}>„Buch Canzler, Mobilität“</span> → gefunden:
      </div>
      {FIELDS.map((f, i) => {
        const s = sp(t, marks[i], fps);
        return (
          <div key={f.k} style={{ position: "absolute", left: 60, right: 60, top: 270 + i * 140, display: "flex", alignItems: "center", gap: 20, opacity: t < marks[i] ? 0.15 : 1, scale: String(0.9 + 0.1 * s) }}>
            <div style={{ width: 170, fontSize: 36, fontWeight: 700, color: NAVY, textAlign: "right" }}>{f.k}</div>
            <div style={{ flex: 1, background: f.c, border: `5px solid ${INK}`, borderRadius: 18, padding: "14px 20px", fontSize: 40, fontWeight: 600 }}>{f.v}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, textAlign: "center", opacity: fade(t, format) }}>
        <span style={{ fontSize: 46, fontWeight: 700, color: "#fff", background: GREEN, border: `5px solid ${INK}`, borderRadius: 20, padding: "8px 26px" }}>✓ Format wie im Merkblatt</span>
      </div>
    </div>
  );
};

// ---------- 5 Die ganze Liste ----------
export const SceneListe: React.FC<{ az: number }> = ({ az }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF7F1" }}>
      <div style={{ scale: String(Math.max(0.8, sp(t, -0.1, fps))) }}>
        <ListCard style={{ left: 36, right: 36, top: 60 }} size={36} showWarn={false} az={t >= az} />
      </div>
    </div>
  );
};

// ---------- 6 Aber: eine Notiz nicht gefunden ----------
export const SceneAber: React.FC<{ findet: number; gelb: number }> = ({ findet, gelb }) => {
  const { t, fps, frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      <div style={{ position: "absolute", left: 60, right: 60, top: 60, background: YEL, border: `6px solid ${INK}`, borderRadius: 16, padding: "24px 28px", fontSize: 56, fontWeight: 600, rotate: "-3deg" }}>
        „tiktok über d-ticket??“
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 260, textAlign: "center", fontSize: 140, opacity: fade(t, 0.3) }}>🔍</div>
      <Pop at={findet} style={{ position: "absolute", left: 0, right: 0, top: 440, textAlign: "center" }}>
        <span style={{ fontSize: 72, fontWeight: 700, color: RED }}>nicht gefunden</span>
      </Pop>
      <div style={{ position: "absolute", left: 50, right: 50, top: 600, opacity: fade(t, gelb), scale: String(Math.max(0.6, sp(t, gelb, fps))) }}>
        <div style={{ background: YEL, border: `6px solid ${INK}`, borderRadius: 18, padding: "20px 24px", fontSize: 42, fontWeight: 600, lineHeight: 1.2 }}>
          ⚠ „TikTok übers Deutschlandticket“: nicht gefunden, Link nachtragen
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 30, marginTop: 30 }}>
          <span style={{ fontSize: 54, fontWeight: 700, color: GREEN, border: `6px solid ${GREEN}`, borderRadius: 16, padding: "2px 20px", rotate: `${-4 + Math.sin(frame / 5) * 1.5}deg` }}>markiert ✓</span>
          <span style={{ fontSize: 54, fontWeight: 700, color: RED, border: `6px solid ${RED}`, borderRadius: 16, padding: "2px 20px", rotate: "4deg" }}>erfunden ✗</span>
        </div>
      </div>
    </div>
  );
};

// ---------- 7 Pointe: fertig ----------
export const ScenePointe: React.FC<{ fertig: number }> = ({ fertig }) => {
  const { t, fps } = useT();
  const s = sp(t, fertig, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF7F1" }}>
      <ListCard style={{ left: 30, right: 30, top: 40 }} size={36} showWarn={false} az />
      <Calendar style={{ left: 40, top: 790, rotate: "-6deg" }} />
      <div style={{ position: "absolute", left: 330, top: 760, scale: String(s), rotate: "-8deg", border: `10px solid ${GREEN}`, color: GREEN, borderRadius: 26, padding: "6px 34px", fontSize: 120, fontWeight: 700, background: "rgba(255,255,255,.92)" }}>FERTIG</div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar-Wort ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 820, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 80 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 110 }}>📋</div>
          <div style={{ fontSize: 40, fontWeight: 700, textAlign: "center", lineHeight: 1.15 }}>Mein Prompt<br />zum Kopieren</div>
          {[0, 1, 2, 3].map((i) => {
            const tt = (frame - i * 9) / fps;
            const y = interpolate(tt % 1.6, [0, 1.6], [0, -300]);
            const o = interpolate(tt % 1.6, [0, 0.2, 1.3, 1.6], [0, 1, 1, 0]);
            return (
              <svg key={i} width={50} height={50} viewBox="0 0 24 24" style={{ position: "absolute", right: 20 + (i % 2) * 28, bottom: 40, translate: `0px ${y}px`, opacity: tt < 0 ? 0 : o }}>
                <path d="M12 21s-7-4.5-9.5-9C.7 8.6 2.6 4 6.6 4c2.1 0 3.6 1.2 4.4 2.5C11.8 5.2 13.3 4 15.4 4c4 0 5.9 4.6 4.1 8-2.5 4.5-9.5 9-9.5 9z" fill="#E05A47" />
              </svg>
            );
          })}
        </div>
      </div>
      <Pop at={commentAt} style={{ position: "absolute", left: 60, bottom: 60 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "20px 36px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 96, fontWeight: 600, color: INK, letterSpacing: 4 }}>QUELLEN</div>
        </div>
      </Pop>
    </div>
  );
};
