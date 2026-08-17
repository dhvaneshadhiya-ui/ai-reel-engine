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

type Props = Extract<Scene, { type: "comparesplit" }>;
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";

const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

function Half({ src, label }: { src: string; label?: string }) {
  return (
    <div style={{ position: "relative", width: "50%", height: "100%", overflow: "hidden", background: "#000" }}>
      {isVideo(src) ? (
        <OffthreadVideo src={staticFile(src)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      )}
      {label && (
        <div style={{ position: "absolute", top: 28, left: 0, right: 0, textAlign: "center", fontSize: 30, fontWeight: 800, color: "#fff", textShadow: "0 2px 12px rgba(0,0,0,0.7)", letterSpacing: 1 }}>
          {label}
        </div>
      )}
    </div>
  );
}

export const CompareSplit: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const total = durationInFrames / fps;

  // banner phases
  const phases = [scene.topText, scene.midText, scene.finalText].filter(Boolean) as string[];
  const segT = total / (phases.length + (scene.question ? 1 : 0));
  let phaseIdx = Math.min(phases.length - 1, Math.floor(t / segT));
  const showQ = scene.question && t >= segT * phases.length;
  const banner = showQ ? scene.question! : phases[phaseIdx];
  const bannerKey = showQ ? "q" : String(phaseIdx);
  const bIn = spring({ frame: frame - Math.round((showQ ? segT * phases.length : segT * phaseIdx) * fps), fps, config: { damping: 14, stiffness: 180 }, durationInFrames: 10 });

  // cyan matching outline pulse
  const pulse = 0.5 + 0.5 * Math.sin(t * 4);

  return (
    <AbsoluteFill style={{ background: "#000", fontFamily: SANS }}>
      <div style={{ display: "flex", width: "100%", height: "100%" }}>
        <Half src={scene.leftSrc} label={scene.leftLabel} />
        <Half src={scene.rightSrc} label={scene.rightLabel} />
      </div>
      {/* center divider */}
      <div style={{ position: "absolute", left: "50%", top: 0, bottom: 0, width: 4, marginLeft: -2, background: "rgba(255,255,255,0.85)" }} />
      {/* matching detail brackets */}
      {[0.27, 0.73].map((cx, i) => (
        <div key={i} style={{ position: "absolute", left: `${cx * 100}%`, top: "52%", width: 150, height: 150, marginLeft: -75, marginTop: -75, border: `4px solid ${CYAN}`, borderRadius: 16, opacity: 0.5 + 0.5 * pulse, boxShadow: `0 0 20px ${CYAN}` }} />
      ))}
      {/* banner */}
      <div
        style={{
          position: "absolute",
          bottom: showQ ? "44%" : 300,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: bIn,
          transform: `translateY(${(1 - bIn) * 30}px)`,
        }}
      >
        <div style={{ display: "inline-block", background: showQ ? CYAN : "rgba(0,0,0,0.82)", color: "#fff", fontSize: showQ ? 60 : 46, fontWeight: 900, padding: showQ ? "26px 48px" : "20px 40px", borderRadius: 20, letterSpacing: 1, lineHeight: 1.15, whiteSpace: "pre-line", border: showQ ? "none" : `2px solid ${CYAN}` }}>
          {banner}
        </div>
      </div>
    </AbsoluteFill>
  );
};
