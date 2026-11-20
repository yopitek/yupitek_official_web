"""Run: uv run --with pytest python -m pytest scripts/qa/test_products_jsonld_check.py -q"""
import re
from pathlib import Path

SRC = Path(__file__).with_name("products_jsonld_check.py").read_text()
# Load only the helper functions; the module body runs the full check at import time.
ns = {}
exec(compile("import json,re\n" + "\n".join(re.findall(r"^def blocks[\s\S]*?(?=^def flat)|^def flat[\s\S]*?(?=^errs)", SRC, re.M)), "jsonld", "exec"), ns)

LD = '{"@context":"https://schema.org","@type":"Product","name":"X"}'


def test_quoted_script_tag():
    html = f'<script type="application/ld+json">{LD}</script>'
    assert [b["@type"] for b in ns["blocks"](html)] == ["Product"]


def test_minified_unquoted_script_tag():
    # hugo --minify drops attribute quotes
    html = f"<script type=application/ld+json>{LD}</script>"
    assert [b["@type"] for b in ns["blocks"](html)] == ["Product"]
