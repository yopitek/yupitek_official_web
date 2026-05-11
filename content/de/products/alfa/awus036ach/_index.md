---
title: "ALFA AWUS036ACH — AC1200 Dual-Band High-Power USB-C WLAN-Adapter"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 Dual-Band, USB-C, zwei abnehmbare 5-dBi-Antennen. Goldstandard für Kali Linux Penetrationstests mit Monitor-Modus und Paketinjektion."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Dual Antenna", "Monitor Mode", "Kali Linux", "Security Research"]
---

{{< alert "warning" >}}
**Rechtlicher Hinweis**: Der Monitor-Modus und die Paketinjektion sind ausschließlich für autorisierte Sicherheitstests, Bildungsforschung und legale Penetrationstests vorgesehen. Stellen Sie sicher, dass Sie eine ausdrückliche Genehmigung für das Zielnetzwerk besitzen.
{{< /alert >}}

## Produktübersicht

Der AWUS036ACH ist Alfa Networks ikonischster Sicherheitsforschungs-Adapter — seit 2017 der Goldstandard für Kali Linux Penetrationstests. Angetrieben vom bewährten Realtek RTL8812AU Chipsatz liefert er zuverlässigen Monitor-Modus und Paketinjektion, einen integrierten Leistungsverstärker für Langstreckenempfang sowie zwei abnehmbare 5-dBi-Antennen. Er war der erste WiFi-5-Adapter der Welt mit einem USB-Typ-C-Anschluss.

> **macOS-Hinweis:** Alle ALFA-Adapter bieten eingeschränkte oder keine macOS-Unterstützung. macOS 11 Big Sur und höher sowie Apple Silicon (M1/M2/M3) werden **NICHT** unterstützt. Die maximale macOS-Unterstützung ist 10.15 Catalina auf Intel-Macs.

## Hauptmerkmale

- Realtek RTL8812AU — meistgetesteter Chipsatz für WLAN-Sicherheitsforschung
- WiFi 5 AC1200 Dual-Band: 5 GHz 867 Mbps + 2,4 GHz 300 Mbps
- Integrierter Leistungsverstärker — bis zu 3× die Reichweite typischer Laptop-Karten
- 2× RP-SMA-Buchse mit 2× 5-dBi-Dual-Band-Antennen (austauschbar)
- Erster WiFi-5-USB-C-Adapter der Welt
- Monitorhalterung (Screen Clip) im Lieferumfang
- Kali Linux-Unterstützung seit 2017.1

## Technische Spezifikationen

| Parameter | Wert |
|------|------|
| Chipsatz | Realtek RTL8812AU |
| WLAN-Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequenzbänder | Dual-Band 2,4 GHz / 5 GHz |
| Max. Datenrate | 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| Kombinierte Max.-Geschwindigkeit | AC1200 (867 + 300 Mbps) |
| Antennenanschlüsse | 2× RP-SMA-Buchse |
| Mitgelieferte Antennen | 2× Dual-Band-Dipol-Omni, 5 dBi |
| USB-Schnittstelle | Typ-C SuperSpeed (5 Gbps); abwärtskompatibel mit USB 2.0 |
| Leistungsverstärker | Ja — erweiterte Reichweite |
| WLAN-Sicherheit | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| Herkunftsland | Taiwan |

## Betriebssystem-Unterstützung

| Betriebssystem | Status | Hinweise |
|------|---------|------|
| Windows 10/11 | ✅ Unterstützt | Treiber von der Alfa-Website herunterladen; WPA3 unterstützt |
| macOS 10.15 Catalina | ⚠️ Eingeschränkt | Manuelle Installation; macOS 11+ und Apple Silicon NICHT unterstützt |
| Ubuntu | ✅ Unterstützt | Manuelle RTL8812AU-DKMS-Installation; im Kernel ab Version ≥ 6.14 |
| Kali Linux | ✅ Ausgezeichnet | Seit Kali 2017.1; voller Monitor-Modus + Paketinjektion; aircrack-ng-Treiber verwenden |
| NetHunter (Android) | ✅ Unterstützt | OTG-USB; weit verbreitet und bestätigt funktionsfähig |

## Hardware-Kompatibilität

| Hardware | Status | Hinweise |
|------|---------|------|
| Raspberry Pi 3B+/4/5 | ✅ Unterstützt | Manueller Treiber über morrownr-DKMS-Skript |
| Desktop/Laptop-PC | ✅ Unterstützt | USB-C oder USB-A über mitgeliefertes Kabel |
| Mac (Intel) | ⚠️ Eingeschränkt | Maximal macOS 10.15 Catalina |

## Erweiterte Funktionen

| Funktion | Status |
|------|------|
| Monitor-Modus | ✅ Ausgezeichnet (Goldstandard — community-bewährt seit 2017) |
| Paketinjektion | ✅ Ausgezeichnet |
| Soft-AP-Modus | ✅ Ja |
| Bluetooth | ❌ Nein |
| VIF | ⚠️ Eingeschränkt |

## Lieferumfang

- 1× AWUS036ACH-Adapter
- 2× Abnehmbare 5-dBi-Dual-Band-Dipol-Antennen
- 1× USB-C-auf-USB-A-Kabel
- 1× Monitorhalterung (Screen Clip)

## Ressourcen & Links

| Ressource | Link |
|------|------|
| Offizielle Produktseite | https://www.alfa.com.tw/products/awus036ach_1 |
| Offizielle Dokumentation | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Treiber (aircrack-ng, empfohlen für Kali) | https://github.com/aircrack-ng/rtl8812au |
| Treiber (morrownr, allgemeines Linux) | https://github.com/morrownr/8812au-20210708 |

## Produktdatenblatt

| Dokument | Download |
|------|------|
| Offizielles Datenblatt (PDF) | [📄 AWUS036ACH Datenblatt herunterladen](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
Benötigen Sie ein Angebot oder weitere Informationen? [Kontaktieren Sie uns](/de/contact/)
{{< /alert >}}
