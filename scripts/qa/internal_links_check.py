#!/usr/bin/env python3
"""Check brand hubs and product pages link to related articles and sibling products, and that the links resolve.
Usage: internal_links_check.py <build_dir> [--lang en ...]  (default: en zh-tw). Exit 1 on any failure."""
import re, sys
from pathlib import Path

BRANDS = ("acr", "flipperzero", "hak5", "sdrlab")
HREF = re.compile(r'<a[^>]+href="([^"#?]+)"')


def links(html, lang, kind):
    hs = {re.sub(r"^https://yupitek\.com", "", h) for h in HREF.findall(html)}
    return {h for h in hs if re.match(rf"^/{lang}/{kind}/[^/]+/(?:[^/]+/)?$", h)
            and not re.search(r"/(tags|categories|page)/", h)}


def main() -> int:
    d = Path(sys.argv[1])
    langs = sys.argv[sys.argv.index("--lang") + 1:] if "--lang" in sys.argv else ["en", "zh-tw"]
    fails = pages = 0
    for lang in langs:
        for b in BRANDS:
            hub = d / lang / "products" / b
            for p in [hub / "index.html"] + sorted(hub.glob("*/index.html")):
                pages += 1
                html = p.read_text(errors="ignore")
                is_hub = p.parent == hub
                me = f"/{lang}/products/{b}/" + ("" if is_hub else p.parent.name + "/")
                arts = links(html, lang, "blog")
                sibs = {h for h in links(html, lang, "products") if f"/products/{b}/" in h and h.count("/") >= 5 and not h.endswith(me)}
                problems = []
                if not arts: problems.append("no related article link")
                if not is_hub and not sibs: problems.append("no related product link")
                for h in arts | sibs:
                    t = d / h.lstrip("/") / "index.html"
                    if not t.exists(): problems.append(f"broken {h}")
                if problems:
                    fails += 1; print(f"FAIL {p.relative_to(d)}: {'; '.join(problems)}")
    print(f"{pages} pages, {fails} failing")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
