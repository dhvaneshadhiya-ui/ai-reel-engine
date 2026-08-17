import React, { createContext, useContext } from "react";

/**
 * Design tokens — the single source of truth for every scene's palette,
 * type, radii and shadows. RULE (FEEDBACK 2026-07-29): no per-scene palette
 * drift; every component pulls from the active style pack's tokens only.
 *
 * editorial = cream/black + yellow accent, Fraunces italic serif (default).
 *             Tech-news reporting: claim -> receipt -> demo -> take.
 * utility   = cream/black + terracotta accent, Fraunces serif + Press Start 2P.
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
  /** text on light bg / text on dark bg */
  ink: string;
  inkOnDark: string;
  /** muted/secondary text */
  muted: string;
  mutedOnDark: string;
  /** font stacks */
  serif: string;
  sans: string;
  mono: string;
  pixel: string;
  radius: { card: number; chip: number };
  shadow: { card: string; cardOnDark: string };
}

export const THEMES: Record<StyleId, Theme> = {
  editorial: {
    id: "editorial",
    cream: "#f4f0e6",
    black: "#0a0a0a",
    white: "#ffffff",
    accent: "#FFD84D",
    accentSoft: "rgba(255, 216, 77, 0.16)",
    ink: "#141414",
    inkOnDark: "#f5f2ea",
    muted: "rgba(20,20,20,0.55)",
    mutedOnDark: "rgba(245,242,234,0.65)",
    serif: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
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
    ink: "#181512",
    inkOnDark: "#f2ede3",
    muted: "rgba(24,21,18,0.55)",
    mutedOnDark: "rgba(242,237,227,0.65)",
    serif: "-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif",
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
