import React from "react";
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "hcompare" }>;
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";
const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

/** Horizontal (top design / bottom ad) accuracy comparison.
 *  Design fills the frame briefly, slides up into the top band, the ad is
 *  revealed underneath, matching details get cyan boxes + a connecting line,
 *  and the banner messages advance one at a time. */
export const HCompare: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, height } = useVideoConfig();
  const t = frame / fps;
  const total = durationInFrames / fps;
  const topFrac = scene.topFrac ?? 0.42;

  const INTRO = 0.5; // design full-screen, then slides up
  const split = spring({ frame: frame - Math.round(INTRO * fps), fps, config: { damping: 20, stiffness: 150 }, durationInFrames: 12 });
  const topH = interpolate(split, [0, 1], [height, height * topFrac]);
  const botOpacity = interpolate(split, [0.3, 1], [0, 1], { extrapolateLeft: "clamp" });

  // matching detail boxes appear after the split settles
  const boxIn = interpolate(t, [INTRO + 0.5, INTRO + 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const lineIn = interpolate(t, [INTRO + 0.9, INTRO + 1.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pulse = 0.6 + 0.4 * Math.sin(t * 5);

  // banner messages advance across the remaining time
  const msgStart = INTRO + 1.0;
  const per = (total - msgStart) / scene.messages.length;
  let mi = Math.floor((t - msgStart) / per);
  mi = Math.max(0, Math.min(scene.messages.length - 1, mi));
  const mIn = spring({ frame: frame - Math.round((msgStart + mi * per) * fps), fps, config: { damping: 14, stiffness: 180 }, durationInFrames: 9 });

  // box centres (design detail ~ centre of top band; ad detail ~ centre of bottom band)
  const topCy = topH * 0.55;
  const botCy = topH + (height - topH) * 0.5;
  const cx = 0.5; // horizontal fraction

  return (
    <AbsoluteFill style={{ background: "#000", fontFamily: SANS }}>
      {/* TOP: original design */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: topH, overflow: "hidden", background: "#fff" }}>
        <Img src={staticFile(scene.topSrc)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        {split > 0.6 && scene.topLabel && (
          <div style={{ position: "absolute", top: 20, left: 24, background: "rgba(0,0,0,0.72)", color: "#fff", fontSize: 26, fontWeight: 800, padding: "8px 18px", borderRadius: 10, letterSpacing: 1 }}>
            {scene.topLabel}
          </div>
        )}
      </div>
      {/* BOTTOM: AI ad */}
      <div style={{ position: "absolute", top: topH, left: 0, right: 0, bottom: 0, overflow: "hidden", background: "#000", opacity: botOpacity }}>
        {isVideo(scene.bottomSrc) ? (
          <OffthreadVideo src={staticFile(scene.bottomSrc)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        ) : (
          <Img src={staticFile(scene.bottomSrc)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        )}
        {scene.bottomLabel && (
          <div style={{ position: "absolute", top: 20, left: 24, background: "rgba(0,0,0,0.72)", color: "#fff", fontSize: 26, fontWeight: 800, padding: "8px 18px", borderRadius: 10, letterSpacing: 1 }}>
            {scene.bottomLabel}
          </div>
        )}
      </div>
      {/* divider */}
      <div style={{ position: "absolute", top: topH - 2, left: 0, right: 0, height: 4, background: "rgba(255,255,255,0.9)", opacity: botOpacity }} />

      {/* matching detail boxes + connecting line */}
      {boxIn > 0 && (
        <>
          <div style={{ position: "absolute", left: `${cx * 100}%`, top: topCy, width: 150, height: 150, marginLeft: -75, marginTop: -75, border: `4px solid ${CYAN}`, borderRadius: 14, opacity: boxIn * (0.6 + 0.4 * pulse), boxShadow: `0 0 18px ${CYAN}` }} />
          <div style={{ position: "absolute", left: `${cx * 100}%`, top: botCy, width: 150, height: 150, marginLeft: -75, marginTop: -75, border: `4px solid ${CYAN}`, borderRadius: 14, opacity: boxIn * (0.6 + 0.4 * pulse), boxShadow: `0 0 18px ${CYAN}` }} />
          <div style={{ position: "absolute", left: `${cx * 100}%`, top: topCy, width: 3, height: (botCy - topCy) * lineIn, marginLeft: -1.5, background: CYAN, opacity: 0.9, boxShadow: `0 0 10px ${CYAN}` }} />
        </>
      )}

      {/* banner (kept off the dividing line) */}
      <div style={{ position: "absolute", top: topH - 150, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: mIn, transform: `translateY(${(1 - mIn) * 20}px)` }}>
        <div style={{ background: "rgba(0,0,0,0.85)", border: `2px solid ${CYAN}`, color: "#fff", fontSize: 44, fontWeight: 900, padding: "18px 38px", borderRadius: 18, letterSpacing: 1, lineHeight: 1.15, whiteSpace: "pre-line", textAlign: "center" }}>
          {scene.messages[mi]}
        </div>
      </div>
    </AbsoluteFill>
  );
};
