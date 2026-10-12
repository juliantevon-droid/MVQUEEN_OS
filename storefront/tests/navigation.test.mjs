import assert from 'node:assert/strict';
import test from 'node:test';
import { renderSection, renderSnippet } from './render-theme.mjs';

const category = (brand, tag, title = tag, links = []) => ({
  title, url: `/collections/${brand}/mvq:collection:${tag}`, links
});
const queen = 'mvqueen-world';
const princess = 'miss-princess-world';
const rootLink = (brand, links) => ({ title: brand, url: `/collections/${brand}`, links });
const catalogs = {
  [queen]: { all_tags: ['mvq:collection:dresses', 'mvq:collection:beauty'] },
  [princess]: { all_tags: ['mvq:collection:beauty'] }
};

async function renderMenu(links, overrides = {}) {
  return renderSection('header', {
    request: { path: '/pages/about', page_type: 'page' },
    routes: { root_url: '/', search_url: '/search', cart_url: '/cart' },
    collections: catalogs,
    section: { settings: { menu: { links } } },
    settings: { show_brand_switcher: false },
    cart: { item_count: 0 },
    ...overrides
  });
}

const menuContainers = (document) => [
  document.querySelector('.mvq-navlinks'), document.querySelector('.mvq-mobile-mega-nav')
];
const hrefs = (container) => [...container.querySelectorAll('a')].map((link) => link.getAttribute('href'));

test('unsupported categories disappear in both menus without losing valid descendants or brand links', async () => {
  const links = [rootLink(queen, [
    category(queen, 'clothing', 'Clothing', [category(queen, 'dresses'), category(queen, 'shoes')]),
    category(queen, 'bags', 'Bags', [category(queen, 'belts')]),
    category(queen, 'beauty')
  ])];
  const document = await renderMenu(links);
  for (const container of menuContainers(document)) {
    const urls = hrefs(container);
    assert.ok(urls.includes(category(queen, 'dresses').url));
    assert.ok(urls.includes(category(queen, 'beauty').url));
    for (const tag of ['clothing', 'shoes', 'bags', 'belts']) {
      assert.ok(!urls.includes(category(queen, tag).url), tag);
    }
    assert.equal(container.querySelector('span').textContent, 'Clothing');
    assert.equal(container.textContent.includes('Bags'), false);
    for (const column of container.querySelectorAll('.mvq-mega-column, .mvq-mobile-mega-cluster')) {
      assert.ok(column.querySelector('a'), 'No empty category column');
    }
  }
  assert.equal(document.querySelector('.mvq-mobile-view-all').getAttribute('href'), `/collections/${queen}`);
});

test('brand catalog tags determine visibility on the house homepage and each brand page', async () => {
  const queenLinks = [rootLink(queen, [category(queen, 'dresses'), category(queen, 'beauty')])];
  const princessLinks = [rootLink(princess, [category(princess, 'dresses'), category(princess, 'beauty')])];
  const linklists = {
    'mvqueen-full-menu': { links: queenLinks },
    'miss-princess-full-menu': { links: princessLinks }
  };
  const paths = [
    ['/', 'index', [category(queen, 'dresses').url, category(princess, 'beauty').url]],
    ['/pages/mvqueen', 'page', [category(queen, 'dresses').url]],
    ['/pages/miss-princess', 'page', [category(princess, 'beauty').url]]
  ];
  for (const [path, page_type, expected] of paths) {
    const document = await renderMenu([], { request: { path, page_type }, linklists });
    for (const container of menuContainers(document)) {
      const urls = hrefs(container);
      expected.forEach((url) => assert.ok(urls.includes(url), `${path}: ${url}`));
      assert.ok(!urls.includes(category(princess, 'dresses').url));
    }
  }
});

test('raw, encoded and handleized known category URLs preserve query strings, fragments and locale prefixes', async () => {
  const urls = [
    `/fr/collections/${queen}/mvq:collection:dresses?sort_by=price-ascending&filter.v.availability=1#products`,
    `/fr/collections/${queen}/mvq-collection-dresses?filter.p.vendor=Gold%20%26%20Pearl`,
    `/fr/collections/${queen}/mvq%3Acollection%3Adresses#products`
  ];
  const hidden = `/fr/collections/${queen}/mvq-collection-shoes?sort_by=price-ascending#products`;
  const document = await renderMenu([...urls, hidden].map((url) => ({ title: url, url, links: [] })), {
    routes: { root_url: '/fr/', search_url: '/fr/search', cart_url: '/fr/cart' }
  });
  menuContainers(document).forEach((container) => assert.deepEqual(hrefs(container), urls));
});

test('full collections, unrelated routes, external URLs and compound tags remain unchanged', async () => {
  const urls = [
    `/collections/${queen}`, '/policies/privacy-policy', '/pages/contact',
    '/collections/other-brand/mvq:collection:shoes', `/collections/${queen}/summer`,
    '/search?q=/collections/mvqueen-world/mvq:collection:shoes',
    'https://example.com/collections/mvqueen-world/mvq:collection:shoes',
    '//example.com/collections/mvqueen-world/mvq:collection:shoes',
    `/collections/${queen}/mvq:collection:dresses+sale`,
    '/pages/example/collections/mvqueen-world/mvq:collection:shoes'
  ];
  const document = await renderMenu(urls.map((url) => ({ title: url, url, links: [] })));
  menuContainers(document).forEach((container) => assert.deepEqual(hrefs(container), urls));
});

test('a brand with no supported categories retains its collection link without empty groups', async () => {
  const document = await renderMenu([rootLink(princess, [category(princess, 'dresses')])]);
  for (const container of menuContainers(document)) {
    assert.deepEqual(hrefs(container), [`/collections/${princess}`]);
    assert.equal(container.querySelector('details'), null);
    assert.equal(container.querySelector('.mvq-mega-column, .mvq-mobile-mega-cluster'), null);
  }
});

test('sold-out categories remain available through all_tags even with an empty filtered product list', async () => {
  const document = await renderMenu([category(queen, 'dresses')], {
    collections: { [queen]: {
      all_tags: ['mvq:collection:dresses'], tags: [], products: [], products_count: 0,
      all_products_count: 1
    } }
  });
  menuContainers(document).forEach((container) => assert.deepEqual(hrefs(container), [category(queen, 'dresses').url]));
});

test('nested menus receive brand tags explicitly without relying on a shared collections scope', async () => {
  for (const mobile of [false, true]) {
    const document = await renderSnippet('mvq-header-menu', {
      mobile,
      mvqueen_tags: catalogs[queen].all_tags,
      princess_tags: catalogs[princess].all_tags,
      links: [rootLink(queen, [category(queen, 'clothing', 'Clothing', [
        category(queen, 'dresses'), category(queen, 'shoes')
      ])]), rootLink(princess, [category(princess, 'beauty'), category(princess, 'dresses')])]
    });
    const urls = hrefs(document);
    assert.ok(urls.includes(category(queen, 'dresses').url));
    assert.ok(urls.includes(category(princess, 'beauty').url));
    assert.ok(!urls.includes(category(queen, 'shoes').url));
    assert.ok(!urls.includes(category(princess, 'dresses').url));
  }
});
