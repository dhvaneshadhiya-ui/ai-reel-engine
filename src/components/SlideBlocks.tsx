import React from "react";
import { Easing, Img, interpolate, staticFile } from "remotion";

/**
 * MOTION BLOCKS FOR SLIDES (2026-09-17).
 *
 * User review of the first PairPods cut: "Followed almost same design and
 * layout. Hardly any animation." Slides only knew cards fading in. These blocks
 * add motion that CARRIES information, never motion on type (continuous scale
 * on text reads as shaking — 2026-09-16):
 *
 *   screen   a real screenshot as a camera subject: zoom/pan to the region being
 *            spoken about (`focus` moves), crossfade between real app STATES the
 *            vendor published (`state` moves), a hand-drawn ring on the focus.
 *            Scaling a bitmap is smooth; only live glyphs shimmer.
 *   steps    a numbered how-to strip; each step lands on its word, the newest is lit.
 *   devices  a Mac with lines to each device; a pulse travels a line once that
 *            device is shown, and keeps travelling (the audio is flowing).
 *   waves    two waveforms that start in step and drift apart on `drift` —
 *            the sync / pitch caveat as a picture.
 *
 * All timing arrives as moves (`on` words resolved by compile_shot_plan).
 */

export interface MoveLike {
  do: string;
  target: string;
  at?: number;
  rect?: [number, number, number, number];
  src?: string;
  ring?: boolean;
}

type Pal = { card: string; line: string; ink: string; sub: string; muted: string; blue: string; red: string; amber: string; pill: string };

const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ease = Easing.inOut(Easing.cubic);
const ramp = (t: number, a: number, d = 0.3) => interpolate(t, [a, a + d], [0, 1], { ...CL, easing: Easing.out(Easing.cubic) });
const FONT = "Inter, -apple-system, 'SF Pro Display', sans-serif";

// ---------------------------------------------------------------- screen ----
export interface ScreenBlockProps {
  id: string;
  kind: "screen";
  /** source image size in px (every state shares it) */
  width: number;
  height: number;
  src: string;
  /** box height in px on the slide (width is the column) */
  h?: number;
}

export const ScreenBlock: React.FC<{ b: ScreenBlockProps; moves: MoveLike[]; t: number; boxW: number; C: Pal; shown: number; wide?: boolean }> = ({ b, moves, t, boxW: fullW, C, shown, wide }) => {
  const boxH = b.h ?? 720;
  // A PHONE SHOT IN A LANDSCAPE PAGE HUGS ITS SOURCE (2026-09-25). Stretched to
  // a 16:9 column, a 1170x1992 screenshot sat in the middle of a bordered card
  // with two dead panels beside it. The references put the phone recording in a
  // phone-shaped panel on the page background, so the card takes the width the
  // source actually uses and centres itself.
  // The test is the FRAME, not the box: a portrait page's column is already
  // 916x760, which is "wider than tall" and briefly made every reel's screen
  // card shrink (caught in a still, 2026-09-25).
  const hug = Boolean(wide) && b.height / b.width > 1.2;
  const boxW = hug ? Math.round(Math.min(fullW, (boxH * b.width) / b.height)) : fullW;
  const mine = moves.filter((m) => m.target === b.id && m.at !== undefined).sort((a, z) => (a.at! - z.at!));
  // camera: every focus is a rect in source px; before the first, the whole image
  const whole: [number, number, number, number] = [0, 0, b.width, b.height];
  const focuses = mine.filter((m) => m.do === "focus" && m.rect);
  // A focus keeps CONTEXT around its target and never zooms past 2.4x the
  // whole-image fit: fitting a 60px crown to the box made it a blur and pushed
  // the ring outside the view as stray lines (first PairPods v2 stills).
  const fit = Math.min(boxW / b.width, boxH / b.height);
  const camFor = (r: [number, number, number, number]) => {
    const whole = r[2] >= b.width && r[3] >= b.height;
    const s = whole ? fit : Math.min(boxW / (r[2] * 1.5), boxH / (r[3] * 1.5), fit * 2.4);
    const cx = r[0] + r[2] / 2, cy = r[1] + r[3] / 2;
    // keep the image edge from drifting inside the box when zoomed in
    const x = Math.min(0, Math.max(boxW - b.width * s, boxW / 2 - cx * s));
    const y = Math.min(0, Math.max(boxH - b.height * s, boxH / 2 - cy * s));
    return { s, x: b.width * s < boxW ? (boxW - b.width * s) / 2 : x, y: b.height * s < boxH ? (boxH - b.height * s) / 2 : y };
  };
  let cam = camFor(whole);
  let prevRect = whole;
  let ringRect: [number, number, number, number] | null = null;
  let ringAt = 0;
  for (const f of focuses) {
    if (t < f.at!) break;
    const from = camFor(prevRect), to = camFor(f.rect!);
    const k = interpolate(t, [f.at!, f.at! + 0.7], [0, 1], { ...CL, easing: ease });
    cam = { s: from.s + (to.s - from.s) * k, x: from.x + (to.x - from.x) * k, y: from.y + (to.y - from.y) * k };
    prevRect = f.rect!;
    ringRect = f.ring === false ? null : f.rect!;
    ringAt = f.at! + 0.6;
  }
  // states: the base image, then each published state crossfades in on its word
  const states = mine.filter((m) => m.do === "state" && m.src);
  const layers = [{ src: b.src, o: 1 }, ...states.map((s) => ({ src: s.src!, o: ramp(t, s.at!, 0.35) }))];
  const draw = ringRect ? ramp(t, ringAt, 0.45) : 0;
  return (
    <div style={{ position: "relative", width: boxW, height: boxH, borderRadius: 30, overflow: "hidden",
      alignSelf: hug ? "center" : undefined,
      background: C.card, border: `2px solid ${C.line}`, opacity: shown, transform: `translateY(${Math.round((1 - shown) * 24)}px)`, flexShrink: 0 }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: b.width, height: b.height, transformOrigin: "0 0",
        transform: `translate(${cam.x}px, ${cam.y}px) scale(${cam.s})` }}>
        {layers.map((l, i) => (
          <Img key={i} src={staticFile(l.src)} style={{ position: "absolute", left: 0, top: 0, width: b.width, height: b.height, opacity: l.o }} />
        ))}
        {ringRect && draw > 0 ? (
          <svg width={b.width} height={b.height} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
            <rect x={ringRect[0] - 10} y={ringRect[1] - 8} width={ringRect[2] + 20} height={ringRect[3] + 16} rx={18}
              fill="none" stroke={C.pill} strokeWidth={6 / cam.s} pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - draw}
              strokeLinecap="round" />
          </svg>
        ) : null}
      </div>
    </div>
  );
};

// ----------------------------------------------------------------- steps ----
export interface StepsBlockProps { id: string; kind: "steps"; steps: string[]; h?: number }

export const StepsBlock: React.FC<{ b: StepsBlockProps; moves: MoveLike[]; t: number; C: Pal }> = ({ b, moves, t, C }) => {
  const at = (i: number) => moves.find((m) => m.do === "show" && m.target === `${b.id}.${i}`)?.at ?? 0;
  const lastShown = b.steps.reduce((acc, _s, i) => (t >= at(i) ? i : acc), -1);
  // `h` given: the strip is the page, so the cards grow to fill it (the
  // ios27 "three jobs" page left 72% of the frame flat without this).
  const tall = (b.h ?? 0) > 360;
  return (
    <div style={{ display: "flex", gap: 12, height: b.h, alignItems: "stretch" }}>
      {b.steps.map((s, i) => {
        const p = ramp(t, at(i), 0.3);
        const live = i === lastShown;
        return (
          <div key={i} style={{ flex: 1, background: live ? "rgba(18,40,68,1)" : C.card, borderRadius: 22,
            padding: tall ? "34px 26px" : "20px 16px", display: "flex", flexDirection: "column",
            justifyContent: tall ? "center" : "flex-start", gap: tall ? 10 : 0,
            border: `2px solid ${live ? C.blue : C.line}`, opacity: 0.25 + 0.75 * p, minHeight: tall ? undefined : 150 }}>
            <div style={{ width: 52, height: 52, borderRadius: 26, background: p > 0.5 ? C.blue : "transparent",
              border: `3px solid ${C.blue}`, display: "flex", alignItems: "center", justifyContent: "center",
              font: `800 28px ${FONT}`, color: p > 0.5 ? "#fff" : C.blue }}>{i + 1}</div>
            <div style={{ marginTop: tall ? 26 : 14, font: `700 ${tall ? 40 : 30}px/1.22 ${FONT}`, color: C.ink }}>{s}</div>
          </div>
        );
      })}
    </div>
  );
};

// --------------------------------------------------------------- devices ----
export interface DevicesBlockProps { id: string; kind: "devices"; hub: string; items: string[]; h?: number }

export const DevicesBlock: React.FC<{ b: DevicesBlockProps; moves: MoveLike[]; t: number; boxW: number; C: Pal }> = ({ b, moves, t, boxW, C }) => {
  const H = b.h ?? 620;
  const n = b.items.length;
  // the diagram grows with its box, so a tall hook card is filled, not dotted
  const f = Math.max(1, Math.min(1.5, H / 560));
  const hubX = Math.round(190 * f), hubY = H / 2;
  const chipW = Math.round(400 * Math.min(f, 1.15)), chipH = Math.round(96 * f), chipX = boxW - chipW;
  // devices spread to the block's edges (a hook card must reach ~70%, 2026-09-17)
  const gap = (H - n * chipH) / Math.max(1, n - 1 + 0.5);
  // a device with no `show` is connected from frame 0 (not fading in at 0.3s)
  const at = (i: number) => moves.find((m) => m.do === "show" && m.target === `${b.id}.${i}`)?.at ?? -1;
  return (
    <div style={{ position: "relative", width: boxW, height: H }}>
      <svg width={boxW} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
        {b.items.map((_it, i) => {
          const y = gap / 4 + i * (chipH + gap) + chipH / 2;
          const p = ramp(t, at(i), 0.45);
          if (p <= 0) return null;
          const x0 = hubX + 130 * f + 12, dx = (chipX - x0) * 0.5;
          const d = `M ${x0} ${hubY} C ${x0 + dx} ${hubY}, ${chipX - dx} ${y}, ${chipX} ${y}`;
          // one pulse per 1.2s after the line lands: the audio is flowing
          const phase = t > at(i) + 0.45 ? ((t - at(i) - 0.45) / 1.2) % 1 : -1;
          return (
            <g key={i}>
              <path d={d} fill="none" stroke={C.blue} strokeOpacity={0.45} strokeWidth={5} pathLength={1}
                strokeDasharray="1 1" strokeDashoffset={1 - p} strokeLinecap="round" />
              {phase >= 0 ? (
                <path d={d} fill="none" stroke={C.pill} strokeWidth={9} pathLength={1} strokeLinecap="round"
                  strokeDasharray="0.08 1" strokeDashoffset={-phase} />
              ) : null}
            </g>
          );
        })}
      </svg>
      {/* the Mac: a laptop drawn in two shapes */}
      <div style={{ position: "absolute", left: hubX - 130 * f, top: hubY - 110 * f, width: 260 * f, textAlign: "center" }}>
        <div style={{ margin: "0 auto", width: 220 * f, height: 140 * f, borderRadius: 16, border: `${Math.round(8 * f)}px solid ${C.sub}`, background: "#101014" }} />
        <div style={{ margin: "0 auto", width: 260 * f, height: 18 * f, borderRadius: "0 0 14px 14px", background: C.sub }} />
        <div style={{ marginTop: 16, font: `700 ${Math.round(34 * f)}px ${FONT}`, color: C.ink }}>{b.hub}</div>
      </div>
      {b.items.map((it, i) => {
        const y = gap / 4 + i * (chipH + gap);
        const p = ramp(t, at(i) + 0.3, 0.3);
        return (
          <div key={i} style={{ position: "absolute", left: chipX, top: y, width: chipW, height: chipH, borderRadius: 24,
            background: C.card, border: `2px solid ${p > 0 ? `rgba(77,163,255,${0.6 * p})` : C.line}`, opacity: p,
            transform: `translateX(${Math.round((1 - p) * 30)}px)`, display: "flex", alignItems: "center", padding: "0 26px",
            font: `700 ${Math.round(36 * f)}px ${FONT}`, color: C.ink }}>{it}</div>
        );
      })}
    </div>
  );
};

// ----------------------------------------------------------------- waves ----
export interface WavesBlockProps { id: string; kind: "waves"; labels: [string, string]; h?: number }

export const WavesBlock: React.FC<{ b: WavesBlockProps; moves: MoveLike[]; t: number; boxW: number; C: Pal; shown: number }> = ({ b, moves, t, boxW, C, shown }) => {
  const H = b.h ?? 380;
  const driftAt = moves.find((m) => m.do === "drift" && m.target === b.id)?.at;
  const drift = driftAt === undefined ? 0 : interpolate(t, [driftAt, driftAt + 2.4], [0, 1], { ...CL, easing: ease });
  const path = (phase: number, freq: number, yMid: number) => {
    const pts: string[] = [];
    for (let x = 0; x <= boxW; x += 8) {
      const y = yMid + Math.sin((x / boxW) * Math.PI * 2 * freq + phase) * 58;
      pts.push(`${x} ${y.toFixed(1)}`);
    }
    return "M " + pts.join(" L ");
  };
  const move = t * 2.2; // the sound is playing: both waves travel
  const yMid = H / 2 + 10;
  return (
    <div style={{ position: "relative", width: boxW, height: H, borderRadius: 30, background: C.card, border: `2px solid ${C.line}`,
      overflow: "hidden", opacity: shown }}>
      <svg width={boxW} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
        <path d={path(move, 3, yMid)} fill="none" stroke={C.blue} strokeWidth={8} strokeLinecap="round" />
        <path d={path(move + drift * 1.9, 3 + drift * 0.55, yMid)} fill="none" stroke={C.amber} strokeWidth={8}
          strokeLinecap="round" strokeOpacity={0.9} />
      </svg>
      <div style={{ position: "absolute", left: 28, top: 22, display: "flex", gap: 28, font: `700 30px ${FONT}` }}>
        <span style={{ color: C.blue }}>● {b.labels[0]}</span>
        <span style={{ color: C.amber }}>● {b.labels[1]}</span>
      </div>
    </div>
  );
};

/** GAUGE — a battery that actually drains (ios27-battery-drain, 2026-09-19).
 *  The topic IS a battery, and no existing block draws one: rows, hero and
 *  spotlight can all say "78%", none of them can show it falling. The fill and
 *  the number move together on a `drain` move (word-anchored like every other
 *  move); with no drain move it holds at `from`, which is how the healthy
 *  battery beat uses it. Motion is on the shape and the tabular digits, never a
 *  scale on type (2026-09-16 shake rule). */
export interface GaugeBlockProps {
  id: string; kind: "gauge";
  /** percent at rest, and where a `drain` move takes it */
  from: number; to?: number;
  label?: string; note?: string; h?: number;
  /** seconds the drain takes (default 2.2) */
  secs?: number;
}

export const GaugeBlock: React.FC<{ b: GaugeBlockProps; moves: MoveLike[]; t: number; boxW: number; C: Pal; shown: number }> = ({ b, moves, t, boxW, C, shown }) => {
  const H = b.h ?? 420;
  const drainAt = moves.find((m) => m.do === "drain" && m.target === b.id)?.at;
  const to = b.to ?? b.from;
  const pct = drainAt === undefined ? b.from
    : interpolate(t, [drainAt, drainAt + (b.secs ?? 2.2)], [b.from, to], { ...CL, easing: ease });
  // the cell: a rounded body plus the nub, drawn to the box, never an emoji
  const padX = 52, bodyW = boxW - padX * 2 - 26, bodyH = Math.round(H * 0.46);
  const bodyY = Math.round(H * 0.20);
  const fillW = Math.max(6, Math.round((bodyW - 20) * (pct / 100)));
  const low = pct <= 35;
  const fill = low ? C.amber : C.blue;
  // a low battery breathes; a healthy one sits still (idle motion, 2% max)
  const pulse = low ? 0.9 + Math.sin(t * 5.2) * 0.1 : 1;
  return (
    <div style={{ position: "relative", width: boxW, height: H, opacity: shown }}>
      <svg width={boxW} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
        <rect x={padX} y={bodyY} width={bodyW} height={bodyH} rx={34} fill={C.card} stroke={C.line} strokeWidth={6} />
        <rect x={padX + bodyW + 8} y={bodyY + bodyH * 0.32} width={20} height={bodyH * 0.36} rx={8} fill={C.line} />
        <rect x={padX + 10} y={bodyY + 10} width={fillW} height={bodyH - 20} rx={26} fill={fill} opacity={pulse} />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: bodyY + bodyH + 26, textAlign: "center",
        font: `800 96px/1 ${FONT}`, letterSpacing: -3, fontVariantNumeric: "tabular-nums", color: fill }}>
        {Math.round(pct)}%
      </div>
      {b.label ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: bodyY + bodyH + 140, textAlign: "center",
          font: `600 38px/1.25 ${FONT}`, color: C.sub }}>{b.label}</div>
      ) : null}
      {b.note ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: bodyY - 68, textAlign: "center",
          font: `700 30px ${FONT}`, letterSpacing: 2, color: C.muted }}>{b.note}</div>
      ) : null}
    </div>
  );
};
