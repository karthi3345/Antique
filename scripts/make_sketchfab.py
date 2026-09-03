import re

# 1. Update base.html to include model-viewer
with open('templates/base.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

if 'model-viewer.min.js' not in base_html:
    base_html = base_html.replace('</head>', '  <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>\n</head>')
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)

# 2. Update home.html hero section
with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

# Replace the img inside .exhibit-frame with a model-viewer
model_viewer_hero = """
          <model-viewer 
            src="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/AntiqueCamera/glTF-Binary/AntiqueCamera.glb" 
            alt="3D model of an antique camera" 
            auto-rotate 
            camera-controls 
            exposure="1.2"
            shadow-intensity="1.5"
            style="width: 100%; height: 100%; background: radial-gradient(circle at center, #1a1612 0%, #0a0806 100%); outline: none;">
          </model-viewer>
"""
home_html = re.sub(r'<img src="/static/img/objects/[^>]+>', model_viewer_hero, home_html)
# Remove the glass reflection overlay because it blocks mouse interactions with the 3D model!
home_html = re.sub(r'<div class="glass-reflection"></div>', '', home_html)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)

# 3. Update artifact.html Examine section
with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    artifact_html = f.read()

# Replace the figure examine-photo with a massive Sketchfab-style 3D viewer
sketchfab_viewer = """
      <div class="sketchfab-viewer-container" style="width: 100%; height: 70vh; min-height: 500px; margin: 40px 0; border-radius: 8px; overflow: hidden; box-shadow: 0 30px 60px rgba(0,0,0,0.8); border: 1px solid rgba(195, 162, 75, 0.2); position: relative; background: #0a0806;">
        <model-viewer 
          src="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/AntiqueCamera/glTF-Binary/AntiqueCamera.glb" 
          alt="{{ artifact.name }} 3D View" 
          auto-rotate 
          camera-controls 
          exposure="1.2"
          shadow-intensity="1.5"
          camera-orbit="45deg 75deg 105%"
          interaction-prompt="auto"
          style="width: 100%; height: 100%; outline: none; background: radial-gradient(circle at center, #1a1612 0%, #050403 100%);">
          
          <div class="viewer-ui" style="position: absolute; bottom: 20px; left: 20px; display: flex; gap: 12px; pointer-events: none;">
            <div style="background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); padding: 8px 16px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); color: #F1EBDD; font-family: var(--font-utility); font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;">
              3D Interactive View
            </div>
            <div style="background: rgba(195, 162, 75, 0.2); backdrop-filter: blur(4px); padding: 8px 16px; border-radius: 4px; border: 1px solid rgba(195, 162, 75, 0.4); color: var(--gold-pale); font-family: var(--font-utility); font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;">
              Drag to Rotate &bull; Scroll to Zoom
            </div>
          </div>
        </model-viewer>
      </div>
"""
artifact_html = re.sub(r'<figure class="examine-photo">.*?</figure>', sketchfab_viewer, artifact_html, flags=re.DOTALL)
# Make sure we don't accidentally remove the JS/CSS from before if it was left over, though we reverted it.
with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(artifact_html)
