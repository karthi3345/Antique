# UX/UI Asset & Animation Craft Upgrade

**Task:** Implement the VOLGO UX/UI brief (hero object as 3D-rotatable product, luxury motion system, consistent imagery) on the existing Django site — preserving identity, content, structure, and all functionality.

## Files to change / create

| Path | Change |
|---|---|
| `scripts/make_trumpet_frames.py` | Rewrite: composite trumpet cutout onto the house cream stage (240,234,218), 36 frames, warm shadow, consistent 1000×1000 |
| `collection/management/commands/seed_volgo.py` | Add Artifact 13 (Contemporary Trumpet — user's own product image) with story, provenance, inspection, docs |
| `templates/collection/artifact.html` | Replace static `examine-photo` with EXAMINE turntable viewer (canvas), thumbnails, hotspots, zoom hint, lightbox |
| `static/js/examine.js` | NEW — turntable engine: progressive frame load, drag rotate, wheel zoom, pinch, hotspot overlay, lightbox, reduced-motion |
| `static/css/volgo.css` | Loader, custom cursor, turntable + hotspot styles, parallax util, page-transition, swipe gallery, QA fixes |
| `static/js/app.js` | Loader, custom cursor, secondary parallax, page-transition capture, drag-swipe for mobile |
| `templates/base.html` | Loader markup, cursor elements, font preload, hero preload link |
| `templates/collection/home.html` | Hero preload, pa/house parallax hooks, palace plate image already removed slide-shade → kept |
| `config/settings.py` | (only if needed) — none expected |

## Acceptance criteria

- [ ] Artifact 013 exists: trumpet, available, featured, appears in catalogue + API + home grids, all frames render on the house cream stage (corner RGB ≈ 240,234,218)
- [ ] Artifact detail page shows EXAMINE turntable: user can drag to rotate through 36 frames; frames load progressively (frame 0 first, no waterfall of 36 requests blocking first paint)
- [ ] Zoom: wheel / pinch zooms object; double-click toggles 1×↔2.2×; cursor zoom-in/out states
- [ ] Hotspots (inspection points) render at stored x/y, clickable, show note panel; hidden while zoomed
- [ ] Lightbox fullscreen viewer: open from EXAMINE, zoom, close, prev/next frames, Esc closes
- [ ] Mobile: swipe rotates the object; page transition disabled (native nav); no custom cursor
- [ ] VOLGO loader ≤1.5s, max once per session (sessionStorage), skipped when reduced-motion
- [ ] Custom cursor: desktop pointer:fine only, circle grows on interactive hover, EXAMINE label over cards, hidden for reduced-motion/touch
- [ ] Hero: image preload + 4-step staggered entrance (eyebrow→h1→desc→CTA) already present — verified intact; parallax 10–20px on hero, Private Acquisition image, House strip
- [ ] Page transition: catalogue card click → object detail, 500–700ms fade/scale, skipped reduced-motion, no double navigation
- [ ] All frames 1000×1000 WebP; below-the-fold lazy; no console errors; no horizontal overflow; `prefers-reduced-motion` kills parallax/cursor/loader/turntable auto-rotate
- [ ] Existing tests still pass + new tests: seed includes 13 artifacts; `/api/objects/` returns 13; api filters unaffected

## Tests

- Unit (Django `collection/tests.py`): seed count = 13; artifact 13 fields; API returns 13 objects; catalogue JSON includes 013 hero path
- Integration: GET `/objects/13/` 200; frames 00–35 of 013 exist on disk and are 1000×1000
- Browser (tester): rotate/zoom/lightbox/hotspots on object 013; catalogue filter; nav; console clean
