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
export const creditLabel = (t: string): string =>
  /^(source|credit|@)/i.test(t.trim()) ? t.trim() : `Source: ${t.trim()}`;

export const Credit: React.FC<CreditProps> = ({
  text,
  // 0.78 of a 1920 frame = 422px up from the bottom. The old 260 put it at
  // y 0.865, on top of Instagram's account row.
  bottom = creditBottomPx(1920),
  left = 64,
  onMedia = true,
  plate,
}) => {
  if (!text || !text.trim()) return null;
  const plated = plate ?? onMedia;
  return (
    <div
      style={{
        position: "absolute",
        bottom,
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
