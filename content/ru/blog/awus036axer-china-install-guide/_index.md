---
title: "Руководство по установке драйвера ALFA AWUS036AXER для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036AXER в Китае с использованием внутренних зеркал. Драйвер RTL8832BU, нано-адаптер WiFi 6. Охватывает Kali Linux, Ubuntu 22/24 (в ядре на 24.04), Debian и Raspberry Pi. GitHub не требуется."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
related_product: "/ru/products/alfa/awus036axer/"
---

AWUS036AXER — это нано-адаптер WiFi 6 от ALFA, компактный донгл, предназначенный для постоянного подключения к ноутбуку. Его чип RTL8832BU находится вне ядра в версиях Linux ниже 6.14, но включен нативно в Ubuntu 24.04 (ядро 6.8). В этом руководстве используются зеркала Gitee для старых ядер. GitHub не требуется.

> **Примечание для исследователей безопасности:** RTL8832BU имеет ограниченную поддержку режима монитора. Результаты зависят от версии ядра и драйвера. Для надежной инъекции пакетов в Kali Linux лучше выбрать [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/) или [AWUS036ACH](/ru/blog/awus036ach-china-install-guide/).

> **Примечание о дальности:** AWUS036AXER имеет встроенную несъемную антенну. Для исследований безопасности адаптеры с внешними антеннами RP-SMA (AWUS036ACH, AWUS036ACM) обеспечивают значительно лучшую дальность.

## Перед началом работы

1. Адаптер **ALFA AWUS036AXER**
2. Кабель USB-A
3. Активное интернет-соединение

```bash
lsusb
```

Ищите:

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

### Шаг 1: Переключитесь на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Шаг 2: Установите зависимости для сборки

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Шаг 3: Клонируйте драйвер из Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **ПРИМЕЧАНИЕ:** Если этот URL-адрес Gitee не загружается, выполните поиск на Gitee по запросу `rtl8852bu` и выберите самый последний обновленный форк. Вы также можете скачать архивы с [files.alfa.com.tw](https://files.alfa.com.tw).

### Шаг 4: Скомпилируйте и установите

```bash
sudo ./install-driver.sh
sudo reboot
```

Проверьте, загружен ли драйвер:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Шаг 5: Включите режим монитора {#enable-monitor-mode}

> **Примечание:** Поддержка режима монитора на RTL8832BU ограничена. Следующие команды работают на большинстве систем, но результаты могут отличаться.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Шаг 6: Протестируйте инъекцию пакетов {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Если инъекция нестабильна, рассмотрите [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/) для работ по тестированию на проникновение.

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

Если модуль загрузился и интерфейс появился, все готово. Переходите к шагам режима монитора выше.

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

Включите режим монитора так же, как в шагах для Kali выше.

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

## Проброс USB в виртуальную машину {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Настройки → USB** → Включите **USB 3.0 (xHCI)**.
2. Добавьте фильтр: **Realtek** (ID: 0bda:885a).
3. Запустите ВМ → `lsusb` для подтверждения → следуйте шагам для Kali.

### VMware

1. **Виртуальная машина → USB и Bluetooth** → Найдите **Realtek RTL8832BU** → **Подключить**.
2. `lsusb` для подтверждения → следуйте шагам для Kali.

---

## Устранение неполадок

| Проблема | Возможная причина | Решение |
|----------|-------------------|---------|
| `lsusb` не показывает 0bda:885a | Адаптер не обнаружен | Попробуйте другой USB-порт |
| `install-driver.sh` завершается с ошибкой | Отсутствуют заголовки | `sudo apt install linux-headers-$(uname -r)` |
| Ошибка клонирования Gitee | Проблема с сетью | Поиск на gitee.com по запросу `rtl8852bu` |
| Ubuntu 24.04: `modprobe 88x2bu` ошибка | Модуль отсутствует | Установите `linux-modules-extra-$(uname -r)` |
| Режим монитора нестабилен | Ограничение RTL8832BU | Используйте AWUS036ACM для пентеста |

> **Примечание о VIF:** Драйвер RTL8832BU вне ядра не поддерживает виртуальные интерфейсы (VIF).

## Справочник зеркал в Китае

| Ресурс | URL | Использовать для |
|--------|-----|------------------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Драйвер RTL8832BU |
| Зеркало Цинхуа | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Зеркало Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Зеркало USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Зеркало Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## Другие руководства по адаптерам Alfa для Китая

- [Руководство по установке AWUS036ACH в Китае](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- [Руководство по установке AWUS036ACM в Китае](/ru/blog/awus036acm-china-install-guide/) — MT7612U, полный VIF
- [Руководство по установке AWUS036ACS в Китае](/ru/blog/awus036acs-china-install-guide/) — RTL8811AU, режим монитора
- [Руководство по установке AWUS036AX в Китае](/ru/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← вы здесь
- [Руководство по установке AWUS036AXM в Китае](/ru/blog/awus036axm-china-install-guide/) — MT7921AUN, L-образный
- [Руководство по установке AWUS036AXML в Китае](/ru/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Руководство по установке AWUS036EACS в Китае](/ru/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Вопросы? Оставьте комментарий ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).
