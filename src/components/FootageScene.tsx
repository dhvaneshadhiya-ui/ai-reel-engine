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
  // `zoom` is the BASE the push runs from, not a replacement for it, so an old
  // sheet with no `zoom` is byte-identical to before: base 1 => 1 -> 1.1.
  const base = scene.zoom ?? 1;
  const zoom =
    dir === "none"
      ? base
      : dir === "in"
        ? interpolate(frame, [0, durationInFrames], [base, base * 1.1], {
            extrapolateRight: "clamp",
          })
        : interpolate(frame, [0, durationInFrames], [base * 1.1, base], {
            extrapolateRight: "clamp",
          });

  // SLIDE — the corpus answer for footage that does not fit a 9:16 frame
  // (measured 2026-08-25 from the two reference shorts the user supplied): a
  // wide desktop page is fitted to the frame HEIGHT and travelled sideways; a
  // tall page or poster is fitted to the WIDTH and travelled vertically. Both
  // read as reading, not as cropping — which is what a static `cover` does to
  // an oversized asset, silently throwing most of it away.
  //
  // Implemented on objectPosition, so `cover` still governs the fit and the
  // travel is exactly the overflow: 0%..100% IS "from one edge to the other",
  // whatever the asset's real aspect. Eased, never linear — a constant-speed
  // pan reads mechanical.
  const slide = scene.slide;
  const ease = (x: number) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);
  const travel = slide
    ? ease(interpolate(frame, [0, durationInFrames], [0, 1], {
        extrapolateRight: "clamp",
      }))
    : 0;
  const span = scene.slideSpan ?? 1;          // 1 = edge to edge
  const start = (1 - span) / 2;
  const along = (start + travel * span) * 100;
  const objectPosition = slide === "left"
    ? `${along}% ${(scene.focusY ?? 0.5) * 100}%`
    : slide === "right"
      ? `${100 - along}% ${(scene.focusY ?? 0.5) * 100}%`
      : slide === "up"
        ? `${(scene.focusX ?? 0.5) * 100}% ${along}%`
        : slide === "down"
          ? `${(scene.focusX ?? 0.5) * 100}% ${100 - along}%`
          : `${(scene.focusX ?? 0.5) * 100}% ${(scene.focusY ?? 0.5) * 100}%`;

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
            objectPosition,
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
