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
  if (score < gate[budgetKey]) failed = true;
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
  if (score < minimum) failed = true;
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
