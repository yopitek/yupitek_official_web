#!/usr/bin/env python3
"""Fail if ACR / Flipper Zero / HAK5 / SDR-Lab product content claims Yopitek is an authorized distributor/dealer.
Only ALFA Network may carry that claim. Usage (repo root): python3 scripts/qa/no_authorized_claims.py"""
import re, sys
from pathlib import Path

PATTERNS = [
    r"authori[sz]ed\s+(?:taiwan\s+)?(?:distributor|dealer|reseller|partner)", r"official\s+(?:taiwan\s+)?(?:distributor|reseller|dealer)",
    r"(?:distributor|reseller)\s+(?:authori[sz]ed|official)", r"authori[sz]ed\s+taiwan",
    r"授權(?:經銷|代理|經銷商|代理商)", r"台灣授權", r"授权(?:经销|代理)", r"台湾授权", r"(?:正規|正规|認定|认定)(?:販売)?(?:代理|経銷|经销|販売店)",
    r"autorisierte[rn]?\s+(?:distributor|händler|vertriebs\w*|fachhändler)", r"(?:distributeur|revendeur)\s+(?:agréé|autorisé)",
    r"(?:distribuidor|revendedor|distribuidora)\s+(?:autorizad[oa]|oficial)", r"autorizad[oa]\s+(?:en|de)\s+taiw", r"distribuidor\s+autorizado",
    r"(?:авторизованн\w+|официальн\w+)\s+(?:дистрибьютор|дилер)\w*", r"(?:موزع|الموزع|وكيل|الوكيل)\s+(?:ال)?معتمد",
    r"offizieller\s+(?:distributor|händler)", r"distributeur\s+officiel", r"authorized\s+distribution",
]
RX = re.compile("|".join(PATTERNS), re.I)
BRANDS = ("acr", "flipperzero", "hak5", "sdrlab")


def main() -> int:
    hits = 0
    for b in BRANDS:
        for f in sorted(Path("content").glob(f"*/products/{b}/**/*.md")):
            for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
                for m in RX.finditer(line):
                    hits += 1
                    print(f"{f}:{n}: {m.group(0)}")
    print(f"TOTAL hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
