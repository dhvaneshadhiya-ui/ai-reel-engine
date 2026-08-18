import React from "react";
import { SPRING, DUR } from "../theme/motion";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";
import { Credit } from "./Credit";
import { fitsZoom } from "../safeArea";
import { SAFE_RECT } from "../platformSafeArea";

export interface ScreenMark {
  /** circle a control, underline a row, box a region, or point at it */
  kind: "circle" | "underline" | "box" | "arrow";
  /** seconds from scene start when the mark starts drawing */
  at: number;
  /** the control, in SOURCE video pixels */
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface ScreenStepProps {
  /** a screen recording under public/ — run it through tools/ingest_screencap.py first */
  src: string;
  srcWidth: number;
  srcHeight: number;
  /** trim point into the recording, seconds */
  from?: number;
  /** region (source px) to settle on; defaults to the union of the marks */
  focus?: { x: number; y: number; w: number; h: number };
  marks?: ScreenMark[];
  credit?: string;
}

const clamp = (v: number, lo: number, hi: number) =>
  Math.max(lo, Math.min(hi, v));
const easeOut = (x: number) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);

/**
 * A step in a how-to: the phone screen playing, zoomed to the control being
 * described, with a mark drawn on it at the moment the voice names it.
 *
 * WHY THIS EXISTS
 * ---------------
 * The engine had 43 scene types and not one could point at anything in a VIDEO.
 * `annotatezoom` draws circles and underlines but takes an <Img>; `footage`
 * plays video with no marks at all. So a screen recording could be shown and
 * never explained — which is the entire job of a fix-it reel.
 *
 * WHAT IS BORROWED, AND WHY IT IS SAFE
 * ------------------------------------
 * The zoom respects `fitsZoom` from safeArea.ts, the ceiling added after 44
 * scenes across 4 reels shipped with the focused text sliced off both frame
 * edges. A phone UI slices exactly the same way — a circled toggle with its
 * label cut off is worse than no mark.
 *
 * The marks draw in FRAME SPACE via strokeDashoffset. Remotion renders no CSS
 * transition or @keyframes, and a mark that animates only in CSS is a mark that
 * renders as a static shape or not at all.
 *
 * WHAT IS NEW
 * -----------
 * Keeping the mark locked to source pixels while the video scales. The video and
 * its SVG overlay are ONE transformed unit sharing a viewBox in source
 * coordinates, so a circle placed on a toggle stays on that toggle at any zoom.
 * Transform them separately and the mark drifts off the control — the same
 * failure crop mode had to avoid in AnnotateZoom.
 */
export const ScreenStep: React.FC<{ scene: ScreenStepProps }> = ({ scene }) => {
  const theme = useTheme();
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const { src, srcWidth, srcHeight, from, focus, marks = [], credit } = scene;

  // The screen FILLS the frame — it is the subject, not an artefact on a card.
  // Fit to width, which is how a 9:16 recording wants to sit in a 9:16 frame.
  const dispW = width;
  const dispH = (srcHeight / srcWidth) * dispW;
  const s = dispW / srcWidth; // source px -> display px

  // ---- what to look at ----
  let fx: number, fy: number, fw: number, fh: number;
  if (focus) {
    ({ x: fx, y: fy, w: fw, h: fh } = focus);
  } else if (marks.length) {
    fx = Math.min(...marks.map((m) => m.x));
    fy = Math.min(...marks.map((m) => m.y));
    fw = Math.max(...marks.map((m) => m.x + m.w)) - fx;
    fh = Math.max(...marks.map((m) => m.y + m.h)) - fy;
  } else {
    fx = 0;
    fy = 0;
    fw = srcWidth;
    fh = srcHeight;
  }

  // Padding around the control, so a circle never touches the frame edge and a
  // row's label stays with it.
  const PAD = Math.round(srcWidth * 0.06);
  const uw = (fw + 2 * PAD) * s;
  const uh = (fh + 2 * PAD) * s;

  // Zoom to the control, but never past the point where it still fits the
  // frame's safe width. Capped at 2.6 so a small toggle does not turn into a
  // pixel soup on a 1080-wide source.
  const zFits = fitsZoom(width, uw);
  const want = Math.min(width / uw, (height * 0.8) / uh);
  const Z = clamp(Math.min(want, zFits), 1, 2.6);

  // Settle into the zoom rather than cutting to it, so the viewer sees WHERE on
  // the screen the control lives before it fills the frame.
  const settle = easeOut(t / 0.7);
  const Zeased = 1 + (Z - 1) * settle;

  // Centre the focus, then keep the picture covering the frame: a phone
  // recording is taller than 9:16, so there is room to pan vertically but none
  // to spare horizontally once zoomed.
  const cx = (fx + fw / 2) * s;
  const cy = (fy + fh / 2) * s;
  const maxTx = Math.max(0, (dispW * Zeased - width) / 2);
  const maxTy = Math.max(0, (dispH * Zeased - height) / 2);
  const tx = clamp(-Zeased * (cx - dispW / 2), -maxTx, maxTx) * settle;
  const ty = clamp(-Zeased * (cy - dispH / 2), -maxTy, maxTy) * settle;

  const enter = spring({
    frame,
    fps,
    config: SPRING.enter,
    durationInFrames: 14,
  });

  const stroke = Math.max(6, srcWidth * 0.008);
  const glow = `drop-shadow(0 0 ${stroke * 2.4}px ${theme.accentSoft})`;

  const renderMark = (m: ScreenMark, i: number) => {
    const p = easeOut((t - m.at) / 0.5);
    if (p <= 0) return null;
    const common = {
      fill: "none" as const,
      stroke: theme.accent,
      strokeWidth: stroke,
      strokeLinecap: "round" as const,
      pathLength: 1,
      strokeDasharray: 1,
      strokeDashoffset: 1 - p,
    };
    if (m.kind === "circle") {
      return (
        <ellipse
          key={i}
          cx={m.x + m.w / 2}
          cy={m.y + m.h / 2}
          rx={m.w / 2 + stroke * 2.2}
          ry={m.h / 2 + stroke * 1.9}
          transform={`rotate(-4 ${m.x + m.w / 2} ${m.y + m.h / 2})`}
          {...common}
        />
      );
    }
    if (m.kind === "box") {
      return (
        <rect
          key={i}
          x={m.x - stroke}
          y={m.y - stroke}
          width={m.w + stroke * 2}
          height={m.h + stroke * 2}
          rx={stroke * 2.5}
          {...common}
        />
      );
    }
    if (m.kind === "underline") {
      const barH = Math.max(stroke, m.h * 0.16);
      return (
        <rect
          key={i}
          x={m.x}
          y={m.y + m.h + barH}
          width={m.w * p}
          height={barH}
          rx={barH / 2}
          fill={theme.accent}
        />
      );
    }
    // arrow: comes in from the right and lands beside the control, so the
    // finger-shaped gap on the left stays clear for a real thumb.
    const tipX = m.x + m.w + stroke * 2;
    const tipY = m.y + m.h / 2;
    const startX = tipX + Math.max(220, m.w * 1.4);
    const head = stroke * 3.2;
    return (
      <g key={i}>
        <path
          d={`M ${startX} ${tipY - m.h * 0.9} Q ${tipX + m.w * 0.5} ${tipY - m.h * 0.4} ${tipX} ${tipY}`}
          {...common}
        />
        {p > 0.8 && (
          <path
            d={`M ${tipX + head} ${tipY - head * 0.8} L ${tipX} ${tipY} L ${tipX + head} ${tipY + head * 0.8}`}
            fill="none"
            stroke={theme.accent}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity={easeOut((p - 0.8) / 0.2)}
          />
        )}
      </g>
    );
  };

  return (
    <AbsoluteFill style={{ background: theme.black, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          opacity: enter,
        }}
      >
        {/* The video and its marks are ONE transformed unit sharing a source
            coordinate space. Transform them separately and the circle drifts off
            the toggle as the zoom changes. */}
        <div
          style={{
            position: "relative",
            width: dispW,
            height: dispH,
            transform: `translate(${tx}px, ${ty}px) scale(${Zeased})`,
            transformOrigin: "50% 50%",
          }}
        >
          <OffthreadVideo
            src={staticFile(src)}
            startFrom={Math.round((from ?? 0) * fps)}
            muted
            style={{ width: "100%", height: "100%", display: "block" }}
          />
          <svg
            viewBox={`0 0 ${srcWidth} ${srcHeight}`}
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              filter: glow,
            }}
          >
            {marks.map(renderMark)}
          </svg>
        </div>
      </AbsoluteFill>

      {/* Lifted clear of the caption band. CaptionChips falls back to
          bottom=400 (y 0.79) and Credit defaults to y 0.78, so on a how-to step
          — which always carries a caption — the two print on top of each other.
          Seen in the first render of this component. */}
      {credit && <Credit text={credit} onMedia plate bottom={560} />}
    </AbsoluteFill>
  );
};

/** Where a step label may sit without meeting the platform's own furniture. */
export const STEP_LABEL_Y = SAFE_RECT.y0 + 0.02;
