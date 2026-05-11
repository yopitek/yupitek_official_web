---
title: "ALFA AWUS036ACM — AC1200 Dual-Band USB-3.0-Adapter (Bestes Linux Plug & Play)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 Dual-Band USB 3.0, In-Kernel-Linux-Treiber seit Kernel 4.19 (Plug & Play, keine Kompilierung). Voller Monitor-Modus, Paketinjektion und VIF-Unterstützung. Bester Alfa-Adapter für Raspberry Pi."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Dual-Band", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**Rechtlicher Hinweis**: Der Monitor-Modus und die Paketinjektion sind ausschließlich für autorisierte Sicherheitstests, Bildungsforschung und legale Penetrationstests vorgesehen. Stellen Sie sicher, dass Sie vor der Verwendung eine ausdrückliche Genehmigung des Eigentümers des Zielnetzwerks besitzen.
{{< /alert >}}

## Produktübersicht

Der AWUS036ACM ist die Top-Empfehlung für Linux-Benutzer, die ein problemloses Setup wünschen. Sein MediaTek MT7612U Chipsatz ist seit Kernel-Version 4.19 im Linux-Kernel integriert — er funktioniert also direkt nach dem Anschließen auf Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux und praktisch jeder modernen Distribution, ohne eine einzige Codezeile kompilieren zu müssen. Er entspricht dem AWUS036ACH in Größe und Antennenkonfiguration, verwendet jedoch MediaTeks zuverlässigen In-Kernel-Treiber. Monitor-Modus, Paketinjektion und VIF (Virtuelles Interface) werden vollständig unterstützt.

> **macOS-Hinweis:** Alle ALFA-Adapter bieten eingeschränkte oder keine macOS-Unterstützung. macOS 11+ und Apple Silicon (M1/M2/M3) werden **NICHT unterstützt**. Der AWUS036ACM unterstützt maximal macOS 10.12 Sierra — strenger als die meisten anderen Modelle.

## Hauptmerkmale

- MediaTek MT7612U Chipsatz — In-Kernel-Linux-Treiber seit Kernel 4.19 (Plug & Play, keine Kompilierung nötig)
- WiFi 5 (802.11ac) Dual-Band AC1200 — bis zu 867 Mbps bei 5 GHz, 300 Mbps bei 2,4 GHz
- 2× RP-SMA-Buchsen mit 2× 5-dBi-abnehmbaren Dual-Band-Antennen — identisches Format wie AWUS036ACH
- USB 3.0 (USB-A)-Schnittstelle
- Voller Monitor-Modus, Paketinjektion und AP-Modus
- VIF (Virtuelles Interface) Unterstützung in Kali Linux
- USB-3.0-Verlängerungskabel im Lieferumfang
- TAA-konform — geeignet für US-Regierungsbeschaffung (GSA-kompatibel)
- Funktioniert direkt auf Raspberry Pi OS — keine Treiberinstallation

## Technische Spezifikationen

| Parameter | Wert |
|-----------|-------|
| Chipsatz | MediaTek MT7612U |
| WLAN-Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequenzbänder | 2,4 GHz (2,412–2,472 GHz) · 5 GHz (5,15–5,825 GHz) |
| Kanalbreiten | 20 / 40 / 80 MHz |
| Max. Datenrate | 5 GHz: bis zu 867 Mbps · 2,4 GHz: bis zu 300 Mbps |
| Kombinierte Max.-Geschwindigkeit | AC1200 (867 + 300 Mbps) |
| Antennenanschlüsse | 2× RP-SMA-Buchse |
| Mitgelieferte Antennen | 2× Dual-Band-Dipol, 5 dBi |
| USB-Schnittstelle | USB 3.0 Typ-A (abwärtskompatibel mit USB 2.0) |
| Sendeleistung | 802.11a: 20 dBm · 802.11b: 23 dBm · 802.11g: 23 dBm · 802.11n: 21 dBm · 802.11ac: 20 dBm |
| Empfangsempfindlichkeit | 802.11a: −92 dBm · 802.11b: −97 dBm · 802.11g: −90 dBm · 802.11n: −90 dBm |
| WLAN-Sicherheit | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | Ja (Strom + WLAN-Aktivität) |
| Zubehör | USB-3.0-Verlängerungskabel |
| Herkunftsland | Taiwan |

## Betriebssystem-Unterstützung

| Betriebssystem | Status | Hinweise |
|----|--------|-------|
| Windows XP–11 | ✅ Unterstützt | Treiber von der Alfa-Website. Windows 10/11 empfohlen. |
| macOS 10.7–10.12 | ⚠️ Eingeschränkt | Offizielle Unterstützung endet bei macOS 10.12 Sierra. macOS 11+ und Apple Silicon NICHT unterstützt. |
| Ubuntu 19.04+ | ✅ Plug & Play | In-Kernel-mt76-Treiber (Kernel ≥ 4.19). Keine Treiberinstallation auf Ubuntu 20.04 LTS und höher. |
| Kali Linux 2019.3+ | ✅ Plug & Play | In-Kernel-Treiber. Monitor-Modus bestätigt. VIF (Virtuelles Interface) unterstützt. AP-Modus bei 5 GHz erfordert ggf. den Modulparameter `disable_usb_sg`. |
| NetHunter (Android) | ✅ Unterstützt | OTG-USB; In-Kernel-Treiber bedeutet breitere Android-Kompatibilität als RTL-Adapter. |

## Hardware-Kompatibilität

| Hardware | Status | Hinweise |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Ausgezeichnet | Funktioniert direkt auf Raspberry Pi OS — keine Treiberinstallation erforderlich. Bester Alfa-Adapter für Pi. |
| Desktop/Laptop-PC | ✅ Unterstützt | Standard-USB-A, mit mitgeliefertem Verlängerungskabel. |
| Mac (Intel) | ⚠️ Eingeschränkt | Nur macOS 10.7–10.12. |

## Erweiterte Funktionen

| Funktion | Status |
|---------|--------|
| Monitor-Modus | ✅ Ja (In-Kernel, keine zusätzlichen Schritte auf modernen Distributionen) |
| Paketinjektion | ✅ Ja |
| Soft-AP-Modus | ✅ Ja (5-GHz-AP: Modulparameter `disable_usb_sg` für beste Performance hinzufügen) |
| Bluetooth | ❌ Nein |
| VIF (Virtuelles Interface) | ✅ Ja (volle VIF-Unterstützung in Kali) |

## Lieferumfang

- 1× AWUS036ACM-Adapter
- 2× Abnehmbare 5-dBi-Dual-Band-Dipol-Antennen
- 1× USB-3.0-Verlängerungskabel
- 1× Treiber-CD (Windows)

## Ressourcen & Links

| Ressource | Link |
|----------|------|
| Offizielle Produktseite | https://www.alfa.com.tw/products/awus036acm_1 |
| Offizielle Dokumentation | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux-Treiber-Info (In-Kernel) | mt76-Treiber — im Linux-Kernel ≥ 4.19 enthalten, keine Installation nötig |

## Datenblatt-Download

| Dokument | Download |
|----------|----------|
| Offizielles Datenblatt (PDF) | [📄 AWUS036ACM Datenblatt herunterladen](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

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
Benötigen Sie ein Angebot oder Kaufberatung? [Kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
