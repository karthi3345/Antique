# Editorial Luxury Redesign — "The Private House"

## Goal
Evolve VOLGO from "dark boutique" to an ultra-luxury European private antique
house: cinematic single-object hero, museum-catalogue cards, editorial archive
grid on the collection page, refined two-column object detail, luxury nav,
Private Acquisition section, chapter-numbered The House, quiet scroll motion,
and a final QA/performance pass. **All functionality preserved**: catalogue
filters/API, enquiry form, testimonials, category navigation, palace plate,
test suite.

## Non-negotiables (locked by existing tests)
- `id="collection-carousel"`, `carousel-track`, `carousel-arrow`, `carousel-dots`
  classes + `/collection/?category=X` links on home.
- No prices/discounts/cart/checkout anywhere.
- Artifact page: `/static/img/objects/NNN/00.webp` + `examine-photo` class, no
  turntable markup (no `viewer-canvas`, `viewer.js`, `Drag to rotate`,
  `frame-indicator`, `hotspot-layer`).
- `inspect-list` renders inspection notes.
- Enquiry POST `/api/enquiry/` unchanged.
- `/checkout/` and `/api/order/` stay 404.

## Files to change
- `static/css/volgo.css` — full editorial redesign of tokens & components.
- `templates/base.html` — luxury nav (left logo / center links / right
  acquisition+search), refined footer, full-screen mobile menu.
- `templates/collection/home.html` — single-object cinematic hero (no carousel),
  category rooms row, recent acquisitions, Private Acquisition section,
  testimonials retained.
- `static/js/app.js` — nav scroll state, full-screen mobile menu, reveal system
  (fade-up + clip reveal + parallax, 600–1000ms, reduced-motion honored),
  search overlay.
- `static/js/catalogue.js` — editorial archive grid card markup.
- `templates/collection/catalogue.html` — archive masthead + filter bar.
- `templates/collection/artifact.html` — two-column detail (photo left, dossier
  right), below: story, provenance, condition+specs, related objects.
- `templates/house/the-house.html` — chaptered editorial layout (01–05).
- `templates/house/acquisition.html` — "Objects of distinction, privately
  acquired." section + six services + CTA.
- `templates/house/contact.html` — refined two-col.
- `templates/house/chronicles*.html` — reading room polish.

## Design tokens
- Ground `#0C0A08` warm charcoal; panel `#14110D`; ivory `#F1EBDD`; muted gold
  `#C3A24B` used ONLY as hairlines/labels/underlines (no gold fills, no gradient
  buttons); body text `#C9C0AC`.
- Serif display: Cormorant Garamond 300/400. Sans: Archivo 400/500 for meta.
  H1 clamp(56px,7.5vw,96px); H2 clamp(36px,4.5vw,64px); metadata 11px/0.2em.
- Motion: 600–1000ms, ease cubic-bezier(0.22,1,0.36,1). No bounce, no spin.
- Border-radius 0 everywhere (sharp museum panels). No stripes, no gradients
  (except photographic shading in hero), no glassmorphism, no patterns.

## Acceptance criteria
- [ ] Hero is a single featured object, full viewport, cinematic reveal, two
      CTAs: "Explore the Collection" (primary) + "Private Acquisition"
      (secondary). No carousel JS on home.
- [ ] Category "rooms" row links to `/collection/?category=…` with counts.
- [ ] Catalogue grid renders asymmetric editorial layout (CSS grid with varied
      row spans; single column on mobile) — not a uniform card grid.
- [ ] Cards: image, category, name, period, region, one-line subtitle,
      "Examine Object" CTA on hover; 2–4% zoom; metadata prominence shift.
-  - [ ] Object detail: left photo column (gallery thumbs of frames + fullscreen
      viewer + zoom), right dossier (number, name, period, origin, material,
      dimensions, provenance link, condition, availability, CTA "Enquire About
      This Object"), then story/provenance/condition/related below.
- [ ] Search overlay reachable from nav (opens `/collection/` prefilled).
- [ ] The House: chapters 01–05 with chapter numbers, editorial imagery.
- [ ] Private Acquisition section on home + dedicated page with six services.
- [ ] Scroll: fade-up reveals, clip image reveals, gentle parallax on hero,
      600–1000ms, `prefers-reduced-motion` disables all.
- [ ] Mobile: single-column catalogue, full-screen menu, large CTAs, swipeable
      gallery on artifact page, no horizontal overflow.
- [ ] Performance: lazy loading below fold, width/height set (CLS), font
      `display=swap`, GPU-friendly transforms only.
- [ ] Django test suite green. Enquiry flow works. Facets/filters work.
- [ ] QA: no broken links, no console errors, no missing images, mobile no
      horizontal overflow, keyboard nav, focus states, alt text.

## Tests
- Existing suite must pass (`run_tests.sh`).
- New tests: home renders private-acquisition section id; house page renders
  chapters 01–05; acquisition page renders six services; detail page renders
  dossier keys (Period/Origin/Materials/Dimensions) and related objects.
