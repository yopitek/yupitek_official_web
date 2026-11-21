---
title: "ALFA AWUS036AXER Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036AXER Treibern in China unter Verwendung lokaler Mirrors. RTL8832BU-Treiber, WiFi 6 Nano-Adapter. Deckt Kali Linux, Ubuntu 22/24 (DKMS), Debian und Raspberry Pi ab."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/de/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
faq:
  - question: "Welchen Chipsatz verwendet der AWUS036AXER? Ist er derselbe wie beim AWUS036AX?"
    answer: "Er verwendet ebenfalls den Realtek RTL8832BU-Chipsatz, unterstützt WiFi 6, ist jedoch kleiner und tragbarer."
  - question: "Braucht der AWUS036AXER unter Ubuntu 24.04 einen Treiber?"
    answer: "Das hängt von Ihrem Kernel ab. Linux-Kernel 6.17 und neuer (zum Beispiel Ubuntu 24.04 HWE / Kernel 6.17) liefert den In-Kernel-Treiber rtw89_8852bu mit — Plug-and-Play, kein DKMS. Nur auf Kerneln älter als 6.17 bauen Sie den Community-Treiber rtl8852bu (morrownr/rtl8852bu-20250826) einmalig über DKMS. Prüfen Sie zuerst mit uname -r."
  - question: "Ist der AWUS036AXER für drahtlose Sicherheitsforschung geeignet?"
    answer: "Ja. Mit dem In-Kernel-Treiber rtw89_8852bu auf Kernel 6.17+ funktionieren Monitor-Modus und Paket-Injektion in unseren Tests beide (Ubuntu 24.04 / Kernel 6.17: Injektion 73 % auf 2,4 GHz sowie ein durchgängiger WPA .22000 Capture). Hinweis: Auf älteren Kerneln mit dem Community-DKMS-Treiber kann die Monitor-Unterstützung eingeschränkt sein. Nur in Netzwerken, die Ihnen gehören oder für die Sie eine Testerlaubnis haben."
  - question: "Was ist die USB-ID des AWUS036AXER?"
    answer: "Die Hersteller-ID (Vendor-ID) des Realtek RTL8832BU ist 0bda. Die Produkt-ID lautet je nach Gerät 8832 oder 885a; bestätigen Sie sie mit lsusb."
  - question: "Brauche ich ein VPN, um den AWUS036AXER in China zu installieren?"
    answer: "Nicht unbedingt. Klonen Sie den Treiber aus dem geprüften GitHub-Repository (morrownr/rtl8852bu-20250826); falls GitHub langsam ist, nutzen Sie einen vertrauenswürdigen Proxy oder Mirror. Die Build-Tools lassen sich weiterhin über inländische Mirrors installieren."
---

Der AWUS036AXER ist ALFAs WiFi 6 Nano-Adapter — ein kompakter Dongle, der so konzipiert ist, dass er permanent an einem Laptop angeschlossen bleiben kann. Sein RTL8832BU-Chip wird vom **In-Kernel-Treiber rtw89_8852bu auf Linux-Kernel 6.17 und neuer** unterstützt (zum Beispiel Ubuntu 24.04 HWE / Kernel 6.17) — Plug-and-Play, kein Kompilieren. Nur auf **älteren Kerneln** (unter 6.17) bauen Sie den Community-Treiber rtl8852bu einmalig über DKMS. Diese Anleitung deckt beide Fälle ab. Der Treiber-Quellcode wird aus dem geprüften GitHub-Repository geklont; falls GitHub langsam ist, nutzen Sie einen vertrauenswürdigen Proxy oder Mirror.

{{< tldr >}}
Der AWUS036AXER verwendet den RTL8832BU-Chipsatz mit WiFi 6. Kernel 6.17+ (inkl. Ubuntu 24.04 / Kernel 6.17) hat den In-Kernel-Treiber rtw89_8852bu — kein DKMS, mit Monitor-Modus und Injektion, die in Tests funktionieren. Ältere Kernel brauchen den Community-Treiber rtl8852bu über DKMS.
{{< /tldr >}}

> **Hinweis zur Sicherheitsforschung:** Mit dem **In-Kernel-Treiber rtw89_8852bu auf Kernel 6.17+** funktionieren der Monitor-Modus und die Paket-Injektion des AWUS036AXER in Tests (Ubuntu 24.04 / Kernel 6.17: 2,4-GHz-Injektion 73 %, durchgängiger WPA .22000). Nur auf älteren Kerneln mit dem Community-DKMS-Treiber ist die Monitor-Unterstützung eingeschränkt. Prüfen Sie zuerst `uname -r`. Nur in Netzwerken, die Ihnen gehören oder für die Sie eine Testerlaubnis haben.

> **Hinweis zur Reichweite:** Der AWUS036AXER verfügt über eine integrierte, nicht abnehmbare Antenne. Für die Sicherheitsforschung bieten Adapter mit externen RP-SMA-Antennen (AWUS036ACH, AWUS036ACM) eine deutlich bessere Reichweite.

## Bevor du startest

1. **ALFA AWUS036AXER** Adapter
2. USB-A Kabel
3. Aktive Internetverbindung

```bash
lsusb
```

Suche nach einer Zeile wie dieser (Beispielausgabe; die Vendor-ID ist immer `0bda`, die Produkt-ID ist je nach Gerät `8832` oder `885a`):

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

### Schritt 3: Treiber von GitHub klonen

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **HINWEIS:** Der gepflegte Upstream-Treiber ist [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Falls GitHub langsam ist, nutzen Sie einen vertrauenswürdigen Proxy oder Mirror. Archive können Sie auch von [files.alfa.com.tw](https://files.alfa.com.tw) herunterladen.

### Schritt 4: Kompilieren und Installieren

```bash
sudo ./install-driver.sh
sudo reboot
```

Überprüfe, ob der Treiber geladen wurde:

```bash
lsmod | grep 8852bu
iwconfig
```

### Schritt 5: Monitor-Modus aktivieren {#enable-monitor-mode}

> **Funktioniert auf Kernel 6.17+:** Mit dem In-Kernel-Treiber rtw89_8852bu funktioniert der Monitor-Modus:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> Auf älteren Kerneln mit dem Community-DKMS-Treiber kann die Monitor-Unterstützung eingeschränkt sein — dort können Sie zu einem Adapter mit In-Kernel-MediaTek-Treiber wechseln, z. B. dem [AWUS036ACM](/de/blog/awus036acm-china-install-guide/).

### Schritt 6: Paket-Injektion testen {#test-packet-injection}

> **Funktioniert auf Kernel 6.17+:** Nach dem Wechsel in den Monitor-Modus testen Sie die Injektion mit aireplay-ng (73 % auf 2,4 GHz in Tests):
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Nur in Netzwerken, die Ihnen gehören oder für die Sie eine Testerlaubnis haben. Auf älteren Kerneln, bei denen dem Community-DKMS-Treiber der Monitor-Modus fehlt, ist auch die Injektion nicht verfügbar.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

Auf Ubuntu 24.04 enthält nur ein **HWE-Kernel 6.17 oder neuer** (z. B. der HWE-Kernel von 24.04.4) den In-Kernel-Treiber rtw89_8852bu — einfach einstecken, kein Bauen nötig. Auf dem **GA-Kernel 6.8** oder dem **HWE-Kernel 6.14** (beide ohne diesen Treiber) wechseln Sie zu einem inländischen Mirror und bauen den Community-Treiber wie bei Ubuntu 22.04 unten, oder aktualisieren Sie auf einen HWE-Kernel 6.17 oder neuer, um den In-Kernel-Treiber zu erhalten.

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
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Führen Sie nach dem Neustart `sudo modprobe 8852bu` und `iwconfig` aus. Wenn das Modul geladen wird und eine Schnittstelle erscheint, sind Sie fertig. Dies ist der Pfad über den Community-DKMS-Treiber für ältere Kernel (unter 6.17), bei dem die Monitor-Unterstützung eingeschränkt sein kann. Auf Kernel 6.17+ nutzt das System den In-Kernel-Treiber rtw89_8852bu, mit dem Monitor-Modus und Injektion funktionieren.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Dieser Weg über den Community-DKMS-Treiber gilt für ältere Kernel (unter 6.17), bei denen die Monitor-Unterstützung eingeschränkt sein kann. Auf Kernel 6.17+ nutzt das System den In-Kernel-Treiber rtw89_8852bu, mit dem Monitor-Modus und Injektion funktionieren (siehe Kali, Schritt 5).

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Virtuelle Maschine USB-Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Einstellungen → USB** → Aktiviere **USB 3.0 (xHCI)**.
2. Filter hinzufügen: **Realtek** (Vendor-ID: 0bda, Produkt-ID: 8832 oder 885a).
3. VM starten → `lsusb` zur Bestätigung → Kali-Schritte folgen.

### VMware

1. **Virtuelle Maschine → USB & Bluetooth** → Finde **Realtek RTL8832BU** → **Verbinden**.
2. `lsusb` zur Bestätigung → Kali-Schritte folgen.

---

## Fehlerbehebung

| Problem | Wahrscheinliche Ursache | Lösung |
|----------|-------------------|---------|
| `lsusb` zeigt 0bda:8832 oder 0bda:885a nicht an | Adapter nicht erkannt | Anderen USB-Port versuchen |
| `install-driver.sh` schlägt fehl | Fehlende Header | `sudo apt install linux-headers-$(uname -r)` |
| GitHub-Klon schlägt fehl oder ist langsam | Netzwerkproblem | Vertrauenswürdigen Proxy oder Mirror verwenden |
| `modprobe 8852bu` schlägt fehl | Treiber nicht gebaut oder nicht geladen | `sudo ./install-driver.sh` erneut ausführen, `sudo dkms status` prüfen, dann neu starten |
| Monitor-Modus / Injektion funktioniert nicht | Kernel älter als 6.17 mit dem Community-DKMS-Treiber rtl8852bu (Monitor-Unterstützung kann eingeschränkt sein) | Mit `uname -r` prüfen; Kernel 6.17+ (In-Kernel rtw89_8852bu) verwenden oder auf älteren Kerneln den AWUS036ACM |

> **Hinweis zu VIF:** Der RTL8832BU Out-of-Kernel-Treiber unterstützt keine virtuellen Schnittstellen (VIF).

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|-----------|-----|----------------|
| Offizielle Alfa-Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU Treiber |
| 清华大学镜像 (Mirror der Tsinghua-Universität) | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 (Aliyun-Mirror) | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 (USTC-Mirror) | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像 (Huawei-Cloud-Mirror) | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

---

{{< faq >}}

## Weitere Alfa Adapter Anleitungen für China

- [AWUS036ACH China Installationsanleitung](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, hohe Leistung
- [AWUS036ACM China Installationsanleitung](/de/blog/awus036acm-china-install-guide/) — MT7612U, volle VIF-Unterstützung
- [AWUS036ACS China Installationsanleitung](/de/blog/awus036acs-china-install-guide/) — RTL8811AU, Monitor-Modus
- [AWUS036AX China Installationsanleitung](/de/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← du bist hier
- [AWUS036AXM China Installationsanleitung](/de/blog/awus036axm-china-install-guide/) — MT7921AUN, L-Form
- [AWUS036AXML China Installationsanleitung](/de/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Installationsanleitung](/de/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Fragen? Hinterlasse unten einen Kommentar oder kontaktiere uns unter [yupitek.com](https://yupitek.com/de/contact/).

## Referenzen

1. [Realtek Offizielle Website](https://www.realtek.com/)
2. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
3. [Kali Linux Offizielle Dokumentation](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
