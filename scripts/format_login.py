import re

with open('templates/admin/login.html', encoding='utf-8') as f:
    html = f.read()

# Replace any relative path starting with ../../assets/ or ./assets/
html = re.sub(r'href=[\"\']\.\./\.\./assets/([^\"\']+)[\"\']', r'href="{% static \'dasher/assets/\1\' %}"', html)
html = re.sub(r'src=[\"\']\.\./\.\./assets/([^\"\']+)[\"\']', r'src="{% static \'dasher/assets/\1\' %}"', html)

# Just in case some are still ./assets/
html = re.sub(r'href=[\"\']\./assets/([^\"\']+)[\"\']', r'href="{% static \'dasher/assets/\1\' %}"', html)
html = re.sub(r'src=[\"\']\./assets/([^\"\']+)[\"\']', r'src="{% static \'dasher/assets/\1\' %}"', html)

with open('templates/admin/login.html', 'w', encoding='utf-8') as f:
    f.write(html)
