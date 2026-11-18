import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneBeispiel, SceneMail, SceneKiosk, SceneHobbys, SceneNeu, SceneDazu, SceneUrteil, SceneEnde } from "../scenes/folge08";
import wordsData from "./folge08.words.json";

// Folge08 · „Wie wird dein Minijob-Lebenslauf besser?“ · Serie (a)-nah · Hook-Test Variante B (Paar 4) · OHNE Werbung
// 1 Take eleven_v3 (Generation 9cERdiBISaF2wKV2RXnH, 34,3 s), Pausen > 0,3 s per ffmpeg auf 0,22 s gekürzt → 32,1 s (Wortzeiten umgerechnet).
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE08_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "elfte": "11.",
  "Fünf": "5",
  "fünf": "5",
  "Zockerkönig": "zockerkoenig",
  "Lebenslauf,": "LEBENSLAUF,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge08: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge08.mp3"
      words={words}
      totalSeconds={FOLGE08_SECONDS}
      werbung={false}
      startle
      dingAt={29.6}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 3.3, el: <SceneHook /> },
        { from: 3.3, to: 6.3, el: <SceneBeispiel frage={1.0} /> },
        { from: 6.3, to: 8.45, el: <SceneMail neu={0.9} /> },
        { from: 8.45, to: 14.1, el: <SceneKiosk cafe={3.9} vorn={4.85} /> },
        { from: 14.1, to: 16.55, el: <SceneHobbys raus={0.6} bleibt={1.2} /> },
        { from: 16.55, to: 18.95, el: <SceneNeu verf={1.45} /> },
        { from: 18.95, to: 24.9, el: <SceneDazu mark={2.1} nirgends={4.95} /> },
        { from: 24.9, to: 29.0, el: <SceneUrteil stempel={0.5} zeilen={1.0} /> },
        { from: 29.0, to: FOLGE08_SECONDS, el: <SceneEnde commentAt={0.55} /> },
      ]}
    />
  </AbsoluteFill>
);
