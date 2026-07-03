---
title: "Monitor-Modus unter Kali Linux 2026 aktivieren: Komplettanleitung"
description: "Schritt-für-Schritt-Anleitung zur Aktivierung des Monitor-Modus unter Kali Linux 2024/2025 mit airmon-ng oder iw-Befehl. Unterstützt ALFA-Adapter, Troubleshooting und Überprüfung mit airodump-ng."
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
faq:
  - question: "Was ist der Unterschied zwischen Monitor-Modus und Managed-Modus?"
    answer: "Der Monitor-Modus ermöglicht es der Netzwerkkarte, alle 802.11-Frames im Funkverkehr zu erfassen, ohne durch den Managed-Modus eingeschränkt zu sein, der nur Pakete empfängt, deren Ziel-MAC-Adresse mit der eigenen übereinstimmt. Dies ist die Grundlage für drahtlose Penetrationstests."
  - question: "Was ist der Unterschied zwischen der Aktivierung des Monitor-Modus mit airmon-ng und dem iw-Befehl?"
    answer: "airmon-ng verarbeitet automatisch störende Prozesse und erstellt eine virtuelle Schnittstelle namens wlan0mon; iw hingegen ändert direkt die bestehende Schnittstelle, ohne eine neue zu erstellen, was sich für präzise Kontrollen eignet."
  - question: "Was tun, wenn die Schnittstelle nach Aktivierung des Monitor-Modus automatisch in den Managed-Modus zurückwechselt?"
    answer: "Dies wird durch den Neustart von wpa_supplicant oder NetworkManager im Hintergrund verursacht. Die Ausführung von airmon-ng check kill zur Beendigung dieser Prozesse löst das Problem."
  - question: "Welche ALFA-Netzwerkkarten unterstützen den Monitor-Modus unter Kali Linux vollständig?"
    answer: "Die Modelle AWUS036ACH (RTL8812AU), AWUS036AXML (MT7921AUN) und AWUS036ACM (MT7612U) werden alle vollständig unterstützt, wobei das ACM-Modul Plug-and-Play-fähig ist."
  - question: "Wie behebt man den Fehler „Fixed channel wlan0mon: -1“, der von airodump-ng angezeigt wird?"
    answer: "Zeigt an, dass airodump-ng den Kanal nicht wechseln kann. Führen Sie iwconfig wlan0mon channel 1 aus, um den Kanal festzulegen, und beenden Sie die verbleibenden wpa_supplicant-Prozesse."

---
Im Managed-Modus (dem Standardmodus) kommuniziert Ihr Adapter nur mit Access-Points, mit denen er verbunden ist. Im **Monitor-Modus** hört der Adapter auf allen Kanälen auf und erfasst **alle** 802.11-Frames in Ihrer Umgebung — einschließlich Handshakes, Deauthentication-Frames, Probe Requests und mehr.

# Monitor-Modus unter Kali Linux 2026 aktivieren: Komplettanleitung

{{< tldr >}}
Der Monitor-Modus hebt die Einschränkung der Netzwerkkarte auf, nur eigene Pakete zu empfangen, und bildet die Grundlage für drahtlose Penetrationstests. Mit airmon-ng oder dem iw-Befehl in Kombination mit einer ALFA-Netzwerkkarte kann er unter Kali Linux stabil aktiviert werden.
{{< /tldr >}}

Der Monitor-Modus ermöglicht es dem WLAN-Adapter, alle 802.11-Frames in der Luft zu erfassen, und bildet die Grundlage für Tools wie airodump-ng, Wireshark und Kismet. Unter Kali Linux wird er über airmon-ng oder den iw-Befehl aktiviert.

Der Monitor-Modus ist eine der wichtigsten Funktionen für Penetration Testing unter Linux. Er ermöglicht es Ihrem WiFi-Adapter, den gesamten drahtlosen Traffic in Ihrer Umgebung — nicht nur den an Sie gerichteten — zu erfassen.

---

## Was ist Monitor-Modus?

---

## Methode A: airmon-ng (Empfohlen)

```bash
# Störende Prozesse überprüfen und töten
sudo airmon-ng check kill

# Monitor-Modus starten
sudo airmon-ng start wlan0

# Überprüfen
iwconfig
```

Sie sollten `wlan0mon` als Monitor-Schnittstelle sehen.

---

## Methode B: iw (Manuell)

```bash
# Interface herunterfahren
sudo ip link set wlan0 down

# Auf Monitor-Modus umschalten
sudo iw dev wlan0 set type monitor

# Wieder hochfahren
sudo ip link set wlan0 up
```

---

## Überprüfung mit airodump-ng

```bash
sudo airodump-ng wlan0mon
```

Sie sollten sofort WiFi-Netzwerke in der Ausgabe sehen. Drücken Sie `Strg+C` zum Stoppen.

---

## Kompatible ALFA-Adapter

| Adapter | Chipsatz | airmon-ng | iw |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✓ | ✓ |
| AWUS036AXML | MT7921AUN | ✓ | ✓ |
| AWUS036ACM | MT7612U | ✓ | ✓ |
| AWUS036AX | RTL8832BU | ✓ | ✓ |

---

{{< faq >}}

## Troubleshooting

**Problem:** Interface nicht gefunden

**Lösung:** Stellen Sie sicher, dass der Treiber geladen ist:

```bash
lsmod | grep -E "88XXau|mt7921u|mt76"
```

**Problem:** Monitor-Modus startet, aber kein Traffic

**Lösung:** Überprüfen Sie den aktuellen Kanal und setzen Sie ihn manuell:

```bash
iwconfig wlan0mon
sudo iwconfig wlan0mon channel 6
```

## Referenzen

1. [aircrack-ng Offizielle Dokumentation](https://www.aircrack-ng.org/documentation.html)
2. [Kali Linux Offizielle Dokumentation](https://www.kali.org/docs/)
3. [Linux Wireless mac80211 Subsystem](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [iw-Befehlsverwendungshinweise](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
