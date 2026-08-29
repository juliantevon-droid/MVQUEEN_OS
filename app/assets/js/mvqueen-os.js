(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('mvqueen-os-theme');
  if (saved === 'dark') root.dataset.theme = 'dark';

  const toast = (message) => {
    document.querySelector('.toast')?.remove();
    const node = document.createElement('div');
    node.className = 'toast'; node.setAttribute('role', 'status'); node.textContent = message;
    document.body.appendChild(node); window.setTimeout(() => node.remove(), 2600);
  };

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    const dark = root.dataset.theme === 'dark';
    root.dataset.theme = dark ? '' : 'dark';
    localStorage.setItem('mvqueen-os-theme', dark ? 'light' : 'dark');
  });

  document.querySelectorAll('[data-toast]').forEach((button) => button.addEventListener('click', () => toast(button.dataset.toast)));

  document.querySelectorAll('form[data-local-save]').forEach((form) => {
    const key = form.dataset.localSave;
    try {
      const prior = JSON.parse(localStorage.getItem(key) || 'null');
      if (prior) Object.entries(prior).forEach(([name, value]) => { const field = form.elements.namedItem(name); if (field && field.type !== 'file') field.value = value; });
    } catch (_) {}
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      localStorage.setItem(key, JSON.stringify(Object.fromEntries(new FormData(form).entries())));
      toast('Saved locally');
    });
  });

  document.querySelectorAll('[data-config]').forEach(async (node) => {
    try {
      const response = await fetch(node.dataset.config);
      if (!response.ok) throw new Error('config');
      const config = await response.json();
      if (node.dataset.configField) node.textContent = node.dataset.configField.split('.').reduce((obj, key) => obj?.[key], config) ?? '—';
    } catch (_) { /* static fallback remains visible */ }
  });
})();
