import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { useTheme } from "../theme/tokens";

export interface ParticleBurstProps {
  /** burst moment, in seconds from the start of the composition */
  at: number;
  /** burst center in px of the 1080x1920 frame (default mid-frame) */
  origin?: { x: number; y: number };
  count?: number;
  /** "accent" = theme accent + cream + ink tones; "multi" adds 2 rotated hues */
  palette?: "accent" | "multi";
  kind?: "confetti" | "sparks";
  seed?: number;
}

/** deterministic PRNG */
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** rotate a hex color's hue by deg (keeps s/l) — used to derive "multi" hues */
const rotateHue = (hex: string, deg: number): string => {
  const h = hex.replace("#", "");
  const n = parseInt(h, 16);
  const r = ((n >> 16) & 255) / 255;
  const g = ((n >> 8) & 255) / 255;
  const b = (n & 255) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const l = (max + min) / 2;
  const d = max - min;
  let hue = 0;
  const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));
  if (d !== 0) {
    if (max === r) hue = 60 * (((g - b) / d) % 6);
    else if (max === g) hue = 60 * ((b - r) / d + 2);
    else hue = 60 * ((r - g) / d + 4);
  }
  hue = (((hue + deg) % 360) + 360) % 360;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const xx = c * (1 - Math.abs(((hue / 60) % 2) - 1));
  const m = l - c / 2;
  let rr = 0;
  let gg = 0;
  let bb = 0;
  if (hue < 60) [rr, gg, bb] = [c, xx, 0];
  else if (hue < 120) [rr, gg, bb] = [xx, c, 0];
  else if (hue < 180) [rr, gg, bb] = [0, c, xx];
  else if (hue < 240) [rr, gg, bb] = [0, xx, c];
  else if (hue < 300) [rr, gg, bb] = [xx, 0, c];
  else [rr, gg, bb] = [c, 0, xx];
  const to255 = (v: number) =>
    Math.round((v + m) * 255)
      .toString(16)
      .padStart(2, "0");
  return `#${to255(rr)}${to255(gg)}${to255(bb)}`;
};

/**
 * Deterministic celebration overlay. At `at` seconds, N particles burst from
 * origin with seeded velocities, gravity, drag, rotation and fade over ~1.2s.
 * Pure math per frame — same seed → identical render. Composite over any
 * scene (transparent, pointer-events none).
 */
export const ParticleBurst: React.FC<ParticleBurstProps> = ({
  at,
  origin,
  count = 80,
  palette = "accent",
  kind = "confetti",
  seed = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const th = useTheme();

  const ox = origin?.x ?? width / 2;
  const oy = origin?.y ?? height / 2;

  const tSec = frame / fps - at;
  if (tSec < 0 || tSec > 1.5) return null;

  const colors =
    kind === "sparks"
      ? [th.accent]
      : palette === "multi"
        ? [th.accent, th.cream, th.ink, rotateHue(th.accent, -35), rotateHue(th.accent, -70)]
        : [th.accent, th.accent, th.cream, th.ink];

  const rnd = mulberry32((seed * 7919 + 1) >>> 0);
  const gravity = kind === "sparks" ? 1500 : 2100;
  const drag = kind === "sparks" ? 3.4 : 2.6;

  const parts: React.ReactNode[] = [];
  for (let i = 0; i < count; i++) {
    // draw all params up-front so every particle is stable across frames
    const angle = rnd() * Math.PI * 2;
    const upBias = -(0.35 + rnd() * 0.5); // shove the cone upward
    const speed = (kind === "sparks" ? 1300 : 950) * (0.45 + rnd() * 0.9);
    const vx = Math.cos(angle) * speed;
    const vy = (Math.sin(angle) * 0.75 + upBias) * speed;
    const life = kind === "sparks" ? 0.45 + rnd() * 0.4 : 0.85 + rnd() * 0.5;
    const rotSpeed = (rnd() - 0.5) * 900;
    const rot0 = rnd() * 360;
    const w = 12 + rnd() * 12;
    const h = 7 + rnd() * 6;
    const flutter = 4 + rnd() * 5; // confetti tumble frequency
    const color = colors[Math.floor(rnd() * colors.length)];

    const p = tSec / life;
    if (p >= 1) continue;

    // closed-form drag + gravity (deterministic per frame)
    const f = (1 - Math.exp(-drag * tSec)) / drag;
    const px = ox + vx * f;
    const py = oy + vy * f + 0.5 * gravity * tSec * tSec;
    const fade =
      p < 0.6 ? 1 : Math.max(0, 1 - (p - 0.6) / 0.4);

    if (kind === "sparks") {
      // streak along current velocity direction
      const cvx = vx * Math.exp(-drag * tSec);
      const cvy = vy * Math.exp(-drag * tSec) + gravity * tSec;
      const dir = (Math.atan2(cvy, cvx) * 180) / Math.PI;
      const len = Math.min(150, Math.hypot(cvx, cvy) * 0.09) + 10;
      parts.push(
        <div
          key={i}
          style={{
            position: "absolute",
            left: px,
            top: py,
            width: len,
            height: 4.5,
            borderRadius: 999,
            background: `linear-gradient(90deg, transparent, ${color})`,
            opacity: fade,
            transform: `translate(-100%, -50%) rotate(${dir}deg)`,
            transformOrigin: "100% 50%",
          }}
        />
      );
    } else {
      const tumble = Math.cos(tSec * flutter + rot0); // paper flip
      parts.push(
        <div
          key={i}
          style={{
            position: "absolute",
            left: px,
            top: py,
            width: w,
            height: h,
            borderRadius: 2.5,
            background: color,
            opacity: fade,
            transform: `translate(-50%, -50%) rotate(${
              rot0 + rotSpeed * tSec
            }deg) scaleY(${0.15 + Math.abs(tumble) * 0.85})`,
          }}
        />
      );
    }
  }

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>{parts}</AbsoluteFill>
  );
};
