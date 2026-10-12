import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Liquid } from 'liquidjs';
import { parseHTML } from 'linkedom';

const theme = fileURLToPath(new URL('../theme/', import.meta.url));
const engine = new Liquid({ root: `${theme}/snippets`, extname: '.liquid' });
const escape = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
})[character]);

// Shopify-only presentation tags/filters are small adapters; Liquid expressions,
// filter order, branches and loops are evaluated by the Liquid renderer itself.
for (const name of ['schema', 'doc', 'stylesheet', 'javascript']) {
  engine.registerTag(name, {
    parse(_token, tokens) {
      while (tokens.length) {
        if (tokens.shift().name === `end${name}`) break;
      }
    },
    render() { return ''; }
  });
}

for (const name of ['form', 'paginate']) {
  engine.registerTag(name, {
    parse(token, tokens) {
      this.args = token.args;
      this.templates = [];
      const stream = this.liquid.parser.parseStream(tokens);
      stream.on(`tag:end${name}`, () => stream.stop());
      stream.on('template', (template) => this.templates.push(template));
      stream.start();
    },
    *render(context, emitter) {
      if (name === 'form') {
        const type = this.args.match(/^'([^']+)'/)[1];
        const idExpression = this.args.match(/\bid:\s*([\w.]+)/)?.[1];
        const id = idExpression ? yield this.liquid.evalValue(idExpression, context) : '';
        emitter.write(`<form method="post" action="${type === 'product' ? '/cart/add' : '/cart'}" id="${escape(id)}">`);
      }
      yield this.liquid.renderer.renderTemplates(this.templates, context, emitter);
      if (name === 'form') emitter.write('</form>');
    }
  });
}

engine.registerFilter('image_url', (image) => image.src);
engine.registerFilter('image_tag', (src, ...args) => {
  const attributes = Object.fromEntries(args.filter(Array.isArray));
  return `<img src="${escape(src)}" ${Object.entries(attributes).map(([key, value]) => `${key}="${escape(value)}"`).join(' ')}>`;
});
engine.registerFilter('money', (value) => `$${(Number(value || 0) / 100).toFixed(2)}`);
engine.registerFilter('money_without_currency', (value) => (Number(value || 0) / 100).toFixed(2));
engine.registerFilter('t', (value) => value);

export async function renderSection(section, data) {
  const source = await readFile(`${theme}/sections/${section}.liquid`, 'utf8');
  const context = {
    section: { id: 'test', settings: {} },
    settings: {}, request: { path: '/' }, routes: {}, paginate: { pages: 1 }, ...data
  };
  const html = await engine.parseAndRender(source, context, { globals: context });
  return parseHTML(`<html><body>${html}</body></html>`).document;
}

export async function renderSnippet(snippet, data) {
  const html = await engine.renderFile(snippet, data);
  return parseHTML(`<html><body>${html}</body></html>`).document;
}

