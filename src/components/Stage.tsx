import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  OffthreadVideo,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useTheme } from "../theme/tokens";
import { Credit } from "./Credit";

/**
 * STAGE — a graphic that ACTS OUT the sentence being spoken (2026-09-15).
 *
 * Learned from woke_engineer's reels, where nearly every sentence gets its own
 * little scene: a number becomes that many things, a cause becomes a line with
 * a pulse running along it, a claim that loses gets faded or struck out. What
 * carries over is the GRAMMAR, not his pictures (user, same day: "different
 * topic ... different things in different ways from video to video").
 *
 * So a stage has no built-in subject. A beat sheet supplies:
 *   elements — the topic's own things: `card` (title + lines), `image` (a real
 *              still: product shot, logo), `text` (a big label), `number`
 *   moves    — verbs timed to the spoken word, in seconds into the scene:
 *              arrive  exit  dim  focus  highlight  stamp  strike  count  connect
 *   set      — light | dark | brand, so two stages need not share a look
 *   layout   — full (the graphic owns the frame above the caption band) or
 *              split (graphic in the top 42%, presenter below, his measured seam)
 *
 * Positions are fractions of the stage area (x, y = centre; w = width), so a
 * plan reads like a sketch, not pixel arithmetic. G65 blocks a stage that
 * would draw nothing or crash, G66 advises on moves that never show, G15
 * wants a source on every number, and G67 advises when one move carries every
 * idea or a stage repeats a recent reel's picture exactly.
 */

export interface StageElement {
  id: string;
  kind: "card" | "image" | "text" | "number";
  /** centre, as fractions of the stage area */
  x: number;
  y: number;
  /** width, as a fraction of the stage width */
  w: number;
  /** image: height as a fraction of stage width (default 0.8 * w) */
  h?: number;
  title?: string;
  lines?: string[];
  tone?: "light" | "dark" | "accent";
  src?: string;
  text?: string;
  /** text: 1 = 76px */
  size?: number;
  value?: number;
  from?: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  label?: string;
  /** number: who reported it (G15) */
  source?: string;
}

export type StageVerb =
  | "arrive" | "exit" | "dim" | "focus" | "highlight" | "stamp" | "strike" | "count" | "connect";

export interface StageMove {
  do: StageVerb;
  /** seconds into the scene: land it on the spoken word */
  at: number;
  target?: string;
  from?: string;
  to?: string;
  /** arrive: left/right = comes from that side, up = rises, down = drops, pop = scales in */
  dir?: "left" | "right" | "up" | "down" | "pop";
  /** stamp: the word on it */
  text?: string;
  /** connect: line + pulse thickness, 1 = normal */
  weight?: number;
  /** connect: how many pulses travel it */
  repeat?: number;
}

export interface StageProps {
  set?: "light" | "dark" | "brand";
  layout?: "full" | "split";
  presenter?: { src: string; from: number };
  elements: StageElement[];
  moves: StageMove[];
  punch?: { text: string; at: number; until?: number }[];
  credit?: string;
}

const W = 1080;
const SEAM = 810; // 42.2% of 1920, measured on 8 reference reels
const FULL_H = 1300; // full layout keeps clear of the caption band below
const UI = "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";
const DISPLAY = "'Space Grotesk', sans-serif";
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const FLY = { damping: 13, stiffness: 140, mass: 0.9 }; // arrives, overshoots, settles
const POP = { damping: 12, stiffness: 220, mass: 0.6 };
const STAMP = { damping: 11, stiffness: 260, mass: 0.7 };

type Pt = [number, number];

const ramp = (t: number, a: number, b: number, ease = Easing.inOut(Easing.cubic)) =>
  interpolate(t, [a, b], [0, 1], { ...CL, easing: ease });
const sp = (frame: number, fps: number, at: number, config: typeof FLY) => {
  const f0 = Math.round(at * fps);
  return frame < f0 ? 0 : spring({ frame: frame - f0, fps, config });
};
const bez = (p: Pt[], u: number): Pt => {
  const v = 1 - u;
  const c = (i: 0 | 1) =>
    v * v * v * p[0][i] + 3 * v * v * u * p[1][i] + 3 * v * u * u * p[2][i] + u * u * u * p[3][i];
  return [c(0), c(1)];
};
const pathOf = (p: Pt[]) =>
  `M ${p[0].join(" ")} C ${p[1].join(" ")} ${p[2].join(" ")} ${p[3].join(" ")}`;

// card type scales with the card's width (first stills, 2026-09-15: a flat 44px
// left a 600px card holding a whisper and the frame reading empty)
const titlePx = (e: StageElement, aw: number) =>
  Math.round(Math.min(100, Math.max(58, e.w * aw * 0.15)) * (e.size ?? 1));
const linePx = (e: StageElement, aw: number) => Math.max(30, Math.round(titlePx(e, aw) * 0.52));
const padPx = (e: StageElement, aw: number) => Math.round(titlePx(e, aw) * 0.42);

// rough height of an element, for anchoring lines to its edges
const estH = (e: StageElement, aw: number) => {
  switch (e.kind) {
    case "card":
      return 2 * padPx(e, aw) + (e.title ? titlePx(e, aw) * 1.1 : 0) + (e.lines?.length ?? 0) * linePx(e, aw) * 1.4;
    case "image": return (e.h ?? e.w * 0.8) * aw;
    case "text": return (e.size ?? 1) * 76 * 1.1;
    default: return 160 + (e.label ? 52 : 0);
  }
};

const Marked: React.FC<{ text: string; p: number; dark: boolean }> = ({ text, p, dark }) => (
  <span style={{ position: "relative", isolation: "isolate" }}>
    {p > 0 ? (
      <span style={{
        position: "absolute", left: -6, bottom: 2, height: "56%", zIndex: -1, borderRadius: 6,
        width: `calc(${p * 100}% + 12px)`,
        background: dark ? "rgba(250,204,21,0.5)" : "#FFE27A",
      }} />
    ) : null}
    {text}
  </span>
);

export const Stage: React.FC<{ scene: StageProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const theme = useTheme();
  const t = frame / fps;
  const dur = durationInFrames / fps;

  const split = scene.layout === "split";
  const AW = W;
  const AH = split ? SEAM : FULL_H;
  const set = scene.set ?? "light";
  const S = set === "dark"
    ? { bg: "radial-gradient(120% 90% at 50% 15%, #1E2433 0%, #10131B 65%, #07080C 100%)",
        grid: "rgba(255,255,255,0.04)", ink: "#F2F4F7", wire: "#3A4252", pulse: "#7DD3FC", dark: true }
    : set === "brand"
      ? { bg: `radial-gradient(80% 55% at 50% 28%, ${theme.accent}40 0%, transparent 72%), linear-gradient(180deg, #14161D 0%, #07080B 100%)`,
          grid: "rgba(255,255,255,0.05)", ink: "#FFFFFF", wire: "rgba(255,255,255,0.28)",
          pulse: theme.accentOnDark, dark: true }
      : { bg: "radial-gradient(120% 90% at 50% 18%, #F7F8FA 0%, #E6E8EC 68%, #D9DCE2 100%)",
          grid: "rgba(0,0,0,0.03)", ink: "#16181D", wire: "#AEB6C2", pulse: "#38BDF8", dark: false };

  const els = scene.elements ?? [];
  const moves = scene.moves ?? [];
  const byId = new Map(els.map((e) => [e.id, e]));
  const centre = (e: StageElement): Pt => [e.x * AW, e.y * AH];

  // camera: never still, and it leans toward whatever is in focus
  const focus = moves.filter((m) => m.do === "focus" && t >= m.at).pop();
  const fk = focus ? ramp(t, focus.at, focus.at + 0.55, Easing.out(Easing.cubic)) : 0;
  const fe = focus ? byId.get(focus.target ?? "") : undefined;
  const camS = 1.02 + 0.03 * (t / Math.max(1, dur)) + 0.06 * fk;
  const camX = fe ? (0.5 - fe.x) * AW * 0.12 * fk : Math.sin(t * 0.35) * 8;
  const camY = fe ? (0.5 - fe.y) * AH * 0.12 * fk : 0;

  const anchors = (a: StageElement, b: StageElement): Pt[] => {
    const [ax, ay] = centre(a);
    const [bx, by] = centre(b);
    const dx = bx - ax;
    const dy = by - ay;
    if (Math.abs(dx) >= Math.abs(dy)) {
      const sx = Math.sign(dx) || 1;
      const p0: Pt = [ax + (sx * a.w * AW) / 2, ay];
      const p3: Pt = [bx - (sx * b.w * AW) / 2, by];
      const k = (p3[0] - p0[0]) * 0.45;
      return [p0, [p0[0] + k, p0[1]], [p3[0] - k, p3[1]], p3];
    }
    const sy = Math.sign(dy) || 1;
    const p0: Pt = [ax, ay + (sy * estH(a, AW)) / 2];
    const p3: Pt = [bx, by - (sy * estH(b, AW)) / 2];
    const k = (p3[1] - p0[1]) * 0.45;
    return [p0, [p0[0], p0[1] + k], [p3[0], p3[1] - k], p3];
  };

  const wires = moves
    .filter((m) => m.do === "connect" && byId.has(m.from ?? "") && byId.has(m.to ?? ""))
    .map((m, i) => {
      const draw = ramp(t, m.at, m.at + 0.35);
      if (draw <= 0) return null;
      const p = anchors(byId.get(m.from!)!, byId.get(m.to!)!);
      const d = pathOf(p);
      const wgt = m.weight ?? 1;
      const n = Math.max(1, m.repeat ?? 1);
      return (
        <g key={i}>
          <path d={d} pathLength={1} fill="none" stroke={S.wire} strokeWidth={4 * wgt}
            strokeLinecap="round" strokeDasharray="1 1" strokeDashoffset={1 - draw} />
          {Array.from({ length: n }, (_, k) => {
            const u = ramp(t, m.at + 0.15 + k * 0.42, m.at + 0.7 + k * 0.42, Easing.inOut(Easing.quad));
            if (u <= 0 || u >= 1) return null;
            const head = bez(p, u);
            return (
              <g key={k} style={{ filter: `drop-shadow(0 0 ${6 + 6 * wgt}px ${S.pulse})` }}>
                <path d={d} pathLength={1} fill="none" stroke={S.pulse} strokeWidth={7 * wgt}
                  strokeLinecap="round" strokeDasharray="0.14 2" strokeDashoffset={-(u - 0.14)} />
                <circle cx={head[0]} cy={head[1]} r={6 + 6 * Math.sqrt(wgt)} fill="white" />
              </g>
            );
          })}
        </g>
      );
    });

  const renderEl = (e: StageElement) => {
    const mine = moves.filter((m) => m.target === e.id);
    const arrive = mine.find((m) => m.do === "arrive");
    const enter = arrive ? sp(frame, fps, arrive.at, arrive.dir === "pop" || !arrive.dir ? POP : FLY) : 1;
    if (enter <= 0.001) return null;
    const exitM = mine.find((m) => m.do === "exit");
    const ex = exitM ? ramp(t, exitM.at, exitM.at + 0.35) : 0;
    if (ex >= 1) return null;
    const dimM = mine.find((m) => m.do === "dim");
    const dm = dimM ? ramp(t, dimM.at, dimM.at + 0.3) : 0;
    const hlM = mine.find((m) => m.do === "highlight");
    const hl = hlM ? ramp(t, hlM.at, hlM.at + 0.45, Easing.out(Easing.quad)) : 0;
    const stM = mine.find((m) => m.do === "stamp");
    const st = stM ? sp(frame, fps, stM.at, STAMP) : 0;
    const skM = mine.find((m) => m.do === "strike");
    const sk = skM ? sp(frame, fps, skM.at, POP) : 0;
    const me = focus?.target === e.id ? fk : 0;

    const dir = arrive?.dir ?? "pop";
    const off = 1 - enter;
    const tx = dir === "left" ? -off * 640 : dir === "right" ? off * 640 : 0;
    const ty = dir === "up" ? off * 420 : dir === "down" ? -off * 420 : 0;
    const scale = (dir === "pop" ? 0.4 + 0.6 * enter : 0.9 + 0.1 * enter) * (1 + 0.1 * me) * (1 - 0.1 * ex);
    const bob = Math.sin(t * 1.4 + e.x * 7) * 4;
    const [cx, cy] = centre(e);
    const w = e.w * AW;
    const h = estH(e, AW);
    const tone = e.tone ?? (S.dark ? "dark" : "light");
    const darkCard = tone === "dark" || (tone === "accent" && S.dark);

    let body: React.ReactNode = null;
    if (e.kind === "card") {
      body = (
        <div style={{
          background: darkCard ? "#15171C" : "rgba(255,255,255,0.95)", borderRadius: 30,
          padding: `${padPx(e, AW)}px ${Math.round(padPx(e, AW) * 1.35)}px`,
          border: tone === "accent" ? `3px solid ${theme.accent}`
            : darkCard ? "1px solid rgba(255,255,255,0.08)" : "1px solid white",
          boxShadow: tone === "accent"
            ? `0 0 ${26 + 34 * me}px ${theme.accent}77, 0 36px 70px rgba(10,12,20,0.30)`
            : "0 36px 70px rgba(10,12,20,0.22), 0 8px 18px rgba(10,12,20,0.12)",
        }}>
          {e.title ? (
            <div style={{ font: `700 ${titlePx(e, AW)}px/1.1 ${DISPLAY}`, color: darkCard ? "#F2F4F7" : "#16181D" }}>
              <Marked text={e.title} p={hl} dark={darkCard} />
            </div>
          ) : null}
          {(e.lines ?? []).map((l, i) => (
            <div key={i} style={{ font: `500 ${linePx(e, AW)}px/1.35 ${UI}`, color: darkCard ? "#A3ABB9" : "#5B6270",
              marginTop: i === 0 && e.title ? 10 : 4 }}>{l}</div>
          ))}
        </div>
      );
    } else if (e.kind === "image" && e.src) {
      body = (
        <Img src={staticFile(e.src)} style={{ width: "100%", height: (e.h ?? e.w * 0.8) * AW,
          objectFit: "contain", filter: "drop-shadow(0 30px 36px rgba(0,0,0,0.35))" }} />
      );
    } else if (e.kind === "text") {
      body = (
        <div style={{ textAlign: "center", font: `800 ${Math.round(76 * (e.size ?? 1))}px/1.05 ${DISPLAY}`,
          color: S.ink, textShadow: S.dark ? "0 8px 30px rgba(0,0,0,0.5)" : "none" }}>
          <Marked text={e.text ?? ""} p={hl} dark={S.dark} />
        </div>
      );
    } else if (e.kind === "number") {
      const cnt = mine.find((m) => m.do === "count");
      const p = cnt ? ramp(t, cnt.at, cnt.at + 1.1, Easing.out(Easing.cubic)) : 1;
      const v0 = e.from ?? 0;
      const val = v0 + ((e.value ?? 0) - v0) * p;
      const land = cnt ? Math.max(0, Math.sin(Math.PI * Math.min(1, Math.max(0, (t - cnt.at - 1.1) / 0.27)))) : 0;
      const fmt = val.toLocaleString("en-US", {
        minimumFractionDigits: e.decimals ?? 0, maximumFractionDigits: e.decimals ?? 0 });
      body = (
        <div style={{ textAlign: "center" }}>
          <div style={{ font: `800 150px/1 ${DISPLAY}`, fontVariantNumeric: "tabular-nums",
            color: S.dark ? theme.accentOnDark : theme.accentInk, transform: `scale(${1 + 0.08 * land})` }}>
            {`${e.prefix ?? ""}${fmt}${e.suffix ?? ""}`}
          </div>
          {e.label ? <div style={{ font: `600 38px ${UI}`, color: S.ink, marginTop: 10 }}>{e.label}</div> : null}
        </div>
      );
    }

    return (
      <div key={e.id} style={{
        position: "absolute", left: cx - w / 2, top: cy, width: w, zIndex: me > 0 ? 3 : 2,
        transform: `translate(${tx}px, calc(-50% + ${ty + bob}px)) scale(${scale})`,
        opacity: Math.min(1, enter * 1.6) * (1 - 0.62 * dm) * (1 - ex),
        filter: dm > 0 ? `saturate(${1 - 0.7 * dm})` : undefined,
      }}>
        {body}
        {st > 0 ? (
          <div style={{
            position: "absolute", right: -18, top: -38, zIndex: 4, whiteSpace: "nowrap",
            transform: `rotate(-6deg) scale(${1.7 - 0.7 * st})`, opacity: Math.min(1, st * 2),
            background: "#E8F8EE", border: "3px solid #34C46E", color: "#15803D",
            font: `800 30px ${UI}`, letterSpacing: 2, padding: "10px 18px", borderRadius: 14,
            boxShadow: "0 12px 30px rgba(21,128,61,0.25)",
          }}>{stM?.text ?? "✓"}</div>
        ) : null}
        {sk > 0 ? (
          <svg viewBox="0 0 100 100" style={{
            position: "absolute", left: "50%", top: "50%", zIndex: 4, overflow: "visible",
            width: Math.min(w, h) * 1.05, height: Math.min(w, h) * 1.05,
            transform: `translate(-50%, -50%) scale(${1.6 - 0.6 * sk})`, opacity: Math.min(1, sk * 2),
            filter: "drop-shadow(0 10px 20px rgba(229,50,45,0.35))",
          }}>
            <circle cx="50" cy="50" r="42" fill="none" stroke="#E5322D" strokeWidth="10" />
            <line x1="21" y1="79" x2="79" y2="21" stroke="#E5322D" strokeWidth="10" strokeLinecap="round" />
          </svg>
        ) : null}
      </div>
    );
  };

  const credit = scene.credit ?? els.find((e) => e.kind === "number" && e.source)?.source;

  return (
    <AbsoluteFill style={{ background: split ? "#0B0B0D" : undefined }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: split ? SEAM : "100%",
        overflow: "hidden", background: S.bg }}>
        <AbsoluteFill style={{
          backgroundImage: `linear-gradient(${S.grid} 1px, transparent 1px), linear-gradient(90deg, ${S.grid} 1px, transparent 1px)`,
          backgroundSize: "96px 96px",
        }} />
        <div style={{ position: "absolute", left: 0, top: 0, width: AW, height: AH,
          transform: `translate(${camX}px, ${camY}px) scale(${camS})` }}>
          <svg width={AW} height={AH} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", zIndex: 1 }}>
            {wires}
          </svg>
          {els.map(renderEl)}
        </div>
      </div>
      {split && scene.presenter ? (
        <div style={{ position: "absolute", left: 0, top: SEAM, width: W, height: 1920 - SEAM, overflow: "hidden" }}>
          <OffthreadVideo src={staticFile(scene.presenter.src)} muted
            startFrom={Math.round(scene.presenter.from * fps)}
            style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 30%" }} />
        </div>
      ) : null}
      {split
        ? (scene.punch ?? []).map((pw, i) => {
            if (t < pw.at || (pw.until !== undefined && t > pw.until)) return null;
            const k = sp(frame, fps, pw.at, POP);
            return (
              <div key={i} style={{
                position: "absolute", left: 0, right: 0, top: 1540, textAlign: "center", color: "white",
                font: "800 118px 'Archivo', sans-serif", letterSpacing: 1, lineHeight: 1,
                textShadow: "0 3px 0 #D7D7D7, 0 6px 0 #B9B9B9, 0 9px 0 #9C9C9C, 0 18px 34px rgba(0,0,0,0.55)",
                opacity: Math.min(1, k * 2), transform: `scale(${1.35 - 0.35 * Math.min(1.08, k)})`,
              }}>{pw.text}</div>
            );
          })
        : null}
      {credit ? <Credit text={credit} onMedia={S.dark || split} /> : null}
    </AbsoluteFill>
  );
};
