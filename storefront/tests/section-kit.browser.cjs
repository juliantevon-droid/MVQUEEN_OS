const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const source = fs.readFileSync(path.join(__dirname, '../theme/snippets/mvq-section-kit.liquid'), 'utf8');
const css = source.match(/{% stylesheet %}([\s\S]*?){% endstylesheet %}/)[1];
const js = source.match(/{% javascript %}([\s\S]*?){% endjavascript %}/)[1];
const controls = '<div data-controls hidden><button data-previous>Previous</button><span data-status data-format="[current] / [total]"></span><button data-next>Next</button><button data-play data-play-label="Play" data-pause-label="Pause">Play</button></div>';
const carousel = (id, slideshow = false) => `<mvq-carousel id="${id}" data-autoplay="${slideshow}" data-loop="${slideshow}" data-interval="5"><div class="mvq-kit__track ${slideshow ? 'mvq-kit__slides' : ''}" data-track tabindex="0">${Array.from({ length: slideshow ? 3 : 6 }, (_, i) => `<div data-slide class="${slideshow ? 'mvq-kit__slide' : 'mvq-kit__card'}"><h3>Item ${i + 1}</h3><a href="#${id}">View item ${i + 1}</a></div>`).join('')}</div>${controls}</mvq-carousel>`;
const fixture = `<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;font-family:Arial,sans-serif}button{min-height:44px} ${css}</style></head><body><main class="mvq-kit" style="--kit-columns:3;--kit-height:340px;--kit-mobile-height:340px"><div class="mvq-kit__wrap"><h1>Section interaction fixture</h1>
<mvq-tabs id="tabs"><div data-tab-list hidden aria-label="Product information"><button data-tab id="tab-a" aria-controls="panel-a">Collection</button><button data-tab id="tab-b" aria-controls="panel-b">Details</button></div><div data-panel id="panel-a" aria-labelledby="tab-a">Collection content</div><div data-panel id="panel-b" aria-labelledby="tab-b">Product details</div></mvq-tabs>
<mvq-compare id="compare"><div data-compare-stage class="mvq-kit__compare-stage" style="aspect-ratio:3"><span class="mvq-kit__compare-line"></span></div><div data-compare-controls hidden><label for="comparison">Comparison</label><input id="comparison" type="range" min="0" max="100" value="50"></div></mvq-compare>
${carousel('products')}${carousel('slideshow', true)}
<details class="mvq-kit__details" id="accordion"><summary>Shipping</summary><div>Delivery information</div></details>
<mvq-parallax id="parallax" class="mvq-kit__slide" data-strength="24" data-mobile="false"><div class="mvq-kit__backdrop mvq-kit__parallax-media"></div><div class="mvq-kit__caption"><h2>Image banner</h2></div></mvq-parallax>
</div></main><div style="height:800px"></div></body></html>`;

(async () => {
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    page.on('pageerror', error => errors.push(error.message));
    await page.setContent(fixture);
    assert.equal(await page.locator('[data-panel]:visible').count(), 2, 'No-JS tab content stays visible');
    assert.equal(await page.locator('[data-tab-list]').isVisible(), false);
    await page.locator('#accordion summary').click();
    assert.equal(await page.locator('#accordion').getAttribute('open'), '');
    await page.addScriptTag({ content: js });
    await page.locator('#tab-b').click();
    assert.equal(await page.locator('#panel-b').isVisible(), true);
    assert.equal(await page.locator('#panel-a').isVisible(), false);
    await page.keyboard.press('ArrowLeft');
    assert.equal(await page.locator('#tab-a').getAttribute('aria-selected'), 'true');
    assert.equal(await page.locator('#tab-b').getAttribute('tabindex'), '-1');
    await page.keyboard.press('End');
    assert.equal(await page.locator('#tab-b').getAttribute('aria-selected'), 'true');
    await page.locator('#panel-a').dispatchEvent('shopify:block:select');
    assert.equal(await page.locator('#panel-a').isVisible(), true);
    await page.evaluate(() => { const el = document.querySelector('#tabs'); el.remove(); document.querySelector('.mvq-kit__wrap').prepend(el); });
    await page.locator('#tab-b').click();
    assert.equal(await page.locator('#panel-b').isVisible(), true, 'Editor section reinsertion works');

    await page.locator('#comparison').focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#compare').evaluate(el => el.style.getPropertyValue('--kit-position')), '51%');
    const stage = await page.locator('[data-compare-stage]').boundingBox();
    await page.mouse.move(stage.x + stage.width * .2, stage.y + 30);
    await page.mouse.down();
    await page.mouse.move(stage.x + stage.width * .8, stage.y + 30);
    await page.mouse.up();
    assert.ok(Number(await page.locator('#comparison').inputValue()) >= 79, 'Pointer drag updates the comparison');

    await page.locator('#products [data-next]').click();
    await page.waitForFunction(() => document.querySelector('#products').index() === 1);
    await page.locator('#products [data-track]').focus();
    await page.keyboard.press('ArrowLeft');
    await page.waitForFunction(() => document.querySelector('#products').index() === 0);
    await page.evaluate(() => document.querySelector('#products').go(5, true));
    await page.waitForFunction(() => document.querySelector('#products [data-next]').disabled);
    await page.evaluate(() => { const el = document.querySelector('#products'); el.dir = 'rtl'; el.go(0, true); });
    await page.locator('#products [data-next]').click();
    await page.waitForFunction(() => document.querySelector('#products').index() === 1);

    await page.locator('#slideshow').scrollIntoViewIfNeeded();
    await page.mouse.move(0, 0);
    await page.waitForFunction(() => document.querySelector('#slideshow').visible && !document.querySelector('#slideshow').hovered);
    await page.evaluate(() => { const el = document.querySelector('#slideshow'); el.go(0, true); el.paused = false; el.schedule(); });
    await page.waitForFunction(() => document.querySelector('#slideshow').index() === 1, null, { timeout: 8000 });
    assert.equal(await page.locator('#slideshow').evaluate(el => el.index()), 1, 'Autoplay advances a visible slide');
    await page.locator('#slideshow [data-play]').click();
    const stopped = await page.locator('#slideshow').evaluate(el => el.index());
    await page.waitForTimeout(5500);
    assert.equal(await page.locator('#slideshow').evaluate(el => el.index()), stopped, 'Pause prevents advancement');
    await page.locator('#slideshow [data-slide]').last().dispatchEvent('shopify:block:select');
    await page.waitForFunction(() => document.querySelector('#slideshow').index() === 2);
    assert.equal(await page.locator('#slideshow').evaluate(el => el.index()), 2, 'Selecting a slide in the editor reveals it');
    await page.locator('#slideshow [data-next]').click();
    await page.waitForFunction(() => document.querySelector('#slideshow').index() === 0);
    assert.equal(await page.locator('#slideshow').evaluate(el => el.index()), 0, 'Slideshow wraps');
    await page.locator('#accordion').evaluate(el => { el.open = false; });
    await page.locator('#accordion').dispatchEvent('shopify:block:select');
    assert.equal(await page.locator('#accordion').getAttribute('open'), '');

    await page.locator('#parallax').scrollIntoViewIfNeeded();
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.waitForFunction(() => document.querySelector('#slideshow [data-play]').hidden);
    assert.equal(await page.locator('#parallax .mvq-kit__backdrop').evaluate(el => getComputedStyle(el).transform), 'none');
    assert.equal(await page.locator('#slideshow [data-play]').isVisible(), false);

    for (const width of [390, 320]) {
      const mobile = await browser.newPage({ viewport: { width, height: 844 }, isMobile: true, hasTouch: true });
      mobile.on('pageerror', error => errors.push(error.message));
      await mobile.setContent(fixture);
      await mobile.addScriptTag({ content: js });
      assert.equal(await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `No page overflow at ${width}px`);
      const dimensions = await mobile.locator('#products [data-track]').evaluate(el => ({ track: el.clientWidth, card: el.firstElementChild.getBoundingClientRect().width }));
      assert.ok(dimensions.card > dimensions.track / 2 && dimensions.card < dimensions.track, 'Mobile carousel shows the next card edge');
      await mobile.locator('#products [data-track]').evaluate(el => { el.scrollLeft = 150; });
      await mobile.waitForFunction(() => document.querySelector('#products [data-track]').scrollLeft > 0);
      await mobile.locator('#parallax').scrollIntoViewIfNeeded();
      await mobile.waitForFunction(() => document.querySelector('#parallax').style.getPropertyValue('--kit-parallax-y') === '0px');
      await mobile.close();
    }
    const editor = await browser.newPage();
    await editor.setContent(fixture);
    await editor.evaluate(() => { window.Shopify = { designMode: true }; });
    await editor.addScriptTag({ content: js });
    assert.equal(await editor.locator('#slideshow').evaluate(el => el.autoplay), false, 'Editor disables autoplay');
    assert.deepEqual(errors, [], 'No browser errors');
    console.log('PASS: no-JS fallback, tabs/keyboard, comparison drag, carousels/RTL, autoplay/pause, editor lifecycle, mobile overflow, reduced motion.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
