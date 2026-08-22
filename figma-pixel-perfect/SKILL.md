---
name: figma-pixel-perfect
description: Match an application page 1:1 to a Figma design, starting from only a Figma URL and a page or screen name. Analyzes the design, diffs it against what the app actually renders, fixes the code, and verifies visually with screenshots. Use whenever the user asks to make a page pixel-perfect, to match, align, fix, or QA a screen against Figma, says the implementation "doesn't match the design", or wants a finished page compared with its Figma frame — even when the words "pixel perfect" never appear. Requires access to the Figma design and a runnable local application.
---

# Figma Pixel Perfect

Take a Figma URL and a page or screen name, then make the matching application page visually identical to the design. The deliverable is a completed code change verified by screenshot comparison — not a specification document, and not a list of differences.

## Input

Terse requests are fine:

```text
/figma-pixel-perfect <figma-url> "<page-or-screen-name>"
```

Treat the URL and page name as sufficient input. Resolve everything else — file key, exact frame, viewport, tokens, assets — from the Figma file and the repository. Ask the user only when two or more genuinely different frames plausibly match the requested name; implementing the wrong frame wastes the whole loop.

## Workflow

### 1. Resolve the frame

Parse the Figma URL. A `node-id` in the URL identifies the frame directly. Without one, list the file's pages and frames via metadata and resolve the name yourself — fuzzy matches (case, whitespace, `Home / Desktop`) are yours to make. Only real ambiguity justifies a question to the user.

### 2. Gather design intelligence

Capture, at minimum:

- A **reference screenshot** of the frame. This image drives the entire validation loop — treat it like an acceptance-test fixture.
- The frame's **dimensions**. They define the viewport to validate at.
- The **visual specs**: layout structure, spacing, typography (family, size, weight, line-height), colors, radii, borders, shadows, icons, copy, and interactive states.

Use whichever source is available, in this order:

1. The `figma-designer` skill, if installed. Use its findings directly; do not write PRD or design-spec files unless requested.
2. Figma MCP tools directly: `get_metadata` for structure, `get_screenshot` for the reference image, `get_design_context` for specs and code hints, `get_variable_defs` for design tokens. If a `figma-design-to-code` skill or MCP resource is available, load it before calling `get_design_context` — it materially improves the output.

### 3. Read the code

Inspect the target repository before changing anything: project instructions, the route and page component for the target screen, shared components, tokens/theme files, fonts, icon and asset conventions, and how the app is built and run. You are looking for what the page should already be reusing — the fix is usually "use the existing token or component correctly", not new code.

### 4. Diff implementation against design

Run the application with its existing scripts and capture the rendered page at the Figma frame's viewport. Compare that screenshot with the reference from step 2, and write down the concrete mismatches before touching code: layout structure, element sizing, spacing, typography, colors, borders, radii, shadows, icons, copy, and states.

The written list matters. It keeps the fixing pass deliberate instead of opportunistic, and it becomes the checklist you validate against in step 6.

### 5. Fix

- Fix the listed mismatches in the fewest files possible.
- Reuse existing components, tokens, fonts, icons, and assets. Introducing parallel values — a new hex for a color that already exists as a token — is how design drift starts.
- Preserve existing behavior, accessibility attributes, and responsive rules.
- Do not redesign, add speculative abstractions, or modify unrelated screens, even where the code invites it.

### 6. Validate visually and iterate

Re-capture the page and compare again. Layout fixes shift neighboring elements, so a single pass is rarely enough. Iterate capture → compare → fix until layout, sizing, spacing, typography, colors, borders, shadows, icons, content, and states match at the designed viewport. Trust the screenshot over the code: reading the diff and concluding it "should look right" is exactly how mismatches survive.

To capture the page, use the best available option: a browser automation tool, a screenshot script in the repo's own tooling, or `npx playwright screenshot --viewport-size=<w>,<h> <url> out.png`. Always render at the frame's viewport so the comparison is apples-to-apples.

### 7. Report

Report:

- The changed files and what changed in each.
- The checks you ran — the smallest relevant existing set (build, tests, lint).
- Any mismatch you could not resolve and why. This is usually missing design data, such as a state the Figma file does not show.

## Completion criteria

- The named frame matches at its designed viewport with no obvious visual differences — verified by screenshot comparison, not by code inspection.
- Responsive variants match when the Figma file provides them.
- Existing functionality still works.
- No generated PRD, placeholder asset, or unrelated refactor left behind.
