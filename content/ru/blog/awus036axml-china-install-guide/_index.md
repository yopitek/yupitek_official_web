---
title: "Руководство по установке драйвера ALFA AWUS036AXML для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036AXML в Китае с использованием локальных зеркал. Драйвер MT7921AUN WiFi 6E в ядре, полная поддержка режима мониторинга и VIF. Охватывает Kali Linux, Ubuntu 22/24, Debian и Raspberry Pi. GitHub не требуется."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Руководства по драйверам"]
series: ["alfa-china-install-guide"]
related_product: "/ru/products/alfa/awus036axml/"
series_order: 7
featureimage: "/images/blog/awus036axml-china-install-guide.webp"

faq:
  - question: "Какой чип используется в AWUS036AXML? Такой же, как в AWUS036AXM?"
    answer: "Тот же чип MediaTek MT7921AUN, но AWUS036AXML — флагманская версия с интерфейсом USB-C."
  - question: "Нужно ли вручную устанавливать драйвер AWUS036AXML?"
    answer: "Нет, драйвер mt7921u встроен в ядро с версии 5.18, нужно только установить пакет прошивки."
  - question: "Поддерживает ли AWUS036AXML VIF-виртуальные интерфейсы?"
    answer: "Да, MT7921AUN полностью поддерживает нативный VIF ядра, может одновременно работать в режиме монитора и управляемом режиме."
  - question: "Почему драйвер не загружается в Ubuntu 22.04?"
    answer: "Ядро 5.15 по умолчанию в Ubuntu 22.04 слишком старое, нужно установить HWE-ядро и обновиться до 5.18+."
  - question: "Какой USB ID у AWUS036AXML?"
    answer: "USB ID MediaTek MT7921AUN — 0e8d:7961, можно проверить через lsusb."
---

AWUS036AXML — это флагманская модель WiFi 6E от ALFA, трехдиапазонный USB-C адаптер, поддерживающий 2,4 ГГц, 5 ГГц и свободный от помех диапазон 6 ГГц. Его чип MT7921AUN использует драйвер `mt7921u`, встроенный в ядро Linux начиная с версии 5.18. В Ubuntu 24.04 и Kali 2025 он работает по принципу plug-and-play сразу после установки пакета прошивки с локального зеркала. Это руководство охватывает полную настройку — прошивку, проверку драйвера, режим мониторинга, инъекцию пакетов и VIF — без использования GitHub.

{{< tldr >}}
AWUS036AXML с чипом MT7921AUN, WiFi 6E трёхдиапазонный USB-C флагман. Драйвер встроен в ядро, после установки прошивки доступны режим монитора, инъекция пакетов и VIF.
{{< /tldr >}}

Убедитесь, что у вас есть:


## Перед началом работы

Убедитесь, что у вас есть:

1. Адаптер **ALFA AWUS036AXML** и кабель USB-C
2. USB-хаб с внешним питанием (обязательно для Raspberry Pi)
3. Активное интернет-соединение для доступа к локальным зеркалам

Подключите адаптер и убедитесь, что система его видит:

```bash
lsusb
```

Найдите в выводе следующую строку:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

Если вы видите `0e8d:7961`, адаптер обнаружен. Переходите к разделу для вашей ОС ниже.

## Выберите вашу операционную систему

Перейдите к соответствующему разделу:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

Драйвер MT7921AUN уже есть в ядре Kali. Вам понадобится только пакет прошивки MediaTek, доступный на локальных зеркалах.

### Шаг 1: Переключение на китайское зеркало

Откройте список источников в терминале.

```bash
sudo nano /etc/apt/sources.list
```

Удалите все содержимое и вставьте эту строку:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните: нажмите **Ctrl+O**, затем Enter, и Ctrl+X для выхода. Обновите индекс пакетов.

```bash
sudo apt update
```

---

### Шаг 2: Установка прошивки

Для работы MT7921AUN требуются файлы прошивки из `firmware-misc-nonfree` и `linux-firmware`.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Шаг 3: Проверка драйвера

После перезагрузки подключите адаптер и проверьте.

```bash
lsmod | grep mt7921
```

Вы должны увидеть `mt7921u` в выводе. Затем убедитесь, что появился беспроводной интерфейс.

```bash
iwconfig
```

Ищите `wlan0` или `wlan1`.

---

### Шаг 4: Включение режима мониторинга {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

Найдите `Mode:Monitor` на интерфейсе.

---

### Шаг 5: Тестирование инъекции пакетов {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

При успешном результате вы увидите: `Injection is working!`.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — ядро 6.8, Plug-and-Play

Ubuntu 24.04 включает драйвер по умолчанию.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Переключитесь на зеркала Aliyun:
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

Переключитесь на зеркало Tsinghua:

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

{{< faq >}}

## Поиск и устранение неисправностей

| Проблема | Возможная причина | Решение |
|---------|-------------|-----|
| `lsusb` не показывает 0e8d:7961 | Недостаточно питания | Попробуйте другой порт или хаб с питанием |

## Справочник китайских зеркал

| Ресурс | URL | Для чего использовать |
|----------|-----|---------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| Зеркало Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

## Другие руководства по адаптерам Alfa для Китая

- [AWUS036ACH China Install Guide](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- AWUS036AXML ← вы здесь

Есть вопросы? Оставьте комментарий ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).


## Источники

1. [Драйвер Linux Kernel mt7921](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Официальная документация aircrack-ng](https://www.aircrack-ng.org/)
3. [Официальный сайт ALFA Network](https://www.alfa.com.tw/)
4. [Официальная документация Kali Linux](https://www.kali.org/docs/)
