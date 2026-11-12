import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneKopier, SceneAuszug, SceneSieben, SceneKauf, SceneApple, SceneMiete, SceneUrteil, SceneEnde } from "../scenes/folge03";
import wordsData from "./folge03.words.json";

// Folge03 · „Wie viel zahlst du für Abos?“ · Serie (a)-nah · Hook-Test Variante B (Paar 1) · OHNE Werbung
// 1 Take eleven_v3 (Generation m2oQJ8MYpr3iyJXQTkpZ, 30,5 s), keine Nachbearbeitung.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE03_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "sieben": "7",
  "hundertsiebzehn": "117,94 €.",
  "Euro": "",
  "vierundneunzig.": "",
  "neunzig": "90 €.",
  "Euro.": "",
  "Abo,": "ABO,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge03: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge03.mp3"
      words={words}
      totalSeconds={FOLGE03_SECONDS}
      werbung={false}
      startle
      dingAt={28.08}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 1.84, el: <SceneHook /> },
        { from: 1.84, to: 5.54, el: <SceneKopier schwarz={1.97} /> },
        { from: 5.54, to: 8.08, el: <SceneAuszug /> },
        { from: 8.08, to: 12.05, el: <SceneSieben summe={1.8} /> },
        { from: 12.05, to: 15.25, el: <SceneKauf einkauf={2.27} /> },
        { from: 15.25, to: 19.76, el: <SceneApple wofuer={1.35} handy={3.27} /> },
        { from: 19.76, to: 24.2, el: <SceneMiete neunzig={1.57} abos={2.88} /> },
        { from: 24.2, to: 27.35, el: <SceneUrteil stempel={0.6} summe={2.4} /> },
        { from: 27.35, to: FOLGE03_SECONDS, el: <SceneEnde commentAt={0.73} /> },
      ]}
    />
  </AbsoluteFill>
);
