/* MVQUEEN_OS Bulk Engine — deterministic catalog optimization with protected-field guarantees */
(() => {
  'use strict';
  const PROTECTED = new Set(['Handle','SKU','Inventory','Option1 Value','Option2 Value','Option3 Value','Image Src']);
  const ALLOWED = new Set(['Title','Body HTML','Product Type','Tags','Image Alt Text','SEO Title','SEO Description']);
  const STOP = /\b(ouhoe|miss\.?\s*queen|supplier|wholesale|generic)\b/gi;
  const BRAND = 'MVQueen';
  const clean = (s='') => String(s ?? '').replace(STOP,'').replace(/\s{2,}/g,' ').replace(/\s+([,.:])/g,'$1').trim();
  const sentence = (s='') => clean(s).replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();
  const limit = (s,n) => { const x=sentence(s); if(x.length<=n) return x; return x.slice(0,n-3).replace(/\s+\S*$/,'').trim()+'...'; };
  function optimizeTitle(name,type='') {
    const n=clean(name), t=clean(type);
    if(!n) return '';
    return n.toLowerCase().includes(BRAND.toLowerCase()) ? n : `${n}${t && !n.toLowerCase().includes(t.toLowerCase()) ? ' — '+t : ''} | ${BRAND}`;
  }
  function optimizeMeta(name, benefit='') {
    const base=clean(benefit) || `Discover ${clean(name)} from ${BRAND}, designed for effortless confidence and modern elegance.`;
    return limit(base,160);
  }
  function optimizeAlt(name) { return `${clean(name)} product by ${BRAND}`.replace(/\s{2,}/g,' ').trim(); }
  function tags(existing,type='') {
    const raw=clean(existing).split(',').map(x=>x.trim()).filter(Boolean).filter(x=>!STOP.test(x));
    STOP.lastIndex=0;
    const add=[clean(type),'MVQueen'].filter(Boolean);
    return [...new Set([...raw,...add])].join(', ');
  }
  function optimizeBody(body,name,type='') {
    const existing=clean(body);
    if(!existing) return `<p><strong>${clean(name)}</strong> is designed for modern confidence, effortless style, and everyday luxury.</p><p>Shop ${clean(name)} from ${BRAND} and elevate your routine with a polished, feminine finish.</p>`;
    return String(body).replace(STOP,'').replace(/\s{2,}/g,' ').trim();
  }
  function optimizeRow(row) {
    const out={...row};
    const name=clean(row.Title), type=clean(row['Product Type']);
    if('Title' in out) out.Title=optimizeTitle(name,type);
    if('SEO Title' in out) out['SEO Title']=optimizeTitle(name,type);
    if('SEO Description' in out) out['SEO Description']=optimizeMeta(name,row['Short Description']||row.Benefits||row['SEO Description']);
    if('Image Alt Text' in out) out['Image Alt Text']=optimizeAlt(name);
    if('Tags' in out) out.Tags=tags(row.Tags,type);
    if('Body HTML' in out) out['Body HTML']=optimizeBody(row['Body HTML'],name,type);
    if('Product Type' in out) out['Product Type']=type || inferType(name);
    return out;
  }
  function inferType(name) {
    const n=String(name||'').toLowerCase();
    if(/serum|cleanser|moistur|cream|mask|toner|skincare|foundation|lip|mascara|eyeshadow|makeup|cosmetic/.test(n)) return 'Beauty';
    if(/dress|top|skirt|pants|jeans|jacket|coat|bodysuit|clothing|fashion/.test(n)) return 'Women’s Fashion';
    if(/necklace|earring|bracelet|ring|jewelry/.test(n)) return 'Jewelry';
    return '';
  }
  function optimizeRows(headers,rows) {
    const objects=rows.map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]??''])));
    const optimized=objects.map(optimizeRow);
    return optimized.map(o=>headers.map(h=>o[h]??''));
  }
  function diff(headers,before,after) {
    const changes=[];
    for(let i=0;i<before.length;i++) for(let j=0;j<headers.length;j++) {
      const h=headers[j]; if(PROTECTED.has(h)) continue;
      const a=before[i]?.[j]??'', b=after[i]?.[j]??'';
      if(a!==b) changes.push({row:i+2,field:h,before:a,after:b});
    }
    return changes;
  }
  function assertProtected(headers,before,after) {
    for(const field of PROTECTED) {
      const j=headers.indexOf(field); if(j<0) continue;
      for(let i=0;i<before.length;i++) if((before[i]?.[j]??'')!==(after[i]?.[j]??'')) throw new Error(`Protected field changed: ${field} at CSV row ${i+2}`);
    }
    return true;
  }
  window.MVQUEENBulkEngine={PROTECTED,ALLOWED,optimizeRow,optimizeRows,diff,assertProtected};
})();
