#!/usr/bin/env python3
"""Generate FR and DE product _index.md files from EN templates."""

import os

PRODUCTS = [
    {"slug": "awus036axml", "dir": "alfa"},
    {"slug": "awus036axm", "dir": "alfa"},
    {"slug": "awus036ax", "dir": "alfa"},
    {"slug": "awus036axer", "dir": "alfa"},
    {"slug": "awus036ach", "dir": "alfa"},
    {"slug": "awus036acm", "dir": "alfa"},
    {"slug": "awus036acs", "dir": "alfa"},
    {"slug": "awus036eacs", "dir": "alfa"},
    {"slug": "awus1900", "dir": "alfa"},
    {"slug": "awus036nhv", "dir": "alfa"},
    {"slug": "awus036achm", "dir": "alfa"},
    {"slug": "apa-m04", "dir": "alfa"},
    {"slug": "apa-m25", "dir": "alfa"},
    {"slug": "apa-m25-6e", "dir": "alfa"},
    {"slug": "ars-25-57a", "dir": "alfa"},
    {"slug": "ars-nt5b7", "dir": "alfa"},
]

FR_DIR = "content/fr/products/alfa"
DE_DIR = "content/de/products/alfa"

FR_TITLE = {
    "awus036axml": "ALFA AWUS036AXML — Adaptateur USB Wi-Fi 6E Tri-Band USB-C",
    "awus036axm": "ALFA AWUS036AXM — Adaptateur USB Wi-Fi 6E Tri-Band",
    "awus036ax": "ALFA AWUS036AX — Adaptateur USB Wi-Fi 6 Dual-Band",
    "awus036axer": "ALFA AWUS036AXER — Adaptateur USB Wi-Fi 6 Ultra-plat",
    "awus036ach": "ALFA AWUS036ACH — Adaptateur USB Wi-Fi 5 AC1200",
    "awus036acm": "ALFA AWUS036ACM — Adaptateur USB Wi-Fi 5 AC1200",
    "awus036acs": "ALFA AWUS036ACS — Adaptateur USB Wi-Fi 5 AC433",
    "awus036eacs": "ALFA AWUS036EACS — Adaptateur USB Wi-Fi 5 AC600",
    "awus1900": "ALFA AWUS1900 — Adaptateur USB Wi-Fi 5 AC1900",
    "awus036nhv": "ALFA AWUS036N-HV — Adaptateur USB Wi-Fi 5 N",
    "awus036achm": "ALFA AWUS036ACHM — Adaptateur USB Wi-Fi 5 AC1200",
    "apa-m04": "ALFA APA-M04 — Antenne Panel Interieur 2,4 GHz",
    "apa-m25": "ALFA APA-M25 — Antenne Panel Double Bande 2,4/5 GHz",
    "apa-m25-6e": "ALFA APA-M25-6E — Antenne Directionnelle Tri-Bande WiFi 6E",
    "ars-25-57a": "ALFA ARS 25-57A — Antenne Omnidirectionnelle Double Bande",
    "ars-nt5b7": "ALFA ARS NT5B7 — Antenne Dipolaire WiFi 7 Tri-Bande",
}

DE_TITLE = {
    "awus036axml": "ALFA AWUS036AXML — Wi-Fi 6E USB-C Tri-Band USB Adapter",
    "awus036axm": "ALFA AWUS036AXM — Wi-Fi 6E USB Tri-Band Adapter",
    "awus036ax": "ALFA AWUS036AX — Wi-Fi 6 Dual-Band USB Adapter",
    "awus036axer": "ALFA AWUS036AXER — Wi-Fi 6 Dual-Band Ultra-Slim Adapter",
    "awus036ach": "ALFA AWUS036ACH — Wi-Fi 5 AC1200 USB Adapter",
    "awus036acm": "ALFA AWUS036ACM — Wi-Fi 5 AC1200 USB Adapter",
    "awus036acs": "ALFA AWUS036ACS — Wi-Fi 5 AC433 USB Adapter",
    "awus036eacs": "ALFA AWUS036EACS — Wi-Fi 5 AC600 USB Adapter",
    "awus1900": "ALFA AWUS1900 — Wi-Fi 5 AC1900 USB Adapter",
    "awus036nhv": "ALFA AWUS036N-HV — Wi-Fi N USB Adapter Hochleistung",
    "awus036achm": "ALFA AWUS036ACHM — Wi-Fi 5 AC1200 USB Adapter",
    "apa-m04": "ALFA APA-M04 — 2,4 GHz Innenpannen-Direktantenne",
    "apa-m25": "ALFA APA-M25 — Dual-Band 2,4/5 GHz Innenpannenantenne",
    "apa-m25-6e": "ALFA APA-M25-6E — Tri-Band WiFi 6E Innenrichtantenne",
    "ars-25-57a": "ALFA ARS 25-57A — Dual-Band Omnidirektionalantenne",
    "ars-nt5b7": "ALFA ARS NT5B7 — WiFi 7 Tri-Band Dipolantenne",
}

# Unique placeholders to avoid f-string brace conflicts
HUGO_L = "\x00L\x00"   # becomes {{
HUGO_R = "\x00R\x00"   # becomes }}


def gen(product, lang):
    slug = product["slug"]
    title_map = FR_TITLE if lang == "fr" else DE_TITLE
    title = title_map.get(slug, f"ALFA {slug.upper()}")

    if lang == "fr":
        desc = f"Adaptateur Wi-Fi USB ALFA {slug.upper()} — distribue par Yopitek."
        intro = f"L'adaptateur ALFA {slug.upper()} est un adaptateur Wi-Fi USB haute puissance, idealement congu pour la recherche en securite et les reseaux."
        macos = "**Remarque macOS:** Tous les adaptateurs ALFA ont un support limite/pas de support macOS. macOS 11 Big Sur et plus tard, et Apple Silicon (M1/M2/M3) ne sont **PAS** supports. Le support macOS maximal est 10.15 Catalina sur les Mac Intel."
        features = [
            "Haute puissance et longue portee",
            "Support du mode monitor et packet injection",
            "Compatible Linux, Kali Linux, Windows",
            "Antenne detachable RP-SMA",
        ]
        specs = [
            ("Marque", "ALFA Network"),
            ("Type", "Adaptateur USB Wi-Fi"),
            ("Connecteur", "RP-SMA"),
            ("Pays d'origine", "TaIwan"),
        ]
        modes = [
            ("Station Mode", "Connexion reseau classique"),
            ("Monitor Mode", "Capture de paquets sans fil"),
            ("Master Mode", "Point d'acces"),
            ("Repeater Mode", "Extension de portee"),
        ]
        downloads_link = "[page d'Assistance Technique](/fr/support/)"
        downloads_text = "Consultez la pour les pilotes officiels ALFA Network."
        contact_link = "[Contactez-nous](/fr/contact/)"
        contact_text = "Besoin d'un devis ou d'un prix en gros?"
    else:
        desc = f"ALFA {slug.upper()} USB-Wi-Fi-Adapter — verbreitet von Yopitek."
        intro = f"Der ALFA {slug.upper()} USB-Wi-Fi-Adapter ist ein Hochleistungsadapter, ideal fUr Sicherheitsforschung und Netzwerke."
        macos = "**macOS-Hinweis:** Alle ALFA-Adapter haben eingeschrankte/keine macOS-Unterstutzung. macOS 11 Big Sur und spater, und Apple Silicon (M1/M2/M3) werden **NICHT** unterstutzt. Maximale macOS-Unterstutzung ist 10.15 Catalina auf Intel-Macs."
        features = [
            "Hochleistung und lange Reichweite",
            "Unterstutzt Monitor-Mode und Packet Injection",
            "Kompatibel mit Linux, Kali Linux, Windows",
            "Abnehmbare RP-SMA Antenne",
        ]
        specs = [
            ("Marke", "ALFA Network"),
            ("Typ", "USB-Wi-Fi-Adapter"),
            ("Connector", "RP-SMA"),
            ("Herkunft", "Taiwuan"),
        ]
        modes = [
            ("Station Mode", "Klassische Netzwerkverbindung"),
            ("Monitor-Mode", "Funk-Paketerfassung"),
            ("Master Mode", "Access Point"),
            ("Repeater Mode", "ReichweitenvergruBerung"),
        ]
        downloads_link = "[Technischen Support-Seite](/de/support/)"
        downloads_text = "Offizielle ALFA Network Treiber-Downloads finden Sie auf der"
        contact_link = "[Kontaktieren Sie uns](/de/contact/)"
        contact_text = "Brauchen Sie ein Angebot oder Mengenpreis?"

    image = f"/images/products/alfa/{slug}.png"

    lines = [
        "---",
        f'title: "{title}"',
        f'description: "{desc}"',
        "date: 2026-03-12",
        "draft: false",
        "showBreadcrumbs: true",
        "showTableOfContents: true",
        'brands: ["alfa"]',
        f'featureimage: "{image}"',
        "---",
        "",
        "## " + ("Apercu du produit" if lang == "fr" else "Produkt-UBersicht"),
        "",
        intro,
        "",
        f"{HUGO_L} alert \"circle-info\" {HUGO_R}",
        macos,
        f"{HUGO_L} /alert {HUGO_R}",
        "",
        "## " + ("Caracteristiques principales" if lang == "fr" else "Hauptmerkmale"),
        "",
    ]

    for feat in features:
        lines.append(f"- {feat}")

    lines.extend(["", "## " + ("Specifications techniques" if lang == "fr" else "Technische Spezifikationen"), ""])

    header = "| " + ("Parametre" if lang == "fr" else "Parameter") + " | " + ("Specification" if lang == "fr" else "Spezifikation") + " |"
    lines.append(header)
    lines.append("|" + "-" * 7 + "|" + "-" * 7 + "|" + "-" * 7 + "|")
    for k, v in specs:
        lines.append(f"| {k} | {v} |")

    section_title = "Modes de fonctionnement" if lang == "fr" else "Betriebsmodi"
    lines.extend(["", f"## {section_title}", ""])
    for k, v in modes:
        lines.append(f"- **{k}:** {v}")

    if lang == "fr":
        lines.extend([
            "",
            "## Telechargements",
            "",
            f"Consultez la {downloads_text} {downloads_link}.",
            "",
            "---",
            "",
            f"{contact_text} {contact_link}",
            "",
            "---",
            "",
            f"{HUGO_L} gallery {HUGO_R}",
            f'  <img src="{image}" alt="{title}" />',
            f"{HUGO_L} /gallery {HUGO_R}",
        ])
    else:
        lines.extend([
            "",
            "## Treiber-Downloads",
            "",
            f"{downloads_text} {downloads_link}.",
            "",
            "---",
            "",
            f"{contact_text} {contact_link}",
            "",
            "---",
            "",
            f"{HUGO_L} gallery {HUGO_R}",
            f'  <img src="{image}" alt="{title}" />',
            f"{HUGO_L} /gallery {HUGO_R}",
        ])

    result = "\n".join(lines)
    return (result.replace(HUGO_L, "{{<").replace(HUGO_R, "}}"))


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for product in PRODUCTS:
        slug = product["slug"]

        for lang, dir_name in [("fr", FR_DIR), ("de", DE_DIR)]:
            out_dir = os.path.join(base, dir_name, slug)
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "_index.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(gen(product, lang))
            print(f"{lang.upper()}: {dir_name}/{slug}/_index.md")

    print(f"Done! Generated {len(PRODUCTS) * 2} product pages total.")


if __name__ == "__main__":
    main()
