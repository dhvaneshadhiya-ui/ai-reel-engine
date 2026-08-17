import type { ChartSceneProps } from "./components/ChartScene";
import type { PixelMascotProps } from "./components/PixelMascot";
import type { ParticleBurstProps } from "./components/ParticleBurst";
import type { DeviceFrameProps } from "./components/DeviceFrame";
import type { TerminalSceneProps } from "./components/TerminalScene";
import type { AnnotateZoomProps } from "./components/AnnotateZoom";
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
    })
  | (SceneBase & { type: "chart" } & ChartSceneProps)
  | (SceneBase & { type: "deviceframe" } & DeviceFrameProps)
  | (SceneBase & { type: "terminal" } & TerminalSceneProps)
  | (SceneBase & { type: "annotatezoom" } & AnnotateZoomProps)
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
  /** substrings rendered accented + larger inside caption chips */
  emphasis?: string[];
  scenes: Scene[];
  captions: CaptionWord[];
}
