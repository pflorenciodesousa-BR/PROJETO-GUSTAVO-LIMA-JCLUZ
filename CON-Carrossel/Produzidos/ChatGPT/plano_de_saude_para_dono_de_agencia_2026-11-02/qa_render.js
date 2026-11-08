const { chromium } = require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const { pathToFileURL } = require('url');
const fs = require('fs');
const path = require('path');

(async () => {
  const base = __dirname;
  const output = path.join(base, 'qa-previews');
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(pathToFileURL(path.join(base, 'carrossel_plano_agencia.html')).href, { waitUntil: 'load' });
  await page.waitForFunction(() => document.querySelectorAll('.slide-scaler .slide').length === SLIDES_HTML.length);
  const slideCount = await page.evaluate(() => SLIDES_HTML.length);
  console.log('libraries', await page.evaluate(() => ({
    html2canvas: typeof html2canvas,
    jspdf: typeof jspdf,
    JSZip: typeof JSZip,
    slides: SLIDES_HTML.length,
    caption: LEGENDA_MODE
  })));
  for (let i = 0; i < slideCount; i++) {
    const measure = await page.evaluate(index => {
      const slide = createSlideElement(index);
      slide.style.position = 'relative';
      document.body.appendChild(slide);
      const sr = slide.getBoundingClientRect();
      const issues = Array.from(slide.querySelectorAll('h2,p,strong,.lead,.note,.check,.cta,.absolute-footer'))
        .filter(el => {
          const r = el.getBoundingClientRect();
          return r.left < sr.left - 2 || r.right > sr.right + 2 || r.top < sr.top - 2 || r.bottom > sr.bottom + 2;
        }).map(el => el.className || el.tagName);
      slide.remove();
      return issues;
    }, i);
    await page.evaluate(index => {
      const slide = createSlideElement(index);
      slide.style.position = 'relative';
      document.body.replaceChildren(slide);
      document.body.style.margin = '0';
    }, i);
    await page.locator('.slide').screenshot({ path: path.join(output, 'view-' + (i + 1) + '.png') });
    await page.goto(pathToFileURL(path.join(base, 'carrossel_plano_agencia.html')).href, { waitUntil: 'load' });
    await page.waitForFunction(() => document.querySelectorAll('.slide-scaler .slide').length === SLIDES_HTML.length);
    const data = await page.evaluate(async index => (await renderSlide(index)).toDataURL('image/png').split(',')[1], i);
    fs.writeFileSync(path.join(output, 'export-' + (i + 1) + '.png'), Buffer.from(data, 'base64'));
    console.log('slide-' + (i + 1), measure.length ? 'overflow: ' + measure.join(',') : 'ok');
  }
  console.log('errors', errors);
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
