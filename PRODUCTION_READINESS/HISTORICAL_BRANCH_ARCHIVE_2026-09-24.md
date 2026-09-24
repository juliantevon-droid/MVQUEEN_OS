# Historical Branch Archive Manifest — 2026-09-24

**Active development branch:** `main`

All branches below are historical recovery references. Their useful logic was audited against `main`; they are not approved merge sources and must not become production deployment sources.

| Historical branch | Preserved head SHA |
|---|---|
| `audit/stabilization-engine` | `46010bc40efb5798e632de9d7f11d2200d5f4190` |
| `build/mvqueen-os-html-foundation` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-html-foundation-v2` | `faedf07ecab9388d56da57d575d2f604377bcce2` |
| `build/mvqueen-os-intelligence` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-build` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-current` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-dev` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-end` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-final` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-go` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-last` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-live` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-ready` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-stage` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-v2` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `build/mvqueen-os-intelligence-work` | `71e1dc1a4296a2f3f343e624c8961c7272ce867b` |
| `feature/module-system` | `6fdf929413ee7558a252c734203940501ed0bfbe` |
| `feature/mvqueen-shopify-backend-v3` | `4047566d9545f633b6f081cb09b8e772e35eb704` |
| `feature/omnieluxe-brand-banks` | `6afb083c14037009b6aa66040431bda562e4ccdb` |
| `feature/shopify-app-runtime` | `26e96ecdc37bcbd0df254b71bd7c94e695e6e6e2` |
| `feature/shopify-backend-foundation` | `6fcd95396bc52c9510ee874b210145f88eaf6a13` |
| `feature/shopify-backend-foundation-v2` | `90180b78b4aa1cfa28f59c5189d034db37c4e8c0` |
| `freeze/pre-production-2026-09-03` | `670000e7a7d2f004dd93af785150135cd64ba466` |
| `integration/mvqueen-catalog-production-control-plane` | `ad42e8f8bd8a3519a982553349b9d1c2ba8e2715` |
| `integration/storefront-design-system-wiring` | `250ac3c7a0137cdb52f1edc9e1713e4336798bf8` |
| `mvqueen-engine-development` | `1ad507455841c1a777d5afa2f3ed14d929fabd24` |
| `production-candidate` | `fa80086c788a0f88e8e54405a1589580b4bed7fd` |
| `production-reconciliation` | `1b1118372a9c071cba6d5f470522925d4af6f2e7` |
| `production/apply-plan` | `b862e00bc9476d230b6cbe68c8d2a607bafcb724` |
| `production/editorial-intelligence-v1` | `4a133cd3a4127b8f3d9f6b9abcbcfb4d00c96951` |
| `production/enterprise-hardening-v1` | `3e445c811385214ee048baa4a9a86d470accb840` |
| `production/launch-build` | `ee748cb9b1bf835e1d8c96ac1e45df0b8760d2a7` |
| `stabilization` | `4d8c387dbb5386e90e48b056c025cdb295772e9a` |

## Policy

- Do not merge these branches wholesale into `main`.
- Recover a specific file/idea only after comparing it with the current canonical implementation.
- No CI/CD, Shopify publishing, or Drive synchronization should target these branches.
- `main` is the only active production line.
- This manifest preserves the exact audited branch heads before any future manual branch deletion.
