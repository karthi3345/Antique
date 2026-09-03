with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Replace the GET logout link with a POST form and JS-triggered link
old_link = '<a href="/admin/logout/" class="text-secondary d-flex align-items-center gap-2">'
new_link = """<form id="logout-form" action="{% url 'admin:logout' %}" method="post" style="display: none;">
                  {% csrf_token %}
                </form>
                <a href="#" onclick="document.getElementById('logout-form').submit(); return false;" class="text-secondary d-flex align-items-center gap-2">"""

html = html.replace(old_link, new_link)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
