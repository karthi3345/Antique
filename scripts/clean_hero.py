import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the hero-proper-royal section
hero_pattern = r'<section class="hero-proper-royal".*?</style>'

clean_premium_hero = """
<section class="hero-classic" id="hero">
  <!-- Ultra-clean dark luxury background -->
  <div class="hero-bg"></div>

  <div class="container hero-content">
    
    <!-- Left: Elegant Typography -->
    <div class="hero-text reveal">
      <div class="eyebrow">
        <span class="line"></span>
        <span class="label">{{ hero.label_number|default:"VOLGO 001" }}</span>
      </div>
      
      <h1 class="title">{{ hero.name }}</h1>
      
      <p class="subtitle">{{ hero.subtitle|default:"An exceptional object of antiquity, documented and offered privately." }}</p>
      
      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">Origin</span>
          <span class="meta-value">{{ hero.region }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Period</span>
          <span class="meta-value">{{ hero.period }}</span>
        </div>
      </div>

      <div class="ctas">
        <a href="/collection/" class="btn btn--gold">Enter Gallery</a>
        <a href="/acquisition/" class="btn btn--outline" style="border-color: rgba(195,162,75,0.3); color: var(--gold);">Private Acquisition</a>
      </div>
    </div>

    <!-- Right: Pure, sharp artifact image -->
    <div class="hero-image reveal">
      <div class="image-wrapper">
        <img src="/static/img/objects/{{ hero.object_number|stringformat:'03d' }}/{{ hero.hero_frame|stringformat:'02d' }}.webp" 
             alt="{{ hero.name }}" fetchpriority="high">
      </div>
    </div>

  </div>
</section>

<style>
  .hero-classic {
    position: relative;
    min-height: 95vh;
    display: flex;
    align-items: center;
    padding-top: var(--nav-h, 100px);
    background: #0a0806;
    overflow: hidden;
    border-bottom: 1px solid rgba(195,162,75,0.15);
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    /* Soft, elegant radial glow behind the artifact */
    background: radial-gradient(circle at 75% 50%, rgba(195,162,75,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }

  .hero-content {
    position: relative;
    z-index: 10;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
  }

  /* Typography */
  .hero-text {
    padding-right: 40px;
  }

  .eyebrow {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 32px;
  }
  .eyebrow .line {
    width: 40px;
    height: 1px;
    background: var(--gold);
  }
  .eyebrow .label {
    font-family: var(--font-utility);
    font-size: 11px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .title {
    font-family: var(--font-display);
    font-size: clamp(48px, 6vw, 84px);
    color: #FBF8F1;
    line-height: 1.1;
    margin-bottom: 32px;
    font-weight: 400;
  }

  .subtitle {
    font-size: 20px;
    color: rgba(241, 235, 221, 0.7);
    line-height: 1.7;
    margin-bottom: 48px;
    max-width: 90%;
  }

  .meta-grid {
    display: flex;
    gap: 60px;
    margin-bottom: 48px;
    padding-top: 32px;
    border-top: 1px solid rgba(195,162,75,0.2);
  }
  .meta-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .meta-label {
    font-family: var(--font-utility);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(195,162,75,0.6);
  }
  .meta-value {
    color: #FBF8F1;
    font-size: 16px;
  }

  .ctas {
    display: flex;
    gap: 20px;
  }
  .ctas .btn {
    padding: 16px 32px;
  }

  /* Image */
  .hero-image {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .image-wrapper {
    position: relative;
    max-width: 500px;
    width: 100%;
  }
  .image-wrapper img {
    width: 100%;
    height: auto;
    display: block;
    box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    transition: transform 1.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .image-wrapper:hover img {
    transform: scale(1.03);
  }

  .reveal {
    animation: royalFadeInUp 1.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  }
  .hero-image.reveal {
    animation-delay: 0.2s;
  }

  @media (max-width: 992px) {
    .hero-content {
      grid-template-columns: 1fr;
      text-align: center;
      gap: 40px;
      padding-top: 40px;
    }
    .hero-text { padding-right: 0; }
    .eyebrow { justify-content: center; }
    .eyebrow .line { display: none; }
    .meta-grid { justify-content: center; }
    .ctas { justify-content: center; }
    .subtitle { margin: 0 auto 40px; }
  }
</style>
"""

html = re.sub(hero_pattern, clean_premium_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
