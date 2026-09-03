import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add the 90s VHS and Vintage elements inside the hero section
hero_vhs_elements = """
  <!-- 90s VHS / Vintage Film Overlay -->
  <div class="vhs-scanlines"></div>
  <div class="vhs-tracking"></div>
  <div class="film-grain"></div>
"""

# Inject them right after the premium-spotlight
html = html.replace('<div class="premium-spotlight"></div>', f'<div class="premium-spotlight"></div>{hero_vhs_elements}')

# Now add the heavy 90s CSS to the bottom of the style block
vhs_css = """
  /* 90s VHS & Vintage Antique Effects */
  
  .hero-premium {
    /* Blend the dark gradient with a sepia tone */
    background: radial-gradient(circle at 70% 50%, #2a2015 0%, #0c0906 80%);
  }

  .film-grain {
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.12'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 1;
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
      rgba(0, 0, 0, 0.2) 3px,
      rgba(0, 0, 0, 0.2) 4px
    );
    pointer-events: none;
    z-index: 2;
  }

  .vhs-tracking {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 10px;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    pointer-events: none;
    z-index: 3;
    animation: trackingScroll 6s infinite linear;
  }

  /* 90s Chromatic Aberration on Title */
  .premium-text h1 {
    text-shadow: 
      2px 0 0 rgba(255, 0, 0, 0.6), 
      -2px 0 0 rgba(0, 255, 255, 0.6),
      0 0 20px rgba(195, 162, 75, 0.4);
    animation: rgbGlitch 4s infinite alternate;
  }

  /* Sepia and Vintage fade on the image */
  .image-wrapper img {
    filter: sepia(0.6) contrast(1.2) brightness(0.9) hue-rotate(-10deg);
  }
  
  .image-wrapper:hover img {
    filter: sepia(0.2) contrast(1.1) brightness(1.1);
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
    0% { text-shadow: 2px 0 0 rgba(255, 0, 0, 0.6), -2px 0 0 rgba(0, 255, 255, 0.6), 0 0 20px rgba(195, 162, 75, 0.4); }
    20% { text-shadow: -2px 0 0 rgba(255, 0, 0, 0.6), 2px 0 0 rgba(0, 255, 255, 0.6), 0 0 20px rgba(195, 162, 75, 0.4); }
    100% { text-shadow: 1px 0 0 rgba(255, 0, 0, 0.6), -1px 0 0 rgba(0, 255, 255, 0.6), 0 0 20px rgba(195, 162, 75, 0.4); }
  }
"""

# Insert the CSS right before the closing </style> tag of the hero CSS
html = html.replace('</style>', f'{vhs_css}\n</style>')

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
