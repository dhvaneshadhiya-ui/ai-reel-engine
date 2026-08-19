/**
 * THE COLOURS THAT WERE ALREADY SHARED, written down once.
 *
 * WHY (2026-08-18)
 * ----------------
 * tools/check_palette.py counted 133 off-palette colours across 19 components.
 * Sorting them by how many files use each one turned "133 stray hexes" into
 * something else entirely: **88 of the 133 uses are the SAME fifteen colours,
 * copy-pasted between components.** Not drift — a real shared palette that
 * nobody ever extracted, so every component re-declared it and each copy was
 * free to rot separately.
 *
 * That is the same finding as the type scale (41 sizes that were really 8) and
 * the motion system (16 stiffness values that were really 5). The fix is the
 * same: name what is already true, then point everything at the name.
 *
 * WHAT IS HERE AND WHAT IS NOT
 * ----------------------------
 * Here: colours used by three or more components with no per-scene meaning.
 * Not here: a chart's categorical series (StatCard's six-hue set is DATA —
 * each hue means "this series", and forcing them onto a brand palette would
 * make two series the same colour), and one-off scrims and shadows.
 *
 * Brand colour still belongs in tokens.ts, where accentInk / accentOnDark are
 * DERIVED from the style pack's single accent. Nothing here is a brand accent.
 */

/**
 * Card tints — the pastel grounds behind designed cards.
 *
 * Used by Carousel, CategoryGrid, Checklist, DesignReveal, PromptCard,
 * FloatingCard and WordCascade, each with its own copy. FloatingCard's copies
 * had already drifted a shade (#dfe8f5 vs #e6edf7, #f3e3d9 vs #f3e6dc,
 * #e8d9f0 vs #ecdcf1) — three near-identical pairs that no viewer could tell
 * apart and no author had chosen.
 */
export const TINT = {
  sand: "#f2ecdf",
  sky: "#e6edf7",
  clay: "#f3e6dc",
  lilac: "#ecdcf1",
} as const;

/**
 * The utility cyan.
 *
 * Nine components declare `const CYAN = "#0aa9c2"` — it is used more widely
 * than either style pack's accent, which makes it a de-facto brand colour that
 * lives in no brand file. Naming it here does not bless it; it makes it
 * visible, so the decision of whether a tools/tips reel should carry a second
 * accent can be made once instead of nine times.
 */
export const CYAN = "#0aa9c2";

/**
 * macOS window controls, for components that RECREATE a desktop window.
 *
 * Declared four times (BrandHook, DeviceFrame, PromptCard, TerminalScene). Not
 * ours and not up for redesign: a close button is #ff5f57 or it is not a macOS
 * window. Named once so the recreation stays consistent and so check_palette
 * has something to point at other than three anonymous hexes.
 */
export const MACOS_TRAFFIC = {
  close: "#ff5f57",
  minimise: "#febc2e",
  zoom: "#28c840",
} as const;

/**
 * The card gradient — the same string in five components, character for
 * character. It is built from three of the tints above, so it lives with them
 * and moves when they move.
 */
export const TINT_GRADIENT =
  `linear-gradient(160deg,${TINT.sky} 0%,${TINT.clay} 55%,${TINT.lilac} 100%)`;
