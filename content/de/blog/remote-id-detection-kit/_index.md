---
title: "ALFA AWUS036ACH × Raspberry Pi: Standard-Remote-ID-Drohnenerkennungs-Kit – Komplettanleitung (2026)"
description: "Baue ein legales passives Remote-ID-Drohnenerkennungs-Kit mit dem ALFA AWUS036ACH und Raspberry Pi. Deckt die ASTM-F3411-Standardanalyse, Hardwareliste, Schritt-für-Schritt-Einrichtung und eine technische Abgrenzung von DJI OcuSync vs. Standard-RID ab."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "Drohnenerkennung", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Warum ist der AWUS036ACH die erste Wahl statt neuerer Wi-Fi-6/6E-Adapter?"
    answer: "Remote-ID-Erfassung benötigt stabilen Monitor Mode und rohe Paketinjektion. Der ausgereifteste Community-Treiber ist derzeit Realtek rtl88xxau (RTL8812AU / RTL8814AU). Wi-Fi-6/6E-Chipsätze (MediaTek MT7921AUN, Realtek RTL8832BU) haben in der gängigen Penetrations-/Sniffing-Toolchain keine Injektionstreiber. Der AWUS036ACH ist doppelt von der Community und diesem Kit verifiziert."
  - question: "Ist der nRF52840 zwingend erforderlich?"
    answer: "Nur für Wi-Fi-Remote-ID (NAN / Beacon) – nein, der AWUS036ACH reicht aus. Um gleichzeitig Bluetooth-5-Long-Range-Broadcasts zu empfangen, brauchst du den nRF52840 (mit Sniffer-Firmware geflasht). Wir empfehlen, dieses Modul für vollständige Abdeckung beizulegen."
  - question: "Kann dieses Kit DJI-Drohnen decodieren?"
    answer: "Es verarbeitet DJIs standardkonforme Wi-Fi-/BT-Remote-ID-Broadcasts. DJIs proprietäres OcuSync-DroneID gehört jedoch nicht zum Standardprotokoll – der ALFA-Adapter kann es nicht decodieren. Dafür brauchst du ein separates SDR (ANTSDR / HackRF) mit einem Kismet-Plugin. Beide können parallel betrieben werden."
  - question: "Welche Raspberry-Pi-Generation soll ich verwenden?"
    answer: "Raspberry Pi 4 (2 GB+) bietet die beste Balance. Der Pi 3B wurde vom unix_rid_capture-Autor in Tests validiert. Pi 5 funktioniert auch (achte auf Kühlung und Stromversorgung). Das integrierte WLAN des Pi kann nicht zuverlässig in den Monitor Mode wechseln – ein externer AWUS036ACH ist erforderlich."
  - question: "Ist passiver Empfang legal?"
    answer: "Der Empfang von öffentlich ausgestrahlten Remote-ID-Informationen von Drohnen ist legal – gleichbedeutend mit dem Lesen öffentlich zugänglicher Informationen. Aktives Stören (Jamming) ist dagegen streng reguliert und nicht Teil dieses Kits."
---
> Yupitek Technik-Team | Offizieller ALFA-Network-Distributor, Taiwan

{{< tldr >}}
Das Remote-ID-Erkennungskit nutzt den Monitor Mode des **ALFA AWUS036ACH**-Adapters, um die Identitäts- und Positionsinformationen passiv zu empfangen, die Drohnen gesetzlich ausstrahlen müssen – stell dir das wie ein „Kennzeichenscanner" für den Luftraum vor. Es gibt Sicherheitsverantwortlichen ein legales, kostengünstiges Werkzeug für die Lageerkennung.
{{< /tldr >}}

---

## 1. Warum du ein Remote-ID-Erkennungskit brauchst

Die Drohnenregulierung weltweit ist in die Ära der „Broadcast-Identität" eingetreten. Standards schreiben vor, dass Drohnen während des Flugs kontinuierlich folgende Informationen ausstrahlen müssen:

| Broadcast-Feld | Beschreibung |
|---|---|
| UAS-/Betreiber-ID | Seriennummer oder Registrierungscode |
| Aktuelle Position (Längengrad, Breitengrad, Höhe) | WGS-84 / barometrische Höhe |
| Geschwindigkeit und Kurs | Horizontale / vertikale Geschwindigkeit |
| Betreiberposition | Startpunkt oder aktueller Standort |

Die Ausstrahlung erfolgt über zwei Arten von Funkträgern:

- **Bluetooth**: BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- **Wi-Fi**: NAN (Wi-Fi Aware, 2,4 / 5 GHz), Beacon (2,4 / 5 GHz)

Für Sicherheitsverantwortliche an Flughäfen, in Industriegebieten, Gefängnissen und bei Großveranstaltungen ist der **passive Empfang dieser öffentlichen Ausstrahlungen** (im Wesentlichen das „Kennzeichen" einer Drohne) eine konforme und kostengünstige Methode zur Lageerkennung – kein aktiver Eingriff erforderlich.

{{< alert "triangle-exclamation" >}}
**Rechtlicher Hinweis**: Alle in diesem Guide beschriebenen Methoden sind **passiver Empfang öffentlich ausgestrahlter Daten**. Aktives Stören (Jamming) ist in allen Rechtsordnungen streng reguliert und weder Teil dieses Kits noch empfehlenswert.
{{< /alert >}}

---

## 2. Produktpositionierung: Der Open-Source-Weg mit dem geringsten Risiko

Nach der Bewertung mehrerer technischer Ansätze haben wir uns für eine Konfiguration mit dem **ALFA AWUS036ACH** als Kern entschieden:

- Der AWUS036ACH verwendet den **Realtek RTL8812AU**-Chipsatz, Dualband 2,4 + 5 GHz (802.11ac), 2×2 MIMO, zwei abnehmbare 5-dBi-Hochgewinn-RP-SMA-Antennen und reichlich USB-3.0-Bandbreite.
- Der von der Community gepflegte Treiber `rtl88xxau` bietet stabilen **Monitor Mode** und **rohe Paketinjektion (raw packet injection)** – die Voraussetzung für den Empfang von Wi-Fi-RID-Beacon-/NAN-Frames.
- Entscheidend: Die README von `sxjack/unix_rid_capture` **gibt explizit an: „Getestet mit einem rtl8812au-basierten WiFi-Dongle, einem nRF52840-Dongle und einem Raspberry Pi 3B"**. Die Community hat die Hardwarevalidierung bereits für uns durchgeführt. Ihre Architektur für ein productisiertes Kit zu reproduzieren, ist der Weg mit dem geringsten Risiko.

---

## 3. Hardwareliste

| Komponente | Modell / Spezifikation | Rolle | Notwendigkeit |
|---|---|---|---|
| **Kernadapter** | ALFA **AWUS036ACH** (RTL8812AU, Dualband 2,4/5 GHz, USB 3.0, zwei 5-dBi-RP-SMA-Antennen) | Wi-Fi-Remote-ID-Erfassung (Monitor Mode) | **Erforderlich** |
| Einplatinencomputer | Raspberry Pi 4 (2 GB+ empfohlen; 3B / 5 ebenfalls kompatibel) | Rechenhost | **Erforderlich** |
| Speicher | microSD 16 GB+ (Samsung / SanDisk Endurance empfohlen) | Systemfestplatte | **Erforderlich** |
| Bluetooth-5-Erfassung | **nRF52840**-USB-Dongle (mit Sniffer-Firmware geflasht, z. B. Nordic Sniffer) | BT5-Long-Range-Remote-ID-Erfassung | Empfohlen (optional) |
| Stromversorgung | 5 V / 3 A USB-C (offizielles Pi-Netzteil) | Spannungsversorgung | **Erforderlich** |
| Netzwerk | Ethernet-Kabel oder WLAN-Zugangsdaten | Upload / Verwaltung | **Erforderlich** |
| Antennen-Upgrade | ALFA **APA-M25** Richtantenne (Panel) | Erweiterte Empfangsreichweite, Unterdrückung von Umgebungsrauschen | Optional |

> Hinweis: Das Community-Projekt `DroneAware` spezifizierte ursprünglich den **AWUS036N (Ralink RT3070, 2,4 GHz Singleband)**. Dieses Kit upgradet auf den **AWUS036ACH (Dualband)**, um sowohl 2,4 GHz als auch 5 GHz **NAN- und Beacon-Wi-Fi-RID-Übertragungsmethoden** abzudecken – breitere Abdeckung und bessere Zukunftssicherheit.

---

## 4. Softwareliste

| Software / Paket | Zweck | Quelle |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | Betriebssystem (headless) | raspberrypi.com |
| **rtl88xxau-Treiber** | RTL8812AU-Monitor-/Injektionstreiber | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | Build-Abhängigkeiten für `unix_rid_capture` | APT |
| **opendroneid-core-c** | Open-Drone-ID-Nachrichten-Codier-/Decodier-C-Bibliothek (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Linux-Wi-Fi-/BT-RID-Erfassungsprogramm (JSON-Ausgabe) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (optional) | Ein-Klick-Community-Echtzeitkarten-Integration | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR-Plugin (DJI-Pfad) | Decodierung von DJI OcuSync DroneID (erfordert SDR-Hardware) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub-Projektlinks

```text
# Kern-Decodierbibliothek (ASTM F3411 / EN 4709-002 Nachrichten-Codierung/Decodierung)
https://github.com/opendroneid/opendroneid-core-c

# Linux-Erfassungsprogramm (Hauptsoftware dieses Kits, getestet mit rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Community-Echtzeitkarten-Netzwerk (Ein-Klick-Installation, automatischer Upload zu droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Drahtloses Erkennungsframework (DJI-OcuSync-Pfad erfordert SDR-Plugin)
https://github.com/kismetwireless/kismet

# RTL8812AU-Monitor-/Injektionstreiber (für AWUS036ACH erforderlich)
https://github.com/morrownr/8812au-20210629
```

---

## 6. Schritt-für-Schritt-Einrichtung

### Schritt 1 — System flashen

Verwende **Raspberry Pi Imager**, um **Raspberry Pi OS Lite (64-bit)** zu schreiben. Klicke auf das Zahnrad (Erweiterte Einstellungen):

- Hostname: `droneid-kit`
- SSH aktivieren und Zugangsdaten festlegen
- WLAN-Zugangsdaten eingeben (spart später das Ethernet-Kabel)

### Schritt 2 — Hardware anschließen und prüfen

Stecke den AWUS036ACH direkt in den **USB-3.0**-Port des Pi (blau / mit `SS` beschriftet). Stelle sicher, dass beide Antennen festgeschraubt sind. Nach dem Booten per SSH einloggen:

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

Du solltest sehen:

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Schritt 3 — rtl88xxau-Monitor-Treiber installieren

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Schritt 4 — Monitor Mode prüfen

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

Die Ausgabe sollte **`Mode:Monitor`** anzeigen.

### Schritt 5 — Build-Abhängigkeiten installieren

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Schritt 6 — opendroneid-core-c bauen

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Erzeugt libopendroneid/libopendroneid.so und test/odidtest
```

### Schritt 7 — unix_rid_capture bauen

`unix_rid_capture` benötigt `opendroneid.c` / `opendroneid.h`. Kopiere sie aus dem vorherigen Schritt:

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Schritt 8 — Erfassung starten

Root-Rechte oder `cap_net_raw` sind erforderlich:

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Erfassen und als JSON speichern
```

Live-UDP-Ausgabe (separates Terminal öffnen):

```bash
nc -lu 32001
```

### Schritt 9 — Flugwege visualisieren (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # .gpx erzeugen
```

Öffne die .gpx-Datei in Google Earth, um den Flugweg der Drohne zu sehen. Ein typischer Erkennungs-JSON-Eintrag sieht so aus:

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Schritt 10 — (Optional) Mit der DroneAware-Community-Echtzeitkarte verbinden

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**Sicherheitshinweis**: Bei jedem Drittanbieter-`curl ... | sudo bash`-Skript empfehlen wir, es zuerst herunterzuladen und zu prüfen: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. Das Installationsprogramm erkennt USB-Adapter automatisch, fragt nach einem Knotennamen und führt dich durch die Registrierung bei droneaware.io. Erkennungen erscheinen in Echtzeit auf der Live-Karte.
{{< /alert >}}

---

## 7. Wichtige technische Abgrenzung: Standard-RID vs. DJI OcuSync

Hier liegt die Fachkompetenz – erkläre deinen Kunden den Unterschied klar:

| Pfad | Zuständig für | Hardware | Funktioniert mit ALFA AWUS036ACH? |
|---|---|---|---|
| **Standard Remote ID** | ASTM F3411 Wi-Fi / BT Broadcast | AWUS036ACH + nRF52840 | ✅ Ja (Hauptthema dieses Artikels) |
| **DJI OcuSync DroneID** | DJI-proprietäres Protokoll (kein Standard-WLAN) | Vollständiges SDR (ANTSDR / HackRF / USRP) + Kismet `kismet_cap_antsdr_droneid`-Plugin | ❌ Nein |

- Der ALFA AWUS036ACH ist ein **WLAN-Band-Empfänger (2,4 / 5 / 6 GHz)**. Er verarbeitet Standard-RID vollständig.
- DJIs proprietäres **OcuSync**-DroneID verwendet keine Standard-WLAN-Protokolle. **Der ALFA-Adapter kann es nicht decodieren**. Du brauchst ein SDR, das 2,4 / 5,8 GHz abdeckt (z. B. ANTSDR E200), mit dem `alphafox02/antsdr_dji_droneid`- + Kismet-Plugin.
- ⚠️ Hinweis: **Standard-RTL-SDR hat eine Bandbreitengrenze von etwa 1,7 GHz** – es kann OcuSync bei 2,4 / 5,8 GHz nicht sehen. Du musst ein SDR wählen, das höhere Frequenzen unterstützt.
- Die beiden Pfade sind **komplementär**: Der ALFA-Adapter übernimmt die Standard-RID-Broadcast-Erkennung, das SDR kümmert sich um DJIs proprietäres Protokoll – zusammen bilden sie ein vollständiges Counter-UAV/RF-Lageerkennungs-Frontend.

---

{{< faq >}}

---

## Anhang: Glossar für Einsteiger

Wenn du neu im Bereich Drohnenregulierung und Counter-UAV-Technologie bist, hier eine kurze Erklärung der in diesem Guide verwendeten Begriffe:

| Begriff | Einfache Erklärung |
|---|---|
| **Remote ID** | Das „digitale Kennzeichen" einer Drohne. Vorschriften verlangen, dass Drohnen während des Flugs kontinuierlich ihre Identität, Position und andere Informationen ausstrahlen, damit Personen am Boden – insbesondere Aufsichtsbehörden – sehen können, „wem diese Drohne gehört und wohin sie fliegt". |
| **ASTM F3411 / EN 4709-002** | Die US-amerikanischen bzw. EU-Standards für Remote-ID-Broadcast-Spezifikationen. Sie legen fest, welche Informationen ausgestrahlt werden müssen und wie sie formatiert sein müssen, um die Interoperabilität zwischen verschiedenen Drohnenmarken und Erkennungsgeräten zu gewährleisten. |
| **Passive Erkennung (Passive Detection)** | Nur „zuhören" bei öffentlich ausgestrahlten Nachrichten. Es werden keine aktiven Signale gesendet, um die Drohne zu stören oder anzugreifen. Rechtlich völlig anders zu bewerten als aktives Stören (Jamming). |
| **Monitor Mode** | Ein Zustand, in dem ein WLAN-Adapter aufhört, sich mit Access Points zu verbinden, und stattdessen „passiv" alle Funkpakete in der Luft mithört – die Voraussetzung für den Empfang von Remote-ID-Broadcasts. |
| **NAN (Wi-Fi Aware) / Beacon** | Zwei WLAN-Frame-Formate, die Drohnen zum Ausstrahlen von Remote-ID verwenden. Dieses Kit versucht, beide zu decodieren. |
| **Bluetooth 5 Long Range** | Neben WLAN senden manche Drohnen Remote-ID auch über Bluetooth aus. Ein zusätzlicher nRF52840-Dongle ist erforderlich, um diese zu empfangen. |
| **DJI OcuSync / DroneID** | DJIs proprietäres Video- und Telemetrie-Übertragungsprotokoll. Es ist **kein** Standard-WLAN und **nicht** Teil des in diesem Artikel behandelten Remote-ID-Protokolls. Es erfordert völlig andere SDR-Hardware und Plugins – siehe Abschnitt 7 für Details. |
| **SDR (Software Defined Radio)** | Ein universeller Funkempfänger, dessen Frequenzbereich und Demodulationsmethoden per Software konfiguriert werden können. Geräte wie ANTSDR und HackRF können Frequenzbänder abdecken, die der ALFA-Adapter nicht erreicht (z. B. DJI OcuSync). |
| **RTL8812AU** | Der Realtek-Chipsatz im ALFA AWUS036ACH. Dieser Chip bestimmt, ob der Adapter den Monitor Mode unterstützt. |
| **GPX-Datei** | Ein Standardformat zum Aufzeichnen von GPS-Koordinaten-Tracks. Du kannst sie direkt in Google Earth und ähnlicher Software öffnen, um den Flugweg einer Drohne zu visualisieren. |

> Zusammengefasst: Dieser Guide zeigt dir, wie du einen ALFA-Adapter in einen „Drohnen-Identitätsscanner" verwandelst – passiver Empfang der öffentlichen Informationen, die Drohnen gesetzlich ausstrahlen müssen. Eine legale Methode für die Sicherheit von Liegenschaften.

---

## Referenzen

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture (rtl8812au + nRF52840 + RPi getestet)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Community-Remote-ID-Erkennungsnetzwerk](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Drahtloses Erkennungsframework](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR-Decoder](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux Monitor-/Injektionstreiber](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH Produktseite (Yupitek)](https://yupitek.com/de/products/alfa/awus036ach/)
8. [Kontakt und Bestellung (Yupitek)](https://www.yupitek.com/de/contact/)

---

*Dieser Artikel wurde vom Yupitek-Technikerteam zusammengestellt. AWUS036ACH und verwandte Hardware sind über Yupitek mit autorisiertem Vertrieb und technischem Support erhältlich.*
