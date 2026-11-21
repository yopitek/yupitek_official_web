---
title: "Руководство по установке драйвера ALFA AWUS036AXER для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036AXER в Китае с использованием внутренних зеркал. Драйвер RTL8832BU, нано-адаптер WiFi 6. Охватывает Kali Linux, Ubuntu 22/24 (DKMS), Debian и Raspberry Pi."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/ru/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽

faq:
  - question: "Какой чип используется в AWUS036AXER? Такой же, как в AWUS036AX?"
    answer: "Тот же чип Realtek RTL8832BU, поддерживает WiFi 6, но корпус меньше и портативнее."
  - question: "Нужно ли устанавливать драйвер AWUS036AXER в Ubuntu 24.04?"
    answer: "Это зависит от ядра. Linux kernel 6.17 и новее (например, Ubuntu 24.04 HWE / kernel 6.17) поставляется со встроенным в ядро драйвером rtw89_8852bu — plug-and-play, без DKMS. Только на ядрах старше 6.17 нужно один раз собрать community-драйвер rtl8852bu (morrownr/rtl8852bu-20250826) через DKMS. Сначала проверьте командой uname -r."
  - question: "Подходит ли AWUS036AXER для исследований беспроводной безопасности?"
    answer: "Да. Со встроенным в ядро драйвером rtw89_8852bu на kernel 6.17+ в наших тестах работают и режим монитора, и инъекция пакетов (Ubuntu 24.04 / kernel 6.17: инъекция 73% на 2.4GHz и сквозной захват WPA .22000). Примечание: на старых ядрах при использовании community-драйвера DKMS поддержка режима монитора может быть ограничена. Только в сетях, которыми вы владеете или которые вам разрешено тестировать."
  - question: "Какой USB ID у AWUS036AXER?"
    answer: "Vendor ID Realtek RTL8832BU — 0bda. Product ID — 8832 или 885a в зависимости от экземпляра; подтвердите его командой lsusb."
  - question: "Нужен ли VPN для установки AWUS036AXER в Китае?"
    answer: "Не обязательно. Клонируйте драйвер из проверенного репозитория GitHub (morrownr/rtl8852bu-20250826); если GitHub работает медленно, используйте надёжный прокси или зеркало. Инструменты сборки по-прежнему можно установить из внутренних зеркал."
---

AWUS036AXER — это нано-адаптер WiFi 6 от ALFA, компактный донгл, предназначенный для постоянного подключения к ноутбуку. Чип RTL8832BU поддерживается **встроенным в ядро драйвером rtw89_8852bu на Linux kernel 6.17 и новее** (например, Ubuntu 24.04 HWE / kernel 6.17) — plug-and-play, без компиляции. Только на **старых ядрах** (ниже 6.17) нужно один раз собрать community-драйвер rtl8852bu через DKMS. В этом руководстве рассмотрены оба варианта. Исходный код драйвера клонируется из проверенного репозитория GitHub; если GitHub работает медленно, используйте надёжный прокси или зеркало.

{{< tldr >}}
AWUS036AXER использует чипсет RTL8832BU с WiFi 6. Kernel 6.17+ (включая Ubuntu 24.04 / kernel 6.17) имеет встроенный в ядро драйвер rtw89_8852bu — без DKMS, при этом в тестах работают режим монитора и инъекция. Старым ядрам нужен community-драйвер rtl8852bu через DKMS.
{{< /tldr >}}

> **Примечание для исследователей безопасности:** Со **встроенным в ядро драйвером rtw89_8852bu на kernel 6.17+** режим монитора и инъекция пакетов AWUS036AXER работают в тестах (Ubuntu 24.04 / kernel 6.17: инъекция 73% на 2.4GHz, сквозной захват WPA .22000). Только на старых ядрах при использовании community-драйвера DKMS поддержка режима монитора ограничена. Сначала проверьте `uname -r`. Только в сетях, которыми вы владеете или которые вам разрешено тестировать.

> **Примечание о дальности:** AWUS036AXER имеет встроенную несъемную антенну. Для исследований безопасности адаптеры с внешними антеннами RP-SMA (AWUS036ACH, AWUS036ACM) обеспечивают значительно лучшую дальность.

## Перед началом работы

1. Адаптер **ALFA AWUS036AXER**
2. Кабель USB-A
3. Активное интернет-соединение

```bash
lsusb
```

Ищите строку, похожую на эту (пример вывода; Vendor ID всегда `0bda`, а Product ID — `8832` или `885a` в зависимости от экземпляра):

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

### Шаг 3: Клонируйте драйвер из GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **ПРИМЕЧАНИЕ:** Поддерживаемый основной драйвер — [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Если GitHub работает медленно, используйте надёжный прокси или зеркало. Архивы также можно скачать с [files.alfa.com.tw](https://files.alfa.com.tw).

### Шаг 4: Скомпилируйте и установите

```bash
sudo ./install-driver.sh
sudo reboot
```

Проверьте, загружен ли драйвер:

```bash
lsmod | grep 8852bu
iwconfig
```

### Шаг 5: Включите режим монитора {#enable-monitor-mode}

> **Работает на kernel 6.17+:** Со встроенным в ядро драйвером rtw89_8852bu режим монитора работает:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> На старых ядрах при использовании community-драйвера DKMS поддержка режима монитора может быть ограничена — там можно переключиться на адаптер со встроенным в ядро драйвером MediaTek, например [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/).

### Шаг 6: Протестируйте инъекцию пакетов {#test-packet-injection}

> **Работает на kernel 6.17+:** После перехода в режим монитора протестируйте инъекцию с помощью aireplay-ng (73% на 2.4GHz в тестах):
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Только в сетях, которыми вы владеете или которые вам разрешено тестировать. На старых ядрах, где community-драйвер DKMS не поддерживает режим монитора, инъекция также недоступна.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

В Ubuntu 24.04 встроенный в ядро драйвер rtw89_8852bu есть только в **ядре HWE 6.17 и новее** (например, HWE из 24.04.4) — просто подключите адаптер, сборка не нужна. На **ядре GA 6.8** или **ядре HWE 6.14** (ни одно из них не содержит этот драйвер) переключитесь на внутреннее зеркало и соберите community-драйвер так же, как для Ubuntu 22.04 ниже, или обновитесь до ядра HWE 6.17 и новее, чтобы получить встроенный драйвер.

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
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

После перезагрузки выполните `sudo modprobe 8852bu` и `iwconfig`. Если модуль загрузился и появился интерфейс, всё готово. Это путь community-драйвера DKMS для старого ядра (ниже 6.17), где поддержка режима монитора может быть ограничена; на kernel 6.17+ используется встроенный в ядро драйвер rtw89_8852bu, с которым режим монитора и инъекция работают.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Этот community-драйвер DKMS используется на ядрах старше 6.17, и режим монитора им может не поддерживаться (см. шаг 5 для Kali). На kernel 6.17+ встроенный в ядро драйвер rtw89_8852bu обеспечивает работу режима монитора и инъекции.

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Проброс USB в виртуальную машину {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Настройки → USB** → Включите **USB 3.0 (xHCI)**.
2. Добавьте фильтр: **Realtek** (Vendor ID: 0bda, Product ID: 8832 или 885a).
3. Запустите ВМ → `lsusb` для подтверждения → следуйте шагам для Kali.

### VMware

1. **Виртуальная машина → USB и Bluetooth** → Найдите **Realtek RTL8832BU** → **Подключить**.
2. `lsusb` для подтверждения → следуйте шагам для Kali.

---

{{< faq >}}

## Устранение неполадок

| Проблема | Возможная причина | Решение |
|----------|-------------------|---------|
| `lsusb` не показывает 0bda:8832 или 0bda:885a | Адаптер не обнаружен | Попробуйте другой USB-порт |
| `install-driver.sh` завершается с ошибкой | Отсутствуют заголовки | `sudo apt install linux-headers-$(uname -r)` |
| Ошибка или медленное клонирование с GitHub | Проблема с сетью | Используйте надёжный прокси или зеркало |
| `modprobe 8852bu` завершается ошибкой | Драйвер не собран или не загружен | Повторно запустите `sudo ./install-driver.sh`, проверьте `sudo dkms status`, затем перезагрузитесь |
| Режим монитора / инъекция не работает | Ядро старше 6.17 с DKMS-драйвером rtl8852bu от сообщества (режим монитора может быть ограничен) | Проверьте `uname -r`; используйте kernel 6.17+ (встроенный rtw89_8852bu) или AWUS036ACM на старых ядрах |

> **Примечание о VIF:** Драйвер RTL8832BU вне ядра не поддерживает виртуальные интерфейсы (VIF).

## Справочник зеркал в Китае

| Ресурс | URL | Использовать для |
|--------|-----|------------------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Драйвер RTL8832BU |
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


## Источники

1. [Официальный сайт Realtek](https://www.realtek.com/)
2. [Официальный сайт ALFA Network](https://www.alfa.com.tw/)
3. [Официальная документация Kali Linux](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
