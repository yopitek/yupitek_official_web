---
title: "ALFA AWUS036AX — Wi-Fi 6 双频 USB 无线网卡"
description: "ALFA AWUS036AX，Realtek RTL8832BU 芯片，Wi-Fi 6（802.11ax）双频 2.4+5 GHz，最高 1200 Mbps，USB 3.0。注意：此为 Wi-Fi 6，非 Wi-Fi 6E，不含 6 GHz 频段。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "USB 3.0", "802.11ax", "双频", "OFDMA", "MU-MIMO"]
---

## 产品概述

AWUS036AX 采用 Realtek RTL8832BU 芯片，支持 Wi-Fi 6（802.11ax）双频（2.4 GHz + 5 GHz），最高传输速率 1200 Mbps，支持 MU-MIMO 2×2 与 OFDMA 技术。天线为一体化设计（不可拆卸）。

> ⚠️ **重要提示：** 此型号为 **Wi-Fi 6**，并非 Wi-Fi 6E，**不含 6 GHz 频段**。如需 6 GHz 频段，请选择 AWUS036AXML 或 AWUS036AXM。此型号在内核 < 6.12 时 Monitor mode 受限，**不建议用于 Linux 安全研究**。

> **注意：** 所有 ALFA 无线网卡对 macOS 支持有限。macOS 11 Big Sur 及以上版本和 Apple Silicon（M1/M2/M3）均**不支持**。最高支持 Intel Mac 上的 macOS 10.15 Catalina。

## 产品特色

- Wi-Fi 6（802.11ax）双频：2.4 GHz + 5 GHz
- Realtek RTL8832BU 芯片
- 最高 1200 Mbps 传输速率
- MU-MIMO 2×2
- OFDMA 技术
- USB 3.0 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ 不含 6 GHz 频段

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | Realtek RTL8832BU |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6）|
| 频段 | 2.4 GHz + 5 GHz（无 6 GHz）|
| 最高传输速率 | 1200 Mbps |
| MIMO | MU-MIMO 2×2 |
| 天线 | 一体化（不可拆卸）|
| USB 接口 | USB 3.0 Type-A |
| 无线安全 | WPA3 / WPA2 / WPA / WEP |

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---------|------|------|
| Windows 10/11 | ✅ 支持 | 从 Alfa 官网下载驱动 |
| macOS | ❌ 不支持 | 不支持 macOS 11+ 及 Apple Silicon |
| Ubuntu | ⚠️ 需安装驱动 | 内核 ≥ 6.14（Ubuntu 24.10+）已内置；旧版需手动 DKMS |
| Kali Linux | ⚠️ 有限 | 内核 < 6.12 时 Monitor mode 受限；不建议用于渗透测试 |
| NetHunter | ⚠️ 有限 | 依内核版本 |

## 硬件支持

| 硬件 | 状态 | 备注 |
|------|------|------|
| Raspberry Pi 4/5 | ⚠️ 需安装驱动 | Pi OS 内核 < 6.14 需手动安装 |
| 台式机/笔记本 | ✅ 支持 | 标准 USB-A |

## 高级功能

| 功能 | 状态 |
|------|------|
| Monitor Mode | ⚠️ 有限（建议内核 ≥ 6.12）|
| Packet Injection | ⚠️ 有限 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ❌ 无 |

## 包装内容

- 1× AWUS036AX 无线网卡

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.alfa.com.tw/ |
| Linux 驱动（RTL8832BU）| https://github.com/morrownr/rtl8852bu-20240418 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036AX 规格书](/docs/alfa/AWUS036AX_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ax_image_1.png" alt="ALFA AWUS036AX" />
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
需要询价？[联系我们](/zh-cn/contact/)，我们提供详细采购建议。
{{< /alert >}}
