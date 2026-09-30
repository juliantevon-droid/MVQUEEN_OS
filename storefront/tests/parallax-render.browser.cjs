const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { Liquid } = require(process.env.LIQUID_MODULE || 'liquidjs');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const theme = path.join(__dirname, '../theme');
const source = fs.readFileSync(path.join(theme, 'sections/mvq-parallax.liquid'), 'utf8');
const schema = JSON.parse(source.match(/{% schema %}([\s\S]*?){% endschema %}/)[1]);
const kit = fs.readFileSync(path.join(theme, 'snippets/mvq-section-kit.liquid'), 'utf8');
const css = kit.match(/{% stylesheet %}([\s\S]*?){% endstylesheet %}/)[1];
const js = kit.match(/{% javascript %}([\s\S]*?){% endjavascript %}/)[1];
const clean = text => text.replace(/{%\s*(schema|doc|stylesheet|javascript)\s*%}[\s\S]*?{%\s*end\1\s*%}/g, '');
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'mvq-parallax-test-'));
for (const name of ['mvq-section-kit', 'mvq-section-image', 'mvq-parallax-panel']) {
  fs.writeFileSync(path.join(temp, `${name}.liquid`), clean(fs.readFileSync(path.join(theme, `snippets/${name}.liquid`), 'utf8')));
}
const engine = new Liquid({ root: temp, extname: '.liquid' });
const escape = value => String(value).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
engine.registerFilter('image_url', (image, ...args) => `${image.url}?width=${Object.fromEntries(args).width}`);
engine.registerFilter('image_tag', (url, ...args) => {
  const { widths, ...attrs } = Object.fromEntries(args);
  const srcset = widths.split(',').map(width => `${url.replace(/width=\d+/, `width=${width}`)} ${width}w`).join(', ');
  return `<img src="${escape(url)}" srcset="${escape(srcset)}" width="1600" height="1000" alt="Test image" ${Object.entries(attrs).map(([key, value]) => `${key}="${escape(value)}"`).join(' ')}>`;
});
engine.registerFilter('t', () => 'Select an image and add your message.');
const defaults = Object.fromEntries(schema.settings.filter(setting => setting.id).map(setting => [setting.id, setting.default ?? '']));
const image = name => ({ url: `https://parallax.test/${name}.svg`, width: 1600, height: 1000 });
const block = (id, settings) => ({ id, type: 'image', settings, shopify_attributes: `data-test-block="${id}"` });
const render = (settings = {}, blocks = [], designMode = false, index = 1) => engine.parseAndRender(clean(source), {
  section: { id: 'test-parallax', settings: { ...defaults, ...settings }, blocks, index }, request: { design_mode: designMode }
});
const fixture = body => `<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}${css}</style></head><body>${body}</body></html>`;

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('https://parallax.test/**', route => route.fulfill({ contentType: 'image/svg+xml', body: '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000"><rect width="1600" height="1000" fill="#e3cfbc"/></svg>' }));
    const legacy = { image: image('legacy-desktop'), mobile_image: image('legacy-mobile'), heading: 'Original banner' };
    await page.setContent(fixture(await render(legacy)));
    assert.equal(await page.locator('mvq-parallax').count(), 1, 'Existing single-panel settings remain valid');
    assert.equal(await page.locator('h2').textContent(), 'Original banner');
    await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('legacy-desktop'));
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('legacy-mobile'));

    const blocks = [
      block('first', { image: image('first-desktop'), mobile_image: image('first-mobile'), heading: 'First panel', button_label: 'Shop', button_link: '/collections/all' }),
      block('second', { mobile_image: image('second-mobile-only'), heading: 'Second panel' }),
      block('empty', {})
    ];
    const html = await render({ panel_gap: 0 }, blocks);
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.setContent(fixture(html));
    await page.addScriptTag({ content: js });
    assert.equal(await page.locator('mvq-parallax').count(), 2, 'Blank main panel and empty blocks stay hidden');
    assert.deepEqual(await page.locator('h2').allTextContents(), ['First panel', 'Second panel']);
    assert.equal(await page.locator('[data-test-block="first"] a').getAttribute('href'), '/collections/all');
    assert.equal(await page.locator('img').first().getAttribute('loading'), 'eager');
    assert.equal(await page.locator('img').nth(1).getAttribute('loading'), 'lazy');
    assert.equal(await page.locator('.mvq-kit__parallax-stack').evaluate(el => getComputedStyle(el).gap), '0px');
    await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('first-desktop'));
    await page.locator('[data-test-block="second"]').scrollIntoViewIfNeeded();
    await page.waitForFunction(() => document.querySelector('[data-test-block="second"] img').currentSrc.includes('second-mobile-only'));
    for (const width of [390, 320]) {
      await page.setViewportSize({ width, height: 844 });
      await page.locator('[data-test-block="first"]').scrollIntoViewIfNeeded();
      await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('first-mobile'));
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `No overflow at ${width}px`);
      await page.waitForFunction(() => [...document.querySelectorAll('mvq-parallax')].every(el => el.style.getPropertyValue('--kit-parallax-y') === '0px'));
    }
    await page.emulateMedia({ reducedMotion: 'reduce' });
    assert.equal(await page.locator('.mvq-kit__parallax-media').first().evaluate(el => getComputedStyle(el).transform), 'none');

    await page.setContent(fixture(await render(legacy, [...blocks].reverse(), true, 3)));
    assert.equal(await page.locator('mvq-parallax').count(), 4, 'Editor retains the main panel and every block');
    assert.deepEqual(await page.locator('[data-test-block]').evaluateAll(els => els.map(el => el.dataset.testBlock)), ['empty', 'second', 'first'], 'Block reordering is preserved');
    assert.equal(await page.locator('img[loading="eager"]').count(), 0, 'Lower sections lazy-load their images');
    await page.setContent(fixture(await render({}, [block('desktop-only', { image: image('desktop-only') })])));
    await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('desktop-only'));
    await page.setContent(fixture(await render({ mobile_image: image('main-mobile-only') })));
    await page.waitForFunction(() => document.querySelector('img').currentSrc.includes('main-mobile-only'));
    await page.setContent(fixture(await render()));
    assert.equal(await page.locator('.mvq-kit').count(), 0, 'A fully empty section leaves no storefront gap');
    assert.deepEqual(errors, []);
    console.log('PASS: actual parallax Liquid rendering, legacy settings, multiple/reordered blocks, mobile picture sources, single-image fallbacks, editor placeholders, lazy loading, 320/390px layouts, reduced motion.');
  } finally {
    await browser.close();
    fs.rmSync(temp, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
