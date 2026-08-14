import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useTheme } from "../theme/tokens";

export interface ChartItem {
  label: string;
  value: number;
  /** final text shown once the bar lands (defaults to value + unit) */
  display?: string;
  /** small secondary line under the label */
  sub?: string;
  /** accent bar + glow + serif badge */
  highlight?: boolean;
}

export interface ChartSceneProps {
  title: string;
  kicker?: string;
  items: ChartItem[];
  /** value that maps to a full bar (defaults to max item value) */
  max?: number;
  unit?: string;
  source?: string;
  bg?: "cream" | "black";
  orientation?: "h" | "v";
}

/** ink hex → rgba at given alpha (for tracks/glows derived from theme colors) */
const withAlpha = (hex: string, alpha: number): string => {
  const h = hex.replace("#", "");
  const n = parseInt(
    h.length === 3 ? h.split("").map((c) => c + c).join("") : h,
    16
  );
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${alpha})`;
};

/** ease-out with a slight overshoot, settling back to 1 */
const easeOutOvershoot = (x: number): number => {
  const c = 0.9;
  const t = x - 1;
  return 1 + t * t * ((c + 1) * t + c);
};

const fmtCount = (value: number, p: number, unit: string): string => {
  const v = value * Math.min(1, p);
  const decimals = Number.isInteger(value) ? 0 : 1;
  const s = v.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return `${s}${unit}`;
};

/**
 * Brand-styled animated benchmark chart — replaces raw leaderboard
 * screenshots. Bars fill row-by-row with a soft overshoot, values count up
 * with the fill, the highlight row gets the accent + a serif badge.
 */
export const ChartScene: React.FC<ChartSceneProps> = ({
  title,
  kicker,
  items,
  max,
  unit = "",
  source,
  bg = "cream",
  orientation = "h",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const t = useTheme();

  const dark = bg === "black";
  const pageBg = dark ? t.black : t.cream;
  const ink = dark ? t.inkOnDark : t.ink;
  const muted = dark ? t.mutedOnDark : t.muted;
  const cardBg = dark ? withAlpha(t.white, 0.06) : t.white;
  const track = dark ? withAlpha(t.white, 0.09) : withAlpha(t.ink, 0.07);
  const rows = items.slice(0, 8);
  const maxVal = max ?? Math.max(...rows.map((r) => r.value), 1);

  // timings (30fps): title in, board scaffolding populates fast, then bars
  // fill staggered row-by-row, ~0.8s per fill
  const fillDur = Math.round(0.8 * fps);
  const rowStagger = Math.round(0.3 * fps);
  const firstFill = Math.round(0.55 * fps);
  const rowStart = (i: number) => firstFill + i * rowStagger;
  const rowInStart = (i: number) => Math.round(0.25 * fps) + i * 4;

  const titleIn = spring({
    frame,
    fps,
    config: { damping: 16, stiffness: 120, mass: 0.7 },
    durationInFrames: 18,
  });

  // slow push-in across the whole scene
  const push = interpolate(frame, [0, durationInFrames], [1, 1.045], {
    extrapolateRight: "clamp",
  });

  const n = rows.length;
  const dense = n > 5;
  const labelSize = dense ? 27 : 30;
  const valueSize = dense ? 32 : 36;
  const barH = dense ? 20 : 26;
  const rowGap = dense ? 30 : 42;

  const rowProgress = (i: number) =>
    interpolate(frame, [rowStart(i), rowStart(i) + fillDur], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  const renderBadge = (i: number, topOfBoard: boolean) => {
    const done = frame - (rowStart(i) + fillDur - 4);
    const pop = spring({
      frame: Math.max(0, done),
      fps,
      config: { damping: 10, stiffness: 260, mass: 0.5 },
      durationInFrames: 12,
    });
    if (done < 0) return null;
    return (
      <div
        style={{
          background: t.accent,
          color: t.ink,
          fontFamily: t.serif,
          fontStyle: "italic",
          fontWeight: 700,
          fontSize: dense ? 22 : 25,
          lineHeight: 1,
          padding: "7px 13px 9px",
          borderRadius: 999,
          transform: `scale(${pop}) rotate(${-5 * pop}deg)`,
          boxShadow: `0 6px 18px ${withAlpha(t.accent, 0.45)}`,
          whiteSpace: "nowrap",
        }}
      >
        {topOfBoard ? "#1" : "★"}
      </div>
    );
  };

  const horizontal = (
    <div
      style={{
        background: cardBg,
        borderRadius: t.radius.card,
        boxShadow: dark ? t.shadow.cardOnDark : t.shadow.card,
        padding: dense ? "52px 52px" : "60px 56px",
        display: "flex",
        flexDirection: "column",
        gap: rowGap,
      }}
    >
      {rows.map((r, i) => {
        const p = rowProgress(i);
        const eased = easeOutOvershoot(p);
        const pct = Math.min(1, r.value / maxVal);
        const barPct = Math.min(100, pct * 100 * Math.max(0, eased));
        const rowIn = spring({
          frame: frame - rowInStart(i),
          fps,
          config: { damping: 15, stiffness: 140, mass: 0.6 },
          durationInFrames: 14,
        });
        const isHi = Boolean(r.highlight);
        const barColor = isHi ? t.accent : dark ? t.mutedOnDark : t.muted;
        const landed = p >= 0.999;
        const valueText = landed
          ? r.display ?? `${r.value.toLocaleString("en-US")}${unit}`
          : fmtCount(r.value, easeOutOvershoot(Math.min(1, p)), unit);
        return (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 26,
              opacity: rowIn,
              transform: `translateY(${(1 - rowIn) * 26}px)`,
            }}
          >
            <div style={{ width: dense ? 300 : 320, flexShrink: 0 }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                }}
              >
                <div
                  style={{
                    fontFamily: t.sans,
                    fontWeight: isHi ? 700 : 600,
                    fontSize: labelSize,
                    letterSpacing: "-0.01em",
                    color: ink,
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  {r.label}
                </div>
                {isHi && renderBadge(i, r.value >= maxVal)}
              </div>
              {r.sub && (
                <div
                  style={{
                    fontFamily: t.sans,
                    fontWeight: 500,
                    fontSize: dense ? 19 : 21,
                    color: muted,
                    marginTop: 4,
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  {r.sub}
                </div>
              )}
            </div>

            <div
              style={{
                flex: 1,
                height: barH,
                background: track,
                borderRadius: 999,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${barPct}%`,
                  height: "100%",
                  background: barColor,
                  borderRadius: 999,
                  boxShadow: isHi
                    ? `0 0 22px ${withAlpha(t.accent, 0.55)}`
                    : undefined,
                }}
              />
            </div>

            <div
              style={{
                width: dense ? 118 : 132,
                flexShrink: 0,
                textAlign: "right",
                fontFamily: t.sans,
                fontWeight: 800,
                fontSize: valueSize,
                letterSpacing: "-0.02em",
                fontVariantNumeric: "tabular-nums",
                color: isHi ? ink : muted,
                opacity: Math.min(1, p * 3),
              }}
            >
              {valueText}
            </div>
          </div>
        );
      })}
    </div>
  );

  const vertical = (
    <div
      style={{
        background: cardBg,
        borderRadius: t.radius.card,
        boxShadow: dark ? t.shadow.cardOnDark : t.shadow.card,
        padding: "64px 48px 48px",
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-between",
        gap: 22,
        height: Math.min(860, height * 0.46),
      }}
    >
      {rows.map((r, i) => {
        const p = rowProgress(i);
        const eased = easeOutOvershoot(p);
        const pct = Math.min(1, r.value / maxVal);
        const isHi = Boolean(r.highlight);
        const barColor = isHi ? t.accent : dark ? t.mutedOnDark : t.muted;
        const landed = p >= 0.999;
        const valueText = landed
          ? r.display ?? `${r.value.toLocaleString("en-US")}${unit}`
          : fmtCount(r.value, easeOutOvershoot(Math.min(1, p)), unit);
        return (
          <div
            key={i}
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 14,
              height: "100%",
              justifyContent: "flex-end",
            }}
          >
            <div
              style={{
                fontFamily: t.sans,
                fontWeight: 800,
                fontSize: dense ? 26 : 30,
                letterSpacing: "-0.02em",
                fontVariantNumeric: "tabular-nums",
                color: isHi ? ink : muted,
                opacity: Math.min(1, p * 3),
              }}
            >
              {valueText}
            </div>
            <div
              style={{
                width: "100%",
                flex: 1,
                display: "flex",
                alignItems: "flex-end",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  width: "72%",
                  height: `${Math.min(100, pct * 100 * Math.max(0, eased))}%`,
                  background: barColor,
                  borderRadius: 14,
                  boxShadow: isHi
                    ? `0 0 22px ${withAlpha(t.accent, 0.55)}`
                    : undefined,
                }}
              />
            </div>
            <div
              style={{
                fontFamily: t.sans,
                fontWeight: isHi ? 700 : 600,
                fontSize: dense ? 20 : 23,
                color: ink,
                textAlign: "center",
                lineHeight: 1.15,
              }}
            >
              {r.label}
            </div>
            {isHi && renderBadge(i, r.value >= maxVal)}
          </div>
        );
      })}
    </div>
  );

  return (
    <AbsoluteFill style={{ background: pageBg }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: `0 ${Math.round(width * 0.074)}px`,
          transform: `scale(${push})`,
        }}
      >
        <div
          style={{
            opacity: titleIn,
            transform: `translateY(${(1 - titleIn) * 30}px)`,
            marginBottom: 54,
          }}
        >
          {kicker && (
            <div
              style={{
                fontFamily: t.sans,
                fontWeight: 700,
                fontSize: 27,
                letterSpacing: "0.22em",
                textTransform: "uppercase",
                color: dark ? t.accent : ink,
                display: "flex",
                alignItems: "center",
                gap: 18,
                marginBottom: 26,
              }}
            >
              <span
                style={{
                  width: 46,
                  height: 8,
                  borderRadius: 999,
                  background: t.accent,
                  display: "inline-block",
                }}
              />
              {kicker}
            </div>
          )}
          <div
            style={{
              fontFamily: t.serif,
              fontStyle: "italic",
              fontWeight: 700,
              fontSize: title.length > 26 ? 76 : 88,
              lineHeight: 1.04,
              letterSpacing: "-0.015em",
              color: ink,
            }}
          >
            {title}
          </div>
        </div>

        {orientation === "v" ? vertical : horizontal}

        {source && (
          <div
            style={{
              marginTop: 44,
              fontFamily: t.sans,
              fontWeight: 500,
              fontSize: 22,
              color: muted,
              opacity: titleIn,
            }}
          >
            {source}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
