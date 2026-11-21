"""產生器測試：11 語系的 alfa_compare 必須與 static/alfa_compare.html 的事實一致。

重點是「事實不可因語系而異」：型號、晶片、驅動、kernel 版本、handshake 結果，
在每個語系都必須完全相同；語系之間只有標籤與說明文字不同。
"""
import importlib.util
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("gen", REPO / "scripts" / "gen_alfa_compare.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ko", "de", "fr", "es", "pt", "ru", "ar"]
MODELS = ["AWUS036AXML", "AWUS036AXM", "AWUS036AX", "AWUS036AXER", "AWUS036ACH",
          "AWUS036ACM", "AWUS036ACHM", "AWUS036ACS", "AWUS036EACS"]


@pytest.fixture(scope="module")
def facts():
    return gen.parse_facts(REPO / "static" / "alfa_compare.html")


def test_parses_nine_models(facts):
    assert [r[0] for r in facts["spec_rows"]] == MODELS


def test_spec_table_shape(facts):
    assert len(facts["spec_headers"]) == 17
    assert all(len(r) == 17 for r in facts["spec_rows"])


def test_i18n_covers_every_locale():
    i18n = gen.load_i18n(REPO / "data" / "alfa_compare_i18n.yaml")
    missing = [loc for loc in LOCALES if loc not in i18n]
    assert not missing, f"缺少語系翻譯：{missing}"


def test_i18n_has_every_key():
    i18n = gen.load_i18n(REPO / "data" / "alfa_compare_i18n.yaml")
    base = set(i18n["en"])
    for loc in LOCALES:
        missing = base - set(i18n[loc])
        assert not missing, f"{loc} 缺少鍵：{sorted(missing)[:6]}"


@pytest.mark.parametrize("loc", LOCALES)
def test_generated_page_exists_and_lists_nine_models(loc):
    page = REPO / "content" / loc / "alfa_compare.md"
    assert page.is_file(), f"缺少 {page}"
    text = page.read_text(encoding="utf-8")
    for m in MODELS:
        assert m in text, f"{loc} 缺少 {m}"


@pytest.mark.parametrize("loc", LOCALES)
def test_generated_page_is_not_a_stub(loc):
    """先前 11 語系都是空殼（本文 <100 字），這是本次要修的問題。"""
    body = (REPO / "content" / loc / "alfa_compare.md").read_text(encoding="utf-8").split("---", 2)[2]
    assert len(body) > 2000, f"{loc} 本文僅 {len(body)} 字，仍是空殼"


def _spec_rows(loc):
    """回傳該語系規格表的資料列，已拆成欄。"""
    text = (REPO / "content" / loc / "alfa_compare.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if re.match(r"^\|\s*\[AWUS036", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


@pytest.mark.parametrize("loc", LOCALES)
def test_fact_columns_identical_to_english(loc):
    """事實欄（型號、晶片、頻段、速率、USB、天線、MIMO、功耗、藍牙）各語系必須一字不差。

    只有標籤與描述可以因語系而異；規格數據不行。先前 11 語系各自為政才會出現
    AXM 晶片與官方規格不符這類錯誤。
    """
    FACT_COLS = {0: "型號", 2: "晶片", 3: "頻段", 4: "速率", 5: "USB", 6: "天線",
                 7: "MIMO", 14: "功耗", 15: "藍牙"}

    def bands(value):
        """只留頻段數字：允許在地化的小數逗號與括號註記，但數字必須一致。"""
        value = re.sub(r"[（(].*?[）)]", "", value)
        value = value.replace(",", ".").replace("ГГц", "GHz")
        return sorted(re.findall(r"\d+(?:\.\d+)?", value))
    en_rows, rows = _spec_rows("en"), _spec_rows(loc)
    assert len(rows) == len(en_rows) == 9
    for en_row, row in zip(en_rows, rows):
        for i, name in FACT_COLS.items():
            if i == 6:   # 天線欄含「Integrated」等可翻譯字樣，不比對
                continue
            got, want = row[i], en_row[i]
            if i == 3:   # 頻段欄可在地化（小數逗號、括號註記翻譯），但頻段數字必須相同
                assert bands(got) == bands(want), \
                    f"{loc} 頻段與英文版不符：{got!r} vs {want!r}"
                continue
            if i in (6,):
                continue
            if i == 0:   # 型號欄是連結，各語系指向自己的產品頁；只比對型號本身
                got = re.match(r"\[([^\]]+)\]", got).group(1)
                want = re.match(r"\[([^\]]+)\]", want).group(1)
                assert f"/{loc}/products/alfa/{got.lower()}/" in row[i], \
                    f"{loc} 型號連結未指向本語系：{row[i]!r}"
            assert got == want, f"{loc} 第 {i} 欄（{name}）與英文版不符：{got!r} vs {want!r}"


@pytest.mark.parametrize("loc", LOCALES)
def test_chipsets_present(loc):
    """9 款的晶片都要出現。AXM 與 AXML 同為 MT7921AUN（ALFA 官方規格，2026-11-22 查證）。"""
    chips = [r[2] for r in _spec_rows(loc)]
    assert sorted(chips) == sorted(["MT7921AUN", "MT7921AUN", "RTL8832BU", "RTL8832BU",
                                    "RTL8812AU", "MT7612U", "MT7610U", "RTL8811AU", "RTL8821CU"])


@pytest.mark.parametrize("loc", LOCALES)
def test_kernel_versions_present(loc):
    text = (REPO / "content" / loc / "alfa_compare.md").read_text(encoding="utf-8")
    for kernel in ("4.19", "5.18", "6.2", "6.13", "6.17"):
        assert kernel in text, f"{loc} 缺少 kernel 版本 {kernel}"


@pytest.mark.parametrize("loc", LOCALES)
def test_handshake_seven_of_nine(loc):
    """9 款中 7 款端到端成功，AXM / AXML 失敗。"""
    rows = _spec_rows(loc)
    ok = [r for r in rows if "✅" in r[10]]
    assert len(ok) == 7, f"{loc} 端到端成功應為 7 款，實得 {len(ok)}"
    for model in ("AWUS036AXM", "AWUS036AXML"):
        row = next(r for r in rows if r[0].startswith(f"[{model}]"))
        assert "❌" in row[10], f"{loc} {model} 端到端應為失敗"


@pytest.mark.parametrize("loc", LOCALES)
def test_acs_eacs_5ghz_ap_note(loc):
    """ACS / EACS 的 5 GHz AP 實測是 802.11a 20 MHz，VHT80 未測。"""
    rows = _spec_rows(loc)
    for model in ("AWUS036ACS", "AWUS036EACS"):
        row = next(r for r in rows if r[0].startswith(f"[{model}]"))
        assert "802.11a" in row[13] and "20 MHz" in row[13], \
            f"{loc} {model} 的 AP 欄缺少 5 GHz 頻寬註記：{row[13]!r}"
