---
title: "ALFA AWUS036ACM Treiber-Installationsanleitung für China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
description: "Schritt-für-Schritt-Anleitung zur Installation von ALFA AWUS036ACM-Treibern in China mit inländischen Spiegeln. MT7612U In-Kernel-Treiber, vollständige VIF-Unterstützung. Für Kali Linux, Ubuntu 22/24, Debian und Raspberry Pi. GitHub nicht erforderlich."
related_product: "/de/products/alfa/awus036acm/"
featureimage: "/images/blog/awus036acm-china-install-guide.webp"
faq:
  - question: "Welchen Chipsatz verwendet der AWUS036ACM? Muss ein Treiber installiert werden?"
    answer: "Er verwendet den MediaTek MT7612U-Chipsatz. Der Treiber mt76x2u ist seit Linux Kernel 4.19 im Kernel integriert, sodass er in den meisten Fällen Plug-and-Play funktioniert."
  - question: "Unterstützt der AWUS036ACM VIF-Virtual-Interfaces?"
    answer: "Ja, der MT7612U unterstützt das native VIF des Kernels vollständig. Es können gleichzeitig ein Monitor-Interface und ein Management-Modus ausgeführt werden, ohne dass Patches erforderlich sind."
  - question: "Muss man in China die Great Firewall umgehen, um den AWUS036ACM zu installieren?"
    answer: "Nein, da der Treiber bereits im Kernel integriert ist, muss lediglich das Firmware-Paket firmware-misc-nonfree von einem lokalen Spiegelserver installiert werden."
  - question: "Wie hoch ist der Stromverbrauch des AWUS036ACM auf einem Raspberry Pi?"
    answer: "Unter Volllast beträgt der Verbrauch etwa 400mW. Es wird empfohlen, ein USB Hub mit separater Stromversorgung zu verwenden, um eine Drosselung durch den Raspberry Pi zu vermeiden."
  - question: "Warum wird die Netzwerkkarte des AWUS036ACM unter Debian erkannt, funktioniert aber nicht?"
    answer: "Das Firmware-Paket firmware-misc-nonfree fehlt. Nach der Installation kann die Netzwerkkarte normal initialisiert werden."
---

Der AWUS036ACM ist einer der einfachsten Alfa-Adapter für die Einrichtung unter Linux. Sein MT7612U-Chip verwendet den `mt76x2u`-Treiber, der seit Kernel-Version 4.19 im Linux-Kernel integriert ist. Auf den meisten modernen Systemen funktioniert der Adapter mit zwei oder drei Befehlen. Diese Anleitung behandelt die vollständige Einrichtung — Treiberprüfung, Monitor-Modus, Paketeinspeisung und VIF — ausschließlich mit inländischen Spiegeln. GitHub ist nicht erforderlich.

{{< tldr >}}
Der AWUS036ACM ist mit dem MT7612U-Chipsatz ausgestattet, dessen Treiber bereits im Kernel integriert ist und keine Kompilierung erfordert. Er unterstützt Monitor Mode, Packet Injection und gleichzeitige VIF-Operationen. In China muss lediglich das Firmware-Paket installiert werden.
{{< /tldr >}}

Stelle sicher, dass du Folgendes bereit hast:


## Vorbereitung

Stelle sicher, dass du Folgendes bereit hast:

1. **ALFA AWUS036ACM** Adapter
2. USB-Kabel (das mitgelieferte funktioniert)
3. Einen USB-Hub mit externer Stromversorgung — bei Raspberry Pi erforderlich
4. Aktive Internetverbindung für inländische Spiegel

Stecke den Adapter ein und prüfe, ob das System ihn erkennt:

```bash
lsusb
```

Suche in der Ausgabe nach:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

Wenn `0e8d:7612` angezeigt wird, ist der Adapter erkannt. Gehe zum passenden OS-Abschnitt unten.

Wenn er nicht erscheint, probiere einen anderen USB-Port oder tausche das Kabel aus, dann führe `lsusb` erneut aus.

## Betriebssystem wählen

Springe zum richtigen Abschnitt für dein OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Bereits installiert? Direkt zu:

- [Monitor-Modus aktivieren](#enable-monitor-mode)
- [Paketeinspeisung testen](#test-packet-injection)
- [Virtuelles Interface (VIF)](#virtual-interface-vif)
- [VM USB-Durchleitung](#virtual-machine-usb-passthrough)

---

## Kali Linux

Der MT7612U-Treiber ist bereits im Kali-Kernel enthalten. In den meisten Fällen funktioniert der Adapter sofort nach dem Einstecken. Die folgenden Schritte prüfen, ob der Treiber geladen ist, und führen durch den Monitor-Modus.

### Schritt 1: Auf China-Spiegel umstellen

Öffne die Quellenliste im Terminal.

```bash
sudo nano /etc/apt/sources.list
```

Lösche den gesamten Inhalt und füge diese Zeile ein:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern: **Ctrl+O** drücken, dann Enter, dann Ctrl+X zum Beenden. Den Paketindex aktualisieren.

```bash
sudo apt update
```

> **Backup-Spiegel:** Wenn 中科大 (USTC) langsam ist, verwende stattdessen 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Schritt 2: Treiber prüfen

Prüfe, ob das Modul beim Einstecken automatisch geladen wurde.

```bash
lsmod | grep mt76
```

Die Ausgabe sollte `mt76x2u` enthalten. Wenn nichts erscheint, lade es manuell.

```bash
sudo modprobe mt76x2u
```

Führe `lsmod | grep mt76` erneut aus zur Bestätigung. Dann prüfe, ob der Adapter aktiv ist.

```bash
iwconfig
```

Suche nach einem WLAN-Interface — typischerweise `wlan0` oder `wlan1`. Wenn das Interface mit einer ESSID oder `unassociated` erscheint, funktioniert der Treiber.

---

### Schritt 2 (Alternative): Extra-Kernelmodule installieren

Wenn `modprobe mt76x2u` einen Fehler „Module not found" liefert, fehlen dem Kernel-Build möglicherweise die MT76-Module. Installiere sie vom China-Spiegel.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

Nach Abschluss der Installation das Modul erneut laden.

```bash
sudo modprobe mt76x2u
```

Wenn das Paket für deine genaue Kernel-Version nicht verfügbar ist, kompiliere den Treiber aus dem Quellcode.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **HINWEIS:** Wenn diese Gitee-URL nicht lädt, suche auf Gitee nach `mt76` und wähle den zuletzt aktualisierten Fork. Du kannst Treiberarchive auch direkt von [files.alfa.com.tw](https://files.alfa.com.tw) herunterladen.

---

### Schritt 3: Monitor-Modus aktivieren {#enable-monitor-mode}

Prüfe vor dem Wechsel in den Monitor-Modus, welchen Interface-Namen das System dem Adapter zugewiesen hat.

```bash
iwconfig
```

Suche nach `wlan0` oder `wlan1`. Verwende diesen Namen in den folgenden Befehlen.

Stoppe NetworkManager und wpa_supplicant, damit sie nicht stören.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Bestätige den Wechsel.

```bash
iwconfig
```

Suche nach einem Eintrag wie `wlan0mon` mit `Mode:Monitor`. Wenn dieser angezeigt wird, ist der Adapter für die Paketerfassung bereit.

---

### Schritt 4: Paketeinspeisung testen {#test-packet-injection}

Führe den Einspeisungstest gegen das Monitor-Interface aus.

```bash
sudo aireplay-ng --test wlan0mon
```

Ein erfolgreiches Ergebnis sieht so aus:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Wenn der Test fehlschlägt, starte neu und führe ihn erneut aus. Wenn er immer noch fehlschlägt, prüfe mit `iwconfig`, ob kein anderer Prozess das Interface belegt.

---

## Ubuntu 22.04 / 24.04

Der MT7612U-Treiber ist auch im Ubuntu-Kernel enthalten, kann jedoch im `linux-modules-extra`-Paket statt im Basis-Kernel-Image enthalten sein. Die folgenden Schritte behandeln beide Fälle.

### Schritt 1: Auf China-Spiegel umstellen

#### Ubuntu 24.04 (Noble)

Die DEB822-Quelldatei öffnen:

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

Mit `Ctrl+O` speichern, dann mit `Ctrl+X` beenden.

#### Ubuntu 22.04 (Jammy)

Die klassische Quelldatei öffnen:

```bash
sudo nano /etc/apt/sources.list
```

Alle Zeilen ersetzen mit:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Speichern und beenden (`Ctrl+O`, dann `Ctrl+X`).

#### Paketindex aktualisieren

```bash
sudo apt update
```

---

### Schritt 2: Treiber laden

Versuche zunächst, das Modul direkt zu laden.

```bash
sudo modprobe mt76x2u
```

Wenn der Fehler „Module not found" erscheint, installiere das Extra-Module-Paket.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Prüfe, ob der Adapter sichtbar ist.

```bash
iwconfig
```

Ein Interface wie `wlan0` oder `wlan1` in der Ausgabe bestätigt, dass der Treiber aktiv ist.

---

### Schritt 3: WLAN-Tools installieren

Installiere aircrack-ng für Monitor-Modus und Einspeisungstest.

```bash
sudo apt install -y aircrack-ng
```

---

### Schritt 4: Monitor-Modus aktivieren

Störende Prozesse beenden, dann Monitor-Modus starten.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Hinweis:** Dein Interface kann `wlan1` sein, wenn eine weitere WLAN-Karte vorhanden ist. Führe zuerst `iwconfig` aus zur Überprüfung.

---

### Schritt 5: Paketeinspeisung testen

```bash
sudo aireplay-ng --test wlan0mon
```

Ein erfolgreiches Ergebnis zeigt `Injection is working!`. Bei Interface-Fehlern prüfe mit `iwconfig wlan0mon`, ob der Monitor-Modus aktiv ist.

---

## Debian

Der MT7612U-Treiber ist im Debian-Kernel enthalten, erfordert aber manchmal das Paket `firmware-misc-nonfree` zur vollständigen Initialisierung.

### Schritt 1: Auf China-Spiegel umstellen

Die Quellenliste öffnen:

```bash
sudo nano /etc/apt/sources.list
```

Alles löschen und diese drei Zeilen einfügen (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Mit `Ctrl+O` speichern, dann mit `Ctrl+X` beenden. Aktualisieren:

```bash
sudo apt update
```

### Schritt 2: Non-Free-Firmware installieren

Der MT7612U benötigt Firmware-Dateien aus dem Paket `firmware-misc-nonfree`. Ohne dieses Paket wird der Adapter initialisiert, kann sich aber möglicherweise nicht verbinden oder in den Monitor-Modus wechseln.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Schritt 3: Treiber laden

```bash
sudo modprobe mt76x2u
```

Wenn das Modul fehlt, installiere zuerst die Extra-Kernelmodule.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Prüfe, ob das Interface erschienen ist.

```bash
iwconfig
```

### Schritt 4: Monitor-Modus aktivieren

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Bestätige den Monitor-Modus mit `iwconfig` — suche nach `wlan0mon` mit `Mode:Monitor`.

### Schritt 5: Paketeinspeisung testen

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` bestätigt, dass der Adapter voll funktionsfähig ist.

---

## Raspberry Pi 4B / 5

> Der AWUS036ACM zieht unter Last etwa 400mW. Verwende einen USB-Hub mit externer Stromversorgung, um Drosselung des Pi zu verhindern.

---

### Schritt 1: Kali Linux ARM64-Image herunterladen

Gehe zur offiziellen Kali ARM-Download-Seite:
https://www.kali.org/get-kali/#kali-arm

Wähle **Raspberry Pi 4 (64-bit)** oder **Raspberry Pi 5 (64-bit)**. Verwende nicht das 32-Bit-Image — 64-Bit ist erforderlich.

> **China-Spiegel:** Wenn kali.org langsam ist, verwende 华为云:
> https://repo.huaweicloud.com/kali-images/
> Navigiere zum neuesten Release-Ordner und lade dort das ARM64-Image herunter.

---

### Schritt 2: Auf MicroSD flashen

Prüfe zuerst den Gerätepfad deiner Karte.

```bash
lsblk
```

Dann flashen, wobei `/dev/sdX` durch deinen tatsächlichen Kartenpfad ersetzt wird.

```bash
# /dev/sdX durch deine tatsächliche SD-Karte ersetzen (mit lsblk prüfen)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Warte, bis `sync` abgeschlossen ist, dann starte. Standardanmeldedaten: **kali / kali**.

---

### Schritt 3: Auf China-Spiegel umstellen

```bash
sudo nano /etc/apt/sources.list
```

Inhalt ersetzen mit:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Speichern und anwenden.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Schritt 4: Treiber prüfen

Nach dem Neustart den Adapter einstecken und prüfen.

```bash
lsmod | grep mt76
```

Wenn `mt76x2u` erscheint, bist du fertig. Falls nicht:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Schritt 5: Monitor-Modus aktivieren

Auf einem Pi mit eingebautem WLAN erscheint der AWUS036ACM als `wlan1` — das eingebaute Radio belegt `wlan0`.

```bash
iwconfig
```

Notiere den Interface-Namen, dann starte den Monitor-Modus darauf.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Bestätige mit `iwconfig` — suche nach `wlan1mon` mit `Mode:Monitor`.

---

### Schritt 6: Paketeinspeisung testen

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` bestätigt den vollständigen Betrieb. Wenn es fehlschlägt, prüfe, ob du einen Hub mit externer Stromversorgung verwendest.

---

## Virtuelle Maschine USB-Durchleitung

### VirtualBox

1. VM ausschalten. Gehe zu **Einstellungen → USB**.
2. **USB 3.0 (xHCI) Controller** aktivieren.
3. Klicke auf **+**, um einen USB-Filter hinzuzufügen.
4. Wähle: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. VM starten — der Adapter erscheint in Kali.

Führe `lsusb` in der VM aus, um `0e8d:7612` zu bestätigen, dann folge den Kali-Schritten oben.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VM starten.
2. Menü: **Virtuelle Maschine → USB & Bluetooth**.
3. **MediaTek MT7612U** finden und **Verbinden** klicken.
4. `lsusb` in der VM ausführen zur Bestätigung, dann den Kali-Schritten oben folgen.

---

## Virtuelles Interface (VIF)

Hier übertrifft der AWUS036ACM den ACH. Der MT7612U-Chip hat vollständige kernel-native VIF-Unterstützung. Du kannst ein Monitor-Interface und ein Managed- oder AP-Interface gleichzeitig auf demselben Adapter betreiben — ohne Patches, ohne Hacks.

### Ein zweites virtuelles Interface erstellen

Wenn der Adapter im Managed-Modus als `wlan0` läuft, füge ein Monitor-Interface daneben hinzu.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Prüfe, ob beide Interfaces aktiv sind.

```bash
iwconfig
```

Du solltest sowohl `wlan0` (verbunden, Managed-Modus) als auch `mon0` (Monitor-Modus) sehen. Der Adapter macht beides gleichzeitig.

### Anwendungsfall: Monitoren bei gleichzeitiger Verbindung

Das ermöglicht das Erfassen von Datenverkehr auf `mon0`, während `wlan0` mit einem Netzwerk verbunden bleibt — nützlich für korrelierte Analysen.

```bash
sudo airodump-ng mon0
```

`wlan0` behält seine normale Verbindung bei, während `mon0` alles in Reichweite erfasst.

### Anwendungsfall: Fake-AP + Monitor

Ein AP-Interface und ein Monitor-Interface zusammen erstellen.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Führe `iwconfig` aus, um zu bestätigen, dass alle drei Interfaces (`wlan0`, `ap0`, `mon0`) aktiv sind.

> **Hinweis zu hostapd:** Für den vollständigen AP-Betrieb muss `hostapd` konfiguriert werden. Das liegt außerhalb des Rahmens dieser Anleitung. Die obigen Schritte bestätigen, dass der Adapter das Interface erstellen kann — die eigentliche AP-Konfiguration ist ein separates Thema.

---

## Fehlerbehebung

| Problem | Wahrscheinliche Ursache | Lösung |
|---------|------------------------|--------|
| `lsusb` zeigt 0e8d:7612 nicht an | Adapter nicht mit Strom versorgt oder schlechtes Kabel | Anderen USB-Port ausprobieren. Hub mit Stromversorgung am Raspberry Pi verwenden. |
| `modprobe mt76x2u` sagt „Module not found" | Kernel fehlen Extra-Module | `sudo apt install linux-modules-extra-$(uname -r)` ausführen |
| Interface erscheint, kann sich aber nicht verbinden | Firmware-Datei fehlt | `sudo apt install firmware-misc-nonfree` ausführen (Debian) |
| `airmon-ng start wlan0` schlägt fehl | NetworkManager läuft noch | Zuerst `sudo airmon-ng check kill` ausführen |
| Monitor-Modus startet, aber kein Datenverkehr erfasst | Falscher Kanal oder falscher Interface-Name | Kanal setzen: `iwconfig wlan0mon channel 6` |
| Einspeisungstest zeigt „No Answer" | AP zu weit oder falsches Interface | Näher an den AP herangehen. `wlan0mon` verwenden, nicht `wlan0`. |
| VIF-Interface-Erstellung schlägt fehl | Treiber nicht vollständig geladen | Adapter abziehen, Modul neu laden: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## China-Spiegel Referenz

Alle in dieser Anleitung verwendeten Ressourcen — kein GitHub erforderlich:

| Ressource | URL | Verwendung |
|-----------|-----|-----------|
| Alfa offizielle Treiber | [files.alfa.com.tw](https://files.alfa.com.tw) | Treiberpakete, Firmware |
| Alfa Dokumentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Produkthandbücher |
| 清华大学 Spiegel | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云 Spiegel | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (empfohlen) |
| 中科大 Spiegel | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (empfohlen) |
| 华为云 Spiegel | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM-Images (Backup) |
| MT76-Treiber (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Manuelles Kompilieren als Fallback |

---

{{< faq >}}

## Weitere Alfa-Adapter-Anleitungen für China

Dies ist Teil der **Alfa China Install Guide**-Reihe. Jeder Artikel behandelt ein Adaptermodell:

- [AWUS036ACH China-Installationsanleitung](/de/blog/awus036ach-china-install-guide/) — RTL8812AU, hohe Leistung
- AWUS036ACM ← du bist hier
- [AWUS036ACS China-Installationsanleitung](/de/blog/awus036acs-china-install-guide/)
- [AWUS036AX China-Installationsanleitung](/de/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China-Installationsanleitung](/de/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China-Installationsanleitung](/de/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China-Installationsanleitung](/de/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China-Installationsanleitung](/de/blog/awus036eacs-china-install-guide/)

Fragen? Hinterlasse einen Kommentar oder kontaktiere uns unter [yupitek.com/de/contact/](https://yupitek.com/de/contact/)

## Referenzen

1. [Linux Kernel mt76 Treiber](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng Offizielle Dokumentation](https://www.aircrack-ng.org/)
3. [ALFA Network Offizielle Website](https://www.alfa.com.tw/)
4. [Kali Linux Offizielle Dokumentation](https://www.kali.org/docs/)
5. [Debian firmware-misc-nonfree Paket](https://packages.debian.org/bookworm/firmware-misc-nonfree)
