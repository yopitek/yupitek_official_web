#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    # 1. Gather all files in the English content directory as the source of truth
    en_dir = os.path.join(content_dir, "en")
    en_structure = {}
    
    for root, dirs, files in os.walk(en_dir):
        for file in files:
            if file in ["index.md", "_index.md"]:
                rel_path = os.path.relpath(root, en_dir)
                en_structure[rel_path] = file

    print(f"Found {len(en_structure)} bundles in English content directory.")
    
    # 2. Check other languages for mismatch
    languages = ["zh-tw", "zh-cn", "ja", "ar", "de", "es", "fr", "pt", "ru"]
    fixed_count = 0
    
    for lang in languages:
        lang_dir = os.path.join(content_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        print(f"\nChecking language: {lang}")
        for rel_path, expected_file in en_structure.items():
            target_folder = os.path.join(lang_dir, rel_path)
            if not os.path.exists(target_folder):
                continue
                
            actual_files = os.listdir(target_folder)
            
            # Check if there is a mismatch
            # Case 1: English has index.md, target has _index.md but no index.md
            if expected_file == "index.md" and "_index.md" in actual_files and "index.md" not in actual_files:
                old_path = os.path.join(target_folder, "_index.md")
                new_path = os.path.join(target_folder, "index.md")
                os.rename(old_path, new_path)
                print(f"  Renamed: {lang}/{rel_path}/_index.md -> index.md")
                fixed_count += 1
                
            # Case 2: English has _index.md, target has index.md but no _index.md
            elif expected_file == "_index.md" and "index.md" in actual_files and "_index.md" not in actual_files:
                old_path = os.path.join(target_folder, "index.md")
                new_path = os.path.join(target_folder, "_index.md")
                os.rename(old_path, new_path)
                print(f"  Renamed: {lang}/{rel_path}/index.md -> _index.md")
                fixed_count += 1
                
            # Case 3: Both exist in the target folder, but one shouldn't.
            # Clean up the redundant one if it's there
            elif expected_file == "index.md" and "index.md" in actual_files and "_index.md" in actual_files:
                # Target has both index.md and _index.md, but English only has index.md.
                # Remove the redundant _index.md to prevent Hugo conflict
                extra_file = os.path.join(target_folder, "_index.md")
                os.remove(extra_file)
                print(f"  Removed redundant _index.md in: {lang}/{rel_path}/")
                fixed_count += 1
                
            elif expected_file == "_index.md" and "_index.md" in actual_files and "index.md" in actual_files:
                # Target has both, but English only has _index.md.
                # Remove the redundant index.md
                extra_file = os.path.join(target_folder, "index.md")
                os.remove(extra_file)
                print(f"  Removed redundant index.md in: {lang}/{rel_path}/")
                fixed_count += 1

    print(f"\nCompleted! Fixed {fixed_count} mismatches/redundancies.")

if __name__ == "__main__":
    main()
