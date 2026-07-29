import os
import re
import shutil
from translation_dataset import LOCALES

BASE_DIR = "/home/yopitek/Documents/Obsidian_vault/GX10_HQ/05_SW/yupitek_official_web/content"
ZH_TW_DIR = os.path.join(BASE_DIR, "zh-tw/products/sierra")

PRODUCTS = ["em7430", "em7455", "em7511", "em7565", "em9190", "em9191", "mc7304", "mc7350", "mc7354", "mc7455"]

def generate_overview_page(loc):
    cfg = LOCALES[loc]
    is_rtl = (loc == 'ar')
    rtl_frontmatter = 'dir: "rtl"\n' if is_rtl else ''

    content = f"""---
title: "Sierra Wireless {cfg['title_suffix']}"
description: "{cfg['description']}"
date: 2026-07-29
draft: false
showBreadcrumbs: true
showTableOfContents: false
showChildPages: false
{rtl_frontmatter}featureimage: "/images/products/sierra/EM9190-5G.png"
---

{cfg['intro']}

---

## {cfg['product_series']}

### {cfg['cat_5g']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM9190" href="/{loc}/products/sierra/em9190/" image="/images/products/sierra/EM9190-5G.png" >}}}}
    5G NR Sub-6 + mmWave, 5.5 Gbps Down / 3 Gbps Up, M.2 3042, Snapdragon X55, SA/NSA & CBRS.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM9191" href="/{loc}/products/sierra/em9191/" image="/images/products/sierra/EM9191-5G.png" >}}}}
    5G NR Sub-6, 4.5 Gbps Down, M.2 3042, Snapdragon X55, Global Bands, -40°C~+85°C.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat12']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM7511" href="/{loc}/products/sierra/em7511/" image="/images/products/sierra/EM7511.png" >}}}}
    4G LTE Cat 12 Americas, 600 Mbps / 150 Mbps, M.2 3042, FirstNet Band 14, CBRS & LAA.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM7565" href="/{loc}/products/sierra/em7565/" image="/images/products/sierra/EM7565.png" >}}}}
    4G LTE Cat 12 Global, 600 Mbps, M.2 3042, 24+ Global LTE Bands, CBRS & LAA.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat6']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless EM7430" href="/{loc}/products/sierra/em7430/" image="/images/products/sierra/EM7430.png" >}}}}
    4G LTE Cat 6 APAC, 300 Mbps / 50 Mbps, M.2 3042, Qualcomm MDM9230.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless EM7455" href="/{loc}/products/sierra/em7455/" image="/images/products/sierra/EM7455.png" >}}}}
    4G LTE Cat 6 Americas/EMEA, 300 Mbps, M.2 3042, Qualcomm MDM9230.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7455" href="/{loc}/products/sierra/mc7455/" image="/images/products/sierra/MC7455.png" >}}}}
    4G LTE Cat 6 Mini PCIe, 300 Mbps, Americas/EMEA.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

### {cfg['cat_cat3']}

{{{{< card-group >}}}}
  {{{{< card title="Sierra Wireless MC7304" href="/{loc}/products/sierra/mc7304/" image="/images/products/sierra/MC7304.png" >}}}}
    4G LTE Cat 3 EMEA/APAC, 100 Mbps / 50 Mbps, Mini PCIe, 3G/2G Fallback.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7350" href="/{loc}/products/sierra/mc7350/" image="/images/products/sierra/MC7350.png" >}}}}
    4G LTE Cat 3 North America AT&T, Mini PCIe, 100 Mbps, Qualcomm MDM9215.
  {{{{< /card >}}}}
  {{{{< card title="Sierra Wireless MC7354" href="/{loc}/products/sierra/mc7354/" image="/images/products/sierra/MC7354.png" >}}}}
    4G LTE Cat 3 North America Multi-carrier (Verizon/Sprint/AT&T), Mini PCIe, 100 Mbps.
  {{{{< /card >}}}}
{{{{< /card-group >}}}}

---

## {cfg['spec_table_title']}

| {cfg['headers'][0]} | {cfg['headers'][1]} | {cfg['headers'][2]} | {cfg['headers'][3]} | {cfg['headers'][4]} | {cfg['headers'][5]} | {cfg['headers'][6]} | {cfg['headers'][7]} |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **EM9190** | 5G NR / 4G LTE | 5G Sub-6 + mmWave | 5.5 Gbps / 3.0 Gbps | M.2 3042 | {cfg['labels']['global_mkt']} | n1/2/3/5/7/8/12/20/28/41/48/77/78/79, mmWave (n257-n261), CBRS | L1+L5 Dual-Band GNSS |
| **EM9191** | 5G NR / 4G LTE | 5G Sub-6 | 4.5 Gbps / 660 Mbps | M.2 3042 | {cfg['labels']['global_mkt']} | n1/2/3/5/7/8/12/20/28/41/48/77/78/79, CBRS, SA/NSA | Multi-constellation |
| **EM7511** | 4G LTE-A Pro / 3G | LTE Cat 12 | 600 Mbps / 150 Mbps | M.2 3042 | {cfg['labels']['americas_mkt']} | B1-B14, B18-B20, B26, B29, B30, B32, B41-B43, B46(LAA), B48(CBRS), Band 14 FirstNet | GPS/GLONASS/Beidou/Galileo |
| **EM7565** | 4G LTE-A Pro / 3G | LTE Cat 12 | 600 Mbps / 150 Mbps | M.2 3042 | {cfg['labels']['global_mkt']} | B1-B9, B12, B13, B18-B20, B26, B28-B30, B32, B41-B43, B46(LAA), B48(CBRS), B66 | GPS/GLONASS/Beidou/Galileo |
| **EM7430** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | M.2 3042 | {cfg['labels']['apac_mkt']} | B1, B3, B5, B7, B8, B18, B19, B21, B28, B38, B39, B40, B41 | GPS/GLONASS/Beidou/Galileo |
| **EM7455** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | M.2 3042 | {cfg['labels']['emea_mkt']} | B1-B5, B7, B8, B12, B13, B20, B25, B26, B29, B30, B41 | GPS/GLONASS/Beidou/Galileo |
| **MC7455** | 4G LTE-A / 3G | LTE Cat 6 | 300 Mbps / 50 Mbps | Mini PCIe | {cfg['labels']['emea_mkt']} | B1-B5, B7, B8, B12, B13, B20, B25, B26, B29, B30, B41 | GPS/GLONASS/Beidou/Galileo |
| **MC7304** | 4G LTE / 3G / 2G | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | {cfg['labels']['emea_mkt']} | B1, B3, B7, B8, B20 (3G/2G Fallback) | Standalone GPS / GLONASS |
| **MC7350** | 4G LTE / 3G | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | North America (AT&T) | B2, B4, B5, B17, B25 | Standalone GPS / GLONASS |
| **MC7354** | 4G LTE / 3G / CDMA | LTE Cat 3 | 100 Mbps / 50 Mbps | Mini PCIe | North America Multi-carrier | B2, B4, B5, B13, B17, B25, EV-DO Rev A / CDMA | Standalone GPS / GLONASS |

---

## {cfg['drivers_title']}

{cfg['drivers_desc']}

---

<div class="mt-6 text-center">
  <a href="/{loc}/contact/" class="btn-inquiry">{cfg['cta_btn']}</a>
</div>

{{{{< alert >}}}}
{cfg['alert_msg']}
{{{{< /alert >}}}}
"""
    target_path = os.path.join(BASE_DIR, loc, "products/sierra/_index.md")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_product_page(loc, p):
    cfg = LOCALES[loc]
    is_rtl = (loc == 'ar')
    rtl_frontmatter = 'dir: "rtl"\n' if is_rtl else ''

    # Load zh-tw template to preserve specs tables & tech values
    zh_path = os.path.join(ZH_TW_DIR, p, "_index.md")
    with open(zh_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Translate section headers
    src = src.replace("## 產品概述", f"## {cfg['labels']['overview']}")
    src = src.replace("## 產品特色", f"## {cfg['labels']['features']}")
    src = src.replace("## 技術規格", f"## {cfg['labels']['tech_specs']}")
    src = src.replace("## 作業系統與驅動支援", f"## {cfg['labels']['os_support']}")
    src = src.replace("## 資源與文件下載", f"## {cfg['labels']['docs']}")

    src = src.replace("| 項目 | 規格細節 |", f"| {cfg['labels']['item']} | {cfg['labels']['details']} |")
    src = src.replace("**製造商**", f"**{cfg['labels']['manufacturer']}**")
    src = src.replace("**產品型號**", f"**{cfg['labels']['model']}**")
    src = src.replace("**蜂窩技術**", f"**{cfg['labels']['tech']}**")
    src = src.replace("**核心晶片組**", f"**{cfg['labels']['chipset']}**")
    src = src.replace("**最高下載 / 上傳速率**", f"**{cfg['labels']['max_speed']}**")
    src = src.replace("**LTE 頻段**", f"**{cfg['labels']['lte_bands']}**")
    src = src.replace("**外型尺寸**", f"**{cfg['labels']['form_factor']}**")
    src = src.replace("**主機介面**", f"**{cfg['labels']['interfaces']}**")
    src = src.replace("**SIM 卡介面**", f"**{cfg['labels']['sim']}**")
    src = src.replace("**作業溫度**", f"**{cfg['labels']['temp']}**")

    # Replace alert message
    src = re.sub(r'\{\{< alert >\}\}[\s\S]*?\{\{< /alert >\}\}', f"{{{{< alert >}}}}\n{cfg['alert_msg']}\n{{{{< /alert >}}}}", src)

    if is_rtl:
        src = src.replace("showTableOfContents: true\n", "showTableOfContents: true\ndir: \"rtl\"\n")

    target_path = os.path.join(BASE_DIR, loc, f"products/sierra/{p}/_index.md")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(src)

def main():
    for loc in LOCALES:
        print(f"Generating locale: {loc}...")
        generate_overview_page(loc)
        for p in PRODUCTS:
            generate_product_page(loc, p)
    print("All locales generated successfully!")

if __name__ == "__main__":
    main()
