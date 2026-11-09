import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Seminar09 · S9 „Noch 1 Tag bis zur Abgabe“ · Letzte-Chance-Video im Stil von S1 · Werbung (eigenes Produkt), ohne Preis · Leinwand 948×1004
// Zeiten in den Props sind Sekunden ab Szenenstart.
const RED = "#C8473A";
const YEL = "#D9A32B";
const MUTED = "#6B5444";
const SAND = "#F5EAD7";
const LINE = "#EAD9BD";
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

const Row: React.FC<{ show: number; label: string; status: "ok" | "warn" | "bad"; note: string }> = ({ show, label, status, note }) => {
  const col = status === "ok" ? GREEN : status === "warn" ? YEL : RED;
  const icon = status === "ok" ? "✓" : status === "warn" ? "!" : "✗";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 20, opacity: show, translate: `${(1 - show) * -40}px 0px`, padding: "14px 0", borderBottom: `3px solid ${LINE}` }}>
      <div style={{ width: 60, height: 60, borderRadius: 30, background: col, color: "#fff", display: "grid", placeItems: "center", fontWeight: 700, fontSize: 40, flex: "none" }}>{icon}</div>
      <div>
        <div style={{ fontSize: 46, fontWeight: 700, lineHeight: 1.1 }}>{label}</div>
        <div style={{ fontSize: 32, fontWeight: 600, color: MUTED }}>{note}</div>
      </div>
    </div>
  );
};

// ---------- 1 Hook: Kalender „MORGEN: Abgabe“ mit roter 1, ab Frame 0 ----------
export const SceneHook: React.FC<{ das: number; letzte: number }> = ({ das, letzte }) => {
  const { t, frame } = useT();
  const wob = Math.sin(frame / 3) * 1.5;
  const ring = interpolate(t, [0.2, 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const left = Math.max(0, 23 * 3600 + 59 * 60 + 41 - Math.floor(t * 1));
  const hh = String(Math.floor(left / 3600)).padStart(2, "0");
  const mm = String(Math.floor((left % 3600) / 60)).padStart(2, "0");
  const ss = String(left % 60).padStart(2, "0");
  const bg = interpolate(Math.sin(frame / 4), [-1, 1], [0, 1]) > 0.5 ? "#FDE8E4" : "#FBE1DC";
  return (
    <div style={{ position: "absolute", inset: 0, background: bg }}>
      {/* Text-Overlay (≤ 6 Wörter), steht ab Frame 0 */}
      <div style={{ position: "absolute", left: 20, right: 20, top: 34, textAlign: "center", fontSize: 80, fontWeight: 700, lineHeight: 1.08, color: NAVY }}>
        Noch 1 Tag. <span style={{ color: RED }}>Letzte Chance.</span>
      </div>
      {/* Kalender */}
      <div style={{ position: "absolute", left: 214, top: 215, width: 520, rotate: `${wob}deg` }}>
        <div style={{ background: RED, color: "#fff", border: `8px solid ${INK}`, borderBottom: "none", borderRadius: "36px 36px 0 0", textAlign: "center", fontSize: 64, fontWeight: 700, padding: "12px 0" }}>MORGEN: Abgabe</div>
        <div style={{ background: PAPER, border: `8px solid ${INK}`, borderRadius: "0 0 36px 36px", textAlign: "center", position: "relative", paddingBottom: 16 }}>
          <div style={{ fontSize: 300, fontWeight: 700, lineHeight: 1, color: RED }}>1</div>
          <div style={{ fontSize: 48, fontWeight: 700, color: INK, marginTop: -10 }}>Tag übrig</div>
          <svg viewBox="0 0 200 160" style={{ position: "absolute", left: 120, top: 10, width: 264, height: 300 }}>
            <ellipse cx={100} cy={80} rx={88} ry={72} fill="none" stroke={RED} strokeWidth={7} strokeDasharray={520} strokeDashoffset={520 * (1 - ring)} strokeLinecap="round" />
          </svg>
        </div>
      </div>
      {/* Countdown ab „DAS“ */}
      <Pop at={das} style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center" }}>
        <div style={{ background: INK, color: "#fff", borderRadius: 24, padding: "10px 34px", fontSize: 72, fontWeight: 700, letterSpacing: 4, fontVariantNumeric: "tabular-nums" }}>
          ⏰ {hh}:{mm}:{ss}
        </div>
      </Pop>
      {/* Stempel ab „LETZTE“ */}
      <Pop at={letzte} style={{ position: "absolute", left: 600, top: 600 }}>
        <div style={{ border: `8px solid ${RED}`, color: RED, background: "rgba(255,255,255,.85)", borderRadius: 18, padding: "6px 22px", fontSize: 52, fontWeight: 700, rotate: "-12deg", lineHeight: 1.05, textAlign: "center" }}>
          JETZT<br />PRÜFEN
        </div>
      </Pop>
    </div>
  );
};

// ---------- 2 Sorgen: Fußnoten-Chaos, Literaturverzeichnis, KI-Frage ----------
export const SceneSorgen: React.FC<{ fn: number; lit: number; ki: number }> = ({ fn, lit, ki }) => {
  const { frame } = useT();
  const card = (rot: number): React.CSSProperties => ({ background: PAPER, border: `6px solid ${INK}`, borderRadius: 30, padding: "18px 30px", boxShadow: "0 14px 0 rgba(58,38,24,.12)", rotate: `${rot + Math.sin(frame / 6) * 0.8}deg` });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBE1DC" }}>
      <Pop at={fn} style={{ position: "absolute", left: 40, top: 50 }}>
        <div style={card(-4)}>
          <div style={{ fontSize: 30, fontWeight: 700, color: MUTED, letterSpacing: 2 }}>FUSSNOTEN</div>
          <div style={{ fontSize: 66, fontWeight: 700, color: RED }}>Chaos¹²³⁴ 😬</div>
          <div style={{ fontSize: 32, fontWeight: 600, color: MUTED, marginTop: 4 }}>„Vgl.“? „ebd.“? Seite?</div>
        </div>
      </Pop>
      <Pop at={lit} style={{ position: "absolute", right: 40, top: 360 }}>
        <div style={{ ...card(3), width: 560 }}>
          <div style={{ fontSize: 30, fontWeight: 700, color: MUTED, letterSpacing: 2 }}>LITERATURVERZEICHNIS</div>
          {["Bauer 2019", "?", "Schmidt 2022"].map((r, i) =>
            r === "?" ? (
              <div key={i} style={{ marginTop: 12, height: 64, borderRadius: 12, border: `5px dashed ${RED}`, display: "flex", alignItems: "center", padding: "0 18px", fontSize: 40, fontWeight: 700, color: RED }}>fehlt was?</div>
            ) : (
              <div key={i} style={{ marginTop: 12, fontSize: 40, fontWeight: 600, color: "#5B4636" }}>{r}</div>
            )
          )}
        </div>
      </Pop>
      <Pop at={ki} style={{ position: "absolute", left: 40, right: 60, top: 720 }}>
        <div style={card(-2)}>
          <div style={{ fontSize: 30, fontWeight: 700, color: NAVY, letterSpacing: 2 }}>🧑‍🏫 PRÜFUNGSGESPRÄCH</div>
          <div style={{ fontSize: 58, fontWeight: 700, lineHeight: 1.1 }}>„Wie hast du KI benutzt?“</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 3 Keine Angst ----------
export const SceneRuhe: React.FC = () => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#E8F4EC" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 330, textAlign: "center", scale: String(Math.max(0.6, sp(t, 0, fps))) }}>
        <div style={{ fontSize: 140, fontWeight: 700, color: GREEN }}>Keine Angst.</div>
        <div style={{ fontSize: 70, fontWeight: 600, marginTop: 10 }}>Es gibt einen Check. 🐹</div>
      </div>
    </div>
  );
};

// ---------- 4 Chat: Arbeit hochladen + „Abgabe morgen, check alles.“ ----------
export const SceneChat: React.FC<{ datei: number; text: number }> = ({ datei, text }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<span style={{ background: GREEN, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>Skill: Seminararbeit-Profi</span>} />
      <div style={{ position: "absolute", right: 40, top: 170, scale: String(Math.max(0.0001, sp(t, datei, fps))), transformOrigin: "right top" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 22, background: SAND, border: `6px solid ${INK}`, borderRadius: 26, padding: "22px 30px", fontSize: 54, fontWeight: 700 }}>
          <div style={{ width: 76, height: 96, background: NAVY, borderRadius: 12, color: "#fff", display: "grid", placeItems: "center", fontSize: 48, fontWeight: 700 }}>W</div>
          Seminararbeit.docx
        </div>
      </div>
      {t >= text - 0.2 && (
        <div style={{ position: "absolute", right: 40, top: 400, maxWidth: 820, background: "#F1E6D3", borderRadius: 34, padding: "26px 36px", fontSize: 66, fontWeight: 700, lineHeight: 1.15, opacity: fade(t, text - 0.2, 0.2) }}>
          <Typed text="Abgabe morgen, check alles." start={text - 0.2} dur={1.2} />
        </div>
      )}
      <Pop at={text + 1.4} style={{ position: "absolute", left: 50, top: 700 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, fontSize: 50, fontWeight: 600, color: MUTED }}>
          <div style={{ width: 26, height: 26, borderRadius: 13, background: "#E5835E" }} /> Claude prüft …
        </div>
      </Pop>
    </div>
  );
};

// ---------- 5 Endcheck-Kacheln + Prüfpunkte nach Merkblatt ----------
export const SceneCheck: React.FC<{ zit: number; fn: number; lit: number; form: number; merk: number }> = ({ zit, fn, lit, form, merk }) => {
  const { t, fps } = useT();
  const count = (n: number, a: number) => Math.round(n * interpolate(t, [a, a + 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const tiles = [
    { l: "Muss", n: 3, c: RED, fg: "#fff" },
    { l: "Sollte", n: 5, c: YEL, fg: "#fff" },
    { l: "Passt", n: 31, c: GREEN, fg: "#fff" },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 30, fontSize: 60, fontWeight: 700 }}>Endcheck vor der Abgabe</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 125, display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 18 }}>
        {tiles.map((x, i) => (
          <div key={x.l} style={{ background: x.c, color: x.fg, border: `5px solid ${INK}`, borderRadius: 24, padding: "10px 22px", scale: String(Math.max(0.3, sp(t, i * 0.1, fps))) }}>
            <div style={{ fontSize: 34, fontWeight: 700 }}>{x.l}</div>
            <div style={{ fontSize: 96, fontWeight: 700, lineHeight: 1 }}>{count(x.n, 0.05 + i * 0.1)}</div>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 370 }}>
        <Row show={fade(t, zit)} label="Zitate" status="ok" note="Wortlaut stimmt" />
        <Row show={fade(t, fn)} label="Fußnoten" status="warn" note="Fn. 12: „Vgl.“ bei wörtlichem Zitat" />
        <Row show={fade(t, lit)} label="Literaturverzeichnis" status="bad" note="„Müller 2021“ fehlt" />
        <Row show={fade(t, form)} label="Formalia" status="warn" note="Ränder 2,5 cm statt 3 cm" />
      </div>
      <Pop at={merk} style={{ position: "absolute", left: 40, top: 880 }}>
        <div style={{ background: NAVY, color: "#fff", border: `5px solid ${INK}`, borderRadius: 18, padding: "8px 26px", fontSize: 44, fontWeight: 700, rotate: "-2deg" }}>📋 nach dem Merkblatt deiner Schule</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Diagramm aus deinen Zahlen ----------
export const SceneDiagramm: React.FC<{ fertig: number }> = ({ fertig }) => {
  const { t } = useT();
  const vals = [0.65, 0.78, 0.97, 1.26, 1.77, 2.2, 2.32];
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 30, display: "flex", gap: 14, flexWrap: "nowrap", fontSize: 34, fontWeight: 600, color: MUTED, opacity: 1 - fade(t, 0.5, 0.4) * 0.5 }}>
        <span style={{ fontWeight: 700, color: INK }}>Deine Zahlen:</span> 0,65 · 0,78 · 0,97 · 1,26 · 1,77 …
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 110, bottom: 40, background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, padding: "30px 36px", display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 22, height: 520, borderBottom: `5px solid ${INK}`, borderLeft: `5px solid ${INK}`, paddingLeft: 14 }}>
          {vals.map((v, i) => {
            const g = interpolate(t, [0.1 + i * 0.1, 0.5 + i * 0.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
            return (
              <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end", height: "100%" }}>
                <div style={{ fontSize: 30, fontWeight: 600, color: MUTED, opacity: g }}>{v.toString().replace(".", ",")}</div>
                <div style={{ width: "100%", height: `${(v / 2.4) * 440 * g}px`, background: i > 4 ? NAVY : "#9CB3D6", borderRadius: "10px 10px 0 0" }} />
              </div>
            );
          })}
        </div>
        <div style={{ display: "flex", gap: 22, paddingLeft: 19, fontSize: 28, color: MUTED, marginTop: 8 }}>
          {["2012", "2013", "2014", "2015", "2016", "2017", "2018"].map((y) => <div key={y} style={{ flex: 1, textAlign: "center" }}>{y}</div>)}
        </div>
        <div style={{ fontSize: 38, fontStyle: "italic", fontWeight: 600, marginTop: 20, opacity: fade(t, 0.7) }}>Abb. 2: Besucher in Island (in Mio.)</div>
        <div style={{ marginTop: 16, alignSelf: "flex-start", background: "#E3F1EA", color: "#1C7049", border: `5px solid ${GREEN}`, borderRadius: 999, padding: "8px 28px", fontSize: 38, fontWeight: 700, scale: String(fertig > 0 && t >= fertig ? 1 : 0) }}>✓ Achsen · Quelle · Dezimalkomma</div>
      </div>
    </div>
  );
};

// ---------- 8 Screenshots → Quellenbelege.pdf ----------
export const SceneBeleg: React.FC<{ pdf: number }> = ({ pdf }) => {
  const { t, fps } = useT();
  const k = interpolate(t, [pdf - 0.35, pdf + 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 40, fontSize: 52, fontWeight: 700, color: MUTED }}>📸 deine Screenshots</div>
      {[0, 1, 2, 3].map((i) => {
        const x0 = 40 + i * 220;
        const y0 = 150 + (i % 2) * 70;
        return (
          <div key={i} style={{ position: "absolute", left: interpolate(k, [0, 1], [x0, 420]), top: interpolate(k, [0, 1], [y0, 520]), width: 200, height: 280, background: "#fff", border: `5px solid ${INK}`, borderRadius: 18, padding: 12, opacity: fade(t, i * 0.1, 0.15) * (1 - k * 0.95), scale: String(1 - k * 0.5), rotate: `${(i - 1.5) * 5}deg` }}>
            <div style={{ height: 22, width: "85%", background: "#9DB8E0", borderRadius: 6 }} />
            {[0, 1, 2, 3].map((r) => <div key={r} style={{ height: 14, width: `${92 - r * 12}%`, background: "#E3D8C6", borderRadius: 6, marginTop: 16 }} />)}
            <div style={{ height: 40, background: "#FFE27A", borderRadius: 6, marginTop: 16 }} />
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 150, right: 150, top: 470, background: PAPER, border: `7px solid ${INK}`, borderRadius: 22, padding: "24px 30px", scale: String(Math.max(0.0001, sp(t, pdf, fps))), boxShadow: "0 16px 0 rgba(58,38,24,.12)" }}>
        <div style={{ position: "absolute", right: -22, top: -26, background: RED, color: "#fff", border: `5px solid ${INK}`, borderRadius: 14, padding: "4px 20px", fontSize: 40, fontWeight: 700, rotate: "6deg" }}>PDF</div>
        <div style={{ fontSize: 50, fontWeight: 700 }}>Quellenbelege</div>
        <div style={{ marginTop: 14, background: "#F3F0EA", borderRadius: 12, padding: "12px 16px", fontSize: 32, lineHeight: 1.35, fontWeight: 600 }}>
          Beleg 3.04 · Müller 2021, S. 14<br />
          <span style={{ color: "#1A56C4" }}>🔗 Link</span> · <span style={{ color: GREEN }}>📅 abgerufen 09.11.2026</span>
        </div>
      </div>
    </div>
  );
};

// ---------- 9 Plagiats- und KI-Check grün ----------
export const ScenePlagiat: React.FC<{ plag: number; floskel: number; ersetzt: number; klingt: number }> = ({ plag, floskel, ersetzt, klingt }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 30, fontSize: 60, fontWeight: 700 }}>Plagiats- &amp; KI-Check</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 120 }}>
        <Row show={fade(t, plag)} label="Plagiate" status="ok" note="gegen deine Quellen: keine Übernahmen" />
        <Row show={fade(t, floskel)} label="KI-Floskeln" status="warn" note="4 gefunden → ersetzt" />
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 440, background: PAPER, border: `6px solid ${INK}`, borderRadius: 24, padding: "22px 30px", fontSize: 44, lineHeight: 1.3, fontWeight: 500, opacity: fade(t, floskel + 0.2) }}>
        <span style={{ textDecoration: t >= ersetzt ? "line-through" : "none", textDecorationThickness: 5, color: t >= ersetzt ? RED : INK }}>Darüber hinaus spielt der Tourismus eine zentrale Rolle.</span>
        {t >= ersetzt && (
          <div style={{ color: GREEN, fontWeight: 700, marginTop: 10, opacity: fade(t, ersetzt + 0.15) }}>2019 kamen rund 2 Mio. Touristen nach Island.</div>
        )}
      </div>
      <Pop at={klingt} style={{ position: "absolute", left: 0, right: 0, top: 820, display: "flex", justifyContent: "center" }}>
        <div style={{ background: GREEN, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "12px 38px", fontSize: 54, fontWeight: 700, scale: String(Math.max(0.0001, sp(t, klingt, fps))) }}>✓ klingt nach dir</div>
      </Pop>
    </div>
  );
};

// ---------- 10 Claude spielt die Lehrkraft ----------
export const SceneLehrkraft: React.FC<{ frage: number; antwort: number; feedback: number }> = ({ frage, antwort, feedback }) => {
  const { t, fps, frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<span style={{ background: NAVY, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>🎓 Probe-Prüfung</span>} />
      <div style={{ position: "absolute", left: 36, right: 100, top: 125, background: "#fff", border: `6px solid ${INK}`, borderRadius: 36, padding: "18px 30px 24px", rotate: `${-1 + Math.sin(frame / 5) * 0.8}deg`, scale: String(Math.max(0.75, sp(t, frage, fps))), transformOrigin: "left top" }}>
        <div style={{ fontSize: 28, fontWeight: 700, color: NAVY, letterSpacing: 2 }}>🧑‍🏫 LEHRKRAFT (simuliert)</div>
        <div style={{ fontSize: 64, fontWeight: 700, lineHeight: 1.12, marginTop: 4 }}>„Warum hast du diese Quelle gewählt?“</div>
        <div style={{ fontSize: 30, fontWeight: 600, color: MUTED, marginTop: 6 }}>Frage zu deiner Arbeit, Kapitel 3</div>
      </div>
      <Pop at={antwort} style={{ position: "absolute", left: 190, right: 50, top: 480 }}>
        <div style={{ background: NAVY, color: "#fff", borderRadius: 30, padding: "18px 28px", fontSize: 44, lineHeight: 1.25 }}>
          <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: 2, opacity: 0.8 }}>DU</div>
          Weil Müller aktuelle Zahlen hat.
        </div>
      </Pop>
      <Pop at={feedback} style={{ position: "absolute", left: 36, right: 36, top: 730 }}>
        <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: 28, padding: "18px 28px", display: "grid", gap: 10 }}>
          <div style={{ fontSize: 46, fontWeight: 700, color: GREEN }}>✓ gut: Quelle genannt</div>
          <div style={{ fontSize: 44, fontWeight: 700, color: "#C27A1E" }}>➜ fehlt noch: warum sie verlässlich ist</div>
        </div>
      </Pop>
    </div>
  );
};
