import React from "react";
import { Easing, Img, OffthreadVideo, interpolate, spring, staticFile } from "remotion";

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

// NO FADE-INS (2026-10-02, adopted from the motion-reel plugin's studio rules:
// "everything fading in" is the signature of template video). A 0.3s opacity
// ramp from zero left every cut on an empty dark frame for 1-2 frames
// (measured on ios27-settings-longform v2: luma ~3 at each cut). Now an
// element ARRIVES: a spring that travels and overshoots a touch, solid within
// ~3 frames. Anything due at the very top of a page starts 0.1s into its move,
// so the cut lands on motion, never on an empty frame.
export const arrive = (t: number, a: number, fps: number) => {
  const f = Math.round((t - (a <= 0.05 ? -0.1 : a)) * fps);
  return f < 0 ? 0 : spring({ frame: f, fps, config: { damping: 13, stiffness: 190, mass: 0.9 } });
};
/** the style of an arriving element: travel with weight, opacity only as a 3-frame snap */
export const rise = (p: number, d = 24) => ({ opacity: Math.min(1, p * 4), transform: `translateY(${Math.round((1 - p) * d * 1.8)}px)` });

// --------------------------------------------------------------- bezels ----
// REAL DEVICE FRAMES (2026-09-30). The drawn black bezel read as "a rounded
// panel", not an iPhone (ios27-settings-longform review). Apple's own bezels
// (developer.apple.com/design/resources) are licensed for marketing use but not
// for redistribution, so the PNG lives in the git-ignored public/assets/_bezels
// and each machine fetches it. screen = [x, y, w, h] of the opening in bezel px;
// the iPhone 17 Pro opening is exactly the simulator's 1206x2622.
export const BEZELS: Record<string, { src: string; w: number; h: number; screen: [number, number, number, number] }> = {
  "iphone-17-pro": { src: "assets/_bezels/iphone-17-pro.png", w: 1350, h: 2760, screen: [72, 69, 1206, 2622] },
};

const RealPhone: React.FC<{ spec: (typeof BEZELS)[string]; boxH: number; shown: number; children: React.ReactNode }>
  = ({ spec, boxH, shown, children }) => {
  const k = boxH / spec.h;
  const [sx, sy, sw, sh] = spec.screen.map((v) => v * k);
  return (
    <div style={{ position: "relative", width: Math.round(spec.w * k), height: boxH, alignSelf: "center", flexShrink: 0,
      ...rise(shown),
      filter: "drop-shadow(0 30px 45px rgba(0,0,0,0.55))" }}>
      <div style={{ position: "absolute", left: sx, top: sy, width: sw, height: sh, overflow: "hidden",
        borderRadius: sw * 0.14, background: "#000" }}>{children}</div>
      <Img src={staticFile(spec.src)} style={{ position: "absolute", left: 0, top: 0, width: spec.w * k, height: boxH }} />
    </div>
  );
};

// ---------------------------------------------------------------- screen ----
export interface ScreenBlockProps {
  /** draw the phone body around it — true for the drawn frame, or a BEZELS key
   *  ("iphone-17-pro") for Apple's real one. Never for a captured web page. */
  device?: boolean | string;
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
  const real = typeof b.device === "string" ? BEZELS[b.device] : undefined;
  const device = Boolean(b.device) && !real;
  const bezel = device ? Math.max(10, Math.round(boxH * 0.022)) : 0;
  const fitW = Math.round(((boxH - bezel * 2) * b.width) / b.height);
  const boxW = real ? Math.round((real.w * boxH) / real.h)
    : device ? Math.min(fullW, fitW + bezel * 2)
    : hug ? Math.round(Math.min(fullW, (boxH * b.width) / b.height)) : fullW;
  const mine = moves.filter((m) => m.target === b.id && m.at !== undefined).sort((a, z) => (a.at! - z.at!));
  // camera: every focus is a rect in source px; before the first, the whole image
  const whole: [number, number, number, number] = [0, 0, b.width, b.height];
  const focuses = mine.filter((m) => m.do === "focus" && m.rect);
  // A focus keeps CONTEXT around its target and never zooms past 2.4x the
  // whole-image fit: fitting a 60px crown to the box made it a blur and pushed
  // the ring outside the view as stray lines (first PairPods v2 stills).
  const innerW = real ? (real.screen[2] * boxH) / real.h : boxW - bezel * 2;
  const innerH = real ? (real.screen[3] * boxH) / real.h : boxH - bezel * 2;
  const fit = Math.min(innerW / b.width, innerH / b.height);
  const camFor = (r: [number, number, number, number]) => {
    const whole = r[2] >= b.width && r[3] >= b.height;
    // never SMALLER than resting: a wide rect used to zoom the image out below
    // its own fit, which inside a device frame left black bars in the bezel.
    const s = whole ? fit : Math.max(fit, Math.min(innerW / (r[2] * 1.5), innerH / (r[3] * 1.5), fit * 2.4));
    const cx = r[0] + r[2] / 2, cy = r[1] + r[3] / 2;
    // keep the image edge from drifting inside the box when zoomed in
    const x = Math.min(0, Math.max(innerW - b.width * s, innerW / 2 - cx * s));
    const y = Math.min(0, Math.max(innerH - b.height * s, innerH / 2 - cy * s));
    return { s, x: b.width * s < innerW ? (innerW - b.width * s) / 2 : x, y: b.height * s < innerH ? (innerH - b.height * s) / 2 : y };
  };
  let cam = camFor(whole);
  let prevRect = whole;
  let ringRect: [number, number, number, number] | null = null;
  let ringAt = 0;
  // loupe rect: glides from the previous focus to the current one
  let loupe: [number, number, number, number] | null = null;
  for (const f of focuses) {
    if (t < f.at!) break;
    const from = camFor(prevRect), to = camFor(f.rect!);
    const k = interpolate(t, [f.at!, f.at! + 0.7], [0, 1], { ...CL, easing: ease });
    cam = { s: from.s + (to.s - from.s) * k, x: from.x + (to.x - from.x) * k, y: from.y + (to.y - from.y) * k };
    const lf = loupe ?? f.rect!;
    loupe = [0, 1, 2, 3].map((i) => lf[i] + (f.rect![i] - lf[i]) * k) as [number, number, number, number];
    prevRect = f.rect!;
    ringRect = f.ring === false ? null : f.rect!;
    ringAt = f.at! + 0.6;
  }
  // states: the base image, then each published state crossfades in on its word
  const states = mine.filter((m) => m.do === "state" && m.src);
  const layers = [{ src: b.src, o: 1 }, ...states.map((s) => ({ src: s.src!, o: ramp(t, s.at!, 0.35) }))];
  const draw = ringRect ? ramp(t, ringAt, 0.45) : 0;
  const camera = (
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
  );
  const phone = real ? <RealPhone spec={real} boxH={boxH} shown={shown}>{camera}</RealPhone> : (
    <div style={{ position: "relative", width: boxW, height: boxH,
      borderRadius: device ? Math.round(boxH * 0.062) : 30, overflow: "hidden",
      alignSelf: hug || device ? "center" : undefined, padding: bezel, boxSizing: "border-box",
      background: device ? "#0A0A0C" : C.card,
      border: device ? "2px solid rgba(255,255,255,0.14)" : `2px solid ${C.line}`,
      boxShadow: device ? "0 30px 70px rgba(0,0,0,0.55)" : undefined,
      ...rise(shown), flexShrink: 0 }}>
      <div style={{ position: "absolute", left: bezel, top: bezel, width: innerW, height: innerH,
        borderRadius: device ? Math.max(0, Math.round(boxH * 0.062) - bezel) : 0, overflow: "hidden", background: "#000" }}>
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
    </div>
  );
  // THE LOUPE (2026-09-30, ios27-settings-longform). A portrait phone in a 16:9
  // frame renders Settings text at ~16px with two dead panels beside it, and a
  // focus cannot zoom a full-width row past fit. So in a wide frame the focused
  // rect is also shown magnified in the space beside the phone: the words the
  // voice names become readable, and the phone keeps the context.
  const useLoupe = hug && focuses.length > 0;
  if (!useLoupe) return phone;
  const room = fullW - boxW - 80;
  const lr = loupe ?? focuses[0].rect!;
  const pad = 24;
  const rw = lr[2] + pad * 2, rh = lr[3] + pad * 2;
  const LW = Math.min(room, 900), LHmax = boxH * 0.72;
  const ls = Math.min(LW / rw, LHmax / rh);
  const lo = loupe ? ramp(t, focuses[0].at!, 0.45) : 0;
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 80, width: fullW, flexShrink: 0 }}>
      {phone}
      <div style={{ width: rw * ls, height: rh * ls, borderRadius: 28, overflow: "hidden", position: "relative",
        background: "#fff", boxShadow: "0 24px 60px rgba(0,0,0,0.5)", border: `3px solid ${C.pill}`,
        opacity: lo * shown, transform: `scale(${0.96 + 0.04 * lo})`, flexShrink: 0 }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: b.width, height: b.height, transformOrigin: "0 0",
          transform: `translate(${-(lr[0] - pad) * ls}px, ${-(lr[1] - pad) * ls}px) scale(${ls})` }}>
          {layers.map((l, i) => (
            <Img key={i} src={staticFile(l.src)} style={{ position: "absolute", left: 0, top: 0, width: b.width, height: b.height, opacity: l.o }} />
          ))}
        </div>
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

// ---------------------------------------------------------------- levels ----
// VOLUME / LEVEL METERS (2026-09-30, ios27-settings-longform: the alarm that
// follows the ringer). Labelled horizontal bars; each bar animates from its
// `from` to its `to` on a `drain` move naming "<id>.<i>" (or the whole block).
export interface LevelsBlockProps {
  id: string; kind: "levels";
  items: { label: string; from: number; to?: number; tone?: "cost" | "free" }[];
  h?: number; secs?: number;
}

export const LevelsBlock: React.FC<{ b: LevelsBlockProps; moves: MoveLike[]; t: number; boxW: number; C: Pal; shown: number }>
  = ({ b, moves, t, boxW, C, shown }) => {
  const H = b.h ?? 360;
  const rowH = Math.min(150, (H - 20 * (b.items.length - 1)) / b.items.length);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20, width: boxW, ...rise(shown) }}>
      {b.items.map((it, i) => {
        const at = moves.find((m) => m.do === "drain" && (m.target === `${b.id}.${i}` || m.target === b.id))?.at;
        const v = at === undefined ? it.from
          : interpolate(t, [at, at + (b.secs ?? 1.4)], [it.from, it.to ?? it.from], { ...CL, easing: ease });
        const col = it.tone === "cost" ? C.red : C.blue;
        return (
          <div key={i} style={{ height: rowH, background: C.card, borderRadius: 26, border: `2px solid ${C.line}`,
            display: "flex", alignItems: "center", gap: 28, padding: "0 32px" }}>
            <div style={{ width: 200, font: `600 38px ${FONT}`, color: C.ink }}>{it.label}</div>
            <div style={{ flex: 1, height: 18, borderRadius: 9, background: "rgba(255,255,255,0.12)", position: "relative" }}>
              <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: `${v}%`, borderRadius: 9, background: col }} />
              <div style={{ position: "absolute", top: -13, left: `calc(${v}% - 22px)`, width: 44, height: 44, borderRadius: 22,
                background: "#fff", boxShadow: "0 2px 10px rgba(0,0,0,0.45)" }} />
            </div>
            <div style={{ width: 110, textAlign: "right", font: `700 38px ${FONT}`, color: col, fontVariantNumeric: "tabular-nums" }}>
              {Math.round(v)}%
            </div>
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
      overflow: "hidden", ...rise(shown) }}>
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
    <div style={{ position: "relative", width: boxW, height: H, ...rise(shown) }}>
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

/** CLIP — a screen RECORDING inside a page (ios27-battery-longform, 2026-09-25).
 *  `screen` takes a still and moves a camera over it; the longform format's core
 *  asset is a real recording of a phone doing the thing, which an <Img> cannot
 *  decode (G35 blocks that on purpose). Same hug rule as ScreenBlock: a portrait
 *  recording in a landscape page takes the width it uses and centres, instead of
 *  sitting in a bordered card between two dead panels. */
export interface ClipBlockProps {
  id: string; kind: "clip"; src: string; width: number; height: number;
  h?: number; from?: number;
  /** draw the phone body around it (default true for a portrait source), or a
   *  BEZELS key for Apple's real frame */
  device?: boolean | string;
}

export const ClipBlock: React.FC<{ b: ClipBlockProps; t: number; boxW: number; C: Pal; shown: number; fps: number; wide?: boolean }>
  = ({ b, boxW: fullW, C, shown, fps, wide }) => {
  const boxH = b.h ?? 720;
  const portrait = b.height / b.width > 1.2;
  const hug = Boolean(wide) && portrait;
  // THE PHONE BODY (2026-09-25). A simulator recording is a screen with nothing
  // around it, so on a page it read as a rounded panel rather than a phone. The
  // references float the recording in a device; the bezel is drawn here rather
  // than baked into the capture, so one recording serves any layout.
  const real = typeof b.device === "string" ? BEZELS[b.device] : undefined;
  if (real) {
    return (
      <RealPhone spec={real} boxH={boxH} shown={shown}>
        <OffthreadVideo src={staticFile(b.src)} muted startFrom={Math.round((b.from ?? 0) * fps)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </RealPhone>
    );
  }
  const device = b.device ?? portrait;
  const bezel = device ? Math.max(10, Math.round(boxH * 0.022)) : 0;
  const screenH = boxH - bezel * 2;
  const screenW = Math.round((screenH * b.width) / b.height);
  const boxW = hug || device ? Math.min(fullW, screenW + bezel * 2) : fullW;
  const radius = device ? Math.round(boxH * 0.062) : 30;
  return (
    <div style={{ position: "relative", width: boxW, height: boxH, borderRadius: radius,
      alignSelf: hug || device ? "center" : undefined, flexShrink: 0,
      background: device ? "#0A0A0C" : C.card,
      padding: bezel, boxSizing: "border-box",
      border: device ? "2px solid rgba(255,255,255,0.14)" : `2px solid ${C.line}`,
      boxShadow: device ? "0 30px 70px rgba(0,0,0,0.55)" : undefined,
      ...rise(shown) }}>
      <div style={{ width: "100%", height: "100%", borderRadius: Math.max(0, radius - bezel),
        overflow: "hidden", background: "#000" }}>
        <OffthreadVideo src={staticFile(b.src)} muted startFrom={Math.round((b.from ?? 0) * fps)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </div>
  );
};
