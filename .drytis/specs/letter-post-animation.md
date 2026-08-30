# Letter & Post Animation — Digital → Analog (90s feel)

**Task:** Replace the plain "Thank you" success state of the enquiry form with a
4-scene cinematic animation in pure code (SVG/CSS keyframes/canvas/WebAudio).
The concept: a modern web form is transmitted from a 1990s CRT enquiry
terminal, dissolves into a handwritten-style typed letter, is sealed in a kraft
envelope (FROM/TO typed, wax seal), and drops into a classic red INDIA POST
post box with a "THUP". Warm nostalgic lighting, Volgo museum restraint.

## Files

| File | Change |
|---|---|
| `static/css/post.css` | NEW — stage, CRT monitor, paper, envelope, seal, postbox, receipt, keyframes |
| `static/js/post.js` | NEW — timeline state machine, typewriter, canvas particles, WebAudio SFX |
| `static/js/enquiry.js` | EDIT — success branch calls `VolgoPost.fire()` (lazy-loads assets if absent); reduced-motion fallback |
| `collection/views.py` | EDIT — `api_enquiry` returns `"number": "V.<year>.<id:03d>"` |
| `templates/house/contact.html` | EDIT — preload post.css + post.js |
| `templates/house/acquisition.html` | EDIT — preload post.css + post.js |
| `static/tests/post.test.js` | NEW — node unit tests for pure helpers |
| `house/tests.py` | EDIT — page/asset tests |
| `collection/tests.py` | EDIT — API number test |
| `run_tests.sh` | REBUILD — file is corrupt on disk (Errno 117); recreate: django tests + node tests |

## Animation timeline (total ≈ 9.3 s, skippable)

1. **Scene 1 — Terminal (≈0–1.6 s).** Full-screen warm-black stage. A CRT
   monitor (bezel, scanlines, flicker, status chip "ENQUIRY TERMINAL · VOLGO /
   2026") shows a replica of the enquiry form with the user's actual values.
   Chunky beige SUBMIT button presses with a beep; status line transmits
   progress blocks.
2. **Transition (≈1.6–1.8 s).** Form rows lift and dissolve into pixel-square
   particles (canvas, gold/ivory) while an ivory ruled letter paper rises
   beneath. Paper swish sound.
3. **Scene 2 — The letter (≈1.8–5.1 s).** Courier typewriter with blinking
   block caret types: `Dear Curator,` + the user's message (word-wrapped,
   clamped rows) + `Yours sincerely,` + name + email. Keystroke clacks. Then
   the paper curls up into a tight roll (scaleY fold + curl shading + paper
   sound).
4. **Scene 3 — The envelope (≈5.1–7.6 s).** Kraft envelope: flap opens, the
   rolled letter sliver drops into the slot, flap closes. FROM: `<user name>`
   and TO: `THE CURATOR'S DESK · VOLGO` type on char-by-char. Oxblood wax seal
   with serif V stamps down with overshoot bounce + thud.
5. **Scene 4 — INDIA POST (≈7.6–9.3 s).** Red post box (SVG: cylindrical body,
   INDIA POST band, slot, भारतीय डाक विभाग). The envelope arcs in from the
   right and drops into the slot with squash-and-stretch, a low-frequency
   "THUP" (sine sweep 80→40 Hz + noise burst), and a brief screen shake.
   Monitor does a CRT power-collapse (bright line → off).
6. **Receipt.** "ENQUIRY POSTED" museum-label receipt: wax seal mark, server
   number `V.<year>.NNN`, the house reply, Close + Replay buttons. ESC or ✕
   (Skip) cancels the timeline and shows the receipt instantly.

## Acceptance criteria

- [ ] Submit on a **valid** form with server `ok:true` starts the full-screen
      animation on contact, acquisition, AND artifact detail enquiry forms.
- [ ] Server failure / validation error → animation does NOT run; existing
      inline error behaviour unchanged.
- [ ] Envelope FROM shows the submitter's name; TO addresses the Curator's Desk.
- [ ] Letter body contains the user's message (wrapped, ≤ 5 rows, clamped).
- [ ] 90s feel: CRT bezel + scanlines + flicker + blinking caret + monospace
      terminal scene + chunky button + status chip.
- [ ] Wax seal stamps with overshoot; envelope drop has squash + THUP sound +
      screen shake.
- [ ] No external video/image/audio assets — CSS, SVG, canvas, WebAudio only.
- [ ] Skip ✕ + ESC cancel pending timers and jump to receipt; no leaked timers
      after close.
- [ ] `prefers-reduced-motion: reduce` → no animation; static receipt with
      number and reply replaces the form.
- [ ] All audio wrapped in try/catch; context created lazily; if audio is
      blocked the animation still completes silently.
- [ ] `POST /api/enquiry/` success JSON includes `number` = `V.<YYYY>.<id
      zero-padded 3>` (year from current date).
- [ ] Node unit tests pass: `wrapLines` (word wrap, width respected, long-word
      clamp), `clamp` behaviour, `formatNumber` pattern.
- [ ] Django tests pass: contact + acquisition pages reference `post.css` +
      `post.js`; both files resolve via staticfiles finders; API returns
      matching number.
- [ ] `run_tests.sh` runs both suites and exits non-zero on any failure.

## Edge cases

- Very long names → clamped with … (envelope FROM ≤ 22 chars, letter ≤ 26).
- Empty/short message → at least one typed row; never blank letter.
- Reduced motion, blocked audio, double submit (second fire ignored while
  running), rapid skip/close (timers cleared, stage removed from DOM).
- Small screens: monitor scales to `min(92vw, 680px)`; all text scales via
  clamp().
