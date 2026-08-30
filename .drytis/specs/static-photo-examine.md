# Task: Replace the 360° turntable viewer with a plain static photograph

## Why
User request: "no need to rotate like this is fine — Rusty vintage kerosene
lanterns with glass globes seen at an outdoor flea market during sunny day"
(attached a plain still photograph). The artifact "Examine" section currently
runs a canvas-based photographic turntable (drag to rotate through 36 frames,
wheel/pinch zoom, hotspot layer). The user wants a simple, still photograph —
no rotation interaction.

## Files to change

### Frontend
- `templates/collection/artifact.html`
  - Replace the `#examine` section (canvas turntable + zoom controls + frame
    indicator) with a static `<img>` of the object's hero frame
    (`/static/img/objects/NNN/00.webp`), styled to match the house aesthetic
    (cream stage, hairline border, contained height).
  - Keep the section id `examine` (acquisition page anchors to it).
  - Render the object's `inspection_points` as a readable list of inspection
    notes under the photograph (label, kind, detail) — the data stays useful
    without the interactive hotspots.
  - Remove `<link viewer.css>`, `<script viewer.js>` includes.
  - Update hint copy: no "Drag to rotate" language anywhere.
- `templates/house/acquisition.html`
  - Step II copy "rotate the object, enlarge the surface" → "study the
    photograph, read the inspection notes".
- `static/js/viewer.js` — DELETE.
- `static/css/viewer.css` — DELETE.
- `static/css/volgo.css` — remove turntable chrome rules (`.viewer-stage
  canvas`, `.viewer-hint`, `.viewer-controls`, `.icon-btn`, `.hotspot`,
  `.hotspot-tip`, `is-interacting`); add a `.examine-photo` block styling the
  static image.

### Backend (models/data)
- No model changes. `frame_count` stays (harmless, drives nothing on the page).
- `InspectionPoint.frame_index/x/y` stay in DB but are no longer rendered as
  hotspots; they appear in the plain notes list.

### Tests
- `collection/tests.py` — add `StaticExamineTest`:
  - artifact page contains `<img` with `objects/{n:03d}/00.webp` src.
  - artifact page does NOT contain `viewer-canvas`, `viewer.js`, `Drag to
    rotate`, `frame-indicator`.
  - artifact page renders inspection points list (label text present).

## Acceptance criteria
- [ ] Artifact page shows a single still photograph; no canvas, no drag/rotate.
- [ ] No "Drag to rotate" / "turntable" copy anywhere in templates.
- [ ] Inspection notes render as a list under the photo.
- [ ] `viewer.js` / `viewer.css` deleted; no template references them.
- [ ] `collectstatic --clear` succeeds with no stale viewer assets.
- [ ] Existing tests still pass; new tests pass.
- [ ] Reviewer + tester PASS.

## Out of scope
- Uploading the user's lantern photo as a specific object image (no object
  matches it; frames are generated placeholders). Site keeps its existing
  per-object hero frame as the still photograph.
