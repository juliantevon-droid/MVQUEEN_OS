import assert from "node:assert/strict";
import { productionPreflight } from "./production-preflight";

const snapshot = { ...process.env };

function restore() {
  for (const key of Object.keys(process.env)) {
    if (!(key in snapshot)) delete process.env[key];
  }
  Object.assign(process.env, snapshot);
}

try {
  Object.assign(process.env, {
    SHOPIFY_API_KEY: "key",
    SHOPIFY_API_SECRET: "secret",
    SHOPIFY_APP_URL: "https://mvqueen.example.shop",
    DATABASE_URL: "postgresql://user:pass@db.example.shop:5432/mvqueen",
    MVQ_DATABASE_PROFILE: "production",
    SCOPES: "read_products,write_products,read_files,write_files",
    MVQ_WRITE_ENABLED: "true",
    MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED: "true",
    MVQ_EDITORIAL_PUBLISH_ENABLED: "true",
    MVQ_MEDIA_ALT_SYNC_ENABLED: "true",
    MVQ_COST_SYNC_ENABLED: "false",
  });
  const ready = productionPreflight();
  assert.equal(ready.ready, true);
  assert.equal(ready.capabilities.automaticEnrollment, true);
  assert.equal(ready.capabilities.editorialSeo, true);
  assert.equal(ready.capabilities.missingAltRepair, true);

  process.env.SHOPIFY_APP_URL = "https://example.com";
  const badHost = productionPreflight();
  assert.equal(badHost.ready, false);
  assert.ok(badHost.errors.some((value) => value.includes("real HTTPS production host")));

  process.env.SHOPIFY_APP_URL = "https://mvqueen.example.shop";
  process.env.MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED = "false";
  const manual = productionPreflight();
  assert.equal(manual.ready, false);
  assert.ok(manual.errors.some((value) => value.includes("AUTO_PRODUCT_ENROLLMENT")));
} finally {
  restore();
}

console.log("production preflight tests passed");
