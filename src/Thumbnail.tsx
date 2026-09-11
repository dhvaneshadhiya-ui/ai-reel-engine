import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { ThemeProvider, useTheme } from "./theme/tokens";

/**
 * Reel / Shorts cover — 1080x1920, rendered with `remotion still`.
 *
 * A COVER IS SPOTTED, NOT READ
 * ----------------------------
 * The first build of this was a cream, serif, 16:9 magazine cover. Elegant, and
 * wrong on all three axes: our reels are vertical, the click is decided in a
 * feed at ~200px, and low-contrast type at that size is a grey smear. Rejected
 * 2026-08-17. What replaced it is the format that actually earns the tap:
 * near-black ground, ALL-CAPS heavy sans, and a two-line headline whose SECOND
 * line sits on a solid accent block. The block is the payoff and the single
 * loudest thing in the frame.
 *
 * THE SAFE AREA IS THE WHOLE GAME
 * -------------------------------
 * A 9:16 cover is almost never seen as 9:16 first. In a profile grid it is
 * CENTRE-CROPPED, so anything outside the crop is invisible exactly where
 * people browse. Everything that must be read lives inside y = 240..1680 — the
 * centre 1080x1440, a 3:4 tile. Above and below is deliberate bleed: it keeps
 * the full-height view composed in the Shorts feed and carries only ground.
 *
 * WAS A 1:1 SQUARE UNTIL 2026-09-11. Instagram replaced its square profile
 * grid with 3:4 tiles in January 2025, twenty months before anyone here
 * checked. Nothing was being cut off — a square fits inside a 3:4 crop — but
 * 360px of VISIBLE height went unused, and that is the space the subject is
 * supposed to fill. The preview make_thumbnail.py writes was also cropping 1:1,
 * so it showed less than viewers actually see.
 *
 * NO PRESENTER FACE. The reference look leans on a creator's face as its
 * anchor; we are a publication, not a personality, so the anchor is the
 * SUBJECT — the product shot or the receipt we actually put on screen.
 */

const W = 1080;
const H = 1920;
/** Instagram's profile grid tile since Jan 2025: 3:4, i.e. 1080x1440. */
const GRID_H = 1440;
/** Centre 3:4 crop — what the grid shows. Read-critical content only. */
const SAFE_TOP = (H - GRID_H) / 2; // 240
const SAFE_H = GRID_H; // 1440

export type ThumbnailProps = {
  /** subject wordmark, e.g. "APPLE" — the authority cue, top of the safe square */
  brand?: string;
  /** frame from the reel, relative to public/ — the subject, not decoration */
  frameSrc?: string;
  /** line 1: plain white caps */
  line1?: string;
  /** line 2: caps on the accent block. The payoff — make it the promise. */
  line2?: string;
  /** style pack — drives every colour */
  style?: string;
  /** block colour override; defaults to the style's accent */
  blockColor?: string;
  /** text colour on the block; defaults to near-black */
  blockText?: string;
  /** 16:9 fallback for surfaces that still want a wide still */
  format?: "vertical" | "wide";
};

type InnerProps = Required<Omit<ThumbnailProps, "style" | "format">>;

const Vertical: React.FC<InnerProps> = ({
  brand,
  frameSrc,
  line1,
  line2,
  blockColor,
  blockText,
}) => {
  const t = useTheme();
  const block = blockColor || t.accent;

  return (
    <AbsoluteFill style={{ backgroundColor: "#07070a" }}>
      {/* Ground: a cool wash so the subject never sits on flat black */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(120% 70% at 50% 38%, #17171f 0%, #0b0b10 55%, #07070a 100%)",
        }}
      />

      {/* THE SAFE SQUARE — everything readable lives here */}
      <div
        style={{
          position: "absolute",
          top: SAFE_TOP,
          left: 0,
          width: W,
          height: SAFE_H,
          padding: "38px 54px 46px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {brand ? (
          <div
            style={{
              display: "block",
              fontFamily: t.sans,
              fontSize: 92,
              fontWeight: 800,
              letterSpacing: -2,
              lineHeight: 1,
              color: "#ffffff",
              textAlign: "center",
            }}
          >
            {brand}
          </div>
        ) : null}

        <div
          style={{
            flex: 1,
            width: "100%",
            margin: "22px 0",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            overflow: "hidden",
          }}
        >
          {frameSrc ? (
            <Img
              src={staticFile(frameSrc)}
              style={{
                // Caps, never enlarges — so the element HUGS the picture and the
                // radius and shadow land on the image itself. Filling the box is
                // done upstream: make_thumbnail.py enlarges any frame smaller than
                // the largest possible box before it gets here (2026-09-11). Doing
                // it here with width/height 100% + objectFit drew the picture
                // inside a larger box, and the corners rounded the box instead.
                maxWidth: "100%",
                maxHeight: "100%",
                objectFit: "contain",
                borderRadius: 22,
                // drop-shadow, not box-shadow (2026-09-11): box-shadow shadows the
                // element's BOX, so a transparent subject (a logo) got a faint
                // dark rectangle under it. drop-shadow follows the alpha, and
                // on an opaque photo it is indistinguishable from box-shadow.
                filter: "drop-shadow(0 26px 40px rgba(0,0,0,0.65))",
              }}
            />
          ) : null}
        </div>

        {/* THE HEADLINE. Line 2 on the block is the loudest thing in frame. */}
        <div style={{ width: "100%", textAlign: "center" }}>
          {line1 ? (
            <div
              style={{
                display: "block",
                fontFamily: t.sans,
                fontSize: 104,
                fontWeight: 900,
                letterSpacing: -2,
                lineHeight: 1.02,
                color: "#ffffff",
                textTransform: "uppercase",
                textShadow: "0 3px 18px rgba(0,0,0,0.6)",
              }}
            >
              {line1}
            </div>
          ) : null}
          {line2 ? (
            <div
              style={{
                display: "inline-block",
                marginTop: 12,
                padding: "6px 22px 14px",
                borderRadius: 12,
                backgroundColor: block,
                fontFamily: t.sans,
                fontSize: 104,
                fontWeight: 900,
                letterSpacing: -2,
                lineHeight: 1.02,
                color: blockText || "#0a0a0a",
                textTransform: "uppercase",
              }}
            >
              {line2}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Wide: React.FC<InnerProps> = ({
  brand,
  frameSrc,
  line1,
  line2,
  blockColor,
  blockText,
}) => {
  const t = useTheme();
  const block = blockColor || t.accent;
  return (
    <AbsoluteFill style={{ backgroundColor: "#07070a", flexDirection: "row" }}>
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(110% 90% at 30% 45%, #17171f 0%, #0b0b10 60%, #07070a 100%)",
        }}
      />
      <div
        style={{
          // POSITIONED on purpose. The radial-gradient behind this is an
          // <AbsoluteFill>, and a positioned element paints ABOVE a static one
          // in the same stacking context — so with position:static these two
          // columns rendered UNDER the gradient and the wide thumbnail came out
          // black with a faint ghost of the image. Caught 2026-08-19; no wide
          // thumbnail had ever been generated before, so it had never shown.
          position: "relative",
          width: "62%",
          height: "100%",
          padding: 64,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        {brand ? (
          <div
            style={{
              display: "block",
              fontFamily: t.sans,
              fontSize: 44,
              fontWeight: 800,
              letterSpacing: 2,
              color: "rgba(255,255,255,0.72)",
              textTransform: "uppercase",
              marginBottom: 18,
            }}
          >
            {brand}
          </div>
        ) : null}
        <div
          style={{
            display: "block",
            fontFamily: t.sans,
            fontSize: 86,
            fontWeight: 900,
            letterSpacing: -2,
            lineHeight: 1.02,
            color: "#ffffff",
            textTransform: "uppercase",
          }}
        >
          {line1}
        </div>
        {line2 ? (
          <div
            style={{
              display: "inline-block",
              alignSelf: "flex-start",
              marginTop: 12,
              padding: "4px 20px 12px",
              borderRadius: 10,
              backgroundColor: block,
              fontFamily: t.sans,
              fontSize: 86,
              fontWeight: 900,
              letterSpacing: -2,
              lineHeight: 1.02,
              color: blockText || "#0a0a0a",
              textTransform: "uppercase",
            }}
          >
            {line2}
          </div>
        ) : null}
      </div>
      <div
        style={{
          position: "relative",
          width: "38%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 40,
        }}
      >
        {frameSrc ? (
          <Img
            src={staticFile(frameSrc)}
            style={{
              // caps only — see the vertical layout; filling is done upstream.
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              borderRadius: 18,
              // drop-shadow for the same reason as the vertical layout above.
              filter: "drop-shadow(0 24px 34px rgba(0,0,0,0.7))",
            }}
          />
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

export const Thumbnail: React.FC<ThumbnailProps> = ({
  brand = "",
  frameSrc = "",
  line1 = "SET LINE1",
  line2 = "IN PROPS",
  style = "editorial",
  blockColor = "",
  blockText = "",
  format = "vertical",
}) => {
  const props = { brand, frameSrc, line1, line2, blockColor, blockText };
  return (
    <ThemeProvider style={style}>
      {format === "wide" ? <Wide {...props} /> : <Vertical {...props} />}
    </ThemeProvider>
  );
};
