---
title: "Vollständige Anleitung: Installation aller Alfa USB-WiFi-Adapter unter Linux in China - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Treiber-Anleitungen"]
series: ["Alfa China Installationsanleitung"]
description: "Die ultimative Anleitung zur Installation aller Alfa USB-WiFi-Adapter unter Linux in China. Deckt Kali Linux, Ubuntu 22/24, Debian und Raspberry Pi ab. Kein GitHub erforderlich - nur lokale Mirrors verwenden."
---

## Willkommen zur ultimativen Alfa Linux Installationsanleitung

Wenn Sie dies lesen, haben Sie wahrscheinlich einen Alfa USB-WiFi-Adapter gekauft und sind steckengeblieben, weil:

- Sie sich in China befinden und nicht auf GitHub zugreifen können
- Die Treiberinstallation kompliziert erscheint
- Sie den Monitor-Modus und die Paket-Injektion für Wireless-Tests aktivieren müssen
- Sie nicht sicher sind, welchen Treiber Ihr spezielles Alfa-Modell benötigt

Diese Anleitung löst **all diese Probleme**. Wir führen Sie durch die Installation **jedes Alfa USB-WiFi-Adapters** auf **allen wichtigen Linux-Distributionen** unter Verwendung von **in China zugänglichen Mirrors**. Kein GitHub. Kein Frust.

---

## Warum diese Anleitung existiert

Alfa USB-WiFi-Adapter sind bei Penetrationstestern, Netzwerkingenieuren und Wireless-Enthusiasten beliebt. Sie unterstützen den Monitor-Modus und die Paket-Injektion — Funktionen, die die meisten herkömmlichen WiFi-Adapter nicht haben.

Aber hier ist das Problem: **Die meisten Anleitungen zur Treiberinstallation setzen voraus, dass Sie auf GitHub zugreifen können**. In China ist das oft nicht möglich. Diese Anleitung wurde speziell für Benutzer in China entwickelt und verwendet nur Mirrors und Ressourcen, die innerhalb der chinesischen Internet-Infrastruktur funktionieren.

---

## Kurze Modell-Referenz

Bevor wir eintauchen, lassen Sie uns herausfinden, welchen Alfa-Adapter Sie haben und welchen Chip er verwendet:

### AX-Serie (Wi-Fi 6 / 802.11ax)

| Modell | Chipsatz | Treiber | Am besten für |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | Allgemeine Nutzung, gute Reichweite |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Kompaktes Design |

### AC-Serie (Wi-Fi 5 / 802.11ac)

| Modell | Chipsatz | Treiber | Am besten für |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | Hohe Leistung, große Reichweite |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Beste VIF-Unterstützung**, Plug-and-Play |

---

## Bevor Sie beginnen: Was Sie benötigen

Stellen Sie sicher, dass Sie Folgendes bereit haben:

1. **Alfa USB-WiFi-Adapter** — Das richtige Modell für Ihre Bedürfnisse
2. **USB-Kabel** — Das mitgelieferte Kabel funktioniert einwandfrei
3. **USB-Hub mit Stromversorgung** — Erforderlich für Raspberry Pi
4. **Aktive Internetverbindung** — Um lokale Mirrors in China zu erreichen
5. **Sudo-Rechte** — Sie benötigen Administratorzugriff

Schließen Sie den Adapter zuerst an, um zu prüfen, ob Ihr System ihn erkennt:

```bash
lsusb
```

---

## In China zugängliche Mirror-Referenz

Alle Ressourcen in dieser Anleitung verwenden diese in China zugänglichen Mirrors:

| Ressource | URL | Verwendung für |
|----------|-----|---------|
| **Offizielle Alfa-Downloads** | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete, Firmware |
| **Tsinghua-Universität Mirror** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **Aliyun Mirror** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (empfohlen) |
| **Gitee (GitHub-Alternative)** | [gitee.com](https://gitee.com) | Treiber-Quellcode |

---

## Kali Linux Installation

Kali Linux wird mit vorinstallierten Wireless-Tools geliefert. Die Einrichtung von Alfa-Adaptern erfordert nur wenige Schritte.

### Schritt 1: Zu China Mirror wechseln

```bash
sudo nano /etc/apt/sources.list
```

Ersetzen Sie alles durch:
`deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

```bash
sudo apt update
```

### Schritt 2: Treiber nach Chipsatz installieren

#### AX-Serie (RTL8832BU)
`sudo apt install -y rtl8832bu-dkms`

#### AC-Serie - Realtek (RTL8812AU / RTL8811AU)
`sudo apt install -y realtek-rtl88xxau-dkms`

---

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-------------|-----|
| `lsusb` zeigt ID nicht an | Schlechtes Kabel | Anderen USB-Port probieren |
| Monitor-Modus startet nicht | NetworkManager stört | `sudo airmon-ng check kill` ausführen |

---

## Fazit

Diese Anleitung deckt **alle Alfa USB-WiFi-Adapter** auf **allen wichtigen Linux-Distributionen** ab, unter Verwendung von **Ressourcen, die in China funktionieren**.

**Fragen oder Probleme?** Schauen Sie sich die spezifischen Modell-Anleitungen in unserer Serie an oder kontaktieren Sie uns auf [yupitek.com](https://yupitek.com/de/contact/).

---

*Zuletzt aktualisiert: 24. April 2026*
