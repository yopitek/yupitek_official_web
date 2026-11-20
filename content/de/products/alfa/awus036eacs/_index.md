---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 Nano USB-Adapter"
description: "ALFA AWUS036EACS, Realtek RTL8821CU, AC600 Dual-Band, USB-2.0-Nano-Formfaktor, Bluetooth 4.2. Mainline-Treiber rtw88_8821cu seit Kernel 6.2; im GX10-Test bestanden Monitor-Modus und Injektion auf beiden Bändern."
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "Windows", "Home"]
---

## Produktübersicht

Der AWUS036EACS ist Alfas ultra-kompakter WiFi-+Bluetooth-Kombinations-Adapter, konzipiert für Heim- und Bürobenutzer, die drahtlose Konnektivität in einem einzigen, unauffälligen USB-Dongle wünschen. Aufgebaut auf dem Realtek RTL8821CU Chipsatz, integriert er AC600-Dual-Band-WLAN und Bluetooth 4.2 in einem Nano-Formfaktor mit integrierter Treiberunterstützung unter Windows. Der Soft-AP-Modus ermöglicht das Teilen Ihrer Internetverbindung. Unter Linux ist der Mainline-Treiber rtw88_8821cu seit Kernel 6.2 enthalten. Im GX10-Test (Ubuntu 24.04, Kernel 6.17) erreichten Monitor-Modus und Paketinjektion auf 2,4 GHz und 5 GHz jeweils 100 %, ein durchgängiger WPA-Handshake-Mitschnitt gelang, und Bluetooth und WLAN ließen sich gleichzeitig nutzen.

> ⚠️ **Hinweis:** Der AWUS036EACS ist für den Windows-Heimgebrauch konzipiert, funktioniert aber auch unter Linux mit dem Mainline-Treiber rtw88_8821cu (Kernel 6.2+). Kein RP-SMA-Port — Antenne ist nicht aufrüstbar.

## Produktmerkmale

- 802.11ac AC600 Dual-Band-WLAN + Bluetooth 4.2 in einem einzigen Nano-USB-Adapter
- Plug-and-Play unter Windows — integrierter Treiber installiert sich automatisch
- Soft-AP-Modus — WLAN-Hotspot direkt über den Adapter erstellen
- Ultra-kompakt und portabel — verschwindet in jedem USB-Port
- Dual-Band: 2,4 GHz (150 Mbps) + 5 GHz (433 Mbps)
- Integrierte 2-dBi-Antenne — kein externer RP-SMA-Anschluss
- Ideal für Desktops, eingebettete Systeme oder Heim-PCs, die WLAN + BT auf minimalem Raum benötigen
- Bluetooth 4.2 unterstützt Audio-Streaming, Tastaturen, Mäuse und andere Peripheriegeräte

## Technische Spezifikationen

| Parameter | Wert |
|-----------|-------|
| Chipsatz | Realtek RTL8821CU |
| WLAN-Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bluetooth | BT 4.2 (2,4 GHz) |
| Frequenzbänder | WLAN: 2,4 GHz · 5 GHz · BT: 2,4 GHz |
| Max. Datenrate | 802.11b: 11 Mbps · 802.11g: 54 Mbps · 802.11n: 150 Mbps · 802.11ac: 433 Mbps |
| Kombinierte Max.-Geschwindigkeit | AC600 (150 + 433 Mbps) |
| Antenne | Integriert, 2 dBi (nicht abnehmbar, kein RP-SMA) |
| USB-Schnittstelle | USB 2.0 |
| Sendeleistung | 17 dBm typisch |
| Empfangsempfindlichkeit | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| WLAN-Sicherheit | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| Betriebstemperatur | −10 °C bis 60 °C |
| Formfaktor | Nano / Low-Profile |
| Herkunftsland | Taiwan |

## Betriebssystem-Kompatibilität

| Betriebssystem | Status | Hinweise |
|----|--------|-------|
| Windows XP–10 | ✅ Unterstützt | Integrierter Treiber; Plug & Play. Alfa-Treiberseite für Windows-11-Kompatibilität prüfen. |
| macOS | ⚠️ Eingeschränkt | Genaue Versionsrange TBC. Keine Apple-Silicon-Unterstützung. |
| Ubuntu / Linux | ✅ Kernel 6.2+ | Mainline-Treiber rtw88_8821cu, keine Installation nötig (getestet auf GX10, Ubuntu 24.04, Kernel 6.17). |
| Kali Linux | ✅ Unterstützt | Monitor-Modus und Paketinjektion auf dem GX10 (Ubuntu 24.04, Kernel 6.17) verifiziert: 100 % auf beiden Bändern, durchgängiger WPA-Handshake-Mitschnitt erfolgreich. Auf echtem Kali nicht getestet. |
| NetHunter (Android) | ❌ Nicht empfohlen | RTL8821CU nicht bestätigt mit NetHunter kompatibel. |

## Hardware-Kompatibilität

| Hardware | Status | Hinweise |
|----------|--------|-------|
| Raspberry Pi | ⚠️ Nicht getestet | Von uns nicht getestet; ab Kernel 6.2 ist der Mainline-Treiber rtw88_8821cu enthalten. |
| Desktop / Laptop-PC | ✅ Unterstützt | Nur Windows empfohlen. |
| Eingebettet / IoT (Windows) | ⚠️ Nur Windows | Kompaktes Design eignet sich für eingebettete Windows-Systeme. |

## Erweiterte Funktionen

| Funktion | Status |
|---------|--------|
| Monitor-Modus | ✅ Ja (GX10-Test: 100 % auf beiden Bändern) |
| Paketinjektion | ✅ Ja (GX10-Test: 100 % auf beiden Bändern) |
| Soft-AP-Modus | ✅ Ja |
| Bluetooth | ✅ BT 4.2 (gleichzeitig mit WLAN nutzbar) |
| VIF | 🟡 Teilweise (passiver monitor + managed auf demselben Kanal; keine unabhängigen doppelten VIFs) |

## Lieferumfang

- 1× AWUS036EACS Nano-Adapter

## Ressourcen & Links

| Ressource | Link |
|----------|------|
| Offizielle Produktseite | https://www.alfa.com.tw/products/awus036eacs_1 |
| Offizielle Dokumentation | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## Datenblatt-Download

Offizielles Datenblatt demnächst verfügbar.

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## Kompatible Antennen-Upgrades

Alle ALFA-Adapter verfügen über einen Standard-RP-SMA-Anschluss. Rüsten Sie mit einer optionalen externen Antenne für größere Reichweite und mehr Gewinn auf:

| Antenne | Frequenz | Gewinn | Typ |
|---------|-----------|------|------|
| [ALFA APA-M04](/de/products/alfa/apa-m04/) | 2,4 GHz | 7 dBi | Indoor-Panel |
| [ALFA APA-M25](/de/products/alfa/apa-m25/) | 2,4 / 5 GHz | 8 / 10 dBi | Dual-Band-Indoor-Panel |
| [ALFA APA-M25-6E](/de/products/alfa/apa-m25-6e/) | 2,4 / 5 / 6 GHz | 8 / 10 / 9 dBi | Tri-Band-Indoor-Panel |
| [ARS 25-57A](/de/products/alfa/ars-25-57a/) | 2,4 / 5 GHz | 2,5 / 7 dBi | Outdoor-Omni |
| [ARS NT5B7](/de/products/alfa/ars-nt5b7/) | 2,4 / 5 GHz | 4 / 5 / 7 dBi | Omni |

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
