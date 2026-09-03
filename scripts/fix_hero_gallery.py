import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the entire hero section
hero_pattern = r'<section class="hero-museum"[^>]*>.*?</section>'

new_hero = """
<section class="hero-gallery-full" style="
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: flex-end;
  padding-bottom: 80px;
  background-image: url('/static/img/custom_gallery.jpg');
  background-size: cover;
  background-position: center;
  border-bottom: 1px solid rgba(195, 162, 75, 0.2);
">
  <!-- Premium dark overlay to make it look luxurious and keep text readable -->
  <div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,8,6,0.1) 0%, rgba(10,8,6,0.6) 60%, rgba(10,8,6,0.95) 100%); pointer-events: none;"></div>
  
  <div class="container" style="position: relative; z-index: 2;">
    <div style="max-width: 600px; animation: royalFadeInUp 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;">
      <p class="hero-eyebrow" style="font-family: var(--font-utility); font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); margin-bottom: 16px; display: flex; align-items: center; gap: 12px;">
        <span style="width: 30px; height: 1px; background: var(--gold);"></span>
        Private Exhibition
      </p>
      <h1 style="font-size: clamp(40px, 5vw, 72px); color: #F1EBDD; line-height: 1.1; margin-bottom: 24px; font-family: var(--font-display);">
        A curated collection, <br>offered privately.
      </h1>
      <div class="hero-ctas" style="display: flex; gap: 20px;">
        <a href="/collection/" class="btn btn--gold">Enter Gallery</a>
        <a href="/acquisition/" class="btn btn--outline" style="border-color: #C3A24B; color: #C3A24B;">Private Acquisition</a>
      </div>
    </div>
  </div>
</section>
"""

html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
