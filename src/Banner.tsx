import React from "react";
import { AbsoluteFill, staticFile } from "remotion";
import { loadFont } from "@remotion/fonts";
import { Hamster } from "./Hamster";
import { INK, GREEN, CREAM } from "./Scenes";

loadFont({ family: "Fredoka", url: staticFile("fonts/fredoka-latin.woff2"), weight: "300 700" });
loadFont({ family: "Fredoka", url: staticFile("fonts/fredoka-latin-ext.woff2"), weight: "300 700", unicodeRange: "U+0100-024F, U+1E00-1EFF, U+20A0-20AB, U+20AD-20CF" });

// YouTube-Banner 2560x1440, sicherer Bereich 1546x423 in der Mitte
export const Banner: React.FC = () => (
  <AbsoluteFill style={{ background: CREAM, fontFamily: "Fredoka", color: INK }}>
    <div style={{ position: "absolute", left: 0, right: 0, top: 940, bottom: 0, background: "#F5E7CF", borderTop: "8px solid #EAD6B4" }} />
    <div style={{ position: "absolute", left: 507, top: 509, width: 1546, height: 423, display: "flex", alignItems: "center", justifyContent: "center", gap: 40 }}>
      <div style={{ position: "relative", width: 420, height: 420, flexShrink: 0 }}>
        <Hamster size={420} talking={false} blink={false} pointerAngle={-6} />
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <div style={{ fontSize: 150, fontWeight: 700, lineHeight: 1 }}>Hamster<span style={{ color: GREEN }}>frei</span></div>
        <div style={{ fontSize: 56, fontWeight: 500, color: "#6B5444", whiteSpace: "nowrap" }}>Kleine Nebenjobs, Schritt für Schritt erklärt</div>
      </div>
    </div>
  </AbsoluteFill>
);
