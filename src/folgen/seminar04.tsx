import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneBeispiel, SceneProjekt, SceneDrei, SceneF1, SceneF2, SceneF3, SceneRegel, ScenePointe, SceneEnde } from "../scenes/seminar04";
import wordsData from "./seminar04.words.json";

// T4 · „Lass Claude deine Seminararbeit prüfen. Nicht schreiben.“ · KEINE Werbung (Produkt nicht genannt/verlinkt, Marke v2)
export const SEMINAR04_SECONDS = 38.7;

const words = (wordsData as { words: Word[] }).words;

const MAP: Record<string, string> = { zehnten: "10.", zwei: "2", drei: "3", "Eins:": "1.", "Zwei:": "2.", "Drei:": "3." };

export const Seminar04: React.FC = () => (
  <Episode
    audio="folgen/seminar04.mp3"
    words={words}
    totalSeconds={SEMINAR04_SECONDS}
    dingAt={34.12}
    werbung={false}
    startle
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 4.09, el: <SceneHook pruefen={2.67} schreiben={3.24} /> },
      { from: 4.09, to: 8.69, el: <SceneBeispiel kap={1.67} frage={3.16} /> },
      { from: 8.69, to: 14.32, el: <SceneProjekt projekt={0.3} files={[2.8, 3.44, 4.8]} /> },
      { from: 14.32, to: 15.86, el: <SceneDrei /> },
      { from: 15.86, to: 18.36, el: <SceneF1 ok={1.47} /> },
      { from: 18.36, to: 21.44, el: <SceneF2 quelle={2.07} /> },
      { from: 21.44, to: 24.24, el: <SceneF3 frage={0.86} /> },
      { from: 24.24, to: 30.31, el: <SceneRegel lehrkraft={1.31} angeben={3.45} /> },
      { from: 30.31, to: 33.67, el: <ScenePointe reparieren={1.64} /> },
      { from: 33.67, to: SEMINAR04_SECONDS, el: <SceneEnde commentAt={0.45} /> },
    ]}
  />
);
