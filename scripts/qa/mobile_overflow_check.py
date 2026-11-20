#!/usr/bin/env python3
"""Fail if any checked page overflows horizontally at a 390 px mobile viewport,
or if a zh-CN page renders body/headings with a Traditional-Chinese font first.
Usage: mobile_overflow_check.py <base_url> [path ...]   (default paths: long-word headings in de/ru)
Needs Playwright with a Chromium build: uv run --with playwright python scripts/qa/mobile_overflow_check.py http://127.0.0.1:8790"""
import glob, pathlib, sys
from playwright.sync_api import sync_playwright

DEFAULT = ["/de/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/", "/ru/products/alfa/awus036ax/",
           "/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/", "/ar/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/"]


def main() -> int:
    base = sys.argv[1].rstrip("/"); paths = sys.argv[2:] or DEFAULT
    exe = (sorted(glob.glob(str(pathlib.Path.home() / ".cache/ms-playwright/chromium-*/chrome-linux*/chrome"))) or [None])[-1]
    fails = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe)
        pg = b.new_page(viewport={"width": 390, "height": 844})
        for path in paths:
            pg.goto(base + path, wait_until="networkidle")
            o = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            ok = o <= 2
            fails += not ok
            print(("OK  " if ok else "FAIL"), f"overflow={o}px", path)
        for path in ("/zh-cn/", "/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/"):
            pg.goto(base + path, wait_until="networkidle")
            fonts = pg.evaluate("() => [getComputedStyle(document.body).fontFamily, getComputedStyle(document.querySelector('h1')).fontFamily]")
            ok = all(f.split(",")[0].strip().strip("'\"").lower() == "noto sans sc" for f in fonts)
            fails += not ok
            print(("OK  " if ok else "FAIL"), "zh-CN first font body/h1 =", [f.split(",")[0] for f in fonts], path)
        # Article body: the first CJK font in the stack must match the page language (Han glyph forms differ)
        want = {"zh-cn": "noto sans sc", "ja": "noto sans jp", "ko": "noto sans kr", "zh-tw": "noto sans tc"}
        for loc, font in want.items():
            pg.goto(f"{base}/{loc}/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/", wait_until="networkidle")
            stack = [f.strip().strip("'\"").lower() for f in pg.evaluate(
                "() => getComputedStyle(document.querySelector('.prose p') || document.body).fontFamily").split(",")]
            first_cjk = next((f for f in stack if f.startswith("noto sans ") and f != "noto sans"), None)
            ok = first_cjk == font
            fails += not ok
            print(("OK  " if ok else "FAIL"), f"{loc} prose first CJK font = {first_cjk} (want {font})")
        b.close()
    print(f"{len(paths) + 2 + len(want)} checks, {fails} failing")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
