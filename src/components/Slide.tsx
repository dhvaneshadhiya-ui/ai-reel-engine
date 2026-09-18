import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { DevicesBlock, ScreenBlock, StepsBlock, WavesBlock } from "./SlideBlocks";
import type { DevicesBlockProps, ScreenBlockProps, StepsBlockProps, WavesBlockProps } from "./SlideBlocks";

/**
 * SLIDE — the Carousel Playbook look, as a reel scene (2026-09-16).
 *
 * Built from the carousel's own slide videos (saas-repos-video_1), after the
 * user's review of five-free-ai-tools: "not even close to Carousel Playbook
 * style". What that look IS, measured on its frames:
 *   - pure black ground, Inter, everything left-aligned on one column
 *   - (carousel pages only) a top bar: series name left, "n / N" right. Reels
 *     leave it out — a reel is not paged (user, 2026-09-16)
 *   - a blue eyebrow ("#1 · Replaces Zapier") and a big bold white headline
 *     that arrives word by word, with at most one yellow pill word
 *   - the layout's shapes are on screen from the first frame and FILL with
 *     their content on the spoken beat, so no frame is ever empty
 *   - paid vs free as two cards and an arrow: a thin red line strikes the old
 *     name, cost reads red, free reads blue with a blue glow
 *   - small data rows, BEST FOR / WATCH OUT tip cards
 *
 * What changes per slide is the CONTENT and which blocks carry it; the look
 * stays one family, like the carousel. Logo tiles are light or dark by
 * measured contrast (`tile`, set by compile_shot_plan; G69 blocks a logo that
 * would vanish on its tile — the Suno mark once rendered black on navy).
 *
 * Moves are timed in words (`on`) and resolved to `at` seconds by the
 * compiler, exactly like stage moves:
 *   show       target = block id, "swapId.left" / "swapId.right", "rowsId.N"
 *   strike     target = "swapId.left|right" or "rowsId.N"
 *   highlight  target = "rowsId.N"
 * A block with no `show` is filled from the start.
 */

export interface SlideSide {
  logo?: string;
  tile?: "light" | "dark";
  name: string;
  /** the big line: a price ("$10") counts up; any other text just lands */
  price?: string;
  tone?: "cost" | "free" | "plain";
  note?: string;
}

export type SlideBlock =
  | { id: string; kind: "hero"; side: SlideSide }
  | { id: string; kind: "swap"; left: SlideSide; right: SlideSide }
  | { id: string; kind: "rows"; rows: { k: string; v: string; tone?: "cost" | "free" | "plain" }[] }
  | { id: string; kind: "text"; text: string }
  | { id: string; kind: "tips"; best?: string; watch?: string }
  | { id: string; kind: "logos"; items: { logo: string; name: string; tile?: "light" | "dark" }[] }
  | ScreenBlockProps | StepsBlockProps | DevicesBlockProps | WavesBlockProps
  | { id: string; kind: "spotlight"; logo: string; name: string; note?: string; overlay?: boolean };

export interface SlideMove {
  /** pill: target "headline" — the yellow pill lands on the spoken word, not
   *  with the headline (the words sit white until then) */
  do: "show" | "strike" | "highlight" | "pill" | "focus" | "state" | "drift";
  target: string;
  at?: number;
  on?: string;
  /** focus: the region of a screen block to move the camera to, source px [x, y, w, h] */
  rect?: [number, number, number, number];
  /** focus: draw the ring (default true) */
  ring?: boolean;
  /** state: the published screenshot to crossfade to */
  src?: string;
}

export interface SlideProps {
  /** a running label + "n / N" top bar — carousel pages only. Reels leave both
   *  out (user, 2026-09-16: "not required as it is reel (shorts) end of the day") */
  series?: string;
  index?: string;
  /** dark = the carousel's own look; light = the same family on a bright
   *  ground (covers that must stand out in a dark feed) */
  theme?: "dark" | "light";
  eyebrow?: string;
  /** [[word]] marks the one yellow pill */
  headline: string;
  /** "xl": the end card's ask — "Comment [[KEYWORD]]" at poster size (2026-09-16,
   *  after the Carousel Playbook's CTA page) */
  headlineSize?: "xl";
  blocks: SlideBlock[];
  moves?: SlideMove[];
  /** the presenter in a corner circle, talking — lets a reel OPEN on the
   *  picture with the face still present (2026-09-16) */
  presenter?: { src: string; from: number };
}

const FONT = "Inter, -apple-system, 'SF Pro Display', sans-serif";
const DARK = {
  bg: "#000000", card: "#1B1B1E", line: "rgba(255,255,255,0.07)", ink: "#FFFFFF", sub: "#D1D1D6",
  muted: "#8E8E93", blue: "#4DA3FF", red: "#FF453A", amber: "#F5A524", pill: "#FFD60A",
  tileLight: "#E5E5EA", tileDark: "#2C2C30",
};
const LIGHT = {
  ...DARK, bg: "#F2F2F7", card: "#FFFFFF", line: "rgba(0,0,0,0.08)", ink: "#0A0A0A", sub: "#3A3A3C",
  muted: "#6E6E73", blue: "#0A6CFF", red: "#E5322D",
};
const L = 72;          // left margin, the carousel's own
const COL = 916;       // column width: clears Instagram's right rail (0.85 of 1080)
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const ramp = (t: number, a: number, d = 0.3) =>
  interpolate(t, [a, a + d], [0, 1], { ...CL, easing: Easing.out(Easing.cubic) });


/** "$239.88" / "10,000" -> counted up; anything else ("Every 5 hours") is shown
 *  as written — counting the 5 there once rendered "Every 4 hours" */
const counted = (price: string, p: number) => {
  const m = price.match(/^(\$?)([0-9][0-9,]*(?:\.[0-9]+)?)()$/);
  if (!m) return price;
  const target = Number(m[2].replace(/,/g, ""));
  if (!target) return price;
  const dec = (m[2].split(".")[1] ?? "").length;
  const v = target * p;
  return `${m[1]}${v.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec })}${m[3]}`;
};

const Tile: React.FC<{ src: string; tile?: "light" | "dark"; size: number }> = ({ src, tile, size }) => (
  <div style={{
    width: size, height: size, borderRadius: size * 0.24, flexShrink: 0,
    background: tile === "light" ? DARK.tileLight : DARK.tileDark,
    display: "flex", alignItems: "center", justifyContent: "center",
  }}>
    <Img src={staticFile(src)} style={{ width: size * 0.6, height: size * 0.6, objectFit: "contain" }} />
  </div>
);

/** a thin red line drawn across whatever it sits on */
const Strike: React.FC<{ p: number }> = ({ p }) =>
  p > 0 ? (
    <div style={{ position: "absolute", left: -6, top: "54%", height: 6, borderRadius: 3,
      width: `calc(${p * 100}% + 12px)`, background: DARK.red }} />
  ) : null;

export const Slide: React.FC<{ scene: SlideProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dur = (scene as { durationSec?: number }).durationSec ?? durationInFrames / fps;
  const C = scene.theme === "light" ? LIGHT : DARK;
  const xl = scene.headlineSize === "xl";
  const toneColor = (tone?: string) => (tone === "cost" ? C.red : tone === "free" ? C.blue : C.ink);
  const moves = scene.moves ?? [];
  const at = (d: string, target: string) => moves.find((m) => m.do === d && m.target === target)?.at;
  // shown from the start unless a `show` names it (or its parent block)
  const shownAt = (target: string) => at("show", target) ?? at("show", target.split(".")[0]) ?? 0;

  // ---- headline: words rise in, 45ms apart; [[x]] becomes the pill ----
  const parts = scene.headline.split(/(\[\[[^\]]+\]\])/).filter(Boolean);
  let wi = 0;
  const headline = parts.map((part, pi) => {
    const pill = part.startsWith("[[");
    const words = (pill ? part.slice(2, -2) : part).split(/(\s+)/);
    const nodes = words.map((w, k) => {
      if (!w.trim()) return <span key={k}>{w}</span>;
      const p = ramp(t, 0.05 + 0.045 * wi++, 0.28);
      return (
        <span key={k} style={{ display: "inline-block", opacity: p, transform: `translateY(${(1 - p) * 26}px)` }}>{w}</span>
      );
    });
    if (!pill) return <React.Fragment key={pi}>{nodes}</React.Fragment>;
    // the pill lands on its spoken word when a `pill` move names one; else WITH
    // its first word — never before it (alone it read as an empty yellow bar)
    const w0 = wi - words.filter((w) => w.trim()).length;
    const pillAt = Math.max(0.05 + 0.045 * w0, at("pill", "headline") ?? 0);
    const f0 = Math.round(pillAt * fps);
    const pp = frame < f0 ? 0 : spring({ frame: frame - f0, fps, config: { damping: 12, stiffness: 200 } });
    const lit = Math.min(1, pp * 2);
    return (
      <span key={pi} style={{ display: "inline-block", borderRadius: 18, padding: "0 18px", margin: "0 2px",
        background: `rgba(255,214,10,${lit})`, color: lit > 0.5 ? "#000" : C.ink,
        transform: `scale(${1 + 0.12 * Math.sin(Math.PI * Math.min(1, pp))})` }}>{nodes}</span>
    );
  });

  // ---- a card side: tile, name, big line, note ----
  const side = (s: SlideSide, target: string, glow: boolean) => {
    const p = ramp(t, shownAt(target));
    const sk = at("strike", target);
    const sp = sk !== undefined ? ramp(t, sk, 0.35) : 0;
    const price = s.price ? (/^\$?0$/.test(s.price) ? s.price : counted(s.price, ramp(t, shownAt(target), 0.9))) : "";
    const lit = glow && p > 0;
    return (
      <div style={{
        flex: 1, background: C.card, borderRadius: 34, padding: "36px 30px",
        // NO EMPTY SHELLS (user, 2026-09-16): the card itself lands with its
        // content. Its space is held from frame 0, so nothing jumps when it does.
        opacity: p, transform: `translateY(${Math.round((1 - p) * 28)}px)`,
        border: `2px solid ${lit ? `rgba(77,163,255,${0.55 * p})` : C.line}`,
        backgroundImage: lit ? `radial-gradient(90% 70% at 50% 0%, rgba(29,95,170,${0.45 * p}) 0%, transparent 70%)` : undefined,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center",
      }}>
        <div style={{ opacity: 1 - 0.35 * sp, display: "flex", flexDirection: "column", alignItems: "center" }}>
          {s.logo ? <Tile src={s.logo} tile={s.tile} size={150} /> : null}
          <div style={{ position: "relative", marginTop: s.logo ? 26 : 0, font: `700 44px/1.15 ${FONT}`,
            color: sp > 0 ? C.muted : C.ink }}>
            {s.name}
            <Strike p={sp} />
          </div>
          {s.price ? (
            <div style={{ position: "relative", marginTop: 8, font: `800 ${s.price.length > 8 ? 62 : 88}px/1.08 ${FONT}`,
              letterSpacing: -2, fontVariantNumeric: "tabular-nums", color: toneColor(s.tone) }}>
              {price}
              {/* a plain big line is the thing being retired ("Once a day"): strike it too */}
              {!s.tone || s.tone === "plain" ? <Strike p={sp} /> : null}
            </div>
          ) : null}
          {s.note ? <div style={{ marginTop: 10, font: `500 30px/1.3 ${FONT}`, color: C.muted }}>{s.note}</div> : null}
        </div>
      </div>
    );
  };

  const block = (b: SlideBlock) => {
    switch (b.kind) {
      case "hero":
        return <div key={b.id} style={{ display: "flex", flex: "1 0 auto", maxHeight: 760 }}>{side(b.side, b.id, b.side.tone === "free")}</div>;
      case "swap": {
        const ar = ramp(t, shownAt(`${b.id}.right`) - 0.15, 0.25);
        return (
          <div key={b.id} style={{ display: "flex", alignItems: "stretch", gap: 0, flex: "1 0 auto", maxHeight: 760 }}>
            {side(b.left, `${b.id}.left`, b.left.tone === "free")}
            <div style={{ width: 84, display: "flex", alignItems: "center", justifyContent: "center",
              font: `600 56px ${FONT}`, color: C.blue, opacity: ar, transform: `translateX(${(ar - 1) * 16}px)` }}>→</div>
            {side(b.right, `${b.id}.right`, b.right.tone === "free")}
          </div>
        );
      }
      case "rows":
        return (
          <div key={b.id} style={{ display: "flex", flexDirection: "column", gap: 14,
            flex: `${b.rows.length} 1 0`, minHeight: b.rows.length * 84, maxHeight: b.rows.length * 270 }}>
            {b.rows.map((r, i) => {
              const tg = `${b.id}.${i}`;
              const own = at("show", tg);
              const p = ramp(t, own ?? shownAt(b.id) + (at("show", b.id) !== undefined ? 0.12 * i : 0));
              const hl = at("highlight", tg);
              const h = hl !== undefined ? ramp(t, hl, 0.3) : 0;
              const sk = at("strike", tg);
              const sp = sk !== undefined ? ramp(t, sk, 0.35) : 0;
              return (
                <div key={i} style={{
                  display: "flex", alignItems: "center", justifyContent: "space-between", gap: 24, flex: "1 1 0",
                  opacity: p, transform: `translateY(${Math.round((1 - p) * 20)}px)`,
                  background: h > 0 ? `rgba(18,40,68,${h})` : C.card, borderRadius: 24,
                  padding: "0 36px",
                  border: `2px solid ${h > 0 ? `rgba(77,163,255,${h})` : C.line}`,
                }}>
                  <div style={{ position: "relative", font: `600 ${b.rows.length <= 4 ? 44 : 38}px/1.2 ${FONT}`, color: C.ink }}>
                    {r.k}<Strike p={sp} />
                  </div>
                  <div style={{ font: `700 ${b.rows.length <= 4 ? 44 : 38}px/1.2 ${FONT}`, color: toneColor(r.tone), textAlign: "right" }}>{r.v}</div>
                </div>
              );
            })}
          </div>
        );
      case "text": {
        const p = ramp(t, shownAt(b.id));
        return (
          <div key={b.id} style={{ opacity: p, transform: `translateY(${(1 - p) * 14}px)`,
            font: `500 42px/1.35 ${FONT}`, color: C.sub }}>{b.text}</div>
        );
      }
      case "tips": {
        const card = (label: string, color: string, text: string, target: string) => {
          const p = ramp(t, shownAt(target));
          return (
            <div style={{ flex: 1, background: C.card, borderRadius: 26, padding: "30px 32px", border: `2px solid ${C.line}`,
              opacity: p, transform: `translateY(${Math.round((1 - p) * 20)}px)` }}>
              <div style={{ font: `700 28px ${FONT}`, letterSpacing: 2, color }}>{label}</div>
              <div style={{ marginTop: 12, font: `500 36px/1.3 ${FONT}`, color: C.ink }}>{text}</div>
            </div>
          );
        };
        return (
          <div key={b.id} style={{ display: "flex", gap: 20 }}>
            {b.best ? card("BEST FOR", C.blue, b.best, `${b.id}.best`) : null}
            {b.watch ? card("WATCH OUT", C.amber, b.watch, `${b.id}.watch`) : null}
          </div>
        );
      }
      case "screen":
        return <ScreenBlock key={b.id} b={b} moves={moves} t={t} boxW={COL} C={C} shown={ramp(t, shownAt(b.id))} />;
      case "steps":
        return <StepsBlock key={b.id} b={b} moves={moves} t={t} C={C} />;
      case "devices":
        return <DevicesBlock key={b.id} b={b} moves={moves} t={t} boxW={COL} C={C} />;
      case "spotlight": {
        // THE PRODUCT REVEAL (2026-09-17: "PairPods doesn't grab the attention
        // when the avatar talks about it"). The icon lands big with a burst
        // ring and a glow on the spoken name; the name sits under it. One
        // arrival, then still — the burst is a shape, never a scale on type.
        const a = shownAt(b.id);
        const k = t < a ? 0 : spring({ frame: frame - Math.round(a * fps), fps, config: { damping: 11, stiffness: 170, mass: 0.8 } });
        const burst = interpolate(t, [a, a + 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
        const size = 300;
        return (
          <div key={b.id} style={b.overlay
            ? { position: "absolute", left: 0, right: 0, top: 0, bottom: 0, zIndex: 5, display: "flex", flexDirection: "column",
                alignItems: "center", justifyContent: "center", background: `rgba(0,0,0,${0.82 * Math.min(1, k * 2)})`,
                opacity: t < a ? 0 : 1 }
            : { position: "relative", display: "flex", flexDirection: "column", alignItems: "center",
                padding: "26px 0", opacity: Math.min(1, k * 2) }}>
            {burst > 0 && burst < 1 ? (
              <div style={{ position: "absolute", top: b.overlay ? "calc(50% - 60px)" : 26 + size / 2, left: "50%", width: size * (1 + 1.2 * burst),
                height: size * (1 + 1.2 * burst), borderRadius: "50%", border: `6px solid ${C.pill}`, opacity: 1 - burst,
                transform: "translate(-50%, -50%)" }} />
            ) : null}
            <div style={{ width: size, height: size, borderRadius: size * 0.23, overflow: "hidden",
              boxShadow: `0 0 ${Math.round(90 * Math.min(1, k))}px rgba(255,214,10,0.45), 0 30px 60px rgba(0,0,0,0.5)`,
              transform: `scale(${0.4 + 0.6 * k})` }}>
              <Img src={staticFile(b.logo)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </div>
            <div style={{ marginTop: 26, font: `800 76px/1.05 ${FONT}`, letterSpacing: -2, color: C.ink,
              opacity: ramp(t, a + 0.25, 0.3) }}>{b.name}</div>
            {b.note ? <div style={{ marginTop: 10, font: `600 38px ${FONT}`, color: C.blue, opacity: ramp(t, a + 0.45, 0.3) }}>{b.note}</div> : null}
          </div>
        );
      }
      case "waves":
        return <WavesBlock key={b.id} b={b} moves={moves} t={t} boxW={COL} C={C} shown={ramp(t, shownAt(b.id))} />;
      case "logos": {
        const base = shownAt(b.id);
        // MORE THAN 6 ITEMS NEEDS A SMALLER GRID (2026-09-18) — the fixed
        // 390px tile was sized for five-free-ai-tools' 5 logos (2 rows) and
        // runs a 10-item grid (4 rows) straight through the platform safe
        // floor. Compact below the size that was ever measured to fit.
        const compact = b.items.length > 6;
        const tileH = compact ? 168 : (xl && scene.presenter ? 300 : 390);
        const logoSize = compact ? 80 : (xl && scene.presenter ? 130 : 170);
        return (
          <div key={b.id} style={{ display: "flex", flexWrap: "wrap", gap: compact ? 12 : 20, justifyContent: "center" }}>
            {b.items.map((it, i) => {
              const p = ramp(t, base + 0.1 * i, 0.3);
              return (
                <div key={i} style={{ width: compact ? (COL - 28) / 3 : (COL - 40) / 3, height: tileH, background: C.card, borderRadius: compact ? 20 : 28,
                  border: `2px solid ${C.line}`, display: "flex", flexDirection: "column", alignItems: "center",
                  justifyContent: "center", opacity: p, transform: `translateY(${Math.round((1 - p) * 24)}px)` }}>
                  <div style={{ display: "flex",
                    flexDirection: "column", alignItems: "center" }}>
                    <Tile src={it.logo} tile={it.tile} size={logoSize} />
                    <div style={{ marginTop: compact ? 10 : 20, font: `600 ${compact ? 22 : 34}px/1.2 ${FONT}`, color: C.ink, textAlign: "center",
                      padding: "0 10px" }}>{it.name}</div>
                  </div>
                </div>
              );
            })}
          </div>
        );
      }
    }
  };

  // NEVER STILL, NEVER SHAKING (2026-09-16). A 3% push on the whole page was
  // tried first and the user saw the text shake: a fractional scale redraws
  // every glyph at a new sub-pixel size each frame (measured on the render: the
  // headline's centroid wobbled +/-0.3-0.5px frame to frame instead of drifting
  // one way). The motion lives in the GROUND instead — a soft glow crossing the
  // page — and type only ever moves while it arrives.
  const glowX = 25 + 50 * Math.min(1, t / Math.max(0.1, dur));
  const pipIn = scene.presenter ? spring({ frame, fps, config: { damping: 14, stiffness: 160 } }) : 0;
  const PIP = 300;
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}>
      <AbsoluteFill style={{ background: `radial-gradient(60% 35% at ${glowX}% 42%, ${scene.theme === "light"
        ? "rgba(10,108,255,0.06)" : "rgba(77,163,255,0.10)"} 0%, transparent 70%)` }} />
      {scene.presenter ? (
        <div style={{ position: "absolute", left: L + COL - PIP, top: 250, width: PIP, height: PIP, zIndex: 2,
          borderRadius: "50%", overflow: "hidden", border: `6px solid ${C.pill}`,
          boxShadow: "0 20px 50px rgba(0,0,0,0.5)", transform: `scale(${0.6 + 0.4 * Math.min(1.04, pipIn)})` }}>
          <OffthreadVideo src={staticFile(scene.presenter.src)} muted startFrom={Math.round(scene.presenter.from * fps)}
            style={{ width: "100%", height: "178%", objectFit: "cover", objectPosition: "50% 0%", marginTop: "-12%" }} />
        </div>
      ) : null}
      <div style={{ position: "absolute", left: L, top: scene.series || scene.index ? 200 : 250, width: COL,
        // CAPTION BAND (user, 2026-09-17): a slide that shows captions stops its
        // content at ~69% so the chips sit alone at 72-77%, above the platform
        // zone. Without captions it fills to the 80% line as before.
        bottom: (scene as { hideCaptions?: boolean }).hideCaptions === false ? 576 : 384,
        display: "flex", flexDirection: "column" }}>
        {scene.series || scene.index ? (
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 40, font: `600 34px ${FONT}`, color: C.sub }}>
            <span>{scene.series ?? ""}</span>
            <span style={{ color: C.muted }}>{scene.index ?? ""}</span>
          </div>
        ) : null}
        {/* An XL end-card ask beside the presenter circle broke into four ragged
            lines ("Link in / the / pinned / comment", 2026-09-17). With a
            presenter, the XL headline starts BELOW the circle at full width;
            the eyebrow keeps the space beside it. */}
        {scene.eyebrow || (xl && scene.presenter) ? (
          <div style={{ font: `600 38px ${FONT}`, color: C.blue, maxWidth: scene.presenter ? COL - PIP - 30 : undefined,
            minHeight: xl && scene.presenter ? PIP : undefined, display: "flex", alignItems: xl && scene.presenter ? "center" : undefined }}>
            {scene.eyebrow ?? ""}
          </div>
        ) : null}
        <div style={{ marginTop: 14, font: `800 ${xl ? 112 : 84}px/1.08 ${FONT}`,
          letterSpacing: xl ? -3.5 : -2.5, color: C.ink,
          maxWidth: scene.presenter && !xl ? COL - PIP - 30 : undefined }}>{headline}</div>
        {/* FILL TO THE 80% LINE (user, 2026-09-16). Blocks start under the
            headline and the cards/rows grow into the page; centring them left a
            gap above and an unfinished lower half, and a dense slide overflowed
            to 90% — under Instagram's caption. lint_frames measures both. */}
        <div style={{ position: "relative", flex: 1, minHeight: 0, display: "flex", flexDirection: "column", justifyContent: "flex-start",
          gap: 28, marginTop: 44 }}>
          {scene.blocks.map(block)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
