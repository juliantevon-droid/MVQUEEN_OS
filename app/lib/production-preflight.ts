const required = (name: string, value?: string) => {
  if (!value?.trim()) throw new Error(name + " is required");
  return value.trim();
};

function truthy(name: string): boolean {
  return process.env[name] === "true";
}

function scopeSet(): Set<string> {
  return new Set(
    (process.env.SCOPES ?? "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean),
  );
}

export function productionPreflight() {
  const errors: string[] = [];
  const warnings: string[] = [];

  const appUrl = process.env.SHOPIFY_APP_URL?.trim() ?? "";
  const databaseUrl = process.env.DATABASE_URL?.trim() ?? "";
  const scopes = scopeSet();

  for (const name of ["SHOPIFY_API_KEY", "SHOPIFY_API_SECRET", "SHOPIFY_APP_URL", "DATABASE_URL"]) {
    try {
      required(name, process.env[name]);
    } catch (error) {
      errors.push(error instanceof Error ? error.message : String(error));
    }
  }

  if (appUrl && (!appUrl.startsWith("https://") || /example\.com|example\.invalid/i.test(appUrl))) {
    errors.push("SHOPIFY_APP_URL must be the real HTTPS production host");
  }

  if (process.env.MVQ_DATABASE_PROFILE !== "production") {
    errors.push("MVQ_DATABASE_PROFILE must be production");
  }
  if (databaseUrl && !/^postgres(?:ql)?:\/\//i.test(databaseUrl)) {
    errors.push("DATABASE_URL must use PostgreSQL in production");
  }

  const requiredScopes = ["read_products", "write_products", "read_content", "write_content", "read_inventory"];
  if (truthy("MVQ_MEDIA_ALT_SYNC_ENABLED")) {
    requiredScopes.push("read_files", "write_files");
  }
  for (const scope of requiredScopes) {
    if (!scopes.has(scope)) errors.push("Missing required Shopify scope: " + scope);
  }

  if (!truthy("MVQ_WRITE_ENABLED")) {
    errors.push("MVQ_WRITE_ENABLED must be true for live automation");
  }
  if (!truthy("MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED")) {
    errors.push("MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED must be true for hands-off new-product automation");
  }
  if (!truthy("MVQ_EDITORIAL_PUBLISH_ENABLED")) {
    errors.push("MVQ_EDITORIAL_PUBLISH_ENABLED must be true for automatic content/SEO publishing");
  }
  if (!truthy("MVQ_AUTO_CONTENT_SURFACES_ENABLED")) {
    errors.push("MVQ_AUTO_CONTENT_SURFACES_ENABLED must be true for FAQ/blog/collection automation");
  }
  if (!truthy("MVQ_PRODUCT_RECONCILE_ENABLED")) {
    errors.push("MVQ_PRODUCT_RECONCILE_ENABLED must be true for missed-webhook recovery");
  }
  const workerToken = process.env.MVQ_PRODUCT_WORKER_TOKEN?.trim() ?? "";
  if (workerToken.length < 32) {
    errors.push("MVQ_PRODUCT_WORKER_TOKEN must be at least 32 characters for unattended product processing");
  }

  if (!truthy("MVQ_MEDIA_ALT_SYNC_ENABLED")) {
    errors.push("MVQ_MEDIA_ALT_SYNC_ENABLED must be true for full always-on product automation");
  }
  if (!truthy("MVQ_COST_SYNC_ENABLED")) {
    errors.push("MVQ_COST_SYNC_ENABLED must be true for full always-on commercial intelligence");
  }

  return {
    ready: errors.length === 0,
    mode: errors.length === 0 ? "production-automation-ready" : "not-production-ready",
    errors,
    warnings,
    capabilities: {
      productWebhooks: true,
      liveWrites: truthy("MVQ_WRITE_ENABLED"),
      automaticEnrollment: truthy("MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED"),
      editorialSeo: truthy("MVQ_EDITORIAL_PUBLISH_ENABLED"),
      contentSurfaces: truthy("MVQ_AUTO_CONTENT_SURFACES_ENABLED"),
      reconciliation: truthy("MVQ_PRODUCT_RECONCILE_ENABLED"),
      durableWorker: (process.env.MVQ_PRODUCT_WORKER_TOKEN?.trim().length ?? 0) >= 32,
      missingAltRepair: truthy("MVQ_MEDIA_ALT_SYNC_ENABLED"),
      costSync: truthy("MVQ_COST_SYNC_ENABLED"),
    },
  };
}

if (process.argv[1]?.endsWith("production-preflight.ts")) {
  const result = productionPreflight();
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  if (!result.ready) process.exitCode = 1;
}
