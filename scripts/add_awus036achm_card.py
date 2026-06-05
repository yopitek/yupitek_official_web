#!/usr/bin/env python3
import os
import re

# Localized descriptions for AWUS036ACHM
DESCRIPTIONS = {
    "en": "AC433 dual-band, MediaTek MT7610U chipset, USB 2.0, single high-gain antenna, compact design — ideal for portable pentesting.",
    "zh-tw": "AC433 雙頻，MediaTek MT7610U 晶片，USB 2.0，單天線輕巧設計 — 適合隨身攜帶與滲透測試。",
    "zh-cn": "AC433 双频，MediaTek MT7610U 芯片，USB 2.0，单天线轻巧设计 — 适合随身携带与渗透测试。",
    "ja": "AC433 デュアルバンド、MediaTek MT7610U チップセット、USB 2.0、シングルアンテナのコンパクト設計 — ポータブルなペネトレーションテストに最適。",
    "ar": "AC433 ثنائي النطاق، شريحة MediaTek MT7610U، منفذ USB 2.0، تصميم مدمج بهوائي فردي — مثالي لاختبار الاختراق المحمول.",
    "de": "AC433 Dual-Band, MediaTek MT7610U Chipsatz, USB 2.0, kompaktes Design mit Einzelantenne — ideal für mobiles Pentesting.",
    "es": "AC433 de doble banda, chipset MediaTek MT7610U, USB 2.0, diseño compacto con antena única — ideal para pentesting portátil.",
    "fr": "AC433 double bande, chipset MediaTek MT7610U, USB 2.0, conception compacte avec antenne unique — idéal pour le pentesting portable.",
    "pt": "AC433 banda dupla, chipset MediaTek MT7610U, USB 2.0, design compacto com antena única — ideal para pentesting portátil.",
    "ru": "AC433 двухдиапазонный, чипсет MediaTek MT7610U, USB 2.0, компактный дизайн с одной антенной — идеально для портативного пентестинга."
}

def add_card_to_file(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the card is already present
    if "awus036achm" in content.lower():
        print(f"AWUS036ACHM already exists in {filepath}")
        return False

    # Find the ### Wi-Fi 5 section and its card group
    pattern = re.compile(r'(### Wi-Fi 5\s*\n\s*\{\{<\s*card-group\s*>\}\}\s*\n)(.*?)(\{\{<\s*/\s*card-group\s*>\}\})', re.DOTALL)
    match = pattern.search(content)
    if not match:
        print(f"Could not find Wi-Fi 5 card group in {filepath}")
        return False
        
    prefix = match.group(1)
    inner_cards = match.group(2)
    suffix = match.group(3)
    
    # Let's insert AWUS036ACHM card right after AWUS036ACH card.
    # Typically, the cards look like:
    #   {{< card title="AWUS036ACH" href="/{lang}/products/alfa/awus036ach/" image="/images/products/alfa/awus036ach.png" >}}
    #     ...
    #   {{< /card >}}
    ach_pattern = re.compile(r'(\{\{<\s*card\s+title="AWUS036ACH".*?\{\{<\s*/\s*card\s*>\}\}\n?)', re.DOTALL)
    ach_match = ach_pattern.search(inner_cards)
    
    new_card = f'  {{{{< card title="AWUS036ACHM" href="/{lang}/products/alfa/awus036achm/" image="/images/products/alfa/awus036achm.png" >}}}}\n    {DESCRIPTIONS[lang]}\n  {{{{< /card >}}}}\n'
    
    if ach_match:
        # Insert after AWUS036ACH
        insert_pos = ach_match.end()
        new_inner = inner_cards[:insert_pos] + new_card + inner_cards[insert_pos:]
    else:
        # Fallback: prepend to the card group
        new_inner = new_card + inner_cards

    # Reconstruct content
    new_block = prefix + new_inner + suffix
    new_content = content.replace(match.group(0), new_block, 1)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Added card to {filepath}")
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    languages = ["zh-tw", "zh-cn", "en", "ja", "ar", "de", "es", "fr", "pt", "ru"]
    count = 0
    
    for lang in languages:
        filepath = os.path.join(content_dir, lang, "products", "alfa", "_index.md")
        if os.path.exists(filepath):
            if add_card_to_file(filepath, lang):
                count += 1
        else:
            print(f"File not found: {filepath}")
            
    print(f"\nDone! Added card to {count} files.")

if __name__ == "__main__":
    main()
