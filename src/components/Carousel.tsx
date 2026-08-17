import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "carousel" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";

/** Fast horizontal card-swipe through N design cards, landing on the winner. */
export const Carousel: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dark = (scene.bg ?? "gradient") === "black";
  const n = scene.items.length;
  const total = durationInFrames / fps;
  // hold the winner ~0.9s at the end; distribute the rest across cards
  const hold = 0.9;
  const perCard = (total - hold) / n;
  // current active index by time
  let active = Math.min(n - 1, Math.floor(t / perCard));
  const inWinner = t >= total - hold;
  if (inWinner) active = scene.selectIndex;

  // slide progress (which card is centered) — animate index as a smooth value
  const idxF = inWinner
    ? scene.selectIndex
    : interpolate(t, [0, total - hold], [0, n - 1], { extrapolateRight: "clamp" });

  const cardW = 620;
  const cardH = 826;
  const step = cardW + 70;

  const winnerPop = inWinner
    ? spring({ frame: frame - Math.round((total - hold) * fps), fps, config: { damping: 12, stiffness: 200 }, durationInFrames: 12 })
    : 0;

  return (
    <AbsoluteFill style={{ background: BGS[scene.bg ?? "gradient"], justifyContent: "center", alignItems: "center", fontFamily: SANS, overflow: "hidden" }}>
      {scene.headline && (
        <div style={{ position: "absolute", top: 210, fontSize: 38, fontWeight: 800, color: dark ? "#fff" : "#111", letterSpacing: 1 }}>{scene.headline}</div>
      )}
      <div style={{ position: "relative", width: cardW, height: cardH }}>
        {scene.items.map((it, i) => {
          const off = (i - idxF) * step;
          const dist = Math.abs(i - idxF);
          const scale = interpolate(dist, [0, 1], [1, 0.82], { extrapolateRight: "clamp" }) * (i === scene.selectIndex && inWinner ? 1 + 0.05 * winnerPop : 1);
          const op = interpolate(dist, [0, 1.2], [1, 0.25], { extrapolateRight: "clamp" });
          const isWin = i === scene.selectIndex && inWinner;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                width: cardW,
                height: cardH,
                transform: `translateX(${off}px) scale(${scale})`,
                opacity: op,
                borderRadius: 26,
                overflow: "hidden",
                background: "#fff",
                boxShadow: isWin ? `0 0 0 8px ${CYAN},0 30px 70px rgba(0,0,0,0.4)` : "0 22px 55px rgba(0,0,0,0.3)",
              }}
            >
              <Img src={staticFile(it.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              <div style={{ position: "absolute", top: 18, left: 22, fontSize: 60, fontWeight: 900, color: "#111", textShadow: "0 2px 10px rgba(255,255,255,0.8)" }}>
                {`0${i + 1}`}
              </div>
              {isWin && winnerPop > 0.3 && (
                <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, background: CYAN, color: "#fff", fontSize: 44, fontWeight: 900, textAlign: "center", padding: "18px 0", letterSpacing: 2, transform: `translateY(${(1 - winnerPop) * 100}px)` }}>
                  SELECTED ✓
                </div>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
