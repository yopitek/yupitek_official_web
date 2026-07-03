---
title: "Руководство по установке драйвера ALFA AWUS036ACH для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйверов ALFA AWUS036ACH в Китае с использованием отечественных зеркал. Охватывает Kali Linux, Ubuntu 22/24, Debian и Raspberry Pi. GitHub не требуется."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "драйвер", "китай", "режим-монитора"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
related_product: "/ru/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"

faq:
  - question: "Какой чип используется в AWUS036ACH? Нужно ли устанавливать драйвер?"
    answer: "AWUS036ACH использует чип Realtek RTL8812AU, драйвер не встроен в ядро Linux, требует ручной установки."
  - question: "Нужен ли VPN для установки драйвера AWUS036ACH в Китае?"
    answer: "Нет, используются внутренние зеркала USTC, Alibaba Cloud и зеркала исходного кода Gitee для завершения установки."
  - question: "Поддерживает ли AWUS036ACH режим монитора и инъекцию пакетов?"
    answer: "Да, после установки драйвера RTL8812AU используйте airmon-ng для включения режима монитора, aireplay-ng для тестирования инъекции пакетов."
  - question: "Можно ли использовать AWUS036ACH на Raspberry Pi?"
    answer: "Да, рекомендуется использовать USB-хаб с питанием и установить Kali ARM64."
  - question: "Какая команда для установки драйвера AWUS036ACH в Kali Linux?"
    answer: "В Kali выполните sudo apt install realtek-rtl88xxau-dkms для установки предкомпилированного драйвера."
---

Вы только что получили AWUS036ACH, но Linux его не распознаёт. Это нормально — данный чип требует драйвер RTL8812AU, который не работает «из коробки». Это руководство проведёт вас через полную установку примерно за 30 минут, используя только отечественные зеркала. Доступ к GitHub не требуется.

{{< tldr >}}
AWUS036ACH использует чип RTL8812AU. В Kali драйвер DKMS устанавливается через apt, в Ubuntu/Debian компилируется из Gitee. 30 минут — и режим монитора с инъекцией пакетов готовы.
{{< /tldr >}}

Убедитесь, что у вас есть:


## Прежде чем начать

Убедитесь, что у вас есть:

1. Адаптер **ALFA AWUS036ACH**
2. USB-кабель (идёт в комплекте)
3. Питаемый USB-хаб — обязателен для Raspberry Pi
4. Активное подключение к интернету для доступа к отечественным зеркалам

Подключите адаптер, затем убедитесь, что система его видит:

```bash
lsusb
```

Найдите в выводе:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

Если вы видите `0bda:8812`, адаптер обнаружен. Переходите к разделу вашей ОС ниже.

Если не видите — попробуйте другой USB-порт или замените кабель, затем снова запустите `lsusb`.

## Выберите вашу операционную систему

Перейдите к нужному разделу:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Уже установлено? Перейдите к:

- [Включение режима монитора](#enable-monitor-mode)
- [Тест инъекции пакетов](#test-packet-injection)
- [Проброс USB в виртуальную машину](#virtual-machine-usb-passthrough)

---

## Kali Linux

В Kali уже встроены мощные инструменты для работы с беспроводными сетями. Для запуска драйвера AWUS036ACH нужно выполнить четыре шага. Начнём с переключения на быстрое китайское зеркало.

### Шаг 1: Переключение на зеркало в Китае

Откройте список источников в терминале.

```bash
sudo nano /etc/apt/sources.list
```

Удалите всё содержимое и вставьте эту строку:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните файл: нажмите **Ctrl+O**, затем Enter, затем Ctrl+X для выхода. Обновите индекс пакетов.

```bash
sudo apt update
```

> **Резервное зеркало:** Если 中科大 (USTC) работает медленно, используйте 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Шаг 2: Установка драйвера

В репозитории Kali есть готовый DKMS-пакет. Установите его одной командой.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS автоматически перекомпилирует драйвер при обновлении ядра — повторная установка не потребуется.

Проверьте, что драйвер загрузился корректно.

```bash
modinfo 88XXau | grep -E "filename|version"
```

Вы должны увидеть строку `filename`, заканчивающуюся на `.ko`, и строку `version` с номером вроде `5.6.4.2`. Если обе появились — драйвер готов.

---

### Шаг 2 (альтернатива): Сборка из исходников

Следуйте этому разделу только если команда `apt install` выше завершилась ошибкой. Сначала установите зависимости для сборки.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Скачайте исходники драйвера с Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **Примечание:** Если этот URL не загружается, найдите на Gitee `rtl8812au` и выберите форк с наиболее свежим коммитом. Также можно скачать архив с исходниками напрямую с [files.alfa.com.tw](https://files.alfa.com.tw).

Перейдите в скачанную директорию, затем скомпилируйте и установите.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Загрузите драйвер в работающее ядро.

```bash
sudo modprobe 88XXau
```

---

### Шаг 3: Включение режима монитора {#enable-monitor-mode}

Перед переключением адаптера в режим монитора проверьте, какое имя интерфейса назначила система.

```bash
iwconfig
```

Найдите запись `wlan0` или `wlan1`. Используйте это имя в командах ниже.

Остановите NetworkManager и wpa_supplicant — они будут конкурировать за доступ к адаптеру и заблокируют режим монитора.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Подтвердите переключение.

```bash
iwconfig
```

Найдите запись вроде `wlan0mon` с `Mode:Monitor`. Когда она появится — адаптер готов к перехвату пакетов.

---

### Шаг 4: Тест инъекции пакетов {#test-packet-injection}

Запустите тест инъекции на мониторном интерфейсе.

```bash
sudo aireplay-ng --test wlan0mon
```

Успешный результат выглядит так:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Если тест не прошёл, перезагрузите машину и повторите. Если после перезагрузки всё равно не работает — убедитесь, что другие процессы не захватили интерфейс. Запустите `iwconfig` и проверьте, что в нём отображается только `wlan0mon`.

---

## Ubuntu 22.04 / 24.04

Ubuntu разделяется на две ветки с разными форматами файлов пакетов. Инструкции ниже охватывают обе. Используйте **阿里云 (Aliyun)** в качестве зеркала — он быстрый, надёжный и поддерживается Alibaba.

### Шаг 1: Переключение на зеркало в Китае

Выберите вашу версию Ubuntu и следуйте только соответствующей инструкции.

#### Ubuntu 24.04 (Noble)

Откройте файл источников в формате DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Удалите всё содержимое файла и вставьте:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Сохраните с помощью `Ctrl+O`, затем выйдите с `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Откройте классический файл источников:

```bash
sudo nano /etc/apt/sources.list
```

Замените все существующие строки на:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Сохраните и выйдите аналогично (`Ctrl+O`, затем `Ctrl+X`).

#### Обновление индекса пакетов

Выполните для обеих версий после редактирования файла источников:

```bash
sudo apt update
```

---

### Шаг 2: Установка зависимостей для сборки

Драйвер компилируется из исходников, поэтому сначала установите заголовки ядра и инструменты сборки:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Фрагмент `$(uname -r)` автоматически определяет версию вашего ядра — вводить её вручную не нужно.

---

### Шаг 3: Загрузка исходников драйвера (зеркало в Китае)

Клонируйте репозиторий драйвера с Gitee, доступного в Китае:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Перейдите в скачанную папку:

```bash
cd rtl8812au
```

> **Примечание:** Если URL не работает, перейдите на [gitee.com](https://gitee.com) и найдите `rtl8812au`. Выберите форк с наиболее свежей датой коммита.

---

### Шаг 4: Сборка и установка

Соберите модуль ядра из исходников:

```bash
make
```

Установите его в систему:

```bash
sudo make install
```

Зарегистрируйте модуль в DKMS для автоматического пережития обновлений ядра:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Загрузите модуль в работающее ядро:

```bash
sudo modprobe 88XXau
```

Проверьте корректность загрузки:

```bash
modinfo 88XXau | grep filename
```

Вы должны увидеть путь, заканчивающийся на `88XXau.ko` или похожее. Если команда вернула вывод — драйвер активен.

---

### Шаг 5: Включение режима монитора

Сначала завершите процессы, которые могут мешать работе беспроводного интерфейса:

```bash
sudo airmon-ng check kill
```

Затем переведите адаптер в режим монитора:

```bash
sudo airmon-ng start wlan0
```

> **Примечание:** Ваш интерфейс может называться `wlan1`, а не `wlan0`. Сначала выполните `iwconfig`, чтобы увидеть все беспроводные интерфейсы, затем подставьте правильное имя в команду выше.

---

### Шаг 6: Тест инъекции пакетов

С адаптером в режиме монитора запустите тест инъекции:

```bash
sudo aireplay-ng --test wlan0mon
```

Успешный результат содержит строки вроде `Injection is working!`. При ошибках с интерфейсом убедитесь, что режим монитора активен: `iwconfig wlan0mon`.

---

## Debian

Менеджер пакетов Debian по умолчанию использует зарубежные серверы. Переключение на зеркало 清华大学 (Пекинский университет Цинхуа) повышает скорость загрузки с нескольких килобайт до мегабайт в секунду.

### Шаг 1: Переключение на зеркало в Китае

Откройте список источников:

```bash
sudo nano /etc/apt/sources.list
```

Удалите всё содержимое и вставьте три строки (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Сохраните с `Ctrl+O`, выйдите с `Ctrl+X`. Обновите индекс пакетов:

```bash
sudo apt update
```

### Шаг 2: Установка зависимостей для сборки

Драйвер AWUS036ACH компилируется из исходников, поэтому установите заголовки ядра и инструменты сборки:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Шаг 3: Загрузка исходников драйвера (зеркало в Китае)

Клонируйте репозиторий с Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Перейдите в папку проекта:

```bash
cd rtl8812au
```

> **URL не работает?** Найдите на Gitee `rtl8812au` и выберите наиболее актуальный форк.

### Шаг 4: Сборка и установка

Выполните команды последовательно в папке `rtl8812au`:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` регистрирует драйвер для автоматической пережития обновлений ядра.

### Шаг 5: Включение режима монитора

**Завершите мешающие процессы** перед переключением режима:

```bash
sudo airmon-ng check kill
```

Запустите режим монитора на адаптере:

```bash
sudo airmon-ng start wlan0
```

Если `airmon-ng` отсутствует, установите его:

```bash
sudo apt install -y aircrack-ng
```

Подтвердите активацию интерфейса:

```bash
iwconfig
```

Найдите в выводе интерфейс с именем `wlan0mon`.

### Шаг 6: Тест инъекции пакетов

```bash
sudo aireplay-ng --test wlan0mon
```

Поток результатов тестирования инъекции подтверждает работоспособность адаптера.

---

## Raspberry Pi 4B / 5

> AWUS036ACH потребляет ~500mW. Прямое подключение к USB-порту Raspberry Pi может вызвать троттлинг или перезагрузку под нагрузкой. **Всегда используйте питаемый USB-хаб.**

---

### Шаг 1: Загрузка образа Kali Linux ARM64

Перейдите на официальную страницу загрузок Kali ARM:
https://www.kali.org/get-kali/#kali-arm

Выберите **Raspberry Pi 4 (64-bit)** или **Raspberry Pi 5 (64-bit)** под ваш одноплатник. Не скачивайте 32-битный образ — сборка драйвера требует 64-битного ядра.

> **Зеркало в Китае:** Если kali.org загружается медленно, попробуйте 华为云:
> https://repo.huaweicloud.com/kali-images/
> Перейдите в папку с последним релизом и скачайте тот же ARM64 образ оттуда.

---

### Шаг 2: Запись на MicroSD

Вставьте карту microSD, затем проверьте её путь устройства перед записью.

```bash
lsblk
```

Найдите вашу карту в списке — она будет отображаться как `sdb` или `mmcblk0`. Запишите образ, заменив `/dev/sdX` на фактический путь.

```bash
# Замените /dev/sdX на вашу SD-карту (проверьте с помощью lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Дождитесь завершения `sync` перед извлечением карты. Загрузите Pi с карты. Учётные данные по умолчанию: **kali / kali**.

---

### Шаг 3: Переключение на зеркало в Китае

После первой загрузки откройте файл источников пакетов.

```bash
sudo nano /etc/apt/sources.list
```

Удалите всё содержимое и замените одной строкой:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните: **Ctrl+O**, Enter, Ctrl+X. Затем примените зеркало и обновите систему.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Перезагрузка учитывает обновления ядра перед установкой драйвера.

---

### Шаг 4: Установка драйвера (ARM64)

DKMS-пакет работает на ARM64 так же, как на x86 — никаких специальных действий не требуется.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

Если команда вернёт ошибку о том, что пакет не найден, соберите драйвер из исходников:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Шаг 5: Включение режима монитора

Перед работой с адаптером проверьте, какое имя интерфейса назначил Pi.

```bash
iwconfig
```

На Pi с встроенным Wi-Fi чипом AWUS036ACH отображается как `wlan1` — встроенное радио занимает `wlan0`. Используйте то имя, которое вернул `iwconfig`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Снова запустите `iwconfig` и найдите запись, заканчивающуюся на `mon` — обычно `wlan1mon` — с `Mode:Monitor`. Это подтверждает успешное переключение.

---

### Шаг 6: Тест инъекции пакетов

```bash
sudo aireplay-ng --test wlan1mon
```

Замените `wlan1mon` на имя мониторного интерфейса из Шага 5. Рабочий адаптер выводит `Injection is working!`. Если тест не прошёл, перезагрузитесь и повторите. Плохое USB-соединение через непитаемый хаб — наиболее частая причина на Pi. Убедитесь, что используете питаемый хаб.

---

## Проброс USB в виртуальную машину {#virtual-machine-usb-passthrough}

Запускаете Kali Linux внутри виртуальной машины на macOS или Windows? Вам нужно пробросить USB-адаптер в гостевую ОС.

### VirtualBox

1. При выключенной ВМ перейдите в **Настройки → USB**.
2. Включите **Контроллер USB 3.0 (xHCI)**.
3. Нажмите значок **+** для добавления USB-фильтра.
4. Выберите: **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Запустите ВМ — адаптер появится внутри Kali.

Внутри ВМ выполните `lsusb`, чтобы подтвердить наличие `0bda:8812`, затем следуйте шагам Kali Linux выше.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Запустите ВМ.
2. В меню: **Виртуальная машина → USB и Bluetooth**.
3. Найдите **Realtek 802.11ac NIC** и нажмите **Подключить**.
4. Адаптер отключится от хоста и появится внутри ВМ.

Выполните `lsusb` внутри ВМ для подтверждения, затем следуйте шагам Kali Linux выше.

### Примечание о VIF (Виртуальный интерфейс)

Чип RTL8812AU в AWUS036ACH имеет ограниченную поддержку VIF на Linux. Надёжный одновременный запуск managed-режима и режима монитора (или AP-режима) на одном адаптере невозможен.

Если ваш рабочий процесс требует VIF — например, одновременный запуск поддельных точек доступа и мониторинга — AWUS036ACH не подходит. Ознакомьтесь с [руководством по установке AWUS036ACM](/ru/blog/awus036acm-china-install-guide/). Этот адаптер использует чип MT7612U с полноценной поддержкой VIF в ядре.

---

{{< faq >}}

## Устранение неисправностей

| Проблема | Вероятная причина | Решение |
|---------|-------------------|---------|
| `lsusb` не показывает 0bda:8812 | Адаптер не подключён или плохой кабель | Попробуйте другой USB-порт. Используйте питаемый хаб на Raspberry Pi. |
| `make` завершается с ошибками заголовков | Заголовки ядра отсутствуют или версия не совпадает | Выполните `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` завершается ошибкой | Secure Boot блокирует неподписанные модули | Отключите Secure Boot в BIOS или подпишите модуль |
| Драйвер исчезает после обновления ядра | Драйвер не зарегистрирован в DKMS | Повторно выполните `sudo dkms install rtl8812au/$(cat VERSION)` из директории исходников |
| `airmon-ng start wlan0` завершается ошибкой | NetworkManager всё ещё работает | Выполните `sudo airmon-ng check kill` сначала |
| Режим монитора запустился, но трафик не перехватывается | Неверный канал или имя интерфейса | Проверьте интерфейс с `iwconfig`. Установите канал: `iwconfig wlan0mon channel 6` |
| Тест инъекции выдаёт «No Answer» | Точка доступа слишком далеко или неверный интерфейс | Подойдите ближе к ТД. Используйте `wlan0mon`, а не `wlan0` |

## Справочник зеркал в Китае

Все ресурсы из этого руководства — GitHub не требуется:

| Ресурс | URL | Для чего |
|--------|-----|---------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов, прошивки |
| Документация Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Руководства по продуктам |
| Зеркало 清华大学 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Зеркало 阿里云 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (рекомендуется) |
| Зеркало 中科大 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (рекомендуется) |
| Зеркало 华为云 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Образы Kali ARM (резерв) |
| Драйвер RTL8812AU (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Сборка из исходников (запасной вариант) |

## Другие руководства по адаптерам Alfa для Китая

Это часть серии **Alfa China Install Guide**. Каждая статья охватывает одну модель адаптера:

- AWUS036ACH ← вы здесь
- [Руководство AWUS036ACM для Китая](/ru/blog/awus036acm-china-install-guide/) — MT7612U, лучшая поддержка VIF
- [Руководство AWUS036ACS для Китая](/ru/blog/awus036acs-china-install-guide/)
- [Руководство AWUS036AX для Китая](/ru/blog/awus036ax-china-install-guide/)
- [Руководство AWUS036AXER для Китая](/ru/blog/awus036axer-china-install-guide/)
- [Руководство AWUS036AXM для Китая](/ru/blog/awus036axm-china-install-guide/)
- [Руководство AWUS036AXML для Китая](/ru/blog/awus036axml-china-install-guide/)
- [Руководство AWUS036EACS для Китая](/ru/blog/awus036eacs-china-install-guide/)

Есть вопросы? Оставьте комментарий ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).


## Источники

1. [Официальная документация aircrack-ng](https://www.aircrack-ng.org/)
2. [Официальный сайт ALFA Network](https://www.alfa.com.tw/)
3. [Официальная документация Kali Linux](https://www.kali.org/docs/)
4. [Зеркало Gitee rtl8812au](https://gitee.com/mirrors/rtl8812au)
5. [Драйвер Realtek RTL8812AU](https://www.realtek.com/)
