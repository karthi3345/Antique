import re

with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add 90s Royal Premium CSS
royal_90s_css = """
  /* 90s ROYAL PREMIUM PAGE-WIDE EFFECTS */
  
  /* Vintage Film Grain across entire page */
  body {
    background: radial-gradient(circle at 50% 150px, #2a1c15 0%, #0a0806 100%) !important;
  }
  
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    mix-blend-mode: overlay;
    animation: filmJitter 0.3s infinite steps(2);
  }

  /* VHS Scanlines across entire page */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      to bottom,
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0) 2px,
      rgba(0, 0, 0, 0.3) 3px,
      rgba(0, 0, 0, 0.3) 4px
    );
    pointer-events: none;
    z-index: 9998;
  }

  @keyframes filmJitter {
    0% { transform: translate(0, 0); }
    100% { transform: translate(2px, 2px); }
  }

  /* Royal Title styling with subtle 90s Chromatic Aberration */
  header .name {
    display: inline-block;
    color: #FBF8F1;
    font-family: var(--font-display);
    text-align: center;
    text-shadow: 
      2px 0 0 rgba(200, 20, 20, 0.7), 
      -2px 0 0 rgba(20, 20, 200, 0.7),
      0 0 40px rgba(195, 162, 75, 0.5);
    animation: rgbGlitch 5s infinite alternate;
  }

  @keyframes rgbGlitch {
    0% { text-shadow: 2px 0 0 rgba(200, 20, 20, 0.7), -2px 0 0 rgba(20, 20, 200, 0.7), 0 0 40px rgba(195, 162, 75, 0.5); }
    10% { text-shadow: -2px 0 0 rgba(200, 20, 20, 0.7), 2px 0 0 rgba(20, 20, 200, 0.7), 0 0 40px rgba(195, 162, 75, 0.5); }
    100% { text-shadow: 1px 0 0 rgba(200, 20, 20, 0.7), -1px 0 0 rgba(20, 20, 200, 0.7), 0 0 40px rgba(195, 162, 75, 0.5); }
  }

  /* Royal Label Block container */
  header .object-label {
    text-align: center;
    background: rgba(16, 10, 8, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(195, 162, 75, 0.3);
    padding: 60px 40px;
    border-radius: 8px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.9), inset 0 0 60px rgba(195, 162, 75, 0.05);
    position: relative;
    overflow: hidden;
  }
  
  /* Vintage film tracking bar */
  header .object-label::after {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 8px;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    pointer-events: none;
    animation: trackingScroll 8s infinite linear;
  }

  @keyframes trackingScroll {
    0% { top: -10%; opacity: 0; }
    10% { opacity: 0.5; }
    50% { opacity: 0.8; }
    90% { opacity: 0.5; }
    100% { top: 110%; opacity: 0; }
  }

  /* Deep Royal Sepia Tone for the Examine Photo */
  .examine-photo img {
    filter: sepia(0.65) contrast(1.25) brightness(0.85) hue-rotate(-15deg);
    transition: filter 1s ease;
  }
  .examine-photo:hover img {
    filter: sepia(0.2) contrast(1.1) brightness(1.1) hue-rotate(0deg);
  }

  /* Enquire Buttons Royal Styling */
  header .btn--gold {
    box-shadow: 0 0 30px rgba(195, 162, 75, 0.3);
  }
"""

html = html.replace('</style>', f'{royal_90s_css}\n</style>')

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(html)
