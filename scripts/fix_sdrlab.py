#!/usr/bin/env python3
"""Fix SDRLab _index.md for ar, es, pt, ru, ja — add all missing product cards."""

import re

BASE = "/home/yopitek/Project/yupitek_official_web"

EN_PRODUCTS_ORDER = [
    "rtl-sdr-v4", "trx-duo", "h4m", "flipper-5g", "flipper-nrf24",
    "flipper-wifi-multiboard", "flipper-ethernet"
]

CARDS = {
    "h4m": {
        "title": "SDRLab H4M",
        "image": "/images/products/sdrlab/h4m.png",
        "ar": "وحدة SDR عالية الأداء من SDRLab لأبحاث الاتصالات اللاسلكية المتقدمة.",
        "es": "Módulo SDR de alto rendimiento de SDRLab para investigación avanzada en comunicaciones inalámbricas.",
        "pt": "Módulo SDR de alto desempenho da SDRLab para pesquisa avançada em comunicações sem fio.",
        "ru": "Высокопроизводительный SDR-модуль от SDRLab для продвинутых исследований беспроводных коммуникаций.",
        "ja": "SDRLab H4M — 高性能SDRモジュール、高度な無線通信研究向け。",
    },
    "flipper-5g": {
        "title": "Flipper Zero 5G Expansion Board",
        "image": "/images/products/sdrlab/flipper-5g.png",
        "ar": "لوحة توسعة RF بنطاق 5G مصممة لـ Flipper Zero.",
        "es": "Placa de expansión RF de banda 5G diseñada para Flipper Zero.",
        "pt": "Placa de expansão RF de banda 5G projetada para Flipper Zero.",
        "ru": "RF-плата расширения диапазона 5G для Flipper Zero.",
        "ja": "Flipper Zero用5GバンドRF拡張ボード。",
    },
    "flipper-wifi-multiboard": {
        "title": "Flipper Zero WiFi Multiboard",
        "image": "/images/products/sdrlab/flipper-wifi-multiboard.png",
        "ar": "لوحة توسعة Wi-Fi متعددة الوظائف لـ Flipper Zero مع وحدة ESP8266.",
        "es": "Placa de expansión Wi-Fi multifunción para Flipper Zero con módulo ESP8266 integrado.",
        "pt": "Placa de expansão Wi-Fi multifuncional para Flipper Zero com módulo ESP8266 integrado.",
        "ru": "Многофункциональная плата расширения Wi-Fi для Flipper Zero с интегрированным модулем ESP8266.",
        "ja": "ESP8266統合Wi-Fi多機能拡張ボード for Flipper Zero。",
    },
    "flipper-ethernet": {
        "title": "Flipper Zero Ethernet Test Module",
        "image": "/images/products/sdrlab/flipper-ethernet.png",
        "ar": "وحدة توسعة اختبار الشبكة السلكية لـ Flipper Zero.",
        "es": "Módulo de expansión de prueba de red cableada para Flipper Zero.",
        "pt": "Módulo de expansão de teste de rede com fio para Flipper Zero.",
        "ru": "Модуль расширения для тестирования проводных сетей для Flipper Zero.",
        "ja": "Flipper Zero用有線ネットワークテスト拡張モジュール。",
    },
}

TARGETS = {
    "ar": ["h4m", "flipper-5g", "flipper-wifi-multiboard", "flipper-ethernet"],
    "es": ["h4m", "flipper-5g", "flipper-wifi-multiboard", "flipper-ethernet"],
    "pt": ["h4m", "flipper-5g", "flipper-wifi-multiboard", "flipper-ethernet"],
    "ru": ["h4m", "flipper-5g", "flipper-wifi-multiboard", "flipper-ethernet"],
    "ja": ["h4m", "flipper-ethernet"],
}


def get_existing_hrefs(content, lang):
    pattern = rf'href="/{lang}/products/sdrlab/([^/"]+)/'
    return set(re.findall(pattern, content))


def build_card(lang, slug):
    c = CARDS[slug]
    desc = c[lang]
    href = f"/{lang}/products/sdrlab/{slug}/"
    return (
        f'  {{{{< card title="{c["title"]}" href="{href}" image="{c["image"]}" >}}}}\n'
        f'    {desc}\n'
        f'  {{{{< /card >}}}}'
    )


for lang, to_add in TARGETS.items():
    path = f"{BASE}/content/{lang}/products/sdrlab/_index.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    existing = get_existing_hrefs(content, lang)
    missing = [s for s in EN_PRODUCTS_ORDER if s in to_add and s not in existing]

    print(f"\n{lang}: existing={sorted(existing)}, adding={missing}")

    if not missing:
        print(f"{lang}: already complete, skipping")
        continue

    new_block = "\n".join(build_card(lang, slug) for slug in missing)
    content = content.replace(
        "{{< /card-group >}}",
        new_block + "\n{{< /card-group >}}"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{lang}: wrote updated file ✓")

print("\nDone!")
