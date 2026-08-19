import React from "react";
import { staticFile } from "remotion";

/**
 * The display serif, declared as CSS — never via loadFont().
 *
 * HISTORY, so nobody re-breaks it (STYLE-RULES 2026-08-16):
 * `loadFont({family:"Fraunces"})` used to sit at module scope in InstaCTA.tsx.
 * Root imports that file, so its `delayRender` ran on EVERY composition and
 * killed unrelated reel renders ~3 frames in with a font timeout. The recorded
 * rule is: never call loadFont() at module scope in a file Root imports.
 *
 * It was then removed as "dead code", and every theme serif token was pointed at
 * the SF Pro stack. What nobody noticed is that SIX components still ask for
 * "Fraunces" or "FrauncesUp" by name — SpecSheet, XPost, TimelineCascade,
 * DesktopMockup, ToolStack. With no face loaded those silently fell back to
 * Georgia, and 'FrauncesUp' is not even the filename. So the engine has been
 * rendering the macOS UI font almost everywhere and accidental Georgia in six
 * places, while three real Fraunces weights sat unused in public/fonts.
 *
 * @font-face carries no delayRender, so it cannot repeat the timeout. The cost
 * it trades in is FOUT — early frames rendering in the fallback before the face
 * arrives. That is why `font-display: block` is set, and why the fix was checked
 * by rendering an early frame and a late one and comparing the glyphs.
 */
export const FontFaces: React.FC = () => (
  <style
    // eslint-disable-next-line react/no-danger
    dangerouslySetInnerHTML={{
      __html: `
@font-face {
  font-family: 'Fraunces';
  src: url('${staticFile("fonts/Fraunces-400.woff2")}') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: block;
}
@font-face {
  font-family: 'Fraunces';
  src: url('${staticFile("fonts/Fraunces-600.woff2")}') format('woff2');
  font-weight: 600 900;
  font-style: normal;
  font-display: block;
}
@font-face {
  font-family: 'Fraunces';
  src: url('${staticFile("fonts/Fraunces-Italic.woff2")}') format('woff2');
  font-weight: 400 900;
  font-style: italic;
  font-display: block;
}
/* Six components ask for this name. Alias it rather than hunt them all down and
   risk missing one — a missed rename is a silent Georgia. */
@font-face {
  font-family: 'FrauncesUp';
  src: url('${staticFile("fonts/Fraunces-600.woff2")}') format('woff2');
  font-weight: 400 900;
  font-style: normal;
  font-display: block;
}
/* DISPLAY-FACE CANDIDATES (2026-08-18). The user's note: "Font style represents
   the theme of our video, like our niche is tech." Fraunces is a magazine serif
   — correct for an editorial voice, wrong for a hardware-news channel. All four
   are OFL-1.1, so they ship with the repo rather than being fetched at render.
   Whichever is chosen becomes theme/type.ts DISPLAY; the rest can be deleted. */
@font-face {
  font-family: 'Space Grotesk';
  src: url('${staticFile("fonts/space-grotesk-700.woff2")}') format('woff2');
  font-weight: 400 900;
  font-display: block;
}
@font-face {
  font-family: 'Archivo';
  src: url('${staticFile("fonts/archivo-800.woff2")}') format('woff2');
  font-weight: 400 900;
  font-display: block;
}
@font-face {
  font-family: 'Chakra Petch';
  src: url('${staticFile("fonts/chakra-petch-700.woff2")}') format('woff2');
  font-weight: 400 900;
  font-display: block;
}
@font-face {
  font-family: 'Sora';
  src: url('${staticFile("fonts/sora-800.woff2")}') format('woff2');
  font-weight: 400 900;
  font-display: block;
}
@font-face {
  font-family: 'Press Start 2P';
  src: url('${staticFile("fonts/PressStart2P.ttf")}') format('truetype');
  font-display: block;
}
`,
    }}
  />
);
