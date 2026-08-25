import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { FootageScene } from "./components/FootageScene";
import { ReceiptScene } from "./components/ReceiptScene";
import { SourceRead } from "./components/SourceRead";
import { TypeCard } from "./components/TypeCard";
import { SplitScene } from "./components/SplitScene";
import { WordCascade } from "./components/WordCascade";
import { StatCard } from "./components/StatCard";
import { DesktopMockup } from "./components/DesktopMockup";
import { UIDialog } from "./components/UIDialog";
import { SettingsPane } from "./components/SettingsPane";
import { LogoBeat } from "./components/LogoBeat";
import { FloatingCard } from "./components/FloatingCard";
import { PromptCard } from "./components/PromptCard";
import { CategoryGrid } from "./components/CategoryGrid";
import { Carousel } from "./components/Carousel";
import { Checklist } from "./components/Checklist";
import { CompareSplit } from "./components/CompareSplit";
import { DesignReveal } from "./components/DesignReveal";
import { HCompare } from "./components/HCompare";
import { EndQuestion } from "./components/EndQuestion";
import { SpecSheet } from "./components/SpecSheet";
import { XPost } from "./components/XPost";
import { HeadlineBuild } from "./components/HeadlineBuild";
import { TimelineCascade } from "./components/TimelineCascade";
import { ToolStack } from "./components/ToolStack";
import { CaptionChips } from "./components/CaptionChips";
import { ChartScene } from "./components/ChartScene";
import { PixelMascot } from "./components/PixelMascot";
import { ParticleBurst } from "./components/ParticleBurst";
import { DeviceFrame } from "./components/DeviceFrame";
import { TerminalScene } from "./components/TerminalScene";
import { AnnotateZoom } from "./components/AnnotateZoom";
import { ScreenStep } from "./components/ScreenStep";
import { PriceLadder } from "./components/PriceLadder";
import { BrandHook } from "./components/BrandHook";
import { LogoAssemble } from "./components/LogoAssemble";
import {
  OssHook,
  NotifStack,
  StrikeSwap,
  SearchSpotlight,
  StackWindows,
  ProblemSolved,
  WalletAttack,
  ForkCustomize,
  SelfHost,
  CheckoutBlock,
  CommentCta,
} from "./components/OssAlt";
import { ThemeProvider } from "./theme/tokens";
import { CreditPolicyProvider, firstUseByCredit } from "./components/Credit";
import { FontFaces } from "./theme/fonts";
import type { BeatSheet, Scene } from "./types";

const SceneSwitch: React.FC<{ scene: Scene }> = ({ scene }) => {
  switch (scene.type) {
    case "footage":
      return <FootageScene scene={scene} />;
    case "receipt":
      return <ReceiptScene scene={scene} />;
    case "sourceread":
      return <SourceRead scene={scene} />;
    case "typecard":
      return <TypeCard scene={scene} />;
    case "split":
      return <SplitScene scene={scene} />;
    case "wordcascade":
      return <WordCascade scene={scene} />;
    case "statcard":
      return <StatCard scene={scene} />;
    case "desktopmockup":
      return <DesktopMockup scene={scene} />;
    case "uidialog":
      return <UIDialog scene={scene} />;
    case "settingspane":
      return <SettingsPane scene={scene} />;
    case "logobeat":
      return <LogoBeat scene={scene} />;
    case "floatcard":
      return <FloatingCard scene={scene} />;
    case "promptcard":
      return <PromptCard scene={scene} />;
    case "categorygrid":
      return <CategoryGrid scene={scene} />;
    case "carousel":
      return <Carousel scene={scene} />;
    case "checklist":
      return <Checklist scene={scene} />;
    case "comparesplit":
      return <CompareSplit scene={scene} />;
    case "designreveal":
      return <DesignReveal scene={scene} />;
    case "hcompare":
      return <HCompare scene={scene} />;
    case "endquestion":
      return <EndQuestion scene={scene} />;
    case "specsheet":
      return <SpecSheet scene={scene} />;
    case "xpost":
      return <XPost scene={scene} />;
    case "timeline":
      return <TimelineCascade scene={scene as never} />;
    case "chart":
      return <ChartScene {...scene} />;
    case "deviceframe":
      return <DeviceFrame {...scene} />;
    case "terminal":
      return <TerminalScene {...scene} />;
    case "annotatezoom":
      return <AnnotateZoom {...scene} />;
    case "screenstep":
      return <ScreenStep scene={scene} />;
    case "brandhook":
      return <BrandHook {...scene} />;
    case "logoassemble":
      return <LogoAssemble {...scene} />;
    case "toolstack":
      return <ToolStack {...scene} />;
    case "osshook":
      return <OssHook scene={scene} />;
    case "notifstack":
      return <NotifStack scene={scene} />;
    case "strikeswap":
      return <StrikeSwap scene={scene} />;
    case "priceladder":
      return <PriceLadder scene={scene} />;
    case "searchspotlight":
      return <SearchSpotlight scene={scene} />;
    case "stackwindows":
      return <StackWindows scene={scene} />;
    case "problemsolved":
      return <ProblemSolved scene={scene} />;
    case "walletattack":
      return <WalletAttack scene={scene} />;
    case "forkcustomize":
      return <ForkCustomize scene={scene} />;
    case "selfhost":
      return <SelfHost scene={scene} />;
    case "checkoutblock":
      return <CheckoutBlock scene={scene} />;
    case "commentcta":
      return <CommentCta scene={scene} />;
    default: {
      const neverScene: never = scene;
      throw new Error(`Unsupported scene: ${JSON.stringify(neverScene)}`);
    }
  }
};

/** Quick punch-in on every cut so nothing ever feels static. */
const PunchIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, 6], [1.09, 1], {
    extrapolateRight: "clamp",
    easing: (t) => 1 - Math.pow(1 - t, 2),
  });
  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
};

export const Reel: React.FC<{ beats: BeatSheet }> = ({ beats }) => {
  const { fps } = useVideoConfig();
  // The single scene that draws each source's credit — see Credit.tsx. The
  // beat sheet keeps `credit` on EVERY scene so provenance and G14 are intact;
  // only the drawing is deduplicated.
  const creditOwners = firstUseByCredit(
    beats.scenes as unknown as { credit?: string }[]);
  let cursor = 0;

  return (
    <ThemeProvider style={beats.style}>
    <AbsoluteFill style={{ background: "black" }}>
      {/* Declared HERE, not in Root: a font load in Root reaches every
          composition, which is what timed out renders in August. */}
      <FontFaces />
      {beats.audio && <Audio src={staticFile(beats.audio)} />}
      {beats.music && (
        <Audio
          src={staticFile(beats.music.src)}
          startFrom={Math.round((beats.music.from ?? 0) * fps)}
          volume={(f) => {
            const t = f / fps;
            const pts = beats.music!.points;
            if (t <= pts[0].t) return pts[0].vol;
            for (let i = 0; i < pts.length - 1; i++) {
              if (t >= pts[i].t && t < pts[i + 1].t) {
                const k = (t - pts[i].t) / (pts[i + 1].t - pts[i].t);
                return pts[i].vol + k * (pts[i + 1].vol - pts[i].vol);
              }
            }
            return pts[pts.length - 1].vol;
          }}
        />
      )}
      {beats.scenes.map((scene, i) => {
        const from = Math.round(cursor * fps);
        const dur = Math.round(scene.durationSec * fps);
        cursor += scene.durationSec;
        return (
          <Sequence
            key={i}
            from={from}
            durationInFrames={dur}
            premountFor={fps}
          >
            <CreditPolicyProvider
              firstFor={creditOwners}
              sceneIndex={i}
              suppressed={Boolean(beats.noCredits)}
            >
              <PunchIn>
                <SceneSwitch scene={scene} />
              </PunchIn>
            </CreditPolicyProvider>
            {scene.headline &&
              typeof scene.headline === "object" &&
              "lines" in scene.headline &&
              Array.isArray(scene.headline.lines) && (
                <HeadlineBuild spec={scene.headline} />
              )}
            {(scene.sprites ?? []).map((sp, j) => (
              <PixelMascot key={`sprite-${j}`} {...sp} />
            ))}
            {scene.burst && <ParticleBurst {...scene.burst} />}
            {(scene.sfx ?? []).map((cue, j) => (
              <Sequence
                key={`sfx-${j}`}
                from={Math.round((cue.at ?? 0) * fps)}
                durationInFrames={dur - Math.round((cue.at ?? 0) * fps)}
                premountFor={fps}
              >
                <Audio src={staticFile(cue.src)} volume={cue.vol ?? 0.4} />
              </Sequence>
            ))}
          </Sequence>
        );
      })}
      <CaptionChips
        captions={beats.captions}
        mode={beats.captionStyle}
        emphasis={beats.emphasis}
        positions={(() => {
          const out: { start: number; end: number; bottom: number }[] = [];
          let c = 0;
          for (const s of beats.scenes) {
            if (s.captionBottom !== undefined) {
              out.push({ start: c, end: c + s.durationSec, bottom: s.captionBottom });
            }
            c += s.durationSec;
          }
          return out;
        })()}
        darkRanges={(() => {
          const out: { start: number; end: number }[] = [];
          let c = 0;
          for (const s of beats.scenes) {
            if (s.captionTheme === "dark") {
              out.push({ start: c, end: c + s.durationSec });
            }
            c += s.durationSec;
          }
          return out;
        })()}
        hidden={(() => {
          // ONE TEXT SYSTEM AT A TIME: chips auto-hide while a display-type
          // scene (typecard/wordcascade), kinetic overlay, or a headline that
          // speaks the same words as the VO is on screen. Headlines with
          // DIFFERENT words (titles over receipts) keep their chips.
          const words = (t: string) =>
            t
              .toLowerCase()
              .replace(/[^a-z0-9\s]/g, "")
              .split(/\s+/)
              .filter((w) => w.length >= 3);
          const out: { start: number; end: number }[] = [];
          let c = 0;
          for (const s of beats.scenes) {
            let autoHide =
              s.type === "typecard" ||
              s.type === "wordcascade" ||
              ("kinetic" in s && s.kinetic !== undefined);
            // BIG TYPE THE SCENE DRAWS ITSELF — headline lines, and a
            // commentcta's own keyword/question. The CTA case was missing:
            // the keyword variant paints "COMMENT CLAUDE" at 200px while the
            // caption printed "Comment Claude I'll" underneath it, the same
            // words twice (user, 2026-08-25). Any scene that spells the
            // spoken line out in display type suppresses the caption.
            const ownText: string[] = [];
            if (
              s.headline &&
              typeof s.headline === "object" &&
              "lines" in s.headline &&
              Array.isArray(s.headline.lines)
            ) {
              ownText.push(...s.headline.lines.map((l) => l.text));
            }
            if (s.type === "commentcta") {
              // The KEYWORD variant keeps the reel's caption rhythm to the
              // last frame (reference fR8AkVkuM18) — so only the chunk that
              // would print the keyword twice is dropped, not the whole beat.
              // The gate variant draws a question card AND a word card AND a
              // notification, so it still suppresses wholesale.
              if (s.variant === "keyword") {
                const kw = words(s.keyword ?? "OPEN");
                for (const cap of beats.captions) {
                  if (
                    cap.start < c + s.durationSec &&
                    cap.end > c &&
                    words(cap.text).some((w) => kw.includes(w))
                  ) {
                    out.push({ start: cap.start, end: cap.end });
                  }
                }
                c += s.durationSec;
                continue;
              }
              ownText.push(s.keyword ?? "OPEN", s.question ?? "");
            }
            if (!autoHide && ownText.length) {
              const hw = new Set(ownText.flatMap(words));
              const voWords = beats.captions
                .filter((w) => w.start < c + s.durationSec && w.end > c)
                .flatMap((w) => words(w.text));
              const overlap = voWords.filter((w) => hw.has(w)).length;
              autoHide = overlap >= 2;
            }
            if (s.hideCaptions ?? autoHide) {
              out.push({ start: c, end: c + s.durationSec });
            }
            c += s.durationSec;
          }
          return out;
        })()}
      />
    </AbsoluteFill>
    </ThemeProvider>
  );
};

export const totalDurationInFrames = (beats: BeatSheet): number =>
  Math.round(beats.scenes.reduce((s, sc) => s + sc.durationSec, 0) * beats.fps);
