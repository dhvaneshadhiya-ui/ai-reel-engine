import React from "react";
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
    const baseZ = Math.max(1.35, Math.min(2.2, fit));
    const push = interpolate(frame, [0, durationInFrames], [0, 0.05]);
    Z = baseZ + push;
  } else {
    // no highlights: gentle ken-burns on the whole page
    Z = 1.0 + interpolate(frame, [0, durationInFrames], [0.02, 0.06]);
    cx = cardW / 2;
    cy = cardH / 2;
  }

  // ease the pull-in from a slightly wider view over the first ~0.5s
  const settle = 1 - Math.pow(1 - Math.min(1, (frame / fps) / 0.5), 3);
  const Zeased = Z - (Z - Math.max(1.0, Z - 0.22)) * (1 - settle);

  // translate so the focus center lands at frame center (origin = card center)
  const tx = -Zeased * (cx - cardW / 2) * settle;
  const ty = -Zeased * (cy - cardH / 2) * settle;

  const enter = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 120, mass: 0.7 },
    durationInFrames: 18,
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
            durationInFrames: 12,
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
