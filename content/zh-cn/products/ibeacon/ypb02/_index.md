---
title: "YPB02 三轴加速度感测 BLE 蓝牙信标"
description: "YPB02 三轴加速度感测 BLE 蓝牙信标。蓝牙低功耗 BLE 5.0 (低功耗蓝牙) 技术，专为考勤打卡、定位与资产追踪设计，可配置参数。"
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0 (低功耗蓝牙)", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## 产品概述

The **YPB02** is a motion-sensing Bluetooth® Low Energy (BLE 5.0 (低功耗蓝牙)) beacon equipped with an integrated **LIS3DH 三轴加速度传感器 sensor**. While sharing the compact form factor, replaceable 1000mAh CR2477 coin-cell battery, and IP67 (防尘防水) waterproof casing of the YPB01, the YPB02 adds intelligent motion detection and telemetry.

The beacon supports trigger-based advertising, allowing it to broadcast real-time acceleration data or modify its transmission interval only when moving, vibrating, or in the event of a fall. This minimizes battery drain and enables advanced asset activity monitoring.

---

## 技术规格

| 参数项目 | 技术规格 | 备注说明 |
| :--- | :--- | :--- |
| **芯片型号** | nRF52 系列 | Ultra-low power consumption |
| **蓝牙版本** | BLE 5.0 (低功耗蓝牙) | High efficiency and speed |
| **防水等级** | IP67 (防尘防水) | Splash and dust resistant (1m immersion) |
| **传感器** | LIS3DH 三轴加速度传感器 | X, Y, Z axes telemetry |
| **传输距离** | 最远 100 米 (开阔空间) | Open space |
| **天线阻抗** | 50 欧姆 | On-board / PCB Antenna |
| **电源规格** | 1 × CR2477 纽扣电池 | Replaceable (3.0V, 1000mAh) |
| **工作电压** | 1.8V - 3.9V | DC |
| **峰值电流** | 5.3 mA | Tested at 0dBm transmission power |
| **外观尺寸** | Φ39 × 15.5 mm | Compact circular shape |
| **默认参数** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## 主要特点

* **3-Axis Acceleration Sensor:** Features the LIS3DH sensor mapping displacement, tilt, and motion telemetry along X, Y, and Z axes.
* **Trigger-Based Broadcasting:** Supports configuring specific trigger conditions (e.g., motion-only broadcasting, falling alerts, or changing the interval to 100ms when moved to trace asset displacement).
* **High Protection Enclosure:** Rated IP67 (防尘防水) waterproof and dustproof, allowing indoor and light outdoor installation.
* **Replaceable Battery:** Long-lasting CR2477 battery (1000mAh) is easily replaced using the rotatable housing mechanism.

---

## 运动触发与遥测数据

Using the LIS3DH sensor, YPB02 supports:
1. **Activity-Based Advertising:** Broadcasts standard iBeacon/Eddystone frames continuously, but triggers sensor data frames (HT/ACC) only when the beacon is shifted or moving.
2. **Coexistence Mode:** Supports static vs. motion parameters. For example, the beacon can stay silent (sleep mode) when stationary, and broadcast at 100ms interval when moved to track real-time position.
3. **Threshold Calibration:** Acceleration thresholds and trigger duration can be customized inside the app.

---

## 配置指南

The parameters of YPB02 (including accelerometer thresholds, triggers, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the beacon's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## 产品图片

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02 Sensor BLE 5.0 (低功耗蓝牙) Coin Beacon" />
{{< /gallery >}}

---

{{< alert >}}
需要专属报价或定制化解决方案？请直接来信联系我们的销售团队：**sales@yupitek.com**
{{</alert >}}
