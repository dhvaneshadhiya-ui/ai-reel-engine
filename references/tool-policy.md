# Tool selection policy

Use the smallest deterministic stack that produces the needed visual.

## Default

- Remotion + React for composition, timing, captions, camera moves, cards,
  charts, counters, UI recreations, asset layering, music, and SFX.
- SVG/CSS inside Remotion for icons, arrows, masks, highlights, and diagrams.
- FFmpeg for exact cuts, crops, audio extraction, loudness, and final encode.
- Playwright or system Chrome for real screenshots and screen recordings.

## Optional

- Lottie: use for a licensed reusable mascot, icon loop, loader, or
  micro-animation. Render through `@remotion/lottie`; disable or pre-render
  unsupported expression-heavy files, and do not add a second timeline engine
  for basic motion.
- Manim: use only for a genuinely explanatory mathematical, geometric, graph,
  or mechanism animation that would be cumbersome in SVG. Render a transparent
  or clean-background clip and embed it.
- Motion Canvas/Revideo: use only for a substantial custom procedural
  explainer sequence with its own timeline. Export once and embed; do not run
  two competing timelines for ordinary scenes. Do not make Revideo a default
  dependency; its runtime and telemetry posture require separate review.
- p5.js/tsParticles: use sparingly for abstract procedural backgrounds. Freeze
  randomness with a seed and drive time from the Remotion frame.
- Typst: use when the reel needs beautifully typeset equations or document
  fragments; export to SVG and animate the SVG in Remotion.

## Avoid by default

- GSAP, anime.js, and Motion/Framer Motion inside renders. Their browser-time
  animation models add little to this engine and can become nondeterministic.
  If a rare effect requires one, set progress explicitly from the current
  Remotion frame; never use autonomous CSS or requestAnimationFrame timelines.
- Manim for ordinary titles, lists, charts, or product screenshots.
- Generative video for factual product UI, logos, receipts, commands, or data.
- Installing multiple libraries merely because they are available.
- Pulling GPL/LGPL or commercially restricted code into the renderer without
  checking the exact package license and distribution impact. Remotion's own
  license and plan terms must also be reviewed before commercial scaling.

## Generative media

Generate stills or short video only when the beat is conceptual and lacks a
real visual. Keep a stable palette and reference frame. Inspect the still and a
mid-video frame before use. Regenerate on text artifacts, palette drift,
unmotivated objects, or weak 9:16 composition.
