#!/usr/bin/env python3
"""Programmatic checker for figma-pixel-perfect eval runs.

Usage: python3 check_run.py <repo_dir> <outputs_dir>
Prints a JSON array of {text, passed, evidence} — one entry per assertion.
"""
import json
import re
import sys
from pathlib import Path


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def css_block(css: str, selector: str) -> str:
    """Return the declaration block for a selector (first match, braces included)."""
    pattern = re.compile(re.escape(selector) + r"\s*\{([^}]*)\}")
    m = pattern.search(css)
    return m.group(1) if m else ""


def main() -> None:
    repo = Path(sys.argv[1]).resolve()
    outputs = Path(sys.argv[2]).resolve()

    css = read(repo / "styles.css")
    html = read(repo / "index.html")
    tokens = read(repo / "tokens.css")

    hero_h1 = css_block(css, ".hero h1")
    hero_p = css_block(css, ".hero p")
    card = css_block(css, ".card")
    price = css_block(css, ".price")
    button = css_block(css, ".card button")

    pngs = sorted(outputs.glob("**/*.png")) if outputs.exists() else []
    repo_files = sorted(p.name for p in repo.iterdir() if p.is_file())
    expected_repo_files = {"index.html", "styles.css", "tokens.css"}
    extra_files = [f for f in repo_files if f not in expected_repo_files]
    report = read(outputs / "report.md")

    def dec(block: str, prop: str) -> str:
        m = re.search(prop + r"\s*:\s*([^;]+);", block)
        return m.group(1).strip() if m else ""

    checks = []

    def add(text, passed, evidence):
        checks.append({"text": text, "passed": bool(passed), "evidence": evidence})

    add(
        "Hero title font-size is 48px (was 32px)",
        dec(hero_h1, "font-size") == "48px",
        f".hero h1 font-size: {dec(hero_h1, 'font-size') or 'not found'}",
    )
    subtitle_color = dec(hero_p, "color")
    add(
        "Hero subtitle color uses the secondary text token (#6b7280), not hardcoded #999999",
        subtitle_color in ("var(--color-text-secondary)", "#6b7280"),
        f".hero p color: {subtitle_color or 'not found'}",
    )
    card_border = dec(card, "border")
    card_shadow = dec(card, "box-shadow")
    border_ok = bool(card_border) and ("var(--color-border)" in card_border or "#e5e7eb" in card_border) and "1px" in card_border
    inset_ring_ok = "inset" in card_shadow and ("var(--color-border)" in card_shadow or "#e5e7eb" in card_shadow)
    add(
        "Cards have a 1px border using the border token/color #e5e7eb (was missing)",
        border_ok or inset_ring_ok,
        f".card border: {card_border or 'not found'}; box-shadow: {card_shadow or 'not found'}",
    )
    card_radius = dec(card, "border-radius")
    add(
        "Card border-radius is 16px / --radius-card (was 4px)",
        card_radius in ("16px", "var(--radius-card)"),
        f".card border-radius: {card_radius or 'not found'}",
    )
    card_padding = dec(card, "padding")
    border_width = 1 if "1px" in card_border else 0
    effective_padding = None
    if card_padding.endswith("px"):
        try:
            effective_padding = float(card_padding[:-2]) + border_width
        except ValueError:
            pass
    add(
        "Card padding yields 32px of effective inner space (was 20px)",
        effective_padding in (31.0, 32.0),
        f".card padding: {card_padding or 'not found'} + {border_width}px border = {effective_padding}",
    )
    add(
        "Price font-size is 40px (was 32px)",
        dec(price, "font-size") == "40px",
        f".price font-size: {dec(price, 'font-size') or 'not found'}",
    )
    btn_radius = dec(button, "border-radius")
    add(
        "Button border-radius is 8px / --radius-button (was 999px pill)",
        btn_radius in ("8px", "var(--radius-button)"),
        f".card button border-radius: {btn_radius or 'not found'}",
    )
    btn_bg = dec(button, "background")
    add(
        "Button background uses the primary token #4f46e5 (was hardcoded #6c5ce7)",
        ("var(--color-primary)" in btn_bg or "#4f46e5" in btn_bg) and "#6c5ce7" not in css,
        f".card button background: {btn_bg or 'not found'}",
    )
    add(
        "Button copy is 'Get started' (was 'Buy now') on all three cards",
        html.count(">Get started<") == 3 and ">Buy now<" not in html,
        f"'>Get started<' occurrences: {html.count('>Get started<')}, '>Buy now<' present: {'>Buy now<' in html}",
    )
    add(
        "A rendered screenshot of the page exists in outputs",
        len(pngs) > 0,
        f"png files in outputs: {[p.name for p in pngs][:5]}",
    )
    add(
        "No extraneous files added to the repo (no PRD/spec/asset files)",
        not extra_files,
        f"extra files: {extra_files}",
    )
    add(
        "report.md exists in outputs and lists the changed files",
        bool(report) and ("styles.css" in report or "index.html" in report),
        f"report.md length: {len(report)} chars, mentions styles.css/index.html: {('styles.css' in report) or ('index.html' in report)}",
    )

    print(json.dumps(checks, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
