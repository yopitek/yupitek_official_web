#!/usr/bin/env python3
"""Check the CSP rollout on a served build: every page sends Content-Security-Policy-Report-Only
(or the enforced header), the browser reports no CSP violations, and /.well-known/security.txt is valid.
Serve the build with Pages semantics first:  npx wrangler@3 pages dev public --port 8790
Usage: uv run --with playwright python scripts/qa/csp_check.py http://127.0.0.1:8790"""
import sys
from playwright.sync_api import sync_playwright

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ko", "de", "fr", "es", "pt", "ru", "ar"]
PAGES = ["", "blog/", "products/alfa/awus036ax/", "blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/"]
EXTRA = ["/en/solution/project/", "/en/contact/", "/alfa_compare.html"]


def main() -> int:
    base = sys.argv[1].rstrip("/")
    paths = [f"/{l}/{p}" for l in LOCALES for p in PAGES] + EXTRA
    fails = []
    with sync_playwright() as pw:
        page = pw.chromium.launch().new_page()
        violations = []
        page.on("console", lambda m: violations.append(m.text) if "Content Security Policy" in m.text else None)
        for p in paths:
            violations.clear()
            res = page.goto(base + p, wait_until="networkidle")
            h = res.headers if res else {}
            if not (h.get("content-security-policy-report-only") or h.get("content-security-policy")):
                fails.append(f"{p}: no CSP header")
            fails += [f"{p}: {v[:160]}" for v in violations]
        txt = page.request.get(base + "/.well-known/security.txt")
        body = txt.text() if txt.ok else ""
        for field in ("Contact:", "Expires:"):
            if field not in body:
                fails.append(f"/.well-known/security.txt: missing {field} (status {txt.status})")
    for f in fails:
        print("FAIL", f)
    print(f"{len(paths)} pages, {len(fails)} problems")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
