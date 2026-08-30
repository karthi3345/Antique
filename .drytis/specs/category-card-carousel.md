# Task: Restyle the Collection category carousel to a clean product-card grid

## Files to change
- `static/css/volgo.css` — replace the `.carousel-*` premium dark-overlay card styles with light, clean product-card styles (image top, caption below on ivory background, subtle bordered "explore" pill button), matching the reference screenshot (`/workspace/userDocs/image_1e8b8e6c.png`).
- `templates/collection/home.html` — markup stays (server-rendered category cards, paged JS carousel, arrows, dots). Optionally adjust card internals to match the new design.

## Context
- Reference layout (from the user's own site, other template): 4 cards per row; each card = photo on white/ivory card, thin hairline border, category name below the image in serif text, small uppercase "explore" pill button with magnifier/arrow icon, no price, no add-to-cart.
- Site is a Django project. Category cards are rendered server-side from `_category_tiles()` in `collection/views.py` — data already correct (7 categories with counts).
- Design language of the site: ivory `--ivory: #FAF6EE`, gold `--gold: #A8853C`, hairline borders, Cormorant Garamond display font, Archivo utility font, restraint is the aesthetic.
- The user said "similar like that i need remove all collection make premium that" → i.e. the reference is the *direction*: clean product-card carousel, not the current dark caption-on-image look. We are NOT selling — no prices, no cart.

## Acceptance criteria
- [ ] Category cards render as clean product cards: photo on top with hairline border, category name below, explore button below name.
- [ ] 4 cards per row on desktop, 2 on tablet, 1 on mobile (already handled by carousel paging JS + media queries — preserve).
- [ ] No dark gradient overlay text on the images.
- [ ] No price, no discount, no add-to-cart anywhere in the carousel.
- [ ] Arrows and dot pagination still work.
- [ ] Cards link to `/collection/?category=<name>`.
- [ ] Carousel still paged (translateX transform), arrows disabled at ends.
- [ ] No console errors on the home page.

## Tests
- Existing test suite: `./run_tests.sh` (or `python3 manage.py test`).
- Unit/integration: a test asserting every category from the DB appears in the home page HTML as a card (already exists? check `collection/tests/`).
- Browser test (tester): visual check of the new card layout + arrows + dots on the preview URL.
