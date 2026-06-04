#!/usr/bin/env python3
"""Sync remaining 2 MSI RTX 5080 graphic card products to 7 language versions."""

import os
import re

BASE = "/home/yopitek/Project/yupitek_official_web"

LANG_DATA = {
    "ja": {
        "inspire_desc": "MSI INSPIRE — クリエイティブな美学とパフォーマンス、 Redmond と視覚的魅力の両立。",
        "suprim_desc": "MSI SUPRIM LIQUID — 一体型水冷フラッグシップモデル、極限のオーバークロック向け。"
    },
    "ar": {
        "inspire_desc": "MSI INSPIRE — جماليات إبداعية مع الأداء والجاذبية البصرية.",
        "suprim_desc": "MSI SUPRIM LIQUID — نظام تبريد مائي متكامل ومغلق لكسر سرعة المعالج القصوى."
    },
    "es": {
        "inspire_desc": "MSI INSPIRE — estética creativa con rendimiento y atractivo visual.",
        "suprim_desc": "MSI SUPRIM LIQUID — refrigeración líquida todo en uno premium para overclocking extremo."
    },
    "pt": {
        "inspire_desc": "MSI INSPIRE — estética criativa com desempenho e apelo visual.",
        "suprim_desc": "MSI SUPRIM LIQUID — refrigeração líquida multifuncional premium para overclocking extremo."
    },
    "ru": {
        "inspire_desc": "MSI INSPIRE — креативная эстетика в сочетании с высокой производительностью.",
        "suprim_desc": "MSI SUPRIM LIQUID — флагманская система жидкостного охлаждения \"все в одном\" для экстремального разгона."
    },
    "de": {
        "inspire_desc": "MSI INSPIRE — kreative Ästhetik vereint mit Leistung und visuellem Design.",
        "suprim_desc": "MSI SUPRIM LIQUID — All-in-One-Wasserkühlungs-Flaggschiff für extremes Übertakten."
    },
    "fr": {
        "inspire_desc": "MSI INSPIRE — une esthétique créative alliant performance et design visuel.",
        "suprim_desc": "MSI SUPRIM LIQUID — le fleuron du refroidissement liquide tout-en-un pour l'overclocking extrême."
    }
}

# Wait, check for 'Redmond' in ja. That was a typo. Let's make it:
LANG_DATA["ja"]["inspire_desc"] = "MSI INSPIRE — クリエイティブな美学とパフォーマンス、そして視覚的魅力の両立。"

for lang, data in LANG_DATA.items():
    path = f"{BASE}/content/{lang}/products/graphiccard/_index.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # If the missing card is already there, skip
    if "msi-rtx5080-inspire-3x-oc" in content:
        print(f"{lang}: already has inspire card, skipping")
        continue

    # We can match:
    # (msi-rtx5080-ventus-3x-oc-white.*?\{\{<\s*/card\s*>\}\}\s*)\{\{<\s*/card-group\s*>\}\}
    pattern = re.compile(
        r'(msi-rtx5080-ventus-3x-oc-white.*?\{\{<\s*/card\s*>\}\}\s*)\{\{<\s*/card-group\s*>\}}',
        re.DOTALL
    )

    new_cards = (
        f'  {{{{< card title="MSI RTX5080 16G INSPIRE 3X OC" href="/{lang}/products/graphiccard/msi-rtx5080-inspire-3x-oc/" image="/images/products/graphiccard/msi-rtx5080-inspire-3x-oc.png" >}}}}\n'
        f'    {data["inspire_desc"]}\n'
        f'  {{{{< /card >}}}}\n'
        f'  {{{{< card title="MSI RTX5080 16G SUPRIM LIQUID SOC" href="/{lang}/products/graphiccard/msi-rtx5080-suprim-liquid-soc/" image="/images/products/graphiccard/msi-rtx5080-suprim-liquid-soc.png" >}}}}\n'
        f'    {data["suprim_desc"]}\n'
        f'  {{{{< /card >}}}}\n'
    )

    replacement = r'\1' + new_cards + '{{< /card-group >}}'
    
    new_content, count = pattern.subn(replacement, content)
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"{lang}: successfully added 2 MSI cards ✓")
    else:
        print(f"Error: Could not find ventus-3x-oc-white pattern in {lang} file.")

print("Sync completed.")
