import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneVertrag, SceneClaude, SceneGesetz, SceneBrief, SceneButton, SceneUrteil, SceneEnde } from "../scenes/folge04";
import wordsData from "./folge04.words.json";

// Folge04 · Hamster-Test „Fitnessstudio kündigen“ · Serie (a) · Hook-Test Variante A (Paar 2) · OHNE Werbung
// 1 Take eleven_v3 (Generation MDvmi2Fe8NBhXLMlFd64, 32,0 s), keine Nachbearbeitung.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE04_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "Zwölf": "12",
  "zweitausendzweiundzwanzig.": "2022.",
  "Raus,": "RAUS,",
  "Ein": "1",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge04: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge04.mp3"
      words={words}
      totalSeconds={FOLGE04_SECONDS}
      werbung={false}
      startle
      dingAt={30.28}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 5.7, el: <SceneHook jahr={4.76} /> },
        { from: 5.7, to: 8.5, el: <SceneVertrag vorbei={1.7} /> },
        { from: 8.5, to: 11.58, el: <SceneClaude hoechstens={1.47} /> },
        { from: 11.58, to: 15.76, el: <SceneGesetz stimmt={0.9} /> },
        { from: 15.76, to: 21.42, el: <SceneBrief tipp={1.36} gebuehren={4.92} /> },
        { from: 21.42, to: 26.55, el: <SceneButton eng={1.84} online={3.53} /> },
        { from: 26.55, to: 29.47, el: <SceneUrteil stempel={0.2} monat={1.4} /> },
        { from: 29.47, to: FOLGE04_SECONDS, el: <SceneEnde commentAt={0.81} /> },
      ]}
    />
  </AbsoluteFill>
);
