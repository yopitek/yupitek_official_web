#!/usr/bin/env python3
"""Pre-release checks for this Hugo site. Run from the repo root: python3 scripts/pre_release_check.py [--no-build]
Checks: (1) git state vs origin/main, (2) secret patterns in tracked+untracked files, (3) leftover simplified characters in zh-tw content,
(4) hugo build with warnings summary. Exit code 1 if any check fails. Never prints secret values."""
import os, re, subprocess, sys, tempfile

SECRET_RULES = [r"cfut_[A-Za-z0-9]{30,}", r"cfat_[A-Za-z0-9]{30,}", r"ghp_[A-Za-z0-9]{30,}", r"gho_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{30,}",
                r"\bsk-[A-Za-z0-9_-]{20,}", r"CWA-[0-9A-F]{8}-(?:[0-9A-F]{4}-){3}[0-9A-F]{12}", r"\bAKIA[0-9A-Z]{16}\b", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"]
SIMPLIFIED = "电为学华云这个们说时进对发关单体产从备点来试层车东门问间头开买场实现"
ALLOWLIST = ("content/zh-tw/blog/ai-generated-product-images-baoyu-workflow/",)  # quotes Xiaohongshu/WeChat prompts verbatim
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".mp4", ".woff", ".woff2", ".svg")


def parse_ahead_behind(out: str) -> tuple:
    a, b = out.split()
    return int(a), int(b)


def scan_text(text: str) -> list:
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        if "secret-scan: allow" in line:
            continue
        for pat in SECRET_RULES:
            for m in re.finditer(pat, line):
                hits.append((n, m.group(0)[:4] + "…(%d chars)" % len(m.group(0))))
    return hits


def simplified_chars(text: str) -> list:
    return sorted({c for c in text if c in SIMPLIFIED})


def is_allowlisted(path: str) -> bool:
    return path.startswith(ALLOWLIST)


def sh(*cmd) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def check_git() -> bool:
    subprocess.run(["git", "fetch", "-q", "origin"], capture_output=True)
    ahead, behind = parse_ahead_behind(sh("git", "rev-list", "--left-right", "--count", "HEAD...origin/main"))
    dirty = [l for l in sh("git", "status", "--porcelain").splitlines() if l.strip()]
    print(f"[git] ahead {ahead}, behind {behind}, uncommitted {len(dirty)}")
    return behind == 0 and not dirty


def tracked_files() -> list:
    return [f for f in sh("git", "ls-files", "-co", "--exclude-standard").splitlines() if os.path.isfile(f)]


def check_secrets() -> bool:
    bad = 0
    for f in tracked_files():
        if f.lower().endswith(SKIP_EXT) or os.path.getsize(f) > 2_000_000:
            continue
        for n, prev in scan_text(open(f, encoding="utf-8", errors="ignore").read()):
            print(f"[secrets] {f}:{n} {prev}"); bad += 1
    print(f"[secrets] {bad} hit(s)")
    return bad == 0


def check_zh_tw() -> bool:
    bad = 0
    for f in tracked_files():
        if f.startswith("content/zh-tw/") and f.endswith(".md") and not is_allowlisted(f):
            chars = simplified_chars(open(f, encoding="utf-8", errors="ignore").read())
            if chars:
                print(f"[zh-tw] {f}: {''.join(chars)}"); bad += 1
    print(f"[zh-tw] {bad} file(s) with simplified characters")
    return bad == 0


def check_build() -> bool:
    out = tempfile.mkdtemp(prefix="prc_build_")
    p = subprocess.run(["hugo", "--destination", out, "--logLevel", "warn"], capture_output=True, text=True)
    warns = [l for l in (p.stdout + p.stderr).splitlines() if "WARN" in l or "ERROR" in l]
    print(f"[hugo] exit {p.returncode}, {len(warns)} warning/error line(s)")
    for w in warns[:6]:
        print("   ", re.sub(r"^[0-9: -]*", "", w)[:140])
    return p.returncode == 0 and not any("ERROR" in w for w in warns)


if __name__ == "__main__":
    checks = [check_git, check_secrets, check_zh_tw] + ([] if "--no-build" in sys.argv else [check_build])
    results = [c() for c in checks]
    print("RESULT:", "PASS" if all(results) else "FAIL")
    sys.exit(0 if all(results) else 1)
