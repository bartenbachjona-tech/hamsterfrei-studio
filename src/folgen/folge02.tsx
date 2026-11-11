import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneFrage, ScenePreis, SceneMarkt, SceneAber, SceneQuelle, SceneUrteil, SceneEnde } from "../scenes/folge02";
import wordsData from "./folge02.words.json";

// Folge02 · Hamster-Test „Was ist meine alte Switch noch wert?“ · Serie (a) · Hook-Test Variante A · OHNE Werbung
// 1 Take eleven_v3 (Generation FrBPyLVxdVFTPwliRYVu), Pausen auf 0,18 s gekürzt + atempo 1,03 (Zeiten umgerechnet).
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE02_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "hundertfünfzig": "150 €",
  "Euro": "",
  "Vau": "VB.",
  "Beh.": "",
  "hundertzwanzig.": "120 €.",
  "hundert": "100",
  "zweihundert.": "200 €.",
  "hundertfünfzehn": "115 €.",
  "Euro.": "",
  "hundertsiebenundvierzig.": "147 €.",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge02: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge02.mp3"
      words={words}
      totalSeconds={FOLGE02_SECONDS}
      werbung={false}
      startle
      dingAt={30.42}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 4.7, el: <SceneHook passt={3.21} nicht={3.91} /> },
        { from: 4.7, to: 7.36, el: <SceneFrage /> },
        { from: 7.36, to: 11.62, el: <ScenePreis unter={2.84} /> },
        { from: 11.62, to: 15.55, el: <SceneMarkt passt={3.35} /> },
        { from: 15.55, to: 19.35, el: <SceneAber mark={2.5} /> },
        { from: 19.35, to: 25.6, el: <SceneQuelle lite={2.51} normal={3.52} /> },
        { from: 25.6, to: 30.0, el: <SceneUrteil stempel={0.59} klick={2.94} /> },
        { from: 30.0, to: FOLGE02_SECONDS, el: <SceneEnde commentAt={0.42} /> },
      ]}
    />
  </AbsoluteFill>
);
