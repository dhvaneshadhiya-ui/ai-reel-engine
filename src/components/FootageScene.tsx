import React from "react";
import {
  AbsoluteFill,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { KineticType } from "./KineticType";
import type { Scene } from "../types";
import { Credit } from "./Credit";

type FootageProps = Extract<Scene, { type: "footage" }>;

/** Full-bleed vertical footage with optional slow push-in, credit, kinetic type. */
export const FootageScene: React.FC<{ scene: FootageProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const dir = scene.zoomDir ?? "in";
  const zoom =
    dir === "none"
      ? 1
      : dir === "in"
        ? interpolate(frame, [0, durationInFrames], [1, 1.1], {
            extrapolateRight: "clamp",
          })
        : interpolate(frame, [0, durationInFrames], [1.1, 1], {
            extrapolateRight: "clamp",
          });

  return (
    <AbsoluteFill style={{ background: "black" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <Video
          src={staticFile(scene.src)}
          startFrom={Math.round((scene.from ?? 0) * fps)}
          muted
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: `${(scene.focusX ?? 0.5) * 100}% 50%`,
          }}
        />
      </AbsoluteFill>
      {scene.kinetic && <KineticType kinetic={scene.kinetic} />}
      {scene.infocard && (() => {
        const at = Math.round((scene.infocard.at ?? 0.2) * fps);
        const p = interpolate(frame, [at, at + 12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: (x) => 1 - Math.pow(1 - x, 3),
        });
        return (
          <div
            style={{
              position: "absolute",
              top: 150,
              left: 0,
              right: 0,
              padding: "56px 64px 90px",
              background:
                "linear-gradient(180deg, rgba(0,0,0,0.86) 0%, rgba(0,0,0,0.7) 55%, rgba(0,0,0,0) 100%)",
              opacity: p,
              transform: `translateY(${(1 - p) * -24}px)`,
            }}
          >
            <div
              style={{
                fontFamily:
                  "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
                fontWeight: 800,
                fontSize: 60,
                letterSpacing: "-0.02em",
                color: "#fff",
                marginBottom: 16,
                lineHeight: 1.05,
              }}
            >
              {scene.infocard.heading}
            </div>
            <div
              style={{
                fontFamily:
                  "-apple-system,'SF Pro Display','Helvetica Neue',sans-serif",
                fontWeight: 400,
                fontSize: 36,
                lineHeight: 1.35,
                color: "rgba(255,255,255,0.9)",
                maxWidth: 900,
              }}
            >
              {scene.infocard.body}
            </div>
          </div>
        );
      })()}
      {scene.credit && <Credit text={scene.credit} />}
    </AbsoluteFill>
  );
};
