# Pricing page — Figma pixel-perfect report

Design: https://www.figma.com/design/Q0Kt1wKVS1PW8aNs8vuCMb — frame "Pricing" (node 1:2, 1440x760, page "Screens").
Repo: ~/dev/skills/figma-pixel-perfect-workspace/iteration-1/casual-pt-prompt/with_skill/repo (static HTML/CSS, no build step).

## Changed files

### index.html
- Button copy: "Buy now" -> "Get started" on all three cards (design label).
- Added Google Fonts link for Inter 400/600/700 — tokens.css declares Inter as --font-family but nothing loaded it, so every browser fell back to Helvetica.

### styles.css
- Hero title: 32px -> 48px/700, line-height 56px (design box y136-192).
- Hero subtitle: color #999999 -> var(--color-text-secondary), line-height 28px.
- Cards: border-radius 4px -> var(--radius-card) (16px); added 1px var(--color-border) border; padding 20px -> 31px (31px + 1px border = 32px visual padding, matching the Figma frame exactly, including the 320px button width and 312px card height).
- Price: 32px -> 40px, line-height 48px, margin 16px 0 24px -> 16px 0.
- "/mo" span: line-height 24px, margin-left 6px (design gap after the "$19" advance).
- Button: border-radius 999px -> var(--radius-button) (8px); background #6c5ce7 -> var(--color-primary) (#4f46e5); text-align: left — in the design the label starts at the button's left edge (verified in the reference PNG: label glyphs x152-230), not centered.
- Footer: restructured to land at y706-726 — body is now min-height: 100vh; display: flex; flex-direction: column, footer margin-top: auto with padding-bottom: 34px; removed the 96px bottom padding on .cards.
- Added missing line-heights: logo 24px, nav links 20px, card title 24px, footer 20px.

tokens.css unchanged — all fixes reuse existing tokens (--color-text-secondary, --color-border, --color-primary, --radius-card, --radius-button). Two hardcoded hex values that were drifting from tokens (#6c5ce7 button, #999999 subtitle) were replaced with tokens.

## Mismatches found (before fixing)

Hero title 32px vs 48px; subtitle wrong color; cards: radius 4 vs 16, no border, padding 20 vs 32; price 32 vs 40 with wrong margins; button: pill radius vs 8px, wrong color #6c5ce7, centered label vs left-aligned, wrong copy "Buy now"; footer position (page did not match the 760px frame); Inter never loaded.

## Validation performed

No build/test/lint tooling exists in the repo (static site). Validation was visual and geometric, at the design viewport 1440x760 via file:// URL in Playwright chromium:

1. DOM geometry vs Figma node coordinates — all exact: header 0,0 1440x72; h1 y136 h56; subtitle y204 h28; cards x=120/528/936 y=280 384x312; card titles y312 h24; features y416 h72; buttons y520 320x40 at x=152/560/968; footer text y706; document scroll height exactly 760 (no scroll).
2. Pixel diff vs the Figma reference screenshot (reference.png): differing pixels (>12/255) went from 10.22% (before.png) to 1.38% (final.png). See also comparison.png (side-by-side).
3. Structural rows/columns (header border y71, card top y280, card border x120, button fill, radius corners, page background) are pixel-identical; 100% of the residual difference lies inside text glyph bands (antialiasing).

## Remaining mismatches

All residual differences are font-rasterization artifacts of chromium vs Figma's canvas renderer (same Inter typeface), not CSS-positionable:

1. Nav link words sit 4-8px left of the Figma render. The nav group is right-anchored at the same 64px margin with the same 32px gaps, but chromium's Inter advances are ~1-3px wider per word, accumulating leftward. Fixing this would require per-word letter-spacing hacks tuned to one rasterizer.
2. The "/mo" suffix lands ~3-4px left of the design because the preceding "$19" advance is ~3px narrower in chromium; it flows inline after the price.
3. Glyph antialiasing differs slightly in weight (e.g., the "1" stem in "1 project" renders lighter in the Figma export). Geometry is identical.

No responsive variants exist in the Figma file (single 1440x760 frame), so none were validated beyond the page not regressing (cards still wrap as before; the footer now sticks to the viewport bottom on tall screens).
