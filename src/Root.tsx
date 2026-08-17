import React from "react";
import { Composition } from "remotion";
import { Reel, totalDurationInFrames } from "./Reel";
import { beatSheets } from "./generatedBeatSheets";
import { InstaCTA } from "./InstaCTA";
import { Thumbnail } from "./Thumbnail";

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
    </>
  );
};
