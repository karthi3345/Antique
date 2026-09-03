import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the 2D image in the Hero section with the 3D model-viewer
hero_img_pattern = r'<img src="/static/img/objects/{{ hero.object_number\|stringformat:\'03d\' }}/{{ hero.hero_frame\|stringformat:\'02d\' }}.webp"[^>]+>'

model_viewer = """<model-viewer 
            src="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/AntiqueCamera/glTF-Binary/AntiqueCamera.glb" 
            alt="3D model of an antique camera" 
            auto-rotate 
            camera-controls 
            exposure="1.2"
            shadow-intensity="1.5"
            style="width: 100%; height: 100%; background: radial-gradient(circle at center, #1a1612 0%, #0a0806 100%); outline: none;">
          </model-viewer>"""

html = re.sub(hero_img_pattern, model_viewer, html)

# 2. Fix the Vulgar Text
html = html.replace('<h2>Objects of distinction,<br>privately acquired.</h2>', '<h2>A curated collection,<br>offered privately.</h2>')
html = html.replace('<div class="glass-reflection"></div>', '')

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
