with open('templates/base.html', encoding='utf-8') as f:
    html = f.read()

nav_links = """<div class="nav-right">
        {% if user.is_authenticated %}
          <span style="color: var(--gold); font-size: 13px; margin-right: 15px; text-transform: uppercase; letter-spacing: 0.1em;">Hello, {{ user.username }}</span>
          <form method="post" action="{% url 'logout' %}" style="display:inline;">{% csrf_token %}<button type="submit" style="margin-right: 20px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.18em; color: var(--text-muted); cursor: pointer; transition: color 0.3s;" onmouseover="this.style.color='#C3A24B'" onmouseout="this.style.color='var(--text-muted)'">Logout</button></form>
        {% else %}
          <a href="{% url 'login' %}" style="margin-right: 15px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.18em; color: var(--text-muted); transition: color 0.3s;" onmouseover="this.style.color='#C3A24B'" onmouseout="this.style.color='var(--text-muted)'">Sign In</a>
          <a href="{% url 'register' %}" class="nav-acquisition" style="margin-right: 20px;">Register</a>
        {% endif %}
        <a href="/acquisition/" class="nav-acquisition">Private Acquisition</a>"""

html = html.replace('<div class="nav-right">\n        <a href="/acquisition/" class="nav-acquisition">Private Acquisition</a>', nav_links)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
