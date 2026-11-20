#!/usr/bin/env python3
"""Check that the web fonts really load (not just appear in a font-family list).
For each locale the page must request Google Fonts and end with the expected faces in
document.fonts with status "loaded". A CSS @import that is not at the top of the bundle is
ignored by browsers, which is how the fonts silently never loaded before.
Usage: uv run --with playwright python scripts/qa/webfont_check.py http://127.0.0.1:8790"""
import sys

from playwright.sync_api import sync_playwright

EXPECT = {
    "zh-tw": ["Inter", "Noto Sans TC"],
    "zh-cn": ["Inter", "Noto Sans SC"],
    "ja": ["Inter", "Noto Sans JP"],
    "ko": ["Inter", "Noto Sans KR"],
    "ar": ["Inter", "Noto Sans Arabic"],
    "en": ["Inter"],
    "de": ["Inter"],
}
PAGE = "blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/"


def main() -> int:
    base = sys.argv[1].rstrip("/")
    fails = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for loc, families in EXPECT.items():
            page = browser.new_page()
            requested = []
            page.on("request", lambda r: requested.append(r.url) if "fonts.g" in r.url else None)
            page.goto(f"{base}/{loc}/{PAGE}", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            loaded = set(page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/[\"']/g, ''))"))
            missing = [f for f in families if f not in loaded]
            # CJK fonts have no italic face; the browser slants the glyphs instead, which reads as garbled
            slanted = loc in ("zh-tw", "zh-cn", "ja", "ko") and page.evaluate(
                "(() => { const b = document.querySelector('.prose blockquote'); return !!b && getComputedStyle(b).fontStyle !== 'normal'; })()")
            if slanted:
                missing.append("blockquote is italic")
            ok = requested and not missing
            fails += not ok
            print(f"{'OK  ' if ok else 'FAIL'} {loc}: google-fonts requests={len(requested)} missing={missing}")
            page.close()
    print(f"{len(EXPECT)} locales, {fails} failing")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
