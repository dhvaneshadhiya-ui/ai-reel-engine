import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "specsheet" }>;
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const SERIF = "'FrauncesUp', Georgia, serif";
const ACCENT = "#d97757";

/** Reference-style spec card: dark field, serif title, label→value rows that
 *  reveal one by one, one row highlighted in the brand accent. */
export const SpecSheet: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  return (
    <AbsoluteFill style={{ background: "#0c0c0c", fontFamily: SANS, justifyContent: "center", padding: "0 90px" }}>
      {scene.bgSrc && (
        <AbsoluteFill>
          <OffthreadVideo
            src={staticFile(scene.bgSrc)}
            startFrom={Math.round((scene.bgFrom ?? 0) * fps)}
            muted
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
          {/* scrim so rows stay legible over the film */}
          <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(6,6,6,0.34) 0%, rgba(6,6,6,0.72) 45%, rgba(6,6,6,0.82) 100%)" }} />
        </AbsoluteFill>
      )}
      {scene.kicker && (
        <div style={{ position: "relative", fontFamily: SERIF, fontSize: 40, color: ACCENT, marginBottom: 14, opacity: interpolate(t, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }) }}>
          {scene.kicker}
        </div>
      )}
      <div style={{ position: "relative", fontFamily: SERIF, fontWeight: 600, fontSize: 92, color: "#fff", lineHeight: 1.0, marginBottom: 40, opacity: interpolate(t, [0.05, 0.4], [0, 1], { extrapolateRight: "clamp" }), transform: `translateY(${interpolate(t, [0.05, 0.4], [22, 0], { extrapolateRight: "clamp" })}px)` }}>
        {scene.title}
      </div>
      {scene.columns && (
        <div style={{ position: "relative", display: "flex", alignItems: "flex-end", padding: "0 26px 16px", opacity: interpolate(t, [0.25, 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
          <span style={{ flex: 1 }} />
          {scene.columns.map((c, j) => (
            <span key={j} style={{ width: 300, textAlign: "right", fontSize: 27, letterSpacing: 1.5, fontWeight: 700, color: "rgba(255,255,255,0.5)", textTransform: "uppercase" }}>{c}</span>
          ))}
        </div>
      )}
      <div style={{ position: "relative", display: "flex", flexDirection: "column", borderRadius: 20, overflow: "hidden", boxShadow: "0 30px 80px rgba(0,0,0,0.5)" }}>
        {scene.rows.map((r, i) => {
          const at = 0.4 + i * 0.3;
          const en = spring({ frame: frame - Math.round(at * fps), fps, config: { damping: 18, stiffness: 150 }, durationInFrames: 12 });
          const vals = r.values ?? (r.value ? [r.value] : []);
          return (
            <div
              key={i}
              style={{
                display: "flex", alignItems: "center", padding: "30px 26px",
                borderTop: i === 0 ? "none" : "1px solid rgba(255,255,255,0.10)",
                background: r.accent ? "rgba(217,119,87,0.20)" : "rgba(255,255,255,0.04)",
                boxShadow: r.accent ? `inset 5px 0 0 ${ACCENT}` : "none",
                opacity: en, transform: `translateX(${(1 - en) * 26}px)`,
              }}
            >
              <span style={{ flex: 1, fontSize: 46, color: r.accent ? "#fff" : "rgba(255,255,255,0.72)", fontWeight: 800 }}>
                {r.label}
                {r.accent && (r as { badge?: string }).badge && <span style={{ marginLeft: 14, fontSize: 26, color: ACCENT, fontWeight: 800, verticalAlign: "middle" }}>{(r as { badge?: string }).badge}</span>}
              </span>
              {vals.map((v, j) => (
                <span key={j} style={{ width: 300, textAlign: "right", fontSize: 50, fontWeight: 800, color: r.accent ? "#fff" : "#dcdcdc", fontVariantNumeric: "tabular-nums" }}>{v}</span>
              ))}
            </div>
          );
        })}
      </div>
      {scene.footnote && (
        <div style={{ position: "relative", fontSize: 32, color: "rgba(255,255,255,0.5)", marginTop: 34, fontStyle: "italic", fontFamily: SERIF }}>{scene.footnote}</div>
      )}
    </AbsoluteFill>
  );
};
