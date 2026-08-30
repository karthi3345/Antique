/* Volgo - The Letter & The Post.
   4-scene code animation (form > letter > envelope > INDIA POST) fired after
   a successful enquiry. Pure DOM/SVG/canvas/WebAudio. Exposes VolgoPost.fire(). */
(function (global) {
  "use strict";

  /* ---------------- pure helpers ---------------- */
  function clampText(s, n) {
    s = String(s || "").replace(/\s+/g, " ").trim();
    return s.length > n ? s.slice(0, n - 1).replace(/\s+$/, "") + "\u2026" : s;
  }

  function wrapLines(text, width) {
    var words = String(text || "").replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
    var lines = [];
    var cur = "";
    if (!words.length) { return [""]; }
    words.forEach(function (w) {
      var piece = w.length > width ? w.slice(0, width) : w;
      if (!cur) { cur = piece; }
      else if ((cur + " " + piece).length <= width) { cur += " " + piece; }
      else { lines.push(cur); cur = piece; }
    });
    if (cur) { lines.push(cur); }
    return lines;
  }

  function formatNumber(id, year) {
    return "V." + String(year) + "." + String(id).padStart(3, "0");
  }

  /* ---------------- WebAudio (all guarded) ---------------- */
  var actx = null;
  function ctx() {
    try {
      if (!actx) { actx = new (global.AudioContext || global.webkitAudioContext)(); }
      if (actx.state === "suspended") { actx.resume(); }
      return actx;
    } catch (e) { return null; }
  }
  function env(g, t0, a, d, peak) {
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(peak, t0 + a);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + a + d);
  }
  function tone(type, f0, f1, dur, peak) {
    var c = ctx(); if (!c) { return; }
    try {
      var o = c.createOscillator(), g = c.createGain();
      o.type = type;
      o.frequency.setValueAtTime(f0, c.currentTime);
      if (f1) { o.frequency.exponentialRampToValueAtTime(f1, c.currentTime + dur); }
      env(g, c.currentTime, 0.008, dur, peak || 0.16);
      o.connect(g).connect(c.destination);
      o.start(); o.stop(c.currentTime + dur + 0.05);
    } catch (e) {}
  }
  function noise(dur, peak, hz) {
    var c = ctx(); if (!c) { return; }
    try {
      var n = Math.floor(c.sampleRate * dur);
      var buf = c.createBuffer(1, n, c.sampleRate);
      var data = buf.getChannelData(0);
      for (var i = 0; i < n; i++) { data[i] = (Math.random() * 2 - 1) * (1 - i / n); }
      var src = c.createBufferSource(); src.buffer = buf;
      var g = c.createGain(); env(g, c.currentTime, 0.004, dur, peak || 0.12);
      var f = c.createBiquadFilter(); f.type = "bandpass"; f.frequency.value = hz || 900; f.Q.value = 0.8;
      src.connect(f).connect(g).connect(c.destination);
      src.start();
    } catch (e) {}
  }
  var SFX = {
    beep: function () { tone("square", 660, 0, 0.09, 0.05); },
    click: function () { noise(0.03, 0.06, 2400); },
    clack: function () { noise(0.02, 0.05, 3200); tone("square", 1900, 0, 0.015, 0.02); },
    paper: function () { noise(0.4, 0.07, 1600); },
    stamp: function () { tone("sine", 120, 55, 0.16, 0.5); noise(0.06, 0.2, 500); },
    thup: function () { tone("sine", 85, 38, 0.22, 0.7); noise(0.09, 0.3, 260); },
  };

  /* ---------------- small DOM utils ---------------- */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (html !== undefined) { e.innerHTML = html; }
    return e;
  }
  function esc(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------------- typewriter ---------------- */
  function typeInto(node, text, cps, tick, done) {
    var i = 0;
    var caret = el("span", "typ-caret");
    node.textContent = "";
    node.appendChild(caret);
    var id = setInterval(function () {
      if (i >= text.length) {
        clearInterval(id);
        if (caret.parentNode) { caret.remove(); }
        if (done) { done(); }
        return;
      }
      var ch = text.charAt(i);
      node.insertBefore(document.createTextNode(ch), caret);
      i += 1;
      if (tick && i % 2 === 0) { tick(); }
    }, Math.max(18, 1000 / (cps || 14)));
    return id;
  }

  /* ---------------- scene builders ---------------- */
  function postBoxSVG() {
    return '' +
    '<svg viewBox="0 0 300 400" role="img" aria-label="Classic red post box">' +
      '<defs>' +
        '<linearGradient id="vpRed" x1="0" y1="0" x2="1" y2="0">' +
          '<stop offset="0" stop-color="#8f1f14"/><stop offset=".38" stop-color="#c0392b"/><stop offset=".62" stop-color="#ab2c1e"/><stop offset="1" stop-color="#7c1a10"/>' +
        '</linearGradient>' +
        '<linearGradient id="vpRedDark" x1="0" y1="0" x2="1" y2="0">' +
          '<stop offset="0" stop-color="#701509"/><stop offset=".5" stop-color="#a02a1a"/><stop offset="1" stop-color="#5c1008"/>' +
        '</linearGradient>' +
        '<linearGradient id="vpBrass" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="#e6c987"/><stop offset=".5" stop-color="#b8934a"/><stop offset="1" stop-color="#8a6c30"/>' +
        '</linearGradient>' +
        '<linearGradient id="vpSlot" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="#1a0503"/><stop offset="1" stop-color="#3a0d06"/>' +
        '</linearGradient>' +
      '</defs>' +
      '<!-- cap -->' +
      '<path d="M24 96 C24 44 150 18 150 18 C150 18 276 44 276 96 L276 106 L24 106 Z" fill="url(#vpRedDark)"/>' +
      '<rect x="24" y="98" width="252" height="10" rx="4" fill="url(#vpBrass)" opacity=".92"/>' +
      '<!-- body -->' +
      '<path d="M40 106 L260 106 C264 106 268 110 268 116 L268 378 C268 384 264 388 258 388 L42 388 C36 388 32 384 32 378 L32 116 C32 110 36 106 40 106 Z" fill="url(#vpRed)"/>' +
      '<!-- slot plate -->' +
      '<rect x="62" y="128" width="176" height="46" rx="10" fill="url(#vpRedDark)"/>' +
      '<rect x="80" y="142" width="140" height="14" rx="7" fill="url(#vpSlot)"/>' +
      '<!-- INDIA POST band -->' +
      '<rect x="32" y="196" width="236" height="54" fill="#F3E4C0" opacity=".96"/>' +
      '<text x="150" y="221" text-anchor="middle" font-family="Georgia, serif" font-size="22" font-weight="700" letter-spacing="3" fill="#7c1410">INDIA POST</text>' +
      '<text x="150" y="241" text-anchor="middle" font-family="Georgia, serif" font-size="12" letter-spacing="1.5" fill="#5c4a24">&#2349;&#2366;&#2352;&#2340;&#2368;&#2351; &#2337;&#2366;&#2325; &#2357;&#2367;&#2349;&#2366;&#2327;</text>' +
      '<!-- collection plate -->' +
      '<rect x="60" y="270" width="180" height="34" rx="6" fill="#F3E4C0" opacity=".9"/>' +
      '<text x="150" y="292" text-anchor="middle" font-family="Georgia, serif" font-size="13" letter-spacing="2" fill="#7c1410">LETTER BOX</text>' +
      '<!-- base shadow -->' +
      '<ellipse cx="150" cy="392" rx="132" ry="7" fill="rgba(0,0,0,.45)"/>' +
    '</svg>';
  }

  function monitorHTML(d) {
    return '<div class="vp-desk"></div>' +
      '<div class="vp-monitor" id="vp-monitor">' +
        '<div class="vp-screen">' +
          '<div class="vp-term">' +
            '<div class="vp-term-head"><span class="vp-term-title">VOLGO ENQUIRY TERMINAL</span><span>EST. MMXXVI</span></div>' +
            '<div class="vp-term-row"><span class="k">NAME</span><span class="v">' + esc(d.name) + '</span></div>' +
            '<div class="vp-term-row"><span class="k">EMAIL</span><span class="v">' + esc(d.email) + '</span></div>' +
            (d.phone ? '<div class="vp-term-row"><span class="k">TEL</span><span class="v">' + esc(d.phone) + '</span></div>' : '') +
            '<div class="vp-term-row"><span class="k">TEXT</span><span class="v">' + esc(clampText(d.message, 34)) + '</span></div>' +
            '<button type="button" class="vp-submit" id="vp-submit">SUBMIT</button>' +
            '<div class="vp-term-status"><span>TX</span><span class="bar" id="vp-bar"></span><span class="vp-term-cursor"></span></div>' +
          '</div>' +
          '<div class="vp-scan"></div>' +
        '</div>' +
      '</div>';
  }

  function envelopeHTML(d) {
    return '<div class="vp-env">' +
        '<div class="vp-letter-sliver" id="vp-sliver"></div>' +
        '<div class="vp-flap" id="vp-flap"></div>' +
        '<div class="vp-env-face">' +
          '<div class="row"><span class="k">FROM:</span><span class="addr" id="vp-from"></span></div>' +
          '<div class="row"><span class="k">TO:</span><span class="addr" id="vp-to"></span></div>' +
        '</div>' +
        '<div class="vp-airmail"></div>' +
        '<div class="vp-stamp"><svg viewBox="0 0 24 24" fill="none" stroke="#7a2e1d" stroke-width="1.4"><path d="M12 3l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.4 6.8 19.2l1-5.9L3.5 9.2l5.9-.8z"/></svg><span class="val"><b>V</b>MMXXVI</span></div>' +
        '<div class="vp-seal" id="vp-seal"><span class="vp-seal-v">V</span></div>' +
      '</div>';
  }

  /* ---------------- particles (form dissolve) ---------------- */
  function particles(canvas, r) {
    var ctx2d = null;
    try { ctx2d = canvas.getContext("2d"); } catch (e) { return; }
    if (!ctx2d) { return; }
    var W = canvas.width = Math.max(300, canvas.offsetWidth);
    var H = canvas.height = Math.max(300, canvas.offsetHeight);
    var N = 130;
    var cols = ["#d9c48a", "#e6ddc2", "#c3a24b", "#a89a6d", "#8a7f5f"];
    var list = [];
    for (var i = 0; i < N; i++) {
      list.push({
        x: r.left + Math.random() * r.width,
        y: r.top + Math.random() * r.height,
        vx: (Math.random() - 0.5) * 1.4,
        vy: -0.6 - Math.random() * 1.2,
        s: 2 + Math.floor(Math.random() * 4),
        life: 1,
        decay: 0.006 + Math.random() * 0.008,
        c: cols[Math.floor(Math.random() * cols.length)],
      });
    }
    var raf = 0;
    function frame() {
      ctx2d.clearRect(0, 0, W, H);
      var alive = false;
      for (var i = 0; i < N; i++) {
        var p = list[i];
        if (p.life <= 0) { continue; }
        alive = true;
        p.x += p.vx; p.y += p.vy; p.vy += 0.015; p.life -= p.decay;
        ctx2d.globalAlpha = Math.max(0, p.life);
        ctx2d.fillStyle = p.c;
        ctx2d.fillRect(p.x, p.y, p.s, p.s);
      }
      ctx2d.globalAlpha = 1;
      if (alive) { raf = requestAnimationFrame(frame); }
    }
    frame();
    return { stop: function () { if (raf) { cancelAnimationFrame(raf); } } };
  }

  /* ---------------- fire() — the timeline ---------------- */
  var running = false;
  var timers = [];
  function after(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function clearTimers() {
    timers.forEach(function (t) { clearTimeout(t); });
    timers = [];
  }

  function fire(d) {
    if (running) { return; }
    var reduce = false;
    try { reduce = global.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
    if (reduce) { return staticReceipt(d, true); }

    running = true;
    var stage = el("div", "vp-stage");
    stage.innerHTML =
      '<button type="button" class="vp-skip" id="vp-skip">Skip ✕</button>' +
      '<div class="vp-chip"><span class="vp-led"></span> ENQUIRY TERMINAL · VOLGO</div>' +
      '<canvas id="vp-particles"></canvas>' +
      '<div id="vp-scene"></div>';
    document.body.appendChild(stage);
    var scene = stage.querySelector("#vp-scene");
    var reduced = false;

    function skip() {
      if (reduced) { return; }
      reduced = true;
      clearTimers();
      var sp = particlesRun; if (sp) { sp.stop(); }
      showReceipt(true);
    }

    function showReceipt(instant) {
      var old = stage.querySelector(".vp-receipt");
      if (old) { return; }
      var r = el("div", "vp-receipt");
      r.innerHTML =
        '<div class="vp-r-label">VOLGO · THE POST DESK</div>' +
        '<div class="vp-r-title">Enquiry posted</div>' +
        '<div class="vp-r-num" id="vp-num">' + esc(d.number || "") + '</div>' +
        '<div class="vp-r-rule"></div>' +
        '<div class="vp-r-reply">' + esc(d.reply || "Thank you. A member of the house will respond within one working day.") + '</div>' +
        '<div class="vp-r-actions">' +
          '<button type="button" class="vp-r-btn vp-r-btn--solid" id="vp-close">Close</button>' +
          '<button type="button" class="vp-r-btn" id="vp-replay">Replay</button>' +
        '</div>' +
        '<div class="vp-r-mark"><span class="dot">V</span><span>Sealed · INDIA POST · MMXXVI</span></div>';
      stage.appendChild(r);
      requestAnimationFrame(function () { r.classList.add("is-visible"); });
      var c = r.querySelector("#vp-close");
      var p = r.querySelector("#vp-replay");
      if (c) { c.addEventListener("click", closeStage); }
      if (p) { p.addEventListener("click", function () {
        closeStage(); setTimeout(function () { fire(d); }, 60);
      }); }
      if (instant) {
        r.classList.add("is-visible");
        r.style.animation = "none";
      }
    }

    function closeStage() {
      clearTimers();
      var sp = particlesRun; if (sp) { sp.stop(); }
      stage.remove();
      running = false;
      document.removeEventListener("keydown", onKey);
    }

    function onKey(e) { if (e.key === "Escape") { skip(); } }

    var particlesRun = null;
    var T = 0;
    var SEQ = [
      /* scene 1 — terminal, press SUBMIT, transmit */
      [200, function () { scene.innerHTML = monitorHTML(d); SFX.click(); }],
      [700, function () {
        var m = stage.querySelector("#vp-monitor");
        var b = stage.querySelector("#vp-submit");
        if (m) { m.classList.add("is-flickering"); }
        if (b) { b.classList.add("is-pressed"); SFX.beep(); }
      }],
      [1250, function () {
        var bar = stage.querySelector("#vp-bar");
        if (bar) {
          var i = 0;
          var id = setInterval(function () {
            bar.textContent += "\u2588";
            i += 1;
            if (i >= 7) { clearInterval(id); }
          }, 90);
          timers.push(id);
        }
      }],
      /* transition — dissolve into pixels */
      [2050, function () {
        var mon = stage.querySelector("#vp-monitor");
        var cv = stage.querySelector("#vp-particles");
        if (mon && cv) { particlesRun = particles(cv, mon.getBoundingClientRect()); }
        if (mon) { mon.style.transition = "opacity 300ms"; mon.style.opacity = "0"; }
      }],
      [2300, function () { scene.innerHTML = ""; }],
      /* scene 2 — the letter types itself */
      [2400, function () {
        scene.innerHTML = '<div class="vp-paper-wrap"><div class="vp-paper" id="vp-paper"><div class="vp-paper-lines" id="vp-lines"></div><span class="vp-caret-lg" id="vp-lcaret" style="display:none"></span></div></div>';
        SFX.paper();
      }],
      [2600, function () {
        var lines = stage.querySelector("#vp-lines");
        if (!lines) { return; }
        var name = clampText(d.name, 26);
        var rows = wrapLines(d.message, 30).slice(0, 5);
        if (!rows.length || rows.join(" ").length < 3) { rows = ["(a brief note)"]; }
        var full = "Dear Curator,\n" + rows.join("\n") + "\n\nYours sincerely,\n" + name;
        var lc = stage.querySelector("#vp-lcaret");
        if (lc) { lc.style.display = "inline-block"; }
        var typeTimer = typeInto(lines, full, 22, SFX.clack, function () {
          if (lc) { lc.style.display = "none"; }
        });
        timers.push(typeTimer);
      }],
      /* roll the letter up */
      [5800, function () {
        var paper = stage.querySelector("#vp-paper");
        if (paper) { paper.classList.add("is-rolling"); SFX.paper(); }
      }],
      [6800, function () {
        var paper = stage.querySelector("#vp-paper");
        if (paper) { paper.classList.add("is-gone"); }
      }],
      /* scene 3 — the envelope */
      [7200, function () {
        scene.innerHTML = '<div class="vp-env-wrap">' + envelopeHTML(d) + '</div>';
        SFX.click();
      }],
      [7500, function () { var f = stage.querySelector("#vp-flap"); if (f) { f.classList.add("is-open"); } }],
      [7700, function () { var s = stage.querySelector("#vp-sliver"); if (s) { s.style.opacity = "1"; SFX.paper(); } }],
      [7950, function () { var f = stage.querySelector("#vp-flap"); if (f) { f.classList.add("is-closed"); SFX.click(); } }],
      /* FROM / TO typewriter */
      [8300, function () {
        var n = stage.querySelector("#vp-from");
        if (n) { timers.push(typeInto(n, clampText(d.name, 22), 20, SFX.clack)); }
      }],
      [9200, function () {
        var n = stage.querySelector("#vp-to");
        if (n) { timers.push(typeInto(n, "THE CURATOR'S DESK · VOLGO", 20, SFX.clack)); }
      }],
      /* wax seal */
      [10300, function () {
        var s = stage.querySelector("#vp-seal");
        if (s) { s.classList.add("is-pressed"); SFX.stamp(); }
      }],
      /* scene 4 — post box + envelope flies in */
      [10800, function () {
        scene.innerHTML =
          '<div class="vp-post-wrap">' +
            '<div class="vp-post">' + postBoxSVG() +
              '<div class="vp-post-label">INDIA POST · MMXXVI</div>' +
            '</div>' +
          '</div>' +
          '<div class="vp-env-fly" id="vp-fly"><div class="vp-fly-body"></div><div class="vp-fly-flap"></div><div class="vp-fly-seal"></div></div>' +
          '<div class="vp-slot-flag" id="vp-flag"></div>';
        SFX.paper();
      }],
      [11200, function () { var f = stage.querySelector("#vp-fly"); if (f) { f.style.opacity = "1"; } }],
      [11400, function () {
        var fly = stage.querySelector("#vp-fly");
        if (fly) {
          fly.style.animation = "vp-fly 880ms cubic-bezier(.32,0,.8,.46) forwards";
          fly.classList.add("is-flying");
        }
      }],
      [11900, function () {
        var fly = stage.querySelector("#vp-fly");
        if (fly) { fly.classList.add("is-dropping"); }
      }],
      /* THUP */
      [12150, function () {
        SFX.thup();
        stage.classList.add("is-shaking");
        var flag = stage.querySelector("#vp-flag");
        if (flag) { flag.classList.add("is-flipped"); }
        var mon2 = stage.querySelector("#vp-monitor");
        if (mon2) { mon2.classList.add("is-off"); }
      }],
      [12600, function () { stage.classList.remove("is-shaking"); }],
      [12800, function () { var s2 = stage.querySelector("#vp-seal"); if (s2) { s2.remove(); } }],
      [12900, function () { showReceipt(false); }],
    ];

    SEQ.forEach(function (step) { after(step[0], step[1]); });
    stage.querySelector("#vp-skip").addEventListener("click", skip);
    document.addEventListener("keydown", onKey);
  }

  /* ---------------- static fallback (reduced motion) ---------------- */
  function staticReceipt(d, append) {
    var stage = el("div", "vp-stage");
    stage.style.animation = "none";
    stage.style.opacity = "1";
    stage.innerHTML =
      '<div class="vp-chip"><span class="vp-led"></span> ENQUIRY RECEIVED · VOLGO</div>' +
      '<div class="vp-receipt is-visible" style="animation:none;">' +
        '<div class="vp-r-label">VOLGO · THE POST DESK</div>' +
        '<div class="vp-r-title">Enquiry posted</div>' +
        '<div class="vp-r-num">' + esc(d.number || "") + '</div>' +
        '<div class="vp-r-rule"></div>' +
        '<div class="vp-r-reply">' + esc(d.reply || "Thank you. A member of the house will respond within one working day.") + '</div>' +
        '<div class="vp-r-actions"><button type="button" class="vp-r-btn vp-r-btn--solid" id="vp-close2">Close</button></div>' +
        '<div class="vp-r-mark"><span class="dot">V</span><span>Sealed · INDIA POST · MMXXVI</span></div>' +
      '</div>';
    document.body.appendChild(stage);
    var c = stage.querySelector("#vp-close2");
    if (c) { c.addEventListener("click", function () { stage.remove(); }); }
    return stage;
  }

  /* ---------------- exports ---------------- */
  global.VolgoPost = {
    fire: fire,
    _internal: { clampText: clampText, wrapLines: wrapLines, formatNumber: formatNumber },
  };
})(window);
