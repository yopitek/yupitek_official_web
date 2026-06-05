#!/usr/bin/env python3
import os

def cache_bust_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    
    # Replace topology image reference
    old_topo = "/images/products/ibeacon/ibeacon_topology.png"
    new_topo = "/images/products/ibeacon/ibeacon_topology.png?v=2"
    if old_topo in content and new_topo not in content:
        content = content.replace(old_topo, new_topo)
        modified = True
        
    # Replace comparison image reference
    old_comp = "/images/products/ibeacon/ibeacon_comparison.png"
    new_comp = "/images/products/ibeacon/ibeacon_comparison.png?v=2"
    if old_comp in content and new_comp not in content:
        content = content.replace(old_comp, new_comp)
        modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Cache-busted: {filepath}")
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    languages = ["zh-tw", "zh-cn", "en", "ja", "ar", "de", "es", "fr", "pt", "ru"]
    count = 0
    
    for lang in languages:
        filepath = os.path.join(content_dir, lang, "products", "ibeacon", "_index.md")
        if os.path.exists(filepath):
            if cache_bust_file(filepath):
                count += 1
                
    print(f"\nCompleted cache-busting for {count} files.")

if __name__ == "__main__":
    main()
