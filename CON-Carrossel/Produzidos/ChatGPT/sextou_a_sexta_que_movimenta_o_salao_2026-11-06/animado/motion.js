(() => {
  const clamp = v => Math.max(0, Math.min(1, v));
  const ease = v => 1 - Math.pow(1-clamp(v), 3);
  let slide, moves=[];
  const add = (el,start=.1,duration=.65,kind='text',initial=0) => {
    if(el) moves.push({el,start,duration,kind,initial});
  };
  function box(selector,start,textDelay=.14) {
    const el=slide.querySelector(selector);
    if(!el)return;
    const inner=document.createElement('div');
    inner.className='motion-inner';
    while(el.firstChild)inner.appendChild(el.firstChild);
    el.appendChild(inner);
    add(el,start,.7,'box');
    add(inner,start+textDelay,.65,'text');
  }
  function photo(selector) {
    const frame=slide.querySelector(selector);
    if(!frame)return;
    const cs=getComputedStyle(frame);
    const inner=document.createElement('div');
    Object.assign(inner.style,{position:'absolute',inset:'0',backgroundImage:cs.backgroundImage,backgroundSize:cs.backgroundSize,backgroundPosition:cs.backgroundPosition,backgroundRepeat:'no-repeat',transformOrigin:'center center'});
    frame.style.position='relative';frame.style.backgroundImage='none';frame.appendChild(inner);
    add(frame,.05,.75,'photo-frame',.45);
    add(inner,0,4,'photo');
  }
  window.mountMotion=async(index) => {
    await document.fonts.ready;
    slide?.remove();moves=[];
    slide=createSlideElement(index);
    slide.id='motion-slide';
    Object.assign(slide.style,{position:'fixed',left:'0',top:'0',transform:'none',zIndex:'10000'});
    document.body.append(slide);
    const title=slide.querySelector('h2');
    if(index===0){
      const gold=title.querySelector('.gold');
      const first=document.createElement('span');first.style.display='block';
      while(title.firstChild && title.firstChild!==gold)first.appendChild(title.firstChild);
      title.insertBefore(first,gold);
      add(first,0,.8,'title',1);add(gold,.20,.85,'title',.58);
      add(slide.querySelector('.cover-art'),0,4,'photo');
    } else {
      add(title,0,.8,'title',1);
      if(index===1){
        add(slide.querySelector('.context'),.30,.7);
        box('.invitation',.72,.18);
      }
      if(index===2){
        photo('.img-box-horizontal');
        add(slide.querySelector('.body-copy p'),.35,.7);
        add(slide.querySelector('.last'),.80,.7);
      }
      if(index===3){
        add(slide.querySelector('.gold-rule'),.15,.65,'rule');
        add(slide.querySelector('.body-copy > p'),.30,.7);
        box('.recognition',.70,.15);
        add(slide.querySelector('.closing'),1.15,.75);
      }
      if(index===4){
        add(slide.querySelector('.opening'),0,.8,'title',1);
        photo('.img-box-horizontal');
        add(slide.querySelector('.body-copy'),.35,.7);
        add(slide.querySelector('.because'),.85,.65);
        box('.highlight',1.15,.18);
      }
      if(index===5){
        const el=slide.querySelector('.comp-col');
        add(el,.20,.7,'box');
        el.querySelectorAll('p').forEach((p,i)=>add(p,.35+i*.35,.7));
        add(slide.querySelector('.closing'),1.0,.75);
      }
      if(index===6){
        box('.cta',.35,.15);
        add(slide.querySelector('.context'),.85,.7);
        add(slide.querySelector('.absolute-footer'),1.10,.85,'signature');
      }
    }
    await Promise.all([...slide.querySelectorAll('*')].map(el=>{
      const bg=getComputedStyle(el).backgroundImage;
      if(!bg.startsWith('url('))return;
      return new Promise(resolve=>{const img=new Image();img.onload=resolve;img.onerror=resolve;img.src=bg.slice(5,-2);});
    }));
    window.seekMotion(0);
    return {text:slide.innerText,elements:moves.length};
  };
  window.seekMotion=(time) => {
    for(const m of moves){
      const p=ease((time-m.start)/m.duration);
      if(m.kind==='photo'){
        m.el.style.transform=`scale(${1+.022*p})`;
      } else if(m.kind==='rule'){
        m.el.style.transform=`scaleX(${p})`;
        m.el.style.opacity=String(p);
      } else {
        m.el.style.opacity=String(m.initial+(1-m.initial)*p);
        const dy=(m.kind==='box'?12:m.kind==='title'?14:20)*(1-p);
        const scale=m.kind==='box'?(.985+.015*p):1;
        m.el.style.transform=`translateY(${dy}px) scale(${scale})`;
      }
    }
  };
})();
