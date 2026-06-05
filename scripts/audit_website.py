#!/usr/bin/env python3
"""
Yupitek Website Audit Script
Checks product counts and image status across all language versions
"""

import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "https://yupitek.com"

# Languages and their URL prefixes
LANGUAGES = {
    "zh-tw": "zh-tw",
    "zh-cn": "zh-cn",
    "en": "en",
    "ja": "ja",
    "ar": "ar",
    "es": "es",
    "pt": "pt",
    "ru": "ru",
    "de": "de",
    "fr": "fr",
}

# Product categories
PRODUCT_CATEGORIES = [
    "acr",
    "alfa",
    "flipperzero",
    "graphiccard",
    "hak5",
    "mellanox",
    "sdrlab",
    "ubiquiti",
]

# Expected counts from English version (ground truth from local files)
EXPECTED_EN_COUNTS = {
    "acr": 3,
    "alfa": 16,
    "flipperzero": 4,
    "graphiccard": 14,
    "hak5": 17,
    "mellanox": 7,
    "sdrlab": 7,
    "ubiquiti": 12,
}


async def count_products_on_page(page, url):
    """Count product cards on a product listing page."""
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        # Look for product card elements - common selectors
        # Try multiple selectors
        selectors = [
            "article.card",
            ".card-group .card",
            "[data-card]",
            "a[href*='/products/'][class*='card']",
            ".product-card",
        ]
        
        count = 0
        for selector in selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                count = len(elements)
                break
        
        # Fallback: count links that go to individual product pages
        if count == 0:
            category = url.split("/products/")[-1].rstrip("/")
            product_links = await page.query_selector_all(f"a[href*='/products/{category}/']")
            # Filter out the breadcrumb link itself
            count = max(0, len(product_links) - 1)

        title = await page.title()
        return {"url": url, "title": title, "count": count, "error": None}
    except Exception as e:
        return {"url": url, "title": None, "count": 0, "error": str(e)}


async def check_images_on_page(page, url):
    """Check all product images on a page and report broken ones."""
    broken_images = []
    all_images = []
    
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Find all images
        img_elements = await page.query_selector_all("img")
        
        for img in img_elements:
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt") or ""
            if src and ("/images/products/" in src or "/images/" in src):
                # Check naturalWidth to detect broken images
                natural_width = await page.evaluate("(img) => img.naturalWidth", img)
                natural_height = await page.evaluate("(img) => img.naturalHeight", img)
                
                img_info = {
                    "src": src,
                    "alt": alt,
                    "broken": natural_width == 0 and natural_height == 0,
                }
                all_images.append(img_info)
                if natural_width == 0 and natural_height == 0:
                    broken_images.append(img_info)
        
        return {"url": url, "total_images": len(all_images), "broken_images": broken_images, "error": None}
    except Exception as e:
        return {"url": url, "total_images": 0, "broken_images": [], "error": str(e)}


async def run_audit():
    results = {
        "task_1_1": {},  # EN product counts
        "task_1_2": {},  # All language product counts
        "task_1_3": {},  # Image checks
        "issues": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        # =========================================================
        # TASK 1.1 — English product page counts
        # =========================================================
        print("\n" + "="*60)
        print("TASK 1.1 — English Product Page Product Counts")
        print("="*60)
        
        en_counts = {}
        for category in PRODUCT_CATEGORIES:
            url = f"{BASE_URL}/en/products/{category}/"
            result = await count_products_on_page(page, url)
            en_counts[category] = result
            status = f"{result['count']} products"
            if result['error']:
                status = f"ERROR: {result['error']}"
            print(f"  {category:20s}: {status}")
        
        results["task_1_1"] = en_counts

        # =========================================================
        # TASK 1.2 — All languages product page counts
        # =========================================================
        print("\n" + "="*60)
        print("TASK 1.2 — All Languages Product Counts")
        print("="*60)
        
        lang_results = {}
        for lang_code, lang_prefix in LANGUAGES.items():
            if lang_code == "en":
                continue  # Already done above
            
            print(f"\n  Language: {lang_code}")
            lang_results[lang_code] = {}
            
            for category in PRODUCT_CATEGORIES:
                url = f"{BASE_URL}/{lang_prefix}/products/{category}/"
                result = await count_products_on_page(page, url)
                lang_results[lang_code][category] = result
                
                en_count = en_counts.get(category, {}).get("count", 0)
                lang_count = result["count"]
                match = "✓" if lang_count == en_count else "⚠️ MISMATCH"
                
                status = f"{lang_count} products (EN: {en_count}) {match}"
                if result["error"]:
                    status = f"ERROR: {result['error']}"
                print(f"    {category:20s}: {status}")
                
                if lang_count != en_count and not result["error"]:
                    results["issues"].append({
                        "type": "count_mismatch",
                        "lang": lang_code,
                        "category": category,
                        "lang_count": lang_count,
                        "en_count": en_count,
                        "url": url,
                    })
        
        results["task_1_2"] = lang_results

        # =========================================================
        # TASK 1.3 — Image checks (EN pages)
        # =========================================================
        print("\n" + "="*60)
        print("TASK 1.3 — Image Checks (English Product Pages)")
        print("="*60)
        
        image_results = {}
        for category in PRODUCT_CATEGORIES:
            url = f"{BASE_URL}/en/products/{category}/"
            result = await check_images_on_page(page, url)
            image_results[category] = result
            
            if result["error"]:
                print(f"  {category:20s}: ERROR - {result['error']}")
            elif result["broken_images"]:
                print(f"  {category:20s}: ⚠️ {len(result['broken_images'])} broken / {result['total_images']} total")
                for broken in result["broken_images"]:
                    print(f"      BROKEN: {broken['src']} (alt: {broken['alt']})")
                    results["issues"].append({
                        "type": "broken_image",
                        "category": category,
                        "lang": "en",
                        "src": broken["src"],
                        "alt": broken["alt"],
                    })
            else:
                print(f"  {category:20s}: ✓ All {result['total_images']} images OK")
        
        results["task_1_3"] = image_results

        await browser.close()

    return results


def main():
    results = asyncio.run(run_audit())
    
    print("\n" + "="*60)
    print("SUMMARY OF ISSUES FOUND")
    print("="*60)
    
    if not results["issues"]:
        print("✅ No issues found!")
    else:
        for i, issue in enumerate(results["issues"], 1):
            if issue["type"] == "count_mismatch":
                print(f"\n  Issue #{i}: Product count mismatch")
                print(f"    Language: {issue['lang']}")
                print(f"    Category: {issue['category']}")
                print(f"    EN count: {issue['en_count']}, {issue['lang']} count: {issue['lang_count']}")
                print(f"    URL: {issue['url']}")
            elif issue["type"] == "broken_image":
                print(f"\n  Issue #{i}: Broken image")
                print(f"    Category: {issue['category']}")
                print(f"    Language: {issue['lang']}")
                print(f"    Image src: {issue['src']}")
    
    # Save results to JSON
    output_path = "/home/yopitek/Project/yupitek_official_web/scripts/audit_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nDetailed results saved to: {output_path}")
    
    return results


if __name__ == "__main__":
    main()
