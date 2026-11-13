#!/usr/bin/env python3
"""hak5_b facts check. Run from repo root. Exit 1 on any failure."""
import re, sys
from pathlib import Path

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
BASE = "content/{loc}/products/hak5"
results = []


def read(loc, prod=None):
    p = Path(BASE.format(loc=loc)) / (f"{prod}/index.md" if prod else "_index.md")
    return p.read_text(encoding="utf-8") if p.exists() else None


def check(name, ok):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def has(loc, prod, s, want=True):
    t = read(loc, prod)
    if t is None:
        return True  # page absent in this locale: skip
    return (s in t) == want


def rx(loc, prod, pattern, want=True):
    t = read(loc, prod)
    if t is None:
        return True
    return (re.search(pattern, t) is not None) == want


DOC = {
    "packet-squirrel": "https://documentation.hak5.org/packet-squirrel-mark-ii/packet-squirrel-mark-ii-by-hak5",
    "screen-crab": "https://documentation.hak5.org/screen-crab/master",
    "shark-jack": "https://documentation.hak5.org/shark-jack/master",
    "shark-jack-cable": "https://documentation.hak5.org/shark-jack/getting-started/shark-jack-basics",
    "usb-rubber-ducky": "https://documentation.hak5.org/hak5-usb-rubber-ducky/master",
    "wifi-pineapple-mark7": "https://documentation.hak5.org/wifi-pineapple/master",
}
OLD = {
    "packet-squirrel": "docs.hak5.org/packet-squirrel-mk-ii",
    "screen-crab": "docs.hak5.org/screen-crab",
    "shark-jack": "docs.hak5.org/shark-jack",
    "shark-jack-cable": "docs.hak5.org/shark-jack",
    "usb-rubber-ducky": "docs.hak5.org/hak5-usb-rubber-ducky",
    "wifi-pineapple-mark7": "docs.hak5.org/wifi-pineapple/",
}
for loc in LOCALES:
    for prod, url in DOC.items():
        if read(loc, prod) is None:
            continue
        # de/fr pages have no docs table; only forbid old URL there
        t = read(loc, prod)
        if "Official Documentation" in t or "docs.hak5.org" in t or "documentation.hak5.org" in t or loc not in ("de", "fr"):
            check(f"{loc}/{prod}: new doc url", url in t)
        check(f"{loc}/{prod}: old doc url gone", OLD[prod] not in t)

    # hub
    hub = read(loc)
    check(f"{loc}/hub: omg-unblocker href lowercase",
          f'href="/{loc}/products/hak5/omg-unblocker/"' in hub and f'href="/{loc}/products/hak5/omg-unBlocker/"' not in hub)

    # shark-jack
    t = read(loc, "shark-jack")
    check(f"{loc}/shark-jack: no metasploit/curl", not re.search(r"metasploit|curl", t, re.I))
    if loc in ("de", "fr"):
        check(f"{loc}/shark-jack: no BashBunny claim", "BashBunny" not in t)
        check(f"{loc}/shark-jack-cable: no BashBunny/direct laptop claim",
              "BashBunny" not in read(loc, "shark-jack-cable"))

    # enterprise
    t = read(loc, "wifi-pineapple-enterprise")
    check(f"{loc}/enterprise: no PtaaS/Cobalt", not re.search(r"PtaaS|Cobalt|Pentest as a Service", t))
    if "downloads.hak5.org" in t:
        check(f"{loc}/enterprise: download ent1", "downloads.hak5.org/pineapple/ent1" in t and "pineapple/enterprise" not in t)
    if loc in ("de", "fr"):
        check(f"{loc}/enterprise: no antenna/OpenWRT claim",
              not re.search(r"Antennendesign|antenne améliorée|d'antenne améliorée|OpenWRT", t))

    # ducky
    t = read(loc, "usb-rubber-ducky")
    check(f"{loc}/ducky: no AT32UC3B1256 MCU", "AT32UC3B1256" not in t)
    check(f"{loc}/ducky: storage mentions MicroSD", "MicroSD" in t)
    check(f"{loc}/ducky: no 'no MicroSD' claim",
          not re.search(r"无需 MicroSD|無需 MicroSD|MicroSD不要|لا يحتاج MicroSD|sin necesidad de MicroSD|sem necessidade de MicroSD|MicroSD не требуется|no MicroSD required", t))
    if loc in ("de", "fr"):
        check(f"{loc}/ducky: interface USB-A + USB-C", "USB-A + USB-C" in t)
        check(f"{loc}/ducky: no 1000 keystrokes claim", not re.search(r"1\.000 Tastenanschl|1 000 frappes", t))

    # screen-crab
    t = read(loc, "screen-crab")
    check(f"{loc}/screen-crab: no 'world's first'",
          not re.search(r"world's first|世界首款|世界初|أول جهاز|Primer dispositivo|Primeiro dispositivo|Первое в мире|Primer|Primeiro", t))
    if loc in ("de", "fr"):
        check(f"{loc}/screen-crab: no video injection", not re.search(r"Videoinjektion|injection vidéo", t))

    # plunder-bug
    if loc in ("de", "fr"):
        t = read(loc, "plunder-bug")
        check(f"{loc}/plunder-bug: USB-C not Micro-B", "USB-C" in t and "Micro-B" not in t)
        check(f"{loc}/plunder-bug: no passive-only claim", not re.search(r"Passiv \(kein|Passif \(aucun|passiver Ethernet-Tap|tap Ethernet passif", t))
        t = read(loc, "packet-squirrel")
        check(f"{loc}/packet-squirrel: WireGuard present, no proxy claim",
              "WireGuard" in t and not re.search(r"Transparenter Proxy|proxy transparent", t))
        t = read(loc, "shark-jack-cable")
        check(f"{loc}/shark-jack-cable: no USB-C-cable-to-laptop claim",
              not re.search(r"USB-C-Kabelformfaktor|facteur de forme de câble USB-C", t))
        t = read(loc, "wifi-pineapple-mark7")
        check(f"{loc}/mark7: no MT7628AN/AR9331/detachable-antenna", not re.search(r"MT7628AN|AR9331|RP-SMA", t))

    # disclaimer (Legal Use Disclaimer merged)
    for prod in ["packet-squirrel", "plunder-bug", "screen-crab", "shark-jack", "shark-jack-cable",
                 "usb-rubber-ducky", "wifi-pineapple-enterprise", "wifi-pineapple-mark7"]:
        check(f"{loc}/{prod}: disclaimer alert", has(loc, prod, '{{< alert "warning" >}}'))

fails = [n for n, ok in results if not ok]
print(f"\nTOTAL {len(results)}  FAIL {len(fails)}")
sys.exit(1 if fails else 0)
