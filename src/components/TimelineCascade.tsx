import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

export interface TimelineItem {
  /** date chip, e.g. "JUL 17" */
  date: string;
  /** model name, e.g. "Kimi K3" */
  name: string;
  /** vendor / sub line, e.g. "Moonshot · 2.8T params" */
  sub?: string;
  /** card accent color (brand), default #FFD84D */
  accent?: string;
  /** seconds into the scene when the card lands */
  at: number;
  /** de-emphasized smaller card (for grouped releases) */
  minor?: boolean;
}

export interface TimelineScene {
  type: "timeline";
  durationSec: number;
  items: TimelineItem[];
  /** big serif headline above the stack (optional) */
  title?: string;
  /** small caps kicker above the title */
  kicker?: string;
  /** footage playing behind, darkened (optional; else deep gradient) */
  bgSrc?: string;
  bgFrom?: number;
  /** fraction of frame height the stack starts at (default 0.30) */
  topY?: number;
  captionBottom?: number;
  sfx?: { src: string; at?: number; vol?: number }[];
  headline?: unknown;
}

/** Dated release cards sliding onto a vertical rail, one per `at`. */
export const TimelineCascade: React.FC<{ scene: TimelineScene }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const topY = (scene.topY ?? 0.3) * height;

  const CARD_H = 148;
  const MINOR_H = 108;
  const GAP = 26;

  // total stack height so far (for gentle upward drift when many cards)
  const landed = scene.items.filter((it) => t >= it.at);
  const stackH = landed.reduce(
    (s, it) => s + (it.minor ? MINOR_H : CARD_H) + GAP,
    0
  );
  const overflow = Math.max(0, topY + stackH - height * 0.82);

  let yCursor = 0;

  return (
    <AbsoluteFill style={{ background: "#0B0B0E" }}>
      {scene.bgSrc && (
        <AbsoluteFill>
          <OffthreadVideo
            muted
            src={staticFile(scene.bgSrc)}
            startFrom={Math.round((scene.bgFrom ?? 0) * fps)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "brightness(0.32) saturate(0.85)",
            }}
          />
        </AbsoluteFill>
      )}
      {/* vertical rail */}
      <div
        style={{
          position: "absolute",
          left: 108,
          top: topY - 40 - overflow,
          width: 4,
          height: Math.min(stackH + 60, height),
          background:
            "linear-gradient(180deg, rgba(255,255,255,0.45), rgba(255,255,255,0.06))",
          borderRadius: 2,
        }}
      />
      {(scene.kicker || scene.title) && (
        <div
          style={{
            position: "absolute",
            top: height * 0.10,
            left: 90,
            right: 90,
            color: "#F5F0E8",
            fontFamily: "Fraunces, Georgia, serif",
          }}
        >
          {scene.kicker && (
            <div
              style={{
                fontSize: 30,
                letterSpacing: 6,
                textTransform: "uppercase",
                opacity: interpolate(t, [0.05, 0.35], [0, 0.75], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
                fontFamily: "Inter, sans-serif",
                fontWeight: 700,
              }}
            >
              {scene.kicker}
            </div>
          )}
          {scene.title && (
            <div
              style={{
                fontSize: 84,
                fontWeight: 600,
                marginTop: 10,
                opacity: interpolate(t, [0.15, 0.5], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
              }}
            >
              {scene.title}
            </div>
          )}
        </div>
      )}
      {scene.items.map((it, i) => {
        const h = it.minor ? MINOR_H : CARD_H;
        const y = topY + yCursor - overflow;
        yCursor += h + GAP;
        const local = t - it.at;
        if (local < 0) return null;
        const s = spring({
          frame: frame - Math.round(it.at * fps),
          fps,
          config: { damping: 16, stiffness: 160, mass: 0.7 },
        });
        const accent = it.accent ?? "#FFD84D";
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 150,
              top: y,
              width: width - 150 - 84,
              height: h,
              transform: `translateX(${(1 - s) * 260}px)`,
              opacity: Math.min(1, s * 1.4),
              background: it.minor
                ? "rgba(20,20,26,0.92)"
                : "rgba(16,16,22,0.96)",
              border: `1px solid ${it.minor ? "rgba(255,255,255,0.10)" : "rgba(255,255,255,0.16)"}`,
              borderLeft: `6px solid ${accent}`,
              borderRadius: 18,
              display: "flex",
              alignItems: "center",
              padding: "0 38px",
              gap: 30,
              boxShadow: "0 18px 50px rgba(0,0,0,0.45)",
            }}
          >
            {/* rail node */}
            <div
              style={{
                position: "absolute",
                left: -50,
                top: h / 2 - 9,
                width: 18,
                height: 18,
                borderRadius: 9,
                background: accent,
                transform: `scale(${s})`,
              }}
            />
            <div
              style={{
                fontFamily: "Inter, sans-serif",
                fontWeight: 800,
                fontSize: it.minor ? 26 : 30,
                letterSpacing: 2.5,
                color: accent,
                whiteSpace: "nowrap",
              }}
            >
              {it.date}
            </div>
            <div style={{ minWidth: 0 }}>
              <div
                style={{
                  fontFamily: "Fraunces, Georgia, serif",
                  fontWeight: 600,
                  fontSize: it.minor ? 40 : 52,
                  color: "#F5F0E8",
                  whiteSpace: "nowrap",
                }}
              >
                {it.name}
              </div>
              {it.sub && (
                <div
                  style={{
                    fontFamily: "Inter, sans-serif",
                    fontWeight: 600,
                    fontSize: it.minor ? 22 : 26,
                    color: "rgba(245,240,232,0.62)",
                    marginTop: 2,
                    whiteSpace: "nowrap",
                  }}
                >
                  {it.sub}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
