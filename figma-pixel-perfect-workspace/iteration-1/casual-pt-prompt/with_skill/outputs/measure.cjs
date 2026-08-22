const { chromium } = require('~/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 760 } });
  await page.goto('file://~/dev/skills/figma-pixel-perfect-workspace/iteration-1/casual-pt-prompt/with_skill/repo/index.html');
  try { await page.evaluate(() => document.fonts.ready); } catch(e) {}
  await page.waitForTimeout(800);
  const data = await page.evaluate(() => {
    const r = (sel) => { const el = document.querySelector(sel); if (!el) return null; const b = el.getBoundingClientRect(); return { x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; };
    const cards = [...document.querySelectorAll('.card')].map(c => { const b = c.getBoundingClientRect(); return { x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; });
    const btns = [...document.querySelectorAll('.card button')].map(c => { const b = c.getBoundingClientRect(); return { x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1) }; });
    const priceRange = document.createRange(); priceRange.selectNodeContents(document.querySelector('.card .price'));
    const pb = priceRange.getBoundingClientRect();
    const ul = [...document.querySelectorAll('.card ul')][0].getBoundingClientRect();
    const h1b = [...document.querySelectorAll('.card h2')][0].getBoundingClientRect();
    const navLinks = [...document.querySelectorAll('nav a')].map(a => { const b = a.getBoundingClientRect(); return { x: +b.x.toFixed(1), w: +b.width.toFixed(1) }; });
    return {
      docH: document.documentElement.scrollHeight,
      header: r('.site-header'), logo: r('.logo'),
      h1: r('.hero h1'), sub: r('.hero p'), footer: r('.site-footer'),
      cards, btns,
      firstTitle: { y: h1b.y, h: h1b.height },
      firstPriceText: { x: +pb.x.toFixed(1), y: +pb.y.toFixed(1), h: +pb.height.toFixed(1) },
      firstUl: { y: +ul.y.toFixed(1), h: +ul.height.toFixed(1) },
      navLinks,
      fontLoaded: document.fonts.check('16px Inter')
    };
  });
  console.log(JSON.stringify(data, null, 1));
  await page.screenshot({ path: 'final.png' });
  await browser.close();
})();
