import React from "react";
import { TINT } from "../theme/palette";
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
import { useTheme, THEMES } from "../theme/tokens";

type CascadeProps = Extract<Scene, { type: "wordcascade" }>;

const BGS: Record<string, string> = {
  cream: TINT.sand,
  black: "#0c0c0c",
  white: "#ffffff",
};

/**
 * The accent pair used to live here as two hand-picked hexes — #C2410C "warm
 * ink, reads on cream" and #FFD84D — the same shape of decision that put
 * `const ACCENT = "#d97757"` at the top of HeadlineBuild and shipped an orange
 * the user did not want (2026-08-18). Both are now derived from the style
 * pack's ONE declared accent; see theme/tokens.ts accentPair().
 */
/**
 * Is this field dark enough that light type is the readable choice?
 * Relative luminance off the resolved colour; anything we cannot parse is
 * treated as light, which is the safe direction — dark ink on an unknown
 * field is legible far more often than light ink on one.
 */
const isDarkField = (colour: string): boolean => {
  const hex = colour.trim().replace(/^#/, "");
  const full =
    hex.length === 3 ? hex.split("").map((c) => c + c).join("") : hex;
  if (!/^[0-9a-f]{6}$/i.test(full)) return false;
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(full.slice(i, i + 2), 16) / 255);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.5;
};

const wordStyle = (
  style: string,
  dark: boolean,
  size: number,
  accent = false,
  theme = THEMES.editorial
): React.CSSProperties => {
  const base: React.CSSProperties = {
    lineHeight: 1.08,
    color: accent
      ? (dark ? theme.accentInk : theme.accentOnDark)
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
        // the accent to its own lighter sibling and back — a gradient built
        // from the palette rather than three clay stops from outside it
        backgroundImage: `linear-gradient(135deg, ${theme.accentInk}, ${theme.accent}, ${theme.accentInk})`,
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
  const theme = useTheme();
  /**
   * RESOLVE THE BACKGROUND, THEN DERIVE THE POLARITY FROM WHAT WE RESOLVED
   * (2026-09-01). This was `BGS[scene.bg ?? "cream"]` with `dark` computed as
   * `scene.bg !== "black"`, and the two disagreed the moment `bg` was anything
   * BGS does not name. A scene authored with `bg: "#0b0d10"` — a perfectly
   * reasonable thing to write — resolved the background to `undefined` AND set
   * dark=true, so the words rendered #111111 on a transparent field: near-black
   * on black, invisible, with nothing in any log to say so. Proven by rendering
   * the four cases side by side, not by reading the code.
   *
   * So: accept a literal colour as well as a named one, and read the polarity
   * off the resolved value's luminance. An unnamed background can now be wrong
   * about taste, but it can no longer be invisible.
   */
  const rawBg = scene.bg ?? "cream";
  const bg = BGS[rawBg] ?? (/^#|^rgb|^hsl/i.test(rawBg) ? rawBg : BGS.cream);
  const dark = !isDarkField(bg);
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
              ...wordStyle(w.style, dark, w.size ?? 1, (w as {accent?: boolean}).accent ?? false, theme),
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
