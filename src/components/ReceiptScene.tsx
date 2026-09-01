import React from "react";
import { SPRING, DUR } from "../theme/motion";
import { Credit } from "./Credit";
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
import { fitsZoom } from "../safeArea";
import type { Scene } from "../types";

type ReceiptProps = Extract<Scene, { type: "receipt" }>;

/**
 * The signature "receipt" scene: a screenshot (tweet / article / GitHub /
 * spec sheet) on a cream or black backdrop. It does a FOCUS PULL — panning and
 * zooming onto each highlight (or cluster of nearby highlights) as it fires, so
 * the highlighted phrase fills the frame instead of getting lost in a wall of
 * text. Highlight boxes still sweep on phrase-by-phrase, synced to the VO.
 */
export const ReceiptScene: React.FC<{ scene: ReceiptProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  const theme = useTheme();
  const backdrop = scene.backdrop ?? "black";
  const bg = backdrop === "cream" ? theme.cream : theme.black;

  // Card sizing: fit screenshot into ~86% width, keep aspect
  const cardW = width * 0.86;
  const cardH = (scene.srcHeight / scene.srcWidth) * cardW;
  const sx = cardW / scene.srcWidth;
  const sy = cardH / scene.srcHeight;

  const hls = scene.highlights ?? [];

  // --- Steady focus on the union of THIS scene's highlights ---
  // Frame the highlighted region big and centered for the whole scene (so the
  // relevant words dominate, not the surrounding wall of text), with a gentle
  // push-in. The highlight boxes still sweep on at their cue.
  let Z: number, cx: number, cy: number;
  let zFits = Infinity; // no ceiling needed on the unzoomed ken-burns path
  if (hls.length) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    hls.forEach((o) => {
      minX = Math.min(minX, o.x);
      minY = Math.min(minY, o.y);
      maxX = Math.max(maxX, o.x + o.w);
      maxY = Math.max(maxY, o.y + o.h);
    });
    const pad = 34;
    const uw = (maxX - minX + 2 * pad) * sx;
    const uh = (maxY - minY + 2 * pad) * sy;
    cx = ((minX + maxX) / 2) * sx;
    cy = ((minY + maxY) / 2) * sy;
    // fit the union to ~88% width / ~55% height, whichever is tighter
    const fit = Math.min((cardW * 0.88) / uw, (cardH * 0.55) / uh);
    // A DOCUMENT MAY BE CROPPED VERTICALLY, NEVER HORIZONTALLY.
    //
    // You can read a page whose bottom is off-screen; you cannot read a line
    // whose beginning is. Rendered 2026-08-18: the mr-pricing receipt at the
    // 1.35 floor put the card 1254px wide inside a 1080px frame and served
    // "ple analyst Ming-Chi Kuo believes that Ap" — 87px sliced off each side,
    // mid-word, on a scene whose entire job is to let the viewer read the
    // claim. zFits below was supposed to prevent exactly this and could not:
    // it measures the HIGHLIGHT union against the frame, and a highlight can
    // sit comfortably inside a card that is itself hanging off both edges.
    const cardFits = width / cardW;
    // HARD CEILING — see AnnotateZoom for the full story. The 1.35 floor is an
    // aesthetic minimum and must never beat the zoom at which the padded
    // highlight union still spans the frame; a floor that wins slices the
    // highlighted words off BOTH edges. 1.35 is harsher than AnnotateZoom's
    // 1.15, so this path cuts even more when it fires.
    // The 1.35 floor is an aesthetic minimum — "don't show a page tiny" — and
    // it yields to both ceilings. An aesthetic minimum that beats a legibility
    // ceiling is not a minimum, it is a bug with a comment.
    zFits = Math.min(fitsZoom(width, uw), cardFits);
    const baseZ = Math.min(Math.max(1.35, Math.min(2.2, fit)), zFits);
    const push = interpolate(frame, [0, durationInFrames], [0, 0.05]);
    Z = Math.min(baseZ + push, zFits);
  } else {
    // No highlights: ken-burns the whole page. Was [0.02, 0.06] — a 4% push,
    // the flattest move in the codebase, on the one scene type that holds a
    // full-page screenshot for 6-9s. It read as a still. 57% of receipts
    // across the reels have no highlights (compile_shot_plan never sets any),
    // so this fallback IS the treatment for most screenshots, not an edge case.
    // Matched to FootageScene's house push (base -> base * 1.1) rather than a
    // new invented number.
    Z = 1.0 + interpolate(frame, [0, durationInFrames], [0.0, 0.1]);
    cx = cardW / 2;
    cy = cardH / 2;
  }

  // ease the pull-in from a slightly wider view over the first ~0.5s
  const settle = 1 - Math.pow(1 - Math.min(1, (frame / fps) / 0.5), 3);
  const Zeased = Z - (Z - Math.max(1.0, Z - 0.22)) * (1 - settle);

  // translate so the focus center lands at frame center (origin = card center)
  const tx0 = -Zeased * (cx - cardW / 2) * settle;
  const ty = -Zeased * (cy - cardH / 2) * settle;

  // When the card fits the frame at this zoom, keep it fully inside: panning to
  // centre the highlight could otherwise hang a card edge, and its text, off
  // the side. Pan freely only when the card really is wider than the frame.
  const onScreenW = cardW * Zeased;
  const slackX = Math.max(0, (width - onScreenW) / 2);
  const tx = onScreenW <= width
    ? Math.max(-slackX, Math.min(slackX, tx0))
    : tx0;

  const enter = spring({
    frame,
    fps,
    config: SPRING.enter,
    durationInFrames: DUR.base,
  });

  return (
    <AbsoluteFill
      style={{
        background: bg,
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* blurred fill of the receipt itself — no dead space around the card */}
      <AbsoluteFill>
        <Img
          src={staticFile(scene.src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter:
              backdrop === "cream"
                ? "blur(48px) brightness(1.02) saturate(1.05)"
                : "blur(48px) brightness(0.42)",
            transform: "scale(1.35)",
          }}
        />
      </AbsoluteFill>
      <div
        style={{
          width: cardW,
          height: cardH,
          position: "relative",
          borderRadius: 24,
          overflow: "hidden",
          boxShadow:
            backdrop === "cream"
              ? "0 30px 80px rgba(0,0,0,0.25)"
              : "0 30px 80px rgba(0,0,0,0.8)",
          opacity: enter,
          transform: `translate(${tx}px, ${ty + (1 - enter) * 40}px) scale(${Zeased})`,
          transformOrigin: "50% 50%",
        }}
      >
        <Img
          src={staticFile(scene.src)}
          style={{ width: "100%", height: "100%" }}
        />
        {hls.map((h, idx) => {
          const local = Math.round((t - h.at) * fps);
          if (local < 0) return null;
          const sweep = spring({
            frame: local,
            fps,
            config: { damping: 20, stiffness: 200, mass: 0.5 },
            durationInFrames: DUR.base,
          });
          // Highlights must never obscure the data: cream keeps the classic
          // yellow marker tint (multiply never hides text); dark backdrops get
          // a stroked accent box + faint tint — NO difference blend (it used
          // to invert the row into an unreadable black bar).
          const pad = 6;
          return backdrop === "cream" ? (
            <div
              key={idx}
              style={{
                position: "absolute",
                left: h.x * sx,
                top: h.y * sy,
                width: h.w * sx * sweep,
                height: h.h * sy,
                background: "rgba(255, 228, 94, 0.55)",
                mixBlendMode: "multiply",
                borderRadius: 4,
              }}
            />
          ) : (
            <div
              key={idx}
              style={{
                position: "absolute",
                left: h.x * sx - pad,
                top: h.y * sy - pad,
                width: (h.w * sx + 2 * pad) * sweep,
                height: h.h * sy + 2 * pad,
                background: theme.accentSoft,
                border: `4px solid ${theme.accent}f2`,
                borderRadius: 8,
                boxShadow: `0 0 24px ${theme.accent}59`,
              }}
            />
          );
        })}
      </div>
      {scene.credit && <Credit text={scene.credit} />}
    </AbsoluteFill>
  );
};
