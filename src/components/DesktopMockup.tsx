import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Scene } from "../types";

type MockProps = Extract<Scene, { type: "desktopmockup" }>;

const ACCENT = "#d97757";

const FileIcon: React.FC<{ kind: string }> = ({ kind }) => {
  if (kind === "folder") {
    return (
      <svg viewBox="0 0 100 84" width={132} height={110}>
        <path d="M6 20 h30 l10 10 h42 a6 6 0 0 1 6 6 v40 a6 6 0 0 1 -6 6 H6 a6 6 0 0 1 -6 -6 V26 a6 6 0 0 1 6 -6 z" fill="#6aa9ee"/>
        <path d="M6 30 h88 v42 a6 6 0 0 1 -6 6 H6 a6 6 0 0 1 -6 -6 V30 z" fill="#8fc0f4"/>
      </svg>
    );
  }
  const tint = kind === "pdf" ? "#e05a5a" : kind === "zip" ? "#8a8f98" : "#3aa06b";
  const label = kind.toUpperCase();
  return (
    <svg viewBox="0 0 88 110" width={116} height={145}>
      <path d="M8 4 h50 l22 22 v76 a6 6 0 0 1 -6 6 H8 a6 6 0 0 1 -6 -6 V10 a6 6 0 0 1 6 -6 z" fill="#fff" stroke="#d7d3c8" strokeWidth="2"/>
      <path d="M58 4 v22 h22 z" fill="#e8e4d8"/>
      <rect x="14" y="72" width="60" height="22" rx="4" fill={tint}/>
      <text x="44" y="88" fontFamily="-apple-system,sans-serif" fontSize="13" fontWeight="700" fill="#fff" textAnchor="middle">{label}</text>
    </svg>
  );
};

/** Nick-style finder mockup: file icons with numbered hand-drawn arrows. */
export const DesktopMockup: React.FC<{ scene: MockProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dark = scene.bg === "black";
  const pageBg = dark ? "#0c0c0c" : "#efe9db";
  const ink = dark ? "#ececf0" : "#2a2a2e";

  return (
    <AbsoluteFill
      style={{ background: pageBg, justifyContent: "center", alignItems: "center" }}
    >
      <div
        style={{
          display: "flex",
          gap: 60,
          flexWrap: "wrap",
          justifyContent: "center",
          maxWidth: 900,
        }}
      >
        {scene.files.map((f, i) => {
          const startF = 8 + i * 7;
          const pop = spring({
            frame: frame - startF,
            fps,
            config: { damping: 14, stiffness: 200, mass: 0.5 },
            durationInFrames: 12,
          });
          const arrow = interpolate(frame, [startF, startF + 10], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: (x) => 1 - Math.pow(1 - x, 3),
          });
          const sel = scene.selected === i;
          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                width: 150,
                opacity: pop,
                transform: `translateY(${(1 - pop) * 20}px)`,
              }}
            >
              <div
                style={{
                  fontFamily: "Fraunces, Georgia, serif",
                  fontStyle: "italic",
                  fontWeight: 700,
                  fontSize: 46,
                  color: ACCENT,
                  opacity: arrow,
                  marginBottom: 4,
                }}
              >
                {i + 1}
              </div>
              <svg width="30" height="46" viewBox="0 0 30 46" style={{ opacity: arrow }}>
                <path
                  d={`M15 2 C 10 16, 20 26, 15 ${2 + 40 * arrow}`}
                  stroke={ACCENT}
                  strokeWidth="3"
                  fill="none"
                  strokeLinecap="round"
                />
                {arrow > 0.8 && (
                  <path d={`M9 ${34} L15 ${42} L21 ${34}`} stroke={ACCENT} strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                )}
              </svg>
              <FileIcon kind={f.kind} />
              <div
                style={{
                  marginTop: 10,
                  fontFamily: "-apple-system,'SF Pro Display',sans-serif",
                  fontSize: 20,
                  fontWeight: 500,
                  color: sel ? "#fff" : ink,
                  background: sel ? "#2563EB" : "transparent",
                  padding: sel ? "4px 10px" : "4px 0",
                  borderRadius: 6,
                  textAlign: "center",
                  lineHeight: 1.2,
                  maxWidth: 160,
                }}
              >
                {f.name}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
