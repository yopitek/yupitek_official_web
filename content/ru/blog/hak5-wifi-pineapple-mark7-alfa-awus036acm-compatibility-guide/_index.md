---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Полное руководство 5GHz (2026)"
description: "Полное руководство по совместимости HAK5 WiFi Pineapple MK7 с ALFA AWUS036ACM (MT7612U) — режим монитора 5GHz, инжекция пакетов и расширение PineAP. Пошаговая настройка с проверенными командами. Компиляция драйверов не требуется."
date: 2026-06-10
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"

faq:
  - question: "Нужен ли WiFi Pineapple Mark VII внешний адаптер?"
    answer: "Да. Встроенный радиомодуль MK7 поддерживает только 2.4 ГГц, в 2026 году большинство сетей перешли на 5 ГГц, внешний AWUS036ACM добавляет возможности мониторинга и инъекции 5 ГГц."
  - question: "Почему AWUS036ACM работает Plug & Play на MK7?"
    answer: "MK7 Firmware 2.x предустанавливает драйвер kmod-mt76x2u, чип MT7612U встроен в ядро с версии 4.19, без компиляции или установки."
  - question: "Ограничивает ли USB 2.0 производительность AWUS036ACM на MK7?"
    answer: "USB 2.0 ограничивает пропускную способность до 150-250 Мбит/с, но рабочие нагрузки пентестинга, такие как захват пакетов и сбор рукопожатий, не затрагиваются, ограничен только высокоскоростной мост."
  - question: "Как включить режим монитора на MK7?"
    answer: "Подключитесь по SSH и выполните airmon-ng start wlan3, интерфейс будет переименован в wlan3mon, проверьте режим через iwconfig."
  - question: "Какие адаптеры ALFA несовместимы с MK7?"
    answer: "AWUS036AX и AWUS036AXER (RTL8832BU), AWUS036EACS (RTL8811CU) — драйверы не поддерживают режим монитора или инъекцию, все несовместимы."
---

HAK5 WiFi Pineapple Mark VII — это золотой стандарт портативного аудита беспроводной безопасности. Но он имеет ограничение: встроенное радио работает только на **2,4 GHz**. К 2026 году большинство сетей перешли на 5 GHz.

{{< tldr >}}
AWUS036ACM с чипсетом MT7612U, MK7 Firmware 2.x предустанавливает драйвер, после подключения определяется как интерфейс wlan3, поддерживает 5 ГГц режим монитора, инъекцию пакетов и расширение PineAP, настройка за 10 минут.
{{< /tldr >}}

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

{{< faq >}}

## 5. Рекомендация

**ALFA AWUS036ACM — лучший доступный адаптер для расширения WiFi Pineapple Mark VII до 5 GHz.**

👉 [Страница продукта AWUS036ACM](/ru/products/alfa/awus036acm/)

*Нужна помощь? Свяжитесь с поддержкой Yupitek: [yupitek.com/support](/ru/support/)*


## Источники

1. [Официальная документация Hak5 — список совместимых адаптеров 802.11ac](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [Репозиторий драйвера OpenWrt mt76 — GitHub](https://github.com/openwrt/mt76)
3. [Официальный сайт aircrack-ng](https://www.aircrack-ng.org/)
4. [Официальный сайт ALFA Network — характеристики AWUS036ACM](https://www.alfa.com.tw/)
5. [Linux Wireless — документация драйвера MT76x2U](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
