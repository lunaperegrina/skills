# Pricing page — Figma sync report

Design source: Figma file `Q0Kt1wKVS1PW8aNs8vuCMb`, frame "Pricing" (node `1:2`), 1440x760.
Repo: `~/dev/skills/figma-pixel-perfect-workspace/iteration-1/casual-pt-prompt/without_skill/repo` (static HTML/CSS, no build step).

## Changed files

### `repo/index.html`
- Button labels changed from "Buy now" to "Get started" on all three cards (design text).
- Added Google Fonts `Inter` (400/600/700) with preconnect — the design uses Inter; previously the page relied on system fallbacks.

### `repo/styles.css`
Rewritten to match the measured design geometry (all values verified against the Figma render):

| Element | Before | After (design) |
|---|---|---|
| Hero title | 32px | 48px / 56px line-height, #111827 |
| Hero subtitle color | #999999 | #6b7280 |
| Hero rhythm | — | title box y136-192, subtitle 204-232, cards start y280 |
| Card | radius 4px, padding 20px, no border | radius 16px, padding 32px, 1px #e5e7eb ring via `box-shadow: inset` (keeps exact 384x312 box; a CSS `border` would shift content 1px and grow the card 2px) |
| Card title | 16px | 16px/24px semibold, box y312-336 |
| Price | 32px | 40px/48px semibold, box y352-400 |
| "/mo" | inline, baseline-ish | flex `align-items: flex-end`, 16px/24px #6b7280, 10px after price — bottom-of-box aligned per design, ink at x231 |
| Features | 14px/24px | unchanged metrics, box y416-488, #4b5563 |
| Button | pill radius, #6c5ce7, "Buy now" | radius 8px, #4f46e5, 320x40 at y520-560; label 14px semibold white |
| Button label alignment | centered | flush left at the button's left edge — this is literally how the Figma design renders (verified by pixel scan: label ink x156-227 inside button x152-471, on all three cards) |
| Header | padding 0 64px | padding 0 60px 0 64px — right padding 60px places nav ink right edge at x1378 as in the design (64px would sit 4px left) |
| Footer | height 96, center y~736 | margin-top 114px + padding-bottom 34px — text box y706-726, page ends exactly at 760px |

### `repo/tokens.css`
- Unchanged (existing tokens already matched: #4f46e5, #e5e7eb, radii 16/8, Inter).

## Validation performed

1. Pulled the design via Figma MCP (`get_metadata`, `get_design_context`, `get_screenshot`) at native 1440x760.
2. Measured glyph/button ink positions in the Figma render with PIL to resolve ambiguities (button label alignment, "/mo" vertical alignment, nav margins, footer position).
3. Rendered the page with Playwright (cached Chromium, viewport 1440x760, file:// URL) — `shot.js` in this folder.
4. Re-measured the same landmarks in the render and compared (design vs after):
   - Buttons: x152-1287, y520-559 — exact match.
   - Hero title ink: y144-190, x554-884 — exact match.
   - Card title ink y318-329; price ink y358-393; "/mo" ink y382-394, x231 — match within 1px.
   - Nav ink: Product/Pricing/Docs gaps 34/35px, right edge x1378 — exact match.
   - Footer ink y711-720 — exact match.
   - Header border at y71 — exact match.
5. Full-frame pixel diff vs design: ~1.5% of pixels differ by >8/255 — all text anti-aliasing (Figma rasterizer vs Chromium), no structural differences.
6. Visual diff review (design vs final.png): no visible layout, spacing, color, typography, or content differences.

## Outputs

- `final.png` — finished page at the design viewport (1440x760).
- `before.png` — original page, same viewport.
- `after.png` — render during validation (identical to final.png).
- `design_reference.png` — Figma "Pricing" frame export.
- `comparison.png` — before / design / final stacked.
- `shot.js` — Playwright capture script (viewport 1440x760; uses the cached Chromium build).

## Remaining mismatches

- Sub-glyph raster differences: "Product"/"$19" ink is 1-4px wider/narrower than Figma's Inter rendering at the same font size (different hinting). Right edges and baselines still align; not fixable without fake stretching (letter-spacing), which was intentionally avoided.
- The button label sits flush left (a deliberate design quirk, faithfully reproduced). If the team actually intended centered labels, that's a design-file fix, not a code one.
- Inter loads from Google Fonts, so an offline render falls back to system sans (metrics shift slightly). Self-hosting the font would remove the network dependency if needed.
