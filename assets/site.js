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
