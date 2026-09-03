import re

with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add the new Premium Royal CSS inside the <style> block
premium_story_css = """
  /* ----------------------------------------------------
     90s ROYAL PREMIUM: STORY & DETAILS UPGRADE
     ---------------------------------------------------- */
  
  /* Glowing Gold Section Dividers (replaces flat border-top) */
  .section, .section-tight {
    border-top: none !important;
    position: relative;
  }
  .section::before, .section-tight::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(195,162,75,0.4) 50%, transparent 100%);
  }

  /* The Story: Royal Cartouche */
  #story .article-body {
    background: rgba(16, 13, 10, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(195, 162, 75, 0.2);
    box-shadow: 0 40px 100px rgba(0,0,0,0.8), inset 0 0 40px rgba(195, 162, 75, 0.05);
    padding: 60px;
    border-radius: 4px;
    color: #F1EBDD;
    font-size: 19px;
    line-height: 1.8;
  }
  #story .article-body .lede {
    color: var(--gold-pale);
    font-size: 22px;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(195,162,75,0.2);
    padding-bottom: 24px;
  }

  /* Provenance Timeline: Glowing Royal Ledger */
  .timeline {
    border-left: 2px solid rgba(195, 162, 75, 0.3) !important;
    padding-left: 40px !important;
    margin-top: 40px;
  }
  .timeline li {
    position: relative;
    padding-bottom: 40px;
  }
  /* The glowing dot */
  .timeline li::before {
    content: '';
    position: absolute;
    left: -46px; /* center on the 2px border */
    top: 0;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 15px var(--gold);
    border: 2px solid #0a0806;
  }
  .timeline li .year {
    font-family: var(--font-display);
    font-size: 24px;
    color: var(--gold-pale);
    margin-bottom: 8px;
  }
  .timeline li.is-current::before {
    background: #FBF8F1;
    box-shadow: 0 0 20px #FBF8F1, 0 0 40px var(--gold);
    animation: pulseAura 2s infinite alternate;
  }

  /* Specifications Ledger */
  .spec-table dl {
    background: rgba(16, 13, 10, 0.7);
    border: 1px solid rgba(195, 162, 75, 0.2);
    border-radius: 4px;
    padding: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  }
  .spec-table dt {
    padding: 12px 20px;
    border-bottom: 1px solid rgba(195,162,75,0.1);
    color: var(--gold);
  }
  .spec-table dd {
    padding: 12px 20px;
    border-bottom: 1px solid rgba(195,162,75,0.1);
    color: #F1EBDD;
  }

  /* Acquisition Box */
  #enquiry-cta {
    background: radial-gradient(circle at center, rgba(195, 162, 75, 0.1) 0%, transparent 80%);
    padding: 40px;
    border: 1px solid rgba(195,162,75,0.3);
    border-radius: 4px;
    text-align: center;
    margin-top: 40px;
  }

  /* Related Objects 90s Vintage Sepia effect */
  .grid-strip .card-img img {
    filter: sepia(0.6) contrast(1.2) brightness(0.8);
    transition: filter 0.8s ease, transform 0.8s ease;
  }
  .grid-strip .card:hover .card-img img {
    filter: sepia(0.1) contrast(1.1) brightness(1.1);
    transform: scale(1.05);
  }
  .grid-strip .card {
    background: rgba(16, 13, 10, 0.8);
    border: 1px solid rgba(195, 162, 75, 0.15);
    border-radius: 4px;
    overflow: hidden;
  }
  .grid-strip .card-meta {
    padding: 20px;
  }
"""

# Insert right before the </style> block closes
html = html.replace('</style>', f'{premium_story_css}\n</style>')

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(html)
