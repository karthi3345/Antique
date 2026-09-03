import re

with open('static/css/volgo.css', encoding='utf-8') as f:
    css = f.read()

# Add premium royal background to body
body_pattern = r'body\s*\{\s*background:\s*var\(--ink\);\s*color:\s*var\(--text\);'
new_body = """body {
  background: radial-gradient(circle at center top, #1c1511 0%, var(--ink) 100%);
  background-attachment: fixed;
  color: var(--text);
  position: relative;
}
body::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.035'/%3E%3C/svg%3E");
  z-index: 9999;
}
"""

css = re.sub(body_pattern, new_body, css)

# Add premium animations and glassmorphism at the end
css += """
/* Premium Animations & Museum Aesthetic */
@keyframes royalFadeInUp {
  0% { opacity: 0; transform: translateY(50px); filter: blur(4px); }
  100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}
section {
  animation: royalFadeInUp 1.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}
section:nth-child(1) { animation-delay: 0.1s; }
section:nth-child(2) { animation-delay: 0.3s; }
section:nth-child(3) { animation-delay: 0.5s; }

/* Premium Header Glassmorphism */
.site-header {
  background: rgba(12, 10, 8, 0.55) !important;
  backdrop-filter: blur(16px) saturate(200%);
  -webkit-backdrop-filter: blur(16px) saturate(200%);
  border-bottom: 1px solid rgba(195, 162, 75, 0.12) !important;
}

/* Subtle Shimmer on Primary Buttons */
.btn--solid {
  position: relative;
  overflow: hidden;
  background: linear-gradient(90deg, var(--gold) 0%, #E6D29A 50%, var(--gold) 100%);
  background-size: 200% auto;
  color: #0c0a08 !important;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 600;
  border: none;
}
.btn--solid:hover {
  background-position: right center;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -6px rgba(195, 162, 75, 0.25);
}

/* Image Premium Treatment */
.card-figure img, .hero-carousel img {
  filter: contrast(1.05) saturate(1.1);
  transition: transform 1s cubic-bezier(0.16, 1, 0.3, 1), filter 1s ease;
}
.card-figure:hover img {
  transform: scale(1.03);
  filter: contrast(1.1) saturate(1.2) brightness(1.1);
}
"""

with open('static/css/volgo.css', 'w', encoding='utf-8') as f:
    f.write(css)
