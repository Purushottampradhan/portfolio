(function () {
  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var header = document.getElementById("site-header");
  function onScrollHeader() {
    if (!header) return;
    var y = window.scrollY || document.documentElement.scrollTop;
    header.classList.toggle("is-scrolled", y > 20);
  }
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  var rolesEl = document.getElementById("hero-roles");
  var phrases = [
    "production-grade MERN & Angular platforms.",
    "resilient microservices, queues & APIs.",
    "LLM, RAG & speech stacks for real users.",
  ];

  if (rolesEl) {
    if (prefersReducedMotion()) {
      rolesEl.textContent = phrases[0];
    } else {
      var phraseIndex = 0;
      var charIndex = 0;
      var deleting = false;
      var tickTimer;

      function schedule(ms, fn) {
        if (tickTimer) window.clearTimeout(tickTimer);
        tickTimer = window.setTimeout(fn, ms);
      }

      function tick() {
        var phrase = phrases[phraseIndex];
        if (!deleting) {
          charIndex += 1;
          rolesEl.textContent = phrase.slice(0, charIndex);
          if (charIndex >= phrase.length) {
            deleting = true;
            schedule(2200, tick);
            return;
          }
          schedule(38, tick);
        } else {
          charIndex -= 1;
          rolesEl.textContent = phrase.slice(0, Math.max(charIndex, 0));
          if (charIndex <= 0) {
            deleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            schedule(380, tick);
            return;
          }
          schedule(26, tick);
        }
      }

      schedule(700, tick);
    }
  }

  if (!prefersReducedMotion()) {
    document.querySelectorAll(".card-tilt").forEach(function (card) {
      card.addEventListener(
        "mousemove",
        function (e) {
          var r = card.getBoundingClientRect();
          var x = e.clientX - r.left - r.width / 2;
          var y = e.clientY - r.top - r.height / 2;
          var cap = 9;
          var rx = Math.max(Math.min((y / r.height) * -cap, cap), -cap);
          var ry = Math.max(Math.min((x / r.width) * cap, cap), -cap);
          card.style.transform =
            "perspective(880px) rotateX(" +
            rx +
            "deg) rotateY(" +
            ry +
            "deg) translateY(-6px)";
        },
        { passive: true }
      );
      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });
  }

  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    function setStaggerDelay(el) {
      var parent = el.parentElement;
      if (!parent) return;
      var index = Array.prototype.indexOf.call(parent.children, el);
      var delay = Math.min(index * 0.07, 0.42);
      el.style.transitionDelay = delay + "s";
    }

    if (!("IntersectionObserver" in window)) {
      reveals.forEach(function (el) {
        el.classList.add("is-visible");
      });
    } else {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            setStaggerDelay(entry.target);
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -6% 0px", threshold: 0.08 }
      );

      reveals.forEach(function (el) {
        observer.observe(el);
      });
    }
  }
})();
