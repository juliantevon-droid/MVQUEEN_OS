(() => {
  const toggle = document.getElementById('themeToggle');
  const saved = localStorage.getItem('mvqueen-os-theme');
  if (saved === 'dark') document.documentElement.dataset.theme = 'dark';
  toggle?.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    document.documentElement.dataset.theme = dark ? '' : 'dark';
    localStorage.setItem('mvqueen-os-theme', dark ? 'light' : 'dark');
  });
})();
