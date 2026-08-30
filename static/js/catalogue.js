/* Volgo — catalogue: fetches /api/objects/ and renders archival cards. */
(function () {
  'use strict';

  var grid = document.getElementById('catalogue-grid');
  if (!grid) return;

  var regionSel = document.getElementById('f-region');
  var categorySel = document.getElementById('f-category');
  var materialSel = document.getElementById('f-material');
  var sortSel = document.getElementById('f-sort');
  var qInput = document.getElementById('f-q');
  var clearBtn = document.getElementById('f-clear');
  var countEl = document.getElementById('catalogue-count');

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad3(n) { return String(n).padStart(3, '0'); }
  function frameUrl(o) {
    return '/static/img/objects/' + pad3(o.number) + '/00.webp';
  }

  function card(o) {
    var meta = [o.region, o.period].filter(Boolean).join(' <span class="sep">·</span> ');
    return '<a href="' + o.url + '" class="card">' +
    '<div class="card-figure">' +
    '<img src="' + frameUrl(o) + '" alt="' + esc(o.name) + ' — ' + esc(o.region) + '" loading="lazy" width="480" height="600" decoding="async">' +
    '</div>' +
    '<div class="object-label">' +
    '<span class="label-number">OBJECT No. ' + pad3(o.number) + '</span>' +
    '<span class="name">' + esc(o.name) + '</span>' +
    '<span class="meta meta-line">' + meta + '</span>' +
    (o.status === 'reserved' ? '<span class="status">' + esc(o.status_line) + '</span>' : '') +
    '</div></a>';
  }

  var state = {};

  function fetchObjects() {
    var params = new URLSearchParams();
    if (state.region) params.set('region', state.region);
    if (state.category) params.set('category', state.category);
    if (state.material) params.set('material', state.material);
    if (state.q) params.set('q', state.q);
    params.set('sort', state.sort || 'number');

    grid.setAttribute('aria-busy', 'true');
    fetch('/api/objects/?' + params.toString())
      .then(function (r) { return r.json(); })
      .then(function (data) {
        grid.innerHTML = data.objects.length
          ? data.objects.map(card).join('')
          : '<p class="serif-italic" style="grid-column:1/-1; text-align:center; padding:var(--s8) 0; font-size:22px;">No objects match this search — the collection is small by intention.</p>';
        if (countEl) countEl.textContent = data.objects.length + ' object' + (data.objects.length === 1 ? '' : 's');
        if (regionSel) fill(regionSel, data.facets.regions, 'Region', state.region);
        if (categorySel) fill(categorySel, data.facets.categories, 'Category', state.category);
        if (materialSel) fill(materialSel, materialFacets(data.objects), 'Material', state.material);
        grid.removeAttribute('aria-busy');
      });
  }

  function materialFacets(objects) {
    var out = {};
    objects.forEach(function (o) {
      var primary = String(o.material || '').split('·')[0].trim();
      if (primary) out[primary] = (out[primary] || 0) + 1;
    });
    return out;
  }

  function fill(sel, values, label, selected) {
    var opts = Array.isArray(values) ? values : Object.keys(values);
    opts.sort();
    sel.innerHTML = '<option value="">' + label + ': All</option>' +
      opts.map(function (v) { return '<option value="' + esc(v) + '">' + esc(v) + '</option>'; }).join('');
    sel.value = selected || '';
  }

  // Seed state from URL (supports /collection/?category=... links from home)
  var url = new URL(window.location.href);
  state.region = url.searchParams.get('region') || '';
  state.category = url.searchParams.get('category') || '';
  state.material = url.searchParams.get('material') || '';
  state.q = url.searchParams.get('q') || '';
  state.sort = url.searchParams.get('sort') || 'number';

  [regionSel, categorySel, materialSel, sortSel, qInput].forEach(function (el) {
    if (!el) return;
    if (state.region && el === regionSel) el.value = state.region;
    if (state.category && el === categorySel) el.value = state.category;
    if (state.material && el === materialSel) el.value = state.material;
    if (state.sort && el === sortSel) el.value = state.sort;
    if (state.q && el === qInput) el.value = state.q;
  });

  if (regionSel) regionSel.addEventListener('change', function () { state.region = regionSel.value; fetchObjects(); });
  if (categorySel) categorySel.addEventListener('change', function () { state.category = categorySel.value; fetchObjects(); });
  if (materialSel) materialSel.addEventListener('change', function () { state.material = materialSel.value; fetchObjects(); });
  if (sortSel) sortSel.addEventListener('change', function () { state.sort = sortSel.value; fetchObjects(); });
  if (qInput) {
    var t = null;
    qInput.addEventListener('input', function () {
      clearTimeout(t);
      t = setTimeout(function () { state.q = qInput.value.trim(); fetchObjects(); }, 300);
    });
  }
  if (clearBtn) clearBtn.addEventListener('click', function () {
    state = { sort: 'number' };
    if (regionSel) regionSel.value = '';
    if (categorySel) categorySel.value = '';
    if (materialSel) materialSel.value = '';
    if (sortSel) sortSel.value = 'number';
    if (qInput) qInput.value = '';
    fetchObjects();
  });

  fetchObjects();
})();
