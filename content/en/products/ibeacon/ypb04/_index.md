---
title: "YPB04 Rechargeable Badge Beacon"
description: "YPB04 Rechargeable Smart Card Badge Bluetooth Beacon. Features magnetic charging, 150m range, IP67 waterproof design, accelerometer, vibration motor, RGB LED, and optional RFID for personnel management and check-in."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "Rechargeable", "Badge", "RFID", "Sensor", "Vibration"]
---

## Product Overview

The **YPB04** is a wearable card-shaped Bluetooth® Low Energy (BLE 5.0) beacon designed for smart office check-in, personnel flow monitoring, and geofencing. Its slim badge form factor (86 × 55 × 6 mm, weighing only 19g) is easily worn on lanyards or attached to uniforms.

Equipped with an **external push button**, a **vibration motor**, and an **RGB LED**, the YPB04 offers visual and physical feedback. It features a magnetic charging port, an integrated 3-axis accelerometer sensor, and optional support for dual-frequency **RFID (LF/HF/UHF)**, allowing it to combine BLE tracking with traditional physical gate card access.

---

## Technical Specifications

| Parameter | Specifications | Remarks |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Low latency and high efficiency |
| **Bluetooth Version** | BLE 5.0 | Secure connection and long range |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensors** | 3-axis accelerometer | Displacement and movement detection |
| **Feedback Elements** | 1 × Vibration Motor, 1 × RGB LED | Tactile and visual cues |
| **Control Button** | 1 × External physical button | Activates triggers and alarms |
| **RFID Compatibility** | LF / HF / UHF | Optional build integrations |
| **Transmission Range** | Up to 150 meters (492 ft) | Maximum in open areas |
| **Power Source** | Magnetic charging Li-po battery | 270mAh capacity (Rechargeable) |
| **Battery Lifetime** | Up to 3 months | Depending on click frequency |
| **Charging Time** | Approximately 2 hours | 5V / 1A power adapter |
| **Dimensions & Weight** | 86 × 55 × 6 mm \| 19 g | Slim card format |

---

## Operational Guide

### Turning the Badge ON
* Press and hold the physical button for **3 seconds**.
* The blue LED will turn on for 3 seconds and the device will vibrate once to confirm activation.

### Turning the Badge OFF
* For security, the device can only be turned off wirelessly via the **BeaconSET+ App** after entering the configuration password.
* When successfully shut down, the blue LED will flash 5 times.

### Battery Status & Charging
* **Low Battery Alert:** When battery falls below 20%, the red LED will flash once every 3 seconds.
* **Charging Indicator:** The red LED remains on while charging.
* **Fully Charged:** The green LED remains on once charging is complete.

### Button Click Triggers
You can configure the badge button to trigger specific broadcasts (e.g. double-click or triple-click to send emergency signals or check-in telemetry):
* **Double-click:** Blue LED flashes twice and the motor vibrates once.
* **Triple-click:** Blue LED flashes 3 times and the motor vibrates twice.

---

## Configuration Guidance

The parameters of YPB04 (including trigger behaviors, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the badge's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Product Gallery

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb04.png" alt="Yupitek YPB04 Rechargeable Smart Card Badge Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Need a custom quotation or integration solution? Please contact our sales team directly at: **sales@yupitek.com**
{{< /alert >}}
