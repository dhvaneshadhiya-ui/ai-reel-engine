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
 * THE SAFE SQUARE IS THE WHOLE GAME
 * ---------------------------------
 * A 9:16 cover is almost never seen as 9:16 first. In a profile grid it is
 * CENTRE-CROPPED, so anything outside the middle square is invisible exactly
 * where people browse. Everything that must be read therefore lives inside
 * y = 420..1500 (the centre 1080x1080). Above and below is deliberate bleed: it
 * keeps the full-height view composed in the Shorts feed and is allowed to
 * carry nothing but ground.
 *
 * NO PRESENTER FACE. The reference look leans on a creator's face as its
 * anchor; we are a publication, not a personality, so the anchor is the
 * SUBJECT — the product shot or the receipt we actually put on screen.
 */

const W = 1080;
const H = 1920;
/** Centre 1:1 crop — the tightest common grid crop. Read-critical content only. */
const SAFE_TOP = (H - W) / 2; // 420
const SAFE_H = W; // 1080

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
                maxWidth: "100%",
                maxHeight: "100%",
                objectFit: "contain",
                borderRadius: 22,
                boxShadow: "0 26px 70px rgba(0,0,0,0.65)",
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
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              borderRadius: 18,
              boxShadow: "0 24px 60px rgba(0,0,0,0.7)",
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
