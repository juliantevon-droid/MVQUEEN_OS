/* MVQUEEN_OS SEO Engine — deterministic, editable browser rules */
(() => {
  'use strict';
  const BRAND='MVQueen';
  const STOP=/\b(ouhoe|miss\.?\s*queen|supplier|wholesale|generic)\b/gi;
  const clean=(s='')=>String(s).replace(STOP,'').replace(/\s{2,}/g,' ').replace(/\s+([,.:])/g,'$1').trim();
  const title=(name,type='')=>{const n=clean(name);const t=clean(type);return n.toLowerCase().includes(BRAND.toLowerCase())?n:`${n}${t&&!n.toLowerCase().includes(t.toLowerCase())?' — '+t:''} | ${BRAND}`;};
  const meta=(name,benefit='')=>{const base=clean(benefit||`Discover ${clean(name)} from ${BRAND}, designed for effortless confidence and modern elegance.`);return base.length>160?base.slice(0,157).replace(/\s+\S*$/,'')+'...':base;};
  const alt=(name,context='product')=>`${clean(name)} ${context} by ${BRAND}`.replace(/\s{2,}/g,' ').trim();
  const optimize=(p={})=>({...p,Title:title(p.Title,p['Product Type']),['SEO Title']:title(p.Title,p['Product Type']),['SEO Description']:meta(p.Title,p.Benefits||p['Short Description']),['Image Alt Text']:alt(p.Title)});
  window.MVQUEENSEO={clean,title,meta,alt,optimize};
})();
