import re

with open('static/css/volgo.css', encoding='utf-8') as f:
    css = f.read()

# Remove the conflicting hover styles
conflict_pattern = r'\.card:hover \.card-figure,\s*\.card:focus-visible \.card-figure \{.*?\}'
css = re.sub(conflict_pattern, '', css, flags=re.DOTALL)

# Also remove the conflicting img hover
conflict_img_pattern = r'\.card:hover \.card-figure img,\s*\.card:focus-visible \.card-figure img \{.*?\}'
css = re.sub(conflict_img_pattern, '', css, flags=re.DOTALL)

with open('static/css/volgo.css', 'w', encoding='utf-8') as f:
    f.write(css)
