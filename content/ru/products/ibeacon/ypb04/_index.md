---
title: "Перезаряжаемый маяк-бейдж YPB04"
description: "Перезаряжаемый маяк-бейдж YPB04. Bluetooth Low Energy BLE 5.0 (低功耗藍牙), для позиционирования, контроля присутствия и трекинга."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0 (低功耗藍牙)", "Bluetooth", "Yupitek", "Rechargeable", "Badge", "RFID", "Sensor", "Vibration"]
---

## Обзор продукта

The **YPB04** is a wearable card-shaped Bluetooth® Low Energy (BLE 5.0 (低功耗藍牙)) beacon designed for smart office check-in, personnel flow monitoring, and geofencing. Its slim badge form factor (86 × 55 × 6 mm, weighing only 19g) is easily worn on lanyards or attached to uniforms.

Equipped with an **external push button**, a **vibration motor**, and an **RGB LED**, the YPB04 offers visual and physical feedback. It features a magnetic charging port, an integrated 3-axis accelerometer sensor, and optional support for dual-frequency **RFID (LF/HF/UHF)**, allowing it to combine BLE tracking with traditional physical gate card access.

---

## Технические характеристики

| Параметр | Технические характеристики | Примечания |
| :--- | :--- | :--- |
| **晶片型號** | nRF52 系列 | Low latency and high efficiency |
| **藍牙版本** | BLE 5.0 (低功耗藍牙) | Secure connection and long range |
| **防水等級** | IP67 (防塵防水) | Splash and dust resistant (1m immersion) |
| **感測器** | 3-axis accelerometer | Displacement and movement detection |
| **反饋機制** | 1 × 震動馬達，1 × RGB LED 指示燈 | Tactile and visual cues |
| **控制按鈕** | 1 × 外部實體按鈕 | Activates triggers and alarms |
| **RFID 相容性** | 低頻(LF) / 高頻(HF) / 超高頻(UHF) (選配) | Optional build integrations |
| **傳輸距離** | 最遠 150 公尺 (492 英尺，開闊空間) | Maximum in open areas |
| **電源規格** | 磁吸充電式鋰聚合物電池 (270mAh) | 270mAh capacity (Rechargeable) |
| **電池壽命** | 最長可達 3 個月 (一般按壓頻率) | Depending on click frequency |
| **充電時間** | 約 2 小時 (室溫，5V/1A 電源供應器) | 5V / 1A power adapter |
| **外觀尺寸與重量** | 86 × 55 × 6 mm \| 19 g | Slim card format |

---

## Руководство по эксплуатации

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

## Руководство по настройке

The parameters of YPB04 (including trigger behaviors, UUID, Major, and Minor) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the badge's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Галерея продукта

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb04.png" alt="Yupitek YPB04 Rechargeable Smart Card Badge Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Нужно индивидуальное предложение или интеграционное решение? Свяжитесь с нашим отделом продаж напрямую по адресу: **sales@yupitek.com**
{{</alert >}}
