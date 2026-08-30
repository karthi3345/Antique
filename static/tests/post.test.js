/* Unit tests for VolgoPost pure helpers (run with node). */
"use strict";
const fs = require("fs");
const path = require("path");

/* Load post.js with a stubbed window. */
const code = fs.readFileSync(path.join(__dirname, "..", "js", "post.js"), "utf8");
const sandbox = { window: {}, setInterval: () => 0, setTimeout: () => 0, clearInterval: () => {}, clearTimeout: () => {}, console };
/* Smoke: ensure the file parses in a browser-like harness. */
try { new Function("window", code)(sandbox.window); } catch (e) { throw new Error("post.js failed to load: " + e.message); }
if (!sandbox.window.VolgoPost || typeof sandbox.window.VolgoPost.fire !== "function") {
  throw new Error("VolgoPost not exported");
}
const { clampText, wrapLines, formatNumber } = sandbox.window.VolgoPost._internal;

let pass = 0, fail = 0;
function t(name, cond) { if (cond) { pass++; console.log("  ok  - " + name); } else { fail++; console.log("  FAIL - " + name); } }

/* clampText */
t("clampText: short string unchanged", clampText("Asha", 22) === "Asha");
t("clampText: long string truncated with ellipsis", clampText("Venkatanarasimharajuvaripeta Maritime Collectors", 22).length === 22 && clampText("Venkatanarasimharajuvaripeta Maritime Collectors", 22).endsWith("\u2026"));
t("clampText: whitespace collapsed", clampText("  Ravi   Kumar  ", 22) === "Ravi Kumar");
t("clampText: empty input safe", clampText("", 22) === "");
t("clampText: undefined input safe", clampText(undefined, 22) === "");

/* wrapLines */
const w1 = wrapLines("I would like to enquire about the bronze Nataraja in the Chennai cabinet", 30);
t("wrapLines: every line within width", w1.every((l) => l.length <= 30));
t("wrapLines: joins back to the same words", w1.join(" ") === "I would like to enquire about the bronze Nataraja in the Chennai cabinet");
const w2 = wrapLines("", 30);
t("wrapLines: empty input gives one blank line", w2.length === 1 && w2[0] === "");
const w3 = wrapLines("supercalifragilisticexpialidocious_and_more_words", 10);
t("wrapLines: over-long word is cut to width", w3[0].length === 10);

/* formatNumber */
t("formatNumber: zero-pads to 3 digits", formatNumber(7, 2026) === "V.2026.007");
t("formatNumber: 3-digit id unchanged", formatNumber(123, 2026) === "V.2026.123");
t("formatNumber: 4-digit id not truncated", formatNumber(1234, 2026) === "V.2026.1234");

console.log(`\npost.test.js: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
