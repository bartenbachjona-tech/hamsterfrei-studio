import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Seminar10 · S2-F „Abgegeben? Jetzt kommt das Prüfungsgespräch“ · ohne Werbung · Leinwand 948×1004
// Zeiten in den Props sind Sekunden ab Szenenstart.
const RED = "#C8473A";
const YEL = "#D9A32B";
const MUTED = "#6B5444";
const SAND = "#F5EAD7";
const PAPER = "#FFFFFF";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.25) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));

const ClaudeHead: React.FC<{ right?: React.ReactNode }> = ({ right }) => (
  <div style={{ height: 90, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 34px", fontSize: 38, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);
const RoleTag: React.FC = () => (
  <span style={{ background: NAVY, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>🧑‍🏫 spielt deine Lehrkraft</span>
);
const Beispiel: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <div style={{ position: "absolute", background: SAND, color: MUTED, border: `3px solid ${MUTED}`, borderRadius: 10, padding: "2px 12px", fontSize: 24, fontWeight: 700, letterSpacing: 2, ...style }}>BEISPIEL</div>
);

const Typed: React.FC<{ text: string; start: number; dur: number }> = ({ text, start, dur }) => {
  const { t } = useT();
  const n = Math.floor(interpolate(t, [start, start + dur], [0, text.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <span>
      {text.slice(0, n)}
      {n < text.length && t >= start && <span style={{ opacity: Math.floor(t * 4) % 2 ? 1 : 0 }}>|</span>}
    </span>
  );
};

const FrageBlase: React.FC<{ size?: number; nr?: string }> = ({ size = 62, nr = "Frage 3 von 10" }) => (
  <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: "34px 34px 34px 8px", padding: "20px 32px", boxShadow: "0 12px 0 rgba(58,38,24,.12)" }}>
    <div style={{ fontSize: 30, fontWeight: 700, color: NAVY, letterSpacing: 1 }}>{nr}</div>
    <div style={{ fontSize: size, fontWeight: 700, lineHeight: 1.12 }}>„Warum hast du nur deinen eigenen Kurs befragt?“</div>
  </div>
);
const Wackelt: React.FC<{ wob?: number }> = ({ wob = 0 }) => (
  <div style={{ background: "#FFF4D6", color: "#8A6210", border: `6px solid ${YEL}`, borderRadius: 24, padding: "12px 30px", fontSize: 58, fontWeight: 700, rotate: `${wob}deg` }}>⚠ Antwort wackelt</div>
);

// ---------- 1 Hook: Arbeit ABGEGEBEN + Prüfungsfrage, ab Frame 0 ----------
export const SceneHook: React.FC<{ durch: number; pg: number }> = ({ durch, pg }) => {
  const { t, frame } = useT();
  const shake = t >= durch && t < durch + 0.6 ? Math.sin(frame * 1.6) * 5 : 0;
  const ring = interpolate(t, [0.1, 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      {/* Overlay = Hook mit Suchbegriff */}
      <div style={{ position: "absolute", left: 20, right: 20, top: 26, textAlign: "center", fontSize: 70, fontWeight: 700, lineHeight: 1.08, color: NAVY }}>
        Abgegeben? Jetzt kommt das <span style={{ color: RED }}>Prüfungsgespräch.</span>
      </div>
      {/* Arbeit mit Stempel */}
      <div style={{ position: "absolute", left: 40, top: 250, width: 330, height: 420, rotate: "-5deg" }}>
        {[2, 1, 0].map((i) => (
          <div key={i} style={{ position: "absolute", left: i * 12, top: i * 12, width: 300, height: 390, background: PAPER, border: `6px solid ${INK}`, borderRadius: 18 }} />
        ))}
        <div style={{ position: "absolute", left: 22, top: 40, width: 260, fontSize: 36, fontWeight: 700, textAlign: "center" }}>Seminararbeit</div>
        {[0, 1, 2, 3, 4].map((r) => <div key={r} style={{ position: "absolute", left: 40, top: 120 + r * 40, height: 14, width: 220 - r * 18, background: "#E3D8C6", borderRadius: 6 }} />)}
        <div style={{ position: "absolute", left: 4, top: 230, border: `8px solid ${GREEN}`, color: GREEN, background: "rgba(255,255,255,.92)", borderRadius: 16, padding: "2px 14px", fontSize: 46, fontWeight: 700, rotate: `${-12 + shake}deg`, whiteSpace: "nowrap" }}>ABGEGEBEN ✓</div>
      </div>
      {/* Prüfungsfrage + Bewertung */}
      <div style={{ position: "absolute", left: 400, right: 30, top: 230 }}>
        <div style={{ fontSize: 30, fontWeight: 700, color: MUTED, marginBottom: 22, marginTop: -12, display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 20, height: 20, borderRadius: 10, background: "#E5835E" }} /> Claude · spielt Lehrkraft
        </div>
        <div style={{ position: "relative" }}>
          <FrageBlase size={52} />
          <div style={{ position: "absolute", left: -8, right: -8, top: -8, bottom: -8, border: `7px solid ${RED}`, borderRadius: 46, opacity: ring, scale: String(1.08 - ring * 0.08) }} />
        </div>
        <div style={{ marginTop: 30, display: "flex", justifyContent: "center" }}>
          <Wackelt wob={Math.sin(frame / 5) * 2} />
        </div>
      </div>
      <Beispiel style={{ left: 40, top: 690 }} />
      {/* Banner Prüfungsgespräch */}
      <Pop at={pg} style={{ position: "absolute", left: 0, right: 0, top: 840, display: "flex", justifyContent: "center" }}>
        <div style={{ background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "8px 30px", fontSize: 50, fontWeight: 700, letterSpacing: 2 }}>🧑‍🏫 PRÜFUNGSGESPRÄCH</div>
      </Pop>
    </div>
  );
};

// ---------- 2 Fragen zu deiner eigenen Arbeit: 6 Fragenfelder ----------
const FELDER = ["📌 Fachliches", "🗂️ Arbeitsprozess", "🤖 KI-Gebrauch", "📊 Ergebnisse", "🔎 konkrete Stellen", "🔭 Transfer"];
export const SceneFelder: React.FC<{ eigene: number }> = ({ eigene }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 40, fontSize: 60, fontWeight: 700, lineHeight: 1.1 }}>
        Fragen zu <span style={{ color: RED, textDecoration: t >= eigene ? "underline" : "none", textDecorationThickness: 8 }}>deiner eigenen</span> Arbeit
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 230, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22 }}>
        {FELDER.map((f, i) => (
          <div key={f} style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: "26px 22px", fontSize: 44, fontWeight: 700, scale: String(Math.max(0.0001, sp(t, 0.1 + i * 0.12, fps))) }}>{f}</div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, bottom: 40, fontSize: 30, fontWeight: 600, color: MUTED, opacity: fade(t, 0.8) }}>Fragenfelder laut oberstufe.bayern.de</div>
    </div>
  );
};

// ---------- 3 Claude spielt die Lehrkraft ----------
export const SceneRolle: React.FC = () => {
  const { t, fps } = useT();
  const s = sp(t, 0.15, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 40 }}>
      <div style={{ position: "relative", width: 300, height: 300, borderRadius: 150, background: "#E5835E", border: `8px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 80, fontWeight: 700, color: "#fff" }}>
        Claude
        <div style={{ position: "absolute", top: -40, left: 75, fontSize: 130, translate: `0px ${(1 - s) * -260}px`, opacity: s }}>👓</div>
      </div>
      <div style={{ scale: String(Math.max(0.0001, sp(t, 0.5, fps))), background: PAPER, border: `6px solid ${INK}`, borderRadius: 20, padding: "14px 36px", fontSize: 60, fontWeight: 700 }}>
        Lehrkraft <span style={{ color: MUTED, fontSize: 44 }}>(gespielt)</span>
      </div>
    </div>
  );
};

// ---------- 4 Chat: Arbeit hochladen + Prompt ----------
export const SceneChat: React.FC<{ datei: number; text: number }> = ({ datei, text }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", right: 40, top: 150, scale: String(Math.max(0.0001, sp(t, datei, fps))), transformOrigin: "right top" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 22, background: SAND, border: `6px solid ${INK}`, borderRadius: 26, padding: "22px 30px", fontSize: 48, fontWeight: 700 }}>
          <div style={{ width: 76, height: 96, background: RED, borderRadius: 12, color: "#fff", display: "grid", placeItems: "center", fontSize: 34, fontWeight: 700 }}>PDF</div>
          Seminararbeit_BEISPIEL.pdf
        </div>
      </div>
      {t >= text - 0.2 && (
        <div style={{ position: "absolute", right: 40, top: 380, maxWidth: 840, background: "#F1E6D3", borderRadius: 34, padding: "26px 36px", fontSize: 64, fontWeight: 700, lineHeight: 1.15, opacity: fade(t, text - 0.2, 0.2) }}>
          <Typed text="Stell mir 10 Prüfungsfragen zu meiner Arbeit. Eine nach der anderen." start={text - 0.2} dur={2.6} />
        </div>
      )}
    </div>
  );
};

// ---------- 5 Themen der Fragen ----------
const CHIPS = ["📌 Thema", "📚 Quellen", "🧪 Methode", "🤖 KI"];
export const SceneThemen: React.FC<{ at: number[] }> = ({ at }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<RoleTag />} />
      <div style={{ position: "absolute", left: 40, right: 40, top: 140, fontSize: 54, fontWeight: 700 }}>Claude fragt nach …</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 260, display: "flex", flexDirection: "column", gap: 26 }}>
        {CHIPS.map((c, i) => (
          <div key={c} style={{ alignSelf: i % 2 ? "flex-end" : "flex-start", background: i === 3 ? NAVY : PAPER, color: i === 3 ? "#fff" : INK, border: `6px solid ${INK}`, borderRadius: 999, padding: "16px 44px", fontSize: 70, fontWeight: 700, scale: String(Math.max(0.0001, sp(t, at[i], fps))) }}>{c}</div>
        ))}
      </div>
    </div>
  );
};

// ---------- 6 Die Frage ----------
export const SceneFrage: React.FC = () => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<RoleTag />} />
      <div style={{ position: "absolute", left: 40, right: 60, top: 220, scale: String(Math.max(0.0001, sp(t, 0, fps))), transformOrigin: "left top" }}>
        <FrageBlase size={78} />
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 720, fontSize: 42, fontWeight: 700, color: INK, opacity: fade(t, 0.5) }}>Beispielarbeit: „Das Deutschlandticket: Hat es das Pendeln in Regensburg verändert?“</div>
      <Beispiel style={{ right: 40, top: 120 }} />
    </div>
  );
};

// ---------- 7 Antwort → wackelt ----------
export const SceneAntwort: React.FC<{ wackelt: number }> = ({ wackelt }) => {
  const { frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<RoleTag />} />
      <div style={{ position: "absolute", left: 40, right: 140, top: 130, opacity: 0.55 }}>
        <FrageBlase size={44} />
      </div>
      <div style={{ position: "absolute", right: 40, top: 460, maxWidth: 760, background: "#F1E6D3", borderRadius: 34, padding: "24px 36px", fontSize: 66, fontWeight: 700, lineHeight: 1.15 }}>
        <Typed text="Weil das am einfachsten war." start={0.05} dur={1.0} />
      </div>
      <Pop at={wackelt} style={{ position: "absolute", left: 40, top: 720 }}>
        <Wackelt wob={Math.sin(frame / 3) * 3} />
      </Pop>
      <Beispiel style={{ right: 40, top: 650 }} />
    </div>
  );
};

// ---------- 8 Rückmeldung ----------
export const SceneFeedback: React.FC<{ wie: number; ergebnis: number }> = ({ wie, ergebnis }) => {
  const { t } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<RoleTag />} />
      <div style={{ position: "absolute", left: 40, right: 40, top: 140, background: PAPER, border: `6px solid ${YEL}`, borderRadius: 30, padding: "26px 34px" }}>
        <div style={{ fontSize: 72, fontWeight: 700, color: "#8A6210" }}>⚠ Zu allgemein.</div>
        <div style={{ fontSize: 50, fontWeight: 600, lineHeight: 1.25, marginTop: 14 }}>
          <span style={{ background: t >= wie ? "#FFE9A8" : "transparent" }}>Nenn, wie viele du befragt hast</span> (z. B. 18 aus deinem Kurs), und sag,{" "}
          <span style={{ background: t >= ergebnis ? "#FFE9A8" : "transparent" }}>was das für dein Ergebnis heißt:</span> Berufspendler fehlen.
        </div>
      </div>
      <Pop at={wie + 0.4} style={{ position: "absolute", left: 40, right: 40, top: 680 }}>
        <div style={{ background: "#E3F1EA", border: `5px solid ${GREEN}`, borderRadius: 24, padding: "16px 28px", fontSize: 46, fontWeight: 700, color: "#1C7049" }}>Fehlt noch: Wie viele? Was heißt das fürs Ergebnis?</div>
      </Pop>
      <Beispiel style={{ right: 40, top: 900 }} />
    </div>
  );
};

// ---------- 9 Ehrlich: Lehrkraft fragt vielleicht anders, aber Schwachstelle gefunden ----------
export const SceneEhrlich: React.FC<{ aber: number }> = ({ aber }) => {
  const { t, fps } = useT();
  const ring = interpolate(t, [aber, aber + 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 60, right: 60, top: 80, background: PAPER, border: `6px solid ${NAVY}`, borderRadius: 26, padding: "22px 30px", fontSize: 56, fontWeight: 700, color: NAVY, rotate: "-2deg", opacity: 1 - fade(t, aber, 0.4) * 0.3 }}>
        🧑‍🏫 Echte Fragen? Vielleicht anders.
      </div>
      <div style={{ position: "absolute", left: 80, right: 80, top: 380, scale: String(Math.max(0.0001, sp(t, aber, fps))) }}>
        <div style={{ position: "relative", background: PAPER, border: `7px solid ${INK}`, borderRadius: 30, padding: "34px 30px", textAlign: "center" }}>
          <div style={{ fontSize: 46, fontWeight: 700, color: MUTED }}>Deine wackelige Stelle:</div>
          <div style={{ fontSize: 80, fontWeight: 700, color: GREEN, marginTop: 8 }}>gefunden ✓</div>
          <svg viewBox="0 0 200 100" style={{ position: "absolute", left: -30, top: -30, width: 850, height: 360, pointerEvents: "none" }}>
            <ellipse cx={100} cy={50} rx={95} ry={45} fill="none" stroke={GREEN} strokeWidth={2.5} strokeDasharray={460} strokeDashoffset={460 * (1 - ring)} strokeLinecap="round" />
          </svg>
        </div>
      </div>
    </div>
  );
};

// ---------- 10 Ende: Handy + Kommentar PRÜFUNG ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 820, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 80 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 110 }}>📋</div>
          <div style={{ fontSize: 40, fontWeight: 700, textAlign: "center", lineHeight: 1.15 }}>Prompt<br />„Probe-Prüfung“<br />zum Kopieren</div>
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
      <Pop at={commentAt} style={{ position: "absolute", left: 60, bottom: 60 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "20px 36px" }}>
          <svg width={64} height={64} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 96, fontWeight: 600, color: INK, letterSpacing: 4 }}>PRÜFUNG</div>
        </div>
      </Pop>
    </div>
  );
};
