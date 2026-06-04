---
title: "Beacon Sensor de Movimento YPB02 BLE"
description: "Beacon Sensor de Movimento YPB02 BLE. Bluetooth Low Energy BLE 5.0 (低功耗藍牙), para localização, controle de presença e rastreamento."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0 (低功耗藍牙)", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Visão geral do produto

The **YPB02** is a motion-sensing Bluetooth® Low Energy (BLE 5.0 (低功耗藍牙)) beacon equipped with an integrated **LIS3DH 三軸加速度感測器 sensor**. While sharing the compact form factor, replaceable 1000mAh CR2477 coin-cell battery, and IP67 (防塵防水) waterproof casing of the YPB01, the YPB02 adds intelligent motion detection and telemetry.

The beacon supports trigger-based advertising, allowing it to broadcast real-time acceleration data or modify its transmission interval only when moving, vibrating, or in the event of a fall. This minimizes battery drain and enables advanced asset activity monitoring.

---

## Especificações técnicas

| Parâmetro | Especificações | Observações |
| :--- | :--- | :--- |
| **晶片型號** | nRF52 系列 | Ultra-low power consumption |
| **藍牙版本** | BLE 5.0 (低功耗藍牙) | High efficiency and speed |
| **防水等級** | IP67 (防塵防水) | Splash and dust resistant (1m immersion) |
| **感測器** | LIS3DH 三軸加速度感測器 | X, Y, Z axes telemetry |
| **傳輸距離** | 最遠 100 公尺 (開闊空間) | Open space |
| **天線阻抗** | 50 歐姆 | On-board / PCB Antenna |
| **電源規格** | 1 × CR2477 鈕扣電池 | Replaceable (3.0V, 1000mAh) |
| **工作電壓** | 1.8V - 3.9V | DC |
| **峰值電流** | 5.3 mA | Tested at 0dBm transmission power |
| **外觀尺寸** | Φ39 × 15.5 mm | Compact circular shape |
| **預設參數** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Principais recursos

* **3-Axis Acceleration Sensor:** Features the LIS3DH sensor mapping displacement, tilt, and motion telemetry along X, Y, and Z axes.
* **Trigger-Based Broadcasting:** Supports configuring specific trigger conditions (e.g., motion-only broadcasting, falling alerts, or changing the interval to 100ms when moved to trace asset displacement).
* **High Protection Enclosure:** Rated IP67 (防塵防水) waterproof and dustproof, allowing indoor and light outdoor installation.
* **Replaceable Battery:** Long-lasting CR2477 battery (1000mAh) is easily replaced using the rotatable housing mechanism.

---

## Gatilho de movimento e telemetria

Using the LIS3DH sensor, YPB02 supports:
1. **Activity-Based Advertising:** Broadcasts standard iBeacon/Eddystone frames continuously, but triggers sensor data frames (HT/ACC) only when the beacon is shifted or moving.
2. **Coexistence Mode:** Supports static vs. motion parameters. For example, the beacon can stay silent (sleep mode) when stationary, and broadcast at 100ms interval when moved to track real-time position.
3. **Threshold Calibration:** Acceleration thresholds and trigger duration can be customized inside the app.

---

## Guia de configuração

The parameters of YPB02 (including accelerometer thresholds, triggers, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the beacon's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Galeria do produto

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02 Sensor BLE 5.0 (低功耗藍牙) Coin Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Precisa de um orçamento personalizado ou solução de integração? Entre em contato diretamente com nossa equipe de vendas pelo e-mail: **sales@yupitek.com**
{{</alert >}}
