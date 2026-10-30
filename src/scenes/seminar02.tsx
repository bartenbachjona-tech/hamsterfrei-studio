import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { INK, GREEN, NAVY, CREAM, Pop } from "../Scenes";
import { Hamster } from "../Hamster";

// Seminar-Offensive S1 · „5 Fehler in deiner Seminararbeit“ · Leinwand 948×1004
const RED = "#C8473A";
const MUTED = "#6B5444";
const PAPER = "#FFFDF8";

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { t: frame / fps, frame, fps };
};
const fade = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const sp = (t: number, a: number, fps: number) => (t < a ? 0 : spring({ frame: (t - a) * fps, fps, config: { damping: 13, stiffness: 170 } }));

const Num: React.FC<{ n: number; title: string }> = ({ n, title }) => {
  const { t, fps } = useT();
  const s = sp(t, 0, fps);
  return (
    <div style={{ position: "absolute", left: 40, top: 36, display: "flex", alignItems: "center", gap: 22, scale: String(s), transformOrigin: "left center" }}>
      <div style={{ width: 110, height: 110, borderRadius: 55, background: RED, color: "#fff", border: `6px solid ${INK}`, display: "grid", placeItems: "center", fontSize: 72, fontWeight: 700 }}>{n}</div>
      <div style={{ fontSize: 54, fontWeight: 700 }}>{title}</div>
    </div>
  );
};

// Ein Blatt Papier mit Text und Fußnotenbereich
const Paper: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{ position: "absolute", background: PAPER, border: `5px solid ${INK}`, borderRadius: 18, padding: "30px 36px", boxShadow: "0 14px 0 rgba(58,38,24,.10)", ...style }}>{children}</div>
);
const Lines: React.FC<{ n: number; w?: number[] }> = ({ n, w = [100, 92, 96, 70] }) => (
  <>
    {Array.from({ length: n }).map((_, i) => (
      <div key={i} style={{ height: 14, width: `${w[i % w.length]}%`, background: "#E6DACA", borderRadius: 7, marginTop: 16 }} />
    ))}
  </>
);
const Strike: React.FC<{ p: number; color?: string }> = ({ p, color = RED }) => (
  <div style={{ position: "absolute", left: -6, top: "50%", height: 7, width: `calc(${p * 100}% + 12px)`, background: color, borderRadius: 4, rotate: "-4deg" }} />
);
const Ring: React.FC<{ p: number; w: number; h: number; style?: React.CSSProperties }> = ({ p, w, h, style }) => (
  <svg viewBox={`0 0 ${w} ${h}`} width={w} height={h} style={{ position: "absolute", overflow: "visible", ...style }}>
    <ellipse cx={w / 2} cy={h / 2} rx={w / 2} ry={h / 2} fill="none" stroke={RED} strokeWidth={7} strokeDasharray={1000} strokeDashoffset={1000 * (1 - p)} strokeLinecap="round" />
  </svg>
);
const Badge: React.FC<{ ok: boolean; at: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ ok, at, style, children }) => (
  <Pop at={at} style={{ position: "absolute", ...style }}>
    <div style={{ display: "inline-flex", alignItems: "center", gap: 14, background: ok ? GREEN : RED, color: "#fff", border: `5px solid ${INK}`, borderRadius: 999, padding: "10px 28px", fontSize: 40, fontWeight: 600, whiteSpace: "nowrap" }}>
      <span style={{ fontSize: 44 }}>{ok ? "✓" : "✗"}</span>
      {children}
    </div>
  </Pop>
);

// ---------- Szene 0: Hook ----------
export const SceneHook: React.FC<{ fehler: number; punkte: number }> = ({ fehler, punkte }) => {
  const { t, fps, frame } = useT();
  const cal = Math.max(0.9, sp(t, -0.2, fps));
  const shake = t > punkte ? Math.sin(frame * 1.6) * 4 : 0;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FDF1E6" }}>
      <div style={{ position: "absolute", left: 60, top: 70, width: 400, scale: String(cal), rotate: "-4deg" }}>
        <div style={{ background: RED, color: "#fff", border: `6px solid ${INK}`, borderBottom: "none", borderRadius: "28px 28px 0 0", textAlign: "center", fontSize: 50, fontWeight: 600, padding: "10px 0" }}>NOVEMBER</div>
        <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: "0 0 28px 28px", textAlign: "center", fontSize: 54, fontWeight: 700, padding: "30px 0 26px", lineHeight: 1.1 }}>
          Abgabe<br />
          <span style={{ fontSize: 40, color: MUTED, fontWeight: 600 }}>Seminararbeit</span>
        </div>
      </div>
      <Pop at={0.05} style={{ position: "absolute", right: 50, top: 110 }}>
        <div style={{ background: NAVY, color: "#fff", border: `6px solid ${INK}`, borderRadius: 26, padding: "16px 30px", fontSize: 50, fontWeight: 600, rotate: "3deg", textAlign: "center", lineHeight: 1.15 }}>
          Bayern<br />13. Klasse
        </div>
      </Pop>
      <Pop at={fehler} style={{ position: "absolute", left: 0, right: 0, top: 470, textAlign: "center" }}>
        <div style={{ fontSize: 190, fontWeight: 700, lineHeight: 1, color: RED, translate: `${shake}px 0px` }}>5 Fehler</div>
      </Pop>
      <Pop at={punkte} style={{ position: "absolute", left: 0, right: 0, top: 720, display: "flex", justifyContent: "center", gap: 26 }}>
        <div style={{ background: "#fff", border: `6px solid ${INK}`, borderRadius: 22, padding: "10px 34px", fontSize: 70, fontWeight: 700, color: RED, rotate: "-3deg", translate: `0px ${Math.sin(frame / 6) * 8}px` }}>
          kosten Punkte 📉
        </div>
      </Pop>
    </div>
  );
};

// ---------- Fehler 1: wörtliches Zitat mit „Vgl.“ ----------
export const SceneVgl: React.FC<{ vgl: number; fix: number }> = ({ vgl, fix }) => {
  const { t } = useT();
  const ring = fade(t, vgl, 0.5);
  const strike = fade(t, fix, 0.35);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={1} title="Wörtliches Zitat" />
      <Paper style={{ left: 50, right: 50, top: 190, height: 560 }}>
        <div style={{ fontSize: 38, lineHeight: 1.45 }}>
          Laut Müller ist der Tourismus <b style={{ background: "#FFF0B8" }}>„der wichtigste Arbeitgeber der Region“</b>
          <sup style={{ color: NAVY, fontWeight: 700 }}>12</sup>.
        </div>
        <Lines n={4} />
        <div style={{ position: "absolute", left: 36, right: 36, bottom: 34, borderTop: "3px solid #CFC2AE", paddingTop: 18, fontSize: 40, display: "flex", alignItems: "center", gap: 10 }}>
          <sup style={{ fontSize: 26 }}>12</sup>
          <span style={{ position: "relative", color: t >= vgl ? RED : INK, fontWeight: 700 }}>
            Vgl.
            <Ring p={ring} w={120} h={70} style={{ left: -22, top: -12 }} />
            <Strike p={strike} />
          </span>
          <span>Müller 2020, S. 12.</span>
        </div>
      </Paper>
      <Badge ok={false} at={fix + 0.2} style={{ left: 60, top: 790 }}>wörtlich → ohne „Vgl.“</Badge>
      <Badge ok at={fix + 1.0} style={{ left: 60, top: 880 }}>sinngemäß → mit „Vgl.“</Badge>
    </div>
  );
};

// ---------- Fehler 2: „ebd.“ nach Kapitelwechsel ----------
export const SceneEbd: React.FC<{ ebd: number; kapitel: number; fix: number }> = ({ ebd, kapitel, fix }) => {
  const { t } = useT();
  const ring = fade(t, ebd, 0.5);
  const strike = fade(t, fix, 0.35);
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={2} title="„ebd.“ nach neuem Kapitel" />
      <Paper style={{ left: 50, right: 50, top: 190, height: 250 }}>
        <div style={{ fontSize: 34, fontWeight: 700 }}>2.3 Ursachen</div>
        <Lines n={2} />
        <div style={{ position: "absolute", left: 36, right: 36, bottom: 24, borderTop: "3px solid #CFC2AE", paddingTop: 12, fontSize: 34 }}>
          <sup style={{ fontSize: 22 }}>18</sup> Vgl. Schmidt 2019, S. 4.
        </div>
      </Paper>
      <Pop at={kapitel} style={{ position: "absolute", left: 0, right: 0, top: 452, display: "flex", justifyContent: "center" }}>
        <div style={{ background: NAVY, color: "#fff", borderRadius: 999, padding: "6px 28px", fontSize: 32, fontWeight: 600, border: `4px solid ${INK}` }}>✂ neues Kapitel</div>
      </Pop>
      <Paper style={{ left: 50, right: 50, top: 530, height: 300 }}>
        <div style={{ fontSize: 34, fontWeight: 700 }}>3 Folgen</div>
        <Lines n={2} />
        <div style={{ position: "absolute", left: 36, right: 36, bottom: 26, borderTop: "3px solid #CFC2AE", paddingTop: 14, fontSize: 40, display: "flex", flexWrap: "wrap", gap: "10px 26px", alignItems: "center" }}>
          <sup style={{ fontSize: 24 }}>19</sup>
          <span style={{ position: "relative", color: RED, fontWeight: 700 }}>
            Vgl. ebd., S. 5.
            <Ring p={ring} w={300} h={76} style={{ left: -18, top: -14 }} />
            <Strike p={strike} />
          </span>
          {t >= fix + 0.3 && <span style={{ color: GREEN, fontWeight: 700, opacity: fade(t, fix + 0.3), marginLeft: 20 }}>→ Vgl. Schmidt 2019, S. 5.</span>}
        </div>
      </Paper>
      <Badge ok at={fix + 0.6} style={{ left: 60, top: 860 }}>Quelle wieder normal nennen</Badge>
    </div>
  );
};

// ---------- Fehler 3: Wertungen im Hauptteil ----------
export const SceneWertung: React.FC<{ dramatisch: number; ueber: number; fazit: number }> = ({ dramatisch, ueber, fazit }) => {
  const { t } = useT();
  const hl = (a: number) => ({ background: t >= a ? "#F8C9C2" : "transparent", color: t >= a ? RED : INK, fontWeight: t >= a ? 700 : 400, borderRadius: 8, padding: "0 6px" });
  const move = interpolate(t, [fazit + 0.1, fazit + 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={3} title="Wertung im Hauptteil" />
      <Paper style={{ left: 50, width: 520, top: 190, height: 520 }}>
        <div style={{ fontSize: 30, color: MUTED, fontWeight: 600 }}>HAUPTTEIL</div>
        <div style={{ fontSize: 38, lineHeight: 1.55, marginTop: 10 }}>
          Die Zahl der Gäste stieg <span style={hl(dramatisch)}>dramatisch</span> an. Das Ergebnis ist <span style={hl(ueber)}>überraschend</span>.
        </div>
        <Lines n={3} />
      </Paper>
      <Paper style={{ left: 600, right: 50, top: 300, height: 300, background: "#EEF7F1", borderColor: GREEN }}>
        <div style={{ fontSize: 30, color: GREEN, fontWeight: 700 }}>FAZIT</div>
        <div style={{ fontSize: 34, marginTop: 14, opacity: move, translate: `${(1 - move) * -200}px 0px`, fontWeight: 600 }}>Meine Bewertung …</div>
        <Lines n={2} w={[90, 70]} />
      </Paper>
      <Badge ok at={fazit + 0.4} style={{ left: 60, top: 780 }}>Wertungen gehören ins Fazit</Badge>
    </div>
  );
};

// ---------- Fehler 4: Internetquelle ohne Abrufdatum ----------
export const SceneAbruf: React.FC<{ abruf: number; ausdruck: number; screenshot: number }> = ({ abruf, ausdruck, screenshot }) => {
  const { t, frame } = useT();
  const filled = t >= abruf + 0.9;
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={4} title="Internetquelle" />
      <Paper style={{ left: 50, right: 50, top: 190, height: 300 }}>
        <div style={{ fontSize: 30, color: MUTED, fontWeight: 600 }}>LITERATURVERZEICHNIS</div>
        <div style={{ fontSize: 36, lineHeight: 1.5, marginTop: 14 }}>
          Landesamt für Statistik (2025): Tourismus in Bayern.{" "}
          <span style={{ color: "#1A56C4" }}>https://www.statistik…</span>{" "}
          {filled ? (
            <span style={{ color: GREEN, fontWeight: 700, opacity: fade(t, abruf + 0.9) }}>(abgerufen am 28.10.2026)</span>
          ) : (
            <span style={{ display: "inline-block", minWidth: 330, border: `4px dashed ${t >= abruf ? RED : "#CFC2AE"}`, borderRadius: 10, color: RED, fontWeight: 700, padding: "0 10px", opacity: t >= abruf ? 0.6 + 0.4 * Math.sin(frame / 3) : 1 }}>
              {t >= abruf ? "Abrufdatum?" : " "}
            </span>
          )}
        </div>
      </Paper>
      <Pop at={ausdruck} style={{ position: "absolute", left: 90, top: 560 }}>
        <div style={{ width: 330, height: 330, background: "#fff", border: `6px solid ${INK}`, borderRadius: 22, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 14, rotate: "-4deg" }}>
          <svg viewBox="0 0 64 64" width={130} height={130}>
            <rect x={14} y={6} width={36} height={18} rx={3} fill="#fff" stroke={INK} strokeWidth={4} />
            <rect x={4} y={22} width={56} height={26} rx={6} fill="#C9B79C" stroke={INK} strokeWidth={4} />
            <rect x={16} y={38} width={32} height={22} rx={2} fill="#fff" stroke={INK} strokeWidth={4} />
            <line x1={21} y1={46} x2={43} y2={46} stroke="#9DB8E0" strokeWidth={3} />
            <line x1={21} y1={53} x2={37} y2={53} stroke="#9DB8E0" strokeWidth={3} />
          </svg>
          <div style={{ fontSize: 44, fontWeight: 700 }}>Ausdruck</div>
        </div>
      </Pop>
      <Pop at={screenshot} style={{ position: "absolute", right: 90, top: 560 }}>
        <div style={{ width: 330, height: 330, background: "#fff", border: `6px solid ${INK}`, borderRadius: 22, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 14, rotate: "4deg" }}>
          <div style={{ width: 200, height: 130, border: `4px solid ${INK}`, borderRadius: 10, padding: 8, background: "#F7F3EC" }}>
            <div style={{ height: 14, width: "90%", background: "#9DB8E0", borderRadius: 4 }} />
            <div style={{ height: 10, width: "70%", background: "#E3D8C6", borderRadius: 4, marginTop: 10 }} />
            <div style={{ height: 10, width: "80%", background: "#FFE27A", borderRadius: 4, marginTop: 10 }} />
            <div style={{ height: 10, width: "60%", background: "#E3D8C6", borderRadius: 4, marginTop: 10 }} />
          </div>
          <div style={{ fontSize: 44, fontWeight: 700 }}>Screenshot</div>
        </div>
      </Pop>
    </div>
  );
};

// ---------- Fehler 5: Fußnoten ≠ Literaturverzeichnis ----------
export const SceneAbgleich: React.FC<{ fehlt: number; umgekehrt: number }> = ({ fehlt, umgekehrt }) => {
  const { t } = useT();
  const left = ["Müller 2020", "Schmidt 2019", "Huber 2021"];
  const right = ["Klein 2018", "Müller 2020", "Schmidt 2019"];
  const rowL = (s: string, i: number) => {
    const bad = s === "Huber 2021" && t >= fehlt;
    return (
      <div key={s} style={{ fontSize: 38, padding: "14px 18px", borderRadius: 12, marginTop: 12, background: bad ? "#F8C9C2" : "#F3EBDD", color: bad ? RED : INK, fontWeight: bad ? 700 : 500, opacity: fade(t, 0.15 * i), display: "flex", justifyContent: "space-between" }}>
        {s}
        <span>{bad ? "✗" : t >= fehlt - 0.6 ? "✓" : ""}</span>
      </div>
    );
  };
  const rowR = (s: string, i: number) => {
    const bad = s === "Klein 2018" && t >= umgekehrt;
    return (
      <div key={s} style={{ fontSize: 38, padding: "14px 18px", borderRadius: 12, marginTop: 12, background: bad ? "#F8C9C2" : "#F3EBDD", color: bad ? RED : INK, fontWeight: bad ? 700 : 500, opacity: fade(t, 0.3 + 0.15 * i), display: "flex", justifyContent: "space-between" }}>
        {s}
        <span>{bad ? "✗" : t >= fehlt - 0.6 && s !== "Klein 2018" ? "✓" : ""}</span>
      </div>
    );
  };
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Num n={5} title="Quelle fehlt" />
      <Paper style={{ left: 40, width: 420, top: 200, height: 520, padding: "24px 24px" }}>
        <div style={{ fontSize: 32, color: MUTED, fontWeight: 700 }}>FUSSNOTEN</div>
        {left.map(rowL)}
      </Paper>
      <Paper style={{ right: 40, width: 420, top: 200, height: 520, padding: "24px 24px" }}>
        <div style={{ fontSize: 32, color: MUTED, fontWeight: 700 }}>LITERATURVERZ.</div>
        {right.map(rowR)}
      </Paper>
      <Badge ok={false} at={fehlt + 0.3} style={{ left: 60, top: 770 }}>Huber 2021 fehlt hinten</Badge>
      <Badge ok={false} at={umgekehrt + 0.2} style={{ left: 60, top: 860 }}>Klein 2018 nie zitiert</Badge>
    </div>
  );
};

// ---------- Merkblatt geht vor ----------
export const SceneMerkblatt: React.FC<{ stamp: number }> = ({ stamp }) => {
  const { t, fps } = useT();
  const s = t < stamp ? 0 : spring({ frame: (t - stamp) * fps, fps, config: { damping: 9, stiffness: 200 } });
  return (
    <div style={{ position: "absolute", inset: 0, background: CREAM }}>
      <Pop at={0} style={{ position: "absolute", left: 214, top: 90 }}>
        <div style={{ width: 520, height: 680, background: PAPER, border: `6px solid ${INK}`, borderRadius: 22, padding: "40px 44px", boxShadow: "0 16px 0 rgba(58,38,24,.12)" }}>
          <div style={{ fontSize: 50, fontWeight: 700 }}>Merkblatt</div>
          <div style={{ fontSize: 34, color: MUTED, fontWeight: 600, marginTop: 4 }}>deiner Schule</div>
          <Lines n={9} w={[100, 85, 94, 60, 100, 78]} />
        </div>
      </Pop>
      <div style={{ position: "absolute", left: 470, top: 520, scale: String(s ? 2.2 - 1.2 * s : 0), rotate: "-12deg", opacity: s ? 1 : 0 }}>
        <div style={{ border: `9px solid ${GREEN}`, color: GREEN, borderRadius: 20, padding: "8px 26px", fontSize: 78, fontWeight: 700, background: "rgba(255,255,255,.85)" }}>GEHT VOR!</div>
      </div>
    </div>
  );
};

// ---------- Schluss: Skill + Link im Profil ----------
export const SceneSkill: React.FC<{ pruefung: number; link: number }> = ({ pruefung, link }) => {
  const { t, fps, frame } = useT();
  const items = ["„Vgl.“ bei Zitaten", "„ebd.“-Ketten", "Wertungen", "Abrufdaten", "Fußnoten ↔ Literatur"];
  if (t >= link) {
    const s = sp(t, link, fps);
    const glow = 0.5 + 0.5 * Math.sin(frame / 4);
    return (
      <div style={{ position: "absolute", inset: 0, background: CREAM }}>
        <div style={{ position: "absolute", left: 214, top: 50, width: 520, height: 880, background: "#fff", border: `10px solid ${INK}`, borderRadius: 56, scale: String(s), overflow: "hidden" }}>
          <div style={{ padding: "54px 36px", textAlign: "center" }}>
            <div style={{ width: 160, height: 160, borderRadius: 80, background: "#F5E7CF", margin: "0 auto", overflow: "hidden", border: `5px solid ${INK}` }}>
              <div style={{ marginTop: 36, marginLeft: -12 }}>
                <Hamster size={190} talking={false} blink={false} pointerAngle={0} />
              </div>
            </div>
            <div style={{ fontSize: 44, fontWeight: 700, marginTop: 18 }}>@hamsterfrei</div>
            <div style={{ fontSize: 28, color: MUTED, marginTop: 10, lineHeight: 1.3 }}>Seminararbeit bis 10.11.?<br />Keine Angst 🐹</div>
            <div style={{ marginTop: 34, fontSize: 32, fontWeight: 700, color: "#1A56C4", border: `5px solid rgba(35,136,90,${glow})`, borderRadius: 18, padding: "14px 8px", background: "#EEF7F1" }}>🔗 hamsterfrei.de/seminar</div>
            <div style={{ marginTop: 60, fontSize: 58, fontWeight: 700, color: GREEN, scale: String(sp(t, link + 0.3, fps)) }}>☝️ Link im Profil</div>
          </div>
        </div>
      </div>
    );
  }
  const exam = t >= pruefung;
  return (
    <div style={{ position: "absolute", inset: 0, background: "#FBF7F0" }}>
      <div style={{ height: 90, background: "#F3EBDD", display: "flex", alignItems: "center", gap: 16, padding: "0 34px", fontSize: 36, fontWeight: 600, borderBottom: "4px solid #E7D9C2" }}>
        <div style={{ width: 22, height: 22, borderRadius: 11, background: "#E5835E" }} />
        Claude
        <span style={{ marginLeft: "auto", background: GREEN, color: "#fff", borderRadius: 999, padding: "6px 20px", fontSize: 28 }}>Skill: Seminararbeit-Profi</span>
      </div>
      {!exam ? (
        <div style={{ padding: "34px 50px" }}>
          <div style={{ fontSize: 48, fontWeight: 700, marginBottom: 14 }}>Check · Seminararbeit.docx</div>
          {items.map((x, i) => {
            const a = 0.3 + i * 0.32;
            return (
              <div key={x} style={{ display: "flex", alignItems: "center", gap: 22, fontSize: 44, padding: "18px 0", borderBottom: "3px solid #EFE4D2", opacity: fade(t, a, 0.2), translate: `${(1 - fade(t, a, 0.2)) * -40}px 0px` }}>
                <div style={{ width: 58, height: 58, borderRadius: 29, background: GREEN, color: "#fff", display: "grid", placeItems: "center", fontWeight: 700, fontSize: 36, flex: "none" }}>✓</div>
                <div style={{ fontWeight: 600 }}>{x}</div>
              </div>
            );
          })}
        </div>
      ) : (
        <div style={{ padding: "34px 50px", display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ fontSize: 52, fontWeight: 700, opacity: fade(t, pruefung) }}>🎓 Probe-Prüfung</div>
          <div style={{ alignSelf: "flex-start", maxWidth: "88%", background: "#fff", border: "4px solid #E7D9C2", borderRadius: 24, padding: "18px 26px", fontSize: 42, lineHeight: 1.3, opacity: fade(t, pruefung + 0.2) }}>
            <span style={{ fontSize: 28, color: MUTED, fontWeight: 700 }}>LEHRKRAFT</span>
            <br />Woher stammt die Zahl auf Seite 7?
          </div>
          <div style={{ alignSelf: "flex-end", maxWidth: "80%", background: "#F1E6D3", borderRadius: 24, padding: "18px 26px", fontSize: 42, lineHeight: 1.3, opacity: fade(t, pruefung + 0.9) }}>
            Aus der amtlichen Statistik …
          </div>
        </div>
      )}
    </div>
  );
};
