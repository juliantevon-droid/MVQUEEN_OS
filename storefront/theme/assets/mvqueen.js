document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('[data-mvq-menu]');
  const panel = document.querySelector('[data-mvq-panel]');
  if (!button || !panel) return;

  const setMenu = (open) => {
    if (open) panel.removeAttribute('hidden');
    else panel.setAttribute('hidden', '');
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.documentElement.classList.toggle('mvq-menu-open', open);
    document.documentElement.classList.toggle('mvq-lock', open);
    if (open) panel.querySelector('a')?.focus();
    else button.focus();
  };

  button.addEventListener('click', () => setMenu(panel.hasAttribute('hidden')));
  panel.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !panel.hasAttribute('hidden')) setMenu(false);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 750 && !panel.hasAttribute('hidden')) {
      panel.setAttribute('hidden', '');
      button.setAttribute('aria-expanded', 'false');
      document.documentElement.classList.remove('mvq-menu-open', 'mvq-lock');
    }
  }, { passive: true });

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
