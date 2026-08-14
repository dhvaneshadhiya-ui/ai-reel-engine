# Job contract

Engine root: `<ENGINE_ROOT>`

Each job uses one slug consistently.

## Files

- `jobs/<slug>/brief.json`: immutable user input plus inferred defaults.
- `jobs/<slug>/giveaway.md`: the real resource promised by the CTA.
- `scripts/<slug>.md`: final script and phrase-to-visual beat map.
- `public/assets/<slug>/manifest.json`: sourced/generated asset ledger.
- `jobs/<slug>/shot-plan.json`: phrase-anchored editorial decisions.
- `public/assets/<slug>/avatar-master.mp4`: presenter plus master voice.
- `public/assets/<slug>/vo.json`: Whisper word timings.
- `public/assets/<slug>/face-x.txt`: measured face-center fraction.
- `src/beats/<slug>.json`: renderable beat sheet.
- `out/<slug>-raw.mp4`: unmastered render.
- `out/<slug>-final.mp4`: mastered delivery.
- `out/<slug>-lint/`: labeled verification frames and contact sheets.

## Brief schema

```json
{
  "slug": "example-topic",
  "topic": "What the reel is about",
  "details": "Optional user facts, angle, links, or constraints",
  "style": "nick-saraev",
  "target_seconds": 38,
  "cta_keyword": "GUIDE",
  "created_at": "ISO-8601 timestamp",
  "status": "initialized"
}
```

## Manifest schema

```json
{
  "slug": "example-topic",
  "items": [
    {
      "id": "official-launch",
      "kind": "receipt",
      "source_url": "https://...",
      "published": "YYYY-MM-DD",
      "local_path": "assets/example-topic/launch.png",
      "claim": "The exact claim this proves",
      "shows": "What is visibly readable in the asset",
      "credit": "Source name",
      "crop": "Region or subject to emphasize",
      "rights_note": "Official page / licensed / generated"
    }
  ]
}
```

## Shot-plan schema

The shot plan stays human-readable and does not contain hand-calculated
timings. `start_phrase` and `end_phrase` are resolved sequentially against
Whisper words. Each `scene` is an engine scene with these compiler tokens:

- `$AVATAR`: `assets/<slug>/avatar-master.mp4`
- `$START`: the shot's absolute start time, useful for avatar/media trims
- `$FACE_X`: measured face-center fraction from `face-x.txt`
- `$FOCUS_FULL`: calculated CSS focus for a full 1080×1920 cover
- `$FOCUS_SPLIT`: calculated CSS focus for a 1080×960 split cover

```json
{
  "emphasis": ["free", "three steps"],
  "caption_corrections": {"heygen": "HeyGen"},
  "shots": [
    {
      "start_phrase": "this is the hook",
      "end_phrase": "first proof",
      "asset_id": "official-launch",
      "scene": {
        "type": "split",
        "topSrc": "assets/example-topic/launch.png",
        "bottomSrc": "$AVATAR",
        "bottomFrom": "$START",
        "bottomFocusX": "$FOCUS_SPLIT",
        "captionBottom": 1000
      }
    }
  ]
}
```

All paths stored in beat sheets are relative to the engine's `public/`
directory. Do not place raw downloads in `public/`; keep them under
`_sources/assets/<slug>/`.

## Beat-sheet invariants

- `id` equals the slug.
- 30 fps, 1080×1920.
- Scene durations sum to the master audio duration within 0.20 seconds.
- Every referenced local asset exists.
- The first scene shows the face in a split, avatar footage, or a word cascade
  with avatar bottom.
- First scene is at most about 2.8 seconds.
- Average scene duration is at most about 2.5 seconds.
- `captionStyle` is `chip-lg`.
- Music automation exists and ends with a fade.
- CTA resource exists before the final script promises it.
