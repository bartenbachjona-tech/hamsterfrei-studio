import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneStand, SceneLuecke, SceneCoach, SceneEnde } from "../scenes/seminar07";
import wordsData from "./seminar07.words.json";

// Seminar07 · S7 Suchbegriff-Video „Seminararbeit mit KI? So geht's.“ · Werbung (eigenes Produkt Seminararbeit-Profi), ohne Preis
// Fassung 2 (Jonas Feedback 06.11.): Hook unverändert, danach „Wo stehst du?“ → ein einfaches Beispiel → Probe-Prüfung → Website.
export const SEMINAR07_SECONDS = 27.2;

const words = (wordsData as { words: Word[] }).words;

export const Seminar07: React.FC = () => (
  <Episode
    audio="folgen/seminar07.mp3"
    words={words}
    totalSeconds={SEMINAR07_SECONDS}
    werbung
    startle
    scenes={[
      { from: 0, to: 3.8, el: <SceneHook weg={2.8} /> },
      { from: 3.8, to: 13.96, el: <SceneStand q={2.6} m={5.24} f={8.08} /> },
      { from: 13.96, to: 18.8, el: <SceneLuecke fehlt={1.36} ergaenze={3.52} /> },
      { from: 18.8, to: 22.4, el: <SceneCoach antwort={1.2} feedback={2.45} /> },
      { from: 22.4, to: SEMINAR07_SECONDS, el: <SceneEnde frei={0.1} link={1.8} /> },
    ]}
  />
);
