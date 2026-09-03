with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Fix static paths by adding 'assets/' where it was stripped by the previous regex
html = html.replace("{% static 'dasher/", "{% static 'dasher/assets/")

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
