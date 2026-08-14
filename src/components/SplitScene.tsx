import React from "react";
import { Credit } from "./Credit";
import {
  AbsoluteFill,
  Img,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { KineticType } from "./KineticType";
import type { Scene } from "../types";

type SplitProps = Extract<Scene, { type: "split" }>;
const isVideo = (src: string) => /\.(mp4|webm|mov)$/i.test(src);

/** Varun-style hook: footage on top, facecam on bottom, hard divider. */
export const SplitScene: React.FC<{ scene: SplitProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.07], {
    extrapolateRight: "clamp",
  });

  const half: React.CSSProperties = {
    position: "absolute",
    left: 0,
    width: "100%",
    height: "50%",
    overflow: "hidden",
  };

  return (
    <AbsoluteFill style={{ background: "black" }}>
      <div style={{ ...half, top: 0 }}>
        {isVideo(scene.topSrc) ? (
          <Video
            src={staticFile(scene.topSrc)}
            startFrom={Math.round((scene.topFrom ?? 0) * fps)}
            muted
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: `${(scene.topFocusX ?? 0.5) * 100}% 50%`,
              transform: `scale(${zoom})`,
            }}
          />
        ) : (
          <Img
            src={staticFile(scene.topSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: `${(scene.topFocusX ?? 0.5) * 100}% 50%`,
              transform: `scale(${zoom})`,
            }}
          />
        )}
      </div>
      <div style={{ ...half, top: "50%" }}>
        {isVideo(scene.bottomSrc) ? (
          <Video
            src={staticFile(scene.bottomSrc)}
            startFrom={Math.round((scene.bottomFrom ?? 0) * fps)}
            muted
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: `${(scene.bottomFocusX ?? 0.5) * 100}% 20%`,
              transform: `scale(${zoom})`,
            }}
          />
        ) : (
          <Img
            src={staticFile(scene.bottomSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: `${(scene.bottomFocusX ?? 0.5) * 100}% 20%`,
              transform: `scale(${zoom})`,
            }}
          />
        )}
      </div>
      <div
        style={{
          position: "absolute",
          top: "calc(50% - 3px)",
          width: "100%",
          height: 6,
          background: "black",
        }}
      />
      {scene.kinetic && <KineticType kinetic={scene.kinetic} />}
      {scene.credit && <Credit text={scene.credit} />}
    </AbsoluteFill>
  );
};
