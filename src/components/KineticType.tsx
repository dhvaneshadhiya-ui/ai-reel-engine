import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import type { Kinetic } from "../types";

/**
 * Display type overlaid on footage or cards.
 * - "caps": condensed heavy caps, white with soft shadow (NEAR-HUMAN PRECISION)
 * - "serif": editorial italic serif (much faster / It does things itself)
 */
export const KineticType: React.FC<{
  kinetic: Kinetic;
  color?: string;
}> = ({ kinetic, color = "white" }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const startFrame = Math.round((kinetic.at ?? 0.15) * fps);
  const local = frame - startFrame;
  if (local < 0) return null;

  const enter = spring({
    frame: local,
    fps,
    config: { damping: 16, stiffness: 160, mass: 0.6 },
    durationInFrames: 16,
  });
  const rise = interpolate(enter, [0, 1], [26, 0]);

  const lines = kinetic.text.split("\n");
  const isCaps = kinetic.style === "caps";

  const style: React.CSSProperties = isCaps
    ? {
        fontFamily: "'HelveticaNeue-CondensedBlack', 'Arial Narrow', sans-serif",
        fontWeight: 900,
        textTransform: "uppercase",
        fontSize: 92,
        letterSpacing: "0.03em",
        lineHeight: 1.02,
      }
    : {
        fontFamily: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
        fontStyle: "italic",
        fontWeight: 700,
        fontSize: 98,
        lineHeight: 1.08,
      };

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: (kinetic.y ?? 0.28) * height,
        textAlign: "center",
        opacity: enter,
        transform: `translateY(${rise}px)`,
        pointerEvents: "none",
      }}
    >
      {/* scrim so light type never dies on a light backdrop */}
      {(kinetic.scrim ?? true) && (
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "50%",
            transform: "translate(-50%, -50%)",
            width: "120%",
            height: "180%",
            background:
              "radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0,0,0,0.55), rgba(0,0,0,0) 70%)",
          }}
        />
      )}
      {lines.map((line, i) => (
        <div
          key={i}
          style={{
            ...style,
            color,
            position: "relative",
            textShadow:
              "0 3px 24px rgba(0,0,0,0.6), 0 1px 4px rgba(0,0,0,0.55)",
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
};
