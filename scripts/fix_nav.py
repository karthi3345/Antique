import re

with open('templates/base.html', encoding='utf-8') as f:
    html = f.read()

# The current nav-right block is a bit of a mess.
# Let's completely replace the <div class="nav-right">...</div> block
nav_right_pattern = r'<div class="nav-right">.*?</div>'

new_nav_right = """<div class="nav-right">
        {% if user.is_authenticated %}
          <span class="nav-search" style="color: var(--gold); cursor: default;">Hello, {{ user.username }}</span>
          <form method="post" action="{% url 'logout' %}" style="display:inline; margin:0; padding:0;">
            {% csrf_token %}
            <button type="submit" class="nav-search">Logout</button>
          </form>
        {% else %}
          <a href="{% url 'login' %}" class="nav-search">Sign In</a>
          <a href="{% url 'register' %}" class="nav-search">Register</a>
        {% endif %}
        <a href="/acquisition/" class="nav-acquisition">Private Acquisition</a>
        <button class="nav-search" id="nav-search" aria-label="Search the collection">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="6.5" cy="6.5" r="5"/><path d="M10.5 10.5L14 14"/></svg>
          Search
        </button>
      </div>"""

# Ensure DOTALL so .*? matches newlines
html = re.sub(nav_right_pattern, new_nav_right, html, flags=re.DOTALL)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
