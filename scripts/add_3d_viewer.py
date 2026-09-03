import re

with open('templates/collection/artifact.html', encoding='utf-8') as f:
    html = f.read()

# Replace the examine-photo block with the interactive 3D viewer
examine_pattern = r'<figure class="examine-photo">.*?</figure>'

new_examine = """
      <!-- 3D Museum Viewer -->
      <div class="museum-3d-container" id="museum-3d-container">
        <p class="instruction-3d"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg> Click and drag to examine object in 3D space</p>
        <div class="museum-3d-scene">
          <div class="museum-3d-object" id="museum-3d-object">
            <figure class="examine-photo" style="margin: 0; padding: 0;">
              <img src="/static/img/objects/{{ artifact.object_number|stringformat:'03d' }}/{{ artifact.hero_frame|stringformat:'02d' }}.webp"
                   alt="{{ artifact.name }} — {{ artifact.region }}, {{ artifact.period }}"
                   loading="lazy" decoding="async" class="object-img-3d">
              <div class="glass-reflection-3d"></div>
            </figure>
          </div>
        </div>
      </div>

<style>
  .museum-3d-container {
    perspective: 1500px;
    margin: var(--s6) 0;
    position: relative;
    cursor: grab;
    touch-action: none; /* Prevent scrolling when rotating */
  }
  .museum-3d-container:active {
    cursor: grabbing;
  }
  .instruction-3d {
    text-align: center;
    font-family: var(--font-utility);
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    opacity: 0.8;
  }
  .museum-3d-scene {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    position: relative;
    transform-style: preserve-3d;
  }
  .museum-3d-object {
    position: relative;
    width: 100%;
    transform-style: preserve-3d;
    transition: transform 0.1s ease-out;
    transform: rotateX(0deg) rotateY(0deg);
  }
  
  .object-img-3d {
    width: 100%;
    height: auto;
    display: block;
    border: 12px solid #1a1612;
    box-shadow: 
      0 0 0 4px var(--gold-deep),
      inset 0 0 0 2px var(--gold),
      0 50px 100px rgba(0,0,0,0.9),
      -20px 20px 40px rgba(0,0,0,0.6);
    border-radius: 4px;
    transform: translateZ(20px);
  }
  
  /* Adds a realistic reflection that moves with the object */
  .glass-reflection-3d {
    position: absolute;
    inset: 12px;
    z-index: 10;
    pointer-events: none;
    background: linear-gradient(
      105deg,
      rgba(255,255,255,0.2) 0%,
      rgba(255,255,255,0) 40%,
      rgba(255,255,255,0.05) 100%
    );
    transform: translateZ(22px);
  }
</style>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('museum-3d-container');
    const object = document.getElementById('museum-3d-object');
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let rotation = { x: 0, y: 0 };

    const startDrag = (e) => {
      isDragging = true;
      const event = e.touches ? e.touches[0] : e;
      previousMousePosition = { x: event.clientX, y: event.clientY };
    };

    const drag = (e) => {
      if (!isDragging) return;
      
      const event = e.touches ? e.touches[0] : e;
      const deltaMove = {
        x: event.clientX - previousMousePosition.x,
        y: event.clientY - previousMousePosition.y
      };

      // Calculate rotation (Y controls left/right, X controls up/down)
      rotation.y += deltaMove.x * 0.4;
      rotation.x -= deltaMove.y * 0.4;

      // Limit vertical rotation to prevent flipping
      rotation.x = Math.max(-45, Math.min(45, rotation.x));
      // Limit horizontal rotation so it doesn't spin infinitely (since it's a flat image)
      rotation.y = Math.max(-60, Math.min(60, rotation.y));

      object.style.transform = `rotateX(${rotation.x}deg) rotateY(${rotation.y}deg)`;

      previousMousePosition = { x: event.clientX, y: event.clientY };
    };

    const endDrag = () => {
      isDragging = false;
      // Optional: auto-return to center
      // object.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
      // rotation = { x: 0, y: 0 };
      // object.style.transform = `rotateX(0deg) rotateY(0deg)`;
      // setTimeout(() => { object.style.transition = 'transform 0.1s ease-out'; }, 600);
    };

    container.addEventListener('mousedown', startDrag);
    window.addEventListener('mousemove', drag);
    window.addEventListener('mouseup', endDrag);

    container.addEventListener('touchstart', startDrag, {passive: false});
    window.addEventListener('touchmove', drag, {passive: false});
    window.addEventListener('touchend', endDrag);
  });
</script>
"""

html = re.sub(examine_pattern, new_examine, html, flags=re.DOTALL)

with open('templates/collection/artifact.html', 'w', encoding='utf-8') as f:
    f.write(html)
