import re

with open('templates/admin/login.html', encoding='utf-8') as f:
    html = f.read()

# Replace the social buttons HTML using regex
html = re.sub(r'<span>Sign in with your social network\.</span>.*?</a>\s*</div>', '', html, flags=re.DOTALL)

with open('templates/admin/login.html', 'w', encoding='utf-8') as f:
    f.write(html)
