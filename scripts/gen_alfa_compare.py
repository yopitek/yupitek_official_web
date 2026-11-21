#!/usr/bin/env python3
"""由 static/alfa_compare.html 產生 11 語系的 content/<locale>/alfa_compare.md。

設計原則：**事實只有一份**。型號、晶片、驅動、kernel 版本、實測結果一律從靜態頁解析，
各語系共用同一份數據；語系之間只有欄名與描述文字不同（data/alfa_compare_i18n.yaml）。
這樣日後更新靜態頁後重跑本腳本，11 語系不可能出現數據不一致。

用法（repo 根目錄）：python3 scripts/gen_alfa_compare.py
"""
import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ko", "de", "fr", "es", "pt", "ru", "ar"]


def _text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def parse_facts(path: Path) -> dict:
    """從靜態頁解析規格表、選購卡片與平台表。"""
    src = path.read_text(encoding="utf-8")
    tables = re.findall(r"<table>.*?</table>", src, re.S)

    def rows(table):
        out = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
            cells = [_text(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            if cells:
                out.append(cells)
        return out

    cards = []
    # 卡片以 <div class="guide-card"> 起頭，用切割取每段，避免巢狀 </div> 造成比對失準
    for block in src.split('<div class="guide-card">')[1:]:
        title = re.search(r"<h3>(.*?)</h3>", block, re.S)
        rec = re.search(r'<div class="rec">(.*?)</div>', block, re.S)
        why = re.search(r'<div class="why">(.*?)</div>', block, re.S)
        if not (title and rec and why):
            continue
        cards.append({"title": _text(title.group(1)),
                      "rec": _text(rec.group(1)),
                      "body": _text(why.group(1))})

    return {
        "spec_headers": [_text(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", tables[0], re.S)],
        "spec_rows": rows(tables[0]),
        "platform_headers": [_text(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", tables[1], re.S)],
        "platform_rows": rows(tables[1]),
        "cards": cards,
    }


def load_i18n(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _tr(strings: dict, value: str) -> str:
    """查翻譯；查不到就原樣保留（型號、單位、晶片名本來就不該翻）。"""
    return strings.get(value, value)


def render(locale: str, facts: dict, strings: dict) -> str:
    t = facts["spec_headers"]
    head = [_tr(strings, h) for h in t]
    lines = [
        "---",
        f'title: "{strings["title"]}"',
        f'description: "{strings["description"]}"',
        "date: 2026-03-12",
        "draft: false",
        "showBreadcrumbs: true",
        "showTableOfContents: true",
        "---",
        "",
        strings["intro"],
        "",
        f"## {strings['section_spec']}",
        "",
        strings["scroll_hint"],
        "",
        "| " + " | ".join(head) + " |",
        "|" + "---|" * len(head),
    ]
    for row in facts["spec_rows"]:
        # 有翻譯就用翻譯，沒有就原樣保留（型號、晶片、單位本來就不該翻）
        cells = [_tr(strings, c) for c in row]
        model = row[0]
        cells[0] = f"[{model}](/{locale}/products/alfa/{model.lower()}/)"  # 型號永遠用原始值
        lines.append("| " + " | ".join(cells) + " |")

    lines += ["", f"## {strings['section_usecase']}", ""]
    for card in facts["cards"]:
        lines.append(f"**{_tr(strings, card['title'])}** — {strings['best']}{strings.get('colon', ': ')}{card['rec'].replace('Best: ', '')}")
        lines.append("")
        lines.append(_tr(strings, card["body"]))
        lines.append("")

    lines += [f"## {strings['section_platform']}", "",
              "| " + " | ".join(_tr(strings, h) for h in facts["platform_headers"]) + " |",
              "|" + "---|" * len(facts["platform_headers"])]
    for row in facts["platform_rows"]:
        cells = [row[0], row[1], row[2], _tr(strings, row[3])]
        lines.append("| " + " | ".join(cells) + " |")

    lines += ["", "---", "", strings["footer"], ""]
    return "\n".join(lines)


def main() -> int:
    facts = parse_facts(REPO / "static" / "alfa_compare.html")
    i18n = load_i18n(REPO / "data" / "alfa_compare_i18n.yaml")
    written = 0
    for locale in LOCALES:
        if locale not in i18n:
            print(f"SKIP {locale}：尚無翻譯")
            continue
        out = REPO / "content" / locale / "alfa_compare.md"
        out.write_text(render(locale, facts, i18n[locale]), encoding="utf-8")
        written += 1
    print(f"{written}/{len(LOCALES)} 語系已產生，共 {len(facts['spec_rows'])} 款")
    return 0 if written == len(LOCALES) else 1


if __name__ == "__main__":
    sys.exit(main())
