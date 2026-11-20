#!/usr/bin/env python3
"""Fail if a built page shows Markdown bold markers (**) as text outside code.
CommonMark does not open/close ** next to CJK punctuation such as （）「」：, so `**用語（English）**後文`
renders the asterisks literally.
Usage: python3 scripts/qa/literal_markdown_check.py public"""
import re
import sys
from pathlib import Path

CODE = re.compile(r"<(pre|code|script|style)[^>]*>.*?</\1>", re.S)


def visible(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", CODE.sub("", html))


def main() -> int:
    root = Path(sys.argv[1])
    bad = []
    pages = list(root.rglob("index.html"))
    for f in pages:
        text = visible(f.read_text(encoding="utf-8"))
        i = text.find("**")
        if i >= 0:
            bad.append((f.relative_to(root), text[max(i - 30, 0):i + 40].replace("\n", " ")))
    for path, ctx in bad[:20]:
        print(f"LITERAL ** /{path.parent}/  …{ctx}…")
    print(f"{len(pages)} pages, {len(bad)} with literal **")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
