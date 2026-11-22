/* Anna Nikulina · parallax, reveal, nav state. No dependencies. */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Nav background after scrolling
  var nav = document.querySelector('.nav');
  function onNav() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 40); }

  // Parallax: elements with data-speed move relative to their section
  var layers = [].slice.call(document.querySelectorAll('[data-speed]'));
  var ticking = false;
  function parallax() {
    var vh = window.innerHeight;
    layers.forEach(function (el) {
      var host = el.parentElement.getBoundingClientRect();
      if (host.bottom < -200 || host.top > vh + 200) return;
      var speed = parseFloat(el.getAttribute('data-speed')) || 0;
      var center = host.top + host.height / 2 - vh / 2;
      var max = host.height * 0.2;
      var y = Math.max(-max, Math.min(max, center * -speed));
      el.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)';
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
