import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneDatei, SceneCheck, SceneFund1, SceneFund2, SceneQuellen, SceneBeleg, ScenePruefung, SceneSchritte, SceneEnde } from "../scenes/seminar07";
import wordsData from "./seminar07.words.json";

// Seminar07 · S7 Suchbegriff-Video „Seminararbeit mit KI? So geht's.“ · Werbung (eigenes Produkt Seminararbeit-Profi), ohne Preis
export const SEMINAR07_SECONDS = 31.2;

// „zwanzig einundzwanzig“ im Untertitel zu „2021“ zusammenfassen
const words: Word[] = (() => {
  const src = (wordsData as { words: Word[] }).words;
  const out: Word[] = [];
  for (let i = 0; i < src.length; i++) {
    const w = src[i];
    if (w.text === "zwanzig" && src[i + 1]?.text === "einundzwanzig") {
      out.push({ ...w, text: "2021", end: src[i + 1].end });
      i++;
    } else out.push(w);
  }
  return out;
})();

const MAP: Record<string, string> = {
  "zwölf:": "12:",
  "Vergleiche.": "„Vgl.“",
  "Drei": "3",
  "zehnten?": "10.11.?",
};

export const Seminar07: React.FC = () => (
  <Episode
    audio="folgen/seminar07.mp3"
    words={words}
    totalSeconds={SEMINAR07_SECONDS}
    werbung
    startle
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 3.5, el: <SceneHook weg={2.5} /> },
      { from: 3.5, to: 5.35, el: <SceneDatei /> },
      { from: 5.35, to: 6.95, el: <SceneCheck /> },
      { from: 6.95, to: 10.2, el: <SceneFund1 vgl={2.4} /> },
      { from: 10.2, to: 13.2, el: <SceneFund2 fehlt={1.36} /> },
      { from: 13.2, to: 15.4, el: <SceneQuellen shots={0.55} /> },
      { from: 15.4, to: 17.4, el: <SceneBeleg link={0.96} datum={1.33} /> },
      { from: 17.4, to: 20.25, el: <ScenePruefung frage={1.29} /> },
      { from: 20.25, to: 25.55, el: <SceneSchritte s1={0.99} s2={1.79} s3={2.77} frei={4.11} /> },
      { from: 25.55, to: SEMINAR07_SECONDS, el: <SceneEnde link={2.52} /> },
    ]}
  />
);
