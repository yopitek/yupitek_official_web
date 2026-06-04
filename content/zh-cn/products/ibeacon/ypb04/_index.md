---
title: "YPB04 充电式多功能智能工卡/胸卡信标"
description: "YPB04 充电式多功能智能工卡/胸卡信标。蓝牙低功耗 BLE 5.0 (低功耗蓝牙) 技术，专为考勤打卡、定位与资产追踪设计，可配置参数。"
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0 (低功耗蓝牙)", "Bluetooth", "Yupitek", "Rechargeable", "Badge", "RFID", "Sensor", "Vibration"]
---

## 产品概述

The **YPB04** is a wearable card-shaped Bluetooth® Low Energy (BLE 5.0 (低功耗蓝牙)) beacon designed for smart office check-in, personnel flow monitoring, and geofencing. Its slim badge form factor (86 × 55 × 6 mm, weighing only 19g) is easily worn on lanyards or attached to uniforms.

Equipped with an **external push button**, a **vibration motor**, and an **RGB LED**, the YPB04 offers visual and physical feedback. It features a magnetic charging port, an integrated 3-axis accelerometer sensor, and optional support for dual-frequency **RFID (LF/HF/UHF)**, allowing it to combine BLE tracking with traditional physical gate card access.

---

## 技术规格

| 参数项目 | 技术规格 | 备注说明 |
| :--- | :--- | :--- |
| **芯片型号** | nRF52 系列 | Low latency and high efficiency |
| **蓝牙版本** | BLE 5.0 (低功耗蓝牙) | Secure connection and long range |
| **防水等级** | IP67 (防尘防水) | Splash and dust resistant (1m immersion) |
| **传感器** | 3-axis accelerometer | Displacement and movement detection |
| **反馈机制** | 1 × 震动马达，1 × RGB LED 指示灯 | Tactile and visual cues |
| **控制按钮** | 1 × 外部实体按钮 | Activates triggers and alarms |
| **RFID 兼容性** | 低频(LF) / 高频(HF) / 超高频(UHF) (选配) | Optional build integrations |
| **传输距离** | 最远 150 米 (492 英尺，开阔空间) | Maximum in open areas |
| **电源规格** | 磁吸充电式锂聚合物电池 (270mAh) | 270mAh capacity (Rechargeable) |
| **电池寿命** | 最长可达 3 个月 (一般按压频率) | Depending on click frequency |
| **充电时间** | 约 2 小时 (室温，5V/1A 电源适配器) | 5V / 1A power adapter |
| **外观尺寸与重量** | 86 × 55 × 6 mm \| 19 g | Slim card format |

---

## 操作说明

### Turning the Badge ON
* Press and hold the physical button for **3 seconds**.
* The blue LED will turn on for 3 seconds and the device will vibrate once to confirm activation.

### Turning the Badge OFF
* For security, the device can only be turned off wirelessly via the **BeaconSET+ App** after entering the configuration password.
* When successfully shut down, the blue LED will flash 5 times.

### 电量状态与充电指示
* **Low Battery Alert:** When battery falls below 20%, the red LED will flash once every 3 seconds.
* **Charging Indicator:** The red LED remains on while charging.
* **Fully Charged:** The green LED remains on once charging is complete.

### 按钮点击触发广播
You can configure the badge button to trigger specific broadcasts (e.g. double-click or triple-click to send emergency signals or check-in telemetry):
* **Double-click:** Blue LED flashes twice and the motor vibrates once.
* **Triple-click:** Blue LED flashes 3 times and the motor vibrates twice.

---

## 配置指南

The parameters of YPB04 (including trigger behaviors, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the badge's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## 产品图片

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb04.png" alt="Yupitek YPB04 Rechargeable Smart Card Badge Beacon" />
{{< /gallery >}}

---

{{< alert >}}
需要专属报价或定制化解决方案？请直接来信联系我们的销售团队：**sales@yupitek.com**
{{</alert >}}
