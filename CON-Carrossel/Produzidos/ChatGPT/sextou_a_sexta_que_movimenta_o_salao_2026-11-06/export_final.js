const { chromium } = require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const { pathToFileURL } = require('url');
const fs = require('fs');
const path = require('path');

(async () => {
  const base = __dirname;
  const browser = await chromium.launch({headless: true, executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'});
  const page = await browser.newPage({viewport: {width: 1200, height: 1500}, deviceScaleFactor: 1, acceptDownloads: true});
  page.setDefaultTimeout(120000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(pathToFileURL(path.join(base, 'carrossel_sextou.html')).href, {waitUntil: 'load'});
  await page.waitForFunction(() => document.querySelectorAll('.slide-scaler .slide').length === 7);
  const checks = [];
  for (let i = 0; i < 7; i++) {
    const data = await page.evaluate(async index => (await renderSlide(index)).toDataURL('image/png').split(',')[1], i);
    fs.writeFileSync(path.join(base, 'pngs', `slide_${String(i+1).padStart(2,'0')}.png`), Buffer.from(data, 'base64'));
    checks.push(await page.evaluate(index => {
      const slide = createSlideElement(index);
      slide.id = 'qa-slide';
      Object.assign(slide.style, {position:'fixed',left:'0',top:'0',transform:'none',zIndex:'10000'});
      document.body.append(slide);
      const sb = slide.getBoundingClientRect();
      const problems = [];
      for (const el of slide.querySelectorAll('h2,p,.absolute-footer,.recognition')) {
        const box = el.getBoundingClientRect();
        if (box.left < sb.left+50 || box.right > sb.right-50 || box.top < sb.top+45 || box.bottom > sb.bottom-45 || el.scrollWidth > el.clientWidth+2) problems.push({text:el.textContent,top:box.top,bottom:box.bottom,width:box.width,scroll:el.scrollWidth});
      }
      return {slide:index+1,text:slide.innerText,problems};
    }, i));
    await page.locator('#qa-slide').screenshot({path:path.join(base,'qa-previews',`browser-${i+1}.png`)});
    await page.evaluate(() => document.getElementById('qa-slide').remove());
    console.log(`Slide ${i+1}: exportado; ${checks[i].problems.length} problemas de limites.`);
  }
  const zipDownload = page.waitForEvent('download');
  await page.getByRole('button', {name:'Baixar PNGs', exact:true}).click();
  await (await zipDownload).saveAs(path.join(base,'sextou.zip'));
  const pdfDownload = page.waitForEvent('download');
  await page.getByRole('button', {name:'Baixar PDF', exact:true}).click();
  await (await pdfDownload).saveAs(path.join(base,'sextou.pdf'));
  await page.setViewportSize({width:390,height:844});
  await page.waitForTimeout(300);
  const mobile = await page.evaluate(() => ({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,slides:document.querySelectorAll('.slide-scaler .slide').length}));
  fs.writeFileSync(path.join(base,'qa-previews','validation.json'),JSON.stringify({checks,errors,mobile},null,2));
  await browser.close();
  if(errors.length || checks.some(c=>c.problems.length) || mobile.scrollWidth>mobile.viewport) throw Error('Verificar validation.json');
  console.log('7 PNGs, ZIP e PDF exportados. Sem erros de página ou transbordamento.');
})().catch(error=>{console.error(error);process.exit(1)});
