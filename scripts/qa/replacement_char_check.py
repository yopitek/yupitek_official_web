#!/usr/bin/env python3
"""Fail if site sources contain U+FFFD (the replacement character a broken emoji or
mis-decoded text leaves behind) or bytes that are not valid UTF-8. Both render as "�" on the page.
Usage (repo root): python3 scripts/qa/replacement_char_check.py"""
import sys
from pathlib import Path

ROOTS = ("content", "layouts", "i18n", "data", "config", "static")
EXTS = {".md", ".html", ".toml", ".txt", ".svg", ".json", ".yaml", ".yml", ".xml"}


def main() -> int:
    hits = 0
    for r in ROOTS:
        for f in sorted(Path(r).rglob("*")) if Path(r).exists() else []:
            if not (f.is_file() and f.suffix in EXTS):
                continue
            try:
                text = f.read_bytes().decode("utf-8")
            except UnicodeDecodeError as e:
                hits += 1
                print(f"{f}: invalid UTF-8 at byte {e.start}")
                continue
            for n, line in enumerate(text.splitlines(), 1):
                if "�" in line:
                    hits += 1
                    print(f"{f}:{n}: {line.strip()[:100]}")
    print(f"TOTAL hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
