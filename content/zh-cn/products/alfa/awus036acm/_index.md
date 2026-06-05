---
title: "ALFA AWUS036ACM — AC1200 双频 USB 3.0 无线网卡（Linux 免驱首选）"
description: "ALFA AWUS036ACM，MediaTek MT7612U，AC1200 双频 USB 3.0，内建 Linux 内核驱动（Kernel 4.19+），无需手动安装，支持 Monitor Mode、Packet Injection 与 VIF，Raspberry Pi 首选。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "双频", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**合法使用声明**：Monitor Mode 与 Packet Injection 功能仅供授权的网络安全测试、教育研究及合法渗透测试使用。请确认已获得目标网络的明确授权。
{{< /alert >}}

## 产品概述

AWUS036ACM 是 Linux 用户零配置即插即用的首选网卡。其 MediaTek MT7612U 芯片组自 Linux 内核 4.19 版本起已内置于内核中，这意味着在 Ubuntu、Kali Linux、Raspberry Pi OS、Arch Linux 及几乎所有现代发行版上，无需编译任何代码即可即插即用。外观尺寸与天线配置与 AWUS036ACH 完全相同，但采用 MediaTek 更稳定的内核内置驱动。Monitor Mode、Packet Injection 与 VIF（虚拟接口）均完整支持。

> **macOS 注意事项：** 所有 ALFA 网卡对 macOS 支持有限。macOS 11+ 及 Apple Silicon（M1/M2/M3）均**不支持**。AWUS036ACM 最高支持 macOS 10.12 Sierra（比其他型号更严格）。

## 产品特色

- MediaTek MT7612U 芯片组 — 自 Linux 内核 4.19 起内置（免驱、无需编译）
- WiFi 5（802.11ac）双频 AC1200 — 5 GHz 最高 867 Mbps，2.4 GHz 最高 300 Mbps
- 2× RP-SMA female 接口搭配 2× 5 dBi 可拆卸双频天线 — 与 AWUS036ACH 完全相同的外观规格
- USB 3.0（USB-A）接口
- 完整支持 Monitor Mode、Packet Injection 与 AP 模式
- 支持 Kali Linux VIF（虚拟接口）
- 附赠 USB 3.0 延长线
- TAA 认证 — 适用于美国政府采购（GSA 兼容）
- Raspberry Pi OS 即插即用 — 无需安装驱动程序

## 技术规格

| 项目 | 规格 |
|------|------|
| 芯片组 | MediaTek MT7612U |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n/ac（WiFi 5）|
| 频率范围 | 2.4 GHz（2.412–2.472 GHz）· 5 GHz（5.15–5.825 GHz）|
| 信道带宽 | 20 / 40 / 80 MHz |
| 最高传输速率 | 5 GHz：最高 867 Mbps · 2.4 GHz：最高 300 Mbps |
| 合计最高速率 | AC1200（867 + 300 Mbps）|
| 天线接口 | 2× RP-SMA female |
| 附赠天线 | 2× 双频偶极天线，5 dBi |
| USB 接口 | USB 3.0 Type-A（向下兼容 USB 2.0）|
| 输出功率 | 802.11a：20 dBm · 802.11b：23 dBm · 802.11g：23 dBm · 802.11n：21 dBm · 802.11ac：20 dBm |
| 接收灵敏度 | 802.11a：−92 dBm · 802.11b：−97 dBm · 802.11g：−90 dBm · 802.11n：−90 dBm |
| 无线安全 | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| 指示灯 | 有（电源 + 无线活动）|
| 附件 | USB 3.0 延长线 |
| 原产地 | 台湾 |

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---------|------|------|
| Windows XP–11 | ✅ 支持 | 驱动程序请至 Alfa 官网下载，推荐 Windows 10/11 |
| macOS 10.7–10.12 | ⚠️ 有限支持 | 官方支持至 macOS 10.12 Sierra，macOS 11+ 及 Apple Silicon 不支持 |
| Ubuntu 19.04+ | ✅ 即插即用 | 内核内置 mt76 驱动（内核 ≥ 4.19），Ubuntu 20.04 LTS 以上零配置安装 |
| Kali Linux 2019.3+ | ✅ 即插即用 | 内核内置驱动，已确认 Monitor Mode，支持 VIF，5 GHz AP 模式可能需要 `disable_usb_sg` 模块参数 |
| NetHunter（Android）| ✅ 支持 | OTG USB；内核内置驱动使其兼容性优于 RTL 系列 |

## 硬件支持

| 硬件 | 状态 | 备注 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 极佳 | Raspberry Pi OS 即插即用，无需安装驱动，ALFA 网卡中 Pi 首选 |
| 台式机/笔记本 | ✅ 支持 | 标准 USB-A，附赠延长线 |
| Mac（Intel）| ⚠️ 有限支持 | 仅限 macOS 10.7–10.12 |

## 高级功能

| 功能 | 状态 |
|------|------|
| Monitor Mode | ✅ 支持（内核内置，现代发行版无需额外步骤）|
| Packet Injection | ✅ 支持 |
| Soft AP 模式 | ✅ 支持（5 GHz AP：加入 `disable_usb_sg` 模块参数以获最佳性能）|
| 蓝牙 | ❌ 不支持 |
| VIF（虚拟接口）| ✅ 支持（Kali 完整 VIF 支持）|

## 包装内容

- 1× AWUS036ACM 无线网卡
- 2× 可拆卸 5 dBi 双频偶极天线
- 1× USB 3.0 延长线
- 1× 驱动程序光盘（Windows）

## 资源与链接

| 资源 | 链接 |
|------|------|
| 官方产品页面 | https://www.alfa.com.tw/products/awus036acm_1 |
| 官方文档 | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux 驱动（内核内置）| mt76 驱动 — Linux 内核 ≥ 4.19 已内置，无需安装 |

## 产品规格书下载

| 文件 | 下载 |
|------|------|
| 官方规格书（PDF） | [📄 下载 AWUS036ACM 规格书](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
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
