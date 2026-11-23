import React from "react";
import { AbsoluteFill } from "remotion";
import { Word } from "../Episode";
import { EpisodeE2 } from "../EpisodeE2";
import { E2Hook, SceneHook, SceneEingabe, SceneMathe, SceneFrei, SceneBio, SceneEnglisch, SceneUrteil, SceneEnde } from "../scenes/folge12";
import wordsData from "./folge12.words.json";

// Folge12 · Hamster-Test „Klausurwoche: drei Klausuren + Minijob“ · Serie (a) · Einstiegs-Test E2 (Paar 1) · OHNE Werbung
// 1 Take eleven_v3 (Flow 0ENzRFzKNL7noDE2vEGt, Generation PzH2L3Wh2RByicCto8jQ, 28,9 s), unbearbeitet.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE12_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "Drei": "3",
  "Achtzigster.": "80.",
  "siebzehn.": "17.",
  "acht": "8",
  "Klausur,": "KLAUSUR,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge12: React.FC = () => (
  <AbsoluteFill>
    <EpisodeE2
      audio="folgen/folge12.mp3"
      words={words}
      totalSeconds={FOLGE12_SECONDS}
      werbung={false}
      dingAt={26.76}
      captionMap={captionMap}
      e2={{ until: 1.0, el: <E2Hook /> }}
      scenes={[
        { from: 0, to: 6.05, el: <SceneHook kurz={4.4} /> },
        { from: 6.05, to: 10.25, el: <SceneEingabe di={1.58} mi={2.38} doo={3.19} /> },
        { from: 10.25, to: 13.86, el: <SceneMathe fast={1.27} zitat={2.35} /> },
        { from: 13.86, to: 16.8, el: <SceneFrei frei={1.26} oma={1.82} /> },
        { from: 16.8, to: 19.34, el: <SceneBio sa={0.1} /> },
        { from: 19.34, to: 23.5, el: <SceneEnglisch nur={1.5} nach={2.26} /> },
        { from: 23.5, to: 26.4, el: <SceneUrteil stempel={0.78} zeilen={1.1} /> },
        { from: 26.4, to: FOLGE12_SECONDS, el: <SceneEnde commentAt={0.36} /> },
      ]}
    />
  </AbsoluteFill>
);
