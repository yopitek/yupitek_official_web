"""banner_ratio_check 的 frontmatter 解析測試。"""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("brc", "scripts/qa/banner_ratio_check.py")
brc = importlib.util.module_from_spec(spec); spec.loader.exec_module(brc)

def write(tmp, body):
    f = tmp / "_index.md"; f.write_text(f"---\n{body}\n---\n內文\n", encoding="utf-8"); return f

def test_double_quotes(tmp_path):
    assert brc.hero(write(tmp_path, 'featureimage: "/images/a.webp"')) == "/images/a.webp"

def test_single_quotes(tmp_path):
    """ja/flipper-alfa-compatibility 用單引號，舊版會把引號一起吃進路徑。"""
    assert brc.hero(write(tmp_path, "featureimage: '/images/a.webp'")) == "/images/a.webp"

def test_unquoted(tmp_path):
    assert brc.hero(write(tmp_path, 'featureimage: /images/a.webp')) == "/images/a.webp"

def test_bannerimage_wins(tmp_path):
    f = write(tmp_path, 'featureimage: "/images/f.webp"\nbannerimage: "/images/b.webp"')
    assert brc.hero(f) == "/images/b.webp"

def test_hidden_hero_is_skipped(tmp_path):
    assert brc.hero(write(tmp_path, 'featureimage: "/images/a.webp"\nhideFeatureImage: true')) is None

def test_no_image(tmp_path):
    assert brc.hero(write(tmp_path, 'title: "x"')) is None
