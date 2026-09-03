import re

with open('templates/collection/artifact.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add the sweeping light and floating animation CSS
magic_css = """
  /* Floating Relic Animation */
  .examine-photo {
    animation: floatRelic 8s ease-in-out infinite;
  }
  @keyframes floatRelic {
    0% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0); }
  }

  /* Sweeping Glass Shine */
  .examine-photo::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.1) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    transform: rotate(30deg);
    pointer-events: none;
    animation: sweepShine 7s infinite linear;
    z-index: 5;
  }
  @keyframes sweepShine {
    0% { transform: rotate(30deg) translateY(-100%) translateX(-100%); }
    20% { transform: rotate(30deg) translateY(100%) translateX(100%); }
    100% { transform: rotate(30deg) translateY(100%) translateX(100%); }
  }

  /* Relic Aura Pulse */
  .examine-photo::before {
    animation: pulseAura 4s infinite alternate ease-in-out;
  }
  @keyframes pulseAura {
    0% { opacity: 0.5; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1.1); }
  }
"""

html = html.replace('</style>', f'{magic_css}\n</style>')

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(html)
