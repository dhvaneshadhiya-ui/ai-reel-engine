import type { CSSProperties } from "react";

/**
 * ONE type system for every component.
 *
 * WHY
 * ---
 * Measured 2026-08-18: 41 distinct font sizes and 7 weights across 38
 * components — 17, 19, 20, 22, 24, 26, 27, 28, 30, 32, 33, 34, 36, 38, 40, 42,
 * 44, 46, 48, 50, 52, 54, 56, 58, 60, 66, 72, 74, 76, 78... Sizes one and two
 * pixels apart that nobody can tell apart, which means they were not chosen,
 * they accumulated. Every component picked its own type in isolation, so the
 * reels have no typographic identity — only local decisions that happen to sit
 * next to each other.
 *
 * THE SCALE keeps the values that are already PROVEN in shipped reels and rounds
 * the rest onto a 1.3 ratio: credit 27 -> micro 28, spec row 44/46 -> body 46,
 * headline 100 -> display 100, stat 118 -> hero 130.
 *
 *   micro    28   credit, footnote, source line
 *   label    36   eyebrow, uppercase, letterspaced
 *   body     46   spec rows, list items, table cells
 *   lead     60   subtitle, the line under a claim
 *   caption  78   the spoken word, burned in
 *   display 100   the claim itself
 *   hero    130   a number that IS the beat
 *
 * THE TWO VOICES, and which gets which:
 *   SERIF (Fraunces)  display, hero, lead — the editorial voice, the thing being
 *                     said. Loaded by theme/fonts.tsx.
 *   SANS (SF Pro)     label, body, micro, caption — anything read at speed or
 *                     scanned as data. A caption is read in under a second and
 *                     wants no personality at all.
 *
 * WEIGHTS collapse from seven to four: 400/600 on the serif, 700/800 on the sans.
 * A 650 next to a 700 is a decision nobody made on purpose.
 */

export const SERIF = "Fraunces, Georgia, serif";
export const SANS =
  "-apple-system, 'SF Pro Display', 'Helvetica Neue', Inter, sans-serif";
export const MONO = "ui-monospace, 'SF Mono', Menlo, monospace";

/** The only sizes any component may use. */
export const SIZE = {
  micro: 28,
  label: 36,
  body: 46,
  lead: 60,
  caption: 78,
  display: 100,
  hero: 130,
} as const;

export type TypeRole = keyof typeof SIZE;

/**
 * A complete treatment per role. Components spread these rather than assembling
 * font properties themselves — that assembling is how 41 sizes happened.
 */
export const TYPE: Record<TypeRole, CSSProperties> = {
  micro: {
    fontFamily: SANS,
    fontSize: SIZE.micro,
    fontWeight: 600,
    letterSpacing: 0.2,
    lineHeight: 1.3,
  },
  label: {
    fontFamily: SANS,
    fontSize: SIZE.label,
    fontWeight: 700,
    letterSpacing: 2,
    textTransform: "uppercase",
    lineHeight: 1.16,
  },
  body: {
    fontFamily: SANS,
    fontSize: SIZE.body,
    fontWeight: 700,
    letterSpacing: -0.2,
    lineHeight: 1.28,
  },
  lead: {
    fontFamily: SERIF,
    fontSize: SIZE.lead,
    fontWeight: 600,
    fontStyle: "italic",
    lineHeight: 1.2,
  },
  caption: {
    // SANS on purpose. A caption is read in under a second, often on mute, and
    // wants legibility rather than personality.
    fontFamily: SANS,
    fontSize: SIZE.caption,
    fontWeight: 800,
    letterSpacing: -0.5,
    lineHeight: 1.1,
  },
  display: {
    fontFamily: SERIF,
    fontSize: SIZE.display,
    fontWeight: 700,
    letterSpacing: -1.5,
    // never below ~1.1: the ink overflows its own box and a flex gap, which
    // measures boxes, stops keeping lines apart (found on iphone-fold-ultra 09)
    lineHeight: 1.12,
  },
  hero: {
    fontFamily: SERIF,
    fontSize: SIZE.hero,
    fontWeight: 700,
    letterSpacing: -2.5,
    lineHeight: 1.0,
    // a number that changes must not jitter as its digits change width
    fontVariantNumeric: "tabular-nums",
  },
};

/** Scale a role for a scene that genuinely needs more or less. */
export const typeAt = (role: TypeRole, scale: number): CSSProperties => ({
  ...TYPE[role],
  fontSize: Math.round(SIZE[role] * scale),
});
