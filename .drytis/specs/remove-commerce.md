# Task: Remove all commerce / selling features

## Why
The user states: "we are not selling". The site must be a pure catalog/showcase —
objects are documented, not priced-and-bought. Everything that reads as an
e-commerce store (add-to-cart, checkout/buying, % OFF discount badges,
struck-through compare prices, cart drawer, "Shop by" copy, payment/delivery
banner) must be removed. Acquisition happens only through private enquiry.

## Files to change

### Backend
- `collection/models.py`
  - Delete `Order` and `OrderLine` models.
  - Delete `compare_price` field and `discount_percent` property from `Artifact`.
  - Keep `price` field internally? → NO: remove from all user-facing output. DB
    column stays (harmless historical data) but API/templates/JS must not render it.
- `collection/migrations/0004_*.py` — new migration removing Order/OrderLine tables
  and compare_price column.
- `collection/views.py`
  - Remove `checkout_view`, `api_order`.
  - Remove `price`, `compare_price`, `discount` keys from `_artifact_card` /
    `_artifact_full`.
  - Remove price sort options from `api_objects` order_map (keep period/name/number).
- `config/urls.py` — remove `/checkout/` and `/api/order/` routes.
- `collection/management/commands/seed_volgo.py` — remove `compare_price` and
  `bestseller` (selling emphasis) usage; keep `price` out of seed data.
- `collection/admin.py` — keep enquiry/chronicle admin (no Order admin existed).

### Frontend
- `templates/base.html` — remove cart button, cart drawer, cart.js include,
  checkout link in footer, payment-on-delivery announcement bar.
- `templates/collection/home.html` — remove price lines, "Acquire This Object"
  CTA (replaced with view-object CTA), bestseller badge/% OFF badges, add-to-cart
  buttons, "Shop by Material" heading → "Explore by Material".
- `templates/collection/artifact.html` — remove price block, % OFF badge,
  Add to Collection button; "Enquire privately" anchor stays as CTA.
- `templates/collection/catalogue.html` — remove price sort options.
- `templates/collection/checkout.html` — DELETE file; add redirect view? No —
  remove route entirely.
- `static/js/cart.js`, `static/js/checkout.js` — DELETE files.
- `static/js/catalogue.js` — remove discount/compare/price rendering + add-to-cart
  button markup.
- `static/css/volgo.css` — remove cart drawer / checkout / .was / badge--sale /
  cart-btn rules (leave `.price` for potential reuse — actually remove sale
  styling; keep base `.price` unused-safe).

### Tests
- `collection/tests.py` — remove CommerceTest order/discount tests; replace with:
  - `/api/objects/` cards contain NO `price`/`discount` keys.
  - `/api/order/` returns 404 (route gone).
  - `/checkout/` returns 404 (route gone).
  - enquiry API still works (already covered elsewhere).
- `run_tests.sh` — unchanged (runs test suite).

## Acceptance criteria
- [ ] No "Add to Cart", "Add to Collection", "buy", "checkout" UI anywhere in templates/JS.
- [ ] No "% OFF" / discount badge / struck-through (was) price rendered anywhere.
- [ ] No `price`, `compare_price`, `discount` keys in `/api/objects/` or `/api/artifact/<n>/` responses.
- [ ] `/checkout/` and `/api/order/` return 404.
- [ ] Order/OrderLine tables dropped; compare_price column dropped (migration applied).
- [ ] Cart drawer/button absent from base template; cart.js/checkout.js deleted; stale cart-badge CSS gone.
- [ ] "Shop by Material" → "Explore by Material"; no shop/buy/sell-for-money language on home.
- [ ] Announcement bar with payment-on-delivery copy removed.
- [ ] Enquiry flow (form + /api/enquiry/) still works end-to-end.
- [ ] Existing catalogue filters/sort (region/category/material/period/name/number) still work.
- [ ] Full test suite passes.
- [ ] collectstatic rebuilds cleanly (no references to deleted JS in templates).
- [ ] Reviewer and tester report PASS.

## Out of scope
- Keeping price info in DB (columns kept for historical data where not dropped).
- New "Price on request" messaging (site shows nothing price-related at all).
