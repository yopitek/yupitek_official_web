---
title: "ALFA-Treiber nach Kernel-Update defekt? So beheben Sie es"
description: "ALFA-USB-WiFi-Adapter funktioniert nach Linux-Kernel-Update nicht? Komplette Fix-Anleitung für RTL8812AU, RTL8811AU und MT7921AUN-Treiber unter Kali Linux und Ubuntu nach Kernel-Updates."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
featureimage: "/images/blog/fix-alfa-driver-kernel-update.webp"
---

# ALFA-Treiber nach Kernel-Update defekt? So beheben Sie es

Ein Linux-Kernel-Update bricht häufig die ALFA-USB-WiFi-Treiber, insbesondere wenn Sie den Treiber ohne DKMS installiert haben. Dieser Leitfaden zeigt Ihnen die Ursache und die Lösung.

---

## Das Problem

Nach einem Kernel-Update (z.B. über `apt upgrade`) ist Ihr ALFA-Adapter möglicherweise nicht mehr erkennbar oder der Monitor-Modus funktioniert nicht mehr.

**Ursache:** Der alte Treiber wurde für den vorherigen Kernel kompiliert und passt nicht zum neuen Kernel.

---

## Schnelle Diagnose

```bash
# Prüfen, ob der Adapter erkannt wird
lsusb | grep -E "0bda|Realtek"

# Prüfen, ob der Treiber geladen ist
lsmod | grep -E "88XXau|mt7921u|mt76"

# DKMS-Status überprüfen
dkms status
```

---

## Lösung 1: Treiber neu kompilieren (schnell)

```bash
cd /pfad/zu/rtl8812au
make clean
make
sudo make install
sudo modprobe 88XXau
```

---

## Lösung 2: DKMS installieren (persistent)

Für eine dauerhafte Lösung empfehlen wir die DKMS-Installation:

```bash
# DKMS entfernen und neu installieren
sudo dkms remove rtl8812au/5.6.4.2 --all
cd rtl8812au
sudo make dkms_install

# Überprüfen
dkms status
# Erwartet: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## Prävention: Automatische Neukompilierung

Mit DKMS wird der Treiber automatisch bei jedem Kernel-Update neu kompiliert. Sie müssen sich keine Sorgen mehr关于 kaputte Treiber nach Updates machen.
