import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge03 · „Wie viel zahlst du für Abos?“ · Hook-Test Variante B · ohne Werbung · Leinwand 948×1004
// Beispiel-Kontoauszug ist erfunden (docs/plaene/beispiel/kontoauszug_oktober_beispiel.txt). Keine Logos, Namen nur als Text.
// Zeiten in den Props = Sekunden ab Szenenstart. Unten links (y > ~860) frei lassen: dort steht der Hamster.
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

const ClaudeHead: React.FC<{ right?: React.ReactNode }> = ({ right }) => (
  <div style={{ height: 84, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 30px", fontSize: 36, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: 24, height: 24, borderRadius: 12, background: "#E5835E" }} />
    Claude
    {right && <span style={{ marginLeft: "auto" }}>{right}</span>}
  </div>
);

const BeispielStempel: React.FC<{ size?: number; rot?: number }> = ({ size = 34, rot = -8 }) => (
  <div style={{ display: "inline-block", border: `5px solid ${RED}`, color: RED, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.85)" }}>BEISPIEL</div>
);

export const ABOS = [
  { n: "D-Ticket", p: "63,00" },
  { n: "Fitnessstudio", p: "24,99" },
  { n: "Handyvertrag", p: "9,99" },
  { n: "Spotify", p: "6,99" },
  { n: "Netflix", p: "6,99" },
  { n: "Apple", p: "4,99" },
  { n: "Apple", p: "0,99" },
];

// Beispiel-Auszug (erfunden), abo: gehört zu Claudes Abo-Liste, kauf: von Claude aussortiert
const AUSZUG = [
  { d: "01.10.", t: "NEBENJOB CAFE LOHN", b: "+480,00" },
  { d: "01.10.", t: "MIETE WG", b: "−390,00" },
  { d: "02.10.", t: "SPOTIFY P2F8K1Q7", b: "−6,99", abo: true },
  { d: "04.10.", t: "REWE", b: "−23,47" },
  { d: "05.10.", t: "NETFLIX.COM", b: "−6,99", abo: true },
  { d: "06.10.", t: "DB VERTRIEB D-TICKET", b: "−63,00", abo: true },
  { d: "08.10.", t: "PAYPAL *APPLE.COM/BILL", b: "−0,99", abo: true, apple: true },
  { d: "10.10.", t: "FITHAUS GMBH BEITRAG", b: "−24,99", abo: true },
  { d: "12.10.", t: "LIDL", b: "−18,30" },
  { d: "15.10.", t: "PAYPAL *STEAM GAMES", b: "−19,99", kauf: true },
  { d: "18.10.", t: "KLARNA LASTSCHRIFT", b: "−29,99", kauf: true },
  { d: "20.10.", t: "MOBILFUNK GMBH", b: "−9,99", abo: true },
  { d: "25.10.", t: "APPLE.COM/BILL", b: "−4,99", abo: true, apple: true },
  { d: "28.10.", t: "DOENER ECK", b: "−7,50" },
];

// Abo-Karte (Claudes Ergebnis) – Frame 0 und Szene 4
const AboKarte: React.FC<{ shown?: number; sumScale?: number; ring?: number; width?: number; fontSize?: number }> = ({ shown = 7, sumScale = 1, ring = 1, width = 560, fontSize = 40 }) => (
  <div style={{ width, background: PAPER, border: `6px solid ${INK}`, borderRadius: 26, overflow: "hidden", boxShadow: "0 10px 0 rgba(58,38,24,.12)" }}>
    <ClaudeHead right={<span style={{ fontSize: 30, color: MUTED }}>Deine Abos</span>} />
    <div style={{ padding: "8px 26px 0" }}>
      {ABOS.map((a, i) => (
        <div key={i} style={{ display: "flex", justifyContent: "space-between", fontSize, fontWeight: 600, lineHeight: 1.32, opacity: i < shown ? 1 : 0.12 }}>
          <span>{a.n}</span>
          <span style={{ color: NAVY }}>{a.p} €</span>
        </div>
      ))}
    </div>
    <div style={{ position: "relative", margin: "10px 18px 20px", padding: "6px 0 4px", borderTop: `4px solid ${INK}`, textAlign: "center" }}>
      <div style={{ fontSize: 68, fontWeight: 700, scale: S(sumScale), lineHeight: 1.1 }}>117,94 € <span style={{ fontSize: 36, color: MUTED }}>/ Monat</span></div>
      <svg viewBox="0 0 200 60" preserveAspectRatio="none" style={{ position: "absolute", left: -8, top: -6, width: "104%", height: 100, pointerEvents: "none" }}>
        <ellipse cx={100} cy={30} rx={97} ry={26} fill="none" stroke={RED} strokeWidth={2.4} strokeDasharray={420} strokeDashoffset={420 * (1 - ring)} strokeLinecap="round" />
      </svg>
    </div>
  </div>
);

// Kontoauszug-Streifen (Papier) mit optional markierten Abo-Zeilen
const Streifen: React.FC<{ marked?: number; fontSize?: number; width?: number; strike?: number; appleQ?: number }> = ({ marked = 0, fontSize = 22, width = 330, strike = -1, appleQ = -1 }) => {
  let k = 0;
  return (
    <div style={{ width, background: "#FBFBF7", border: `4px solid ${INK}`, borderRadius: 8, padding: "10px 12px", fontFamily: "monospace", fontSize, lineHeight: 1.55, color: "#3a3a3a" }}>
      {AUSZUG.map((r, i) => {
        const isMarked = r.abo && k++ < marked;
        return (
          <div key={i} style={{ position: "relative", display: "flex", justifyContent: "space-between", gap: 8, background: isMarked ? MARK : "transparent", opacity: r.kauf && strike >= 0 ? 0.45 : 1 }}>
            <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{r.t}</span>
            <span style={{ whiteSpace: "nowrap" }}>{r.b}</span>
            {r.kauf && strike >= 0 && <div style={{ position: "absolute", left: 0, top: "50%", height: 3, width: `${strike * 100}%`, background: INK }} />}
            {r.apple && appleQ >= 0 && <span style={{ position: "absolute", right: -46, top: -8, fontSize: fontSize * 1.6, fontWeight: 700, color: RED, fontFamily: "Fredoka", scale: S(appleQ) }}>?</span>}
          </div>
        );
      })}
    </div>
  );
};

// ---------- 1 Hook: Ergebnis ab Frame 0 ----------
// Bild-Kritik R1: Zeigestab-Spitze liegt bei Leinwand ~ (440, 930) → dort hängt das Summen-Schild.
export const SceneHook: React.FC = () => {
  const { frame } = useT();
  const pulse = 1 + Math.max(0, Math.sin(frame / 5)) * 0.05;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 22, textAlign: "center", fontSize: 60, fontWeight: 700, lineHeight: 1.08, color: NAVY }}>
        Abos finden:<br /><span style={{ color: GREEN }}>Wie viel zahlst du?</span>
      </div>
      {/* Kontoauszug als schräg hereinragendes Blatt, ganz im Bild */}
      <div style={{ position: "absolute", left: 22, top: 200, rotate: "-4deg" }}>
        <div style={{ position: "absolute", left: 0, top: -48, zIndex: 2 }}>
          <BeispielStempel size={28} />
        </div>
        <Streifen marked={7} fontSize={17} width={290} />
      </div>
      <div style={{ position: "absolute", left: 312, top: 400, fontSize: 70, fontWeight: 700, color: GREEN }}>➜</div>
      <div style={{ position: "absolute", right: 26, top: 180 }}>
        <AboKarte ring={1} width={540} fontSize={36} />
      </div>
      {/* Summen-Schild genau an der Zeigestab-Spitze */}
      <div style={{ position: "absolute", left: 395, top: 805, rotate: "-5deg", scale: String(pulse) }}>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 12, background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: "16px 34px 34px 16px", padding: "6px 22px 6px 14px", fontSize: 52, fontWeight: 700, color: RED, whiteSpace: "nowrap" }}>
          <div style={{ width: 18, height: 18, borderRadius: 9, background: CREAM, border: `4px solid ${INK}` }} />
          117,94 € / Monat
        </div>
      </div>
    </div>
  );
};

// ---------- 2 Kopieren + schwärzen ----------
export const SceneKopier: React.FC<{ schwarz: number }> = ({ schwarz }) => {
  const { t, fps } = useT();
  const w = interpolate(t, [schwarz, schwarz + 0.5], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <ClaudeHead />
      <div style={{ position: "absolute", left: 40, right: 36, top: 140, background: "#F1E6D3", borderRadius: 30, padding: "26px 28px", scale: S(sp(t, 0.05, fps)), transformOrigin: "top right" }}>
        <div style={{ fontSize: 50, fontWeight: 700, marginBottom: 16 }}>Welche Abos zahle ich? 📋</div>
        <div style={{ fontFamily: "monospace", fontSize: 33, lineHeight: 1.6, background: PAPER, border: `3px solid ${INK}`, borderRadius: 10, padding: "10px 16px" }}>
          {[
            ["Kontoinhaber: Max Muster", true],
            ["IBAN DE12 3456 7890 1234 5678 90", true],
            ["02.10. SPOTIFY ......  −6,99", false],
            ["05.10. NETFLIX.COM ... −6,99", false],
            ["06.10. D-TICKET ...... −63,00", false],
            ["…", false],
          ].map(([line, secret], i) => (
            <div key={i} style={{ position: "relative", whiteSpace: "nowrap" }}>
              {line as string}
              {secret && <div style={{ position: "absolute", left: -4, top: 4, bottom: 4, width: `${w}%`, background: "#111", borderRadius: 4 }} />}
            </div>
          ))}
        </div>
      </div>
      <Pop at={schwarz + 0.3} style={{ position: "absolute", left: 300, right: 36, top: 690 }}>
        <div style={{ background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: 22, padding: "10px 24px", fontSize: 44, fontWeight: 700, color: RED, lineHeight: 1.15 }}>✏️ vorher schwärzen:<br />Name, IBAN, andere Personen</div>
      </Pop>
    </div>
  );
};

// ---------- 3 Beispiel-Auszug ----------
export const SceneAuszug: React.FC = () => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 30, fontSize: 52, fontWeight: 700 }}>Kontoauszug Oktober</div>
      <div style={{ position: "absolute", left: 60, top: 120, scale: S(sp(t, 0.05, fps)), transformOrigin: "top left" }}>
        <Streifen fontSize={34} width={820} />
      </div>
      <div style={{ position: "absolute", right: 40, top: 30 }}>
        <BeispielStempel size={44} rot={6} />
      </div>
      <div style={{ position: "absolute", right: 40, bottom: 26, fontSize: 30, fontWeight: 600, color: MUTED }}>erfunden · Preise echt (Stand 11/2026)</div>
    </div>
  );
};

// ---------- 4 Sieben Abos + Summe ----------
export const SceneSieben: React.FC<{ summe: number }> = ({ summe }) => {
  const { t, fps } = useT();
  const shown = Math.min(7, Math.floor(interpolate(t, [0.1, 1.5], [0, 7], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })) + (t >= 0.1 ? 1 : 0));
  const ring = interpolate(t, [summe + 0.3, summe + 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 40, display: "flex", alignItems: "center", gap: 20 }}>
        <div style={{ width: 120, height: 120, borderRadius: 60, background: GREEN, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 84, fontWeight: 700, border: `6px solid ${INK}` }}>{shown}</div>
        <div style={{ fontSize: 60, fontWeight: 700 }}>Abos gefunden</div>
      </div>
      <div style={{ position: "absolute", left: 130, right: 130, top: 200, scale: S(t < summe ? 1 : 1 + 0.04 * sp(t, summe, fps)) }}>
        <AboKarte shown={shown} ring={ring} width={688} fontSize={44} sumScale={t < summe ? 0.0001 : sp(t, summe, fps)} />
      </div>
    </div>
  );
};

// ---------- 5 Steam + Klarna aussortiert ----------
export const SceneKauf: React.FC<{ einkauf: number }> = ({ einkauf }) => {
  const { t } = useT();
  const strike = interpolate(t, [0.2, 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 34, fontSize: 54, fontWeight: 700 }}>Nicht mitgezählt:</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 140, display: "flex", flexDirection: "column", gap: 28 }}>
        {[
          ["PAYPAL *STEAM GAMES", "−19,99"],
          ["KLARNA LASTSCHRIFT", "−29,99"],
        ].map(([n, b], i) => (
          <div key={n} style={{ position: "relative", background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: "22px 26px", display: "flex", justifyContent: "space-between", fontFamily: "monospace", fontSize: 44, fontWeight: 700, opacity: fade(t, i * 0.15, 0.2) }}>
            <span>{n}</span>
            <span>{b}</span>
            <div style={{ position: "absolute", left: 18, top: "50%", height: 6, width: `${strike * 94}%`, background: RED, borderRadius: 3 }} />
          </div>
        ))}
      </div>
      <Pop at={einkauf} style={{ position: "absolute", left: 0, right: 0, top: 520, display: "flex", justifyContent: "center" }}>
        <div style={{ background: "#E9E2D6", border: `6px solid ${MUTED}`, borderRadius: 24, padding: "10px 40px", fontSize: 72, fontWeight: 700, color: INK, rotate: "-3deg" }}>🛒 eher Einkäufe</div>
      </Pop>
      <div style={{ position: "absolute", left: 300, right: 40, top: 720, fontSize: 36, fontWeight: 600, color: MUTED, opacity: fade(t, einkauf + 0.4), lineHeight: 1.2 }}>Claude: Klarna „meist Ratenzahlung oder Online-Kauf“</div>
    </div>
  );
};

// ---------- 6 Zweimal Apple ----------
export const SceneApple: React.FC<{ wofuer: number; handy: number }> = ({ wofuer, handy }) => {
  const { t, fps, frame } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ position: "absolute", left: 40, right: 40, top: 34, fontSize: 60, fontWeight: 700, color: RED }}>Aber: zweimal Apple</div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 150, display: "flex", flexDirection: "column", gap: 24 }}>
        {[
          ["PAYPAL *APPLE.COM/BILL", "−0,99"],
          ["APPLE.COM/BILL", "−4,99"],
        ].map(([n, b]) => (
          <div key={n} style={{ position: "relative", background: MARK, border: `5px solid ${INK}`, borderRadius: 18, padding: "20px 26px", display: "flex", justifyContent: "space-between", fontFamily: "monospace", fontSize: 42, fontWeight: 700 }}>
            <span>{n}</span>
            <span>{b}</span>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", right: 70, top: 440, fontSize: 200, fontWeight: 700, color: RED, scale: S(sp(t, wofuer, fps)), rotate: `${Math.sin(frame / 4) * 7}deg` }}>?</div>
      <div style={{ position: "absolute", left: 300, top: 470, width: 380, background: PAPER, border: `5px solid ${INK}`, borderRadius: "30px 30px 30px 6px", padding: "16px 22px", fontSize: 36, fontWeight: 600, lineHeight: 1.2, opacity: fade(t, wofuer + 0.3) }}>Claude: „weiß ich nicht genau, wofür“</div>
      <Pop at={handy} style={{ position: "absolute", left: 300, top: 720 }}>
        <div style={{ background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "12px 28px", fontSize: 44, fontWeight: 700 }}>📱 Einstellungen → Abos</div>
      </Pop>
    </div>
  );
};

// ---------- 7 Beispiel: nach Miete 90 € vs. Abos 117,94 € ----------
export const SceneMiete: React.FC<{ neunzig: number; abos: number }> = ({ neunzig, abos }) => {
  const { t } = useT();
  const max = 740;
  const b1 = interpolate(t, [neunzig, neunzig + 0.5], [0, (90 / 117.94) * max], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const b2 = interpolate(t, [abos, abos + 0.6], [0, max], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 34, display: "flex", alignItems: "center", gap: 24 }}>
        <div style={{ fontSize: 50, fontWeight: 700 }}>Im Beispiel:</div>
        <BeispielStempel size={30} rot={-4} />
      </div>
      <div style={{ position: "absolute", left: 40, right: 40, top: 150, fontSize: 40, fontWeight: 600, color: MUTED }}>480 € rein − 390 € Miete</div>
      <div style={{ position: "absolute", left: 40, top: 250 }}>
        <div style={{ fontSize: 44, fontWeight: 700, marginBottom: 10 }}>nach Miete übrig</div>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div style={{ width: b1, height: 90, background: GREEN, border: `5px solid ${INK}`, borderRadius: 14 }} />
          <div style={{ fontSize: 64, fontWeight: 700, opacity: fade(t, neunzig + 0.3) }}>90 €</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 40, top: 470 }}>
        <div style={{ fontSize: 44, fontWeight: 700, marginBottom: 10, opacity: fade(t, abos - 0.2) }}>Abos</div>
        <div style={{ position: "relative", width: b2, height: 90, background: RED, border: `5px solid ${INK}`, borderRadius: 14 }}>
          <div style={{ position: "absolute", right: 18, top: 6, fontSize: 60, fontWeight: 700, color: "#fff", opacity: fade(t, abos + 0.4) }}>117,94 €</div>
        </div>
      </div>
      <Pop at={abos + 0.6} style={{ position: "absolute", left: 250, right: 30, top: 690 }}>
        <div style={{ background: "#FDE3DF", border: `6px solid ${RED}`, borderRadius: 22, padding: "8px 28px", fontSize: 56, fontWeight: 700, color: RED }}>Abos kosten mehr 😬</div>
      </Pop>
    </div>
  );
};

// ---------- 8 Urteil: GEKLAPPT ----------
export const SceneUrteil: React.FC<{ stempel: number; summe: number }> = ({ stempel, summe }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: "#1C7049", borderRadius: 30, padding: "0 46px", fontSize: 160, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 300, right: 40, top: 420, display: "flex", flexDirection: "column", gap: 18, fontSize: 60, fontWeight: 700 }}>
        <div style={{ opacity: fade(t, stempel + 0.3) }}>Abos gefunden <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, summe) }}>Summe stimmt <span style={{ color: GREEN }}>✓</span></div>
        <div style={{ opacity: fade(t, summe + 0.3), fontSize: 46, color: MUTED }}>Apple: selbst nachschauen</div>
      </div>
    </div>
  );
};

// ---------- 9 Ende: Handy + Kommentar ABO ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>📋</div>
          <div style={{ fontSize: 54, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Meine Frage<br />zum<br />Kopieren</div>
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
          <div style={{ fontSize: 92, fontWeight: 600, color: INK, letterSpacing: 4 }}>ABO</div>
        </div>
      </Pop>
    </div>
  );
};
