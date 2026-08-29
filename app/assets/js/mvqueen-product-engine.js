/* MVQUEEN_OS Product Engine — browser-native foundation */
(() => {
  'use strict';
  const PROTECTED = ['Handle','SKU','Inventory','Option1 Value','Option2 Value','Option3 Value','Image Src'];
  const LIMIT = 850;
  function parseCSV(text) {
    const rows=[]; let row=[], cell='', quoted=false;
    for(let i=0;i<text.length;i++){
      const c=text[i], n=text[i+1];
      if(c==='"'){ if(quoted && n==='"'){cell+='"';i++;} else quoted=!quoted; }
      else if(c===',' && !quoted){row.push(cell);cell='';}
      else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(cell);cell='';if(row.some(v=>v!==''))rows.push(row);row=[];}
      else cell+=c;
    }
    if(cell!==''||row.length){row.push(cell);if(row.some(v=>v!==''))rows.push(row);}
    return rows;
  }
  function escapeCSV(v){const s=String(v??'');return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}
  function toCSV(rows){return rows.map(r=>r.map(escapeCSV).join(',')).join('\r\n');}
  function validate(headers,rows){const missing=['Title'].filter(x=>!headers.includes(x));const protectedPresent=PROTECTED.filter(x=>headers.includes(x));return {valid:missing.length===0,missing,protectedPresent,products:Math.max(0,rows.length-1),batches:Math.ceil(Math.max(0,rows.length-1)/LIMIT)};}
  function split(rows){if(rows.length<2)return [];const header=rows[0],data=rows.slice(1),out=[];for(let i=0;i<data.length;i+=LIMIT)out.push([header,...data.slice(i,i+LIMIT)]);return out;}
  function download(content,name,type='text/csv'){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([content],{type}));a.download=name;a.click();URL.revokeObjectURL(a.href);}
  window.MVQUEENProductEngine={parseCSV,toCSV,validate,split,download,PROTECTED,LIMIT};
})();
