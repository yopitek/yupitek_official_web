---
title: "ALFA-Treiber nach Kernel-Update defekt? So beheben Sie es"
description: "ALFA-USB-WiFi-Adapter funktioniert nach Linux-Kernel-Update nicht? Komplette Fix-Anleitung für RTL8812AU, RTL8811AU und MT7921AUN-Treiber unter Kali Linux und Ubuntu nach Kernel-Updates."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
featureimage: "/images/blog/fix-alfa-driver-kernel-update.webp"
faq:
  - question: "Warum fallen ALFA-Netzwerkkarten nach einem Kernel-Update aus?"
    answer: "RTL8812AU verwendet einen Kernel-External-Treiber; nach jeder Änderung der Kernel-Version sind die zuvor kompilierten Module nicht mehr kompatibel. DKMS kann die Neukompilierung automatisch durchführen, jedoch führt das Fehlen von Kernel-Headern oder veralteten Konfigurationen zu Fehlern."
  - question: "Wie können Sie die Ursache für das Versagen von ALFA-Treibern schnell diagnostizieren?"
    answer: "Führen Sie uname -r aus, um die Kernel-Version zu bestätigen, prüfen Sie dann den Build-Status der Module mit dkms status und verwenden Sie abschließend dmesg, um Fehlermeldungen zur Firmware oder zum Laden der Module anzuzeigen."
  - question: "Was ist die schnellste Methode zur Behebung eines Ausfalls von RTL8812AU-Treibern?"
    answer: "Installieren Sie die passenden Kernel-Header und führen Sie dkms autoinstall aus. Falls dies fehlschlägt, kopieren Sie das Repository von aircrack-ng/rtl8812au neu und führen Sie make dkms_install aus."
  - question: "Was tun, wenn eine MT7921AUN-Netzwerkkarte nach einem Kernel-Update keine Verbindung mehr herstellen kann?"
    answer: "MT7921AUN verwendet einen im Kernel integrierten Treiber; das Problem liegt meist an der Firmware. Installieren Sie das Paket firmware-misc-nonfree und stellen Sie sicher, dass die Kernel-Version mindestens 5.18 beträgt."
  - question: "Wie können Sie verhindern, dass Kernel-Updates die Treiber erneut beschädigen?"
    answer: "Verwenden Sie anstelle von `apt upgrade` den Befehl `apt full-upgrade`, um sicherzustellen, dass Header und Kernel synchron installiert werden. Installieren Sie die Metapakete `dkms` und `linux-headers-generic`, um die Abhängigkeiten aufrechtzuerhalten."

---
Nach einem Kernel-Update (z.B. über `apt upgrade`) ist Ihr ALFA-Adapter möglicherweise nicht mehr erkennbar oder der Monitor-Modus funktioniert nicht mehr.

# ALFA-Treiber nach Kernel-Update defekt? So beheben Sie es

{{< tldr >}}
Das Hauptproblem, das die ALFA-Treiber durch Kernel-Updates beschädigt, ist die Asynchronität zwischen Header-Dateien und Modulen. RTL8812AU wird über dkms autoinstall neu erstellt, für MT7921AUN muss firmware-misc-nonfree installiert werden, und zur langfristigen Behebung wird apt full-upgrade verwendet.
{{< /tldr >}}

Ein ALFA-Adapter, der nach einem Kernel-Update ausfällt, ist das häufigste Problem von Linux-Nutzern. Der RTL8812AU muss über DKMS neu gebaut werden, der MT7921AUN benötigt ein Firmware-Paket. Beide lassen sich mit systematischen Schritten in 15 Minuten beheben.

Ein Linux-Kernel-Update bricht häufig die ALFA-USB-WiFi-Treiber, insbesondere wenn Sie den Treiber ohne DKMS installiert haben. Dieser Leitfaden zeigt Ihnen die Ursache und die Lösung.

---

## Das Problem

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

{{< faq >}}

## Prävention: Automatische Neukompilierung

Mit DKMS wird der Treiber automatisch bei jedem Kernel-Update neu kompiliert. Sie müssen sich keine Sorgen mehr关于 kaputte Treiber nach Updates machen.

## Referenzen

1. [aircrack-ng Offizielle rtl8812au Treiber](https://github.com/aircrack-ng/rtl8812au)
2. [DKMS Offizielle Dokumentation](https://github.com/dell/dkms)
3. [Kali Linux Paketverwaltungsdokumentation](https://www.kali.org/docs/general-use/package-management/)
4. [Linux Kernel Offizielle Dokumentation](https://www.kernel.org/doc/html/latest/)
5. [MediaTek MT7921 Treiber](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt7921)
