# MVQUEEN_OS Production Specialist Agent System

**Version:** 1.0  
**Authority:** Overseer-governed, evidence-driven, fail-closed

## Purpose

This is the canonical production-agent contract. Specialist agents own narrow domains, share evidence through the Overseer, and improve from verified outcomes without silently increasing their authority or rewriting protected rules.

## Production agents

| Agent | Owns | Primary evidence |
|---|---|---|
| Catalog Agent | product normalization, taxonomy, catalog completeness | product records, validation reports |
| Editorial Agent | titles, descriptions, brand vocabulary, factual copy | Brand Bible, source product facts, linter |
| SEO Agent | metadata, internal linking, structured search readiness | SEO audits, indexability, search data |
| Merchandising Agent | collections, navigation, recommendations, product discovery | catalog + collection state |
| Conversion Agent | PDP/collection/home conversion architecture | funnel events, UX audits, experiments |
| Mobile UX Agent | mobile interaction and purchase path | viewport tests, performance/UX evidence |
| Theme Agent | Liquid/theme contracts and storefront components | theme tests, Shopify theme state |
| Shopify Agent | Admin API/runtime integration | API contracts, dry-run output, userErrors |
| Data Agent | metafields, schemas, data quality | schema validation, catalog contracts |
| Performance Agent | speed, payload and rendering efficiency | measured performance evidence |
| Accessibility Agent | semantic/keyboard/screen-reader accessibility | automated + manual accessibility evidence |
| Security Agent | credentials, permissions, unsafe writes | security scans, workflow permissions |
| QA Agent | regression, integration and contract testing | test results, crawler/audit findings |
| Release Agent | production gate and rollback readiness | all specialist evidence + release ledger |

## Coordination

Specialists do not overwrite one another. A finding that crosses domains is escalated to the Overseer, which assigns a primary owner and reviewers.

**Flow:** Evidence → Specialist analysis → Recommendation → Overseer validation → Approval boundary → Change → Tests → Outcome → Learning candidate.

## Learning contract

Agents improve through an outcome ledger. Every reusable lesson must contain:

- immutable lesson ID
- agent/domain
- source finding or change
- hypothesis
- evidence before
- approved action
- verification/test evidence
- evidence after
- outcome: success / failure / inconclusive
- confidence: low / medium / high / verified
- scope where the lesson is valid
- rollback information
- approval state
- timestamps/commit references when available

A lesson may influence future recommendations only after verification. It may become a canonical operating rule only after explicit approval.

### Promotion levels

1. **Observation** — raw evidence; no behavioral effect.
2. **Candidate lesson** — pattern observed; recommendation only.
3. **Verified lesson** — reproduced or directly validated; may adjust prioritization/recommendations.
4. **Approved operating rule** — explicitly approved and version-controlled.
5. **Retired lesson** — contradicted, obsolete, or superseded; retained for audit history.

Agents must not treat correlation as causation. Conversion learning requires measured evidence; copy/SEO learning must preserve factual product truth.

## Authority boundary

Learning never grants new permissions. Agents may inspect, classify, recommend, draft, and test within their declared domain. They may not independently:

- publish a Shopify theme or catalog change
- alter inventory, SKU, variant identity, pricing, handles, credentials, or permissions
- delete or rewrite Drive/Git history
- weaken security, QA, protected-field, brand, or release controls
- invent product attributes, ingredients, certifications, reviews, performance claims, urgency, scarcity, or customer evidence
- promote their own learning candidate into an approved rule

## Conflict resolution

Priority order:

1. security and legal/compliance constraints
2. protected data and factual truth
3. Brand Constitution / Brand Bible
4. production contracts and release safety
5. accessibility and customer usability
6. measured conversion/SEO optimization
7. aesthetic preference

The Overseer records the disposition when specialist recommendations conflict.

## Success standard

The system is improving only when verified outcomes improve reliability, customer usability, factual content quality, search readiness, or measured commerce performance without degrading protected constraints elsewhere.
