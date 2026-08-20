import type { ChartSceneProps } from "./components/ChartScene";
import type { PixelMascotProps } from "./components/PixelMascot";
import type { ParticleBurstProps } from "./components/ParticleBurst";
import type { DeviceFrameProps } from "./components/DeviceFrame";
import type { TerminalSceneProps } from "./components/TerminalScene";
import type { AnnotateZoomProps } from "./components/AnnotateZoom";
import type { ScreenStepProps } from "./components/ScreenStep";
import type { BrandHookProps } from "./components/BrandHook";
import type { LogoAssembleProps } from "./components/LogoAssemble";
import type { ToolStackProps } from "./components/ToolStack";
import type { SourceReadProps } from "./components/SourceRead";
import type { PriceLadderProps } from "./components/PriceLadder";

export type KineticStyle = "serif" | "caps" | "chip";

export interface Kinetic {
  text: string;
  style: KineticStyle;
  /** seconds into the scene when the type lands */
  at?: number;
  /** vertical anchor 0..1 of frame height (default 0.28) */
  y?: number;
  /** dark radial scrim behind the type (default true) — set false for ink
   *  type on light cards, where the scrim reads as a grey smear */
  scrim?: boolean;
  /**
   * When a card carries MORE THAN ONE CLAIM: the second when each `\n`-separated
   * line lands, measured from the scene start.
   *
   * Added 2026-08-18, merging two thin typecards into one. Two cards each
   * holding a single phrase were 76% and 74% empty frame; one card holding both
   * fills properly — but only if each line arrives when ITS OWN phrase is
   * spoken. A merged card with one entrance would put "September 9" on screen
   * 1.4s before the creator says it, which is Rule 3 broken in the name of
   * fixing dead space.
   *
   * Derived from vo.json word onsets, never typed by feel. Falls back to the
   * per-line stagger when absent.
   */
  ats?: number[];
}

export interface HighlightBox {
  /** seconds into the scene */
  at: number;
  /** rect in source-image pixel coords */
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface SfxCue {
  /** file under public/, e.g. "sfx/whoosh.wav" */
  src: string;
  /** seconds into the scene */
  at?: number;
  /** 0..1 */
  vol?: number;
}

/** Editorial serif headline that builds line-by-line (reference "Finally Revealed" hook). */
export interface Headline {
  lines: {
    text: string;
    /** label = small upright serif; headline = large bold serif; subtitle = italic serif */
    kind: "label" | "headline" | "subtitle";
    /** seconds into the scene when this line lands */
    at: number;
    /** render this line in the brand accent colour */
    accent?: boolean;
  }[];
  /** vertical anchor 0..1 (default 0.5 = seam) */
  y?: number;
  align?: "left" | "center";
  /** force text colour theme when over dark/light footage (default light) */
  theme?: "light" | "dark";
  /**
   * Extra seconds within the scene at which the block is STRUCK — a visual
   * transient matching a sound effect that lands away from a line's own `at`.
   *
   * Every line is already struck when it lands, so this is only for a cue with
   * no text event of its own. Written by tools/sync_impacts.py from the scene's
   * `sfx` cues, never typed: the whole point is that the hit you see and the
   * hit you hear are the same instant. See src/theme/impact.ts.
   */
  impacts?: number[];
}

interface SceneBase {
  durationSec: number;
  /**
   * Which product this beat is about, in a `comparison` reel.
   * "a" / "b" = the two sides as declared in the sheet's `sides`;
   * "both" = a scene that shows them together (comparesplit, hcompare).
   * Gate G26 uses this to prove the reel is BALANCED — a comparison that
   * gives one side 80% of the screen time is an ad, not a comparison.
   */
  side?: "a" | "b" | "both";
  /** Optional provenance pointers copied from the job asset manifest. */
  claimId?: string;
  assetId?: string;
  sourceUrl?: string;
  sfx?: SfxCue[];
  /** px from frame bottom for the caption chip during this scene (default 400) */
  captionBottom?: number;
  /** editorial serif headline overlay (any scene type) */
  headline?: Headline;
  /**
   * Hide the karaoke caption chips during this scene. Defaults to TRUE for
   * typecard/wordcascade and any scene carrying a kinetic overlay (one text
   * system at a time); set false explicitly to force chips back on.
   */
  hideCaptions?: boolean;
  /** caption text theme while this scene is active: light = white (over
   *  footage/facecam), dark = ink (over cream/light card fields). */
  captionTheme?: "light" | "dark";
  /** deterministic confetti/spark burst overlaid on this scene */
  burst?: ParticleBurstProps;
  /** animated pixel-art mascot sprites overlaid on this scene */
  sprites?: PixelMascotProps[];
}

export type Scene =
  | (SceneBase & {
      type: "footage";
      src: string;
      /** trim start inside the source clip, seconds */
      from?: number;
      credit?: string;
      kinetic?: Kinetic;
      /** slow push, default "in"; "none" disables */
      zoomDir?: "in" | "out" | "none";
      /** horizontal focus 0..1 when source is wider than canvas (default 0.5) */
      focusX?: number;
      /** vertical focus 0..1 when source is taller than canvas (default 0.5) */
      focusY?: number;
      /**
       * ADDED 2026-08-20. Locked-off scale multiplier, default 1 — the base the
       * `zoomDir` push runs from, so `zoom: 1.4` + `zoomDir: "none"` holds a
       * tight frame dead still. Added for camera-snap cuts: consecutive scenes
       * on ONE avatar clip, each a different `focusX`/`focusY`/`zoom`, cutting
       * on vo.json word onsets. Before this, framing could only move sideways
       * and only at a fixed 1.1x push.
       *
       * Below 1 the scaled layer no longer covers the canvas and the black
       * backdrop shows through — that is G48, and it blocks.
       */
      zoom?: number;
      /** Nick-style info-card overlaid on the footage: bold heading + body */
      infocard?: { heading: string; body: string; at?: number };
    })
  | (SceneBase & {
      type: "receipt";
      src: string;
      backdrop?: "cream" | "black";
      srcWidth: number;
      srcHeight: number;
      highlights?: HighlightBox[];
      credit?: string;
    })
  | (SceneBase & {
      type: "typecard";
      kinetic: Kinetic;
      bg?: string;
      fg?: string;
      /**
       * ADDED 2026-08-18. Five typecards in iphone-fold-ultra already carried
       * `"credit": "MacRumors"`; the variant never declared the field, so the
       * value sat in the beat sheet, passed G14 (which reads the sheet), and
       * reached no frame. Excess properties survive JSON.parse silently — the
       * contract has to name a field for anything to be able to miss it.
       */
      credit?: string;
    })
  | (SceneBase & {
      type: "wordcascade";
      /** words/phrases appearing sequentially, each at `at` seconds */
      words: {
        text: string;
        style: "serif" | "caps" | "pixel" | "gradient";
        at: number;
        /** relative size multiplier (default 1) */
        size?: number;
        /** render in the accent colour — use on the punchline line only */
        accent?: boolean;
      }[];
      bg?: "cream" | "black" | "white";
      /** show the subject-brand mascot image above the stack (e.g. Clawd) */
      mascot?: string;
      /** bottom half shows facecam instead of full-frame cascade */
      bottomSrc?: string;
      bottomFrom?: number;
      bottomFocusX?: number;
    })
  | (SceneBase & {
      type: "desktopmockup";
      bg?: "cream" | "black";
      files: { name: string; kind: "pdf" | "md" | "folder" | "zip" }[];
      /** which file (index) gets the blue "selected" highlight */
      selected?: number;
    })
  | (SceneBase & {
      type: "uidialog";
      app?: string;
      title: string;
      body?: string;
      field?: { label: string; value: string };
      select?: { label: string; value: string };
      primary?: string;
      cancel?: string;
    })
  | (SceneBase & {
      /**
       * Rendered iOS Settings pane — for how-to and troubleshooting reels.
       * Built rather than screen-recorded, for the same reason `terminal`
       * replaced terminal recordings and `chart` replaced leaderboard
       * screenshots: reusable, animatable, and pin-sharp at 1080x1920.
       * A real device recording still wins when the pane is one we cannot
       * faithfully rebuild — use `deviceframe` for those.
       */
      type: "settingspane";
      /** nav bar title, e.g. "Cellular" */
      title: string;
      /** back-chevron label, e.g. "Settings" */
      back?: string;
      /** iOS light or dark appearance */
      appearance?: "light" | "dark";
      /** grouped sections, like real Settings */
      groups: {
        header?: string;
        footer?: string;
        rows: {
          label: string;
          /** right-hand detail text, e.g. "On" or "Automatic" */
          value?: string;
          /** SF-ish icon tile colour; omit for no tile */
          tint?: string;
          /** single glyph drawn in the tile */
          glyph?: string;
          /** renders a switch instead of a value/chevron */
          toggle?: boolean;
          /** starting toggle state */
          on?: boolean;
          /** seconds into the scene when the toggle flips */
          flipAt?: number;
          chevron?: boolean;
        }[];
      }[];
      /** "group.row" coordinates of the row to spotlight, e.g. "0.2" */
      focus?: string;
      /** seconds into the scene when the spotlight lands (default 0.5) */
      focusAt?: number;
    })
  | (SceneBase & {
      type: "statcard";
      title: string;
      titleRight?: string;
      rows: { label: string; value: string; pct: number; color?: string }[];
      bg?: "cream" | "black";
      footnote?: string;
    })
  | (SceneBase & {
      type: "logobeat";
      /** image in public/ OR text mark */
      src?: string;
      text?: string;
      textColor?: string;
      bg?: string;
      label?: string;
      /** "starburst" draws an animated spinning pixel star + a drawing beam */
      mark?: "starburst";
      markColor?: string;
      /** render the text in the pixel font (Press Start 2P) */
      pixel?: boolean;
    })
  | (SceneBase & {
      type: "floatcard";
      src: string;
      from?: number;
      /** media aspect ratio w/h — card adapts (default 16/9) */
      aspect?: number;
      bg?: "black" | "cream" | "gradient";
      credit?: string;
      /** MG text overlaid above the card (e.g. "TOP-SELLING · INDIA") */
      kinetic?: Kinetic;
    })
  | (SceneBase & {
      type: "promptcard";
      app?: string;
      headline?: string;
      /** the prompt text that types in */
      promptText?: string;
      /** substrings highlighted (cyan) as spoken */
      highlights?: string[];
      /** stacked lines that appear one-by-one (e.g. NO PRODUCT / NO PHOTOSHOOT) */
      lines?: string[];
      /** show N shimmer loader cards below (design generation) */
      loaders?: number;
      subtext?: string;
      bg?: "gradient" | "black" | "cream";
    })
  | (SceneBase & {
      type: "categorygrid";
      cards: { label: string; sub?: string }[];
      headline?: string;
      /** which card gets selected; omit to just show the grid */
      selectIndex?: number;
      /** seconds into the scene when selection happens */
      selectAt?: number;
      bg?: "gradient" | "black" | "cream";
    })
  | (SceneBase & {
      type: "carousel";
      items: { src: string; label?: string }[];
      headline?: string;
      /** index that is the winner (held at end with SELECTED ✓) */
      selectIndex: number;
      bg?: "gradient" | "black" | "cream";
    })
  | (SceneBase & {
      type: "checklist";
      headline?: string;
      /**
       * done = confirmed yes (tick) · no = confirmed exclusion (cross) ·
       * q = genuinely unknown / unconfirmed (question mark).
       * USER FEEDBACK 2026-08-12: "?" appeared on an exclusion list because
       * "no" did not exist and "q" was the only non-tick state. Never use "q"
       * to mean "excluded" — a question mark tells the viewer we do not know,
       * which is a different (and weaker) claim.
       */
      rows: { label: string; state: "done" | "no" | "q" }[];
      bg?: "gradient" | "black" | "cream";
      /** seconds between row entrances (default 0.55) */
      stagger?: number;
      /** smaller rows/icons so long lists (8-10 rows) fit under the headline */
      compact?: boolean;
    })
  | (SceneBase & {
      type: "specsheet";
      title: string;
      rows: { label: string; value?: string; values?: string[]; accent?: boolean }[];
      footnote?: string;
      /** small serif kicker above the title */
      kicker?: string;
      /** column headers over the value columns (e.g. ["QUALITY /10","COST /run"]) */
      columns?: string[];
      /** film footage playing behind the sheet (darkened); default solid dark */
      bgSrc?: string;
      bgFrom?: number;
    })
  | (SceneBase & {
      type: "designreveal";
      /** 5 full-screen design stills, shown sequentially with number badges */
      items: { src: string }[];
      /** index of the winner (held longer, cyan border, SELECTED ✓) */
      selectIndex: number;
      bg?: "gradient" | "black" | "cream";
    })
  | (SceneBase & {
      type: "hcompare";
      /** top section (original design) */
      topSrc: string;
      /** bottom section (AI ad frame) */
      bottomSrc: string;
      topLabel?: string;
      bottomLabel?: string;
      /** top section height fraction (default 0.42) */
      topFrac?: number;
      /** banner messages shown sequentially */
      messages: string[];
    })
  | (SceneBase & {
      type: "endquestion";
      /** ad freeze background */
      src: string;
      question: string;
      bg?: "gradient" | "black" | "cream";
    })
  | (SceneBase & {
      type: "xpost";
      /** display name + @handle (real, credited) */
      name: string;
      handle: string;
      /** post text; wrap **word** to accent it */
      text: string;
      /** optional build media (video/image) shown under the text */
      media?: string;
      mediaFrom?: number;
      /** big stat pinned bottom-left (e.g. "$0.87", "27 min", "2 prompts") */
      stat?: string;
      /** footage playing behind the card, darkened */
      bgSrc?: string;
      bgFrom?: number;
      verified?: boolean;
    })
  | (SceneBase & {
      type: "comparesplit";
      leftSrc: string;
      rightSrc: string;
      leftLabel?: string;
      rightLabel?: string;
      /** first banner (e.g. DESIGN ACCURACY ✓) */
      topText?: string;
      /** swaps to this mid-scene (e.g. BASIC PROMPT → BASIC CONCEPT) */
      midText?: string;
      /** final held message (e.g. BETTER DIRECTION → BETTER OUTPUT) */
      finalText?: string;
      /** optional closing question */
      question?: string;
    })
  | (SceneBase & {
      type: "timeline";
      items: {
        date: string;
        name: string;
        sub?: string;
        accent?: string;
        at: number;
        minor?: boolean;
      }[];
      title?: string;
      kicker?: string;
      bgSrc?: string;
      bgFrom?: number;
      topY?: number;
      /**
       * Attribution for the reporting this timeline is built from.
       *
       * ADDED 2026-08-18, the second field found declared-but-undeclared in one
       * day (see `typecard.credit`). airpods-camera and iphone18-split both set
       * it — "Source: Mark Gurman, Bloomberg" and "MacRumors · Aug 12, 2026" —
       * and both shipped with it drawn nowhere, because the variant did not
       * name the field and TypeScript cannot check a property that does not
       * exist in the contract.
       */
      footnote?: string;
    })
  | (SceneBase & { type: "chart" } & ChartSceneProps)
  | (SceneBase & { type: "deviceframe" } & DeviceFrameProps)
  | (SceneBase & { type: "terminal" } & TerminalSceneProps)
  | (SceneBase & { type: "annotatezoom" } & AnnotateZoomProps)
  // a how-to step: a screen recording, zoomed, with the control marked
  | (SceneBase & { type: "screenstep" } & ScreenStepProps)
  | (SceneBase & { type: "brandhook" } & BrandHookProps)
  | (SceneBase & { type: "logoassemble" } & LogoAssembleProps)
  | (SceneBase & { type: "toolstack" } & ToolStackProps)
  | (SceneBase & { type: "sourceread" } & SourceReadProps)
  | (SceneBase & { type: "osshook"; src: string; from?: number; focusX?: number })
  | (SceneBase & {
      type: "notifstack";
      src: string;
      from?: number;
      focusX?: number;
      /** seconds into scene when the red strike + wallet-drain phase begins */
      strikeAt?: number;
    })
  | (SceneBase & { type: "strikeswap" })
  | (SceneBase & { type: "priceladder" } & PriceLadderProps)
  | (SceneBase & {
      type: "searchspotlight";
      src: string;
      from?: number;
      /** cyan outline rect in 1080x1920 canvas px */
      rect?: { x: number; y: number; w: number; h: number };
      rectAt?: number;
      label?: string;
      /** cursor-dot keyframes, seconds into scene / canvas px */
      cursor?: { t: number; x: number; y: number }[];
      /** FREE / OPEN SOURCE / NO MONTHLY FEE tick-labels */
      freeLabels?: { text: string; at: number }[];
    })
  | (SceneBase & {
      type: "stackwindows";
      shots: { src: string; from: number; label: string }[];
      title1: string;
      title2: string;
    })
  | (SceneBase & { type: "problemsolved" })
  | (SceneBase & {
      type: "walletattack";
      src: string;
      from?: number;
      focusX?: number;
      /** seconds into scene when notifications jump the wallet */
      jumpAt?: number;
    })
  | (SceneBase & { type: "forkcustomize" })
  | (SceneBase & { type: "selfhost" })
  | (SceneBase & {
      type: "checkoutblock";
      src: string;
      from?: number;
      focusX?: number;
      /** seconds into scene when the cursor freezes on the button */
      freezeAt?: number;
    })
  | (SceneBase & {
      type: "commentcta";
      src: string;
      from?: number;
      focusX?: number;
      typeAt?: number;
      growAt?: number;
      dropAt?: number;
    })
  | (SceneBase & {
      type: "split";
      /** top half */
      topSrc: string;
      topFrom?: number;
      topFocusX?: number;
      /** bottom half (usually facecam) */
      bottomSrc: string;
      bottomFrom?: number;
      bottomFocusX?: number;
      kinetic?: Kinetic;
      credit?: string;
    });

export interface CaptionWord {
  /** absolute seconds in the reel */
  start: number;
  end: number;
  text: string;
  /** per-word reveal times for display-style captions (absolute seconds) */
  words?: { t: number; text: string }[];
}

export interface MusicBed {
  src: string;
  /** trim into the track, seconds */
  from?: number;
  /** volume automation points (linear interp between them), t = reel seconds */
  points: { t: number; vol: number }[];
}

export interface BeatSheet {
  id: string;
  fps: number;
  width: number;
  height: number;
  /** active style pack — drives theme tokens for every scene (default
   * "editorial"). Legacy creator ids ("varun"/"varun-mayya"/"nick"/
   * "nick-saraev") still resolve via STYLE_ALIASES in theme/tokens.ts. */
  style?: "editorial" | "utility" | "varun" | "varun-mayya" | "nick" | "nick-saraev";
  /** optional VO track in public/ */
  audio?: string;
  /** optional ducked music bed */
  music?: MusicBed;
  /** "word-reveal" is the production caption treatment (per-word reveal,
   * emphasis list drives the accent keyword). "nick-display" is its pre-
   * 2026-08-16 name, still accepted. chip-* are legacy fallbacks. */
  captionStyle?:
    | "word-reveal"
    | "ink-circle"
    | "nick-display"
    | "sans"
    | "mono"
    | "chip-small"
    | "chip-lg";
  /** Run past the format's measured runtime band. Requires
   * `allowLongReason` (G02). Capped by RUNTIME_CEILING = 120s in
   * tools/reel_gates.py — allowLong cannot pass that wall. Was enforced by
   * the gate but never declared here until 2026-08-16. */
  allowLong?: boolean;
  /** One line arguing why this topic needs the extra runtime. G02 rejects
   * `allowLong` without it — the flag is an argument, not a switch. */
  allowLongReason?: string;
  /**
   * Draw NO source credits on screen for this reel (user, 2026-08-19: "if I
   * don't want to credit any source in a particular video, our system won't
   * credit any source for that video only").
   *
   * The REASON IS PART OF THE FLAG, not a sibling field, so it cannot be set
   * without one. Same shape as `allowLong` + `allowLongReason` and the capture
   * tool's `--desktop-reason`: this repo asks for an argument, not a switch,
   * wherever a decision removes something a rule normally requires.
   *
   * `credit` STAYS on every scene. The manifest, the beat sheet and G14 are
   * untouched — the reel still records where every asset came from, and the
   * packaging can still list sources. Only the on-screen label is suppressed.
   *
   * This does not change what a source's licence requires. Where footage is
   * borrowed under terms that ask for attribution, turning the label off does
   * not satisfy those terms; it just moves the obligation somewhere the
   * renderer cannot see.
   */
  noCredits?: { reason: string };
  /** substrings rendered accented + larger inside caption chips */
  emphasis?: string[];
  scenes: Scene[];
  captions: CaptionWord[];
}
