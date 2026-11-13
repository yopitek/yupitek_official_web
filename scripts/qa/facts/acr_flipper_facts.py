#!/usr/bin/env python3
"""Phase C facts check for ACR + Flipper Zero product pages. Run from repo root."""
import sys, os, re

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
ACR122_URL = ("https://www.acs.com.hk/cn/products/73/acr122u-nfc-"
              "%E9%9D%9E%E6%8E%A5%E8%A7%B8%E5%BC%8F%E6%99%BA%E8%83%BD%E5%8D%A1%E8%AF%BB%E5%86%99%E5%99%A8/")
FZ = "https://flipper.net/products/"
SAM_CLK = {  # new SAM clock cell per locale (10 MHz only on request)
    "en": "5 MHz (10 MHz on special request)", "zh-tw": "5 MHz（10 MHz 須另行要求）",
    "zh-cn": "5 MHz（10 MHz 需另行要求）", "ja": "5 MHz（10 MHz は要請により対応）",
    "ar": "5 MHz (10 MHz عند الطلب الخاص)", "es": "5 MHz (10 MHz bajo solicitud especial)",
    "pt": "5 MHz (10 MHz mediante solicitação especial)", "ru": "5 МГц (10 МГц по специальному запросу)",
    "de": "5 MHz (10 MHz auf besondere Anfrage)", "fr": "5 MHz (10 MHz sur demande spécifique)",
}
fails = 0
total = 0

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def check(path, must=(), mustnot=()):
    global fails, total
    if not os.path.exists(path):
        print(f"SKIP (no page) {path}")
        return
    t = read(path)
    for s in must:
        total += 1
        ok = s in t
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} contains {s!r} :: {path}")
    for s in mustnot:
        total += 1
        ok = s not in t
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} not-contains {s!r} :: {path}")

def card_line(path, href_part):
    lines = read(path).splitlines()
    for i, l in enumerate(lines):
        if href_part in l:
            return lines[i + 1]
    return ""

for L in LOCALES:
    b = f"content/{L}/products"
    p15 = f"{b}/acr/acr1552u/_index.md"
    t15 = read(p15)
    for name, rx in [("dims", r"98[.,]0 × 65[.,]0 × 12[.,]8 (mm|мм)"), ("weight", r"89 (g|г) \(±5 (g|г), USB Type-A\)"),
                     ("current", r"300 (mA|мА)")]:
        total += 1
        ok = re.search(rx, t15) is not None
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} 1552U {name} ~ {rx!r} :: {p15}")
    check(p15,
          must=["-20°C – 70°C",
                "ACR1552U-M1", "ACR1552U-MF", "500,000", "FIDO2", "UKCA", "WEEE", "WHQL",
                "J-LIS", SAM_CLK[L]],
          mustnot=["0°C – 60°C", "up to 10 MHz"])
    check(f"{b}/acr/acr1252u/_index.md",
          must=["IEC/EN 62368", "TELEC", "UKCA", "BIS", "WEEE", "500,000", "0°C – 60°C"],
          mustnot=["60950", "MIC", "Solaris", "3.1", "FeliCa Performance"])
    check(f"{b}/acr/acr122u/_index.md", must=[ACR122_URL])
    p = f"{b}/acr/_index.md"
    if os.path.exists(p):
        total += 1
        ok = "FeliCa" in card_line(p, "/products/acr/acr122u/")
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} hub ACR122U card mentions FeliCa :: {p}")
    check(f"{b}/flipperzero/flipper-zero/_index.md",
          must=["2100", "5.4", "100 × 40 × 25 mm", FZ + "flipper-zero", "microSD", "USB-A"],
          mustnot=["2000mAh", "2000 mAh", "5.0", "102 ×", "GPIO × 23", "23 Pin", "23-pin", "23ピン",
                   "23 pin", "23 دبوس", "23 pines", "23 pinos", "23-пин", "23 broches", "23-Pin"])
    fp = f"{b}/flipperzero/flipper-zero/_index.md"
    total += 1
    ok = any("GPIO" in l and "13" in l for l in read(fp).splitlines())
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} a GPIO line states 13 user I/O :: {fp}")
    check(f"{b}/flipperzero/_index.md", must=["5.4", FZ + "flipper-zero"], mustnot=["5.0"])
    check(f"{b}/flipperzero/wifi-devboard/_index.md", must=[FZ + "wifi-devboard"])
    check(f"{b}/flipperzero/silicone-case/_index.md", must=[FZ + "flipper-silicone-case"])
    check(f"{b}/flipperzero/video-game-module/_index.md", must=[FZ + "video-game-module-for-flipper-zero"])

print(f"\n{total - fails}/{total} passed, {fails} failed")
sys.exit(1 if fails else 0)
