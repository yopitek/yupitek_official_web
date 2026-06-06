---
title: "ALFA-USB-WiFi-Treiber unter Kali Linux & Ubuntu 24.04 installieren (2026)"
description: "Komplettanleitung zur Installation von ALFA Network USB-WiFi-Adapter-Treibern unter Kali Linux 2024 und Ubuntu 24.04 für RTL8812AU, MT7612U und MT7921AUN-Chipsätze, mit Troubleshooting-Tipps."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
featureimage: "/images/blog/install-alfa-driver-kali-ubuntu.webp"
---

# ALFA-USB-WiFi-Treiber unter Kali Linux & Ubuntu 24.04 installieren (2026)

Dieser Leitfaden deckt die Installation aller wichtigen ALFA-USB-WiFi-Treiber für Kali Linux und Ubuntu 24.04 ab.

---

## Treiberübersicht

| Chipsatz | Treiber-Repo |DKMS-Unterstützung | Komplettzeit |
|---|---|---|---|
| RTL8812AU | aircrack-ng/rtl8812au | ✓ | ~10 Min. |
| MT7612U | Kernel-inklusive | N/A | ~2 Min. |
| MT7921AUN | Kernel-inklusive | N/A | ~2 Min. |
| RTL8832BU | aircrack-ng/rtl8832bu | ✓ | ~10 Min. |

---

## Installation: RTL8812AU (Empfohlen für Kali)

```bash
# Abhängigkeiten installieren
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)

# Treiber klonen und installieren
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
sudo make dkms_install

# Überprüfen
dkms status
```

---

## Installation: MT7612U (Plug-and-Play)

Der MT7612U-Treiber (`mt76`) ist im主线-Linux-Kernel enthalten. Kein zusätzlicher Treiber erforderlich:

```bash
# Adapter einstecken und überprüfen
lsusb | grep MediaTek

# Kernel-Modul laden (falls nicht automatisch)
sudo modprobe mt76

# Überprüfen
iwconfig
```

---

## Installation: MT7921AUN (Kernel 5.18+)

Der MT7921AUN-Treiber (`mt7921u`) ist ab Kernel 5.18 im主线-Kernel:

```bash
# Kernel-Modul überprüfen
lsmod | grep mt7921u

# Falls nicht geladen:
sudo modprobe mt7921u

# Firmware-Update für optimale Leistung
sudo apt update && sudo apt install linux-firmware
```

---

## Troubleshooting

**Problem:** Treiber lädt nicht nach Neustart

**Lösung:** Stellen Sie sicher, dass das Modul in `/etc/modules` aufgelistet ist:

```bash
echo "88XXau" | sudo tee -a /etc/modules
```

**Problem:** DKMS-Fehler nach Ubuntu-Update

**Lösung:**

```bash
sudo dkms remove rtl8812au/5.6.4.2 --all
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```
