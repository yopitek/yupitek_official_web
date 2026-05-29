用 yupitek-publish 上架這篇article 

/home/yopitek/Project/obsidian/GX10_HQ/05_SW/yupitek_official_web/blog/prompt/0522_article_final2.md

https://yupitek.com/zh-tw/blog/

我們公司的網頁有十種語言
1.
上架完成，請review 所有的語言網站都有這一篇文章的內容

use this skill 來潤飾稿子的內容 
/home/yopitek/Project/obsidian/GX10_HQ/06_resources/_prompts/_general/humanizer

/home/yopitek/Project/obsidian/GX10_HQ/06_resources/_prompts/_general/Humanizer-zh

/home/yopitek/Project/obsidian/GX10_HQ/06_resources/_prompts/_general/Humanizer-zh-TW

2.
before publish to github and cloudflare, need to check blog article locale and its link , if it is english blog article, all the product related links must link to https://yupitek.com/en/products/alfa/ english page, 
if it is japanese blog article, it must link to yupitek japan product page.  
use playright cli to confirm all the links before publish. 
and save 0522_testing_link.md to
/home/yopitek/Project/obsidian/GX10_HQ/05_SW/yupitek_official_web/blog/prompt

github address 
cloudflare address details are all in env files 
/home/yopitek/Project/obsidian/GX10_HQ/05_SW/env

3.location of clone yupitek website : 
/home/yopitek/Project/yupitek_official_web
GitHub repo: https://github.com/yopitek/yupitek_official_web
4.live URL : https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/

after uploading, please keep monitoring the github action status 
let me know if there is any issue. 

Basic website information 
1. Hugo site with 10 languages: ar, de, en, es, fr, ja, pt, ru, zh-cn, zh-tw
2. Blog posts are Hugo page bundles: content/{lang}/blog/{slug}/_index.md
3. Frontmatter format: title, description, date, draft, showBreadcrumbs, showTableOfContents, tags
4. Deployment: GitHub → Cloudflare Pages via GitHub Actions
5. Cloudflare Pages project: yupitek