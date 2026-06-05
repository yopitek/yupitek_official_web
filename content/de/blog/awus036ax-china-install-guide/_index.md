---
title: "ALFA AWUS036AX Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036AX Treibern in China unter Verwendung lokaler Mirrors. RTL8832BU-Treiber, WiFi 6 AX1800. Deckt Kali Linux, Ubuntu 22/24 (in-kernel auf 24.04), Debian und Raspberry Pi ab. Kein GitHub erforderlich."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/de/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
---

Der AWUS036AX ist ALFAs WiFi 6 AX1800 Dual-Band Adapter. Sein RTL8832BU-Chip ist bei Linux-Versionen unter 6.14 nicht im Kernel enthalten — aber Ubuntu 24.04 (Kernel 6.8) enthält ihn nativ. Diese Anleitung verwendet Gitee-Mirrors für ältere Kernel und den integrierten Treiber für Ubuntu 24.04. Kein GitHub erforderlich.

> **Sicherheitsforschung Hinweis:** Der RTL8832BU hat eine begrenzte Unterstützung für den Monitor-Modus. Die Ergebnisse variieren je nach Kernel- und Treiberversion. Für zuverlässige Paket-Injektion unter Kali Linux sind der [AWUS036ACM](/de/blog/awus036acm-china-install-guide/) oder [AWUS036ACH](/de/blog/awus036ach-china-install-guide/) die bessere Wahl.

## Bevor du startest

1. **ALFA AWUS036AX** Adapter
2. USB-A Kabel
3. Aktive Internetverbindung

```bash
lsusb
```

Suche nach:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Wähle dein Betriebssystem

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### Schritt 1: Zu China Mirror wechseln

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Schritt 2: Build-Abhängigkeiten installieren

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Schritt 3: Treiber von Gitee klonen

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **HINWEIS:** Wenn diese Gitee-URL nicht lädt, suche auf Gitee nach `rtl8852bu` und wähle den aktuellsten Fork. Du kannst auch Archive von [files.alfa.com.tw](https://files.alfa.com.tw) herunterladen.

### Schritt 4: Kompilieren und Installieren

```bash
sudo ./install-driver.sh
sudo reboot
```

Überprüfe, ob der Treiber geladen wurde:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Schritt 5: Monitor-Modus aktivieren {#enable-monitor-mode}

> **Hinweis:** Die Unterstützung des Monitor-Modus ist beim RTL8832BU begrenzt. Die folgenden Befehle funktionieren auf den meisten Setups, aber die Ergebnisse können variieren.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Schritt 6: Paket-Injektion testen {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Wenn die Injektion unzuverlässig ist, ziehe den [AWUS036ACM](/de/blog/awus036acm-china-install-guide/) für Penetrationstests in Betracht.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — Treiber im Kernel, kein Gitee erforderlich

Ubuntu 24.04 wird mit Kernel 6.8 ausgeliefert, der den RTL8832BU-Treiber nativ enthält.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

Wenn das Modul geladen wird und ein Interface erscheint, bist du fertig. Fahre mit den Schritten für den Monitor-Modus oben fort.

---

### Ubuntu 22.04 (Jammy) — DKMS erforderlich

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Aktiviere den Monitor-Modus wie in den Kali-Schritten oben beschrieben.

---

## Raspberry Pi 4B / 5

Zuerst zum China-Mirror wechseln:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Virtuelle Maschine USB-Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Einstellungen → USB** → Aktiviere **USB 3.0 (xHCI)**.
2. Filter hinzufügen: **Realtek** (ID: 0bda:885a).
3. VM starten → `lsusb` zur Bestätigung → Kali-Schritte folgen.

### VMware

1. **Virtuelle Maschine → USB & Bluetooth** → Finde **Realtek RTL8832BU** → **Verbinden**.
2. `lsusb` zur Bestätigung → Kali-Schritte folgen.

---

## Fehlerbehebung

| Problem | Wahrscheinliche Ursache | Lösung |
|---------|-------------|-----|
| `lsusb` zeigt 0bda:885a nicht an | Adapter nicht erkannt | Anderen USB-Port versuchen |
| `install-driver.sh` schlägt fehl | Fehlende Header | `sudo apt install linux-headers-$(uname -r)` |
| Gitee-Klon schlägt fehl | Netzwerkproblem | Auf gitee.com nach `rtl8852bu` suchen |
| Ubuntu 24.04: `modprobe 88x2bu` schlägt fehl | Modul nicht vorhanden | `linux-modules-extra-$(uname -r)` installieren |
| Monitor-Modus unzuverlässig | RTL8832BU-Einschränkung | AWUS036ACM für Pentest-Arbeiten verwenden |

> **Hinweis zu VIF:** Der RTL8832BU Out-of-Kernel-Treiber unterstützt keine virtuellen Schnittstellen (VIF).

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|----------|-----|---------|
| Offizielle Alfa-Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | RTL8832BU Treiber |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## Weitere Alfa Adapter Anleitungen für China

- [AWUS036ACH China Installationsanleitung](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, hohe Leistung
- [AWUS036ACM China Installationsanleitung](/de/blog/awus036acm-china-install-guide/) — MT7612U, volle VIF-Unterstützung
- [AWUS036ACS China Installationsanleitung](/de/blog/awus036acs-china-install-guide/) — RTL8811AU, Monitor-Modus
- AWUS036AX ← du bist hier
- [AWUS036AXER China Installationsanleitung](/de/blog/awus036axer-china-install-guide/) — RTL8832BU, Nano
- [AWUS036AXM China Installationsanleitung](/de/blog/awus036axm-china-install-guide/) — MT7921AUN, L-Form
- [AWUS036AXML China Installationsanleitung](/de/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Installationsanleitung](/de/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Fragen? Hinterlasse unten einen Kommentar oder kontaktiere uns unter [yupitek.com](https://yupitek.com/de/contact/).
