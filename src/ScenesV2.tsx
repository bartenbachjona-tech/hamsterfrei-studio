import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { Pop, INK, GREEN, NAVY } from "./Scenes";

const center: React.CSSProperties = {
  position: "absolute",
  inset: 0,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
};

const at = (frame: number, fps: number, s: number) => frame >= s * fps;

// Sonnenuntergangs-Lampe als Zeichnung
export const Lamp: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 200 200">
    <rect x={88} y={120} width={24} height={52} rx={6} fill="#3B3B46" stroke={INK} strokeWidth={5} />
    <rect x={62} y={168} width={76} height={18} rx={9} fill="#3B3B46" stroke={INK} strokeWidth={5} />
    <circle cx={100} cy={82} r={50} fill="#4A4A57" stroke={INK} strokeWidth={6} />
    <circle cx={100} cy={82} r={34} fill="#FF8A3D" stroke={INK} strokeWidth={4} />
    <circle cx={100} cy={82} r={18} fill="#FFD166" />
  </svg>
);

const Tag: React.FC<{ text: string; color: string; size?: number }> = ({ text, color, size = 110 }) => (
  <div style={{ background: color, color: "#fff", fontSize: size, fontWeight: 600, padding: "16px 44px", borderRadius: 28, border: `6px solid ${INK}` }}>{text}</div>
);

// A: Produkt, das viral geht -> Lampe mit Sonnenuntergang an der Wand
export const SceneLamp: React.FC<{ example: number }> = ({ example }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const glow = interpolate(frame, [example * fps, (example + 0.8) * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const hearts = [0, 1, 2];
  return (
    <div style={{ ...center, background: interpolate(glow, [0, 1], [0, 1]) > 0 ? `rgba(40,30,60,${0.85 * glow})` : "transparent" }}>
      <div
        style={{
          position: "absolute",
          top: 90,
          width: 520,
          height: 520,
          borderRadius: "50%",
          background: "radial-gradient(circle, #FFD166 0%, #FF8A3D 45%, #E0475A 70%, rgba(224,71,90,0) 72%)",
          opacity: glow,
          scale: String(0.6 + 0.4 * glow),
        }}
      />
      <div style={{ position: "absolute", bottom: 90 }}>
        <Lamp size={360} />
      </div>
      {!at(frame, fps, example) &&
        hearts.map((i) => {
          const t = (frame - i * 10) / fps;
          const y = interpolate(t % 1.5, [0, 1.5], [0, -300]);
          const o = interpolate(t % 1.5, [0, 0.2, 1.2, 1.5], [0, 1, 1, 0]);
          return (
            <svg key={i} width={70} height={70} viewBox="0 0 24 24" style={{ position: "absolute", right: 170 + i * 40, bottom: 260, translate: `0px ${y}px`, opacity: t < 0 ? 0 : o }}>
              <path d="M12 21s-7-4.5-9.5-9C.7 8.6 2.6 4 6.6 4c2.1 0 3.6 1.2 4.4 2.5C11.8 5.2 13.3 4 15.4 4c4 0 5.9 4.6 4.1 8-2.5 4.5-9.5 9-9.5 9z" fill="#E05A47" />
            </svg>
          );
        })}
    </div>
  );
};

// B: ein paar Euro gegen 32 Euro
export const ScenePricesV2: React.FC<{ shopAt: number }> = ({ shopAt }) => (
  <div style={{ ...center, gap: 34 }}>
    <Pop at={0.1}>
      <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
        <Lamp size={170} />
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ fontSize: 48, fontWeight: 600 }}>AliExpress</div>
          <Tag text="ein paar €" color={GREEN} size={78} />
        </div>
      </div>
    </Pop>
    <Pop at={shopAt - 0.4}>
      <svg width={110} height={100} viewBox="0 0 60 55">
        <path d="M30 4 L30 40 M14 26 L30 44 L46 26" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </Pop>
    <Pop at={shopAt}>
      <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
        <Lamp size={170} />
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ fontSize: 48, fontWeight: 600 }}>Onlineshop in Deutschland</div>
          <Tag text="32 €" color={NAVY} size={120} />
        </div>
      </div>
    </Pop>
  </div>
);

const Field: React.FC<{ label: string; value: string; typedFrom?: number; typedTo?: number }> = ({ label, value, typedFrom, typedTo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = typedFrom === undefined ? value.length : Math.round(interpolate(frame, [typedFrom * fps, (typedTo ?? typedFrom + 0.8) * fps], [0, value.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <div style={{ width: "100%" }}>
      <div style={{ fontSize: 34, fontWeight: 500, color: "#6B5444", marginBottom: 8 }}>{label}</div>
      <div style={{ border: `4px solid ${INK}`, borderRadius: 16, padding: "14px 22px", fontSize: 46, fontWeight: 600, minHeight: 58, background: "#FFFFFF" }}>{value.slice(0, n)}</div>
    </div>
  );
};

// C: Shopify Schritt für Schritt. Marken (Sekunden relativ zur Szene)
export type ShopMarks = { account: number; name: number; design: number; product: number; images: number; title: number; price: number; live: number };

export const SceneShopify: React.FC<{ m: ShopMarks }> = ({ m }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const step = at(frame, fps, m.live) ? 4 : at(frame, fps, m.product) ? 3 : at(frame, fps, m.design) ? 2 : 1;
  const stepLabel = ["", "1 · Konto anlegen", "2 · Design wählen", "3 · Produkt hinzufügen", "4 · Fertig"][step];
  return (
    <div style={{ ...center, justifyContent: "flex-start", paddingTop: 50 }}>
      <div style={{ fontSize: 60, fontWeight: 600, marginBottom: 26 }}>Shopify</div>
      <div style={{ width: 820, height: 760, border: `8px solid ${INK}`, borderRadius: 30, background: "#FBF7F0", overflow: "hidden", display: "flex", flexDirection: "column" }}>
        <div style={{ height: 70, background: INK, display: "flex", alignItems: "center", gap: 14, padding: "0 26px" }}>
          {["#E05A47", "#FFD166", "#34B27B"].map((c) => (
            <div key={c} style={{ width: 22, height: 22, borderRadius: 11, background: c }} />
          ))}
          <div style={{ marginLeft: 20, color: "#FFF8EC", fontSize: 36, fontWeight: 600 }}>{stepLabel}</div>
        </div>
        <div style={{ flex: 1, padding: 40, display: "flex", flexDirection: "column", gap: 28, alignItems: "center", justifyContent: "center" }}>
          {step === 1 && (
            <>
              <Field label="E-Mail" value="du@beispiel.de" typedFrom={m.account} typedTo={m.account + 0.7} />
              <Field label="Shopname" value="Abendlicht" typedFrom={m.name + 0.6} typedTo={m.name + 1.6} />
            </>
          )}
          {step === 2 && (
            <div style={{ display: "flex", gap: 24 }}>
              {[0, 1, 2].map((i) => {
                const picked = i === 1 && at(frame, fps, m.design + 0.8);
                return (
                  <div key={i} style={{ width: 210, height: 380, borderRadius: 20, border: `${picked ? 10 : 5}px solid ${picked ? GREEN : INK}`, background: "#FFFFFF", display: "flex", flexDirection: "column", gap: 12, padding: 16, boxSizing: "border-box" }}>
                    <div style={{ height: 30, borderRadius: 8, background: ["#E9A24E", "#24426B", "#8C5A2B"][i] }} />
                    <div style={{ height: 150, borderRadius: 12, background: "#F1E6D3" }} />
                    <div style={{ height: 18, borderRadius: 9, background: "#D8CBB8", width: "80%" }} />
                    <div style={{ height: 18, borderRadius: 9, background: "#D8CBB8", width: "60%" }} />
                    <div style={{ marginTop: "auto", height: 40, borderRadius: 10, background: ["#E9A24E", "#24426B", "#8C5A2B"][i] }} />
                  </div>
                );
              })}
            </div>
          )}
          {step === 3 && (
            <>
              <div style={{ width: "100%", height: 230, borderRadius: 18, border: `4px dashed ${INK}`, background: "#FFFFFF", display: "flex", alignItems: "center", justifyContent: "center", gap: 20 }}>
                {at(frame, fps, m.images) ? [0, 1, 2].map((i) => <Lamp key={i} size={170} />) : <div style={{ fontSize: 40, color: "#6B5444" }}>+ Bilder hinzufügen</div>}
              </div>
              <Field label="Titel" value="Sonnenuntergangs-Lampe" typedFrom={m.title} typedTo={m.title + 0.6} />
              <Field label="Preis" value="29,90 €" typedFrom={m.price} typedTo={m.price + 0.6} />
            </>
          )}
          {step === 4 && (
            <Pop at={m.live}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
                <svg width={200} height={200} viewBox="0 0 24 24">
                  <circle cx={12} cy={12} r={10} fill={GREEN} stroke={INK} strokeWidth={1.2} />
                  <path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" strokeWidth={2.4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div style={{ fontSize: 64, fontWeight: 600 }}>Shop ist live</div>
              </div>
            </Pop>
          )}
        </div>
      </div>
    </div>
  );
};

// D: Problem statt Produkt
export const SceneProblemV2: React.FC<{ led: number; strike: number; better: number }> = ({ led, strike, better }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const w = interpolate(frame, [strike * fps, (strike + 0.4) * fps], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1) });
  return (
    <div style={{ ...center, gap: 60, padding: "0 60px" }}>
      <Pop at={0.1}>
        <div style={{ display: "flex", alignItems: "center", gap: 24, fontSize: 64, fontWeight: 600 }}>
          <svg width={90} height={90} viewBox="0 0 24 24">
            <path d="M4 20l1-5L16 4l4 4L9 19z" fill="#FFE27A" stroke={INK} strokeWidth={1.6} strokeLinejoin="round" />
            <path d="M14 6l4 4" stroke={INK} strokeWidth={1.6} />
          </svg>
          Dein Produkttitel
        </div>
      </Pop>
      <Pop at={led}>
        <div style={{ position: "relative", fontSize: 96, fontWeight: 600, color: "#8C7B6B" }}>
          LED-Lampe
          <div style={{ position: "absolute", left: -10, top: "52%", height: 12, width: `calc(${w}% + 20px)`, background: "#E05A47", borderRadius: 6 }} />
        </div>
      </Pop>
      <Pop at={better}>
        <div style={{ fontSize: 80, fontWeight: 600, textAlign: "center", lineHeight: 1.15, background: "linear-gradient(180deg, #FFE1B3, #FFC9A3)", border: `6px solid ${INK}`, borderRadius: 30, padding: "34px 40px" }}>
          Dein Zimmer jeden Abend im Sonnenuntergang
        </div>
      </Pop>
    </div>
  );
};
