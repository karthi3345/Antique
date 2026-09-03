import re

# 1. Update base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

base_html = base_html.replace('Objects of distinction, privately acquired.', 'Maison d\\'Antiquités.')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

# 2. Update home.html
with open('templates/collection/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

home_html = home_html.replace('<h2>Objects of distinction,<br>privately acquired.</h2>', '<h2>A curated collection,<br>offered privately.</h2>')

with open('templates/collection/home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)
