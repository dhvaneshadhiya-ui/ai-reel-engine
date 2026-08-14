import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";

export interface TerminalLine {
  text: string;
  /** cmd = typed after a $ prompt; out = instant; ok = green check; err = red cross */
  kind: "cmd" | "out" | "ok" | "err";
  /** seconds from scene start when this line begins */
  at: number;
}

export interface TerminalSceneProps {
  /** window title, e.g. "creator@mac — zsh" */
  title?: string;
  lines: TerminalLine[];
  bg?: "cream" | "black";
  zoomDir?: "in" | "out" | "none";
}

const CHARS_PER_SEC = 28;
const LINE_H = 50;
const FONT_SIZE = 27;

// Semantic terminal status colors (not brand palette)
const OK_GREEN = "#3fce8c";
const ERR_RED = "#ff6f66";
const TRAFFIC = ["#ff5f57", "#febc2e", "#28c840"];

const easeOut = (x: number) => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);

/**
 * A rendered macOS terminal window (not a screenshot): dark panel, traffic
 * lights, character-by-character command typing with a blinking block cursor,
 * instant output lines, green/red status lines, auto-scroll. Themed backdrop
 * with a soft accent wash, slow push-in on the whole window.
 */
export const TerminalScene: React.FC<TerminalSceneProps> = ({
  title,
  lines,
  bg = "cream",
  zoomDir = "in",
}) => {
  const theme = useTheme();
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dark = bg === "black";
  const base = dark ? theme.black : theme.cream;

  // ---- window geometry ----
  const winW = 950;
  const winH = 780;
  const barH = 68;
  const padX = 40;
  const padY = 30;
  const viewH = winH - barH - padY * 2;

  // ---- slow push on the window ----
  const push =
    zoomDir === "none"
      ? 1
      : zoomDir === "in"
        ? interpolate(frame, [0, durationInFrames], [1, 1.06])
        : interpolate(frame, [0, durationInFrames], [1.06, 1]);

  const enter = spring({
    frame,
    fps,
    config: { damping: 17, stiffness: 130, mass: 0.7 },
    durationInFrames: 20,
  });

  // ---- per-line visibility / typing progress (deterministic from frame) ----
  const visible = lines
    .map((line, i) => ({ line, i }))
    .filter(({ line }) => t >= line.at);

  // the line that owns the cursor: the last visible cmd line, but only when
  // nothing newer has appeared after it (a fresh output line "takes over")
  const lastVisibleIdx = visible.length
    ? visible[visible.length - 1].i
    : -1;

  // a fresh $ prompt (blinking cursor) lands once the final line has settled,
  // so the window never hard-freezes at the end of the scene
  const last = lines.length ? lines[lines.length - 1] : undefined;
  const lastEnd = last
    ? last.at + (last.kind === "cmd" ? last.text.length / CHARS_PER_SEC : 0)
    : 0;
  const promptAt = lastEnd + 0.45;
  const showPrompt = Boolean(last && last.kind !== "cmd" && t >= promptAt);

  // smooth auto-scroll: each line contributes its height with a short ramp,
  // so the scroll position is a continuous function of the frame
  let contentH = 0;
  visible.forEach(({ line }) => {
    contentH += LINE_H * easeOut((t - line.at) / 0.2);
  });
  if (showPrompt) contentH += LINE_H * easeOut((t - promptAt) / 0.2);
  const scrollY = Math.max(0, contentH - viewH);

  const cursorOn = Math.floor(frame / 16) % 2 === 0;

  return (
    <AbsoluteFill
      style={{
        background: base,
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* themed wash — accent glow + soft vignette, never a flat backdrop */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(1000px 780px at 18% 10%, ${theme.accentSoft}, transparent 62%),
            radial-gradient(1200px 950px at 86% 92%, ${
              dark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.07)"
            }, transparent 58%)`,
        }}
      />

      <div
        style={{
          transform: `scale(${push})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div
          style={{
            width: winW,
            height: winH,
            borderRadius: theme.radius.card,
            overflow: "hidden",
            boxShadow: dark ? theme.shadow.cardOnDark : theme.shadow.card,
            background: `linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.015)), ${theme.black}`,
            border: "1px solid rgba(255,255,255,0.08)",
            opacity: enter,
            transform: `translateY(${(1 - enter) * 46}px) scale(${
              0.965 + 0.035 * enter
            })`,
          }}
        >
          {/* title bar */}
          <div
            style={{
              height: barH,
              display: "flex",
              alignItems: "center",
              padding: "0 26px",
              background: "rgba(255,255,255,0.05)",
              borderBottom: "1px solid rgba(255,255,255,0.07)",
              position: "relative",
            }}
          >
            <div style={{ display: "flex", gap: 13 }}>
              {TRAFFIC.map((c) => (
                <div
                  key={c}
                  style={{
                    width: 19,
                    height: 19,
                    borderRadius: "50%",
                    background: c,
                  }}
                />
              ))}
            </div>
            {title && (
              <div
                style={{
                  position: "absolute",
                  left: 0,
                  right: 0,
                  textAlign: "center",
                  fontFamily: theme.mono,
                  fontSize: 22,
                  color: theme.mutedOnDark,
                  pointerEvents: "none",
                }}
              >
                {title}
              </div>
            )}
          </div>

          {/* scrolling console body */}
          <div
            style={{
              height: winH - barH,
              padding: `${padY}px ${padX}px`,
              overflow: "hidden",
            }}
          >
            <div style={{ transform: `translateY(${-scrollY}px)` }}>
              {visible.map(({ line, i }) => {
                const local = t - line.at;
                const isCmd = line.kind === "cmd";

                // cmd lines type on; everything else pops in instantly
                const typed = isCmd
                  ? line.text.slice(
                      0,
                      Math.floor(local * CHARS_PER_SEC)
                    )
                  : line.text;
                const doneTyping =
                  !isCmd || typed.length >= line.text.length;
                const hasCursor =
                  isCmd && (i === lastVisibleIdx || !doneTyping);

                const pop = isCmd
                  ? 1
                  : spring({
                      frame: frame - Math.round(line.at * fps),
                      fps,
                      config: { damping: 20, stiffness: 260, mass: 0.5 },
                      durationInFrames: 8,
                    });

                const color =
                  line.kind === "cmd"
                    ? theme.inkOnDark
                    : line.kind === "ok"
                      ? OK_GREEN
                      : line.kind === "err"
                        ? ERR_RED
                        : theme.mutedOnDark;

                return (
                  <div
                    key={i}
                    style={{
                      height: LINE_H,
                      display: "flex",
                      alignItems: "center",
                      fontFamily: theme.mono,
                      fontSize: FONT_SIZE,
                      whiteSpace: "pre",
                      color,
                      opacity: pop,
                      transform: `translateY(${(1 - pop) * 8}px)`,
                    }}
                  >
                    {isCmd && (
                      <span
                        style={{
                          color: theme.accent,
                          fontWeight: 700,
                          marginRight: 16,
                        }}
                      >
                        $
                      </span>
                    )}
                    {line.kind === "ok" && (
                      <span style={{ marginRight: 14 }}>✓</span>
                    )}
                    {line.kind === "err" && (
                      <span style={{ marginRight: 14 }}>✗</span>
                    )}
                    <span style={{ fontWeight: isCmd ? 600 : 400 }}>
                      {typed}
                    </span>
                    {hasCursor && (doneTyping ? cursorOn : true) && (
                      <span
                        style={{
                          display: "inline-block",
                          width: FONT_SIZE * 0.58,
                          height: FONT_SIZE * 1.18,
                          marginLeft: 4,
                          background: theme.inkOnDark,
                          opacity: 0.9,
                        }}
                      />
                    )}
                  </div>
                );
              })}
              {showPrompt && (
                <div
                  style={{
                    height: LINE_H,
                    display: "flex",
                    alignItems: "center",
                    fontFamily: theme.mono,
                    fontSize: FONT_SIZE,
                  }}
                >
                  <span
                    style={{
                      color: theme.accent,
                      fontWeight: 700,
                      marginRight: 16,
                    }}
                  >
                    $
                  </span>
                  {cursorOn && (
                    <span
                      style={{
                        display: "inline-block",
                        width: FONT_SIZE * 0.58,
                        height: FONT_SIZE * 1.18,
                        background: theme.inkOnDark,
                        opacity: 0.9,
                      }}
                    />
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
