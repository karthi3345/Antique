with open('templates/admin/login.html', encoding='utf-8') as f:
    html = f.read()

html = html.replace("\\'", "'")

with open('templates/admin/login.html', 'w', encoding='utf-8') as f:
    f.write(html)
