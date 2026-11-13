#!/usr/bin/env python3
"""e2_hak5_hub facts: hak5 hub cleanup + new Shark Jack Display / LAN Turtle Hub pages. Run from repo root."""
import re, sys
from pathlib import Path

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
NEW = ["shark-jack-display", "lan-turtle-hub"]
fails = 0


def check(name, ok):
    global fails
    fails += not ok
    print(("PASS " if ok else "FAIL ") + name)


def card(text, slug):
    m = re.search(r'\{\{< card [^>]*href="[^"]*/hak5/%s/"[^>]*>\}\}(.*?)\{\{< /card >\}\}' % slug, text, re.S)
    return m.group(1) if m else None


AUTH = re.compile(r"authori[sz]ed (?:taiwan )?distributor|授權(?:經銷|代理)|台灣授權|台湾授权|授权(?:经销|代理)|distribuye|distribue|vertreibt|поставляет|توزع|distribuidor|代理 HAK5", re.I)
BAND = re.compile(r"802\.11|dual-band|dual band|双频|雙頻|デュアルバンド|doppio|double bande|Dual-Band|ثنائي النطاق|dual-band|двухдиап", re.I)
ANT = re.compile(r"antenna|天線|天线|アンテナ|Antenne|antena|антенн|هوائي|antenne", re.I)

for loc in LOCALES:
    hub = Path(f"content/{loc}/products/hak5/_index.md").read_text(encoding="utf-8")
    fm = hub.split("---")[1]
    check(f"{loc} hub frontmatter no authorization/distribution claim", not AUTH.search(fm))
    check(f"{loc} hub Mark VII card no band claim", not BAND.search(card(hub, "wifi-pineapple-mark7") or "BAND"))
    check(f"{loc} hub Enterprise card no antenna claim", not ANT.search(card(hub, "wifi-pineapple-enterprise") or "ANT"))
    for s in NEW:
        check(f"{loc} hub has card -> /{loc}/products/hak5/{s}/", card(hub, s) is not None)
        p = Path(f"content/{loc}/products/hak5/{s}/index.md")
        check(f"{loc} {s} page exists", p.exists())
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        check(f"{loc} {s} draft:false + brands hak5", "draft: false" in t and 'brands: ["hak5"]' in t)
        check(f"{loc} {s} no authorization claim", not AUTH.search(t))
        check(f"{loc} {s} has warning alert", '{{< alert "warning" >}}' in t)
        check(f"{loc} {s} official doc link", "documentation.hak5.org/" + s in t)
        if loc in ("en", "zh-tw"):
            check(f"{loc} {s} seo_title + faq>=3 + faq shortcode", "seo_title:" in t and len(re.findall(r"- question:", t)) >= 3 and "{{< faq >}}" in t)
        check(f"{loc} {s} no sold-out wording", not re.search(r"sold out|售完|缺貨|在庫切れ", t, re.I))

print(f"{fails} failing")
sys.exit(1 if fails else 0)
