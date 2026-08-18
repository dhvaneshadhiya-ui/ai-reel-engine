import React from "react";
import { SPRING, DUR } from "../theme/motion";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "checklist" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";

/** Series palette — do not introduce new hues here (RULES.md §design system). */
const CYAN = "#0aa9c2";   // q  — genuinely unknown
const GREEN = "#2fb98a";  // done — confirmed yes
const RUST = "#C2410C";   // no — confirmed exclusion (the pack's accent)

const TINT: Record<string, string> = { done: GREEN, no: RUST, q: CYAN };

/**
 * Drawn marks, not typed glyphs. USER FEEDBACK 2026-08-12: the old component
 * rendered literal "?" / "✓" text inside a circle, which read as a crude
 * fallback. These are stroked paths that draw on with the row, so weight and
 * terminals stay consistent across states and never depend on a font.
 */
const Mark: React.FC<{ state: string; size: number; draw: number }> = ({
  state,
  size,
  draw,
}) => {
  const s = size;
  const stroke = Math.max(3, s * 0.135);
  const common = {
    fill: "none",
    stroke: "#fff",
    strokeWidth: stroke,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
  };
  // dash-offset draw-on: one length covers every path below
  const LEN = s * 2.2;
  const dash = { strokeDasharray: LEN, strokeDashoffset: LEN * (1 - draw) };

  return (
    <svg width={s} height={s} viewBox="0 0 100 100">
      {state === "done" && (
        <path d="M16 52 L40 76 L84 24" {...common} style={dash} />
      )}
      {state === "no" && (
        <>
          <path d="M22 22 L78 78" {...common} style={dash} />
          <path d="M78 22 L22 78" {...common} style={dash} />
        </>
      )}
      {state === "q" && (
        <>
          <path
            d="M30 34 a20 20 0 1 1 20 20 v10"
            {...common}
            style={dash}
          />
          <circle cx="50" cy="80" r={stroke * 0.7} fill="#fff" opacity={draw} />
        </>
      )}
    </svg>
  );
};

export const Checklist: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const dark = (scene.bg ?? "gradient") === "black";
  const ink = dark ? "#fff" : "#111";

  // A list with exactly one unknown among knowns is making a point about that
  // unknown, so it gets emphasis. A list that is ALL one state is a plain
  // enumeration — emphasising every row emphasises nothing.
  const qCount = scene.rows.filter((r) => r.state === "q").length;
  const mixed = qCount > 0 && qCount < scene.rows.length;

  const dotSize = scene.compact ? 52 : 66;
  const labelSize = scene.compact ? 50 : 62;

  return (
    <AbsoluteFill
      style={{
        background: BGS[scene.bg ?? "gradient"],
        justifyContent: "center",
        alignItems: "center",
        fontFamily: SANS,
        padding: "0 96px",
      }}
    >
      {/* USER FEEDBACK 2026-08-12: the block sat low with the headline pinned
          absolutely at the top, leaving a large dead gap. Headline and rows are
          now one flow-centred column, so the group is optically centred on the
          frame whatever the row count. */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch",
          maxWidth: 880,
          width: "100%",
        }}
      >
        {scene.headline && (
          <div
            style={{
              fontSize: 46,
              fontWeight: 800,
              color: dark ? "#c9c9c9" : "#5a5a5a",
              letterSpacing: 2,
              textTransform: "uppercase",
              textAlign: "center",
              marginBottom: scene.compact ? 34 : 52,
              opacity: interpolate(t, [0, 0.35], [0, 1], {
                extrapolateRight: "clamp",
              }),
            }}
          >
            {scene.headline}
          </div>
        )}

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: scene.compact ? 16 : 22,
          }}
        >
          {scene.rows.map((r, i) => {
            const at = 0.25 + i * (scene.stagger ?? 0.55);
            const en = spring({
              frame: frame - Math.round(at * fps),
              fps,
              config: SPRING.enter,
              durationInFrames: DUR.base,
            });
            const draw = interpolate(
              t,
              [at + 0.08, at + 0.42],
              [0, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            );
            const hero = mixed && r.state === "q";
            const pulse = hero ? 1 + 0.02 * Math.sin(t * 5) : 1;
            const tint = TINT[r.state] ?? CYAN;

            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 26,
                  padding: scene.compact ? "12px 26px" : "18px 30px",
                  borderRadius: 22,
                  // A soft plate behind each row lifts the label off the
                  // gradient — the readability rule, checked on a phone.
                  background: dark
                    ? "rgba(255,255,255,0.05)"
                    : "rgba(255,255,255,0.55)",
                  boxShadow: dark
                    ? "none"
                    : "0 2px 14px rgba(30,30,60,0.07)",
                  border: `1px solid ${
                    hero ? tint + "55" : dark ? "#ffffff14" : "#1111110d"
                  }`,
                  opacity: en,
                  transform: `translateY(${(1 - en) * 22}px) scale(${pulse})`,
                }}
              >
                <div
                  style={{
                    width: dotSize,
                    height: dotSize,
                    borderRadius: 50,
                    background: tint,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                    boxShadow: `0 4px 14px ${tint}44`,
                  }}
                >
                  <Mark state={r.state} size={dotSize * 0.74} draw={draw} />
                </div>
                <div
                  style={{
                    fontSize: labelSize,
                    fontWeight: 800,
                    color: r.state === "done" && !hero ? (dark ? "#d8d8d8" : "#2b2b2b") : ink,
                    letterSpacing: 0.5,
                    lineHeight: 1.1,
                  }}
                >
                  {r.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
