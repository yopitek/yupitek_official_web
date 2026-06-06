#!/usr/bin/env python3
import os
import sys
from playwright.sync_api import sync_playwright

# Wording dictionary for validation
CTA_TEXTS = {
    "zh-tw": "需要詢問產品報價?請來信與我們聯絡",
    "zh-cn": "需要询问产品报价?请来信与我们联系",
    "en": "Need a product quotation? Please contact us",
    "ja": "製品のお見積もりをご希望ですか？お問い合わせください。",
    "ar": "هل تحتاج إلى طلب عرض سعر للمنتج؟ يرجى الاتصال بنا。",
    "de": "Benötigen Sie ein Produktangebot? Bitte kontaktieren Sie uns。",
    "es": "¿Necesita una cotización del producto? Por favor, contáctenos。",
    "fr": "Besoin d'un devis pour le produit ? Veuillez nous contacter。",
    "pt": "Precisa de uma cotação do produto? Por favor, entre em contato conosco。",
    "ru": "Нужно коммерческое предложение? Пожалуйста, свяжитесь с нами。"
}

# RES-3: Localized contact links mapping
CTA_LINKS = {
    "zh-tw": "/zh-tw/contact/",
    "zh-cn": "/zh-cn/contact/",
    "en": "/en/contact/",
    "ja": "/ja/contact/",
    "ar": "/ar/contact/",
    "de": "/de/contact/",
    "es": "/es/contact/",
    "fr": "/fr/contact/",
    "pt": "/pt/contact/",
    "ru": "/ru/contact/"
}

def get_language(url_path):
    parts = url_path.split("/")
    for part in parts:
        if part in CTA_TEXTS:
            return part
    return None

def main():
    base_url = "http://127.0.0.1:1313"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        
    print(f"Starting audit against base URL: {base_url}")
    
    # Gather all routes to scan
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(project_root, "content")
    
    routes = []
    
    for root, dirs, files in os.walk(content_dir):
        if "products" not in root:
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # Convert filepath to relative URL route
                rel_path = os.path.relpath(filepath, content_dir)
                # e.g., zh-tw/products/alfa/awus036ax/_index.md
                url_path = "/" + rel_path.replace("\\", "/").replace("/_index.md", "/").replace("/index.md", "/")
                # Normalize double slashes
                url_path = re.sub(r'/+', '/', url_path)
                
                # Exclude top-level /products/ and brand category listing pages (e.g. /zh-tw/products/alfa/)
                parts = url_path.strip("/").split("/")
                if len(parts) <= 3 and parts[1] == "products" and not url_path.endswith("/products/ibeacon/"):
                    continue
                    
                routes.append(url_path)
                
    routes = sorted(list(set(routes)))
    print(f"Identified {len(routes)} product routes to verify.")
    
    success_count = 0
    failure_count = 0
    failures = []
    verified_links = set()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Test connection first
        try:
            res = page.goto(base_url)
            if not res or res.status != 200:
                print(f"Error: Base URL {base_url} is not accessible. Make sure the Hugo server is running.")
                sys.exit(1)
        except Exception as e:
            print(f"Error connecting to server: {e}")
            sys.exit(1)
            
        for route in routes:
            url = base_url + route
            lang = get_language(route)
            
            if not lang:
                # Top level index or other
                continue
                
            try:
                res = page.goto(url, wait_until="load")
                if not res:
                    failures.append((route, "Navigation failed (no response)"))
                    failure_count += 1
                    print(f"FAIL: {route} -> Navigation failed")
                    continue
                if res.status != 200:
                    failures.append((route, f"HTTP status {res.status}"))
                    failure_count += 1
                    print(f"FAIL: {route} -> status {res.status}")
                    continue
                
                # 1. Verify CTA alert exists and matches language wording
                page_text = page.inner_text("body")
                
                # Check for catalog index page (e.g., /zh-tw/products/ibeacon/)
                is_catalog = route.endswith("/products/ibeacon/")
                
                if is_catalog:
                    # Verify Task 1 & 2: Topology and Comparison Table images exist and load correctly
                    # Check topology image
                    topo_img = page.locator('img[src*="ibeacon_topology.png"]').first
                    if topo_img.count() == 0:
                        failures.append((route, "Missing ibeacon_topology.png"))
                        failure_count += 1
                        print(f"FAIL: {route} -> Missing ibeacon_topology.png")
                        continue
                    
                    # Verify it loaded successfully (wait up to 5s)
                    try:
                        page.wait_for_function(
                            "img => img.complete && img.naturalWidth > 0",
                            arg=topo_img.element_handle(),
                            timeout=5000
                        )
                        loaded_topo = True
                    except Exception:
                        loaded_topo = False
                        
                    if not loaded_topo:
                        failures.append((route, "Broken ibeacon_topology.png"))
                        failure_count += 1
                        print(f"FAIL: {route} -> Broken ibeacon_topology.png")
                        continue
                        
                    # Check comparison table image
                    comp_img = page.locator('img[src*="ibeacon_comparison.png"]').first
                    if comp_img.count() == 0:
                        failures.append((route, "Missing ibeacon_comparison.png"))
                        failure_count += 1
                        print(f"FAIL: {route} -> Missing ibeacon_comparison.png")
                        continue
                    
                    try:
                        page.wait_for_function(
                            "img => img.complete && img.naturalWidth > 0",
                            arg=comp_img.element_handle(),
                            timeout=5000
                        )
                        loaded_comp = True
                    except Exception:
                        loaded_comp = False
                        
                    if not loaded_comp:
                        failures.append((route, "Broken ibeacon_comparison.png"))
                        failure_count += 1
                        print(f"FAIL: {route} -> Broken ibeacon_comparison.png")
                        continue
                        
                    print(f"PASS: {route} (Topology and Comparison images verified)")
                    success_count += 1
                    continue
                
                # Verify CTA alert box text on detail pages
                expected_cta = CTA_TEXTS[lang]
                expected_link = CTA_LINKS[lang]
                
                # Match punctuation-flexible plain text content
                normalized_page_text = re.sub(r'[\s\?\?！!？,.。，：:\'’‘"““”]', '', page_text)
                normalized_expected = re.sub(r'[\s\?\?！!？,.。，：:\'’‘"““”]', '', expected_cta)
                
                if normalized_expected not in normalized_page_text:
                    failures.append((route, f"CTA text mismatch. Expected: '{expected_cta}'"))
                    failure_count += 1
                    print(f"FAIL: {route} -> CTA text mismatch.")
                    continue
                
                # 2. Verify CTA link is correct and resolves
                # Look for a link inside the alert box that points to contact
                link_locator = page.locator('div.flex.px-4.py-3 a, .alert a, a[href*="/contact/"]').first
                if link_locator.count() == 0:
                    failures.append((route, "No contact link found in alert box"))
                    failure_count += 1
                    print(f"FAIL: {route} -> No contact link found.")
                    continue
                    
                actual_href = link_locator.get_attribute("href")
                # Normalize host or relative URL prefix
                parsed_href = actual_href.replace(base_url, "")
                if parsed_href != expected_link and not parsed_href.endswith(expected_link):
                    failures.append((route, f"Link mismatch. Expected: '{expected_link}', got: '{parsed_href}'"))
                    failure_count += 1
                    print(f"FAIL: {route} -> Link mismatch: {parsed_href}")
                    continue
                    
                # Test target contact link resolves to 200 (only if not already verified for this locale)
                contact_url = base_url + parsed_href
                if contact_url not in verified_links:
                    chk_page = context.new_page()
                    try:
                        contact_res = chk_page.goto(contact_url, wait_until="load", timeout=10000)
                        if not contact_res or contact_res.status != 200:
                            status_code = contact_res.status if contact_res else 0
                            failures.append((route, f"Contact link returns {status_code}"))
                            failure_count += 1
                            print(f"FAIL: {route} -> Contact link {contact_url} returned {status_code}")
                            continue
                        verified_links.add(contact_url)
                    except Exception as le:
                        failures.append((route, f"Contact link navigation failed: {le}"))
                        failure_count += 1
                        print(f"FAIL: {route} -> Contact link {contact_url} failed: {le}")
                        continue
                    finally:
                        chk_page.close()
                
                # Check for zero console errors during this visit
                success_count += 1
                
            except Exception as e:
                failures.append((route, f"Exception: {e}"))
                failure_count += 1
                print(f"FAIL: {route} -> Exception: {e}")
                
        browser.close()
        
    print("\n" + "="*40)
    print(f"Audit Complete: {success_count} passed, {failure_count} failed.")
    print("="*40)
    
    if failure_count > 0:
        print("\nFailures:")
        for r, err in failures:
            print(f"- {r}: {err}")
        sys.exit(1)
    else:
        print("\nAll tasks verified successfully! 🎉")
        sys.exit(0)

import re
if __name__ == "__main__":
    main()
