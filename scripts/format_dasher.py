import re

with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Make sure we add load static
if '{% load static %}' not in html:
    html = '{% load static %}\n' + html

html = re.sub(r'href=[\"\']\./assets/([^\"\']+)[\"\']', r'href="{% static \'dasher/\1\' %}"', html)
html = re.sub(r'src=[\"\']\./assets/([^\"\']+)[\"\']', r'src="{% static \'dasher/\1\' %}"', html)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
