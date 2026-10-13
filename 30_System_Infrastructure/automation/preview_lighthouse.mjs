#!/usr/bin/env node
/** Audit the working preview and prove the identity of each actual audited page. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const STORE_HOST = 'tsucu0-1i.myshopify.com';
const WORKING_THEME_ID = '155277918406';
const VISITOR_HOST = /^[a-z0-9]+-76426182854\.shopifypreview\.com$/;

export function validatePreviewUrl(value) {
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password || url.port ||
      url.pathname !== '/' || url.hash ||
      (url.hostname !== STORE_HOST && !VISITOR_HOST.test(url.hostname))) {
    throw new Error('Expected an HTTPS MVQUEEN preview homepage URL without credentials, port, or fragment');
  }
  const themeIds = url.searchParams.getAll('preview_theme_id');
  if ((url.hostname === STORE_HOST && themeIds.length !== 1) ||
      themeIds.length > 1 || themeIds.some((id) => id !== WORKING_THEME_ID)) {
    throw new Error(`Preview must target working theme ${WORKING_THEME_ID}`);
  }
  url.searchParams.set('pb', '0');
  return url.href;
}

export function assertPreviewIdentity(targetUrl, report, state) {
  const target = new URL(validatePreviewUrl(targetUrl));
  if (!report || report.runtimeError) throw new Error('Lighthouse failed to audit the preview');
  // A redirect can remove preview_theme_id after Shopify sets the preview cookie.
  // Host checks alone cannot distinguish that preview from the live theme.
  const finalUrls = [report.finalDisplayedUrl ?? report.finalUrl, state?.url];
  for (const value of finalUrls) {
    const url = new URL(value);
    if (url.origin !== target.origin || url.pathname !== '/' || url.username || url.password) {
      throw new Error('The audited page left the intended preview homepage');
    }
  }
  if (String(state?.theme?.id) !== WORKING_THEME_ID || state?.theme?.role !== 'unpublished') {
    throw new Error(`The audited page must render unpublished working theme ${WORKING_THEME_ID}`);
  }
  return { themeId: String(state.theme.id), role: state.theme.role, host: target.hostname };
}

export async function runPreviewSamples({ targetUrl, toolRoot, outputDirectory = '.', samples = 3, chromeFlags = [] }) {
  const target = validatePreviewUrl(targetUrl);
  if (!Number.isInteger(samples) || samples < 1) throw new Error('Sample count must be a positive integer');
  const toolRequire = createRequire(path.resolve(toolRoot, 'package.json'));
  const lighthouseEntry = toolRequire.resolve('lighthouse');
  const lighthouseRequire = createRequire(lighthouseEntry);
  const { default: lighthouse } = await import(pathToFileURL(lighthouseEntry));
  const { launch } = await import(pathToFileURL(toolRequire.resolve('chrome-launcher')));
  // Use the same Puppeteer version as Lighthouse; no dependency in the storefront app.
  const puppeteer = lighthouseRequire('puppeteer-core');
  await fs.mkdir(outputDirectory, { recursive: true });
  for (let sample = 1; sample <= samples; sample++) {
    console.log(`Unpublished Shopify preview sample ${sample}/${samples}`);
    // chrome-launcher creates and later removes a fresh temporary profile per sample.
    const chrome = await launch({ chromeFlags: ['--headless', '--no-sandbox', ...chromeFlags] });
    let browser;
    try {
      browser = await puppeteer.connect({ browserURL: `http://127.0.0.1:${chrome.port}`, defaultViewport: null });
      const page = await browser.newPage();
      // Supplying our own page keeps it open for inspection after Lighthouse. Its
      // default mobile emulation, storage reset, throttling, and audits are retained.
      const result = await lighthouse(target, { port: chrome.port, logLevel: 'error', output: 'json' }, undefined, page);
      const reportPath = path.join(outputDirectory, `preview-lighthouse-${sample}.json`);
      await fs.writeFile(reportPath, JSON.stringify(result?.lhr ?? {}, null, 2));
      const session = await page.createCDPSession();
      let evaluation;
      try {
        evaluation = await session.send('Runtime.evaluate', {
          expression: 'JSON.stringify({url: location.href, theme: window.Shopify?.theme ?? null})',
          returnByValue: true,
        });
      } finally {
        await session.detach();
      }
      if (evaluation.exceptionDetails || typeof evaluation.result?.value !== 'string') {
        throw new Error('Could not inspect the actual Lighthouse page');
      }
      const state = JSON.parse(evaluation.result.value);
      const identity = assertPreviewIdentity(target, result?.lhr, state);
      await fs.writeFile(path.join(outputDirectory, `preview-lighthouse-${sample}-identity.json`), JSON.stringify({
        checkedAt: new Date().toISOString(),
        sample,
        ...identity,
        lighthouseVersion: result.lhr.lighthouseVersion,
        fetchTime: result.lhr.fetchTime,
      }, null, 2));
      console.log(`PASS: sample ${sample} audited unpublished theme ${identity.themeId}`);
    } finally {
      try {
        await browser?.disconnect();
      } finally {
        await chrome.kill();
      }
    }
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const [targetUrl, toolRoot, outputDirectory] = process.argv.slice(2);
  if (!targetUrl || !toolRoot) {
    console.error('Usage: node preview_lighthouse.mjs <preview-url> <temporary-tool-root> [output-directory]');
    process.exitCode = 2;
  } else {
    await runPreviewSamples({ targetUrl, toolRoot, outputDirectory });
  }
}
