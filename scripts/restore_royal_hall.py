import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire hero-premium section
hero_pattern = r'<section class="hero-premium".*?</style>'

royal_hall_hero = """
<section class="hero-royal-hall" id="hero">
  <!-- The Royal Hall Background -->
  <div class="hall-bg"></div>

  <!-- 90s VHS / Vintage Film Overlay -->
  <div class="vhs-scanlines"></div>
  <div class="vhs-tracking"></div>
  <div class="film-grain"></div>
  
  <div class="hall-overlay"></div>

  <div class="container" style="position: relative; z-index: 10;">
    <div class="royal-text-box reveal">
      <div class="eyebrow-line" style="justify-content: center; margin-bottom: 24px;">
        <span class="line" style="width: 50px;"></span>
        <span class="text">Private Exhibition</span>
        <span class="line" style="width: 50px;"></span>
      </div>
      <h1>Objects of Distinction</h1>
      <p class="premium-desc" style="text-align: center; margin: 0 auto 32px; color: rgba(241, 235, 221, 0.9);">
        A curated collection of antiquities, offered privately.
      </p>

      <div class="hero-ctas" style="justify-content: center;">
        <a href="/collection/" class="btn btn--gold" style="box-shadow: 0 0 30px rgba(195,162,75,0.4);">Enter the Royal Gallery</a>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-royal-hall {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding-top: var(--nav-h, 100px);
    border-bottom: 1px solid rgba(195, 162, 75, 0.3);
  }

  .hall-bg {
    position: absolute;
    inset: -20px;
    background-image: url('/static/img/custom_gallery.jpg');
    background-size: cover;
    background-position: center;
    filter: sepia(0.4) contrast(1.1) brightness(0.8);
    z-index: 0;
    /* Slow pan animation to make the hall feel alive */
    animation: panHall 30s infinite alternate ease-in-out;
  }
  
  @keyframes panHall {
    0% { transform: scale(1.05) translateX(-1%); }
    100% { transform: scale(1.05) translateX(1%); }
  }

  .hall-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(10,8,6,0.2) 0%, rgba(10,8,6,0.9) 100%);
    z-index: 1;
  }

  .royal-text-box {
    background: rgba(16, 10, 8, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(195, 162, 75, 0.4);
    padding: 60px 40px;
    border-radius: 4px;
    box-shadow: 0 40px 100px rgba(0,0,0,0.9), inset 0 0 40px rgba(195, 162, 75, 0.1);
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
  }

  .eyebrow-line {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .eyebrow-line .line {
    height: 1px;
    background: var(--gold);
  }
  .eyebrow-line .text {
    font-family: var(--font-utility);
    font-size: 12px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .royal-text-box h1 {
    font-size: clamp(48px, 7vw, 96px);
    color: #FBF8F1;
    line-height: 1.1;
    margin-bottom: 24px;
    font-family: var(--font-display);
    font-weight: 400;
    text-shadow: 
      2px 0 0 rgba(200, 20, 20, 0.8), 
      -2px 0 0 rgba(20, 20, 200, 0.8),
      0 0 40px rgba(195, 162, 75, 0.6);
    animation: rgbGlitch 4s infinite alternate;
  }

  .premium-desc {
    font-size: clamp(18px, 2vw, 24px);
    line-height: 1.6;
  }

  .reveal {
    animation: royalFadeInUp 1.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  /* 90s Effects */
  .film-grain {
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 2;
    mix-blend-mode: overlay;
    animation: filmJitter 0.3s infinite steps(2);
  }

  .vhs-scanlines {
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      to bottom,
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0) 2px,
      rgba(0, 0, 0, 0.4) 3px,
      rgba(0, 0, 0, 0.4) 4px
    );
    pointer-events: none;
    z-index: 3;
  }

  .vhs-tracking {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 12px;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    pointer-events: none;
    z-index: 4;
    animation: trackingScroll 6s infinite linear;
  }

  @keyframes filmJitter {
    0% { transform: translate(0, 0); }
    100% { transform: translate(2px, 2px); }
  }

  @keyframes trackingScroll {
    0% { top: -10%; opacity: 0; }
    10% { opacity: 0.5; }
    50% { opacity: 0.8; }
    90% { opacity: 0.5; }
    100% { top: 110%; opacity: 0; }
  }

  @keyframes rgbGlitch {
    0% { text-shadow: 2px 0 0 rgba(200, 20, 20, 0.8), -2px 0 0 rgba(20, 20, 200, 0.8), 0 0 40px rgba(195, 162, 75, 0.6); }
    20% { text-shadow: -2px 0 0 rgba(200, 20, 20, 0.8), 2px 0 0 rgba(20, 20, 200, 0.8), 0 0 40px rgba(195, 162, 75, 0.6); }
    100% { text-shadow: 1px 0 0 rgba(200, 20, 20, 0.8), -1px 0 0 rgba(20, 20, 200, 0.8), 0 0 40px rgba(195, 162, 75, 0.6); }
  }
</style>
"""

html = re.sub(hero_pattern, royal_hall_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
