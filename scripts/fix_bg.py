import re

def update_journal_css(filepath):
    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    # The previous URL was 404ing. Let's replace it with a valid Pexels Museum URL
    html = html.replace(
        "url('https://images.unsplash.com/photo-1582560469719-7565eb6340f1?q=80&w=2070&auto=format&fit=crop')",
        "url('https://images.pexels.com/photos/208912/pexels-photo-208912.jpeg?auto=compress&cs=tinysrgb&w=2000')"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

update_journal_css('templates/house/chronicles.html')
update_journal_css('templates/house/chronicle.html')
