import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneTitel, SceneFleck, ScenePreis, SceneErfunden, SceneUrteil, SceneEnde } from "../scenes/folge14";
import wordsData from "./folge14.words.json";

// Folge14 · Vorher/Nachher „Winterjacken-Anzeige“ · Serie (b) · Einstiegs-Test E1 (Paar 2) · OHNE Werbung
// 1 Take eleven_v3 (Flow HbQnnOgWny8oIVM3b0y9, Generation NOAHV5qpEPtOJtKZe37f, 31,3 s), unbearbeitet. Audio-Tags entfernt.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE14_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "zwei": "2",
  "Jacke,": "JACKE,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge14: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge14.mp3"
      words={words}
      totalSeconds={FOLGE14_SECONDS}
      werbung={false}
      startle
      dingAt={29.0}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 6.15, el: <SceneHook fast={5.57} links={1.4} rechts={2.96} /> },
        { from: 6.15, to: 11.05, el: <SceneTitel a={[1.05, 1.74, 2.12, 2.77]} /> },
        { from: 11.05, to: 14.4, el: <SceneFleck mangel={2.67} /> },
        { from: 14.4, to: 18.6, el: <ScenePreis frage={3.3} /> },
        { from: 18.6, to: 23.8, el: <SceneErfunden waschen={1.9} notiz={3.1} /> },
        { from: 23.8, to: 28.35, el: <SceneUrteil stempel={0.3} zeilen={0.8} /> },
        { from: 28.35, to: FOLGE14_SECONDS, el: <SceneEnde commentAt={0.63} /> },
      ]}
    />
  </AbsoluteFill>
);
