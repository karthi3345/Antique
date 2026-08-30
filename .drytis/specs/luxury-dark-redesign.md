# Luxury Dark Redesign — "Modern Luxury"

## Goal
Replace the ivory/cream French-boutique theme with a dark, cinematic modern-luxury
aesthetic: obsidian black surfaces, champagne-gold accents, large serif display
type, refined motion. All existing functionality (catalogue filters, enquiry
forms, carousels, testimonial rotation, mobile nav) must keep working unchanged.

## Scope — files to change
- `static/css/volgo.css` — full rewrite of the design-token layer and component
  styles to a dark theme. Keep all class names identical so templates/JS keep working.
- `templates/base.html` — announce bar, header (now transparent-over-hero, blur
  on scroll), footer, font link update, favicon link stays.
- `static/img/favicon.svg` — gold monogram on dark.
- `static/css/volgo.css` (carousel/hero sections) — restyled for dark.
- `templates/collection/home.html` — hero markup adjustments only if needed
  for styling hooks; JS logic unchanged.
- `templates/house/chronicles.html` — remove hardcoded `#3A342A` /
  `--hairline-light` inline styles (light-theme leftovers).
- Inline `style` references to light tokens in other templates
  (`--hairline-dark`, `#3A342A`) get remapped to dark-theme equivalents.
- `static/js/catalogue.js` — card markup unchanged (classes identical).
- `static/js/enquiry.js` — unchanged (uses classes only).

## Design tokens (dark)
- Surfaces: `--ink` #0B0A08 (page), panels #12100C / #171410
- Gold: `--gold` #C9A227 (primary accent), `--gold-pale` #E8CE7E, `--gold-deep` #9A7B1E
- Text: ivory `#F2EDE3`, muted `#A79E8D`, soft `#CFC7B6`
- Hairlines: rgba(201,162,39,.25) gold-tinted, strong rgba(201,162,39,.45)
- Fonts unchanged (Cormorant Garamond / Newsreader / Archivo)

## Acceptance criteria
- [ ] Page background is obsidian dark on every page (home, catalogue, artifact,
      house, chronicles index+article, acquisition, contact).
- [ ] Champagne-gold accents on interactive elements: nav underline, buttons,
      timeline markers, hero dots, carousel explore pills.
- [ ] Header starts transparent over hero; on scroll becomes dark glass
      (rgba(11,10,8,.92) + backdrop blur) with gold hairline border.
- [ ] Hero: full-bleed object photography with a dark gradient shade (left-to-right,
      dark → transparent), gold eyebrow with rule, ivory display type.
- [ ] Cards (catalogue + carousel): dark panels, gold hairline borders,
      hover raises a soft gold glow/shadow and image scale.
- [ ] Forms: dark inputs with gold focus underline; labels same.
- [ ] Reading room (chronicles): deep parchment-dark panel, ivory text, gold rules.
- [ ] Footer: darkest panel with gold wordmark.
- [ ] WhatsApp float styled dark+gold (no green) to match brand.
- [ ] No light-theme color literals remain in templates (grep #3A342A, #F3EDDF,
      ivory backgrounds, --hairline-light).
- [ ] Mobile nav: dark glass panel, gold links.
- [ ] All JS-driven components still work (hero carousel, category carousel,
      catalogue fetch/filters, enquiry form submit, testimonials).
- [ ] Django test suite passes (no backend change, but must not regress).
- [ ] Contrast: body text ≥ 4.5:1 on dark backgrounds.
- [ ] Reduced-motion still honored.

## Tests
- Existing Django suite (`run_tests.sh`) — must stay green (no logic change).
- Browser verification via tester agent on preview URL: home, catalogue filter,
      artifact page, enquiry form (validation state), chronicles, contact.
