#!/usr/bin/env python3
import os

REPLACEMENTS = {
    "zh-tw": [
        (
            "它使用 **4 × AA (三號) 乾電池** 供電（總容量達 5800mAh），在預設參數下可提供長達 **10 年** 的超長續航力。",
            "它使用 **4 × AA (三號) 乾電池** 供電（總容量達 5800mAh）。"
        ),
        (
            "* **10年免維護壽命：** 採用四顆標準可更換的三號電池，超大 5800mAh 電量讓維護成本降至最低。",
            "* **低維護成本：** 採用四顆標準可更換的三號電池，超大 5800mAh 電量讓維護成本降至最低。"
        ),
        (
            "| **電池壽命** | 最長可達 10 年 (預設參數下) | 基於預設廣播參數 |\n",
            ""
        )
    ],
    "zh-cn": [
        (
            "它使用 **4 × AA (三号) 干电池** 供电（总容量达 5800mAh），在默认参数下可提供长达 **10 年** 的超长续航力。",
            "它使用 **4 × AA (三号) 干电池** 供电（总容量达 5800mAh）。"
        ),
        (
            "* **10年免维护寿命：** 采用四颗标准可更换的三号电池，超大 5800mAh 电量让维护成本降至最低。",
            "* **低维护成本：** 采用四颗标准可更换的三号电池，超大 5800mAh 电量让维护成本降至最低。"
        ),
        (
            "| **电池寿命** | 最长可达 10 年 (默认参数下) | 基于默认广播参数 |\n",
            ""
        )
    ],
    "en": [
        (
            "description: \"YPB03 Long-Range Max Beacon broadcasting LINE Simple Beacon packets. Features up to 10 years battery life, 240m range, IP65 waterproof casing, and seamless LINE Bot Messaging API integration.\"",
            "description: \"YPB03 Long-Range Max Beacon broadcasting LINE Simple Beacon packets. Features 240m range, IP65 waterproof casing, and seamless LINE Bot Messaging API integration.\""
        ),
        (
            "Powered by **4 × AA batteries** providing a massive 5800mAh capacity, it boasts an exceptional battery lifetime of **up to 10 years** under default broadcasting parameters.",
            "Powered by **4 × AA batteries** providing a massive 5800mAh capacity."
        ),
        (
            "* **10-Year Service Life:** Massive 5800mAh capacity using four standard replaceable AA batteries reduces hardware maintenance overhead to near-zero.",
            "* **Low Maintenance:** Massive 5800mAh capacity using four standard replaceable AA batteries reduces hardware maintenance overhead to near-zero."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "de": [
        (
            "Betrieben mit **4 × AA-Batterien** (5800mAh), erreicht er eine Lebensdauer von **bis zu 10 Jahren**.",
            "Betrieben mit **4 × AA-Batterien** (5800mAh)."
        ),
        (
            "* **10 Jahre Batterielaufzeit:** Große 5800mAh Kapazität mit vier Standard-AA-Batterien reduziert den Wartungsaufwand.",
            "* **Geringer Wartungsaufwand:** Große 5800mAh Kapazität mit vier Standard-AA-Batterien reduziert den Wartungsaufwand."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "fr": [
        (
            "Elle fonctionne avec **4 piles AA** (5800mAh), lui offrant une autonomie allant **jusqu'à 10 ans**.",
            "Elle fonctionne avec **4 piles AA** (5800mAh)."
        ),
        (
            "* **10 ans d'autonomie:** Fonctionne avec 4 piles AA standards pour réduire la maintenance.",
            "* **Maintenance réduite:** Fonctionne avec 4 piles AA standards pour réduire la maintenance."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "es": [
        (
            "Funciona con **4 pilas AA** (5800mAh), alcanzando una vida útil de **hasta 10 años**.",
            "Funciona con **4 pilas AA** (5800mAh)."
        ),
        (
            "* **10 años de autonomía:** Utiliza 4 pilas AA comunes que minimizan el costo de mantenimiento.",
            "* **Bajo mantenimiento:** Utiliza 4 pilas AA comunes que minimizan el costo de mantenimiento."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "pt": [
        (
            "Ele funciona com **4 pilhas AA** (5800mAh), garantindo durabilidade de **até 10 anos**.",
            "Ele funciona com **4 pilhas AA** (5800mAh)."
        ),
        (
            "* **10 anos de autonomia:** Usa 4 pilhas AA comuns que diminuem custos de manutenção.",
            "* **Baixo custo de manutenção:** Usa 4 pilhas AA comuns que diminuem custos de manutenção."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "ru": [
        (
            "Работает от **4 батареек AA** (5800 мАч), обеспечивающих работу **до 10 лет**.",
            "Работает от **4 батареек AA** (5800 мАч)."
        ),
        (
            "* **10 лет автономной работы:** Питание от 4 обычных пальчиковых батареек минимизирует затраты на обслуживание.",
            "* **Простота обслуживания:** Питание от 4 обычных пальчиковых батареек минимизирует затраты на обслуживание."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "ja": [
        (
            "**単3乾電池×4本**（計 5800mAh）で駆動し、デフォルトの設定で **最大10年間** という圧倒的なバッテリー寿命を実現しています。",
            "**単3乾電池×4本**（計 5800mAh）で駆動します。"
        ),
        (
            "* **10年間のメンテナンスフリー:** 入手性の高い単3乾電池4本で駆動。5800mAh の大容量により、頻繁な電池交換コストを削減します。",
            "* **優れたメンテナンス性:** 入手性の高い単3乾電池4本で駆動。5800mAh の大容量により、頻繁な電池交換コストを削減します。"
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ],
    "ar": [
        (
            "تعمل بـ **4 بطاريات AA** بسعة 5800 مللي أمبير، وتتميز بعمر بطارية يصل إلى **10 سنوات**。",
            "تعمل بـ **4 بطاريات AA** بسعة 5800 مللي أمبير。"
        ),
        (
            "وتتميز بعمر بطارية يصل إلى **10 سنوات**.",
            ""
        ),
        (
            "* **عمر بطارية 10 سنوات:** سعة 5800 مللي أمبير باستخدام 4 بطاريات AA شائعة يقلل الصيانة.",
            "* **صيانة منخفضة:** سعة 5800 مللي أمبير باستخدام 4 بطاريات AA شائعة يقلل الصيانة."
        ),
        (
            "| **Battery Lifetime** | Up to 10 years | Based on default broadcasting parameters |\n",
            ""
        )
    ]
}

def clean_file(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    
    # Process custom replacements for the language
    for old, new in REPLACEMENTS[lang]:
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    # Also do standard search and replace just in case of formatting variants
    # Remove specs table row if it is still there
    for row_start in ["| **Battery Lifetime**", "| **電池壽命**", "| **电池寿命**"]:
        if row_start in content:
            lines = content.splitlines(keepends=True)
            new_lines = [l for l in lines if not l.startswith(row_start)]
            content = "".join(new_lines)
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Cleaned YPB03 battery life text from {filepath}")
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    languages = ["zh-tw", "zh-cn", "en", "ja", "ar", "de", "es", "fr", "pt", "ru"]
    count = 0
    
    for lang in languages:
        filepath = os.path.join(content_dir, lang, "products", "ibeacon", "ypb03", "_index.md")
        if os.path.exists(filepath):
            if clean_file(filepath, lang):
                count += 1
        else:
            print(f"File not found: {filepath}")
            
    print(f"\nDone! Cleaned battery life references from {count} files.")

if __name__ == "__main__":
    main()
