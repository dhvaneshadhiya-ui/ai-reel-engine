/**
 * HOW MUCH TYPE FITS — one implementation, used by every component that sets
 * display type, and mirrored by the gate that used to guess at it.
 *
 * WHY THIS FILE EXISTS (2026-08-18)
 * ---------------------------------
 * `LINE_MAX_CHARS = {"label": 30, "headline": 18, "subtitle": 26}` sat in
 * tools/reel_gates.py behind G05, a BLOCKING gate. Those numbers were
 * calibrated against Fraunces, which fits ~18.8 characters at SIZE.display.
 *
 * The display face changed to Space Grotesk the same day, on the user's pick.
 * Space Grotesk is wider: the real budget dropped to ~14.4 characters. The gate
 * kept allowing 18. It did not fail, warn, or notice — it silently began
 * passing headlines that overflow the frame, and six of them were already in
 * the library, including the hook of airpods-camera ("NEVER ANNOUNCED", 15).
 *
 * A typed character budget is a measurement of a font, written down somewhere
 * the font cannot reach. So there is now one constant, one solver, and
 * components that SHRINK TO FIT rather than trusting anyone to count.
 */

/**
 * Mean glyph advance as a fraction of em, Space Grotesk 700, mixed case.
 * Verified by rendering the widest line in the library and checking both frame
 * edges. If DISPLAY in theme/type.ts changes, re-measure this in the same
 * commit — it is the one number here that belongs to the typeface.
 */
export const ADVANCE = 0.655;

/** Characters that fit on one line of `size` px within `boxW` px. */
export const charBudget = (size: number, boxW: number): number =>
  boxW / (size * ADVANCE);

/**
 * Largest size at or below `size` at which `text` fits `boxW` on one line.
 *
 * Shrinking beats wrapping for a headline: a claim that wraps orphans a word
 * and changes the block's height, which then moves it inside the safe band.
 * A claim two points smaller changes nothing structural.
 *
 * `floor` stops the shrink becoming its own defect — below it the line is no
 * longer display type and the copy is the thing that needs fixing, which is
 * what the (now advisory) G05 says.
 */
export const fitOneLine = (
  text: string,
  size: number,
  boxW: number,
  floor = 0.62
): number => {
  const need = text.trim().length * ADVANCE;
  if (need === 0) return size;
  return Math.round(Math.max(size * floor, Math.min(size, boxW / need)));
};
