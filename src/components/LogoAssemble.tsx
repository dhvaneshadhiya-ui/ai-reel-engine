import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";

/**
 * Brand-logo assembly (reference: Google-reel hook, 2026-07-31): the logo's
 * SVG paths fly in from staggered directions, rotate + spring-settle into the
 * full mark, then an optional count-up label lands beneath ("15 NEW TOOLS").
 * Paths come from tools/get_logo.mjs (svgl.app) or a hand-written
 * <name>.paths.json — embedded into the beat by the build script, so no
 * runtime fetch. Monochrome marks can be tinted via fillOverride.
 */
export interface LogoAssembleProps {
  viewBox: string;
  paths: { d: string; fill: string }[];
  /** logo square size in px (default 430) */
  size?: number;
  /** vertical center of the logo, 0..1 of frame height (default 0.30) */
  y?: number;
  bg?: "cream" | "black";
  /** tint all paths (for monochrome/currentColor marks) */
  fillOverride?: string;
  /** small caps label under the logo */
  label?: string;
  /** count-up number rendered above the label (e.g. 15) */
  countTo?: number;
  /** seconds into the scene when label/count start (default 0.55) */
  labelAt?: number;
}

export const LogoAssemble: React.FC<LogoAssembleProps> = ({
  viewBox,
  paths,
  size = 430,
  y = 0.3,
  bg = "cream",
  fillOverride,
  label,
  countTo,
  labelAt = 0.55,
}) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const theme = useTheme();
  const dark = bg === "black";
  const ink = dark ? theme.inkOnDark : theme.ink;

  // directional offsets — paths fly in from spread angles
  const dirs = paths.map((_, i) => {
    const angle = (i * 137 + 30) * (Math.PI / 180); // golden-angle spread
    return {
      dx: Math.cos(angle) * 150,
      dy: Math.sin(angle) * 150,
      rot: i % 2 === 0 ? -55 : 40,
    };
  });

  const allInFrame = paths.length * 3 + 18;
  const settle = interpolate(frame, [allInFrame, allInFrame + 10], [1.04, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (t) => 1 - Math.pow(1 - t, 2),
  });

  const labelF = Math.round(labelAt * fps);
  const labelIn = spring({
    frame: frame - labelF,
    fps,
    config: { damping: 16, stiffness: 180, mass: 0.5 },
    durationInFrames: 14,
  });
  const count =
    countTo !== undefined
      ? Math.round(
          interpolate(frame, [labelF, labelF + Math.round(0.8 * fps)], [0, countTo], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: (t) => 1 - Math.pow(1 - t, 3),
          })
        )
      : undefined;

  return (
    <AbsoluteFill
      style={{ background: dark ? theme.black : theme.cream }}
    >
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(120% 90% at 50% 0%, rgba(255,255,255,0.5), rgba(0,0,0,0.04))",
        }}
      />
      <svg
        viewBox={viewBox}
        width={size}
        height={size}
        style={{
          position: "absolute",
          left: "50%",
          top: height * y,
          transform: `translate(-50%, -50%) scale(${settle})`,
          overflow: "visible",
        }}
      >
        {paths.map((p, i) => {
          const en = spring({
            frame: frame - i * 3,
            fps,
            config: { damping: 15, stiffness: 150, mass: 0.6 },
            durationInFrames: 18,
          });
          const { dx, dy, rot } = dirs[i];
          return (
            <path
              key={i}
              d={p.d}
              fill={fillOverride ?? p.fill}
              style={{
                opacity: Math.min(1, en * 1.6),
                transform: `translate(${(1 - en) * dx}px, ${(1 - en) * dy}px) rotate(${(1 - en) * rot}deg) scale(${0.4 + 0.6 * en})`,
                transformBox: "fill-box",
                transformOrigin: "center",
              }}
            />
          );
        })}
      </svg>

      {(countTo !== undefined || label) && (
        <div
          style={{
            position: "absolute",
            top: height * y + size / 2 + 40,
            width: "100%",
            textAlign: "center",
            opacity: labelIn,
            transform: `translateY(${(1 - labelIn) * 22}px)`,
          }}
        >
          {countTo !== undefined && (
            <div
              style={{
                fontFamily: theme.serif,
                fontWeight: 800,
                fontSize: 120,
                lineHeight: 1.05,
                color: ink,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {count}
            </div>
          )}
          {label && (
            <div
              style={{
                marginTop: 10,
                fontFamily: theme.sans,
                fontWeight: 700,
                fontSize: 42,
                letterSpacing: "0.26em",
                textTransform: "uppercase",
                color: dark ? theme.mutedOnDark : theme.muted,
              }}
            >
              {label}
            </div>
          )}
        </div>
      )}
    </AbsoluteFill>
  );
};
