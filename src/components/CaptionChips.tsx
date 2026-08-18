import React from "react";
import { SPRING, DUR } from "../theme/motion";
import { TYPE, SIZE } from "../theme/type";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Easing,
} from "remotion";
import { useTheme } from "../theme/tokens";
import type { CaptionWord } from "../types";

/** Split chip text into plain/emphasized runs based on the emphasis list. */
const tokenize = (
  text: string,
  emphasis: string[]
): { text: string; emph: boolean }[] => {
  if (!emphasis.length) return [{ text, emph: false }];
  const pattern = emphasis
    .map((e) => e.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
    .join("|");
  const re = new RegExp(`(${pattern})`, "gi");
  return text
    .split(re)
    .filter((s) => s.length > 0)
    .map((s) => ({
      text: s,
      emph: emphasis.some((e) => e.toLowerCase() === s.toLowerCase()),
    }));
};

/**
 * Word-synced caption chips, Varun-sized: large bold white on black pill,
 * key tokens (numbers, prices, names) pop in accent yellow and bigger.
 */
const isEmph = (word: string, emphasis: string[]) => {
  const clean = word.replace(/[^\w$%+.'-]/g, "").toLowerCase();
  return emphasis.some((e) => {
    const el = e.toLowerCase();
    return el === clean || (el.includes(" ") && el.split(" ").includes(clean));
  });
};

/**
 * "word-reveal" caption (formerly "nick-display"): measured from the 12
 * reels (2026-07-30 teardown). Big free-floating text, NO pill: connective
 * words in italic, the KEY word (emphasis list) lands heavier + bigger +
 * accent-colored. Words accumulate as spoken (per-word reveal). Deep soft
 * drop shadow carries legibility; `themes` ranges flip white↔ink so text
 * never blends with cream card fields. (SF Pro only — the italic voice is
 * SF Pro Italic, not a serif, per the 2026-07-29 brand font rule.)
 */
const NickDisplay: React.FC<{
  active: CaptionWord;
  emphasis: string[];
  bottom: number;
  dark: boolean;
  accent: string;
  fps: number;
  frame: number;
}> = ({ active, emphasis, bottom, dark, accent, fps, frame }) => {
  const t = frame / fps;
  const words = active.words ?? [{ t: active.start, text: active.text }];
  const base = dark ? "#141414" : "#ffffff";
  const shadow = dark
    ? "0 3px 10px rgba(0,0,0,0.22), 0 1px 3px rgba(0,0,0,0.18)"
    : "0 4px 16px rgba(0,0,0,0.85), 0 1px 3px rgba(0,0,0,0.6)";
  return (
    <div
      style={{
        position: "absolute",
        left: 40,
        right: 40,
        bottom,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        columnGap: 20,
        rowGap: 2,
        pointerEvents: "none",
      }}
    >
      {words.map((w, i) => {
        if (t < w.t - 0.02) return null;
        const local = frame - Math.round(w.t * fps);
        const pop = spring({
          frame: local,
          fps,
          config: { damping: 14, stiffness: 320, mass: 0.4 },
          durationInFrames: DUR.quick,
        });
        const emph = isEmph(w.text, emphasis);
        return (
          <span
            key={i}
            style={{
              // ONE scale: the caption role, with emphasis a step up. 66/86
              // were the proven pair; the scale keeps that relationship at
              // 78 and 78*1.3.
              ...TYPE.caption,
              fontStyle: emph ? "normal" : "italic",
              fontWeight: emph ? 900 : TYPE.caption.fontWeight,
              fontSize: emph ? Math.round(SIZE.caption * 1.3) : SIZE.caption,
              letterSpacing: emph ? "-0.015em" : "0.005em",
              color: emph ? accent : base,
              textShadow: shadow,
              opacity: pop,
              transform: `translateY(${(1 - pop) * 14}px) scale(${
                0.9 + 0.1 * pop
              })`,
              display: "inline-block",
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};

/**
 * "ink-circle" caption — measured 2026-08-14 from the reference reel the user
 * supplied (instagram.com/reels/Db_Xf3tAuzH).
 *
 * MEASURED, not eyeballed: near-black sentence-case text sitting at ~0.65 of
 * frame height, ONE accent word in coral (#d86c48 sampled off the frame), and
 * a hand-drawn ellipse looping that word — irregular, and overshooting where
 * the stroke crosses itself, like a real marker.
 *
 * It differs from `word-reveal` on every axis: ink instead of white, sentence
 * case instead of caps, upright instead of italic, and the line BUILDS word by
 * word and stays up rather than replacing itself. Use it on light grounds.
 */
const InkCircle: React.FC<{
  active: CaptionWord;
  emphasis: string[];
  bottom: number;
  accent: string;
  fps: number;
  frame: number;
}> = ({ active, emphasis, bottom, accent, fps, frame }) => {
  const t = frame / fps;
  // words appear one at a time and STAY — the sentence assembles
  const words =
    active.words && active.words.length
      ? active.words
      : active.text.split(/\s+/).filter(Boolean).map((w, i, a) => ({
          text: w,
          t:
            active.start +
            ((active.end - active.start) * i) / Math.max(a.length, 1),
        }));

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "baseline",
        gap: "0 0.30em",
        padding: "0 78px",
        fontFamily:
          "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
        ...TYPE.caption,
        letterSpacing: "-0.015em",
        lineHeight: 1.22,
        color: "#111417",
      }}
    >
      {words.map((w, i) => {
        const appeared = t >= w.t;
        if (!appeared) return null;
        const local = Math.max(0, t - w.t);
        const rise = interpolate(local, [0, 0.16], [10, 0], {
          extrapolateRight: "clamp",
          easing: Easing.out(Easing.cubic),
        });
        const fade = interpolate(local, [0, 0.14], [0, 1], {
          extrapolateRight: "clamp",
        });
        const key = w.text.toLowerCase().replace(/[^a-z0-9$%.+-]/g, "");
        const emph = emphasis.some((e) => e.toLowerCase() === key);
        return (
          <span
            key={i}
            style={{
              position: "relative",
              display: "inline-block",
              transform: `translateY(${rise}px)`,
              opacity: fade,
              color: emph ? accent : "#111417",
              padding: emph ? "0 .12em" : undefined,
            }}
          >
            {w.text}
            {emph && <HandCircle accent={accent} draw={local} />}
          </span>
        );
      })}
    </div>
  );
};

/** A marker loop that draws on, overshoots, and crosses itself. */
const HandCircle: React.FC<{ accent: string; draw: number }> = ({
  accent,
  draw,
}) => {
  const p = interpolate(draw, [0.08, 0.52], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const LEN = 340;
  return (
    <svg
      viewBox="0 0 120 60"
      preserveAspectRatio="none"
      style={{
        position: "absolute",
        left: "-9%",
        top: "-16%",
        width: "118%",
        height: "132%",
        overflow: "visible",
        pointerEvents: "none",
      }}
    >
      <path
        d="M104 22 C104 8 78 3 58 4 C30 5 12 14 13 29 C14 44 40 55 66 54
           C90 53 108 44 106 30 C104 18 84 10 58 10"
        fill="none"
        stroke={accent}
        strokeWidth={3.4}
        strokeLinecap="round"
        vectorEffect="non-scaling-stroke"
        style={{ strokeDasharray: LEN, strokeDashoffset: LEN * (1 - p) }}
      />
    </svg>
  );
};

export const CaptionChips: React.FC<{
  captions: CaptionWord[];
  mode?:
    | "word-reveal"
    | "ink-circle"
    | "nick-display"
    | "sans"
    | "mono"
    | "chip-small"
    | "chip-lg";
  emphasis?: string[];
  /** time-ranged bottom offsets so chips never cover a face */
  positions?: { start: number; end: number; bottom: number }[];
  /** time ranges where chips are suppressed (display-type scenes own the text) */
  hidden?: { start: number; end: number }[];
  /** time ranges where the caption text theme is dark (ink on light fields) */
  darkRanges?: { start: number; end: number }[];
}> = ({
  captions,
  mode = "sans",
  emphasis = [],
  positions = [],
  hidden = [],
  darkRanges = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const theme = useTheme();
  const ACCENT = theme.accent;
  const t = frame / fps;

  if (hidden.some((h) => t >= h.start && t < h.end)) return null;

  const active = captions.find((c) => t >= c.start && t < c.end);
  if (!active) return null;

  if (mode === "ink-circle") {
    return (
      <InkCircle
        active={active}
        emphasis={emphasis}
        bottom={positions.find((p) => t >= p.start && t < p.end)?.bottom ?? 672}
        accent="#d86c48"
        fps={fps}
        frame={frame}
      />
    );
  }

  // "nick-display" is the pre-2026-08-16 name for "word-reveal"; the seven
  // already-published beat sheets still carry it.
  if (mode === "word-reveal" || mode === "nick-display") {
    const dark = darkRanges.some((r) => t >= r.start && t < r.end);
    return (
      <NickDisplay
        active={active}
        emphasis={emphasis}
        bottom={positions.find((p) => t >= p.start && t < p.end)?.bottom ?? 400}
        dark={dark}
        accent={dark ? "#E8A200" : ACCENT}
        fps={fps}
        frame={frame}
      />
    );
  }

  const localFrame = frame - Math.round(active.start * fps);
  const pop = spring({
    frame: localFrame,
    fps,
    config: { damping: 13, stiffness: 300, mass: 0.35 },
    durationInFrames: DUR.quick,
  });
  const scale = 0.88 + 0.12 * pop;

  const font =
    mode === "chip-lg"
      ? {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 50,
          fontWeight: 800 as const,
          letterSpacing: "-0.01em",
        }
      : mode === "chip-small"
      ? {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 38,
          fontWeight: 700 as const,
        }
      : mode === "mono"
      ? {
          fontFamily: "'Menlo', 'Courier New', monospace",
          textTransform: "uppercase" as const,
          fontSize: 48,
          letterSpacing: "0.02em",
          fontWeight: 700 as const,
        }
      : {
          fontFamily:
            "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
          fontSize: 56,
          fontWeight: 800 as const,
        };

  const runs = tokenize(active.text, emphasis);
  const hasEmph = runs.some((r) => r.emph);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: positions.find((p) => t >= p.start && t < p.end)?.bottom ?? 400,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          ...font,
          color: "white",
          background:
            mode === "chip-small"
              ? "rgba(0,0,0,0.55)"
              : mode === "chip-lg"
              ? "rgba(0,0,0,0.82)"
              : "rgba(0,0,0,0.94)",
          padding:
            mode === "chip-small"
              ? "9px 20px"
              : mode === "chip-lg"
              ? "13px 26px"
              : "14px 30px",
          borderRadius: mode === "chip-small" ? 9 : mode === "chip-lg" ? 12 : 14,
          transform: `scale(${hasEmph ? scale * 1.04 : scale})`,
          maxWidth: 940,
          textAlign: "center",
          lineHeight: 1.18,
          boxShadow:
            mode === "chip-lg"
              ? "0 6px 26px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(255,255,255,0.08)"
              : "0 4px 22px rgba(0,0,0,0.45)",
        }}
      >
        {runs.map((r, i) =>
          r.emph ? (
            <span
              key={i}
              style={{
                color: ACCENT,
                fontSize: "1.22em",
                fontWeight: 900,
                textShadow: `0 0 22px ${ACCENT}73`,
              }}
            >
              {r.text}
            </span>
          ) : (
            <span key={i}>{r.text}</span>
          )
        )}
      </div>
    </div>
  );
};
