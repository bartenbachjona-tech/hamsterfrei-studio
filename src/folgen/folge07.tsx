import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneAnzeige, SceneChat, ScenePaypal, SceneIcloud, SceneAusland, SceneAkku, ScenePreis, SceneUrteil, SceneEnde } from "../scenes/folge07";
import wordsData from "./folge07.words.json";

// Folge07 · „Ist diese Handy-Anzeige faul?“ · Serie (a)-nah · Hook-Test Variante B (Paar 3) · OHNE Werbung
// 1 Take eleven_v3 (Generation axiiW4yiFbyJKvI3pVrF, 36,3 s), Pausen > 0,3 s per ffmpeg auf 0,22 s gekürzt → 33,1 s (Wortzeiten umgerechnet).
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const FOLGE07_SECONDS = Math.ceil((LAST + 1.8) * 10) / 10;

const MAP: Record<string, string> = {
  "fünf": "5",
  "fünf,": "5,",
  "Vier": "4",
  "Check,": "CHECK,",
};
const captionMap = (t: string) => (t in MAP ? MAP[t] : t);

export const Folge07: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/folge07.mp3"
      words={words}
      totalSeconds={FOLGE07_SECONDS}
      werbung={false}
      startle
      dingAt={30.5}
      captionMap={captionMap}
      scenes={[
        { from: 0, to: 3.06, el: <SceneHook /> },
        { from: 3.06, to: 4.9, el: <SceneAnzeige fallen={1.0} /> },
        { from: 4.9, to: 7.0, el: <SceneChat urteil={1.2} /> },
        { from: 7.0, to: 9.88, el: <ScenePaypal schutz={1.64} /> },
        { from: 9.88, to: 13.45, el: <SceneIcloud wertlos={2.85} /> },
        { from: 13.45, to: 17.22, el: <SceneAusland whatsapp={2.6} /> },
        { from: 17.22, to: 21.1, el: <SceneAkku haken={2.08} /> },
        { from: 21.1, to: 26.6, el: <ScenePreis lock={1.37} general={2.35} /> },
        { from: 26.6, to: 29.95, el: <SceneUrteil stempel={0.56} vier={1.35} /> },
        { from: 29.95, to: FOLGE07_SECONDS, el: <SceneEnde commentAt={0.55} /> },
      ]}
    />
  </AbsoluteFill>
);
