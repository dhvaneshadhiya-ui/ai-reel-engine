import React from "react";
import { InkMarks, type InkMark } from "./InkMarks";
import { SPRING } from "../theme/motion";
import { Credit } from "./Credit";
import {
  spring,
  Easing,
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { useTheme } from "../theme/tokens";

/**
 * SOURCE READ-ALONG — the primary source on screen with the exact sentence
 * highlighted as the voice-over reaches it.
 *
 * This is the strongest receipt the engine has: instead of asserting a claim
 * and cutting to a card, the viewer watches the claim appear in the source
 * document itself, marker sweeping across the line being spoken.
 *
 * WHEN TO USE IT (judgement — see RULES.md §5):
 *   YES — a text-dense portrait-friendly artefact (article body, paper,
 *         filing, changelog) where the VO closely tracks the passage, and the
 *         claim is load-bearing enough to be worth proving.
 *   NO  — a wide screenshot (use `floatcard`), an image-led page, a passage
 *         the VO only loosely paraphrases, or a claim nobody would dispute.
 *         Over-used it becomes a wall of small text, which is the failure this
 *         engine already has rules against.
 *
 * `lines` are rects in SOURCE-IMAGE pixel coordinates, each with the second it
 * lands. Highlights ACCUMULATE — earlier lines stay marked, so the frame shows
 * how far the read has got, exactly like the reference.
 */
export interface SourceReadProps {
  src: string;
  srcWidth: number;
  srcHeight: number;
  lines: { at: number; x: number; y: number; w: number; h: number }[];
  credit?: string;
  /** highlight colour; defaults to the reference's mint */
  tint?: string;
  /** keep the active line in view on a page taller than the frame */
  follow?: boolean;
  /** seconds each highlight takes to sweep across (default 0.28) */
  sweepSec?: number;
  /**
   * FILM THE PAGE, don't paste it (2026-09-11, idea from video-talkcraft;
   * our own implementation — its code is non-commercial). Instead of jumping
   * to each line and holding still until the next, the page keeps moving:
   * it glides onto the first line, ARRIVES on each line as that line lands
   * (decelerating, so the eye catches it as the sweep starts), holds briefly,
   * travels to the next, and drifts on after the last. whatsapp-agents spent
   * 41% of its runtime in sourceread and measured 61% near-static.
   */
  film?: boolean;
  /**
   * DIM THE REST (2026-09-11, talkcraft's focus-dim-spotlight / highlighter
   * rule): the line being read stays lit and everything else goes dark, the
   * lit band sliding from line to line and restoring as the scene ends. A
   * highlight with nothing subtracted around it is half an emphasis.
   */
  dimRest?: boolean;
  /** hand-drawn underline / circle / arrow, drawn on at `at` (see InkMarks) */
  marks?: InkMark[];
  /**
   * MAGNIFIER for the one number the voice reads out (2026-09-11). A round
   * lens lands in empty space, pixel-true to the source, the page dims, and a
   * line points back to where it came from. Source-px box; zoom default 1.8.
   */
  magnify?: { at: number; x: number; y: number; w: number; h: number; zoom?: number; until?: number };
}

// film mode — every number is a fraction of the frame, so it scales with it
const FILM_ENTRY = 0.06;    // the page arrives from this far below its first stop
const FILM_DRIFT = 0.03;    // per second, after the last stop
const FILM_HOLD_MAX = 0.5;  // s; a hold never takes more than 40% of a gap

function filmY(t: number, stops: { at: number; y: number }[], h: number,
               clampY: (y: number) => number): number {
  const glide = Easing.inOut(Easing.cubic);
  const first = stops[0];
  if (t <= first.at) {
    if (first.at <= 0.05) return first.y;
    const from = clampY(first.y + FILM_ENTRY * h);
    return from + (first.y - from) * Easing.out(Easing.cubic)(t / first.at);
  }
  for (let i = 0; i < stops.length - 1; i++) {
    const a = stops[i], b = stops[i + 1];
    if (t < b.at) {
      const hold = Math.min(FILM_HOLD_MAX, 0.4 * (b.at - a.at));
      if (t <= a.at + hold) return a.y;
      const k = (t - a.at - hold) / Math.max(1e-6, b.at - a.at - hold);
      return a.y + (b.y - a.y) * glide(Math.min(1, k));
    }
  }
  const last = stops[stops.length - 1];
  if (t <= last.at + FILM_HOLD_MAX) return last.y;
  return clampY(last.y - FILM_DRIFT * h * (t - last.at - FILM_HOLD_MAX));
}

export const SourceRead: React.FC<{ scene: SourceReadProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const sceneDur = durationInFrames / fps;
  const theme = useTheme();
  const t = frame / fps;

  const {
    src, srcWidth, srcHeight, lines, credit,
    // sweep 0.45s, was 0.28 — talkcraft's highlighter card measures under 0.3s
    // as "looks like a render bug" and 0.4-0.8 as a pen following the voice.
    tint = "#B7E4C7", follow = true, sweepSec = 0.45, film = false,
    dimRest = false, marks, magnify,
  } = scene;

  // fit to frame WIDTH — the page stays at reading size, never zoomed. A
  // document that needs zooming to read is the wrong asset for this treatment.
  const scale = width / srcWidth;
  const pageH = srcHeight * scale;

  // slow push-in so the frame is never static (universal rule)
  const zoom = 1 + Math.min(t, 8) * 0.004;

  // follow the read: keep the newest landed line ~58% down the frame.
  //
  // 2026-08-14: this used to compute one offset and hand the smoothing to a
  // CSS `transition`. Remotion does not render CSS transitions or animations
  // (remotion-markup), so the scroll HARD JUMPED between lines — and the
  // `interpolate(frame, [0,1], [offsetY, offsetY])` beneath it interpolated a
  // value to itself, which is a no-op. The comment claimed a glide the code
  // never produced. It is now eased in frame-space, which is the only kind of
  // motion that survives a render.
  const offsetFor = (l?: { y: number; h: number }) => {
    if (!follow || pageH <= height || !l) return 0;
    const target = (l.y + l.h / 2) * scale - height * 0.58;
    return -Math.max(0, Math.min(pageH - height, target));
  };
  const landed = lines.filter((l) => l.at <= t);
  const idx = landed.length ? landed.length - 1 : 0;
  const active = landed.length ? landed[idx] : lines[0];
  const prev = idx > 0 ? landed[idx - 1] : active;

  const SCROLL_SEC = 0.45;
  const p = active
    ? interpolate(t, [active.at, active.at + SCROLL_SEC], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: Easing.out(Easing.cubic),
      })
    : 1;
  const clampY = (y: number) => Math.max(-(pageH - height), Math.min(0, y));
  const ordered = [...lines].sort((a, b) => a.at - b.at);
  const smoothY = film && follow && pageH > height && ordered.length
    ? filmY(t, ordered.map((l) => ({ at: l.at, y: offsetFor(l) })), height, clampY)
    : offsetFor(prev) + (offsetFor(active) - offsetFor(prev)) * p;

  // ── dim the rest ────────────────────────────────────────────────────────
  let dimEls: React.ReactNode = null;
  if (dimRest && landed.length && ordered.length) {
    const band = (l: { y: number; h: number }) => [l.y * scale - 12, (l.y + l.h) * scale + 12];
    const [a0, a1] = band(active), [b0, b1] = band(prev);
    const q = interpolate(t, [active.at, active.at + 0.22], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic),
    });
    const top = b0 + (a0 - b0) * q, bot = b1 + (a1 - b1) * q;
    const on = interpolate(t, [ordered[0].at, ordered[0].at + 0.25], [0, 1], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const off = interpolate(t, [sceneDur - 0.35, sceneDur], [1, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const o = 0.46 * Math.min(on, off);
    dimEls = (
      <>
        <div style={{ position: "absolute", left: 0, top: 0, width, height: Math.max(0, top),
          background: "linear-gradient(to bottom, rgb(8,9,12) calc(100% - 24px), transparent)", opacity: o }} />
        <div style={{ position: "absolute", left: 0, top: bot, width, height: Math.max(0, pageH - bot),
          background: "linear-gradient(to top, rgb(8,9,12) calc(100% - 24px), transparent)", opacity: o }} />
      </>
    );
  }

  // ── magnifier ───────────────────────────────────────────────────────────
  let lens: React.ReactNode = null;
  if (magnify && t >= magnify.at) {
    const until = magnify.until ?? sceneDur - 0.25;
    const inP = spring({ frame: Math.max(0, frame - Math.round(magnify.at * fps)), fps,
                         config: SPRING.pop, durationInFrames: 12 });
    const outP = interpolate(t, [until, until + 0.22], [1, 0], {
      extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const vis = Math.min(inP, outP);
    if (vis > 0.001) {
      // where the box is ON SCREEN: the page layer is translateY(smoothY)
      // scale(zoom) about 50% 40%, so p' = o + zoom * (p - o) + (0, smoothY)
      const ox = width * 0.5, oy = height * 0.4;
      const sxy = (px: number, py: number) =>
        [ox + zoom * (px * scale - ox), oy + zoom * (py * scale - oy) + smoothY];
      const [bx0, by0] = sxy(magnify.x, magnify.y);
      const [bx1, by1] = sxy(magnify.x + magnify.w, magnify.y + magnify.h);
      const tcx = (bx0 + bx1) / 2, tcy = (by0 + by1) / 2;
      const D = width * 0.44;
      // never wider than the lens: a clipped box shows half a word (seen on
      // the first stills, 2026-09-11). G63 advises when this leaves ~no zoom.
      const zl = Math.min(magnify.zoom ?? 1.8, (D * 0.9) / Math.max(1, bx1 - bx0));
      const above = tcy > height * 0.45;          // land in empty space
      const lcx = Math.max(D / 2 + 40, Math.min(width - D / 2 - 40, tcx));
      const lcy = Math.max(height * 0.06 + D / 2,
                  Math.min(height * 0.8 - D / 2, above ? tcy - height * 0.3 : tcy + height * 0.3));
      const k = scale * zoom * zl;                // source px -> lens px
      const scan = 7 * Math.sin(t * 1.4);         // keep-alive: a lens never sits as a sticker
      const imgLeft = D / 2 - (magnify.x + magnify.w / 2) * k + scan;
      const imgTop = D / 2 - (magnify.y + magnify.h / 2) * k;
      const ax = tcx, ay = above ? by0 : by1;     // connector: box edge -> lens rim
      const ang = Math.atan2(lcy - ay, lcx - ax);
      const ex = lcx - Math.cos(ang) * (D / 2), ey = lcy - Math.sin(ang) * (D / 2);
      lens = (
        <>
          <AbsoluteFill style={{ background: "rgba(8,9,12,0.42)", opacity: vis }} />
          <div style={{ position: "absolute", left: bx0 - 6, top: by0 - 6,
            width: bx1 - bx0 + 12, height: by1 - by0 + 12, border: "3px solid #fff",
            borderRadius: 10, opacity: vis }} />
          <svg width={width} height={height} style={{ position: "absolute", left: 0, top: 0, opacity: vis }}>
            <line x1={ax} y1={ay} x2={ex} y2={ey} stroke="#fff" strokeWidth={3} strokeLinecap="round" />
          </svg>
          <div style={{ position: "absolute", left: lcx - D / 2, top: lcy - D / 2, width: D, height: D,
            borderRadius: "50%", overflow: "hidden", border: "5px solid #fff", background: theme.cream,
            boxShadow: "0 24px 60px rgba(0,0,0,0.55)", opacity: vis,
            transform: `scale(${0.6 + 0.4 * vis})` }}>
            <Img src={staticFile(src)} style={{ position: "absolute", left: imgLeft, top: imgTop,
              width: srcWidth * k, height: srcHeight * k, maxWidth: "none" }} />
          </div>
        </>
      );
    }
  }

  return (
    <AbsoluteFill style={{ background: theme.cream, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transform: `translateY(${smoothY}px) scale(${zoom})`,
          transformOrigin: "50% 40%",
        }}
      >
        <div style={{ position: "relative", width, height: pageH }}>
          <Img
            src={staticFile(src)}
            style={{ width, height: pageH, display: "block" }}
          />
          {lines.map((l, i) => {
            const p = interpolate(
              t, [l.at, l.at + sweepSec], [0, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp",
                easing: Easing.inOut(Easing.quad) }   // pen-down, pen-up
            );
            if (p <= 0) return null;
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: l.x * scale - 4,
                  top: l.y * scale,
                  width: (l.w * scale + 8) * p,
                  height: l.h * scale,
                  background: tint,
                  // multiply keeps the words readable THROUGH the marker —
                  // a solid fill would cover the very text being proved
                  mixBlendMode: "multiply",
                  // irregular corners read as a marker stroke, not a box
                  borderRadius: "10px 4px 8px 3px / 6px 10px 4px 8px",
                }}
              />
            );
          })}
          {dimEls}
          <InkMarks marks={marks} scale={scale} />
        </div>
      </AbsoluteFill>
      {lens}

      {/* was a hand-rolled credit at bottom: 26 — y 0.986, under Instagram's
          "Add comment" bar. The size check could not see it (24px is below
          display size); the hand-rolled-credit check did. */}
      {credit ? <Credit text={credit} onMedia plate /> : null}
    </AbsoluteFill>
  );
};
