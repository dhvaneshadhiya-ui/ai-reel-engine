/**
 * Where Instagram Reels and YouTube Shorts paint their OWN interface over ours.
 *
 * WHY THIS FILE EXISTS
 * --------------------
 * We render a correct 1080x1920 and then the platform draws on top of it. Our
 * source credits sat at `bottom: 96` — y = 0.95 — which is inside Instagram's
 * username / caption / comment-bar stack. The credit the user explicitly asked
 * for on 2026-08-12 was being printed into the one band the platform covers, so
 * it shipped invisible. Nothing in the repo modelled the overlay: G32 reasoned
 * about the TOP band for the outro and there was no equivalent for the bottom
 * or the right-hand action rail.
 *
 * MEASURED, not guessed. Taken off real Instagram Reels screenshots of our own
 * published reel (919 x 1964 device px, 2026-08-17):
 *
 *   top header ("Reels", back, camera)      y 0.100
 *   action rail (like/comment/share/more)   x 0.881 -> 1.000, y 0.51 -> 0.84
 *   account row ("igeeksblog / AI content") y 0.835
 *   platform caption line                   y 0.881
 *   "Add comment..." bar                    y 0.957
 *
 * YouTube Shorts differs in detail but not in kind: title and channel bottom
 * left, actions bottom right. The rect below clears both.
 */

/** Fractions of the frame. Everything essential belongs inside this rect. */
export const SAFE_RECT = {
  x0: 0.06,
  y0: 0.12,
  x1: 0.85,
  y1: 0.80,
} as const;

/**
 * Secondary furniture — a source credit — may sit a little lower than primary
 * content, but NOT at 0.86: the account row measures 0.835, so 0.86 lands on
 * top of the username. This is deliberately tighter than that, just inside the
 * safe floor, so the credit is legible on both platforms.
 */
export const CREDIT_Y = 0.78;

export interface SafeBox {
  left: number;
  top: number;
  right: number;
  bottom: number;
  width: number;
  height: number;
}

/** The safe rect in pixels for a given frame. */
export const safeBox = (frameW: number, frameH: number): SafeBox => {
  const left = frameW * SAFE_RECT.x0;
  const top = frameH * SAFE_RECT.y0;
  const right = frameW * SAFE_RECT.x1;
  const bottom = frameH * SAFE_RECT.y1;
  return {
    left,
    top,
    right,
    bottom,
    width: right - left,
    height: bottom - top,
  };
};

/** Distance from the frame bottom, in px, for the credit line. */
export const creditBottomPx = (frameH: number): number =>
  Math.round(frameH * (1 - CREDIT_Y));

/** Left inset in px matching the safe rect. */
export const safeLeftPx = (frameW: number): number =>
  Math.round(frameW * SAFE_RECT.x0);
