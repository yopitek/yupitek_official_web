---
title: "AWUS036AXML Monitor-Modus Firmware-Fix: Aktive Abstürze beheben"
description: "So beheben Sie Monitor-Modus-Firmware-Abstürze des AWUS036AXML unter Kali Linux. Deckt MT7921AUN-Firmware-Update, Kernel-Version-Anforderungen, Active-vs-Passive-Modus-Arbeitsumgehung und hcxdumptool-Alternative ab."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
featureimage: "/images/blog/awus036axml-firmware-monitor-mode-fix.webp"
faq:
  - question: "Warum stürzt AWUS036AXML im aktiven Monitor Mode ab?"
    answer: "MT7921AUN verwendet eine firmwarebasierte MAC-Architektur. Die aktuelle Kombination aus Linux mt7921u-Treiber und Firmware implementiert die für aktive Injection erforderlichen Befehlswege nicht vollständig, sodass die Schnittstelle nach der Ausführung von aireplay-ng verschwindet."
  - question: "Wie lässt sich der Absturz im aktiven Modus bei MT7921AUN beheben?"
    answer: "Das Aktualisieren des Pakets firmware-misc-nonfree auf die neueste Version, das Upgrade auf Kernel 6.6 oder höher sowie das Vermeiden von Deauth-Floods mit hoher Paketrate können das Problem verbessern, aber möglicherweise nicht vollständig beseitigen."
  - question: "Wie erfasst hcxdumptool PMKID ohne Packet Injection?"
    answer: "hcxdumptool erfasst PMKID im passiven Modus aus Beacon- und Probe-Paketen, die vom Access Point gesendet werden, ohne selbst Pakete zu senden, wodurch Firmware-Abstürze vermieden werden."
  - question: "Welche Einschränkungen gibt es beim passiven Monitoring von AWUS036AXML?"
    answer: "Beim passiven Monitoring können Beacon-, Handshake- und PMKID-Daten normal erfasst werden, jedoch können keine aktiven Aktionen wie Deauth, Probe Request oder Association Floods ausgeführt werden. Für diese Aufgaben sollte stattdessen AWUS036ACH verwendet werden."
  - question: "Welche Kernel-Versionen verbessern die Stabilität von MT7921AUN?"
    answer: "Der Kernel 6.1 LTS oder höher enthält mehrere Stabilitäts-Patches für mt7921u, während der Kernel 6.6 und höher zusätzliche Verbesserungen des MediaTek USB-Treiber-Stacks aufweist."
---
Wenn Sie den AWUS036AXML im aktiven Monitor-Modus verwenden (gleichzeitiges Überwachen und Senden von Frames), können zufällige Abstürze auftreten, die auf unzureichende Firmware-Unterstützung für aktive Überwachung beim MT7921AUN zurückzuführen sind.

# AWUS036AXML Monitor-Modus Firmware-Fix: Aktive Abstürze beheben

{{< tldr >}}
Der mt7921u-Treiber für AWUS036AXML führt bei aktiver Packet Injection zu einem Firmware-Absturz. Dieser Artikel erläutert die Ursache, Diagnose-Schritte sowie Korrekturmaßnahmen wie Firmware-Updates, Kernel-Updates und den Wechsel zu hcxdumptool für passive Erfassung.
{{< /tldr >}}

Der AWUS036AXML kann im aktiven Monitor-Modus durch MT7921AUN-Firmware-Einschränkungen einfrieren. Abhilfe schaffen ein Firmware-Update, ein Kernel-Upgrade auf 6.6 oder höher oder der Wechsel auf hcxdumptool für passives PMKID-Capture.

Der AWUS036AXML mit MT7921AUN-Chipsatz bietet erstklassige Wi-Fi-6E-Leistung unter Kali Linux, hat jedoch einige Firmware-bezogene Probleme im aktiven Monitor-Modus. Dieser Leitfaden zeigt Ihnen, wie Sie diese beheben können.

---

## Das Problem: Firmware-bedingte Abstürze im aktiven Modus

**Symptome:**
- Monitor-Modus startet erfolgreich, stürzt jedoch nach einigen Minuten ab
- `hcxdumptool` zeigt "Firmware not responding"
- Paketinjektion funktioniert, aber mit erhöhter Latenz

**Lösung:** Aktualisieren Sie die MT7921AUN-Firmware auf die neueste Version.

---

## Firmware-Update-Prozess

```bash
# Aktuelle Firmware-Version prüfen
modinfo mt7921u | grep version

# Linux-Firmware-Paket aktualisieren
sudo apt update && sudo apt install --reinstall linux-firmware

# Modul neu laden
sudo modprobe -r mt7921u
sudo modprobe mt7921u

# Überprüfen
dmesg | grep mt7921u
```

---

## Active-vs-Passive-Modus-Arbeitsumgehung

Wenn das Firmware-Update allein nicht ausreicht, können Sie zwischen aktivem und passivem Monitoring wechseln:

```bash
# Passiver Monitor-Modus (stabil, aber keine Frame-Sendung)
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up

# Aktiver Monitor-Modus (mit Frame-Sendung)
sudo airmon-ng start wlan0
```

---

## hcxdumptool-Alternative

Als Alternative zu standardmäßigen Monitor-Modus-Tools können Sie `hcxdumptool` verwenden, das besser mit der MT7921AUN-Firmware funktioniert:

```bash
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1
```

---

{{< faq >}}

## Zusammenfassung

| Problem | Lösung | Erwarteter Erfolg |
|---|---|---|
| Firmware-Abstürze | `linux-firmware` aktualisieren | Stabil |
| Hohe Latenz | Passiver Modus | Sofortige Reaktion |
| hcxdumptool-Fehler | Firmware-Update + aktiver Modus | Zuverlässig |

## Referenzen

1. [Linux firmware Repository（kernel.org）](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git)
2. [Linux Kernel mt76 Treiber](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
3. [aircrack-ng Werkzeugsatz](https://www.aircrack-ng.org/)
4. [hcxdumptool GitHub-Projekt](https://github.com/ZerBea/hcxdumptool)
5. [ALFA Network OffizielleUnterstuetzung](https://www.alfa.com.tw/)
