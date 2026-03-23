---
title: "ALFA AWUS036AXM — Wi-Fi 6E 三频双天线无线网卡"
description: "ALFA AWUS036AXM，MediaTek MT7921AUN 芯片，Wi-Fi 6E 三频，USB-A L型接头，2× 5 dBi 天线，Bluetooth 5.2，适合 Kali Linux 渗透测试。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-A", "802.11ax", "三频", "蓝牙 5.2", "双天线", "Kali Linux"]
---

{{< alert "warning" >}}
**合法使用声明**：Monitor Mode 与 Packet Injection 功能仅供授权的安全测试、教育研究及合法渗透测试使用。请确认已获得目标网络的明确授权。
{{< /alert >}}

## 产品概述

AWUS036AXM 采用 MediaTek MT7921AUN 芯片，支持 Wi-Fi 6E 三频（2.4 GHz / 5 GHz / 6 GHz），最高传输速率达 3000 Mbps，内置 Bluetooth 5.2（含独立 BT 天线）。L 型 USB-A 接头可避免遮挡相邻 USB 端口。附赠 2 根 5 dBi RP-SMA 可拆卸天线。

> **注意：** 所有 ALFA 无线网卡对 macOS 支持有限。macOS 11 Big Sur 及以上版本和 Apple Silicon（M1/M2/M3）均**不支持**。最高支持 Intel Mac 上的 macOS 10.15 Catalina。

## 产品特色

- Wi-Fi 6E 三频：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN 芯片
- 最高 3000 Mbps 传输速率
- Bluetooth 5.2（含独立 BT 天线及 LED 指示灯）
- USB-A L 型接头（USB 3.2 Gen 1，5 Gbps）
- 2× RP-SMA female 可拆卸天线（5 dBi）
- WPA3/WPA2/WPA/WEP/WPS
- 支持 Kali Linux Monitor Mode + Packet Injection

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | MediaTek MT7921AUN |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 频段 | 2.4 GHz · 5 GHz · 6 GHz |
| 最高传输速率 | 3000 Mbps |
| 蓝牙 | BT 5.2（含独立天线）|
| 天线 | 2× RP-SMA female，2× 5 dBi 双频天线（可拆卸）|
| USB 接口 | USB 3.2 Gen 1 Type-A L 型（5 Gbps）|
| 无线安全 | WPA3 / WPA2 / WPA / WEP / WPS |

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---------|------|------|
| Windows 10 | ✅ 支持 | 2.4+5 GHz；6 GHz 需 Windows 11 |
| Windows 11 | ✅ 支持 | 完整三频含 6 GHz |
| macOS | ❌ 不支持 | 不支持 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支持 | 内核内置 mt7921u，内核 ≥ 5.18 |
| Kali Linux | ✅ 支持 | Monitor mode + packet injection；可能需固件文件 |
| NetHunter | ⚠️ 部分支持 | OTG；依内核版本 |

## 硬件支持

| 硬件 | 状态 | 备注 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支持 | 更新 Pi OS（内核 ≥ 5.18）|
| 台式机/笔记本 | ✅ 支持 | L 型 USB-A 接头不遮挡邻近端口 |
| Mac（Intel）| ⚠️ 有限支持 | 最高 macOS 10.15 Catalina |

## 高级功能

| 功能 | 状态 |
|------|------|
| Monitor Mode | ✅ 支持 |
| Packet Injection | ✅ 支持 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ✅ BT 5.2（含独立 BT 天线）|
| VIF | ✅ 支持 |

## 包装内容

- 1× AWUS036AXM 无线网卡
- 2× 5 dBi 天线
- 快速设置指南

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方产品页面 | https://www.alfa.com.tw/products/awus036axm |
| 官方文档 | https://docs.alfa.com.tw/ |
| Linux 驱动 | mt7921u — Linux 内核 ≥ 5.18 已内置 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036AXM 规格书](/docs/alfa/AWUS036AXM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axm_image_1.png" alt="ALFA AWUS036AXM" />
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
