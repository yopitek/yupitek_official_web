---
title: "ALFA Network USB-WLAN-Adapter im Vergleich"
description: "Vollständiger Spezifikationsvergleich von 9 ALFA Network USB-WLAN-Adaptern: Chipsatz, Linux-Treiber, Monitor-/Injection-/AP-Fähigkeit, mit gemessenen Ergebnissen am ASUS GX10 (Ubuntu 24.04 ARM64, Kernel 6.17)."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

Die folgende Tabelle vergleicht alle 9 ALFA Network USB-WLAN-Adapter. Die Spalten Monitor, Injection, AP und durchgängiger Handshake sind Messergebnisse aus Yopitek-Tests an einem ASUS GX10 (Ubuntu 24.04 LTS / ARM64 / Kernel 6.17) mit eigener Ausrüstung und dem WLAN unseres eigenen Büros — keine aus Datenblättern übernommenen Werte.

## Vollständiger Spezifikationsvergleich

Auf Mobilgeräten die Tabelle seitlich scrollen; auf einen Modellnamen tippen, um die Produktseite zu öffnen.

| Modell | WiFi-Generation | Chipsatz | Frequenzbänder | Max. Geschwindigkeit | USB | Antennen | MIMO | Monitor Mode | Packet Injection | Handshake (GX10-Test) | Linux-Treiber | Treibertyp | AP-Modus | Max. Leistung | Bluetooth | Am besten für |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/de/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Ja | ❌ Schlägt unter Standard-6.17 fehl | ❌ Nein (Injection schlägt fehl) | Im Kernel ≥5.18 | Im Kernel (Plug & Play) | ✅ Nativ | 3.6W | BT 5.2 | WiFi 6E + Linux + USB-C |
| [AWUS036AXM](/de/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2,4 + 5 + 6 GHz (6 GHz ungetestet) | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Ja | ❌ Schlägt unter Standard-6.17 fehl | ❌ Nein (Injection schlägt fehl) | Im Kernel ≥5.18 | Im Kernel (Plug & Play) | ✅ Nativ | 3.6W | BT 5.2 | WiFi 6E + Dualantenne |
| [AWUS036AX](/de/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Ja | ✅ Ja | ✅ Durchgängig (.22000) | Im Kernel ≥6.17 | Im Kernel (Plug & Play) | ✅ Nativ | 3.6W | — | WiFi 6 + AP-Hotspot |
| [AWUS036AXER](/de/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | Integriert (nano) | 2×2 MIMO | ✅ Ja | ✅ Ja | ✅ Durchgängig (.22000) | Im Kernel ≥6.17 | Im Kernel (Plug & Play) | ✅ Nativ | 3.0W | — | Kompakter Reiseadapter |
| [AWUS036ACH](/de/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ Am besten | ✅✅ Am besten | ✅ Durchgängig (.22000) | Im Kernel ≥6.13 | Im Kernel (Plug & Play) | ✅ Nativ | 3.6W | — | Goldstandard unter Kali Linux |
| [AWUS036ACM](/de/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ Ja | ✅ Ja | ✅ Durchgängig (.22000) | Im Kernel ≥4.19 | Im Kernel (Plug & Play) | ✅ Nativ | 3.0W | — | Linux Plug & Play |
| [AWUS036ACHM](/de/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ Ja | ✅ 2,4 GHz / ⚠️ 5 GHz nur Broadcast | ✅ Durchgängig (.22000) | Im Kernel ≥4.19 | Im Kernel (Plug & Play) | ✅ Nativ | — | — | Kompaktes AC600, Linux Plug & Play |
| [AWUS036ACS](/de/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ Ja | ✅ Ja | ✅ Durchgängig (.22000) | Im Kernel ≥6.13 | Im Kernel (Plug & Play) | ✅ Nativ (5 GHz getestet als 802.11a 20 MHz; VHT80 nicht getestet) | 2.5W | — | Sicherheitstests mit kleinem Budget |
| [AWUS036EACS](/de/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | Integriert 2dBi | 1×1 SISO | ✅ Ja | ✅✅ Am besten | ✅ Durchgängig (.22000) | Im Kernel ≥6.2 | Im Kernel (Plug & Play) | ✅ Nativ (5 GHz getestet als 802.11a 20 MHz; VHT80 nicht getestet) | 2.5W | BT 4.2 | WLAN für Windows-Heimnutzer + BT |

## Kurzer Kaufratgeber — nach Anwendungsfall

**🔴 Kali Linux / Pentesting** — Am besten: AWUS036ACH

RTL8812AU — der ausgereifteste Monitor Mode und Packet Injection unter Kali; 100 % Injection auf beiden Bändern am GX10 (Kernel 6.17). Treiber rtw88_8812au im Kernel seit 6.13. Tipp: Bei älteren Kernels den aircrack-ng-DKMS-Treiber verwenden, festgelegt auf den stabilen Commit 63cf0b4.

**🔵 WiFi 6E (Tri-Band) für Power-User** — Am besten: AWUS036AXML or AWUS036AXM

MT7921AUN — Linux-Treiber im Kernel seit 5.18, 6-GHz-Band (an AXML verifiziert; AXM ungetestet), Bluetooth 5.2. Hinweis: Packet Injection schlägt unter dem Standard-Kernel 6.17 fehl (mac80211-Regression seit 6.16), daher nicht für Pentesting geeignet. Bauformen: AXML hat einen abnehmbaren USB-C-Anschluss und ein Gehäuse mit einer Antenne und zwei Ausgängen; AXM hat ein integriertes L-förmiges USB-A-Format.

**🌐 Soft-AP / Hotspot-Emulation** — Am besten: AWUS036ACM

MT7612U — AP-Modus Plug & Play über das native hostapd im Linux-Kernel. Anders als Realtek-Adapter, die problematische angepasste hostapd-Builds erfordern, läuft MediaTek nahtlos und stabil für Rogue-AP-/Evil-Twin-Simulationen.

**🟢 Linux im Alltag (Plug & Play)** — Am besten: AWUS036ACM

MT7612U — im Kernel seit Kernel 4.19, keine Treiberinstallation unter Ubuntu / Debian / Fedora. Die unkomplizierteste Linux-Erfahrung.

**🟣 Raspberry Pi / Embedded** — Am besten: AWUS036ACM

Geringer Stromverbrauch + Treiber im Kernel machen ihn ideal für den Raspberry Pi. Hinweis: Modelle mit hoher Leistung (ACH, AXML) ziehen bis zu 3.6W und benötigen einen aktiven USB-Hub, um Spannungseinbrüche und Verbindungsabbrüche am Pi zu vermeiden.

**🟡 Einstieg / Sicherheitstests mit kleinem Budget** — Am besten: AWUS036ACS

RTL8811AU — günstiger Einstieg mit Unterstützung für Monitor Mode und Packet Injection. Eine Antenne, kompaktes Design.

**⚡ Kompakter Reiseadapter** — Am besten: AWUS036AXER

Ultradünnes Nano-Gehäuse mit nur 10.5g. WiFi 6 (1800 Mbps), USB-A. Gut für Geschäftsreisen, ausgerichtet auf Windows.

**🏠 Windows-Heimnutzer + Bluetooth** — Am besten: AWUS036EACS

RTL8821CU — Dual-Mode-Kombination aus WiFi 5 + Bluetooth 4.2. Nano-Bauform. Am besten für Desktop-PCs, die schnell WLAN + BT ohne PCIe-Steckplatz benötigen.

**🍎 macOS-Kompatibilität** — Am besten: AWUS036ACH or AWUS036AXML

ACH hat über einen Drittanbieter-Treiber gute macOS-Unterstützung. Der MT7921AUN des AXML hat Community-Unterstützung unter macOS. Die Kompatibilität mit der macOS-Version stets prüfen. Intel-Macs haben die bessere Treiberhistorie als M-Serie.

## Kurzer Kaufratgeber — nach Plattform / Betriebssystem

| Plattform / Betriebssystem | Erste Wahl | Alternative | Hinweise |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = bester Monitor Mode; ACM = einfachste Kernel-Unterstützung. Für VMs: VM auf einen USB-3.0-Controller (xHCI) konfigurieren, um Verbindungsabbrüche zu vermeiden. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U im Kernel seit 4.19; MT7921AUN seit 5.18 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | Geringer Stromverbrauch + Treiber im Kernel; kein manuelles Kompilieren nötig. Für Karten mit hoher Leistung wird ein aktiver USB-Hub empfohlen, um Abbrüche zu vermeiden. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | WiFi-6-Leistung; EACS ergänzt eine Bluetooth-Kombination |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | Treiber von Drittanbietern verfügbar; macOS-Version prüfen. Intel-Macs haben ältere Treiber; Apple Silicon (M1/M2/M3) hat nur eingeschränkte experimentelle Unterstützung. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU & RTL8811AU werden von NetHunter unterstützt; OTG-Adapter und eigene Kernel-Kompilierung erforderlich. |

---

Testplattform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / Kernel 6.17.0-1014-nvidia (November 2026). Berichte zu den einzelnen Adaptern finden Sie im [Blog](/de/blog/).
