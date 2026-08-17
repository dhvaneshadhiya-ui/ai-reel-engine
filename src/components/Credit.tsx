import React from "react";

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
 * So the treatment now lives in ONE component that every scene imports, and
 * `lint_frames.py` fails the build if a component hand-rolls its own credit.
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
}

/** "Apple" -> "Source: Apple";  "@user" / "Source: X" pass through unchanged. */
export const creditLabel = (t: string): string =>
  /^(source|credit|@)/i.test(t.trim()) ? t.trim() : `Source: ${t.trim()}`;

export const Credit: React.FC<CreditProps> = ({
  text,
  bottom = 260,
  left = 64,
  onMedia = true,
}) => {
  if (!text || !text.trim()) return null;
  return (
    <div
      style={{
        position: "absolute",
        bottom,
        left,
        right: 64,
        textAlign: "left",
        fontFamily: CREDIT_FONT,
        fontSize: 27,
        fontWeight: 600,
        letterSpacing: 0.2,
        color: onMedia ? "rgba(255,255,255,0.94)" : "rgba(20,20,22,0.72)",
        textShadow: onMedia ? "0 2px 10px rgba(0,0,0,0.75)" : "none",
      }}
    >
      {creditLabel(text)}
    </div>
  );
};
