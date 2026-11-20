---
title: "ALFA Network Soft AP Полное Руководство 2026: Создание WiFi Хотспотов на Kali Linux, Ubuntu, Debian и Raspberry Pi 4/5"
description: "Всестороннее исследование поддержки Soft AP (hostapd/WiFi Hotspot) USB WiFi адаптеров ALFA Network на Kali Linux, Ubuntu, Debian и Raspberry Pi 4/5. Полные руководства по настройке AWUS036ACM, AWUS036ACH и AWUS036AXML."
date: 2026-05-21
author: "benny-lai"
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"

faq:
  - question: "Может ли USB-адаптер ALFA работать как WiFi-точка доступа в Linux?"
    answer: "Зависит от чипсета. AWUS036ACM (MT7612U) полностью поддерживает и работает Plug & Play, AWUS036ACH (RTL8812AU) поддерживается условно, AWUS036AXML поддерживается частично и требует настройки."
  - question: "Какая модель ALFA лучше всего подходит для создания Soft AP на Raspberry Pi?"
    answer: "AWUS036ACM — лучший выбор. Встроенный драйвер работает Plug & Play, потребление всего 400 мА подходит для питания Pi, поддерживает WPA3 и VIF-виртуальные интерфейсы, стабилен на всех платформах."
  - question: "Как проверить, поддерживает ли адаптер режим AP?"
    answer: "Выполните iw list | grep -A 10 'Supported interface modes'. Если вывод содержит * AP, драйвер поддерживает Soft AP, и hostapd будет работать корректно."
  - question: "Какие ограничения у Soft AP с драйвером RTL8812AU?"
    answer: "Не поддерживает WPA3, только WPA2-PSK; не поддерживает VIF-виртуальные интерфейсы, нужны две карты; потребление около 800 мА, на Pi нужен USB-хаб с питанием."
  - question: "Что делать, если WiFi внезапно отключается при работе Soft AP на AWUS036AXML?"
    answer: "Встроенный Bluetooth 5.2 в MT7921AUN мешает WiFi. Выполните echo 'install btusb /bin/false' в /etc/modprobe.d/ для постоянного отключения драйвера Bluetooth, затем перезагрузите."
---
> «Можно ли использовать USB WiFi-адаптеры ALFA как точку доступа WiFi (Soft AP) в Kali Linux / Ubuntu / Raspberry Pi?»

{{< tldr >}}
Совместимость Soft AP адаптеров ALFA зависит от драйвера чипсета. AWUS036ACM — стабильный выбор для всех платформ, AWUS036ACH работает, но без WPA3, AWUS036AXML требует отключения Bluetooth и обновления прошивки, RTL8832BU (AX / AXER) работает со встроенным драйвером на ядре 6.17+.
{{< /tldr >}}


Адаптер ALFA AWUS036ACM (MT7612U) — лучший выбор для Linux Soft AP: драйвер в основном ядре работает по принципу plug-and-play, поддерживаются WPA3 и виртуальные интерфейсы (VIF). RTL8812AU поддерживается с ограничениями, MT7921AUN требует ручной настройки.

## Введение

Это один из самых частых вопросов, которые мы получаем в Yopitek. Вопрос звучит просто, но ответ кардинально зависит от модели и чипсета — **не каждый USB WiFi адаптер может работать в режиме Soft AP.**

В этой статье собрано более 500 обсуждений сообщества с GitHub (morrownr/USB-WiFi), технических форумов Reddit, из официальной документации Raspberry Pi и реальных отзывов пользователей, чтобы дать вам честный и исчерпывающий отчёт о том, какие адаптеры ALFA работают, какие нет, а также полное пошаговое руководство по настройке.

---

## 1. Что такое Soft AP? Как это работает в Linux {#what-is-softap}

**Soft AP (Software Access Point)** — это возможность превратить обычный USB WiFi-адаптер в беспроводную базовую станцию (Access Point) программными средствами — прежде всего с помощью **hostapd**. Это позволяет другим устройствам (смартфонам, ноутбукам, IoT-оборудованию) подключаться к сети без покупки отдельного маршрутизатора или точки доступа.

Эта возможность незаменима в ряде сценариев:

- **Дорожный / домашний маршрутизатор**: в поездке или в походе подключите адаптер ALFA к ноутбуку или Raspberry Pi и мгновенно создайте портативную точку доступа WiFi
- **Лаборатория тестирования на проникновение**: создайте изолированную Rogue AP для исследований в области безопасности
- **IoT-ретранслятор**: создайте повторитель в зонах без покрытия, чтобы IoT-датчики могли передавать данные
- **Развёртывание Edge AI**: в промышленной среде без проводной сети превратите устройство в точку доступа для подключения другого оборудования
- **Аварийная связь**: быстро разверните временную сеть при потере связи

### Четыре основных компонента Linux Soft AP

| Компонент | Функция |
|-----------|----------|
| **hostapd** | Основной демон, создающий точку доступа — управляет SSID, аутентификацией, шифрованием |
| **nl80211** | Стандартный интерфейс беспроводной подсистемы Linux — драйвер должен поддерживать этот фреймворк для работы с hostapd |
| **dnsmasq** | DHCP-сервер, автоматически назначающий IP-адреса подключённым клиентам |
| **iptables / nftables** | Трансляция сетевых адресов (NAT) — позволяет подключённым клиентам использовать вышестоящую сеть |

### Ключевая концепция: Режим Master

**Режим Master** (также называемый режимом AP или режимом Infrastructure) — это возможность на уровне драйвера. Если драйвер не поддерживает режим Master, hostapd просто не запустится — какой бы идеальной ни была ваша конфигурация.

Проверьте поддержку режима AP командой:

```bash
iw list | grep -A 10 "Supported interface modes"
```

Если вывод содержит `* AP`, драйвер адаптера поддерживает Soft AP. Если нет — этот адаптер для данной задачи непригоден.

### 💡 Драйверы In-kernel и Out-of-kernel

Это **самое важное** понятие при выборе адаптера для Soft AP:

| Тип | Описание | Влияние на Soft AP |
|------|-------------|-------------------|
| **In-kernel драйвер** | Интегрирован в официальное дерево исходного кода Linux; загружается автоматически при загрузке — установка не требуется | ✅ Стабилен в долгосрочной перспективе; переживает обновления ядра |
| **Out-of-kernel драйвер** | Необходимо скачать с GitHub и скомпилировать вручную; может потребоваться перекомпиляция после каждого обновления ядра | ⚠️ Может сломаться после любого обновления ядра |

**Для долгосрочной стабильности Soft AP драйверы in-kernel значительно превосходят out-of-kernel.**

---

## 2. Линейка продуктов ALFA и обзор чипсетов {#product-lineup}

Ниже приведена текущая линейка продуктов ALFA, которую продаёт Yopitek, с чипсетами и предварительной оценкой Soft AP:

| Модель | Чипсет | Тип драйвера | Стандарт WiFi | Оценка Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (ядро 4.19+) | WiFi 5 AC1200 Двухдиапазонный | ✅ Полная поддержка |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel с 6.13+) | WiFi 5 AC1200 Двухдиапазонный | ⚠️ Условная |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, режим AP 5.19+) | WiFi 6E AX3000 Трёхдиапазонный | ⚠️ Частичная |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (как выше) | WiFi 6E AX3000 Трёхдиапазонный | ⚠️ Частичная |
| AWUS036AX | Realtek RTL8832BU | Встроенный rtw89_8852bu (ядро 6.17+); на старых ядрах — DKMS-драйвер от сообщества | WiFi 6 AX1800 Двухдиапазонный | ✅ Работает (ядро 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | Встроенный rtw89_8852bu (ядро 6.17+; как у AX) | WiFi 6 AX1800 Двухдиапазонный | ✅ Работает (ядро 6.17+) |

> **Примечание**: производство AWUS036ACHM (MT7610U) прекращено, и он больше не представлен на странице продуктов Yopitek. В статье рассматриваются только доступные в настоящее время продукты.

---

## 3. AWUS036ACM (MT7612U) — ⭐ Лучшая рекомендация {#acm}

### Статус Soft AP: ✅ Полная поддержка

MT7612U — самый стабильный чипсет для Soft AP в текущей линейке ALFA. Его драйвер `mt76x2u` входит в официальное ядро Linux с 2018 года (ядро 4.19), а значит, работает «из коробки» на любой достаточно актуальной системе — **никаких `git clone`, никаких `dkms`, никакой перекомпиляции после обновления ядра.**

### Ключевые преимущества

- **Двойная поддержка WPA2 + WPA3**: встроенный в ядро драйвер MediaTek нативно поддерживает WPA3 SAE — преимущество, с которым драйверы Realtek не могут сравниться
- **Поддержка виртуальных интерфейсов VIF**: режимы AP + Managed + Monitor одновременно на одном адаптере — не нужно покупать вторую карту. Раздавайте сеть и одновременно отслеживайте беспроводной эфир
- **Сверхнизкое энергопотребление**: максимум ~400mA, идеально для Raspberry Pi (подсистема USB в Pi 4 выдаёт в сумме лишь 1200mA)
- **Кроссплатформенность**: широко проверен на Kali Linux 2022.x–2025.x, Ubuntu 22.04/24.04, Debian 11/12 и Raspberry Pi OS (Pi 3B+, 4, 5)

### Правильная конфигурация hostapd (MT7612U)

Следующие флаги возможностей проверены годами тестирования в сообществе (morrownr/USB-WiFi). **Они должны точно соответствовать фактическим аппаратным возможностям MT7612U:**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ Самая распространённая ошибка

Если `ht_capab` содержит флаги возможностей, которые MT7612U фактически не поддерживает (особенно при принудительном включении некоторых конфигураций HT40 через USB 2.0), hostapd молча аварийно завершится с крайне малоинформативными сообщениями об ошибке. **Используйте только проверенную комбинацию флагов выше — не копируйте настройки других чипсетов, например RTL8812AU.** (Источник: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### Отзывы сообщества

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> *(Перевод: «Alfa AWUS036ACM отлично работает с оборудованием Raspberry Pi. Я тестировал Alfa AWUS036ACM со множеством разных компьютеров и дистрибутивов Linux. По моему мнению, это выдающийся USB WiFi-адаптер.»)*
> — **morrownr**, мейнтейнер самой авторитетной базы знаний сообщества Linux USB WiFi на GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> *(Перевод: «Этот адаптер безупречно справляется с режимом monitor и инжекцией пакетов. Очень стабилен в Linux на штатных ядрах, не нужно компилировать сторонние драйверы.»)*
> — отзыв пользователя eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> *(Перевод: «ACM немного универсальнее и проще в настройке для режима AP.»)*
> — ветка обсуждения GitHub issue #2

---

## 4. AWUS036ACH (RTL8812AU) — Работает, но с компромиссами {#ach}

### Статус Soft AP: ⚠️ Условная поддержка

RTL8812AU — самый знаковый чипсет ALFA для тестирования на проникновение и давний фаворит сообщества Kali Linux. Функция Soft AP на нём действительно работает — базовая точка доступа создаётся без проблем, — но архитектура внешнего (out-of-kernel) драйвера Realtek накладывает ряд постоянных ограничений:

### Известные ограничения

1. **Нет поддержки WPA3**: хотя драйвер RTL8812AU заявляет поддержку WPA3, многие пользователи подтвердили, что на деле она не работает. **Только WPA2-PSK.**
2. **Нет поддержки VIF**: невозможно одновременно запустить режимы AP + Monitor на одной карте. Если нужны AP и мониторинг, придётся использовать два отдельных адаптера.
3. **Проблемы драйвера в Kali Linux 2025.x**: последний драйвер aircrack-ng/rtl8812au в новейшей Kali имеет проблемы совместимости — нужно откатиться к определённому старому коммиту (`63cf0b4`). Ситуация может улучшиться с встроенным драйвером rtw88 в ядре 6.13+.
4. **Высокое энергопотребление**: максимум ~800mA — на Raspberry Pi с несколькими подключёнными USB-устройствами это может вызывать нестабильность системы. Используйте USB-хаб с внешним питанием.

### Конфигурация hostapd (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### Установка драйвера (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### Отзывы сообщества

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> *(Перевод: «Я могу поставить вместо него RTL8812AU (AWUS036AC) и выполнить 'sudo service hostapd restart && sudo service dnsmasq restart' — всё отлично работает.»)*
> — пользователь GitHub issue #2

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> *(Перевод: «Адаптеры на RTL8812AU — режим AP работает, но по сравнению с MediaTek вы теряете поддержку WPA3 и VIF.»)*
> — технические заметки morrownr

### Вердикт по ACH

Если у вас уже есть AWUS036ACH, он может служить Soft AP (базовая функция точки доступа работает). Но если вы ещё не купили адаптер и ваша основная цель — Soft AP, **берите ACM.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — Действовать с осторожностью {#axml}

### Статус Soft AP: ⚠️ Частичная поддержка — известные проблемы прошивки/драйвера

AWUS036AXML и AWUS036AXM — трёхдиапазонные флагманы ALFA стандарта WiFi 6E, охватывающие 2.4 GHz, 5 GHz и новый диапазон 6 GHz. Их встроенный драйвер `mt7921u` присутствует в ядре начиная с версии 5.18, а поддержка режима AP официально добавлена в 5.19. Однако чип MT7921AUN также интегрирует Bluetooth 5.2 — что стало главной головной болью сообщества в 2024–2025 годах.

### Версии ядра для режима AP: ключевые вехи

| Режим | Минимальное ядро |
|------|---------------|
| Managed (обычный WiFi) | 5.18+ |
| **Режим AP (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Известные проблемы и решения

#### Проблема 1: помехи Bluetooth вызывают сбои WiFi

На ядрах 6.6+ изменения в подсистеме BT вызывают периодические сбои WiFi с mt7921u. Воспроизводимость зависит от системного окружения. **Самый эффективный обходной путь — отключить драйвер btusb:**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### Проблема 2: устаревшая прошивка

Если прошивка MediaTek в системе слишком старая, адаптер может распознаваться некорректно. Установите прошивку от ноября 2024 года или новее:

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### Проблема 3: требования к версии hostapd

Некоторые пользователи сообщают, что для полной поддержки режима AP WiFi 6 приходится компилировать hostapd из git. Версии из системного менеджера пакетов могут быть неполными.

#### Проблема 4: аномалия отображения мощности передачи (Tx Power) в режиме AP

`iw` показывает всего 3 dBm без возможности регулировки, но на самом деле чип имеет встроенный усилитель — это проблема отображения в драйвере ядра, а не аппаратное ограничение.

#### Проблема 5: проблемы режима monitor на некоторых версиях ядра

По состоянию на декабрь 2025 года ядро 6.18 и некоторые более ранние версии драйвера mt7921u имеют проблемы с режимом monitor.

### Отзыв сообщества

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> *(Перевод: «У меня Alfa AXML работает как AP на хосте RPi3B с ArchLinux ARM aarch64. Это самый стабильный mt7921 в моей коллекции. Правда, hostapd у меня собран из git.»)*
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Вердикт по AXML/AXM

Выбирайте их, если вам нужен диапазон 6 GHz стандарта WiFi 6E и вы готовы время от времени подстраивать настройки. **Для производственных сред, требующих абсолютной стабильности Soft AP, выбирайте ACM.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Работает для Soft AP на ядре 6.17+ {#ax}

### Статус Soft AP: ✅ Работает на ядре 6.17+ (на более старых ядрах нужен DKMS-драйвер от сообщества)

В наших тестах на ASUS GX10 (Ubuntu 24.04 ARM64, ядро 6.17) со встроенным драйвером `rtw89_8852bu` AWUS036AX и AWUS036AXER (один чип, один драйвер) ведут себя одинаково, а Soft AP работает и на 2,4 ГГц, и на 5 ГГц.

**Результаты тестов (ядро 6.17):**

1. **Режим AP**: работают и 2,4 ГГц (802.11n), и 5 ГГц (VHT 80 МГц)
2. **VIF (STA + AP)**: работает — клиентское подключение и интерфейс AP одновременно на одном канале
3. **WPA3-SAE AP**: работает в 2.4 ГГц (iPhone 15 Pro подключился, MFP включён; 5 ГГц не тестировался)
4. **Monitor / инъекция**: сильный приём в режиме monitor на 2,4 и 5 ГГц; инъекция на 2,4 ГГц: AX 96% / AXER 73%, 5 ГГц доступен; сквозной захват WPA-handshake выполнен успешно
5. **Не поддерживается**: IBSS, Mesh, active monitor

**Оговорки:**

- **Версия ядра — обязательное условие**: `rtw89_8852bu` входит в ядро начиная с 6.17. На более старых ядрах нужен DKMS-драйвер от сообщества (rtl8852bu): с ним режим monitor может быть ограничен, а VIF не поддерживается.
- **Режим USB**: некоторые экземпляры могут определяться в режиме CD-ROM (`0bda:1a2b`) и требовать `usb_modeswitch -v 0bda -p 1a2b -K`; наш тестовый экземпляр определился сразу как WLAN-адаптер.
- **Случаи в сообществе**: отчётов о Soft AP на этом чипсете пока меньше, чем для MT7612U и RTL8812AU.

> Результат тестов Yopitek (ASUS GX10, ядро 6.17): со встроенным драйвером AWUS036AX / AWUS036AXER имеют сильный приём в режиме monitor и рабочую инъекцию пакетов, поэтому подходят и для тестирования на проникновение. Ограниченная поддержка monitor относится только к старым ядрам с DKMS-драйвером от сообщества.
>
> Обновление: на штатном ядре 6.16 и новее (проверено на 6.17) у AWUS036AXML работают режим monitor, AP, WPA3 и VIF, но тест инжекции пакетов не пройден (aireplay-ng --test: Found 0 APs / No Answer). Причина — регрессия mac80211 chanctx, а не сам чип. Если нужна инжекция, используйте AWUS036ACH, EACS, ACS или AX.

---

## 7. Матрица совместимости платформ {#compat-matrix}

### AWUS036ACM (MT7612U)

| Платформа | Soft AP | Примечания |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel, plug-and-play, ядро 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, без настройки, используйте LTS |
| Debian 11 / 12 | ✅ | In-kernel, стабильно |
| Raspberry Pi 4 (RPi OS) | ✅ | Минимальное энергопотребление (400mA), многолетняя проверка morrownr. Предпочтителен порт USB 3.0 на Pi 4 |
| Raspberry Pi 5 (RPi OS) | ✅ | Тот же драйвер, что и для Pi 4, стабильно |

### AWUS036ACH (RTL8812AU)

| Платформа | Soft AP | Примечания |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Нужен внешний драйвер; для 2025.x требуется коммит `63cf0b4`. С rtw88 в ядре 6.13+ возможно улучшение |
| Ubuntu 22.04 / 24.04 | ⚠️ | Может потребоваться ручная установка драйвера rtw88 или aircrack-ng |
| Debian 11 / 12 | ⚠️ | То же, что выше |
| Raspberry Pi 4 | ⚠️ | Работает, но высокое энергопотребление (800mA); используйте USB-хаб с внешним питанием |
| Raspberry Pi 5 | ⚠️ | То же; различия USB-контроллера Pi 5 могут влиять на работу |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Платформа | Soft AP | Примечания |
|----------|---------|-------|
| Kali Linux 2022.x (ядро 5.18+) | ✅ | Отключите btusb, обновите прошивку |
| Kali Linux 2024.x / 2025.x | ⚠️ | Конфликт BT/WiFi на ядре 6.11+, нестабильно |
| Ubuntu 24.04 (ядро 6.8+) | ⚠️ | Проблемы зафиксированы в конце 2024 года |
| Ubuntu 25.04 / CachyOS (ядро 6.14+) | ✅ | Plug-and-play, заметное улучшение на новых ядрах |
| Debian 12 | ⚠️ | Зависит от версии ядра |
| Raspberry Pi 4 / 5 | ⚠️ | Есть успешные случаи, но проверьте прошивку и отключите BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Платформа | Soft AP | Примечания |
|----------|---------|-------|
| Kali Linux | ✅ | Встроенный rtw89_8852bu на ядре 6.17+; на более старых ядрах нужен DKMS-драйвер от сообщества |
| Ubuntu / Debian | ✅ | Для Ubuntu 24.04 нужно ядро HWE 6.17+ (на GA 6.8 / HWE 6.14 нужен DKMS-драйвер от сообщества); для Debian нужно ядро 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | На Pi не проверялось; на ядрах ниже 6.17 нужен DKMS-драйвер от сообщества |

---

## 8. Полное руководство по настройке Soft AP (AWUS036ACM) {#setup-guide}

Ниже приведено полное пошаговое руководство по настройке Soft AP в диапазоне 5GHz с AWUS036ACM на Raspberry Pi 4.

### Шаг 1: проверка обнаружения адаптера и драйвера

```bash
# Confirm the adapter is detected
lsusb | grep MediaTek
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check driver loaded
dmesg | grep mt76
# Expected: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# Confirm AP mode support
iw list | grep -A 10 "Supported interface modes"
# Check that output includes "* AP"
```

### Шаг 2: установка необходимых пакетов

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Шаг 3: настройка hostapd

Создайте файл `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### Шаг 4: настройка dnsmasq (DHCP)

Создайте файл `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Шаг 5: статический IP и NAT

```bash
# Assign static IP to wlan0
sudo ip addr add 192.168.10.1/24 dev wlan0

# Enable IP forwarding
sudo sysctl net.ipv4.ip_forward=1

# Configure NAT (assuming eth0 is the upstream interface)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Persist iptables rules
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Шаг 6: запуск служб

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Check service status
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Enable auto-start on boot
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

После завершения найдите сети WiFi на телефоне или ноутбуке — вы должны увидеть SSID `Yupitek_AP`.

---

## 9. Устранение распространённых проблем {#troubleshooting}

### В1: hostapd аварийно завершается сразу после запуска

**Симптом**: `sudo systemctl status hostapd` показывает `exited` или `failed`

**Вероятная причина**: `hostapd.conf` содержит флаги возможностей, которые чипсет не поддерживает

**Решение**: удалите лишние флаги. Для MT7612U (ACM) самый надёжный путь — использовать проверенную конфигурацию из раздела 3. **Не копируйте ht_capab с других чипсетов.**

---

### В2: клиенты подключаются, но не имеют доступа к интернету

**Симптом**: WiFi подключён, IP получен, но `ping 8.8.8.8` не получает ответа

**Что проверить**:

```bash
# 1. Check IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# 2. Check NAT rules exist
sudo iptables -t nat -L POSTROUTING -v
# Should see MASQUERADE rule

# 3. Confirm upstream interface is working
ping -I eth0 8.8.8.8
```

---

### В3: точка доступа 5GHz не видна или работает нестабильно

**Возможные причины**:

1. **Использование каналов DFS (100–144)**: MT7612U / MT7610U не поддерживают DFS — используйте каналы UNII-1 (36–48)
2. **Недостаточная мощность передачи**: убедитесь, что антенны плотно закручены на разъёмах RP-SMA
3. **Недостаточное питание USB** (Raspberry Pi): используйте официальный блок питания 5A или USB-хаб с внешним питанием

---

### В4: hostapd постоянно перезапускается на Raspberry Pi

**Симптом**: `dmesg` показывает частые сообщения о сбросе USB

**Вероятная причина**: недостаточное питание порта USB (особенно с высокопотребляющим чипсетом AWUS036ACH, максимум 800mA)

**Решение**:
- Используйте официальный блок питания Pi 5A
- Используйте USB-хаб с внешним питанием
- Подключите адаптер к порту USB 3.0 (только Pi 4)

---

### В5: WiFi на AWUS036AXML/AXM внезапно пропадает или не запускается

**Вероятная причина**: подсистема Bluetooth создаёт помехи WiFi (в MT7921AUN встроен BT 5.2)

**Решение**: навсегда отключите драйвер Bluetooth

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Технический анализ: VIF, WPA3, каналы DFS {#technical}

### VIF (виртуальный интерфейс): одна карта — несколько ролей

VIF (Virtual Interface) позволяет одному физическому адаптеру одновременно работать с несколькими логическими интерфейсами. Например, один интерфейс подключается к вышестоящему маршрутизатору (режим managed), а другой работает как AP (режим master) для других устройств.

Три типичных сценария:

| Сценарий | Нужен VIF? | Лучший адаптер |
|----------|--------------|--------------|
| Базовая NAT-маршрутизация (eth0 вверх + wlan AP) | ❌ Нет | Любой адаптер с поддержкой AP |
| Беспроводной мост (приём WiFi + WiFi AP одновременно) | ✅ Да | ACM (MT7612U) |
| Monitor + AP одновременно (исследования безопасности / Rogue AP) | ✅ Да | ACM (MT7612U) |

**Практический пример VIF (MT7612U):**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

VIF полностью поддерживают только встроенные в ядро драйверы MediaTek (mt76x2u, mt7921u). У внешних драйверов Realtek такой возможности по сути нет — если вам нужны AP + Monitor одновременно, придётся использовать два отдельных адаптера.

---

### Сравнение поддержки WPA3

| Чипсет | Соответствующая модель | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Нативная поддержка SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Нативная поддержка SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Поддержка заявлена, но не работает |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ Проверено на ядре 6.17 (`sae_pwe=0`, MFP включён) |

---

### Выбор канала для Soft AP 5GHz: избегайте DFS

Каналы DFS (Dynamic Frequency Selection) (ch100–ch140) требуют обнаружения радаров на уровне ядра. MT7612U и подобные чипсеты не поддерживают DFS. Для режима AP в диапазоне 5GHz выбирайте:

| Диапазон | Рекомендуемые каналы | Причина |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Поддерживается всеми чипсетами; самый надёжный выбор |
| UNII-2 (DFS) | 52–144 | В основном не поддерживается; не рекомендуется |
| UNII-3 | 149–165 | Частичная поддержка (зависит от региона) |

---

## 11. Реальные примеры из сообщества {#real-cases}

### Случай 1: RPi4B + AWUS036ACM = долговременно стабильная домашняя AP 5GHz

**Источник**: база знаний morrownr/7612u на GitHub
**Сценарий**: morrownr давно использует RPi4B + AWUS036ACM как домашнюю AP 5GHz в паре со встроенным модулем 2.4GHz в Pi для двухдиапазонного обслуживания
**Результат**: долговременная стабильная работа без перезапусков, оценка «outstanding» (выдающийся)
**Конфигурация**: hostapd + dnsmasq + iptables NAT

### Случай 2: RPi3B+ + ACM — первоначальный сбой, исправлен

**Источник**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Проблема**: hostapd аварийно завершался при работе через USB 2.0 на RPi3B+
**Первопричина**: `ht_capab` содержал флаги HT40, не поддерживаемые в пределах пропускной способности USB 2.0
**Решение**: лишние флаги удалены; успешный запуск в Kali Linux

### Случай 3: Pi PwnBox + AWUS036ACH = Rogue AP для Red Team

**Источник**: GitHub koutto/pi-pwnbox-rogueap
**Сценарий**: платформа Rogue AP на RPi3B+: один RTL8812AU (AWUS036ACH) для AP, другой RT3070 (AWUS036NEH) для атак с инжекцией пакетов
**Ключевой вывод**: поскольку RTL8812AU не поддерживает VIF, потребовались два отдельных адаптера (в отличие от ACM, который справляется с обеими задачами на одной карте)

### Случай 4: стабильная AP на AWUS036AXML с RPi3B и ArchLinux ARM

**Источник**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Сценарий**: пользователь успешно запустил AWUS036AXML в режиме AP на RPi3B с ArchLinux aarch64
**Цитата**: «Это самый стабильный mt7921 в моей коллекции».
**Ключевые требования**: hostapd, собранный из git, + отключённый btusb

### Случай 5: AP на полной скорости с AWUS036ACHM (MT7610U, снят с производства) на Pi4

**Источник**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Проблема**: начальная конфигурация давала скорость соединения лишь 65 Mbps — намного ниже полной скорости AC в диапазоне 5GHz
**Решение**: добавлены корректные `vht_oper_chwidth=1` и `vht_oper_centr_freq_seg0_idx`; достигнута скорость соединения 433 Mbps
**Значение для ACM**: та же настройка параметров VHT критически важна и для MT7612U (ACM)

---

{{< faq >}}

## 12. Рекомендации по покупке и окончательный вердикт {#recommendations}

### Матрица быстрого решения

| Оценка | Модель | Кому подходит | Коротко |
|--------|-------|----------|-----------|
| 🥇 **Лучший выбор** | **AWUS036ACM** | Всем, особенно тем, кто впервые настраивает Soft AP | Стабилен на всех платформах, без хлопот |
| 🥈 Приемлемо | AWUS036ACH | Пользователям, у которых уже есть эта модель | Нужен драйвер, нет WPA3 |
| 🥉 Для опытных | AWUS036AXML | Тем, кому нужен WiFi 6E и кто готов повозиться | Преимущество 6GHz, нужны ручные исправления |
| ✅ Работает на ядре 6.17+ | AWUS036AX / AXER | AP Wi-Fi 6; monitor и инъекция тоже доступны | Встроенный драйвер; AP 2,4 / 5 ГГц и VIF проверены, WPA3 проверен в 2,4 ГГц |

### 🎯 Как выбрать

- **Нужна стабильная Soft AP на Kali / Ubuntu / Debian / Raspberry Pi 4 или 5?**
  → Берите **AWUS036ACM**, без вариантов.

- **Уже есть AWUS036ACH и хотите попробовать Soft AP?**
  → Работает, но только с WPA2, и потребуется установить драйвер. Если эти ограничения вас устраивают — вперёд.

- **Нужен WiFi 6E (диапазон 6 GHz) и готовы заниматься настройкой?**
  → AWUS036AXML — не забудьте отключить драйвер BT и убедиться, что ядро ≥ 6.6 LTS.

- **Основная задача — Soft AP, а не тестирование на проникновение?**
  → AWUS036ACM — единственный вариант с обширной проверкой сообществом на всех платформах.

---

### Заключение

Ключевой фактор при создании Soft AP — не скорость WiFi и не количество антенн, — **это поддержка режима AP драйвером чипсета.**

Среди всех изученных нами продуктов ALFA **AWUS036ACM (MT7612U)** — единственный адаптер, одновременно удовлетворяющий: in-kernel драйвер, нативный WPA3, виртуальные интерфейсы VIF, низкое энергопотребление и кроссплатформенная стабильность. Это золотой стандарт для Soft AP.

AWUS036ACH (RTL8812AU) подойдёт, если вы готовы мириться с ограничениями. У AWUS036AXML/AXM (MT7921AUN) большой потенциал, но драйвер всё ещё дорабатывается. AWUS036AX/AXER (RTL8832BU) хорошо работают на ядре 6.17+ со встроенным драйвером (AP, VIF и WPA3 проверены); на более старых ядрах нужен DKMS-драйвер от сообщества.

**Если вы впервые настраиваете Soft AP на Raspberry Pi или Kali Linux — выбирайте ACM. Вы не пожалеете.**

---

### Ссылки для покупки

- [AWUS036ACM — Лучший выбор Soft AP](/ru/products/alfa/awus036acm/)
- [AWUS036ACH — классический адаптер для пентеста](/ru/products/alfa/awus036ach/)
- [AWUS036AXML — трёхдиапазонный флагман WiFi 6E](/ru/products/alfa/awus036axml/)
- [Полная линейка ALFA Network](/ru/products/alfa/)

### Дополнительные материалы

- [AWUS036ACH и AWUS036ACM: полное сравнение драйверов чипсетов](/ru/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM: режимы IBSS и Mesh на Raspberry Pi](/ru/blog/)
- [morrownr/USB-WiFi — авторитетная база знаний о Linux USB WiFi](https://github.com/morrownr/USB-WiFi) (более 4,100 звёзд)
- [morrownr/7612u — справочник по MT7612U (включая руководство по Bridged AP на RPi4B)](https://github.com/morrownr/7612u)
- [DeepWiki — автоматически собираемая база знаний morrownr/USB-WiFi](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Источники данных

Статья основана на информации из следующих источников:
- **morrownr/USB-WiFi** — база знаний на GitHub (более 4,100 звёзд) с полными записями iw_list
- **morrownr/7612u** — руководство по Bridged AP на MT7612U для RPi4B
- **Трекер задач GitHub** — issue #2 (конфигурация AP для ACM), #476 (тестирование AP на AXML), Discussion #31 (AP на полной скорости с ACHM)
- **koutto/pi-pwnbox-rogueap** — пример реализации RogueAP на адаптере Alfa
- Страницы поддержки Linux авторизованного продавца **Rokland**
- Технические обзоры **Lab401** и рейтинги лучших решений для пентеста 2025 года
- **Официальный форум Raspberry Pi** — обсуждения совместимости USB WiFi с Pi 4/5
- **Существующие статьи блога Yopitek** — руководство по установке ACM в Китае, обзор AXML WiFi 6E, лучшие адаптеры для Kali Linux 2026

---

> **Теги**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> **Автор**: Yopitek Ltd — Авторизованный дистрибьютор ALFA Network в Тайване
>
> **Отказ от ответственности**: Данные исследования актуальны на май 2026 г. Ядра Linux и дистрибутивы продолжают развиваться; поддержка драйверов может меняться с новыми версиями. Перед развёртыванием проверьте версию ядра целевой платформы и совместимость драйвера.
>
> **Техническая поддержка**: по вопросам настройки Soft AP обращайтесь в службу технической поддержки Yopitek Taiwan. Вопросы о продуктах: [yupitek.com](https://yupitek.com/ru/).


## Источники

1. [AWUS036ACH vs AWUS036ACM: полное сравнение драйверов чипсетов](/zh-tw/blog/awus036ach-vs-awus036acm/)
2. [AWUS036ACM: режимы IBSS и Mesh на Raspberry Pi](/zh-tw/blog/)
3. [morrownr/USB-WiFi — репозиторий знаний о Linux USB WiFi](https://github.com/morrownr/USB-WiFi)
4. [morrownr/7612u — документация по MT7612U](https://github.com/morrownr/7612u)
5. [DeepWiki — база знаний morrownr/USB-WiFi](https://deepwiki.com/morrownr/USB-WiFi)
