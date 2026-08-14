import React from "react";
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";

/**
 * Nick-style product-launch HOOK: brand mark + giant brand name on a clean
 * cream field, the tool's real screen in a floating window beneath it, one
 * italic serif line, and the facecam in a rounded bottom card. Display type
 * NEVER sits on footage here — the field is always light (FEEDBACK
 * 2026-07-29). Pair with hideCaptions: true in the beat.
 *
 * Motion contract (FEEDBACK 2026-08-04 astra v2→v3: "looks like a still
 * screen"): every band animates IN staggered, and something keeps moving for
 * the whole scene — mark rotation settle, window push-in + image pan, serif
 * word pops + underline sweep. A still image in the window must never read
 * as a freeze-frame.
 */
export interface BrandHookProps {
  /** giant brand/product name (the center of attraction) */
  title: string;
  /** small caps line under the title (e.g. product name) */
  subtitle?: string;
  /** official brand mark: svgl paths.json entries ({d} objects or d-strings) */
  logoPaths?: Array<string | { d: string }>;
  logoViewBox?: string;
  /** brand color for the animated mark (defaults to theme ink) */
  markColor?: string;
  /** media (video/image) shown in the floating dark window */
  mediaSrc: string;
  mediaFrom?: number;
  /** italic serif line between window and face (caps) */
  serifLine?: string;
  /** seconds into the scene when the serif line lands */
  serifAt?: number;
  /** facecam video for the rounded bottom card */
  bottomSrc: string;
  bottomFrom?: number;
  /** horizontal focus 0..1 for the facecam crop */
  bottomFocusX?: number;
}

const isVideo = (src: string) => /\.(mp4|webm|mov)$/i.test(src);

export const BrandHook: React.FC<BrandHookProps> = ({
  title,
  subtitle,
  logoPaths,
  logoViewBox = "0 0 256 260",
  markColor,
  mediaSrc,
  mediaFrom = 0,
  serifLine,
  serifAt = 0.55,
  bottomSrc,
  bottomFrom = 0,
  bottomFocusX = 0.5,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const theme = useTheme();

  const pop = (delay: number, dur = 14) =>
    spring({
      frame: frame - delay,
      fps,
      config: { damping: 16, stiffness: 160, mass: 0.6 },
      durationInFrames: dur,
    });

  const winIn = pop(6, 16);
  const faceIn = pop(9, 16);
  const subIn = pop(10, 12);

  const hasMark = !!(logoPaths && logoPaths.length > 0);

  // ── brand mark: draw-on stroke → fill, spin settling in, then slow drift
  const markIn = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 90, mass: 0.8 },
    durationInFrames: 22,
  });
  const draw = interpolate(frame, [0, 18], [1, 0], {
    extrapolateRight: "clamp",
  });
  const fillIn = interpolate(frame, [10, 22], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  // keeps rotating gently forever so the lockup never freezes
  const markSpin = -140 * (1 - markIn) + frame * 0.25;

  // ── title: per-letter staggered rise
  const letters = title.split("");
  const markSize = 132;
  const titleSize = hasMark ? 188 : 232;

  // ── serif line: word-by-word pops
  const words = (serifLine ?? "").split(" ");
  const serifBase = Math.round(serifAt * fps);
  const wordSpring = (i: number) =>
    spring({
      frame: frame - (serifBase + i * 4),
      fps,
      config: { damping: 13, stiffness: 200, mass: 0.5 },
      durationInFrames: 12,
    });
  const underline = interpolate(
    frame,
    [serifBase + words.length * 4 + 6, serifBase + words.length * 4 + 20],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // floating window geometry (16:9 media)
  const winW = width * 0.86;
  const winH = (winW * 9) / 16 + 34; // + title bar
  const winX = (width - winW) / 2;
  const winY = height * 0.215;
  // continuous push-in + slow pan so a still screenshot stays alive
  const winZoom = 1 + frame * 0.0006;
  const panY = interpolate(frame, [0, fps * 3], [18, 46], {
    extrapolateRight: "clamp",
  });

  // facecam card
  const cardTop = height * 0.565;
  const facePos = `${bottomFocusX * 100}% 24%`;

  return (
    <AbsoluteFill style={{ background: theme.cream }}>
      {/* subtle vignette texture so the field isn't flat */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(120% 90% at 50% 0%, rgba(255,255,255,0.65), rgba(0,0,0,0.05))",
        }}
      />

      {/* brand lockup: animated mark + per-letter title */}
      <div
        style={{
          position: "absolute",
          top: height * 0.038,
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 26,
        }}
      >
        {hasMark && (
          <svg
            viewBox={logoViewBox}
            width={markSize}
            height={markSize}
            style={{
              flex: "0 0 auto",
              opacity: markIn,
              transform: `rotate(${markSpin}deg) scale(${0.5 + 0.5 * markIn})`,
            }}
          >
            {logoPaths!.map((p, i) => {
              const d = typeof p === "string" ? p : p.d;
              return (
              <React.Fragment key={i}>
                <path
                  d={d}
                  fill="none"
                  stroke={markColor ?? theme.ink}
                  strokeWidth={5}
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={draw}
                />
                <path d={d} fill={markColor ?? theme.ink} opacity={fillIn} />
              </React.Fragment>
              );
            })}
          </svg>
        )}
        <div
          style={{
            fontFamily: theme.serif,
            fontWeight: 800,
            fontSize: titleSize,
            letterSpacing: "-0.02em",
            lineHeight: 1,
            color: theme.ink,
            whiteSpace: "pre",
          }}
        >
          {letters.map((ch, i) => {
            const s = spring({
              frame: frame - (2 + i * 2),
              fps,
              config: { damping: 14, stiffness: 190, mass: 0.55 },
              durationInFrames: 13,
            });
            return (
              <span
                key={i}
                style={{
                  display: "inline-block",
                  opacity: s,
                  transform: `translateY(${(1 - s) * 54}px)`,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>
      </div>
      {subtitle && (
        <div
          style={{
            position: "absolute",
            top: height * 0.038 + titleSize + 22,
            width: "100%",
            textAlign: "center",
            fontFamily: theme.sans,
            fontWeight: 700,
            fontSize: 44,
            letterSpacing: `${interpolate(subIn, [0, 1], [0.6, 0.24])}em`,
            textTransform: "uppercase",
            color: theme.muted,
            opacity: subIn,
          }}
        >
          {subtitle}
        </div>
      )}

      {/* floating product window */}
      <div
        style={{
          position: "absolute",
          left: winX,
          top: winY,
          width: winW,
          height: winH,
          borderRadius: 18,
          overflow: "hidden",
          background: "#161616",
          boxShadow: theme.shadow.card,
          opacity: winIn,
          transform: `translateY(${(1 - winIn) * 60}px) scale(${winZoom})`,
        }}
      >
        <div
          style={{
            height: 34,
            display: "flex",
            alignItems: "center",
            gap: 8,
            paddingLeft: 16,
            background: "#242424",
          }}
        >
          {["#ff5f57", "#febc2e", "#28c840"].map((c) => (
            <div
              key={c}
              style={{ width: 12, height: 12, borderRadius: 6, background: c }}
            />
          ))}
        </div>
        {isVideo(mediaSrc) ? (
          <OffthreadVideo
            src={staticFile(mediaSrc)}
            startFrom={Math.round(mediaFrom * fps)}
            muted
            style={{
              width: "100%",
              height: winH - 34,
              objectFit: "cover",
            }}
          />
        ) : (
          <Img
            src={staticFile(mediaSrc)}
            style={{
              width: "100%",
              height: winH - 34,
              objectFit: "cover",
              objectPosition: `50% ${panY}%`,
            }}
          />
        )}
      </div>

      {/* italic serif line — word pops + accent numbers + underline sweep */}
      {serifLine && (
        <div
          style={{
            position: "absolute",
            top: cardTop - 100,
            width: "100%",
            textAlign: "center",
            fontFamily: theme.serif,
            fontStyle: "italic",
            fontWeight: 800,
            fontSize: 74,
            letterSpacing: "0.01em",
            textTransform: "uppercase",
            color: theme.ink,
          }}
        >
          {words.map((w, i) => {
            const s = wordSpring(i);
            const accent = /[\d$]/.test(w);
            return (
              <span
                key={i}
                style={{
                  display: "inline-block",
                  marginRight: 18,
                  color: accent ? "#E8A200" : theme.ink,
                  opacity: s,
                  transform: `translateY(${(1 - s) * 30}px) scale(${
                    0.7 + 0.3 * s
                  })`,
                }}
              >
                {w}
              </span>
            );
          })}
          <div
            style={{
              margin: "10px auto 0",
              height: 7,
              width: `${underline * 46}%`,
              borderRadius: 4,
              background: theme.accent,
            }}
          />
        </div>
      )}

      {/* rounded facecam card */}
      <div
        style={{
          position: "absolute",
          left: 24,
          right: 24,
          top: cardTop,
          bottom: 0,
          borderRadius: "44px 44px 0 0",
          overflow: "hidden",
          boxShadow: "0 -18px 60px rgba(0,0,0,0.18)",
          opacity: faceIn,
          transform: `translateY(${(1 - faceIn) * 80}px)`,
        }}
      >
        <OffthreadVideo
          src={staticFile(bottomSrc)}
          startFrom={Math.round(bottomFrom * fps)}
          muted
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: facePos,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
