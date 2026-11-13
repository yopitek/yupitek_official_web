#!/usr/bin/env python3
"""e2_hak5_a Phase E2 斷言：hak5 Part1 八品（從 repo 根目錄執行；純標準庫）。"""
import importlib.util
import re
import sys
from pathlib import Path

LOC = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
FULL = [l for l in LOC if l not in ("de", "fr")]
PRODUCTS = ["bash-bunny", "key-croc", "malicious-cable-detector", "omg-adapter",
            "omg-cable", "omg-plug", "omg-programmer", "omg-unblocker"]
results = []


def txt(loc, p, name="index.md"):
    f = Path(f"content/{loc}/products/hak5/{p}/{name}")
    return f.read_text(encoding="utf-8") if f.exists() else ""


def check(name, ok):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name)


def must(loc, p, s):
    check(f"[{loc}/{p}] 含 {s!r}", s in txt(loc, p))


def mustnot(loc, p, s):
    check(f"[{loc}/{p}] 不含 {s!r}", s not in txt(loc, p))


spec = importlib.util.spec_from_file_location("nac", "scripts/qa/no_authorized_claims.py")
nac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nac)
EXTRA = re.compile(r"distributor|經銷|经销|経銷|代理商|authorized hak5|дистрибьютор|موزع|distribuidor|distribuidora|distributeur|Händler|revendeur", re.I)

# 決策 1
for p in PRODUCTS:
    for loc in LOC:
        for name in ("index.md", "_index.md"):
            t = txt(loc, p, name)
            if t:
                hit = nac.RX.search(t) or EXTRA.search(t)
                check(f"[{loc}/{p}/{name}] 無授權經銷字樣", not hit)


def front(t):
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    return (m.group(1), m.group(2)) if m else ("", t)


def field(fm, key):
    m = re.search(rf'^{key}: "(.*)"$', fm, re.M)
    return m.group(1) if m else ""


def model(loc, p):
    return field(front(txt(loc, p))[0], "title")


for p in PRODUCTS:
    en, zh = txt("en", p), txt("zh-tw", p)
    fe, be = front(en)
    fz, bz = front(zh)
    me, mz = model("en", p), model("zh-tw", p)
    st = field(fe, "seo_title")
    check(f"[en/{p}] seo_title", st == f"{me} | Hak5 Taiwan | Yopitek" and len(st) <= 60 and "ALFA" not in st)
    st = field(fz, "seo_title")
    check(f"[zh-tw/{p}] seo_title", st == f"{mz} Hak5 台灣 | Yopitek" and len(st) <= 60)
    check(f"[en/{p}] description 120-160", 120 <= len(field(fe, "description")) <= 160)
    check(f"[zh-tw/{p}] description 50-90", 50 <= len(field(fz, "description")) <= 90)
    check(f"[en/{p}] FAQ 改為購買／詢價", "Where can I buy" not in en and "get a quote" in fe)
    check(f"[zh-tw/{p}] FAQ 改為購買／詢價", "在台灣哪裡可以購買" not in zh and "詢價" in fz)

    def para(body):
        body = re.sub(r"\{\{< alert.*?\{\{< /alert >\}\}", "", body, flags=re.S)
        return body.split("\n## ")[0].strip()

    n = len(para(be).split())
    check(f"[en/{p}] AI 引用段 40-60 字 (={n})", 40 <= n <= 60)
    n = len(para(bz))
    check(f"[zh-tw/{p}] AI 引用段 60-100 字 (={n})", 60 <= n <= 100)

# 決策 3
for loc in FULL:
    for bad in ("dual-head", "雙頭", "双头", "デュアルヘッド", "cabeza doble", "duas pontas", "двусторонняя", "مزدوج الرأس"):
        mustnot(loc, "omg-programmer", bad)
    t = txt(loc, "omg-programmer")
    check(f"[{loc}/omg-programmer] 連接介面列標示 USB A+C", bool(re.search(r"^\|.*USB-A \+ USB-C.*USB A\+C", t, re.M)))
    mustnot(loc, "bash-bunny", "bash-bunny-by-hak5")
    must(loc, "bash-bunny", "https://documentation.hak5.org/bash-bunny")
    for s in ("890", "300", "192"):
        t = txt(loc, "omg-unblocker")
        check(f"[{loc}/omg-unblocker] 規格列含 {s}", bool(re.search(rf"^\|.*{s}.*\|\s*$", t, re.M)))
for loc in LOC:
    for s in ("500", "900", "MFi"):
        must(loc, "malicious-cable-detector", s)
for loc in ("de", "fr"):
    must(loc, "bash-bunny", "| SERIAL |")
    for s in ("Basic", "Elite", "DuckyScript 2", "DuckyScript 3"):
        must(loc, "omg-cable", s)
for s in ("USB-A zu USB-C / Lightning", "Sicherheitsbewusstsein der Benutzer gegenüber", "Zielbewusstseins", "Datenblocker-Bypass"):
    for p in PRODUCTS:
        mustnot("de", p, s)
for s in ("USB-A vers USB-C / Lightning", "sensibilité des utilisateurs", "sensibilisation des environnements", "Contournement de Bloqueurs"):
    for p in PRODUCTS:
        mustnot("fr", p, s)
must("de", "omg-adapter", "Red Team")
must("fr", "omg-adapter", "Red Team")

print(f"\n總計 {len(results)} 條，失敗 {results.count(False)} 條")
sys.exit(1 if False in results else 0)
