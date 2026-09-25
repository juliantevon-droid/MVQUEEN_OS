document.addEventListener('DOMContentLoaded',()=>{
  const open=document.querySelector('[data-filter-open]');
  const close=document.querySelector('[data-filter-close]');
  const drawer=document.querySelector('[data-filter-drawer]');
  const back=document.querySelector('[data-filter-backdrop]');
  if(!drawer)return;

  const media=window.matchMedia('(max-width: 900px)');
  const focusSelector='a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),summary,[tabindex]:not([tabindex="-1"])';
  let returnFocus=null;

  const setDrawerA11y=openState=>{
    if(!media.matches){
      drawer.removeAttribute('role');
      drawer.removeAttribute('aria-modal');
      drawer.removeAttribute('aria-hidden');
      drawer.removeAttribute('inert');
      return;
    }
    drawer.setAttribute('aria-hidden',String(!openState));
    if(openState){
      drawer.setAttribute('role','dialog');
      drawer.setAttribute('aria-modal','true');
      drawer.removeAttribute('inert');
    }else{
      drawer.removeAttribute('role');
      drawer.removeAttribute('aria-modal');
      drawer.setAttribute('inert','');
    }
  };

  const set=openState=>{
    if(openState&&!media.matches)return;
    if(openState)returnFocus=document.activeElement;
    drawer.classList.toggle('is-open',openState);
    back?.classList.toggle('is-open',openState);
    open?.setAttribute('aria-expanded',String(openState));
    document.documentElement.classList.toggle('mvq-lock',openState);
    setDrawerA11y(openState);
    if(openState){
      close?.focus();
    }else if(returnFocus instanceof HTMLElement){
      returnFocus.focus();
      returnFocus=null;
    }
  };

  const syncMode=()=>{
    if(media.matches){
      if(!drawer.classList.contains('is-open'))setDrawerA11y(false);
    }else{
      drawer.classList.remove('is-open');
      back?.classList.remove('is-open');
      open?.setAttribute('aria-expanded','false');
      document.documentElement.classList.remove('mvq-lock');
      setDrawerA11y(false);
      returnFocus=null;
    }
  };

  open?.addEventListener('click',()=>set(true));
  close?.addEventListener('click',()=>set(false));
  back?.addEventListener('click',()=>set(false));
  media.addEventListener?.('change',syncMode);

  document.addEventListener('keydown',event=>{
    if(!drawer.classList.contains('is-open'))return;
    if(event.key==='Escape'){
      event.preventDefault();
      set(false);
      return;
    }
    if(event.key!=='Tab')return;
    const focusable=[...drawer.querySelectorAll(focusSelector)].filter(el=>el.offsetParent!==null);
    if(!focusable.length)return;
    const first=focusable[0];
    const last=focusable[focusable.length-1];
    if(event.shiftKey&&document.activeElement===first){
      event.preventDefault();
      last.focus();
    }else if(!event.shiftKey&&document.activeElement===last){
      event.preventDefault();
      first.focus();
    }
  });

  syncMode();
});