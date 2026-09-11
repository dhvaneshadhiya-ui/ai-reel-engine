import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

/**
 * Hand-drawn marks that DRAW ON when the word is spoken: underline, circle,
 * arrow. Added 2026-09-11, built from video-talkcraft's written descriptions of
 * ink-underline / scribble-annotation / hand-drawn-ellipse — our own code; its
 * code is non-commercial and was not read.
 *
 * What makes a mark read as a live hand rather than a printed rule:
 *   - ONE stroke, start to end, eased at pen-down and lift-off. A constant speed
 *     reads as a loading bar.
 *   - thick, round-capped ink. Much under ~5px at phone size it reads as a rule.
 *   - a circle is never a perfect ellipse: it wobbles and overshoots its start.
 *
 * Coordinates are SOURCE-image pixels, exactly like `lines`/`highlights`, and
 * `scale` maps them into whatever layer the marks sit in — so a mark rides a
 * scrolling page or a zooming receipt card instead of floating over it.
 */
export interface InkMark {
  kind: "underline" | "circle" | "arrow";
  /** seconds into the scene when the pen goes down — the spoken word */
  at: number;
  x: number;
  y: number;
  w: number;
  h: number;
  /** stroke colour; default INK_RED */
  color?: string;
  /** draw duration in seconds (default underline 0.4, circle 0.55, arrow 0.45) */
  dur?: number;
}

export const INK_RED = "#E5322D";
const DEFAULT_DUR = { underline: 0.4, circle: 0.55, arrow: 0.45 } as const;

function pathFor(m: InkMark, s: number): string {
  const x = m.x * s, y = m.y * s, w = m.w * s, h = m.h * s;
  if (m.kind === "underline") {
    const yb = y + h + 6; // just under the baseline, with a slight hand sag
    return `M ${x - 4} ${yb + 2} Q ${x + w * 0.5} ${yb - 4} ${x + w + 4} ${yb + 1}`;
  }
  if (m.kind === "circle") {
    // started near ten o'clock and carried past it; deterministic wobble
    const cx = x + w / 2, cy = y + h / 2, rx = w / 2 + 18, ry = h / 2 + 14;
    const N = 56, start = Math.PI * 1.15, sweep = Math.PI * 2.12;
    const pts: string[] = [];
    for (let i = 0; i <= N; i++) {
      const a = start + (sweep * i) / N;
      const wob = 1 + 0.035 * Math.sin(a * 3);
      pts.push(`${(cx + Math.cos(a) * rx * wob).toFixed(1)} ${(cy + Math.sin(a) * ry * wob).toFixed(1)}`);
    }
    return "M " + pts.join(" L ");
  }
  // arrow: a curved shaft toward the box, then a two-stroke head. It comes in
  // from whichever side has room, so it never starts off the page.
  const fromRight = x < 180;
  const dir = fromRight ? -1 : 1;
  const tx = fromRight ? x + w + 10 : x - 10;
  const ty = y + h / 2;
  const sx = tx - dir * 150, sy = ty + 110;
  const hx = tx - dir * 34;
  return `M ${sx} ${sy} Q ${tx - dir * 90} ${ty + 10} ${tx} ${ty} ` +
         `M ${hx} ${ty - 14} L ${tx} ${ty} L ${tx - dir * 18} ${ty + 32}`;
}

export const InkMarks: React.FC<{
  marks?: InkMark[];
  /** source px -> layer px */
  scale: number;
  stroke?: number;
}> = ({ marks, scale, stroke = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!marks || !marks.length) return null;
  const t = frame / fps;
  return (
    <svg
      width={1}
      height={1}
      style={{ position: "absolute", left: 0, top: 0, overflow: "visible", zIndex: 2, pointerEvents: "none" }}
    >
      {marks.map((m, i) => {
        const d = m.dur ?? DEFAULT_DUR[m.kind];
        const p = interpolate(t, [m.at, m.at + d], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.inOut(Easing.quad),
        });
        if (p <= 0) return null;
        return (
          <path
            key={i}
            d={pathFor(m, scale)}
            pathLength={1}
            fill="none"
            stroke={m.color ?? INK_RED}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray="1 1"
            strokeDashoffset={1 - p}
          />
        );
      })}
    </svg>
  );
};
