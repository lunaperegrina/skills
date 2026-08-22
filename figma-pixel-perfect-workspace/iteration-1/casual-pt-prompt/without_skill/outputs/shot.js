const { chromium } = require('playwright');

(async () => {
  const [,, url, outPath, width, height] = process.argv;
  const browser = await chromium.launch({
    executablePath: '~/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
  });
  const page = await browser.newPage({
    viewport: { width: Number(width || 1440), height: Number(height || 760) },
    deviceScaleFactor: 1,
  });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await page.screenshot({ path: outPath, fullPage: false });
  await browser.close();
  console.log('saved', outPath);
})();
