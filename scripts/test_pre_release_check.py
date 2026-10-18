import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import pre_release_check as prc


def test_secret_patterns_detected_and_masked():
    hits = prc.scan_text("a\nT='ghp_" + "a" * 36 + "'\n")
    assert hits and hits[0][0] == 2 and "aaaa" not in hits[0][1]


def test_secret_scan_allow_marker():
    assert prc.scan_text("x='ghp_" + "b" * 36 + "'  # secret-scan: allow") == []


def test_simplified_heuristic_flags_simplified_not_traditional():
    assert prc.simplified_chars("供电不足") == ["电"]
    assert prc.simplified_chars("供電不足") == []


def test_allowlisted_zh_tw_page_is_skipped():
    assert prc.is_allowlisted("content/zh-tw/blog/ai-generated-product-images-baoyu-workflow/_index.md")
    assert not prc.is_allowlisted("content/zh-tw/blog/other/_index.md")


def test_ahead_behind_parser():
    assert prc.parse_ahead_behind("3\t0\n") == (3, 0)
