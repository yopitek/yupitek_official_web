---
title: "ALFA 无线网卡是否支持 OpenWrt"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "路由器韧体"
description: "OpenWrt 是三大第三方路由器韧体（DD-WRT / OpenWrt / Tomato）中对 ALFA USB WiFi 网卡支持最好的平台。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）透过官方 kmod-mt76 系列套件可直接支持；Realtek 晶片机型（AWUS036ACH / ACS / EACS / AX / AXER）需使用社群..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 OpenWrt 路由器上使用？」

简短结论：OpenWrt 是三大第三方路由器韧体（DD-WRT / OpenWrt / Tomato）中对 ALFA USB WiFi 网卡支持最好的平台。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）透过官方 kmod-mt76 系列套件可直接支持；Realtek 晶片机型（AWUS036ACH / ACS / EACS / AX / AXER）需使用社群维护的 out-of-tree 驱动套件，可用性因 OpenWrt 版本而异。首选 AWUS036ACM（MT7612U），驱动成熟、稳定、支持监听与注入。

判定母体：ALFA 现役 9 款 USB 网卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目标软体规格与需求

### 2.1 OpenWrt 是什么

OpenWrt 是一款高度模组化的开源路由器韧体，采用 Linux kernel 与 opkg 套件管理系统。与 DD-WRT / Tomato 不同，OpenWrt 的驱动程式以可单独安装的 kernel module（kmod）套件形式提供，使用者可依需求安装 USB WiFi 驱动，不需重新编译整个韧体。

### 2.2 OpenWrt 的 USB WiFi 驱动框架

OpenWrt 官方套件库包含以下 USB WiFi 驱动：

| 驱动套件 | 来源 | 涵盖晶片 / 机型 | 维护状态 |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | 官方 in-kernel | MediaTek MT7612U（AWUS036ACM） | 活跃，稳定 |
| kmod-mt76-usb + kmod-mt76x0u | 官方 in-kernel | MediaTek MT7610U（AWUS036ACHM） | 活跃 |
| kmod-mt7921u | 官方 in-kernel | MediaTek MT7921AUN（AWUS036AXML / AXM） | 23.05+ 版本可用 |
| kmod-rtl8812au-ct | 社群 out-of-tree | Realtek RTL8812AU / RTL8811AU（AWUS036ACH / ACS） | 社群维护，24.10 有 kernel crash 回报 |
| kmod-rtl8821cu | 社群 out-of-tree | Realtek RTL8811CU（AWUS036EACS） | 社群维护 |
| kmod-rtw89 / kmod-rtl8852bu | 开发中 | Realtek RTL8832BU（AWUS036AX / AXER） | rtw89 USB 支持逐步合入，需较新 kernel |

### 2.3 先决条件：USB 核心支持

在安装 WiFi 驱动前，必须先确保 OpenWrt 已启用 USB 核心支持：

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

多数现代 OpenWrt 版本已预设包含 kmod-usb-core，但 usbutils（提供 lsusb 指令）需手动安装。

## 3. 分析目前 ALFA 网路卡规格和晶片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下（判定母体：9 款）：

| 机型 | Wi-Fi 等级 | 晶片组 | 介面 | OpenWrt 驱动套件 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u（23.05+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u（23.05+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89（开发中）/ 自编 rtl8852bu |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct（社群） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u（官方） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u（官方）⭐ 首选 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct（涵盖） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu（社群） |

## 4. 适用机型与晶片组

### 4.1 推荐等级分类

| 推荐等级 | 机型（晶片组） | 说明 |
|---|---|---|
| ⭐ 强烈推荐 | AWUS036ACM（MT7612U） | 官方驱动成熟稳定，支持 AP / STA / Monitor / Injection，OpenWrt 上的最佳选择 |
| ✅ 推荐 | AWUS036ACHM（MT7610U） | 官方驱动，双频但仅 433Mbps，适合低功耗场景 |
| ✅ 推荐（新版本） | AWUS036AXML / AXM（MT7921AUN） | Wi-Fi 6E，官方驱动，需 OpenWrt 23.05+ 且 kernel 5.15+ |
| ⚠️ 可用但需注意 | AWUS036ACH（RTL8812AU） | 社群驱动，24.10 版本有 kernel crash 回报，建议用 23.05 |
| ⚠️ 可用但需注意 | AWUS036ACS（RTL8811AU） | 同上，由 8812au 驱动涵盖 |
| ⚠️ 可用但需注意 | AWUS036EACS（RTL8811CU） | 社群驱动，稳定性中等 |
| ❌ 不建议 | AWUS036AX / AXER（RTL8832BU） | Wi-Fi 6，rtw89 USB 支持尚在开发，多数 OpenWrt 版本无法直接使用 |

### 4.2 路由器硬体需求

| 项目 | 最低需求 | 建议需求 |
|---|---|---|
| USB 埠 | USB 2.0（AWUS036ACHM / ACS / EACS） | USB 3.0（AWUS036ACH / ACM / AX 系列） |
| Flash | 16MB（安装驱动 + 依赖套件） | 32MB+ |
| RAM | 128MB | 256MB+（AP 模式 + 多使用者） |
| OpenWrt 版本 | 21.02+ | 23.05.x（稳定版） |

## 5. 环境需求

### 5.1 软体环境

- OpenWrt 稳定版本：23.05.x（kernel 5.15）或 24.10.x（kernel 6.6）
- 套件来源：官方 opkg 套件库（https://downloads.openwrt.org/releases/{version}/packages/{arch}/）
- 网路连线：安装驱动期间路由器需可联网（透过 WAN 埠）

### 5.2 硬体环境

- 具备 USB 2.0 / 3.0 埠的 OpenWrt 相容路由器
- 高功率机型（AWUS036ACH）建议使用有电源的 USB 3.0 Hub，避免路由器 USB 埠供电不足
- AWUS036AXML 为 USB-C 介面，需确保路由器有 USB-C 埠或使用 USB-C to USB-A 转接

## 6. 相容性判定

### ALFA 现役机型 × OpenWrt 相容性矩阵

| 机型 | 晶片组 | 驱动方式 | USB 侦测 | STA 上网 | AP 模式 | Monitor | 最低版本 | 综合评价 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ 最佳 |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ 有限 | 21.02+ | ✅ 良好 |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 有限 | 23.05+ | ✅ 良好 |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 有限 | 23.05+ | ✅ 良好 |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ 有限 | 22.03+（24.10 有 crash） | ⚠️ 可用 |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ 可用 |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | rtw89（开发中） | ⚠️ | ❌ | ❌ | ❌ | 需自订编译 | ❌ 不建议 |
| AWUS036AXER | RTL8832BU | rtw89（开发中） | ⚠️ | ❌ | ❌ | ❌ | 需自订编译 | ❌ 不建议 |

判定依据：OpenWrt 官方套件库（23.05 / 24.10）的 kmod 套件可用性 + OpenWrt 论坛使用者回报。Realtek 晶片的驱动为社群维护，稳定性与功能完整性不及 MediaTek mt76 系列。

## 7. 超详细 Step by Step 设定步骤

### 7.1 前置作业：启用 USB 核心支持

**步骤 1：SSH 登入 OpenWrt 路由器**

```bash
ssh root@192.168.1.1
```

**步骤 2：更新套件库并安装 USB 核心支持**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**步骤 3：插入 ALFA 网卡，确认 USB 侦测**

```bash
lsusb
# 预期输出范例（AWUS036ACM / MT7612U）：
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 路径 A：MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）

以 AWUS036ACM（MT7612U）为例：

**步骤 1：安装驱动套件**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — 改用
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — 改用（需 23.05+）
# opkg install kmod-mt7921u
```

**步骤 2：安装无线管理工具**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**步骤 3：确认网路介面已建立**

```bash
iw dev
# 预期出现 wlan0 或 wlan1 介面
```

**步骤 4：扫描附近 WiFi（验证功能）**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**步骤 5：设定为 STA 用户端模式（连线到既有 AP）**

编辑 /etc/config/wireless：

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid '你的WiFi名称'
       option encryption 'psk2'
       option key '你的WiFi密码'
```

**步骤 6：重启无线服务**

```bash
/etc/init.d/network restart
```

**步骤 7：设定为 AP 热点模式（分享网路）**

编辑 /etc/config/wireless，将 mode 改为 ap：

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key '你的热点密码'
```

**步骤 8：启用监听模式（渗透测试用）**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# 验证
iw dev wlan0 info
# type 应显示 monitor
```

### 7.3 路径 B：Realtek 晶片机型（AWUS036ACH / ACS / EACS）

以 AWUS036ACH（RTL8812AU）为例：

**步骤 1：安装社群驱动**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — 改用
# opkg install kmod-rtl8821cu
```

**步骤 2：安装无线管理工具**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**步骤 3：确认介面**

```bash
iw dev
# 注意：rtl8812au-ct 驱动的介面名可能是 wlan0 或 wlan1
```

设定方式同 7.2 步骤 5-7（STA / AP 模式设定）。

**步骤 4：监听模式**

```bash
# rtl8812au-ct 驱动支持监听模式
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# 封包注入功能有限，建议用 mt76 晶片做渗透测试
```

**步骤 5：若遇到 kernel crash（24.10 版本已知问题）**

```bash
# 降回 23.05 稳定版，或使用自订编译的驱动
# 检查 crash 日志
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 路径 C：Wi-Fi 6 机型（AWUS036AX / AXER，RTL8832BU）

⚠️ 此路径需自订编译 OpenWrt，不适合一般使用者。

**步骤 1：确认 OpenWrt 版本是否已包含 rtw89 USB 支持**

```bash
opkg list | grep rtw89
# 若无结果，代表该版本未包含
```

**步骤 2：若需使用，需自行编译 OpenWrt 映像档**

加入 kmod-rtw89 与对应 firmware。

**替代建议**：在 OpenWrt 路由器上使用 Wi-Fi 6 USB 网卡的需求，目前以 AWUS036AXML（MT7921AUN）替代为佳。

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB 核心未安装 / 供电不足 | 确认已安装 kmod-usb-core kmod-usb2 kmod-usb3；使用有电源 USB Hub |
| lsusb 看得到但 iw dev 无介面 | 驱动未安装 / 驱动不相容 | 安装对应 kmod 套件；检查 dmesg 是否有 firmware 缺失错误 |
| opkg install kmod-mt76x2u 报「kernel version mismatch」 | OpenWrt 版本与套件库版本不一致 | 执行 opkg update 后重试；确认韧体版本与套件库架构匹配 |
| AP 模式启动失败（hostapd 错误） | 驱动不支持 AP / 通道设定错误 | 确认晶片支持 AP 模式；尝试固定通道（如 6 或 149）；检查 Regulatory Domain |
| 监听模式无法注入封包 | 驱动不支持注入 / 通道冲突 | MediaTek mt76 系列支持最佳；Realtek 8812au-ct 注入功能有限；确认 airmon-ng check kill |
| AWUS036ACH 高功率时断线 | USB 供电不足 | 使用有电源 USB 3.0 Hub；在 /etc/config/wireless 中设定 option txpower '20' 降低功率 |
| 24.10 上安装 rtl8812au-ct 后 kernel panic | 已知驱动相容性问题 | 降回 23.05.x 稳定版；或追踪 GitHub issue 等待修复 |
| MT7921（AXML/AXM）无法使用 6GHz | Regulatory Domain 限制 / kernel 版本 | 需 kernel 5.19+ 且正确设定 Wi-Fi 6E 法规区域；OpenWrt 23.05 的 6GHz 支持仍在测试 |

## 9. 已知限制

- Realtek 晶片驱动为社群维护：kmod-rtl8812au-ct、kmod-rtl8821cu 非 OpenWrt 官方维护，稳定性与更新时程无法保证
- 24.10 版本的 rtl8812au-ct 有 kernel crash 回报：建议 Realtek 晶片使用者维持在 23.05.x
- Wi-Fi 6（RTL8832BU）支持不足：rtw89 USB 驱动尚在开发，多数 OpenWrt 版本无法直接使用 AWUS036AX / AXER
- AP 模式效能受限：USB WiFi 做 AP 时，吞吐量低于路由器内建 WiFi（USB 汇流排频宽 + 驱动 overhead）
- 监听 / 注入功能差异：MediaTek mt76 系列支持最完整；Realtek 晶片的注入功能有限，不适合专业渗透测试
- 路由器硬体资源：低阶路由器（16MB Flash / 128MB RAM）安装驱动后可能空间不足，影响其他功能
- USB 3.0 干扰：USB 3.0 设备会对 2.4GHz WiFi 产生干扰，建议使用 USB 2.0 埠或隔离良好的 USB Hub
- 多网卡同时使用：同时使用路由器内建 WiFi + USB WiFi 时，可能出现通道冲突或资源竞争
- ⚠️ **RTL8832BU（AWUS036AX/AXER）驱动维护者已公开建议避免使用**：本文第 4.1 节标为「❌ 不建议」，原因不只是 rtw89 USB 尚在开发，驱动维护者 morrownr 更公开表示该晶片系列「是很糟糕的驱动，怀疑晶片本身有问题」，建议 Linux 使用者现阶段避开（来源见第 10 节）
- **kernel 版本门槛用词需澄清**：第 4.1 节「MT7921AUN 需 OpenWrt 23.05+ 且 kernel 5.15+」的写法容易误导——mt7921u 驱动本身在桌机 Linux 上实际需要 **kernel 5.19+** 才会存在（见驱动维护者原话），但 OpenWrt 官方套件常透过 backport 机制提前收录，因此 OpenWrt 23.05（虽标示基础 kernel 5.15）仍有使用者回报安装 kmod-mt7921u 成功。**判定请以客户版本 `opkg list` 实际查询结果为准，不要用 kernel 版号反推**

反驳条件：若 OpenWrt 后续套件更新修复 24.10 的 rtl8812au-ct kernel crash 问题，第 4.1 节与第 6 节对 AWUS036ACH 的建议可由「维持 23.05」升级；若 rtw89 USB 支持正式进入 OpenWrt 官方套件库，AWUS036AX / AXER 的「不建议」判定需重审；若官方发布 MT7921 的 6GHz 完整支持声明，AXML / AXM 的限制说明需更新。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| OpenWrt 官方文档 | OpenWrt 官方文件入口（无线设定 / 套件管理） | https://openwrt.org/docs/start | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方论坛 | USB WiFi 驱动讨论入口 | https://forum.openwrt.org/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动上游 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Network 产品总览（Yupitek） | ALFA 现役产品规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驱动维护者官方声明：建议避开 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko 需 kernel 5.19+ 才会出现于核心（驱动维护者原话） | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方论坛 — Best USB WiFi dongle for Raspberry Pi 4B | 使用者回报 OpenWrt 23.05.0 成功安装 kmod-mt7921u | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[ALFA 无线网卡是否支持 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免责声明：本文相容性判定以 OpenWrt 23.05.x / 24.10.x 官方套件库为准。不同路由器架构（ath79 / ramips / mvebu / x86 等）的套件可用性可能不同。Realtek 晶片驱动为社群维护，实际稳定性可能随版本变化。建议以 MediaTek 晶片机型（AWUS036ACM 为首选）作为 OpenWrt USB WiFi 的优先选择。
