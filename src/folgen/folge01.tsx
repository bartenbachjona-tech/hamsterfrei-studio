import React from "react";
import { Episode, Word } from "../Episode";
import { SceneFlow, SceneVideos } from "../Scenes";
import { SceneLamp, ScenePricesV2, SceneShopify, SceneProblemV2 } from "../ScenesV2";
import wordsData from "./folge01.words.json";

// Folge 1 · Ein Produkt, ein Shop · Wort: SHOP (veröffentlicht 29.10.2026)
export const FOLGE01_SECONDS = 46;

const words = (wordsData as { words: Word[] }).words;

export const Folge01: React.FC = () => (
  <Episode
    audio="folgen/folge01.mp3"
    words={words}
    totalSeconds={FOLGE01_SECONDS}
    dingAt={43.6}
    werbung
    captionMap={(t) => t.replace("neunundzwanzig", "29,90 €").replace(/^neunzig\.$/, "").replace("zweiunddreißig", "32")}
    scenes={[
      { from: 0, to: 5.25, el: <SceneLamp example={2.9} /> },
      { from: 5.25, to: 12.1, el: <ScenePricesV2 shopAt={5.45} /> },
      { from: 12.1, to: 27.05, el: <SceneShopify m={{ account: 3.24, name: 5.7, design: 7.26, product: 9.1, images: 11.1, title: 12.06, price: 12.78, live: 14.4 }} /> },
      { from: 27.05, to: 32.0, el: <SceneProblemV2 led={0.75} strike={1.95} better={2.5} /> },
      { from: 32.0, to: 37.1, el: <SceneFlow du={1.1} lief={2.2} send={3.5} note={false} /> },
      { from: 37.1, to: FOLGE01_SECONDS, el: <SceneVideos commentAt={6.5} lamp /> },
    ]}
  />
);
