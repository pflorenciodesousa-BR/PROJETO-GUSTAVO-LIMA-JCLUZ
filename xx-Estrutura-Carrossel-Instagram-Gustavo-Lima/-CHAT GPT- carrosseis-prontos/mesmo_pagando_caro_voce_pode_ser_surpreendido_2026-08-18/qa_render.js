const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
const path = require('path');
const fs = require('fs');

(async () => {
  const root = __dirname;
  const source = path.join(root, 'carrossel_cancelamento_unilateral.html');
  const output = path.join(root, 'qa-previews');
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1120, height: 1390 }, deviceScaleFactor: 1 });

  for (let index = 0; index < 7; index += 1) {
    await page.goto(pathToFileURL(source).href, { waitUntil: 'load' });
    if (index === 0) {
      const libraries = await page.evaluate(() => ({
        html2canvas: typeof window.html2canvas,
        jspdf: typeof window.jspdf,
      }));
      console.log(`export-libraries: ${libraries.html2canvas}/${libraries.jspdf}`);
      const exportCanvas = await page.evaluate(async () => {
        const canvas = await renderSlide(document.querySelector('.slide'));
        return { width: canvas.width, height: canvas.height };
      });
      if (exportCanvas.width !== 1080 || exportCanvas.height !== 1350) {
        throw new Error(`export-canvas inválido: ${exportCanvas.width}x${exportCanvas.height}`);
      }
      console.log(`export-canvas: ${exportCanvas.width}x${exportCanvas.height}`);
    }
    if (index >= 2 && index <= 5) {
      const content = await page.locator('.slide').nth(index).locator('.inner').innerText();
      const wordCount = content.trim().split(/\s+/).length;
      console.log(`slide-${index + 1}: ${wordCount} palavras`);
    }
    const exportDataUrl = await page.evaluate(async (slideIndex) => {
      const canvas = await renderSlide(document.querySelectorAll('.slide')[slideIndex]);
      return canvas.toDataURL('image/png');
    }, index);
    fs.writeFileSync(
      path.join(output, `export-slide-${index + 1}.png`),
      Buffer.from(exportDataUrl.split(',', 2)[1], 'base64'),
    );
    await page.evaluate(async (slideIndex) => {
      await document.fonts.ready;
      const original = document.querySelectorAll('.slide')[slideIndex];
      const clone = original.cloneNode(true);
      document.body.replaceChildren(clone);
      document.body.style.margin = '0';
      document.body.style.background = '#fff';
      clone.style.position = 'relative';
      clone.style.transform = 'none';
    }, index);

    const issues = await page.locator('.slide').evaluate((slide) => {
      const slideRect = slide.getBoundingClientRect();
      return [...slide.querySelectorAll('*')].flatMap((element) => {
        const style = getComputedStyle(element);
        if (style.display === 'none' || style.visibility === 'hidden') return [];
        const rect = element.getBoundingClientRect();
        const overflow = rect.left < slideRect.left - 1 || rect.top < slideRect.top - 1 || rect.right > slideRect.right + 1 || rect.bottom > slideRect.bottom + 1;
        return overflow ? [`${element.tagName}.${element.className || ''}`] : [];
      });
    });

    console.log(`slide-${index + 1}: ${issues.length ? `overflow ${issues.join(', ')}` : 'ok'}`);
    await page.locator('.slide').screenshot({ path: path.join(output, `slide-${index + 1}.png`) });
  }

  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
