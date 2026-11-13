#!/usr/bin/env python3
"""SDRLab 產品頁事實斷言（Phase C）。從 repo 根目錄執行。失敗 exit 1。"""
import re, sys, pathlib

LOCALES = ["zh-tw", "zh-cn", "en", "ja", "ar", "es", "pt", "ru", "de", "fr"]
BASE = pathlib.Path("content")
S = "https://opensourcesdrlab.com/products/"
URLS = {
    "flipper-5g": S + "opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754",
    "rtl-sdr-v4": S + "rtl-sdr-v4",
    "h4m": S + "h4m-receiver-and-spectrum-analyzer?VariantsId=10129",
    "flipper-nrf24": S + "improved-version-nrf24-module-and-gpio-for-flipper-for-sniffer-and-mouse-jacker?VariantsId=10383",
    "flipper-ethernet": S + "for-flipper-zero-ethernet-test-module-wired-network-module-devboard-for-flipper-zero-attachment-accessory",
    "trx-duo": S + "trx-duo-compatible-with-red-pitaya-sdr-dual-16bit-adc-zynq7010?VariantsId=10980",
}
# (page) -> (must regexes, must-not regexes)
M = lambda *a: list(a)
RULES = {
    "flipper-5g": (
        M(r"ESP32-C5", r"3\s*dBi", r"20\s*dBi", r"11\s*cm", r"800\s*mAh", r"A07", r"10 dBm", r"TVS",
          r"2[.,]8", r"Marauder", r"USB-?\s?C|Type-?C", r"Sub-GHz.{0,80}External|External"),
        M(r"RTL8720", r"(?<![\d.])5\s*dBi", r"BLE", r"BR/EDR", r"FAT32", r"32\s*GB", r"microSD",
          r"\.pcap", r"802\.11", r"Wi-?Fi\s?6", r"240\s*MHz", r"RISC-V", r"5\s*V\s*/\s*2(\.4)?\s*A",
          r"90\s*[×x]\s*58", r"\b3D\b", r"(?i)\bblack\b|黑|黒|أسود|negro|preto|черн|schwarz"),
    ),
    "h4m": (
        M(r"R10C", r"240\s*[×x]\s*320", r"microSD", r"3\.5\s*mm", r"ABS"),
        M(r"R10c", r"MAX2837", r"I2C",
          r"(?i)acrylic|壓克力|压克力|亚克力|アクリル|أكريليك|acrílic|акрил|acryl"),
    ),
    "flipper-ethernet": (
        M(r"(?i)ping", r"MAC"),
        M(r"(?i)penetration|滲透|渗透|ペネトレーション|ペンテスト|الاختراق|penetración|penetração|пентест|проникновени|penetrationstest|pénétration",
          r"(?i)educational|教學|教学|教育|教材|educativ|éducati|bildung|educaç|образоват|التعليم|学習|実習"),
    ),
    "trx-duo": (
        M(r"LTC2208", r"Red Pitaya"),
        M(r"622", r"WSPR", r"HPSDR", r"(?i)linux",
          r"(?i)power amplifier|功放|功率放大|パワーアンプ|amplificador de potencia|усилител|leistungsverstärker|amplificateur de puissance|مضخم"),
    ),
    "rtl-sdr-v4": (M(r"23\s*cm", r"13\s*cm"), []),
    "flipper-nrf24": ([], []),
}
fails = 0
def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails += 1

for page in ["flipper-5g", "h4m", "flipper-ethernet", "trx-duo", "rtl-sdr-v4", "flipper-nrf24"]:
    must, mustnot = RULES[page]
    for loc in LOCALES:
        p = BASE / loc / "products/sdrlab" / page / "_index.md"
        if not p.exists():
            print(f"SKIP {loc}/{page} (no file)"); continue
        t = p.read_text(encoding="utf-8")
        check(URLS[page] in t, f"{loc}/{page}: has store URL")
        for r in must: check(re.search(r, t) is not None, f"{loc}/{page}: must /{r}/")
        for r in mustnot: check(re.search(r, t) is None, f"{loc}/{page}: must-not /{r}/")
        if page == "flipper-5g":
            fm = t.split("---")[1]
            m = re.search(r"^description:.*$", fm, re.M)
            check(m is None or "ESP32-C5" in m.group(0), f"{loc}/{page}: description (if any) has ESP32-C5")
            n = len(re.findall(r"^## ", t, re.M))
            check(n <= 6, f"{loc}/{page}: H2 count {n} <= 6 (pending-spec section removed)")
print(f"\nfailures: {fails}")
sys.exit(1 if fails else 0)
