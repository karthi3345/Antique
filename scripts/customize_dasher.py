import re

with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Replace site name
html = html.replace('Dasher Free - Responsive Bootstrap 5 Admin Dashboard', 'Volgo Antique Admin Dashboard')
html = html.replace('<span class="fw-bold fs-4  site-logo-text">Dasher</span>', '<span class="fw-bold fs-4  site-logo-text">Volgo Antique</span>')
html = html.replace('Hello Ana,', 'Hello Admin,')
html = html.replace('Welcome to your E-commerce Dashboard!', 'Welcome to the Volgo Antique Dashboard!')

# Replace sidebar links
html = html.replace('<span class="text">Ecommerce</span>', '<span class="text">Artifacts</span>')
html = html.replace('href="./index.html"', 'href="/admin/collection/artifact/"')

html = html.replace('<span class="text">Pages</span>', '<span class="text">Enquiries</span>')
html = html.replace('href="./pages/error/maintenance.html"', 'href="/admin/collection/enquiry/"')
html = html.replace('Maintenance', 'View Enquiries')

html = html.replace('<span class="text">Authentication</span>', '<span class="text">Security</span>')
html = html.replace('href="./pages/authentication/sign-in.html"', 'href="/admin/auth/user/"')
html = html.replace('Sign In', 'Manage Users')
html = html.replace('href="./pages/authentication/sign-up.html"', 'href="/admin/auth/group/"')
html = html.replace('Sign Up', 'Manage Groups')

# Replace top-right user name
html = html.replace('Jitu Chauhan', 'Admin')
html = html.replace('@imjituchauhan', '@admin')

# To make it dark mode by default, the template uses color-modes.js which reads localstorage.
# We can force data-bs-theme="dark" on the html tag.
html = html.replace('<html lang="en">', '<html lang="en" data-bs-theme="dark">')

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
