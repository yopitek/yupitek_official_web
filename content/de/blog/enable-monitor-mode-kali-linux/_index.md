---
title: "Monitor-Modus unter Kali Linux 2026 aktivieren: Komplettanleitung"
description: "Schritt-für-Schritt-Anleitung zur Aktivierung des Monitor-Modus unter Kali Linux 2024/2025 mit airmon-ng oder iw-Befehl. Unterstützt ALFA-Adapter, Troubleshooting und Überprüfung mit airodump-ng."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
---

# Monitor-Modus unter Kali Linux 2026 aktivieren: Komplettanleitung

Der Monitor-Modus ist eine der wichtigsten Funktionen für Penetration Testing unter Linux. Er ermöglicht es Ihrem WiFi-Adapter, den gesamten drahtlosen Traffic in Ihrer Umgebung — nicht nur den an Sie gerichteten — zu erfassen.

---

## Was ist Monitor-Modus?

Im Managed-Modus (dem Standardmodus) kommuniziert Ihr Adapter nur mit Access-Points, mit denen er verbunden ist. Im **Monitor-Modus** hört der Adapter auf allen Kanälen auf und erfasst **alle** 802.11-Frames in Ihrer Umgebung — einschließlich Handshakes, Deauthentication-Frames, Probe Requests und mehr.

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
