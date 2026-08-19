import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { useTheme } from "../theme/tokens";
import { DISPLAY, TYPE } from "../theme/type";
import { SAFE_RECT, BANDS } from "../platformSafeArea";
import { easeOut } from "../theme/motion";
import { ADVANCE } from "../theme/fit";
import { Credit } from "./Credit";
import type { Scene } from "../types";

type TypeCardProps = Extract<Scene, { type: "typecard" }>;

/**
 * A full-frame card carrying one piece of display type.
 *
 * REBUILT 2026-08-18, for two defects found in the same frame.
 *
 * 1. DEAD SPACE. tools/lint_frames.py measured these cards at 88-90% flat
 *    frame against a 70% limit — the worst in the reel, and it had been
 *    advising it for three renders. The cause was structural: KineticType set
 *    ONE line at a fixed 100px, centred, on a 1080x1920 field. "4.5mm unfolded"
 *    at 100px covers about a tenth of the frame, so nine tenths was cream. The
 *    lint's own advice is "fill the empty band with large type", and the only
 *    way to do that for arbitrary copy is to stop typing a size and SOLVE for
 *    one.
 *
 * 2. THE CREDIT WAS NEVER DRAWN. Five typecards in iphone-fold-ultra carry
 *    "credit": "MacRumors" in the beat sheet. This component rendered no
 *    Credit, so all five were invisible — MacRumors' numbers on screen with no
 *    attribution anywhere. G14 (RIGHTS, blocking) passed every time, because it
 *    reads the beat sheet and the beat sheet was correct. Another check that
 *    could not see the thing it protects.
 *
 * The type is FITTED, not chosen: given the copy and the safe band, solve for
 * the size that fills it. Long copy gets smaller, short copy gets enormous, and
 * neither needs a human to pick a number per card.
 */

/**
 * Solve for a font size that fills `boxW` x `boxH` with `text`.
 *
 * Width is estimated from character count rather than measured, deliberately:
 * hyperframes-core forbids deriving layout from getBoundingClientRect() at
 * render time because the renderer samples frames in parallel and a measured
 * layout desyncs between them. An estimate that is identical on every frame
 * beats a measurement that is not.
 *
 * ADVANCE is the mean glyph width as a fraction of em for Space Grotesk 700 in
 * mixed case. It is an approximation and the CAP below is what keeps a bad
 * estimate from overflowing: the fit is checked against both axes, and the
 * smaller wins.
 */
// ADVANCE now lives in theme/fit.ts, shared with HeadlineBuild and
// mirrored by G05 — it is a property of the typeface, not of this card.

/**
 * Break the copy into lines and size EACH ONE to the frame.
 *
 * One size for the whole block is what left the card 88% empty: the longest
 * word is the binding constraint, so "unfolded" held "4.5mm" down to its own
 * width and the number — the thing the beat exists to deliver — came out the
 * same size as its qualifier. Sizing per line lets the payload be enormous and
 * the qualifier sit under it, which is both a fuller frame and the correct
 * hierarchy. It is the SpecSheet/stat treatment, applied to a card.
 *
 * Short connectives ("a", "two", "of") are joined to the following word rather
 * than given a line of their own — a line reading just "a" at 260px is a joke.
 */
/** One rendered line, tagged with the CLAIM it belongs to (for its timing). */
type Line = { text: string; size: number; claim: number };

/**
 * Break the copy into lines and size EACH ONE to the frame.
 *
 * Two levels, because a card can carry two claims:
 *
 *   CLAIMS are the `\n`-separated units. Each lands on its own spoken phrase
 *   (Kinetic.ats), so the break between them is fixed and may never be
 *   re-decided by the layout.
 *   LINES are how a claim is broken to fill its share of the band, chosen by
 *   the ink search below.
 *
 * The first version treated a claim as a LINE, which quietly made the merged
 * card WORSE than the two it replaced — 86% empty against 76% and 74% — because
 * "nothing confirmed" as one 17-character line is width-capped at 87px, while
 * the search puts it on two lines at 212px. Fixing dead space by merging cards
 * and then not searching inside them is doing the arithmetic and skipping the
 * point.
 */
const layout = (text: string, boxW: number, boxH: number): Line[] => {
  const claims = text.split("\n").map((l) => l.trim()).filter(Boolean);
  if (!claims.length) return [{ text: "", size: 90, claim: 0 }];

  // Each claim gets an equal share of the band's height to fill.
  const share = boxH / claims.length;
  const out: Line[] = [];
  claims.forEach((claim, ci) => {
    const raw = claim.split(/\s+/).filter(Boolean);
    const size = (g: string, lines: number) =>
      Math.min(boxW / (g.length * ADVANCE), share / lines / 1.12, 300);

    // SEARCH, don't rule-of-thumb. Every contiguous split into 1..3 lines is
    // scored by the INK it puts on the frame — the same quantity
    // lint_frames.py measures the absence of — so the layout optimises what is
    // actually being judged rather than a proxy somebody invented.
    let best: string[] = [raw.join(" ")];
    let bestInk = -1;
    const walk = (start: number, acc: string[]) => {
      if (start === raw.length) {
        if (acc.length > Math.min(3, raw.length)) return;
        const sizes = acc.map((g) => size(g, acc.length));
        if (sizes.reduce((s, v) => s + v * 1.12, 0) > share) return;
        const ink = acc.reduce(
          (s, g, i) => s + g.length * ADVANCE * sizes[i] * sizes[i], 0);
        if (ink > bestInk) { bestInk = ink; best = [...acc]; }
        return;
      }
      for (let end = start + 1; end <= raw.length; end++) {
        acc.push(raw.slice(start, end).join(" "));
        walk(end, acc);
        acc.pop();
      }
    };
    walk(0, []);
    best.forEach((g) =>
      out.push({ text: g, size: Math.round(size(g, best.length)), claim: ci }));
  });
  return out;
};

/** A token the beat exists to deliver — a number, a measurement, a date. */
const isPayload = (tok: string) => /\d/.test(tok);

export const TypeCard: React.FC<{ scene: TypeCardProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const theme = useTheme();

  const bg = scene.bg ?? theme.black;
  const at = scene.kinetic?.at ?? 0.15;
  const text = scene.kinetic?.text ?? "";
  const words = text.split(/\s+/).filter(Boolean);

  // The band this card may fill: the safe rect, less the credit lane.
  // A CENTRED block is bounded by the tighter of the two side margins, not by
  // the asymmetric safe rect. SAFE_RECT.x1 = 0.85 exists to clear Instagram's
  // action rail, which sits at x 0.881-1.0 AND y 0.51-0.84; a card's type is
  // centred, so using (x1 - x0) shrank it from both sides to dodge a rail that
  // only ever threatens one. Bounded by x0 mirrored instead: 0.06 either side.
  const boxW = width * (1 - 2 * SAFE_RECT.x0) * 0.99;
  const boxH = height * (BANDS.caption[1] - SAFE_RECT.y0) * 0.82;
  const lines = layout(text, boxW, boxH);

  // Dark card or light card decides ink, and which accent variant survives it.
  const light = typeof bg === "string" && /^#(f|e)/i.test(bg.trim());
  const ink = scene.fg ?? (light ? theme.ink : theme.inkOnDark);
  const accent = light ? theme.accentInk : theme.accentOnDark;

  // A rule that draws under the block, frame-driven so it renders.
  const rule = easeOut((t - at - 0.22) / 0.5);

  return (
    <AbsoluteFill style={{ background: bg }}>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          padding: `0 ${Math.round(width * SAFE_RECT.x0)}px`,
          // Centre in the BAND, not in what is left over after the bottom
          // inset. With only paddingBottom the block centred at y 0.37 and hung
          // high; padding both ends puts it at 0.43, the middle of the band the
          // layout contract actually allocates to a card.
          paddingTop: height * SAFE_RECT.y0,
          paddingBottom: height * (1 - BANDS.caption[1]),
        }}
      >
        <div
          style={{
            fontFamily: DISPLAY,
            fontWeight: 700,
            color: ink,
            textAlign: "center",
            maxWidth: boxW,
          }}
        >
          {lines.map((ln, li) => {
            const heavy = isPayload(ln.text);
            // waterfall-entry.md: binary opacity, travel by WEIGHT,
            // power4.out, and gaps that SHRINK across the cascade — the
            // payload line anchors and the qualifier follows tighter.
            // Each line lands on ITS OWN phrase when the sheet says so;
            // otherwise the lines cascade. See Kinetic.ats in types.ts.
            const start = scene.kinetic?.ats?.[ln.claim] ?? at + li * 0.11;
            const p = easeOut((t - start) / (heavy ? 0.19 : 0.14));
            if (t < start) return null;
            return (
              <div
                key={li}
                style={{
                  fontSize: ln.size,
                  // SEPARATE THE CLAIMS, not the lines. Lines inside one claim
                  // are a wrapped phrase and belong tight together; a new claim
                  // is a new sentence. Without this the merged card read as one
                  // run-on — "nothing confirmed September 9" — even though the
                  // two halves land 2.1s apart in the audio.
                  marginTop:
                    li > 0 && ln.claim !== lines[li - 1].claim
                      ? Math.round(ln.size * 0.42)
                      : 0,
                  lineHeight: 1.06,
                  letterSpacing: "-0.03em",
                  color: heavy ? accent : ink,
                  fontVariantNumeric: heavy ? "tabular-nums" : undefined,
                  whiteSpace: "nowrap",
                  transform: `translateY(${(1 - p) * (heavy ? 72 : 40)}px)`,
                }}
              >
                {ln.text}
              </div>
            );
          })}
          <div
            style={{
              height: Math.max(5, Math.round(lines[0].size * 0.05)),
              width: `${Math.round(rule * 62)}%`,
              margin: `${Math.round(lines[0].size * 0.26)}px auto 0`,
              background: accent,
              borderRadius: 999,
            }}
          />
        </div>
      </AbsoluteFill>
      {/* Five of these shipped with a declared credit and nothing on screen. */}
      {scene.credit && <Credit text={scene.credit} onMedia={!light} plate={false} />}
    </AbsoluteFill>
  );
};
