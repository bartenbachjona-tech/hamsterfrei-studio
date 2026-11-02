import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneKMS, SceneDauer, SceneVier, SceneF1, SceneF2, SceneF3, SceneF4, SceneSkill } from "../scenes/seminar03";
import wordsData from "./seminar03.words.json";

// Seminar-Offensive S2 · „Prüfungsgespräch: Wofür hast du KI benutzt?“ · Werbung (eigenes Produkt Seminararbeit-Profi)
export const SEMINAR03_SECONDS = 39;

const words = (wordsData as { words: Word[] }).words;

const MAP: Record<string, string> = {
  "fünfundzwanzig": "25",
  "vier": "4",
  "zwölf": "12",
  "Eins:": "1.",
  "Zwei:": "2.",
  "Drei:": "3.",
  "Vier:": "4.",
};

export const Seminar03: React.FC = () => (
  <Episode
    audio="folgen/seminar03.mp3"
    words={words}
    totalSeconds={SEMINAR03_SECONDS}
    dingAt={36.4}
    werbung
    startle
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 4.68, el: <SceneHook frage={2.04} pg={3.24} /> },
      { from: 4.68, to: 8.93, el: <SceneKMS km={0.2} ki={1.52} thema={3.08} /> },
      { from: 8.93, to: 12.9, el: <SceneDauer min={0.51} vortrag={2.47} /> },
      { from: 12.9, to: 15.46, el: <SceneVier vier={1.5} /> },
      { from: 15.46, to: 18.66, el: <SceneF1 bubble={0.15} idee={1.62} /> },
      { from: 18.66, to: 24.86, el: <SceneF2 seite={1.78} worte={2.62} wer={4.26} /> },
      { from: 24.86, to: 29.24, el: <SceneF3 ki={0.15} geprueft={2.5} /> },
      { from: 29.24, to: 31.9, el: <SceneF4 bubble={0.15} /> },
      { from: 31.9, to: SEMINAR03_SECONDS, el: <SceneSkill katalog={2.14} probe={3.46} link={4.5} /> },
    ]}
  />
);
