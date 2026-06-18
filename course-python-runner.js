(function () {
  "use strict";

  const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  const MOBILE_BP = 768;

  let pyodide = null;
  let pyodideLoading = null;

  function isMobile() {
    return window.innerWidth <= MOBILE_BP;
  }

  function getCourseTitle() {
    const headerTitle = document.querySelector("body > header h1");
    if (headerTitle) return headerTitle.textContent.trim();

    const sidebarTitle = document.querySelector(".sidebar h1");
    if (sidebarTitle) return sidebarTitle.textContent.trim();

    return document.title.replace(/\s*\|.*$/, "").trim();
  }

  function isPythonLike(text) {
    if (!text || text.length < 8) return false;
    const markers = [
      /\bdef\s+\w+/,
      /\bimport\s+\w+/,
      /\bfrom\s+\w+\s+import\b/,
      /\bprint\s*\(/,
      /\bfor\s+\w+\s+in\b/,
      /\bwhile\s+/,
      /\bclass\s+\w+/,
      /\bif\s+.+:/,
      /\blambda\b/,
      /\breturn\b/,
    ];
    return markers.some((re) => re.test(text));
  }

  function createNavController(nav) {
    if (!nav.id) nav.id = "course-nav";

    let desktopToggle = null;
    let mobileToggle = null;

    const backdrop = document.createElement("div");
    backdrop.className = "course-nav-backdrop";
    backdrop.setAttribute("aria-hidden", "true");
    document.body.appendChild(backdrop);
    backdrop.addEventListener("click", () => setOpen(false));

    function setOpen(open) {
      if (!isMobile()) {
        nav.classList.add("course-nav-open");
        return;
      }

      nav.classList.toggle("course-nav-open", open);
      document.body.classList.toggle("course-nav-drawer-open", open);
      backdrop.classList.toggle("is-visible", open);
      backdrop.setAttribute("aria-hidden", String(!open));
      [desktopToggle, mobileToggle].forEach((btn) => {
        if (!btn) return;
        btn.setAttribute("aria-expanded", String(open));
        btn.textContent = open ? "Close" : "Contents";
      });
    }

    function toggle() {
      if (!isMobile()) return;
      setOpen(!nav.classList.contains("course-nav-open"));
    }

    nav.querySelectorAll("a[href^='#']").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });

    return {
      bindToggle(button) {
        if (!button) return;
        button.setAttribute("aria-controls", nav.id);
        button.addEventListener("click", (e) => {
          e.stopPropagation();
          toggle();
        });
        if (button.classList.contains("course-nav-toggle")) desktopToggle = button;
        if (button.classList.contains("course-topbar-menu")) mobileToggle = button;
      },
      close: () => setOpen(false),
    };
  }

  function setupMobileTopbar(navController) {
    const bar = document.createElement("div");
    bar.className = "course-topbar";
    bar.setAttribute("role", "banner");
    bar.innerHTML = `
      <a class="course-topbar-back" href="index.html">← Portfolio</a>
      <span class="course-topbar-title"></span>
      <button type="button" class="course-topbar-menu" aria-expanded="false">Contents</button>
    `;

    bar.querySelector(".course-topbar-title").textContent = getCourseTitle();
    document.body.prepend(bar);

    navController.bindToggle(bar.querySelector(".course-topbar-menu"));
  }

  function setupPortfolioBackLink() {
    if (document.querySelector(".portfolio-back")) return;
    const link = document.createElement("a");
    link.className = "portfolio-back";
    link.href = "index.html";
    link.textContent = "← Portfolio";
    document.body.appendChild(link);
  }

  function setupMobileNav() {
    const nav =
      document.querySelector(".layout > nav") ||
      document.querySelector(".container > .sidebar");
    if (!nav) return;

    const controller = createNavController(nav);
    setupMobileTopbar(controller);

    if (!isMobile()) {
      nav.classList.add("course-nav-open");
    }

    window.addEventListener("resize", () => {
      if (isMobile()) {
        nav.classList.remove("course-nav-open");
      } else {
        nav.classList.add("course-nav-open");
        document.body.classList.remove("course-nav-drawer-open");
        document.querySelector(".course-nav-backdrop")?.classList.remove("is-visible");
      }
    });
  }

  function patchAICourseScroll() {
    const contentPanel = document.querySelector(".container > .content");
    const sidebar = document.querySelector(".container > .sidebar");
    if (!contentPanel || !sidebar) return;

    let scrollTimer;
    let resizeTimer;

    function usesWindowScroll() {
      const style = getComputedStyle(contentPanel);
      return style.overflowY === "visible" || style.overflow === "visible";
    }

    function scrollOffset() {
      return isMobile() ? 68 : 32;
    }

    function closeNavDrawer() {
      if (!isMobile()) return;

      sidebar.classList.remove("course-nav-open");
      document.body.classList.remove("course-nav-drawer-open");
      const backdrop = document.querySelector(".course-nav-backdrop");
      if (backdrop) {
        backdrop.classList.remove("is-visible");
        backdrop.setAttribute("aria-hidden", "true");
      }
      document.querySelectorAll(".course-topbar-menu, .course-nav-toggle").forEach((btn) => {
        btn.setAttribute("aria-expanded", "false");
        btn.textContent = "Contents";
      });
    }

    function scrollToTarget(target) {
      if (!target) return;
      const offset = scrollOffset();

      if (usesWindowScroll()) {
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
      } else {
        const contentRect = contentPanel.getBoundingClientRect();
        const targetRect = target.getBoundingClientRect();
        const top = targetRect.top - contentRect.top + contentPanel.scrollTop - 20;
        contentPanel.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
      }
    }

    function updateActiveSection() {
      const sections = contentPanel.querySelectorAll("h2[id], h3[id], h4[id]");
      const links = sidebar.querySelectorAll('a[href^="#"]');
      let current = "";
      const offset = scrollOffset() + 20;

      sections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= offset) current = section.getAttribute("id") || "";
      });

      links.forEach((link) => {
        const href = link.getAttribute("href");
        link.classList.toggle("active", href === `#${current}`);
      });
    }

    function onScroll() {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(updateActiveSection, 50);
    }

    function handleAnchorClick(e) {
      const link = e.currentTarget;
      const href = link.getAttribute("href");
      if (!href || href === "#" || href === "#table-of-contents") return;

      const target = document.getElementById(href.slice(1));
      if (!target || !target.closest(".content")) return;

      e.preventDefault();

      closeNavDrawer();

      // Wait for drawer close layout shift before scrolling
      requestAnimationFrame(() => {
        requestAnimationFrame(() => scrollToTarget(target));
      });

      if (history.pushState) {
        history.pushState(null, "", href);
      } else {
        window.location.hash = href;
      }
    }

    sidebar.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener("click", handleAnchorClick, true);
    });

    window.addEventListener("scroll", onScroll, { passive: true });
    contentPanel.addEventListener("scroll", onScroll, { passive: true });

    if (window.location.hash) {
      const target = document.querySelector(window.location.hash);
      if (target && target.closest(".content")) {
        setTimeout(() => scrollToTarget(target), 200);
      }
    }

    updateActiveSection();

    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(updateActiveSection, 150);
    });
  }

  async function loadPyodide() {
    if (pyodide) return pyodide;
    if (pyodideLoading) return pyodideLoading;

    pyodideLoading = (async () => {
      if (!window.loadPyodide) {
        await new Promise((resolve, reject) => {
          const script = document.createElement("script");
          script.src = `${PYODIDE_BASE}pyodide.js`;
          script.onload = resolve;
          script.onerror = () => reject(new Error("Failed to load Pyodide"));
          document.head.appendChild(script);
        });
      }
      pyodide = await window.loadPyodide({ indexURL: PYODIDE_BASE });
      return pyodide;
    })();

    return pyodideLoading;
  }

  async function maybeLoadMLPackages(code, statusEl) {
    const packages = new Set();
    if (/\b(numpy|np\.)\b/.test(code)) packages.add("numpy");
    if (/\b(pandas|pd\.)\b/.test(code)) packages.add("pandas");
    if (/\b(scipy)\b/.test(code)) packages.add("scipy");
    if (/\b(sklearn)\b/.test(code)) packages.add("scikit-learn");
    if (/\b(matplotlib|plt\.)\b/.test(code)) packages.add("matplotlib");
    if (!packages.size) return;

    statusEl.textContent = `Loading ${[...packages].join(", ")}…`;
    await pyodide.loadPackage([...packages]);
  }

  function createEditor() {
    const overlay = document.createElement("div");
    overlay.className = "py-editor-overlay";

    const panel = document.createElement("section");
    panel.className = "py-editor-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-modal", "true");
    panel.setAttribute("aria-label", "Python editor");

    panel.innerHTML = `
      <div class="py-editor-header">
        <div class="py-editor-header-left">
          <h2 class="py-editor-title">Python Editor</h2>
          <div class="py-editor-status" id="py-editor-status">Ready — edit code and press Run</div>
        </div>
        <div class="py-editor-actions">
          <button type="button" class="primary" id="py-run-btn">Run</button>
          <button type="button" id="py-clear-output-btn">Clear output</button>
          <button type="button" id="py-reset-code-btn">Reset</button>
          <button type="button" class="py-editor-close" id="py-close-btn" aria-label="Close editor">✕</button>
        </div>
      </div>
      <div class="py-editor-tabs" role="tablist">
        <button type="button" class="py-editor-tab is-active" data-tab="code" role="tab" aria-selected="true">Code</button>
        <button type="button" class="py-editor-tab" data-tab="output" role="tab" aria-selected="false">Output</button>
      </div>
      <div class="py-editor-body">
        <div class="py-editor-pane is-active" data-pane="code" role="tabpanel">
          <div class="py-editor-pane-label">Code</div>
          <textarea id="py-editor-code" class="py-editor-code" spellcheck="false" aria-label="Python code">print("Hello from Python!")

def add(a, b):
    return a + b

print(add(2, 3))</textarea>
        </div>
        <div class="py-editor-pane" data-pane="output" role="tabpanel">
          <div class="py-editor-pane-label">Output</div>
          <pre id="py-editor-output" class="py-editor-output" aria-label="Program output"></pre>
        </div>
      </div>
    `;

    const fab = document.createElement("button");
    fab.type = "button";
    fab.className = "py-editor-fab";
    fab.textContent = "Python";

    document.body.appendChild(overlay);
    document.body.appendChild(panel);
    document.body.appendChild(fab);

    const codeEl = panel.querySelector("#py-editor-code");
    const outputEl = panel.querySelector("#py-editor-output");
    const statusEl = panel.querySelector("#py-editor-status");
    const tabs = panel.querySelectorAll(".py-editor-tab");
    const panes = panel.querySelectorAll(".py-editor-pane");
    const defaultCode = codeEl.value;

    function setActiveTab(name) {
      tabs.forEach((tab) => {
        const active = tab.dataset.tab === name;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", String(active));
      });
      panes.forEach((pane) => {
        pane.classList.toggle("is-active", pane.dataset.pane === name);
      });
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => setActiveTab(tab.dataset.tab));
    });

    function openPanel(code, options = {}) {
      if (typeof code === "string" && code.trim()) {
        codeEl.value = code.trim();
      }
      document.body.classList.add("py-editor-open");
      overlay.classList.add("is-open");
      panel.classList.add("is-open");
      setActiveTab(options.showOutput ? "output" : "code");
      codeEl.focus();
    }

    function closePanel() {
      document.body.classList.remove("py-editor-open");
      overlay.classList.remove("is-open");
      panel.classList.remove("is-open");
    }

    fab.addEventListener("click", () => openPanel());
    overlay.addEventListener("click", closePanel);
    panel.querySelector("#py-close-btn").addEventListener("click", closePanel);
    panel.addEventListener("click", (e) => e.stopPropagation());

    panel.querySelector("#py-clear-output-btn").addEventListener("click", () => {
      outputEl.textContent = "";
      statusEl.textContent = "Output cleared";
      setActiveTab("output");
    });

    panel.querySelector("#py-reset-code-btn").addEventListener("click", () => {
      codeEl.value = defaultCode;
      statusEl.textContent = "Code reset";
      setActiveTab("code");
    });

    async function runCode() {
      const code = codeEl.value;
      outputEl.textContent = "";
      statusEl.textContent = "Running…";
      setActiveTab("output");

      try {
        await loadPyodide();
        statusEl.textContent = "Pyodide ready";
        await maybeLoadMLPackages(code, statusEl);

        pyodide.setStdout({
          batched: (msg) => {
            outputEl.textContent += msg + "\n";
          },
        });
        pyodide.setStderr({
          batched: (msg) => {
            outputEl.textContent += msg + "\n";
          },
        });

        const result = await pyodide.runPythonAsync(code);
        if (result !== undefined && result !== null) {
          outputEl.textContent += String(result) + "\n";
        }
        statusEl.textContent = "Done";
      } catch (err) {
        outputEl.textContent += (err && err.message) || String(err);
        statusEl.textContent = "Error";
      }
    }

    panel.querySelector("#py-run-btn").addEventListener("click", runCode);

    document.addEventListener("keydown", (e) => {
      if (!panel.classList.contains("is-open")) return;
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        runCode();
      }
      if (e.key === "Escape") closePanel();
    });

    return { openPanel, runCode };
  }

  function attachRunButtons(editor) {
    document.querySelectorAll("pre").forEach((pre) => {
      const codeEl = pre.querySelector("code");
      const clone = pre.cloneNode(true);
      clone.querySelectorAll(".code-run-btn").forEach((btn) => btn.remove());
      const text = (codeEl ? codeEl.textContent : clone.textContent).trim();
      if (!isPythonLike(text)) return;

      pre.classList.add("code-runnable");

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "code-run-btn";
      btn.textContent = "Open";
      btn.title = "Open in Python editor";

      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        editor.openPanel(text);
      });

      pre.appendChild(btn);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("course-page");
    document.documentElement.style.colorScheme = "dark";

    setupPortfolioBackLink();
    setupMobileNav();
    patchAICourseScroll();

    const editor = createEditor();
    attachRunButtons(editor);

    const params = new URLSearchParams(window.location.search);
    const initialCode = params.get("code");
    if (initialCode) {
      try {
        editor.openPanel(decodeURIComponent(initialCode));
      } catch (_) {
        editor.openPanel(initialCode);
      }
    }
  });
})();
