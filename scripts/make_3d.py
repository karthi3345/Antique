import re

with open('static/css/volgo.css', encoding='utf-8') as f:
    css = f.read()

# Make the card a 3D perspective container
card_pattern = r'\.card \{\s*display: flex;\s*flex-direction: column;\s*height: 100%;\s*border: 0; border-radius: 0;\s*background: none;\s*position: relative;\s*\}'
new_card = """.card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 0; border-radius: 0;
  background: none;
  position: relative;
  perspective: 1200px; /* Enable 3D space */
}"""
css = re.sub(card_pattern, new_card, css)

# Make the figure a 3D object that tilts on hover
figure_pattern = r'\.card \.card-figure \{.*?\n.*?transition: border-color.*?\n.*?\}'
new_figure = """.card .card-figure {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4 / 5;
  background: var(--cream);
  border: 6px solid var(--gold);
  box-shadow:
    inset 0 0 0 2px var(--gold-deep),
    inset 0 0 8px rgba(195, 162, 75, 0.25),
    0 4px 15px rgba(0, 0, 0, 0.4);
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1),
              box-shadow 0.6s cubic-bezier(0.25, 1, 0.5, 1),
              border-color 0.6s ease;
  will-change: transform;
}
.card:hover .card-figure {
  transform: rotateX(6deg) rotateY(-8deg) translateY(-10px) translateZ(20px);
  box-shadow:
    inset 0 0 0 2px var(--gold-deep),
    inset 0 0 15px rgba(195, 162, 75, 0.4),
    -15px 25px 40px rgba(0, 0, 0, 0.9),
    10px -10px 20px rgba(195, 162, 75, 0.15); /* golden backlight reflection */
  border-color: #E6D29A;
}"""
css = re.sub(figure_pattern, new_figure, css, flags=re.DOTALL)

# Add 3D parallax to the image and glass overlay
parallax_img_pattern = r'\.card-figure:hover img \{\s*transform: scale\(1\.03\);\s*filter: contrast\(1\.1\) saturate\(1\.2\) brightness\(1\.1\);\s*\}'
new_parallax_img = """.card:hover .card-figure img {
  transform: scale(1.1) translateZ(40px); /* 3D pop inside the frame */
  filter: contrast(1.15) saturate(1.2) brightness(1.1);
}
.card:hover .card-figure::before {
  /* Shift the glass reflection on hover */
  transform: translateX(20%) translateY(-20%) translateZ(60px);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 40%,
    rgba(255, 255, 255, 0)    60%,
    rgba(255, 255, 255, 0.05) 100%
  );
}"""
css = re.sub(parallax_img_pattern, new_parallax_img, css)

# Make glass overlay 3d
glass_pattern = r'\.card \.card-figure::before \{.*?\n.*?\}'
# Find the exact block to replace just to ensure we add preserve-3d and transition
# Actually let's just do a blanket replace.
css = css.replace('z-index: 2;', 'z-index: 2; transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);')

with open('static/css/volgo.css', 'w', encoding='utf-8') as f:
    f.write(css)
