import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export type MascotMotion = "bob" | "hop" | "spin" | "walk";

export interface PixelMascotProps {
  /** path under public/, e.g. "assets/dev/mascot.png" */
  src: string;
  /** rendered sprite width in px (default 320) */
  size?: number;
  /** center of the sprite, in px of the 1080x1920 frame */
  x: number;
  y: number;
  motion?: MascotMotion;
  /** motion speed multiplier (default 1) */
  speed?: number;
  /** mirror horizontally */
  flip?: boolean;
}

/**
 * Animated pixel-art garnish sprite (Nick's orange robot energy). Positioned
 * absolutely, meant to be overlaid on cards/scenes. All motion is pure
 * frame math — deterministic renders.
 */
export const PixelMascot: React.FC<PixelMascotProps> = ({
  src,
  size = 320,
  x,
  y,
  motion = "bob",
  speed = 1,
  flip = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (frame / fps) * speed;

  let dx = 0;
  let dy = 0;
  let rot = 0;
  let scaleX = 1;
  let scaleY = 1;
  /** 0..1 — how far off the ground (drives the contact shadow) */
  let air = 0;

  switch (motion) {
    case "bob": {
      const w = Math.sin(t * Math.PI * 2 * 0.55);
      dy = w * 12;
      rot = Math.sin(t * Math.PI * 2 * 0.55 + 0.9) * 2.2;
      air = (w + 1) / 2;
      break;
    }
    case "hop": {
      const period = 1.15;
      const p = ((t % period) + period) % period / period; // 0..1
      if (p < 0.18) {
        // anticipation squash
        const s = Math.sin((p / 0.18) * Math.PI);
        scaleY = 1 - 0.14 * s;
        scaleX = 1 + 0.1 * s;
      } else if (p < 0.72) {
        // airborne — parabolic arc with slight stretch
        const q = (p - 0.18) / 0.54;
        const arc = Math.sin(q * Math.PI);
        dy = -arc * size * 0.34;
        air = arc;
        scaleY = 1 + 0.07 * arc;
        scaleX = 1 - 0.05 * arc;
        rot = Math.sin(q * Math.PI) * 4;
      } else {
        // landing squash, recover
        const q = (p - 0.72) / 0.28;
        const s = Math.sin(q * Math.PI);
        scaleY = 1 - 0.1 * s;
        scaleX = 1 + 0.08 * s;
      }
      break;
    }
    case "spin": {
      rot = t * 60; // slow, continuous
      dy = Math.sin(t * Math.PI * 2 * 0.4) * 8;
      air = 0.5;
      break;
    }
    case "walk": {
      const stride = 3.2; // steps per second-ish waddle
      dx = Math.sin(t * Math.PI * 2 * 0.16) * size * 0.35;
      dy = -Math.abs(Math.sin(t * Math.PI * stride)) * size * 0.045;
      rot = Math.sin(t * Math.PI * stride) * 3.5;
      // face the direction of travel
      const dir = Math.cos(t * Math.PI * 2 * 0.16) >= 0 ? 1 : -1;
      scaleX = dir;
      air = Math.abs(Math.sin(t * Math.PI * stride)) * 0.3;
      break;
    }
  }

  if (flip) scaleX *= -1;

  const shadowW = size * 0.52 * (1 - air * 0.35);
  const shadowOpacity = 0.18 * (1 - air * 0.6);

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: 0,
        height: 0,
        pointerEvents: "none",
      }}
    >
      {/* contact shadow */}
      <div
        style={{
          position: "absolute",
          left: dx - shadowW / 2,
          top: size * 0.52,
          width: shadowW,
          height: size * 0.09,
          borderRadius: "50%",
          background: `rgba(0,0,0,${shadowOpacity})`,
          filter: "blur(6px)",
        }}
      />
      <Img
        src={staticFile(src)}
        style={{
          position: "absolute",
          left: -size / 2,
          top: -size / 2,
          width: size,
          height: size,
          imageRendering: "pixelated",
          transform: `translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(${scaleX}, ${scaleY})`,
          transformOrigin: "50% 60%",
        }}
      />
    </div>
  );
};
