/* MVQUEEN_OS Control Tower — browser-side status/orchestration contract. */
(() => {
  const CONFIG_URL = "data/os-config.json";
  const GATES_URL = "data/production-gates.json";

  async function loadJSON(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`MVQUEEN_OS: failed to load ${url}`);
    return response.json();
  }

  async function getStatus() {
    const [config, gates] = await Promise.all([
      loadJSON(CONFIG_URL),
      loadJSON(GATES_URL)
    ]);
    return {
      brand: config.brand,
      catalog: config.catalog,
      storefront: config.storefront,
      production: config.production,
      gates: gates.gates,
      executionOrder: gates.executionOrder,
      writePipeline: gates.writePipeline
    };
  }

  function renderGateSummary(target, gates) {
    if (!target) return;
    target.replaceChildren();
    for (const gate of gates) {
      const item = document.createElement("div");
      item.className = `control-gate control-gate-${gate.status}`;
      item.innerHTML = `<span>${gate.id}</span><strong>${gate.name}</strong><small>${gate.status}</small>`;
      target.appendChild(item);
    }
  }

  window.MVQUEENControlTower = Object.freeze({ getStatus, renderGateSummary });
})();
