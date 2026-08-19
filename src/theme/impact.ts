/**
 * IMPACT — the visual half of a sound effect.
 *
 * WHY (2026-08-18, user: "how about adding the similar effects to the text
 * (headlines) similar to sound effects when they are in the video")
 * ---------------------------------------------------------------------------
 * Measured on iphone-fold-ultra before writing this: 8 SFX cues, 6 scenes with
 * headlines, and the two sets INTERSECT ONCE — scene 05, where the whoosh fires
 * at 0.00s and the headline lands at 0.15 / 0.45 / 0.85. Not one sound in the
 * reel lands on a picture event. A whoosh over nothing is a noise; the same
 * whoosh on the frame where the claim arrives is an accent, and the viewer
 * cannot tell you why the second one feels produced.
 *
 * So text gets an envelope of the same shape a transient has, and — where a cue
 * exists — the two are locked to the same instant by tools/sync_impacts.py.
 *
 * THE SHAPE IS A TRANSIENT, not a spring. A spring is how something ARRIVES
 * and settles; an impact is how something is STRUCK. Instant attack, then
 * exponential decay, because that is the envelope of every percussive sound the
 * SFX library contains — a shutter, a pop, a click. Motion that shares an
 * envelope with the audio reads as one event rather than two.
 */

/** Frames of decay for an impact. 0.22s at 30fps — a transient, not a move. */
const DECAY_S = 0.22;

/**
 * Envelope 1 -> 0 for the most recent cue at or before `t`, else 0.
 *
 * `cues` are absolute seconds within the scene. Returns 0 before the first cue,
 * so nothing flickers on frame 0 of a scene whose impact comes later.
 */
export const impactAt = (t: number, cues: number[]): number => {
  let best = 0;
  for (const c of cues) {
    if (t < c) continue;
    const age = t - c;
    if (age > DECAY_S * 3) continue;
    const v = Math.exp(-age / (DECAY_S / 2.2));
    if (v > best) best = v;
  }
  return best;
};

/**
 * HOW HARD a line is struck, from what the line IS.
 *
 * The same derivation the type treatments use: a number is the thing the beat
 * exists to deliver and should land hardest; an eyebrow is context and should
 * barely register. A single global strength would either flatten the payload or
 * make every label twitch.
 */
export const IMPACT = {
  payload: 1.0,
  claim: 0.62,
  question: 0.45,
  label: 0.28,
} as const;

/** Scale punch at the moment of impact — the body of the hit. */
export const punch = (env: number, strength: number): number =>
  1 + 0.09 * strength * env;

/**
 * Sub-pixel displacement. Deliberately TINY (max ~3px at full strength): a
 * shake big enough to notice as a shake reads as a broken render, while one
 * you can only feel reads as weight. Alternating sign by index keeps two lines
 * struck at once from moving as a block.
 */
export const jolt = (env: number, strength: number, index = 0): number =>
  (index % 2 === 0 ? 1 : -1) * 3 * strength * env * env;

/**
 * Glow flare, as an alpha for a colour the caller supplies. Squared so it is
 * gone almost immediately — a flare that lingers is a gradient, not a hit.
 */
export const flare = (env: number, strength: number): number =>
  0.85 * strength * env * env;
