import React from "react";
import { SPRING, DUR } from "../theme/motion";
import {
  AbsoluteFill,
  Img,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
} from "remotion";
import type { Scene } from "../types";

type CascadeProps = Extract<Scene, { type: "wordcascade" }>;

const BGS: Record<string, string> = {
  cream: "#f2ecdf",
  black: "#0c0c0c",
  white: "#ffffff",
};

const ACCENT_ON_LIGHT = "#C2410C";   // warm ink — reads on cream
const ACCENT_ON_DARK = "#FFD84D";

const wordStyle = (
  style: string,
  dark: boolean,
  size: number,
  accent = false
): React.CSSProperties => {
  const base: React.CSSProperties = {
    lineHeight: 1.08,
    color: accent
      ? (dark ? ACCENT_ON_LIGHT : ACCENT_ON_DARK)
      : (dark ? "#111111" : "#f5f1e8"),
  };
  switch (style) {
    case "serif":
      return {
        ...base,
        // SF Pro only — Georgia breached the brand rule (STYLE-RULES 2026-07-29)
        fontFamily: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
        fontStyle: "italic",
        fontWeight: 700,
        fontSize: 100 * size,
        letterSpacing: "-0.01em",
      };
    case "caps":
      return {
        ...base,
        fontFamily: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
        fontWeight: 900,
        textTransform: "uppercase",
        fontSize: 100 * size,
        letterSpacing: "0.02em",
      };
    case "pixel":
      return {
        ...base,
        fontFamily: "'Menlo', 'Courier New', monospace",
        fontWeight: 400,
        textTransform: "uppercase",
        fontSize: 46 * size,
        lineHeight: 1.5,
        textShadow: dark
          ? "4px 4px 0 rgba(217,119,87,0.55)"
          : "4px 4px 0 rgba(217,119,87,0.6)",
      };
    case "gradient":
      return {
        ...base,
        fontFamily:
          "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
        fontWeight: 800,
        fontSize: 100 * size,
        backgroundImage: "linear-gradient(135deg, #d97757, #e8a87c, #d97757)",
        WebkitBackgroundClip: "text",
        backgroundClip: "text",
        color: "transparent",
      };
    default:
      return base;
  }
};

/**
 * Nick-style kinetic word stack: words/phrases pop in one at a time in mixed
 * typography on a clean cream/black field. Optional facecam bottom half.
 */
export const WordCascade: React.FC<{ scene: CascadeProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bg = BGS[scene.bg ?? "cream"];
  const dark = (scene.bg ?? "cream") !== "black";
  const hasFace = Boolean(scene.bottomSrc);

  const stack = (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 14,
        padding: "0 60px",
        textAlign: "center",
      }}
    >
      {scene.mascot && (
        <Img
          src={staticFile(scene.mascot)}
          style={{ width: 130, marginBottom: 14, imageRendering: "pixelated" }}
        />
      )}
      {scene.words.map((w, i) => {
        const local = frame - Math.round(w.at * fps);
        if (local < 0) return null;
        const pop = spring({
          frame: local,
          fps,
          config: SPRING.pop,
          durationInFrames: DUR.quick,
        });
        return (
          <div
            key={i}
            style={{
              ...wordStyle(w.style, dark, w.size ?? 1, (w as {accent?: boolean}).accent ?? false),
              opacity: pop,
              transform: `scale(${0.86 + 0.14 * pop}) translateY(${(1 - pop) * 18}px)`,
            }}
          >
            {w.text}
          </div>
        );
      })}
    </div>
  );

  return (
    <AbsoluteFill style={{ background: bg }}>
      {hasFace ? (
        <>
          <div
            style={{
              position: "absolute",
              top: 0,
              width: "100%",
              height: "50%",
              overflow: "hidden",
            }}
          >
            {stack}
          </div>
          <div
            style={{
              position: "absolute",
              top: "50%",
              width: "100%",
              height: "50%",
              overflow: "hidden",
              borderRadius: "28px 28px 0 0",
            }}
          >
            <Video
              src={staticFile(scene.bottomSrc!)}
              startFrom={Math.round((scene.bottomFrom ?? 0) * fps)}
              muted
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                objectPosition: `${(scene.bottomFocusX ?? 0.5) * 100}% 20%`,
              }}
            />
          </div>
        </>
      ) : (
        stack
      )}
    </AbsoluteFill>
  );
};
