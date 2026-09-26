(() => {
  const contextNode = document.getElementById("MVQAnalyticsContext");

  function readContext() {
    if (!contextNode) return {};
    try {
      return JSON.parse(contextNode.textContent || "{}");
    } catch {
      return {};
    }
  }

  const base = readContext();

  function emit(name, detail = {}) {
    window.dispatchEvent(new CustomEvent(name, {
      detail: {
        ...base,
        ...detail,
        event_name: name,
        occurred_at: new Date().toISOString(),
      },
    }));
  }

  function pageEvent() {
    switch (base.page_type) {
      case "product":
        emit("mvq:view_item");
        break;
      case "collection":
        emit("mvq:view_collection");
        break;
      case "cart":
        emit("mvq:view_cart");
        break;
      case "search":
        if (base.search_performed) {
          emit("mvq:search", { search_terms: base.search_terms || null });
        }
        break;
      default:
        break;
    }
  }

  document.addEventListener("DOMContentLoaded", pageEvent, { once: true });

  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    const action = form.action || "";

    if (action.includes("/cart/add")) {
      emit("mvq:add_to_cart", { form_id: form.id || null });
    }

    const submitter = event.submitter;
    const checkoutSubmit =
      action.includes("/checkout") ||
      (submitter instanceof HTMLElement && submitter.getAttribute("name") === "checkout");

    if (checkoutSubmit) {
      emit("mvq:begin_checkout", { cart_item_count: base.cart_item_count ?? null });
    }
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const link = target.closest("a");
    if (!link) return;

    const href = link.getAttribute("href") || "";

    if (href === "/pages/mvqueen") {
      emit("mvq:brand_select", { selected_brand: "MVQueen" });
    } else if (href === "/pages/miss-princess") {
      emit("mvq:brand_select", { selected_brand: "Miss.Princess" });
    } else if (href.includes("/checkout")) {
      emit("mvq:begin_checkout", { cart_item_count: base.cart_item_count ?? null });
    }
  });
})();
