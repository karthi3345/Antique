import re

with open('templates/base.html', encoding='utf-8') as f:
    html = f.read()

# Replace the nav-right block with a much cleaner, perfectly aligned flex structure
nav_right_pattern = r'<div class="nav-right">.*?</div>'

new_nav_right = """<div class="nav-right" style="display: flex; align-items: center; gap: 24px;">
        {% if user.is_authenticated %}
          <form id="logout-form" action="{% url 'logout' %}" method="post" style="display: none;">{% csrf_token %}</form>
          <a href="#" onclick="document.getElementById('logout-form').submit(); return false;" class="nav-search" style="padding: 0; display: inline-block;">Logout</a>
        {% else %}
          <a href="{% url 'login' %}" class="nav-search" style="padding: 0; display: inline-block;">Sign In</a>
        {% endif %}
        <a href="/acquisition/" class="nav-acquisition">Private Acquisition</a>
        <button class="nav-search" id="nav-search" aria-label="Search the collection" style="padding: 0; margin-left: 8px;">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="6.5" cy="6.5" r="5"/><path d="M10.5 10.5L14 14"/></svg>
          Search
        </button>
      </div>"""

# Replace the block
html = re.sub(nav_right_pattern, new_nav_right, html, flags=re.DOTALL)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
