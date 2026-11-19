import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneFragen, SceneZettel, SceneStreicht, SceneRegel, SceneHaken, SceneUrteil, SceneEnde } from "../scenes/folge09";
import wordsData from "./folge09.words.json";

// Folge09 · Hamster-Test „Aushang fürs Schneeschippen“ · Serie (a) · Hook-Test Variante A (Paar 4) · OHNE Werbung
// 1 Take eleven_v3 (Generation U7xe6zyv64VMJLyERzKG, 30,6 s), unbearbeitet.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE09_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "fünfzehn.": "15.",
  "acht": "8",
  "zehn": "10",
  "Zehn": "10",
  "Aushang,": "AUSHANG,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge09: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge09.mp3"
      words={words}
      totalSeconds={FOLGE09_SECONDS}
      werbung={false}
      startle
      dingAt={28.8}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 5.5, el: <SceneHook ringAt={4.5} /> },
        { from: 5.5, to: 8.5, el: <SceneFragen claudeAt={1.4} /> },
        { from: 8.5, to: 12.75, el: <SceneZettel a={0.6} b={2.2} c={3.35} /> },
        { from: 12.75, to: 15.7, el: <SceneStreicht strikeAt={1.65} /> },
        { from: 15.7, to: 20.75, el: <SceneRegel voll={1.2} unterricht={2.0} /> },
        { from: 20.75, to: 25.1, el: <SceneHaken mark={1.9} beleg={3.0} /> },
        { from: 25.1, to: 28.35, el: <SceneUrteil stempel={0.75} zeilen={1.3} /> },
        { from: 28.35, to: FOLGE09_SECONDS, el: <SceneEnde commentAt={0.4} /> },
      ]}
    />
  </AbsoluteFill>
);
