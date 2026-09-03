import re

with open('templates/admin/login.html', encoding='utf-8') as f:
    html = f.read()

# Add load static at the top
if '{% load static %}' not in html:
    html = '{% load static %}\n' + html

# Fix brand name
html = html.replace('Dasher Free - Responsive Bootstrap 5 Admin Dashboard', 'Volgo Antique - Admin Login')
html = html.replace('<span class="fw-bold fs-4  site-logo-text">Dasher</span>', '<span class="fw-bold fs-4  site-logo-text">Volgo Antique</span>')
html = html.replace('Sign In to Dasher', 'Sign In to Volgo Antique')
html = html.replace('Welcome back to Dasher! Enter your email to get started.', 'Welcome back. Please sign in to manage the collection.')

# Remove Google and Facebook login section
start_marker = '<!-- Google / Facebook Buttons -->'
end_marker = '<div class="mb-4 mt-6 text-center">'
# Since we don't know exact markers, let's just use regex to remove the grid of buttons.
html = re.sub(r'<div class="d-grid gap-2 mb-4">.*?</div>\s*<div class="mb-4 mt-6 text-center">.*?</div>', '', html, flags=re.DOTALL)

# Make form functional for Django Admin
# Change <form> to <form method="post" action="{{ app_path }}">
html = re.sub(r'<form\b[^>]*>', r'<form method="post" action="{{ app_path }}">', html)

# Insert csrf token
html = html.replace('<form method="post" action="{{ app_path }}">', '<form method="post" action="{{ app_path }}">\n                  {% csrf_token %}\n                  <input type="hidden" name="next" value="{{ next }}">')

# Fix inputs
html = html.replace('id="email"', 'id="email" name="username"')
html = html.replace('type="email"', 'type="text"')  # Django admin allows usernames
html = html.replace('id="password"', 'id="password" name="password"')

# If there are form errors (like invalid login), Django passes {{ form.errors }}
error_block = """
{% if form.errors and not form.non_field_errors %}
<p class="text-danger mb-3">Please correct the errors below.</p>
{% endif %}
{% if form.non_field_errors %}
{% for error in form.non_field_errors %}
<p class="text-danger mb-3">{{ error }}</p>
{% endfor %}
{% endif %}
"""
html = html.replace('{% csrf_token %}', '{% csrf_token %}\n' + error_block)

# Force dark mode
html = html.replace('<html lang="en">', '<html lang="en" data-bs-theme="dark">')

with open('templates/admin/login.html', 'w', encoding='utf-8') as f:
    f.write(html)
