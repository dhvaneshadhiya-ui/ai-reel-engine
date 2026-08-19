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
 *   DISPLAY (Space Grotesk)  display, hero, lead — the thing being said.
 *                     Loaded by theme/fonts.tsx.
 *   SANS (SF Pro)     label, body, micro, caption — anything read at speed or
 *                     scanned as data. A caption is read in under a second and
 *                     wants no personality at all.
 *
 * WHY NOT A SERIF ANY MORE (2026-08-18). The display voice was Fraunces, a
 * magazine serif, and the user's note was exact: "Font style represents the
 * theme of our video, like our niche is tech." Fraunces is the right face for
 * an essay and the wrong one for hardware news — it reads Sunday-supplement,
 * not product. Space Grotesk is a geometric grotesk with deliberate quirks in
 * its R, G and question mark; it is the face the dev-tool and hardware world
 * actually uses, and at headline size on a phone it is wider and heavier than
 * Fraunces, so it holds up better at a glance.
 *
 * It is a SANS, which means the old SERIF/SANS split no longer describes
 * anything: both voices are sans now, separated by CHARACTER rather than by
 * category. The token is named DISPLAY because that is its job. The name SERIF
 * survives only as a deprecated alias so a missed import cannot silently fall
 * through to Georgia — the exact failure documented in theme/fonts.tsx.
 *
 * Fraunces stays in public/fonts. A future style pack aimed at a different
 * niche may well want it back; deleting it would make that a download instead
 * of a one-line change.
 *
 * WEIGHTS collapse from seven to four: 400/600 on the serif, 700/800 on the sans.
 * A 650 next to a 700 is a decision nobody made on purpose.
 */

/** The display voice. One constant; nothing may name a face directly. */
export const DISPLAY = "'Space Grotesk', 'Archivo', 'Helvetica Neue', sans-serif";
/** @deprecated name only — points at DISPLAY. Kept so no import falls to Georgia. */
export const SERIF = DISPLAY;
export const SANS =
  "-apple-system, 'SF Pro Display', 'Helvetica Neue', Inter, sans-serif";
export const MONO = "ui-monospace, 'SF Mono', Menlo, monospace";

/** The only sizes any component may use. */
export const SIZE = {
  /**
   * nano 22 — a sub-label inside a dense row.
   *
   * NOT INVENTED. Added 2026-08-18 the same way the motion system's fifth
   * spring role was: by measuring what people had already written when the
   * system could not express what they needed. Three components independently
   * reached below micro for secondary text — ToolStack's tagline at 19,
   * ChartScene's row sub at 19/21 and its source line at 22 — because the
   * scale stopped at micro 28 and a tagline set at 28 under a 28px name is not
   * a sub-label, it is a second title.
   *
   * 22 is both the scale's own next step down (28 / 1.3 = 21.5) and inside the
   * observed cluster, so it satisfies the ratio and the practice at once. A
   * system that cannot express what is already being written is a preference,
   * not a system.
   */
  nano: 22,
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
  nano: {
    fontFamily: SANS,
    fontSize: SIZE.nano,
    // 600, not the 650 and 500 the three sites were using. A 650 beside a 700
    // is a decision nobody made on purpose — the same finding that collapsed
    // seven weights to four.
    fontWeight: 600,
    letterSpacing: 0.1,
    lineHeight: 1.25,
  },
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
