import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Headline } from "../types";

const SERIF = "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";
const SERIF_IT = "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";
const ACCENT = "#d97757"; // Anthropic clay

/**
 * Editorial serif headline that builds line-by-line — the reference-reel hook
 * treatment ("Open AI" → "Finally Revealed" → "first hardware"). Each line
 * fades + rises in; headline lines also do a grey→ink colour reveal.
 */
export const HeadlineBuild: React.FC<{ spec: Headline }> = ({ spec }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const y = spec.y ?? 0.5;
  const align = spec.align ?? "center";
  const dark = spec.theme === "dark";
  const ink = dark ? "#0f0f0f" : "#ffffff";
  const rgb = dark ? "15,15,15" : "255,255,255";

  const styleFor = (kind: string): React.CSSProperties => {
    if (kind === "label")
      return { fontFamily: SERIF, fontWeight: 700, fontSize: 46, letterSpacing: 2, textTransform: "uppercase" as const };
    if (kind === "subtitle")
      return { fontFamily: SERIF_IT, fontStyle: "italic", fontWeight: 700, fontSize: 52, opacity: 0.95 };
    return { fontFamily: SERIF, fontWeight: 800, fontSize: 100, lineHeight: 1.02, letterSpacing: -1.5 };
  };

  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: align === "center" ? "center" : "flex-start" }}>
      <div
        style={{
          position: "absolute",
          top: `${y * 100}%`,
          transform: "translateY(-50%)",
          width: "100%",
          padding: align === "center" ? "0 70px" : "0 84px",
          textAlign: align,
          display: "flex",
          flexDirection: "column",
          alignItems: align === "center" ? "center" : "flex-start",
          gap: 6,
          // soft scrim so serif never dies on busy footage
          filter: dark ? "none" : "drop-shadow(0 3px 22px rgba(0,0,0,0.55))",
        }}
      >
        {spec.lines.map((ln, i) => {
          const en = spring({ frame: frame - Math.round(ln.at * fps), fps, config: { damping: 18, stiffness: 150 }, durationInFrames: 14 });
          const reveal = interpolate(t, [ln.at, ln.at + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const isHead = ln.kind === "headline";
          const a = 0.34 + 0.66 * reveal; // grey → ink reveal
          const color = ln.accent ? ACCENT : isHead ? `rgba(${rgb},${a})` : ink;
          return (
            <div
              key={i}
              style={{
                ...styleFor(ln.kind),
                color,
                opacity: en,
                transform: `translateY(${(1 - en) * 26}px)`,
                whiteSpace: "pre-line",
              }}
            >
              {ln.text}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
