import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";

// Folge13 · Hamster-Test „Notenrechner aus einem Satz“ · Einstiegs-Test E1 (Paar 1) · ohne Werbung · Leinwand 948×1004
// Ben + Noten vom Studio erfunden (docs/plaene/beispiel/schnitt_beispiel.txt).
// Rechner = Nachzeichnung von Claudes echtem Rechner (docs/plaene/beispiel/schnitt_rechner_claude.html), Werte aus dem Playwright-Test.
// Unten links (y > ~860, x < ~380) frei lassen: dort steht der Hamster.
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFFFF";
const DGREEN = "#1C7049";
const LRED = "#F9DEDA";
const APPBG = "#F4F5F7";
const BLUE = "#3B5BDB";
const LBLUE = "#E3E8FB";
const LTEAL = "#DDF3EA";
const TEAL = "#16865A";
const OCHRE = "#C49A1E";
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
  <div style={{ display: "inline-block", border: `5px solid ${color}`, color, borderRadius: 12, padding: "2px 14px", fontSize: size, fontWeight: 700, letterSpacing: 3, rotate: `${rot}deg`, background: "rgba(255,255,255,.9)", whiteSpace: "nowrap" }}>{text}</div>
);

const ClaudeHead: React.FC<{ size?: number; title?: string }> = ({ size = 32, title = "Claude" }) => (
  <div style={{ height: size * 2.1, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 14, padding: "0 24px", fontSize: size, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
    <div style={{ width: size * 0.65, height: size * 0.65, borderRadius: size, background: "#E5835E" }} />
    {title}
  </div>
);

const Badge: React.FC<{ v: string; color: string; fs: number }> = ({ v, color, fs }) => (
  <div style={{ background: LBLUE, color, fontSize: fs, fontWeight: 700, borderRadius: fs * 0.3, padding: `${fs * 0.06}px ${fs * 0.35}px` }}>{v}</div>
);

const FAECHER: [string, string, string][] = [
  ["Deutsch", "2,25", "#3F9E4D"],
  ["Mathematik", "3,20", OCHRE],
  ["Englisch", "2,17", "#3F9E4D"],
  ["Biologie", "2,50", OCHRE],
];

// Der Rechner (Nachzeichnung): Gesamtschnitt + Fachkärtchen
const Rechner: React.FC<{ w: number; fs: number; hl?: number; hlv?: number }> = ({ w, fs, hl = -1, hlv = 0 }) => (
  <div style={{ width: w, background: APPBG, border: `5px solid ${INK}`, borderRadius: 24, padding: fs * 0.45, boxShadow: "6px 8px 0 rgba(58,38,24,.14)", fontFamily: "Fredoka" }}>
    <div style={{ fontSize: fs * 0.95, fontWeight: 700, color: "#1E2430", marginBottom: fs * 0.3 }}>Notenrechner Halbjahr</div>
    <div style={{ background: PAPER, borderRadius: 18, border: "3px solid #E1E4EA", display: "flex", alignItems: "center", gap: fs * 0.5, padding: `${fs * 0.2}px ${fs * 0.5}px`, marginBottom: fs * 0.3 }}>
      <div style={{ fontSize: fs * 2.6, fontWeight: 700, color: OCHRE, lineHeight: 1 }}>2,53</div>
      <div style={{ fontSize: fs * 0.75, color: "#555E6E", lineHeight: 1.2 }}><b style={{ color: "#1E2430" }}>Gesamtschnitt</b><br />4 Fächer mit Noten</div>
    </div>
    <div style={{ display: "flex", flexDirection: "column", gap: fs * 0.2 }}>
      {FAECHER.map(([n, v, c], i) => {
        const on = i === hl ? hlv : 0;
        return (
          <div key={n} style={{ background: on ? "#FFF0C2" : PAPER, borderRadius: 14, border: `${3 + on * 4}px solid ${on ? RED : "#E1E4EA"}`, display: "flex", alignItems: "center", justifyContent: "space-between", padding: `${fs * 0.12}px ${fs * 0.4}px`, scale: S(1 + on * 0.04) }}>
            <div style={{ fontSize: fs, fontWeight: 700, color: "#1E2430" }}>{n}</div>
            <Badge v={v} color={c} fs={fs} />
          </div>
        );
      })}
    </div>
  </div>
);

// ---------- 0 Hook (E1): Rechner auf der Leinwand ab Frame 0 ----------
export const SceneHook: React.FC<{ bio: number }> = ({ bio }) => {
  const { t } = useT();
  const hlv = fade(t, bio, 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 20, right: 20, top: 14, textAlign: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 700, letterSpacing: 4, color: MUTED }}>HAMSTER-TEST</div>
        <div style={{ fontSize: 70, fontWeight: 700, lineHeight: 1.05, color: NAVY }}>1 Satz <span style={{ color: GREEN }}>→ Notenrechner</span></div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 150, rotate: "1deg" }}>
        <Rechner w={700} fs={40} hl={3} hlv={hlv} />
        <div style={{ position: "absolute", right: -10, top: -30 }}><Stempel size={22} text="BEISPIEL · NACHGEZEICHNET" rot={3} /></div>
      </div>
      <div style={{ position: "absolute", left: 290, top: 800, fontSize: 62, fontWeight: 700, color: RED, opacity: hlv, scale: S(0.8 + 0.2 * hlv), rotate: "-2deg", whiteSpace: "nowrap" }}>⬆ zählt Bio zu viel?</div>
    </div>
  );
};

// ---------- 1 Der eine Satz (echt, wörtlich) ----------
export const SceneSatz: React.FC<{ doppelt: number; einfach: number }> = ({ doppelt, einfach }) => {
  const { t, fps } = useT();
  const mark = (txt: string, a: number) => (
    <span style={{ background: t >= a ? "#CDEBD9" : "transparent", color: t >= a ? DGREEN : INK, borderRadius: 8, padding: "0 4px" }}>{txt}</span>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 48, fontWeight: 700, color: NAVY }}>Mein ganzer Auftrag:</div>
      <div style={{ position: "absolute", left: 40, right: 30, top: 120, scale: S(sp(t, 0, fps)), transformOrigin: "top right" }}>
        <div style={{ background: "#F1E6D3", border: `4px solid ${INK}`, borderRadius: "30px 30px 6px 30px", padding: "18px 26px", fontSize: 50, fontWeight: 600, lineHeight: 1.3 }}>
          <div style={{ fontSize: 30, color: MUTED, marginBottom: 6 }}>An Claude · 1 Satz:</div>
          „Bau mir einen Notenrechner fürs Halbjahr, in den ich pro Fach meine Noten eintrage, wobei {mark("Schulaufgaben doppelt", doppelt)} und {mark("mündliche Noten einfach", einfach)} zählen, und der mir den Schnitt pro Fach und insgesamt anzeigt.“
        </div>
      </div>
      <Pop at={einfach + 0.4} style={{ position: "absolute", left: 470, top: 640 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, background: PAPER, border: `5px solid ${GREEN}`, borderRadius: 20, padding: "12px 24px", fontSize: 46, fontWeight: 700, color: DGREEN }}>
          ✓ fertiger Rechner
        </div>
      </Pop>
    </div>
  );
};

// Fachkarte im Rechner-Look mit Noten-Chips
const Chip: React.FC<{ g: number; sa: boolean; a: number; fs: number }> = ({ g, sa, a, fs }) => (
  <div style={{ width: fs * 1.5, height: fs * 1.5, borderRadius: 14, background: sa ? LBLUE : LTEAL, color: sa ? BLUE : TEAL, fontSize: fs, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", opacity: a, scale: S(a) }}>{g}</div>
);
const Fach: React.FC<{ name: string; sa: number[]; m: number[]; avg: string; avgColor: string; fs: number; ca?: number[]; avgA?: number }> = ({ name, sa, m, avg, avgColor, fs, ca = [], avgA = 1 }) => {
  let k = 0;
  const row = (label: string, gs: number[], isSa: boolean) => (
    <div style={{ display: "flex", alignItems: "center", gap: fs * 0.4, marginTop: fs * 0.3 }}>
      <div style={{ width: fs * 6.4, fontSize: fs * 0.8, color: "#1E2430", fontWeight: 700, lineHeight: 1.1 }}>{label}<div style={{ fontSize: fs * 0.55, color: "#6B7280", fontWeight: 500 }}>{isSa ? "zählen ×2" : "zählen ×1"}</div></div>
      {gs.length === 0 ? <div style={{ fontSize: fs * 0.7, fontStyle: "italic", color: "#6B7280" }}>noch keine</div> : gs.map((g) => <Chip key={k} g={g} sa={isSa} a={ca[k++] ?? 1} fs={fs} />)}
    </div>
  );
  return (
    <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, padding: `${fs * 0.4}px ${fs * 0.6}px ${fs * 0.5}px`, boxShadow: "6px 8px 0 rgba(58,38,24,.12)" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ fontSize: fs * 1.1, fontWeight: 700, color: "#1E2430" }}>{name}</div>
        <div style={{ opacity: avgA }}><Badge v={avg} color={avgColor} fs={fs * 1.1} /></div>
      </div>
      {row("Schulaufgaben", sa, true)}
      {row("Mündlich", m, false)}
    </div>
  );
};

// ---------- 2 Bens Mathe ----------
export const SceneMathe: React.FC<{ vier: number; drei: number; zwei: number }> = ({ vier, drei, zwei }) => {
  const { t, fps } = useT();
  const a = (x: number) => (t < x ? 0 : spring({ frame: (t - x) * fps, fps, config: { damping: 10, stiffness: 200 } }));
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 26 }}><Stempel size={28} text="BEISPIEL · Ben ist erfunden" rot={-3} /></div>
      <div style={{ position: "absolute", left: 40, top: 120, fontSize: 56, fontWeight: 700, color: NAVY }}>Bens Noten tippen</div>
      <div style={{ position: "absolute", left: 60, right: 40, top: 230, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <Fach name="Mathematik" sa={[4, 3]} m={[2]} avg="–" avgColor={MUTED} fs={64} ca={[a(vier), a(drei), a(zwei)]} avgA={0.35} />
      </div>
    </div>
  );
};

// ---------- 3 Rechner vs. Handrechnung ----------
export const SceneNachrechnen: React.FC<{ hand: number }> = ({ hand }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 24, fontSize: 50, fontWeight: 700, color: MUTED }}>Mathematik</div>
      <div style={{ position: "absolute", left: 50, top: 110, width: 380, textAlign: "center", scale: S(sp(t, 0, fps)) }}>
        <div style={{ fontSize: 40, fontWeight: 700, color: NAVY, marginBottom: 10 }}>Rechner</div>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 24, padding: "30px 0" }}>
          <div style={{ display: "inline-block", background: LBLUE, color: OCHRE, fontSize: 120, fontWeight: 700, borderRadius: 26, padding: "0 30px" }}>3,20</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 470, top: 110, width: 440, opacity: fade(t, hand), translate: `0px ${(1 - fade(t, hand)) * 40}px`, rotate: "2deg" }}>
        <div style={{ fontSize: 40, fontWeight: 700, color: NAVY, marginBottom: 10, textAlign: "center" }}>Von Hand</div>
        <div style={{ background: "#FFFDF5", backgroundImage: "linear-gradient(#DCE6F5 2px, transparent 2px), linear-gradient(90deg, #DCE6F5 2px, transparent 2px)", backgroundSize: "34px 34px", border: `5px solid ${INK}`, borderRadius: 16, padding: "22px 20px", fontFamily: HAND, color: "#2E3F8F", fontSize: 44, lineHeight: 1.35 }}>
          (4×2 + 3×2 + 2)<br />÷ (2 + 2 + 1)<br />= 16 ÷ 5<br /><b style={{ fontSize: 60 }}>= 3,20</b>
        </div>
      </div>
      <Pop at={hand + 0.9} style={{ position: "absolute", left: 300, top: 640 }}>
        <div style={{ fontSize: 96, fontWeight: 700, color: GREEN, whiteSpace: "nowrap" }}>✓ stimmt</div>
      </Pop>
    </div>
  );
};

// ---------- 4 Bio ohne Schulaufgabe ----------
export const SceneBio: React.FC<{ ok: number }> = ({ ok }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: "#EEF2F8" }}>
      <div style={{ position: "absolute", left: 40, top: 26, fontSize: 52, fontWeight: 700, color: NAVY }}>Ohne Schulaufgabe?</div>
      <div style={{ position: "absolute", left: 60, right: 40, top: 140, scale: S(sp(t, 0, fps)), transformOrigin: "top center" }}>
        <Fach name="Biologie" sa={[]} m={[2, 3]} avg="2,50" avgColor={OCHRE} fs={52} avgA={fade(t, ok)} />
      </div>
      <Pop at={ok + 0.2} style={{ position: "absolute", left: 330, top: 560 }}>
        <div style={{ fontFamily: HAND, color: "#2E3F8F", fontSize: 58, whiteSpace: "nowrap", background: "#FFFDF5", border: `4px solid ${INK}`, borderRadius: 14, padding: "10px 22px", rotate: "-2deg" }}>(2 + 3) ÷ 2 = 2,50 <span style={{ color: GREEN, fontFamily: "Fredoka", fontWeight: 700 }}>✓</span></div>
      </Pop>
    </div>
  );
};

// ---------- 5 Gesamtschnitt ----------
export const SceneGesamt: React.FC<{ stimmt: number }> = ({ stimmt }) => {
  const { t, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 30, textAlign: "center", fontSize: 52, fontWeight: 700, color: MUTED }}>Gesamtschnitt</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 110, display: "flex", justifyContent: "center", scale: S(sp(t, 0, fps)) }}>
        <div style={{ background: PAPER, border: `6px solid ${INK}`, borderRadius: 30, padding: "10px 60px", fontSize: 230, fontWeight: 700, color: OCHRE, lineHeight: 1.1 }}>2,53</div>
      </div>
      <div style={{ position: "absolute", left: 120, right: 60, top: 470, opacity: fade(t, stimmt - 0.6), fontFamily: HAND, color: "#2E3F8F", fontSize: 50, lineHeight: 1.35 }}>
        von Hand:<br />(3,20 + 2,25 + 2,17 + 2,50) ÷ 4
      </div>
      <Pop at={stimmt} style={{ position: "absolute", left: 420, top: 640 }}>
        <div style={{ fontSize: 96, fontWeight: 700, color: GREEN, whiteSpace: "nowrap" }}>= 2,53 ✓</div>
      </Pop>
    </div>
  );
};

// ---------- 6 Der Haken: Waage Bio = Mathe ----------
export const SceneWaage: React.FC<{ bio: number; zitat: number }> = ({ bio, zitat }) => {
  const { t, frame } = useT();
  const wob = Math.sin(frame / 6) * 1.5 * (1 - fade(t, bio + 0.8, 0.6));
  const pan = (label: string, sub: string, chips: [number, boolean][], c: string) => (
    <div style={{ width: 385, textAlign: "center" }}>
      <div style={{ background: PAPER, border: `5px solid ${c}`, borderRadius: 20, padding: "10px 12px" }}>
        <div style={{ fontSize: 54, fontWeight: 700, color: INK }}>{label}</div>
        <div style={{ display: "flex", gap: 8, justifyContent: "center", margin: "8px 0" }}>
          {chips.map(([g, sa], i) => <Chip key={i} g={g} sa={sa} a={1} fs={46} />)}
        </div>
        <div style={{ fontSize: 32, color: MUTED, fontWeight: 600 }}>{sub}</div>
      </div>
    </div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 40, top: 22, fontSize: 54, fontWeight: 700, color: RED }}>Aber: jedes Fach zählt gleich</div>
      <div style={{ position: "absolute", left: 469, top: 190, width: 10, height: 330, background: INK, borderRadius: 5 }} />
      <div style={{ position: "absolute", left: 404, top: 500, width: 140, height: 30, background: INK, borderRadius: 10 }} />
      <div style={{ position: "absolute", left: 60, top: 150, width: 830, rotate: `${wob}deg` }}>
        <div style={{ height: 12, background: INK, borderRadius: 6 }} />
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 20 }}>
          {pan("Biologie", "nur 2 mündliche", [[2, false], [3, false]], "#D9772B")}
          {pan("Mathematik", "2 Schulaufgaben + 1", [[4, true], [3, true], [2, false]], NAVY)}
        </div>
      </div>
      <Pop at={bio} style={{ position: "absolute", left: 0, right: 0, top: 560, textAlign: "center" }}>
        <div style={{ fontSize: 70, fontWeight: 700, color: RED }}>Bio zählt wie Mathe</div>
      </Pop>
      <Pop at={zitat} style={{ position: "absolute", left: 330, right: 20, top: 690 }}>
        <div style={{ background: PAPER, border: `5px solid ${INK}`, borderRadius: 22, overflow: "hidden" }}>
          <ClaudeHead size={30} />
          <div style={{ padding: "10px 20px 14px", fontSize: 44, fontWeight: 600, lineHeight: 1.25 }}>„… <b style={{ color: RED }}>jedes Fach zählt also gleich viel.</b>“</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- 7 Urteil ----------
export const SceneUrteil: React.FC<{ stempel: number; zeilen: number }> = ({ stempel, zeilen }) => {
  const { t, fps } = useT();
  const s = t < stempel ? 0 : spring({ frame: (t - stempel) * fps, fps, config: { damping: 9, stiffness: 220 } });
  const z: [string, boolean][] = [["Doppelt zählen", true], ["Ohne Schulaufgabe", true], ["Gesamt richtig", true], ["Fächer gleich schwer", false]];
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 36, textAlign: "center", fontSize: 50, fontWeight: 700, color: MUTED }}>Urteil des Hamsters</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 130, display: "flex", justifyContent: "center" }}>
        <div style={{ border: `14px solid ${GREEN}`, color: DGREEN, borderRadius: 30, padding: "0 40px", fontSize: 128, fontWeight: 700, letterSpacing: 6, rotate: "-7deg", scale: S(s === 0 ? 0 : 2.2 - 1.2 * s), opacity: s === 0 ? 0 : 1, background: "rgba(255,255,255,.7)" }}>GEKLAPPT</div>
      </div>
      <div style={{ position: "absolute", left: 280, right: 10, top: 420, display: "flex", flexDirection: "column", gap: 22, fontSize: 54, whiteSpace: "nowrap", fontWeight: 700 }}>
        {z.map(([txt, ok], i) => (
          <div key={txt} style={{ opacity: fade(t, zeilen + i * 0.22), color: ok ? INK : RED, background: ok ? "transparent" : LRED, borderRadius: 12, padding: "0 8px" }}>{txt} <span style={{ color: ok ? GREEN : RED }}>{ok ? "✓" : "✗"}</span></div>
        ))}
      </div>
    </div>
  );
};

// ---------- 8 Ende: Handy + Kommentar SCHNITT ----------
export const SceneEnde: React.FC<{ commentAt: number }> = ({ commentAt }) => {
  const { frame, fps } = useT();
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 430, height: 800, background: "#1F1A24", border: `8px solid ${INK}`, borderRadius: 60, padding: 22, display: "flex", flexDirection: "column", marginBottom: 90, marginLeft: 200 }}>
        <div style={{ flex: 1, borderRadius: 40, background: "#FFF8EC", position: "relative", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 16 }}>
          <div style={{ fontSize: 100 }}>🧮</div>
          <div style={{ fontSize: 50, fontWeight: 700, textAlign: "center", lineHeight: 1.12 }}>Der Satz<br />zum<br />Kopieren</div>
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
          <div style={{ fontSize: 66, fontWeight: 600, color: INK, letterSpacing: 3 }}>SCHNITT</div>
        </div>
      </Pop>
    </div>
  );
};
