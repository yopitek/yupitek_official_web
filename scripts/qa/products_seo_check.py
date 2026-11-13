#!/usr/bin/env python3
"""Check built product pages for SEO/AEO basics. Usage: products_seo_check.py <build_dir> [--lang en]
Exit 1 if any page fails. Pages = <build_dir>/<lang>/products/{acr,flipperzero,hak5,sdrlab}/<product>/index.html"""
import html, json, re, sys
from pathlib import Path

BRANDS = ("acr", "flipperzero", "hak5", "sdrlab")
NEED_TYPES = {"Product", "FAQPage", "BreadcrumbList"}
HUB_TYPES = {"CollectionPage", "ItemList", "BreadcrumbList"}


def check_page(doc: str, need=NEED_TYPES, lang: str = "en") -> list:
    errs = []
    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    title = html.unescape(m.group(1)).strip() if m else ""
    if not title or len(title) > 60:
        errs.append(f"title len {len(title)} (>60)")
    if "ALFA Network" in title:
        errs.append("title mentions ALFA Network")
    d = re.search(r'<meta name="?description"? content="?([^">]*)', doc)
    dl = len(html.unescape(d.group(1))) if d else 0
    lo, hi = (50, 90) if lang.startswith("zh") else (120, 160)
    if not lo <= dl <= hi:
        errs.append(f"description len {dl} (need {lo}-{hi})")
    types = set()
    for blk in re.findall(r'<script type="?application/ld\+json"?>(.*?)</script>', doc, re.S):
        try:
            data = json.loads(blk)
        except ValueError:
            errs.append("invalid JSON-LD")
            continue
        for it in data if isinstance(data, list) else [data]:
            types.add(it.get("@type"))
            if it.get("@type") == "FAQPage" and len(it.get("mainEntity", [])) < 3:
                errs.append("FAQPage has <3 questions")
            if it.get("@type") == "BreadcrumbList":
                urls = [i.get("item", "") for i in it.get("itemListElement", [])]
                if any(not b.startswith(a) or a == b for a, b in zip(urls, urls[1:])):
                    errs.append("BreadcrumbList order wrong (parents must come first)")
    for t in sorted(need - types):
        errs.append(f"missing {t} schema")
    return errs


def main(argv):
    root, lang = Path(argv[1]), (argv[argv.index("--lang") + 1] if "--lang" in argv else "en")
    pages = sorted(p for b in BRANDS for p in (root / lang / "products" / b).glob("*/index.html"))
    hubs = [root / lang / "products" / b / "index.html" for b in BRANDS]
    pages = hubs + pages
    bad = 0
    for p in pages:
        errs = check_page(p.read_text(errors="ignore"), HUB_TYPES if p in hubs else NEED_TYPES, lang)
        bad += bool(errs)
        print(("FAIL " if errs else "ok   ") + str(p.relative_to(root)) + ("  " + "; ".join(errs) if errs else ""))
    print(f"{len(pages)} pages, {bad} failing")
    return 1 if bad or not pages else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
