import re

def replace_with_sketchfab(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    pattern = r'<model-viewer[\s\S]*?</model-viewer>'
    
    iframe = """<iframe title="Little Mermaid Statue" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/31a5e3261edd4945a8b107abc6f39/embed?autostart=1&ui_theme=dark" style="width: 100%; height: 100%; outline: none; background: radial-gradient(circle at center, #1a1612 0%, #0a0806 100%);"></iframe>"""
    
    new_html = re.sub(pattern, iframe, html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

replace_with_sketchfab('templates/collection/home.html')
replace_with_sketchfab('templates/collection/artifact.html')
