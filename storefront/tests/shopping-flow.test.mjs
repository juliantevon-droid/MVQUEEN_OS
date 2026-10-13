import assert from 'node:assert/strict';
import test from 'node:test';
import { renderSection as render } from './render-theme.mjs';

const variant = { id: 101, available: true, price: 2500, compare_at_price: 3000, title: 'Gold' };
const product = {
  title: 'Queen "Gold" & Pearl', tags: [], metafields: {}, has_only_default_variant: true,
  selected_or_first_available_variant: variant, variants: [variant],
  media: [
    { preview_image: { src: '/first.jpg' }, alt: '' },
    { preview_image: { src: '/second.jpg' }, alt: 'Clasp "detail" & finish' }
  ]
};

test('product gallery renders image elements with safe fallback alt and loading priorities', async () => {
  const document = await render('main-product', { product });
  const images = [...document.querySelectorAll('.mvq-product-media img')];
  assert.equal(images.length, 2);
  assert.equal(images[0].getAttribute('src'), '/first.jpg');
  assert.equal(images[0].getAttribute('alt'), product.title);
  assert.equal(images[0].getAttribute('loading'), 'eager');
  assert.equal(images[0].getAttribute('fetchpriority'), 'high');
  assert.equal(images[1].getAttribute('alt'), product.media[1].alt);
  assert.equal(images[1].getAttribute('loading'), 'lazy');
  assert.equal(document.querySelector('.mvq-product-media').textContent.includes('<img'), false);
});

test('cart image renders without escaping its markup, and retains quantity and checkout controls', async () => {
  const document = await render('main-cart', { cart: {
    item_count: 2, total_price: 5000,
    items: [{ product, image: { src: '/bag.jpg', alt: '' }, variant, quantity: 2,
      final_line_price: 5000, url: '/products/queen', url_to_remove: '/cart/change?line=1&quantity=0' }]
  } });
  const image = document.querySelector('.mvq-cart-image img');
  assert.ok(image);
  assert.equal(image.getAttribute('alt'), product.title);
  assert.equal(image.getAttribute('loading'), 'lazy');
  assert.equal(document.querySelector('[name="updates[]"]').getAttribute('value'), '2');
  assert.equal(document.querySelector('[name="checkout"]').getAttribute('type'), 'submit');
});

const path = '/collections/mvqueen-world/mvq:collection:jewelry';
const listValue = (value) => ({ param_name: 'filter.p.vendor', value, label: value, active: true, count: 2 });
const filters = [
  { type: 'list', label: 'Brand', active_values: [listValue('MVQueen'), listValue('Gold & Pearl')],
    values: [listValue('MVQueen'), listValue('Gold & Pearl')] },
  { type: 'price_range', label: 'Price', active_values: [],
    min_value: { param_name: 'filter.v.price.gte', value: 1299 },
    max_value: { param_name: 'filter.v.price.lte', value: 4500 } }
];

async function renderCollection(overrides = {}) {
  return render('main-collection', {
    request: { path }, collection: {
      url: '/collections/mvqueen-world', handle: 'mvqueen-world', title: 'MVQueen',
      products: [], products_count: 0, filters, sort_by: 'price-descending',
      default_sort_by: 'best-selling',
      sort_options: [{ value: 'best-selling', name: 'Best selling' }, { value: 'price-descending', name: 'Price, high to low' }],
      ...overrides
    }
  });
}

function inputValues(form, name) {
  return [...form.querySelectorAll('input')].filter((input) => input.name === name)
    .map((input) => input.getAttribute('value'));
}

test('sorting preserves all active filters, fractional prices, and the category path', async () => {
  const document = await renderCollection();
  const form = document.querySelector('#CollectionSort').closest('form');
  assert.equal(form.getAttribute('action'), path);
  assert.deepEqual(inputValues(form, 'filter.p.vendor'), ['MVQueen', 'Gold & Pearl']);
  assert.deepEqual(inputValues(form, 'filter.v.price.gte'), ['12.99']);
  assert.deepEqual(inputValues(form, 'filter.v.price.lte'), ['45']);
  assert.equal(form.querySelector('option[selected]').value, 'price-descending');
});

test('applying or clearing filters preserves sorting and the category path', async () => {
  const document = await renderCollection();
  const form = document.querySelector('#CollectionFilters form');
  assert.equal(form.getAttribute('action'), path);
  assert.deepEqual(inputValues(form, 'sort_by'), ['price-descending']);
  const priceInputs = [...form.querySelectorAll('input[type="number"]')];
  assert.deepEqual(priceInputs.map((input) => input.value), ['12.99', '45']);
  assert.ok(priceInputs.every((input) => input.getAttribute('step') === 'any'));
  const clear = new URL(document.querySelector('.mvq-filter-actions a').getAttribute('href'), 'https://example.com');
  assert.equal(clear.pathname, path);
  assert.equal(clear.searchParams.get('sort_by'), 'price-descending');
  assert.equal([...clear.searchParams].length, 1);
});

test('unset price limits stay blank and are not introduced when sorting', async () => {
  const document = await renderCollection({ sort_by: null, filters: [{
    type: 'price_range', label: 'Price', active_values: [],
    min_value: { param_name: 'filter.v.price.gte', value: null },
    max_value: { param_name: 'filter.v.price.lte', value: null }
  }] });
  const sortForm = document.querySelector('#CollectionSort').closest('form');
  assert.deepEqual(inputValues(sortForm, 'filter.v.price.gte'), []);
  assert.deepEqual(inputValues(sortForm, 'filter.v.price.lte'), []);
  assert.deepEqual([...document.querySelectorAll('#CollectionFilters input[type="number"]')].map((input) => input.value), ['', '']);
  assert.deepEqual(inputValues(document.querySelector('#CollectionFilters form'), 'sort_by'), ['best-selling']);
});

test('a zero minimum price remains active when sorting', async () => {
  const document = await renderCollection({ filters: [{
    ...filters[1], min_value: { param_name: 'filter.v.price.gte', value: 0 }
  }] });
  assert.deepEqual(inputValues(document.querySelector('#CollectionSort').closest('form'), 'filter.v.price.gte'), ['0']);
});
