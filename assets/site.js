/* Anna Nikulina · parallax, reveal, nav state. No dependencies. */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav background after scrolling
  var nav = document.querySelector('.nav');
  function onNav() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 40); }

  // Parallax: elements with data-speed move relative to their section
  var layers = [].slice.call(document.querySelectorAll('[data-speed],[data-x]'));
  var ticking = false;
  function parallax() {
    var vh = window.innerHeight;
    layers.forEach(function (el) {
      var host = el.parentElement.getBoundingClientRect();
      if (host.bottom < -200 || host.top > vh + 200) return;
      var speed = parseFloat(el.getAttribute('data-speed')) || 0;
      var xs = parseFloat(el.getAttribute('data-x')) || 0;
      var center = host.top + host.height / 2 - vh / 2;
      var max = host.height * 0.4;
      var y = Math.max(-max, Math.min(max, center * -speed));
      if (el._base === undefined) el._base = host.top < vh ? center : 0;
      var x = (center - el._base) * xs;
      el.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
      if (el.hasAttribute('data-fade')) {
        var gone = Math.max(0, -host.top - host.height * 0.25) / (host.height * 0.6);
        el.style.opacity = Math.max(0, 1 - gone).toFixed(3);
      }
    });
    ticking = false;
  }
  function onScroll() {
    onNav();
    if (!reduce && !ticking) { ticking = true; requestAnimationFrame(parallax); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // Reveal on scroll
  var items = [].slice.call(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }
})();

/* Videos: play inside a modal, show all toggle */
(function () {
  var modal = document.querySelector('.vmodal');
  if (!modal) return;
  var frame = modal.querySelector('.vmodal-frame');
  var title = modal.querySelector('.vmodal-title');
  function close() {
    frame.innerHTML = '';
    if (modal.open) modal.close();
  }
  document.querySelectorAll('.vcard-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = btn.getAttribute('data-embed');
      src += (src.indexOf('?') < 0 ? '?' : '&') + 'autoplay=1';
      var f = document.createElement('iframe');
      f.src = src;
      f.title = btn.getAttribute('data-title');
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen; clipboard-write';
      f.allowFullscreen = true;
      frame.innerHTML = '';
      frame.appendChild(f);
      title.textContent = btn.getAttribute('data-title');
      if (modal.showModal) modal.showModal(); else modal.setAttribute('open', '');
    });
  });
  modal.querySelector('.vmodal-close').addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  modal.addEventListener('close', function () { frame.innerHTML = ''; });

  var more = document.querySelector('.vmore');
  if (more) {
    var label = more.textContent, less = more.getAttribute('data-less');
    more.addEventListener('click', function () {
      var sec = document.querySelector('.videos');
      var on = sec.classList.toggle('show-all');
      more.textContent = on ? less : label;
      if (on) sec.querySelectorAll('.vcard.is-extra').forEach(function (el) { el.classList.add('in'); });
    });
  }
})();

/* Glow: soft light follows the cursor over buttons, a flash on click */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.glow').forEach(function (el) {
    function pos(e) {
      var r = el.getBoundingClientRect();
      return { x: e.clientX - r.left, y: e.clientY - r.top };
    }
    el.addEventListener('pointermove', function (e) {
      var p = pos(e);
      el.style.setProperty('--mx', p.x + 'px');
      el.style.setProperty('--my', p.y + 'px');
    });
    el.addEventListener('pointerdown', function (e) {
      var p = pos(e);
      var f = document.createElement('span');
      f.className = 'glow-flash';
      f.style.left = p.x + 'px';
      f.style.top = p.y + 'px';
      el.appendChild(f);
      setTimeout(function () { f.remove(); }, 750);
    });
  });
})();
