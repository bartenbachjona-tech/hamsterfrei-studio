import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneZettel, SceneTrick, ScenePruefen, SceneElf, SceneEier, SceneGemuese, SceneUrteil, SceneEnde } from "../scenes/folge06";
import wordsData from "./folge06.words.json";

// Folge06 · Hamster-Test „5 Mittagessen für 20 €“ · Serie (a) · Hook-Test Variante A (Paar 3) · OHNE Werbung
// 1 Take eleven_v3 (Generation UKSSN2ogjHfpknAihxvu, 32,3 s, 16.11.2026), keine Nachbearbeitung.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE06_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "fünf": "5",
  "zwanzig": "20 €",
  "Sechzehn": "16",
  "sechzehn": "16",
  "achtzehn": "18,36 €",
  "Euro": "",
  "sechsunddreißig.": "",
  "Elf": "11",
  "fünfzig": "50",
  "Zwei": "2,29 €",
  "neunundzwanzig": "",
  "eins": "1,69 €",
  "neunundsechzig.": "",
  "neunzehn": "19",
  "Zettel,": "ZETTEL,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge06: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge06.mp3"
      words={words}
      totalSeconds={FOLGE06_SECONDS}
      werbung={false}
      startle
      dingAt={29.88}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 5.1, el: <SceneHook /> },
        { from: 5.1, to: 8.7, el: <SceneZettel summe={1.86} /> },
        { from: 8.7, to: 12.55, el: <SceneTrick reste={0.66} chili={1.42} nudeln={2.46} /> },
        { from: 12.55, to: 15.78, el: <ScenePruefen aldi={1.65} /> },
        { from: 15.78, to: 19.35, el: <SceneElf summe={2.42} /> },
        { from: 19.35, to: 23.03, el: <SceneEier echt={1.37} claude={2.6} /> },
        { from: 23.03, to: 25.62, el: <SceneGemuese geschaetzt={1.96} /> },
        { from: 25.62, to: 29.49, el: <SceneUrteil stempel={0.58} summe={1.55} reis={2.62} /> },
        { from: 29.49, to: FOLGE06_SECONDS, el: <SceneEnde commentAt={0.39} /> },
      ]}
    />
  </AbsoluteFill>
);
