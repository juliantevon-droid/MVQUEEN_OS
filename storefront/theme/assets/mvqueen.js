document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.querySelector('[data-mvq-menu]');
  const menuPanel = document.querySelector('[data-mvq-panel]');

  if (menuButton && menuPanel) {
    const setMenu = (open) => {
      if (open) menuPanel.removeAttribute('hidden');
      else menuPanel.setAttribute('hidden', '');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.documentElement.classList.toggle('mvq-menu-open', open);
      document.documentElement.classList.toggle('mvq-lock', open);
      if (open) menuPanel.querySelector('a')?.focus();
      else menuButton.focus();
    };

    menuButton.addEventListener('click', () => setMenu(menuPanel.hasAttribute('hidden')));
    menuPanel.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !menuPanel.hasAttribute('hidden')) setMenu(false);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth >= 750 && !menuPanel.hasAttribute('hidden')) {
        menuPanel.setAttribute('hidden', '');
        menuButton.setAttribute('aria-expanded', 'false');
        document.documentElement.classList.remove('mvq-menu-open', 'mvq-lock');
      }
    }, { passive: true });
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
      });
    });
  });
});
