import React from "react";
import {
  AbsoluteFill,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { useTheme } from "../theme/tokens";
import type { Scene } from "../types";

/* oss-alt bespoke scenes — user-storyboarded reel. Two-accent system on nick
 * tokens: CYAN = open-source/free, RED = paid/warning. */
const CYAN = "#0aa9c2";
const RED = "#e0244a";
const GREEN = "#1fa864";
const SANS = "-apple-system,'SF Pro Display','Helvetica Neue',Inter,sans-serif";

const easeOut = (x: number) => 1 - Math.pow(1 - x, 3);

const Face: React.FC<{ src: string; from?: number; focusX?: number; scale?: number }> = ({
  src,
  from,
  focusX,
  scale = 1,
}) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      <Video
        src={staticFile(src)}
        startFrom={Math.round((from ?? 0) * fps)}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          objectPosition: `${(focusX ?? 0.5) * 100}% 50%`,
        }}
      />
    </AbsoluteFill>
  );
};

/* ---------- 1. HOOK: face + STOP PAYING (PAYING red), 8% punch ---------- */
export const OssHook: React.FC<{ scene: Extract<Scene, { type: "osshook" }> }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const punch = interpolate(frame, [0, 5], [1.08, 1], {
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const inP = interpolate(frame, [1, 7], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  return (
    <AbsoluteFill style={{ background: "#000", transform: `scale(${punch})` }}>
      <Face src={scene.src} from={scene.from} focusX={scene.focusX} scale={1.04} />
      <div
        style={{
          position: "absolute",
          top: 210,
          width: "100%",
          textAlign: "center",
          fontFamily: SANS,
          fontWeight: 900,
          fontSize: 150,
          letterSpacing: "-0.03em",
          lineHeight: 0.98,
          color: "#fff",
          textShadow: "0 8px 40px rgba(0,0,0,0.55)",
          opacity: inP,
          transform: `scale(${0.9 + 0.1 * inP})`,
        }}
      >
        STOP
        <br />
        <span style={{ color: RED }}>PAYING</span>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 2. NOTIFSTACK: sub cards fly in, wallet drain, red strike ---------- */
const SUBS = [
  { name: "AI WRITING", price: "$20/MO", dx: -1, dy: -1 },
  { name: "AI CODING", price: "$20/MO", dx: 1, dy: -1 },
  { name: "DESIGN TOOL", price: "$15/MO", dx: -1, dy: 0.2 },
  { name: "NOTES APP", price: "$10/MO", dx: 1, dy: 0.4 },
  { name: "VIDEO TOOL", price: "$30/MO", dx: 0, dy: 1 },
];

export const NotifStack: React.FC<{ scene: Extract<Scene, { type: "notifstack" }> }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const strikeAt = scene.strikeAt ?? 1.0;
  const faceScale = interpolate(t, [0, 0.5], [1, 0.94], {
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const CARD_W = 640;
  const positions = [
    { x: width / 2 - CARD_W / 2, y: 285 },
    { x: width / 2 - CARD_W / 2, y: 500 },
    { x: width / 2 - CARD_W / 2, y: 715 },
    { x: width / 2 - CARD_W / 2, y: 930 },
    { x: width / 2 - CARD_W / 2, y: 1145 },
  ];
  const strikeP = interpolate(t, [strikeAt, strikeAt + 0.28], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const labelP = interpolate(t, [strikeAt + 0.15, strikeAt + 0.45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ filter: "brightness(0.65)" }}>
        <Face src={scene.src} from={scene.from} focusX={scene.focusX} scale={faceScale} />
      </AbsoluteFill>
      {SUBS.map((s, i) => {
        const delay = i * 0.1;
        const p = spring({
          frame: frame - Math.round(delay * fps),
          fps,
          config: { damping: 16, stiffness: 220 },
          durationInFrames: 14,
        });
        const pos = positions[i];
        const offX = s.dx * (1 - p) * 900;
        const offY = s.dy * (1 - p) * 1100;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: pos.x + offX,
              top: pos.y + offY,
              width: CARD_W,
              borderRadius: 22,
              background: "rgba(255,255,255,0.97)",
              boxShadow: "0 24px 60px rgba(0,0,0,0.45)",
              padding: "26px 34px",
              opacity: p,
              fontFamily: SANS,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ fontWeight: 800, fontSize: 40, color: "#141414" }}>{s.name}</div>
              <div style={{ fontWeight: 900, fontSize: 40, color: RED }}>{s.price}</div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 10 }}>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 800,
                  letterSpacing: "0.06em",
                  color: "#fff",
                  background: RED,
                  borderRadius: 8,
                  padding: "4px 12px",
                }}
              >
                RENEWED
              </div>
              <div style={{ fontSize: 26, color: "rgba(20,20,20,0.5)", fontWeight: 600 }}>
                just now
              </div>
            </div>
          </div>
        );
      })}
      {/* wallet + escaping dollars */}
      {(() => {
        const wp = spring({
          frame: frame - Math.round(0.5 * fps),
          fps,
          config: { damping: 15, stiffness: 200 },
          durationInFrames: 14,
        });
        return (
          <>
            <div
              style={{
                position: "absolute",
                left: width / 2 - 90,
                top: 1420,
                width: 180,
                height: 150,
                opacity: wp,
                transform: `translateY(${(1 - wp) * 200}px)`,
              }}
            >
              <svg viewBox="0 0 120 100" width={180} height={150}>
                <rect x="6" y="22" width="108" height="72" rx="14" fill="#8a5a2b" />
                <rect x="6" y="22" width="108" height="20" rx="10" fill="#a06c36" />
                <rect x="76" y="48" width="38" height="26" rx="10" fill="#c9944d" />
                <circle cx="88" cy="61" r="6" fill="#5c3a17" />
              </svg>
            </div>
            {[0, 1, 2, 3, 4].map((i) => {
              const start = 0.55 + i * 0.09;
              const p = interpolate(t, [start, start + 0.5], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              });
              if (p <= 0) return null;
              const target = positions[i];
              const sx = width / 2;
              const sy = 1470;
              const x = sx + (target.x + CARD_W - 60 - sx) * p;
              const y = sy + (target.y + 40 - sy) * p - Math.sin(p * Math.PI) * 160;
              return (
                <div
                  key={`d${i}`}
                  style={{
                    position: "absolute",
                    left: x,
                    top: y,
                    fontFamily: SANS,
                    fontWeight: 900,
                    fontSize: 52,
                    color: "#7ee081",
                    textShadow: "0 3px 14px rgba(0,0,0,0.5)",
                    opacity: 1 - p * 0.25,
                  }}
                >
                  $
                </div>
              );
            })}
          </>
        );
      })()}
      {/* red diagonal strike across the stack */}
      <div
        style={{
          position: "absolute",
          left: 130,
          top: 640,
          width: 900 * strikeP,
          height: 22,
          background: RED,
          borderRadius: 11,
          transform: "rotate(28deg)",
          transformOrigin: "left center",
          boxShadow: "0 6px 24px rgba(224,36,74,0.6)",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 168,
          width: "100%",
          textAlign: "center",
          fontFamily: SANS,
          fontWeight: 900,
          fontSize: 56,
          letterSpacing: "-0.01em",
          color: "#fff",
          textShadow: "0 6px 30px rgba(0,0,0,0.7)",
          opacity: labelP,
          transform: `translateY(${(1 - labelP) * 30}px)`,
        }}
      >
        CANCEL THE
        <br />
        SUBSCRIPTION SPIRAL
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 3. STRIKESWAP: PAID TOOLS ⟶ OPEN-SOURCE ALTERNATIVES ---------- */
export const StrikeSwap: React.FC<{ scene: Extract<Scene, { type: "strikeswap" }> }> = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const strike = interpolate(t, [0.14, 0.3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const swap = interpolate(t, [0.34, 0.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const check = spring({
    frame: frame - Math.round(0.45 * fps),
    fps,
    config: { damping: 12, stiffness: 260 },
    durationInFrames: 12,
  });
  return (
    <AbsoluteFill
      style={{
        background: "#0b0b0d",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: SANS,
      }}
    >
      {swap < 1 && (
        <div style={{ position: "relative", opacity: 1 - swap }}>
          <div
            style={{
              fontWeight: 900,
              fontSize: 110,
              letterSpacing: "-0.02em",
              color: "#fff",
            }}
          >
            PAID TOOLS
          </div>
          <div
            style={{
              position: "absolute",
              left: "-4%",
              top: "50%",
              width: `${108 * strike}%`,
              height: 16,
              background: RED,
              borderRadius: 8,
              transform: "rotate(-6deg)",
            }}
          />
        </div>
      )}
      {swap > 0 && (
        <div
          style={{
            position: "absolute",
            textAlign: "center",
            opacity: swap,
            transform: `scale(${0.92 + 0.08 * swap})`,
          }}
        >
          <div style={{ fontWeight: 900, fontSize: 96, letterSpacing: "-0.02em", lineHeight: 1.04 }}>
            <span style={{ color: CYAN }}>OPEN-SOURCE</span>
            <br />
            <span style={{ color: "#fff" }}>ALTERNATIVES</span>
          </div>
          <div
            style={{
              marginTop: 42,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 18,
              opacity: check,
              transform: `scale(${0.6 + 0.4 * check})`,
            }}
          >
            <svg viewBox="0 0 40 40" width={64} height={64}>
              <circle cx="20" cy="20" r="19" fill={GREEN} />
              <path
                d="M11 20.5 L17.5 27 L29 14.5"
                stroke="#fff"
                strokeWidth="5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div style={{ fontWeight: 800, fontSize: 54, color: "#fff" }}>LEGAL + FREE</div>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 4. SEARCHSPOTLIGHT: footage + cyan outline + cursor dot ---------- */
export const SearchSpotlight: React.FC<{
  scene: Extract<Scene, { type: "searchspotlight" }>;
}> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const r = scene.rect;
  const rectP = r
    ? interpolate(t, [scene.rectAt ?? 0.2, (scene.rectAt ?? 0.2) + 0.35], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: easeOut,
      })
    : 0;
  const pulse = 0.55 + 0.45 * Math.sin(t * 6);
  // cursor keyframe interpolation
  let cx = -100;
  let cy = -100;
  const kf = scene.cursor ?? [];
  if (kf.length > 0) {
    if (t <= kf[0].t) {
      cx = kf[0].x;
      cy = kf[0].y;
    } else if (t >= kf[kf.length - 1].t) {
      cx = kf[kf.length - 1].x;
      cy = kf[kf.length - 1].y;
    } else {
      for (let i = 0; i < kf.length - 1; i++) {
        if (t >= kf[i].t && t <= kf[i + 1].t) {
          const k = easeOut((t - kf[i].t) / (kf[i + 1].t - kf[i].t));
          cx = kf[i].x + k * (kf[i + 1].x - kf[i].x);
          cy = kf[i].y + k * (kf[i + 1].y - kf[i].y);
        }
      }
    }
  }
  const zoom = interpolate(frame, [0, Math.max(1, (scene.durationSec ?? 2) * fps)], [1, 1.05]);
  return (
    <AbsoluteFill style={{ background: "#0b0b0d" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <Video
          src={staticFile(scene.src)}
          startFrom={Math.round((scene.from ?? 0) * fps)}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </AbsoluteFill>
      {r && rectP > 0 && (
        <>
          <div
            style={{
              position: "absolute",
              left: r.x - 10,
              top: r.y - 10,
              width: (r.w + 20) * rectP,
              height: r.h + 20,
              border: `6px solid ${CYAN}`,
              borderRadius: 20,
              boxShadow: `0 0 ${24 + 18 * pulse}px rgba(10,169,194,${0.5 + 0.3 * pulse})`,
            }}
          />
          {scene.label && (
            <div
              style={{
                position: "absolute",
                left: r.x - 10,
                top: r.y - 84,
                fontFamily: SANS,
                fontWeight: 800,
                fontSize: 40,
                letterSpacing: "0.04em",
                color: "#fff",
                background: CYAN,
                padding: "10px 24px",
                borderRadius: 14,
                opacity: rectP,
                boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
              }}
            >
              {scene.label}
            </div>
          )}
        </>
      )}
      {/* free-standing tick labels (results beat) */}
      {(scene.freeLabels ?? []).map((l, i) => {
        const p = spring({
          frame: frame - Math.round(l.at * fps),
          fps,
          config: { damping: 14, stiffness: 240 },
          durationInFrames: 12,
        });
        if (p <= 0.01) return null;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              right: 40,
              top: 1010 + i * 122,
              display: "flex",
              alignItems: "center",
              gap: 14,
              fontFamily: SANS,
              fontWeight: 900,
              fontSize: 38,
              color: "#141414",
              background: "rgba(255,255,255,0.96)",
              border: `4px solid ${CYAN}`,
              borderRadius: 18,
              padding: "12px 26px",
              boxShadow: "0 16px 40px rgba(0,0,0,0.3)",
              opacity: p,
              transform: `translateX(${(1 - p) * 220}px)`,
            }}
          >
            <svg viewBox="0 0 40 40" width={44} height={44}>
              <circle cx="20" cy="20" r="19" fill={GREEN} />
              <path
                d="M11 20.5 L17.5 27 L29 14.5"
                stroke="#fff"
                strokeWidth="5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {l.text}
          </div>
        );
      })}
      {/* big cursor dot with soft white ring */}
      {kf.length > 0 && (
        <div
          style={{
            position: "absolute",
            left: cx - 34,
            top: cy - 34,
            width: 68,
            height: 68,
            borderRadius: "50%",
            background: "rgba(255,255,255,0.35)",
            border: "3px solid rgba(255,255,255,0.9)",
            boxShadow: "0 4px 24px rgba(0,0,0,0.35)",
          }}
        >
          <div
            style={{
              position: "absolute",
              left: 22,
              top: 22,
              width: 24,
              height: 24,
              borderRadius: "50%",
              background: "#141414",
            }}
          />
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 5. STACKWINDOWS: five mini windows + big claim ---------- */
export const StackWindows: React.FC<{ scene: Extract<Scene, { type: "stackwindows" }> }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const theme = useTheme();
  const W = 560;
  const H = 430;
  const slots = [
    { x: 60, y: 210, r: -5 },
    { x: width - W - 60, y: 330, r: 4 },
    { x: 100, y: 620, r: -3 },
    { x: width - W - 100, y: 740, r: 5 },
    { x: width / 2 - W / 2, y: 1010, r: -2 },
  ];
  const t1 = spring({
    frame: frame - Math.round(0.75 * fps),
    fps,
    config: { damping: 14, stiffness: 220 },
    durationInFrames: 14,
  });
  return (
    <AbsoluteFill style={{ background: theme.cream }}>
      {scene.shots.slice(0, 5).map((s, i) => {
        const p = spring({
          frame: frame - i * 3,
          fps,
          config: { damping: 15, stiffness: 240 },
          durationInFrames: 13,
        });
        const slot = slots[i];
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: slot.x,
              top: slot.y,
              width: W,
              borderRadius: 18,
              overflow: "hidden",
              boxShadow: "0 26px 70px rgba(0,0,0,0.3)",
              transform: `rotate(${slot.r}deg) scale(${0.5 + 0.5 * p})`,
              opacity: p,
              background: "#fff",
            }}
          >
            <div
              style={{
                height: 54,
                background: "#ece7db",
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "0 18px",
              }}
            >
              <div style={{ width: 16, height: 16, borderRadius: 8, background: "#e8695a" }} />
              <div style={{ width: 16, height: 16, borderRadius: 8, background: "#e8c35a" }} />
              <div style={{ width: 16, height: 16, borderRadius: 8, background: "#79c877" }} />
              <div
                style={{
                  marginLeft: 12,
                  fontFamily: SANS,
                  fontWeight: 700,
                  fontSize: 24,
                  color: "rgba(20,20,20,0.6)",
                }}
              >
                {s.label}
              </div>
            </div>
            <Video
              src={staticFile(s.src)}
              startFrom={Math.round(s.from * fps)}
              muted
              style={{ width: "100%", height: H - 54, objectFit: "cover", objectPosition: "50% 18%" }}
            />
          </div>
        );
      })}
      <div
        style={{
          position: "absolute",
          bottom: 260,
          width: "100%",
          textAlign: "center",
          fontFamily: SANS,
          fontWeight: 900,
          fontSize: 84,
          letterSpacing: "-0.02em",
          lineHeight: 1.02,
          color: theme.ink,
          opacity: t1,
          transform: `translateY(${(1 - t1) * 60}px)`,
          textShadow: "0 2px 0 rgba(255,255,255,0.6)",
        }}
      >
        {scene.title1}
        <br />
        <span style={{ color: CYAN }}>{scene.title2}</span>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 6. PROBLEMSOLVED: red vs cyan cards → one check ---------- */
export const ProblemSolved: React.FC<{ scene: Extract<Scene, { type: "problemsolved" }> }> = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const theme = useTheme();
  const left = spring({ frame, fps, config: { damping: 15, stiffness: 220 }, durationInFrames: 13 });
  const right = spring({
    frame: frame - 5,
    fps,
    config: { damping: 15, stiffness: 220 },
    durationInFrames: 13,
  });
  const arrows = interpolate(frame / fps, [0.45, 0.72], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const check = spring({
    frame: frame - Math.round(0.74 * fps),
    fps,
    config: { damping: 11, stiffness: 260 },
    durationInFrames: 12,
  });
  const CW = 470;
  const row = (txt: string, ok: boolean, key: number) => (
    <div
      key={key}
      style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 18, fontSize: 33,
               fontWeight: 650, color: "rgba(20,20,20,0.78)" }}
    >
      <span style={{ color: ok ? CYAN : RED, fontWeight: 900, fontSize: 36 }}>
        {ok ? "✓" : "•"}
      </span>
      {txt}
    </div>
  );
  return (
    <AbsoluteFill style={{ background: theme.cream, fontFamily: SANS }}>
      {/* left / paid */}
      <div
        style={{
          position: "absolute",
          left: 40,
          top: 360,
          width: CW,
          borderRadius: 26,
          background: "#fff",
          borderTop: `14px solid ${RED}`,
          boxShadow: "0 26px 70px rgba(0,0,0,0.18)",
          padding: "36px 36px 42px",
          opacity: left,
          transform: `translateY(${(1 - left) * 120}px)`,
        }}
      >
        <svg viewBox="0 0 48 48" width={64} height={64}>
          <path
            d="M24 8 a16 16 0 1 1 -11.3 4.7"
            fill="none"
            stroke={RED}
            strokeWidth="5"
            strokeLinecap="round"
          />
          <path d="M8 4 L14 14 L4 15 Z" fill={RED} />
          <text x="24" y="30" textAnchor="middle" fontSize="15" fontWeight="800" fill={RED}>
            $
          </text>
        </svg>
        <div style={{ fontWeight: 900, fontSize: 44, color: "#141414", marginTop: 16, lineHeight: 1.05 }}>
          PAID TOOL
        </div>
        {row("Monthly subscription", false, 0)}
        {row("Closed source", false, 1)}
      </div>
      {/* right / open source */}
      <div
        style={{
          position: "absolute",
          right: 40,
          top: 360,
          width: CW,
          borderRadius: 26,
          background: "#fff",
          borderTop: `14px solid ${CYAN}`,
          boxShadow: "0 26px 70px rgba(0,0,0,0.18)",
          padding: "36px 36px 42px",
          opacity: right,
          transform: `translateY(${(1 - right) * 120}px)`,
        }}
      >
        <svg viewBox="0 0 48 48" width={64} height={64}>
          <rect x="10" y="22" width="28" height="20" rx="5" fill="none" stroke={CYAN} strokeWidth="5" />
          <path d="M16 22 v-5 a8 8 0 0 1 15 -3" fill="none" stroke={CYAN} strokeWidth="5" strokeLinecap="round" />
        </svg>
        <div style={{ fontWeight: 900, fontSize: 44, color: "#141414", marginTop: 16, lineHeight: 1.05 }}>
          OPEN-SOURCE ALTERNATIVE
        </div>
        {row("Free to use", true, 0)}
        {row("Customizable", true, 1)}
      </div>
      {/* converging arrows */}
      <svg
        viewBox={`0 0 ${width} 1920`}
        width={width}
        height={1920}
        style={{ position: "absolute", inset: 0 }}
      >
        <path
          d={`M ${40 + CW / 2} 900 Q ${width / 2 - 120} 1060 ${width / 2 - 30} 1120`}
          fill="none"
          stroke={RED}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray="500"
          strokeDashoffset={500 * (1 - arrows)}
        />
        <path
          d={`M ${width - 40 - CW / 2} 900 Q ${width / 2 + 120} 1060 ${width / 2 + 30} 1120`}
          fill="none"
          stroke={CYAN}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray="500"
          strokeDashoffset={500 * (1 - arrows)}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          top: 1130,
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
          opacity: check,
          transform: `scale(${0.5 + 0.5 * check})`,
        }}
      >
        <svg viewBox="0 0 40 40" width={150} height={150}>
          <circle cx="20" cy="20" r="19" fill={GREEN} />
          <path
            d="M11 20.5 L17.5 27 L29 14.5"
            stroke="#fff"
            strokeWidth="5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <div style={{ fontWeight: 900, fontSize: 66, color: "#141414" }}>PROBLEM SOLVED</div>
        <div style={{ fontWeight: 600, fontSize: 30, color: "rgba(20,20,20,0.55)" }}>
          same need · different price tag
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 7. WALLETATTACK: notifs sneak in, jump wallet, flatten ---------- */
const ATTACKS = ["RENEWED", "PAYMENT SUCCESSFUL", "NEXT BILLING DATE", "AUTO-RENEW ON"];

export const WalletAttack: React.FC<{ scene: Extract<Scene, { type: "walletattack" }> }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const t = frame / fps;
  const jumpAt = scene.jumpAt ?? 1.6;
  const WX = width / 2;
  const WY = 1430;
  const crushed = t > jumpAt + 0.45;
  const shake = t > jumpAt + 0.2 && t < jumpAt + 0.55 ? Math.sin(t * 70) * 9 : 0;
  const critP = interpolate(t, [jumpAt + 0.55, jumpAt + 0.85], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const starts = [
    { x: -320, y: 1035 },
    { x: width + 320, y: 1075 },
    { x: -320, y: 1195 },
    { x: width + 320, y: 1235 },
  ];
  const rests = [
    { x: 70, y: 1035 },
    { x: width - 470, y: 1075 },
    { x: 100, y: 1195 },
    { x: width - 490, y: 1235 },
  ];
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Face src={scene.src} from={scene.from} focusX={scene.focusX} />
      {ATTACKS.map((a, i) => {
        const sneakStart = 0.25 + i * 0.28;
        const sneak = interpolate(t, [sneakStart, sneakStart + 0.5], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easeOut,
        });
        const jump = interpolate(t, [jumpAt, jumpAt + 0.3], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const sx = starts[i].x + (rests[i].x - starts[i].x) * sneak;
        const sy = starts[i].y + (rests[i].y - starts[i].y) * sneak;
        const x = sx + (WX - 180 - sx) * jump;
        const y = sy + (WY - 40 - sy) * jump - Math.sin(jump * Math.PI) * 260;
        const op = jump < 1 ? sneak : interpolate(t, [jumpAt + 0.3, jumpAt + 0.5], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              fontFamily: SANS,
              fontWeight: 800,
              fontSize: 30,
              color: "#141414",
              background: "rgba(255,255,255,0.97)",
              borderLeft: `10px solid ${RED}`,
              borderRadius: 14,
              padding: "16px 26px",
              boxShadow: "0 16px 40px rgba(0,0,0,0.4)",
              opacity: op,
              transform: `scale(${0.8 + 0.2 * sneak})`,
            }}
          >
            {a}
          </div>
        );
      })}
      {/* wallet */}
      <div
        style={{
          position: "absolute",
          left: WX - 120 + shake,
          top: WY,
          transform: crushed ? "scaleY(0.5) translateY(60px)" : undefined,
          transition: "none",
        }}
      >
        <svg viewBox="0 0 120 100" width={240} height={200}>
          <rect x="6" y="22" width="108" height="72" rx="14" fill="#8a5a2b" />
          <rect x="6" y="22" width="108" height="20" rx="10" fill="#a06c36" />
          <rect x="76" y="48" width="38" height="26" rx="10" fill="#c9944d" />
          <circle cx="88" cy="61" r="6" fill="#5c3a17" />
        </svg>
      </div>
      {critP > 0 && (
        <div
          style={{
            position: "absolute",
            left: WX - 330,
            top: WY + 140,
            width: 660,
            textAlign: "center",
            fontFamily: SANS,
            fontWeight: 900,
            fontSize: 46,
            color: "#fff",
            background: RED,
            borderRadius: 18,
            padding: "18px 10px",
            boxShadow: "0 18px 50px rgba(224,36,74,0.5)",
            opacity: critP,
            transform: `scale(${0.7 + 0.3 * critP})`,
          }}
        >
          BANK BALANCE: CRITICAL
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 8. FORKCUSTOMIZE ---------- */
export const ForkCustomize: React.FC<{ scene: Extract<Scene, { type: "forkcustomize" }> }> = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;
  const click = t > 0.22;
  const dup = interpolate(t, [0.28, 0.62], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const custom = interpolate(t, [0.75, 1.25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const headP = spring({
    frame: frame - Math.round(0.85 * fps),
    fps,
    config: { damping: 13, stiffness: 240 },
    durationInFrames: 12,
  });
  const cardColor = custom < 0.5 ? CYAN : "#7c5cff";
  const CW = 620;
  const baseX = width / 2 - CW / 2;
  const copyX = baseX + dup * 0;
  const copyY = 600 + dup * 330;
  const slider = (label: string, i: number) => {
    const p = Math.min(1, Math.max(0, (custom - i * 0.18) * 2.2));
    return (
      <div key={label} style={{ marginTop: 26 }}>
        <div style={{ fontSize: 26, fontWeight: 700, color: "rgba(20,20,20,0.6)", marginBottom: 10 }}>
          {label}
        </div>
        <div style={{ width: 340, height: 14, borderRadius: 7, background: "rgba(20,20,20,0.12)" }}>
          <div
            style={{
              width: 340 * (0.25 + 0.6 * p),
              height: 14,
              borderRadius: 7,
              background: cardColor,
            }}
          />
        </div>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{ background: theme.cream, fontFamily: SANS }}>
      <div
        style={{
          position: "absolute",
          top: 300,
          width: "100%",
          textAlign: "center",
          fontWeight: 900,
          fontSize: 92,
          color: theme.ink,
          opacity: headP,
          transform: `translateY(${(1 - headP) * 40}px)`,
        }}
      >
        CHANGE <span style={{ color: cardColor }}>IT</span>
      </div>
      {/* original card (greys out) */}
      <div
        style={{
          position: "absolute",
          left: baseX,
          top: 600,
          width: CW,
          borderRadius: 22,
          background: "#fff",
          boxShadow: "0 22px 60px rgba(0,0,0,0.16)",
          padding: "34px 40px",
          filter: dup > 0.4 ? "grayscale(1) opacity(0.55)" : "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <svg viewBox="0 0 24 24" width={44} height={44}>
            <circle cx="6" cy="6" r="3" fill="#141414" />
            <circle cx="18" cy="6" r="3" fill="#141414" />
            <circle cx="12" cy="19" r="3" fill="#141414" />
            <path d="M6 9 v3 a3 3 0 0 0 3 3 h6 a3 3 0 0 0 3 -3 V9 M12 15 v1" stroke="#141414" strokeWidth="2" fill="none" />
          </svg>
          <div style={{ fontWeight: 800, fontSize: 40, color: "#141414" }}>the-project</div>
          <div
            style={{
              marginLeft: "auto",
              fontSize: 26,
              fontWeight: 800,
              color: click ? "#fff" : "#141414",
              background: click ? CYAN : "rgba(20,20,20,0.08)",
              borderRadius: 12,
              padding: "10px 24px",
              transform: click && t < 0.34 ? "scale(0.92)" : "scale(1)",
            }}
          >
            ⑂ FORK
          </div>
        </div>
        <div style={{ marginTop: 22, fontSize: 28, color: "rgba(20,20,20,0.55)", fontWeight: 600 }}>
          open-source licence · public code
        </div>
      </div>
      {/* the copy */}
      {dup > 0 && (
        <div
          style={{
            position: "absolute",
            left: copyX,
            top: copyY,
            width: CW,
            borderRadius: 22 + custom * 22,
            background: "#fff",
            border: `8px solid ${cardColor}`,
            boxShadow: "0 30px 80px rgba(0,0,0,0.25)",
            padding: "34px 40px",
            opacity: Math.min(1, dup * 1.4),
            display: "flex",
            gap: 30,
          }}
        >
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <div style={{ fontWeight: 800, fontSize: 40, color: "#141414" }}>the-project</div>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: 800,
                  color: "#fff",
                  background: cardColor,
                  borderRadius: 10,
                  padding: "6px 16px",
                }}
              >
                YOUR COPY
              </div>
            </div>
            <div style={{ marginTop: 8, fontSize: 26, color: "rgba(20,20,20,0.5)", fontWeight: 600 }}>
              yours to edit — every file
            </div>
            {slider("COLOUR", 0)}
          </div>
          <div style={{ width: 340 }}>
            {slider("LAYOUT", 1)}
            {(() => {
              const p = Math.min(1, Math.max(0, (custom - 0.4) * 2.2));
              return (
                <div style={{ marginTop: 26 }}>
                  <div
                    style={{ fontSize: 26, fontWeight: 700, color: "rgba(20,20,20,0.6)", marginBottom: 10 }}
                  >
                    FEATURES
                  </div>
                  <div
                    style={{
                      width: 96,
                      height: 52,
                      borderRadius: 26,
                      background: p > 0.5 ? cardColor : "rgba(20,20,20,0.15)",
                      position: "relative",
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        top: 6,
                        left: 6 + p * 44,
                        width: 40,
                        height: 40,
                        borderRadius: 20,
                        background: "#fff",
                        boxShadow: "0 3px 10px rgba(0,0,0,0.25)",
                      }}
                    />
                  </div>
                </div>
              );
            })()}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 9. SELFHOST: laptop → glowing line → server, padlock opens ---------- */
export const SelfHost: React.FC<{ scene: Extract<Scene, { type: "selfhost" }> }> = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;
  const move = interpolate(t, [0.06, 0.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const line = interpolate(t, [0.42, 0.85], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const unlockP = interpolate(t, [0.88, 1.05], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const labels = spring({
    frame: frame - Math.round(0.95 * fps),
    fps,
    config: { damping: 13, stiffness: 220 },
    durationInFrames: 13,
  });
  const LX = width / 2;
  const LY = 660;
  const SY = 1260;
  const pulse = 0.5 + 0.5 * Math.sin(t * 7);
  return (
    <AbsoluteFill style={{ background: "#0b0b0d", fontFamily: SANS }}>
      {/* project chip flying into laptop */}
      <div
        style={{
          position: "absolute",
          left: LX - 130,
          top: 430 + move * 130,
          width: 260,
          borderRadius: 16,
          background: "#fff",
          border: `6px solid #7c5cff`,
          padding: "14px 20px",
          fontWeight: 800,
          fontSize: 30,
          color: "#141414",
          textAlign: "center",
          opacity: 1 - move * 0.7,
          transform: `scale(${1 - move * 0.5})`,
        }}
      >
        the-project
      </div>
      {/* laptop */}
      <svg
        viewBox="0 0 200 120"
        width={360}
        height={216}
        style={{ position: "absolute", left: LX - 180, top: LY - 60 }}
      >
        <rect x="35" y="10" width="130" height="80" rx="8" fill="#1c1c22" stroke="#5a5a68" strokeWidth="4" />
        <rect x="43" y="18" width="114" height="64" rx="4" fill="#101014" />
        <text x="100" y="55" textAnchor="middle" fontSize="17" fontWeight="800" fill="#7c5cff">
          the-project
        </text>
        <rect x="15" y="92" width="170" height="12" rx="6" fill="#2c2c34" />
      </svg>
      {/* glowing connection */}
      <svg
        viewBox={`0 0 ${width} 1920`}
        width={width}
        height={1920}
        style={{ position: "absolute", inset: 0 }}
      >
        <path
          d={`M ${LX} ${LY + 170} L ${LX} ${SY - 40}`}
          stroke={CYAN}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray="480"
          strokeDashoffset={480 * (1 - line)}
          style={{ filter: `drop-shadow(0 0 ${12 + 10 * pulse}px ${CYAN})` }}
        />
      </svg>
      {/* server */}
      <svg
        viewBox="0 0 160 140"
        width={280}
        height={245}
        style={{ position: "absolute", left: LX - 140, top: SY - 20, opacity: 0.3 + 0.7 * line }}
      >
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <rect x="20" y={12 + i * 42} width="120" height="34" rx="8" fill="#1c1c22" stroke="#5a5a68" strokeWidth="3" />
            <circle cx="38" cy={29 + i * 42} r="5" fill={line > 0.9 ? "#37e08b" : "#444"} />
            <rect x="56" y={24 + i * 42} width="70" height="4" rx="2" fill="#3c3c46" />
            <rect x="56" y={33 + i * 42} width="46" height="4" rx="2" fill="#33333c" />
          </g>
        ))}
      </svg>
      <div
        style={{
          position: "absolute",
          left: LX + 150,
          top: SY + 60,
          fontWeight: 800,
          fontSize: 34,
          color: "#fff",
          background: "rgba(10,169,194,0.2)",
          border: `4px solid ${CYAN}`,
          borderRadius: 14,
          padding: "10px 22px",
          opacity: 0.2 + 0.8 * line,
        }}
      >
        YOUR SERVER
      </div>
      {/* padlock above, opens */}
      <svg viewBox="0 0 48 48" width={120} height={120} style={{ position: "absolute", left: LX - 60, top: 300 }}>
        <rect x="10" y="22" width="28" height="20" rx="5" fill="none" stroke={unlockP > 0.5 ? GREEN : "#8a8a96"} strokeWidth="5" />
        {unlockP > 0.5 ? (
          <path d="M16 22 v-5 a8 8 0 0 1 15 -3" fill="none" stroke={GREEN} strokeWidth="5" strokeLinecap="round" />
        ) : (
          <path d="M16 22 v-6 a8 8 0 0 1 16 0 v6" fill="none" stroke="#8a8a96" strokeWidth="5" strokeLinecap="round" />
        )}
      </svg>
      {/* end labels */}
      <div
        style={{
          position: "absolute",
          bottom: 190,
          width: "100%",
          display: "flex",
          justifyContent: "center",
          gap: 34,
          opacity: labels,
          transform: `translateY(${(1 - labels) * 50}px)`,
        }}
      >
        {["YOUR VERSION", "YOUR CONTROL"].map((l) => (
          <div
            key={l}
            style={{
              fontWeight: 900,
              fontSize: 46,
              color: "#fff",
              background: "rgba(255,255,255,0.08)",
              border: `5px solid ${CYAN}`,
              borderRadius: 18,
              padding: "16px 34px",
            }}
          >
            {l}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- 10. CHECKOUTBLOCK: checkout card blocked over facecam ---------- */
export const CheckoutBlock: React.FC<{ scene: Extract<Scene, { type: "checkoutblock" }> }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const push = interpolate(frame, [0, durationInFrames], [1, 1.08]);
  const cardIn = spring({
    frame: frame - Math.round(0.15 * fps),
    fps,
    config: { damping: 15, stiffness: 200 },
    durationInFrames: 14,
  });
  const freezeAt = scene.freezeAt ?? 1.15;
  const cursorP = interpolate(t, [0.45, freezeAt], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (x) => x * x * (3 - 2 * x),
  });
  const warned = t >= freezeAt;
  const coverP = interpolate(t, [freezeAt + 0.25, freezeAt + 0.55], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const trashP = interpolate(t, [freezeAt + 0.95, freezeAt + 1.35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easeOut,
  });
  const CW = 640;
  const CX = width / 2 - CW / 2;
  const CY = 430;
  const btnX = CX + CW / 2;
  const btnY = CY + 470;
  const curX = CX + CW + 140 + (btnX + 90 - CX - CW - 140) * cursorP;
  const curY = CY - 90 + (btnY + 18 - CY + 90) * cursorP;
  const cardScale = 1 - trashP * 0.92;
  const cardTX = trashP * (width - 200 - btnX);
  const cardTY = trashP * (1500 - CY - 300);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ transform: `scale(${push})` }}>
        <Face src={scene.src} from={scene.from} focusX={scene.focusX} />
      </AbsoluteFill>
      {/* checkout window */}
      <div
        style={{
          position: "absolute",
          left: CX + cardTX,
          top: CY + cardTY,
          width: CW,
          borderRadius: 24,
          background: "rgba(255,255,255,0.98)",
          boxShadow: "0 30px 90px rgba(0,0,0,0.5)",
          padding: "40px 44px",
          fontFamily: SANS,
          opacity: cardIn * (1 - trashP * 0.2),
          transform: `translateY(${(1 - cardIn) * 90}px) scale(${cardScale})`,
          transformOrigin: "center",
        }}
      >
        <div style={{ fontWeight: 900, fontSize: 44, color: "#141414" }}>UPGRADE TO PRO</div>
        <div style={{ fontWeight: 900, fontSize: 76, color: "#141414", marginTop: 14 }}>
          $20<span style={{ fontSize: 38, fontWeight: 700, color: "rgba(20,20,20,0.55)" }}>/month</span>
        </div>
        <div
          style={{
            marginTop: 6,
            fontSize: 26,
            fontWeight: 700,
            letterSpacing: "0.08em",
            color: "rgba(20,20,20,0.5)",
          }}
        >
          BILLED MONTHLY
        </div>
        <div
          style={{
            position: "relative",
            marginTop: 34,
            borderRadius: 16,
            background: warned ? "#fff" : "#141414",
            border: warned ? `6px solid ${RED}` : "6px solid #141414",
            color: warned ? RED : "#fff",
            textAlign: "center",
            fontWeight: 800,
            fontSize: 36,
            padding: "22px 10px",
            boxShadow: warned ? `0 0 34px rgba(224,36,74,0.55)` : "none",
          }}
        >
          START SUBSCRIPTION
          {/* cyan blocker card */}
          {coverP > 0 && (
            <div
              style={{
                position: "absolute",
                left: -30,
                right: -30,
                top: -16,
                bottom: -16,
                borderRadius: 18,
                background: CYAN,
                color: "#fff",
                fontWeight: 900,
                fontSize: 34,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 20px 60px rgba(10,169,194,0.5)",
                opacity: coverP,
                transform: `translateX(${(1 - coverP) * 320}px) rotate(${(1 - coverP) * 6}deg)`,
              }}
            >
              CHECK FOR A FREE ALTERNATIVE FIRST
            </div>
          )}
        </div>
      </div>
      {/* trash bin */}
      <svg
        viewBox="0 0 48 48"
        width={130}
        height={130}
        style={{ position: "absolute", left: width - 250, top: 1440, opacity: Math.max(0.25, trashP) }}
      >
        <rect x="12" y="16" width="24" height="26" rx="4" fill="none" stroke="#fff" strokeWidth="4" />
        <path d="M8 16 h32 M18 16 v-4 h12 v4 M19 23 v13 M29 23 v13" stroke="#fff" strokeWidth="4" fill="none" strokeLinecap="round" />
      </svg>
      {/* cursor */}
      {trashP < 0.2 && (
        <div style={{ position: "absolute", left: curX, top: curY }}>
          {warned && (
            <div
              style={{
                position: "absolute",
                left: -26,
                top: -26,
                width: 84,
                height: 84,
                borderRadius: "50%",
                border: `5px solid ${RED}`,
                opacity: 0.8,
              }}
            />
          )}
          <svg viewBox="0 0 24 24" width={56} height={56} style={{ filter: "drop-shadow(0 3px 10px rgba(0,0,0,0.5))" }}>
            <path d="M5 3 L19 12.5 L12.5 13.8 L16 21 L13 22.3 L9.6 15.2 L5 19 Z" fill="#fff" stroke="#141414" strokeWidth="1.6" />
          </svg>
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- 11. COMMENTCTA ---------- */
export const CommentCta: React.FC<{ scene: Extract<Scene, { type: "commentcta" }> }> = ({
  scene,
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const t = frame / fps;
  const typeAt = scene.typeAt ?? 0.9;
  const growAt = scene.growAt ?? 1.5;
  const dropAt = scene.dropAt ?? 2.5;
  const FY = 1500;
  const typed = Math.min(4, Math.max(0, Math.floor((t - typeAt) / 0.09)));
  const word = "OPEN".slice(0, typed);
  const growP =
    t < dropAt
      ? spring({
          frame: frame - Math.round(growAt * fps),
          fps,
          config: { damping: 10, stiffness: 190 },
          durationInFrames: 16,
        })
      : 1 - interpolate(t, [dropAt, dropAt + 0.3], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easeOut,
        });
  const dmP = spring({
    frame: frame - Math.round((dropAt + 0.25) * fps),
    fps,
    config: { damping: 14, stiffness: 220 },
    durationInFrames: 14,
  });
  const finalP = spring({
    frame: frame - Math.round((dropAt + 0.55) * fps),
    fps,
    config: { damping: 13, stiffness: 200 },
    durationInFrames: 14,
  });
  const wantP = spring({
    frame: frame - Math.round(0.2 * fps),
    fps,
    config: { damping: 14, stiffness: 220 },
    durationInFrames: 13,
  });
  return (
    <AbsoluteFill style={{ background: "#000", fontFamily: SANS }}>
      <Face src={scene.src} from={scene.from} focusX={scene.focusX} />
      {/* WANT THE WEBSITE? */}
      {t < growAt + 0.2 && (
        <div
          style={{
            position: "absolute",
            top: 250,
            width: "100%",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 72,
            color: "#fff",
            textShadow: "0 6px 30px rgba(0,0,0,0.6)",
            opacity: wantP * (t > growAt ? 1 - (t - growAt) * 5 : 1),
            transform: `translateY(${(1 - wantP) * 40}px)`,
          }}
        >
          WANT THE WEBSITE?
        </div>
      )}
      {/* comment field */}
      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          top: FY,
          height: 108,
          borderRadius: 54,
          background: "rgba(255,255,255,0.97)",
          boxShadow: "0 18px 50px rgba(0,0,0,0.45)",
          display: "flex",
          alignItems: "center",
          padding: "0 44px",
          fontSize: 38,
          fontWeight: 600,
          color: word ? "#141414" : "rgba(20,20,20,0.4)",
        }}
      >
        {t >= dropAt + 0.3 ? (
          <span style={{ fontWeight: 900, color: CYAN }}>OPEN</span>
        ) : word && growP < 0.2 ? (
          <span style={{ fontWeight: 900 }}>{word}</span>
        ) : (
          "Add a comment…"
        )}
        <span
          style={{
            marginLeft: 6,
            width: 4,
            height: 46,
            background: "#141414",
            opacity: t > typeAt - 0.35 && t < dropAt && Math.floor(t * 3) % 2 === 0 ? 1 : 0,
          }}
        />
        <div style={{ marginLeft: "auto", fontWeight: 800, color: CYAN, fontSize: 34 }}>Post</div>
      </div>
      {/* big bouncing word card */}
      {growP > 0.02 && t < dropAt + 0.3 && (
        <div
          style={{
            position: "absolute",
            left: width / 2 - 380,
            top: 640,
            width: 760,
            borderRadius: 44,
            background: "#fff",
            boxShadow: "0 40px 110px rgba(0,0,0,0.5)",
            textAlign: "center",
            padding: "70px 20px 58px",
            opacity: Math.min(1, growP * 1.6),
            transform: `scale(${0.2 + 0.8 * growP}) translateY(${(1 - growP) * 500}px)`,
          }}
        >
          <div style={{ fontWeight: 900, fontSize: 190, letterSpacing: "0.02em", color: CYAN, lineHeight: 0.95 }}>
            OPEN
          </div>
          <div
            style={{
              marginTop: 26,
              fontWeight: 800,
              fontSize: 34,
              letterSpacing: "0.12em",
              color: "rgba(20,20,20,0.55)",
            }}
          >
            COMMENT THIS WORD
          </div>
        </div>
      )}
      {/* DM notification */}
      {dmP > 0.02 && (
        <div
          style={{
            position: "absolute",
            left: width / 2 - 300,
            top: 150 + (1 - dmP) * -220,
            width: 600,
            borderRadius: 24,
            background: "rgba(255,255,255,0.97)",
            boxShadow: "0 24px 70px rgba(0,0,0,0.5)",
            display: "flex",
            alignItems: "center",
            gap: 22,
            padding: "24px 32px",
            opacity: dmP,
          }}
        >
          <div
            style={{
              width: 74,
              height: 74,
              borderRadius: 37,
              background: `linear-gradient(135deg, ${CYAN}, #7c5cff)`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <svg viewBox="0 0 24 24" width={40} height={40}>
              <path d="M3 11 L21 3 L14 21 L11 13 Z" fill="#fff" />
            </svg>
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 36, color: "#141414" }}>Link sent ✓</div>
            <div style={{ fontWeight: 600, fontSize: 27, color: "rgba(20,20,20,0.5)" }}>
              check your DMs
            </div>
          </div>
        </div>
      )}
      {/* final display */}
      {finalP > 0.02 && (
        <div
          style={{
            position: "absolute",
            top: 640,
            width: "100%",
            textAlign: "center",
            fontWeight: 900,
            fontSize: 96,
            color: "#fff",
            textShadow: "0 8px 40px rgba(0,0,0,0.65)",
            opacity: finalP,
            transform: `scale(${0.85 + 0.15 * finalP})`,
          }}
        >
          COMMENT
          <br />
          <span
            style={{
              display: "inline-block",
              marginTop: 18,
              color: "#fff",
              background: CYAN,
              borderRadius: 28,
              padding: "10px 54px",
            }}
          >
            “OPEN”
          </span>
        </div>
      )}
    </AbsoluteFill>
  );
};
