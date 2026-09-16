import React from "react";
import { Composition } from "remotion";
import { Reel, totalDurationInFrames } from "./Reel";
import { beatSheets } from "./generatedBeatSheets";
import { InstaCTA } from "./InstaCTA";
import { Thumbnail } from "./Thumbnail";
import type { BeatSheet } from "./types";
import labQualcommStage from "./lab/qualcomm-stage.json";
import { Stage } from "./components/Stage";
import { Slide, type SlideProps } from "./components/Slide";
import { FontFaces } from "./theme/fonts";

// a single slide as a still: cover frames in the reel's own look (2026-09-16)
const SlideStill: React.FC<{ scene: SlideProps }> = ({ scene }) => (
  <>
    <FontFaces />
    <Slide scene={scene} />
  </>
);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* LAB 2026-09-16: the two moves borrowed from the carousel playbook's slide
          videos — a card that lands as a placeholder and fills, and a paid/free
          swap with an arrowed connector. Numbers are the carousel's own. */}
      <Composition
        id="lab-stage-swap"
        component={Stage}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          scene: {
            set: "light" as const,
            layout: "full" as const,
            credit: "vendor pricing pages",
            elements: [
              { id: "paid", kind: "card" as const, x: 0.25, y: 0.40, w: 0.42,
                title: "Zapier", price: "$239.88", priceTone: "cost" as const,
                lines: ["per year, one seat"] },
              { id: "free", kind: "card" as const, x: 0.75, y: 0.40, w: 0.42, tone: "accent" as const,
                title: "n8n", price: "$0", priceTone: "free" as const, lines: ["self-hosted"] },
              { id: "note", kind: "text" as const, x: 0.5, y: 0.72, w: 0.82, size: 0.72,
                text: "Same jobs, your own server" },
            ],
            moves: [
              { do: "arrive" as const, target: "paid", at: 0.0, dir: "left" as const },
              { do: "arrive" as const, target: "free", at: 0.25, dir: "right" as const },
              { do: "fill" as const, target: "paid", at: 0.8 },
              { do: "connect" as const, from: "paid", to: "free", at: 1.2, arrow: true, weight: 1.5, repeat: 2 },
              { do: "fill" as const, target: "free", at: 1.6 },
              { do: "strike" as const, target: "paid", at: 2.6 },
              { do: "arrive" as const, target: "note", at: 3.1, dir: "up" as const },
            ],
          },
        }}
      />
      {/* LAB 2026-09-15: qualcomm-chip-hike with three lines rebuilt as `stage`
          scenes — the test of the stage grammar. Not a publishable reel. */}
      <Composition
        id="lab-qualcomm-stage"
        component={Reel}
        durationInFrames={totalDurationInFrames(labQualcommStage as unknown as BeatSheet)}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ beats: labQualcommStage as unknown as BeatSheet }}
      />
      <Composition
        id="insta-cta"
        component={InstaCTA}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="insta-cta-preview"
        component={InstaCTA}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ background: "#1b1b1d" }}
      />
      {/* Reel / Shorts cover — 1080x1920. Driven by tools/make_thumbnail.py.
          Read-critical content lives in the centre 1:1 crop (y 420-1500),
          because a profile grid centre-crops a 9:16 cover. */}
      <Composition
        id="thumbnail"
        component={Thumbnail}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          brand: "APPLE",
          line1: "TIM COOK'S",
          line2: "LAST KEYNOTE",
          format: "vertical" as const,
          style: "editorial",
        }}
      />
      <Composition
        id="thumbnail-wide"
        component={Thumbnail}
        durationInFrames={1}
        fps={30}
        width={1280}
        height={720}
        defaultProps={{
          brand: "APPLE",
          line1: "TIM COOK'S",
          line2: "LAST KEYNOTE",
          format: "wide" as const,
          style: "editorial",
        }}
      />
      {beatSheets.map((beats) => (
        <Composition
          key={beats.id}
          id={beats.id}
          component={Reel}
          durationInFrames={totalDurationInFrames(beats)}
          fps={beats.fps}
          width={beats.width}
          height={beats.height}
          defaultProps={{ beats }}
        />
      ))}
      <Composition
        id="slide-still"
        component={SlideStill}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ scene: { headline: "A [[slide]]", blocks: [] } as SlideProps }}
      />
    </>
  );
};
