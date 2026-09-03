with open('templates/admin/index.html', encoding='utf-8') as f:
    html = f.read()

# Replace the specific href for the Logout link
html = html.replace(
    '<a href="#!" class="text-secondary d-flex align-items-center gap-2">\n                <span>\n                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"\n                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"\n                    class="icon icon-tabler icons-tabler-outline icon-tabler-login-2">\n                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />\n                    <path d="M9 8v-2a2 2 0 0 1 2 -2h7a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-7a2 2 0 0 1 -2 -2v-2" />\n                    <path d="M3 12h13l-3 -3" />\n                    <path d="M13 15l3 -3" />\n                  </svg>\n                </span>\n                <span>Logout</span></a>',
    '<a href="/admin/logout/" class="text-secondary d-flex align-items-center gap-2">\n                <span>\n                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"\n                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"\n                    class="icon icon-tabler icons-tabler-outline icon-tabler-login-2">\n                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />\n                    <path d="M9 8v-2a2 2 0 0 1 2 -2h7a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-7a2 2 0 0 1 -2 -2v-2" />\n                    <path d="M3 12h13l-3 -3" />\n                    <path d="M13 15l3 -3" />\n                  </svg>\n                </span>\n                <span>Logout</span></a>'
)

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
