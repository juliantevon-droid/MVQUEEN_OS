/* MVQUEEN_OS Catalog QA Engine — deterministic pre-production checks */
(() => {
  'use strict';
  const PROTECTED=new Set(['Handle','SKU','Inventory','Option1 Value','Option2 Value','Option3 Value','Image Src']);
  const SUPPLIER=/\b(ouhoe|miss\.?\s*queen|hoegoa|fanzhen|eelhope|color\s*fit|west\s*&\s*month|supplier|wholesale|generic)\b/i;
  const CLAIM=/\b(cures?|treats?|heals?|guaranteed|clinically\s+proven|medical\s+grade|permanent(?:ly)?|100%\s+(?:safe|effective|guaranteed))\b/i;
  const htmlText=(s='')=>String(s??'').replace(/<[^>]*>/g,' ').replace(/&nbsp;/gi,' ').replace(/\s+/g,' ').trim();
  const clean=(s='')=>htmlText(s).replace(/\s+([,.:])/g,'$1').trim();
  const has=(s,re)=>re.test(String(s??''));
  const field=(p,n)=>String(p?.[n]??'').trim();
  function rowQA(p={}){
    const issues=[],warnings=[],info=[];
    const title=clean(field(p,'Title')), body=clean(field(p,'Body HTML')||field(p,'Description')), type=clean(field(p,'Product Type')), tags=clean(field(p,'Tags')), seoTitle=clean(field(p,'SEO Title')), seoDesc=clean(field(p,'SEO Description')), alt=clean(field(p,'Image Alt Text'));
    if(!title)issues.push('Missing Title');
    if(title.length>70)warnings.push('Title may be too long for search display');
    if(!body)issues.push('Missing product description');
    if(body.length<80)warnings.push('Description is very short');
    if(!type)warnings.push('Missing Product Type');
    if(!tags)warnings.push('Missing Tags');
    if(!seoTitle)warnings.push('Missing SEO Title');
    if(seoTitle.length>70)warnings.push('SEO Title may be too long');
    if(!seoDesc)warnings.push('Missing SEO Description');
    if(seoDesc.length>160)warnings.push('SEO Description exceeds recommended length');
    if(!alt)warnings.push('Missing Image Alt Text');
    if(has([title,body,tags].join(' '),SUPPLIER))issues.push('Third-party/supplier branding detected');
    if(has([title,body,seoDesc].join(' '),CLAIM))issues.push('Potential unsupported product claim');
    if(/<script\b|onerror\s*=|javascript:/i.test(field(p,'Body HTML')))issues.push('Unsafe HTML pattern detected');
    if(/<[^>]+>/.test(field(p,'Title')))issues.push('HTML markup found in Title');
    if(title.toLowerCase().includes('mvqueen')===false)info.push('Brand not explicitly present in title');
    return {ok:issues.length===0,issues,warnings,info};
  }
  function auditRows(headers,rows){const products=[];const summary={products:rows.length,pass:0,review:0,issues:0,warnings:0};rows.forEach((r,i)=>{const p=Object.fromEntries(headers.map((h,j)=>[h,r[j]??'']));const qa=rowQA(p);products.push({row:i+2,qa});if(qa.ok)summary.pass++;else summary.review++;summary.issues+=qa.issues.length;summary.warnings+=qa.warnings.length;});return {summary,products};}
  function assertProtected(headers,before,after){for(const f of PROTECTED){const j=headers.indexOf(f);if(j<0)continue;for(let i=0;i<before.length;i++){if((before[i]?.[j]??'')!==(after[i]?.[j]??''))throw new Error(`QA BLOCK: protected field changed — ${f}, CSV row ${i+2}`);}}return true;}
  function duplicateTitles(headers,rows){const j=headers.indexOf('Title');if(j<0)return [];const seen=new Map(),dupes=[];rows.forEach((r,i)=>{const v=clean(r[j]).toLowerCase();if(!v)return;if(seen.has(v))dupes.push({row:i+2,title:r[j],duplicateOf:seen.get(v)});else seen.set(v,i+2);});return dupes;}
  function htmlHealth(headers,rows){const j=headers.indexOf('Body HTML');if(j<0)return [];const bad=[];rows.forEach((r,i)=>{const v=String(r[j]??'');if((v.match(/<p\b/gi)||[]).length!==(v.match(/<\/p>/gi)||[]).length||/<(?!\/?(p|strong|em|ul|ol|li|br|h[1-6])\b)[^>]+>/i.test(v))bad.push({row:i+2});});return bad;}
  function fullAudit(headers,rows,before=null){const result=auditRows(headers,rows);result.duplicates=duplicateTitles(headers,rows);result.htmlIssues=htmlHealth(headers,rows);if(before){try{result.protectedIntegrity=assertProtected(headers,before,rows);}catch(e){result.protectedIntegrity=false;result.protectedError=e.message;}}else result.protectedIntegrity=true;result.ready=result.summary.review===0&&result.duplicates.length===0&&result.htmlIssues.length===0&&result.protectedIntegrity;return result;}
  window.MVQUEENQA={rowQA,auditRows,assertProtected,duplicateTitles,htmlHealth,fullAudit,PROTECTED};
})();