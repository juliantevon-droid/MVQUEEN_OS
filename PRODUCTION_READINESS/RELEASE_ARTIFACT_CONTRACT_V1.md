# MVQUEEN Release Artifact Contract V1

## Purpose

Keep publishing authorization outside the canonical product record while preserving enough lineage to audit every release decision.

## Required fields

- `release_schema_version`
- `product_id`
- `schema_version`
- `content_fingerprint`
- `decision`
- `actor`
- `timestamp`

## Valid decisions

- `APPROVED_FOR_PUBLISH`
- `BLOCKED`

## Rules

1. Approval applies only to the exact canonical product fingerprint reviewed.
2. Any change to the canonical product record invalidates prior approval.
3. QA must pass before approval can be accepted.
4. An approved publish price must exist.
5. The release artifact authorizes a publisher; it does not perform the Shopify write itself.
6. Release artifacts must be retained with the deployment/audit record.
7. A blocked decision must include the reason in the surrounding operational log.

## Separation of duties

Generation, QA, approval, and publishing remain distinct operations. This contract intentionally prevents a content-generation function from becoming a production publisher.
