import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";

export interface AnnotateZoomAnnotation {
  kind: "box" | "underline" | "circle" | "arrow";
  /** seconds from scene start when the annotation starts drawing */
  at: number;
  /** region in SOURCE pixels */
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface AnnotateZoomProps {
  /** screenshot under public/ */
  src: string;
  srcWidth: number;
  srcHeight: number;
  bg?: "cream" | "black";
  /** region (source px) the camera settles on; defaults to union of annotations */
  focus?: { x: number; y: number; w: number; h: number };
  annotations?: AnnotateZoomAnnotation[];
  credit?: string;
}

const clamp = (v: number, lo: number, hi: number) =>
  Math.max(lo, Math.min(hi, v));
const easeOut = (x: number) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);

/**
 * The premium screenshot treatment: the shot lives in a rounded themed card,
 * the camera starts slightly wide and eases in to frame the focus region big
 * and centered, and accent annotations (box / underline / circle / arrow)
 * DRAW ON at their cue with soft glow. Blurred enlarged self as bg fill.
 */
export const AnnotateZoom: React.FC<AnnotateZoomProps> = ({
  src,
  srcWidth,
  srcHeight,
  bg = "cream",
  focus,
  annotations = [],
  credit,
}) => {
  const theme = useTheme();
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dark = bg === "black";

  // ---- card geometry (card aspect == source aspect) ----
  const cardW = width * 0.9;
  const cardH = (srcHeight / srcWidth) * cardW;
  const s = cardW / srcWidth; // source px -> card px

  // ---- focus rect: explicit prop, else union of annotations, else full ----
  let fx: number, fy: number, fw: number, fh: number;
  if (focus) {
    ({ x: fx, y: fy, w: fw, h: fh } = focus);
  } else if (annotations.length) {
    let minX = Infinity,
      minY = Infinity,
      maxX = -Infinity,
      maxY = -Infinity;
    annotations.forEach((a) => {
      minX = Math.min(minX, a.x);
      minY = Math.min(minY, a.y);
      maxX = Math.max(maxX, a.x + a.w);
      maxY = Math.max(maxY, a.y + a.h);
    });
    fx = minX;
    fy = minY;
    fw = maxX - minX;
    fh = maxY - minY;
  } else {
    fx = 0;
    fy = 0;
    fw = srcWidth;
    fh = srcHeight;
  }

  // safe padding so card edges never slice a line of text mid-word
  const FPAD = 46;
  const uw = (fw + 2 * FPAD) * s;
  const uh = (fh + 2 * FPAD) * s;

  // fit the padded focus into a comfortable window of the 1080x1920 frame
  const fit = Math.min((cardW * 0.86) / uw, (cardH * 0.58) / uh);
  const baseZ = clamp(fit, 1.15, 2.4);
  const pushIn = interpolate(frame, [0, durationInFrames], [0, 0.05]);
  const Z = baseZ + pushIn;

  // settle from slightly wide to the focus framing over ~0.8s
  const settle = easeOut(t / 0.8);
  const Zeased = Z - (Z - Math.max(1.0, Z - 0.24)) * (1 - settle);

  // focus center in card px, clamped so the viewport stays inside the card
  // horizontally (no card edge cutting through the focused text)
  const halfVw = width / 2 / Zeased;
  let cx = (fx + fw / 2) * s;
  let cy = (fy + fh / 2) * s;
  if (cardW > 2 * halfVw) cx = clamp(cx, halfVw, cardW - halfVw);
  cy = clamp(cy, Math.min(cardH / 2, cardH * 0.18), cardH * 0.9);

  const tx = -Zeased * (cx - cardW / 2) * settle;
  const ty = -Zeased * (cy - cardH / 2) * settle;

  const enter = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 120, mass: 0.7 },
    durationInFrames: 18,
  });

  // ---- annotation drawing ----
  const stroke = Math.max(5, srcWidth * 0.0055);
  const glow = `drop-shadow(0 0 ${stroke * 2.2}px ${theme.accentSoft}) drop-shadow(0 0 ${stroke * 0.9}px ${theme.accentSoft})`;

  const renderAnnotation = (a: AnnotateZoomAnnotation, idx: number) => {
    const p = easeOut((t - a.at) / 0.55);
    if (p <= 0) return null;

    if (a.kind === "box") {
      const pad = stroke * 1.6;
      return (
        <rect
          key={idx}
          x={a.x - pad}
          y={a.y - pad}
          width={a.w + 2 * pad}
          height={a.h + 2 * pad}
          rx={stroke * 2}
          fill="none"
          stroke={theme.accent}
          strokeWidth={stroke}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - p}
        />
      );
    }

    if (a.kind === "underline") {
      const barH = clamp(a.h * 0.22, stroke, stroke * 2.6);
      return (
        <rect
          key={idx}
          x={a.x}
          y={a.y + a.h + barH * 0.6}
          width={a.w * p}
          height={barH}
          rx={barH / 2}
          fill={theme.accent}
        />
      );
    }

    if (a.kind === "circle") {
      const cxE = a.x + a.w / 2;
      const cyE = a.y + a.h / 2;
      const rx = a.w / 2 + stroke * 3;
      const ry = a.h / 2 + stroke * 2.4;
      return (
        <ellipse
          key={idx}
          cx={cxE}
          cy={cyE}
          rx={rx}
          ry={ry}
          fill="none"
          stroke={theme.accent}
          strokeWidth={stroke}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - p}
          transform={`rotate(-5 ${cxE} ${cyE})`}
        />
      );
    }

    // arrow: short curved accent arrow swooping in from the upper right,
    // tip landing just above the region
    const tipX = a.x + a.w / 2 + a.w * 0.1;
    const tipY = a.y - stroke * 3;
    const startX = tipX + Math.max(90, a.w * 0.6);
    const startY = tipY - Math.max(110, a.h * 3);
    const ctrlX = tipX + Math.max(100, a.w * 0.7);
    const ctrlY = tipY - Math.max(20, a.h * 0.8);
    const headLen = stroke * 3.6;
    return (
      <g key={idx}>
        <path
          d={`M ${startX} ${startY} Q ${ctrlX} ${ctrlY} ${tipX} ${tipY}`}
          fill="none"
          stroke={theme.accent}
          strokeWidth={stroke}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - p}
        />
        {p > 0.82 && (
          <path
            d={`M ${tipX + headLen * 0.9} ${tipY - headLen * 0.5} L ${tipX} ${tipY} L ${tipX + headLen * 0.75} ${tipY + headLen * 0.7}`}
            fill="none"
            stroke={theme.accent}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity={easeOut((p - 0.82) / 0.18)}
          />
        )}
      </g>
    );
  };

  return (
    <AbsoluteFill
      style={{
        background: dark ? theme.black : theme.cream,
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* blurred enlarged self as background fill */}
      <AbsoluteFill>
        <Img
          src={staticFile(src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: dark
              ? "blur(50px) brightness(0.4)"
              : "blur(50px) brightness(1.02) saturate(1.05)",
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
          width: cardW,
          height: cardH,
          position: "relative",
          borderRadius: theme.radius.card,
          overflow: "hidden",
          boxShadow: dark ? theme.shadow.cardOnDark : theme.shadow.card,
          opacity: enter,
          transform: `translate(${tx}px, ${ty + (1 - enter) * 40}px) scale(${Zeased})`,
          transformOrigin: "50% 50%",
        }}
      >
        <Img
          src={staticFile(src)}
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
          {annotations.map(renderAnnotation)}
        </svg>
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
