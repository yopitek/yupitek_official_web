---
title: "Руководство по установке драйвера ALFA AWUS036ACM для Китая: Kali Linux, Ubuntu, Debian и Raspberry Pi"
description: "Пошаговое руководство по установке драйвера ALFA AWUS036ACM в Китае с использованием отечественных зеркал. Встроенный в ядро драйвер MT7612U, полная поддержка VIF. Охватывает Kali Linux, Ubuntu 22/24, Debian и Raspberry Pi. Без GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "драйвер", "китай", "режим-монитора", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
related_product: "/ru/products/alfa/awus036acm/"
---

AWUS036ACM — один из самых простых в настройке адаптеров ALFA на Linux. Чип MT7612U использует драйвер `mt76x2u`, встроенный в ядро Linux начиная с версии 4.19. На большинстве современных систем адаптер заработает с двух-трёх команд. Руководство охватывает полную настройку — проверку драйвера, режим монитора, инъекцию пакетов и VIF — с использованием только отечественных зеркал. GitHub не требуется.

## Перед началом работы

Убедитесь, что у вас есть следующее:

1. Адаптер **ALFA AWUS036ACM**
2. USB-кабель (подойдёт кабель из комплекта)
3. USB-хаб с внешним питанием — обязателен для Raspberry Pi
4. Активное подключение к интернету для доступа к отечественным зеркалам

Подключите адаптер, затем убедитесь, что система его обнаружила:

```bash
lsusb
```

Найдите в выводе следующую строку:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

Если видите `0e8d:7612` — адаптер определён. Переходите к разделу своей ОС.

Если строки нет, попробуйте другой USB-порт или замените кабель, затем снова выполните `lsusb`.

## Выберите операционную систему

Перейдите к нужному разделу:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Если драйвер уже установлен, перейдите сразу к:

- [Включение режима монитора](#enable-monitor-mode)
- [Тест инъекции пакетов](#test-packet-injection)
- [Виртуальный интерфейс (VIF)](#virtual-interface-vif)
- [Проброс USB в виртуальную машину](#virtual-machine-usb-passthrough)

---

## Kali Linux

Драйвер MT7612U уже включён в ядро Kali. В большинстве случаев адаптер работает сразу после подключения. Шаги ниже позволяют проверить загрузку драйвера и перейти в режим монитора.

### Шаг 1: Переключитесь на китайское зеркало

Откройте список источников в терминале.

```bash
sudo nano /etc/apt/sources.list
```

Удалите всё содержимое и вставьте следующую строку:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните: нажмите **Ctrl+O**, затем Enter, затем Ctrl+X для выхода. Обновите индекс пакетов.

```bash
sudo apt update
```

> **Резервное зеркало:** Если 中科大 (USTC) работает медленно, используйте 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Шаг 2: Проверьте драйвер

Убедитесь, что модуль загрузился автоматически при подключении адаптера.

```bash
lsmod | grep mt76
```

В выводе должна присутствовать строка `mt76x2u`. Если ничего нет, загрузите модуль вручную.

```bash
sudo modprobe mt76x2u
```

Снова выполните `lsmod | grep mt76` для подтверждения. Затем проверьте, что адаптер активен.

```bash
iwconfig
```

Найдите беспроводной интерфейс — обычно `wlan0` или `wlan1`. Если интерфейс отображается с ESSID или `unassociated`, драйвер работает.

---

### Шаг 2 (альтернативный): Установка дополнительных модулей ядра

Если `modprobe mt76x2u` возвращает ошибку «Module not found», в вашей сборке ядра могут отсутствовать модули MT76. Установите их с китайского зеркала.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

После завершения установки снова загрузите модуль.

```bash
sudo modprobe mt76x2u
```

Если пакет недоступен для вашей версии ядра, скомпилируйте драйвер из исходников.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **Примечание:** Если ссылка на Gitee не открывается, найдите `mt76` на Gitee и выберите наиболее актуальный форк. Также можно загрузить архивы с драйвером напрямую с [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Шаг 3: Включение режима монитора {#enable-monitor-mode}

Перед переключением в режим монитора проверьте, какое имя интерфейса присвоила система адаптеру.

```bash
iwconfig
```

Найдите `wlan0` или `wlan1`. Используйте это имя в командах ниже.

Остановите NetworkManager и wpa_supplicant, чтобы они не мешали работе.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Подтвердите переключение.

```bash
iwconfig
```

Найдите запись вида `wlan0mon` с `Mode:Monitor`. Когда она появится, адаптер готов к захвату пакетов.

---

### Шаг 4: Тест инъекции пакетов {#test-packet-injection}

Запустите тест инъекции на интерфейсе в режиме монитора.

```bash
sudo aireplay-ng --test wlan0mon
```

Успешный результат выглядит так:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Если тест не прошёл, перезагрузитесь и повторите. Если ошибка сохраняется, убедитесь, что интерфейс не занят другим процессом — проверьте с помощью `iwconfig`.

---

## Ubuntu 22.04 / 24.04

Драйвер MT7612U также встроен в ядро Ubuntu, однако может поставляться в пакете `linux-modules-extra`, а не в базовом образе ядра. Шаги ниже охватывают оба случая.

### Шаг 1: Переключитесь на китайское зеркало

#### Ubuntu 24.04 (Noble)

Откройте файл источников в формате DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Удалите всё содержимое и вставьте:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Сохраните с помощью `Ctrl+O`, затем выйдите через `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Откройте классический файл источников:

```bash
sudo nano /etc/apt/sources.list
```

Замените все строки на:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Сохраните и выйдите (`Ctrl+O`, затем `Ctrl+X`).

#### Обновите индекс пакетов

```bash
sudo apt update
```

---

### Шаг 2: Загрузите драйвер

Попробуйте загрузить модуль напрямую.

```bash
sudo modprobe mt76x2u
```

Если получаете ошибку «Module not found», установите пакет с дополнительными модулями.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Проверьте видимость адаптера.

```bash
iwconfig
```

Наличие в выводе интерфейса `wlan0` или `wlan1` подтверждает, что драйвер активен.

---

### Шаг 3: Установите инструменты для работы с беспроводными сетями

Установите aircrack-ng для работы в режиме монитора и тестирования инъекций.

```bash
sudo apt install -y aircrack-ng
```

---

### Шаг 4: Включите режим монитора

Завершите мешающие процессы, затем запустите режим монитора.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Примечание:** Если в системе присутствует другая беспроводная карта, ваш интерфейс может называться `wlan1`. Сначала выполните `iwconfig` для проверки.

---

### Шаг 5: Тест инъекции пакетов

```bash
sudo aireplay-ng --test wlan0mon
```

Успешный результат показывает `Injection is working!`. При ошибках интерфейса убедитесь, что режим монитора активен, с помощью `iwconfig wlan0mon`.

---

## Debian

Драйвер MT7612U включён в ядро Debian, однако для полной инициализации иногда требуется пакет `firmware-misc-nonfree`.

### Шаг 1: Переключитесь на китайское зеркало

Откройте список источников:

```bash
sudo nano /etc/apt/sources.list
```

Удалите всё содержимое и вставьте следующие три строки (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Сохраните с помощью `Ctrl+O`, затем выйдите через `Ctrl+X`. Обновите индекс:

```bash
sudo apt update
```

### Шаг 2: Установите несвободную прошивку

MT7612U требует файлы прошивки из пакета `firmware-misc-nonfree`. Без него адаптер инициализируется, но может не устанавливать ассоциацию и не переходить в режим монитора.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Шаг 3: Загрузите драйвер

```bash
sudo modprobe mt76x2u
```

Если модуль отсутствует, сначала установите пакет с дополнительными модулями ядра.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Убедитесь, что интерфейс появился.

```bash
iwconfig
```

### Шаг 4: Включите режим монитора

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Подтвердите режим монитора с помощью `iwconfig` — найдите `wlan0mon` с `Mode:Monitor`.

### Шаг 5: Тест инъекции пакетов

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` подтверждает полную работоспособность адаптера.

---

## Raspberry Pi 4B / 5

> AWUS036ACM потребляет около 400 мВт под нагрузкой. Используйте USB-хаб с внешним питанием, чтобы Pi не начал ограничивать мощность.

---

### Шаг 1: Загрузите образ Kali Linux ARM64

Перейдите на официальную страницу загрузок Kali для ARM:
https://www.kali.org/get-kali/#kali-arm

Выберите **Raspberry Pi 4 (64-bit)** или **Raspberry Pi 5 (64-bit)**. Не используйте 32-битный образ — требуется 64-битный.

> **Китайское зеркало:** Если kali.org работает медленно, используйте 华为云:
> https://repo.huaweicloud.com/kali-images/
> Перейдите в папку с последним релизом и скачайте образ ARM64 оттуда.

---

### Шаг 2: Запишите образ на MicroSD

Сначала проверьте путь к вашей карте.

```bash
lsblk
```

Затем запишите образ, заменив `/dev/sdX` на реальный путь к карте.

```bash
# Replace /dev/sdX with your actual SD card (check with lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Дождитесь завершения `sync`, затем загрузитесь. Учётные данные по умолчанию: **kali / kali**.

---

### Шаг 3: Переключитесь на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

Замените содержимое на:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните и примените изменения.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Шаг 4: Проверьте драйвер

После перезагрузки подключите адаптер и проверьте.

```bash
lsmod | grep mt76
```

Если `mt76x2u` присутствует в выводе, настройка завершена. Если нет:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Шаг 5: Включите режим монитора

На Pi со встроенным Wi-Fi адаптер AWUS036ACM отображается как `wlan1` — встроенный радиомодуль занимает `wlan0`.

```bash
iwconfig
```

Запомните имя интерфейса, затем переключите его в режим монитора.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Подтвердите с помощью `iwconfig` — найдите `wlan1mon` с `Mode:Monitor`.

---

### Шаг 6: Тест инъекции пакетов

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` подтверждает полную работоспособность. Если тест не прошёл, убедитесь, что используете хаб с внешним питанием.

---

## Проброс USB в виртуальную машину {#virtual-machine-usb-passthrough}

### VirtualBox

1. Выключите виртуальную машину. Перейдите в **Settings → USB**.
2. Включите **USB 3.0 (xHCI) Controller**.
3. Нажмите **+**, чтобы добавить USB-фильтр.
4. Выберите: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. Запустите виртуальную машину — адаптер появится внутри Kali.

Выполните `lsusb` в виртуальной машине для подтверждения `0e8d:7612`, затем следуйте шагам для Kali выше.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Запустите виртуальную машину.
2. Меню: **Virtual Machine → USB & Bluetooth**.
3. Найдите **MediaTek MT7612U** и нажмите **Connect**.
4. Выполните `lsusb` в виртуальной машине для подтверждения, затем следуйте шагам для Kali выше.

---

## Виртуальный интерфейс (VIF) {#virtual-interface-vif}

Здесь AWUS036ACM превосходит ACH. Чип MT7612U имеет полную встроенную в ядро поддержку виртуальных интерфейсов. Можно одновременно запускать интерфейс монитора и управляемый интерфейс или точку доступа на одном адаптере — без патчей и хаков.

### Создание второго виртуального интерфейса

При работе адаптера в управляемом режиме как `wlan0` добавьте рядом интерфейс монитора.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Теперь убедитесь, что оба интерфейса активны.

```bash
iwconfig
```

Должны отображаться и `wlan0` (ассоциирован, управляемый режим), и `mon0` (режим монитора). Адаптер работает в обоих режимах одновременно.

### Сценарий использования: мониторинг при сохранении подключения

Позволяет захватывать трафик через `mon0`, пока `wlan0` остаётся подключённым к сети — удобно для коррелированного анализа.

```bash
sudo airodump-ng mon0
```

`wlan0` продолжает нормальную ассоциацию, пока `mon0` захватывает всё в радиусе действия.

### Сценарий использования: фиктивная точка доступа + мониторинг

Создайте интерфейс точки доступа и интерфейс монитора одновременно.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Выполните `iwconfig`, чтобы убедиться в активности всех трёх интерфейсов (`wlan0`, `ap0`, `mon0`).

> **Примечание о hostapd:** Полноценная работа точки доступа требует настройки `hostapd`. Это выходит за рамки данного руководства. Шаги выше подтверждают, что адаптер может создать интерфейс — настройка самой точки доступа является отдельной темой.

---

## Устранение неполадок

| Проблема | Вероятная причина | Решение |
|---------|-------------|-----|
| `lsusb` не показывает 0e8d:7612 | Адаптер не получает питание или повреждён кабель | Попробуйте другой USB-порт. Используйте хаб с питанием на Raspberry Pi. |
| `modprobe mt76x2u` говорит «Module not found» | В ядре отсутствуют дополнительные модули | Выполните `sudo apt install linux-modules-extra-$(uname -r)` |
| Интерфейс появляется, но не устанавливает ассоциацию | Отсутствует файл прошивки | Выполните `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` завершается с ошибкой | NetworkManager всё ещё запущен | Сначала выполните `sudo airmon-ng check kill` |
| Режим монитора запущен, но трафик не захватывается | Неверный канал или неверное имя интерфейса | Задайте канал: `iwconfig wlan0mon channel 6` |
| Тест инъекции показывает «No Answer» | Точка доступа слишком далеко или неверный интерфейс | Подойдите ближе к точке доступа. Используйте `wlan0mon`, а не `wlan0`. |
| Создание виртуального интерфейса завершается с ошибкой | Драйвер загружен не полностью | Отключите адаптер, перезагрузите модуль: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## Справочник китайских зеркал

Все ресурсы, использованные в данном руководстве, — GitHub не требуется:

| Ресурс | URL | Назначение |
|----------|-----|---------|
| Официальные драйверы Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов, прошивки |
| Документация Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Руководства по продуктам |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (рекомендуется) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (рекомендуется) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Образы Kali ARM (резервное) |
| Драйвер MT76 (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Резервная компиляция из исходников |

## Другие руководства по адаптерам Alfa для Китая

Это часть серии **Alfa China Install Guide**. Каждая статья посвящена одной модели адаптера:

- [AWUS036ACH China Install Guide](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- AWUS036ACM ← вы здесь
- [AWUS036ACS China Install Guide](/ru/blog/awus036acs-china-install-guide/)
- [AWUS036AX China Install Guide](/ru/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China Install Guide](/ru/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China Install Guide](/ru/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China Install Guide](/ru/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China Install Guide](/ru/blog/awus036eacs-china-install-guide/)

Есть вопросы? Оставьте комментарий ниже или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).
