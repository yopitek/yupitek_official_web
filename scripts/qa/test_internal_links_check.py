"""Run: uv run --with pytest python -m pytest scripts/qa/test_internal_links_check.py -q"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("ilc", Path(__file__).with_name("internal_links_check.py"))
ilc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ilc)


def test_quoted_href_is_found():
    html = '<a class=x href="/en/blog/foo/">Foo</a>'
    assert ilc.links(html, "en", "blog") == {"/en/blog/foo/"}


def test_minified_unquoted_href_is_found():
    # hugo --minify drops attribute quotes
    html = "<a class=x href=/en/blog/foo/>Foo</a><a href=https://yupitek.com/en/products/acr/acr122u/>R</a>"
    assert ilc.links(html, "en", "blog") == {"/en/blog/foo/"}
    assert ilc.links(html, "en", "products") == {"/en/products/acr/acr122u/"}


def test_fragment_and_query_links_are_ignored():
    html = "<a href=/en/blog/foo/#x>a</a><a href=/en/blog/bar/?q=1>b</a><a href=/en/blog/tags/x/>c</a>"
    assert ilc.links(html, "en", "blog") == set()
