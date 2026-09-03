import urllib.request, re

url = 'https://unsplash.com/photos/natural-history-museum-hall-in-london-iqeG5xA96M4'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if match:
        img_url = match.group(1)
        # Download the image to static folder
        print('Found URL:', img_url)
        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data = urllib.request.urlopen(img_req).read()
        with open('static/img/museum-bg.jpg', 'wb') as f:
            f.write(img_data)
        print("Image saved to static/img/museum-bg.jpg")
    else:
        print('Not found in HTML')
except Exception as e:
    print('Error:', e)
