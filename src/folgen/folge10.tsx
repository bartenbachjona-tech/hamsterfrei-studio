import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneBeispiel, SceneDrei, SceneKarte, SceneZitat, SceneKreis, SceneUrteil, SceneEnde } from "../scenes/folge10";
import wordsData from "./folge10.words.json";

// Folge10 · „Steht auf deiner Referat-Folie zu viel?“ · Serie (a)-nah · Hook-Test Variante B (Paar 5) · OHNE Werbung
// 1 Take eleven_v3 (Generation fCxA5usobwRE7QSlQazs, 32,7 s), unbearbeitet.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE10_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "drei": "3",
  "sieben": "7",
  "vierte": "4.",
  "Referat,": "REFERAT,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge10: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge10.mp3"
      words={words}
      totalSeconds={FOLGE10_SECONDS}
      werbung={false}
      startle
      dingAt={30.2}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 6.0, el: <SceneHook /> },
        { from: 6.0, to: 8.75, el: <SceneBeispiel zaehl={1.8} /> },
        { from: 8.75, to: 13.08, el: <SceneDrei w1={1.99} w2={2.81} w3={3.65} /> },
        { from: 13.08, to: 16.3, el: <SceneKarte ok={2.1} /> },
        { from: 16.3, to: 21.1, el: <SceneZitat mark={0.5} /> },
        { from: 21.1, to: 24.5, el: <SceneKreis luecke={2.37} /> },
        { from: 24.5, to: 29.77, el: <SceneUrteil stempel={0.75} plus={2.1} zeilen={0.9} /> },
        { from: 29.77, to: FOLGE10_SECONDS, el: <SceneEnde commentAt={0.4} /> },
      ]}
    />
  </AbsoluteFill>
);
