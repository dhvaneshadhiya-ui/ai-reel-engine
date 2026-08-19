import React from "react";
import { SPRING, DUR, slideFor } from "../theme/motion";
import { TYPE, SIZE, MONO, typeAt } from "../theme/type";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Easing,
} from "remotion";
import { useTheme } from "../theme/tokens";
import { clampCaptionBottom } from "../platformSafeArea";
import type { CaptionWord } from "../types";

/**
 * power4.out — the whip ease waterfall-entry.md specifies for an arrival.
 * Remotion renders nothing that is not frame-driven, so GSAP's named ease is
 * reimplemented rather than imported.
 */
const easeOutQuart = (x: number): number => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 4);

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
  /** the measured ground is BRIGHT — white ink needs help to survive it */
  bright: boolean;
  accent: string;
  fps: number;
  frame: number;
}> = ({ active, emphasis, bottom, bright, accent, fps, frame }) => {
  const t = frame / fps;
  const words = active.words ?? [{ t: active.start, text: active.text }];

  // ONE INK FOR THE WHOLE REEL. `dark` used to flip the caption to #141414
  // wherever the footage was bright — and tools/auto_contrast.py now measures
  // that as 17 of the 33 caption scenes in iphone-fold-ultra. A caption that
  // changes colour seventeen times in eighty seconds does not read as adaptive,
  // it reads as broken. So the measurement drives the caption's GROUND instead:
  // white always, and over a bright frame it gets a contour — a tight dark ring
  // in eight directions plus a deeper drop — which is the treatment every
  // platform's own captions use, and the reason they survive any footage.
  const base = "#ffffff";

  /**
   * KARAOKE ENVELOPE — hyperframes-animation rules/asr-keyword-glow.md, the
   * variation that rule marks "RECOMMENDED for video narration", with its
   * stated reason: the subtle default "reads too subtle in video: inactive
   * words still dominate".
   *
   * That was exactly this component's state. Every revealed word sat at full
   * white, so a line of six words was six equal claims and the eye had nowhere
   * to go — flat, in the way the user kept reporting, even after the type and
   * motion systems landed.
   *
   * Attack -> sustain -> release -> REST, never back to zero. The rule is
   * explicit that the envelope "decays to a rest level, leaving a breadcrumb of
   * recent emphasis" — a word that fully extinguishes makes the line flicker;
   * one that rests at 0.55 keeps the sentence readable while the live word owns
   * the frame. At any instant one or two words are bright.
   *
   * Word ends come from the NEXT word's onset — whisper gives us onsets, and a
   * word is being spoken until the next one starts. No hand-typed windows.
   */
  const ATTACK = 0.07;
  const RELEASE = 0.20;
  const REST = 0.55;
  const envelopeAt = (i: number): number => {
    const start = words[i].t;
    const end = i + 1 < words.length ? words[i + 1].t : active.end;
    if (t < start) return 0;
    if (t < end) return Math.min((t - start) / ATTACK, 1);
    const releaseEnd = end + RELEASE;
    if (t < releaseEnd) return 1 - ((t - end) / RELEASE) * (1 - REST);
    return REST;
  };

  const RING = 2.2;
  const ring = bright
    ? Array.from({ length: 8 }, (_, k) => {
        const a = (k * Math.PI) / 4;
        return `${(Math.cos(a) * RING).toFixed(1)}px ${(
          Math.sin(a) * RING
        ).toFixed(1)}px 0 rgba(10,10,12,0.92)`;
      }).join(", ") + ", 0 6px 22px rgba(0,0,0,0.55)"
    : "0 4px 16px rgba(0,0,0,0.85), 0 1px 3px rgba(0,0,0,0.6)";
  const shadow = ring;
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
        const emph = isEmph(w.text, emphasis);
        // WEIGHT, NOT INDEX — hyperframes-animation rules/waterfall-entry.md.
        // Its table sets travel and settle time by what an element WEIGHS:
        // anchor 60-80px over 0.16-0.20s, normal 40-50px over 0.13-0.16s,
        // light 30-48px over 0.10-0.13s. This used to be slideFor(i, 34), a
        // decay on POSITION IN THE LINE — so the emphasis word got a small hop
        // purely for arriving late, and a throwaway "the" got the big one for
        // arriving first. Weight is the thing the eye actually reads.
        const heavy = emph || w.text.replace(/\W/g, "").length >= 7;
        const light = w.text.replace(/\W/g, "").length <= 3;
        const rise = heavy ? 72 : light ? 34 : 46;
        const settle = heavy ? 0.19 : light ? 0.12 : 0.15;
        // power4.out, never a spring and never .inOut on an entry — same rule.
        // A spring's overshoot is a SETTLE; this is a WHIP, and the difference
        // is what separates kinetic from bouncy.
        const p = easeOutQuart(Math.min(1, (t - w.t) / settle));
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
              // BINARY, never a fade. waterfall-entry.md states it as a rule
              // with no exception: "Opacity is BINARY 0->1 via tl.set — never
              // fade an arrival." A word that fades in is a word arriving
              // slowly; the MOTION is what should carry the arrival. This was
              // `opacity: pop * 1.35` — a ramp on every single word.
              opacity: 1,
              // The karaoke envelope rides on top of the arrival: the live word
              // is full white and a touch larger, spoken words rest dim.
              filter: `brightness(${0.62 + 0.38 * envelopeAt(i)})`,
              transform: `translateY(${(1 - p) * rise}px) scale(${
                (0.94 + 0.06 * p) * (1 + 0.05 * envelopeAt(i))
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
  const { fps, height } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;

  if (hidden.some((h) => t >= h.start && t < h.end)) return null;

  const active = captions.find((c) => t >= c.start && t < c.end);
  if (!active) return null;

  // `darkRanges` is named for the ink it used to force; what the range actually
  // marks is a BRIGHT ground (tools/auto_contrast.py sets captionTheme:"dark"
  // where it measures luminance > 0.55). Reading it as what it measures.
  const brightGround = darkRanges.some((r) => t >= r.start && t < r.end);
  // ONE accent decision for every caption mode, from the theme and the measured
  // ground — not three hardcoded hexes (#d86c48 / #E8A200 / theme.accent) that
  // happened to sit in three branches of the same component.
  const ACCENT = brightGround ? theme.accentInk : theme.accentOnDark;
  // Authors raise captions to clear a face; nothing may sink one into the
  // credit lane or Instagram's account row. See platformSafeArea.
  const bottomAt = (fallback: number) =>
    clampCaptionBottom(
      positions.find((p) => t >= p.start && t < p.end)?.bottom ?? fallback,
      height
    );

  if (mode === "ink-circle") {
    return (
      <InkCircle
        active={active}
        emphasis={emphasis}
        bottom={bottomAt(672)}
        accent={ACCENT}
        fps={fps}
        frame={frame}
      />
    );
  }

  // "nick-display" is the pre-2026-08-16 name for "word-reveal"; the seven
  // already-published beat sheets still carry it.
  if (mode === "word-reveal" || mode === "nick-display") {
    return (
      <NickDisplay
        active={active}
        emphasis={emphasis}
        bottom={bottomAt(560)}
        bright={brightGround}
        accent={theme.accentOnDark}
        fps={fps}
        frame={frame}
      />
    );
  }

  const localFrame = frame - Math.round(active.start * fps);
  const pop = spring({
    frame: localFrame,
    fps,
    config: SPRING.pop,
    durationInFrames: DUR.quick,
  });
  const scale = 0.88 + 0.12 * pop;

  // ON THE SCALE. These four modes carried 50 / 38 / 48 / 56 and re-declared the
  // SF Pro stack four times — the exact sprawl theme/type.ts was built to end,
  // in the one component that is on screen for the whole reel. A chip is the
  // caption voice at a smaller size, so it scales the caption role rather than
  // inventing sizes: chip-lg 0.64, mono 0.6, chip-small 0.46 of caption.
  const font =
    mode === "chip-lg"
      ? { ...typeAt("caption", 0.64), letterSpacing: "-0.01em" }
      : mode === "chip-small"
      ? { ...typeAt("caption", 0.46), fontWeight: 700 as const }
      : mode === "mono"
      ? {
          ...typeAt("caption", 0.6),
          fontFamily: MONO,
          textTransform: "uppercase" as const,
          letterSpacing: "0.02em",
          fontWeight: 700 as const,
        }
      : typeAt("caption", 0.72);

  const runs = tokenize(active.text, emphasis);
  const hasEmph = runs.some((r) => r.emph);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: bottomAt(560),
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
