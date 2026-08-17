import React from "react";
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";

export interface DeviceFrameProps {
  /** browser = macOS window chrome; phone = iPhone-style frame with notch */
  kind: "browser" | "phone";
  /** image or video under public/ — .mp4/.webm/.mov are treated as video */
  src: string;
  /** video trim start, in seconds (video sources only) */
  from?: number;
  /** URL string shown in the browser chrome pill */
  url?: string;
  bg?: "cream" | "black";
  zoomDir?: "in" | "out" | "none";
  /** small serif caption under the device */
  label?: string;
  credit?: string;
  /**
   * Media-area aspect ratio (w/h). Defaults to 16/9 for VIDEO sources so
   * clips are never side-cropped (FEEDBACK 2026-07-29: cover-crop in a tall
   * window cut clip text mid-word); page screenshots default to a tall area.
   */
  mediaAspect?: number;
}

const isVideoSrc = (src: string) => /\.(mp4|webm|mov)$/i.test(src);

/** The media itself — Img for stills, OffthreadVideo for clips. */
const Media: React.FC<{
  src: string;
  from?: number;
  fps: number;
  style: React.CSSProperties;
}> = ({ src, from, fps, style }) =>
  isVideoSrc(src) ? (
    <OffthreadVideo
      src={staticFile(src)}
      startFrom={Math.round((from ?? 0) * fps)}
      muted
      style={style}
    />
  ) : (
    <Img src={staticFile(src)} style={style} />
  );

/**
 * A screenshot / clip presented inside a device — macOS browser window or
 * iPhone frame — floating on a themed backdrop with a blurred copy of the
 * same media as the background fill. Slow Ken Burns push on the whole group.
 */
export const DeviceFrame: React.FC<DeviceFrameProps> = ({
  kind,
  src,
  from,
  url,
  bg = "cream",
  zoomDir = "in",
  label,
  credit,
  mediaAspect,
}) => {
  const theme = useTheme();
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const dark = bg === "black";
  const backdrop = dark ? theme.black : theme.cream;

  // ---- slow push on the whole device group ----
  const push =
    zoomDir === "none"
      ? 1
      : zoomDir === "in"
        ? interpolate(frame, [0, durationInFrames], [1, 1.07])
        : interpolate(frame, [0, durationInFrames], [1.07, 1]);

  // ---- staggered entrances: device first, label after ----
  const enter = spring({
    frame,
    fps,
    config: { damping: 17, stiffness: 130, mass: 0.7 },
    durationInFrames: 20,
  });
  const labelIn = spring({
    frame: frame - 10,
    fps,
    config: { damping: 15, stiffness: 160, mass: 0.6 },
    durationInFrames: 16,
  });

  // ---- device geometry ----
  const isBrowser = kind === "browser";
  // Media area follows the source aspect: videos default to 16:9 (never
  // side-crop a clip); page screenshots keep the tall reading pane.
  const aspect = mediaAspect ?? (isVideoSrc(src) ? 16 / 9 : 940 / 1050);
  const cardW = isBrowser ? (aspect >= 1 ? 1000 : 940) : 470;
  const chromeH = isBrowser ? 76 : 0;
  const mediaH = isBrowser ? Math.round(cardW / aspect) : 922;
  const bezel = isBrowser ? 0 : 14;

  const trafficColors = ["#ff5f57", "#febc2e", "#28c840"];

  const device = isBrowser ? (
    <div
      style={{
        width: cardW,
        borderRadius: theme.radius.card,
        overflow: "hidden",
        boxShadow: dark ? theme.shadow.cardOnDark : theme.shadow.card,
        background: theme.white,
      }}
    >
      {/* macOS window chrome */}
      <div
        style={{
          height: chromeH,
          display: "flex",
          alignItems: "center",
          padding: "0 26px",
          background: theme.white,
          borderBottom: "1px solid rgba(0,0,0,0.08)",
          position: "relative",
        }}
      >
        <div style={{ display: "flex", gap: 13 }}>
          {trafficColors.map((c) => (
            <div
              key={c}
              style={{
                width: 19,
                height: 19,
                borderRadius: "50%",
                background: c,
                boxShadow: "inset 0 0 0 0.5px rgba(0,0,0,0.12)",
              }}
            />
          ))}
        </div>
        {url && (
          <div
            style={{
              position: "absolute",
              left: "50%",
              transform: "translateX(-50%)",
              height: 42,
              minWidth: cardW * 0.52,
              maxWidth: cardW * 0.66,
              borderRadius: 21,
              background: "rgba(0,0,0,0.06)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 10,
              padding: "0 24px",
            }}
          >
            {/* padlock */}
            <svg width="16" height="20" viewBox="0 0 16 20">
              <rect
                x="1"
                y="8"
                width="14"
                height="11"
                rx="3"
                fill="rgba(0,0,0,0.45)"
              />
              <path
                d="M4 8 V6 a4 4 0 0 1 8 0 V8"
                stroke="rgba(0,0,0,0.45)"
                strokeWidth="2.4"
                fill="none"
              />
            </svg>
            <span
              style={{
                fontFamily: theme.sans,
                fontSize: 24,
                fontWeight: 500,
                color: "rgba(0,0,0,0.62)",
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {url}
            </span>
          </div>
        )}
      </div>
      {/* page media */}
      <div style={{ width: cardW, height: mediaH, overflow: "hidden" }}>
        <Media
          src={src}
          from={from}
          fps={fps}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 0%",
            display: "block",
          }}
        />
      </div>
    </div>
  ) : (
    <div
      style={{
        width: cardW,
        borderRadius: 66,
        padding: bezel,
        background: theme.black,
        boxShadow: dark ? theme.shadow.cardOnDark : theme.shadow.card,
        position: "relative",
      }}
    >
      <div
        style={{
          width: cardW - bezel * 2,
          height: mediaH,
          borderRadius: 66 - bezel,
          overflow: "hidden",
          position: "relative",
          background: theme.black,
        }}
      >
        <Media
          src={src}
          from={from}
          fps={fps}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 0%",
            display: "block",
          }}
        />
        {/* dynamic-island notch */}
        <div
          style={{
            position: "absolute",
            top: 16,
            left: "50%",
            transform: "translateX(-50%)",
            width: 128,
            height: 36,
            borderRadius: 20,
            background: theme.black,
          }}
        />
      </div>
    </div>
  );

  return (
    <AbsoluteFill
      style={{
        background: backdrop,
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* blurred enlarged copy of the same media — no flat dead space */}
      <AbsoluteFill>
        <Media
          src={src}
          from={from}
          fps={fps}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: dark
              ? "blur(52px) brightness(0.4)"
              : "blur(52px) brightness(1.02) saturate(1.05)",
            transform: "scale(1.4)",
          }}
        />
        {/* warm themed wash so the fill reads cream/black, never gray */}
        <AbsoluteFill
          style={{
            background: dark ? theme.black : theme.cream,
            opacity: dark ? 0.35 : 0.42,
          }}
        />
      </AbsoluteFill>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${push})`,
        }}
      >
        <div
          style={{
            opacity: enter,
            transform: `translateY(${(1 - enter) * 46}px) scale(${
              0.965 + 0.035 * enter
            })`,
          }}
        >
          {device}
        </div>
        {label && (
          <div
            style={{
              marginTop: 52,
              fontFamily: theme.serif,
              fontStyle: "italic",
              fontWeight: 700,
              fontSize: 46,
              letterSpacing: "-0.01em",
              color: dark ? theme.inkOnDark : theme.ink,
              textAlign: "center",
              maxWidth: 900,
              lineHeight: 1.15,
              opacity: labelIn,
              transform: `translateY(${(1 - labelIn) * 22}px)`,
            }}
          >
            {label}
          </div>
        )}
      </div>

      {credit && (
        <div
          style={{
            position: "absolute",
            bottom: 96,
            width: "100%",
            textAlign: "center",
            fontFamily: theme.sans,
            fontSize: 25,
            color: dark ? theme.mutedOnDark : theme.muted,
          }}
        >
          {credit}
        </div>
      )}
    </AbsoluteFill>
  );
};
