---
title: "SDRLab Flipper Zero 5G Add-On Board — Dual-Band WLAN Sicherheitsforschungsmodul"
description: "Flipper Zero 5G Add-On Board, RTL8720DN Dual-Band (2,4+5GHz) WLAN, BLE 5.0, vorinstallierte Deauth-Firmware, GPIO-gespeist, kompatibel mit Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

# SDRLab Flipper Zero 5G Erweiterungsboard — Dual-Band Wi-Fi Sicherheitsforschungsmodul

> **Haftungsausschluss für die legale Nutzung**: Dieses Erweiterungsboard ist ausschließlich für autorisierte Sicherheitsforschung und legale Untersuchungen bestimmt. Tests an Netzwerken, Geräten oder Infrastrukturen, die dir nicht gehören oder für die du keine schriftliche Genehmigung hast, sind in den meisten Ländern illegal. Bitte stelle sicher, dass du die lokalen Vorschriften zur Funkfrequenznutzung einhältst und dieses Produkt verantwortungsvoll und ethisch einsetzt.

---

## 1. Was ist das?

Ein Funkforschungs-Erweiterungsboard, das auf den GPIO-Stiften auf der Rückseite deines Flipper Zero aufgesteckt wird. Damit rügst du dein bisheriges, nur 2.4GHz-fähiges Flipper Zero auf vier Funkfähigkeiten auf:

- **Dual-Band Wi-Fi 2.4GHz + 5GHz** (802.11 b/g/n/ax, Wi-Fi 6)
- **Bluetooth BLE 5.0**
- **433MHz Sub-GHz** Funk
- **Aktives GPS**

Zusätzlich gibt es einen **2,8-Zoll-Farb-TFT-Bildschirm**, einen **800mAh hot-swappable Akku**, **microSD-Aufzeichnung**, **vier SMA-Antennenanschlüsse samt vier Antennen** und die **ausgewerkte ESP32 Marauder 5G-Firmware**.

Kein Kauf eines Programmiergeräts nötig, kein selbst kompilieren der Firmware. Anschließen, drei Parameter einstellen, loslegen.

---

## 2. Produktmerkmale

### Vier Funkarten auf einmal
- **Dual-Band Wi-Fi 2.4GHz + 5GHz** — Scanne moderne 5GHz-Netzwerke und schließe die Lücke der alten Boards, die nur 2.4GHz konnten.
- **433MHz Sub-GHz (A07-Funkmodul, 10 dBm)** — Eine zusätzliche Option für Umgebungen, in denen der eingebaute Empfänger des Flipper Zero schlecht empfängt.
- **Aktives GPS** — Wardrive-Aufzeichnungen erhalten automatisch Koordinaten. Während des Anschlusses am Flipper wird das Board vom Host versorgt, im abgekoppelten Zustand wechselt es automatisch auf den internen Akku.
- **Bluetooth BLE 5.0** — BLE-Geräte-Enumeration und Beacon-Analyse, parallel zur Wi-Fi-Forschung möglich.

### 2,8-Zoll-Farb-TFT-Bildschirm
Scan-Ergebnisse, Signalstärke, Akkustand und microSD-Nutzung werden direkt auf dem Board angezeigt. Du musst nicht mehr am Computer-Terminal raten. Die Marauder-Oberfläche ist bereits integriert.

### Vier SMA-Antennenanschlüsse, vier Antennen inklusive
Die Rückseite ist beschriftet, um die Zuordnung der Anschlüsse klar zu machen:

| Beschriftung | Position | Verwendung |
|---|---|---|
| `433M A` | Oben links | 433MHz Funk (A07-Modul, 10 dBm) |
| `GPS` | Oben rechts | Aktive GPS-Antenne |
| `2.4G` | Linke Seite | Wi-Fi 2.4GHz |
| `2.4G/5G` | Rechte Seite | Wi-Fi Dual-Band 2.4GHz + 5GHz |

Alle vier Anschlüsse sind unabhängige, schraubbare SMA-Buchsen. **Alle vier Antennen werden mitgeliefert, jede hat eine Verstärkung von 5dBi.**

### 800mAh Hot-Swappable Akku
Das Board kommt werkseitig mit einem 800mAh-Lithium-Polymer-Akku. Du kannst es vom Flipper abkoppeln, im Eigenbetrieb Pakete mitschneiden und danach wieder als Erweiterungsboard an den Host anschließen. USB-C-Ladung, ca. 2 Stunden für volle Ladung.

### microSD-Aufzeichnung für spätere Analyse
Unterstützt **FAT32-formatierte microSD-Karten bis 32GB**. Mitgeschnittene Pakete werden als `.pcap` gespeichert und können direkt mit Wireshark analysiert werden. Wardrive-Routen werden zusätzlich als `wardrive_*.csv` exportiert.

### Werkseitig vorinstallierte Marauder 5G-Firmware
Plug & Play, kein separates Programmiergerät nötig. Der USB-C-Anschluss auf dem Board bleibt für fortgeschrittene Nutzer erhalten, um die Firmware selbst zu aktualisieren.

### Goldkontakte + TVS-Überspannungsschutz
Alle Signalpins sind vergoldet. Jeder Pin ist mit einem TVS-Transientenspannungsableiter ausgestattet, der beim Ein- und Ausstecken des Flipper Zero vor Überspannungsspitzen schützt.

### Kompatibel mit der Firmware-Ökosystem
Kompatibel mit angepassten Firmwares wie Momentum, Unleashed und Xtreme, die WiFi Marauder- und GPS-Anwendungen unterstützen.

---

## 3. Technische Daten

| Spezifikation | Wert / Beschreibung |
|---|---|
| **Hauptchip** | **Espressif ESP32-C5** (RISC-V) |
| **CPU** | Hochleistungs-RISC-V-Kern, bis zu 240 MHz, plus Low-Power (LP)-Kern für Hintergrundaufgaben |
| **Wi-Fi-Standard** | **IEEE 802.11 b/g/n/ax** (Wi-Fi 6), Dual-Band 2.4GHz + 5GHz |
| **Wi-Fi-Antennenanschluss** | **4 SMA-Buchsen**: 433M A / GPS / 2.4G / 2.4G+5G, **vier Antennen inklusive, alle 5dBi** |
| **Bluetooth** | **BLE 5.0** (⚠️ Kein Bluetooth Classic / BR-EDR unterstützt) |
| **Sub-GHz** | 433MHz A07-Funkmodul, **10 dBm** Ausgangsleistung |
| **GNSS** | Aktives GPS-Modul, **automatischer Versorgungswechsel** (Host-Stromversorgung beim Anschluss, interner Akku im abgekoppelten Zustand) |
| **Bildschirm** | **2,8-Zoll-Farb-TFT**, integrierte Marauder-Oberfläche |
| **Akku** | **800 mAh Lithium-Polymer**, hot-swappable |
| **Laden** | USB-C, 5V / 2A, ca. **2 Stunden** Ladezeit (vorne oben) |
| **Stromausgabe an Flipper** | 5V / 2.4A |
| **Speicher** | **microSD, FAT32-Format, max. 32GB** (kein exFAT/NTFS unterstützt) |
| **Schnittstelle** | Standard-GPIO-Leiste des Flipper Zero (**2x8 Pin**), vergoldet + TVS-Schutz pro Pin |
| **Vorinstallierte Firmware** | **ESP32 Marauder 5G** (Open Source, werkseitig vorinstalliert) |
| **Firmware-Kompatibilität** | Momentum, Unleashed, Xtreme |
| **Gehäusematerial** | 3D-gedruckter Kunststoff |
| **Verfügbare Farben** | Schwarz / Weiß / Transparent / Rot / Blau |
| **Abmessungen** | **90 × 58 × 15 mm** (ohne Antennen) |

### Lieferumfang
- 1x Hauptplatine (montiert, mit 3D-gedrucktem Gehäuse und 2,8-Zoll-Bildschirm)
- 4x Antennen (alle 5dBi) — je 1x `2.4G`, `2.4G+5G` (Dual-Band), `433M A`, `GPS`
- Flipper GPIO-Leistenverbindung

### Separat erhältlich
- **Flipper Zero Host-Gerät** (dieses Board ist eine Erweiterung, Host nicht enthalten)
- **microSD-Speicherkarte** (FAT32, max. 32GB)

---

## 4. Erste Schritte: Drei einzustellende Parameter

Das Board kommt werkseitig mit der Firmware vorinstalliert, ein Flashen ist nicht nötig. Nach dem Anschließen an das Flipper Zero müssen nur drei Pin-Konfigurationen gesetzt werden:

| Funktion | Einstellungspfad | Wert |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 oder 14** |
| **ESP32 (WiFi / BLE / Marauder)** |同上 → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS und ESP32 verwenden zwei verschiedene UART-Pins und dürfen nicht auf denselben Pin gesetzt werden**, sonst funktionieren weder GPS noch Wi-Fi.

Nach der Konfiguration starte das Flipper Zero neu. Unter `Apps → GPIO` sollten die entsprechenden WiFi Marauder- und GPS-Anwendungen erscheinen.

**Die microSD muss manuell im FAT32-Format formatiert werden**, und in `Device → Settings` muss die Speicherung von PCAP-Dateien aktiviert sein.

---

## 5. Anwendungsbereiche

- **Dual-Band Wi-Fi-Scan** — Passives Enumerieren von 2.4GHz- und 5GHz-Netzwerken; Erfassen von SSID, BSSID, Kanal, RSSI, Verschlüsselungstyp und verbundenen Clients
- **WPA-Handshake-Erfassung** — Sniffen von EAPOL/PMKID-Handshakes für autorisierte Sicherheitsaudits
- **Deauth-Tests** — Senden von Deauth-Paketen zur Netzresilienzprüfung, nur für eigene oder autorisierte Netzwerke
- **BLE-Geräte-Enumeration** — Scannen und Identifizieren von BLE 5.0-Peripheriegeräten in der Nähe, parallel zur Wi-Fi-Forschung möglich
- **Wardrive-Netzwerktopologie-Mapping** — GPS-markierte Wi-Fi- und Geräteaufzeichnungen, CSV-Export für die Nachanalyse
- **433MHz-Funkforschung** — Bedienung über das Sub-GHz-Menü des Flipper, ideal für Umgebungen mit schlechtem Empfang des internen Moduls
- **Evil Portal-Übungen** — Prototyping und Tests von Login-Seiten in autorisierten Umgebungen
- **IoT-Funkprotokollforschung** — Analyse des Verhaltens von IoT-Geräten im Dual-Band-Betrieb in kontrollierten Laboreinstellungen

---

## 6. Bekannte Einschränkungen (bitte beachten)

- **Die Stabilität von 5GHz Deauth hängt von der Firmware-Version ab.** Die Open-Source-Marauder-Firmware unterstützt 5GHz Deauth auf dem ESP32-C5 noch in der Verbesserung. Wir empfehlen, Deauth-Tests primär auf **2.4GHz** durchzuführen. Für 5GHz eignen sich Scan, Signalüberwachung und Wardrive-Aufzeichnungen besser. Die tatsächliche Leistung hängt von der aktuellen Firmware-Version ab.
- **GPS-Antennen sind richtungsabhängig**, obwohl sie als omnidirektional beworben werden. Richte die Antenne in Richtung freiem Himmel für eine bessere Positionsbestimmung. Der erste Kaltstart benötigt einige Minuten zum Herunterladen der Satellitendaten. Die Leistung in Innenräumen ist schlechter; nutze das Board draußen oder in der Nähe von Fenstern.
- **GPS-Zeiten sind in UTC+0**. Es gibt keine Zeitzonen-Einstellung in der Firmware. Für die Zeit in Taiwan (UTC+8) musst du 8 Stunden addieren.
- **microSD unterstützt nur FAT32**. exFAT und NTFS werden nicht unterstützt, und die Kapazität ist auf maximal 32GB beschränkt.
- **GPS und ESP32 nutzen verschiedene UART-Pins** (GPS: 13 oder 14; ESP32: 15, 16). Setze sie nicht auf denselben Pin, sonst funktionieren GPS und Wi-Fi nicht.
- **Bluetooth unterstützt nur BLE 5.0**. Die ESP32-C5-Hardware hat keinen Bluetooth Classic (BR/EDR), daher können keine klassischen Bluetooth-Lautsprecher, Kopfhörer oder Autoradios gekoppelt werden.
- **Die beiden USB-C-Anschlüsse haben unterschiedliche Funktionen** — Der vordere obere Anschluss dient dem Laden (5V/2A); der vordere linke Anschluss dient nur dem Firmware-Flashen und lädt nicht. Ein falsches Anschließen führt nicht zur Beschädigung des Hosts, lädt aber auch nicht.
- **Automatischer GPS-Versorgungswechsel** — Beim Anschluss an das Flipper wird das Board vom Host versorgt, im abgekoppelten Zustand wechselt es auf den internen Akku. Kurze Neustarts beim Umschalten sind normal.

---

## 7. Offene Spezifikationspunkte

Für die folgenden Punkte liegen keine zuverlässigen schriftlichen Angaben vom Hersteller vor. Wir haben die konkreten Zahlen bewusst weggelassen, um keine Fehlinformationen zu verbreiten:

| Punkt | Status |
|---|---|
| Wi-Fi-Sendeleistung (dBm) | Wird vom Hersteller bestätigt |
| Aktiver Stromverbrauch (mA) | Wird vom Hersteller bestätigt |
| Betriebstemperaturbereich | Wird vom Hersteller bestätigt |
| Anzahl der Akku-Anzeige-LEDs (einzelne oder segmentiert) | Wird am Gerät bestätigt |

Sobald diese Punkte bestätigt sind, werden sie hier aktualisiert.

---

**Produktlink**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Vollständiges Benutzerhandbuch**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/