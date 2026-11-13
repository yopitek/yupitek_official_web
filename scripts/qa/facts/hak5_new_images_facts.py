#!/usr/bin/env python3
"""Shark Jack Display / LAN Turtle Hub must carry an (existing) official image on the page and the hub card, in all 10 locales."""
import re, sys
from pathlib import Path

LOCALES = "en zh-tw zh-cn ja ar es pt ru de fr".split()
PRODUCTS = ("shark-jack-display", "lan-turtle-hub")
fails = total = 0


def check(ok, msg):
    global fails, total
    total += 1
    if not ok:
        fails += 1
        print("FAIL", msg)


for p in PRODUCTS:
    img = f"/images/products/hak5/{p}.jpg"
    check(Path("static" + img).is_file() and Path("static" + img).stat().st_size < 400_000, f"image file exists and <400KB: {img}")
    for l in LOCALES:
        page = Path(f"content/{l}/products/hak5/{p}/index.md")
        text = page.read_text() if page.exists() else ""
        check(f'featureimage: "{img}"' in text, f"{l}/{p}: featureimage")
        check(f"]({img})" in text, f"{l}/{p}: inline image")
        hub = Path(f"content/{l}/products/hak5/_index.md").read_text()
        m = re.search(r'\{\{< card [^>]*href="/%s/products/hak5/%s/"[^>]*>\}\}' % (l, p), hub)
        check(bool(m) and f'image="{img}"' in m.group(0), f"{l}/hub card image for {p}")
print(f"{total - fails}/{total} passed, {fails} failed")
sys.exit(1 if fails else 0)
