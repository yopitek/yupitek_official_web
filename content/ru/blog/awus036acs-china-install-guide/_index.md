---
title: "Руководство по установке драйверов ALFA AWUS036ACS для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036ACS в Китае с использованием внутренних зеркал. Драйвер RTL8811AU DKMS, полная поддержка режима монитора и инъекции пакетов. Охватывает Kali Linux, Ubuntu 22/24, Debian и Raspberry Pi. GitHub не требуется."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Руководства по драйверам"]
series: ["alfa-china-install-guide"]
related_product: "/ru/products/alfa/awus036acs/"
series_order: 3
---

AWUS036ACS — это компактный двухдиапазонный адаптер ALFA для исследований в области безопасности. Его чип RTL8811AU поддерживает полноценный режим монитора и инъекцию пакетов в Kali Linux, но так как драйвер не входит в состав ядра, его необходимо скомпилировать из исходного кода. В Китае доступ к GitHub заблокирован, поэтому данное руководство использует исключительно зеркала Gitee. GitHub не требуется.

## Перед началом работы

Убедитесь, что у вас готовы:

1. Адаптер **ALFA AWUS036ACS**
2. USB-кабель (USB-A 2.0, тот, что в коробке, отлично подходит)
3. Активное интернет-соединение для доступа к внутренним зеркалам

Подключите адаптер и убедитесь, что система его видит:

```bash
lsusb
```

Ищите в выводе следующую строку:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

Если вы видите `0bda:0811`, адаптер обнаружен. Переходите к разделу для вашей ОС ниже.

## Выберите вашу операционную систему

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Уже установили? Переходите к:

- [Включение режима монитора](#включение-режима-монитора)
- [Тестирование инъекции пакетов](#тестирование-инъекции-пакетов)
- [Проброс USB в виртуальную машину](#проброс-usb-в-виртуальную-машину)

---

## Kali Linux

### Шаг 1: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

Удалите все содержимое и вставьте:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните с помощью **Ctrl+O**, Enter, затем **Ctrl+X**. Обновите список пакетов:

```bash
sudo apt update
```

> **Резервное зеркало:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Шаг 2: Установка зависимостей для сборки

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Шаг 3: Клонирование драйвера из Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **ПРИМЕЧАНИЕ:** Если URL-адрес Gitee не загружается, выполните поиск в Gitee по запросу `8821au` и выберите наиболее свежий форк. Вы также можете скачать архивы драйверов с [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Шаг 4: Компиляция и установка

```bash
sudo ./install-driver.sh
sudo reboot
```

После перезагрузки проверьте, загрузился ли драйвер.

```bash
lsmod | grep 88XXau
```

Вы должны увидеть модуль `88XXau` в списке. Затем подтвердите появление интерфейса.

```bash
iwconfig
```

Ищите `wlan0` или `wlan1`.

---

### Шаг 5: Включение режима монитора {#включение-режима-монитора}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Проверьте с помощью `iwconfig` — ищите `wlan1mon` с `Mode:Monitor`.

---

### Шаг 6: Тестирование инъекции пакетов {#тестирование-инъекции-пакетов}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Шаг 1: Переключение на китайское зеркало

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Удалите все и вставьте:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Замените все строки на:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Шаг 2: Установка зависимостей для сборки

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Шаг 3: Клонирование и установка драйвера из Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Шаг 4: Включение режима монитора

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Шаг 5: Тестирование инъекции пакетов

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Шаг 1: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

Вставьте (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Шаг 2: Установка зависимостей для сборки

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Шаг 3: Клонирование и установка

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Шаг 4: Включение режима монитора

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Подтверждение: `iwconfig` → ищите `wlan1mon` с `Mode:Monitor`.

### Шаг 5: Тестирование инъекции пакетов

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Шаг 1: Загрузка и прошивка Kali ARM64

Официальный сайт: https://www.kali.org/get-kali/#kali-arm — выберите Raspberry Pi 4/5 64-bit.

Китайское зеркало: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Данные для входа по умолчанию: **kali / kali**.

### Шаг 2: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Шаг 3: Установка зависимостей для сборки

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Шаг 4: Клонирование и установка драйвера

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Шаг 5: Включение режима монитора

На Pi со встроенным Wi-Fi адаптер AWUS036ACS обычно отображается как `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Шаг 6: Тестирование инъекции пакетов

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Проброс USB в виртуальную машину {#проброс-usb-в-виртуальную-машину}

### VirtualBox

1. Выключите ВМ → **Настройки (Settings) → USB** → Включите **USB 2.0 Controller**.
2. Нажмите **+** → Выберите: **Realtek** (ID: 0bda:0811).
3. Запустите ВМ. Выполните `lsusb`, чтобы подтвердить наличие `0bda:0811`, затем следуйте шагам для Kali выше.

### VMware Fusion / Workstation

1. **Virtual Machine → USB & Bluetooth** → Найдите **Realtek 8811AU** → **Connect**.
2. Выполните `lsusb` для подтверждения, затем следуйте шагам для Kali выше.

---

## Устранение неполадок

| Проблема | Вероятная причина | Решение |
|----------|-------------------|---------|
| `lsusb` не показывает 0bda:0811 | Нет питания или плохой кабель | Попробуйте другой USB-порт |
| `install-driver.sh` завершается ошибкой | Отсутствуют заголовки ядра | Выполните `sudo apt install linux-headers-$(uname -r)` |
| Ошибка клонирования из Gitee | Проблема с сетью | Поищите `8821au` на gitee.com, попробуйте другой форк |
| Ошибка `airmon-ng start` | Запущен NetworkManager | Сначала выполните `sudo airmon-ng check kill` |
| Нет трафика в режиме монитора | Неверный канал | Установите канал: `iwconfig wlan1mon channel 6` |
| Ошибка инъекции "No Answer" | Точка доступа слишком далеко | Подойдите ближе. Используйте `wlan1mon`, а не `wlan1`. |

> **Примечание о VIF:** Драйвер RTL8811AU не поддерживает виртуальные интерфейсы (VIF). Одновременная работа в режиме монитора и управляемом режиме на этом адаптере недоступна.

## Список китайских зеркал

| Ресурс | URL | Для чего использовать |
|----------|-----|----------------------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| Документация Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Руководства пользователя |
| Драйвер 8821au (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | Драйвер RTL8811AU |
| Зеркало Tsinghua University | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Зеркало Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (рекомендуется) |
| Зеркало USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (рекомендуется) |
| Зеркало Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Образы Kali ARM |

## Другие руководства по адаптерам Alfa для Китая

- [Руководство по установке AWUS036ACH в Китае](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- [Руководство по установке AWUS036ACM в Китае](/ru/blog/awus036acm-china-install-guide/) — MT7612U, полная поддержка VIF
- AWUS036ACS ← вы находитесь здесь
- [Руководство по установке AWUS036AX в Китае](/ru/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [Руководство по установке AWUS036AXER в Китае](/ru/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Руководство по установке AWUS036AXM в Китае](/ru/blog/awus036axm-china-install-guide/) — MT7921AUN, L-образный
- [Руководство по установке AWUS036AXML в Китае](/ru/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Руководство по установке AWUS036EACS в Китае](/ru/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Вопросы? Оставляйте комментарии ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).
