#!/usr/bin/env python3
"""Check blog top banners. The article hero box is ~975x280 (ratio ~3.5), so the image shown there
must have that shape or the product gets cropped. For each article (all locales) the hero image is
`bannerimage` if set, else `featureimage`; it must exist, be at least 975 px wide and have a ratio of 3.3-3.7.
Usage (repo root): python3 scripts/qa/banner_ratio_check.py [slug ...]   (no slug = every article)"""
import re
import sys
from pathlib import Path

from PIL import Image


def hero(md: Path):
    fm = md.read_text(encoding="utf-8").split("---", 2)[1]
    if re.search(r"^hideFeatureImage:\s*true", fm, re.M):
        return None
    for key in ("bannerimage", "featureimage"):
        # Values appear double-quoted, single-quoted or bare; strip whichever quote is used
        m = re.search(rf"^{key}:\s*(\"[^\"\n]*\"|'[^'\n]*'|[^\n]*?)\s*$", fm, re.M)
        if m:
            value = m.group(1).strip().strip("\"'").strip()
            if value:
                return value
    return None


def articles(slugs):
    for md in sorted(Path("content").glob("*/blog/*/_index.md")):
        if not slugs or md.parent.name in slugs:
            yield md


def main() -> int:
    slugs = set(sys.argv[1:])
    bad = n = 0
    for md in articles(slugs):
        src = hero(md)
        if not src:
            continue
        n += 1
        f = Path("static" + src)
        if not f.is_file():
            bad += 1
            print(f"MISSING {md}: {src}")
            continue
        w, h = Image.open(f).size
        if w < 975 or not 3.3 <= w / h <= 3.7:
            bad += 1
            print(f"RATIO {md}: {src} {w}x{h} ({w / h:.2f})")
    print(f"{n} article heroes, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
