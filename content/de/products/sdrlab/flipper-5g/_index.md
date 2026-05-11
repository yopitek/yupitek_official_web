---
title: "SDRLab Flipper Zero 5G Add-On Board — Dual-Band WLAN Sicherheitsforschungsmodul"
description: "Flipper Zero 5G Add-On Board, RTL8720DN Dual-Band (2,4+5GHz) WLAN, BLE 5.0, vorinstallierte Deauth-Firmware, GPIO-gespeist, kompatibel mit Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

{{< alert "warning" >}}
**Hinweis zur legalen Nutzung**: Dieses Add-On Board ist ausschließlich für autorisierte Sicherheitsforschung und rechtmäßige Tests vorgesehen. Stellen Sie die Einhaltung der örtlichen Funkfrequenzvorschriften vor der Verwendung sicher.
{{< /alert >}}

## Funktionen

![SDRLab Flipper Zero 5G Add-On Board](/images/products/sdrlab/flipper-5g.png)

- **Dual-Band-Abdeckung** — 2,4 GHz + 5 GHz (IEEE 802.11 a/b/g/n); Zugang zu modernen 5-GHz-Netzwerken, die mit älteren Flipper-Add-Ons nicht erreichbar waren
- **Realtek RTL8720DN via AI Thinker BW16** — Industriestandard-Dual-Band-SoC mit FCC/CE-vorzertifiziertem Modul
- **Dual-Core CPU** — ARM Cortex-M4 @ 200 MHz verarbeitet aktive Protokolle; Cortex-M0 @ 20 MHz führt Hintergrundaufgaben mit geringem Stromverbrauch aus
- **Vorinstallierte Marauder 5G Firmware** — enthält Scan-, Deauth-, Beacon-Flood-, Sniff- (EAPOL/PMKID) und Evil-Portal-Modi; sofort einsatzbereit
- **BLE 5.0** — Bluetooth Low Energy Geräteaufzählung und Beacon-Analyse neben der WLAN-Forschung
- **GPIO-gespeist** — bezieht 5 V direkt vom GPIO-Header des Flipper Zero; kein externes Netzteil erforderlich
- **Antennen-Upgrade-Pfad** — IPEX (U.FL)-Anschluss bei unterstützten Revisionen für den Anschluss einer externen Hochgewinn-Antenne
- **Firmware-Ökosystem** — kompatibel mit Momentum und Unleashed Custom-Firmware-Frameworks
- **PlatformIO-Entwicklung** — vollständige Unterstützung für benutzerdefinierte Firmware-Entwicklung über das Arduino-kompatible Ameba D Framework
- **Robuster Betriebsbereich** — −40°C bis 85°C für den Feldeinsatz in jedem Klima

## Spezifikationen

| Spezifikation | Wert / Beschreibung |
|---------------|---------------------|
| Hauptchip | Realtek RTL8720DN (AI Thinker BW16 Modul) |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| WLAN-Standard | IEEE 802.11 a/b/g/n (2,4 GHz + 5 GHz Dual-Band) |
| WLAN TX-Leistung | ~17 dBm (je nach regionaler Regulierung) |
| Bluetooth | BLE 5.0 |
| Flash | 4 MB |
| Stromversorgung | Flipper Zero GPIO (5 V) |
| Typische Stromaufnahme | 150–250 mA (aktives Scanning) |
| Verbindungsschnittstelle | Flipper Zero Standard-GPIO-Header (2×8 Pin) |
| Vorinstallierte Firmware | Marauder 5G (Scan, Deauth, Beacon, Sniff, Evil Portal) |
| Firmware-Kompatibilität | Momentum, Unleashed |
| Benutzerdefinierte Entwicklung | PlatformIO (Ameba D / RTL8720DN Framework) |
| Betriebstemperatur | −40°C bis 85°C |
| Antennenschnittstelle | IPEX (U.FL) oder On-Board PCB-Antenne (je nach Revision) |
| Formfaktor | Flipper Zero GPIO Add-On Board |

## Anwendungsfälle

- **Dual-Band WLAN-Scanning** — passives Aufzählen von 2,4-GHz- und 5-GHz-Netzwerken; Erfassen von SSID, BSSID, Kanal, RSSI, Verschlüsselungstyp und verbundenen Clients
- **WLAN-Deauthentifizierungsforschung** — 802.11-Deauth-Frames senden, um die Netzwerkresilienz zu testen und den 802.11w/PMF (Protected Management Frames)-Schutz auf autorisierten Netzwerken zu evaluieren
- **WPA-Handshake-Erfassung** — EAPOL/PMKID-Handshakes für autorisierte Netzwerksicherheitsaudits abfangen
- **Evil Portal Entwicklung** — Prototyping von Rogue-AP-Captive-Portal-Szenarien für Phishing-Bewusstseinstests (nur in autorisierten Umgebungen)
- **Beacon-Flood-Testing** — benutzerdefinierte SSIDs übertragen, um die Auswirkungen von HF-Überlastung und das Client-Verhalten zu untersuchen
- **BLE-Geräteaufzählung** — nahegelegene BLE 5.0-Peripheriegeräte neben der WLAN-Forschung scannen und identifizieren
- **Mesh-Netzwerk-Topologiekartierung** — Mesh-AP-Beziehungen, Backhaul-Kanäle und versteckte SSID-Konfigurationen identifizieren
- **IoT-Funkprotokollforschung** — IoT-Geräteverhalten auf beiden WLAN-Bändern in einer kontrollierten Laborumgebung analysieren
- **Autorisierte Penetrationstest-Ausbildung** — praktische Lernplattform für WLAN-Sicherheitsgrundlagen in autorisierten Umgebungen

---

{{< alert "warning" >}}
**Neu mit diesem Board?** Folgen Sie unserem Schritt-für-Schritt-Einsteigerleitfaden — mit Voraussetzungen, Firmware-Setup, erstem Scan und allen wichtigen Funktionen.
[📖 Online-Benutzerhandbuch öffnen](/de/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
Angebot gewünscht? [Kontaktieren Sie uns](/de/contact/)
{{< /alert >}}
