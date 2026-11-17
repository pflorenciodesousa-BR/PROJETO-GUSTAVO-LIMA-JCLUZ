const {chromium}=require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const {pathToFileURL}=require('url');
const path=require('path'),fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'});
 try{
  const page=await browser.newPage({viewport:{width:1200,height:1500}});
  await page.goto(pathToFileURL(path.join(__dirname,'carrossel_beneficios.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const report=await page.evaluate(()=>{
   const out=[];
   for(let i=0;i<SLIDES_HTML.length;i++){
    const slide=createSlideElement(i);Object.assign(slide.style,{position:'fixed',left:'0',top:'0',transform:'none'});document.body.append(slide);
    for(const el of slide.querySelectorAll('.cover-title,.slide-two h2,.context,.promise,.benefit-hook,.benefit-body,.comment-card,.slide-save h2,.summary-desc,.slide-final h2,.lead,.cta,.absolute-footer')){
     const rows=new Map();
     const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
     while(walker.nextNode()){
      const node=walker.currentNode;
      for(const match of node.textContent.matchAll(/\S+/g)){
       const range=document.createRange();range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);
       const rect=range.getBoundingClientRect(),key=Math.round(rect.top);
       if(!rows.has(key))rows.set(key,[]);rows.get(key).push(match[0]);
      }
     }
     const lines=[...rows.values()].map(words=>words.join(' '));
     const last=lines.at(-1)||'';
     out.push({slide:i+1,selector:el.className||el.tagName,lines,orphan:lines.length>1&&last.split(/\s+/).length===1});
    }
    slide.remove();
   }
   return out;
  });
  fs.writeFileSync(path.join(__dirname,'qa-previews','typography.json'),JSON.stringify(report,null,2));
  for(const block of report) console.log(`${block.orphan?'ORFA':'OK'} ${block.slide} ${block.selector}: ${block.lines.join(' / ')}`);
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
