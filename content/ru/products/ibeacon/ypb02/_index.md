---
title: "Маяк YPB02 BLE с датчиком движения"
description: "Маяк YPB02 BLE с датчиком движения. Bluetooth Low Energy BLE 5.0, для позиционирования, контроля присутствия и трекинга."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## Обзор продукта

**YPB02** — это Bluetooth® (BLE 5.0) маяк с встроенным **3-осевым акселерометром LIS3DH**. Он имеет тот же корпус IP67 и батарейку CR2477, что и YPB01, но поддерживает детекцию движения и телеметрию.

Маяк можно настроить на изменение частоты отправки сигналов или отправку алармов только при движении, вибрации или падении.

---

## Ключевые свойства

* **3-осевой акселерометр:** Датчик LIS3DH для измерения наклона и перемещения по осям X, Y, Z.
* **Трансляция по триггеру:** Вещание только при движении, оповещение о падении или сокращение интервала до 100 мс при сдвиге.
* **Защита IP67:** Пыле- и влагозащищенность.
* **Заменяемая батарея:** Удобная замена монетной батарейки CR2477.

---

## Триггеры движения и телеметрия

С помощью датчика LIS3DH маяк YPB02 поддерживает:
1. **Вещание по активности:** Отправка стандартных кадров непрерывно и активация кадров с датчиков только при перемещении.
2. **Двойной режим:** Режим сна в покое и вещание с интервалом 100 мс при движении.
3. **Настройка чувствительности:** Пороги срабатывания можно откалибровать в приложении.

---

## Руководство по настройке

Настройка выполняется по беспроводному каналу через приложение **BeaconSET+**:
1. Установите **BeaconSET+**.
2. Включите Bluetooth и геолокацию.
3. Выполните сопряжение по MAC-адресу.
4. Введите пароль администратора для изменения настроек.

## Technical Specifications

| Параметр | Технические характеристики | Примечания |
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

## Галерея продукта

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
Нужно индивидуальное предложение или интеграционное решение? Свяжитесь с нашим отделом продаж напрямую по адресу: **sales@yupitek.com**
{{< /alert >}}
