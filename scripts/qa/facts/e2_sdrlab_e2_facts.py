#!/usr/bin/env python3
"""SDRLab Phase E2 facts (no authorized claims; official-only rtl-sdr-v4; no TRX-duo upper limit;
wifi-multiboard = store-listed content only; leftover fixes). Run from repo root. Exit 1 on failure."""
import re, sys, pathlib

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
PAGES = ["rtl-sdr-v4", "trx-duo", "h4m", "flipper-5g", "flipper-nrf24", "flipper-wifi-multiboard", "flipper-ethernet"]
BASE = pathlib.Path("content")
fails = 0


def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails += 1


def read(loc, page):
    p = BASE / loc / "products/sdrlab" / (page + "/_index.md" if page else "_index.md")
    return p.read_text(encoding="utf-8")


def fm(t):
    return t.split("---")[1]


def field(t, name):
    m = re.search(rf'^{name}:\s*"?(.*?)"?\s*$', fm(t), re.M)
    return m.group(1) if m else ""


def ai_para(t, hub=False):
    body = t.split("---", 2)[2]
    body = body.split("\n## ")[0]
    out = []
    for blk in re.split(r"\n\s*\n", body):
        b = blk.strip()
        if not b or b.startswith(("#", ">", "{{<", "---", "![", "<")):
            continue
        out.append(b)
    if hub:
        out = [o for o in out if "Yopitek" in o]
    return out[0] if out else ""


# ---- 1. no authorization / distributor wording (all locales, hub + 7 pages)
BAD_AUTH = re.compile(
    r"(?i)authori[sz]ed\s+(taiwan\s+)?(distributor|dealer|reseller)|distributor|distributed in|reseller|dealer"
    r"|經銷|经销|代理|授權經銷|台灣授權|台湾授权|distribuye|distribui\b|distribue\b|vertreibt|توزع")
for loc in LOCALES:
    for page in [""] + PAGES:
        t = read(loc, page)
        m = BAD_AUTH.search(t)
        check(m is None, f"{loc}/{page or 'hub'}: no authorized/distributor wording" + (f" (hit: {m.group(0)})" if m else ""))

# ---- 2. en / zh-tw seo_title, description, AI paragraph
for page in [""] + PAGES:
    te, tz = read("en", page), read("zh-tw", page)
    se, sz = field(te, "seo_title"), field(tz, "seo_title")
    check(len(se) <= 60 and "SDRLab Taiwan | Yopitek" in se and not re.search("(?i)authori|ALFA", se), f"en/{page or 'hub'}: seo_title format ({se})")
    check(len(sz) <= 60 and "SDRLab 台灣 | Yopitek" in sz and "授權" not in sz, f"zh-tw/{page or 'hub'}: seo_title format ({sz})")
    de, dz = field(te, "description"), field(tz, "description")
    check(120 <= len(de) <= 160, f"en/{page or 'hub'}: description len {len(de)}")
    check(50 <= len(dz) <= 90, f"zh-tw/{page or 'hub'}: description len {len(dz)}")
    w = len(ai_para(te, not page).split())
    c = len(re.sub(r"\s", "", ai_para(tz, not page)))
    check(40 <= w <= 60, f"en/{page or 'hub'}: AI paragraph words {w}")
    check(60 <= c <= 100, f"zh-tw/{page or 'hub'}: AI paragraph chars {c}")
    for loc, t in (("en", te), ("zh-tw", tz)):
        n = len(re.findall(r"^\s+- question:", fm(t), re.M)) if page else 3
        check(n >= 3, f"{loc}/{page or 'hub'}: FAQ >= 3 ({n})")

# ---- 3. rtl-sdr-v4: official-only facts
RTL_BAD = [
    (r"\b8[- ]?(bit|bits)\b|8-бит|8 бит", "8-bit"),
    (r"3[.,]2\s*(MHz|МГц)", "3.2 MHz bandwidth"),
    (r"(?i)triple-notch|三路分波|3 系統のダイプレクサー|triple notch|triple-?filtre|notch triple", "triple-notch"),
    (r"1[.,]7\s*(GHz|ГГц)", "1.7 GHz"),
    (r"USB 2\.0", "USB 2.0"),
    (r"(?i)alumin|鋁|铝|アルミ|алюмин|ألومني", "aluminum"),
    (r"Osmocom", "Osmocom claim"),
    (r"(?i)DC-shorted|DC short|直流短路|直流短絡|DC-kurzgeschlossen|cortocircuito|court-circuit|закорочен|مقصور|curto-circuito|DC \(short|短絡", "DC-short advice"),
    (r"24\s*(MHz|МГц)", "24 MHz claim"),
]
RTL_MUST = [r"R828D", r"28[.,]8", r"4[.,]5 ?V", r"180 ?mA", r"1[.,]766", r"https://www\.rtl-sdr\.com/v4/", r"1 ?PPM"]
for loc in LOCALES:
    t = read(loc, "rtl-sdr-v4")
    for rx, name in RTL_BAD:
        check(re.search(rx, t) is None, f"{loc}/rtl-sdr-v4: must-not {name}")
    for rx in RTL_MUST:
        check(re.search(rx, t) is not None, f"{loc}/rtl-sdr-v4: must /{rx}/")
t = read("zh-cn", "rtl-sdr-v4")
check(re.search("[頻轉鋁調換數據準內採專屬圖觀監號體變關機組統雜訊靈敏壓縮載動權]", t) is None, "zh-cn/rtl-sdr-v4: no traditional characters")

# ---- 4. trx-duo: no receive upper limit
for loc in LOCALES:
    t = read(loc, "trx-duo")
    check(re.search(r"60\s?(MHz|МГц)", t) is None, f"{loc}/trx-duo: no 60 MHz")
    check(re.search(r"10\s?(kHz|кГц)", t) is None, f"{loc}/trx-duo: no receive range row")
    check(re.search(r"2[.,]5 ?mW", t) is None, f"{loc}/trx-duo: no derived 2.5 mW row")
    check("LTC2208" in t and "Red Pitaya" in t, f"{loc}/trx-duo: core facts kept")

# ---- 5. wifi multiboard: store-listed content only
WIFI_BAD = [r"300", r"928", r"\bASK\b", r"\bOOK\b", r"\bFSK\b", r"Marauder", r"ESP8266", r"ESP32", r"(?i)3[- ]in[- ]1|三合一|3 в 1|3 en 1|3 em 1|3-en-1|3 合 1|3 つ|tout-en-un",
            r"(?i)mousejacker", r"(?i)sniff|嗅探|スニッ|嗅探|إستنشاق|التنصت|escuch|farejamento|сниф|прослуш|écoute", r"Nordic|nRF24L01|Texas Instruments", r"(?i)red team|紅隊|红队|レッドチーム"]
WIFI_MUST = [r"NRF24", r"CC1101", r"GPS", r"MH-Z19", r"BME280", r"CO2|CO₂|二氧化碳", r"Air[- ]Mouse", r"VariantsId=10382"]
for loc in LOCALES:
    t = read(loc, "flipper-wifi-multiboard")
    for rx in WIFI_BAD:
        check(re.search(rx, t) is None, f"{loc}/wifi: must-not /{rx[:30]}/")
    for rx in WIFI_MUST:
        check(re.search(rx, t) is not None, f"{loc}/wifi: must /{rx}/")
    h = read(loc, "")
    check("ESP8266" not in h and "ESP32" not in h, f"{loc}/hub: no ESP8266/ESP32 on wifi card")

# ---- 2b. disputed Sub-GHz numbers gone everywhere in sdrlab pages
for loc in LOCALES:
    for page in [""] + PAGES:
        t = read(loc, page)
        check(re.search(r"300\s*[–〜~-]\s*928|315\s*[–〜~-]\s*9\d\d|315–900", t) is None, f"{loc}/{page or 'hub'}: no Sub-GHz band numbers")

# ---- 6. leftover fixes
t = read("ja", "flipper-5g")
check("タッチ" not in t and "修正済み" not in t and "原文" not in t, "ja/flipper-5g: no touch / internal note")
t = read("zh-cn", "flipper-5g")
check(not re.search(r"source_url:|待上架|revision:", t), "zh-cn/flipper-5g: no duplicate front matter")
check(len(re.findall(r"(?m)^title:", t)) == 1, "zh-cn/flipper-5g: exactly one title:")
for loc in ("ar", "de", "es", "pt", "ru", "fr"):
    t = read(loc, "flipper-5g")
    check(re.search(r"[一-鿿]", t) is None, f"{loc}/flipper-5g: no stray CJK")
check("Externo (External)" not in read("es", "flipper-5g") and re.search(r"\| \*\*External\*\* \|", read("es", "flipper-5g")), "es/flipper-5g: Sub-GHz value is **External**")
t = read("ar", "flipper-5g")
h2 = re.findall(r"(?m)^## (.+)$", t)
check(len(h2) == 6 and [x.split(":")[0].strip() for x in h2] == ["أولاً", "ثانياً", "ثالثاً", "رابعاً", "خامساً", "سادساً"], f"ar/flipper-5g: six ordered H2 ({len(h2)})")
for loc in LOCALES:
    t = read(loc, "h4m")
    if loc != "en":
        check("The complete beginner guide" not in t and "Open manual in full screen" not in t, f"{loc}/h4m: user manual block localized")
t = read("zh-tw", "h4m")
check(re.search(r"使用手冊", t) and re.search(r"全螢幕", t), "zh-tw/h4m: manual block in Taiwan Chinese")

print(f"\nfailures: {fails}")
sys.exit(1 if fails else 0)
