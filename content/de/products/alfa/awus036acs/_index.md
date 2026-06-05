---
title: "ALFA AWUS036ACS — AC600 Dual-Band USB-Adapter (Einstieg in die Sicherheitsforschung)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 Dual-Band USB 2.0, 1× 2-dBi-RP-SMA-Antenne (abnehmbar), unterstützt Monitor-Modus und Paketinjektion — idealer Einsteiger-Adapter für die Sicherheitsforschung."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Budget"]
---

{{< alert "warning" >}}
**Rechtlicher Hinweis**: Der Monitor-Modus und die Paketinjektion sind ausschließlich für autorisierte Sicherheitstests, Bildungsforschung und legale Penetrationstests vorgesehen. Stellen Sie stets sicher, dass Sie eine ausdrückliche Genehmigung des Eigentümers des Zielnetzwerks besitzen.
{{< /alert >}}

## Produktübersicht

Der AWUS036ACS ist Alfas günstigster Einstieg in die Dual-Band-802.11ac-Produktreihe mit Monitor-Modus und Paketinjektion. Angetrieben vom Realtek RTL8811AU Chipsatz ist er kompakt und leicht, mit einer einzelnen abnehmbaren RP-SMA-Antenne, die für bessere Reichweite aufgerüstet werden kann. Auch wenn er nicht so leistungsstark wie der ACH oder ACM ist, ist er eine praktische Wahl für Einsteiger in die drahtlose Sicherheitsforschung oder Benutzer, die einen kostengünstigen 5-GHz-Adapter mit externer Antennenfähigkeit benötigen.

> **macOS-Hinweis:** Alle ALFA-Adapter bieten eingeschränkte macOS-Unterstützung. macOS 10.15 Catalina und höher sowie alle Apple Silicon (M1/M2/M3) Macs werden **nicht unterstützt**. Der AWUS036ACS unterstützt bis zu macOS 10.14 Mojave (nur Intel-Mac).

## Hauptmerkmale

- Realtek RTL8811AU Chipsatz — Monitor-Modus und Paketinjektion unterstützt
- WiFi 5 (802.11ac) Dual-Band — 2,4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- 1× RP-SMA-Buchse mit 1× 2-dBi-Mini-Antenne (abnehmbar) — aufrüstbar auf Panel- oder Hochgewinn-Antennen
- Kompakter Formfaktor — kleines Profil für einfache Portabilität
- USB 2.0 (USB-A)-Schnittstelle — kompatibel mit jedem USB-Port
- Kompatibel mit Alfa APA-M25 Dual-Band-Panel-Antenne für direktionalen Empfang
- Unterstützt Kali Linux auf Raspberry Pi (KaliPi) — Treiberinstallation über DKMS

## Technische Spezifikationen

| Parameter | Wert |
|---|---|
| Chipsatz | Realtek RTL8811AU |
| WLAN-Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequenzbänder | 2,4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| Kombinierte Max.-Geschwindigkeit | AC600 (150 + 433 Mbps) |
| Antennenanschluss | 1× RP-SMA-Buchse |
| Mitgelieferte Antenne | 1× Dual-Band-Dipol-Mini, 2 dBi |
| USB-Schnittstelle | USB 2.0 Typ-A |
| Empfangsempfindlichkeit | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| WLAN-Sicherheit | WPA2 / WPA / WEP / 802.1X |
| Herkunftsland | Taiwan |

> ⚠️ **HINWEIS:** Nur USB 2.0 — maximale Datenbusgeschwindigkeit 480 Mbps. Durchsatz auf 433 Mbps begrenzt. Für maximale Geschwindigkeit AWUS036ACM oder AWUS036ACH mit USB 3.0 verwenden.

## Betriebssystem-Unterstützung

| Betriebssystem | Status | Hinweise |
|---|---|---|
| Windows XP–11 | ✅ Unterstützt | Treiber von der Alfa-Website verfügbar |
| macOS 10.5–10.14 | ⚠️ Eingeschränkt | macOS 10.15+ und Apple Silicon NICHT unterstützt |
| Ubuntu | ✅ Unterstützt | Manuelle DKMS-Treiberinstallation erforderlich (morrownr/8821au). Keine In-Kernel-Unterstützung. |
| Kali Linux | ✅ Unterstützt | Monitor-Modus + Paketinjektion unterstützt. Community-Treiber von morrownr GitHub. |
| NetHunter (Android) | ✅ Unterstützt | OTG-USB-Verbindung; RTL8811AU hat bestätigte NetHunter-Kompatibilität |

## Hardware-Kompatibilität

| Hardware | Status | Hinweise |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ Unterstützt | KaliPi-spezifische Installation über morrownr DKMS verfügbar. |
| Desktop/Laptop-PC | ✅ Unterstützt | Standard-USB-A |
| Mac (Intel) | ⚠️ Eingeschränkt | Nur macOS 10.5–10.14 |

## Erweiterte Funktionen

| Funktion | Status |
|---|---|
| Monitor-Modus | ✅ Ja |
| Paketinjektion | ✅ Ja |
| Soft-AP-Modus | ✅ Ja |
| Bluetooth | ❌ Nein |
| VIF | ⚠️ Eingeschränkt |

## Lieferumfang

- 1× AWUS036ACS-Adapter
- 1× Abnehmbare 2-dBi-Dual-Band-Mini-Dipol-Antenne

## Ressourcen & Links

| Ressource | Link |
|---|---|
| Offizielle Produktseite | https://www.alfa.com.tw/products/awus036acs_1 |
| Offizielle Dokumentation | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux-Treiber (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## Datenblatt-Download

[📄 AWUS036ACS Datenblatt herunterladen](/docs/alfa/AWUS036ACS_spec.pdf)

## Galerie

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

---

## Kompatible Antennen-Upgrades

Alle ALFA-Adapter verfügen über einen Standard-RP-SMA-Anschluss. Rüsten Sie mit einer optionalen externen Antenne für größere Reichweite und mehr Gewinn auf:

| Antenne | Frequenz | Gewinn | Typ |
|---------|-----------|------|------|
| [ALFA APA-M04](/de/products/alfa/apa-m04/) | 2,4 GHz | 7 dBi | Indoor-Panel |
| [ALFA APA-M25](/de/products/alfa/apa-m25/) | 2,4 / 5 GHz | 7 dBi | Dual-Band-Indoor-Panel |
| [ALFA APA-M25-6E](/de/products/alfa/apa-m25-6e/) | 2,4 / 5 / 6 GHz | 7 dBi | Tri-Band-Indoor-Panel |
| [ARS 25-57A](/de/products/alfa/ars-25-57a/) | 2,4 / 5 GHz | 2,5 / 7 dBi | Outdoor-Omni |
| [ARS NT5B7](/de/products/alfa/ars-nt5b7/) | 2,4 / 5 GHz | 5 / 7 dBi | Omni |

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
