import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Headline } from "../types";
import { SAFE_RECT } from "../platformSafeArea";

const SANS = "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";
const ACCENT = "#d97757"; // Anthropic clay

/**
 * The headline treatment for text laid over footage.
 *
 * REBUILT 2026-08-17 after three defects were found in one rendered frame
 * (iphone-fold-ultra scene 09, "UNFOLDED / 7.76″ / reported · MacRumors"):
 *
 * 1. INK COLLISION. `lineHeight: 1.02` makes the line BOX shorter than the
 *    glyphs it contains, and a flex `gap` measures boxes, not ink — so the
 *    subtitle's ascenders sat on top of the numerals. It looked like a
 *    mid-animation artefact; it was permanent, on every three-line headline.
 *    Line height is now >= 1.12 and the gap scales with the largest type.
 *
 * 2. UNREADABLE ACCENT. Clay #d97757 was chosen against cream. Over a warm
 *    orange wallpaper it nearly vanished, and a drop-shadow cannot rescue a
 *    colour that matches its background in hue AND value. There is now a scrim
 *    behind the block, sized to the text, so the type always has its own ground.
 *
 * 3. FROZEN. The only motion was a 14-frame entrance per line, after which the
 *    frame was static — the "flat" the user kept reporting. Lines now keep a
 *    slow drift, and an accent line gets a bar that draws under it.
 *
 * It also CLAMPS y into the platform safe band rather than trusting the beat
 * sheet: a headline at y 0.07 renders under Instagram's own header, and that is
 * a structural fact about Reels, not a matter of taste. Composition inside the
 * band stays the author's call.
 */
export const HeadlineBuild: React.FC<{ spec: Headline }> = ({ spec }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const t = frame / fps;
  const align = spec.align ?? "center";
  const dark = spec.theme === "dark";
  const ink = dark ? "#0f0f0f" : "#ffffff";
  const rgb = dark ? "15,15,15" : "255,255,255";

  const sizeFor = (kind: string) =>
    kind === "label" ? 46 : kind === "subtitle" ? 52 : 100;

  const styleFor = (kind: string): React.CSSProperties => {
    const fontSize = sizeFor(kind);
    if (kind === "label")
      return {
        fontFamily: SANS, fontWeight: 700, fontSize, letterSpacing: 2,
        textTransform: "uppercase" as const, lineHeight: 1.16,
      };
    if (kind === "subtitle")
      return {
        fontFamily: SANS, fontStyle: "italic", fontWeight: 700, fontSize,
        opacity: 0.95, lineHeight: 1.2,
      };
    // 1.12, never 1.02: below ~1.1 the ink overflows its own box and the flex
    // gap — which measures boxes — stops keeping lines apart.
    return {
      fontFamily: SANS, fontWeight: 800, fontSize, lineHeight: 1.12,
      letterSpacing: -1.5,
    };
  };

  const biggest = Math.max(...spec.lines.map((l) => sizeFor(l.kind)), 46);
  const gap = Math.round(biggest * 0.14);

  // Rough block height, to keep the whole thing inside the safe band rather
  // than only its anchor point.
  const blockH = spec.lines.reduce(
    (h, l) => h + sizeFor(l.kind) * 1.2, 0) + gap * (spec.lines.length - 1);
  const halfFrac = blockH / 2 / height;
  const yWanted = spec.y ?? 0.5;
  const y = Math.min(
    Math.max(yWanted, SAFE_RECT.y0 + halfFrac),
    SAFE_RECT.y1 - halfFrac,
  );

  // Never frozen: a slow drift that continues for the whole scene. Small enough
  // to read as life rather than movement.
  const drift = interpolate(t, [0, 6], [0, -10], { extrapolateRight: "clamp" });
  const breathe = 1 + 0.012 * Math.sin(t * 0.9);

  const firstAt = Math.min(...spec.lines.map((l) => l.at));
  const scrim = interpolate(t, [firstAt, firstAt + 0.45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: align === "center" ? "center" : "flex-start",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: `${y * 100}%`,
          transform: `translateY(-50%) translateY(${drift}px) scale(${breathe})`,
          width: "100%",
          padding: align === "center" ? "0 70px" : "0 84px",
          textAlign: align,
          display: "flex",
          flexDirection: "column",
          alignItems: align === "center" ? "center" : "flex-start",
          gap,
        }}
      >
        {/* Its own ground. A drop-shadow cannot save type whose colour matches
            the footage in both hue and value, which is what happened to the
            clay accent over an orange wallpaper. */}
        {!dark && (
          <div
            style={{
              position: "absolute",
              // Reaches well past the text so the falloff happens off the type,
              // not across it. A scrim clipped tight to the text block reads as
              // a translucent RECTANGLE with hard edges — which is what the
              // first attempt produced.
              left: -120,
              right: -120,
              top: -gap * 5,
              bottom: -gap * 5,
              background:
                "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.46) 26%, rgba(0,0,0,0.5) 74%, rgba(0,0,0,0) 100%)",
              opacity: scrim,
              pointerEvents: "none",
            }}
          />
        )}

        {spec.lines.map((ln, i) => {
          const en = spring({
            frame: frame - Math.round(ln.at * fps),
            fps,
            config: { damping: 18, stiffness: 150 },
            durationInFrames: 14,
          });
          const reveal = interpolate(t, [ln.at, ln.at + 0.5], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const isHead = ln.kind === "headline";
          const a = 0.34 + 0.66 * reveal;
          const color = ln.accent ? ACCENT : isHead ? `rgba(${rgb},${a})` : ink;
          // An accent line earns a bar that draws under it — the emphasis the
          // treatment was missing, frame-driven so it actually renders.
          const bar = ln.accent
            ? interpolate(t, [ln.at + 0.18, ln.at + 0.62], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            : 0;
          return (
            <div
              key={i}
              style={{
                position: "relative",
                opacity: en,
                transform: `translateY(${(1 - en) * 26}px)`,
              }}
            >
              <div
                style={{
                  ...styleFor(ln.kind),
                  color,
                  whiteSpace: "pre-line",
                  textShadow: dark
                    ? "none"
                    : "0 3px 18px rgba(0,0,0,0.75), 0 1px 3px rgba(0,0,0,0.6)",
                }}
              >
                {ln.text}
              </div>
              {bar > 0 && (
                <div
                  style={{
                    height: Math.max(5, sizeFor(ln.kind) * 0.055),
                    width: `${bar * 100}%`,
                    marginTop: Math.round(sizeFor(ln.kind) * 0.06),
                    marginLeft: align === "center" ? `${(1 - bar) * 50}%` : 0,
                    background: ACCENT,
                    borderRadius: 999,
                    boxShadow: `0 2px 14px ${ACCENT}88`,
                  }}
                />
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
