import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Easing,
} from "remotion";
// NOTE: the Fraunces loadFont() that used to sit here was removed — its
// module-scope delayRender ran on EVERY composition in the project (Root
// imports this file) and timed out the reel render. It was also dead: the
// SF-Pro-only rule (STYLE-RULES 2026-07-29) already points every theme
// serif token at the SF Pro stack, so no Fraunces face is used.

const CREAM = "#f2ecdf";
const INK = "#141414";
const ORANGE = "#e8845b";

const SANS =
  "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";

// One headline word/line popping in nick-style: ease-out-cubic + slight scale.
const Pop: React.FC<{
  at: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ at, children, style }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [at, at + 11], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        opacity: t,
        transform: `scale(${0.86 + 0.14 * t}) translateY(${(1 - t) * 14}px)`,
        transformOrigin: "left center",
        ...style,
      }}
    >
      {children}
    </div>
  );
};

const IgGlyph: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <rect x="2.5" y="2.5" width="19" height="19" rx="5.5" stroke="#fff" strokeWidth="2" />
    <circle cx="12" cy="12" r="4.4" stroke="#fff" strokeWidth="2" />
    <circle cx="17.4" cy="6.6" r="1.5" fill="#fff" />
  </svg>
);

export const InstaCTA: React.FC<{ background?: string }> = ({ background }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Card entrance: slide up + soft spring settle
  const cardIn = spring({ frame, fps, config: { damping: 15, stiffness: 120 } });

  // Phone entrance: slides in from the left with a rotation settle
  const phoneIn = spring({
    frame: frame - 8,
    fps,
    config: { damping: 14, stiffness: 100 },
  });
  const idle = Math.sin((frame / fps) * 1.6) * 5; // gentle float after settling

  // Global exit
  const exit = interpolate(
    frame,
    [durationInFrames - 22, durationInFrames - 6],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.in(Easing.cubic),
    }
  );

  // Underline draw under the orange line
  const underline = interpolate(frame, [58, 74], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const pillIn = spring({
    frame: frame - 66,
    fps,
    config: { damping: 12, stiffness: 160 },
  });

  const arrowIn = interpolate(frame, [84, 96], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: background ?? "transparent" }}>
      <div
        style={{
          position: "absolute",
          left: 90,
          top: "50%",
          transform: `translateY(-50%) translateY(${(1 - cardIn) * 60 - exit * 30}px) scale(${
            0.94 + 0.06 * cardIn - exit * 0.03
          })`,
          opacity: Math.min(cardIn * 1.4, 1) * (1 - exit),
        }}
      >
        <div
          style={{
            width: 1000,
            height: 660,
            background: CREAM,
            borderRadius: 30,
            filter:
              "drop-shadow(0 24px 40px rgba(0,0,0,0.38)) drop-shadow(0 4px 12px rgba(0,0,0,0.22))",
            display: "flex",
            alignItems: "center",
            padding: "0 54px 0 44px",
            position: "relative",
            overflow: "visible",
          }}
        >
          {/* Phone with the real IG profile recording */}
          <div
            style={{
              width: 296,
              height: 636,
              flexShrink: 0,
              transform: `translateX(${(1 - phoneIn) * -140}px) rotate(${
                -12 + 8 * phoneIn
              }deg) translateY(${idle}px)`,
              opacity: phoneIn,
              background: "#101010",
              borderRadius: 46,
              padding: 9,
              filter: "drop-shadow(0 18px 32px rgba(0,0,0,0.35))",
              marginTop: -6,
            }}
          >
            <div
              style={{
                width: "100%",
                height: "100%",
                borderRadius: 38,
                overflow: "hidden",
                position: "relative",
                background: "#000",
              }}
            >
              {/* crop the status bar (recording indicator) off the top */}
              <OffthreadVideo
                muted
                src={staticFile("assets/ig-cta/ig-profile-rec.mp4")}
                style={{
                  position: "absolute",
                  width: "100%",
                  height: "112%",
                  top: "-7%",
                  left: 0,
                  objectFit: "cover",
                }}
              />
            </div>
          </div>

          {/* Copy block */}
          <div style={{ marginLeft: 62, paddingTop: 8 }}>
            <Pop at={10}>
              <div
                style={{
                  fontFamily: SANS,
                  fontWeight: 900,
                  fontSize: 84,
                  letterSpacing: 1,
                  color: INK,
                  lineHeight: 1.02,
                }}
              >
                EVERY
              </div>
            </Pop>
            <Pop at={19}>
              <div
                style={{
                  fontFamily: "Fraunces, Georgia, serif",
                  fontStyle: "italic",
                  fontWeight: 700,
                  fontSize: 76,
                  color: INK,
                  lineHeight: 1.12,
                }}
              >
                single reel
              </div>
            </Pop>
            <Pop at={30}>
              <div
                style={{
                  fontFamily: SANS,
                  fontWeight: 900,
                  fontSize: 84,
                  letterSpacing: 1,
                  color: INK,
                  lineHeight: 1.06,
                }}
              >
                IS LIVE
              </div>
            </Pop>
            <Pop at={42}>
              <div style={{ position: "relative", display: "inline-block" }}>
                <div
                  style={{
                    fontFamily: SANS,
                    fontWeight: 900,
                    fontSize: 74,
                    color: ORANGE,
                    lineHeight: 1.1,
                  }}
                >
                  on Instagram
                </div>
                <div
                  style={{
                    height: 8,
                    borderRadius: 4,
                    background: ORANGE,
                    width: `${underline * 100}%`,
                    marginTop: 4,
                  }}
                />
              </div>
            </Pop>

            {/* Handle pill — nick chip style */}
            <div
              style={{
                marginTop: 40,
                transform: `scale(${Math.max(pillIn, 0)})`,
                transformOrigin: "left center",
                display: "inline-flex",
                alignItems: "center",
                gap: 15,
                background: "rgba(0,0,0,0.85)",
                borderRadius: 14,
                padding: "17px 24px",
                boxShadow: "inset 0 0 0 1px rgba(255,255,255,0.08)",
              }}
            >
              <IgGlyph size={38} />
              <span
                style={{
                  fontFamily: SANS,
                  fontWeight: 800,
                  fontSize: 35,
                  color: "#fff",
                  whiteSpace: "nowrap",
                }}
              >
                @thesoloentrepreneur.yt
              </span>
            </div>

            <div
              style={{
                marginTop: 26,
                opacity: arrowIn,
                transform: `translateX(${(1 - arrowIn) * -16}px)`,
                fontFamily: SANS,
                fontWeight: 700,
                fontSize: 30,
                letterSpacing: 6,
                color: INK,
              }}
            >
              WATCH THEM ALL →
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
