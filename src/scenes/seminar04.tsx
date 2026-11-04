import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// T4 · „Lass Claude deine Seminararbeit prüfen – nicht schreiben“ · Leinwand 948×1004
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFDF8";
const CLAUDE = "#D97757"; // nur Farbfläche, kein Logo

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));

const GLIEDERUNG = ["1 Einleitung", "2 Geschichte des ÖPNV seit 1950", "3 Das Deutschlandticket", "4 Umfrage unter Pendlern", "5 Fazit"];

// Chat-Karte mit der echten Claude-Antwort (zur Beispiel-Gliederung)
const ClaudeCard: React.FC<{ style?: React.CSSProperties; size?: number }> = ({ style, size = 44 }) => (
  <div style={{ position: "absolute", background: "#fff", border: `6px solid ${INK}`, borderRadius: 30, padding: "22px 30px", boxShadow: "0 14px 0 rgba(58,38,24,.12)", ...style }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 30, fontWeight: 700, color: MUTED }}>
      <div style={{ width: 40, height: 40, borderRadius: 12, background: CLAUDE, border: `4px solid ${INK}` }} />
      Claude · Gliederungs-Check
    </div>
    <div style={{ fontSize: size, fontWeight: 600, lineHeight: 1.2, marginTop: 12 }}>
      <span style={{ background: "#FFD7CF", color: RED, borderRadius: 10, padding: "0 8px" }}>Kapitel 2</span> beantwortet deine Forschungsfrage nicht – kürzen oder streichen.
    </div>
    <div style={{ fontSize: size * 0.78, fontWeight: 500, lineHeight: 1.2, marginTop: 10, color: MUTED }}>In Kapitel 4 fehlt der Vergleich vorher/nachher.</div>
  </div>
);

// ---------- Hook: steht ab Frame 0 ----------
export const SceneHook: React.FC<{ pruefen: number; schreiben: number }> = ({ pruefen, schreiben }) => {
  const { t, frame, fps } = useT();
  const shake = frame < 18 ? Math.sin(frame * 2.2) * (18 - frame) * 0.9 : 0;
  const pulse = 1 + 0.03 * Math.sin(frame / 4);
  const s1 = sp(t, pruefen, fps);
  const s2 = sp(t, schreiben, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      {/* Kalenderblatt */}
      <div style={{ position: "absolute", left: 40, top: 36, width: 250, background: "#fff", border: `6px solid ${INK}`, borderRadius: 22, overflow: "hidden", rotate: `${-6 + Math.sin(frame / 6) * 2}deg`, translate: `${shake}px 0px`, scale: String(pulse) }}>
        <div style={{ background: RED, color: "#fff", fontSize: 34, fontWeight: 700, textAlign: "center", padding: "6px 0" }}>ABGABE</div>
        <div style={{ fontSize: 96, fontWeight: 700, textAlign: "center", lineHeight: 1.15 }}>10.11.</div>
      </div>
      <div style={{ position: "absolute", left: 320, top: 60, right: 30, fontSize: 60, fontWeight: 700, lineHeight: 1.1 }}>
        Claude <span style={{ color: GREEN }}>prüft</span> deine Seminararbeit.
      </div>
      <svg width={948} height={1004} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d="M 445 1000 C 470 910, 500 850, 520 795" stroke={RED} strokeWidth={14} fill="none" strokeLinecap="round" strokeDasharray="30 20" />
        <path d="M 478 812 L 522 780 L 548 828" stroke={RED} strokeWidth={14} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <ClaudeCard style={{ left: 40, right: 40, top: 330 }} size={50} />
      {/* Ring um „Kapitel 2“ + Pfeil vom Zeigestab des Hamsters (ab Frame 0) */}
      <div style={{ position: "absolute", left: 52, top: 414, width: 284, height: 78, border: `8px solid ${RED}`, borderRadius: 999, rotate: "-3deg", scale: String(1 + 0.04 * Math.sin(frame / 3)) }} />
      <div style={{ position: "absolute", left: 40, right: 40, top: 760, display: "flex", justifyContent: "space-around" }}>
        <div style={{ scale: String(s1), rotate: "-5deg", border: `7px solid ${GREEN}`, color: GREEN, borderRadius: 18, padding: "4px 22px", fontSize: 64, fontWeight: 700, background: "rgba(255,255,255,.9)" }}>PRÜFEN ✓</div>
        <div style={{ scale: String(s2), rotate: "5deg", border: `7px solid ${RED}`, color: RED, borderRadius: 18, padding: "4px 22px", fontSize: 64, fontWeight: 700, background: "rgba(255,255,255,.9)" }}>SCHREIBEN ✗</div>
      </div>
    </div>
  );
};

// ---------- Beispiel-Gliederung, Kapitel 2 fliegt raus ----------
export const SceneBeispiel: React.FC<{ kap: number; frage: number }> = ({ kap, frage }) => {
  const { t, fps } = useT();
  const strike = interpolate(t, [kap, kap + 0.4], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 60, right: 60, top: 40, height: 860, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "30px 40px", scale: String(Math.max(0.85, sp(t, -0.1, fps))) }}>
        <div style={{ display: "inline-block", background: "#FFE27A", border: `4px solid ${INK}`, borderRadius: 12, padding: "2px 16px", fontSize: 30, fontWeight: 700 }}>BEISPIEL</div>
        <div style={{ fontSize: 30, color: MUTED, fontWeight: 700, marginTop: 18 }}>FORSCHUNGSFRAGE</div>
        <div style={{ fontSize: 42, fontWeight: 600, lineHeight: 1.15, marginTop: 4, padding: "4px 10px", borderRadius: 12, background: t >= frage ? "#DDF3E6" : "transparent" }}>
          Wie hat das Deutschlandticket das Pendeln nach Regensburg verändert?
        </div>
        <div style={{ fontSize: 30, color: MUTED, fontWeight: 700, marginTop: 26 }}>GLIEDERUNG</div>
        {GLIEDERUNG.map((g, i) => {
          const bad = i === 1;
          return (
            <div key={g} style={{ position: "relative", marginTop: 14, fontSize: 44, fontWeight: bad && t >= kap ? 700 : 500, color: bad && t >= kap ? RED : INK, opacity: fade(t, 0.05 + i * 0.1, 0.2) }}>
              {g}
              {bad && <div style={{ position: "absolute", left: 0, top: "52%", height: 7, width: `${strike}%`, background: RED, borderRadius: 4 }} />}
            </div>
          );
        })}
      </div>
      <Pop at={kap + 0.3} style={{ position: "absolute", left: 120, top: 830 }}>
        <div style={{ background: RED, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 30px", fontSize: 40, fontWeight: 600, whiteSpace: "nowrap" }}>
          passt nicht zur Forschungsfrage
        </div>
      </Pop>
    </div>
  );
};

// ---------- Projekt anlegen + Dateien hochladen ----------
const FILES = [
  { name: "Seminararbeit.docx", icon: "📄" },
  { name: "Merkblatt Schule.pdf", icon: "📋" },
  { name: "Quellen", icon: "📚" },
];
export const SceneProjekt: React.FC<{ projekt: number; files: number[] }> = ({ projekt, files }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Pop at={projekt} style={{ position: "absolute", left: 70, right: 70, top: 50 }}>
        <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: 26, padding: "22px 30px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 30, fontWeight: 700, color: MUTED }}>
            <div style={{ width: 36, height: 36, borderRadius: 10, background: CLAUDE, border: `4px solid ${INK}` }} />
            Claude · Neues Projekt
          </div>
          <div style={{ fontSize: 58, fontWeight: 700, marginTop: 8 }}>📁 Seminararbeit</div>
        </div>
      </Pop>
      {FILES.map((f, i) => {
        const s = sp(t, files[i], fps);
        const y = interpolate(s, [0, 1], [260, 0]);
        return (
          <div key={f.name} style={{ position: "absolute", left: 110, right: 110, top: 300 + i * 190, opacity: t < files[i] ? 0 : 1, translate: `0px ${y}px`, display: "flex", alignItems: "center", gap: 24, background: PAPER, border: `5px solid ${INK}`, borderRadius: 26, padding: "30px 32px", fontSize: 56, fontWeight: 600 }}>
            <span style={{ fontSize: 76 }}>{f.icon}</span>
            {f.name}
            <span style={{ marginLeft: "auto", color: GREEN, fontSize: 50, opacity: fade(t, files[i] + 0.4) }}>✓</span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 830, textAlign: "center", fontSize: 44, fontWeight: 600, color: MUTED, opacity: fade(t, files[2] + 0.3) }}>
        Tipp: Name &amp; Schule vorher rausnehmen
      </div>
    </div>
  );
};

// ---------- „3 Fragen“ ----------
export const SceneDrei: React.FC = () => {
  const { t, fps } = useT();
  const s = sp(t, 0, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6", display: "grid", placeItems: "center" }}>
      <div style={{ textAlign: "center", scale: String(s) }}>
        <div style={{ fontSize: 300, fontWeight: 700, color: RED, lineHeight: 1 }}>3</div>
        <div style={{ fontSize: 90, fontWeight: 700 }}>Fragen</div>
      </div>
    </div>
  );
};

// Nutzerfrage als Chat-Blase + Nummer
const Ask: React.FC<{ n: number; children: React.ReactNode }> = ({ n, children }) => {
  const { t, fps } = useT();
  return (
    <>
      <div style={{ position: "absolute", left: 40, top: 36, width: 110, height: 110, borderRadius: 55, background: RED, color: "#fff", border: `6px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 72, fontWeight: 700, scale: String(Math.max(0.6, sp(t, -0.1, fps))) }}>{n}</div>
      <div style={{ position: "absolute", left: 180, right: 40, top: 40, background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: "36px 36px 8px 36px", padding: "22px 30px", fontSize: 50, fontWeight: 600, lineHeight: 1.15, opacity: fade(t, 0.05, 0.2) }}>
        {children}
      </div>
    </>
  );
};

export const SceneF1: React.FC<{ ok: number }> = ({ ok }) => {
  const { t } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Ask n={1}>Passt meine Gliederung zur Forschungsfrage?</Ask>
      <div style={{ position: "absolute", left: 120, right: 120, top: 360, background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: "16px 30px" }}>
        {GLIEDERUNG.map((g, i) => (
          <div key={g} style={{ fontSize: 40, fontWeight: 500, marginTop: 10, display: "flex", justifyContent: "space-between", opacity: fade(t, 0.2 + i * 0.1, 0.2) }}>
            <span>{g.split(" ").slice(0, 3).join(" ")}</span>
            <span style={{ color: i === 1 ? RED : GREEN, fontWeight: 700, opacity: fade(t, ok + i * 0.12, 0.15) }}>{i === 1 ? "✗" : "✓"}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export const SceneF2: React.FC<{ quelle: number }> = ({ quelle }) => {
  const { t } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Ask n={2}>Welche Zitate soll ich nochmal mit der Quelle vergleichen?</Ask>
      <div style={{ position: "absolute", left: 50, top: 440, width: 380, height: 360, background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: 24 }}>
        <div style={{ fontSize: 32, fontWeight: 700, color: MUTED }}>DEINE ARBEIT</div>
        <div style={{ fontSize: 46, fontWeight: 600, marginTop: 14, lineHeight: 1.2 }}>„… rund 30 % mehr Fahrgäste …“<sup>12</sup></div>
      </div>
      <div style={{ position: "absolute", right: 50, top: 440, width: 380, height: 360, background: PAPER, border: `5px solid ${INK}`, borderRadius: 20, padding: 24, opacity: fade(t, quelle) }}>
        <div style={{ fontSize: 32, fontWeight: 700, color: MUTED }}>QUELLE</div>
        <div style={{ fontSize: 46, fontWeight: 600, marginTop: 14, lineHeight: 1.2 }}>„… rund 13 % mehr Fahrgäste …“</div>
      </div>
      <Pop at={quelle + 0.4} style={{ position: "absolute", left: 404, top: 560 }}>
        <div style={{ width: 140, height: 140, borderRadius: 70, background: "#FFE27A", border: `6px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 50 }}>🔍</div>
      </Pop>
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, textAlign: "center", fontSize: 40, fontWeight: 600, color: MUTED, opacity: fade(t, quelle + 0.6) }}>
        Beispiel · selbst nachschauen musst du trotzdem
      </div>
    </div>
  );
};

export const SceneF3: React.FC<{ frage: number }> = ({ frage }) => (
  <div style={{ position: "absolute", inset: 0, background: CREAM }}>
    <Ask n={3}>Frag mich ab wie im Prüfungsgespräch.</Ask>
    <Pop at={frage} style={{ position: "absolute", left: 60, right: 60, top: 380 }}>
      <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: "36px 36px 36px 8px", padding: "24px 30px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 30, fontWeight: 700, color: MUTED }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: CLAUDE, border: `4px solid ${INK}` }} />
          Claude
        </div>
        <div style={{ fontSize: 50, fontWeight: 600, lineHeight: 1.2, marginTop: 10 }}>Warum hast du gerade Pendler in Regensburg befragt?</div>
      </div>
    </Pop>
    <Pop at={frage + 0.8} style={{ position: "absolute", left: 300, top: 760 }}>
      <div style={{ fontSize: 120 }}>🎤</div>
    </Pop>
  </div>
);

// ---------- Regel: „Aber vorher“ ----------
export const SceneRegel: React.FC<{ lehrkraft: number; angeben: number }> = ({ lehrkraft, angeben }) => {
  const rows = [
    { at: lehrkraft, icon: "🧑‍🏫", text: "Lehrkraft fragen: Claude erlaubt?" },
    { at: angeben, icon: "📝", text: "In der Arbeit angeben, wofür" },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      <div style={{ position: "absolute", left: 60, top: 60, fontSize: 80, fontWeight: 700 }}>Aber <span style={{ color: RED }}>vorher</span>:</div>
      {rows.map((r, i) => (
        <Pop key={r.text} at={r.at} style={{ position: "absolute", left: 60, right: 60, top: 250 + i * 290 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 26, background: "#fff", border: `6px solid ${INK}`, borderRadius: 26, padding: "40px 34px", fontSize: 62, fontWeight: 600, lineHeight: 1.1 }}>
            <span style={{ fontSize: 96 }}>{r.icon}</span>
            {r.text}
          </div>
        </Pop>
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 50, textAlign: "center", fontSize: 46, color: MUTED, fontWeight: 500 }}>Claude-Konto ab 18</div>
    </div>
  );
};

// ---------- Pointe: Claude findet, du reparierst ----------
export const ScenePointe: React.FC<{ reparieren: number }> = ({ reparieren }) => {
  const { t, fps } = useT();
  const s = sp(t, reparieren, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <ClaudeCard style={{ left: 50, right: 50, top: 60, scale: String(Math.max(0.8, sp(t, -0.1, fps))) }} size={46} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 520, textAlign: "center", fontSize: 54, fontWeight: 700, color: MUTED, opacity: fade(t, 0.1) }}>Claude findet's.</div>
      <div style={{ position: "absolute", left: 80, right: 80, top: 620, scale: String(s), rotate: "-3deg", background: GREEN, color: "#fff", border: `7px solid ${INK}`, borderRadius: 30, padding: "26px 20px", textAlign: "center", fontSize: 84, fontWeight: 700 }}>
          Reparieren: DU ✍️
      </div>
    </div>
  );
};

// ---------- Schluss: Handy mit Kommentar „SEMINAR“ ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 820, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column" }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 110 }}>📋</div>
          <div style={{ fontSize: 40, fontWeight: 700, textAlign: "center", lineHeight: 1.15 }}>3 Prompts<br />zum Kopieren</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 60, bottom: 70 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "20px 36px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 96, fontWeight: 600, color: INK, letterSpacing: 4 }}>SEMINAR</div>
        </div>
      </Pop>
    </div>
  );
};
