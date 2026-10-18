---
title: "ALFA AWUS036AXER Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036AXER Treibern in China unter Verwendung lokaler Mirrors. RTL8832BU-Treiber, WiFi 6 Nano-Adapter. Deckt Kali Linux, Ubuntu 22/24 (DKMS), Debian und Raspberry Pi ab."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
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
faq:
  - question: "Welchen Chipsatz verwendet der AWUS036AXER? Ist er derselbe wie beim AWUS036AX?"
    answer: "Er verwendet ebenfalls den Realtek RTL8832BU-Chipsatz, unterstützt WiFi 6, ist jedoch kleiner und tragbarer."
  - question: "Braucht der AWUS036AXER unter Ubuntu 24.04 einen Treiber?"
    answer: "Ja. Der RTL8832BU ist nicht im Kernel von Ubuntu 24.04 enthalten. Bauen Sie den Community-Treiber rtl8852bu (morrownr/rtl8852bu-20250826) einmalig über DKMS; er wird bei Kernel-Updates automatisch neu gebaut."
  - question: "Ist der AWUS036AXER für drahtlose Sicherheitsforschung geeignet?"
    answer: "Nein. Der Community-Treiber rtl8852bu unterstützt weder Monitor-Modus noch Paket-Injektion. Verwenden Sie stattdessen einen Adapter mit In-Kernel-MediaTek-Treiber wie den AWUS036ACM."
  - question: "Was ist die USB-ID des AWUS036AXER?"
    answer: "Die Hersteller-ID (Vendor-ID) des Realtek RTL8832BU ist 0bda. Die Produkt-ID lautet je nach Gerät 8832 oder 885a; bestätigen Sie sie mit lsusb."
  - question: "Brauche ich ein VPN, um den AWUS036AXER in China zu installieren?"
    answer: "Nicht unbedingt. Klonen Sie den Treiber aus dem geprüften GitHub-Repository (morrownr/rtl8852bu-20250826); falls GitHub langsam ist, nutzen Sie einen vertrauenswürdigen Proxy oder Mirror. Die Build-Tools lassen sich weiterhin über inländische Mirrors installieren."
---

Der AWUS036AXER ist ALFAs WiFi 6 Nano-Adapter — ein kompakter Dongle, der so konzipiert ist, dass er permanent an einem Laptop angeschlossen bleiben kann. Der RTL8832BU-Chip des AWUS036AXER hat keinen In-Kernel-Linux-Treiber, daher bauen Sie auf jeder Distribution (auch Ubuntu 24.04) den Community-Treiber rtl8852bu einmalig über DKMS. Der Treiber-Quellcode wird aus dem geprüften GitHub-Repository geklont; falls GitHub langsam ist, nutzen Sie einen vertrauenswürdigen Proxy oder Mirror. Der Monitor-Modus wird von diesem Treiber nicht unterstützt.

{{< tldr >}}
Der AWUS036AXER verwendet den RTL8832BU-Chipsatz mit WiFi 6. Der Treiber ist nicht im Kernel enthalten: Jede Distribution (auch Ubuntu 24.04) braucht rtl8852bu per DKMS. Der Monitor-Modus wird nicht unterstützt.
{{< /tldr >}}

> **Hinweis zur Sicherheitsforschung:** Der Community-Treiber rtl8852bu unterstützt weder Monitor-Modus noch Paket-Injektion. Verwenden Sie für Sicherheitsforschung einen Adapter mit In-Kernel-MediaTek-Treiber, z. B. den [AWUS036ACM](/de/blog/awus036acm-china-install-guide/).

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

> **Nicht unterstützt:** Der Community-Treiber rtl8852bu für den RTL8832BU unterstützt keinen Monitor-Modus, daher gibt es hier keine Befehle. Für den Monitor-Modus verwenden Sie einen Adapter mit In-Kernel-MediaTek-Treiber, z. B. den [AWUS036ACM](/de/blog/awus036acm-china-install-guide/).

### Schritt 6: Paket-Injektion testen {#test-packet-injection}

> **Nicht unterstützt:** Paket-Injektion setzt den Monitor-Modus voraus, den dieser Treiber nicht bietet. Verwenden Sie für Injektionstests den [AWUS036ACM](/de/blog/awus036acm-china-install-guide/).

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — DKMS erforderlich

Ubuntu 24.04 (Kernel 6.8) enthält keinen Treiber für den RTL8832BU. Wechseln Sie zu einem inländischen Mirror und bauen Sie den Treiber wie bei Ubuntu 22.04 unten.

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

Führen Sie nach dem Neustart `sudo modprobe 8852bu` und `iwconfig` aus. Wenn das Modul geladen wird und eine Schnittstelle erscheint, sind Sie fertig (nur Managed-Modus; der Monitor-Modus wird nicht unterstützt).

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

Der Monitor-Modus wird von diesem Treiber nicht unterstützt (siehe Kali, Schritt 5).

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
| Monitor-Modus / Injektion funktioniert nicht | Vom Treiber rtl8852bu nicht unterstützt | AWUS036ACM für Pentest-Arbeiten verwenden |

> **Hinweis zu VIF:** Der RTL8832BU Out-of-Kernel-Treiber unterstützt keine virtuellen Schnittstellen (VIF).

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|-----------|-----|----------------|
| Offizielle Alfa-Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU Treiber |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

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
