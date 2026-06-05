---
title: "YPB02 Bewegungssensor BLE Beacon"
description: "YPB02 Bewegungssensor BLE Beacon. Bluetooth Low Energy BLE 5.0, für Lokalisierung, Zeiterfassung und Asset-Tracking."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Produktübersicht

Der **YPB02** ist ein Bluetooth® Low Energy (BLE 5.0) Bewegungssensor-Beacon mit integriertem **LIS3DH 3-Achsen-Beschleunigungssensor**. Er teilt das Gehäuse, die CR2477-Batterie und die IP67-Schutzklasse mit dem YPB01, bietet jedoch zusätzlich intelligente Bewegungserkennung.

Der Beacon unterstützt triggerbasierte Werbung, um Beschleunigungsdaten in Echtzeit zu senden oder das Sendeintervall nur bei Bewegung, Vibration oder Sturz zu verkürzen.

---

## Hauptmerkmale

* **3-Achsen-Beschleunigungssensor:** LIS3DH-Sensor zur Erfassung von Bewegung, Neigung und Beschleunigung auf X-, Y- und Z-Achsen.
* **Triggerbasierte Ausstrahlung:** Nur bei Bewegung senden, Sturzalarm senden oder das Intervall bei Bewegung auf 100 ms verkürzen.
* **IP67 Schutz:** Staub- und wasserdicht.
* **Austauschbare Batterie:** Einfacher Austausch der CR2477-Münzzelle.

---

## Bewegungsauslöser & Telemetrie

Unterstützt durch den LIS3DH-Sensor bietet der YPB02:
1. **Aktivitätsabhängiges Senden:** Sendet Standard-Frames dauerhaft, triggert Sensordaten-Frames jedoch nur bei Bewegung.
2. **Ruhe- und Bewegungsmodus:** Schläft im Stillstand und sendet im 100ms-Intervall, sobald sich das Asset bewegt.
3. **Schwellenwert-Kalibrierung:** Bewegungsschwellen und Dauer sind in der App konfigurierbar.

---

## Konfigurationsanleitung

Die Konfiguration erfolgt drahtlos über die **BeaconSET+** App:
1. Laden Sie **BeaconSET+** herunter.
2. Aktivieren Sie Bluetooth und Standortdienste.
3. Suchen Sie nach der MAC-Adresse und verbinden Sie sich.
4. Geben Sie das Passwort ein, um die Bewegungsschwellen und andere Parameter anzupassen.

## Technical Specifications

| Parameter | Spezifikationen | Anmerkungen |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensor** | LIS3DH 3-axis accelerometer | X, Y, Z axes telemetry |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Produktgalerie

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
