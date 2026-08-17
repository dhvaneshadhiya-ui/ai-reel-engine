import React from "react";

/** y 0.79 — just inside the platform safe floor (platformSafeArea.ts). */
const SAFE_LOW = 400;
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import type { Scene } from "../types";

type Props = Extract<Scene, { type: "promptcard" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: "#f2ecdf",
  gradient: "linear-gradient(160deg,#e6edf7 0%,#f3e6dc 55%,#ecdcf1 100%)",
};
const SANS =
  "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";
const CYAN = "#0aa9c2";

/** Renders prompt text with highlighted substrings wrapped in a cyan pill. */
function renderPrompt(text: string, highlights: string[], lit: number) {
  if (!highlights.length) return text;
  const parts: React.ReactNode[] = [];
  let rest = text;
  let key = 0;
  let hi = 0;
  while (rest.length) {
    let idx = -1;
    let hit = "";
    for (const h of highlights) {
      const i = rest.toLowerCase().indexOf(h.toLowerCase());
      if (i !== -1 && (idx === -1 || i < idx)) {
        idx = i;
        hit = rest.slice(i, i + h.length);
      }
    }
    if (idx === -1) {
      parts.push(<span key={key++}>{rest}</span>);
      break;
    }
    if (idx > 0) parts.push(<span key={key++}>{rest.slice(0, idx)}</span>);
    const on = hi < lit;
    hi++;
    parts.push(
      <span
        key={key++}
        style={{
          color: on ? "#fff" : "inherit",
          background: on ? CYAN : "transparent",
          borderRadius: 8,
          padding: on ? "0 10px" : "0",
          boxDecorationBreak: "clone",
          WebkitBoxDecorationBreak: "clone",
        }}
      >
        {hit}
      </span>
    );
    rest = rest.slice(idx + hit.length);
  }
  return parts;
}

export const PromptCard: React.FC<{ scene: Props }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const bg = BGS[scene.bg ?? "gradient"];
  const dark = (scene.bg ?? "gradient") === "black";

  const enter = spring({ frame, fps, config: { damping: 18, stiffness: 150 }, durationInFrames: 14 });

  // typing reveal
  const full = scene.promptText ?? "";
  const typeStart = 0.12;
  const typeDur = Math.min(0.5, durationInFrames / fps - 0.4);
  const shown = Math.round(
    interpolate(t, [typeStart, typeStart + typeDur], [0, full.length], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const typed = full.slice(0, shown);
  const litCount = interpolate(t, [typeStart + typeDur, typeStart + typeDur + 1.0], [0, (scene.highlights ?? []).length], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: bg, justifyContent: "center", alignItems: "center", fontFamily: SANS }}>
      {scene.headline && (
        <div
          style={{
            position: "absolute",
            top: 250,
            fontSize: 40,
            fontWeight: 800,
            letterSpacing: 1,
            color: dark ? "#fff" : "#111",
            opacity: enter,
            textAlign: "center",
          }}
        >
          {scene.headline}
        </div>
      )}

      {scene.lines ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 34, alignItems: "center" }}>
          {scene.lines.map((ln, i) => {
            const at = 0.3 + i * 0.35;
            const o = interpolate(t, [at, at + 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            const y = interpolate(t, [at, at + 0.25], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <div key={i} style={{ fontSize: 74, fontWeight: 900, color: dark ? "#fff" : "#111", opacity: o, transform: `translateY(${y}px)`, letterSpacing: 1 }}>
                {ln}
              </div>
            );
          })}
        </div>
      ) : (
        <div
          style={{
            width: 920,
            background: dark ? "#161616" : "#fff",
            borderRadius: 30,
            boxShadow: "0 30px 80px rgba(0,0,0,0.28)",
            padding: "48px 52px",
            opacity: enter,
            transform: `translateY(${(1 - enter) * 40}px)`,
          }}
        >
          <div style={{ display: "flex", gap: 10, marginBottom: 30 }}>
            <span style={{ width: 15, height: 15, borderRadius: 8, background: "#ff5f57" }} />
            <span style={{ width: 15, height: 15, borderRadius: 8, background: "#febc2e" }} />
            <span style={{ width: 15, height: 15, borderRadius: 8, background: "#28c840" }} />
            {scene.app && (
              <span style={{ marginLeft: "auto", fontSize: 24, color: dark ? "#888" : "#999", fontWeight: 600 }}>{scene.app}</span>
            )}
          </div>
          <div style={{ fontSize: 52, lineHeight: 1.3, fontWeight: 650, color: dark ? "#f2f2f2" : "#1a1a1a" }}>
            {renderPrompt(typed, scene.highlights ?? [], Math.round(litCount))}
            {shown < full.length && <span style={{ opacity: (frame % 20) < 10 ? 1 : 0 }}>|</span>}
          </div>
          {scene.loaders ? (
            <div style={{ display: "flex", gap: 16, marginTop: 40 }}>
              {Array.from({ length: scene.loaders }).map((_, i) => {
                const shimmer = interpolate((t * 1.2 + i * 0.2) % 1, [0, 0.5, 1], [0.35, 0.7, 0.35]);
                return (
                  <div key={i} style={{ flex: 1, height: 150, borderRadius: 16, background: dark ? "#242424" : "#eef1f5", position: "relative", overflow: "hidden" }}>
                    <div style={{ position: "absolute", inset: 0, background: `linear-gradient(90deg,transparent, rgba(10,169,194,${shimmer * 0.5}), transparent)`, transform: `translateX(${(shimmer - 0.5) * 300}px)` }} />
                    <div style={{ position: "absolute", top: 12, left: 14, fontSize: 26, fontWeight: 800, color: dark ? "#666" : "#b8c0cc" }}>{`0${i + 1}`}</div>
                  </div>
                );
              })}
            </div>
          ) : null}
        </div>
      )}
      {scene.subtext && (
        <div style={{ position: "absolute", bottom: SAFE_LOW, fontSize: 40, fontWeight: 800, color: CYAN, letterSpacing: 1, opacity: interpolate(t, [0.4, 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
          {scene.subtext}
        </div>
      )}
    </AbsoluteFill>
  );
};
