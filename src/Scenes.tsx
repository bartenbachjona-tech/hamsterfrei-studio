import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const INK = "#3A2618";
export const GREEN = "#23885A";
export const NAVY = "#24426B";
export const CREAM = "#FFF8EC";

// Erscheint mit federndem Pop ab Sekunde `at` (relativ zur Szene)
export const Pop: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - at * fps, fps, config: { damping: 12, stiffness: 160 } });
  return (
    <div style={{ ...style, scale: String(frame < at * fps ? 0 : s), opacity: frame < at * fps ? 0 : 1 }}>{children}</div>
  );
};

const center: React.CSSProperties = {
  position: "absolute",
  inset: 0,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
};

const Tag: React.FC<{ text: string; color: string; size?: number }> = ({ text, color, size = 120 }) => (
  <div
    style={{
      background: color,
      color: "#fff",
      fontSize: size,
      fontWeight: 600,
      padding: "18px 44px 18px 64px",
      borderRadius: 28,
      position: "relative",
      border: `6px solid ${INK}`,
    }}
  >
    <div style={{ position: "absolute", left: 22, top: "50%", width: 22, height: 22, marginTop: -11, borderRadius: 11, background: CREAM, border: `5px solid ${INK}` }} />
    {text}
  </div>
);

// Szene 1: ein Gadget für 4 Euro
export const SceneProduct: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = interpolate(Math.sin(frame / 6), [-1, 1], [0.35, 0.8]);
  return (
    <div style={center}>
      <svg width={420} height={420} viewBox="0 0 200 200">
        <circle cx={100} cy={80} r={70} fill="#FFE27A" opacity={glow} />
        <rect x={62} y={40} width={76} height={110} rx={22} fill="#FFFFFF" stroke={INK} strokeWidth={6} />
        <rect x={74} y={56} width={52} height={40} rx={10} fill="#FFE27A" stroke={INK} strokeWidth={4} />
        <circle cx={100} cy={124} r={9} fill={INK} />
        <rect x={84} y={150} width={32} height={22} rx={6} fill="#D8CBB8" stroke={INK} strokeWidth={4} />
      </svg>
      <Pop at={1.9} style={{ marginTop: 10 }}>
        <Tag text="4 €" color={GREEN} />
      </Pop>
    </div>
  );
};

// Szene 2: 4 Euro gegen 20 Euro
export const ScenePrices: React.FC = () => (
  <div style={{ ...center, gap: 40 }}>
    <Pop at={0.15}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
        <div style={{ fontSize: 46, fontWeight: 600, color: INK }}>Einkauf</div>
        <Tag text="4 €" color={GREEN} />
      </div>
    </Pop>
    <Pop at={2.5}>
      <svg width={120} height={110} viewBox="0 0 60 55">
        <path d="M30 4 L30 40 M14 26 L30 44 L46 26" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </Pop>
    <Pop at={4.4}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
        <div style={{ fontSize: 46, fontWeight: 600, color: INK }}>Preis in Deutschland</div>
        <Tag text="20 €" color={NAVY} size={150} />
      </div>
    </Pop>
  </div>
);

const Phone: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      width: 430,
      height: 800,
      borderRadius: 60,
      border: `10px solid ${INK}`,
      background: "#FFFFFF",
      position: "relative",
      overflow: "hidden",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "70px 34px 34px",
      boxSizing: "border-box",
      gap: 26,
    }}
  >
    <div style={{ position: "absolute", top: 22, width: 120, height: 22, borderRadius: 11, background: INK }} />
    {children}
  </div>
);

// Szene 3: Shop mit genau einem Produkt
export const SceneShop: React.FC = () => (
  <div style={center}>
    <Phone>
      <Pop at={0.3}>
        <div style={{ fontSize: 44, fontWeight: 600, color: INK }}>Dein Shop</div>
      </Pop>
      <Pop at={1.0} style={{ width: "100%" }}>
        <div style={{ width: "100%", height: 300, borderRadius: 26, background: "#FFF1D0", border: `5px solid ${INK}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <svg width={170} height={170} viewBox="0 0 200 200">
            <rect x={62} y={40} width={76} height={110} rx={22} fill="#FFFFFF" stroke={INK} strokeWidth={7} />
            <rect x={74} y={56} width={52} height={40} rx={10} fill="#FFE27A" stroke={INK} strokeWidth={5} />
            <rect x={84} y={150} width={32} height={22} rx={6} fill="#D8CBB8" stroke={INK} strokeWidth={5} />
          </svg>
        </div>
      </Pop>
      <Pop at={5.2} style={{ width: "100%" }}>
        <div style={{ display: "flex", gap: 14, width: "100%" }}>
          {[0, 1, 2].map((i) => (
            <div key={i} style={{ flex: 1, height: 90, borderRadius: 16, background: "#FFF1D0", border: `4px solid ${INK}` }} />
          ))}
        </div>
      </Pop>
      <Pop at={6.0} style={{ width: "100%" }}>
        <div style={{ width: "100%", textAlign: "center", background: GREEN, color: "#fff", fontSize: 46, fontWeight: 600, borderRadius: 22, padding: "18px 0", border: `5px solid ${INK}` }}>
          Kaufen · 20 €
        </div>
      </Pop>
    </Phone>
  </div>
);

// Szene 4: Problem statt Produkt
export const SceneProblem: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const strike = interpolate(frame, [4.9 * fps, 5.3 * fps], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  return (
    <div style={{ ...center, gap: 70, padding: "0 60px" }}>
      <Pop at={0.2}>
        <div style={{ display: "flex", alignItems: "center", gap: 24, fontSize: 64, fontWeight: 600, color: INK }}>
          <svg width={90} height={90} viewBox="0 0 24 24">
            <path d="M4 20l1-5L16 4l4 4L9 19z" fill="#FFE27A" stroke={INK} strokeWidth={1.6} strokeLinejoin="round" />
            <path d="M14 6l4 4" stroke={INK} strokeWidth={1.6} />
          </svg>
          Deine Produktseite
        </div>
      </Pop>
      <Pop at={3.5}>
        <div style={{ position: "relative", fontSize: 96, fontWeight: 600, color: "#8C7B6B" }}>
          „LED-Lampe“
          <div style={{ position: "absolute", left: -10, top: "52%", height: 12, width: `calc(${strike}% + 20px)`, background: "#E05A47", borderRadius: 6 }} />
        </div>
      </Pop>
      <Pop at={5.5}>
        <div style={{ fontSize: 82, fontWeight: 600, color: INK, textAlign: "center", lineHeight: 1.15, background: "#FFF1D0", border: `6px solid ${INK}`, borderRadius: 30, padding: "34px 40px" }}>
          „Nie wieder im Dunkeln den Schlüssel suchen“
        </div>
      </Pop>
    </div>
  );
};

const Node: React.FC<{ label: string; color: string }> = ({ label, color }) => (
  <div style={{ background: color, color: "#fff", fontSize: 58, fontWeight: 600, padding: "22px 40px", borderRadius: 26, border: `6px solid ${INK}`, minWidth: 260, textAlign: "center" }}>
    {label}
  </div>
);

// Szene 5: Lieferant schickt direkt
export const SceneFlow: React.FC<{ du?: number; lief?: number; send?: number; note?: boolean }> = ({ du = 1.2, lief = 1.6, send = 2.7, note = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const parcel = interpolate(frame, [send * fps, (send + 1.6) * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.55, 1),
  });
  return (
    <div style={center}>
      <div style={{ position: "relative", width: 820, height: 860 }}>
        <Pop at={0.1} style={{ position: "absolute", left: 0, top: 40 }}>
          <Node label="Kunde" color={NAVY} />
        </Pop>
        <Pop at={du} style={{ position: "absolute", right: 0, top: 40 }}>
          <Node label="Du" color={GREEN} />
        </Pop>
        <Pop at={lief} style={{ position: "absolute", right: 0, top: 600 }}>
          <Node label="Lieferant" color="#8C5A2B" />
        </Pop>
        <svg width={820} height={860} style={{ position: "absolute", inset: 0 }}>
          <defs>
            <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M0 0L10 5L0 10z" fill={INK} />
            </marker>
          </defs>
          <path d="M290 100 H540" stroke={INK} strokeWidth={8} fill="none" markerEnd="url(#ah)" opacity={frame > (du - 0.3) * fps ? 1 : 0} />
          <path d="M690 180 V580" stroke={INK} strokeWidth={8} fill="none" markerEnd="url(#ah)" opacity={frame > (lief - 0.1) * fps ? 1 : 0} />
          <path d="M470 690 Q150 690 130 200" stroke={GREEN} strokeWidth={8} fill="none" strokeDasharray="22 16" markerEnd="url(#ah)" opacity={frame > (send - 0.1) * fps ? 1 : 0} />
        </svg>
        <div
          style={{
            position: "absolute",
            left: interpolate(parcel, [0, 1], [400, 90]),
            top: interpolate(parcel, [0, 0.6, 1], [650, 600, 260]),
            opacity: frame > (send - 0.1) * fps && parcel < 1 ? 1 : 0,
            width: 110,
            height: 90,
            background: "#D9A066",
            border: `6px solid ${INK}`,
            borderRadius: 12,
          }}
        />
        <Pop at={note ? 4.9 : 999} style={{ position: "absolute", left: 230, top: 330 }}>
          <div style={{ fontSize: 54, fontWeight: 600, color: INK, background: "#FFF1D0", border: `5px solid ${INK}`, borderRadius: 24, padding: "18px 28px", textAlign: "center", lineHeight: 1.2 }}>
            Kein Paket
            <br />
            in deiner Hand
          </div>
        </Pop>
      </div>
    </div>
  );
};

// Szene 6: Kunden über Videos, am Ende Kommentar SHOP
export const SceneVideos: React.FC<{ commentAt: number; lamp?: boolean }> = ({ commentAt, lamp = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hearts = [0, 1, 2, 3, 4];
  return (
    <div style={center}>
      <Phone>
        <div style={{ width: "100%", flex: 1, borderRadius: 26, background: "#2E2A3A", position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
          {lamp ? (
            <>
              <div style={{ position: "absolute", top: 70, width: 240, height: 240, borderRadius: "50%", background: "radial-gradient(circle, #FFD166 0%, #FF8A3D 45%, #E0475A 70%, rgba(224,71,90,0) 72%)" }} />
              <svg width={200} height={200} viewBox="0 0 200 200" style={{ position: "absolute", bottom: 120 }}>
                <rect x={88} y={120} width={24} height={52} rx={6} fill="#3B3B46" stroke={INK} strokeWidth={5} />
                <rect x={62} y={168} width={76} height={18} rx={9} fill="#3B3B46" stroke={INK} strokeWidth={5} />
                <circle cx={100} cy={82} r={50} fill="#4A4A57" stroke={INK} strokeWidth={6} />
                <circle cx={100} cy={82} r={34} fill="#FF8A3D" stroke={INK} strokeWidth={4} />
              </svg>
            </>
          ) : (
            <svg width={200} height={200} viewBox="0 0 200 200">
              <rect x={62} y={40} width={76} height={110} rx={22} fill="#FFFFFF" stroke={INK} strokeWidth={6} />
              <rect x={74} y={56} width={52} height={40} rx={10} fill="#FFE27A" stroke={INK} strokeWidth={4} />
            </svg>
          )}
          <svg width={90} height={90} viewBox="0 0 40 40" style={{ position: "absolute", bottom: 30, left: 30 }}>
            <path d="M12 8 L32 20 L12 32 Z" fill="#FFFFFF" />
          </svg>
          {hearts.map((i) => {
            const t = (frame - i * 9) / fps;
            const y = interpolate(t % 1.6, [0, 1.6], [0, -360]);
            const o = interpolate(t % 1.6, [0, 0.2, 1.3, 1.6], [0, 1, 1, 0]);
            return (
              <svg key={i} width={56} height={56} viewBox="0 0 24 24" style={{ position: "absolute", right: 24 + (i % 2) * 30, bottom: 60, translate: `0px ${y}px`, opacity: t < 0 ? 0 : o }}>
                <path d="M12 21s-7-4.5-9.5-9C.7 8.6 2.6 4 6.6 4c2.1 0 3.6 1.2 4.4 2.5C11.8 5.2 13.3 4 15.4 4c4 0 5.9 4.6 4.1 8-2.5 4.5-9.5 9-9.5 9z" fill="#E05A47" />
              </svg>
            );
          })}
        </div>
      </Phone>
      <Pop at={commentAt} style={{ position: "absolute", right: 50, bottom: 60 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20, background: "#FFFFFF", border: `6px solid ${INK}`, borderRadius: 40, padding: "20px 40px" }}>
          <svg width={70} height={70} viewBox="0 0 24 24">
            <path d="M4 5h16v11H9l-5 4z" fill={GREEN} stroke={INK} strokeWidth={1.5} strokeLinejoin="round" />
          </svg>
          <div style={{ fontSize: 110, fontWeight: 600, color: INK, letterSpacing: 4 }}>SHOP</div>
        </div>
      </Pop>
    </div>
  );
};
