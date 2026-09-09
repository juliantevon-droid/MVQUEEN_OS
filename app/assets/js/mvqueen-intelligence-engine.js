/* MVQUEEN_OS Product Intelligence Engine — conservative, deterministic catalog intelligence */
(() => {
  'use strict';
  const BRAND='MVQueen';
  const STOP=/\b(ouhoe|miss\.?\s*queen|supplier|wholesale|generic)\b/gi;
  const PROTECTED=new Set(['Handle','SKU','Inventory','Option1 Value','Option2 Value','Option3 Value','Image Src']);
  const clean=(s='')=>String(s??'').replace(STOP,'').replace(/\s{2,}/g,' ').replace(/\s+([,.:])/g,'$1').trim();
  const text=(s='')=>clean(String(s).replace(/<[^>]*>/g,' '));
  const first=(s='')=>text(s).split(/[|;\n]+/).map(x=>x.trim()).filter(Boolean)[0]||'';
  const has=(s,re)=>re.test(text(s).toLowerCase());
  const CATEGORY_RULES=[
    ['Skincare',/\b(serum|cleanser|moisturizer|moisturiser|cream|lotion|toner|essence|facial|face mask|sheet mask|exfoliat|sunscreen|spf|skin care|skincare|eye cream|face oil)\b/i],
    ['Cosmetics',/\b(foundation|concealer|blush|bronzer|highlighter|mascara|eyeliner|eyeshadow|lipstick|lip gloss|lip liner|lip stain|makeup|cosmetic|powder|primer)\b/i],
    ['Jewelry',/\b(necklace|earring|bracelet|ring|jewelry|jewellery|pendant|anklet|brooch)\b/i],
    ['Women’s Fashion',/\b(dress|top|blouse|shirt|skirt|pants|trouser|jeans|jacket|coat|bodysuit|jumpsuit|romper|cardigan|sweater|hoodie|clothing|fashion|set|outfit)\b/i]
  ];
  function source(p={}){return [p.Title,p['Product Type'],p.Tags,p['Body HTML'],p['Short Description'],p.Description,p.Benefits,p.Usage,p.Ingredients,p.Fabric,p.Fit].filter(Boolean).join(' | ');}
  function classifyProduct(p={}){const s=source(p);for(const [category,re] of CATEGORY_RULES)if(re.test(s))return category;return 'Other';}
  function extractByLabel(s,labels){const t=text(s);for(const label of labels){const re=new RegExp(label+'\\s*[:\\-]\\s*([^\\n|;]+)','i');const m=t.match(re);if(m)return clean(m[1]);}return '';}
  function extractAttributes(p={},category=classifyProduct(p)){
    const s=source(p); const a={category,ingredients:'',usage:'',benefits:'',skin_type:'',finish:'',texture:'',fabric:'',fit:'',silhouette:'',occasion:'',care:'',selling_angle:'',keywords:[]};
    a.ingredients=extractByLabel(s,['ingredients','ingredient list'])||first(p.Ingredients);
    a.usage=extractByLabel(s,['usage','how to use','directions'])||first(p.Usage);
    a.benefits=extractByLabel(s,['benefits','key benefits'])||first(p.Benefits);
    a.skin_type=extractByLabel(s,['skin type','skin types'])||first(p.skin_type||p['Skin Type']);
    a.finish=extractByLabel(s,['finish']); a.texture=extractByLabel(s,['texture']);
    a.fabric=extractByLabel(s,['fabric','material'])||first(p.Fabric||p.Material);
    a.fit=extractByLabel(s,['fit'])||first(p.Fit); a.silhouette=extractByLabel(s,['silhouette']);
    a.occasion=extractByLabel(s,['occasion','occasions']); a.care=extractByLabel(s,['care','care instructions']);
    if(category==='Skincare') a.selling_angle=a.benefits||'A polished addition to a simple, consistent skincare routine.';
    else if(category==='Cosmetics') a.selling_angle=a.finish||'An easy beauty essential for a polished, confident look.';
    else if(category==='Jewelry') a.selling_angle='A refined finishing touch designed to elevate everyday looks.';
    else if(category==='Women’s Fashion') a.selling_angle=a.fit||'A feminine wardrobe piece designed for effortless styling.';
    else a.selling_angle='A thoughtfully selected MVQueen piece for modern everyday style.';
    a.keywords=[category,...[a.skin_type,a.finish,a.texture,a.fabric,a.fit,a.silhouette,a.occasion].filter(Boolean)].map(clean).filter(Boolean);
    return a;
  }
  function buildShortDescription(p,a){const n=clean(p.Title)||'This MVQueen piece'; if(a.benefits)return `${n} — ${a.benefits}.`; if(a.usage)return `${n} — designed for easy use as part of your routine.`; return `${n} — ${a.selling_angle}`;}
  function buildBodyHTML(p,a){const n=clean(p.Title)||'MVQueen product'; const existing=text(p['Body HTML']||p.Description); const facts=[]; if(a.benefits)facts.push(`<li><strong>Benefits:</strong> ${a.benefits}</li>`); if(a.usage)facts.push(`<li><strong>Usage:</strong> ${a.usage}</li>`); if(a.ingredients)facts.push(`<li><strong>Ingredients:</strong> ${a.ingredients}</li>`); if(a.skin_type)facts.push(`<li><strong>Skin type:</strong> ${a.skin_type}</li>`); if(a.finish)facts.push(`<li><strong>Finish:</strong> ${a.finish}</li>`); if(a.texture)facts.push(`<li><strong>Texture:</strong> ${a.texture}</li>`); if(a.fabric)facts.push(`<li><strong>Fabric:</strong> ${a.fabric}</li>`); if(a.fit)facts.push(`<li><strong>Fit:</strong> ${a.fit}</li>`); if(a.silhouette)facts.push(`<li><strong>Silhouette:</strong> ${a.silhouette}</li>`); if(a.occasion)facts.push(`<li><strong>Occasion:</strong> ${a.occasion}</li>`); if(a.care)facts.push(`<li><strong>Care:</strong> ${a.care}</li>`); const intro=`<p><strong>${n}</strong> is selected for the MVQueen woman who values modern elegance, confidence, and effortless everyday luxury.</p>`; const factBlock=facts.length?`<ul>${facts.join('')}</ul>`:''; const original=existing && !/^${n}$/i.test(existing)?`<p>${existing}</p>`:''; return `${intro}<p>${a.selling_angle}</p>${factBlock}${original}`.replace(/<p>\s*<\/p>/g,'');}
  function buildTags(p,a){const raw=clean(p.Tags||'').split(',').map(x=>clean(x)).filter(Boolean).filter(x=>!STOP.test(x)); STOP.lastIndex=0; return [...new Set([...raw,a.category,...a.keywords,'MVQueen'].filter(Boolean))].join(', ');}
  function optimizeProduct(p={}){const out={...p}; const category=classifyProduct(p); const a=extractAttributes(p,category); const name=clean(p.Title); if('Title'in out&&name)out.Title=name.toLowerCase().includes(BRAND.toLowerCase())?name:`${name} | ${BRAND}`; if('Product Type'in out)out['Product Type']=category; if('Short Description'in out)out['Short Description']=buildShortDescription(p,a); if('Body HTML'in out)out['Body HTML']=buildBodyHTML(p,a); if('Tags'in out)out.Tags=buildTags(p,a); if('SEO Title'in out)out['SEO Title']=out.Title||name; if('SEO Description'in out)out['SEO Description']=buildShortDescription(p,a).slice(0,157).replace(/\s+\S*$/,'')+'...'; if('Image Alt Text'in out)out['Image Alt Text']=`${name} ${category.toLowerCase()} by ${BRAND}`.trim(); return {product:out,intelligence:a};}
  function auditProduct(p={}){const issues=[];const category=classifyProduct(p);if(!clean(p.Title))issues.push('Missing title');if(category==='Other')issues.push('Category requires review');if(/ouhoe|miss\.?\s*queen|supplier|wholesale|generic/i.test(source(p)))issues.push('Supplier/third-party wording detected');if(/\b(cures?|treats?|heals?|guaranteed|clinically proven)\b/i.test(source(p)))issues.push('Potential unsupported claim');return {ok:issues.length===0,issues,category};}
  function optimizeRows(headers,rows){const results=[];const optimized=rows.map(r=>{const input=Object.fromEntries(headers.map((h,i)=>[h,r[i]??'']));const result=optimizeProduct(input);results.push(result);return headers.map(h=>PROTECTED.has(h)?(r[headers.indexOf(h)]??''):(result.product[h]??''));});return {rows:optimized,results};}
  window.MVQUEENIntelligence={classifyProduct,extractAttributes,buildShortDescription,buildBodyHTML,buildTags,optimizeProduct,auditProduct,optimizeRows,PROTECTED};
})();