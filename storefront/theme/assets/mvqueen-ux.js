document.addEventListener('DOMContentLoaded',()=>{
  // Collection filter behavior lives here; header/menu behavior remains in mvqueen.js.
  const open=document.querySelector('[data-filter-open]');
  const close=document.querySelector('[data-filter-close]');
  const drawer=document.querySelector('[data-filter-drawer]');
  const back=document.querySelector('[data-filter-backdrop]');
  if(!drawer)return;
  const set=v=>{
    drawer.classList.toggle('is-open',v);
    back?.classList.toggle('is-open',v);
    open?.setAttribute('aria-expanded',String(v));
    document.documentElement.classList.toggle('mvq-lock',v);
    if(v) close?.focus(); else open?.focus();
  };
  open?.addEventListener('click',()=>set(true));
  close?.addEventListener('click',()=>set(false));
  back?.addEventListener('click',()=>set(false));
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'&&drawer.classList.contains('is-open'))set(false);
  });
});