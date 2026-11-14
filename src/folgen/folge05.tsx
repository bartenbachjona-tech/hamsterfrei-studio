import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneNotizen, SceneZelle, SceneChat, SceneTabelle, SceneSeiten, SceneUrteil, SceneEnde } from "../scenes/folge05";
import wordsData from "./folge05.words.json";

// Folge05 · „Wie wird aus deinem Heft-Chaos ein Lernzettel?“ · Serie (a)-nah · Hook-Test Variante B (Paar 2) · OHNE Werbung
// 1 Take eleven_v3 (Generation 0FG8FDZbKtAxHCrYtRQm, 32,1 s), keine Nachbearbeitung.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE05_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "Zytoplasma.": "Cytoplasma.",
  "fünf": "5",
  "zwei.": "2.",
  "Lernen,": "LERNEN,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge05: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge05.mp3"
      words={words}
      totalSeconds={FOLGE05_SECONDS}
      werbung={false}
      startle
      dingAt={29.56}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 4.7, el: <SceneHook /> },
        { from: 4.7, to: 9.2, el: <SceneNotizen fehler={2.78} /> },
        { from: 9.2, to: 13.65, el: <SceneZelle falsch={2.32} /> },
        { from: 13.65, to: 17.25, el: <SceneChat oben={1.9} /> },
        { from: 17.25, to: 20.4, el: <SceneTabelle fragen={1.4} /> },
        { from: 20.4, to: 24.4, el: <SceneSeiten eine={1.09} zwei={3.3} /> },
        { from: 24.4, to: 28.95, el: <SceneUrteil stempel={1.04} fehler={2.26} lang={3.3} /> },
        { from: 28.95, to: FOLGE05_SECONDS, el: <SceneEnde commentAt={0.61} /> },
      ]}
    />
  </AbsoluteFill>
);
