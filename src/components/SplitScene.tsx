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
              // THE HANDS WERE BEING CROPPED OUT (2026-09-02).
              //
              // This was hardcoded to 20%, anchoring a half-height panel near
              // the TOP of a 1080x1920 source. The digital twin is recorded
              // waist-up with hands in frame on purpose
              // (references/digital-twin-recording-spec.md), and measured on
              // the shipped masters it gestures hard: 7.6 to 11.4 against the
              // registry's 4.41 for a look that "gestures". Compared frame to
              // frame, the master showed both hands raised in an open-palm
              // gesture and the rendered split showed head and shoulders only.
              // Every gesture in a split beat was thrown away by the crop.
              //
              // AND NO ANCHOR CAN FIX IT. Measured on the master at the
              // same timestamp: eyes at 23% of frame height, hands at 74-92%.
              // Containing both needs a 69% span; a half-height panel over a
              // 9:16 source shows ~47% after the 1.07 push. Anchoring at 45%
              // was tried and rendered: it cut the eyes AND still missed the
              // hands, which is worse than where it started.
              //
              // So the default stays at 20% — face-first, which is the right
              // call for a panel that cannot hold the whole gesture — and
              // `bottomFocusY` exists for a presenter framed differently.
              // The gestures belong to FULL-FRAME footage beats, and the real
              // fault is how few of those a reel gets: see G60.
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
              objectPosition: `${(scene.bottomFocusX ?? 0.5) * 100}% ${
                (scene.bottomFocusY ?? 0.20) * 100}%`,
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
              objectPosition: `${(scene.bottomFocusX ?? 0.5) * 100}% ${
                (scene.bottomFocusY ?? 0.20) * 100}%`,
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
