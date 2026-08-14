import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "settingspane" }>;

const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";

/**
 * Rendered iOS Settings pane.
 *
 * WHY BUILT, NOT RECORDED (2026-08-12): the same reasoning that gave us
 * `terminal` over terminal screen-recs and `chart` over leaderboard
 * screenshots. A rendered pane is reusable across reels, animates (the
 * spotlight, the toggle flip), stays pin-sharp at 1080x1920, and needs no
 * Xcode/simulator — which this machine does not have, and whose Settings app
 * is missing whole panes (Cellular, Face ID) anyway.
 *
 * LIMIT: this is a faithful RECREATION, not a capture. When a pane cannot be
 * rebuilt honestly, use a real device recording in `deviceframe` instead.
 */
const T = {
  light: {
    page: "#f2f2f7",
    card: "#ffffff",
    ink: "#000000",
    dim: "#8a8a8e",
    sep: "rgba(60,60,67,0.29)",
    nav: "rgba(249,249,249,0.94)",
    tintText: "#007aff",
    spot: "rgba(0,122,255,0.10)",
  },
  dark: {
    page: "#000000",
    card: "#1c1c1e",
    ink: "#ffffff",
    dim: "#8d8d93",
    sep: "rgba(84,84,88,0.65)",
    nav: "rgba(28,28,30,0.94)",
    tintText: "#0a84ff",
    spot: "rgba(10,132,255,0.16)",
  },
};

/** iOS switch, with a spring flip so the change is legible on a phone. */
const Toggle: React.FC<{ on: boolean; p: number }> = ({ on, p }) => {
  const W = 92;
  const H = 56;
  const knob = H - 8;
  // p: 0 -> starting state, 1 -> flipped
  const at = on ? 1 - p : p;
  const x = interpolate(at, [0, 1], [4, W - knob - 4]);
  const green = "#34c759";
  const grey = "#e9e9ea";
  return (
    <div
      style={{
        width: W,
        height: H,
        borderRadius: H / 2,
        background: at > 0.5 ? green : grey,
        position: "relative",
        flexShrink: 0,
        transition: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 4,
          left: x,
          width: knob,
          height: knob,
          borderRadius: knob / 2,
          background: "#fff",
          boxShadow: "0 3px 8px rgba(0,0,0,0.18)",
        }}
      />
    </div>
  );
};

const Chevron: React.FC<{ color: string }> = ({ color }) => (
  <svg width={20} height={34} viewBox="0 0 20 34" style={{ flexShrink: 0 }}>
    <path
      d="M3 3 L16 17 L3 31"
      fill="none"
      stroke={color}
      strokeWidth={4}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const SettingsPane: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const c = T[scene.appearance ?? "light"];

  const enter = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 150, mass: 0.7 },
    durationInFrames: 14,
  });

  const [fg, fr] = (scene.focus ?? "").split(".").map(Number);
  const focusAt = scene.focusAt ?? 0.5;
  const focusP = interpolate(t, [focusAt, focusAt + 0.35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: c.page,
        fontFamily: SANS,
        justifyContent: "center",
        alignItems: "center",
        padding: "0 40px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 940,
          opacity: enter,
          transform: `translateY(${(1 - enter) * 26}px)`,
        }}
      >
        {/* nav bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "0 6px 26px",
          }}
        >
          {scene.back && (
            <>
              <svg width={22} height={38} viewBox="0 0 22 38">
                <path
                  d="M17 3 L4 19 L17 35"
                  fill="none"
                  stroke={c.tintText}
                  strokeWidth={4.5}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div style={{ fontSize: 40, color: c.tintText, fontWeight: 400 }}>
                {scene.back}
              </div>
            </>
          )}
          <div
            style={{
              flex: 1,
              textAlign: "center",
              fontSize: 44,
              fontWeight: 700,
              color: c.ink,
              marginRight: scene.back ? 120 : 0,
            }}
          >
            {scene.title}
          </div>
        </div>

        {scene.groups.map((g, gi) => (
          <div key={gi} style={{ marginBottom: 44 }}>
            {g.header && (
              <div
                style={{
                  fontSize: 30,
                  color: c.dim,
                  textTransform: "uppercase",
                  letterSpacing: 0.8,
                  padding: "0 30px 12px",
                }}
              >
                {g.header}
              </div>
            )}
            <div
              style={{
                background: c.card,
                borderRadius: 26,
                overflow: "hidden",
              }}
            >
              {g.rows.map((r, ri) => {
                const isFocus = gi === fg && ri === fr;
                const flipAt = r.flipAt;
                const flipP =
                  flipAt === undefined
                    ? 0
                    : interpolate(t, [flipAt, flipAt + 0.28], [0, 1], {
                        extrapolateLeft: "clamp",
                        extrapolateRight: "clamp",
                      });
                return (
                  <div
                    key={ri}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 24,
                      padding: "26px 30px",
                      minHeight: 104,
                      background: isFocus
                        ? `rgba(0,0,0,0)`
                        : "transparent",
                      boxShadow: isFocus
                        ? `inset 0 0 0 999px ${c.spot}`
                        : "none",
                      borderBottom:
                        ri === g.rows.length - 1
                          ? "none"
                          : `1px solid ${c.sep}`,
                      transform: isFocus
                        ? `scale(${1 + 0.012 * focusP})`
                        : "none",
                    }}
                  >
                    {r.tint && (
                      <div
                        style={{
                          width: 62,
                          height: 62,
                          borderRadius: 15,
                          background: r.tint,
                          color: "#fff",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 34,
                          fontWeight: 600,
                          flexShrink: 0,
                        }}
                      >
                        {r.glyph ?? ""}
                      </div>
                    )}
                    <div
                      style={{
                        flex: 1,
                        fontSize: 40,
                        fontWeight: isFocus ? 700 : 400,
                        color: c.ink,
                      }}
                    >
                      {r.label}
                    </div>
                    {r.toggle ? (
                      <Toggle on={!!r.on} p={flipP} />
                    ) : (
                      <>
                        {r.value && (
                          <div style={{ fontSize: 38, color: c.dim }}>
                            {r.value}
                          </div>
                        )}
                        {r.chevron !== false && <Chevron color={c.dim} />}
                      </>
                    )}
                  </div>
                );
              })}
            </div>
            {g.footer && (
              <div
                style={{
                  fontSize: 28,
                  color: c.dim,
                  padding: "14px 30px 0",
                  lineHeight: 1.35,
                }}
              >
                {g.footer}
              </div>
            )}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
