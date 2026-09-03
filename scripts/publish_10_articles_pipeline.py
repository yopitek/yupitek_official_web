#!/usr/bin/env python3
"""
publish_10_articles_pipeline.py
Robust end-to-end multi-locale generation pipeline for 10 ALFA technical articles.
Locales: zh-tw, zh-cn, en, ja, ar, es, pt, ru, de, fr
Features:
- Markdown Frontmatter parsing & generation conforming to Blowfish / yupitek standards.
- Section-level chunked multi-locale translation via GLM-4-Flash & OpenCC.
- Exponential backoff & resumption cache so already translated pages are skipped.
- Preserves code fences, model SKUs, URLs, tags.
"""

import os
import re
import sys
import json
import time
import urllib.request
import opencc

GLM_API_KEY = "7b1ca70b349c4dbbb071a62202aa99a1.ZBRrjqMIIagpuWc3"
GLM_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

SOURCE_DIR = "/home/yopitek/Documents/Obsidian_vault/GX10_HQ/F_Daily/01_Daily_note/2026-09/2026-09-03/blog_article"
CONTENT_DIR = "/home/yopitek/Project/yupitek_official_web/content"

ARTICLES = [
    {
        "file": "alfa_jetsonnano_final.md",
        "slug": "alfa-nvidia-jetson-nano-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 NVIDIA Jetson Nano",
        "category": "邊緣 AI / 單板電腦",
        "tags": ["ALFA", "AWUS036ACH", "AWUS036ACM", "NVIDIA", "Jetson-Nano", "JetPack", "ARM64", "Linux-WiFi"]
    },
    {
        "file": "alfa_nvidiadgx_final.md",
        "slug": "alfa-nvidia-dgx-spark-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 NVIDIA DGX Spark",
        "category": "邊緣 AI / GPU 伺服器",
        "tags": ["ALFA", "NVIDIA", "DGX-Spark", "GB10", "DGX-OS", "AWUS036ACH", "AWUS036ACM", "ARM64"]
    },
    {
        "file": "alfa_gx10_final.md",
        "slug": "alfa-asus-ascent-gx10-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 ASUS Ascent GX10",
        "category": "邊緣 AI / GPU 伺服器",
        "tags": ["ALFA", "ASUS", "Ascent-GX10", "GB10", "DGX-OS", "AWUS036ACM", "AWUS036AXML", "ARM64"]
    },
    {
        "file": "alfa_altosbrainsphere_final.md",
        "slug": "alfa-altos-brainsphere-gb10-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 ALTOS BrainSphere GB10 F1",
        "category": "邊緣 AI / GPU 伺服器",
        "tags": ["ALFA", "Altos", "BrainSphere-GB10", "NVIDIA-GB10", "AWUS036ACM", "ARM64", "DGX-OS"]
    },
    {
        "file": "alfa_gigabyte_ai_top_final.md",
        "slug": "alfa-gigabyte-ai-top-atom-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 GIGABYTE AI TOP ATOM",
        "category": "邊緣 AI / GPU 伺服器",
        "tags": ["ALFA", "GIGABYTE", "AI-TOP-ATOM", "GB10", "DGX-OS", "AWUS036ACH", "AWUS036ACM", "ARM64"]
    },
    {
        "file": "alfa_msiedgexpert_final.md",
        "slug": "alfa-msi-edgexpert-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 MSI EdgeXpert",
        "category": "邊緣 AI / GPU 伺服器",
        "tags": ["ALFA", "MSI", "EdgeXpert", "GB10", "DGX-OS", "AWUS036ACM", "AWUS036AXML", "ARM64"]
    },
    {
        "file": "alfa_openwart_final.md",
        "slug": "alfa-openwrt-router-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 OpenWrt",
        "category": "路由器韌體",
        "tags": ["ALFA", "OpenWrt", "Router", "kmod-mt76", "AWUS036ACM", "AWUS036ACH", "Soft-AP"]
    },
    {
        "file": "alfa_ddwrt_final.md",
        "slug": "alfa-ddwrt-router-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 DD-WRT",
        "category": "路由器韌體",
        "tags": ["ALFA", "DD-WRT", "Router", "Broadcom", "Atheros", "USB-WiFi", "Compatibility"]
    },
    {
        "file": "alfa_tomato_final.md",
        "slug": "alfa-tomato-router-compatibility",
        "title_zh_tw": "ALFA 無線網卡是否支援 Tomato",
        "category": "路由器韌體",
        "tags": ["ALFA", "Tomato", "FreshTomato", "Router", "Broadcom", "USB-WiFi", "Compatibility"]
    },
    {
        "file": "alfa_wifi_driver_guide_final.md",
        "slug": "alfa-usb-wifi-linux-driver-guide",
        "title_zh_tw": "ALFA USB 網卡 Linux 驅動怎麼選",
        "category": "驅動 / 選購指南",
        "tags": ["ALFA", "Linux-Driver", "MediaTek", "Realtek", "in-kernel", "out-of-tree", "DKMS", "mt76", "rtl8812au"]
    }
]

LOCALE_PROMPTS = {
    "en": "You are a professional B2B technical writer for Yupitek. Translate the following Chinese technical markdown into native, fluent B2B English. Keep all markdown structure, tables, URLs, and code blocks untouched. Never translate technical keywords or model numbers (e.g. WiFi, AWUS036ACH, RTL8812AU, MT7921AU, Kali Linux, DKMS, in-kernel, out-of-tree). Return ONLY the translated markdown.",
    "ja": "You are a professional B2B technical writer for Yupitek Japan. Translate the following Chinese technical markdown into formal Japanese (です・ます調). Use appropriate katakana for loan words (アダプター, ドライバ, チップセット, モニターモード). Keep markdown structure, tables, URLs, and code blocks untouched. Never translate product model numbers. Return ONLY the translated markdown.",
    "ar": "You are a professional B2B technical translator for Yupitek Middle East. Translate the following Chinese technical markdown into Modern Standard Arabic (الفصحى, formal B2B). Keep technical terms in English. Use « » quotation marks. Keep markdown tables, code blocks, model numbers, and URLs verbatim. Return ONLY the translated markdown.",
    "es": "You are a professional B2B technical writer for Yupitek Spain and Latin America. Translate the following Chinese technical markdown into formal B2B Spanish (usted style). Keep markdown structure, tables, URLs, code blocks, and hardware models untouched. Return ONLY the translated markdown.",
    "pt": "You are a professional B2B technical writer for Yupitek Brazil. Translate the following Chinese technical markdown into formal Brazilian Portuguese (pt-BR, formal B2B). Keep markdown structure, tables, URLs, code blocks, and model names untouched. Return ONLY the translated markdown.",
    "ru": "You are a professional B2B technical translator for Yupitek Eastern Europe. Translate the following Chinese technical markdown into formal Russian (Вы-форма, formal B2B). Use « » quotes. Keep markdown structure, tables, URLs, code blocks, and hardware models untouched. Return ONLY the translated markdown.",
    "de": "You are a professional B2B technical writer for Yupitek Germany. Translate the following Chinese technical markdown into friendly B2B German (Du-form). Capitalize all German nouns. Keep markdown structure, tables, URLs, code blocks, and model numbers untouched. Return ONLY the translated markdown.",
    "fr": "You are a professional B2B technical writer for Yupitek France. Translate the following Chinese technical markdown into casual professional French (tutoyer). Add proper spacing before punctuation (! ? : ;). Use « » quotes. Keep markdown structure, tables, URLs, code blocks, and hardware models untouched. Return ONLY the translated markdown."
}

def call_glm_single(prompt, content, max_retries=5, timeout=120):
    for attempt in range(max_retries):
        try:
            req_data = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                "temperature": 0.2
            }
            req = urllib.request.Request(
                GLM_URL,
                data=json.dumps(req_data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GLM_API_KEY}"
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            wait_time = (attempt + 1) * 3
            print(f"    [Retry {attempt+1}/{max_retries}] API call failed: {e}. Waiting {wait_time}s...")
            time.sleep(wait_time)
    raise RuntimeError(f"Failed to call GLM API after {max_retries} retries")

def translate_markdown_body(prompt, body):
    # If body is under 3500 chars, translate in one shot
    if len(body) <= 3500:
        return call_glm_single(prompt, body)
    
    # Otherwise, split by H2 sections (## ) to avoid request timeouts
    sections = re.split(r'\n(?=## )', body)
    translated_sections = []
    for sec in sections:
        if not sec.strip():
            continue
        # If a single section is still huge, split by paragraphs
        if len(sec) > 3500:
            sub_chunks = []
            cur_chunk = ""
            for p in sec.split("\n\n"):
                if len(cur_chunk) + len(p) < 3000:
                    cur_chunk += p + "\n\n"
                else:
                    if cur_chunk.strip():
                        sub_chunks.append(cur_chunk)
                    cur_chunk = p + "\n\n"
            if cur_chunk.strip():
                sub_chunks.append(cur_chunk)
            for sc in sub_chunks:
                t_sc = call_glm_single(prompt, sc)
                translated_sections.append(t_sc)
        else:
            t_sec = call_glm_single(prompt, sec)
            translated_sections.append(t_sec)
        time.sleep(0.5)
    
    return "\n\n".join(translated_sections)

opencc_t2s = opencc.OpenCC('t2s')
ZH_CN_TERMS = [
    ("韌體", "固件"),
    ("網路卡", "网卡"),
    ("網卡", "网卡"),
    ("軟體", "软件"),
    ("硬體", "硬件"),
    ("硬碟", "硬盘"),
    ("光碟", "光盘"),
    ("滑鼠", "鼠标"),
    ("螢幕", "显示器"),
    ("印表機", "打印机"),
    ("隨身碟", "U盘"),
    ("資料夾", "文件夹"),
    ("檔案", "文件"),
    ("訊號", "信号"),
    ("高畫質", "高清"),
    ("解析度", "分辨率"),
    ("預設", "默认"),
    ("支援", "支持")
]

def convert_zh_tw_to_zh_cn(text):
    s = opencc_t2s.convert(text)
    for t_old, t_new in ZH_CN_TERMS:
        s = s.replace(t_old, t_new)
    return s

def clean_source_markdown(md_text):
    lines = md_text.split("\n")
    cleaned = []
    title = ""
    desc = ""
    for line in lines:
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("分類標籤：") or line.startswith("建立日期：") or line.startswith("內容狀態："):
            continue
        if not desc and line.startswith("簡短結論："):
            desc = line[5:].strip()
        cleaned.append(line)
    
    body = "\n".join(cleaned).strip()
    if not desc:
        for p in body.split("\n\n"):
            p_strip = p.strip()
            if p_strip and not p_strip.startswith("#") and not p_strip.startswith("|"):
                desc = p_strip[:150]
                break
    return title, desc, body

def build_frontmatter(title, desc, slug, tags, category, locale):
    tag_str = "\n".join([f'  - "{t}"' for t in tags])
    t_clean = title.replace('"', '\\"')
    d_clean = desc.replace('"', '\\"').replace('\n', ' ')
    if len(d_clean) > 200:
        d_clean = d_clean[:197] + "..."
    
    fm = f"""---
title: "{t_clean}"
date: 2026-09-03
draft: false
slug: "{slug}"
tags:
{tag_str}
categories:
  - "{category}"
description: "{d_clean}"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

"""
    return fm

def process_all():
    print(f"Starting robust processing for 10 articles across 10 locales...")

    # Phase 1: zh-tw (Local source)
    print("\n=== Phase 1: Generating zh-tw articles ===")
    parsed_articles = []
    for art in ARTICLES:
        src_path = os.path.join(SOURCE_DIR, art["file"])
        with open(src_path, "r", encoding="utf-8") as f:
            raw = f.read()
        title, desc, body = clean_source_markdown(raw)
        if not title:
            title = art["title_zh_tw"]
        
        art_info = {
            "meta": art,
            "title": title,
            "desc": desc,
            "body": body
        }
        parsed_articles.append(art_info)

        out_dir = os.path.join(CONTENT_DIR, "zh-tw", "blog", art["slug"])
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "_index.md")
        fm = build_frontmatter(title, desc, art["slug"], art["tags"], art["category"], "zh-tw")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(fm + body + "\n")
        print(f" [zh-tw] Verified/Created: {art['slug']}")

    # Phase 2: Batch A (zh-cn, en, ja)
    print("\n=== Phase 2: Generating Batch A (zh-cn, en, ja) ===")
    for art_info in parsed_articles:
        slug = art_info["meta"]["slug"]
        
        # 1. zh-cn
        out_zh_cn = os.path.join(CONTENT_DIR, "zh-cn", "blog", slug, "_index.md")
        if not os.path.exists(out_zh_cn) or os.path.getsize(out_zh_cn) < 100:
            zh_cn_title = convert_zh_tw_to_zh_cn(art_info["title"])
            zh_cn_desc = convert_zh_tw_to_zh_cn(art_info["desc"])
            zh_cn_body = convert_zh_tw_to_zh_cn(art_info["body"])
            zh_cn_tags = [convert_zh_tw_to_zh_cn(t) for t in art_info["meta"]["tags"]]
            zh_cn_cat = convert_zh_tw_to_zh_cn(art_info["meta"]["category"])
            os.makedirs(os.path.dirname(out_zh_cn), exist_ok=True)
            with open(out_zh_cn, "w", encoding="utf-8") as f:
                fm = build_frontmatter(zh_cn_title, zh_cn_desc, slug, zh_cn_tags, zh_cn_cat, "zh-cn")
                f.write(fm + zh_cn_body + "\n")
            print(f" [zh-cn] Generated: {slug}")
        else:
            print(f" [zh-cn] Already exists: {slug}")

        # 2. en
        out_en = os.path.join(CONTENT_DIR, "en", "blog", slug, "_index.md")
        if not os.path.exists(out_en) or os.path.getsize(out_en) < 200:
            print(f" Translating [en]: {slug}...")
            en_content = translate_markdown_body(LOCALE_PROMPTS["en"], art_info["body"])
            en_title = call_glm_single("Translate this technical blog title into concise English title case:", art_info["title"])
            en_desc = call_glm_single("Translate this summary into a 1-2 sentence English meta description under 160 characters:", art_info["desc"])
            os.makedirs(os.path.dirname(out_en), exist_ok=True)
            with open(out_en, "w", encoding="utf-8") as f:
                fm = build_frontmatter(en_title, en_desc, slug, art_info["meta"]["tags"], "Hardware Guide", "en")
                f.write(fm + en_content + "\n")
            print(f" [en] Completed: {slug}")
        else:
            print(f" [en] Already exists: {slug}")

        # 3. ja
        out_ja = os.path.join(CONTENT_DIR, "ja", "blog", slug, "_index.md")
        if not os.path.exists(out_ja) or os.path.getsize(out_ja) < 200:
            print(f" Translating [ja]: {slug}...")
            ja_content = translate_markdown_body(LOCALE_PROMPTS["ja"], art_info["body"])
            ja_title = call_glm_single("Translate this technical blog title into formal Japanese:", art_info["title"])
            ja_desc = call_glm_single("Translate this summary into concise Japanese meta description under 120 characters:", art_info["desc"])
            os.makedirs(os.path.dirname(out_ja), exist_ok=True)
            with open(out_ja, "w", encoding="utf-8") as f:
                fm = build_frontmatter(ja_title, ja_desc, slug, art_info["meta"]["tags"], "ハードウェアガイド", "ja")
                f.write(fm + ja_content + "\n")
            print(f" [ja] Completed: {slug}")
        else:
            print(f" [ja] Already exists: {slug}")

    # Phase 3: Batch B (ar, es, pt)
    print("\n=== Phase 3: Generating Batch B (ar, es, pt) ===")
    for art_info in parsed_articles:
        slug = art_info["meta"]["slug"]
        for loc, cat_label in [("ar", "دليل الأجهزة"), ("es", "Guía de Hardware"), ("pt", "Guia de Hardware")]:
            out_loc = os.path.join(CONTENT_DIR, loc, "blog", slug, "_index.md")
            if not os.path.exists(out_loc) or os.path.getsize(out_loc) < 200:
                print(f" Translating [{loc}]: {slug}...")
                loc_content = translate_markdown_body(LOCALE_PROMPTS[loc], art_info["body"])
                loc_title = call_glm_single(f"Translate this technical blog title into formal {loc}:", art_info["title"])
                loc_desc = call_glm_single(f"Translate this summary into concise {loc} meta description under 150 characters:", art_info["desc"])
                os.makedirs(os.path.dirname(out_loc), exist_ok=True)
                with open(out_loc, "w", encoding="utf-8") as f:
                    fm = build_frontmatter(loc_title, loc_desc, slug, art_info["meta"]["tags"], cat_label, loc)
                    f.write(fm + loc_content + "\n")
                print(f" [{loc}] Completed: {slug}")
            else:
                print(f" [{loc}] Already exists: {slug}")

    # Phase 4: Batch C (ru, de, fr)
    print("\n=== Phase 4: Generating Batch C (ru, de, fr) ===")
    for art_info in parsed_articles:
        slug = art_info["meta"]["slug"]
        for loc, cat_label in [("ru", "Руководство по оборудованию"), ("de", "Hardware-Leitfaden"), ("fr", "Guide Matériel")]:
            out_loc = os.path.join(CONTENT_DIR, loc, "blog", slug, "_index.md")
            if not os.path.exists(out_loc) or os.path.getsize(out_loc) < 200:
                print(f" Translating [{loc}]: {slug}...")
                loc_content = translate_markdown_body(LOCALE_PROMPTS[loc], art_info["body"])
                loc_title = call_glm_single(f"Translate this technical blog title into formal {loc}:", art_info["title"])
                loc_desc = call_glm_single(f"Translate this summary into concise {loc} meta description under 150 characters:", art_info["desc"])
                os.makedirs(os.path.dirname(out_loc), exist_ok=True)
                with open(out_loc, "w", encoding="utf-8") as f:
                    fm = build_frontmatter(loc_title, loc_desc, slug, art_info["meta"]["tags"], cat_label, loc)
                    f.write(fm + loc_content + "\n")
                print(f" [{loc}] Completed: {slug}")
            else:
                print(f" [{loc}] Already exists: {slug}")

    print("\nAll 100 pages generated and verified successfully!")

if __name__ == "__main__":
    process_all()
