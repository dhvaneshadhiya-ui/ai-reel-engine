import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "categorygrid" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";
const CARDBG = ["#ff8a4c", "#7c6cf0", "#2fb98a", "#f05a8a"];

export const CategoryGrid: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const dark = (scene.bg ?? "gradient") === "black";
  const sel = scene.selectIndex;
  const selAt = scene.selectAt ?? 999;
  const selP = interpolate(t, [selAt, selAt + 0.45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  // 2x2 layout coordinates (card centers), in a 940-wide, 940-tall grid
  const GW = 940;
  const cw = 440;
  const ch = 300;
  const gap = 40;
  const pos = [
    { x: -(cw + gap) / 2, y: -(ch + gap) / 2 },
    { x: (cw + gap) / 2, y: -(ch + gap) / 2 },
    { x: -(cw + gap) / 2, y: (ch + gap) / 2 },
    { x: (cw + gap) / 2, y: (ch + gap) / 2 },
  ];

  return (
    <AbsoluteFill style={{ background: BGS[scene.bg ?? "gradient"], justifyContent: "center", alignItems: "center", fontFamily: SANS }}>
      {scene.headline && (
        <div style={{ position: "absolute", top: 230, fontSize: 40, fontWeight: 800, letterSpacing: 1, color: dark ? "#fff" : "#111" }}>
          {scene.headline}
        </div>
      )}
      <div style={{ position: "relative", width: GW, height: GW * 0.72 }}>
        {scene.cards.map((c, i) => {
          const enter = spring({ frame: frame - i * 5, fps, config: { damping: 16, stiffness: 150 }, durationInFrames: 14 });
          const isSel = sel === i;
          // selection transforms
          const toCenter = isSel ? selP : 0;
          const x = pos[i].x * (1 - toCenter);
          const y = pos[i].y * (1 - toCenter);
          const scale = (isSel ? 1 + 0.28 * selP : 1) * enter;
          const dim = sel != null && !isSel ? 1 - 0.8 * selP : 1;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: "50%",
                top: "50%",
                width: cw,
                height: ch,
                marginLeft: -cw / 2,
                marginTop: -ch / 2,
                transform: `translate(${x}px,${y}px) scale(${scale})`,
                opacity: dim * enter,
                borderRadius: 28,
                background: CARDBG[i % 4],
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: isSel ? `0 0 0 ${6 * selP}px ${CYAN}, 0 30px 70px rgba(0,0,0,0.35)` : "0 20px 50px rgba(0,0,0,0.25)",
                zIndex: isSel ? 5 : 1,
              }}
            >
              <div style={{ fontSize: 46, fontWeight: 900, color: "#fff", textAlign: "center", letterSpacing: 1, lineHeight: 1.1, padding: "0 24px" }}>
                {c.label}
              </div>
              {c.sub && <div style={{ fontSize: 24, color: "rgba(255,255,255,0.85)", marginTop: 10 }}>{c.sub}</div>}
              {isSel && selP > 0.4 && (
                <div style={{ position: "absolute", top: 18, right: 22, width: 56, height: 56, borderRadius: 30, background: CYAN, color: "#fff", fontSize: 36, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${interpolate(selP, [0.4, 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})` }}>
                  ✓
                </div>
              )}
            </div>
          );
        })}
      </div>
      {sel != null && selP > 0.5 && (
        <div style={{ position: "absolute", bottom: 340, fontSize: 44, fontWeight: 900, color: dark ? "#fff" : "#111", letterSpacing: 1, opacity: interpolate(selP, [0.5, 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
          SELECTED: <span style={{ color: CYAN }}>{scene.cards[sel].label}</span>
        </div>
      )}
    </AbsoluteFill>
  );
};
