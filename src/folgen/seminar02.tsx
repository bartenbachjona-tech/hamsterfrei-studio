import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneVgl, SceneEbd, SceneWertung, SceneAbruf, SceneAbgleich, SceneMerkblatt, SceneSkill } from "../scenes/seminar02";
import wordsData from "./seminar02.words.json";

// Seminar-Offensive S1 · „5 Fehler in deiner Seminararbeit“ · Wort: SEMINAR · Werbung (eigenes Produkt Seminararbeit-Profi)
export const SEMINAR02_SECONDS = 47;

const words = (wordsData as { words: Word[] }).words;

const MAP: Record<string, string> = {
  "dreizehnte": "13.",
  "fünf": "5",
  "Eins:": "1.",
  "Zwei:": "2.",
  "Drei:": "3.",
  "Vier:": "4.",
  "Fünf:": "5.",
  "vergleiche.": "„Vgl.“",
  "ebenda,": "„ebd.“",
  "Seminararbeit-Abgabe": "Abgabe",
};

export const Seminar02: React.FC = () => (
  <Episode
    audio="folgen/seminar02.mp3"
    words={words}
    totalSeconds={SEMINAR02_SECONDS}
    dingAt={44.06}
    werbung
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 5.34, el: <SceneHook fehler={3.58} punkte={4.14} /> },
      { from: 5.34, to: 12.04, el: <SceneVgl vgl={3.23} fix={4.22} /> },
      { from: 12.04, to: 17.44, el: <SceneEbd ebd={0.84} kapitel={2.16} fix={3.24} /> },
      { from: 17.44, to: 23.28, el: <SceneWertung dramatisch={1.34} ueber={2.32} fazit={3.78} /> },
      { from: 23.28, to: 29.6, el: <SceneAbruf abruf={1.82} ausdruck={4.4} screenshot={5.04} /> },
      { from: 29.6, to: 35.44, el: <SceneAbgleich fehlt={2.77} umgekehrt={4.7} /> },
      { from: 35.44, to: 38.83, el: <SceneMerkblatt stamp={2.05} /> },
      { from: 38.83, to: SEMINAR02_SECONDS, el: <SceneSkill pruefung={3.13} link={5.23} /> },
    ]}
  />
);
