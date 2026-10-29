import React from "react";
import { Composition } from "remotion";
import { Avatar } from "./Avatar";
import { Banner } from "./Banner";
import { HamsterCut } from "./HamsterCut";
import { Folge01, FOLGE01_SECONDS } from "./folgen/folge01";

// Jede neue Folge: src/folgen/folgeNN.tsx anlegen und hier eine Composition "FolgeNN" ergänzen.
const FOLGEN: { id: string; component: React.FC; seconds: number }[] = [
  { id: "Folge01", component: Folge01, seconds: FOLGE01_SECONDS },
];

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="HamsterCut" component={HamsterCut} durationInFrames={1} fps={30} width={640} height={640} />
    <Composition id="Banner" component={Banner} durationInFrames={1} fps={30} width={2560} height={1440} />
    <Composition id="Avatar" component={Avatar} durationInFrames={1} fps={30} width={1080} height={1080} />
    {FOLGEN.map((f) => (
      <Composition key={f.id} id={f.id} component={f.component} durationInFrames={Math.round(f.seconds * 30)} fps={30} width={1080} height={1920} />
    ))}
  </>
);
