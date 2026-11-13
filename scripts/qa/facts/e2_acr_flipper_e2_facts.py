#!/usr/bin/env python3
"""Phase E2 facts check for ACR + Flipper Zero product pages (stdlib only, run from repo root).
Decision 1: no authorization/distributor claims (10 locales), new seo_title format.
Decision 2: no disputed numbers (Flipper Sub-GHz band numbers, ACR1552U ISO 15693 speed).
Decision 3: official-sourced fixes (NFC row, weight, 1552U colour/cable, ACR122U RoHS 2, VGM video out)."""
import re, sys
from pathlib import Path

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
AUTH = re.compile(
    r"authori[sz]ed\s+(?:taiwan\s+)?(?:\w+\s+)?(?:distributor|dealer|reseller|partner)|distributor|reseller|"
    r"授權(?:經銷|代理)|台灣授權|授权(?:经销|代理)|台湾授权|經銷|经销|代理|"
    r"vertreibt|distribuye|distribui\b|distribue\b|توزع|موزع|وكيل|дистрибь|дилер", re.I)
SUBGHZ_NUM = re.compile(r"\b(?:300|315|433|868|915|928|900)\b")
fails = total = 0


def check(ok, msg):
    global fails, total
    total += 1
    fails += not ok
    print(("PASS " if ok else "FAIL ") + msg)


def body_and_fm(path):
    t = Path(path).read_text(encoding="utf-8")
    _, fm, body = t.split("---", 2)
    return fm, body


def fm_get(fm, key):
    m = re.search(rf'^{key}:\s*"(.*)"\s*$', fm, re.M)
    return m.group(1) if m else ""


def ai_paragraph(body):
    pre = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
    paras = [p.strip() for p in re.split(r"\n\s*\n", pre) if p.strip() and not p.strip().startswith("{{<")
             and not p.strip().startswith("**") and len(p.split()) > 5]
    return paras[-1] if paras else ""


def files(loc, brand):
    return sorted(Path(f"content/{loc}/products/{brand}").rglob("*.md"))


# ---- Decision 1: no authorization claims, any locale
for L in LOCALES:
    for brand in ("acr", "flipperzero"):
        for f in files(L, brand):
            hits = [m.group(0) for m in AUTH.finditer(f.read_text(encoding="utf-8"))]
            check(not hits, f"no authorization/distributor words {hits[:3]} :: {f}")

# ---- Decision 1: seo_title format (en, zh-tw)
EN_T = {"acr/_index.md": "ACR Series | ACS Taiwan | Yopitek", "acr/acr122u/_index.md": "ACR122U | ACS Taiwan | Yopitek",
        "acr/acr1252u/_index.md": "ACR1252U | ACS Taiwan | Yopitek", "acr/acr1552u/_index.md": "ACR1552U | ACS Taiwan | Yopitek",
        "flipperzero/_index.md": "Flipper Zero Series | Flipper Taiwan | Yopitek",
        "flipperzero/flipper-zero/_index.md": "Flipper Zero | Flipper Taiwan | Yopitek",
        "flipperzero/wifi-devboard/_index.md": "WiFi Devboard | Flipper Taiwan | Yopitek",
        "flipperzero/video-game-module/_index.md": "Video Game Module | Flipper Taiwan | Yopitek",
        "flipperzero/silicone-case/_index.md": "Silicone Case | Flipper Taiwan | Yopitek"}
ZH_T = {"acr/_index.md": "ACR 系列 ACS 台灣 | Yopitek", "acr/acr122u/_index.md": "ACR122U ACS 台灣 | Yopitek",
        "acr/acr1252u/_index.md": "ACR1252U ACS 台灣 | Yopitek", "acr/acr1552u/_index.md": "ACR1552U ACS 台灣 | Yopitek",
        "flipperzero/_index.md": "Flipper Zero 系列 Flipper 台灣 | Yopitek",
        "flipperzero/flipper-zero/_index.md": "Flipper Zero 台灣 | Yopitek",
        "flipperzero/wifi-devboard/_index.md": "WiFi Devboard Flipper 台灣 | Yopitek",
        "flipperzero/video-game-module/_index.md": "Video Game Module Flipper 台灣 | Yopitek",
        "flipperzero/silicone-case/_index.md": "Silicone Case Flipper 台灣 | Yopitek"}
for loc, table in (("en", EN_T), ("zh-tw", ZH_T)):
    for rel, want in table.items():
        p = f"content/{loc}/products/{rel}"
        fm, body = body_and_fm(p)
        got = fm_get(fm, "seo_title")
        check(got == want and len(got) <= 60, f"seo_title {got!r} == {want!r} :: {p}")
        ai = ai_paragraph(body)
        n = len(ai.split()) if loc == "en" else len(re.sub(r"\s", "", ai))
        lo, hi = (40, 60) if loc == "en" else (60, 100)
        check(lo <= n <= hi, f"AI paragraph size {n} in {lo}-{hi} :: {p}")

# ---- Decision 1: "where to buy" FAQ reworded (en, zh-tw)
for loc, rx in (("en", r"How (?:do|can) I (?:buy|request)"), ("zh-tw", r"如何.*(?:購買|詢價)")):
    for sub in ("wifi-devboard", "video-game-module"):
        p = f"content/{loc}/products/flipperzero/{sub}/_index.md"
        fm, _ = body_and_fm(p)
        check(re.search(rx, fm) is not None and "Where can I buy" not in fm and "哪裡可以購買" not in fm,
              f"FAQ buy question reworded :: {p}")

# ---- Decision 2: no Sub-GHz band numbers anywhere in flipperzero pages
for L in LOCALES:
    for f in files(L, "flipperzero"):
        hits = SUBGHZ_NUM.findall(f.read_text(encoding="utf-8"))
        check(not hits, f"no Sub-GHz band numbers {hits[:3]} :: {f}")
    p = f"content/{L}/products/flipperzero/flipper-zero/_index.md"
    check("Sub-GHz" in Path(p).read_text(encoding="utf-8"), f"'Sub-GHz' term kept :: {p}")

# ---- Decision 2: ACR1552U has no ISO 15693 speed
for L in LOCALES:
    p = f"content/{L}/products/acr/acr1552u/_index.md"
    t = Path(p).read_text(encoding="utf-8")
    check(re.search(r"\b(?:26|53)\s*[kK][bB]?(?:ps|it)", t) is None, f"no ISO 15693 speed :: {p}")

# ---- Decision 3: official-sourced fixes
WHITE = {"en": "White", "zh-tw": "白色", "zh-cn": "白色", "ja": "ホワイト", "ar": "أبيض", "es": "Blanco",
         "pt": "Branco", "ru": "Белый", "de": "Weiß", "fr": "Blanc"}
for L in LOCALES:
    p = f"content/{L}/products/acr/acr1552u/_index.md"
    lines = Path(p).read_text(encoding="utf-8").splitlines()
    check(any(l.startswith("|") and WHITE[L].lower() in l.lower() for l in lines), f"1552U colour white :: {p}")
    check(any(l.startswith("|") and re.search(r"\| 1 [mм]\b", l) for l in lines), f"1552U cable 1 m :: {p}")
    p = f"content/{L}/products/acr/acr122u/_index.md"
    comp = [l for l in Path(p).read_text(encoding="utf-8").splitlines() if "CCID" in l and l.startswith("|")]
    check(bool(comp) and re.search(r"RoHS 2", comp[0]) is not None, f"ACR122U compliance RoHS 2 :: {p}")
    p = f"content/{L}/products/flipperzero/flipper-zero/_index.md"
    t = Path(p).read_text(encoding="utf-8")
    nfc = [l for l in t.splitlines() if l.startswith("| NFC")]
    check(bool(nfc) and "15693" not in nfc[0] and "FeliCa" in nfc[0] and "iClass" in nfc[0],
          f"NFC row official protocols, no 15693 :: {p}")
    check(re.search(r"^\|[^|]+\| 102 (?:g|г)\s*\|", t, re.M) is not None, f"weight 102 g row :: {p}")
    p = f"content/{L}/products/flipperzero/video-game-module/_index.md"
    check("DVI-D" in Path(p).read_text(encoding="utf-8"), f"VGM video out DVI-D :: {p}")

print(f"\n{total - fails}/{total} passed, {fails} failed")
sys.exit(1 if fails else 0)
