---
title: "ALFA AWUS036AXML — Wi-Fi 6E USB-C 三频无线网卡"
description: "ALFA AWUS036AXML，MediaTek MT7921AUN 芯片，Wi-Fi 6E 三频（2.4/5/6 GHz），USB-C 接口，Bluetooth 5.2，支持 Kali Linux Monitor Mode。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "三频", "蓝牙 5.2", "6GHz", "Kali Linux"]
---

{{< alert "warning" >}}
**合法使用声明**：Monitor Mode 与 Packet Injection 功能仅供授权的安全测试、教育研究及合法渗透测试使用。请确认已获得目标网络的明确授权。
{{< /alert >}}

## 产品概述

AWUS036AXML 搭载 MediaTek MT7921AUN 芯片，支持 Wi-Fi 6E 三频（2.4 GHz / 5 GHz / 6 GHz），最高传输速率达 3000 Mbps，内置 Bluetooth 5.2。采用 USB-C 接口，附赠 2-in-1 USB-C/USB-A 传输线，完美适配现代笔记本与台式机。

> **注意：** 所有 ALFA 无线网卡对 macOS 支持有限。macOS 11 Big Sur 及以上版本和 Apple Silicon（M1/M2/M3）均**不支持**。最高支持 Intel Mac 上的 macOS 10.15 Catalina。

## 产品特色

- Wi-Fi 6E 三频：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN 芯片
- 最高 3000 Mbps 传输速率
- Bluetooth 5.2（复合芯片）
- USB-C 接口（USB 3.2 Gen 1，5 Gbps）
- 附赠 2-in-1 USB-C/USB-A 传输线
- 1× RP-SMA 可拆卸天线
- 附赠屏幕夹架
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode（内核 ≥ 5.18）

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | MediaTek MT7921AUN |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 频段 | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| 最高传输速率 | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · 合计: 3000 Mbps |
| 蓝牙 | BT 5.2（复合芯片）|
| 天线接头 | 1× RP-SMA female（可拆卸）|
| USB 接口 | USB 3.2 Gen 1 Type-C（5 Gbps）|
| 传输线 | 2-in-1 USB-C/USB-A |
| 无线安全 | WPA3 / WPA2 / WPA / WEP / WPS |
| 产地 | 台湾 |

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---------|------|------|
| Windows 10 | ✅ 支持 | 仅 2.4 GHz 与 5 GHz；Windows 10 不支持 6 GHz |
| Windows 11 | ✅ 支持 | 完整三频，含 6 GHz |
| macOS | ❌ 不支持 | 不支持 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支持 | 内核内置 mt7921u，内核 ≥ 5.18（Ubuntu 22.10+）|
| Kali Linux | ✅ 支持 | Monitor mode ≥ 内核 5.18；主动 monitor mode ≥ 6.12；支持 packet injection |
| NetHunter（Android）| ⚠️ 部分支持 | OTG；依内核版本 |

## 硬件支持

| 硬件 | 状态 | 备注 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支持 | 更新 Pi OS（内核 ≥ 5.18）；可能需复制固件文件 |
| 台式机/笔记本 | ✅ 支持 | USB-C 或附赠 2-in-1 传输线 |
| Mac（Intel）| ⚠️ 有限支持 | 最高 macOS 10.15 Catalina |

## 高级功能

| 功能 | 状态 |
|------|------|
| Monitor Mode | ✅ 支持（内核 ≥ 5.18；主动模式 ≥ 6.12）|
| Packet Injection | ✅ 支持 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ✅ BT 5.2 |
| VIF | ✅ 支持 |

## 包装内容

- 1× AWUS036AXML 无线网卡
- 1× 可拆卸双频天线
- 1× 2-in-1 USB-C/USB-A 传输线
- 1× 屏幕夹架

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方产品页面 | https://www.alfa.com.tw/products/awus036axml |
| 官方文档 | https://docs.alfa.com.tw/ |
| Linux 驱动（内核内置）| mt7921u — Linux 内核 ≥ 5.18 已内置 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036AXML 规格书](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
{{< /gallery >}}

---

## 可搭配的天线配件

所有 ALFA USB 无线网卡均采用标准 RP-SMA 接头，可搭配以下外接天线提升信号范围与增益：

| 天线型号 | 频段 | 增益 | 类型 |
|---------|------|------|------|
| [ALFA APA-M04](/zh-cn/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室内面板定向 |
| [ALFA APA-M25](/zh-cn/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | 双频室内面板 |
| [ALFA APA-M25-6E](/zh-cn/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | 三频室内面板 |
| [ARS 25-57A](/zh-cn/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | 户外全向 |
| [ARS NT5B7](/zh-cn/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | 全向 |


{{< alert >}}
需要询问产品报价?请来信[与我们联系](/zh-cn/contact/)
{{< /alert >}}
