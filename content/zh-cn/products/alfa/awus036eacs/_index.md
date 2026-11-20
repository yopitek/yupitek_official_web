---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 迷你 USB 无线网卡"
description: "ALFA AWUS036EACS，Realtek RTL8821CU，AC600 双频，USB 2.0 Nano 超轻薄，Bluetooth 4.2。内核 6.2 起内置 mainline rtw88_8821cu 驱动，GX10 实测 Monitor mode 与数据包注入两个频段均通过。"
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "蓝牙 4.2", "家用", "Windows"]
---

## 产品概述

AWUS036EACS 是 Alfa Network 专为家用与办公室设计的超小型 WiFi + Bluetooth 复合型 USB 无线网卡。采用 Realtek RTL8821CU 芯片，集成 AC600 双频 WiFi 与 Bluetooth 4.2，Nano 机身设计插入 USB 口后几乎不占空间。Windows 系统内置驱动支持，即插即用。支持 Soft AP 模式，可作为 WiFi 热点共享网络。在 Linux 上，内核 6.2 起已内置 mainline rtw88_8821cu 驱动。在 GX10（Ubuntu 24.04、内核 6.17）实测中，Monitor mode 与数据包注入在 2.4 GHz 和 5 GHz 均为 100%，端到端 WPA handshake 抓取成功，蓝牙与 Wi-Fi 可同时使用。

> ⚠️ **注意：** AWUS036EACS 原为 Windows 家用机型，在 Linux 上也可使用 mainline rtw88_8821cu 驱动（内核 6.2 及以上）。无 RP-SMA 接口，天线无法升级。

## 产品特色

- 802.11ac AC600 双频 WiFi + Bluetooth 4.2，单一 Nano USB 集成
- Windows 即插即用，内置驱动程序自动安装
- Soft AP 模式，可直接建立 WiFi 热点
- 超迷你设计，插入 USB 口几乎无感
- 双频：2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）
- 集成式 2 dBi 天线，无外接 RP-SMA 接口
- 适合台式电脑、嵌入式系统或家用 PC 同时需要 WiFi 与蓝牙的场景
- Bluetooth 4.2 支持音频流、键盘、鼠标等外接设备

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | Realtek RTL8821CU |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac（Wi-Fi 5） |
| 蓝牙 | BT 4.2（2.4 GHz） |
| 频段 | WiFi：2.4 GHz / 5 GHz；BT：2.4 GHz |
| 最大传输速率 | 802.11b：11 Mbps · 802.11g：54 Mbps · 802.11n：150 Mbps · 802.11ac：433 Mbps |
| 综合最高速率 | AC600（150 + 433 Mbps） |
| 天线 | 集成式 2 dBi（固定，无 RP-SMA） |
| USB 接口 | USB 2.0 |
| 输出功率 | 典型值 17 dBm |
| 接收灵敏度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 无线加密 | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| 工作温度 | −10°C 至 60°C |
| 外形规格 | Nano 超薄型 |
| 产地 | 台湾 |

## 操作系统支持

| 操作系统 | 支持状态 | 备注 |
|---------|---------|------|
| Windows XP–10 | ✅ 支持 | 内置驱动，即插即用。Windows 11 兼容性请参阅 Alfa 驱动页面。 |
| macOS | ⚠️ 有限支持 | 确切版本待确认，不支持 Apple Silicon。 |
| Ubuntu / Linux | ✅ 内核 6.2 及以上 | 内核内置 mainline rtw88_8821cu 驱动，无需另外安装（GX10、Ubuntu 24.04、内核 6.17 实测）。 |
| Kali Linux | ✅ 支持 | 在 GX10（Ubuntu 24.04、内核 6.17）实测 Monitor mode 与数据包注入两个频段均为 100%，端到端 WPA handshake 抓取成功。Kali 实机未实测。 |
| NetHunter（Android） | ❌ 不建议 | RTL8821CU 未确认与 NetHunter 兼容。 |

## 硬件支持

| 硬件 | 支持状态 | 备注 |
|------|---------|------|
| Raspberry Pi | ⚠️ 未实测 | 未实测；内核 6.2 及以上已内置 mainline rtw88_8821cu 驱动。 |
| 台式机／笔记本电脑 | ✅ 支持 | 仅建议 Windows 系统使用。 |
| 嵌入式 / IoT（Windows） | ⚠️ 仅限 Windows | 迷你设计适合 Windows 嵌入式系统。 |

## 高级功能

| 功能 | 支持状态 |
|------|---------|
| Monitor Mode | ✅ 支持（GX10 实测：两个频段均为 100%） |
| 数据包注入 | ✅ 支持（GX10 实测：两个频段均为 100%） |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ✅ BT 4.2（可与 Wi-Fi 同时使用） |
| VIF | 🟡 部分支持（被动 monitor 与 managed 同频道并存；不支持独立双 VIF） |

## 包装内容

- 1× AWUS036EACS Nano 无线网卡

## 资源与链接

| 资源 | 链接 |
|------|------|
| 原厂产品页面 | https://www.alfa.com.tw/products/awus036eacs_1 |
| 原厂技术文档 | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## 产品规格书下载

规格书即将提供，敬请期待。

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## 可搭配的天线配件

所有 ALFA USB 无线网卡均采用标准 RP-SMA 接头，可搭配以下外接天线提升信号范围与增益：

| 天线型号 | 频段 | 增益 | 类型 |
|---------|------|------|------|
| [ALFA APA-M04](/zh-cn/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室内面板定向 |
| [ALFA APA-M25](/zh-cn/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | 双频室内面板 |
| [ALFA APA-M25-6E](/zh-cn/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | 三频室内面板 |
| [ARS 25-57A](/zh-cn/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | 户外全向 |
| [ARS NT5B7](/zh-cn/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | 全向 |


{{< alert >}}
需要询问产品报价?请来信[与我们联系](/zh-cn/contact/)
{{< /alert >}}
