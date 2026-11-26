import React from "react";
import { AbsoluteFill } from "remotion";
import { Word } from "../Episode";
import { EpisodeE2 } from "../EpisodeE2";
import { E2Hook, SceneHook, SceneLinks, SceneSatz, SceneFragen, SceneBrief, SceneErfunden, SceneUrteil, SceneEnde } from "../scenes/folge15";
import wordsData from "./folge15.words.json";

// Folge15 · Vorher/Nachher „Gleicher Job, zwei Bewerbungen – ein Satz Unterschied“ · Serie (b) · Einstiegs-Test E2 (Paar 2) · OHNE Werbung
// 1 Take eleven_v3 (Flow 2domS0YdxCxu3f6qhete, Generation g0OngPSeLJFCH08j836V, 35,6 s), per atempo 1,07 auf 33,3 s gestrafft (Länge 30–35 s laut Testdesign). Audio-Tags entfernt, Scribe-Zeiten ÷ 1,07.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE15_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "zwei": "2",
  "fünf": "5",
  "sechs": "6",
  "drei": "3",
  "Fragen,": "FRAGEN,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge15: React.FC = () => (
  <AbsoluteFill>
    <EpisodeE2
      audio="folgen/folge15.mp3"
      words={words}
      totalSeconds={FOLGE15_SECONDS}
      werbung={false}
      dingAt={30.7}
      captionMap={captionMap}
      e2={{ until: 1.0, el: <E2Hook /> }}
      scenes={[
        { from: 0, to: 5.67, el: <SceneHook satz={5.0} /> },
        { from: 5.67, to: 10.92, el: <SceneLinks floskel={3.58} klammer={4.46} /> },
        { from: 10.92, to: 13.6, el: <SceneSatz tipp={1.19} /> },
        { from: 13.6, to: 16.99, el: <SceneFragen hl={[0.81, 1.43, 2.14]} /> },
        { from: 16.99, to: 22.2, el: <SceneBrief m={[1.38, 2.49, 3.7]} /> },
        { from: 22.2, to: 27.4, el: <SceneErfunden drei={0.36} schlange={2.89} /> },
        { from: 27.4, to: 30.34, el: <SceneUrteil stempel={0.1} zeilen={0.4} /> },
        { from: 30.34, to: FOLGE15_SECONDS, el: <SceneEnde commentAt={0.36} /> },
      ]}
    />
  </AbsoluteFill>
);

// Cover (Hook-Paket, LOOK.md): E2-Schlüsselbild ohne Untertitel, Standbild bei 0,5 s
export const Folge15Cover: React.FC = () => (
  <AbsoluteFill style={{ fontFamily: "Fredoka", color: "#3A2618" }}>
    <E2Hook />
  </AbsoluteFill>
);
