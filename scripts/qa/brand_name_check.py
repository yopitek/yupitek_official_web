#!/usr/bin/env python3
"""Fail if the legacy brand spelling "Yupitek" appears in visible site text. Official name: Yopitek Ltd.
Allowed: lowercase domain/email (yupitek.com), and the Yupitek_AP SSID in Soft-AP guides.
Usage (repo root): python3 scripts/qa/brand_name_check.py"""
import re, sys
from pathlib import Path

RX = re.compile(r"Yupitek(?!_AP)")
ROOTS = ("content", "layouts", "i18n", "data", "config", "hugo.toml", "static")
SKIP_PREFIX = ("static/project/js/", "static/project/css/")
EXTS = {".md", ".html", ".toml", ".txt", ".svg", ".json", ".yaml", ".yml"}


def files():
    for r in ROOTS:
        p = Path(r)
        for f in ([p] if p.is_file() else sorted(p.rglob("*")) if p.exists() else []):
            if f.is_file() and f.suffix in EXTS and not str(f).startswith(SKIP_PREFIX):
                yield f


def main() -> int:
    hits = 0
    for f in files():
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for m in RX.finditer(line):
                hits += 1
                print(f"{f}:{n}: {line.strip()[:100]}")
    print(f"TOTAL hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
