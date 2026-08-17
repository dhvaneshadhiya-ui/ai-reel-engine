import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import { useTheme } from "../theme/tokens";
import type { Scene } from "../types";

type StatProps = Extract<Scene, { type: "statcard" }>;

const PALETTE = ["#E0518A", "#8B5CF6", "#3FB6C4", "#48C4B0", "#F5B840", "#6366F1"];

/**
 * Nick-style stat / budget card: a titled panel with labelled rows whose
 * colored progress bars FILL left-to-right, staggered row by row. This is his
 * signature "wow" graphic — the motion is the point.
 */
export const StatCard: React.FC<{ scene: StatProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const theme = useTheme();
  const dark = scene.bg === "black";
  const pageBg = dark ? theme.black : theme.cream;
  const cardBg = dark ? "#17171b" : "#ffffff";
  const ink = dark ? "#f2f2f4" : "#16181d";
  const sub = dark ? "#9a9aa2" : "#6e6e73";
  const track = dark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.06)";

  const cardW = width * 0.82;
  const enter = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 130, mass: 0.7 },
    durationInFrames: 16,
  });

  return (
    <AbsoluteFill
      style={{ background: pageBg, justifyContent: "center", alignItems: "center" }}
    >
      <div
        style={{
          width: cardW,
          background: cardBg,
          borderRadius: 26,
          padding: "40px 44px",
          boxShadow: dark
            ? "0 30px 70px rgba(0,0,0,0.6)"
            : "0 30px 70px rgba(0,0,0,0.14)",
          opacity: enter,
          transform: `translateY(${(1 - enter) * 40}px) scale(${0.96 + 0.04 * enter})`,
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "baseline",
            marginBottom: 34,
          }}
        >
          <div
            style={{
              fontFamily:
                "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
              fontWeight: 700,
              fontSize: 40,
              letterSpacing: "-0.02em",
              color: ink,
            }}
          >
            {scene.title}
          </div>
          {scene.titleRight && (
            <div
              style={{
                fontFamily:
                  "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
                fontWeight: 700,
                fontSize: 34,
                color: PALETTE[0],
              }}
            >
              {scene.titleRight}
            </div>
          )}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
          {scene.rows.map((r, i) => {
            const startF = 10 + i * 6; // stagger row by row
            const grow = interpolate(frame, [startF, startF + 20], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: (x) => 1 - Math.pow(1 - x, 3),
            });
            const color = r.color ?? PALETTE[i % PALETTE.length];
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 22 }}>
                <div
                  style={{
                    width: 220,
                    fontFamily:
                      "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
                    fontWeight: 600,
                    fontSize: 27,
                    color: ink,
                    whiteSpace: "nowrap",
                  }}
                >
                  {r.label}
                </div>
                <div
                  style={{
                    flex: 1,
                    height: 18,
                    background: track,
                    borderRadius: 999,
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${Math.max(0, Math.min(1, r.pct)) * 100 * grow}%`,
                      height: "100%",
                      background: color,
                      borderRadius: 999,
                    }}
                  />
                </div>
                <div
                  style={{
                    width: 130,
                    textAlign: "right",
                    fontFamily: "ui-monospace,'SF Mono',Menlo,monospace",
                    fontSize: 24,
                    color: sub,
                    opacity: grow,
                  }}
                >
                  {r.value}
                </div>
              </div>
            );
          })}
        </div>

        {scene.footnote && (
          <div
            style={{
              marginTop: 30,
              fontFamily:
                "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
              fontSize: 22,
              color: sub,
            }}
          >
            {scene.footnote}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
