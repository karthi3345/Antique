# Task: Trumpet as a Catalogued Product with a 3D Turntable Viewer

## Why
User request: "use hi as product and acts a 3d" — the uploaded trumpet photo
(`/workspace/userDocs/image_c53cbcb5.png`, a 3000×3000 studio shot on a dark
green-black background) becomes a catalogued product on the site, and the site
presents objects in 3D.

## Approach
1. **New product** — the trumpet becomes **OBJECT No. 013** in the collection:
   a full archival record (story, provenance chain, condition, specs,
   inspection notes, documents) in `seed_volgo.py`, matching the house style
   of the existing 12 objects. Category "Musical Instruments" (new room).
2. **3D presentation** — every artifact's existing 36-frame photo sequence
   (`/static/img/objects/NNN/00–35.webp`) is upgraded from a static hero image
   to an interactive **drag-to-rotate turntable viewer**:
   - Pointer/touch drag spins the object horizontally (frame scrub).
   - Inertia glide after release; snaps to nearest frame; slows gently.
   - Gentle auto-rotate until first interaction; stops on drag.
   - Drag hint chip ("Drag to turn — 36 views") fades after first use.
   - D-pad buttons (left/right) step one frame; auto-repeat on hold.
   - Keyboard: ArrowLeft/ArrowRight rotate, Enter opens object page.
   - Reduced-motion: no auto-rotate, no inertia.
   - Viewport-visibility pause for auto-rotate.
   - Preload neighbor frames for smooth scrubbing.
   - Feature is progressive — plain `<img>` with correct hero frame stays for
     no-JS.
3. **Trumpet frames** — a Python/Pillow script renders 36 distinct views of
   the trumpet from the source photo: perspective horizontal skew + edge
   extension to simulate rotation around a vertical axis, with slight elliptical
   squash and per-frame specular sheen so consecutive frames differ (matches
   the house convention of 36 genuinely distinct frames). Output:
   `static/img/objects/013/00–35.webp`, 1000×1000 WebP, transparent edges —
   same pipeline/shape as the existing 12 objects.

## Files to change
- `scripts/make_trumpet_frames.py` — NEW, idempotent renderer (skips when 36
  frames exist and match a sentinel).
- `static/img/objects/013/*.webp` — 36 generated frames (binary assets).
- `collection/management/commands/seed_volgo.py` — add artifact 13 (trumpet),
  provenance chain, inspection points, documents; trumpet `featured=True`.
- `static/js/turntable.js` — NEW, dependency-free 3D turntable viewer.
- `templates/collection/artifact.html` — wrap the Examine photo in the
  turntable markup (progressive: img stays, JS enhances).
- `static/js/catalogue.js` — card hover rotates the hero frame a few steps
  (uses frames 00–05) so the catalogue itself feels 3D.
- `static/css/volgo.css` — `.turntable`, `.turntable-hint`, `.turntable-dpad`,
  `.card-figure` hover rotation polish; dark-luxury styling.
- `templates/collection/home.html` — hero slide gets a "turn the object" affordance.
- `collection/tests.py` — new tests: artifact 13 rendered fields, seed
  idempotency, turntable markup present, frame URL pattern, catalogue API
  includes 013, category counts.
- `.drytis/infrastructure.md` — document the new script.

## Acceptance criteria
- [ ] Trumpet exists as OBJECT No. 013: artifact page `/objects/13/` renders
      full record (label, story, provenance timeline, condition, specs,
      inspection notes, documents).
- [ ] Artifact page shows the interactive 3D viewer on the Examine photo:
      pointer drag rotates through 36 frames; buttons/keyboard also rotate;
      hint chip appears and fades; no layout shift; reduced-motion honored.
- [ ] Without JS, the Examine photo still shows the correct hero frame `<img>`.
- [ ] Catalogue grid card for the trumpet hovers into a short rotation preview.
- [ ] Home hero carousel includes the trumpet; explore carousel has a
      "Musical Instruments" category card linking to `/collection/?category=Musical%20Instruments`.
- [ ] `/api/objects/` returns 13 objects; facets include the new category.
- [ ] 36 distinct frames exist at `/static/img/objects/013/00–35.webp`
      (1000×1000 WebP); at least 30 unique md5s.
- [ ] Django test suite passes (24 existing + new tests).
- [ ] collectstatic re-run; preview serves the new viewer (HTTP 200).
- [ ] reviewer + tester + infra_verifier PASS.

## Tests
- Unit: seed produces artifact 13 with expected fields; category counts
  include Musical Instruments = 1; API returns 13 cards; template includes
  turntable wrapper + data attributes; reduced-motion attr propagation.
- Integration: `/objects/13/` renders 200 with story/provenance/inspection;
  `/api/objects/` JSON includes trumpet; static frame files exist on disk
  (checked from tests via base dir).
- Browser (tester): drag interaction on artifact 13 Examine viewer, buttons,
  keyboard, hint chip, catalogue hover, home carousel card.
