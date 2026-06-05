#!/usr/bin/env python3
import os
import re

# Standardized CTA dictionary for all 10 languages
CTA_MAP = {
    "zh-tw": "需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)",
    "zh-cn": "需要询问产品报价?请来信[与我们联系](/zh-cn/contact/)",
    "en": "Need a product quotation? Please [contact us](/en/contact/)",
    "ja": "製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。",
    "ar": "هل تحتاج إلى طلب عرض سعر للمنتج؟ يرجى [الاتصال بنا](/ar/contact/).",
    "de": "Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).",
    "es": "¿Necesita una cotización del producto? Por favor, [contáctenos](/es/contact/).",
    "fr": "Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).",
    "pt": "Precisa de uma cotação do produto? Por favor, [entre em contato conosco](/pt/contact/).",
    "ru": "Нужно коммерческое предложение? Пожалуйста, [свяжитесь с нами](/ru/contact/)."
}

# Key phrases to identify CTA alerts/lines and avoid matching general warning/info alerts
CTA_KEYWORDS = [
    "sales@yupitek.com", "contact", "聯絡我們", "聯繫我們", "與我們聯絡", 
    "與我們聯繫", "詢問", "詢價", "報價", "报价", "询价", "見積もり", "お問い合わせ", 
    "quotation", "price", "pricing", "devis", "offerte", "presupuesto", "cotización", 
    "orçamento", "предложение", "цена", "تواصل", "مهتم"
]

def get_language(filepath):
    # Detect language from directory path (e.g. content/zh-tw/products/...)
    parts = filepath.split(os.sep)
    for part in parts:
        if part in CTA_MAP:
            return part
    return None

def standardize_file(filepath):
    lang = get_language(filepath)
    if not lang:
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    new_content = content
    
    # Targetized text replacement for YPB01-YPB05 templates which might be used during generation
    has_alert_cta = False
    
    # 1. First check if there is an {{< alert ... >}} block containing CTA keywords
    alert_pattern = re.compile(r'(\{\{<\s*alert(?:\s+[^>]+)?\s*>\}\}(.*?)\{\{<\s*/\s*alert\s*>\}\})', re.DOTALL)
    matches = list(alert_pattern.finditer(content))
    
    if matches:
        for match in reversed(matches):
            full_block = match.group(1)
            inner_text = match.group(2)
            
            is_warning = any(w in inner_text.lower() for w in ["disclaimer", "warning", "rechtlicher", "合法使用", "聲明", "声明", "hint"])
            is_cta = any(kw.lower() in inner_text.lower() for kw in CTA_KEYWORDS) and not is_warning
            if is_cta:
                has_alert_cta = True
                cta_text = CTA_MAP[lang]
                new_block = f"{{{{< alert >}}}}\n{cta_text}\n{{{{< /alert >}}}}"
                
                if full_block.strip() != new_block.strip():
                    new_content = new_content[:match.start()] + new_block + new_content[match.end():]
                    modified = True
                    
    # 2. If no {{< alert >}} block was modified or found (and none was already present as a CTA alert), search for plain text lines containing contact links and CTA keywords
    if not modified and not has_alert_cta:
        # Match a line containing a contact markdown link, e.g., [Contact us](/en/contact/)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            # Check if this line has a markdown link with "contact" inside the URL
            if re.search(r'\[([^\]]+)\]\(([^)]*?contact/?)\)', line):
                # Verify if it contains CTA keywords
                is_cta = any(kw.lower() in line.lower() for kw in CTA_KEYWORDS)
                if is_cta:
                    cta_text = CTA_MAP[lang]
                    new_line = f"{{{{< alert >}}}}\n{cta_text}\n{{{{< /alert >}}}}"
                    
                    # Also clean up any preceding line separators like "---" right before it if needed,
                    # but simple replacement of the line is safer.
                    lines[idx] = new_line
                    modified = True
        
        if modified:
            new_content = "\n".join(lines) + "\n"

    # 3. Handle files that might have sales email directly in text but no link at all (as a fallback)
    if not modified and not has_alert_cta:
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if "sales@yupitek.com" in line and any(kw.lower() in line.lower() for kw in ["quotation", "price", "詢問", "報價"]):
                cta_text = CTA_MAP[lang]
                lines[idx] = f"{{{{< alert >}}}}\n{cta_text}\n{{{{< /alert >}}}}"
                modified = True
        if modified:
            new_content = "\n".join(lines) + "\n"

    # 4. Fallback: If no CTA was found/modified, append it to the end of product detail pages
    if not modified and not has_alert_cta:
        parts = filepath.split(os.sep)
        if len(parts) >= 6 and "products" in parts:
            new_content = content.rstrip() + f"\n\n{{{{< alert >}}}}\n{CTA_MAP[lang]}\n{{{{< /alert >}}}}\n"
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Standardized: {filepath}")

    return modified

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content")
    
    print(f"Sweeping directory: {content_dir}")
    
    count = 0
    for root, dirs, files in os.walk(content_dir):
        # Scan products and solutions (since some solutions pages might have CTAs too)
        if "products" not in root and "solution" not in root:
            continue
            
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # Skip top-level category indices if they are just catalog listings
                parts = filepath.split(os.sep)
                if len(parts) >= 3 and parts[-2] == "products" and file == "_index.md":
                    continue
                
                if standardize_file(filepath):
                    count += 1
                    
    print(f"\nSuccessfully standardized {count} files.")

if __name__ == "__main__":
    main()
