---
title: "ALFA AWUS036ACS — AC600 双频 USB 无线网卡（入门安全研究）"
description: "ALFA AWUS036ACS，Realtek RTL8811AU，AC600 双频 USB 2.0，1× 2 dBi RP-SMA 可拆卸天线，支持 Monitor Mode 与 Packet Injection，入门级安全研究首选。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "入门"]
---

{{< alert "warning" >}}
**合法使用声明**：Monitor Mode 与 Packet Injection 功能仅供授权的安全测试、教育研究及合法渗透测试使用。请确认已获得目标网络的明确授权。
{{< /alert >}}

## 产品概述

AWUS036ACS 是 Alfa 双频 802.11ac 产品线中最经济实惠的入门款，搭载 Realtek RTL8811AU 芯片，支持 Monitor Mode 与 Packet Injection。机身轻巧小型，配备 1 根可拆卸 RP-SMA 天线，可按需升级为高增益或定向天线。虽然性能不及 ACH 或 ACM，但对于初学者或需要预算友好型 5 GHz 外接天线网卡的用户而言，是十分实用的选择。

> **macOS 注意事项：** 所有 ALFA 网卡对 macOS 支持有限。macOS 10.15 Catalina 及以上版本和 Apple Silicon（M1/M2/M3）均**不支持**。AWUS036ACS 最高支持 macOS 10.14 Mojave（Intel Mac）。

## 产品特色

- Realtek RTL8811AU 芯片 — 支持 Monitor Mode 与 Packet Injection
- WiFi 5（802.11ac）双频 — 2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）= AC600
- 1× RP-SMA 母头连接器，附 1× 2 dBi 迷你可拆卸天线 — 可升级为面板天线或高增益天线
- 轻巧小型机身 — 便于携带
- USB 2.0（USB-A）接口 — 兼容所有 USB 端口
- 兼容 Alfa APA-M25 双频面板天线，可实现定向接收
- 支持 Kali Linux on Raspberry Pi（KaliPi）— 通过 DKMS 安装驱动程序

## 技术规格

| 参数 | 规格 |
|---|---|
| 芯片组 | Realtek RTL8811AU |
| 无线标准 | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| 频段 | 2.4 GHz（150 Mbps）· 5 GHz（433 Mbps） |
| 最大合计速率 | AC600（150 + 433 Mbps） |
| 天线连接器 | 1× RP-SMA 母头 |
| 随附天线 | 1× 双频全向迷你偶极天线，2 dBi |
| USB 接口 | USB 2.0 Type-A |
| 接收灵敏度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 无线安全 | WPA2 / WPA / WEP / 802.1X |
| 原产地 | 台湾 |

> ⚠️ **注意：** 仅支持 USB 2.0，最高总线速度 480 Mbps，传输速率上限为 433 Mbps。如需更高速度，请选择搭载 USB 3.0 的 AWUS036ACM 或 AWUS036ACH。

## 操作系统支持

| 操作系统 | 状态 | 备注 |
|---|---|---|
| Windows XP–11 | ✅ 支持 | 驱动程序请至 Alfa 官网下载 |
| macOS 10.5–10.14 | ⚠️ 有限支持 | macOS 10.15+ 及 Apple Silicon 不支持 |
| Ubuntu | ✅ 支持 | 需手动安装 DKMS 驱动（morrownr/8821au），无内核内置支持 |
| Kali Linux | ✅ 支持 | 支持 Monitor Mode + Packet Injection，使用 morrownr GitHub 社区驱动 |
| NetHunter（Android） | ✅ 支持 | OTG USB 连接；RTL8811AU 已确认兼容 NetHunter |

## 硬件支持

| 硬件 | 状态 | 备注 |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ 支持 | 可通过 morrownr DKMS 安装 KaliPi 专用驱动 |
| 台式机／笔记本电脑 | ✅ 支持 | 标准 USB-A 连接 |
| Mac（Intel） | ⚠️ 有限支持 | 仅支持 macOS 10.5–10.14 |

## 高级功能

| 功能 | 状态 |
|---|---|
| Monitor Mode（监听模式） | ✅ 支持 |
| Packet Injection（数据包注入） | ✅ 支持 |
| Soft AP 模式 | ✅ 支持 |
| 蓝牙 | ❌ 不支持 |
| VIF（虚拟接口） | ⚠️ 有限支持 |

## 包装内容

- 1× AWUS036ACS 无线网卡
- 1× 可拆卸 2 dBi 双频迷你偶极天线

## 资源与链接

| 资源 | 链接 |
|---|---|
| 官方产品页面 | https://www.alfa.com.tw/products/awus036acs_1 |
| 官方技术文档 | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux 驱动（RTL8811AU） | https://github.com/morrownr/8821au-20210708 |

## 产品规格书下载

| 文件 | 链接 |
|---|---|
| 官方规格书（PDF） | [📄 下载 AWUS036ACS 规格书](/docs/alfa/AWUS036ACS_spec.pdf) |

## 产品图片

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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


{{< alert "info" >}}
需要询价？[联系我们](/zh-cn/contact/)，我们提供详细采购建议。
{{< /alert >}}
