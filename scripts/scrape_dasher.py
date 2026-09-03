import urllib.request
import os
import re
from urllib.parse import urljoin

base_url = 'https://themewagon.github.io/dasher/'
with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Replace local paths in HTML to use Django static tags
# We'll do this in a moment. Let's just download first.
assets = re.findall(r'(?:href|src)=[\"\'](\./assets/[^\"\']+)[\"\']', html)
assets = list(set(assets))

for asset in assets:
    # asset is like './assets/css/theme.min.css'
    url = urljoin(base_url, asset[2:])
    local_path = os.path.join('static', 'dasher', asset[2:])
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print('Fetching', url)
    try:
        urllib.request.urlretrieve(url, local_path)
    except Exception as e:
        print('Failed', url, e)

# Also fetch JS map files if they exist or images referenced in CSS (might break, but let's try)
