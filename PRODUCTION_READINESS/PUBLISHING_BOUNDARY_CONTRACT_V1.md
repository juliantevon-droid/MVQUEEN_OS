# MVQUEEN Publishing Boundary V1

## Purpose

The publishing boundary is the controlled hand-off between the canonical MVQueen production system and any external side effect such as Shopify publishing.

The required path is:

`Canonical Product → Schema/QA → Release Fingerprint → Explicit Approval → Publishing Boundary → External Publisher`

No legacy catalog processor, editorial engine, SEO engine, or generation function may bypass this boundary.

## Preconditions

A release may cross the boundary only when all of the following are true:

1. The canonical product status is `PRODUCTION_READY`.
2. QA has passed and contains no errors.
3. `approved_publish_price` exists.
4. An explicit `APPROVED_FOR_PUBLISH` approval exists.
5. The approval fingerprint exactly matches the current canonical product fingerprint.
6. The approval identifies an actor and timestamp.

If any precondition fails, the boundary returns `BLOCKED` and does not invoke the external publisher.

## Side-effect isolation

The boundary itself does not import or call Shopify APIs. An external publisher is injected as a callable. This keeps authorization separate from transport and makes the gate independently testable.

The publisher receives a deep copy of the approved canonical record. The pipeline-owned record and approval artifact must not be mutated by the publishing side effect.

## Separation of duties

- **Generation:** creates canonical content and intelligence.
- **QA:** validates the canonical record.
- **Approval:** authorizes the exact content fingerprint.
- **Publishing boundary:** enforces authorization before hand-off.
- **Publisher:** performs the external write only after authorization.

Generation must never publish.

## Failure behavior

The system must fail closed. Missing evidence, failed QA, missing price approval, missing approval, stale fingerprints, or invalid approval decisions must result in a held record rather than a partial or silent publish.

Publisher failures must not be represented as successful authorization. The external publisher is responsible for its own transport/error contract and audit details.

## Audit requirements

Every attempted hand-off should retain at minimum:

- product identifier
- canonical content fingerprint
- release decision
- approval actor
- approval timestamp
- boundary result
- publisher result or failure information

The release artifact authorizes publishing; it does not itself perform the external write.

## Legacy path rule

The legacy Shopify catalog processor is not an alternative production path. Direct product, metafield, or variant updates from catalog-processing code are prohibited on the enterprise production branch.

Actual Shopify publishing will be implemented behind a dedicated publisher adapter after this boundary and its tests are established.
