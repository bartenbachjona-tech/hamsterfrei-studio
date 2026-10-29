import React from "react";
import { AbsoluteFill } from "remotion";
import { Hamster } from "./Hamster";
// Freigestellter Hamster (transparent), zeigt mit dem Stab nach rechts oben – für die Website
export const HamsterCut: React.FC = () => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
    <Hamster size={560} talking={false} blink={false} pointerAngle={8} />
  </AbsoluteFill>
);
