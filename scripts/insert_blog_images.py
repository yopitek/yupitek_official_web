#!/usr/bin/env python3
import os
import shutil

def update_frontmatter(filepath, slug):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    if not content.startswith("---"):
        print(f"  No frontmatter in {filepath}")
        return False
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  Invalid frontmatter in {filepath}")
        return False
        
    frontmatter = parts[1]
    body = parts[2]
    
    lines = frontmatter.splitlines()
    has_featureimage = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith("featureimage:"):
            new_lines.append(f'featureimage: "/images/blog/{slug}.webp"')
            has_featureimage = True
        else:
            new_lines.append(line)
            
    if not has_featureimage:
        new_lines.append(f'featureimage: "/images/blog/{slug}.webp"')
        
    new_frontmatter = "\n".join(new_lines) + "\n"
    new_content = "---" + new_frontmatter + "---" + body
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    static_blog_dir = os.path.join(base_dir, "static", "images", "blog")
    
    # Create static/images/blog/ directory if it doesn't exist
    os.makedirs(static_blog_dir, exist_ok=True)
    
    source_img_dir = "/home/yopitek/Project/obsidian/GX10_HQ/01_Daily_note/2026-06/2026-06-05/website_blog/image_asset"
    if not os.path.exists(source_img_dir):
        print(f"Error: Source directory {source_img_dir} does not exist.")
        return
        
    # Get all webp files in the source directory
    images = [f for f in os.listdir(source_img_dir) if f.endswith(".webp")]
    print(f"Found {len(images)} images to process.")
    
    languages = [d for d in os.listdir(content_dir) if os.path.isdir(os.path.join(content_dir, d))]
    print(f"Detected languages: {languages}")
    
    copied_count = 0
    updated_files_count = 0
    
    for img_name in images:
        slug = os.path.splitext(img_name)[0]
        src_path = os.path.join(source_img_dir, img_name)
        dst_path = os.path.join(static_blog_dir, img_name)
        
        # 1. Copy image file to static/images/blog/
        shutil.copy(src_path, dst_path)
        print(f"\nCopied {img_name} -> static/images/blog/")
        copied_count += 1
        
        # 2. Find and update the article in all language subdirectories
        for lang in languages:
            blog_dir = os.path.join(content_dir, lang, "blog")
            if not os.path.exists(blog_dir):
                continue
                
            possible_paths = [
                os.path.join(blog_dir, slug, "_index.md"),
                os.path.join(blog_dir, slug, "index.md"),
                os.path.join(blog_dir, f"{slug}.md")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    if update_frontmatter(path, slug):
                        print(f"  Updated: {lang}/blog/.../{os.path.basename(path)}")
                        updated_files_count += 1
                        
    print(f"\nExecution summary:")
    print(f"  - Images copied: {copied_count}")
    print(f"  - Markdown files updated: {updated_files_count}")

if __name__ == "__main__":
    main()
