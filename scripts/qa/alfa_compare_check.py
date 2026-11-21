#!/usr/bin/env python3
"""Check static/alfa_compare.html against the GX10 test results (2026-11): all 9 adapters,
correct chipsets, a handshake column (7 of 9 end-to-end) and the ACS/EACS 5 GHz AP note.
Usage (repo root): python3 scripts/qa/alfa_compare_check.py [path-or-url]"""
import html
import re
import sys
import urllib.request

# Chipsets per ALFA's official spec sheets (checked 2026-11-22). The AXM and AXML carry the same
# MT7921AUN and enumerate as 0e8d:7961, so the suffix cannot be told apart by testing.
CHIPS = {
    "AWUS036ACM": "MT7612U", "AWUS036ACHM": "MT7610U", "AWUS036ACH": "RTL8812AU",
    "AWUS036ACS": "RTL8811AU", "AWUS036EACS": "RTL8821CU", "AWUS036AX": "RTL8832BU",
    "AWUS036AXER": "RTL8832BU", "AWUS036AXM": "MT7921AUN", "AWUS036AXML": "MT7921AUN",
}
NO_HANDSHAKE = {"AWUS036AXM", "AWUS036AXML"}
AP_20MHZ = {"AWUS036ACS", "AWUS036EACS"}


def text(cell):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", cell))).strip()


def spec_table(page):
    table = re.search(r"<table>.*?</table>", page, re.S).group(0)
    heads = [text(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)]
    rows = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
        cells = [text(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if cells:
            rows[cells[0]] = dict(zip(heads, cells))
    return heads, rows


def problems(page):
    heads, rows = spec_table(page)
    errs = []
    missing = set(CHIPS) - set(rows)
    if missing:
        errs.append(f"missing models: {sorted(missing)}")
    hs = next((h for h in heads if "handshake" in h.lower()), None)
    if not hs:
        errs.append("no handshake column")
    for model, chip in CHIPS.items():
        row = rows.get(model)
        if not row:
            continue
        if row.get("Chipset") != chip:
            errs.append(f"{model} chipset {row.get('Chipset')!r} != {chip}")
        if hs:
            want = "❌" if model in NO_HANDSHAKE else "✅"
            if want not in row.get(hs, ""):
                errs.append(f"{model} handshake {row.get(hs)!r} should contain {want}")
        if model in AP_20MHZ and not ("802.11a" in row.get("AP Mode", "") and "20 MHz" in row.get("AP Mode", "")):
            errs.append(f"{model} AP Mode {row.get('AP Mode')!r} lacks the 5 GHz 802.11a 20 MHz note")
    if re.search(r"All 8 Models|8 款", page):
        errs.append("page still says 8 models")
    return errs


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 else "static/alfa_compare.html"
    if src.startswith("http"):
        page = urllib.request.urlopen(src).read().decode("utf-8")
    else:
        page = open(src, encoding="utf-8").read()
    errs = problems(page)
    for e in errs:
        print("FAIL", e)
    print(f"{len(errs)} problems")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
