import React from "react";
import { Credit } from "./Credit";
import {
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
  const { fps, width, height } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;

  const {
    src, srcWidth, srcHeight, lines, credit,
    tint = "#B7E4C7", follow = true, sweepSec = 0.28, film = false,
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
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            );
            if (p <= 0) return null;
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: l.x * scale,
                  top: l.y * scale,
                  width: l.w * scale * p,
                  height: l.h * scale,
                  background: tint,
                  // multiply keeps the words readable THROUGH the marker —
                  // a solid fill would cover the very text being proved
                  mixBlendMode: "multiply",
                  borderRadius: 3,
                }}
              />
            );
          })}
        </div>
      </AbsoluteFill>

      {/* was a hand-rolled credit at bottom: 26 — y 0.986, under Instagram's
          "Add comment" bar. The size check could not see it (24px is below
          display size); the hand-rolled-credit check did. */}
      {credit ? <Credit text={credit} onMedia plate /> : null}
    </AbsoluteFill>
  );
};
