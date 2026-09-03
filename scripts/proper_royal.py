import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the hero-royal-hall section
hero_pattern = r'<section class="hero-royal-hall".*?</style>'

proper_royal_hero = """
<section class="hero-proper-royal" id="hero">
  <!-- Gorgeous Dark Royal Palace Background -->
  <div class="royal-palace-bg"></div>
  
  <!-- Royal Darkness Overlay to make text pop -->
  <div class="royal-overlay"></div>

  <!-- 90s Vintage Touch -->
  <div class="film-grain"></div>

  <div class="container hero-content">
    
    <!-- Floating Artifact Showcase -->
    <div class="royal-showcase reveal">
      <div class="artifact-halo"></div>
      <img src="/static/img/objects/{{ hero.object_number|stringformat:'03d' }}/{{ hero.hero_frame|stringformat:'02d' }}.webp" 
           alt="{{ hero.name }}" class="showcase-img" fetchpriority="high">
    </div>

    <!-- Elegant Royal Text -->
    <div class="royal-typography reveal">
      <p class="eyebrow">{{ hero.label_number|default:"Maison d'Antiquités" }}</p>
      <h1>{{ hero.name }}</h1>
      <p class="subtitle">{{ hero.subtitle|default:"A curated collection of antiquities, offered privately." }}</p>
      
      <div class="royal-meta">
        <div class="meta-item"><span>Origin</span><br>{{ hero.region }}</div>
        <div class="meta-item"><span>Period</span><br>{{ hero.period }}</div>
      </div>

      <div class="hero-ctas">
        <a href="/collection/" class="btn btn--gold">Enter the Gallery</a>
      </div>
    </div>

  </div>
</section>

<style>
  .hero-proper-royal {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    overflow: hidden;
    padding-top: var(--nav-h, 100px);
  }

  .royal-palace-bg {
    position: absolute;
    inset: -5%;
    /* Stunning European Palace/Museum Interior */
    background-image: url('https://images.unsplash.com/photo-1541845157-a6d2d100c931?q=80&w=2000&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    filter: sepia(0.5) contrast(1.2) brightness(0.4) blur(4px);
    z-index: 0;
    animation: slowZoom 40s infinite alternate ease-in-out;
  }

  .royal-overlay {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(30,20,15,0.4) 0%, rgba(10,8,6,0.95) 100%);
    z-index: 1;
  }

  .hero-content {
    position: relative;
    z-index: 10;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
  }

  .royal-showcase {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .artifact-halo {
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(195, 162, 75, 0.2) 0%, transparent 60%);
    z-index: 0;
    animation: pulseHalo 4s infinite alternate ease-in-out;
  }

  .showcase-img {
    position: relative;
    z-index: 1;
    max-width: 80%;
    max-height: 75vh;
    box-shadow: 0 50px 100px rgba(0,0,0,0.9);
    border: 1px solid rgba(195,162,75,0.3);
    border-radius: 4px;
    animation: floatRoyal 8s infinite ease-in-out;
  }

  .royal-typography {
    text-align: left;
  }

  .eyebrow {
    font-family: var(--font-utility);
    font-size: 13px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 24px;
  }

  .royal-typography h1 {
    font-family: var(--font-display);
    font-size: clamp(48px, 6vw, 84px);
    color: #FBF8F1;
    line-height: 1.1;
    margin-bottom: 24px;
    text-shadow: 0 20px 40px rgba(0,0,0,0.8);
  }

  .subtitle {
    font-size: 20px;
    color: rgba(241, 235, 221, 0.7);
    line-height: 1.6;
    margin-bottom: 40px;
  }

  .royal-meta {
    display: flex;
    gap: 40px;
    margin-bottom: 40px;
    border-top: 1px solid rgba(195,162,75,0.2);
    padding-top: 32px;
  }

  .meta-item {
    color: #FBF8F1;
    font-size: 16px;
  }
  .meta-item span {
    font-family: var(--font-utility);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .reveal {
    animation: royalFadeInUp 1.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  }
  
  .film-grain {
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 2;
    mix-blend-mode: overlay;
    animation: filmJitter 0.3s infinite steps(2);
  }

  @keyframes slowZoom {
    0% { transform: scale(1); }
    100% { transform: scale(1.1); }
  }

  @keyframes floatRoyal {
    0% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0); }
  }
  
  @keyframes pulseHalo {
    0% { transform: scale(0.9); opacity: 0.6; }
    100% { transform: scale(1.1); opacity: 1; }
  }
  
  @keyframes filmJitter {
    0% { transform: translate(0, 0); }
    100% { transform: translate(2px, 2px); }
  }

  @media (max-width: 992px) {
    .hero-content {
      grid-template-columns: 1fr;
      text-align: center;
    }
    .royal-typography { text-align: center; }
    .royal-meta { justify-content: center; }
  }
</style>
"""

html = re.sub(hero_pattern, proper_royal_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
