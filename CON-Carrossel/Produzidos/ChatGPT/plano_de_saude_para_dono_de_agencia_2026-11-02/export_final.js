const { chromium } = require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const { pathToFileURL } = require('url');
const fs = require('fs');
const path = require('path');

(async () => {
  const base = __dirname;
  const pngDir = path.join(base, 'pngs');
  fs.mkdirSync(pngDir, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(pathToFileURL(path.join(base, 'carrossel_plano_agencia.html')).href, { waitUntil: 'load' });
  await page.waitForFunction(() => document.querySelectorAll('.slide-scaler .slide').length === SLIDES_HTML.length);
  const slideCount = await page.evaluate(() => SLIDES_HTML.length);
  for (let i = 0; i < slideCount; i++) {
    const data = await page.evaluate(async index => (await renderSlide(index)).toDataURL('image/png').split(',')[1], i);
    fs.writeFileSync(path.join(pngDir, 'slide_' + String(i + 1).padStart(2, '0') + '.png'), Buffer.from(data, 'base64'));
  }
  const zipDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Baixar PNGs' }).click();
  await (await zipDownload).saveAs(path.join(base, 'plano_de_saude_para_dono_de_agencia.zip'));
  const pdfDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Baixar PDF' }).click();
  await (await pdfDownload).saveAs(path.join(base, 'plano_de_saude_para_dono_de_agencia_v5.pdf'));
  if (errors.length) throw new Error(errors.join('; '));
  console.log('Exportados ' + slideCount + ' PNGs, ZIP e PDF.');
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
