import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useTheme } from "../theme/tokens";

export interface ToolStackProps {
  headline?: string;
  bg?: "cream" | "black";
  items: {
    name: string;
    src: string;
    tagline?: string;
  }[];
}

const POSITIONS = [
  { x: 70, y: 365, rotate: -4.5 },
  { x: 565, y: 335, rotate: 4 },
  { x: 95, y: 760, rotate: 3.5 },
  { x: 550, y: 735, rotate: -3 },
  { x: 315, y: 1135, rotate: 1.5 },
];

/**
 * A tactile five-product overview: official screenshots arrive as paper-like
 * cards, then settle into one coherent stack. This is intentionally distinct
 * from the engine's generic grid and carousel treatments.
 */
export const ToolStack: React.FC<ToolStackProps> = ({
  headline = "Google's free AI stack",
  bg = "cream",
  items,
}) => {
  const theme = useTheme();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dark = bg === "black";

  return (
    <AbsoluteFill
      style={{
        background: dark ? theme.black : theme.cream,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 68,
          right: 68,
          top: 122,
          fontFamily: "Fraunces",
          fontStyle: "italic",
          fontWeight: 700,
          fontSize: 88,
          lineHeight: 0.95,
          letterSpacing: -3,
          color: dark ? theme.white : theme.ink,
        }}
      >
        {headline}
      </div>
      <div
        style={{
          position: "absolute",
          top: 280,
          left: 72,
          width: 230,
          height: 8,
          borderRadius: 8,
          background: theme.accent,
          transformOrigin: "0 50%",
          transform: `scaleX(${interpolate(frame, [3, 22], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })})`,
        }}
      />
      {items.slice(0, 5).map((item, index) => {
        const position = POSITIONS[index];
        const enter = spring({
          frame: frame - index * 5,
          fps,
          config: { damping: 15, stiffness: 145, mass: 0.72 },
          durationInFrames: 22,
        });
        const cardW = index === 4 ? 450 : 420;
        const cardH = index === 4 ? 330 : 320;
        const float = Math.sin((frame + index * 11) / 18) * 4;
        return (
          <div
            key={item.name}
            style={{
              position: "absolute",
              left: position.x,
              top: position.y,
              width: cardW,
              height: cardH,
              borderRadius: 26,
              overflow: "hidden",
              background: theme.white,
              boxShadow: dark ? theme.shadow.cardOnDark : theme.shadow.card,
              opacity: enter,
              transform: `translateY(${(1 - enter) * 110 + float}px) rotate(${position.rotate * enter}deg) scale(${0.84 + enter * 0.16})`,
            }}
          >
            <Img
              src={staticFile(item.src)}
              style={{
                width: "100%",
                height: cardH - 94,
                objectFit: "cover",
                objectPosition: "50% 35%",
                display: "block",
              }}
            />
            <div
              style={{
                height: 94,
                display: "flex",
                alignItems: "center",
                gap: 18,
                padding: "0 24px",
                color: theme.ink,
              }}
            >
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: 16,
                  background: theme.accent,
                  color: theme.white,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: theme.sans,
                  fontWeight: 900,
                  fontSize: 24,
                }}
              >
                {String(index + 1).padStart(2, "0")}
              </div>
              <div>
                <div
                  style={{
                    fontFamily: theme.sans,
                    fontWeight: 900,
                    fontSize: 30,
                    lineHeight: 1,
                  }}
                >
                  {item.name}
                </div>
                {item.tagline && (
                  <div
                    style={{
                      marginTop: 7,
                      fontFamily: theme.sans,
                      color: theme.muted,
                      fontSize: 19,
                      fontWeight: 650,
                    }}
                  >
                    {item.tagline}
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
      <div
        style={{
          position: "absolute",
          right: 56,
          bottom: 90,
          fontFamily: theme.pixel,
          fontSize: 17,
          letterSpacing: 1,
          color: dark ? theme.mutedOnDark : theme.muted,
        }}
      >
        FREE STARTING ACCESS · LIMITS APPLY
      </div>
    </AbsoluteFill>
  );
};
