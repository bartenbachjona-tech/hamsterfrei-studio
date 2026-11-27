import React from "react";
import { AbsoluteFill } from "remotion";
import { Word } from "../Episode";
import { EpisodeE2 } from "../EpisodeE2";
import { E2Hook, SceneHook, SceneFrage, SceneJa, SceneGesetz, SceneAchtzehn, SceneLuecke, SceneUrteil, SceneEnde } from "../scenes/folge16";
import wordsData from "./folge16.words.json";

// Folge16 · Hamster-Test „Neun Euro mit siebzehn – erlaubt?“ · Serie (a) · Einstiegs-Test E2 (Paar 3, E2 zuerst) · OHNE Werbung
// 1 Take eleven_v3 (Flow B7GpQDq7KwtnPqr0ysl9, Generation wqJRDAOGGpHC0wU4mSvb, 35,55 s), per atempo 1,07 auf 33,2 s gestrafft (wie F15). Audio-Tags entfernt, Scribe-Zeiten ÷ 1,07. Für die Untertitel sind „dreizehn Euro neunzig.“ / „vierzehn Euro sechzig.“ in words.json zu je einem Eintrag „13,90 €.“ / „14,60 €.“ zusammengefasst (gleiche Zeiten).
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE16_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "siebzehn": "17",
  "achtzehn": "18",
  "achtzehnten": "18.",
  "neun": "9",
  "Euro": "€",
  "Paragraf": "§",
  "zweiundzwanzig": "22",
  "fünf": "5",
  "Lohn,": "LOHN,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge16: React.FC = () => (
  <AbsoluteFill>
    <EpisodeE2
      audio="folgen/folge16.mp3"
      words={words}
      totalSeconds={FOLGE16_SECONDS}
      werbung={false}
      dingAt={30.7}
      captionMap={captionMap}
      e2={{ until: 1.0, el: <E2Hook /> }}
      scenes={[
        { from: 0, to: 4.02, el: <SceneHook /> },
        { from: 4.02, to: 7.95, el: <SceneFrage neun={1.94} /> },
        { from: 7.95, to: 14.47, el: <SceneJa par={1.27} unter={3.65} /> },
        { from: 14.47, to: 16.62, el: <SceneGesetz stimmt={1.45} /> },
        { from: 16.62, to: 22.1, el: <SceneAchtzehn lohn={2.43} jan={3.74} /> },
        { from: 22.1, to: 26.45, el: <SceneLuecke sitten={2.83} /> },
        { from: 26.45, to: 30.3, el: <SceneUrteil stempel={0.4} zeilen={0.7} fair={1.4} /> },
        { from: 30.3, to: FOLGE16_SECONDS, el: <SceneEnde commentAt={0.4} /> },
      ]}
    />
  </AbsoluteFill>
);

// Cover (Hook-Paket, LOOK.md): E2-Schlüsselbild ohne Untertitel, Standbild bei 0,5 s
export const Folge16Cover: React.FC = () => (
  <AbsoluteFill style={{ fontFamily: "Fredoka", color: "#3A2618" }}>
    <E2Hook />
  </AbsoluteFill>
);
