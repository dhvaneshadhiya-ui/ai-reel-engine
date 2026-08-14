import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type LogoProps = Extract<Scene, { type: "logobeat" }>;

const PIXEL = "'PressStart2P','Menlo',monospace";

/** Animated pixel starburst: 12 rays that grow out + slow spin. */
const Starburst: React.FC<{ color: string; progress: number; spin: number }> = ({
  color,
  progress,
  spin,
}) => {
  const rays = 12;
  return (
    <svg
      viewBox="-50 -50 100 100"
      width={230}
      height={230}
      style={{ transform: `rotate(${spin}deg)`, display: "block" }}
    >
      {Array.from({ length: rays }).map((_, i) => {
        const a = (i / rays) * Math.PI * 2;
        const inner = 8;
        const outer = 14 + 30 * progress;
        const x1 = Math.cos(a) * inner;
        const y1 = Math.sin(a) * inner;
        const x2 = Math.cos(a) * outer;
        const y2 = Math.sin(a) * outer;
        return (
          <line
            key={i}
            x1={x1}
            y1={y1}
            x2={x2}
            y2={y2}
            stroke={color}
            strokeWidth={7}
            strokeLinecap="butt"
          />
        );
      })}
      <circle cx="0" cy="0" r={6 * progress} fill={color} />
    </svg>
  );
};

/** Nick-style beat separator: an animated logo/wordmark alone on a clean field. */
export const LogoBeat: React.FC<{ scene: LogoProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const enter = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 170, mass: 0.6 },
    durationInFrames: 14,
  });

  const isStar = scene.mark === "starburst";
  const markColor = scene.markColor ?? scene.textColor ?? "#d97757";
  // starburst grows in over ~16f, then slowly spins the whole time
  const burst = interpolate(frame, [0, 16], [0, 1], { extrapolateRight: "clamp" });
  const spin = frame * 0.55;
  // beam draws downward after the mark lands
  const beam = interpolate(frame, [16, 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (x) => 1 - Math.pow(1 - x, 3),
  });

  return (
    <AbsoluteFill
      style={{
        background: scene.bg ?? "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ opacity: enter, textAlign: "center" }}>
        {isStar ? (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Starburst color={markColor} progress={burst} spin={spin} />
            {scene.text && (
              <div
                style={{
                  marginTop: 18,
                  fontFamily: PIXEL,
                  fontSize: 40,
                  letterSpacing: "0.06em",
                  textTransform: "uppercase",
                  color: markColor,
                  lineHeight: 1.4,
                }}
              >
                {scene.text}
              </div>
            )}
            <div
              style={{
                marginTop: 20,
                width: 3,
                height: 120 * beam,
                background: "rgba(255,255,255,0.55)",
              }}
            />
          </div>
        ) : scene.src ? (
          <Img
            src={staticFile(scene.src)}
            style={{
              maxWidth: 560,
              maxHeight: 560,
              transform: `scale(${0.8 + 0.2 * enter})`,
            }}
          />
        ) : (
          <div
            style={{
              fontFamily: scene.pixel
                ? PIXEL
                : "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
              fontWeight: scene.pixel ? 400 : 700,
              fontSize: scene.pixel ? 64 : 130,
              color: scene.textColor ?? "#d97757",
              letterSpacing: scene.pixel ? "0.04em" : "-0.02em",
              transform: `scale(${0.8 + 0.2 * enter})`,
            }}
          >
            {scene.text}
          </div>
        )}
        {scene.label && !isStar && (
          <div
            style={{
              marginTop: 26,
              fontFamily: "'Menlo', monospace",
              fontSize: 30,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "rgba(255,255,255,0.55)",
            }}
          >
            {scene.label}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
