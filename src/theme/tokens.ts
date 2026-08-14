import React, { createContext, useContext } from "react";

/**
 * Design tokens — the single source of truth for every scene's palette,
 * type, radii and shadows. RULE (FEEDBACK 2026-07-29): no per-scene palette
 * drift; every component pulls from the active style pack's tokens only.
 *
 * varun  = cream/black + yellow accent, Fraunces italic serif (default)
 * nick   = cream/black + terracotta accent, Fraunces serif + Press Start 2P
 */
export type StyleId = "varun" | "nick";

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
  varun: {
    id: "varun",
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
  nick: {
    id: "nick",
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

const ThemeContext = createContext<Theme>(THEMES.varun);

/**
 * Beat sheets name their style with the STYLE-PACK id ("varun-mayya"), which
 * is the canonical id in config.json and styles/. The theme table is keyed by
 * the shorter runtime id ("varun"). Accept either, and never hand `undefined`
 * to a component — on 2026-08-12 an unmapped id crashed EVERY reel with
 * "Cannot read properties of undefined (reading 'accent')".
 */
export const resolveStyle = (style?: string): StyleId => {
  if (!style) return "varun";
  if (style in THEMES) return style as StyleId;
  const head = style.split("-")[0];
  if (head in THEMES) return head as StyleId;
  console.warn(
    `[theme] unknown style ${JSON.stringify(style)} — falling back to "varun". ` +
      `Known: ${Object.keys(THEMES).join(", ")}`
  );
  return "varun";
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
