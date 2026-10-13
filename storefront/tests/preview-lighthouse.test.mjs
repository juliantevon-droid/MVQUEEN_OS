import assert from 'node:assert/strict';
import test from 'node:test';
import { assertPreviewIdentity, validatePreviewUrl } from '../../30_System_Infrastructure/automation/preview_lighthouse.mjs';

const canonical = 'https://tsucu0-1i.myshopify.com/?preview_theme_id=155277918406&pb=0';
const visitor = 'https://abc123-76426182854.shopifypreview.com/';
const rendered = {
  url: 'https://tsucu0-1i.myshopify.com/?pb=0',
  theme: { id: 155277918406, role: 'unpublished' },
};

test('allows the exact canonical working preview and store-scoped visitor links', () => {
  assert.equal(validatePreviewUrl(canonical), canonical);
  assert.equal(validatePreviewUrl(`${visitor}?pb=1`), `${visitor}?pb=0`);
});

test('rejects live, other-store, ambiguous, and incorrectly scoped preview targets', () => {
  for (const value of [
    'https://tsucu0-1i.myshopify.com/',
    canonical.replace('155277918406', '155002798278'),
    `${canonical}&preview_theme_id=155277918406`,
    canonical.replace('tsucu0-1i', 'another-store'),
    canonical.replace('https:', 'http:'),
    canonical.replace('https://', 'https://user:password@'),
    canonical.replace('/?', ':8443/?'),
    canonical.replace('/?', '/collections/all?'),
    `${canonical}#preview`,
    visitor.replace('76426182854', '11111111111'),
    visitor.replace('.com/', '.com.example.invalid/'),
    `${visitor}?preview_theme_id=155002798278`,
  ]) assert.throws(() => validatePreviewUrl(value), undefined, value);
});

test('accepts a cookie-preserving redirect only when the audited page renders the unpublished working theme', () => {
  assert.deepEqual(assertPreviewIdentity(canonical, { finalUrl: rendered.url }, rendered), {
    themeId: '155277918406', role: 'unpublished', host: 'tsucu0-1i.myshopify.com',
  });
  const visitorState = { ...rendered, url: visitor };
  assert.equal(assertPreviewIdentity(visitor, { finalUrl: visitor }, visitorState).role, 'unpublished');
});

test('rejects a silent fallback to MAIN even when the audited URL is unchanged', () => {
  for (const theme of [
    { id: 155002798278, role: 'main' },
    { id: 155277918406, role: 'main' },
    { id: 155002798278, role: 'unpublished' },
    { id: 155277918406 },
    null,
  ]) assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: rendered.url }, { ...rendered, theme }));
});

test('rejects failed audits and mismatched final page/report locations', () => {
  assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: rendered.url, runtimeError: { code: 'NO_FCP' } }, rendered));
  assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: visitor }, rendered));
  assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: rendered.url }, { ...rendered, url: visitor }));
  assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: rendered.url, finalDisplayedUrl: visitor }, rendered));
  assert.throws(() => assertPreviewIdentity(canonical, { finalUrl: rendered.url }, { ...rendered, url: `${rendered.url.split('?')[0]}collections/all` }));
});
