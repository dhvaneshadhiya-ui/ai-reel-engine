import React from "react";
import { TYPE } from "../theme/type";
import { creditBottomPx } from "../platformSafeArea";

/**
 * ONE credit treatment for every borrowed asset.
 *
 * WHY THIS EXISTS (2026-08-14)
 * ----------------------------
 * On 2026-08-12 the user asked for credits that read "Source: SpaceXAI",
 * left-aligned under the footage. That was applied to FloatingCard ONLY.
 * FootageScene, SplitScene and ReceiptScene kept their old treatment — bare
 * name, centred, 85% white — so september-preview shipped with a prominent
 * "Source: MacRumors" on the article card and a faint centred "Apple" under
 * the video, in the same reel.
 *
 * The instruction had been recorded in the ledger as prose. Prose regresses.
 * So the treatment now lives in ONE component that every scene imports.
 *
 * THIS DOCSTRING USED TO CLAIM lint_frames.py failed the build on a hand-rolled
 * credit. It did not — "credits present" was item 6 on a checklist a human
 * eyeballs, and AnnotateZoom quietly carried its own credit at bottom: 96 for
 * weeks as a result. A claimed check that does not exist is worse than no
 * check, because it stops anyone looking. The real one now lives in
 * tools/check_credits.py and runs in doctor.
 *
 * POSITION (2026-08-17): the default clears the PLATFORM's own furniture, not
 * just ours. See src/platformSafeArea.ts — Instagram's account row measures
 * y 0.835 and its caption y 0.881, so anything below ~0.80 is contested.
 */
export const CREDIT_FONT =
  "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";

export interface CreditProps {
  /** raw credit from the beat sheet, e.g. "Apple" or "@user" */
  text: string;
  /** distance from the frame bottom, px. Default clears the caption band. */
  bottom?: number;
  /**
   * Anchor from the TOP instead, in px. For components that attach attribution
   * to their card rather than to the frame — FloatingCard puts it just under
   * the card's bottom-left corner (user feedback 2026-08-12: a bare name
   * floating in the field reads as a stray word). Those components used to
   * hand-roll the whole label to get that placement, which meant they silently
   * opted out of the once-per-source rule and the qualifier stripping.
   */
  top?: number;
  /** left inset, px — the frame's safe margin */
  left?: number;
  /** dark asset behind it? (adds a shadow so it survives bright footage) */
  onMedia?: boolean;
  /**
   * Draw a translucent plate behind the text.
   *
   * Needed because moving the credit up out of the platform caption band put it
   * OVER the screenshot card instead of below it, and a screenshot can be any
   * colour — dark ink vanished on a dark photo, white would vanish on a white
   * article. `onMedia` keys off the scene's backdrop, which says nothing about
   * the pixels actually behind these words. A plate is the only treatment that
   * survives arbitrary content, so it is the default whenever `onMedia`.
   */
  plate?: boolean;
}

/** "Apple" -> "Source: Apple";  "@user" / "Source: X" pass through unchanged. */
/**
 * ONE CREDIT PER SOURCE (user decision 2026-08-19).
 *
 * Measured before changing it: iphone-fold-ultra carried a credit on 76% of its
 * runtime — Unbox Therapy for 35.3s across 24 scenes, MacRumors for 22.5s
 * across 12. The label never animates and sits at a fixed position, so it did
 * not flicker; it simply never left.
 *
 * The provenance STAYS IN THE BEAT SHEET on every scene — G14 reads the sheet,
 * and stripping credits there would lose which asset came from where. Only the
 * DRAWING is deduplicated: the first scene to use a source shows it, later
 * scenes carry the same data and render nothing.
 */
const CreditPolicy = React.createContext<{
  firstFor: Record<string, number>;
  sceneIndex: number;
  /** the whole reel opts out — see BeatSheet.noCredits */
  suppressed?: boolean;
} | null>(null);

export const CreditPolicyProvider: React.FC<{
  firstFor: Record<string, number>;
  sceneIndex: number;
  suppressed?: boolean;
  children: React.ReactNode;
}> = ({ firstFor, sceneIndex, suppressed, children }) =>
  React.createElement(
    CreditPolicy.Provider,
    { value: { firstFor, sceneIndex, suppressed } },
    children);

/** Which scene index owns the single on-screen credit for each source. */
export const firstUseByCredit = (
  scenes: { credit?: string }[]
): Record<string, number> => {
  const first: Record<string, number> = {};
  scenes.forEach((s, i) => {
    const c = (s.credit ?? "").trim();
    if (c && !(c in first)) first[c] = i;
  });
  return first;
};

/**
 * Strip a trailing qualifier from a credit for DISPLAY.
 *
 * "Unbox Therapy — dummy unit" -> "Unbox Therapy"  (user decision 2026-08-19)
 *
 * The sheet and manifest keep the full string, so provenance is unchanged and
 * G14 still reads what it always read. Only the drawn label shortens — the same
 * split as the once-per-source rule above.
 *
 * NOTE, recorded because it is a real consequence and not a style one: on
 * iphone-fold-ultra the suffix was the ONLY place the word "dummy" appeared in
 * all 46 scenes. The manifest asks for "a DUMMY UNIT label AND the Unbox
 * Therapy credit"; the label was never built, so the credit had been carrying
 * the disclaimer alone. After this change nothing on screen tells a viewer the
 * folding phone is a non-functional mockup. Restoring that means adding the
 * label the manifest already specifies — a headline or typecard on one dummy
 * beat — not putting the suffix back on every credit.
 */
const stripQualifier = (t: string): string =>
  t.split(/\s+[—–-]\s+/)[0].trim();

export const creditLabel = (t: string): string => {
  const base = stripQualifier(t);
  return /^(source|credit|@)/i.test(base) ? base : `Source: ${base}`;
};

export const Credit: React.FC<CreditProps> = ({
  text,
  // 0.78 of a 1920 frame = 422px up from the bottom. The old 260 put it at
  // y 0.865, on top of Instagram's account row.
  bottom = creditBottomPx(1920),
  top,
  left = 64,
  onMedia = true,
  plate,
}) => {
  if (!text || !text.trim()) return null;
  // Draw only on the scene that owns this source. No provider (a still, a
  // preview, a component rendered outside the reel) means draw as before.
  const policy = React.useContext(CreditPolicy);
  // The reel opted out entirely. One check, before the per-source rule, so it
  // covers every component that draws attribution — which is now all of them.
  if (policy?.suppressed) return null;
  if (policy) {
    const owner = policy.firstFor[text.trim()];
    if (owner !== undefined && owner !== policy.sceneIndex) return null;
  }
  const plated = plate ?? onMedia;
  return (
    <div
      style={{
        position: "absolute",
        ...(top !== undefined ? { top } : { bottom }),
        left,
        right: 64,
        textAlign: "left",
        // The plate has to hug the words, not span the frame, so the row is a
        // flex line with the plate on the inline child.
        display: "flex",
        justifyContent: "flex-start",
      }}
    >
      <span
        style={{
          ...TYPE.micro,
          color: plated || onMedia
            ? "rgba(255,255,255,0.96)"
            : "rgba(20,20,22,0.72)",
          textShadow: onMedia && !plated
            ? "0 2px 10px rgba(0,0,0,0.75)"
            : "none",
          background: plated ? "rgba(12,12,14,0.62)" : "transparent",
          padding: plated ? "7px 15px 8px" : 0,
          borderRadius: plated ? 8 : 0,
        }}
      >
        {creditLabel(text)}
      </span>
    </div>
  );
};
