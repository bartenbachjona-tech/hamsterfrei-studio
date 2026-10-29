import React from "react";
import { AbsoluteFill } from "remotion";
import { Hamster } from "./Hamster";
export const Avatar: React.FC = () => (
  <AbsoluteFill style={{ background: "#DDF1E4", alignItems: "center", justifyContent: "center" }}>
    <div style={{ position: "relative", marginTop: 20, marginLeft: -40 }}><Hamster size={1060} talking={false} blink={false} pointerAngle={0} /></div>
  </AbsoluteFill>
);
