#!/usr/bin/env node
/**
 * MVQUEEN Lighthouse median gate.
 *
 * Usage:
 *   node lighthouse_median_gate.mjs <mode> <report...>
 * mode: live | preview
 *
 * Uses a 3-run median (or any odd-sized sample) to reduce third-party/platform
 * timing noise without lowering MVQUEEN's enterprise targets or release floors.
 */
import fs from 'node:fs';

const [mode, ...reportPaths] = process.argv.slice(2);
if (!['live', 'preview'].includes(mode) || reportPaths.length < 1) {
  console.error('Usage: node lighthouse_median_gate.mjs <live|preview> <report...>');
  process.exit(2);
}
if (reportPaths.length % 2 === 0) {
  console.error('Use an odd number of Lighthouse reports so the median is deterministic.');
  process.exit(2);
}

const budgetConfig = JSON.parse(
  fs.readFileSync('30_System_Infrastructure/system/registry/performance_budget.json', 'utf8')
);
const reports = reportPaths.map((path) => JSON.parse(fs.readFileSync(path, 'utf8')));
const gate = mode === 'live' ? budgetConfig.liveReleaseGate : budgetConfig.releaseCandidatePreview;
const target = budgetConfig.lighthouse;

const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor(sorted.length / 2)];
};

const checks = {
  performance: 'performance',
  accessibility: 'accessibility',
  bestPractices: 'best-practices',
  seo: 'seo',
};

// Preview is deliberately blocked from indexing, and Shopify-controlled Shop Pay
// and Web Pixel requests can fail on its visitor-preview hostname. Only the
// precisely observed preview-only conditions below are exempted. Raw Lighthouse
// scores, all other required audits, and the live release gate stay unchanged.
const isWorkingPreview = (report) => {
  try {
    const url = new URL(report.finalUrl);
    return url.protocol === 'https:' &&
      /^[a-z0-9]+-76426182854\.shopifypreview\.com$/.test(url.hostname);
  } catch {
    return false;
  }
};

const isShopifyPreviewAsset = (value, report, pathPredicate) => {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' &&
      url.hostname === new URL(report.finalUrl).hostname &&
      pathPredicate(url.pathname);
  } catch {
    return false;
  }
};

const isPixelAsset = (path) =>
  /^\/web-pixels@[^/]+\/app\/web-pixel-[^/]+\/pixel\.modern\.js$/.test(path);

const isKnownPreviewConsoleIssue = (item, report) => {
  const description = item.description ?? '';
  if (item.source === 'network' &&
      description === 'Failed to load resource: the server responded with a status of 404 ()') {
    return isShopifyPreviewAsset(
      item.sourceLocation?.url, report,
      (path) => isPixelAsset(path) || path === '/shopify_pay/accelerated_checkout'
    );
  }
  if (item.source !== 'security') return false;
  if (description.trim() ===
      'Framing \'https://shop.app/\' violates the following Content Security Policy directive: ' +
      '"frame-ancestors https://tsucu0-1i.myshopify.com https://tsucu0-1i.account.myshopify.com https://shopify.com". The request has been blocked.') {
    return true;
  }
  const mime = description.match(
    /^Refused to execute script from '([^']+)' because its MIME type \('text\/html'\) is not executable, and strict MIME type checking is enabled\.$/
  );
  return Boolean(mime &&
    isShopifyPreviewAsset(mime[1], report, isPixelAsset));
};

const hasOnlyKnownPreviewConsoleIssues = (report) => {
  if (!isWorkingPreview(report)) return false;
  const audit = report.audits['errors-in-console'];
  if (audit?.score === 1) return true;
  const items = audit?.details?.items;
  return audit?.score === 0 && Array.isArray(items) &&
    items.length > 0 && items.every((item) => isKnownPreviewConsoleIssue(item, report));
};

const hasOnlyPreviewRobotsSeoBlocker = (report) => {
  if (!isWorkingPreview(report) || report.audits['robots-txt']?.score !== 1) return false;
  const failures = report.categories.seo.auditRefs
    .filter((ref) => ref.weight > 0 && typeof report.audits[ref.id]?.score === 'number' &&
      report.audits[ref.id].score < 1);
  if (failures.length !== 1 || failures[0].id !== 'is-crawlable') return false;
  const blocked = report.audits['is-crawlable']?.details?.items;
  return Array.isArray(blocked) && blocked.some((item) =>
    isShopifyPreviewAsset(item.source?.url, report, (path) => path === '/robots.txt')
  );
};

let failed = false;
const categoryMedians = {};
for (const [budgetKey, categoryKey] of Object.entries(checks)) {
  const values = reports.map((report) => report.categories[categoryKey].score);
  const score = median(values);
  categoryMedians[budgetKey] = score;
  const enterpriseTarget = target[budgetKey];
  console.log(
    `${budgetKey}: runs=[${values.join(', ')}] median=${score} ` +
    `(enterprise target ${enterpriseTarget}, release floor ${gate[budgetKey]})`
  );
  if (score < enterpriseTarget) {
    console.log(
      `::warning::${budgetKey} median is below the MVQUEEN enterprise target; target is retained and not downgraded.`
    );
  }
  if (score < gate[budgetKey]) {
    if (mode === 'preview' && budgetKey === 'seo' &&
        reports.every(hasOnlyPreviewRobotsSeoBlocker)) {
      console.log(
        '::warning::Preview SEO is not launch-certifiable: the only failed SEO audit ' +
        'is the expected Shopify visitor-preview robots.txt indexing block. ' +
        'The raw SEO score is retained; the live release gate still enforces its SEO floor.'
      );
    } else {
      failed = true;
    }
  }
}

for (const [auditId, minimum] of Object.entries(gate.requiredAuditScores ?? {})) {
  const values = reports.map((report) => {
    const score = report.audits[auditId]?.score;
    return typeof score === 'number' ? score : -1;
  });
  const score = median(values);
  console.log(
    `requiredAudit ${auditId}: runs=[${values.join(', ')}] median=${score} (minimum ${minimum})`
  );
  if (score < minimum) {
    if (mode === 'preview' && auditId === 'errors-in-console' &&
        reports.every(hasOnlyKnownPreviewConsoleIssues)) {
      console.log(
        '::warning::Preview console contains only verified Shopify-hosted pixel, ' +
        'accelerated-checkout, and Shop Pay frame failures on the visitor-preview host. ' +
        'The raw audit score remains 0; any unexpected console error still fails. ' +
        'The live release gate has no exception.'
      );
    } else {
      failed = true;
    }
  }
}

const representative = [...reports]
  .sort((a, b) =>
    Math.abs(a.categories.performance.score - categoryMedians.performance) -
    Math.abs(b.categories.performance.score - categoryMedians.performance)
  )[0];

console.log(`Representative requested URL: ${representative.requestedUrl}`);
console.log(`Representative final URL: ${representative.finalUrl}`);
console.log(
  (mode === 'live' ? 'Documented platform overhead: ' : 'Preview-overhead exceptions: ') +
  (
    mode === 'live'
      ? (gate.documentedPlatformOverhead ?? [])
      : (gate.documentedPreviewOverhead ?? [])
  ).join(' | ')
);

for (const id of [
  'errors-in-console',
  'third-party-cookies',
  'largest-contentful-paint',
  'largest-contentful-paint-element',
  'render-blocking-resources',
  'uses-responsive-images',
  'image-size-responsive',
  'image-delivery-insight',
  'lcp-discovery-insight',
  'unused-javascript',
  'mainthread-work-breakdown',
]) {
  const audit = representative.audits[id];
  if (!audit) continue;
  console.log(
    `Representative diagnostic ${id}: ` +
    JSON.stringify({
      score: audit.score,
      title: audit.title,
      displayValue: audit.displayValue,
      details: audit.details?.items?.slice?.(0, 10) ?? audit.details ?? null,
    })
  );
}

if (failed) process.exit(1);
