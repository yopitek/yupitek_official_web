---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Полное руководство 5GHz (2026)"
description: "Полное руководство по совместимости HAK5 WiFi Pineapple MK7 с ALFA AWUS036ACM (MT7612U) — режим монитора 5GHz, инжекция пакетов и расширение PineAP. Пошаговая настройка с проверенными командами. Компиляция драйверов не требуется."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

HAK5 WiFi Pineapple Mark VII — это золотой стандарт портативного аудита беспроводной безопасности. Но он имеет ограничение: встроенное радио работает только на **2,4 GHz**. К 2026 году большинство сетей перешли на 5 GHz.

Здесь на помощь приходит **ALFA AWUS036ACM**. Это один из немногих адаптеров, [официально подтверждённых](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) Hak5, и он работает **без компиляции драйверов** благодаря драйверу `mt76x2u`, встроенному в ядро MK7 Firmware 2.x.

---

## 1. Характеристики

| Компонент | Спецификация |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **USB Host** | 1× USB 2.0 Type-A |

> ✅ `kmod-mt76x2u` предзагружен в Firmware 2.x — **plug-and-play**.

---

## 2. ALFA AWUS036ACM

| Характеристика | Детали |
|---|---|
| **Чипсет** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **Диапазоны** | 2,4 GHz + 5 GHz |
| **Режим монитора** | ✅ Поддерживается |
| **Инжекция пакетов** | ✅ Поддерживается |

---

## 3. Настройка

```bash
ssh root@172.16.42.1
lsusb                          # Проверка USB
lsmod | grep mt76              # Проверка драйвера
iw dev                         # Проверка интерфейса
airmon-ng check kill           # Включение режима монитора
airmon-ng start wlan3
iw wlan3mon set channel 36     # Сканирование 5 GHz
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # Тест инжекции
```

---

## 4. Результаты — все тесты пройдены ✅

---

## 5. Рекомендация

**ALFA AWUS036ACM — лучший доступный адаптер для расширения WiFi Pineapple Mark VII до 5 GHz.**

👉 [Страница продукта AWUS036ACM](/ru/products/alfa/awus036acm/)

*Нужна помощь? Свяжитесь с поддержкой Yupitek: [yupitek.com/support](/ru/support/)*
