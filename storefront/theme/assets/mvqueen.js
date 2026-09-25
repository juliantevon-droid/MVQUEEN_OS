document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.querySelector('[data-mvq-menu]');
  const menuPanel = document.querySelector('[data-mvq-panel]');
  const desktopMenus = [...document.querySelectorAll('.mvq-nav-item')];
  const focusSelector = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),summary,[tabindex]:not([tabindex="-1"])';

  const closeDesktopMenus = (except = null) => {
    desktopMenus.forEach((menu) => {
      if (menu !== except) menu.removeAttribute('open');
    });
  };

  desktopMenus.forEach((menu) => {
    menu.addEventListener('toggle', () => {
      if (menu.open) closeDesktopMenus(menu);
    });
  });

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.mvq-navlinks')) closeDesktopMenus();
  });

  if (menuButton && menuPanel) {
    let returnFocus = null;

    const setMenu = (open) => {
      if (open) {
        returnFocus = document.activeElement;
        menuPanel.removeAttribute('hidden');
        menuPanel.removeAttribute('inert');
        menuPanel.setAttribute('aria-hidden', 'false');
      } else {
        menuPanel.setAttribute('hidden', '');
        menuPanel.setAttribute('inert', '');
        menuPanel.setAttribute('aria-hidden', 'true');
        menuPanel.querySelectorAll('details[open]').forEach((details) => details.removeAttribute('open'));
      }

      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.documentElement.classList.toggle('mvq-menu-open', open);
      document.documentElement.classList.toggle('mvq-lock', open);

      if (open) {
        const first = menuPanel.querySelector(focusSelector);
        first?.focus();
      } else if (returnFocus instanceof HTMLElement) {
        returnFocus.focus();
        returnFocus = null;
      }
    };

    menuButton.addEventListener('click', () => setMenu(menuPanel.hasAttribute('hidden')));
    menuPanel.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));

    document.addEventListener('keydown', (event) => {
      const menuOpen = !menuPanel.hasAttribute('hidden');

      if (event.key === 'Escape') {
        if (menuOpen) {
          event.preventDefault();
          setMenu(false);
        } else {
          closeDesktopMenus();
        }
        return;
      }

      if (event.key !== 'Tab' || !menuOpen) return;
      const focusable = [...menuPanel.querySelectorAll(focusSelector)].filter((element) => element.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth >= 750 && !menuPanel.hasAttribute('hidden')) {
        menuPanel.setAttribute('hidden', '');
        menuPanel.setAttribute('inert', '');
        menuPanel.setAttribute('aria-hidden', 'true');
        menuButton.setAttribute('aria-expanded', 'false');
        menuButton.setAttribute('aria-label', 'Open menu');
        document.documentElement.classList.remove('mvq-menu-open', 'mvq-lock');
        returnFocus = null;
      }
    }, { passive: true });
  }

  document.querySelectorAll('[data-mvq-recommendations]').forEach((shell) => {
    if (!shell.dataset.url || shell.children.length > 0) return;
    fetch(shell.dataset.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw new Error('Recommendations request failed');
        return response.text();
      })
      .then((html) => {
        const documentFragment = new DOMParser().parseFromString(html, 'text/html');
        const incoming = documentFragment.querySelector('[data-mvq-recommendations]');
        if (incoming && incoming.innerHTML.trim()) shell.innerHTML = incoming.innerHTML;
      })
      .catch(() => {
        shell.hidden = true;
      });
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
      });
    });
  });
});
