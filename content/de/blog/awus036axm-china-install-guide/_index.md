---
title: "ALFA AWUS036AXM Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036AXM-Treibern in China unter Verwendung lokaler Mirrors. MT7921AUN WiFi 6E In-Kernel-Treiber, volle Monitor-Modus- und VIF-Unterstützung. Deckt Kali Linux, Ubuntu 22/24, Debian und Raspberry Pi ab. Kein GitHub erforderlich."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Treiber-Anleitungen"]
series: ["alfa-china-install-guide"]
related_product: "/de/products/alfa/awus036axm/"
series_order: 6
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
---

Der AWUS036AXM ist der WiFi 6E Triband-Adapter von ALFA mit einem platzsparenden L-förmigen USB-A-Anschluss. Sein MT7921AUN-Chip verwendet den `mt7921u`-Treiber, der seit Version 5.18 in den Linux-Kernel integriert ist. Der L-förmige Stecker hält benachbarte USB-Anschlüsse an Laptops frei. Diese Anleitung deckt die vollständige Einrichtung ab — Firmware, Treiber-Verifizierung, Monitor-Modus, Paket-Injektion und VIF — ohne GitHub zu berühren.

## Bevor Sie beginnen

Stellen Sie sicher, dass Sie Folgendes bereit haben:

1. **ALFA AWUS036AXM** Adapter
2. Einen USB-Hub mit eigener Stromversorgung — erforderlich für Raspberry Pi
3. Aktive Internetverbindung, um lokale Mirrors zu erreichen

Schließen Sie den Adapter an und bestätigen Sie, dass Ihr System ihn erkennt:

```bash
lsusb
```

Suchen Sie nach diesem Eintrag in der Ausgabe:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

Wenn Sie `0e8d:7961` sehen, wurde der Adapter erkannt. Fahren Sie mit dem entsprechenden Abschnitt für Ihr Betriebssystem fort.

## Wählen Sie Ihr Betriebssystem

Springen Sie zum richtigen Abschnitt für Ihr Betriebssystem:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

Der MT7921AUN-Treiber ist bereits im Kali-Kernel enthalten. Alles, was Sie benötigen, ist das MediaTek-Firmware-Paket, das über lokale Mirrors verfügbar ist.

### Schritt 1: Zu China Mirror wechseln

Öffnen Sie Ihre Quellenliste im Terminal.

```bash
sudo nano /etc/apt/sources.list
```

Löschen Sie alles darin und fügen Sie diese Zeile ein:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern: Drücken Sie **Strg+O**, dann Enter, dann Strg+X zum Beenden. Aktualisieren Sie den Paketindex.

```bash
sudo apt update
```

---

### Schritt 2: Firmware installieren

Der MT7921AUN benötigt Firmware-Dateien von `firmware-misc-nonfree` und `linux-firmware`.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Schritt 3: Treiber verifizieren

Schließen Sie nach dem Neustart den Adapter an und prüfen Sie.

```bash
lsmod | grep mt7921
```

Sie sollten `mt7921u` in der Ausgabe sehen. Bestätigen Sie dann, dass eine drahtlose Schnittstelle erschienen ist.

```bash
iwconfig
```

Suchen Sie nach `wlan0` oder `wlan1`.

---

### Schritt 4: Monitor-Modus aktivieren {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

Suchen Sie nach `Mode:Monitor` auf der Schnittstelle.

---

### Schritt 5: Paket-Injektion testen {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Ein erfolgreiches Ergebnis zeigt: `Injection is working!`.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — Kernel 6.8, Plug-and-Play

Ubuntu 24.04 enthält den Treiber nativ.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Wechseln Sie zu den Aliyun-Mirrors:
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

Wechseln Sie zum Tsinghua-Mirror:

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-------------|-----|
| `lsusb` zeigt 0e8d:7961 nicht an | Stromversorgung fehlt | Anderen Port oder aktiven Hub probieren |

## China Mirror Referenz

| Ressource | URL | Verwendung für |
|----------|-----|---------|
| Offizielle Alfa Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete |
| Tsinghua Mirror | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

## Weitere Alfa Adapter Anleitungen für China

- [AWUS036ACH China Install Guide](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, High Power
- AWUS036AXM ← Sie sind hier

Fragen? Hinterlassen Sie unten einen Kommentar oder kontaktieren Sie uns auf [yupitek.com](https://yupitek.com/de/contact/).
