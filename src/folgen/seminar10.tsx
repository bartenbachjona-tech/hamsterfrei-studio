import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneFelder, SceneRolle, SceneChat, SceneThemen, SceneFrage, SceneAntwort, SceneFeedback, SceneEhrlich, SceneEnde } from "../scenes/seminar10";
import wordsData from "./seminar10.words.json";

// Seminar10 · S2-F „Abgegeben? Jetzt kommt das Prüfungsgespräch“ · Follow-up S2 · OHNE Werbung
// 1 Take eleven_v3 (Generation X4XqA0aL4UuzfgNt0LCz), Szenenwechsel auf Scribe-Wortzeiten.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const SEMINAR10_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const captionMap = (t: string) =>
  t.replace(/^zehn$/, "10").replace(/^Prüfung,$/, "PRÜFUNG,");

export const Seminar10: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/seminar10.mp3"
      words={words}
      totalSeconds={SEMINAR10_SECONDS}
      werbung={false}
      startle
      dingAt={36.35}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 4.17, el: <SceneHook durch={1.4} pg={3.07} /> },
        { from: 4.17, to: 7.33, el: <SceneFelder eigene={1.88} /> },
        { from: 7.33, to: 9.39, el: <SceneRolle /> },
        { from: 9.39, to: 15.03, el: <SceneChat datei={0.05} text={2.16} /> },
        { from: 15.03, to: 20.39, el: <SceneThemen at={[1.04, 1.82, 2.63, 4.13]} /> },
        { from: 20.39, to: 23.71, el: <SceneFrage /> },
        { from: 23.71, to: 26.95, el: <SceneAntwort wackelt={2.33} /> },
        { from: 26.95, to: 31.58, el: <SceneFeedback wie={1.23} ergebnis={3.09} /> },
        { from: 31.58, to: 35.95, el: <SceneEhrlich aber={1.2} /> },
        { from: 35.95, to: SEMINAR10_SECONDS, el: <SceneEnde commentAt={0.4} /> },
      ]}
    />
  </AbsoluteFill>
);
