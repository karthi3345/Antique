import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern for the current hero gallery full section and all the lingering old CSS
# We'll just replace the entire top block down to the end of the old <style> tag
hero_pattern = r'<section class="hero-gallery-full".*?</style>'

premium_hero = """
<section class="hero-premium" id="hero" aria-label="Featured object — {{ hero.name }}">
  <div class="premium-spotlight"></div>
  <div class="container">
    <div class="premium-layout">
      
      <div class="premium-text reveal">
        <div class="eyebrow-line">
          <span class="line"></span>
          <span class="text">{{ hero.label_number|default:"VOLGO 001" }}</span>
        </div>
        <h1>{{ hero.name }}</h1>
        <p class="premium-desc">{{ hero.subtitle|default:"An object examined, documented, and offered — with its history intact." }}</p>
        
        <div class="premium-meta">
          <div class="meta-block">
            <span class="meta-label">Origin</span>
            <span class="meta-value">{{ hero.region }}</span>
          </div>
          <div class="meta-block">
            <span class="meta-label">Period</span>
            <span class="meta-value">{{ hero.period }}</span>
          </div>
        </div>

        <div class="hero-ctas" style="margin-top: 40px;">
          <a href="/collection/" class="btn btn--gold">Explore Collection</a>
          <a href="/acquisition/" class="btn btn--outline" style="border-color: rgba(195,162,75,0.4); color: var(--gold-pale);">Private Acquisition</a>
        </div>
      </div>

      <div class="premium-media reveal">
        <div class="image-wrapper">
          <img src="/static/img/objects/{{ hero.object_number|stringformat:'03d' }}/{{ hero.hero_frame|stringformat:'02d' }}.webp" 
               alt="{{ hero.name }}" fetchpriority="high" decoding="async">
        </div>
      </div>

    </div>
  </div>
</section>

<style>
  .hero-premium {
    position: relative;
    min-height: 90vh;
    display: flex;
    align-items: center;
    background: radial-gradient(circle at 70% 50%, #17130F 0%, #0A0806 80%);
    overflow: hidden;
    padding-top: var(--nav-h, 100px);
    border-bottom: 1px solid rgba(195, 162, 75, 0.15);
  }

  .premium-spotlight {
    position: absolute;
    top: -20%; left: 50%;
    width: 800px; height: 800px;
    background: radial-gradient(circle, rgba(195, 162, 75, 0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }

  .premium-layout {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
    padding: 60px 0;
  }

  .eyebrow-line {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
  }
  .eyebrow-line .line {
    width: 40px; height: 1px;
    background: var(--gold);
  }
  .eyebrow-line .text {
    font-family: var(--font-utility);
    font-size: 11px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .premium-text h1 {
    font-size: clamp(48px, 6vw, 84px);
    color: #FBF8F1;
    line-height: 1.05;
    margin-bottom: 32px;
    font-family: var(--font-display);
    font-weight: 400;
  }

  .premium-desc {
    font-size: clamp(18px, 2vw, 22px);
    color: rgba(241, 235, 221, 0.7);
    line-height: 1.6;
    max-width: 90%;
    margin-bottom: 40px;
  }

  .premium-meta {
    display: flex;
    gap: 48px;
    padding-top: 32px;
    border-top: 1px solid rgba(195, 162, 75, 0.2);
  }
  .meta-block {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .meta-label {
    font-family: var(--font-utility);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(195, 162, 75, 0.6);
  }
  .meta-value {
    font-size: 15px;
    color: #F1EBDD;
  }

  .premium-media {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .image-wrapper {
    position: relative;
    width: 100%;
    max-width: 520px;
  }
  .image-wrapper img {
    width: 100%;
    height: auto;
    display: block;
    box-shadow: 0 40px 80px rgba(0,0,0,0.8);
    transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .image-wrapper:hover img {
    transform: scale(1.02);
  }

  /* Entrance Animations */
  .reveal {
    animation: royalFadeInUp 1.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  }
  .premium-text { animation-delay: 0.1s; }
  .premium-media { animation-delay: 0.4s; }

  @media (max-width: 992px) {
    .premium-layout {
      grid-template-columns: 1fr;
      text-align: center;
      gap: 40px;
    }
    .eyebrow-line { justify-content: center; }
    .eyebrow-line .line { display: none; }
    .premium-meta { justify-content: center; }
    .hero-ctas { justify-content: center; }
    .premium-desc { margin: 0 auto 40px; }
  }
</style>
"""

html = re.sub(hero_pattern, premium_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
