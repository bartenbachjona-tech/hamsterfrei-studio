import React from "react";
import { Episode, Word } from "../Episode";
import { SceneHook, SceneBeispiel, SceneProjekt, SceneDrei, SceneF1, SceneF2, SceneF3, SceneRegel, SceneEnde } from "../scenes/seminar04";

// T4 · „Lass Claude deine Seminararbeit prüfen – nicht schreiben“ · Werbung (eigenes Produkt, Skill nicht genannt)
// ENTWURF: Zeiten geschätzt. Nach der Vertonung words aus seminar04.words.json laden und Zeiten auf die Wort-Zeitstempel legen.
export const SEMINAR04_SECONDS = 38;

const words: Word[] = []; // TODO: (wordsData as { words: Word[] }).words nach Scribe

const MAP: Record<string, string> = { zehnten: "10.", zwei: "2", drei: "3", "Eins:": "1.", "Zwei:": "2.", "Drei:": "3." };

export const Seminar04: React.FC = () => (
  <Episode
    audio="folgen/seminar03.mp3" /* Platzhalter, wird durch folgen/seminar04.mp3 ersetzt */
    words={words}
    totalSeconds={SEMINAR04_SECONDS}
    dingAt={36}
    werbung
    startle
    captionMap={(t) => MAP[t] ?? t}
    scenes={[
      { from: 0, to: 4.3, el: <SceneHook pruefen={2.4} schreiben={3.4} /> },
      { from: 4.3, to: 9.0, el: <SceneBeispiel kap={2.0} frage={3.4} /> },
      { from: 9.0, to: 15.5, el: <SceneProjekt projekt={0.3} files={[2.6, 3.4, 4.6]} /> },
      { from: 15.5, to: 17.0, el: <SceneDrei /> },
      { from: 17.0, to: 19.8, el: <SceneF1 ok={1.6} /> },
      { from: 19.8, to: 23.6, el: <SceneF2 quelle={1.5} /> },
      { from: 23.6, to: 26.3, el: <SceneF3 frage={0.8} /> },
      { from: 26.3, to: 32.5, el: <SceneRegel selbst={0.4} lehrkraft={2.0} angeben={4.0} /> },
      { from: 32.5, to: SEMINAR04_SECONDS, el: <SceneEnde commentAt={3.5} /> },
    ]}
  />
);
