---
title: "ALFA 无线网卡是否支持 DD-WRT"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "路由器韧体"
description: "目前 ALFA 全系列现役机型（AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM，共 9 款）在 DD-WRT 上均无官方驱动支持，不建议使用。（判定母体：ALFA 现役 9 款 USB 网卡）DD-WRT 的 USB WiFi 支持仅限极少数旧型 Atheros / Ralink 晶片，且需特定编译版本。若需要在路由..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在刷了 DD-WRT 韧体的路由器上使用？」

简短结论：目前 ALFA 全系列现役机型（AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM，共 9 款）在 DD-WRT 上均无官方驱动支持，不建议使用。（判定母体：ALFA 现役 9 款 USB 网卡）DD-WRT 的 USB WiFi 支持仅限极少数旧型 Atheros / Ralink 晶片，且需特定编译版本。若需要在路由器上使用 USB WiFi 网卡，建议改用 OpenWrt（见 [ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)）。

## 2. 分析目标软体规格与需求

### 2.1 DD-WRT 是什么

DD-WRT 是一款开源路由器第三方韧体，主要针对内建 WiFi 晶片的路由器（Broadcom / Atheros / Ralink SoC）设计。其核心架构为 Linux kernel，但驱动程式预设仅编入目标路由器 SoC 对应的无线驱动。

### 2.2 DD-WRT 的 USB WiFi 支持框架

DD-WRT 透过 ipkg 套件管理系统安装额外驱动，但官方套件库中 USB WiFi 驱动极少：

| 驱动 | DD-WRT 状态 | 对应晶片（ALFA 机型） |
|---|---|---|
| ath9k_htc | 部分版本内建 | Atheros AR9271（如 TP-Link TL-WN722N v1） |
| rt2800usb | 部分版本内建 | Ralink RT3070 / RT3370 / RT5370（旧型 ALFA AWUS036NH 等） |
| rtl8812au | 无官方套件 | Realtek RTL8812AU（AWUS036ACH） |
| mt76 / mt76x2u | 无官方套件 | MediaTek MT7612U / MT7610U（AWUS036ACM / ACHM） |
| mt7921u | 无官方套件 | MediaTek MT7921AUN（AWUS036AXML / AXM） |
| rtl8852bu / rtw89 | 无官方套件 | Realtek RTL8832BU（AWUS036AX / AXER） |

### 2.3 关键限制

- DD-WRT 的核心优先支持路由器内建 WiFi，USB WiFi 属于次要功能
- 不同路由器型号的 DD-WRT 编译版本不同，驱动可用性差异极大
- 即使社群自行编译加入驱动，也常因 Flash / RAM 不足而无法安装
- DD-WRT 对 USB WiFi 的监听模式（Monitor Mode）与封包注入（Packet Injection）几乎不支持

## 3. 分析目前 ALFA 网路卡规格和晶片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下：

| 机型 | Wi-Fi 等级 | 晶片组 | 介面 | Linux 驱动状态 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel（mt7921u，需 kernel 5.12+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel（mt7921u，需 kernel 5.12+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree（8812au，morrownr 维护） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel（mt76x2u） |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree（8812au 涵盖） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree（8821cu，morrownr 维护） |

## 4. 适用机型与晶片组

### 4.1 在 DD-WRT 上可能可用的 ALFA 机型（已停产 / 旧款）

| 机型 | 晶片组 | 驱动 | DD-WRT 状态 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 部分 DD-WRT 版本内建，仅 2.4GHz / 150Mbps |
| AWUS036H | Realtek RTL8187L | rtl8187 | 极旧型，部分版本支持，仅 2.4GHz / 54Mbps |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | 极旧型，双频，但已停产多年 |

### 4.2 在 DD-WRT 上不可用的现役机型

所有现役 ALFA 机型（见第 3 节表格）均不被 DD-WRT 官方支持，原因：

- Realtek 晶片（RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU）：DD-WRT 无对应 out-of-tree 驱动套件
- MediaTek 晶片（MT7612U / MT7610U / MT7921AUN）：DD-WRT 未编入 mt76 / mt7921 驱动
- 即使路由器有 USB 埠，硬体层面可以辨识装置（lsusb 可看到 VID/PID），但无驱动无法建立网路介面

## 5. 环境需求

若客户仍想尝试在 DD-WRT 上使用 ALFA 网卡，需满足以下条件：

| 项目 | 需求 |
|---|---|
| 路由器硬体 | 必须有 USB 2.0 / 3.0 埠，且 DD-WRT 已启用 USB 核心支持（Services > USB） |
| DD-WRT 版本 | 需为支持该路由器的最新 BrainSlayer / Kong 版本，旧版驱动更少 |
| Flash 空间 | 至少 16MB Flash（多数入门路由器仅 4-8MB，无法安装额外驱动） |
| RAM | 至少 128MB RAM（USB WiFi 驱动 + hostapd 会占用记忆体） |
| 供电 | USB 埠需提供足够电流（AWUS036ACH 高功率输出时可达 800mA+，建议使用有电源 USB Hub） |

## 6. 相容性判定

### ALFA 现役机型 × DD-WRT 相容性矩阵

| 机型 | 晶片组 | USB 汇流排侦测 | 驱动载入 | STA 上网 | AP 模式 | Monitor | 综合判定 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支持 |

判定依据：DD-WRT 官方套件库与核心预设编译均未包含上述晶片的 USB WiFi 驱动。lsusb 能看到装置仅代表 USB 汇流排层级的辨识，不代表网路功能可用。

## 7. 超详细 Step by Step 设定步骤

由于现役 ALFA 机型在 DD-WRT 上不可用，本节提供两种替代路径：

### 路径 A：确认你的 DD-WRT 路由器是否真的不支持（除错步骤）

**步骤 1：登入 DD-WRT 管理介面**

浏览器输入 `192.168.1.1`（或你的路由器 IP）。

**步骤 2：启用 USB 支持**

- 进入 Services > USB
- 勾选 Core USB Support、USB 2.0 Support、USB 3.0 Support（若有）
- 勾选 USB Wireless Device Support（若有此选项）
- 点击 Save > Apply Settings

**步骤 3：插入 ALFA 网卡到路由器 USB 埠**

**步骤 4：透过 SSH 登入路由器检查**

```bash
# 检查 USB 装置是否被侦测
lsusb
# 预期输出应包含 ALFA 网卡的 VID/PID，例如：
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# 检查网路介面是否被建立
ip link show
# 若没有 wlan0 / wlan1 等新介面，代表驱动未载入

# 检查核心日志
dmesg | tail -30
# 若出现 "no driver" 或仅有 USB 列举讯息，确认驱动缺失
```

**步骤 5：检查可用的 WiFi 驱动模组**

```bash
# 列出已载入的无线驱动
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# 若仅有路由器内建 WiFi 的驱动（如 wl / b43 / ath9k），代表无 USB WiFi 驱动
```

**步骤 6：尝试安装社群驱动（若有）**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 若搜寻结果为空，确认该 DD-WRT 版本无可用驱动
```

### 路径 B：建议替代方案 — 改用 OpenWrt

若客户需要在路由器上使用 ALFA USB WiFi 网卡，强烈建议将路由器韧体从 DD-WRT 改刷为 OpenWrt。OpenWrt 有活跃的 USB WiFi 驱动套件库，支持 MT7612U / MT7610U / RTL8812AU 等晶片。详细步骤请参考 [ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)。

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB 供电不足 / 接触不良 / DD-WRT 未启用 USB 核心 | 检查 Services > USB 是否已启用；更换 USB 埠或使用有电源 USB Hub |
| lsusb 看得到但 ip link 无 wlan 介面 | 缺少对应晶片驱动 | 确认 DD-WRT 版本是否有该驱动；多数情况下无解，建议改用 OpenWrt |
| 有 wlan 介面但无法扫描 AP | 驱动不完全支持 / 监听模式冲突 | 检查 dmesg 是否有 firmware 载入错误；确认 Regulatory Domain 设定 |
| 路由器重启后设定遗失 | DD-WRT NVRAM 空间不足 | 避免在低阶路由器上安装额外驱动；考虑升级硬体或改用 OpenWrt |
| AWUS036ACH 高功率输出时断线 | USB 埠供电不足 | 使用有电源的 USB 3.0 Hub；降低 TX Power 设定 |

## 9. 已知限制

- 驱动缺失：DD-WRT 官方不提供 ALFA 现役机型的 USB WiFi 驱动，这是最根本的限制
- 硬体资源：多数可刷 DD-WRT 的路由器 Flash（4-16MB）和 RAM（32-128MB）有限，即使有驱动也可能无法安装
- 监听 / 注入不支持：DD-WRT 的 USB WiFi 架构不支持渗透测试所需的 Monitor Mode 与 Packet Injection
- AP 模式不稳定：即使旧型 Ralink 晶片可运作，USB WiFi 的 AP 模式在 DD-WRT 上常见断线与效能问题
- 版本碎片化：不同路由器型号的 DD-WRT 编译版本差异大，无法保证某个版本的驱动在另一个版本也可用
- 不再活跃维护：DD-WRT 开发节奏放缓，新增 USB WiFi 驱动的可能性低
- 补充：即使抛开 DD-WRT 本身的限制，AWUS036AX / AXER（RTL8832BU）这两款机型的驱动维护者 morrownr 本身也公开建议 Linux 使用者避开此晶片系列（详见 [ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) 第 9 节），并非仅是 DD-WRT 平台的问题

反驳条件：若客户使用的是 BrainSlayer / Kong 等含额外驱动的社群编译版本，实际支持状况可能不同；本判定以官方发布版本为准。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| DD-WRT 官方 Wiki | 安装 / 支持 / FAQ 总入口 | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ 已查核 | 2026-09-03 |
| DD-WRT 官方 Wiki — Installation | 安装说明（含 USB 支持） | https://wiki.dd-wrt.com/wiki/Installation | ✅ 经主页连结确认存在 | 2026-09-03 |
| OpenWrt 官方文件 | USB WiFi 对比参考 | https://openwrt.org/docs/start | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动（DD-WRT 未整合） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Network 产品总览（Yupitek） | ALFA 现役产品规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 无线网卡是否支持 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

免责声明：本文相容性判定以晶片组驱动状态与 DD-WRT 官方套件库为准。DD-WRT 社群存在大量自订编译版本，若客户使用非官方版本，实际结果可能不同。建议客户以 OpenWrt 作为路由器 USB WiFi 的优先选择。
