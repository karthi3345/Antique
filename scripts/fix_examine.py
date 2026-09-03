import re

with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS to fix the examine-photo background
css_fix = """
<style>
  /* Premium overrides for Examine section */
  .examine-photo {
    background: transparent !important;
    border: none !important;
    box-shadow: 0 40px 100px rgba(0,0,0,0.8), 0 10px 40px rgba(195,162,75,0.1) !important;
    border-radius: 4px;
    position: relative;
    max-width: 700px !important;
    margin: 40px auto !important;
  }
  .examine-photo::before {
    content: '';
    position: absolute;
    inset: -150px;
    background: radial-gradient(circle at center, rgba(195,162,75,0.15) 0%, transparent 60%);
    z-index: -1;
    pointer-events: none;
  }
  .examine-photo img {
    border-radius: 2px;
  }
  .inspect-list { 
    background: rgba(16, 13, 10, 0.8) !important; 
    padding: 40px !important; 
    border-radius: 8px !important; 
    border: 1px solid rgba(195, 162, 75, 0.15) !important;
    backdrop-filter: blur(10px);
  }
</style>
"""

html = html.replace('{% endblock %}', css_fix + '\n{% endblock %}', 1)

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(html)
