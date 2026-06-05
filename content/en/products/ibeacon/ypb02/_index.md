---
title: "YPB02 Motion-Sensing BLE Beacon"
description: "YPB02 Bluetooth Low Energy (BLE 5.0) sensor beacon. Features LIS3DH 3-axis accelerometer, replaceable CR2477 battery, IP67 waterproof design for motion detection, fall alarm, and asset tracking."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Product Overview

The **YPB02** is a motion-sensing Bluetooth® Low Energy (BLE 5.0) beacon equipped with an integrated **LIS3DH 3-axis accelerometer sensor**. While sharing the compact form factor, replaceable 1000mAh CR2477 coin-cell battery, and IP67 waterproof casing of the YPB01, the YPB02 adds intelligent motion detection and telemetry.

The beacon supports trigger-based advertising, allowing it to broadcast real-time acceleration data or modify its transmission interval only when moving, vibrating, or in the event of a fall. This minimizes battery drain and enables advanced asset activity monitoring.

---

## Technical Specifications

| Parameter | Specifications | Remarks |
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

## Key Features

* **3-Axis Acceleration Sensor:** Features the LIS3DH sensor mapping displacement, tilt, and motion telemetry along X, Y, and Z axes.
* **Trigger-Based Broadcasting:** Supports configuring specific trigger conditions (e.g., motion-only broadcasting, falling alerts, or changing the interval to 100ms when moved to trace asset displacement).
* **High Protection Enclosure:** Rated IP67 waterproof and dustproof, allowing indoor and light outdoor installation.
* **Replaceable Battery:** Long-lasting CR2477 battery (1000mAh) is easily replaced using the rotatable housing mechanism.

---

## Motion Trigger & Telemetry

Using the LIS3DH sensor, YPB02 supports:
1. **Activity-Based Advertising:** Broadcasts standard iBeacon/Eddystone frames continuously, but triggers sensor data frames (HT/ACC) only when the beacon is shifted or moving.
2. **Coexistence Mode:** Supports static vs. motion parameters. For example, the beacon can stay silent (sleep mode) when stationary, and broadcast at 100ms interval when moved to track real-time position.
3. **Threshold Calibration:** Acceleration thresholds and trigger duration can be customized inside the app.

---

## Configuration Guidance

The parameters of YPB02 (including accelerometer thresholds, triggers, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the beacon's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Product Gallery

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02 Sensor BLE 5.0 Coin Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}
