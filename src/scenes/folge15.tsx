import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";
import { Hamster } from "../Hamster";

// Folge15 · Vorher/Nachher „Gleicher Job, zwei Bewerbungen – ein Satz Unterschied“ · Serie (b) · Einstiegs-Test E2 (Paar 2) · ohne Werbung
// Mia vom Studio erfunden (docs/plaene/beispiel/fragen_beispiel.txt). Beide Bewerbungen = wörtliche Claude-Antworten (fragen_claude_antwort.md), nur gekürzt.
// Zeiten in Props = Sekunden ab Szenenstart. Unten links auf der Leinwand (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LRED = "#F9DEDA";
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

// Eckige Klammer, optional rot eingekreist (v 0..1)
const K: React.FC<{ children: React.ReactNode; v?: number }> = ({ children, v = 0 }) => (
  <span style={{ color: v > 0.5 ? RED : "#6A707A", background: v > 0 ? `rgba(249,222,218,${v})` : "transparent", outline: v > 0.5 ? `4px solid ${RED}` : "none", borderRadius: 8, padding: "0 4px", fontWeight: 600 }}>[{children}]</span>
);
const M: React.FC<{ children: React.ReactNode; v?: number; c?: "g" | "r" }> = ({ children, v = 0, c = "g" }) => {
  const bg = c === "g" ? `rgba(205,235,217,${v})` : `rgba(249,222,218,${v})`;
  return <span style={{ background: v > 0 ? bg : "transparent", color: v > 0.5 ? (c === "g" ? DGREEN : RED) : "inherit", borderRadius: 8, padding: "0 4px", fontWeight: v > 0.5 ? 700 : "inherit" }}>{children}</span>;
};

// ---------- Karten (Ausschnitte der echten Antworten) ----------
const Links: React.FC<{ w: number; fs: number; k?: number[]; floskel?: number }> = ({ w, fs, k = [0, 0, 0, 0], floskel = 0 }) => (
  <div style={{ width: w, background: "#ECEDEF", border: `4px solid ${GREY}`, borderRadius: 18, padding: fs * 0.55, color: "#3E434A", lineHeight: 1.28, fontSize: fs }}>
    <div>Sehr geehrte/r <K v={k[0]}>Frau/Herr Nachname</K>,</div>
    <div style={{ marginTop: fs * 0.35 }}>… und <M v={floskel} c="r">bewerbe mich hiermit sehr gern</M> bei Ihnen.</div>
    <div style={{ marginTop: fs * 0.35 }}>Zurzeit <K v={k[1]}>besuche ich die … Klasse</K>. Ich arbeite <M v={floskel} c="r">zuverlässig</M>.</div>
    <div style={{ marginTop: fs * 0.35 }}>Ich kann <K v={k[2]}>zum Beispiel samstags …</K> arbeiten, ab dem <K v={k[3]}>Datum</K>.</div>
  </div>
);

const Rechts: React.FC<{ w: number; fs: number; m?: number[]; schlange?: number; kurz?: boolean }> = ({ w, fs, m = [0, 0, 0], schlange = 0, kurz = false }) => (
  <div style={{ width: w, background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: fs * 0.55, color: "#1E2430", lineHeight: 1.28, fontSize: fs, boxShadow: "6px 8px 0 rgba(58,38,24,.14)" }}>
    <div>fast jeden Morgen <M v={m[0]}>vor der Schule hole ich mir bei Ihnen eine Brezel</M>.</div>
    <div style={{ marginTop: fs * 0.35 }}>Seit zwei Jahren übernehme ich … <M v={m[1]}>die Kasse am Kuchenstand</M>.{!kurz && <> Dort habe ich gelernt, auch bei einer <M v={schlange} c="r">langen Schlange</M> freundlich … zu bleiben.</>}</div>
    <div style={{ marginTop: fs * 0.35 }}>Ab Januar kann ich <M v={m[2]}>jeden Samstag ab 6 Uhr</M> arbeiten.</div>
  </div>
);

// ---------- 0 E2-Hook (Vollbild 1080×1920, 0–1,0 s) ----------
export const E2Hook: React.FC = () => {
  const { t, frame } = useT();
  const kv = [0, 0.1, 0.2, 0.3].map((a) => fade(t, a, 0.1));
  const n = Math.round(interpolate(t, [0, 0.45], [4, 20], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const mv = [fade(t, 0.05, 0.25), fade(t, 0.25, 0.2), fade(t, 0.4, 0.2)];
  return (
    <AbsoluteFill style={{ background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center" }}>
        <div style={{ fontSize: 34, fontWeight: 700, letterSpacing: 4, color: MUTED }}>VORHER / NACHHER · Bewerbung Aushilfe</div>
        <div style={{ fontSize: 70, fontWeight: 700, lineHeight: 1.05, color: NAVY, whiteSpace: "nowrap" }}>Gleiche KI. <span style={{ color: GREEN }}>Ein Satz Unterschied.</span></div>
      </div>
      <div style={{ position: "absolute", left: 44, top: 290, rotate: "-1.5deg" }}>
        <div style={{ fontSize: 50, fontWeight: 700, color: GREY, marginBottom: 6 }}>OHNE Fragen</div>
        <Links w={440} fs={45} k={kv} floskel={fade(t, 0.35, 0.2)} />
        <div style={{ marginTop: 18, display: "inline-block", background: RED, color: "#fff", borderRadius: 18, padding: "4px 22px", fontSize: 60, fontWeight: 700 }}>{n}× [ ]</div>
      </div>
      <div style={{ position: "absolute", left: 500, top: 280, rotate: "1deg" }}>
        <div style={{ fontSize: 50, fontWeight: 700, color: GREEN, marginBottom: 6 }}>MIT „5 Fragen“</div>
        <Rechts w={460} fs={50} m={mv} kurz />
      </div>
      <div style={{ position: "absolute", left: 560, top: 1330 }}><Stempel size={26} text="BEISPIEL · Mia, 17, erfunden" rot={-2} /></div>
      <svg width={300} height={160} viewBox="0 100 300 160" style={{ position: "absolute", left: 330, top: 1270, opacity: fade(t, 0.15, 0.15) }}>
        <path d="M20 240 Q150 200 260 40" stroke={GREEN} strokeWidth={14} fill="none" strokeLinecap="round" strokeDasharray="28 20" strokeDashoffset={-frame * 4} />
        <path d="M225 50 L268 22 L270 76 Z" fill={GREEN} />
      </svg>
      <div style={{ position: "absolute", left: 60, top: 1340 }}>
        <Hamster size={300} talking={frame % 6 < 3} blink={false} pointerAngle={22 + Math.sin(frame / 3) * 4} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- 0b Hook auf der Leinwand (ab 1,0 s) ----------
export const SceneHook: React.FC<{ satz: number }> = ({ satz }) => {
  const { t, frame } = useT();
  const pulse = (Math.sin(frame / 4) + 1) / 2;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 10, textAlign: "center" }}>
        <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: 4, color: MUTED }}>VORHER / NACHHER · Bewerbung Aushilfe</div>
        <div style={{ fontSize: 54, fontWeight: 700, lineHeight: 1.05, color: NAVY, whiteSpace: "nowrap" }}>Gleiche KI. <span style={{ color: GREEN }}>Ein Satz Unterschied.</span></div>
      </div>
      <div style={{ position: "absolute", left: 12, top: 120, rotate: "-1.5deg" }}>
        <div style={{ fontSize: 32, fontWeight: 700, color: GREY, marginBottom: 4 }}>OHNE Fragen</div>
        <Links w={450} fs={40} k={[1, 1, 1, 1]} floskel={1} />
      </div>
      <div style={{ position: "absolute", left: 474, top: 110, rotate: "1deg" }}>
        <div style={{ fontSize: 32, fontWeight: 700, color: GREEN, marginBottom: 4 }}>MIT „5 Fragen“</div>
        <Rechts w={458} fs={44} m={[1, 1, 1]} kurz />
      </div>
      <Pop at={satz} style={{ position: "absolute", left: 400, right: 20, top: 850 }}>
        <div style={{ background: "#FFF0C2", border: `6px solid ${GREEN}`, borderRadius: 20, padding: "8px 20px", fontSize: 50, fontWeight: 700, color: INK, scale: S(1 + 0.04 * pulse), textAlign: "center" }}>Welcher Satz? 🔍</div>
      </Pop>
      <div style={{ position: "absolute", left: 470, top: 880, opacity: 1 - fade(t, satz) }}><Stempel size={24} text="BEISPIEL · Mia, 17, erfunden" rot={-2} /></div>
    </div>
  );
};

// ---------- 1 Links: Eingabe + Vorlage voller Klammern ----------
export const SceneLinks: React.FC<{ floskel: number; klammer: number }> = ({ floskel, klammer }) => {
  const { t, fps } = useT();
  const n = Math.round(interpolate(t, [klammer, klammer + 0.6], [0, 20], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const kv = [0, 0.12, 0.24, 0.36].map((a) => fade(t, klammer + a, 0.1));
  return (
    <div style={{ position: "absolute", inset: 0, background: "#ECEDEF" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 56, fontWeight: 700, color: GREY }}>LINKS · ohne Fragen</div>
      <div style={{ position: "absolute", left: 150, right: 30, top: 110, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "14px 26px", fontSize: 44, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ fontSize: 28, color: MUTED, marginBottom: 4 }}>An Claude:</div>
          „Schreib mir eine Bewerbung als Aushilfe in einer Bäckerei.“
        </div>
      </div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 340, opacity: fade(t, 0.9) }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={28} title="Claude · Vorlage" />
          <div style={{ padding: "16px 24px", fontSize: 48, lineHeight: 1.3 }}>
            <div><K v={kv[0]}>Vorname Nachname</K> <K v={kv[1]}>Straße</K> <K v={kv[2]}>PLZ Ort</K></div>
            <div style={{ marginTop: 8 }}>… <M v={fade(t, floskel)} c="r">bewerbe mich hiermit sehr gern</M> … <M v={fade(t, floskel + 0.2)} c="r">offen und freundlich</M> … <M v={fade(t, floskel + 0.4)} c="r">zuverlässig</M> …</div>
            <div style={{ marginTop: 8 }}>Zurzeit <K v={kv[3]}>besuche ich die … Klasse</K> …</div>
          </div>
        </div>
      </div>
      <Pop at={klammer} style={{ position: "absolute", left: 420, top: 850 }}>
        <div style={{ background: RED, color: "#fff", borderRadius: 20, padding: "6px 26px", fontSize: 70, fontWeight: 700, whiteSpace: "nowrap" }}>{n}× [ ]</div>
      </Pop>
    </div>
  );
};

// ---------- 2 Rechts: der eine Satz tippt sich dazu ----------
export const SceneSatz: React.FC<{ tipp: number }> = ({ tipp }) => {
  const { t, fps, frame } = useT();
  const satz = "Stell mir vorher fünf Fragen.";
  const k = Math.round(interpolate(t, [tipp, tipp + 1.2], [0, satz.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const cursor = frame % 16 < 8 ? "|" : " ";
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF7F1" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 56, fontWeight: 700, color: GREEN }}>RECHTS · ein Satz mehr</div>
      <div style={{ position: "absolute", left: 60, right: 30, top: 140, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "18px 28px", fontSize: 52, fontWeight: 600, lineHeight: 1.25 }}>
          <div style={{ fontSize: 30, color: MUTED, marginBottom: 4 }}>An Claude:</div>
          „Schreib mir eine Bewerbung als Aushilfe in einer Bäckerei.{" "}
          <span style={{ background: k > 0 ? "rgba(205,235,217,1)" : "transparent", color: DGREEN, fontWeight: 700, borderRadius: 8 }}>{satz.slice(0, k)}{k < satz.length && t >= tipp ? cursor : ""}</span>“
        </div>
      </div>
      <Pop at={tipp + 1.3} style={{ position: "absolute", left: 60, right: 60, top: 600 }}>
        <div style={{ textAlign: "center", fontSize: 64, fontWeight: 700, color: NAVY }}>Nur dieser Satz ist anders.</div>
      </Pop>
    </div>
  );
};

// ---------- 3 Claude fragt: fünf Fragekarten ----------
export const SceneFragen: React.FC<{ hl: number[] }> = ({ hl }) => {
  const { t, fps } = useT();
  const q: [string, number][] = [["Wer bist du?", -1], ["Welche Bäckerei?", -1], ["Welche Erfahrung?", 0], ["Wann kannst du?", 1], ["Warum dieser Laden?", 2]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 30, right: 30, top: 24 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={30} title="Claude fragt zuerst:" />
        </div>
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 160, display: "flex", flexDirection: "column", gap: 16 }}>
        {q.map(([txt, h], i) => {
          const on = h >= 0 ? fade(t, hl[h], 0.15) : 0;
          return (
            <div key={txt} style={{ scale: S(sp(t, 0.1 + i * 0.12, fps)), transformOrigin: "left center", display: "flex", alignItems: "center", gap: 20, background: on > 0.5 ? "#CDEBD9" : PAPER, border: `5px solid ${on > 0.5 ? GREEN : INK}`, borderRadius: 18, padding: "8px 22px", fontSize: 54, fontWeight: 700, marginLeft: i % 2 ? 60 : 0, width: 700 }}>
              <span style={{ color: on > 0.5 ? DGREEN : NAVY }}>{i + 1}</span> {txt}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------- 4 Rechte Bewerbung nah: drei Markierungen ----------
export const SceneBrief: React.FC<{ m: number[] }> = ({ m }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF7F1" }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 52, fontWeight: 700, color: GREEN }}>Jetzt steht drin:</div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 110, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={28} title="Claude · Bewerbung für Mia" />
          <div style={{ padding: "16px 24px", fontSize: 48, lineHeight: 1.3 }}>
            <div>fast jeden Morgen <M v={fade(t, m[0], 0.2)}>vor der Schule hole ich mir bei Ihnen eine Brezel</M>.</div>
            <div style={{ marginTop: 12 }}>Seit zwei Jahren übernehme ich … <M v={fade(t, m[1], 0.2)}>die Kasse am Kuchenstand</M>.</div>
            <div style={{ marginTop: 12 }}>Ab Januar kann ich <M v={fade(t, m[2], 0.2)}>jeden Samstag ab 6 Uhr</M> arbeiten.</div>
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 400, top: 820, fontSize: 46, fontWeight: 700, color: DGREEN, opacity: fade(t, m[2] + 0.4) }}>alles aus Mias Antworten ✓</div>
    </div>
  );
};

// ---------- 5 Haken: drei Sätze dazugedichtet ----------
export const SceneErfunden: React.FC<{ drei: number; schlange: number }> = ({ drei, schlange }) => {
  const { t, fps } = useT();
  const w = fade(t, schlange, 0.2);
  const liste = ["lange Schlange", "Wechselgeld „schnell und richtig“", "„macht mir Spaß“"];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 58, fontWeight: 700, color: RED }}>Aber: 3× dazugedichtet</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 120, display: "flex", flexDirection: "column", gap: 12 }}>
        {liste.map((x, i) => (
          <div key={x} style={{ scale: S(sp(t, drei + i * 0.18, fps)), transformOrigin: "left center", fontSize: 46, fontWeight: 700, color: RED, background: LRED, borderRadius: 14, padding: "4px 16px", width: "fit-content" }}>✗ {x}</div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 30, right: 30, top: 410, opacity: fade(t, schlange - 0.6) }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: "14px 24px", fontSize: 50, fontWeight: 600, lineHeight: 1.3 }}>
          „… auch bei einer{" "}
          <span style={{ background: `rgba(249,222,218,${w})`, color: w > 0.5 ? RED : INK, border: `${w > 0.5 ? 5 : 0}px solid ${RED}`, borderRadius: 10, padding: "0 6px", fontWeight: 700 }}>langen Schlange</span>{" "}
          freundlich … zu bleiben“
        </div>
      </div>
      <Pop at={schlange + 0.7} style={{ position: "absolute", left: 330, right: 30, top: 700 }}>
        <div style={{ background: "#FFFDF5", border: `4px solid ${INK}`, borderRadius: 16, padding: "12px 20px", fontFamily: HAND, color: "#2E3F8F", fontSize: 40, lineHeight: 1.25, rotate: "-1.5deg" }}>
          Mia: „Kasse beim Kuchenstand, so einmal im Monat“<br />
          <span style={{ fontFamily: "Fredoka", fontWeight: 700, color: RED }}>Schlange? ✗ nie gesagt</span>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 6 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  const z: [string, boolean][] = [["Mias Fakten statt Klammern", true], ["Samstag ab 6 Uhr drin", true], ["3 Sätze erfunden", false]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 36px", fontSize: 86, fontWeight: 700, letterSpacing: 2, rotate: "-6deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)", whiteSpace: "nowrap" }}>RECHTS GEWINNT</div>
      </div>
      <div style={{ position: "absolute", left: 250, right: 10, top: 410, display: "flex", flexDirection: "column", gap: 22, fontSize: 52, whiteSpace: "nowrap", fontWeight: 700 }}>
        {z.map(([txt, ok], i) => (
          <div key={txt} style={{ opacity: fade(t, zeilen + i * 0.15, 0.15), color: ok ? INK : RED, background: ok ? "transparent" : LRED, borderRadius: 12, padding: "0 8px", width: "fit-content" }}>{txt} <span style={{ color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span></div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 250, right: 10, top: 700, fontSize: 48, fontWeight: 700, color: NAVY, opacity: fade(t, zeilen + 1.1) }}>→ jeden Satz gegenlesen</div>
    </div>
  );
};

// ---------- 7 Ende: Handy + Kommentar FRAGEN ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 440, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 18, padding: 18 }}>
          <div style={{ background: "#CDEBD9", border: `4px solid ${GREEN}`, borderRadius: 16, padding: "10px 14px", fontSize: 38, fontWeight: 700, color: DGREEN, textAlign: "center", lineHeight: 1.2 }}>„Stell mir vorher fünf Fragen.“</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Der Satz<br />+ Gegenlese-<br />Check</div>
          <div style={{ fontSize: 24, color: MUTED }}>Claude-Konto ab 18</div>
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
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>FRAGEN</div>
        </div>
      </Pop>
    </div>
  );
};
