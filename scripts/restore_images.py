import re

# 1. Update home.html
with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

# Replace iframe with dynamic image
iframe_pattern = r'<iframe[^>]*src="https://sketchfab[^>]*></iframe>'
hero_img = """<img src="/static/img/objects/{{ hero.object_number|stringformat:'03d' }}/{{ hero.hero_frame|stringformat:'02d' }}.webp"
                 alt="{{ hero.name }}" fetchpriority="high" decoding="async">
            <div class="glass-reflection"></div>"""

home_html = re.sub(iframe_pattern, hero_img, home_html)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)

# 2. Update artifact.html
with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    artifact_html = f.read()

artifact_img_section = """
      <figure class="examine-photo">
        <img src="/static/img/objects/{{ artifact.object_number|stringformat:'03d' }}/{{ artifact.hero_frame|stringformat:'02d' }}.webp"
             alt="{{ artifact.name }} — {{ artifact.region }}, {{ artifact.period }}"
             loading="lazy" decoding="async">
      </figure>
"""

# Replace the entire sketchfab-viewer-container div
container_pattern = r'<div class="sketchfab-viewer-container"[^>]*>[\s\S]*?</div>'
artifact_html = re.sub(container_pattern, artifact_img_section, artifact_html)

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(artifact_html)
