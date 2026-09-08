/* Volgo — base behaviours: header state, mobile menu, search overlay,
   scroll reveals (fade-up, clip, parallax). Reduced-motion honored. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     Header gains ground on scroll
     ------------------------------------------------------------------ */
  var header = document.getElementById("site-header");
  var onScrollHeader = function () {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  /* ------------------------------------------------------------------
     Mobile menu — full-screen editorial navigation
     ------------------------------------------------------------------ */
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  var toggleLabel = toggle ? toggle.querySelector(".nav-toggle-label") : null;

  function setMenu(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.classList.toggle("is-open", open);
    if (toggleLabel) toggleLabel.textContent = open ? "Close" : "Menu";
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 720) setMenu(false);
    });
  }

  /* ------------------------------------------------------------------
     Active nav link
     ------------------------------------------------------------------ */
  var here = location.pathname;
  document.querySelectorAll(".site-nav a[data-nav]").forEach(function (a) {
    var key = a.getAttribute("data-nav");
    if (key === "collection" && here.indexOf("/collection") === 0) a.classList.add("active");
    if (key === "the-house" && here.indexOf("/the-house") === 0) a.classList.add("active");
    if (key === "chronicles" && here.indexOf("/chronicles") === 0) a.classList.add("active");
  });

  /* ------------------------------------------------------------------
     Search overlay
     ------------------------------------------------------------------ */
  var searchBtn = document.getElementById("nav-search");
  var overlay = document.getElementById("search-overlay");
  var searchInput = document.getElementById("search-input");
  var searchClose = document.getElementById("search-close");
  var searchForm = document.getElementById("search-form");

  function openSearch() {
    if (!overlay) return;
    overlay.hidden = false;
    requestAnimationFrame(function () {
      overlay.classList.add("is-open");
      if (searchInput) {
        searchInput.value = new URLSearchParams(location.search).get("q") || "";
        searchInput.focus();
      }
    });
  }
  function closeSearch() {
    if (!overlay) return;
    overlay.classList.remove("is-open");
    setTimeout(function () { overlay.hidden = true; }, 400);
  }

  if (searchBtn && overlay) {
    searchBtn.addEventListener("click", openSearch);
    if (searchClose) searchClose.addEventListener("click", closeSearch);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && overlay.classList.contains("is-open")) closeSearch();
    });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeSearch();
    });
    var hints = overlay.querySelectorAll("[data-term]");
    hints.forEach(function (b) {
      b.addEventListener("click", function () {
        if (searchInput) {
          searchInput.value = b.getAttribute("data-term");
          if (searchForm) searchForm.submit();
        }
      });
    });
    // "/" opens search
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) {
        e.preventDefault();
        openSearch();
      }
    });
  }

  /* ------------------------------------------------------------------
     Scroll reveals — fade-up, clip, group stagger; parallax on hero
     ------------------------------------------------------------------ */
  var revealEls = document.querySelectorAll(".reveal, .reveal-clip, .reveal-group");
  if (!reduceMotion && "IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Gentle hero parallax — transform only, rAF-throttled */
  var heroMedia = document.querySelector(".hero-media img");
  if (heroMedia && !reduceMotion) {
    var ticking = false;
    var updateHero = function () {
      var y = window.scrollY;
      if (y < window.innerHeight * 1.2) {
        heroMedia.style.setProperty("--hero-shift", (y * 0.12).toFixed(1) + "px");
      }
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(updateHero); }
    }, { passive: true });
  }

  /* Lazy-load below-the-fold card images by data attribute */
  document.querySelectorAll("img[data-src]").forEach(function (img) {
    img.src = img.getAttribute("data-src");
    img.removeAttribute("data-src");
  });
})();

  /* ------------------------------------------------------------------
     Neon Atmosphere: Audio & Particles
     ------------------------------------------------------------------ */
  var searchOverlay = document.getElementById("search-overlay");
  var searchAudio = document.getElementById("search-audio");
  var soundToggle = document.getElementById("search-sound-toggle");
  var particlesContainer = document.getElementById("particles-container");
  var searchBtnNode = document.getElementById("nav-search");
  var searchCloseNode = document.getElementById("search-close");

  if (soundToggle && searchAudio) {
    var iconOn = soundToggle.querySelector(".icon-sound-on");
    var iconOff = soundToggle.querySelector(".icon-sound-off");
    searchAudio.volume = 0.4;
    var audioUserEnabled = false;

    soundToggle.addEventListener("click", function() {
      if (searchAudio.paused) {
        searchAudio.volume = 0;
        searchAudio.play().then(function() {
          audioUserEnabled = true;
          var fade = setInterval(function() {
            if (searchAudio.volume < 0.35) {
              searchAudio.volume += 0.05;
            } else {
              clearInterval(fade);
            }
          }, 100);
          iconOff.style.display = "none";
          iconOn.style.display = "block";
        }).catch(function(e) { console.error("Audio play failed:", e); });
      } else {
        audioUserEnabled = false;
        var fade = setInterval(function() {
          if (searchAudio.volume > 0.05) {
            searchAudio.volume -= 0.05;
          } else {
            clearInterval(fade);
            searchAudio.pause();
            iconOn.style.display = "none";
            iconOff.style.display = "block";
          }
        }, 100);
      }
    });

    if (searchBtnNode) {
      searchBtnNode.addEventListener("click", function() {
        if (true) {
          searchAudio.volume = 0.4; searchAudio.play().then(()=>{iconOff.style.display='none';iconOn.style.display='block';audioUserEnabled=true;}).catch(function(){});
        }
      });
    }
    if (searchCloseNode) {
      searchCloseNode.addEventListener("click", function() {
        searchAudio.pause();
      });
    }
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && searchOverlay && searchOverlay.classList.contains("is-open")) {
        searchAudio.pause();
      }
    });
    if (searchOverlay) {
      searchOverlay.addEventListener("click", function (e) {
        if (e.target === searchOverlay) searchAudio.pause();
      });
    }
  }
  
  if (particlesContainer && searchOverlay) {
    function createParticle() {
      if (!searchOverlay.classList.contains("is-open")) return;
      var p = document.createElement("div");
      p.className = "particle";
      p.style.left = Math.random() * 100 + "%";
      p.style.top = (80 + Math.random() * 20) + "%";
      var size = Math.random() * 3 + 1;
      p.style.width = size + "px";
      p.style.height = size + "px";
      p.style.animationDuration = (Math.random() * 3 + 4) + "s";
      particlesContainer.appendChild(p);
      setTimeout(function() { p.remove(); }, 7000);
    }
    setInterval(createParticle, 400);
  }

