#!/usr/bin/env python3
"""hak5_a 事實斷言：hak5 Part1 八品（從 repo 根目錄執行）。"""
import sys
from pathlib import Path

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
FULL = [l for l in LOCALES if l not in ("de", "fr")]
BASE = "content/{loc}/products/hak5/{p}/index.md"
OMG4 = ["omg-adapter", "omg-cable", "omg-plug", "omg-unblocker"]
results = []


def read(loc, p):
    f = Path(BASE.format(loc=loc, p=p))
    return f.read_text(encoding="utf-8") if f.exists() else None


def check(name, ok):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def must(loc, p, s):
    t = read(loc, p)
    check(f"[{loc}/{p}] 必含 {s!r}", t is not None and s in t)


def mustnot(loc, p, s):
    t = read(loc, p)
    check(f"[{loc}/{p}] 必不含 {s!r}", t is not None and s not in t)


# 1. 失效連結
for loc in LOCALES:
    for p in OMG4 + ["omg-programmer"]:
        mustnot(loc, p, "downloads.hak5.org/omg")
    if loc in FULL:
        for p in OMG4:
            must(loc, p, "https://o-mg.github.io/WebFlasher/")
    for p in ("omg-adapter", "omg-unblocker"):
        mustnot(loc, p, "o.mg.lol/setup/OMGCable/")
    mustnot(loc, "malicious-cable-detector", "downloads.hak5.org/malicious-cable-detector")
    mustnot(loc, "key-croc", "keycroc-by-hak5")
for loc in FULL:
    must(loc, "key-croc", "https://documentation.hak5.org/key-croc")
    must(loc, "malicious-cable-detector", "https://shop.hak5.org/products/malicious-cable-detector-by-o-mg")
for loc in ("de", "fr"):
    must(loc, "malicious-cable-detector", "https://shop.hak5.org/products/malicious-cable-detector-by-o-mg")

# 2. key-croc 規格
for loc in LOCALES:
    for s in ("2.4 GHz", "74 × 27 × 14 mm", "5 W"):
        must(loc, "key-croc", s)
for loc in FULL:
    must(loc, "key-croc", "SSH")

# 3. bash-bunny：移除首創與 Cloud C²
first = {"en": ["world's first"], "zh-tw": ["世界首款"], "zh-cn": ["世界首款"], "ja": ["世界初"],
         "es": ["Primera plataforma", "Primera en el mundo"], "pt": ["Primeira plataforma", "Primeira no mundo"],
         "ru": ["Первая в мире"], "ar": ["الأولى من نوعها", "الأولى عالمياً"]}
for loc in FULL:
    mustnot(loc, "bash-bunny", "Cloud C²")
    for s in first[loc]:
        mustnot(loc, "bash-bunny", s)
for s in ("eMMC", "BashBunny-Skriptsprache"):
    mustnot("de", "bash-bunny", s)
for s in ("eMMC", "langage de script BashBunny"):
    mustnot("fr", "bash-bunny", s)

# 4. malicious-cable-detector：移除「唯一」
only = {"en": ["World's Only", "world's only"], "zh-tw": ["全球唯一"], "zh-cn": ["全球唯一"], "ja": ["世界唯一"],
        "es": ["Única herramienta", "única herramienta"], "pt": ["Única ferramenta", "única ferramenta"],
        "ru": ["Единственный", "единственный"], "ar": ["الوحيدة"]}
for loc in FULL:
    for s in only[loc]:
        mustnot(loc, "malicious-cable-detector", s)
mustnot("de", "malicious-cable-detector", "versteckte Mikrocontroller")
mustnot("fr", "malicious-cable-detector", "microcontrôleurs cachés")

# 5. omg-plug Self-Destruct 僅 Elite
suffix = {"en": "(Elite only)", "zh-tw": "（僅限 Elite）", "zh-cn": "（仅限 Elite）", "ja": "（Eliteのみ）",
          "es": "(solo Elite)", "pt": "(somente Elite)", "ru": "(только Elite)", "ar": "(في إصدار Elite فقط)"}
for loc in FULL:
    must(loc, "omg-plug", "Self-Destruct" + ("" if suffix[loc].startswith("（") else " ") + suffix[loc])

# 6. 警語併入 index.md
label = {"en": "Legal Use Disclaimer", "zh-tw": "合法使用聲明", "zh-cn": "合法使用声明",
         "ja": "法的使用に関する免責事項", "es": "Aviso legal de uso", "pt": "Aviso legal de uso",
         "ru": "Юридическое предупреждение об использовании", "ar": "إخلاء المسؤولية القانونية للاستخدام"}
for loc in FULL:
    for p in ["bash-bunny", "key-croc", "omg-adapter", "omg-cable", "omg-plug", "omg-programmer", "omg-unblocker"]:
        must(loc, p, '{{< alert "warning" >}}')
        must(loc, p, label[loc])

# 7. de/fr 不實內容
bad = [("de", "omg-cable", "Exfiltrations-"), ("fr", "omg-cable", "d'exfiltration"),
       ("de", "omg-plug", "Ladegerät-"), ("fr", "omg-plug", "boîtier de chargeur"),
       ("de", "omg-programmer", "Payload-Einstellungen"), ("fr", "omg-programmer", "paramètres de payload"),
       ("de", "omg-unblocker", "Wirksamkeit von USB-Datenblockierungsgeräten"),
       ("fr", "omg-unblocker", "tester l'efficacité des dispositifs")]
for loc, p, s in bad:
    mustnot(loc, p, s)

fails = [n for n, ok in results if not ok]
print(f"\n總計 {len(results)} 條，失敗 {len(fails)} 條")
sys.exit(1 if fails else 0)
