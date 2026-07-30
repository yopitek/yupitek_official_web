#!/usr/bin/env python3
"""Replace source.sierrawireless.com spec links with local /docs/sierra/ PDF links
in all 10 locale blog files for sierra-wireless-selections."""

import os

BASE = "/home/yopitek/Project/yupitek_official_web/content"
LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
FILE = "blog/sierra-wireless-selections/_index.md"

REPLACEMENTS = {
    # EM7430
    "https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/":
        "https://yupitek.com/docs/sierra/em7430_spec.pdf",
    # EM7455
    "https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/":
        "https://yupitek.com/docs/sierra/em7455_spec.pdf",
    # EM7511
    "https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/":
        "https://yupitek.com/docs/sierra/EM7511_spec.pdf",
    # EM7565
    "https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/":
        "https://yupitek.com/docs/sierra/EM7565_spec.pdf",
    # EM9190 / EM9191 (combined)
    "https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/":
        "https://yupitek.com/docs/sierra/EM919x.pdf",
    # MC7304
    "https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/":
        "https://yupitek.com/docs/sierra/MC7304_spec.pdf",
    # MC7455
    "https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/":
        "https://yupitek.com/docs/sierra/mc7455_spec.pdf",
}

total_replaced = 0
total_files = 0

for locale in LOCALES:
    filepath = os.path.join(BASE, locale, FILE)
    if not os.path.exists(filepath):
        print(f"⚠️  MISSING: {filepath}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    count = 0
    for old_url, new_url in REPLACEMENTS.items():
        if old_url in content:
            content = content.replace(old_url, new_url)
            count += 1
        else:
            print(f"  ⚠️  Not found in {locale}: {old_url[:60]}...")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    total_files += 1
    total_replaced += count
    print(f"  ✅ {locale}: {count} URLs replaced")

print(f"\n✅ Done: {total_files} files, {total_replaced} URLs replaced")
