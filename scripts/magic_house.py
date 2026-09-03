import re

new_html = """{% extends "base.html" %}

{% block title %}The House — VOLGO{% endblock %}

{% block head %}
<style>
  /* Premium Magical Aesthetic for The House */
  .house-hero {
    position: relative;
    padding: 200px 0 140px;
    background: radial-gradient(circle at center, #1a1511 0%, #0a0806 100%);
    overflow: hidden;
    text-align: center;
    border-bottom: 1px solid rgba(195, 162, 75, 0.2);
  }

  /* Magical glowing orb */
  .magic-orb {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 60vw; height: 60vw;
    background: radial-gradient(circle, rgba(195, 162, 75, 0.15) 0%, rgba(195, 162, 75, 0) 70%);
    border-radius: 50%;
    filter: blur(40px);
    animation: pulseOrb 8s infinite alternate ease-in-out;
    pointer-events: none;
    z-index: 0;
  }

  @keyframes pulseOrb {
    0% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
    100% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
  }

  /* Floating Magic Dust */
  .magic-dust {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
  }
  .dust-particle {
    position: absolute;
    width: 3px; height: 3px;
    background: #fbf8f1;
    border-radius: 50%;
    box-shadow: 0 0 12px 2px #c3a24b;
    opacity: 0;
    animation: floatUp var(--duration, 8s) infinite linear;
    animation-delay: var(--delay, 0s);
    left: var(--left, 50%);
    bottom: -10px;
  }
  @keyframes floatUp {
    0% { transform: translateY(0) scale(0.5); opacity: 0; }
    20% { opacity: 0.8; }
    80% { opacity: 0.8; }
    100% { transform: translateY(-300px) scale(1.5); opacity: 0; }
  }

  .house-hero-content {
    position: relative;
    z-index: 2;
    animation: royalFadeInUp 1.5s forwards;
  }

  .house-hero h1 {
    font-size: clamp(52px, 8vw, 100px);
    color: #F1EBDD;
    text-shadow: 0 0 40px rgba(195, 162, 75, 0.4);
    line-height: 1.1;
    margin-bottom: 24px;
    font-family: var(--font-display);
    letter-spacing: -0.02em;
  }
  
  .house-hero .lede {
    font-size: clamp(18px, 2vw, 24px);
    color: var(--gold-pale);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* Magical Cartouche styling */
  .magic-cartouche {
    position: relative;
    padding: 80px;
    background: rgba(16, 13, 10, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(195, 162, 75, 0.3);
    box-shadow: 
      0 0 0 1px rgba(255, 255, 255, 0.05),
      0 40px 80px rgba(0,0,0,0.8),
      inset 0 0 60px rgba(195, 162, 75, 0.05);
    border-radius: 4px;
    overflow: hidden;
  }
  
  /* Animated Sweep over the cartouche */
  .magic-cartouche::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(195, 162, 75, 0.1) 90deg, transparent 180deg);
    animation: rotateAura 12s linear infinite;
    pointer-events: none;
    z-index: -1;
  }
  
  @keyframes rotateAura {
    100% { transform: rotate(360deg); }
  }

  .philosophy-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    position: relative;
    z-index: 1;
  }
  
  .philosophy-block h2 {
    color: #F1EBDD;
    font-size: 32px;
    margin-bottom: 20px;
  }
  .philosophy-block p {
    color: rgba(241, 235, 221, 0.7);
    line-height: 1.8;
    font-size: 17px;
  }

  @media (max-width: 768px) {
    .philosophy-grid { grid-template-columns: 1fr; gap: 40px; }
    .magic-cartouche { padding: 40px 20px; }
  }
</style>
{% endblock %}

{% block content %}
<!-- MAGICAL HERO -->
<section class="house-hero">
  <div class="magic-orb"></div>
  
  <div class="magic-dust" id="dust-container">
    <!-- Particles injected via JS -->
  </div>

  <div class="container narrow house-hero-content">
    <p class="label-number" style="justify-content:center; margin-bottom: 24px;">The House</p>
    <h1>A young house<br>with an old discipline</h1>
    <p class="lede">
      Volgo was founded in 2026. We are a private antiquities house: we examine, document, and place objects with their next keepers — one collector at a time.
    </p>
  </div>
</section>

<!-- MAGICAL CARTOUCHE -->
<section class="section">
  <div class="container">
    <div class="magic-cartouche reveal">
      <div class="philosophy-grid">
        <div class="philosophy-block">
          <p class="label-number">Philosophy</p>
          <h2>The record is the luxury</h2>
          <p>An object survives; a record proves it. What endures across centuries is not ownership but custody — invoices, ledgers, catalogues, photographs. We treat documentation as half of every object we offer.</p>
          <p>We decline to sell. We present, verify, and step back. If an object is not right for a collector, we say so.</p>
        </div>
        <div class="philosophy-block">
          <p class="label-number">Curatorial approach</p>
          <h2>Small by intention</h2>
          <p>The collection holds fewer than one hundred and fifty objects at any time. Each is examined in person, photographed in full rotation, and catalogued with its attribution stated in the professional vocabulary — <em>attributed to</em>, <em>circle of</em>, <em>in the manner of</em> — never rounded up to certainty.</p>
          <p>Rarity is proven by restraint. A house that offers everything offers nothing.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <p class="label-number reveal">Authentication</p>
    <h2 class="reveal" style="margin:16px 0 var(--s5);">How a claim becomes a record</h2>
    <div class="reveal">
      <p>Every object is examined at the house before it is catalogued. Attribution is written against evidence: maker's marks, construction, materials, documentary references, and the object's provenance line.</p>
      <p>Where evidence is absent, the record says so plainly. An honest gap is worth more than a decorated guess — and a collector can weigh an uncertainty that is stated.</p>
      <p>Each acquisition leaves the house with a certificate of authenticity, a condition report, and the provenance document: the same records, in paper and digital form.</p>
    </div>
  </div>
</section>

<section class="section" style="border-top:1px solid rgba(195, 162, 75, 0.2);">
  <div class="container narrow">
    <p class="label-number reveal">Private clients</p>
    <h2 class="reveal" style="margin:16px 0 var(--s5);">Conducted personally</h2>
    <div class="reveal">
      <p>Our clients are collectors, collections, and institutions. Acquisitions are conducted personally — by correspondence, in the viewing room, and through private delivery.</p>
      <p>Enquire about an object and a member of the house responds, usually within one working day.</p>
      <div style="margin-top:var(--s5);"><a href="/acquisition/" class="btn btn--gold">The acquisition process</a></div>
    </div>
  </div>
</section>

<script>
  // Generate magical dust particles
  document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('dust-container');
    for (let i = 0; i < 40; i++) {
      const particle = document.createElement('div');
      particle.className = 'dust-particle';
      particle.style.setProperty('--left', `${Math.random() * 100}%`);
      particle.style.setProperty('--duration', `${5 + Math.random() * 10}s`);
      particle.style.setProperty('--delay', `${Math.random() * 5}s`);
      container.appendChild(particle);
    }
  });
</script>
{% endblock %}"""

with open('templates/house/the-house.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
