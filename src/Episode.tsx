import React from "react";
import { AbsoluteFill, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { Hamster } from "./Hamster";
import { INK, CREAM } from "./Scenes";

const fontFamily = "Fredoka";
loadFont({ family: fontFamily, url: staticFile("fonts/fredoka-latin.woff2"), weight: "300 700" });
loadFont({ family: fontFamily, url: staticFile("fonts/fredoka-latin-ext.woff2"), weight: "300 700", unicodeRange: "U+0100-024F, U+1E00-1EFF, U+20A0-20AB, U+20AD-20CF" });

export type Word = { text: string; start: number; end: number; type: string };
export type SceneDef = { from: number; to: number; el: React.ReactNode };
export type EpisodeProps = {
  audio: string; // Pfad in public/, z. B. "folgen/folge02.mp3"
  words: Word[]; // ElevenLabs-Scribe-Wörter (alle Typen, wird gefiltert)
  scenes: SceneDef[]; // Szenen auf der Leinwand, Sekunden ab Videostart
  totalSeconds: number;
  dingAt?: number; // Sekunde für den Schluss-Ding (Kommentar-Wort)
  werbung?: boolean; // kleines "Werbung"-Label oben links
  captionMap?: (text: string) => string; // Zahlwörter -> Ziffern usw.
  music?: string; // Pfad in public/, dezentes Musikbett (Standard: music/bett01.mp3)
  musicVolume?: number; // Standard 0.10
};

// Untertitel in kurzen Gruppen (max. 3 Wörter, Umbruch nach Satzzeichen)
type Chunk = { words: Word[]; start: number; end: number };
const buildChunks = (WORDS: Word[]): Chunk[] => {
  const out: Chunk[] = [];
  let cur: Word[] = [];
  WORDS.forEach((w) => {
    cur.push(w);
    if (cur.length >= 3 || /[.,“]$/.test(w.text)) {
      out.push({ words: cur, start: cur[0].start, end: w.end });
      cur = [];
    }
  });
  if (cur.length) out.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end });
  return out.map((c, i) => ({ ...c, end: i < out.length - 1 ? out[i + 1].start : c.end + 1.5 }));
};

const Captions: React.FC<{ chunks: Chunk[]; map: (t: string) => string }> = ({ chunks, map }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const chunk = chunks.find((c) => t >= c.start && t < c.end);
  if (!chunk) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: 520,
        width: 420,
        top: 1230,
        height: 300,
        display: "flex",
        flexWrap: "wrap",
        alignContent: "center",
        justifyContent: "center",
        gap: "4px 18px",
        textAlign: "center",
      }}
    >
      {chunk.words.map((w, i) => {
        const active = t >= w.start && t < w.end + 0.08;
        const label = map(w.text.replace(/[„“]/g, ""));
        return (
          <span
            key={i}
            style={{
              fontSize: label.length > 13 ? 46 : 66,
              fontWeight: 600,
              lineHeight: 1.15,
              color: active ? "#23885A" : INK,
              WebkitTextStroke: "0px",
            }}
          >
            {label}
          </span>
        );
      })}
    </div>
  );
};

export const Episode: React.FC<EpisodeProps> = ({ audio, words, scenes, totalSeconds, dingAt, werbung = true, captionMap, music = "music/bett01.mp3", musicVolume = 0.1 }) => {
  const WORDS = React.useMemo(() => words.filter((w) => w.type === "word"), [words]);
  const chunks = React.useMemo(() => buildChunks(WORDS), [WORDS]);
  const SCENES = scenes;
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const speaking = WORDS.some((w) => t >= w.start && t <= w.end);
  const talking = speaking && frame % 6 < 3;
  const blink = frame % 105 < 4;
  const lastSceneStart = [...SCENES].reverse().find((s) => t >= s.from)?.from ?? 0;
  const since = t - lastSceneStart;
  const pointerAngle = interpolate(since, [0, 0.15, 0.4, 0.7], [0, -14, 6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const bob = Math.sin(frame / 9) * 6;

  return (
    <AbsoluteFill style={{ background: CREAM, fontFamily, color: INK }}>
      <Audio src={staticFile(audio)} />
      {music && (
        <Audio
          src={staticFile(music)}
          loop
          volume={(f) =>
            musicVolume *
            interpolate(f, [0, 15, totalSeconds * fps - 30, totalSeconds * fps], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
          }
        />
      )}
      {SCENES.slice(1).map((s) => (
        <Sequence key={s.from} from={Math.round(s.from * fps) - 3} durationInFrames={12} layout="none">
          <Audio src={staticFile("sfx/whoosh.wav")} volume={0.6} />
        </Sequence>
      ))}
      {dingAt !== undefined && (
        <Sequence from={Math.round(dingAt * fps)} durationInFrames={10} layout="none">
          <Audio src={staticFile("sfx/ding.wav")} volume={0.7} />
        </Sequence>
      )}

      {/* Werbung */}
      {werbung && <div style={{ position: "absolute", left: 60, top: 64, fontSize: 30, fontWeight: 500, color: "#6B5444", background: "#FFFFFF", border: "3px solid #6B5444", borderRadius: 14, padding: "4px 16px" }}>
        Werbung
      </div>}

      {/* Leinwand */}
      <div style={{ position: "absolute", left: 40, top: 148, width: 1000, height: 28, borderRadius: 14, background: INK }} />
      <div
        style={{
          position: "absolute",
          left: 66,
          top: 176,
          width: 948,
          height: 1004,
          background: "#FFFFFF",
          border: `8px solid ${INK}`,
          borderTop: "none",
          borderRadius: "0 0 30px 30px",
          overflow: "hidden",
        }}
      >
        {SCENES.map((s) => (
          <Sequence key={s.from} from={Math.round(s.from * fps)} durationInFrames={Math.round((s.to - s.from) * fps)}>
            <AbsoluteFill>{s.el}</AbsoluteFill>
          </Sequence>
        ))}
      </div>

      {/* Boden */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1500, bottom: 0, background: "#F5E7CF", borderTop: "6px solid #EAD6B4" }} />

      {/* Hamster */}
      <div style={{ position: "absolute", left: 10, top: 1050, translate: `0px ${bob}px` }}>
        <Hamster size={520} talking={talking} blink={blink} pointerAngle={pointerAngle} />
      </div>

      <Captions chunks={chunks} map={captionMap ?? ((t) => t)} />
    </AbsoluteFill>
  );
};
