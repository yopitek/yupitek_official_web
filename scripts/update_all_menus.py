import os

CONFIG_DIR = "/home/yopitek/Documents/Obsidian_vault/GX10_HQ/05_SW/yupitek_official_web/config/_default"

def update_menu_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Avoid duplicate insertion
    if 'pageRef  = "/products/sierra"' in content or 'pageRef = "/products/sierra"' in content:
        print(f"Already updated: {os.path.basename(filepath)}")
        return

    # Find the parent used by ALFA Network or Mellanox
    parent_val = "Products"
    for line in content.splitlines():
        if "parent" in line and "weight" not in line:
            # e.g., parent   = "產品"
            parts = line.split("=")
            if len(parts) == 2:
                parent_val = parts[1].strip().strip('"').strip("'")
                break

    sierra_entry = f"""
  [[main]]
    name     = "Sierra Wireless"
    pageRef  = "/products/sierra"
    parent   = "{parent_val}"
    weight   = 28
"""
    # Insert right before Ubiquiti or right after SDRLAB
    if 'name     = "SDRLAB"' in content or 'name = "SDRLAB"' in content:
        content = content.replace('  [[main]]\n    name     = "Ubiquiti"', f'{sierra_entry}\n  [[main]]\n    name     = "Ubiquiti"')
        content = content.replace('  [[main]]\n    name = "Ubiquiti"', f'{sierra_entry}\n  [[main]]\n    name = "Ubiquiti"')
    else:
        content += sierra_entry

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully updated menu: {os.path.basename(filepath)} with parent='{parent_val}'")

def main():
    for fname in os.listdir(CONFIG_DIR):
        if fname.startswith("menus.") and fname.endswith(".toml"):
            update_menu_file(os.path.join(CONFIG_DIR, fname))

if __name__ == "__main__":
    main()
