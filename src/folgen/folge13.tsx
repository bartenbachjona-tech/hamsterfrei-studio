import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneSatz, SceneMathe, SceneNachrechnen, SceneBio, SceneGesamt, SceneWaage, SceneUrteil, SceneEnde } from "../scenes/folge13";
import wordsData from "./folge13.words.json";

// Folge13 · Hamster-Test „Notenrechner aus einem Satz“ · Serie (a) · Einstiegs-Test E1 (Paar 1) · OHNE Werbung
// 1 Take eleven_v3 (Flow idZ0QGkgpeqyoM79NSdg, Generation jaN5xvMgdMBVNi6N9FiG, 33,0 s), unbearbeitet.
// words.json: „drei Komma zwei“ / „zwei Komma fünf drei“ zu einem Untertitel-Wort zusammengezogen, Audio-Tags entfernt.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE13_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "Zwölf": "12",
  "vier": "4",
  "drei,": "3,",
  "Zwei.": "2.",
  "zwei": "2",
  "Schnitt,": "SCHNITT,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge13: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge13.mp3"
      words={words}
      totalSeconds={FOLGE13_SECONDS}
      werbung={false}
      startle
      dingAt={30.95}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 6.02, el: <SceneHook bio={4.2} /> },
        { from: 6.02, to: 9.6, el: <SceneSatz doppelt={0.84} einfach={2.1} /> },
        { from: 9.6, to: 13.7, el: <SceneMathe vier={1.9} drei={2.4} zwei={3.33} /> },
        { from: 13.7, to: 17.7, el: <SceneNachrechnen hand={2.0} /> },
        { from: 17.7, to: 19.94, el: <SceneBio ok={0.6} /> },
        { from: 19.94, to: 22.46, el: <SceneGesamt stimmt={1.85} /> },
        { from: 22.46, to: 26.85, el: <SceneWaage bio={1.58} zitat={2.6} /> },
        { from: 26.85, to: 30.38, el: <SceneUrteil stempel={0.79} zeilen={1.3} /> },
        { from: 30.38, to: FOLGE13_SECONDS, el: <SceneEnde commentAt={0.53} /> },
      ]}
    />
  </AbsoluteFill>
);
