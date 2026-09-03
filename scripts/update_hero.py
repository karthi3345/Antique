import re

with open('templates/collection/home.html', encoding='utf-8') as f:
    html = f.read()

# Completely redesign the hero section HTML
hero_pattern = r'<section class="hero" id="hero".*?</section>'

new_hero = """<section class="hero-museum" id="hero" aria-label="Featured object — {{ hero.name }}">
  <div class="museum-wall-texture"></div>
  <div class="container">
    <div class="hero-grid">
      <!-- Left: Museum Plaque (Text) -->
      <div class="hero-plaque">
        <div class="plaque-inner">
          <p class="hero-eyebrow">{{ hero.label_number }} &mdash; {% if hero.featured %}Exhibition Centerpiece{% else %}Recent Accession{% endif %}</p>
          <h1>{{ hero.name }}</h1>
          <p class="hero-desc">{{ hero.subtitle|default:"An object examined, documented, and offered — with its history intact." }}</p>
          <div class="plaque-meta">
            <span class="meta-item"><strong>Origin</strong><br>{{ hero.region }}</span>
            <span class="meta-item"><strong>Era</strong><br>{{ hero.period }}</span>
            <span class="meta-item"><strong>Medium</strong><br>{{ hero.material }}</span>
          </div>
          <div class="hero-ctas">
            <a href="/collection/" class="btn btn--solid">Explore Exhibition</a>
            <a href="/acquisition/" class="btn btn--outline" style="border-color: #C3A24B; color: #C3A24B;">Private Acquisition</a>
          </div>
        </div>
      </div>
      
      <!-- Right: The Framed Artifact -->
      <div class="hero-exhibit">
        <div class="exhibit-spotlight"></div>
        <div class="exhibit-frame">
          <img src="/static/img/objects/{{ hero.object_number|stringformat:'03d' }}/{{ hero.hero_frame|stringformat:'02d' }}.webp"
               alt="{{ hero.name }}" fetchpriority="high" decoding="async">
          <div class="glass-reflection"></div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  /* The Museum Wall */
  .hero-museum {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: #0a0806; /* Dark gallery base */
    overflow: hidden;
    padding-top: var(--nav-h, 100px);
  }
  .museum-wall-texture {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 75% 50%, #221c16 0%, #0a0806 60%);
    opacity: 0.9;
  }
  .museum-wall-texture::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
  }

  /* Grid Layout */
  .hero-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
    padding: 40px 0;
  }

  /* The Plaque (Text) */
  .hero-plaque {
    background: rgba(20, 17, 13, 0.6);
    border: 1px solid rgba(195, 162, 75, 0.15);
    border-radius: 4px;
    padding: 48px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    animation: royalFadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  .hero-plaque h1 {
    font-size: clamp(40px, 4.5vw, 64px);
    color: #F1EBDD;
    line-height: 1.1;
    margin-bottom: 24px;
    font-family: var(--font-display);
  }
  .hero-eyebrow {
    font-family: var(--font-utility);
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .hero-eyebrow::before {
    content: "";
    width: 30px; height: 1px;
    background: var(--gold);
  }
  .hero-desc {
    font-size: 18px;
    color: rgba(241, 235, 221, 0.8);
    line-height: 1.6;
    margin-bottom: 32px;
  }
  .plaque-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding-top: 24px;
    border-top: 1px solid rgba(195, 162, 75, 0.2);
    margin-bottom: 40px;
  }
  .meta-item {
    font-size: 14px;
    color: rgba(241, 235, 221, 0.9);
  }
  .meta-item strong {
    font-family: var(--font-utility);
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold-pale);
    display: block;
    margin-bottom: 4px;
  }
  .hero-ctas {
    display: flex;
    gap: 20px;
  }

  /* The Exhibit (Image) */
  .hero-exhibit {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 1000px;
    animation: royalFadeInUp 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  
  .exhibit-spotlight {
    position: absolute;
    top: -20%; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 500px;
    background: radial-gradient(ellipse at top, rgba(195, 162, 75, 0.15) 0%, rgba(0,0,0,0) 70%);
    pointer-events: none;
    z-index: 0;
  }

  .exhibit-frame {
    position: relative;
    z-index: 1;
    width: 80%;
    max-width: 500px;
    aspect-ratio: 4/5;
    background: #111;
    /* Museum Gold Frame */
    border: 16px solid #1a1612;
    box-shadow: 
      0 0 0 4px var(--gold-deep),
      inset 0 0 0 2px var(--gold),
      0 30px 60px rgba(0,0,0,0.9),
      -20px 20px 40px rgba(0,0,0,0.6);
    border-radius: 2px;
    transform: rotateY(-8deg) rotateX(4deg);
    transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .exhibit-frame:hover {
    transform: rotateY(0deg) rotateX(0deg) scale(1.05);
  }
  
  .exhibit-frame img {
    width: 100%; height: 100%;
    object-fit: cover;
    filter: contrast(1.1) saturate(1.1);
  }

  .glass-reflection {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(
      135deg,
      rgba(255,255,255,0.15) 0%,
      rgba(255,255,255,0) 40%,
      rgba(255,255,255,0.05) 100%
    );
  }

  @media (max-width: 992px) {
    .hero-grid {
      grid-template-columns: 1fr;
      text-align: center;
    }
    .hero-plaque { padding: 32px 24px; }
    .hero-eyebrow { justify-content: center; }
    .hero-eyebrow::before { display: none; }
    .hero-ctas { justify-content: center; }
    .exhibit-frame { transform: none; width: 100%; }
  }
</style>
"""

# Replace the hero block using regex DOTALL
html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
