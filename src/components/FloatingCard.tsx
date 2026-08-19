import React from "react";
import { Credit } from "./Credit";
import { TINT } from "../theme/palette";
import { SPRING, DUR } from "../theme/motion";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import { KineticType } from "./KineticType";
import type { Scene } from "../types";

type CardProps = Extract<Scene, { type: "floatcard" }>;

const BGS: Record<string, string> = {
  black: "#0a0a0a",
  cream: TINT.sand,
  gradient: "linear-gradient(160deg, #dfe8f5 0%, #f3e3d9 55%, #e8d9f0 100%)",
};

/**
 * Nick-style floating UI card: a 16:9 screen recording in a rounded card on
 * a clean field, sliding up on entry with a slow float afterwards.
 */
export const FloatingCard: React.FC<{ scene: CardProps }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();

  const enter = spring({
    frame,
    fps,
    config: SPRING.enter,
    durationInFrames: DUR.base,
  });
  const float = interpolate(frame, [0, durationInFrames], [0, -26]);
  // card follows media aspect (FEEDBACK 2026-07-31: never re-crop a shot)
  const aspect = scene.aspect ?? 16 / 9;
  const cardW = aspect >= 1 ? width * 0.92 : Math.min(width * 0.7, 1560 * aspect);
  const cardH = cardW / aspect;

  const bg = BGS[scene.bg ?? "gradient"];

  return (
    <AbsoluteFill
      style={{
        background: bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: cardW,
          height: cardH,
          borderRadius: 28,
          overflow: "hidden",
          boxShadow: "0 34px 90px rgba(0,0,0,0.4)",
          opacity: enter,
          transform: `translateY(${(1 - enter) * 90 + float}px)`,
        }}
      >
        <OffthreadVideo
          src={staticFile(scene.src)}
          startFrom={Math.round((scene.from ?? 0) * fps)}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>
      {scene.kinetic && <KineticType kinetic={scene.kinetic} color="#111" />}
      {scene.credit && (
        // USER FEEDBACK 2026-08-12 #5: a bare name floating in the field reads
        // as a stray word. It is labelled, and sits just under the card's
        // bottom-left corner so it is unambiguously attached to that footage.
        //
        // It used to hand-roll the whole label to get that placement, which
        // meant it silently opted out of the once-per-source rule and the
        // qualifier stripping (2026-08-19). Credit takes a `top` anchor now,
        // so the placement is kept and the policy applies.
        <Credit
          text={scene.credit}
          top={height / 2 + cardH / 2 + 22}
          left={(width - cardW) / 2}
          onMedia={(scene.bg ?? "gradient") === "black"}
          plate={false}
        />
      )}
    </AbsoluteFill>
  );
};
