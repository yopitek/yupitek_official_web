#!/usr/bin/env python3
"""Fix HAK5 _index.md for ja — add all missing product cards."""

import re

BASE = "/home/yopitek/Project/yupitek_official_web"

EN_PRODUCTS_ORDER = [
    "wifi-pineapple-mark7", "wifi-pineapple-enterprise", "usb-rubber-ducky",
    "bash-bunny", "shark-jack", "key-croc", "packet-squirrel",
    "omg-cable", "omg-plug", "omg-adapter", "omg-programmer", "omg-unBlocker",
    "malicious-cable-detector", "screen-crab", "plunder-bug",
    "wifi-pineapple-pager", "shark-jack-cable"
]

JA_CARDS = {
    "wifi-pineapple-enterprise": {
        "title": "WiFi Pineapple Enterprise",
        "image": "/images/products/hak5/wifi-pineapple-enterprise.png",
        "desc": "エンタープライズ向け無線ネットワーク監査プラットフォーム、強化アンテナ設計で大規模セキュリティ評価に対応。",
    },
    "key-croc": {
        "title": "Key Croc",
        "image": "/images/products/hak5/key-croc.png",
        "desc": "キーロガー兼HIDインジェクションツール、Wi-Fi内蔵でリモートアクセス可能。",
    },
    "omg-plug": {
        "title": "O.MG Plug",
        "image": "/images/products/hak5/omg-plug.png",
        "desc": "充電ヘッドに偽装したO.MGデバイス、リモート制御機能付き。",
    },
    "omg-adapter": {
        "title": "O.MG Adapter",
        "image": "/images/products/hak5/omg-adapter.png",
        "desc": "USBアダプター形状のO.MGデバイス、ターゲット機器へ容易に接続可能。",
    },
    "omg-programmer": {
        "title": "O.MG Programmer",
        "image": "/images/products/hak5/omg-programmer.png",
        "desc": "O.MG Cable専用プログラマー — DuckyScriptファームウェアのフラッシュに使用。",
    },
    "omg-unBlocker": {
        "title": "O.MG UnBlocker",
        "image": "/images/products/hak5/omg-unBlocker.png",
        "desc": "USB データブロッカーを回避 — 充電専用ケーブルソリューションの正当なテストに使用。",
    },
    "malicious-cable-detector": {
        "title": "Malicious Cable Detector",
        "image": "/images/products/hak5/malicious-cable-detector.png",
        "desc": "偽装悪意あるケーブル検出スキャナー、O.MGタイプのデバイス識別を支援。",
    },
    "shark-jack-cable": {
        "title": "Shark Jack Cable",
        "image": "/images/products/hak5/shark-jack-cable.png",
        "desc": "ネットワークポートへの直接接続用Shark Jackのケーブル版。",
    },
}

lang = "ja"
path = f"{BASE}/content/{lang}/products/hak5/_index.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find existing slugs
existing = set(re.findall(rf'href="/{lang}/products/hak5/([^/"]+)/', content))
missing_slugs = [s for s in EN_PRODUCTS_ORDER if s not in existing and s in JA_CARDS]

print(f"ja existing: {sorted(existing)}")
print(f"ja missing:  {missing_slugs}")

if not missing_slugs:
    print("ja: already complete")
else:
    new_cards_lines = []
    for slug in missing_slugs:
        c = JA_CARDS[slug]
        new_cards_lines.append(
            f'  {{{{< card title="{c["title"]}" href="/{lang}/products/hak5/{slug}/" image="{c["image"]}" >}}}}\n'
            f'    {c["desc"]}\n'
            f'  {{{{< /card >}}}}'
        )
    new_block = "\n".join(new_cards_lines)
    content = content.replace(
        "{{< /card-group >}}",
        new_block + "\n{{< /card-group >}}"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("ja: wrote updated file ✓")

print("Done!")
