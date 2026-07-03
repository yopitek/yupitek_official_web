---
title: "Руководство по установке драйверов ALFA AWUS036AX для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036AX в Китае с использованием внутренних зеркал. Драйвер RTL8832BU, WiFi 6 AX1800. Охватывает Kali Linux, Ubuntu 22/24 (входит в ядро 24.04), Debian и Raspberry Pi. GitHub не требуется."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Руководства по драйверам"]
series: ["alfa-china-install-guide"]
related_product: "/ru/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"

faq:
  - question: "Какой чип используется в AWUS036AX? Поддерживает ли WiFi 6?"
    answer: "Чип Realtek RTL8832BU, поддерживает WiFi 6 (802.11ax) высокоскоростную сеть."
  - question: "Нужно ли устанавливать драйвер AWUS036AX в Ubuntu 24.04?"
    answer: "Нет, ядро Ubuntu 24.04 нативно поддерживает RTL8832BU, Plug & Play."
  - question: "Подходит ли AWUS036AX для исследований беспроводной безопасности?"
    answer: "Менее подходит, поддержка режима монитора у RTL8832BU ограничена, рекомендуется AWUS036ACM или AWUS036ACH."
  - question: "Нужен ли VPN для установки AWUS036AX в Китае?"
    answer: "Нет, скачайте исходный код rtl8852bu с Gitee и используйте внутренние зеркала для установки инструментов компиляции."
  - question: "Какой USB ID у AWUS036AX?"
    answer: "USB ID Realtek RTL8832BU — 0bda:8832, можно проверить через lsusb."
---

AWUS036AX — это двухдиапазонный адаптер ALFA WiFi 6 AX1800. Его чип RTL8832BU не поддерживается ядром в версиях Linux ниже 6.14, но в Ubuntu 24.04 (ядро 6.8) он уже встроен. В этом руководстве используются зеркала Gitee для более старых ядер и встроенный драйвер для Ubuntu 24.04. GitHub не требуется.

{{< tldr >}}
AWUS036AX с чипом RTL8832BU поддерживает WiFi 6. В Ubuntu 24.04 работает без драйвера, в Kali/Ubuntu 22.04 компилируется из Gitee rtl8852bu.
{{< /tldr >}}

> **Заметка для исследователей безопасности:** RTL8832BU имеет ограниченную поддержку режима монитора. Результаты зависят от версии ядра и драйвера. Для надежной инъекции пакетов в Kali Linux лучше выбрать [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/) или [AWUS036ACH](/ru/blog/awus036ach-china-install-guide/).

## Перед началом работы

1. Адаптер **ALFA AWUS036AX**
2. Кабель USB-A
3. Активное интернет-соединение

```bash
lsusb
```

Ищите строку:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Выберите вашу операционную систему

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### Шаг 1: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Шаг 2: Установка зависимостей для сборки

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Шаг 3: Клонирование драйвера из Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **ПРИМЕЧАНИЕ:** Если URL-адрес Gitee не загружается, выполните поиск в Gitee по запросу `rtl8852bu` и выберите наиболее свежий форк. Вы также можете скачать архивы с [files.alfa.com.tw](https://files.alfa.com.tw).

### Шаг 4: Компиляция и установка

```bash
sudo ./install-driver.sh
sudo reboot
```

Проверьте загрузку драйвера:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Шаг 5: Включение режима монитора {#включение-режима-монитора}

> **Примечание:** Поддержка режима монитора в RTL8832BU ограничена. Следующие команды работают в большинстве случаев, но результаты могут отличаться.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Шаг 6: Тестирование инъекции пакетов {#тестирование-инъекции-пакетов}

```bash
sudo aireplay-ng --test wlan1
```

Если инъекция работает нестабильно, рассмотрите возможность использования [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/) для задач тестирования на проникновение.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — драйвер в ядре, Gitee не требуется

Ubuntu 24.04 поставляется с ядром 6.8, которое включает драйвер RTL8832BU нативно.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

Если модуль загрузился и интерфейс появился, значит все готово. Переходите к шагам по включению режима монитора выше.

---

### Ubuntu 22.04 (Jammy) — требуется DKMS

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Включите режим монитора, следуя тем же шагам, что и для Kali выше.

---

## Raspberry Pi 4B / 5

Сначала переключитесь на китайское зеркало:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Проброс USB в виртуальную машину {#проброс-usb-в-виртуальную-машину}

### VirtualBox

1. **Settings → USB** → Включите **USB 3.0 (xHCI)**.
2. Добавьте фильтр: **Realtek** (ID: 0bda:885a).
3. Запустите ВМ → `lsusb` для подтверждения → следуйте шагам для Kali.

### VMware

1. **Virtual Machine → USB & Bluetooth** → Найдите **Realtek RTL8832BU** → **Connect**.
2. `lsusb` для подтверждения → следуйте шагам для Kali.

---

{{< faq >}}

## Устранение неполадок

| Проблема | Вероятная причина | Решение |
|----------|-------------------|---------|
| `lsusb` не показывает 0bda:885a | Адаптер не обнаружен | Попробуйте другой USB-порт |
| Ошибка `install-driver.sh` | Отсутствуют заголовки ядра | `sudo apt install linux-headers-$(uname -r)` |
| Ошибка клонирования из Gitee | Проблема с сетью | Поищите `rtl8852bu` на gitee.com |
| Ubuntu 24.04: ошибка `modprobe 88x2bu` | Модуль отсутствует | Установите `linux-modules-extra-$(uname -r)` |
| Режим монитора работает нестабильно | Ограничение RTL8832BU | Используйте AWUS036ACM для пентеста |

> **Примечание о VIF:** Драйвер RTL8832BU (out-of-kernel) не поддерживает виртуальные интерфейсы (VIF).

## Список китайских зеркал

| Ресурс | URL | Для чего использовать |
|----------|-----|----------------------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Драйвер RTL8832BU |
| Зеркало Tsinghua University | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Зеркало Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Зеркало USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Зеркало Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## Другие руководства по адаптерам Alfa для Китая

- [Руководство по установке AWUS036ACH в Китае](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- [Руководство по установке AWUS036ACM в Китае](/ru/blog/awus036acm-china-install-guide/) — MT7612U, полная поддержка VIF
- [Руководство по установке AWUS036ACS в Китае](/ru/blog/awus036acs-china-install-guide/) — RTL8811AU, режим монитора
- AWUS036AX ← вы находитесь здесь
- [Руководство по установке AWUS036AXER в Китае](/ru/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Руководство по установке AWUS036AXM в Китае](/ru/blog/awus036axm-china-install-guide/) — MT7921AUN, L-образный
- [Руководство по установке AWUS036AXML в Китае](/ru/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Руководство по установке AWUS036EACS в Китае](/ru/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Вопросы? Оставляйте комментарии ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).


## Источники

1. [Официальный сайт Realtek](https://www.realtek.com/)
2. [Официальный сайт ALFA Network](https://www.alfa.com.tw/)
3. [Официальная документация Kali Linux](https://www.kali.org/docs/)
4. [Зеркало Gitee rtl8852bu](https://gitee.com/mirrors/rtl8852bu)
