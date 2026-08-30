# Real Museum Imagery — The Curated Archive

## Goal
Replace all AI/synthetic turntable-derived object imagery with **real
museum-quality photography** from open-access collections (The Met Open
Access CC0, Rijksmuseum, Wikimedia Commons public domain). Scale the
collection from 13 to **56 documented objects** (8 per category × 7
categories), each with a real, licensed, archival-style photograph.
Keep the existing site structure, functionality, and editorial design.

## Principles (from the sourcing brief)
- No Google Images, no Pinterest, no auction-house copyrighted photos.
- Prefer **The Met Open Access (CC0)** — API gives high-res download URLs +
  per-object rights + rich metadata (period, culture, medium, dimensions).
  Rijksmuseum/Wikimedia as fallbacks.
- Every object record stores: object_number, title, category, origin,
  period, material, image files, source museum, source URL, license,
  credit line, rights_verified flag.
- Images are downloaded once, cropped to consistent ratios, converted to
  WebP, saved under `static/img/objects/NNN/00.webp` (hero) — the existing
  `frame_count`/`hero_frame` model fields keep working (frame_count=1,
  hero_frame=0; older 36-frame sequences retired for renumbered objects).
- Consistent visual language: neutral warm ivory/grey studio-style
  presentation, object 60–80% of frame, no mixed lifestyle shots.
  Post-processing: gentle center-crop to 4:5 (cards) with neutral ivory
  background padding where the source is white-on-grey — pass through the
  existing PIL pipeline with background normalization to warm ivory.

## Scope of changes
1. `scripts/fetch_museum_images.py` (new) — Met Open Access API search per
   category (8 objects each), filter `IsPublicDomain=true`, download
   primaryImage (original, high-res), record metadata JSON to
   `collection/data/museum_objects.json`.
2. `collection/management/commands/seed_volgo.py` — extend ARTIFACTS to 56
   entries derived from the fetched metadata (real titles, periods,
   regions, materials, dimensions). Each entry gets honest display
   language: images credited as "Reference photograph: <Museum>, <license>"
   on the object page; VOLGO does not claim ownership of the depicted
   museum object. Enquiry/about copy adjusted to reflect that the archive
   is a curated study catalogue.
3. `templates/collection/artifact.html` — add "Reference photograph" credit
   block under Examine photo; add related objects row (same category,
   3 others, museum-card style) with real links.
4. `templates/collection/home.html` — hero: single featured real object
   (keep no-carousel). Rooms carousel keeps category → collection links.
5. `views.py` — pass credit/source fields through `_artifact_full` /
   `_artifact_card`; add `related` list to detail view; expose counts.
6. New migration — add fields to Artifact: `image_source`,
   `image_source_url`, `image_license`, `image_credit`,
   `rights_verified` (bool), `frame_count` default 1.
7. `static/css/volgo.css` — credit-line styling; related-objects row;
   consistency tweaks for mixed-ratio images (object-fit: contain on
   ivory stage, so museum photos never distort).
8. Tests — new: seed produces 56 artifacts; every artifact's hero image
   exists on disk; every artifact has image_license + rights_verified;
   detail page renders credit; related objects same category; API
   `_artifact_card` includes license fields; home view context has
   category tiles for 7 categories.

## Non-negotiables (existing tests + design)
- Keep ids/classes the home/test suite relies on: `collection-carousel`,
  `carousel-track`, `carousel-arrow`, `carousel-dots`, `/collection/?category=`
  links, `examine-photo`, `inspect-list`, no turntable markup, no prices,
  no cart/checkout, enquiry API unchanged.
- Editorial design language unchanged (tokens, motion, typography).
- Static 24-test suite must stay green; new tests added on top.

## Acceptance criteria
- [ ] 56 seeded artifacts (8 × 7 categories), each with real museum image
      on disk at `static/img/objects/NNN/00.webp`, WebP, long edge ≤ 1600px.
- [ ] Every artifact carries source museum, source URL, license, credit,
      rights_verified=true (only CC0/public-domain images accepted).
- [ ] Object page shows "Reference photograph — The Metropolitan Museum of
      Art, Open Access CC0" style credit under the photograph.
- [ ] Object page shows related objects (same category, real links).
- [ ] Hero shows one real museum photograph (no carousel), LCP image
      preloaded (fetchpriority=high).
- [ ] Category rooms tiles use each category's first object image.
- [ ] Collection grid object images render inside ivory stage without
      distortion (object-fit rules).
- [ ] Catalogue filters/facets/search work with 56 objects.
- [ ] Full test suite green (24 existing + new).
- [ ] No broken images on home/collection/detail pages (QA).
- [ ] Home, collection, detail pages have no console errors.

## Tests
- `collection/tests.py` + new test module for imagery pipeline.
- Browser QA by tester sub-agent on preview URL.
