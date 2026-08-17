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

type Props = Extract<Scene, { type: "designreveal" }>;
const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";

/** Each design shown nearly full-screen with a number badge + push-in.
 *  Cards 1-4 short, the winner held ~2x with a cyan border + SELECTED ✓. */
export const DesignReveal: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const total = durationInFrames / fps;
  const n = scene.items.length;

  // weights: last card 2x the others
  const weights = scene.items.map((_, i) => (i === n - 1 ? 2.0 : 1.0));
  const wsum = weights.reduce((a, b) => a + b, 0);
  const segs: { start: number; end: number }[] = [];
  let c = 0;
  for (const w of weights) {
    const d = (w / wsum) * total;
    segs.push({ start: c, end: c + d });
    c += d;
  }
  let active = segs.findIndex((s) => t >= s.start && t < s.end);
  if (active === -1) active = n - 1;

  const cardW = 830;
  const cardH = 1180;

  return (
    <AbsoluteFill style={{ background: BGS[scene.bg ?? "gradient"], justifyContent: "center", alignItems: "center", fontFamily: SANS, overflow: "hidden" }}>
      {scene.items.map((it, i) => {
        if (i !== active) return null;
        const seg = segs[i];
        const local = t - seg.start;
        const segDur = seg.end - seg.start;
        const inLocalF = frame - Math.round(seg.start * fps);
        // swipe-in from right
        const slide = spring({ frame: inLocalF, fps, config: { damping: 20, stiffness: 170 }, durationInFrames: 8 });
        const x = (1 - slide) * 520;
        // subtle push-in across the whole hold
        const push = interpolate(local, [0, segDur], [1.0, 1.07]);
        const isWin = i === scene.selectIndex;
        const winPop = isWin ? interpolate(local, [0.1, 0.45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
        return (
          <div
            key={i}
            style={{
              position: "relative",
              width: cardW,
              height: cardH,
              transform: `translateX(${x}px) scale(${push})`,
              borderRadius: 26,
              overflow: "hidden",
              background: "#fff",
              boxShadow: isWin ? `0 0 0 ${9 * winPop}px ${CYAN},0 30px 80px rgba(0,0,0,0.4)` : "0 26px 70px rgba(0,0,0,0.32)",
            }}
          >
            <Img src={staticFile(it.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            <div style={{ position: "absolute", top: 22, left: 28, fontSize: 96, fontWeight: 900, color: "#111", lineHeight: 1, textShadow: "0 3px 14px rgba(255,255,255,0.85)" }}>
              {`0${i + 1}`}
            </div>
            {isWin && winPop > 0.25 && (
              <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, background: CYAN, color: "#fff", fontSize: 50, fontWeight: 900, textAlign: "center", padding: "20px 0", letterSpacing: 3, transform: `translateY(${(1 - winPop) * 110}px)` }}>
                SELECTED ✓
              </div>
            )}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
