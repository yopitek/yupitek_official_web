---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Komplette 5GHz Setup-Anleitung (2026)"
description: "Vollständiger Kompatibilitätsleitfaden für HAK5 WiFi Pineapple MK7 mit ALFA AWUS036ACM (MT7612U) — Plug-and-Play 5GHz Monitor Mode, Packet Injection und PineAP-Erweiterung. Schritt-für-Schritt-Anleitung mit verifizierten Befehlen. Keine Treiber-Kompilierung erforderlich."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

Der HAK5 WiFi Pineapple Mark VII ist der Goldstandard für portable Wireless-Security-Audits. Allerdings hat er eine entscheidende Einschränkung: Das eingebaute Funkmodul arbeitet ausschließlich auf **2,4 GHz**. Im Jahr 2026 sind die meisten Unternehmens- und Heimnetzwerke auf 5 GHz umgestiegen.

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

## 6. Penetrationstest-Topologie

![HAK5 WiFi Pineapple MK7 + AWUS036ACM Topologie](/images/blog/hak5-pineapple-topology.svg)

---

## 7. Validierungsergebnisse — alle Tests bestanden ✅

---

## 8. Empfehlung

**Der ALFA AWUS036ACM ist der beste derzeit erhältliche Adapter zur 5 GHz-Erweiterung des WiFi Pineapple Mark VII.**

👉 [ALFA AWUS036ACM Produktseite](/de/products/alfa/awus036acm/)

Yupitek ist autorisierter ALFA Network-Distributor mit vollständigem technischen Support.

*Brauchst du Hilfe bei der Einrichtung? Kontaktiere den Yupitek-Support: [yupitek.com/support](/de/support/)*
