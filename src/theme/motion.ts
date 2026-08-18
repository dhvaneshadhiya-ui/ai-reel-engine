/**
 * ONE motion system, the companion to theme/type.ts.
 *
 * WHY
 * ---
 * Measured 2026-08-18: 10 distinct damping values, 16 stiffness values and 12
 * entrance durations across the components. Damping 17 beside damping 18.
 * Stiffness 140 beside 145. Thirteen frames beside fourteen — 33 milliseconds,
 * which no viewer has ever perceived. Nobody chose those; every component tuned
 * its own spring in isolation, so nothing in a reel shares a rhythm. That is
 * what "flat" looks like in motion: not too little movement, but movement with
 * no common pulse.
 *
 * FIVE ROLES. Four were designed; the fifth (pop) was DISCOVERED by snapping
 * and finding 25 hand-written configs clustered somewhere none of the four
 * reached. A system that cannot express what people are already writing is not
 * a system, it is a preference.
 *
 *   enter    something arrives — the default, used by almost everything
 *   land     a payload arrives WITH WEIGHT: a number, an impact, a reveal.
 *            Slower and heavier, so it reads as consequential rather than quick
 *   soft     something appears without asking for attention: a label, a credit,
 *            a footnote. Barely a spring at all
 *   draw     a mark drawing ON — an underline, a circle, a bar. No bounce ever:
 *            a rule that overshoots and settles looks like a mistake
 *
 * DURATIONS quantise to three values. The gap between them is perceptible; the
 * gaps inside the old spread were not.
 */

/** Spring configs. Pass straight into Remotion's spring({ config }). */
export const SPRING = {
  enter: { damping: 18, stiffness: 150, mass: 0.7 },
  land: { damping: 14, stiffness: 110, mass: 1.0 },
  soft: { damping: 22, stiffness: 130, mass: 0.6 },
  draw: { damping: 26, stiffness: 160, mass: 0.5 },
  /**
   * pop — quick and snappy, with a visible overshoot.
   *
   * NOT invented: it was already the most-used family in the codebase and the
   * first four roles missed it. Snapping revealed ~25 configs clustered at low
   * damping (10-16) with high stiffness (180-320) — chips, list rows, anything
   * that should feel like it lands rather than arrives. The role is the
   * centroid of what was already being written by hand.
   */
  pop: { damping: 14, stiffness: 220, mass: 0.6 },
} as const;

/** Frames at 30fps. Three steps, each perceptibly different from the next. */
export const DUR = {
  quick: 8,   // 0.27s — a label, a chip, anything secondary
  base: 14,   // 0.47s — the default arrival
  slow: 22,   // 0.73s — a payload that should feel like it weighs something
} as const;

/**
 * Sequences. A stagger below ~60ms reads as simultaneous and above ~140ms reads
 * as a queue, so there are two: one for tight groups, one for a list the viewer
 * is meant to count.
 */
export const STAGGER = {
  word: 0.08,   // per-word reveal — hyperframes-animation techniques.md #4
  row: 0.13,    // list rows, checklist items, spec lines
} as const;

/**
 * The slide decay for per-word reveals: the first word travels furthest and
 * later ones settle quicker, which is what makes it read as kinetic rather than
 * as a queue. From hyperframes-animation techniques.md #4, whose sample is
 * 80, 60, 50, 25, 12px.
 */
export const slideFor = (index: number, first = 80): number =>
  Math.max(10, first * Math.pow(0.72, index));

/** Shared easing, so nothing invents its own curve. */
export const easeOut = (x: number): number =>
  1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);
