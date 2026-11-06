import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Seminar07 · S7 Suchbegriff-Video „Seminararbeit mit KI? So geht's.“ · Werbung (eigenes Produkt) · Leinwand 948×1004
// Website-Nachzeichnung nach site/pages/seminararbeit-profi.src.html + site/site.v2.css (ohne Preis).
const RED = "#C8473A";
const FUR = "#E9A24E";
const MUTED = "#7A6352";
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

const Lupe: React.FC<{ size: number; color?: string }> = ({ size, color = INK }) => (
  <svg width={size} height={size} viewBox="0 0 40 40" style={{ flex: "none" }}>
    <circle cx={17} cy={17} r={11} fill="none" stroke={color} strokeWidth={4.5} />
    <line x1={25} y1={25} x2={35} y2={35} stroke={color} strokeWidth={5} strokeLinecap="round" />
  </svg>
);

const Beispiel: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <div style={{ position: "absolute", fontSize: 26, fontWeight: 700, color: MUTED, letterSpacing: 2, border: `3px solid ${MUTED}`, borderRadius: 10, padding: "2px 12px", background: "#fff", ...style }}>BEISPIEL</div>
);

// Suchleiste (eigene Nachzeichnung, kein Logo)
const SearchBar: React.FC<{ text: string; cursor: boolean; scale?: number }> = ({ text, cursor, scale = 1 }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 18, scale: String(scale) }}>
    <div style={{ fontSize: 56, fontWeight: 700, color: INK }}>‹</div>
    <div style={{ flex: 1, display: "flex", alignItems: "center", gap: 16, background: "#F1F1F2", border: `5px solid ${INK}`, borderRadius: 999, padding: "18px 26px" }}>
      <Lupe size={50} color="#8A8B91" />
      <div style={{ fontSize: 50, fontWeight: 600, color: "#161823", whiteSpace: "nowrap" }}>
        {text}
        <span style={{ display: "inline-block", width: 5, height: 56, marginLeft: 4, verticalAlign: "-8px", background: cursor ? RED : "transparent" }} />
      </div>
    </div>
    <div style={{ fontSize: 40, fontWeight: 700, color: RED, paddingRight: 6 }}>Suchen</div>
  </div>
);

// ---------- 1 Hook: Suchleiste „seminararbeit mit ki“ ab Frame 0 ----------
export const SceneHook: React.FC<{ weg: number }> = ({ weg }) => {
  const { t, frame, fps } = useT();
  const cursor = frame % 16 < 9;
  const tap = interpolate(t % 1.2, [0, 0.6], [0.6, 1.5], { extrapolateRight: "clamp" });
  const tapO = interpolate(t % 1.2, [0, 0.6, 0.9], [1, 0.6, 0], { extrapolateRight: "clamp" });
  const vors = ["seminararbeit ki", "w seminar quellen", "w seminar", "seminar arbeit ki kostenlos"];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      {/* Text-Overlay (≤ 6 Wörter), steht ab Frame 0 */}
      <div style={{ position: "absolute", left: 40, right: 40, top: 46, textAlign: "center", fontSize: 76, fontWeight: 700, lineHeight: 1.1, color: NAVY }}>
        Seminararbeit mit KI?<br />
        <span style={{ color: GREEN }}>So geht's.</span>
      </div>
      {/* Such-Ansicht */}
      <div style={{ position: "absolute", left: 30, right: 30, top: 270, background: PAPER, border: `6px solid ${INK}`, borderRadius: 34, padding: "34px 28px", boxShadow: "0 14px 0 rgba(58,38,24,.12)" }}>
        <SearchBar text="seminararbeit mit ki" cursor={cursor} scale={1 + 0.02 * Math.sin(frame / 4)} />
        <div style={{ marginTop: 26 }}>
          {vors.map((v, i) => (
            <div key={v} style={{ display: "flex", alignItems: "center", gap: 22, padding: "18px 14px", borderBottom: "3px solid #EEE", fontSize: 44, color: "#3D3F48", fontWeight: 500 }}>
              <Lupe size={36} color="#A3A4AA" />
              {v}
            </div>
          ))}
        </div>
      </div>
      {/* Zeigestab-Tipp auf die Suchleiste */}
      <div style={{ position: "absolute", left: 102, top: 297, width: 622, height: 134, borderRadius: 999, border: `8px solid ${RED}`, scale: String(1 + (tap - 0.6) * 0.06), opacity: 0.35 + tapO * 0.65 }} />
      <Pop at={weg} style={{ position: "absolute", left: 0, right: 0, top: 880, display: "flex", justifyContent: "center" }}>
        <div style={{ background: GREEN, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 34px", fontSize: 50, fontWeight: 700, rotate: `${-2 + Math.sin(frame / 6) * 1.5}deg`, scale: String(Math.max(0.9, sp(t, weg, fps))) }}>⚡ der schnellste Weg</div>
      </Pop>
    </div>
  );
};

// Claude-Fensterkopf
const ClaudeHead: React.FC<{ right?: React.ReactNode }> = ({ right }) => (
  <div style={{ height: 90, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 34px", fontSize: 38, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);

const WordFile: React.FC<{ size?: number }> = ({ size = 1 }) => (
  <div style={{ display: "inline-flex", alignItems: "center", gap: 18 * size, background: SAND, border: `5px solid ${INK}`, borderRadius: 22 * size, padding: `${18 * size}px ${26 * size}px`, fontSize: 46 * size, fontWeight: 700 }}>
    <div style={{ width: 64 * size, height: 80 * size, background: NAVY, borderRadius: 10 * size, color: "#fff", display: "grid", placeItems: "center", fontSize: 40 * size, fontWeight: 700, flex: "none" }}>W</div>
    Seminararbeit_v4.docx
  </div>
);

// ---------- 2 Word-Datei rein ----------
export const SceneDatei: React.FC = () => {
  const { t, fps } = useT();
  const fly = sp(t, 0.15, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", right: 40, top: 180, display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 22, translate: `0px ${(1 - fly) * 420}px`, opacity: t < 0.15 ? 0.4 : 1 }}>
        <div style={{ fontSize: 30, fontWeight: 700, color: MUTED, letterSpacing: 2 }}>DU SCHICKST</div>
        <WordFile size={1.15} />
        <div style={{ background: "#F1E6D3", borderRadius: 26, padding: "20px 30px", fontSize: 48, fontWeight: 600 }}>„Abgabe am 10.11. Check alles.“</div>
      </div>
      <Pop at={0.9} style={{ position: "absolute", left: 50, top: 640 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, fontSize: 46, fontWeight: 600, color: MUTED }}>
          <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} /> Claude prüft …
        </div>
      </Pop>
      <Beispiel style={{ left: 40, bottom: 34 }} />
    </div>
  );
};

// ---------- 3 Endcheck-Ergebnis (wie auf der Website) ----------
export const SceneCheck: React.FC = () => {
  const { t, fps } = useT();
  const count = (n: number, a: number) => Math.round(n * interpolate(t, [a, a + 0.35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const tiles: { l: string; n: number; warn?: boolean }[] = [
    { l: "Muss vor Abgabe", n: 5, warn: true },
    { l: "Sollte", n: 7 },
    { l: "Passt schon", n: 31 },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 34, right: 34, top: 40, background: PAPER, borderRadius: 34, border: `6px solid ${INK}`, padding: "30px 34px", scale: String(Math.max(0.85, sp(t, -0.1, fps))), boxShadow: "0 16px 0 rgba(58,38,24,.12)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div>
            <div style={{ fontSize: 24, fontWeight: 800, letterSpacing: 2, color: MUTED }}>DU SCHICKST</div>
            <div style={{ marginTop: 8 }}><WordFile size={0.72} /></div>
          </div>
          <div style={{ fontSize: 70, color: GREEN, fontWeight: 700 }}>→</div>
          <div style={{ fontSize: 24, fontWeight: 800, letterSpacing: 2, color: MUTED, alignSelf: "flex-start" }}>DU BEKOMMST</div>
        </div>
        <div style={{ fontSize: 46, fontWeight: 700, marginTop: 20, lineHeight: 1.15 }}>Endcheck mit Fundstellen und Plan bis zur Abgabe</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 18, marginTop: 24 }}>
          {tiles.map((x, i) => (
            <div key={x.l} style={{ background: x.warn ? RED : SAND, color: x.warn ? "#fff" : INK, borderRadius: 22, padding: "16px 20px", scale: String(Math.max(0.3, sp(t, 0 + i * 0.1, fps))) }}>
              <div style={{ fontSize: 28, fontWeight: 700, opacity: 0.85 }}>{x.l}</div>
              <div style={{ fontSize: 96, fontWeight: 700, lineHeight: 1 }}>{count(x.n, 0.05 + i * 0.1)}</div>
            </div>
          ))}
        </div>
        <div style={{ borderTop: `3px solid ${LINE}`, marginTop: 26, paddingTop: 18, display: "grid", gap: 14 }}>
          {[
            { c: RED, s: "Fußnote 12: wörtliches Zitat, aber mit „Vgl.“" },
            { c: RED, s: "„Müller 2021“ fehlt im Literaturverzeichnis" },
            { c: FUR, s: "Kap. 3.2: „dramatisch“ ist eine Wertung" },
          ].map((f, i) => (
            <div key={f.s} style={{ display: "flex", alignItems: "center", gap: 18, fontSize: 36, fontWeight: 600, opacity: fade(t, 0.4 + i * 0.2), translate: `${(1 - fade(t, 0.4 + i * 0.2)) * -30}px 0px` }}>
              <div style={{ width: 22, height: 22, borderRadius: 11, background: f.c, flex: "none" }} />
              {f.s}
            </div>
          ))}
        </div>
      </div>
      <Beispiel style={{ right: 40, bottom: 26 }} />
    </div>
  );
};

const Lines: React.FC<{ n: number; w?: number[] }> = ({ n, w = [100, 92, 96, 70] }) => (
  <>
    {Array.from({ length: n }).map((_, i) => (
      <div key={i} style={{ height: 16, width: `${w[i % w.length]}%`, background: "#E6DACA", borderRadius: 8, marginTop: 18 }} />
    ))}
  </>
);

// ---------- 4 Fundstelle 1: Fußnote 12 ----------
export const SceneFund1: React.FC<{ vgl: number }> = ({ vgl }) => {
  const { t, fps } = useT();
  const strike = interpolate(t, [vgl, vgl + 0.35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 36, display: "flex", alignItems: "center", gap: 18 }}>
        <div style={{ background: RED, color: "#fff", borderRadius: 999, padding: "8px 26px", fontSize: 38, fontWeight: 700, border: `5px solid ${INK}` }}>Muss vor Abgabe</div>
        <div style={{ fontSize: 40, fontWeight: 700, color: MUTED }}>1 von 5</div>
      </div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 150, height: 760, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "34px 44px", scale: String(Math.max(0.85, sp(t, -0.1, fps))), rotate: "-1deg" }}>
        <Lines n={2} />
        <div style={{ marginTop: 26, fontSize: 44, lineHeight: 1.35, fontWeight: 500, background: "#FFF3C4", borderRadius: 12, padding: "8px 14px" }}>
          „Die Fahrgastzahlen stiegen deutlich an.“<sup style={{ color: RED, fontWeight: 700 }}>12</sup>
        </div>
        <Lines n={3} w={[96, 100, 64]} />
        <div style={{ position: "absolute", left: 44, right: 44, bottom: 40, borderTop: `4px solid ${INK}`, paddingTop: 22, fontSize: 52, fontWeight: 600 }}>
          <span style={{ color: RED, fontWeight: 700 }}>12 </span>
          <span style={{ position: "relative", display: "inline-block" }}>
            Vgl.
            <span style={{ position: "absolute", left: -6, top: "52%", height: 9, width: `${strike * 112}%`, background: RED, borderRadius: 5 }} />
          </span>{" "}
          Müller 2021, S. 14.
        </div>
      </div>
      <Pop at={0.25} style={{ position: "absolute", left: 120, top: 560 }}>
        <div style={{ background: "#fff", border: `6px solid ${RED}`, borderRadius: 24, padding: "14px 26px", fontSize: 46, fontWeight: 700, color: RED, rotate: "-3deg" }}>wörtliches Zitat</div>
      </Pop>
      <Pop at={vgl + 0.3} style={{ position: "absolute", right: 70, top: 700 }}>
        <div style={{ background: GREEN, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 28px", fontSize: 44, fontWeight: 700, rotate: "4deg" }}>→ ohne „Vgl.“</div>
      </Pop>
    </div>
  );
};

// ---------- 5 Fundstelle 2: Müller 2021 fehlt ----------
export const SceneFund2: React.FC<{ fehlt: number }> = ({ fehlt }) => {
  const { t, frame, fps } = useT();
  const shake = t >= fehlt && t < fehlt + 0.5 ? Math.sin(frame * 2) * 8 : 0;
  const rows = ["Bauer, Lena: Mobilität im Wandel. 2019.", "Destatis: Pressemitteilung Nr. 120. 2026.", "?", "Schmidt, Jonas: Pendeln in Bayern. 2022."];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 36, display: "flex", alignItems: "center", gap: 18 }}>
        <div style={{ background: RED, color: "#fff", borderRadius: 999, padding: "8px 26px", fontSize: 38, fontWeight: 700, border: `5px solid ${INK}` }}>Muss vor Abgabe</div>
        <div style={{ fontSize: 40, fontWeight: 700, color: MUTED }}>2 von 5</div>
      </div>
      <div style={{ position: "absolute", left: 50, right: 50, top: 150, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "30px 40px 40px", scale: String(Math.max(0.85, sp(t, -0.1, fps))) }}>
        <div style={{ fontSize: 50, fontWeight: 700 }}>Literaturverzeichnis</div>
        {rows.map((r, i) =>
          r === "?" ? (
            <div key={i} style={{ marginTop: 22, height: 92, borderRadius: 14, border: `6px dashed ${t >= fehlt ? RED : LINE}`, display: "flex", alignItems: "center", padding: "0 22px", fontSize: 42, fontWeight: 700, color: RED, translate: `${shake}px 0px` }}>
              {t >= fehlt ? "Müller 2021 … fehlt!" : ""}
            </div>
          ) : (
            <div key={i} style={{ marginTop: 22, fontSize: 38, fontWeight: 500, color: "#5B4636", lineHeight: 1.25, opacity: fade(t, 0.05 + i * 0.12) }}>{r}</div>
          )
        )}
      </div>
      <Pop at={0.15} style={{ position: "absolute", left: 90, top: 770 }}>
        <div style={{ background: "#FFF3C4", border: `5px solid ${INK}`, borderRadius: 20, padding: "12px 24px", fontSize: 44, fontWeight: 700, rotate: "-3deg" }}>
          im Text zitiert: <span style={{ color: NAVY }}>Müller 2021</span>
        </div>
      </Pop>
      <Beispiel style={{ right: 40, bottom: 26 }} />
    </div>
  );
};

// ---------- 6 „W-Seminar Quellen?“ → Screenshots ----------
export const SceneQuellen: React.FC<{ shots: number }> = ({ shots }) => {
  const { frame } = useT();
  const cursor = frame % 16 < 9;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 30, right: 30, top: 60, background: PAPER, border: `6px solid ${INK}`, borderRadius: 34, padding: "28px 24px" }}>
        <SearchBar text="w seminar quellen" cursor={cursor} />
      </div>
      {[0, 1, 2].map((i) => (
        <Pop key={i} at={shots + i * 0.18} style={{ position: "absolute", left: 120 + i * 230, top: 360 + (i % 2) * 50 }}>
          <div style={{ width: 260, height: 420, background: "#fff", border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", rotate: `${(i - 1) * 8 + Math.sin(frame / 7 + i) * 1.5}deg` }}>
            <div style={{ height: 50, background: "#EEF1F6", borderBottom: "3px solid #DDE2EA", display: "flex", alignItems: "center", padding: "0 12px", fontSize: 20, color: "#55606F", fontWeight: 600 }}>🔒 quelle-{i + 1}.de/…</div>
            <div style={{ padding: "6px 18px" }}>
              <Lines n={2} />
              <div style={{ marginTop: 16, height: 70, background: "#FFE27A", borderRadius: 8 }} />
              <Lines n={3} w={[100, 80, 90]} />
            </div>
          </div>
        </Pop>
      ))}
      <Pop at={shots + 0.5} style={{ position: "absolute", left: 0, right: 0, top: 860, textAlign: "center" }}>
        <div style={{ fontSize: 54, fontWeight: 700, color: MUTED }}>📸 deine Screenshots</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Beleg-PDF mit Link und Datum ----------
export const SceneBeleg: React.FC<{ link: number; datum: number }> = ({ link, datum }) => {
  const { t, fps } = useT();
  const ent = [
    { nr: "3.04", q: "Müller 2021, S. 14" },
    { nr: "3.05", q: "Destatis, PM Nr. 120" },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 90, right: 90, top: 40, height: 900, background: PAPER, border: `6px solid ${INK}`, borderRadius: 18, padding: "30px 40px", scale: String(Math.max(0.6, sp(t, -0.1, fps))), boxShadow: "0 16px 0 rgba(58,38,24,.12)" }}>
        <div style={{ position: "absolute", right: -20, top: -24, background: RED, color: "#fff", border: `5px solid ${INK}`, borderRadius: 16, padding: "6px 22px", fontSize: 40, fontWeight: 700, rotate: "6deg" }}>PDF</div>
        <div style={{ fontSize: 44, fontWeight: 700 }}>Quellenbelege</div>
        <div style={{ fontSize: 28, fontWeight: 600, color: MUTED }}>Stand 06.11.2026</div>
        {ent.map((e, i) => (
          <div key={e.nr} style={{ marginTop: 24, border: `4px solid ${LINE}`, borderRadius: 16, padding: "16px 20px", opacity: fade(t, 0.1 + i * 0.2) }}>
            <div style={{ fontSize: 34, fontWeight: 700 }}>
              <span style={{ color: NAVY }}>{e.nr}</span> · {e.q}
            </div>
            <div style={{ display: "flex", gap: 16, marginTop: 12 }}>
              <div style={{ flex: 1, height: 100, background: "#F3F0EA", borderRadius: 10, padding: "10px 12px" }}>
                <div style={{ height: 30, background: "#FFE27A", borderRadius: 6, marginTop: 24 }} />
              </div>
            </div>
            <div style={{ marginTop: 12, fontSize: 30, fontWeight: 600, display: "flex", gap: 20, flexWrap: "wrap" }}>
              <span style={{ background: t >= link ? "#DDEEFF" : "transparent", color: "#1A56C4", borderRadius: 8, padding: "2px 8px" }}>🔗 Link</span>
              <span style={{ background: t >= datum ? "#E3F1EA" : "transparent", color: GREEN, borderRadius: 8, padding: "2px 8px" }}>📅 abgerufen 06.11.2026</span>
            </div>
          </div>
        ))}
      </div>
      <Pop at={datum + 0.2} style={{ position: "absolute", left: 0, right: 0, top: 790, display: "flex", justifyContent: "center" }}>
        <div style={{ background: GREEN, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "12px 34px", fontSize: 48, fontWeight: 700 }}>✓ fertig zum Abgeben</div>
      </Pop>
    </div>
  );
};

// ---------- 8 Probe-Prüfung ----------
export const ScenePruefung: React.FC<{ frage: number }> = ({ frage }) => {
  const { t, frame } = useT();
  const wob = Math.sin(frame / 4) * 1.5;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead right={<span style={{ background: NAVY, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>🎓 Probe-Prüfung</span>} />
      <Pop at={frage - 0.25} style={{ position: "absolute", left: 40, right: 120, top: 170 }}>
        <div style={{ background: "#fff", border: `7px solid ${INK}`, borderRadius: 40, padding: "24px 36px 30px", rotate: `${-1.5 + wob}deg`, boxShadow: "0 14px 0 rgba(58,38,24,.12)" }}>
          <div style={{ fontSize: 30, fontWeight: 700, color: NAVY, letterSpacing: 2 }}>🧑‍🏫 LEHRKRAFT (geübt)</div>
          <div style={{ fontSize: 84, fontWeight: 700, lineHeight: 1.1, marginTop: 6 }}>„Wofür hast du KI benutzt?“</div>
        </div>
      </Pop>
      <div style={{ position: "absolute", right: 40, left: 220, top: 600, background: NAVY, color: "#fff", borderRadius: 30, padding: "22px 30px", fontSize: 42, lineHeight: 1.3, opacity: fade(t, frage + 0.9) }}>
        <div style={{ fontSize: 24, fontWeight: 700, letterSpacing: 2, opacity: 0.8 }}>DU</div>
        Für die Gliederung. Jede Zahl hab ich nachgeschlagen …
      </div>
      <div style={{ position: "absolute", left: 40, top: 850, background: "#E3F1EA", color: "#1C7049", borderRadius: 24, padding: "14px 26px", fontSize: 38, fontWeight: 700, opacity: fade(t, frage + 1.1) }}>✓ Quelle genannt. Nächstes Mal kürzer.</div>
    </div>
  );
};

// ---------- 9 Drei Schritte + kostenlos ----------
export const SceneSchritte: React.FC<{ s1: number; s2: number; s3: number; frei: number }> = ({ s1, s2, s3, frei }) => {
  const { frame } = useT();
  const steps = [
    { at: s1, n: 1, ico: "📦", t: "Skill holen" },
    { at: s2, n: 2, ico: "⬆️", t: "in Claude hochladen" },
    { at: s3, n: 3, ico: "📄", t: "Word-Datei rein" },
  ];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 40, textAlign: "center", fontSize: 70, fontWeight: 700, color: NAVY }}>3 Schritte</div>
      {steps.map((s, i) => (
        <Pop key={s.n} at={s.at} style={{ position: "absolute", left: 40, right: 40, top: 165 + i * 195 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 26, background: "#fff", border: `6px solid ${INK}`, borderRadius: 30, padding: "22px 30px", rotate: `${(i - 1) * 1.5 + Math.sin(frame / 8 + i) * 0.8}deg` }}>
            <div style={{ width: 100, height: 100, borderRadius: 50, background: GREEN, color: "#fff", border: `5px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 60, fontWeight: 700, flex: "none" }}>{s.n}</div>
            <div style={{ fontSize: 54, fontWeight: 700, flex: 1, whiteSpace: "nowrap" }}>{s.t}</div>
            <div style={{ fontSize: 70 }}>{s.ico}</div>
          </div>
        </Pop>
      ))}
      <Pop at={frei} style={{ position: "absolute", left: 0, right: 0, top: 800, display: "flex", justifyContent: "center" }}>
        <div style={{ background: "#E3F1EA", color: "#1C7049", border: `6px solid ${GREEN}`, borderRadius: 999, padding: "14px 38px", fontSize: 52, fontWeight: 700, rotate: "-2deg" }}>✓ läuft im kostenlosen Claude</div>
      </Pop>
    </div>
  );
};

// ---------- 10 Schluss: Handy mit der neuen Website + Adresse ----------
export const SceneEnde: React.FC<{ link: number }> = ({ link }) => {
  const { t, fps, frame } = useT();
  const s = Math.max(0.5, sp(t, -0.05, fps));
  const glow = 0.5 + 0.5 * Math.sin(frame / 4);
  const big = sp(t, link, fps);
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      {/* Handy (Nachzeichnung der Seite im neuen Look, ohne Preis) */}
      <div style={{ position: "absolute", left: 290, top: 26, width: 430, height: 660, background: "#FFF8EC", border: `10px solid ${INK}`, borderRadius: 54, overflow: "hidden", scale: String(s), rotate: "3deg", boxShadow: "0 18px 0 rgba(58,38,24,.15)" }}>
        <div style={{ height: 54, display: "flex", alignItems: "center", gap: 8, padding: "0 22px", fontSize: 22, fontWeight: 700, borderBottom: "2px solid rgba(58,38,24,.08)" }}>
          🐹 Hamster<span style={{ color: GREEN }}>frei</span>
          <span style={{ marginLeft: "auto", fontSize: 16, color: INK }}>Seminar</span>
        </div>
        <div style={{ background: "#fff", textAlign: "center", fontSize: 15, padding: "8px 10px", color: MUTED, borderBottom: `2px solid ${LINE}` }}>
          Abgabe in Bayern: meist am <b style={{ color: INK }}>10.11.</b>
        </div>
        <div style={{ textAlign: "center", padding: "30px 22px 0" }}>
          <div style={{ fontSize: 22, fontWeight: 700, color: GREEN }}>Seminararbeit-Profi</div>
          <div style={{ fontSize: 50, fontWeight: 700, lineHeight: 1.04, marginTop: 8, letterSpacing: -1 }}>
            Seminararbeit bis zum 10.11.?<br />
            <span style={{ color: FUR }}>Keine Angst.</span>
          </div>
          <div style={{ fontSize: 20, fontWeight: 600, color: MUTED, marginTop: 14, lineHeight: 1.3 }}>Ein Skill für dein Claude-Konto. Von der ersten Zeile bis zum Prüfungsgespräch.</div>
          <div style={{ display: "inline-block", marginTop: 20, background: GREEN, color: "#fff", borderRadius: 999, padding: "12px 30px", fontSize: 22, fontWeight: 700 }}>So funktioniert's ›</div>
          <div style={{ margin: "26px auto 0", width: 340, background: "#fff", borderRadius: 18, padding: "14px 16px", textAlign: "left", boxShadow: "0 0 0 2px rgba(58,38,24,.08)" }}>
            <div style={{ fontSize: 13, fontWeight: 800, color: MUTED, letterSpacing: 1 }}>DU BEKOMMST</div>
            <div style={{ display: "flex", gap: 6, marginTop: 6 }}>
              <div style={{ flex: 1, background: RED, color: "#fff", borderRadius: 8, padding: "4px 6px", fontSize: 22, fontWeight: 700 }}>5</div>
              <div style={{ flex: 1, background: SAND, borderRadius: 8, padding: "4px 6px", fontSize: 22, fontWeight: 700 }}>7</div>
              <div style={{ flex: 1, background: SAND, borderRadius: 8, padding: "4px 6px", fontSize: 22, fontWeight: 700 }}>31</div>
            </div>
          </div>
        </div>
      </div>
      {/* Zeigestab-Tipp aufs Handy */}
      <div style={{ position: "absolute", left: 250, top: 560, width: 90, height: 90, borderRadius: 45, border: `7px solid ${RED}`, scale: String(interpolate(t % 1.3, [0, 0.6], [0.6, 1.4], { extrapolateRight: "clamp" })), opacity: interpolate(t % 1.3, [0, 0.6, 0.9], [1, 0.6, 0], { extrapolateRight: "clamp" }) }} />
      {/* Adresse groß */}
      <div style={{ position: "absolute", left: 20, right: 20, top: 730, textAlign: "center" }}>
        <div style={{ display: "inline-block", fontSize: 66, fontWeight: 700, color: "#1A56C4", background: "#fff", border: `6px solid rgba(35,136,90,${0.5 + glow * 0.5})`, borderRadius: 26, padding: "8px 30px", scale: String(1 + 0.08 * big) }}>hamsterfrei.de/seminar</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 875, textAlign: "center", fontSize: 66, fontWeight: 700, color: GREEN, scale: String(Math.max(0.0001, big)), opacity: t >= link ? 1 : 0 }}>Link im Profil ☝️</div>
    </div>
  );
};
