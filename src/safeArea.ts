/**
 * Horizontal safe area for any scene that zooms into a captured screenshot.
 *
 * WHY THIS FILE EXISTS
 * --------------------
 * `AnnotateZoom` and `ReceiptScene` both compute a "fit" zoom — the zoom at
 * which the focused region still fits the frame — and both then applied an
 * aesthetic MINIMUM zoom (1.15 and 1.35) that overrode it. For an article
 * column, which is nearly as wide as the capture, the fit lands below 1.0 and
 * the floor pushes in on something that already did not fit, slicing the
 * focused text off BOTH edges.
 *
 * That shipped to Instagram and YouTube: 44 scenes across 4 reels, up to 113
 * source px lost per side, so viewers read "Phone 15" where the capture said
 * "iPhone 15".
 *
 * The constant lives here because the same number in two components is a
 * number that drifts. `tools/check_safe_area.py` models this arithmetic to
 * measure beats files before a render; if the geometry here changes, change the
 * model in the same commit or it measures nothing.
 */

/**
 * Fraction of the frame width the padded focus region may occupy. Below 1 so a
 * glyph never lands under a rounded card corner or its shadow, and so there is
 * real margin against the platform chrome that crowds a phone screen — the
 * Instagram action rail on the right, the caption block at the bottom.
 */
export const SAFE_W = 0.96;

/**
 * The largest zoom at which a padded focus region of `unionW` card-px still sits
 * inside the frame's safe width. Cap every computed zoom with this, INCLUDING
 * after any push-in is added — a ceiling applied before the push-in is not a
 * ceiling.
 */
export const fitsZoom = (frameW: number, unionW: number): number =>
  unionW > 0 ? (frameW * SAFE_W) / unionW : Infinity;
