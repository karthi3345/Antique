import re

def update_journal_css(filepath):
    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    # 1. Update .reading-room to have the museum background
    museum_bg_css = """
  .reading-room {
    padding-top: 180px; 
    padding-bottom: var(--s9);
    position: relative;
    /* Dark museum background to match requested aesthetic */
    background-image: linear-gradient(rgba(12, 10, 8, 0.7), rgba(12, 10, 8, 0.9)), url('https://images.unsplash.com/photo-1582560469719-7565eb6340f1?q=80&w=2070&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
  }
"""
    # Replace existing .reading-room
    html = re.sub(r'\.reading-room\s*\{[^\}]+\}', museum_bg_css, html, count=1)

    # 2. Update .journal-paper to have a "glossy effect"
    glossy_css = """
  .journal-paper {
    background: linear-gradient(135deg, rgba(241, 235, 221, 0.9) 0%, rgba(241, 235, 221, 0.95) 50%, rgba(220, 210, 190, 0.85) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: #231f1c; /* Dark iron gall ink */
    box-shadow: 
      0 30px 60px rgba(0, 0, 0, 0.8), 
      inset 0 2px 5px rgba(255, 255, 255, 0.8), /* Glossy top highlight */
      inset 0 -2px 10px rgba(139, 107, 74, 0.15); /* Vintage bottom shadow */
    border: 1px solid rgba(255, 255, 255, 0.6); /* Glossy border */
    border-radius: 6px;
    padding: 80px 8%;
    position: relative;
    overflow: hidden;
  }
  
  /* The Glossy Shine Overlay */
  .journal-paper::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%);
    transform: skewX(-20deg);
    pointer-events: none;
    animation: glossyShine 8s infinite;
  }
  @keyframes glossyShine {
    0% { left: -100%; }
    15% { left: 200%; }
    100% { left: 200%; }
  }
"""
    # Find .journal-paper block and replace it
    html = re.sub(r'\.journal-paper\s*\{[^\}]+\}', glossy_css, html, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

update_journal_css('templates/house/chronicles.html')
update_journal_css('templates/house/chronicle.html')
