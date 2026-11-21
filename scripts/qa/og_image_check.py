#!/usr/bin/env python3
"""Every page must carry an og:image, so links shared to social or chat show a preview card.

Pages with their own featureimage use it; the rest fall back to the site-wide brand image.
Before the fallback existed, 15,366 of 16,595 built pages had no og:image at all — including
every locale's home page.
Usage (repo root): python3 scripts/qa/og_image_check.py <build_dir> [--sample N]
"""
import re
import sys
from collections import Counter
from pathlib import Path

# hugo --minify drops attribute quotes and can reorder them, so match the whole meta tag
OG = re.compile(r'<meta[^>]*og:image[^>]*>')
# Tag pages are generated per keyword and are not meaningful share targets
SKIP_SEGMENTS = ("/tags/",)
# Hugo emits bare meta-refresh stubs for /page/1/ and the root language redirect; they carry no head
REDIRECT = re.compile(r'<meta[^>]+http-equiv=["\']?refresh', re.I)


def kind(rel: str) -> str:
    parts = rel.split("/")
    if len(parts) <= 2:
        return "home"
    return parts[1] if parts[1] else "home"


def main() -> int:
    build = Path(sys.argv[1])
    missing, total = [], 0
    by_kind = Counter()
    for f in build.rglob("index.html"):
        rel = str(f.relative_to(build))
        if any(s in "/" + rel for s in SKIP_SEGMENTS):
            continue
        html = f.read_text(encoding="utf-8", errors="ignore")
        if REDIRECT.search(html):
            continue
        total += 1
        if not OG.search(html):
            missing.append(rel)
            by_kind[kind(rel)] += 1
    for rel in missing[:15]:
        print(f"NO og:image  /{rel.rsplit('/', 1)[0]}/")
    if by_kind:
        print("by section:", dict(by_kind.most_common()))
    print(f"{total} pages, {len(missing)} without og:image")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
