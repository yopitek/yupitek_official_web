---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Komplette 5GHz Setup-Anleitung (2026)"
description: "Vollständiger Kompatibilitätsleitfaden für HAK5 WiFi Pineapple MK7 mit ALFA AWUS036ACM (MT7612U) — Plug-and-Play 5GHz Monitor Mode, Packet Injection und PineAP-Erweiterung. Schritt-für-Schritt-Anleitung mit verifizierten Befehlen. Keine Treiber-Kompilierung erforderlich."
date: 2026-06-10
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
faq:
  - question: "Benötigt der WiFi Pineapple Mark VII eine externe Netzwerkkarte?"
    answer: "Ja. Der im MK7 integrierte Funkadapter unterstützt nur 2,4 GHz. Da die meisten Netzwerke bis 2026 auf 5 GHz migriert sein werden, ermöglicht der externe AWUS036ACM die Hinzufügung von 5-GHz-Monitor- und Injection-Fähigkeiten."
  - question: "Warum ist der AWUS036ACM auf dem MK7 Plug-and-Play-fähig?"
    answer: "Die MK7-Firmware 2.x ist bereits mit dem kmod-mt76x2u-Treiber vorinstalliert. Der MT7612U-Chipsatz ist seit Linux 4.19 im Kernel integriert, sodass kein Kompilieren oder manuelle Installation erforderlich ist."
  - question: "Drosselt der USB 2.0-Port des MK7 die Leistung des AWUS036ACM?"
    answer: "USB 2.0 begrenzt die Durchsatzrate auf 150–250 Mbit/s. Dies hat jedoch keinen Einfluss auf Penetrationstest-Arbeitslasten wie Packet Capture und das Sammeln von Handshakes. Lediglich hochdurchsatzintensive Bridge-Szenarien sind eingeschränkt."
  - question: "Wie aktiviere ich den Monitor Mode auf dem MK7?"
    answer: "Melden Sie sich per SSH an und führen Sie den Befehl airmon-ng start wlan3 aus. Die Schnittstelle wird dann in wlan3mon umbenannt. Überprüfen Sie den Modus anschließend mit iwconfig."
  - question: "Welche ALFA-Netzwerkkarten sind nicht mit dem MK7 kompatibel?"
    answer: "AWUS036AX und AWUS036AXER verwenden den RTL8832BU-Chip, AWUS036EACS verwendet den RTL8811CU-Chip; die Treiber unterstützen weder Monitor Mode noch Packet Injection und sind daher nicht kompatibel."

---

Der HAK5 WiFi Pineapple Mark VII ist der Goldstandard für portable Wireless-Security-Audits. Allerdings hat er eine entscheidende Einschränkung: Das eingebaute Funkmodul arbeitet ausschließlich auf **2,4 GHz**. Im Jahr 2026 sind die meisten Unternehmens- und Heimnetzwerke auf 5 GHz umgestiegen.

{{< tldr >}}
Der AWUS036ACM verwendet den MT7612U-Chipsatz, und die MK7-Firmware 2.x ist bereits mit dem Treiber vorinstalliert. Nach dem Einstecken steht die Schnittstelle als wlan3 zur Verfügung und unterstützt den Monitor Mode, Packet Injection sowie PineAP-Erweiterungen. Die Einrichtung ist innerhalb von 10 Minuten abgeschlossen.
{{< /tldr >}}

Hier kommt der **ALFA AWUS036ACM** ins Spiel. Er ist einer der wenigen 802.11ac-Adapter, die von Hak5 [offiziell als kompatibel bestätigt](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) wurden. Dank des vorinstallierten `mt76x2u`-Kernel-Treibers in MK7 Firmware 2.x funktioniert er **ohne jegliche Treiber-Kompilierung** per Plug-and-Play.

---

## 1. Warum dein WiFi Pineapple 5 GHz braucht

| Szenario | 2,4 GHz (eingebaut) | 5 GHz (AWUS036ACM) |
|---|---|---|
| WPA2-Enterprise-Netzwerke | Teilweise vorhanden | **Primärband moderner Deployments** |
| Heim-Mesh-Systeme | Legacy-Fallback | **Standardband für Clients** |
| Kanalüberlastung | Extrem überlastet (1–11) | Sauberes Spektrum (36–165) |

---

## 2. Zielplattform

| Komponente | Spezifikation |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **Speicher** | 2 GB eMMC |
| **USB Host** | 1× USB 2.0 Type-A (max. 480 Mbps) |

> ✅ **Wichtige Tatsache**: `kmod-mt76x2u` ist in Firmware 2.x vorinstalliert. Der AWUS036ACM funktioniert **Plug-and-Play**.

---

## 3. ALFA AWUS036ACM — Spezifikationen

| Spezifikation | Detail |
|---|---|
| **Chipsatz** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **Frequenzbänder** | 2,4 GHz + 5 GHz |
| **Max. Datenrate** | 867 Mbps (5 GHz) |
| **Monitor Mode** | ✅ Unterstützt |
| **Packet Injection** | ✅ Unterstützt |
| **Antenne** | 2× 5 dBi RP-SMA (abnehmbar) |

---

## 4. Kompatibilitätsmatrix — alle Tests bestanden ✅

---

## 5. Schritt-für-Schritt-Einrichtung

```bash
ssh root@172.16.42.1
lsusb                          # Schritt 1: USB-Erkennung prüfen
lsmod | grep mt76              # Schritt 2: Treiber prüfen
iw dev                         # Schritt 3: Interface prüfen
airmon-ng check kill           # Schritt 4: Monitor Mode aktivieren
airmon-ng start wlan3
iw wlan3mon set channel 36     # Schritt 5: 5 GHz scannen
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # Schritt 6: Injection testen
```

---

## 6. Validierungsergebnisse — alle Tests bestanden ✅

---

{{< faq >}}

## 7. Empfehlung

**Der ALFA AWUS036ACM ist der beste derzeit erhältliche Adapter zur 5 GHz-Erweiterung des WiFi Pineapple Mark VII.**

👉 [ALFA AWUS036ACM Produktseite](/de/products/alfa/awus036acm/)

Yupitek ist autorisierter ALFA Network-Distributor mit vollständigem technischen Support.

*Brauchst du Hilfe bei der Einrichtung? Kontaktiere den Yupitek-Support: [yupitek.com/support](/de/support/)*

## Referenzen

1. [Hak5 Offizielle Dokumentation — Liste kompatibler 802.11ac-Adapter](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [OpenWrt mt76 Treiber-Repository — GitHub](https://github.com/openwrt/mt76)
3. [aircrack-ng — WLAN-SicherheitstoolkitOffizielle Website](https://www.aircrack-ng.org/)
4. [ALFA Network Offizielle Website — AWUS036ACM Produktspezifikationen](https://www.alfa.com.tw/)
5. [Linux Wireless — MT76x2U-Treiberdokumentation](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
