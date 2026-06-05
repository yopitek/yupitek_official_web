#!/usr/bin/env python3
import os
import re

def remove_table_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for the comparison image line:
    # ![iBeacon Series Comparison Matrix](/images/products/ibeacon/ibeacon_comparison.png)
    # followed by the markdown table.
    
    # Let's find the position of the comparison image
    image_pattern = r'!\[[^\]]*\]\(/images/products/ibeacon/ibeacon_comparison\.png\)'
    image_match = re.search(image_pattern, content)
    if not image_match:
        print(f"Comparison image not found in {filepath}")
        return False
        
    image_end_idx = image_match.end()
    
    # The table follows after the image, usually separated by newlines.
    # Let's match any table starting with | and ending before the next section divider "---" or "##"
    table_section = content[image_end_idx:]
    
    # We want to find the first occurrence of a markdown table (lines starting with '|')
    # and remove it up to the next divider.
    # Typically: \n\n| ... | \n| ... | \n ...
    table_pattern = re.compile(r'(\s*\n\s*\|.*?\n\s*\|[-:| ]+\|\s*\n(?:^\s*\|.*?\n)+)', re.MULTILINE)
    table_match = table_pattern.search(table_section)
    
    if not table_match:
        # Fallback check: look for any lines starting with '|' and remove them
        # until a line that does not start with '|'
        lines = table_section.splitlines(keepends=True)
        table_start = -1
        table_end = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('|'):
                if table_start == -1:
                    table_start = i
                table_end = i + 1
            elif table_start != -1:
                # Table ended
                break
                
        if table_start != -1:
            # We found the table lines. Let's remove them.
            # Also remove preceding empty lines if any.
            new_lines = lines[:table_start] + lines[table_end:]
            # Clean up double newlines right before separator
            new_table_section = "".join(new_lines)
            new_content = content[:image_end_idx] + new_table_section
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully removed table (fallback method) from {filepath}")
            return True
            
        print(f"Could not find markdown table in {filepath}")
        return False
        
    # Standard match found
    table_str = table_match.group(1)
    new_content = content[:image_end_idx] + table_section.replace(table_str, "\n\n", 1)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Successfully removed table from {filepath}")
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    languages = ["zh-tw", "zh-cn", "en", "ja", "ar", "de", "es", "fr", "pt", "ru"]
    modified_count = 0
    
    for lang in languages:
        filepath = os.path.join(content_dir, lang, "products", "ibeacon", "_index.md")
        if os.path.exists(filepath):
            if remove_table_from_file(filepath):
                modified_count += 1
        else:
            print(f"File not found: {filepath}")
            
    print(f"\nDone! Modified {modified_count} files.")

if __name__ == "__main__":
    main()
