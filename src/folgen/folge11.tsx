import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneEingabe, SceneKarte, SceneAbend, SceneKonflikt, SceneGeschenk, SceneHaken, SceneUrteil, SceneEnde } from "../scenes/folge11";
import wordsData from "./folge11.words.json";

// Folge11 · Hamster-Test „Morgen-Briefing aus Notiz-Chaos“ · Serie (a) · Hook-Test Variante A (Paar 5) · OHNE Werbung
// 1 Take eleven_v3 (Flow U5NqH0mlA1NXtAfj8YYR, Generation M6CYKN9xdfKUKyUXqw0T, 34,6 s), unbearbeitet.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE11_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "neun": "9",
  "siebzehn,": "17,",
  "neunzehn": "19",
  "Morgen,": "MORGEN,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge11: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge11.mp3"
      words={words}
      totalSeconds={FOLGE11_SECONDS}
      werbung={false}
      startle
      dingAt={32.3}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 4.75, el: <SceneHook /> },
        { from: 4.75, to: 6.98, el: <SceneEingabe /> },
        { from: 6.98, to: 10.7, el: <SceneKarte bus={0.82} mathe={2.62} /> },
        { from: 10.7, to: 12.95, el: <SceneAbend /> },
        { from: 12.95, to: 19.3, el: <SceneKonflikt warn={0.6} training={2.85} zitat={4.3} /> },
        { from: 19.3, to: 21.75, el: <SceneGeschenk vor={1.44} /> },
        { from: 21.75, to: 27.05, el: <SceneHaken buch={1.4} geb={4.3} /> },
        { from: 27.05, to: 31.55, el: <SceneUrteil stempel={0.89} zeilen={1.6} /> },
        { from: 31.55, to: FOLGE11_SECONDS, el: <SceneEnde commentAt={0.73} /> },
      ]}
    />
  </AbsoluteFill>
);
