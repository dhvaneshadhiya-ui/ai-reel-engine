import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const SANS =
  '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif';

export interface PriceLadderProps {
  /** small caps kicker above the title, e.g. "THE CATCH" */
  kicker?: string;
  /** big title, e.g. "EVERY PRICE +$100" */
  title: string;
  /** rows land in sequence: old price gets struck, new price springs in */
  rows: { label: string; oldPrice: string; newPrice: string }[];
  /** per-row delta chip, e.g. "+$100" */
  badge?: string;
  bg?: "black" | "cream";
  /** seconds between row entrances (default 0.5) */
  stagger?: number;
  footnote?: string;
}

const easeOut = (x: number) => 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 3);

export const PriceLadder: React.FC<{
  scene: PriceLadderProps & { durationSec: number };
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const dark = scene.bg !== "cream";
  const ink = dark ? "#f5f2ea" : "#1a1712";
  const dim = dark ? "rgba(245,242,234,0.45)" : "rgba(26,23,18,0.45)";
  const accent = "#FFD84D";
  const red = "#e5484d";
  const stagger = scene.stagger ?? 0.5;
  const titleIn = easeOut(t / 0.35);
  return (
    <AbsoluteFill
      style={{
        background: dark ? "#0e0d0b" : "#f4f0e6",
        fontFamily: SANS,
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ width: 880 }}>
        {scene.kicker && (
          <div
            style={{
              fontSize: 30,
              fontWeight: 700,
              letterSpacing: "0.22em",
              color: dim,
              textTransform: "uppercase",
              opacity: titleIn,
              marginBottom: 14,
            }}
          >
            {scene.kicker}
          </div>
        )}
        <div
          style={{
            fontSize: 78,
            fontWeight: 900,
            letterSpacing: "-0.02em",
            color: ink,
            marginBottom: 54,
            opacity: titleIn,
            transform: `translateY(${(1 - titleIn) * 24}px)`,
          }}
        >
          {scene.title}
        </div>
        {scene.rows.map((r, i) => {
          const at = 0.45 + i * stagger;
          const inT = easeOut((t - at) / 0.3);
          const strike = easeOut((t - at - 0.22) / 0.22);
          const swapF = spring({
            frame: frame - Math.round((at + 0.4) * fps),
            fps,
            config: { damping: 13, stiffness: 240 },
            durationInFrames: 14,
          });
          return (
            <div
              key={r.label}
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 26,
                marginBottom: 40,
                opacity: inT,
                transform: `translateY(${(1 - inT) * 26}px)`,
              }}
            >
              <div style={{ fontSize: 40, fontWeight: 700, color: ink, width: 330 }}>
                {r.label}
              </div>
              <div style={{ position: "relative", fontSize: 44, fontWeight: 700, color: dim }}>
                {r.oldPrice}
                <div
                  style={{
                    position: "absolute",
                    left: "-6%",
                    top: "54%",
                    width: `${112 * strike}%`,
                    height: 7,
                    background: red,
                    borderRadius: 4,
                    transform: "rotate(-5deg)",
                  }}
                />
              </div>
              <div
                style={{
                  fontSize: 56,
                  fontWeight: 900,
                  color: accent,
                  opacity: swapF,
                  transform: `scale(${0.7 + 0.3 * swapF})`,
                  transformOrigin: "left center",
                }}
              >
                {r.newPrice}
              </div>
              {scene.badge && (
                <div
                  style={{
                    fontSize: 26,
                    fontWeight: 800,
                    color: dark ? "#0e0d0b" : "#f4f0e6",
                    background: red,
                    borderRadius: 999,
                    padding: "6px 16px",
                    opacity: swapF,
                  }}
                >
                  {scene.badge}
                </div>
              )}
            </div>
          );
        })}
        {scene.footnote && (
          <div style={{ fontSize: 24, fontWeight: 600, color: dim, marginTop: 8 }}>
            {scene.footnote}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
