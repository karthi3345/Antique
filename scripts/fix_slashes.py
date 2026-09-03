with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Replace literal \' with just '
html = html.replace("\\'", "'")

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
