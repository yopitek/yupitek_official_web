---
title: "ALFA-USB-WiFi-Treiber unter Kali Linux & Ubuntu 24.04 installieren (2026)"
description: "Komplettanleitung zur Installation von ALFA Network USB-WiFi-Adapter-Treibern unter Kali Linux 2024 und Ubuntu 24.04 für RTL8812AU, MT7612U und MT7921AUN-Chipsätze, mit Troubleshooting-Tipps."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
featureimage: "/images/blog/install-alfa-driver-kali-ubuntu.webp"
faq:
  - question: "Müssen ALFA USB WiFi-Netzwerkkarten unter Linux mit Treibern ausgestattet werden?"
    answer: "Dies hängt vom Chipsatz ab. MT7612U und MT7921AUN sind bereits im Kernel integriert und können durch Ausführen von modprobe aktiviert werden. Für RTL8812AU muss ein externer Treiber aus dem aircrack-ng GitHub-Repository installiert werden."
  - question: "Wie kann ich herausfinden, welchen Chipsatz meine ALFA-Netzwerkkarte verwendet?"
    answer: "Stecken Sie die Netzwerkkarte ein und führen Sie lsusb aus. Durch Abgleich der USB-ID können Sie den Chipsatz identifizieren. 0bda:8812 steht für RTL8812AU, 0e8d:7612 für MT7612U und 0e8d:7961 für MT7921AUN."
  - question: "Was ist DKMS und warum wird es benötigt?"
    answer: "DKMS kompiliert Treibermodule automatisch neu, wenn ein neuer Kernel installiert wird. Ohne DKMS würden externe Treiber nach jedem Kernel-Update nicht mehr funktionieren und müssten manuell neu kompiliert werden."
  - question: "Kann Ubuntu 22.04 mit einer MT7921AUN-Netzwerkkarte verwendet werden?"
    answer: "Der vorinstallierte Kernel 5.15 unterstützt diesen Chipsatz nicht. Sie müssen den HWE-Kernel linux-generic-hwe-22.04 installieren, um auf Version 6.2 oder höher zu aktualisieren, oder ein Upgrade auf Ubuntu 24.04 LTS durchführen."
  - question: "Was tun, wenn bei der Kompilierung des Treibers mit make der Fehler linux/module.h not found auftritt?"
    answer: "Die zentralen Header-Dateien sind nicht installiert. Führen Sie sudo apt install linux-headers-$(uname -r) aus, um die Header zur aktuellen Kernel-Version zu installieren, und kompilieren Sie anschließend erneut."
---
| Chipsatz | Treiber-Repo |DKMS-Unterstützung | Komplettzeit | |---|---|---|---| | RTL8812AU | aircrack-ng/rtl8812au | ✓ | ~10 Min. | | MT7612U | Kernel-inklusive | N/A | ~2 Min. | | MT7921AUN | Kernel-inklusive | N/A | ~2 Min. | | RTL8832BU | aircrack-ng/rtl8832bu | ✓ | ~10 Min. |

# ALFA-USB-WiFi-Treiber unter Kali Linux & Ubuntu 24.04 installieren (2026)

{{< tldr >}}
Die Installation der ALFA-Netzwerktreiber hängt vom Chipsatz ab: MT7612U und MT7921AUN sind im Kernel integriert und funktionieren nach dem Einstecken sofort (Plug-and-Play), während für RTL8812AU ein Treiber aus dem aircrack-ng GitHub-Repository installiert werden muss und DKMS erforderlich ist, um die Funktionalität nach Kernel-Updates sicherzustellen.
{{< /tldr >}}

Der Schlüssel zur Installation von Linux-USB-WiFi-Treibern liegt im Chipsatz. MT7612U und MT7921AUN werden vom Kernel nativ unterstützt, der RTL8812AU erfordert einen externen Treiber von aircrack-ng in Kombination mit DKMS.

Dieser Leitfaden deckt die Installation aller wichtigen ALFA-USB-WiFi-Treiber für Kali Linux und Ubuntu 24.04 ab.

---

## Treiberübersicht

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

{{< faq >}}

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

## Referenzen

1. [aircrack-ng Offizielle rtl8812au Treiber](https://github.com/aircrack-ng/rtl8812au)
2. [morrownr USB-WiFi Wissensdatenbank](https://github.com/morrownr/USB-WiFi)
3. [Kali Linux Offizielle Dokumentation](https://www.kali.org/docs/)
4. [Ubuntu Offizielle HWE-Kernel-Dokumentation](https://wiki.ubuntu.com/Kernel/LTSEnablementStack)
5. [Linux Wireless mt76 Treiber](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
