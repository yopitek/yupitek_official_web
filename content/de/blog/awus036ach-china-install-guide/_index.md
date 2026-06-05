---
title: "ALFA AWUS036ACH Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
description: "Schritt-für-Schritt-Anleitung zur Installation des ALFA AWUS036ACH-Treibers in China mit inländischen Mirrors. Für Kali Linux, Ubuntu 22/24, Debian und Raspberry Pi. Kein GitHub erforderlich."
related_product: "/de/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
---

Du hast den AWUS036ACH bekommen und dein Linux erkennt ihn nicht. Das ist normal — dieser Chip braucht den RTL8812AU-Treiber, der nicht automatisch funktioniert. Diese Anleitung führt dich in etwa 30 Minuten durch die vollständige Installation, ausschließlich mit inländischen Mirrors. GitHub-Zugang ist nicht erforderlich.

## Vorbereitung

Stelle sicher, dass du folgendes bereit hast:

1. **ALFA AWUS036ACH** Adapter
2. USB-Kabel (das mitgelieferte Kabel reicht aus)
3. Aktiver USB-Hub mit eigener Stromversorgung — erforderlich beim Raspberry Pi
4. Aktive Internetverbindung zu inländischen Mirrors

Schließe den Adapter an und bestätige, dass das System ihn erkennt:

```bash
lsusb
```

Suche in der Ausgabe nach dieser Zeile:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

Wenn du `0bda:8812` siehst, wurde der Adapter erkannt. Gehe zum passenden OS-Abschnitt unten.

Wenn er nicht erscheint, probiere einen anderen USB-Port oder tausche das Kabel aus und führe `lsusb` erneut aus.

## Betriebssystem wählen

Springe zum richtigen Abschnitt für dein OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Bereits installiert? Springe direkt zu:

- [Monitor-Modus aktivieren](#monitor-modus-aktivieren)
- [Paketinjektion testen](#paketinjektion-testen)
- [VM USB-Durchleitung](#usb-durchleitung-f%C3%BCr-virtuelle-maschinen)

---

## Kali Linux

Kali wird mit leistungsstarken Wireless-Tools geliefert. Den AWUS036ACH-Treiber zum Laufen zu bringen dauert vier Schritte. Fange damit an, zu einem schnellen chinesischen Mirror zu wechseln, damit alle Downloads schnell bleiben.

### Schritt 1: Auf China-Mirror umstellen

Öffne die Quellenliste im Terminal.

```bash
sudo nano /etc/apt/sources.list
```

Lösche alles darin und füge diese eine Zeile ein:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern: **Ctrl+O**, dann Enter, dann Ctrl+X zum Beenden. Aktualisiere den Paketindex.

```bash
sudo apt update
```

> **Backup-Mirror:** Wenn 中科大 (USTC) bei dir langsam ist, verwende stattdessen 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Schritt 2: Treiber installieren

Kalis Paketrepository enthält einen vorgefertigten DKMS-Treiber. Installiere ihn mit einem Befehl.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS kompiliert den Treiber automatisch neu, wenn der Kernel aktualisiert wird. Du musst ihn nach einem Upgrade nicht manuell neu installieren.

Überprüfe, ob der Treiber korrekt geladen wurde.

```bash
modinfo 88XXau | grep -E "filename|version"
```

Du solltest eine `filename`-Zeile sehen, die auf `.ko` endet, und eine `version`-Zeile mit einem Versions-String wie `5.6.4.2`. Wenn beide erscheinen, ist der Treiber bereit.

---

### Schritt 2 (Alternative): Manuelles Kompilieren aus dem Quellcode

Folge diesem Abschnitt nur, wenn `apt install` oben fehlgeschlagen ist. Installiere zuerst die Build-Abhängigkeiten.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Lade den Treiber-Quellcode von Gitee herunter.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **HINWEIS:** Wenn diese URL nicht lädt, suche auf Gitee nach `rtl8812au` und wähle den zuletzt aktualisierten Fork. Du kannst auch ein Quellcode-Archiv direkt von [files.alfa.com.tw](https://files.alfa.com.tw) herunterladen.

Wechsle in das geklonte Verzeichnis, dann kompiliere und installiere.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Lade den Treiber in den laufenden Kernel.

```bash
sudo modprobe 88XXau
```

---

### Schritt 3: Monitor-Modus aktivieren {#monitor-modus-aktivieren}

Bevor du den Adapter in den Monitor-Modus versetzt, prüfe, welchen Interface-Namen dein System ihm zugewiesen hat.

```bash
iwconfig
```

Suche nach einem `wlan0`- oder `wlan1`-Eintrag. Verwende diesen Namen in den folgenden Befehlen.

Stoppe NetworkManager und wpa_supplicant — beide beanspruchen den Adapter und blockieren den Monitor-Modus.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Bestätige, dass der Wechsel funktioniert hat.

```bash
iwconfig
```

Suche nach einem Eintrag wie `wlan0mon` mit `Mode:Monitor`. Wenn du das siehst, ist der Adapter für die Paketerfassung bereit.

---

### Schritt 4: Paketinjektion testen {#paketinjektion-testen}

Führe den Injektionstest gegen das Monitor-Interface aus.

```bash
sudo aireplay-ng --test wlan0mon
```

Ein erfolgreiches Ergebnis sieht so aus:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Wenn der Test fehlschlägt, starte den Rechner neu und führe den Test erneut aus. Wenn es nach einem Neustart immer noch fehlschlägt, prüfe, ob kein anderer Prozess das Interface hält — führe `iwconfig` aus und stelle sicher, dass nur `wlan0mon` erscheint und nichts anderes den Adapter beansprucht.

---

## Ubuntu 22.04 / 24.04

Ubuntu teilt sich in zwei Zweige mit unterschiedlichen Paketdatei-Formaten auf. Die folgenden Schritte decken beide ab. Verwende **阿里云 (Aliyun)** als deinen Mirror — er ist schnell, zuverlässig und wird von Alibaba gepflegt.

### Schritt 1: Auf China-Mirror umstellen

Wähle deine Ubuntu-Version und folge nur dem entsprechenden Pfad.

#### Ubuntu 24.04 (Noble)

Öffne die neue DEB822-Format-Quellendatei:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Lösche alles in der Datei und füge genau diesen Inhalt ein:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Speichern mit `Ctrl+O`, dann beenden mit `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Öffne stattdessen die klassische Quellendatei:

```bash
sudo nano /etc/apt/sources.list
```

Ersetze alle vorhandenen Zeilen durch:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Speichere und beende genauso (`Ctrl+O`, dann `Ctrl+X`).

#### Paketindex aktualisieren

Führe dies für beide Versionen nach dem Bearbeiten der Quellendatei aus:

```bash
sudo apt update
```

---

### Schritt 2: Build-Abhängigkeiten installieren

Der Treiber wird aus dem Quellcode kompiliert, daher brauchst du zuerst die Kernel-Header und Build-Tools:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Dies lädt gcc, make und die genauen Header herunter, die zu deinem laufenden Kernel passen. Der `$(uname -r)`-Teil erkennt deine Kernel-Version automatisch — du musst sie nicht manuell eingeben.

---

### Schritt 3: Treiber-Quellcode herunterladen (China-Mirror)

Klone das Treiber-Repository von Gitee, das in China zugänglich ist:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Wechsle dann in den geklonten Ordner:

```bash
cd rtl8812au
```

> **Hinweis:** Wenn diese URL einen Timeout oder 404 zurückgibt, gehe zu [gitee.com](https://gitee.com) und suche nach `rtl8812au`. Wähle den Fork mit dem neuesten Commit-Datum.

---

### Schritt 4: Kompilieren und installieren

Baue das Kernel-Modul aus dem Quellcode:

```bash
make
```

Installiere es in das System:

```bash
sudo make install
```

Registriere das Modul bei DKMS, damit es Kernel-Upgrades übersteht:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Lade das Modul in den laufenden Kernel:

```bash
sudo modprobe 88XXau
```

Überprüfe, ob das Modul korrekt geladen wurde:

```bash
modinfo 88XXau | grep filename
```

Du solltest einen Pfad sehen, der auf `88XXau.ko` oder ähnliches endet. Wenn der Befehl eine Ausgabe zurückgibt, ist der Treiber aktiv.

---

### Schritt 5: Monitor-Modus aktivieren

Beende zunächst alle Prozesse, die das Wireless-Interface stören könnten:

```bash
sudo airmon-ng check kill
```

Versetze den Adapter dann in den Monitor-Modus:

```bash
sudo airmon-ng start wlan0
```

> **Hinweis:** Dein Interface könnte `wlan1` statt `wlan0` heißen. Führe zuerst `iwconfig` aus, um alle Wireless-Interfaces aufzulisten, und ersetze dann den korrekten Namen im obigen Befehl.

---

### Schritt 6: Paketinjektion testen

Mit dem Adapter im Monitor-Modus führe den Injektionstest aus:

```bash
sudo aireplay-ng --test wlan0mon
```

Ein erfolgreiches Ergebnis zeigt Zeilen wie `Injection is working!`. Wenn du Fehler über das Interface siehst, prüfe mit `iwconfig wlan0mon`, ob der Monitor-Modus aktiv ist.

---

## Debian

Debians Paketmanager zeigt standardmäßig auf Overseas-Server. Der Wechsel zum 清华大学 (Tsinghua University) Mirror bringt die Download-Geschwindigkeit von Schneckenzeit auf Rennstrecke.

### Schritt 1: Auf China-Mirror umstellen

Öffne die Quellenliste:

```bash
sudo nano /etc/apt/sources.list
```

Lösche alles darin und füge diese drei Zeilen ein (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Speichern mit `Ctrl+O`, dann beenden mit `Ctrl+X`. Paketindex aktualisieren:

```bash
sudo apt update
```

### Schritt 2: Build-Abhängigkeiten installieren

Der AWUS036ACH-Treiber wird aus dem Quellcode kompiliert, daher brauchst du die Kernel-Header und Build-Tools:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Dieser Befehl installiert das zum laufenden Kernel passende Header-Paket automatisch.

### Schritt 3: Treiber-Quellcode herunterladen (China-Mirror)

Klone das Treiber-Repository von Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Wechsle in den Projektordner:

```bash
cd rtl8812au
```

> **URL nicht erreichbar?** Suche auf Gitee nach `rtl8812au` und wähle den zuletzt aktualisierten Fork.

### Schritt 4: Kompilieren und installieren

Führe diese Befehle der Reihe nach im `rtl8812au`-Ordner aus:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` registriert den Treiber, damit er Kernel-Updates automatisch übersteht.

### Schritt 5: Monitor-Modus aktivieren

**Beende störende Prozesse** bevor du den Modus wechselst:

```bash
sudo airmon-ng check kill
```

Starte den Monitor-Modus auf deinem Adapter:

```bash
sudo airmon-ng start wlan0
```

Wenn `airmon-ng` fehlt, installiere es zuerst:

```bash
sudo apt install -y aircrack-ng
```

Bestätige, dass das Interface hochgekommen ist:

```bash
iwconfig
```

Suche in der Ausgabe nach einem Interface namens `wlan0mon`.

### Schritt 6: Paketinjektion testen

```bash
sudo aireplay-ng --test wlan0mon
```

Ein Strom von Injektionstestergebnissen bestätigt, dass der Adapter funktioniert. Du bist startklar.

---

## Raspberry Pi 4B / 5

> Der AWUS036ACH zieht ca. 500mW. Ihn direkt an einen Raspberry-Pi-USB-Port anzuschließen kann dazu führen, dass der Pi unter Last drosselt oder neu startet. **Verwende immer einen USB-Hub mit eigener Stromversorgung.**

---

### Schritt 1: Kali Linux ARM64-Image herunterladen

Gehe auf die offizielle Kali ARM-Download-Seite:
https://www.kali.org/get-kali/#kali-arm

Wähle **Raspberry Pi 4 (64-bit)** oder **Raspberry Pi 5 (64-bit)** passend zu deinem Board. Lade nicht das 32-Bit-Image herunter — der Treiber-Build erfordert einen 64-Bit-Kernel.

> **China-Mirror:** Wenn kali.org langsam lädt, versuche stattdessen 华为云:
> https://repo.huaweicloud.com/kali-images/
> Navigiere zum neuesten Release-Ordner und lade das gleiche ARM64-Image von dort herunter.

---

### Schritt 2: Auf MicroSD flashen

Stecke deine microSD-Karte ein und prüfe den Gerätepfad bevor du schreibst.

```bash
lsblk
```

Finde deine Karte in der Liste — sie erscheint als etwas wie `sdb` oder `mmcblk0`. Flashe dann das Image und ersetze `/dev/sdX` mit deinem tatsächlichen Pfad.

```bash
# Ersetze /dev/sdX mit deiner tatsächlichen SD-Karte (prüfe mit lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Warte auf den Abschluss von `sync`, bevor du die Karte herausziehst. Starte den Pi von der Karte. Standard-Anmeldedaten nach dem Start: **kali / kali**.

---

### Schritt 3: Auf China-Mirror umstellen

Nach dem ersten Start öffne die Paketquellen-Datei.

```bash
sudo nano /etc/apt/sources.list
```

Lösche alles in der Datei und ersetze es durch diese eine Zeile:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern: **Ctrl+O**, dann Enter, dann Ctrl+X. Wende den Mirror an und aktualisiere das System.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Der Neustart übernimmt Kernel-Updates bevor du den Treiber installierst.

---

### Schritt 4: Treiber installieren (ARM64)

Das DKMS-Paket funktioniert auf ARM64 genau wie auf x86 — keine besonderen Schritte notwendig.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

Wenn dieser Befehl einen Fehler zurückgibt, dass das Paket nicht gefunden wurde, kompiliere den Treiber stattdessen aus dem Quellcode.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Schritt 5: Monitor-Modus aktivieren

Prüfe vor dem Anfassen des Adapters, welchen Interface-Namen der Pi ihm zugewiesen hat.

```bash
iwconfig
```

Auf einem Pi mit eingebautem WLAN-Chip erscheint der AWUS036ACH als `wlan1` — das eingebaute Radio belegt `wlan0`. Verwende den Namen, den `iwconfig` oben gemeldet hat.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Führe `iwconfig` erneut aus und suche nach einem Eintrag, der auf `mon` endet — beim typischen Pi `wlan1mon` — mit `Mode:Monitor`. Das bestätigt, dass der Adapter erfolgreich gewechselt hat.

---

### Schritt 6: Paketinjektion testen

```bash
sudo aireplay-ng --test wlan1mon
```

Ersetze `wlan1mon` mit dem Monitor-Interface-Namen, der in Schritt 5 erschienen ist. Ein funktionierender Adapter gibt `Injection is working!` aus. Wenn der Test fehlschlägt, starte neu und versuche es noch einmal. Eine schlechte USB-Verbindung durch einen Hub ohne eigene Stromversorgung ist auf dem Pi die häufigste Ursache — prüfe nochmals, ob du den aktiven Hub verwendest.

---

## USB-Durchleitung für virtuelle Maschinen

Läuft Kali Linux in einer VM auf macOS oder Windows? Du musst den USB-Adapter an das Gast-OS durchreichen.

### VirtualBox

1. Schalte die VM aus und gehe zu **Einstellungen → USB**.
2. Aktiviere **USB 3.0 (xHCI) Controller**.
3. Klicke auf das **+**-Symbol, um einen USB-Filter hinzuzufügen.
4. Wähle: **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Starte die VM — der Adapter erscheint innerhalb von Kali.

Führe in der VM `lsusb` aus, um zu bestätigen, dass `0bda:8812` erscheint, und folge dann den obigen Kali-Linux-Schritten.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Starte die VM.
2. Im Menü: **Virtuelle Maschine → USB & Bluetooth**.
3. Finde **Realtek 802.11ac NIC** und klicke auf **Verbinden**.
4. Der Adapter trennt sich vom Host und erscheint in der VM.

Führe `lsusb` in der VM zur Bestätigung aus und folge dann den obigen Kali-Linux-Schritten.

### Hinweis zu VIF (Virtual Interface)

Der RTL8812AU-Chip im AWUS036ACH hat unter Linux eingeschränkten VIF-Support. Du kannst den Managed-Modus und den Monitor-Modus (oder AP-Modus) nicht zuverlässig gleichzeitig auf demselben Adapter betreiben.

Wenn dein Workflow VIF benötigt — zum Beispiel gleichzeitig Fake-APs betreiben und überwachen — ist der AWUS036ACH das falsche Werkzeug. Schau stattdessen in den [AWUS036ACM Installationsguide](/de/blog/awus036acm-china-install-guide/). Dieser Adapter verwendet den MT7612U-Chip, der vollständigen Kernel-nativen VIF-Support bietet und gleichzeitige virtuelle Interfaces ohne Patches verwaltet.

---

## Fehlerbehebung

| Problem | Mögliche Ursache | Lösung |
|---------|-----------------|--------|
| `lsusb` zeigt 0bda:8812 nicht | Adapter ohne Strom oder schlechtes Kabel | Versuche einen anderen USB-Port. Verwende auf dem Raspberry Pi einen aktiven Hub. |
| `make` schlägt mit Header-Fehlern fehl | Kernel-Header fehlen oder Versions-Mismatch | Führe `sudo apt install linux-headers-$(uname -r)` aus |
| `modprobe 88XXau` schlägt fehl | Secure Boot blockiert unsignierte Module | Deaktiviere Secure Boot im BIOS oder signiere das Modul |
| Treiber verschwindet nach Kernel-Update | Treiber nicht mit DKMS registriert | Führe `sudo dkms install rtl8812au/$(cat VERSION)` aus dem Quellverzeichnis erneut aus |
| `airmon-ng start wlan0` schlägt fehl | NetworkManager läuft noch | Führe zuerst `sudo airmon-ng check kill` aus |
| Monitor-Modus startet, aber erfasst keinen Traffic | Falscher Kanal oder falscher Interface-Name | Prüfe das Interface mit `iwconfig`. Setze den Kanal: `iwconfig wlan0mon channel 6` |
| Injektionstest zeigt "No Answer" | AP zu weit entfernt oder falsches Interface | Näher an den AP heran. Verwende `wlan0mon` nicht `wlan0` |

## China-Mirror-Referenz

Alle in dieser Anleitung verwendeten Ressourcen — kein GitHub erforderlich:

| Ressource | URL | Verwendung |
|-----------|-----|-----------|
| Alfa offizielle Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete, Firmware |
| Alfa-Dokumentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Produkthandbücher |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (empfohlen) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (empfohlen) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM-Images (Backup) |
| RTL8812AU-Treiber (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Manuelles Kompilieren als Fallback |

## Weitere Alfa-Adapter-Anleitungen für China

Dies ist Teil der **Alfa China Install Guide** Serie. Jeder Artikel behandelt ein Adaptermodell:

- AWUS036ACH ← du bist hier
- [AWUS036ACM China-Installationsguide](/de/blog/awus036acm-china-install-guide/) — MT7612U, bester VIF-Support
- [AWUS036ACS China-Installationsguide](/de/blog/awus036acs-china-install-guide/)
- [AWUS036AX China-Installationsguide](/de/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China-Installationsguide](/de/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China-Installationsguide](/de/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China-Installationsguide](/de/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China-Installationsguide](/de/blog/awus036eacs-china-install-guide/)

Fragen? Hinterlasse einen Kommentar unten oder kontaktiere uns über [yupitek.com](https://yupitek.com/de/contact/).
