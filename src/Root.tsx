import React from "react";
import { Composition } from "remotion";
import { Reel, totalDurationInFrames } from "./Reel";
import { beatSheets } from "./generatedBeatSheets";
import { InstaCTA } from "./InstaCTA";

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
