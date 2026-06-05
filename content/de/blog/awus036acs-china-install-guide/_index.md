---
title: "ALFA AWUS036ACS Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036ACS Treibern in China unter Verwendung lokaler Mirrors. RTL8811AU DKMS-Treiber, voller Monitor-Modus und Paket-Injektion. Deckt Kali Linux, Ubuntu 22/24, Debian und Raspberry Pi ab. Kein GitHub erforderlich."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Treiber-Anleitungen"]
series: ["alfa-china-install-guide"]
related_product: "/de/products/alfa/awus036acs/"
series_order: 3
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
---

Der AWUS036ACS ist ALFAs kompakter Dual-Band-Adapter für Sicherheitsforschung. Sein RTL8811AU-Chip unterstützt den vollen Monitor-Modus und Paket-Injektion unter Kali Linux – aber da der Treiber nicht im Kernel enthalten ist, müssen Sie ihn aus dem Quellcode kompilieren. In China ist GitHub blockiert, daher verwendet diese Anleitung ausschließlich Gitee-Mirrors. Kein GitHub erforderlich.

## Bevor Sie beginnen

Stellen Sie sicher, dass Sie Folgendes bereit haben:

1. **ALFA AWUS036ACS** Adapter
2. USB-Kabel (USB-A 2.0, das in der Box enthaltene funktioniert prima)
3. Aktive Internetverbindung, um die lokalen Mirrors zu erreichen

Schließen Sie den Adapter an und bestätigen Sie dann, dass Ihr System ihn erkennt:

```bash
lsusb
```

Suchen Sie in der Ausgabe nach diesem Eintrag:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

Wenn Sie `0bda:0811` sehen, wurde der Adapter erkannt. Fahren Sie mit dem Abschnitt für Ihr Betriebssystem fort.

## Wählen Sie Ihr Betriebssystem

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Schon installiert? Springen Sie zu:

- [Monitor-Modus aktivieren](#monitor-modus-aktivieren)
- [Paket-Injektion testen](#paket-injektion-testen)
- [Virtuelle Maschine USB-Passthrough](#virtuelle-maschine-usb-passthrough)

---

## Kali Linux

### Schritt 1: Zu China-Mirror wechseln

```bash
sudo nano /etc/apt/sources.list
```

Löschen Sie alles, was dort steht, und fügen Sie ein:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern mit **Strg+O**, Enter, dann **Strg+X**. Aktualisieren:

```bash
sudo apt update
```

> **Backup-Mirror:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Schritt 2: Build-Abhängigkeiten installieren

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Schritt 3: Treiber von Gitee klonen

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **HINWEIS:** Falls diese Gitee-URL nicht lädt, suchen Sie auf Gitee nach `8821au` und wählen Sie den am kürzesten aktualisierten Fork. Sie können auch Treiber-Archive von [files.alfa.com.tw](https://files.alfa.com.tw) herunterladen.

---

### Schritt 4: Kompilieren und Installieren

```bash
sudo ./install-driver.sh
sudo reboot
```

Überprüfen Sie nach dem Neustart, ob der Treiber geladen wurde.

```bash
lsmod | grep 88XXau
```

Sie sollten ein `88XXau`-Modul in der Liste sehen. Bestätigen Sie dann, dass das Interface erschienen ist.

```bash
iwconfig
```

Suchen Sie nach `wlan0` oder `wlan1`.

---

### Schritt 5: Monitor-Modus aktivieren {#monitor-modus-aktivieren}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Bestätigen Sie mit `iwconfig` – suchen Sie nach `wlan1mon` mit `Mode:Monitor`.

---

### Schritt 6: Paket-Injektion testen {#paket-injektion-testen}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Schritt 1: Zu China-Mirror wechseln

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Alles löschen und einfügen:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Ersetzen Sie alle Zeilen durch:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Schritt 2: Build-Abhängigkeiten installieren

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Schritt 3: Treiber von Gitee klonen und installieren

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Schritt 4: Monitor-Modus aktivieren

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Schritt 5: Paket-Injektion testen

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Schritt 1: Zu China-Mirror wechseln

```bash
sudo nano /etc/apt/sources.list
```

Einfügen (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Schritt 2: Build-Abhängigkeiten installieren

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Schritt 3: Klonen und Installieren

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Schritt 4: Monitor-Modus aktivieren

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Bestätigen: `iwconfig` → suchen Sie nach `wlan1mon` mit `Mode:Monitor`.

### Schritt 5: Paket-Injektion testen

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Schritt 1: Kali ARM64 herunterladen und flashen

Offiziell: https://www.kali.org/get-kali/#kali-arm — wählen Sie Raspberry Pi 4/5 64-bit.

China-Mirror: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Standard-Anmeldedaten: **kali / kali**.

### Schritt 2: Zu China-Mirror wechseln

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Schritt 3: Build-Abhängigkeiten installieren

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Schritt 4: Treiber klonen und installieren

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Schritt 5: Monitor-Modus aktivieren

Auf einem Pi mit integriertem WLAN erscheint der AWUS036ACS als `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Schritt 6: Paket-Injektion testen

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Virtuelle Maschine USB-Passthrough {#virtuelle-maschine-usb-passthrough}

### VirtualBox

1. VM ausschalten → **Einstellungen → USB** → **USB 2.0-Controller** aktivieren.
2. Auf **+** klicken → Auswählen: **Realtek** (ID: 0bda:0811).
3. VM starten. Führen Sie `lsusb` aus, um `0bda:0811` zu bestätigen, und folgen Sie dann den obigen Kali-Schritten.

### VMware Fusion / Workstation

1. **Virtuelle Maschine → USB & Bluetooth** → **Realtek 8811AU** suchen → **Verbinden**.
2. Führen Sie `lsusb` zur Bestätigung aus und folgen Sie dann den obigen Kali-Schritten.

---

## Fehlerbehebung

| Problem | Wahrscheinliche Ursache | Lösung |
|---------|-------------------------|--------|
| `lsusb` zeigt 0bda:0811 nicht an | Adapter hat keinen Strom oder Kabel defekt | Anderen USB-Port versuchen |
| `install-driver.sh` schlägt fehl | Fehlende Header | `sudo apt install linux-headers-$(uname -r)` ausführen |
| Gitee-Clone schlägt fehl | Netzwerkproblem | Auf gitee.com nach `8821au` suchen, anderen Fork versuchen |
| `airmon-ng start` schlägt fehl | NetworkManager läuft | Zuerst `sudo airmon-ng check kill` ausführen |
| Kein Traffic im Monitor-Modus | Falscher Kanal | Kanal einstellen: `iwconfig wlan1mon channel 6` |
| Injektion "No Answer" | AP zu weit entfernt | Näher herangehen. `wlan1mon` verwenden, nicht `wlan1`. |

> **Hinweis zu VIF:** Der RTL8811AU-Treiber unterstützt keine virtuellen Schnittstellen (VIF). Gleichzeitiger Monitor- und Managed-Modus ist mit diesem Adapter nicht möglich.

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|-----------|-----|----------------|
| Offizielle Alfa-Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete |
| Alfa-Dokumentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Produkthandbücher |
| 8821au Treiber (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | RTL8811AU-Treiber |
| Tsinghua Universität Mirror | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Alibaba Cloud Mirror | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (empfohlen) |
| USTC Mirror | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (empfohlen) |
| Huawei Cloud Mirror | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM Images |

## Weitere Alfa Adapter Anleitungen für China

- [AWUS036ACH China Installationsanleitung](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, hohe Sendeleistung
- [AWUS036ACM China Installationsanleitung](/de/blog/awus036acm-china-install-guide/) — MT7612U, volle VIF-Unterstützung
- AWUS036ACS ← Sie sind hier
- [AWUS036AX China Installationsanleitung](/de/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER China Installationsanleitung](/de/blog/awus036axer-china-install-guide/) — RTL8832BU, Nano
- [AWUS036AXM China Installationsanleitung](/de/blog/awus036axm-china-install-guide/) — MT7921AUN, L-Form
- [AWUS036AXML China Installationsanleitung](/de/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Installationsanleitung](/de/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Fragen? Hinterlassen Sie unten einen Kommentar oder kontaktieren Sie uns auf [yupitek.com](https://yupitek.com/de/contact/).
