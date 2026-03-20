---
title: "ALFA AWUS036AXER — Wi-Fi 6 超薄 Nano 无线网卡"
description: "ALFA AWUS036AXER，Realtek RTL8832BU 芯片，Wi-Fi 6 双频，Nano 超薄设计（~65×24×10mm），适合日常使用。不建议用于 Kali Linux 安全研究。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "802.11ax", "超薄", "USB 3.2", "随身型", "Nano"]
---

## 产品概述

AWUS036AXER 采用 Realtek RTL8832BU 芯片，支持 Wi-Fi 6（802.11ax）双频（2.4 GHz + 5 GHz），最高传输速率 1800 Mbps（2.4 GHz: 573 Mbps + 5 GHz: 1200 Mbps）。超薄 Nano 设计（约 65 × 24 × 10 mm，约 10g），适合随身携带使用。

> ⚠️ **注意：** Nano 外型设计，**无 RP-SMA 接头**，天线无法升级。**不建议用于 Kali Linux 或安全研究**。

> **注意：** 所有 ALFA 无线网卡对 macOS 支持有限。macOS 11 Big Sur 及以上版本和 Apple Silicon（M1/M2/M3）均**不支持**。最高支持 Intel Mac 上的 macOS 10.15 Catalina。

## 产品特色

- Wi-Fi 6（802.11ax）双频：2.4 GHz + 5 GHz
- Realtek RTL8832BU 芯片
- 最高 1800 Mbps
- 超薄 Nano 设计（~65×24×10mm，~10g）
- USB 3.2 Gen 1 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ 无 RP-SMA 接头，天线不可拆卸

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | Realtek RTL8832BU |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6）|
| 频段 | 2.4 GHz + 5 GHz（无 6 GHz）|
| 最高传输速率 | 1800 Mbps（2.4G: 573 Mbps + 5G: 1200 Mbps）|
| 天线 | 一体化 Nano（无 RP-SMA）|
| USB 接口 | USB 3.2 Gen 1 Type-A |
| 尺寸 | ~65 × 24 × 10 mm，~10g |
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
| Monitor Mode | ⚠️ 有限 |
| Packet Injection | ⚠️ 有限 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ❌ 无 |

## 包装内容

- 1× AWUS036AXER Nano 无线网卡

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.alfa.com.tw/ |
| Linux 驱动（RTL8832BU）| https://github.com/morrownr/rtl8852bu-20240418 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036AXER 规格书](/docs/alfa/AWUS036AXER_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axer_image_1.png" alt="ALFA AWUS036AXER" />
{{< /gallery >}}

---

{{< alert >}}
需要询价？[联系我们](/zh-cn/contact/)，我们提供详细采购建议。
{{< /alert >}}
