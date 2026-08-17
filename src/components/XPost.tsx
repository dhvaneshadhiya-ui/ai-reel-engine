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

type Props = Extract<Scene, { type: "xpost" }>;
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const ACCENT = "#1d9bf0";
const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

function renderText(text: string) {
  return text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
    p.startsWith("**") ? (
      <span key={i} style={{ color: "#111", fontWeight: 800, background: "#e8f4ff", borderRadius: 6, padding: "0 6px" }}>{p.slice(2, -2)}</span>
    ) : (
      <span key={i}>{p}</span>
    )
  );
}

/** A faithful X/Twitter post card (real handle + text, credited) over darkened
 *  build footage — the "what people built" receipt. */
export const XPost: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const en = spring({ frame, fps, config: { damping: 18, stiffness: 150 }, durationInFrames: 14 });

  return (
    <AbsoluteFill style={{ background: "#0b0b0d", fontFamily: SANS, justifyContent: "center", alignItems: "center" }}>
      {scene.bgSrc && (
        <AbsoluteFill>
          {isVideo(scene.bgSrc) ? (
            <OffthreadVideo src={staticFile(scene.bgSrc)} startFrom={Math.round((scene.bgFrom ?? 0) * fps)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          ) : (
            <Img src={staticFile(scene.bgSrc)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          )}
          <AbsoluteFill style={{ background: "rgba(6,6,8,0.62)" }} />
        </AbsoluteFill>
      )}
      <div
        style={{
          position: "relative", width: 900, background: "#fff", borderRadius: 30,
          boxShadow: "0 40px 100px rgba(0,0,0,0.55)", padding: "44px 46px",
          opacity: en, transform: `translateY(${(1 - en) * 40}px)`,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div style={{ width: 84, height: 84, borderRadius: 50, background: "linear-gradient(135deg,#4b5563,#111827)", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 40, fontWeight: 800 }}>
            {scene.name.trim()[0]}
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 40, fontWeight: 800, color: "#0f1419" }}>
              {scene.name}
              {scene.verified !== false && (
                <span style={{ width: 34, height: 34, borderRadius: 20, background: ACCENT, color: "#fff", fontSize: 22, fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center" }}>✓</span>
              )}
            </div>
            <div style={{ fontSize: 32, color: "#536471" }}>{scene.handle}</div>
          </div>
          <div style={{ marginLeft: "auto", fontSize: 46, color: "#0f1419", fontWeight: 900 }}>𝕏</div>
        </div>

        <div style={{ fontSize: 46, lineHeight: 1.32, color: "#0f1419", fontWeight: 500, marginTop: 26 }}>
          {renderText(scene.text)}
        </div>

        {scene.media && (
          <div style={{ marginTop: 26, borderRadius: 20, overflow: "hidden", height: 470, border: "1px solid #eee", background: "#000" }}>
            {isVideo(scene.media) ? (
              <OffthreadVideo src={staticFile(scene.media)} startFrom={Math.round((scene.mediaFrom ?? 0) * fps)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            ) : (
              <Img src={staticFile(scene.media)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            )}
          </div>
        )}
      </div>

      {scene.stat && (
        <div style={{ position: "absolute", bottom: 210, left: 90, opacity: en, transform: `translateY(${(1 - en) * 24}px)` }}>
          <div style={{ fontFamily: "'FrauncesUp', Georgia, serif", fontSize: 118, fontWeight: 600, color: "#fff", lineHeight: 0.95, textShadow: "0 4px 30px rgba(0,0,0,0.8)" }}>{scene.stat}</div>
        </div>
      )}
    </AbsoluteFill>
  );
};
