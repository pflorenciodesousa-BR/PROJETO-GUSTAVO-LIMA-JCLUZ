const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const sharp = require('sharp');
const JSZip = require('jszip');
const { PDFDocument } = require('pdf-lib');

const root = __dirname;
const sourcePath = path.join(root, 'carrossel.html');
const outputDir = path.join(root, 'telas');
const previewDir = path.join(root, 'qa-previews');
const assetDir = path.join(root, 'assets');

function makeOfflineHtml() {
  let html = fs.readFileSync(sourcePath, 'utf8');
  for (const name of ['html2canvas.min.js', 'jspdf.umd.min.js', 'jszip.min.js']) {
    const source = `<script src="assets/${name}"></script>`;
    html = html.replace(source, `<script>${fs.readFileSync(path.join(assetDir, name), 'utf8')}</script>`);
  }
  for (const name of ['capa-asa-dourada.png', 'mesa-profissional.png', 'lideranca-mentoria.png', 'Montserrat-Variable.ttf']) {
    const mime = name.endsWith('.png') ? 'image/png' : 'font/ttf';
    const data = `data:${mime};base64,${fs.readFileSync(path.join(assetDir, name)).toString('base64')}`;
    html = html.replaceAll(`assets/${name}`, data);
  }
  fs.writeFileSync(path.join(root, 'carrossel_offline.html'), html);
}

async function main() {
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(previewDir, { recursive: true });
  makeOfflineHtml();

  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    args: ['--allow-file-access-from-files', '--disable-web-security'],
  });
  const page = await browser.newPage({ viewport: { width: 1100, height: 1380 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(pathToFileURL(sourcePath).href, { waitUntil: 'load' });
  await page.evaluate(async () => {
    document.body.classList.add('exporting');
    document.querySelectorAll('.slide').forEach(slide => { slide.style.transform = 'none'; });
    document.querySelectorAll('.slide-shell').forEach(shell => { shell.style.width = '1080px'; shell.style.height = '1350px'; });
    await document.fonts.ready;
    await Promise.all([...document.images].map(img => img.decode()));
  });

  const report = await page.evaluate(() => [...document.querySelectorAll('.slide')].map((slide, index) => {
    const content = slide.querySelector('.content, .cover-copy');
    const box = content?.getBoundingClientRect();
    const slideBox = slide.getBoundingClientRect();
    const words = slide.innerText.replace(/\d\d\s*\/\s*09/g, '').split(/\s+/).filter(Boolean).length;
    return {
      slide: index + 1,
      words,
      contentTop: Math.round(box?.top - slideBox.top || 0),
      contentBottom: Math.round(box?.bottom - slideBox.top || 0),
      overflow: content ? content.scrollHeight > content.clientHeight + 2 : false,
      imageLoaded: [...slide.querySelectorAll('img')].every(img => img.complete && img.naturalWidth > 0),
    };
  }));

  const pdf = await PDFDocument.create();
  const zip = new JSZip();
  const thumbnails = [];
  for (let i = 1; i <= 9; i++) {
    const name = `tela-${String(i).padStart(2, '0')}.png`;
    const buffer = await page.locator(`#slide-${String(i).padStart(2, '0')}`).screenshot({ type: 'png' });
    fs.writeFileSync(path.join(outputDir, name), buffer);
    zip.file(name, buffer);
    const embedded = await pdf.embedPng(buffer);
    const pdfPage = pdf.addPage([1080, 1350]);
    pdfPage.drawImage(embedded, { x: 0, y: 0, width: 1080, height: 1350 });
    thumbnails.push({ input: await sharp(buffer).resize(270, 338).toBuffer(), left: 24 + ((i - 1) % 3) * 294, top: 24 + Math.floor((i - 1) / 3) * 362 });
  }
  fs.writeFileSync(path.join(root, 'do_lixo_a_luz.pdf'), await pdf.save());
  fs.writeFileSync(path.join(root, 'do_lixo_a_luz_telas.zip'), await zip.generateAsync({ type: 'nodebuffer' }));
  await sharp({ create: { width: 906, height: 1110, channels: 3, background: '#262b31' } })
    .composite(thumbnails).png().toFile(path.join(previewDir, 'montagem.png'));

  const offlinePage = await browser.newPage({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
  offlinePage.on('pageerror', e => errors.push(e.message));
  await offlinePage.goto(pathToFileURL(path.join(root, 'carrossel_offline.html')).href, { waitUntil: 'load' });
  const mobileWidth = await offlinePage.locator('.slide-shell').first().evaluate(el => el.getBoundingClientRect().width);
  if (mobileWidth > 390) errors.push(`Prévia móvel excede a largura da janela: ${mobileWidth}px`);
  const [download] = await Promise.all([
    offlinePage.waitForEvent('download', { timeout: 120000 }),
    offlinePage.getByRole('button', { name: 'PNG (ZIP)' }).click(),
  ]);
  if (await download.failure()) errors.push(`Falha no botão ZIP: ${await download.failure()}`);
  await offlinePage.close();

  await browser.close();
  console.log(JSON.stringify({ report, errors, files: fs.readdirSync(root) }, null, 2));
  if (errors.length || report.some(item => item.overflow || !item.imageLoaded || item.contentBottom > 1350)) process.exitCode = 1;
}

main().catch(e => { console.error(e); process.exitCode = 1; });
