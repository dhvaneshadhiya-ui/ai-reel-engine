import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "endquestion" }>;
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";
const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

/** Closing beat: strong ad freeze + "WOULD YOU RUN THIS AD?" + YES / NO.
 *  (Left region reserved for the HeyGen avatar drop-in once available.) */
export const EndQuestion: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const en = spring({ frame, fps, config: { damping: 15, stiffness: 170 }, durationInFrames: 10 });

  return (
    <AbsoluteFill style={{ background: "#000", fontFamily: SANS, justifyContent: "center", alignItems: "center" }}>
      {isVideo(scene.src) ? (
        <OffthreadVideo src={staticFile(scene.src)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <Img src={staticFile(scene.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      )}
      <AbsoluteFill style={{ background: "linear-gradient(180deg,rgba(0,0,0,0.15),rgba(0,0,0,0.55))" }} />
      <div style={{ position: "absolute", top: "34%", left: 0, right: 0, textAlign: "center", opacity: en, transform: `translateY(${(1 - en) * 24}px)` }}>
        <div style={{ display: "inline-block", background: "rgba(0,0,0,0.7)", border: `2px solid ${CYAN}`, color: "#fff", fontSize: 58, fontWeight: 900, padding: "22px 40px", borderRadius: 18, letterSpacing: 1, lineHeight: 1.15, whiteSpace: "pre-line" }}>
          {scene.question}
        </div>
        <div style={{ marginTop: 44, display: "flex", gap: 40, justifyContent: "center" }}>
          <div style={{ background: CYAN, color: "#fff", fontSize: 46, fontWeight: 900, padding: "16px 56px", borderRadius: 14, letterSpacing: 2 }}>YES</div>
          <div style={{ background: "rgba(255,255,255,0.16)", border: "2px solid #fff", color: "#fff", fontSize: 46, fontWeight: 900, padding: "16px 56px", borderRadius: 14, letterSpacing: 2 }}>NO</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
