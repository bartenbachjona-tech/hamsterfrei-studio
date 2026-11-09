import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode, Word } from "../Episode";
import { SceneLuecke, SceneEnde } from "../scenes/seminar07";
import { SceneHook, SceneSorgen, SceneRuhe, SceneChat, SceneCheck, SceneDiagramm, SceneBeleg, ScenePlagiat, SceneLehrkraft } from "../scenes/seminar09";
import wordsData from "./seminar09.words.json";

// Seminar09 · S9 „Noch 1 Tag bis zur Abgabe“ · Letzte-Chance-Video im Stil von S1 · Werbung (eigenes Produkt Seminararbeit-Profi), ohne Preis
// Take A (Generation 6dzv3ygZ2uP0HP2jbLm1), atempo 1.04; Szenenwechsel auf Scribe-Wortzeiten.
const words = (wordsData as { words: Word[] }).words;
const LAST = words[words.length - 1].end;
export const SEMINAR09_SECONDS = Math.ceil((LAST + 2.0) * 10) / 10;

export const Seminar09: React.FC = () => (
  <AbsoluteFill>
    <Episode
      audio="folgen/seminar09.mp3"
      words={words}
      totalSeconds={SEMINAR09_SECONDS}
      werbung
      startle
      scenes={[
        { from: 0, to: 4.77, el: <SceneHook das={1.85} letzte={2.62} /> },
        { from: 4.77, to: 12.23, el: <SceneSorgen fn={0} lit={1.77} ki={3.87} /> },
        { from: 12.23, to: 13.2, el: <SceneRuhe /> },
        { from: 13.2, to: 17.46, el: <SceneChat datei={0.07} text={2.26} /> },
        { from: 17.46, to: 22.42, el: <SceneCheck zit={0.58} fn={1.23} lit={1.85} form={3.12} merk={3.85} /> },
        { from: 22.42, to: 24.31, el: <SceneLuecke fehlt={1.19} ergaenze={1.4} /> },
        { from: 24.31, to: 26.39, el: <SceneDiagramm fertig={1.58} /> },
        { from: 26.39, to: 28.39, el: <SceneBeleg pdf={1.0} /> },
        { from: 28.39, to: 33.15, el: <ScenePlagiat plag={1.3} floskel={2.0} ersetzt={2.89} klingt={4.07} /> },
        { from: 33.15, to: 39.91, el: <SceneLehrkraft frage={0.1} antwort={2.58} feedback={5.27} /> },
        { from: 39.91, to: SEMINAR09_SECONDS, el: <SceneEnde frei={2.86} link={4.04} /> },
      ]}
    />
    {/* Pflicht-Hinweis, da ein Claude-Weg gezeigt wird */}
    <div style={{ position: "absolute", left: 540, width: 400, top: 1545, textAlign: "center", fontFamily: "Fredoka", fontSize: 34, fontWeight: 500, color: "#6B5444" }}>Claude-Konto ab 18</div>
  </AbsoluteFill>
);
