import React from "react";
import { SPRING, DUR, easeOut } from "../theme/motion";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { DISPLAY, SANS, SIZE } from "../theme/type";
import { fitOneLine } from "../theme/fit";
import { SAFE_RECT } from "../platformSafeArea";
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
  const { fps, width, height } = useVideoConfig();
  const startFrame = Math.round((kinetic.at ?? 0.15) * fps);
  const local = frame - startFrame;
  if (local < 0) return null;

  // waterfall-entry.md: an arrival is BINARY plus a whip, never a fade. This
  // carried `opacity: enter` on a 26px hop — the same ramp removed from
  // HeadlineBuild and CaptionChips, still live here because KineticType was
  // the one text component nobody had migrated. It is used by FootageScene,
  // SplitScene, FloatingCard and TypeCard, so it is on screen constantly.
  const p = easeOut(local / fps / 0.19);
  const rise = (1 - p) * 72;

  const lines = kinetic.text.split("\n");
  const isCaps = kinetic.style === "caps";
  // FIT, don't type. 100px was hardcoded for both styles regardless of how much
  // copy arrived, so a long kinetic line ran off the frame exactly the way the
  // six G05 headlines did.
  const boxW = width * (1 - 2 * SAFE_RECT.x0) - 90;
  const longest = lines.reduce((a, b) => (b.length > a.length ? b : a), "");
  const fitted = fitOneLine(longest, SIZE.display, boxW);

  const style: React.CSSProperties = isCaps
    ? {
        // the condensed-black face was never loaded and silently fell back to
        // Arial Narrow; the caps voice is the display face, tracked out
        fontFamily: DISPLAY,
        fontWeight: 900,
        textTransform: "uppercase",
        fontSize: fitted,
        letterSpacing: "0.02em",
        lineHeight: 1.08,
      }
    : {
        fontFamily: DISPLAY,
        fontWeight: 700,
        fontSize: fitted,
        letterSpacing: "-0.02em",
        lineHeight: 1.1,
      };

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: (kinetic.y ?? 0.28) * height,
        textAlign: "center",
        opacity: 1,
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
