# Security Policy — MVQUEEN OS

## Proprietary System Security

MVQUEEN OS is a proprietary system containing custom code, architecture, brand frameworks, content systems, SEO methodology, automation logic, Shopify integration logic, and business processes developed for MVQueen.

### Repository Visibility — Critical

The source repository must be treated as **private, owner-controlled intellectual property**.

- Repository visibility should be **Private**.
- Do not add collaborators unless access is explicitly required.
- Do not enable public forking.
- Do not publish internal architecture, implementation details, credentials, deployment configuration, or proprietary business logic in public repositories, gists, screenshots, or documentation.
- Keep production credentials, Shopify access tokens, API secrets, webhook secrets, and internal API keys outside Git history.
- If the repository has ever been public, changing visibility does not erase copies, forks, caches, screenshots, or previously exposed commit history. Review historical commits and rotate any credential that may have been exposed.

### Credential Management

- **NEVER** commit plain-text API keys, secrets, access tokens, passwords, or private certificates.
- Use environment variables, GitHub Actions secrets, Shopify-managed credentials, or a secure secret manager.
- Never place a real Shopify token in `.env.example`, documentation, notebooks, CSV exports, or code comments.
- Use placeholders only.

### Source-Control Protection

- Keep `main` as the protected production source of truth.
- Do not create unapproved branches for production work.
- Require review before changes that affect production integrations, customer data, catalog writes, authentication, payments, redirects, or deployment.
- Keep backups and recovery artifacts private.
- Preserve commit history as an ownership and development record.

### Intellectual Property

The MVQUEEN OS structure, custom implementation, proprietary workflows, brand systems, editorial frameworks, SEO architecture, automation methodology, and other original work are proprietary. No license to copy, redistribute, sublicense, publish, or create derivative systems is granted by access to the source code.

### Security Incidents

If proprietary information or credentials are exposed:

1. Revoke or rotate the affected credential immediately.
2. Preserve the relevant commit/hash and evidence.
3. Restrict repository visibility and collaborator access.
4. Review Git history for additional exposure.
5. Document the incident privately.
6. Remove the exposed material from future commits where appropriate; understand that rewriting history does not remove copies already obtained by others.

### Reporting

Report suspected credential exposure, unauthorized access, or unauthorized use of proprietary MVQUEEN OS material privately to the owner. Do not publish sensitive details in public issues or discussions.