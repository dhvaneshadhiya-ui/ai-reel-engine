import React, { createContext, useContext } from "react";
import { DISPLAY } from "./type";

/**
 * Design tokens — the single source of truth for every scene's palette,
 * type, radii and shadows. RULE (FEEDBACK 2026-07-29): no per-scene palette
 * drift; every component pulls from the active style pack's tokens only.
 *
 * editorial = cream/black + amber accent, Space Grotesk display (default).
 *             Tech-news reporting: claim -> receipt -> demo -> take.
 * utility   = cream/black + terracotta accent, Space Grotesk + Press Start 2P.
 *             Tips/tools: designed artifacts, comment-gate CTA.
 *
 * Renamed 2026-08-16 from the creator names (varun / nick) to what the style
 * IS, matching the format vocabulary (news / top5 / comparison). Old ids are
 * still accepted -- see STYLE_ALIASES below.
 */
export type StyleId = "editorial" | "utility";

export interface Theme {
  id: StyleId;
  /** backgrounds */
  cream: string;
  black: string;
  white: string;
  /** brand accent (highlights, bars, annotations, emphasis) */
  accent: string;
  /** accent at low alpha for tints/fills */
  accentSoft: string;
  /**
   * The accent AS TEXT, in two grounds. Derived, never typed — see
   * accentPair() below for why a single `accent` could not do this job.
   */
  accentOnDark: string;
  accentInk: string;
  /** text on light bg / text on dark bg */
  ink: string;
  inkOnDark: string;
  /** muted/secondary text */
  muted: string;
  mutedOnDark: string;
  /** font stacks. `serif` is a legacy KEY NAME — the display voice is a
   *  grotesk since 2026-08-18; see theme/type.ts DISPLAY. */
  serif: string;
  sans: string;
  mono: string;
  pixel: string;
  radius: { card: number; chip: number };
  shadow: { card: string; cardOnDark: string };
}

/* -------------------------------------------------------------------------
 * ACCENT AS TEXT — derived, not typed.
 *
 * WHY THIS MATH EXISTS (2026-08-18, user: "I don't like this sort of orange")
 * --------------------------------------------------------------------------
 * The orange in the published reel was `const ACCENT = "#d97757"` sitting at
 * the top of HeadlineBuild.tsx — a colour from no palette, in a file whose
 * theme contract says "Components must use this — never hardcode colors". It
 * got there for a real reason: the editorial accent is #FFD84D, and amber text
 * on a bright frame is unreadable, so somebody reached for a colour that works
 * on light grounds and hardcoded it for BOTH grounds. One accent cannot be a
 * highlighter fill AND legible type on cream AND legible type on black.
 *
 * So a style declares ONE accent, and the two text variants are computed from
 * it against the WCAG contrast its ground demands. Change the accent and both
 * follow; there is no second hex to keep in sync, and no component may pick.
 *
 * Darkening happens in HSL lightness, holding hue and saturation. Scaling RGB
 * channels is the obvious way and it is wrong: it drags a saturated hue toward
 * grey, so the "accent" arrives as mud and looks like a rendering fault.
 * ---------------------------------------------------------------------------- */

const hexToRgb = (hex: string): [number, number, number] => {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
};

const toHex = (r: number, g: number, b: number): string =>
  "#" +
  [r, g, b]
    .map((v) => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, "0"))
    .join("");

/** WCAG relative luminance. */
const relLum = (r: number, g: number, b: number): number => {
  const f = (c: number) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};

const contrast = (a: [number, number, number], b: [number, number, number]) => {
  const la = relLum(...a);
  const lb = relLum(...b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
};

const rgbToHsl = (r: number, g: number, b: number): [number, number, number] => {
  const [R, G, B] = [r / 255, g / 255, b / 255];
  const max = Math.max(R, G, B);
  const min = Math.min(R, G, B);
  const l = (max + min) / 2;
  if (max === min) return [0, 0, l];
  const d = max - min;
  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  const h =
    max === R
      ? ((G - B) / d + (G < B ? 6 : 0))
      : max === G
      ? (B - R) / d + 2
      : (R - G) / d + 4;
  return [h * 60, s, l];
};

const hslToRgb = (h: number, s: number, l: number): [number, number, number] => {
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const hp = ((h % 360) + 360) % 360 / 60;
  const x = c * (1 - Math.abs((hp % 2) - 1));
  const [r1, g1, b1]: [number, number, number] =
    hp < 1 ? [c, x, 0]
    : hp < 2 ? [x, c, 0]
    : hp < 3 ? [0, c, x]
    : hp < 4 ? [0, x, c]
    : hp < 5 ? [x, 0, c]
    : [c, 0, x];
  const m = l - c / 2;
  return [(r1 + m) * 255, (g1 + m) * 255, (b1 + m) * 255];
};

/**
 * Walk HSL lightness toward the target until the accent clears `ratio` against
 * `ground`, then stop. Stopping AT the threshold matters: overshooting produces
 * a near-black "accent" that no longer reads as the brand colour at all.
 */
const shiftToContrast = (
  accent: string,
  ground: string,
  ratio: number,
  direction: "darker" | "lighter"
): string => {
  const g = hexToRgb(ground);
  const [h, s] = rgbToHsl(...hexToRgb(accent));
  let [, , l] = rgbToHsl(...hexToRgb(accent));
  const step = direction === "darker" ? -0.01 : 0.01;
  for (let i = 0; i < 100; i++) {
    const rgb = hslToRgb(h, s, l);
    if (contrast(rgb, g) >= ratio) return toHex(...rgb);
    l += step;
    if (l <= 0 || l >= 1) break;
  }
  return toHex(...hslToRgb(h, s, Math.max(0, Math.min(1, l))));
};

/**
 * 4.5:1 is WCAG AA for body text. Captions and headlines are large, so 3:1
 * would pass the letter of the standard — but a reel is watched at arm's length,
 * outdoors, on a phone at 40% brightness, over MOVING footage whose luminance
 * changes mid-word. AA is the floor here, not the target.
 */
const accentPair = (accent: string, cream: string, black: string) => ({
  accentOnDark: shiftToContrast(accent, black, 4.5, "lighter"),
  accentInk: shiftToContrast(accent, cream, 4.5, "darker"),
});

export const THEMES: Record<StyleId, Theme> = {
  editorial: {
    id: "editorial",
    cream: "#f4f0e6",
    black: "#0a0a0a",
    white: "#ffffff",
    accent: "#FFD84D",
    accentSoft: "rgba(255, 216, 77, 0.16)",
    ...accentPair("#FFD84D", "#f4f0e6", "#0a0a0a"),
    ink: "#141414",
    inkOnDark: "#f5f2ea",
    muted: "rgba(20,20,20,0.55)",
    mutedOnDark: "rgba(245,242,234,0.65)",
    serif: DISPLAY,
    sans: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
    mono: "'Menlo', 'SF Mono', 'Courier New', monospace",
    pixel: "'Press Start 2P', monospace",
    radius: { card: 24, chip: 14 },
    shadow: {
      card: "0 30px 80px rgba(0,0,0,0.25)",
      cardOnDark: "0 30px 80px rgba(0,0,0,0.8)",
    },
  },
  utility: {
    id: "utility",
    cream: "#efe9dc",
    black: "#0d0d0d",
    white: "#ffffff",
    accent: "#E0785A",
    accentSoft: "rgba(224, 120, 90, 0.16)",
    ...accentPair("#E0785A", "#efe9dc", "#0d0d0d"),
    ink: "#181512",
    inkOnDark: "#f2ede3",
    muted: "rgba(24,21,18,0.55)",
    mutedOnDark: "rgba(242,237,227,0.65)",
    serif: DISPLAY,
    sans: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
    mono: "'Menlo', 'SF Mono', 'Courier New', monospace",
    pixel: "'Press Start 2P', monospace",
    radius: { card: 22, chip: 11 },
    shadow: {
      card: "0 24px 64px rgba(0,0,0,0.22)",
      cardOnDark: "0 24px 64px rgba(0,0,0,0.75)",
    },
  },
};

const ThemeContext = createContext<Theme>(THEMES.editorial);

/**
 * Pre-2026-08-16 style ids, kept so the seven already-published beat sheets
 * keep rendering untouched. They were creator names; the canonical ids now
 * describe the style itself. Do NOT add new entries here — new styles get a
 * canonical name in THEMES.
 */
export const STYLE_ALIASES: Record<string, StyleId> = {
  varun: "editorial",
  "varun-mayya": "editorial",
  nick: "utility",
  "nick-saraev": "utility",
};

/**
 * Accept a canonical id, a legacy creator id, or nothing, and never hand
 * `undefined` to a component — on 2026-08-12 an unmapped id crashed EVERY
 * reel with "Cannot read properties of undefined (reading 'accent')".
 */
export const resolveStyle = (style?: string): StyleId => {
  if (!style) return "editorial";
  if (style in THEMES) return style as StyleId;
  if (style in STYLE_ALIASES) return STYLE_ALIASES[style];
  console.warn(
    `[theme] unknown style ${JSON.stringify(style)} — falling back to "editorial". ` +
      `Known: ${Object.keys(THEMES).join(", ")}; ` +
      `legacy: ${Object.keys(STYLE_ALIASES).join(", ")}`
  );
  return "editorial";
};

export const ThemeProvider: React.FC<{
  style?: string;
  children: React.ReactNode;
}> = ({ style, children }) =>
  React.createElement(
    ThemeContext.Provider,
    { value: THEMES[resolveStyle(style)] },
    children
  );

/** Active style-pack theme. Components must use this — never hardcode colors. */
export const useTheme = (): Theme => useContext(ThemeContext);
