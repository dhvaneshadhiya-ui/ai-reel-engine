import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from "remotion";
import type { Scene } from "../types";

type DialogProps = Extract<Scene, { type: "uidialog" }>;

/** Nick-style app-dialog recreation (e.g. the NVIDIA "Generate API Key" modal). */
export const UIDialog: React.FC<{ scene: DialogProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const enter = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 150, mass: 0.7 },
    durationInFrames: 14,
  });
  const cardW = width * 0.84;
  const sans = "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif";

  return (
    <AbsoluteFill
      style={{ background: "#0a0c10", justifyContent: "center", alignItems: "center" }}
    >
      <div
        style={{
          width: cardW,
          background: "#15181e",
          border: "1px solid rgba(255,255,255,0.08)",
          borderRadius: 22,
          padding: "40px 44px",
          boxShadow: "0 40px 90px rgba(0,0,0,0.7)",
          opacity: enter,
          transform: `translateY(${(1 - enter) * 40}px) scale(${0.96 + 0.04 * enter})`,
        }}
      >
        {scene.app && (
          <div
            style={{
              fontFamily: sans,
              fontSize: 24,
              fontWeight: 700,
              color: "#76b900",
              letterSpacing: "0.02em",
              marginBottom: 22,
            }}
          >
            {scene.app}
          </div>
        )}
        <div style={{ fontFamily: sans, fontSize: 42, fontWeight: 700, color: "#fff", marginBottom: 14 }}>
          {scene.title}
        </div>
        {scene.body && (
          <div style={{ fontFamily: sans, fontSize: 26, color: "rgba(255,255,255,0.55)", lineHeight: 1.4, marginBottom: 30 }}>
            {scene.body}
          </div>
        )}
        {scene.field && (
          <div style={{ marginBottom: 24 }}>
            <div style={{ fontFamily: sans, fontSize: 22, color: "rgba(255,255,255,0.7)", marginBottom: 10 }}>{scene.field.label}</div>
            <div style={{ fontFamily: "ui-monospace,'SF Mono',Menlo,monospace", fontSize: 26, color: "#fff", background: "#0d0f13", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 10, padding: "16px 18px" }}>
              {scene.field.value}<span style={{ opacity: (frame % 30 < 15) ? 1 : 0 }}>|</span>
            </div>
          </div>
        )}
        {scene.select && (
          <div style={{ marginBottom: 34 }}>
            <div style={{ fontFamily: sans, fontSize: 22, color: "rgba(255,255,255,0.7)", marginBottom: 10 }}>{scene.select.label}</div>
            <div style={{ fontFamily: sans, fontSize: 26, color: "#fff", background: "#0d0f13", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 10, padding: "16px 18px", display: "flex", justifyContent: "space-between" }}>
              <span>{scene.select.value}</span><span style={{ color: "rgba(255,255,255,0.4)" }}>⌄</span>
            </div>
          </div>
        )}
        <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", gap: 24 }}>
          <div style={{ fontFamily: sans, fontSize: 26, fontWeight: 600, color: "rgba(255,255,255,0.7)" }}>{scene.cancel ?? "Cancel"}</div>
          <div style={{ fontFamily: sans, fontSize: 26, fontWeight: 700, color: "#fff", background: "#4a9d2f", borderRadius: 10, padding: "14px 26px" }}>
            {scene.primary ?? "Generate Key"}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
