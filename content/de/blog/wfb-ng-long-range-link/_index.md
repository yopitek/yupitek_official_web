---
title: "DIY Langstrecken-Digital-FPV- und Telemetrie-Link mit ALFA AWUS036ACH und wfb-ng (2026)"
description: "Baue mit dem ALFA AWUS036ACH WLAN-Adapter und der Open-Source-Software wfb-ng einen latenzarmen, verschlüsselten digitalen Langstrecken-Video- und MAVLink-Telemetrie-Link. Komplette Hardwareliste, Raspberry-Pi-Setup-Anleitung und Tipps zur Stromversorgung."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "Drohnen-Video-Link", "digital-FPV", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "Langstrecken-Video", "Telemetrie-Link"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Was ist der Unterschied zwischen wfb-ng und normalem WLAN?"
    answer: "Normales WLAN braucht Verbindungsaufbau und ACK-Bestätigungen, was auf große Distanzen ineffizient und zu langsam ist. wfb-ng umgeht den 802.11-Overhead durch raw packet injection und nutzt FEC zur Fehlerkorrektur – die Ende-zu-Ende-Latenz liegt im Bereich weniger Dutzend Millisekunden."
  - question: "Warum braucht der ALFA-Adapter an der Drohne eine eigene Stromversorgung?"
    answer: "Der AWUS036ACH zieht beim Senden (TX) kurzzeitig sehr viel Strom. Direkt am USB-2.0-Port eines Raspberry Pi führt das zu Spannungseinbrüchen – der Adapter wird zurückgesetzt, die Verbindung bricht ab oder Pakete werden korrumpiert. Verwende ein separates 5V-BEC und schalte einen 470µF-niedrig-ESR-Kondensator zwischen +5V und GND."
  - question: "Ich habe eine Verbindung, aber kein Bild und keine Telemetrie – was tun?"
    answer: "Der häufigste Grund ist ein Schlüsselkonflikt – prüfe, ob drone.key auf der Drohne und gs.key auf der Bodenstation zusammengehören. Stelle außerdem sicher, dass wifi_channel und link_domain auf beiden Seiten identisch sind. Mit journalctl -xu wifibroadcast@gs siehst du die Echtzeit-Logs."
  - question: "Muss ich zwingend den ALFA AWUS036ACH für wfb-ng verwenden?"
    answer: "Theoretisch funktioniert jeder RTL8812AU-Adapter. Der AWUS036ACH ist aber die vom wfb-ng-Projekt offiziell getestete Hardware mit dem stabilsten Treibersupport. Gerade für hohe Sendeleistung und große Reichweiten spielen ALFAs Power-Design und die abnehmbaren Antennen ihre Stärken aus."
---
> Autor: Yupitek Technik-Team (offizieller ALFA-Network-Distributor, Taiwan)
> Zielgruppe: Drohnen-Enthusiasten, Maker, Sicherheitsforscher, Entwickler von Agrar- und Inspektionsdrohnen
> Schwierigkeit: ★★★☆☆ (grundlegende Linux- und Flugcontroller-Kenntnisse erforderlich)

{{< tldr >}}
wfb-ng ist eine Open-Source-Software, die WLAN-Adapter mit Monitor-Mode-Unterstützung – wie den **ALFA AWUS036ACH** – in spezialisierte Langstrecken-Funkmodule für Drohnen verwandelt. Du kannst damit einen latenzarmen, verschlüsselten Video- und MAVLink-Telemetrie-Link aus handelsüblichen Komponenten aufbauen.
{{< /tldr >}}

---

## 1. Warum einen digitalen FPV-Link mit einer ALFA-Karte bauen?

Wenn du analoges FPV (5,8-GHz-Analog-Video) kennst, weißt du, wie es läuft: Sobald ein Hindernis das Signal blockiert, rauscht das Bild, die Reichweite bricht ein, und **jeder mit einem Empfänger kann dein Bild sehen** – keine Verschlüsselung, kein Telemetrie-Rückkanal.

Unser Team hat im letzten Jahr Links für Agrar-Sprühbetreiber, Inspektionsteams und Security-Training-Kunden aufgebaut. Eine Frage kam immer wieder: **Kann ich einen handelsüblichen ALFA-USB-Adapter mit Open-Source-Software nutzen, um einen digitalen, verschlüsselten Langstrecken-Link für Video und Telemetrie zu bauen?**

Die Antwort ist ja – und es ist einfacher, als du denkst.

Im Vergleich zu analogen FPV-Systemen bietet wfb-ng auf einem ALFA-Adapter entscheidende Vorteile:

- **Niedrige Latenz**: Raw-WLAN-Injection umgeht 802.11-ACK und Handshake-Overhead. Die Ende-zu-Ende-Latenz liegt im zweistelligen Millisekundenbereich – das FPV-Gefühl kommt nah an analog heran.
- **Digitale Verschlüsselung**: Video- und Telemetrie-Pakete werden mit libsodium verschlüsselt. Selbst wenn jemand das Signal aufzeichnet, kann er dein Bild oder die Flugdaten nicht entschlüsseln.
- **Ein Link, mehrere Streams**: Ein einziger Adapter auf einer Frequenz überträgt:
  - Live-Video (RTP / RTSP)
  - MAVLink-Telemetrie (bidirektional, Flugcontroller ↔ Bodenstation)
  - Einen TCP/IP-Tunnel (für VPN, SSH oder Dateitransfer)
- **TX-Diversity**: Mehrere Adapter können für Sendediversity kombiniert werden, was die Störfestigkeit verbessert.
- **Open Source, vollständig anpassbar**: Der ALFA AWUS036ACH zusammen mit wfb-ng kostet nur einen Bruchteil kommerzieller Digital-FPV-Systeme (DJI O3, Walksnail usw.) – und jeder Code ist offen.

{{< alert "circle-info" >}}
Dieser Guide soll kein DJI-System ersetzen. Er zeigt einen praktischen Open-Source-Weg für alle, die **ihren eigenen Link in der Hand haben, eine sekundäre Redundanz aufbauen oder kundenspezifische Nutzlasten realisieren wollen**.
{{< /alert >}}

---

## 2. Was das ist: wfb-ng erklärt

**wfb-ng** (Wireless Fibre / WiFi Broadcast – next generation) ist ein Open-Source-Projekt für digitales FPV und Telemetrie mit einer cleveren Grundidee:

> Es nutzt WLAN nicht als „Netzwerk", sondern als „Funk".

Normales 802.11 wurde für lokale Netzwerke entwickelt – Verbindungsaufbau, ACK, Neuübertragung. Über große Entfernungen, mit bewegten Fahrzeugen und schwachen Signalen wird dieser Overhead zum Problem. wfb-ng geht einen anderen Weg mit **raw WiFi injection**:

- Der Adapter wechselt in den **Monitor Mode** – er „verbindet" sich mit niemandem.
- Er injiziert direkt rohe WLAN-Frames. **Kein ACK, keine Neuübertragung** (FEC Forward Error Correction gleicht Paketverluste aus).
- Das umgeht die Reichweiten- und Latenzgrenzen von Standard-802.11 und treibt Distanz und Stabilität an das physische Limit der Hardware.

Einfach gesagt: Ein handelsüblicher USB-Adapter wird zu einem Paar „Digitalfunkgeräte", die RTP-Video, MAVLink-Telemetrie und sogar einen IP-Tunnel übertragen können.

- Projektseite (GitHub): https://github.com/svpcom/wfb-ng.git
- Weit verbreitet im PX4-/ArduPilot-Ökosystem für DIY-Digital-FPV. Aktive Community, auch in der ukrainischen Drohnen-Community im Einsatz.

---

## 3. Der Hauptdarsteller: ALFA AWUS036ACH

Das „Funkgerät" dieses Links ist der **ALFA AWUS036ACH**.

Er verwendet den **Realtek RTL8812AU**-Chipsatz mit **802.11ac (WiFi 5)**, **Dualband 2,4 GHz / 5 GHz**, USB 3.0 Type-C und abnehmbaren RP-SMA-Antennen. Entscheidend: **Die offizielle wfb-ng-Testhardware verwendet AWUS036ACH auf beiden Enden im 5-GHz-Modus**. Dieser Adapter wurde vom Projektautor für den stabilsten Treibersupport validiert.

Drei Gründe für diese Wahl:

1. **Genug Leistung**: ALFAs charakteristisches High-Power-Design zusammen mit externen Hochgewinnantennen liefert eine weit bessere Langstrecken-Performance als jede interne Laptop-Karte.
2. **Monitor Mode + Injection**: Mit dem gepatchten Treiber (siehe unten) unterstützt der RTL8812AU zuverlässig Monitor Mode und raw packet injection – die Grundvoraussetzung für wfb-ng.
3. **Universell und robust**: Das USB-Format funktioniert sowohl an der Drohne als auch an der Bodenstation. Keine verschiedenen Adapter für verschiedene Geräte. Fällt einer aus, wird er einfach getauscht.

{{< alert "triangle-exclamation" >}}
**Hinweis**: wfb-ng benötigt einen **gepatchten Treiber** (z. B. `rtl88xxau_wfb`). Der Standard-Linux-Kernel-Treiber kann den von wfb-ng benötigten Injection-Modus nicht aktivieren. Die Installationsanleitung findest du in den Abschnitten „Softwareliste" und „Step-by-Step".
{{< /alert >}}

---

## 4. Hardwareliste

Der Link besteht aus **Drohne (Luftfahrzeug)** und **Bodenstation**.

### Drohne (Luftfahrzeug)

| Komponente | Empfohlenes Modell / Hinweise |
|---|---|
| Bordcomputer | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (für 1080p empfehlen wir **Pi 4 oder Zero 2 W**) |
| Kamera | Raspberry Pi Camera (CSI) oder Logitech C920 (USB) |
| WLAN-Adapter | **ALFA AWUS036ACH** (oder ein beliebiger RTL8812AU-Adapter) |
| Spannungsversorgung | **5V BEC** (separate Stromversorgung für den Adapter – siehe Fehlerhinweis) |
| Filterkondensator | **470µF Low-ESR-Kondensator** (zwischen Adapter +5V und GND) |
| Flugcontroller | Pixhawk oder vergleichbar (MAVLink über UART an den Bordcomputer) |

### Bodenstation

| Komponente | Empfohlenes Modell / Hinweise |
|---|---|
| Computer | Linux-Rechner (Ubuntu / Debian x86-64) oder ein weiterer Raspberry Pi |
| WLAN-Adapter | **ALFA AWUS036ACH** |
| Überwachungssoftware | Rechner mit **QGroundControl** (kann derselbe wie der Bodenstations-Computer sein) |

> Hinweis: Für **reine Empfänger-Setups (RX)** reicht jeder Adapter mit Monitor-Mode-Support – sogar ein Router mit OpenWRT. Die offiziell getestete Konfiguration und dieser Guide verwenden jedoch den AWUS036ACH.

---

## 5. Softwareliste

### Betriebssystem

- **Raspberry Pi OS** / **Debian** / **Ubuntu** (Linux-Kernel ≥ 4.x)

### Kernprojekte

- **wfb-ng** (svpcom/wfb-ng): Digitales FPV / Telemetrie-Hauptprogramm
- **Gepatchter Treiber**:
  - RTL8812AU → `svpcom/rtl8812au` (Branch **v5.2.20**, Installation via dkms)
  - RTL8812EU → `svpcom/rtl8812eu`
  - Nach dem Laden erscheint der Adapter als `rtl88xxau_wfb` (bzw. `rtl8812eu`)

### Systemabhängigkeiten

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### Verschlüsselung

- **libsodium**: Mit `wfb_keygen` erzeugst du `drone.key` (Drohne) und `gs.key` (Bodenstation)

### Wiedergabe auf der Bodenstation

- **QGroundControl**: Überwachung des Flugcontroller-Status und der Telemetrie
- **GStreamer / RTSP**: Empfang und Wiedergabe des Live-Videos von der Drohne

---

## 6. GitHub-Links und ALFA AWUS036ACH-Datenblatt

### Offizielle Links

| Element | Link |
|---|---|
| wfb-ng-Projekt | https://github.com/svpcom/wfb-ng.git |
| Gepatchter Treiber (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| Gepatchter Treiber (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH-Produktseite | https://yupitek.com/de/products/alfa/awus036ach/ |
| PX4 WFB-ng Tutorial | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH-Datenblatt

| Spezifikation | Detail |
|---|---|
| Chipsatz | Realtek **RTL8812AU** |
| WLAN-Standard | 802.11a / b / g / n / **ac (WiFi 5)** |
| Frequenz | **2,4 GHz + 5 GHz** Dualband |
| Schnittstelle | USB 3.0 **Type-C** |
| Antenne | 2 × abnehmbar **RP-SMA** (2T2R MIMO) |
| Monitor Mode | Unterstützt Monitor Mode + Packet Injection (erfordert wfb-ng-gepatchten Treiber) |
| wfb-ng-Treiber | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| Status | wfb-ng **offiziell getesteter Adapter** (5 GHz auf beiden Seiten) |

---

## 7. Schritt-für-Schritt-Einrichtung

Dieser Abschnitt hat vier Teile. **Pfad A (Raspberry Pi Quick Start)** ist die empfohlene Methode – nahezu „brennen und loslegen". **Pfad B** ist für die manuelle Installation auf x86-Linux-Bodenstationen. **Pfad C und D** behandeln Schlüsselpaarung und Konfiguration; beide Pfade nutzen diese.

### A. Raspberry Pi Quick Start (Empfohlen)

wfb-ng bietet vorgefertigte Raspberry-Pi-Images. Brenne eines für die Drohne und eines für die Bodenstation – nach dem Booten läuft alles.

**1. Image herunterladen und brennen**

Gehe auf der wfb-ng GitHub-**Releases**-Seite, lade das aktuellste `*.img.gz` herunter, entpacke es und brenne es auf **zwei** SD-Karten (eine für die Drohne, eine für die Bodenstation).

```bash
# Image entpacken (Dateiname je nach Release)
gunzip wfb-ng-*.img.gz
# Mit Raspberry Pi Imager, dd oder balenaEtcher auf SD-Karte brennen
```

**2. Adapter einstecken, booten, per SSH einloggen**

Stecke einen ALFA AWUS036ACH in beide Boards, schalte sie ein und verbinde dich per SSH (Standard-IP und -Zugangsdaten unten):

```bash
ssh pi@192.168.0.111
# Passwort: raspberry
```

**3. Bodenstation-Dienste aktivieren**

Führe auf dem **Bodenstation-Pi** aus:

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. Drohnen-Dienste aktivieren**

Führe auf dem **Drohnen-Pi** aus:

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. Link-Status auf der Bodenstation überwachen**

```bash
wfb-cli gs
```

> Wenn du Verbindungs-, Kanal- und Paketverlust-Informationen siehst, ist der Link aktiv. Öffne QGroundControl, um Telemetrie und Video zu nutzen.

---

### B. Manuelle Installation der Debian-/Ubuntu-Bodenstation

Wenn du einen x86-64-Linux-Desktop oder ein Laptop als Bodenstation verwendest, installiere manuell.

**1. dkms und den gepatchten Treiber installieren**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. Prüfen, ob der Adapter den wfb-ng-Treiber verwendet**

```bash
# Sollte wlan0 mit MTU 2312 anzeigen
ifconfig

# Der Treibername sollte rtl88xxau_wfb (RTL8812AU) oder rtl8812eu (RTL8812EU) sein
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
Wenn `ethtool -i wlan0` nur `rtl8812au` statt `rtl88xxau_wfb` anzeigt, wurde der gepatchte Treiber nicht korrekt installiert, und wfb-ng kann nicht in den Injection-Modus wechseln. Überprüfe die dkms-Installation auf Fehler.
{{< /alert >}}

**3. Offizielles Auto-Installations-Skript ausführen**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. Link überwachen**

```bash
wfb-cli gs
```

---

### C. Schlüsselpaarung

wfb-ng-Video und -Telemetrie sind verschlüsselt. Drohne und Bodenstation müssen **zusammengehörige Schlüssel** verwenden.

```bash
# Schlüssel erzeugen (auf der Drohnenseite, dann verteilen)
wfb_keygen

# drone.key auf die Drohne legen
# gs.key auf die Bodenstation legen
# Beide müssen zusammengehören – sonst zeigt der Link „verbunden" aber keine Daten
```

> Wenn du **Pfad B's Auto-Installations-Skript (install_gs.sh)** verwendet hast, werden die Schlüssel automatisch erzeugt und konfiguriert. Bei manueller Installation stell sicher, dass `drone.key` und `gs.key` ein Paar sind.

---

### D. Die zentrale Konfigurationsdatei: /etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` ist die Kernkonfigurationsdatei von wfb-ng. Hier sind die Parameter, die du am häufigsten anpassen musst:

```ini
[common]
# Kanal 165 = 5825 MHz (5,8-GHz-Band)
wifi_channel = 165

# Ländercode auf 'BO' (Bolivien) setzen, um maximale Sendeleistung freizuschalten
wifi_region = 'BO'

[drone]
# link_domain muss auf Drohne UND Bodenstation IDENTISCH sein
link_domain = "my_wfb_link_01"

[drone_mavlink]
# MAVLink vom Flugcontroller-UART empfangen (UART auf 1500000 Baud einstellen)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Gleiche Einstellung wie oben – muss mit der Drohne übereinstimmen
link_domain = "my_wfb_link_01"
```

**Die drei häufigsten Fehlerquellen:**

1. **`wifi_channel` muss auf beiden Seiten gleich sein**: Dieser Guide verwendet 165 (5825 MHz, 5,8 GHz). Setze ihn auf Drohne und Bodenstation identisch.
2. **`link_domain` muss auf beiden Seiten gleich sein**: Das ist die Link-Kennung. Unterschiedliche Werte bedeuten keine Verbindung.
3. **Flugcontroller-UART-Baudrate auf 1500000 einstellen**: `peer = 'serial:ttyS0:1500000'` setzt voraus, dass der UART des Flugcontrollers ebenfalls auf 1500000 Baud konfiguriert ist – sonst kommt keine MAVLink-Verbindung zustande.

{{< alert "triangle-exclamation" >}}
**Hinweis**: `wifi_region = 'BO'` schaltet die maximale Sendeleistung frei, aber **das bedeutet nicht, dass dies an deinem Standort legal ist**. Beachte den rechtlichen Hinweis unten.
{{< /alert >}}

---

## 8. Praktische Hinweise und häufige Fehler

Dieser Abschnitt behandelt Probleme, auf die wir bei echten Installationen gestoßen sind. Bitte lesen.

### Stolperfalle 1: Zu schwache Stromversorgung führt zu Adapter-Resets und Paketverlust

Der AWUS036ACH zieht **beim Senden (TX) kurzzeitig sehr viel Strom**. Eingesteckt in einen normalen USB-2.0-Port des Raspberry Pi reicht die USB-Stromversorgung nicht aus. Ergebnis: **Adapter-Port wird zurückgesetzt, Verbindung bricht ab, Pakete werden korrumpiert, Bild bleibt stehen**.

Lösung (auf der Drohnenseite zwingend erforderlich):

- Versorge den Adapter **direkt über ein 5V-BEC** (nicht über den USB-Port des Pi). Schließe den BEC-Ausgang an den Adapter an.
- Schalte einen **470µF Low-ESR-Kondensator zwischen +5V und GND** des Adapters, um die Stromspitzen beim Senden abzufangen.
- Auf der Bodenstation reicht ein **USB-3.0-Port eines Laptops mit dem Original-USB-3.0-Kabel** normalerweise aus – kein zusätzliches BEC nötig.

> Dieser Schritt entscheidet darüber, ob dein Link stabil läuft. Wir haben unzählige Fälle von Paketverlust gesehen, die auf eine schlechte Stromversorgung zurückzuführen waren.

### Stolperfalle 2: Verschlüsselungsfehler / keine Verbindung

Wenn `wfb-cli gs` „verbunden" anzeigt, aber **kein Video und keine Telemetrie ankommt**, liegt es fast immer an einem der folgenden Punkte:

- **Schlüsselkonflikt**: Prüfe, ob `drone.key` auf der Drohne und `gs.key` auf der Bodenstation zusammengehören.
- **Kanal- oder link_domain-Konflikt**: Beide Seiten müssen identische `wifi_channel`- und `link_domain`-Einstellungen haben.

Debug-Befehl:

```bash
# Bodenstations-Logs auf Verschlüsselungs-/Verbindungsfehler prüfen
journalctl -xu wifibroadcast@gs
```

### Stolperfalle 3: Rechtliche Hinweise (wichtig)

Dieser Link sendet aktiv Funkwellen. Er ist eine Funkübertragungseinrichtung.

- **Prüfe vor der Nutzung, ob deine lokalen Vorschriften diese Art von WLAN-Übertragung mit der geplanten Leistung und den verwendeten Frequenzen erlauben.**
- Taiwan, China, die EU und die USA haben jeweils eigene Regelungen für Sendeleistung, verfügbare Kanäle und „Nicht-Verbindungs"-Übertragungen im 5,8-GHz-ISM-Band.
- Die Einstellung `wifi_region = 'BO'` hebt das Hardware-Leistungslimit auf, aber **macht die Nutzung nicht automatisch in deinem Land legal**. Passe Kanäle und Leistung an die lokalen Funkvorschriften an.
- Verwende den Link nur in autorisierten Umgebungen (privates Ackerland, abgeschlossene Testgelände, Schulungseinrichtungen). Störe nicht den Funkverkehr anderer.

---

## 9. Fazit

Mit einem einzigen ALFA AWUS036ACH und dem Open-Source-Projekt wfb-ng haben wir einen Link gebaut, der Folgendes bietet:

- **Kostenvorteil**: Die gesamten Materialkosten liegen weit unter jeder kommerziellen Digital-FPV-Lösung.
- **Open Source**: Jede Codezeile, jeder Treiber, jede Konfiguration ist öffentlich einsehbar.
- **Vollständig anpassbar**: Kanäle, Leistung, Verschlüsselungsschlüssel, MAVLink-Routing – alles unter deiner Kontrolle.
- **Große Reichweite**: Digitales Video und Telemetrie auf einem Link, 5-GHz-Feldtests zeigen Reichweiten weit über analog, mit Verschlüsselung und Störfestigkeit.

Für Agrar-Sprühanwendungen, Inspektionen, Security-Training oder alle, die verstehen wollen, wie digitales FPV im Detail funktioniert, ist dies ein lohnender Weg.

Unser Team wird auf diesem Blog weitere ALFA-Adapter-Drohnenlink-Implementierungen vorstellen. Wenn du bei der Einrichtung auf Probleme stößt, melde dich gerne – **selber bauen ist der schnellste Weg, etwas zu lernen**.

---

{{< faq >}}

---

## Anhang: Glossar für Einsteiger

Wenn du dich zum ersten Mal mit Drohnen-Link-Technik beschäftigst, hier eine kurze Erklärung der in diesem Guide verwendeten Begriffe:

| Begriff | Einfache Erklärung |
|---|---|
| **FPV** (First Person View) | Eine Live-Kameraübertragung von der Drohne zu einem Bildschirm oder einer Brille am Boden – als ob du im Cockpit sitzt. |
| **Digital FPV vs. Analog FPV** | Analog ist wie altes Fernsehen: schwaches Signal bedeutet Rauschen, und jeder kann mithören. Digital codiert Video in Datenpakete – es kann verschlüsselt werden, kommt besser mit Störungen klar, braucht aber komplexere Hardware und Einrichtung. |
| **Monitor Mode** | Normale WLAN-Adapter verbinden sich nur mit Access Points. Der Monitor Mode versetzt den Adapter in einen Zustand, in dem er rohe Funksignale hört und sendet, ohne sich mit etwas zu verbinden – die Grundlage dieses Guides. |
| **Packet Injection** | Im Monitor Mode kannst du eigene Funkframes direkt in die Luft schicken, ohne den normalen WLAN-Verbindungsablauf. wfb-ng nutzt dies, um Video und Telemetrie zu übertragen. |
| **wfb-ng** | Open-Source-Software, die einen WLAN-Adapter in eine drohnenspezifische Funkverbindung verwandelt. Die Kernsoftware dieses Guides. |
| **FEC (Forward Error Correction)** | Der Sender fügt zusätzliche redundante Daten hinzu. Gehen auf dem Funkweg Pakete verloren, rekonstruiert der Empfänger die Originaldaten aus der Redundanz – keine Neuübertragung nötig (die bei großer Entfernung und Bewegung zu langsam wäre). |
| **MAVLink** | Das Standardprotokoll, mit dem Drohnen-Flugcontroller (Pixhawk usw.) mit Bodenstationen kommunizieren – für Flugstatus, Befehle und Telemetriedaten. |
| **RTP / RTSP** | Standardprotokolle zum Streamen von Live-Video über ein Netzwerk. Deine IP-Kamera und Überwachungsanlage nutzen vermutlich ähnliche Protokolle. |
| **libsodium-Verschlüsselung** | Die Open-Source-Verschlüsselungsbibliothek, die in diesem Guide zum Verschlüsseln von Video und Telemetrie verwendet wird. Nur die zusammengehörige Drohne und Bodenstation können die Inhalte entschlüsseln. |
| **TX-Diversity (Sendediversity)** | Mehrere Adapter senden dieselben Daten gleichzeitig. Wird das Signal eines Adapters blockiert, springt ein anderer ein – wie ein doppeltes Sicherungssystem. |
| **BEC (Battery Eliminator Circuit)** | Ein Spannungsregler, der die Akkuspannung der Drohne auf die 5 V herunterregelt, die der Adapter braucht, und dabei die hohen Stromspitzen abfängt, ohne dass die Spannung einbricht. |
| **RTL8812AU** | Der Realtek-Chipsatz im ALFA AWUS036ACH. Dieser Chip bestimmt, ob der Adapter Monitor Mode und Packet Injection unterstützt. |

> Zusammengefasst: wfb-ng verwandelt den ALFA-Adapter in eine dedizierte Drohnenfunkstation, sodass Video und Flugdaten über offene, verschlüsselte Wege große Entfernungen zurücklegen können – dein eigener privater Kanal.

---

## Referenzen

- **wfb-ng-Projekt (svpcom/wfb-ng)**: https://github.com/svpcom/wfb-ng.git
- **ALFA AWUS036ACH-Produktseite**: https://yupitek.com/de/products/alfa/awus036ach/
- **Gepatchter Treiber (RTL8812AU)**: https://github.com/svpcom/rtl8812au
- **Gepatchter Treiber (RTL8812EU)**: https://github.com/svpcom/rtl8812eu
- **PX4 WFB-ng-Tutorial**: https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*Dieser Artikel wurde vom Yupitek-Technikerteam (offizieller ALFA-Network-Distributor, Taiwan) auf Basis der wfb-ng-Dokumentation und praktischer Erfahrung erstellt. Prüfe vor dem Bau deines Links die lokalen Funkvorschriften und passe Sendeleistung und Frequenzen entsprechend an.*
