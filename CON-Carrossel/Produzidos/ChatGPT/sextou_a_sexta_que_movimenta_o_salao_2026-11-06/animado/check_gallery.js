const {chromium}=require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const path=require('path');const fs=require('fs');const {pathToFileURL}=require('url');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'});
  try{
    const page=await browser.newPage({viewport:{width:1280,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(path.join(__dirname,'..','carrossel_sextou_animado.html')).href,{waitUntil:'load'});
    await page.waitForFunction(()=>[...document.querySelectorAll('video')].every(v=>v.readyState>=1));
    const metadata=await page.evaluate(()=>[...document.querySelectorAll('video')].map(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null})));
    await page.getByRole('button',{name:'Rever animação'}).first().click();
    await page.waitForFunction(()=>document.querySelector('video').currentTime>.3);
    await page.getByRole('button',{name:'Rever animação'}).nth(1).click();
    const firstPaused=await page.locator('video').first().evaluate(v=>v.paused);
    await page.waitForFunction(()=>document.querySelectorAll('video')[1].currentTime>.3);
    await page.evaluate(()=>document.querySelectorAll('video').forEach(v=>v.pause()));
    await page.screenshot({path:path.join(__dirname,'qa','gallery-desktop.png')});
    await page.setViewportSize({width:390,height:844});
    const mobile=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
    const report={metadata,errors,firstPaused,mobile};
    fs.writeFileSync(path.join(__dirname,'qa','gallery-check.json'),JSON.stringify(report,null,2));
    if(errors.length||metadata.length!==7||!firstPaused||mobile.scrollWidth>mobile.width||metadata.some(v=>v.error))throw Error(JSON.stringify(report));
    console.log('Visualizador: 7 vídeos reproduzíveis, controles funcionando, sem erros e sem transbordamento no celular.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
