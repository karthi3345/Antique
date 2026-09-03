import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace all <model-viewer> blocks with the correct image tag
# Because the formatting might have arbitrary whitespace, we will use a generic regex
viewer_pattern = r'<model-viewer[^>]*src="https://raw\.githubusercontent\.com/KhronosGroup/glTF-Sample-Models/master/2\.0/AntiqueCamera/glTF-Binary/AntiqueCamera\.glb"[^>]*>[\s\S]*?</model-viewer>'

# What was the original grid image tag?
# <img src="/static/img/objects/{{ obj.object_number|stringformat:'03d' }}/00.webp" alt="{{ obj.name }} — {{ obj.region }}, {{ obj.period }}" loading="lazy" decoding="async">
# But for the carousel it was {{ item.hero }}. Let's check where the <model-viewer> tags are!

# The problem is that the previous greedy regex replaced EVERY image tag.
# We need to revert home.html entirely from git, and then just apply the Hero and Text fixes properly!

