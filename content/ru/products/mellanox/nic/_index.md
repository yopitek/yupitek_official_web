---
title: "Сетевые адаптеры NVIDIA Mellanox ConnectX (NIC)"
description: "Сравнение сетевых адаптеров NVIDIA Mellanox ConnectX-4 Lx, ConnectX-5, ConnectX-6 Dx/Lx и ConnectX-7. Варианты на 10G, 25G, 50G, 100G, 200G и 400G для шин PCIe Gen3/4/5."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Сетевые адаптеры Mellanox / NVIDIA ConnectX: от 10G до 400G

Сетевые адаптеры NVIDIA Mellanox ConnectX обеспечивают лучшую в отрасли пропускную способность и минимальную задержку для корпоративных серверов и вычислительных кластеров ИИ. Ниже представлен полный каталог моделей, поставляемых компанией Yupitek, с разделением по скоростным характеристикам.

---

## Сетевые карты 10GbE / 25GbE

Оптимальное решение для стандартных корпоративных серверов, виртуализации (VMware ESXi) и высокопроизводительных систем хранения данных (NAS).

### Модель 10G

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Монтажная планка |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | Два | 10GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Стандартная |

### Модели 25G

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*Двухпортовый сетевой адаптер NVIDIA ConnectX-4 Lx 25GbE*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*Двухпортовый сетевой адаптер NVIDIA ConnectX-5 25GbE*

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Планка / Форм-фактор | Особенности |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | Два | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Стандартная | Стандартная карта PCIe |
| **MCX4121A-ACUT** | ConnectX-4 Lx | Два | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Стандартная | Поддержка UEFI |
| **MCX512A-ACAT** | ConnectX-5 EN | Два | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Стандартная | Улучшенный RoCEv2 |
| **MCX512A-ACUT** | ConnectX-5 EN | Два | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Стандартная | UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | Два | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | Стандартная | Secure Boot, без шифрования|
| **MCX623432AS-ADAB**| ConnectX-6 Lx | Два | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | OCP 3.0 (винты) | Secure Boot, OCP 3.0 |

---

## Сетевые карты 50GbE / 100GbE

Разработаны для высокоскоростных систем хранения данных NVMe over Fabrics (NVMe-oF), гиперконвергентной инфраструктуры (HCI) и серверов баз данных.

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*Сетевой адаптер NVIDIA ConnectX-5 100GbE*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*Двухпортовый сетевой адаптер NVIDIA ConnectX-6 Dx 100GbE*

### Модель 50G

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Монтажная планка |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | Один | 50GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | Стандартная |

### Модели 100G

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Форм-фактор | Особенности |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | Один | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | Стандартная PCIe | Стандартный адаптер 100G |
| **MCX555A-ECAT** | ConnectX-5 VPI | Один | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Стандартная PCIe | EDR IB и 100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | Два | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | Стандартная PCIe | Двухпортовый 100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | Два | 100GbE | PCIe 4.0 x16 | QSFP28 | Ethernet | Стандартная PCIe | Интерфейс PCIe 4.0|
| **MCX556A-ECAT** | ConnectX-5 VPI | Два | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Стандартная PCIe | Двухпортовый EDR IB |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| Два | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | Стандартная PCIe | PCIe 4.0, два порта EDR |
| **MCX653105A-ECAT**| ConnectX-6 VPI | Один | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Стандартная PCIe | HDR100 IB и 100GbE|
| **MCX653106A-ECAT**| ConnectX-6 VPI | Два | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | Стандартная PCIe | HDR100 IB и 100GbE|
| **MCX623106AN-CDAT**| ConnectX-6 Dx | Два | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | Стандартная PCIe | 100G, два порта SFP56/QSFP56|
| **MCX623436AN-CDAB**| ConnectX-6 Dx | Два | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | OCP 3.0 (винты) | Форм-фактор OCP |

---

## Сетевые карты 200GbE / 400GbE

Флагманские сетевые карты для серверов с графическими процессорами ИИ (например, архитектур NVIDIA HGX/DGX), высокочастотного трейдинга (HFT) и магистральных сетей HPC.

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*Сетевой адаптер NVIDIA ConnectX-7 400G OSFP*

### Модели 200G

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Форм-фактор | Особенности |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | Один | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | Стандартная PCIe | HDR IB и 200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | Два | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | Стандартная PCIe | Двухпортовый HDR/200G|
| **MCX623105A-VDAT**| ConnectX-6 Dx | Один | 200GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | Стандартная PCIe | Однопортовый 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | Один | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | Стандартная PCIe | NDR200, Socket Direct|
| **MCX755106AS-HEAT**| ConnectX-7 VPI | Два | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | Стандартная PCIe | 1 порт IB, 2-й порт VPI|
| **MCX753436MS-HEAB**| ConnectX-7 VPI | Два | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0 (винты) | OCP Multi-Host / Socket Direct|

### Модели 400G

| Артикул (P/N) | Поколение / Чипсет | Порты | Скорость | Слот PCIe | Разъем | Протокол | Форм-фактор | Особенности |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | Один | 400 Гбит/с| PCIe 5.0 x16 | OSFP | InfiniBand | Стандартная PCIe | NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | Один | 400 Гбит/с| PCIe 5.0 x16 | OSFP | InfiniBand | Стандартная PCIe | NDR OSFP, поддержка Socket Direct|

---

## Рекомендации по выбору

При выборе сетевого адаптера ConnectX обратите внимание на следующие параметры:

### 1. Поддерживаемые протоколы (VPI или EN)
- **Адаптеры EN** поддерживают только сети Ethernet.
- **Адаптеры VPI (Virtual Protocol Interconnect)** поддерживают программную настройку: их можно использовать как в сетях InfiniBand, так и в Ethernet. Это обеспечивает максимальную гибкость внедрения.

### 2. Требования к пропускной способность шины PCIe
Убедитесь, что версия и количество линий слота PCIe на сервере соответствуют требованиям карты для работы на полной скорости:
- Для работы двухпортовой карты 100G на полной скорости на обоих портах одновременно требуется слот PCIe 4.0 x16.
- Карты PCIe 4.0 обратно совместимы со слотами PCIe 3.0, однако в этом случае пропускная способность будет ограничена лимитом PCIe 3.0 (примерно 64 Гбит/с для x8 и 128 Гбит/с для x16).

### 3. Форм-фактор OCP 3.0 против стандартного PCIe
Модели с суффиксами `-ADAB`, `-CDAB`, `-HEAB` выполнены в форм-факторе **OCP NIC 3.0**. Они устанавливаются в специальные слоты на серверах (распространены в современных поколениях Supermicro, Dell, HPE и Lenovo) и физически несовместимы со стандартными слотами PCIe.

---

{{< alert >}}
Нужно коммерческое предложение? Пожалуйста, [свяжитесь с нами](/ru/contact/).
{{< /alert >}}
