(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('mvqueen-os-theme');
  if (saved === 'dark') root.dataset.theme = 'dark';

  const toggle = document.getElementById('themeToggle');
  toggle?.addEventListener('click', () => {
    const dark = root.dataset.theme === 'dark';
    root.dataset.theme = dark ? '' : 'dark';
    localStorage.setItem('mvqueen-os-theme', dark ? 'light' : 'dark');
  });

  document.querySelectorAll('[data-toast]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelector('.toast')?.remove();
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.setAttribute('role', 'status');
      toast.textContent = button.dataset.toast;
      document.body.appendChild(toast);
      window.setTimeout(() => toast.remove(), 2600);
    });
  });

  document.querySelectorAll('form[data-local-save]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      localStorage.setItem(form.dataset.localSave, JSON.stringify(data));
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = 'Saved locally';
      document.body.appendChild(toast);
      window.setTimeout(() => toast.remove(), 2200);
    });
  });
})();
