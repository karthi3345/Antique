/* Volgo — private acquisition enquiry form (injected on artifact pages
   and rendered natively on acquisition/contact pages). */
(function () {
  "use strict";

  var ctaHost = document.getElementById("enquiry-cta");
  var nativeForm = document.getElementById("enquiry-form");

  function esc(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function fallbackThanks(form, reply) {
    form.innerHTML =
      '<p class="lede">Thank you.</p><p>' + esc(reply || "Your enquiry has been received. A member of the house will respond within one working day.") + "</p>";
  }

  function formHTML(objectNumber, objectName) {
    var objNote = objectNumber
      ? '<p class="form-note" style="margin-bottom:var(--s4);">Concerning <span class="label-number" style="font-size:10px;">OBJECT No. ' + String(objectNumber).padStart(3, "0") + "</span>" + (objectName ? " — " + esc(objectName) : "") + "</p>"
      : "";
    return (
      objNote +
      '<form id="enquiry-form-inner" novalidate>' +
      '<div class="field"><label for="e-name">Your name</label><input id="e-name" name="name" type="text" autocomplete="name" required><span class="error">Your name is required.</span></div>' +
      '<div class="field"><label for="e-email">Email</label><input id="e-email" name="email" type="email" autocomplete="email" required><span class="error">A valid email address is required.</span></div>' +
      '<div class="field"><label for="e-phone">Telephone <span style="text-transform:none; letter-spacing:0; font-weight:400;">(optional)</span></label><input id="e-phone" name="phone" type="tel" autocomplete="tel"></div>' +
      '<div class="field"><label for="e-message">Your interest</label><textarea id="e-message" name="message" rows="5" required></textarea><span class="error">A few words about your interest help us respond well.</span></div>' +
      '<button type="submit" class="btn btn--solid">Begin enquiry</button>' +
      '<p class="form-note" id="enquiry-status" style="margin-top:16px;" role="status"></p>' +
      "</form>"
    );
  }

  function wire(form, objectNumber) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var status = form.querySelector("#enquiry-status");
      var payload = {
        name: (form.querySelector('[name="name"]') || {}).value || "",
        email: (form.querySelector('[name="email"]') || {}).value || "",
        phone: (form.querySelector('[name="phone"]') || {}).value || "",
        message: (form.querySelector('[name="message"]') || {}).value || "",
        object: objectNumber,
      };

      form.querySelectorAll(".field").forEach(function (f) { f.classList.remove("is-invalid"); });

      var csrf = (document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/) || [])[1] || "";
      fetch("/api/enquiry/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify(payload),
      })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); })
        .then(function (res) {
          if (res.ok) {
            var anim = {
              name: payload.name, email: payload.email, phone: payload.phone,
              message: payload.message,
              number: res.body.number || "", reply: res.body.reply || "",
            };
            var css = document.querySelector('link[data-vp-post]');
            if (!css) {
              css = document.createElement("link");
              css.rel = "stylesheet";
              css.href = "/static/css/post.css";
              css.setAttribute("data-vp-post", "1");
              document.head.appendChild(css);
            }
            if (window.VolgoPost && window.VolgoPost.fire) {
              window.VolgoPost.fire(anim);
            } else {
              var s = document.createElement("script");
              s.src = "/static/js/post.js";
              s.onload = function () {
                if (window.VolgoPost) { window.VolgoPost.fire(anim); }
                else { fallbackThanks(form, anim.reply); }
              };
              s.onerror = function () { fallbackThanks(form, anim.reply); };
              document.head.appendChild(s);
            }
          } else {
            if (status) status.textContent = res.body.error || "A detail appears to be missing below.";
            var fields = res.body.fields || {};
            Object.keys(fields).forEach(function (k) {
              var input = form.querySelector('[name="' + k + '"]');
              if (input) input.closest(".field").classList.add("is-invalid");
            });
          }
        })
        .catch(function () {
          if (status) status.textContent = "The enquiry could not be sent. Please try again, or write to the house directly.";
        });
    });
  }

  // Artifact page: CTA expands the form inline
  if (ctaHost) {
    var article = ctaHost.closest("article");
    var objectNumber = article ? parseInt(article.dataset.objectNumber, 10) : null;
    var objectName = article ? (article.querySelector(".object-label .name") || {}).textContent : "";
    var btn = document.createElement("button");
    btn.className = "btn";
    btn.textContent = "Request private acquisition";
    btn.addEventListener("click", function () {
      ctaHost.innerHTML = formHTML(objectNumber, objectName ? objectName.trim() : "");
      var form = document.getElementById("enquiry-form-inner");
      if (form) wire(form, objectNumber);
    });
    ctaHost.appendChild(btn);
  }

  // Native form pages (acquisition/contact): wire if present
  if (nativeForm) {
    var num = nativeForm.dataset.object ? parseInt(nativeForm.dataset.object, 10) : null;
    wire(nativeForm, num);
  }
})();
