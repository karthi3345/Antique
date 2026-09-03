import re

with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

# Pattern for the hero image (it's inside .exhibit-frame)
hero_img_pattern = r'<img src="/static/img/objects/\{\{\s*hero\.object_number.*?\.webp"[^>]*>'

new_hero_img = """<img src="/static/img/custom_gallery.jpg" alt="Volgo Museum Gallery" fetchpriority="high" decoding="async">"""

home_html = re.sub(hero_img_pattern, new_hero_img, home_html, count=1)

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)
