---
title: "Руководство по установке драйверов ALFA AWUS036AX для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036AX в Китае с использованием внутренних зеркал. Драйвер RTL8832BU, WiFi 6 AX1800. Охватывает Kali Linux, Ubuntu 22/24 (DKMS), Debian и Raspberry Pi."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
related_product: "/ru/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"

faq:
  - question: "Какой чип используется в AWUS036AX? Поддерживает ли WiFi 6?"
    answer: "Чип Realtek RTL8832BU, поддерживает WiFi 6 (802.11ax) высокоскоростную сеть."
  - question: "Нужно ли устанавливать драйвер AWUS036AX в Ubuntu 24.04?"
    answer: "Да. RTL8832BU нет в ядре Ubuntu 24.04. Один раз соберите community-драйвер rtl8852bu (morrownr/rtl8852bu-20250826) через DKMS; затем он автоматически пересобирается при обновлении ядра."
  - question: "Подходит ли AWUS036AX для исследований беспроводной безопасности?"
    answer: "Нет. Community-драйвер rtl8852bu не поддерживает режим монитора и инъекцию пакетов. Используйте вместо него адаптер со встроенным в ядро драйвером MediaTek, например AWUS036ACM."
  - question: "Нужен ли VPN для установки AWUS036AX в Китае?"
    answer: "Не обязательно. Клонируйте драйвер из проверенного репозитория GitHub (morrownr/rtl8852bu-20250826); если GitHub работает медленно, используйте надёжный прокси или зеркало. Инструменты сборки по-прежнему можно установить из внутренних зеркал."
  - question: "Какой USB ID у AWUS036AX?"
    answer: "Vendor ID Realtek RTL8832BU — 0bda. Product ID — 8832 или 885a в зависимости от экземпляра; подтвердите его командой lsusb."
---

AWUS036AX — это двухдиапазонный адаптер ALFA WiFi 6 AX1800. У чипа RTL8832BU адаптера AWUS036AX нет драйвера в ядре Linux, поэтому в любом дистрибутиве (включая Ubuntu 24.04) нужно один раз собрать community-драйвер rtl8852bu через DKMS. Исходный код драйвера клонируется из проверенного репозитория GitHub; если GitHub работает медленно, используйте надёжный прокси или зеркало. Этот драйвер не поддерживает режим монитора.

{{< tldr >}}
AWUS036AX использует чипсет RTL8832BU с WiFi 6. Драйвера в ядре нет: в любом дистрибутиве (включая Ubuntu 24.04) rtl8852bu нужно собрать через DKMS. Режим монитора не поддерживается.
{{< /tldr >}}

> **Примечание для исследователей безопасности:** Community-драйвер rtl8852bu не поддерживает режим монитора и инъекцию пакетов. Для исследований безопасности используйте адаптер со встроенным в ядро драйвером MediaTek, например [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/).

## Перед началом работы

1. Адаптер **ALFA AWUS036AX**
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

### Шаг 3: Клонирование драйвера из GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **ПРИМЕЧАНИЕ:** Поддерживаемый основной драйвер — [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Если GitHub работает медленно, используйте надёжный прокси или зеркало. Архивы также можно скачать с [files.alfa.com.tw](https://files.alfa.com.tw).

### Шаг 4: Компиляция и установка

```bash
sudo ./install-driver.sh
sudo reboot
```

Проверьте загрузку драйвера:

```bash
lsmod | grep 8852bu
iwconfig
```

### Шаг 5: Включение режима монитора {#enable-monitor-mode}

> **Не поддерживается:** Community-драйвер rtl8852bu для RTL8832BU не поддерживает режим монитора, поэтому команд для выполнения здесь нет. Если нужен режим монитора, используйте адаптер со встроенным в ядро драйвером MediaTek, например [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/).

### Шаг 6: Тестирование инъекции пакетов {#test-packet-injection}

> **Не поддерживается:** Инъекция пакетов зависит от режима монитора, которого этот драйвер не предоставляет. Для тестов инъекции используйте [AWUS036ACM](/ru/blog/awus036acm-china-install-guide/).

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — требуется DKMS

В Ubuntu 24.04 (ядро 6.8) нет драйвера для RTL8832BU. Переключитесь на внутреннее зеркало и соберите драйвер так же, как для Ubuntu 22.04 ниже.

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

После перезагрузки выполните `sudo modprobe 8852bu` и `iwconfig`. Если модуль загрузился и появился интерфейс, всё готово (только управляемый режим; режим монитора не поддерживается).

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

Режим монитора этим драйвером не поддерживается (см. шаг 5 для Kali).

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

| Проблема | Вероятная причина | Решение |
|----------|-------------------|---------|
| `lsusb` не показывает 0bda:8832 или 0bda:885a | Адаптер не обнаружен | Попробуйте другой USB-порт |
| Ошибка `install-driver.sh` | Отсутствуют заголовки ядра | `sudo apt install linux-headers-$(uname -r)` |
| Ошибка или медленное клонирование с GitHub | Проблема с сетью | Используйте надёжный прокси или зеркало |
| `modprobe 8852bu` завершается ошибкой | Драйвер не собран или не загружен | Повторно запустите `sudo ./install-driver.sh`, проверьте `sudo dkms status`, затем перезагрузитесь |
| Режим монитора / инъекция не работает | Не поддерживается драйвером rtl8852bu | Используйте AWUS036ACM для задач пентеста |

> **Примечание о VIF:** Драйвер RTL8832BU (out-of-kernel) не поддерживает виртуальные интерфейсы (VIF).

## Список китайских зеркал

| Ресурс | URL | Для чего использовать |
|----------|-----|----------------------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Драйвер RTL8832BU |
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
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
