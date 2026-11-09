import React from "react";
import { Composition } from "remotion";
import { Avatar } from "./Avatar";
import { Banner } from "./Banner";
import { HamsterCut } from "./HamsterCut";
import { Folge01, FOLGE01_SECONDS } from "./folgen/folge01";
import { Seminar01, SEMINAR01_SECONDS } from "./folgen/seminar01";
import { Seminar02, SEMINAR02_SECONDS } from "./folgen/seminar02";
import { Seminar03, SEMINAR03_SECONDS } from "./folgen/seminar03";
import { Seminar04, SEMINAR04_SECONDS } from "./folgen/seminar04";
import { Seminar05, SEMINAR05_SECONDS } from "./folgen/seminar05";
import { Seminar06, SEMINAR06_SECONDS } from "./folgen/seminar06";
import { Seminar07, SEMINAR07_SECONDS } from "./folgen/seminar07";
import { Seminar09, SEMINAR09_SECONDS } from "./folgen/seminar09";

// Jede neue Folge: src/folgen/folgeNN.tsx anlegen und hier eine Composition "FolgeNN" ergänzen.
const FOLGEN: { id: string; component: React.FC; seconds: number }[] = [
  { id: "Folge01", component: Folge01, seconds: FOLGE01_SECONDS },
  { id: "Seminar01", component: Seminar01, seconds: SEMINAR01_SECONDS },
  { id: "Seminar02", component: Seminar02, seconds: SEMINAR02_SECONDS },
  { id: "Seminar03", component: Seminar03, seconds: SEMINAR03_SECONDS },
  { id: "Seminar04", component: Seminar04, seconds: SEMINAR04_SECONDS },
  { id: "Seminar05", component: Seminar05, seconds: SEMINAR05_SECONDS },
  { id: "Seminar06", component: Seminar06, seconds: SEMINAR06_SECONDS },
  { id: "Seminar07", component: Seminar07, seconds: SEMINAR07_SECONDS },
  { id: "Seminar09", component: Seminar09, seconds: SEMINAR09_SECONDS },
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
