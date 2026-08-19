import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { Headline } from "../types";
import { SAFE_RECT } from "../platformSafeArea";
import { TYPE, SIZE } from "../theme/type";
import { useTheme } from "../theme/tokens";
import { fitOneLine } from "../theme/fit";
import { impactAt, IMPACT, punch, jolt, flare } from "../theme/impact";

const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
const easeOut = (x: number) => 1 - Math.pow(1 - clamp01(x), 3);


const SANS = "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif";

/**
 * The headline treatment for text laid over footage.
 *
 * REBUILT 2026-08-17 after three defects were found in one rendered frame
 * (iphone-fold-ultra scene 09, "UNFOLDED / 7.76″ / reported · MacRumors"):
 *
 * 1. INK COLLISION. `lineHeight: 1.02` makes the line BOX shorter than the
 *    glyphs it contains, and a flex `gap` measures boxes, not ink — so the
 *    subtitle's ascenders sat on top of the numerals. It looked like a
 *    mid-animation artefact; it was permanent, on every three-line headline.
 *    Line height is now >= 1.12 and the gap scales with the largest type.
 *
 * 2. UNREADABLE ACCENT. Clay #d97757 was chosen against cream. Over a warm
 *    orange wallpaper it nearly vanished, and a drop-shadow cannot rescue a
 *    colour that matches its background in hue AND value. There is now a scrim
 *    behind the block, sized to the text, so the type always has its own ground.
 *
 * 3. FROZEN. The only motion was a 14-frame entrance per line, after which the
 *    frame was static — the "flat" the user kept reporting. Lines now keep a
 *    slow drift, and an accent line gets a bar that draws under it.
 *
 * It also CLAMPS y into the platform safe band rather than trusting the beat
 * sheet: a headline at y 0.07 renders under Instagram's own header, and that is
 * a structural fact about Reels, not a matter of taste. Composition inside the
 * band stays the author's call.
 */

/**
 * WHICH TREATMENT A LINE GETS, derived from what the line IS.
 *
 * `kind` (label/headline/subtitle) is a typed flag, the same shape of guess as
 * `theme` was before contrast became a measurement. What a line NEEDS follows
 * from its content:
 *
 *   payload   a number is the thing the beat exists to deliver — it should
 *             land as one object, punched, with figures that do not jitter
 *   claim     a sentence is READ, so it arrives per-word, synced to speech
 *   label     an eyebrow is context, not content: it tracks in, quietly
 *   question  a question is an invitation — italic, softer landing
 *
 * Per-word timing and the SLIDE DECAY come from the hyperframes-animation skill
 * (techniques.md #4, "Per-Word Kinetic Typography"): the first word travels
 * furthest and later words settle quicker, which is what makes it read as
 * kinetic rather than as a queue. Implemented natively because that skill's
 * recipes are GSAP, and Remotion renders nothing that is not frame-driven.
 */
type Treatment = "payload" | "claim" | "label" | "question";

const treatmentOf = (text: string, kind: string): Treatment => {
  const words = text.trim().split(/\s+/);
  if (kind === "label") return "label";
  if (text.trim().endsWith("?")) return "question";
  // a line that is mostly a number, e.g. "7.76\u2033" or "$249" or "248 MP"
  const numeric = words.filter((w) => /\d/.test(w)).length;
  if (words.length <= 3 && numeric >= 1) return "payload";
  return kind === "headline" ? "claim" : "label";
};

export const HeadlineBuild: React.FC<{ spec: Headline }> = ({ spec }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const align = spec.align ?? "center";
  const dark = spec.theme === "dark";

  // THE ACCENT COMES FROM THE STYLE PACK, and which of its two text variants is
  // used comes from the ground this headline was measured onto (tools/
  // auto_contrast.py writes `theme` from the pixels). This file used to carry
  // `const ACCENT = "#d97757"` — a colour belonging to no palette, applied to
  // both grounds, which is what shipped the orange the user called out on
  // 2026-08-18. See theme/tokens.ts accentPair().
  const theme = useTheme();
  const ACCENT = dark ? theme.accentInk : theme.accentOnDark;
  // Ink from the style pack too. #0f0f0f was a near-black that belonged to no
  // palette and differed from theme.ink (#141414) by an amount nobody can see —
  // the same accumulation the type and motion scales were built to end.
  const ink = dark ? theme.ink : theme.inkOnDark;
  const rgb = [1, 3, 5]
    .map((i) => parseInt(ink.slice(i, i + 2), 16))
    .join(",");

  // SIZES COME FROM THE SCALE, THEN SHRINK TO FIT.
  //
  // The scale sets the intent; the frame has the final say. G05 used to be a
  // BLOCKING gate holding a typed character budget — headline 18, subtitle 26 —
  // calibrated against Fraunces. When the display face became Space Grotesk
  // (wider) on 2026-08-18 the real budget fell to ~14 characters and the gate
  // silently kept passing 18, so six headlines already in the library overflow
  // the frame while the build says they are fine — "NEVER ANNOUNCED" on the
  // airpods-camera hook among them.
  //
  // A character budget is a measurement of a typeface written down somewhere
  // the typeface cannot reach. Fitting here makes overflow impossible by
  // construction, which is what let G05 become advice.
  const boxW = width * (1 - 2 * SAFE_RECT.x0) - (align === "center" ? 140 : 168);
  const sizeFor = (kind: string, text = "") => {
    const base =
      kind === "label" ? SIZE.label : kind === "subtitle" ? SIZE.lead : SIZE.display;
    return fitOneLine(text, base, boxW);
  };

  const styleFor = (kind: string, text = ""): React.CSSProperties => {
    const fontSize = sizeFor(kind, text);
    if (kind === "label") return { ...TYPE.label, fontSize };
    if (kind === "subtitle") return { ...TYPE.lead, fontSize, opacity: 0.95 };
    // 1.12, never 1.02: below ~1.1 the ink overflows its own box and the flex
    // gap — which measures boxes — stops keeping lines apart.
    // THE DISPLAY VOICE COMES FROM THE SCALE. HeadlineBuild hardcoded its own
    // SANS and never read the theme, so every headline rendered in the macOS UI
    // font. Since 2026-08-18 that voice is Space Grotesk, not a serif — the
    // eyebrow stays SF Pro, so the pairing is now grotesk display over neutral
    // sans label. Two sans faces separated by character, not by category.
    return { ...TYPE.display, fontSize };
  };

  const biggest = Math.max(...spec.lines.map((l) => sizeFor(l.kind, l.text)), 46);
  const gap = Math.round(biggest * 0.14);

  // Rough block height, to keep the whole thing inside the safe band rather
  // than only its anchor point.
  const blockH = spec.lines.reduce(
    (h, l) => h + sizeFor(l.kind, l.text) * 1.2, 0) + gap * (spec.lines.length - 1);
  const halfFrac = blockH / 2 / height;
  const yWanted = spec.y ?? 0.5;
  const y = Math.min(
    Math.max(yWanted, SAFE_RECT.y0 + halfFrac),
    SAFE_RECT.y1 - halfFrac,
  );

  // Never frozen: a slow drift that continues for the whole scene. Small enough
  // to read as life rather than movement.
  const drift = interpolate(t, [0, 6], [0, -10], { extrapolateRight: "clamp" });
  const breathe = 1 + 0.012 * Math.sin(t * 0.9);

  const firstAt = Math.min(...spec.lines.map((l) => l.at));
  const scrim = interpolate(t, [firstAt, firstAt + 0.45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: align === "center" ? "center" : "flex-start",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: `${y * 100}%`,
          transform: `translateY(-50%) translateY(${drift}px) scale(${breathe})`,
          width: "100%",
          padding: align === "center" ? "0 70px" : "0 84px",
          textAlign: align,
          display: "flex",
          flexDirection: "column",
          alignItems: align === "center" ? "center" : "flex-start",
          gap,
        }}
      >
        {/* Its own ground. A drop-shadow cannot save type whose colour matches
            the footage in both hue and value, which is what happened to the
            clay accent over an orange wallpaper. */}
        {/* A scrim is needed whenever type sits over MEDIA — the question is
            its COLOUR, not whether to draw it. This used to be `{!dark && ...}`,
            so choosing dark ink switched the scrim off entirely: the airpods
            hook rendered black, unscrimmed and unshadowed over a bright window.
            Dark ink now gets a LIGHT scrim; light ink gets a dark one. */}
        {true && (
          <div
            style={{
              position: "absolute",
              // Reaches well past the text so the falloff happens off the type,
              // not across it. A scrim clipped tight to the text block reads as
              // a translucent RECTANGLE with hard edges — which is what the
              // first attempt produced.
              left: -120,
              right: -120,
              top: -gap * 5,
              bottom: -gap * 5,
              background: dark
                ? "linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.62) 26%, rgba(255,255,255,0.66) 74%, rgba(255,255,255,0) 100%)"
                : "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.46) 26%, rgba(0,0,0,0.5) 74%, rgba(0,0,0,0) 100%)",
              opacity: scrim,
              pointerEvents: "none",
            }}
          />
        )}

        {spec.lines.map((ln, i) => {
          // The entrance spring that used to live here is gone, not disabled:
          // it drove `opacity` and a 26px hop, and waterfall-entry.md rules out
          // both — binary opacity, and travel by weight on a power4.out whip
          // rather than a spring's settle. Leaving it computed-but-unused is
          // how dead motion code survives long enough to get re-attached.
          //
          // THE VISUAL HALF OF THE SOUND EFFECT. A line is STRUCK at the
          // instant it lands, on the transient envelope of theme/impact.ts —
          // and where the beat sheet carries an SFX cue, tools/sync_impacts.py
          // has already moved that cue onto this same instant, so the hit the
          // viewer hears and the hit they see are one event. Measured before
          // building it: this reel had 8 cues and 6 headline scenes that
          // intersected exactly once, at different times.
          const treat = treatmentOf(ln.text, ln.kind);
          const strength = IMPACT[treat];
          const env = impactAt(t, [ln.at, ...(spec.impacts ?? [])]);
          const hit = punch(env, strength);
          const shift = jolt(env, strength, i);
          const reveal = interpolate(t, [ln.at, ln.at + 0.5], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const isHead = ln.kind === "headline";
          const a = 0.34 + 0.66 * reveal;
          const color = ln.accent ? ACCENT : isHead ? `rgba(${rgb},${a})` : ink;
          // An accent line earns a bar that draws under it — the emphasis the
          // treatment was missing, frame-driven so it actually renders.
          const bar = ln.accent
            ? interpolate(t, [ln.at + 0.18, ln.at + 0.62], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            : 0;
          return (
            <div
              key={i}
              style={{
                position: "relative",
                // BINARY — waterfall-entry.md, "never fade an arrival". This
                // was `opacity: en`, a spring-driven ramp on every headline
                // line in every reel. A claim that fades up reads as tentative;
                // the whip below is what should announce it.
                opacity: t >= ln.at ? 1 : 0,
                // Travel by WEIGHT, per the same rule's table: the display
                // claim is an anchor (72px), an eyebrow is light (34px).
                transform:
                  `translateY(${(1 - easeOut(Math.min(1, (t - ln.at) / (isHead ? 0.19 : 0.13)))) *
                    (isHead ? 72 : 34) + shift}px) scale(${hit})`,
              }}
            >
              <div
                style={{
                  ...styleFor(ln.kind, ln.text),
                  ...(treatmentOf(ln.text, ln.kind) === "payload"
                    ? { fontVariantNumeric: "tabular-nums" as const,
                        letterSpacing: -2.5,
                        transform: `scale(${1 + 0.06 * (1 - easeOut((t - ln.at) / 0.34))})` }
                    : {}),
                  ...(treatmentOf(ln.text, ln.kind) === "label"
                    ? { letterSpacing: 2 + 6 * (1 - easeOut((t - ln.at) / 0.5)) }
                    : {}),
                  ...(treatmentOf(ln.text, ln.kind) === "question"
                    ? { fontStyle: "italic" as const }
                    : {}),
                  color,
                  whiteSpace: "pre-line",
                  // dark ink got textShadow: "none", which removed its last
                  // defence on busy footage. It needs a LIGHT halo, the mirror
                  // of what light ink gets.
                  textShadow:
                    (dark
                      ? "0 2px 14px rgba(255,255,255,0.85), 0 1px 2px rgba(255,255,255,0.9)"
                      : "0 3px 18px rgba(0,0,0,0.75), 0 1px 3px rgba(0,0,0,0.6)")
                    // The flare — a bloom in the ACCENT colour on the frames
                    // the line is struck, gone within ~4 frames. Layered onto
                    // the legibility shadow rather than replacing it, because
                    // the shadow is what keeps the type readable and an effect
                    // must never cost legibility.
                    + (env > 0.01
                        ? `, 0 0 ${Math.round(34 * env)}px ${ACCENT}${Math.round(
                            flare(env, strength) * 255
                          ).toString(16).padStart(2, "0")}`
                        : ""),
                }}
              >
                {treatmentOf(ln.text, ln.kind) !== "claim"
                  ? ln.text
                  : ln.text.split(/(\s+)/).map((tok, wi) => {
                      if (!tok.trim()) return tok;
                      const idx = wi >> 1;
                      // 80ms apart, and the SLIDE DECAYS: 80,60,50,25,12...
                      // early words travel, later ones settle. Straight from
                      // hyperframes-animation techniques.md #4.
                      const at = ln.at + idx * 0.08;
                      const slide = Math.max(10, 80 * Math.pow(0.72, idx));
                      const p = easeOut((t - at) / 0.42);
                      return (
                        <span
                          key={wi}
                          style={{
                            display: "inline-block",
                            opacity: p,
                            transform: `translateX(${(1 - p) * slide}px)`,
                          }}
                        >
                          {tok}
                        </span>
                      );
                    })}
              </div>
              {bar > 0 && (
                <div
                  style={{
                    height: Math.max(5, sizeFor(ln.kind) * 0.055),
                    width: `${bar * 100}%`,
                    marginTop: Math.round(sizeFor(ln.kind) * 0.06),
                    marginLeft: align === "center" ? `${(1 - bar) * 50}%` : 0,
                    background: ACCENT,
                    borderRadius: 999,
                    boxShadow: `0 2px 14px ${ACCENT}88`,
                  }}
                />
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
