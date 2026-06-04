#!/usr/bin/env python3
"""
Post-fix Playwright Verification Script
Confirms all product cards are visible on live yupitek.com after fixes applied.
Run: python3 scripts/verify_after_fix.py
"""

import asyncio
from playwright.async_api import async_playwright

import os

BASE_URL = os.environ.get("BASE_URL", "http://localhost:1313")

LANGS = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]

# Expected card counts (from content/_index.md shortcode count)
EXPECTED_CARDS = {
    "acr": 3,
    "alfa": 13,
    "flipperzero": 4,
    "graphiccard": 14,
    "hak5": 17,
    "mellanox": 7,
    "sdrlab": 7,
    "ubiquiti": 10,
}


async def count_product_links(page, url, category):
    """Count unique sub-product links on a category page."""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        links = await page.query_selector_all(f"a[href*='/products/{category}/']")
        hrefs = set()
        for link in links:
            href = await link.get_attribute("href")
            if href:
                # Only count sub-product links (not the category page itself)
                parts = href.rstrip("/").split("/")
                if len(parts) >= 5 and parts[-2] == category:
                    hrefs.add(href)
        return len(hrefs)
    except Exception as e:
        return -1


async def check_broken_images(page, url):
    """Return list of broken image srcs on the page."""
    broken = []
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        imgs = await page.query_selector_all("img")
        for img in imgs:
            src = await img.get_attribute("src") or ""
            if "/images/products/" in src:
                w = await page.evaluate("(el) => el.naturalWidth", img)
                if w == 0:
                    broken.append(src)
    except Exception as e:
        broken.append(f"ERROR: {e}")
    return broken


async def run_verification():
    all_issues = []
    print("=" * 65)
    print("Yupitek.com Post-Fix Verification")
    print("=" * 65)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # ── Product count check ──────────────────────────────────────
        print("\n📦 Product Count Check (all languages × all categories)")
        print("-" * 65)

        for lang in LANGS:
            lang_ok = True
            for cat, expected in EXPECTED_CARDS.items():
                url = f"{BASE_URL}/{lang}/products/{cat}/"
                count = await count_product_links(page, url, cat)
                if count >= expected:
                    status = f"✓ ({count})"
                else:
                    status = f"❌ {count}/{expected}"
                    lang_ok = False
                    all_issues.append({
                        "type": "count_mismatch",
                        "lang": lang,
                        "cat": cat,
                        "actual": count,
                        "expected": expected,
                        "url": url,
                    })
                print(f"  [{lang:5s}] {cat:15s}: {status}")

        # ── Image check (EN only, images are shared) ─────────────────
        print("\n🖼️  Broken Image Check (EN pages)")
        print("-" * 65)

        for cat in EXPECTED_CARDS:
            url = f"{BASE_URL}/en/products/{cat}/"
            broken = await check_broken_images(page, url)
            if broken:
                for src in broken:
                    print(f"  ❌ [{cat}] BROKEN: {src}")
                    all_issues.append({
                        "type": "broken_image",
                        "cat": cat,
                        "src": src,
                    })
            else:
                print(f"  ✓  [{cat}] All images OK")

        await browser.close()

    # ── Summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    if not all_issues:
        print("✅ ALL CHECKS PASSED — Website is fully synchronized!")
    else:
        print(f"⚠️  {len(all_issues)} ISSUE(S) FOUND:")
        for i, issue in enumerate(all_issues, 1):
            if issue["type"] == "count_mismatch":
                print(f"  {i}. [{issue['lang']}] {issue['cat']}: "
                      f"{issue['actual']}/{issue['expected']} products")
                print(f"     URL: {issue['url']}")
            elif issue["type"] == "broken_image":
                print(f"  {i}. BROKEN IMAGE in [{issue['cat']}]: {issue['src']}")
    print("=" * 65)

    return all_issues


if __name__ == "__main__":
    issues = asyncio.run(run_verification())
    exit(0 if not issues else 1)
