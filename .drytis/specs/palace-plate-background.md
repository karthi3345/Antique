# Palace Plate — Subtle Background Layer (Homepage / The House)

## Goal

Use the user-supplied 18th-century palace elevation engraving
(`userDocs/image_db33dd73.png`, 1117×766 landscape) as a whisper-level
(5–8% opacity) architectural background layer on the **Homepage (`/`)** and
**The House (`/the-house/`)** pages, reinforcing the "royal first impression"
of the brand without distracting from content.

## Files to change

- **New** `scripts/make_plate.py` — PIL pipeline that converts the engraving
  into an ivory-ink-on-transparent WebP plate, extended to a 16:9 canvas.
- **New** `static/img/plate-palace.webp` — processed plate asset.
- `templates/base.html` — add `{% block plate %}` inside `<main>`; render
  the plate only on pages that opt in.
- `templates/collection/home.html` — `{% block plate %}` opt-in + a thin
  hairline divider under the hero so the plate doesn't compete with the
  hero slide imagery.
- `templates/house/the-house.html` — `{% block plate %}` opt-in.
- `static/css/volgo.css` — new §12 "palace plate" section: tokens
  (`--plate-tint`, `--plate-opacity`, `--plate-object-position`), the
  `.palace-plate` fixed-position layer, `.hero { border-bottom: … }`, and
  `@media (prefers-reduced-motion)` guard.

## Design decisions

- The site ground is obsidian (`--ink: #0B0A08`). A raw aged-paper engraving
  pasted at 5–8% opacity would tint the page brownish. Instead: extract the
  ink (dark) linework, invert it to ivory, and composite on **transparent** so
  only the drawn lines glow faintly on the dark ground — "etched into the
  gallery wall".
- The supplied engraving is landscape (~1.46:1), slightly taller than 16:9;
  the script letterboxes it onto a true 16:9 transparent canvas
  (2048×1152) so `background-size: cover` never crops the dome/roofline.
- Fixed positioning: the plate is a page-level ambient layer behind `main`,
  not per-section, so it behaves as one continuous etched wall. It sits
  under all content (z-index −1 below `.hero`, which has its own imagery).
- Supplied text/caption strip along the bottom (architect credits, scale
  note) is cropped away: it would read as noise at background opacity.
- Named block `{% block plate %}` in base.html: only the two pages opt in —
  no risk of the plate appearing on catalogue/artifact/contact pages.
- 5–8% overall opacity per the art direction; 7% base, 5% while the user
  scrolls on The House (reduced-motion / perf friendly), and fade-in on
  load for a quiet entrance.

## Acceptance criteria

- [ ] `static/img/plate-palace.webp` exists, 2048×1152, transparent ground,
      ivory-tinted linework (hue ≈ warm ivory #F5EEDC family), no caption text
      visible in the plate (bottom strip cropped).
- [ ] `/` homepage renders `.palace-plate` layer behind content at 7%
      opacity; plate not visible above hero imagery (hero z-index above).
- [ ] `/the-house/` renders `.palace-plate` at 5% opacity.
- [ ] Plate never appears on `/collection/`, `/objects/N/`, `/chronicles/`,
      `/acquisition/`, `/contact/` (block not overridden).
- [ ] Plate ignores pointer events, `prefers-reduced-motion` disables the
      fade animation.
- pointer-events: none, aria-hidden — no a11y impact.
- [ ] `collectstatic` succeeds; plate served with HTTP 200 at
      `/static/img/plate-palace.webp` (hashed variant via manifest storage).
- [ ] No env keys, services, proxies, or DB schema touched. No hardcoded
      URLs/creds — asset referenced via `{% static %}`.
- [ ] Existing test suite (`bash run_tests.sh`) still green.
- [ ] `run_bash("curl -sf preview_url")` → 200 on `/` and `/the-house/`.

## Tests

- Existing Django test suite (unit/integration) — must remain green.
- Visual/browser verification delegated to tester (page renders, plate
  present on the two pages only, no layout shift, no console errors).
