/* HAZE — shared behaviors. No frameworks, no build step.
   Everything here is intentionally quiet: long durations, no bounce. */

(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isFinePointer = window.matchMedia('(pointer: fine)').matches;

  /* ---------------- Loader ---------------- */
  function initLoader() {
    var loader = document.querySelector('[data-loader]');
    if (!loader) return;
    var bar = loader.querySelector('[data-loader-progress]');
    document.documentElement.style.overflow = 'hidden';

    function finish() {
      if (bar) bar.style.width = '100%';
      window.setTimeout(function () {
        loader.classList.add('is-hidden');
        document.documentElement.style.overflow = '';
      }, prefersReducedMotion ? 0 : 500);
      window.setTimeout(function () {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      }, prefersReducedMotion ? 50 : 1600);
    }

    if (bar) window.requestAnimationFrame(function () { bar.style.width = '70%'; });

    if (document.readyState === 'complete') {
      window.setTimeout(finish, 300);
    } else {
      window.addEventListener('load', function () { window.setTimeout(finish, 200); });
      window.setTimeout(finish, 1800); // safety fallback
    }
  }

  /* ---------------- Nav: glass on scroll + mobile toggle ---------------- */
  function initNav() {
    var nav = document.querySelector('[data-nav]');
    if (!nav) return;
    var threshold = 24;

    function onScroll() {
      if (window.scrollY > threshold) nav.classList.add('is-glass');
      else nav.classList.remove('is-glass');
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    var toggle = document.querySelector('[data-nav-toggle]');
    var links = document.querySelector('[data-nav-links]');
    if (toggle && links) {
      toggle.addEventListener('click', function () {
        var open = links.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.documentElement.style.overflow = open ? 'hidden' : '';
      });
      links.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          links.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          document.documentElement.style.overflow = '';
        });
      });
    }
  }

  /* ---------------- Scroll progress ---------------- */
  function initScrollProgress() {
    var bar = document.querySelector('[data-scroll-progress]');
    if (!bar) return;
    function onScroll() {
      var h = document.documentElement;
      var scrollTop = h.scrollTop || document.body.scrollTop;
      var height = h.scrollHeight - h.clientHeight;
      var ratio = height > 0 ? scrollTop / height : 0;
      bar.style.transform = 'scaleX(' + ratio + ')';
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------------- Scroll reveal ---------------- */
  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------------- Image reveal (fade / blur-to-sharp) ---------------- */
  function initImageReveal() {
    var imgs = document.querySelectorAll('img.img-reveal');
    imgs.forEach(function (img) {
      if (img.complete && img.naturalWidth > 0) {
        img.classList.add('is-loaded');
      } else {
        img.addEventListener('load', function () { img.classList.add('is-loaded'); }, { once: true });
      }
    });
  }

  /* ---------------- Custom cursor ---------------- */
  function initCursor() {
    if (!isFinePointer || prefersReducedMotion) return;
    document.body.classList.add('has-custom-cursor');

    var dot = document.createElement('div');
    dot.className = 'cursor-dot';
    var ring = document.createElement('div');
    ring.className = 'cursor-ring';
    document.body.appendChild(dot);
    document.body.appendChild(ring);

    var mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    var ringPos = { x: mouse.x, y: mouse.y };

    window.addEventListener('mousemove', function (e) {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      dot.style.transform = 'translate(' + mouse.x + 'px,' + mouse.y + 'px) translate(-50%,-50%)';
    });

    function raf() {
      ringPos.x += (mouse.x - ringPos.x) * 0.16;
      ringPos.y += (mouse.y - ringPos.y) * 0.16;
      ring.style.transform = 'translate(' + ringPos.x + 'px,' + ringPos.y + 'px) translate(-50%,-50%)';
      window.requestAnimationFrame(raf);
    }
    window.requestAnimationFrame(raf);

    var hoverables = document.querySelectorAll('a, button, .magnetic, [data-cursor-hover]');
    hoverables.forEach(function (el) {
      el.addEventListener('mouseenter', function () { ring.classList.add('is-active'); });
      el.addEventListener('mouseleave', function () { ring.classList.remove('is-active'); });
    });

    document.addEventListener('mouseleave', function () {
      dot.style.opacity = '0';
      ring.style.opacity = '0';
    });
    document.addEventListener('mouseenter', function () {
      dot.style.opacity = '1';
      ring.style.opacity = '1';
    });
  }

  /* ---------------- Magnetic buttons ---------------- */
  function initMagnetic() {
    if (!isFinePointer || prefersReducedMotion) return;
    var items = document.querySelectorAll('.magnetic');
    items.forEach(function (el) {
      var strength = 18;
      el.addEventListener('mousemove', function (e) {
        var rect = el.getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        el.style.transform = 'translate(' + (x / rect.width) * strength + 'px,' + (y / rect.height) * strength + 'px)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transform = 'translate(0,0)';
      });
    });
  }

  /* ---------------- Smooth in-page anchor scrolling ---------------- */
  function initAnchorScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href').slice(1);
        var target = id ? document.getElementById(id) : null;
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', block: 'start' });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initLoader();
    initNav();
    initScrollProgress();
    initReveal();
    initImageReveal();
    initCursor();
    initMagnetic();
    initAnchorScroll();
  });
})();
