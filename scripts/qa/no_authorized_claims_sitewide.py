#!/usr/bin/env python3
"""Site-wide rule: only ALFA Network is a Taiwan *authorized* distributor; every other brand is plain resale.
A line that claims authorization/official-distributor status is a violation unless it names ALFA and names no other brand.
Scans content/**/*.md, i18n/*.yaml, config/**/*.toml, layouts/**/*.html, static/llms.txt. Judged per sentence; negations ("not an authorized distributor") are allowed. Usage (repo root): python3 scripts/qa/no_authorized_claims_sitewide.py"""
import re, sys
from pathlib import Path

CLAIM = re.compile("|".join([
    r"authori[sz]ed\s+(?:taiwan\s+)?(?:distributor|dealer|reseller|partner|agent)", r"official\s+(?:taiwan\s+)?(?:distributor|reseller|dealer)",
    r"(?:distributor|reseller)\s+(?:authori[sz]ed|official)", r"authori[sz]ed\s+taiwan", r"taiwan\s+authori[sz]ed",
    r"授權(?:經銷|代理|經銷商|代理商|通路)", r"台灣授權", r"授权(?:经销|代理|经销商|代理商)", r"台湾授权", r"(?:正規|正规|認定|认定)(?:販売)?(?:代理|販売店)",
    r"autorisierte[rn]?\s+(?:distributor|händler|vertriebs\w*|fachhändler)", r"(?:distributeur|revendeur)\s+(?:agréé|autorisé)",
    r"(?:distribuidor|revendedor|distribuidora)\s+(?:autorizad[oa]|oficial)", r"(?:distribuidor|distribuidora)\s+autorizad",
    r"(?:авторизованн|официальн)\w+\s+(?:дистрибьютор|дилер)\w*", r"(?:موزع|الموزع|وكيل|الوكيل)\s+(?:ال)?معتمد",
    r"offizieller\s+(?:distributor|händler)", r"distributeur\s+officiel", r"authori[sz]ed\s+distribution",
]), re.I)
OTHERS = re.compile(r"ubiquiti|unifi|sierra|mellanox|nvidia|connectx|flipper|hak5|acs\b|acr\d|sdr-?lab|sdrlab|ibeacon|rtx\s?50|graphic ?card|顯示卡|显卡|rtl-sdr|o\.mg|pineapple", re.I)
NEGATION = re.compile(r"\bnot\b|\bnon-|\bno\b|非|不是|並非|并非|nicht|\bne\b|\bpas\b|\bno es\b|\bnão\b|не явля\w+|не авторизован\w*|\bkein\w*|ليس|لسنا|ではありません|ではない|ではなく", re.I)
SPLIT = re.compile(r"[.;。；!?]\s*|\s[—–-]\s")
FILES = [*Path("content").rglob("*.md"), *Path("i18n").glob("*.yaml"), *Path("config").rglob("*.toml"), *Path("layouts").rglob("*.html"), Path("static/llms.txt")]


def main(argv) -> int:
    n = 0
    for f in sorted(p for p in FILES if p.is_file()):
        for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for sent in SPLIT.split(line):
                m = CLAIM.search(sent)
                if m and not NEGATION.search(sent) and ("alfa" not in sent.lower() or OTHERS.search(sent)):
                    n += 1
                    print(f"{f}:{i}: [{m.group(0)}] {sent.strip()[:110]}")
    print(f"TOTAL violations: {n}")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
