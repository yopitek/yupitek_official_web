---
title: "ALFA AWUS036ACH — AC1200 双频高功率 USB-C 无线网卡"
description: "ALFA AWUS036ACH，Realtek RTL8812AU，AC1200 双频，USB-C，双 5 dBi 外接天线，Kali Linux 渗透测试金标准，支持 Monitor Mode 与 Packet Injection。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "双天线", "Monitor Mode", "Kali Linux", "安全研究"]
---

{{< alert "warning" >}}
**合法使用声明**：Monitor Mode 与 Packet Injection 功能仅供授权的安全测试、教育研究及合法渗透测试使用。请确认已获得目标网络的明确授权。
{{< /alert >}}

## 产品概述

AWUS036ACH 是 ALFA Network 安全研究社区公认的黄金标准无线网卡，自 2017 年起成为 Kali Linux 渗透测试首选。搭载 Realtek RTL8812AU 芯片，具备稳定的 Monitor Mode 与 Packet Injection 支持，内置功率放大器提升远距接收能力，配备两根可拆卸 5 dBi 天线。全球首款搭载 USB Type-C 接口的 Wi-Fi 5 USB 网卡。

> **macOS 注意：** 不支持 macOS 11 及以上版本和 Apple Silicon（M1/M2/M3）。最高支持 Intel Mac 上的 macOS 10.15 Catalina。

## 产品特色

- Realtek RTL8812AU 芯片 — 安全研究社区文档最完整的芯片组
- Wi-Fi 5（802.11ac）AC1200 双频：5 GHz 867 Mbps + 2.4 GHz 300 Mbps
- 内置功率放大器 — 接收距离可达普通笔记本内置网卡的 3 倍
- 2× RP-SMA female 天线接口配 2× 5 dBi 可拆卸双频天线（可升级高增益天线）
- 全球首款 Wi-Fi 5 USB Type-C 接口无线网卡
- 附赠屏幕夹架

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | Realtek RTL8812AU |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac（Wi-Fi 5） |
| 频段 | 双频 2.4 GHz / 5 GHz |
| 最高传输速率 | 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| 合计最高速率 | AC1200（867 + 300 Mbps） |
| 天线接口 | 2× RP-SMA female |
| 内附天线 | 2× 双频全向天线，5 dBi |
| USB 接口 | Type-C SuperSpeed（5 Gbps）；兼容 USB 2.0 |
| 功率放大器 | 有 |
| 无线安全 | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| 产地 | 台湾 |

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---------|------|------|
| Windows 10/11 | ✅ 支持 | 从 ALFA 官网下载驱动；支持 WPA3 |
| macOS 10.15 Catalina | ⚠️ 有限支持 | 需手动安装；不支持 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支持 | 需 DKMS 手动安装；Ubuntu 24.10+（内核 ≥ 6.14）已内置 |
| Kali Linux | ✅ 优秀 | 自 2017.1 起支持；完整 Monitor Mode + Packet Injection |
| NetHunter（Android） | ✅ 支持 | OTG USB 连接 |

## 硬件支持

| 硬件 | 状态 | 备注 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支持 | 通过 morrownr DKMS 手动安装 |
| 台式机/笔记本 | ✅ 支持 | USB-C 或附赠数据线 |
| Mac（Intel） | ⚠️ 有限支持 | 最高 macOS 10.15 Catalina |

## 高级功能

| 功能 | 状态 |
|------|------|
| Monitor Mode | ✅ 优秀（黄金标准 — 社区验证自 2017 年） |
| Packet Injection | ✅ 优秀 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ❌ 无 |
| VIF | ⚠️ 有限 |

## 包装内容

- 1× AWUS036ACH 无线网卡
- 2× 可拆卸 5 dBi 双频天线
- 1× USB-C to USB-A 数据线
- 1× 屏幕夹架

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方产品页面 | https://www.alfa.com.tw/products/awus036ach_1 |
| 官方文档 | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| 驱动（aircrack-ng，Kali 推荐）| https://github.com/aircrack-ng/rtl8812au |
| 驱动（morrownr，通用 Linux） | https://github.com/morrownr/8812au-20210708 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036ACH 规格书](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
