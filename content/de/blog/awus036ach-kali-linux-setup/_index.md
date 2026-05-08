---
title: "ALFA AWUS036ACH Einrichtungshandbuch für Kali Linux: Monitor-Modus & Packet Injection (2026)"
description: "Schritt-für-Schritt-Anleitung zur Installation des ALFA AWUS036ACH unter Kali Linux 2024/2025, Aktivierung des Monitor-Modus mit airmon-ng und Überprüfung der Packet Injection — einschließlich Treiber-Installationsbefehle."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "kali-linux", "monitor-mode", "packet-injection", "RTL8812AU", "airmon-ng"]
---

Die meisten Benutzer stoßen auf drei Hauptprobleme beim Einrichten des AWUS036ACH unter Kali: Der Treiber kompiliert nicht, die VM leitet das USB-Gerät nicht weiter oder der Monitor-Modus funktioniert stillschweigend nicht. Dieses Handbuch deckt alle drei ab, plus die vollständige Setup-Anleitung von Grund auf.

{{< alert "circle-info" >}}
Nutzen Sie **VirtualBox oder VMware**? Springen Sie zuerst zum Abschnitt [USB-Weiterleitung](#usb-passthrough-in-virtualbox-and-vmware) — dies ist das häufigste Setup-Problem. Verwenden Sie **macOS** oder **Windows** als Host-Betriebssystem? Siehe die [ALFA unter macOS](/fr/blog/alfa-adapter-macos-vm-setup/) oder [ALFA unter Windows](/fr/blog/alfa-adapter-windows-10-11-setup/) Anleitungen.
{{< /alert >}}

---

## Warum der AWUS036ACH die erste Wahl ist

Bevor wir in die Befehle eintauchen, lohnt es sich zu verstehen, was diesen Adapter besonders macht.

**Der RTL8812AU Chipsatz**

Realteks RTL8812AU ist ein Dual-Band (2,4 + 5 GHz) 802.11ac-Chipsatz mit robuster Unterstützung für die auf Ebene der Frames erforderlichen Operationen. Der Open-Source-Treiber, der bei `aircrack-ng/rtl8812au` auf GitHub gepflegt wird, ist das Ergebnis jahrelanger Zusammenarbeit zwischen dem Aircrack-ng-Team und der breiteren Linux-Sicherheitscommunity. Er wird aktiv gewartet, regelmäßig mit neuen Kernel-Versionen getestet und hat explizite Unterstützung für Monitor-Modus und Packet Injection — nicht als nachträgliche Funktion.

**Community-Support Seit 2017**

Wenn Sie ein Problem mit dem AWUS036ACH haben, finden Sie Antworten. Der Adapter erscheint in Tausenden von Forenbeiträgen, YouTube-Tutorials, Hack-The-Walkthroughs, Offensive-Security-Kursmaterialien und GitHub-Issues. Die Wissensdatenbank für Troubleshooting ist unübertroffen von jedem anderen Adapter.

Sie können ihn in unserem Shop finden: [ALFA AWUS036ACH](/fr/products/alfa/awus036ach/).

---

## Zusammenfassung

| Schritt | Befehl |
|---|---|
| Erkennung prüfen | `lsusb \| grep Realtek` |
| Abhängigkeiten installieren | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| Treiber klonen | `git clone https://github.com/aircrack-ng/rtl8812au` |
| Erstellen & installieren | `make && sudo make install` |
| Modul laden | `sudo modprobe 88XXau` |
| Störende Prozesse töten | `sudo airmon-ng check kill` |
| Monitor-Modus aktivieren | `sudo airmon-ng start wlan0` |
| Monitor-Modus verify | `iwconfig wlan0mon` |
| Injection testen | `sudo aireplay-ng --test wlan0mon` |
| Geschätzte Zeit | ~15 Minuten (frisches System) |

Der [ALFA AWUS036ACH](/fr/products/alfa/awus036ach/) kombiniert mit Kali Linux 2024+ und dem aircrack-ng RTL8812AU-Treiber bleibt der zuverlässigste, am besten dokumentierte WiFi-Adapter-Setup in der Penetration-Testing-Community.
