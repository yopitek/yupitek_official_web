---
title: "Полное руководство: установка всех USB WiFi адаптеров Alfa на Linux в Китае — Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "Исчерпывающее руководство по установке всех USB WiFi адаптеров Alfa на Linux в Китае. Охватывает Kali Linux, Ubuntu 22/24, Debian и Raspberry Pi. Без GitHub — только отечественные зеркала."
---

## Добро пожаловать в полное руководство по установке Alfa на Linux

Если вы читаете это, значит, вы купили USB WiFi адаптер Alfa и столкнулись с трудностями:

- Вы находитесь в Китае и не можете получить доступ к GitHub
- Установка драйвера кажется сложной
- Вам нужно включить режим мониторинга и инъекцию пакетов для тестирования беспроводных сетей
- Вы не уверены, какой драйвер нужен вашей конкретной модели Alfa

Это руководство решает **все эти проблемы**. Мы проведём вас через установку **каждого USB WiFi адаптера Alfa** на **всех основных дистрибутивах Linux**, используя только **зеркала, доступные из Китая**. Без GitHub. Без лишних сложностей.

---

## Зачем создано это руководство

USB WiFi адаптеры Alfa популярны среди специалистов по тестированию на проникновение, сетевых инженеров и энтузиастов беспроводных сетей. Они поддерживают режим мониторинга и инъекцию пакетов — функции, которых нет у большинства потребительских WiFi адаптеров.

Но проблема в том, что **большинство руководств по установке драйверов предполагают наличие доступа к GitHub**. Если вы находитесь в Китае, это невозможно. Данное руководство разработано специально для пользователей в Китае и использует исключительно зеркала и ресурсы, работающие внутри китайской интернет-инфраструктуры.

---

## Краткий справочник по моделям

Прежде чем приступить, определите, какой адаптер Alfa у вас есть и какой чип он использует:

### Серия AX (Wi-Fi 6 / 802.11ax)

| Модель | Чипсет | Драйвер | Лучший выбор для |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | Общее использование, хороший радиус действия |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Компактный форм-фактор |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | Ультракомпактный |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | Повышенная мощность |

### Серия AC (Wi-Fi 5 / 802.11ac)

| Модель | Чипсет | Драйвер | Лучший выбор для |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | Высокая мощность, большой радиус действия |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Лучшая поддержка VIF**, plug-and-play |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | Бюджетный вариант |

### Какой адаптер у вас?

1. Посмотрите на наклейку на адаптере
2. Проверьте коробку, в которой он поставлялся
3. Если вы купили его онлайн, проверьте историю заказов

Как только вы узнаете свою модель, переходите к соответствующему разделу ниже или следуйте общей инструкции.

---

## Прежде чем начать: что вам понадобится

Убедитесь, что всё готово перед началом работы:

1. **USB WiFi адаптер Alfa** — подходящая модель для ваших задач
2. **USB-кабель** — тот, что был в комплекте, подойдёт
3. **Активный USB-хаб с питанием** — обязателен для Raspberry Pi
4. **Активное интернет-соединение** — для доступа к отечественным зеркалам в Китае
5. **Права sudo** — вам потребуется доступ администратора для установки драйверов

Сначала подключите адаптер и убедитесь, что система его видит:

```bash
lsusb
```

Найдите идентификатор вендора вашего адаптера в выводе:

- **Адаптеры Alfa** отображаются как `0e8d` (MediaTek) или `0bda` (Realtek)
- Пример: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- Пример: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

Если ID виден — адаптер определён. Переходите к разделу установки драйвера ниже.

Если ID не виден — попробуйте другой USB-порт, замените кабель и снова выполните `lsusb`.

---

## Выберите вашу операционную систему

Перейдите в нужный раздел:

- [Kali Linux](#kali-linux-installation)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-installation)
- [Debian 12 (Bookworm)](#debian-12-bookworm-installation)
- [Raspberry Pi OS (64-bit)](#raspberry-pi-os-installation)

Драйвер уже установлен? Переходите к расширенным разделам:

- [Включение режима мониторинга](#enable-monitor-mode-on-any-adapter)
- [Тест инъекции пакетов](#test-packet-injection)
- [Поддержка виртуального интерфейса (VIF)](#virtual-interface-vif-support)
- [USB Passthrough для виртуальных машин](#virtual-machine-usb-passthrough)

---

## Справочник зеркал, доступных из Китая

Все ресурсы в этом руководстве используют следующие зеркала, доступные из Китая:

| Ресурс | URL | Для чего |
|----------|-----|---------|
| **Официальные загрузки Alfa** | [files.alfa.com.tw](https://files.alfa.com.tw) | Пакеты драйверов, прошивки |
| **Документация Alfa** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Руководства по продуктам (на английском) |
| **Зеркало Университета Цинхуа** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **Зеркало Aliyun** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (рекомендуется) |
| **Зеркало USTC** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (рекомендуется) |
| **Зеркало Huawei Cloud** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Образы Kali ARM (резервный) |
| **Gitee (альтернатива GitHub)** | [gitee.com](https://gitee.com) | Исходный код драйверов |

---

## Установка на Kali Linux

Kali Linux поставляется с предустановленными инструментами для работы с беспроводными сетями. Запуск адаптеров Alfa занимает всего несколько шагов.

### Шаг 1: Переключение на китайское зеркало

Откройте список источников:

```bash
sudo nano /etc/apt/sources.list
```

Замените всё содержимое на:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните: **Ctrl+O**, Enter, затем **Ctrl+X**. Обновите индекс:

```bash
sudo apt update
```

> **Резервное зеркало:** Если зеркало USTC (中科大) работает медленно, используйте Tsinghua (清华):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### Шаг 2: Установка драйвера по чипсету

#### Серия AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Серия AC — Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Серия AC — MediaTek (MT7612U)

Драйвер MT7612U встроен в ядро Kali. Проверьте его загрузку:

```bash
lsmod | grep mt76
```

Если в выводе есть `mt76x2u` — готово. Если нет:

```bash
sudo modprobe mt76x2u
```

### Шаг 3: Проверка загрузки драйвера

Снова выполните `lsusb`. Ваш адаптер должен быть виден. Затем проверьте беспроводные интерфейсы:

```bash
iwconfig
```

Ищите `wlan0` или `wlan1`. Если интерфейс появился — драйвер работает.

### Шаг 4: Включение режима мониторинга

Остановите мешающие процессы:

```bash
sudo airmon-ng check kill
```

Запустите режим мониторинга:

```bash
sudo airmon-ng start wlan0
```

Проверьте:

```bash
iwconfig
```

Ищите `wlan0mon` с `Mode:Monitor`. Готово!

---

## Установка на Ubuntu 22.04 / 24.04

### Шаг 1: Переключение на китайское зеркало

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Замените содержимое на:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Сохраните с помощью **Ctrl+O**, выйдите с помощью **Ctrl+X**.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Замените содержимое на:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Сохраните и выйдите.

#### Обновление индекса пакетов

```bash
sudo apt update
```

### Шаг 2: Установка зависимостей для сборки

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Шаг 3: Установка драйвера

#### Серия AX (RTL8832BU)

Клонируйте с Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Серия AC — Realtek (RTL8812AU)

Клонируйте с Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Серия AC — MediaTek (MT7612U)

Драйвер встроен в ядро Ubuntu. Загрузите его:

```bash
sudo modprobe mt76x2u
```

### Шаг 4: Включение режима мониторинга

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Ищите `wlan0mon` с `Mode:Monitor`.

---

## Установка на Debian 12 (Bookworm)

### Шаг 1: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

Замените содержимое на:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Сохраните и выйдите. Обновите индекс:

```bash
sudo apt update
```

### Шаг 2: Установка несвободной прошивки

```bash
sudo apt install -y firmware-misc-nonfree
```

### Шаг 3: Установка зависимостей для сборки

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Шаг 4: Установка драйвера

#### Серия AX (RTL8832BU)

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Серия AC — Realtek (RTL8812AU)

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Серия AC — MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Шаг 5: Установка Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### Шаг 6: Включение режима мониторинга

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Ищите `wlan0mon` с `Mode:Monitor`.

---

## Установка на Raspberry Pi OS

> **ВАЖНО:** AWUS036ACH потребляет ~500 мВт. AWUS036ACM — ~400 мВт. **Всегда используйте активный USB-хаб с питанием**, чтобы предотвратить троттлинг или зависание Raspberry Pi под нагрузкой.

### Шаг 1: Загрузка образа Kali Linux ARM64

Перейдите на: https://www.kali.org/get-kali/#kali-arm

Выберите **Raspberry Pi 4 (64-bit)** или **Raspberry Pi 5 (64-bit)**. Не используйте 32-битный вариант — требуется 64-битная версия.

> **Зеркало для Китая:** Если kali.org работает медленно, используйте Huawei Cloud: https://repo.huaweicloud.com/kali-images/

### Шаг 2: Запись образа на MicroSD

Определите путь к вашей SD-карте:

```bash
lsblk
```

Запишите образ (замените `/dev/sdX` на фактический путь к карте):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Дождитесь завершения `sync`. Загрузите Pi. Учётные данные по умолчанию: **kali / kali**.

### Шаг 3: Переключение на китайское зеркало

```bash
sudo nano /etc/apt/sources.list
```

Замените содержимое на:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Сохраните и примените:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Шаг 4: Установка драйвера

#### Серия AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Серия AC — Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Серия AC — MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Шаг 5: Включение режима мониторинга

На Raspberry Pi со встроенным Wi-Fi адаптер Alfa отображается как `wlan1`:

```bash
iwconfig
```

Затем:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

Ищите `wlan1mon` с `Mode:Monitor`.

---

## Включение режима мониторинга на любом адаптере

После установки драйвера включить режим мониторинга несложно:

### Шаг 1: Узнайте имя интерфейса

```bash
iwconfig
```

Запомните, какой у вас интерфейс: `wlan0` или `wlan1`.

### Шаг 2: Остановите мешающие процессы

```bash
sudo airmon-ng check kill
```

### Шаг 3: Запустите режим мониторинга

```bash
sudo airmon-ng start wlan0
```

Замените `wlan0` на фактическое имя вашего интерфейса, если оно отличается.

### Шаг 4: Проверка

```bash
iwconfig
```

Ищите интерфейс с суффиксом `mon` (например, `wlan0mon`) с `Mode:Monitor`.

---

## Тест инъекции пакетов

Это подтверждает, что адаптер может отправлять произвольные пакеты — необходимое условие для тестирования беспроводных сетей.

```bash
sudo aireplay-ng --test wlan0mon
```

**Успешный результат:**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**Если тест не прошёл:**
- Перезагрузитесь и попробуйте снова
- Убедитесь, что никакой другой процесс не держит интерфейс (`iwconfig`)
- Подойдите ближе к точке доступа WiFi для теста
- Убедитесь, что используете `wlan0mon`, а не `wlan0`

---

## Поддержка виртуального интерфейса (VIF)

VIF (Virtual Interface Functionality) позволяет одновременно использовать несколько интерфейсов на одном адаптере. Например:

- **Управляемый режим** (`wlan0`) + **режим мониторинга** (`mon0`) одновременно
- Работа в сети И захват трафика без разрыва соединения

### Какие адаптеры поддерживают VIF?

| Чипсет | Поддержка VIF | Примечания |
|---------|-------------|-------|
| **MT7612U (AWUS036ACM)** | ✅ Полная нативная поддержка | Лучший выбор для задач с VIF |
| **RTL8812AU (AWUS036ACH)** | ⚠️ Ограниченная | Нельзя одновременно использовать управляемый и мониторный режимы |
| **RTL8832BU (серия AX)** | ⚠️ Ограниченная | Уточняйте в документации к конкретной модели |

### Создание виртуального интерфейса (MT7612U)

Если у вас есть AWUS036ACM (MT7612U):

```bash
# Создание мониторного интерфейса, пока wlan0 остаётся в управляемом режиме
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Проверьте, что оба интерфейса активны:

```bash
iwconfig
```

Вы должны увидеть:
- `wlan0` — управляемый режим (подключён к точке доступа)
- `mon0` — режим мониторинга (захватывает весь трафик)

### Сценарии использования

**Захват трафика при активном подключении:**

```bash
sudo airodump-ng mon0
```

`wlan0` продолжает обычную работу, пока `mon0` захватывает весь трафик.

**Поддельная точка доступа + мониторинг:**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## USB Passthrough для виртуальных машин

Запускаете Linux внутри виртуальной машины? Вам нужно пробросить USB-адаптер в гостевую ОС.

### VirtualBox

1. Выключите виртуальную машину
2. Откройте **Настройки → USB**
3. Включите **USB 3.0 (xHCI) Controller**
4. Нажмите **+**, чтобы добавить USB-фильтр
5. Выберите ваш адаптер Alfa (ID: `0bda:8812` или `0e8d:7612`)
6. Запустите виртуальную машину

Внутри VM выполните `lsusb` для подтверждения, затем следуйте инструкции по установке на Kali Linux выше.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Запустите виртуальную машину
2. Меню: **Virtual Machine → USB & Bluetooth**
3. Найдите ваш адаптер Alfa и нажмите **Connect**
4. Адаптер появится внутри виртуальной машины

Выполните `lsusb` для подтверждения, затем следуйте инструкции по установке драйвера.

---

## Устранение неполадок

| Проблема | Вероятная причина | Решение |
|---------|-------------|-----|
| `lsusb` не показывает ID адаптера | Плохой кабель или нет питания | Попробуйте другой USB-порт. На Pi используйте активный хаб. |
| `modprobe` сообщает «Module not found» | Отсутствуют модули ядра | Выполните `sudo apt install linux-modules-extra-$(uname -r)` |
| Драйвер работает, но не переключается в режим мониторинга | Вмешательство NetworkManager | Сначала выполните `sudo airmon-ng check kill` |
| Режим мониторинга запущен, но ничего не захватывает | Неверный интерфейс или канал | Выполните `iwconfig`. Установите канал: `iwconfig wlan0mon channel 6` |
| Тест инъекции пакетов не прошёл | Используется неверный интерфейс | Используйте `wlan0mon`, а не `wlan0` |
| Создание VIF завершается ошибкой | Драйвер загружен не полностью | Отключите и снова подключите адаптер или перезагрузите модуль |

---

## Приложение: полный список моделей Alfa

| Модель | Чипсет | Драйвер | Источник для Китая |
|-------|---------|--------|---------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | Встроенный драйвер ядра |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## Заключение

Это руководство охватывает **все USB WiFi адаптеры Alfa** на **всех основных дистрибутивах Linux**, используя **исключительно ресурсы, доступные из Китая**. Теперь вы умеете:

✅ Устанавливать драйверы для любого адаптера Alfa  
✅ Включать режим мониторинга на Kali, Ubuntu, Debian или Raspberry Pi  
✅ Тестировать инъекцию пакетов  
✅ Использовать виртуальные интерфейсы (VIF) на поддерживаемых моделях  
✅ Пробрасывать адаптеры в виртуальные машины  

**Остались вопросы или возникли проблемы?** Обратитесь к руководствам по конкретным моделям в нашей серии или свяжитесь с нами на [yupitek.com](https://yupitek.com/ru/contact/).

---

## Связанные руководства

Это часть серии **Alfa China Install Guide**:

- [Руководство по установке AWUS036ACH в Китае](/ru/blog/awus036ach-china-install-guide/) — RTL8812AU, высокая мощность
- [Руководство по установке AWUS036ACM в Китае](/ru/blog/awus036acm-china-install-guide/) — MT7612U, лучшая поддержка VIF
- [Руководство по установке AWUS036ACS в Китае](/ru/blog/awus036acs-china-install-guide/) — RTL8811AU, бюджетный вариант
- [Руководство по установке AWUS036AX в Китае](/ru/blog/awus036ax-china-install-guide/) — Wi-Fi 6, RTL8832BU
- [Руководство по установке AWUS036AXM в Китае](/ru/blog/awus036axm-china-install-guide/) — Wi-Fi 6, компактный форм-фактор
- [Руководство по установке AWUS036AXML в Китае](/ru/blog/awus036axml-china-install-guide/) — Wi-Fi 6, ультракомпактный
- [Руководство по установке AWUS036AXER в Китае](/ru/blog/awus036axer-china-install-guide/) — Wi-Fi 6, повышенная мощность
- [Руководство по установке AWUS036EAC в Китае](/ru/blog/awus036eacs-china-install-guide/) — RTL8814AU, высокая мощность

---

*Последнее обновление: 24 апреля 2026 г.*
