import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useTheme } from "../theme/tokens";
import { Credit } from "./Credit";

/**
 * ONE NUMBER, ROLLED UP — `type: "counter"`. Added 2026-09-11, built from
 * video-talkcraft's number-counter description (our own code).
 *
 * Pasted onto the screen a number is merely seen; rolled up from zero the
 * viewer counts along and FEELS the size. The rules that make it land:
 *   - fast then slow (ease-out), so the final digits are readable — a linear
 *     roll is still flipping digits when it stops;
 *   - one pulse on landing (1 -> 1.08 -> 1): "this is the number";
 *   - never longer than ~1.5s, or it is still moving after the sentence ends;
 *   - fixed-width digits, so the number does not jitter as it rolls.
 * The label is the noun and the source is the receipt: G55 refuses a counter
 * with no numeric `value` or no `label`, and G15 refuses one with no `source`.
 */
export interface CounterProps {
  value: number;
  /** start of the roll, default 0 */
  from?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  /** what the number counts — required */
  label: string;
  /** seconds into the scene the roll starts (default 0.2) */
  at?: number;
  /** roll duration in seconds (default 1.3) */
  rollSec?: number;
  bg?: "black" | "cream";
  /** who reported the number — required by G15 */
  source?: string;
}

export const CounterScene: React.FC<{ scene: CounterProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;

  const {
    value, from = 0, decimals = 0, prefix = "", suffix = "", label,
    at = 0.2, rollSec = 1.3, bg = "black", source,
  } = scene;
  const dark = bg === "black";

  const p = interpolate(t, [at, at + rollSec], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const v = from + (value - from) * p;
  const fmt = (n: number) =>
    n.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  const shown = `${prefix}${fmt(v)}${suffix}`;
  const finalText = `${prefix}${fmt(value)}${suffix}`;

  // one pulse on landing
  const k = Math.max(0, Math.min(1, (t - (at + rollSec)) / 0.27));
  const pulse = 1 + 0.08 * Math.sin(Math.PI * k);
  // and never static: a slow push across the whole scene
  const push = 1 + 0.04 * (frame / Math.max(1, durationInFrames));

  // sized off the FINAL string so the number does not grow as it rolls
  const numSize = Math.min(width * 0.26, (width * 0.86) / (finalText.length * 0.6));
  const labelIn = interpolate(t, [at + rollSec * 0.6, at + rollSec * 0.6 + 0.3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: dark ? theme.black : theme.cream }}>
      <AbsoluteFill
        style={{
          transform: `scale(${push})`,
          alignItems: "center",
          justifyContent: "center",
          paddingBottom: height * 0.12,
        }}
      >
        <div
          style={{
            fontFamily: theme.serif,
            fontWeight: 800,
            fontSize: numSize,
            lineHeight: 1,
            letterSpacing: -2,
            fontVariantNumeric: "tabular-nums",
            color: dark ? theme.accentOnDark : theme.accentInk,
            transform: `scale(${pulse})`,
            whiteSpace: "nowrap",
          }}
        >
          {shown}
        </div>
        <div
          style={{
            marginTop: height * 0.025,
            maxWidth: width * 0.84,
            textAlign: "center",
            fontFamily: theme.sans,
            fontWeight: 650,
            fontSize: width * 0.056,
            lineHeight: 1.15,
            color: dark ? theme.inkOnDark : theme.ink,
            opacity: labelIn,
            transform: `translateY(${(1 - labelIn) * 14}px)`,
          }}
        >
          {label}
        </div>
      </AbsoluteFill>
      {/* the shared credit: once-per-source rule, safe-area placement */}
      {source ? <Credit text={source} onMedia={dark} /> : null}
    </AbsoluteFill>
  );
};
