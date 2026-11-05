import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneChat, SceneMerkblatt, SceneEintrag, SceneListe, SceneAber, ScenePointe, SceneEnde } from "../scenes/seminar06";
import wordsData from "./seminar06.words.json";

// Seminar06 · S5-Countdown Teil 2 „Noch fünf Tage: Literaturverzeichnis“ · KEINE Werbung (Produkt nicht genannt/verlinkt)
export const SEMINAR06_SECONDS = 35.4;

const words = (wordsData as { words: Word[] }).words;

const MAP: Record<string, string> = { fünf: "5", "Fünf": "5", "Kanzler,": "Canzler," };

export const Seminar06: React.FC = () => (
  <Episode
    audio="folgen/seminar06.mp3"
    words={words}
    totalSeconds={SEMINAR06_SECONDS}
    dingAt={30.96}
    werbung={false}
    startle
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 4.35, el: <SceneHook haufen={3.31} /> },
      { from: 4.35, to: 9.56, el: <SceneChat canzler={3.03} /> },
      { from: 9.56, to: 11.5, el: <SceneMerkblatt /> },
      { from: 11.5, to: 16.1, el: <SceneEintrag marks={[0.73, 1.2, 1.58, 2.15]} format={3.36} /> },
      { from: 16.1, to: 19.78, el: <SceneListe az={2.14} /> },
      { from: 19.78, to: 26.8, el: <SceneAber findet={3.54} gelb={4.92} /> },
      { from: 26.8, to: 30.3, el: <ScenePointe fertig={1.0} /> },
      { from: 30.3, to: SEMINAR06_SECONDS, el: <SceneEnde commentAt={0.66} /> },
    ]}
  />
);
