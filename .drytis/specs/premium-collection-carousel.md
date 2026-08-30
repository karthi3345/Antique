# Task: Premium category carousel on the home page

## Why
User request: "similar like that i need remove all collection make prmeium that" —
with a pasted Mobirise/Bootstrap multi-item category carousel (photo card + category
name + "explore" link, floating prev/next arrows). The user wants the home page's
current collection-browsing sections replaced with ONE premium carousel in the same
spirit, styled to the Volgo French-boutique aesthetic (ivory/cream/gold, Cormorant
Garamond, hairlines — no Bootstrap markup or CDN).

## What changes
- REMOVE the "Explore by Category" tile grid (`#categories`, .grid-categories/.cat-tile).
- REMOVE the "Explore by Material" chip row (`#materials`, .grid-materials/.mat-chip).
- ADD one section `#collection-carousel` — "La Collection / The Collection":
  - Horizontal multi-card carousel: category photo, category name, object count,
    and an "Explore" link → `/collection/?category=<name>`.
  - Floating circular prev/next arrow controls at the sides (like the pasted
    .btn-floating-lt/.btn-floating-rt), disabled at the ends.
  - Dots per page under the track (matching .hero-dot styling).
  - 4 cards per page desktop, 2 tablet, 1 mobile; swipe support on touch.
  - No auto-rotation (restraint; user dislikes needless rotation).
- Images rendered SERVER-SIDE (no client fetch pop-in): first object of each
  category supplies the hero photo (`/static/img/objects/NNN/00.webp`).

## Files to change
- `collection/views.py`
  - Add `_category_tiles()` → [{cat, count, hero}] ordered by first object number.
  - `home()` passes `categories=_category_tiles()`; drop `materials` context and
    the now-unused `_material_facets()`.
- `templates/collection/home.html`
  - Replace the two explore sections with the carousel markup.
  - Remove the `[data-cat-img]` fetch JS; add carousel JS (paging, arrows, dots,
    resize, swipe).
- `static/css/volgo.css`
  - Delete .grid-categories/.cat-tile/.grid-materials/.mat-chip rules (+ responsive
    lines for .grid-categories).
  - Add .carousel-* rules (frame, viewport, track, card, figure, veil, count,
    caption, explore line, arrows, dots) using the --per CSS var for page size.
- No DB / migration / env / service changes.

## Tests (`collection/tests.py`)
New `CollectionCarouselTest`:
- Home renders `carousel-track`, one card per category, and explore links
  `/collection/?category=Sculpture` etc.
- Card image is server-rendered hero of the category's first object.
- Old sections gone: no `grid-categories`, `grid-materials`, `mat-chip`,
  "Explore by Category", "Explore by Material".
- Prev/next arrow buttons and dots container present.

## Acceptance criteria
- [ ] Home page shows ONE premium category carousel; old category tiles and material chips are gone.
- [ ] Each card links to the catalogue filtered by that category.
- [ ] Arrows page the carousel; disabled at the ends; dots reflect the page.
- [ ] 4/2/1 cards per page responsive breakpoints work.
- [ ] No client-side fetch needed for category images (server-rendered src).
- [ ] Full test suite passes (19 existing + new).
- [ ] collectstatic clean; preview serves updated CSS/HTML.
- [ ] infra_verifier, reviewer, tester all PASS.
