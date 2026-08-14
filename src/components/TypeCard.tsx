import React from "react";
import { AbsoluteFill } from "remotion";
import { KineticType } from "./KineticType";
import { useTheme } from "../theme/tokens";
import type { Scene } from "../types";

type TypeCardProps = Extract<Scene, { type: "typecard" }>;

/** Full-frame solid-color card carrying one piece of display type. */
export const TypeCard: React.FC<{ scene: TypeCardProps }> = ({ scene }) => {
  const theme = useTheme();
  return (
    <AbsoluteFill style={{ background: scene.bg ?? theme.black }}>
      <KineticType
        kinetic={{ y: 0.42, at: 0.05, ...scene.kinetic }}
        color={scene.fg ?? theme.inkOnDark}
      />
    </AbsoluteFill>
  );
};
