#!/usr/bin/env python3
"""Phase E2 facts for hak5 part 2 (e2_hak5_b). Run from repo root. Exit 1 on any failure."""
import re, sys
from pathlib import Path

sys.path.insert(0, "scripts/qa")
from no_authorized_claims import RX  # noqa: E402

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
PRODS = ["packet-squirrel", "plunder-bug", "screen-crab", "shark-jack", "shark-jack-cable",
         "usb-rubber-ducky", "wifi-pineapple-enterprise", "wifi-pineapple-mark7", "wifi-pineapple-pager"]
results = []


def check(name, ok):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def files(loc, prod):
    d = Path(f"content/{loc}/products/hak5/{prod}")
    return [p for p in (d / "index.md", d / "_index.md") if p.exists()]


def text(loc, prod):
    ps = files(loc, prod)
    return "\n".join(p.read_text(encoding="utf-8") for p in ps)


def fm_value(t, key):
    m = re.search(rf'^{key}:\s*"(.*)"\s*$', t, re.M)
    return m.group(1) if m else None


def no(loc, prod, pattern, label):
    t = text(loc, prod)
    m = re.search(pattern, t, re.I)
    check(f"{loc}/{prod}: {label}", m is None)
    if m:
        print("     hit:", m.group(0))


# ---- Decision 1: no authorized / distributor claims; title format (en + zh-tw)
for loc in LOCALES:
    for prod in PRODS:
        t = text(loc, prod)
        m = RX.search(t)
        check(f"{loc}/{prod}: no authorized-claim regex hit", m is None)
for prod in PRODS:
    t = Path(f"content/en/products/hak5/{prod}/index.md").read_text(encoding="utf-8")
    title = fm_value(t, "title")
    st = fm_value(t, "seo_title")
    want = f"{title} | Hak5 Taiwan | Yopitek"
    if len(want) > 60:
        want = f"{title} | Yopitek"
    check(f"en/{prod}: seo_title == '{want}'", st == want)
    check(f"en/{prod}: no distributor/authorized words outside legal", not re.search(
        r"distributor|authorized (?:dealer|reseller|partner)", t, re.I))
    t = Path(f"content/zh-tw/products/hak5/{prod}/index.md").read_text(encoding="utf-8")
    title = fm_value(t, "title")
    st = fm_value(t, "seo_title")
    want = f"{title} Hak5 台灣 | Yopitek"
    if len(want) > 60:
        want = f"{title} | Yopitek"
    check(f"zh-tw/{prod}: seo_title == '{want}'", st == want)
    check(f"zh-tw/{prod}: no 經銷/代理商", not re.search(r"經銷|代理商|授權經銷|台灣授權", t))

# ---- Decision 2: disputed values removed
ENT = (r"five dual-band|五組|五组|5つの|5基|خمسة راديو|cinco radios|cinco rádios|пять двухдиапазонных"
       r"|Radio ?[0-4]|Radio 2/3/4|راديو [0-4]|Rádio [0-4]|Радио [0-4]|Radio0")
MK7 = (r"5 ?GHz|5 ?ГГц|dual-?band|double bande|doble banda|banda dupla|雙頻|双频|デュアルバンド|ثنائي النطاق"
       r"|MT7601U|MT7610U|802\.11 ?a/b/g/n/ac|802\.11ac|\b2[.,]4 ?(?:GHz|ГГц)|Двухдиапазон")
for loc in LOCALES:
    no(loc, "wifi-pineapple-enterprise", ENT, "no radio-count claims")
    no(loc, "wifi-pineapple-mark7", MK7, "no band/5GHz/dual-band claims")

# ---- Decision 3
RACK = (r"rack-mountable|rack-mounted|機架可安裝|机架可安装|機架安裝）|机架安装）|ラックマウント対応|ラックマウント）"
        r"|قابل للتركيب في حامل|تركيب في حامل بغرفة|montable en rack|montaje en rack en sala"
        r"|montável em rack|montagem em rack em sala|монтаж в стойку 1U|монтаж в стойку в серверной|1U-Rack|rackmount")
for loc in LOCALES:
    no(loc, "wifi-pineapple-enterprise", RACK, "1U rack not presented as standard")
    no(loc, "wifi-pineapple-pager", r"Retina", "no Retina wording")
    no(loc, "wifi-pineapple-pager", r"Python", "no Python payload claim")
    no(loc, "wifi-pineapple-pager", r"WPA3", "no WPA3 Enterprise attack claim")
    no(loc, "wifi-pineapple-pager",
       r"4 ?(?:顆|颗|つの)? ?RGB[ -]?(?:buttons?|按鈕|按钮|ボタン|botones|botões|Tasten|boutons|кнопки)|أزرار RGB",
       "buttons wording follows official (D-pad + A/B)")
    t = text(loc, "wifi-pineapple-pager")
    check(f"{loc}/wifi-pineapple-pager: battery ~4 hours present",
          re.search(r"(?<![\d.])4 ?(?:hours?|小時|小时|時間|ساعات|horas|час\w*|Stunden|heures)", t) is not None)
    no(loc, "usb-rubber-ducky",
       r"1 ?(?:second|秒|segundo|секунд|Sekunde|seconde)|1秒|أقل من ثانية|menos de 1|менее чем за 1",
       "no unsourced '1 second' OS detection")
    t = text(loc, "usb-rubber-ducky")
    check(f"{loc}/usb-rubber-ducky: has OS detection wording (OS_DETECT / ANDROID list)",
          loc in ("de", "fr") or re.search(r"ChromeOS", t) is not None)
    no(loc, "usb-rubber-ducky", r"Kompatibilität \||Compatibilité \|", "no unsourced compatibility row")
    no(loc, "screen-crab", r"1920", "no resolution number")
    no(loc, "shark-jack", r"0\.2 ?(?:Wh|W\b|Вт)", "no disputed battery 0.2Wh")
    no(loc, "wifi-pineapple-pager", r"Retina", "no Retina (dup)")
    t = text(loc, "packet-squirrel")
    check(f"{loc}/packet-squirrel: size 50 x 40 x 15 mm / 24 g",
          re.search(r"50 ?[×x] ?40 ?[×x] ?15", t) is not None and re.search(r"(?<![\d.])24 ?g\b", t) is not None)
    t = text(loc, "shark-jack")
    check(f"{loc}/shark-jack: runtime 10-15 min",
          re.search(r"10[–~-] ?15", t) is not None)

# plunder-bug de/fr title must not be passive-only
for loc in ("de", "fr"):
    t = text(loc, "plunder-bug")
    check(f"{loc}/plunder-bug: title not passive-only", not re.search(r'^title:.*(Passives|Passif)', t, re.M))

fails = [n for n, ok in results if not ok]
print(f"\nTOTAL {len(results)}  FAIL {len(fails)}")
sys.exit(1 if fails else 0)
