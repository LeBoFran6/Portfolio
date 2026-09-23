/* =============================================================================
   site.js — progressive enhancement only.

   Everything this file does is an optional extra. With JavaScript disabled:
     - all navigation is reachable (the mobile menu is a <details> element)
     - all project content, images and links are plain HTML
     - the contact page states plainly that sending needs JavaScript, and lists
       the contact details as text beside the form
   The reveal animations are gated behind html.js, so nothing is ever hidden
   from a visitor whose JavaScript fails to load.

   No dependencies. No tracking. No network calls.
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
    : false;

  /* ---------------------------------------------------------------------------
     1. Mobile navigation — <details> handles open/close natively.
        We only add: Escape to close, close on link click, close on resize,
        and focus return. All of it is additive.
     ------------------------------------------------------------------------ */
  function initNav() {
    var nav = document.querySelector("[data-mobile-nav]");
    if (!nav) return;

    var summary = nav.querySelector("summary");
    if (!summary) return;

    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) nav.open = false;
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" || !nav.open) return;
      nav.open = false;
      summary.focus();
    });

    var mq = window.matchMedia("(min-width: 1000px)");
    var onChange = function () { if (mq.matches) nav.open = false; };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ---------------------------------------------------------------------------
     2. Scroll reveal — additive polish only.
     ------------------------------------------------------------------------ */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(items, function (el) { el.classList.add("is-in"); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });

    Array.prototype.forEach.call(items, function (el, i) {
      el.style.setProperty("--reveal-delay", (Math.min(i % 4, 3) * 70) + "ms");
      io.observe(el);
    });
  }

  /* ---------------------------------------------------------------------------
     3. Work filters. Without JS every card stays visible — nothing is hidden.
     ------------------------------------------------------------------------ */
  function initFilters() {
    var bar = document.querySelector("[data-filters]");
    var grid = document.querySelector("[data-grid]");
    if (!bar || !grid) return;

    var buttons = Array.prototype.slice.call(bar.querySelectorAll("button[data-filter]"));
    var cards = Array.prototype.slice.call(grid.querySelectorAll("[data-tags]"));
    var live = document.querySelector("[data-filter-live]");

    function apply(tag) {
      var shown = 0;
      cards.forEach(function (card) {
        var tags = (card.getAttribute("data-tags") || "").split(/\s+/);
        var match = tag === "all" || tags.indexOf(tag) !== -1;
        card.hidden = !match;
        if (match) shown++;
      });
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === tag));
      });
      if (live) {
        live.textContent = shown + (shown === 1 ? " project shown" : " projects shown");
      }
      // Keep the filter in the URL so a filtered view can be shared or reloaded.
      try {
        var url = new URL(window.location.href);
        if (tag === "all") url.searchParams.delete("filter");
        else url.searchParams.set("filter", tag);
        window.history.replaceState(null, "", url);
      } catch (err) { /* older browser: filtering still works, URL just stays put */ }
    }

    bar.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      apply(btn.getAttribute("data-filter"));
    });

    // Honour ?filter= on load.
    var initial = "all";
    try {
      initial = new URL(window.location.href).searchParams.get("filter") || "all";
    } catch (err) { /* ignore */ }
    if (!buttons.some(function (b) { return b.getAttribute("data-filter") === initial; })) {
      initial = "all";
    }
    apply(initial);
  }

  /* ---------------------------------------------------------------------------
     4. Showreel — the video file is only fetched when the visitor asks for it.
        preload="none" + hidden until play, so it costs nothing on page load.
     ------------------------------------------------------------------------ */
  function initReel() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-reel]"), function (root) {
      var btn = root.querySelector("[data-reel-play]");
      var video = root.querySelector("video");
      if (!btn || !video) return;

      btn.addEventListener("click", function () {
        root.setAttribute("data-playing", "true");
        btn.hidden = true;
        video.hidden = false;
        var p = video.play();
        if (p && typeof p.catch === "function") {
          p.catch(function () { /* autoplay blocked — native controls are visible */ });
        }
      });
    });
  }

  /* ---------------------------------------------------------------------------
     5. Contact form — no backend, so it builds a mailto: draft and says so.
        The mailto: address is also printed as a normal link next to the form,
        so the page is fully usable with JavaScript disabled.
     ------------------------------------------------------------------------ */
  function initForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var note = form.querySelector("[data-form-note]");
    var to = form.getAttribute("data-mailto");

    function say(message, isError) {
      if (!note) return;
      note.textContent = message;
      note.setAttribute("data-state", isError ? "error" : "info");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (!form.checkValidity()) {
        say("Please fill in every field before sending.", true);
        var first = form.querySelector(":invalid");
        if (first && first.focus) first.focus();
        return;
      }

      var data = new FormData(form);
      var name = (data.get("name") || "").toString().trim();
      var email = (data.get("email") || "").toString().trim();
      var message = (data.get("message") || "").toString().trim();

      var subject = "Portfolio enquiry — " + name;
      var body = message + "\n\n—\n" + name + "\n" + email;

      window.location.href = "mailto:" + to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      say("Opening your email client with the message pre-filled. " +
          "If nothing happens, write to " + to + " directly.", false);
    });
  }

  /* ---------------------------------------------------------------------------
     6. Footer year.
     ------------------------------------------------------------------------ */
  function initYear() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    initNav();
    initReveal();
    initFilters();
    initReel();
    initForm();
    initYear();
  });
})();
