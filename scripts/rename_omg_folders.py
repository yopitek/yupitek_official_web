#!/usr/bin/env python3
import os
import shutil

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    languages = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru"]
    
    for lang in languages:
        parent_dir = os.path.join(content_dir, lang, "products", "hak5")
        if not os.path.exists(parent_dir):
            continue
            
        old_path = os.path.join(parent_dir, "omg-unBlocker")
        new_path = os.path.join(parent_dir, "omg-unblocker")
        
        if os.path.exists(old_path):
            if os.path.exists(new_path):
                # If both exist, merge contents
                print(f"Merging {old_path} into {new_path}")
                for item in os.listdir(old_path):
                    shutil.move(os.path.join(old_path, item), os.path.join(new_path, item))
                os.rmdir(old_path)
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
        else:
            print(f"Path does not exist: {old_path}")

if __name__ == "__main__":
    main()
