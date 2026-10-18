# scripts/

One-off and maintenance scripts. Draft by local Qwen; paths checked by code against the directory listing.

| Script | Purpose |
|---|---|
| `add_awus036achm_card.py` | The script inserts a localized AWUS036ACHM product card into Markdown files, modifying them in place without network access or secrets. |
| `audit_website.py` | Audits product counts and broken images across all locales on https://yupitek.com using Playwright (network) and writes results to scripts/audit_results.json; no secrets. |
| `build_alfa_80_pages.py` | Helper module (no __main__) defining the article-file generator and a zh-TW to zh-CN character mapper; writes nothing on its own; files under content/<locale>/blog/ are written only when build_all_locales_pipeline.py calls generate_article_file(); no network, no secrets. |
| `build_all_locales_pipeline.py` | It generates localized markdown files by reading sources, calling a translation function, and writing output files in place. |
| `cache_bust_images.py` | The script appends a version query string to specific image URLs in multilingual Markdown files, modifying them in place. |
| `check_images.sh` | The script checks for missing image files referenced in product markdown files across multiple locales, printing warnings to stdout without modifying files or accessing the network. |
| `fix_bundle_mismatches.py` | The script renames or deletes mismatched index files in non-English content directories to match the English structure, modifying files in place. |
| `fix_hak5_ar_es_pt_ru.py` | The script updates local Markdown files in place by inserting translated HAK5 product cards for Arabic, Spanish, Portuguese, and Russian, requiring no network access or secrets. |
| `fix_hak5_ja.py` | Adds missing HAK5 product cards (Japanese) to content/ja/products/hak5/_index.md, modifying the file in place; no network, no secrets. |
| `fix_sdrlab.py` | Inserts missing SDRLab product cards into content/{ar,es,pt,ru,ja}/products/sdrlab/_index.md in place; no network, no secrets. |
| `gen_fr_de_products.py` | Generates French and German product _index.md files from product data hardcoded in the script (reads no English templates), overwriting existing files under the fr/de content directories; no network, no secrets. |
| `gen_ibeacon_multilingual.py` | Generates iBeacon landing and YPB01-YPB05 product pages for 9 locales (translated from the English pages) and inserts an iBeacon card into each locale's products index in place; no network, no secrets. |
| `generate_all_80_blog_posts.py` | Data/config module holding metadata of 8 articles (titles, descriptions, FAQs) across 10 locales plus a source-reader helper; writes no files, no network, no secrets. |
| `generate_all_locales.py` | Writes localized Sierra overview and per-product pages (derived from the zh-TW pages) into the Obsidian-vault copy of the site's content directory (not this repo's content/); no network, no secrets. |
| `generate_all_locales_v2.py` | The script generates localized Markdown content files for Sierra Wireless modules by writing translated text directly into the specified local Obsidian vault directory. |
| `generate_project_html.py` | It generates a Hugo-compatible HTML page for projects by merging JSON data, writing the output file locally without network calls or secrets. |
| `generate_sierra_v2.py` | The script generates localized product pages for Sierra Wireless modules across ten languages using translation data, writing files in place without network calls or secrets. |
| `insert_blog_images.py` | The script copies webp images to a static directory and updates blog frontmatter in place, requiring no network access or secrets. |
| `kanban-workflow.sh` | The script manages a seven-column Kanban workflow by moving tasks, checking limits, and scoring items, writing updates directly to local Markdown files. |
| `link-skills.sh` | The script clones mattpocock/skills from GitHub and writes installed_skills.json to ~/.claude/skills, requiring network access. |
| `pre_release_check.py` | It checks git status, scans for secrets, verifies Chinese characters, and builds Hugo, calling network and reading files without writing or printing secrets. |
| `publish_10_articles_pipeline.py` | Translates 10 articles into 10 locales via the Zhipu GLM API (network) and creates/overwrites blog markdown under content/. WARNING: the GLM API key is hardcoded in source and committed to git — rotate it and move it to an environment variable. |
| `qa/blog_verify.js` | This script uses Playwright to verify blog page titles and hreflang tags across multiple locales on yupitek.com, requiring network access but no secrets or file writes. |
| `remove_ibeacon_tables.py` | The script removes iBeacon comparison markdown tables from specified files, modifying them in place without network access or secrets. |
| `remove_ypb03_battery_life.py` | The script removes battery life claims from YPB03 documentation files in multiple languages by performing in-place text replacements. |
| `rename_omg_folders.py` | Renames or merges "omg-unBlocker" folders to "omg-unblocker" across multiple language directories, modifying the local filesystem in place without network access or secrets. |
| `standardize_ctas.py` | It standardizes multilingual contact CTAs in Markdown files by replacing keyword-matched alert blocks with canonical links, modifying files in place without network access or secrets. |
| `sync_graphiccard.py` | The script updates local Markdown files in place by inserting localized product descriptions for MSI RTX 5080 graphics cards across seven language directories. |
| `test_pre_release_check.py` | The script tests pre-release checks for secret detection, simplified Chinese identification, and Git status parsing without side effects, network calls, or secrets. |
| `translation_dataset.py` | The script defines static translation dictionaries for Chinese and English locales, with no side effects, network calls, or secret requirements. |
| `update_all_menus.py` | The script inserts a Sierra Wireless menu entry into TOML configuration files, modifying them in place without network access or secrets. |
| `verify_after_fix.py` | Verifies product card counts and broken images with Playwright against BASE_URL (default http://localhost:1313, overridable by env var); HTTP requests only, no file writes, no secrets. |
| `verify_website_improvements.py` | The script uses Playwright to audit localized product pages on a local server, verifying CTA text and links without writing files or requiring secrets. |
