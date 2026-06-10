---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM：5GHz 完整设置指南（2026）"
description: "HAK5 WiFi Pineapple MK7 搭配 ALFA AWUS036ACM (MT7612U) 完整兼容性指南 — 即插即用 5GHz 监听模式、数据包注入与 PineAP 扩展。逐步设置教程，附验证命令。无需编译驱动程序。"
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz", "渗透测试"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

HAK5 WiFi Pineapple Mark VII 是便携式无线安全审计的行业标杆。但开箱即用的它有一个重要限制：内置无线模块仅支持 **2.4 GHz**。到了 2026 年，大多数企业和家庭网络已迁移至 5 GHz 以获得更好的性能和更少的干扰——这意味着原厂 MK7 会错过一半的无线频谱。

这就是 **ALFA AWUS036ACM** 登场的时刻。它是少数被 Hak5 [官方确认兼容](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) 的 802.11ac 无线网卡之一，并且因为 MK7 Firmware 2.x 已预载 `mt76x2u` 内核驱动，达到**完全无需编译驱动**的即插即用体验。

本指南涵盖所有内容：硬件规格、驱动兼容性分析、经过验证的 7 步设置流程，以及完整的渗透测试拓扑图，让你在 10 分钟内为 Pineapple 添加 5 GHz 监听模式与数据包注入能力。

---

## 1. 为什么你的 WiFi Pineapple 需要 5 GHz

MK7 内置的 MT7628AN SoC 提供了一个可靠的 2.4 GHz b/g/n 无线模块——足以应对基本的 PineAP 操作，例如信标洪水攻击、解除认证攻击与客户端探测。但无线环境已经进化：

| 场景 | 2.4 GHz（内置） | 5 GHz（AWUS036ACM） |
|---|---|---|
| 企业 WPA2-Enterprise 网络 | 偶尔仍有 2.4 GHz | **现代部署的主要频段** |
| 家用 Mesh 系统（Eero、Google WiFi） | 仅作为旧设备备援 | **客户端连接的默认频段** |
| 802.11ac 客户端设备 | 几乎不使用 2.4 GHz | **永远优先选择 5 GHz** |
| 信道拥堵（公寓／办公室） | 极度拥挤（信道 1–11） | 干净频谱（信道 36–165） |
| WPA3-SAE 握手包捕获 | 有限 | 完整 5 GHz 捕获能力 |

**结论**：如果你正在审计现代网络，你需要 5 GHz。AWUS036ACM 是为 WiFi Pineapple MK7 添加 5 GHz 最可靠的方式。

---

## 2. 目标平台：HAK5 WiFi Pineapple Mark VII

### 2.1 硬件规格

MK7 基于 MediaTek MT7628AN 系统芯片，这是一款针对数据包级别操作优化的单核 MIPS 24KEc 网络处理器：

| 组件 | 规格 |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **内存** | 256 MB DDR2 |
| **存储** | 2 GB eMMC |
| **供电** | USB-C，5V @ 2A |
| **USB Host** | 1× USB 2.0 Type-A（最高 480 Mbps） |
| **USB 供电能力** | 500 mA @ 5V（共 2.5W） |

USB 2.0 端口值得特别注意。虽然 AWUS036ACM 是 USB 3.0 设备，在 5 GHz 下最高可达 867 Mbps，但 MK7 的 USB 2.0 总线将吞吐量限制在约 150–250 Mbps。对于渗透测试工作负载——监听模式数据包捕获、握手包收集、信标分析——这个带宽完全足够。只有在你试图将 MK7 用作高吞吐量无线网桥时才会遇到限制，而这并非其设计用途。

### 2.2 软件环境

MK7 运行由 Hak5 维护的高度客制化 OpenWrt 发行版：

| 层级 | 详细信息 |
|---|---|
| **操作系统** | OpenWrt（Hak5 客制版） |
| **内核版本** | 5.4.x（Firmware 2.x 系列） |
| **预载驱动** | `kmod-mt76x2u`（MT7612U）、`kmod-mt7601u`（MT7601U） |
| **包管理器** | `opkg` |
| **无线工具** | `iw`、`iwconfig`、`airmon-ng`、`hostapd`（2.9）、`uci` |
| **管理界面** | PineAP Web UI + SSH（端口 22） |

> ✅ **关键事实**：`kmod-mt76x2u` 已预载于 MK7 Firmware 2.x。AWUS036ACM 达到**即插即用**——无需 `opkg install`、无需交叉编译、无 DKMS 困扰。

---

## 3. ALFA AWUS036ACM — 硬件深入分析

### 3.1 规格

AWUS036ACM 基于 **MediaTek MT7612U** 芯片组，该芯片于 Linux 内核 4.19 版（2018 年 10 月）合并至主线。正是这个上游集成使其在 MK7 上实现无缝兼容。

| 规格 | 详细信息 |
|---|---|
| **芯片组** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **USB 接口** | USB 3.0 Type-A（向下兼容 USB 2.0） |
| **支持频段** | 2.4 GHz (b/g/n) + 5 GHz (a/n/ac) |
| **最大传输速率** | 2.4 GHz：300 Mbps · 5 GHz：867 Mbps |
| **信道宽度** | 20 / 40 / 80 MHz |
| **监听模式** | ✅ 支持 |
| **数据包注入** | ✅ 支持（通过 mac80211 框架） |
| **AP 模式** | ✅ 支持 |
| **天线** | 2× 5 dBi 双频 RP-SMA（可拆卸） |
| **发射功率** | 2.4G：23 dBm · 5G：20 dBm（±2 dBm） |
| **峰值电流消耗** | ~380 mA @ 5V |
| **安全协议** | WEP / WPA / WPA2 / WPA3 / 802.1X |

### 3.2 Hak5 官方确认兼容

Hak5 维护一份官方的[兼容 802.11ac 网卡列表](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)。AWUS036ACM (MT7612U) 被明确列为兼容——与 Hak5 自家的 MK7AC Adapter 使用**相同 MT7612U 芯片组**。

---

## 4. 兼容性矩阵

| 评估项 | 结果 | 备注 |
|---|---|---|
| 芯片组兼容性 | ✅ **完全** | MT7612U 是 MK7 确认兼容的芯片 |
| 驱动可用性 | ✅ **已预载** | `kmod-mt76x2u` 内置于 Firmware 2.x |
| USB 识别 | ✅ **自动** | VID/PID 由 `mt76x2u` 自动匹配 |
| 监听模式 | ✅ **支持** | 可通过 `airmon-ng` 或 `iw` |
| 数据包注入 | ✅ **支持** | 通过 mac80211 框架 |
| 5 GHz 扫描 | ✅ **支持** | 插入后显示为 `wlan3` |

---

## 5. 逐步设置指南

### 前置条件

- WiFi Pineapple MK7 运行 **Firmware 2.x**（建议 2.1.3 Stable 或更新）
- ALFA AWUS036ACM——验证正版芯片：`lsusb` 应显示 PID `7612`
- MK7 上的互联网连接
- SSH 客户端

### 步骤 1：连接并确认 USB 检测

```bash
ssh root@172.16.42.1
lsusb
```

预期输出应包含：`ID 0e8d:7612 MediaTek Inc.`

### 步骤 2：确认驱动已加载

```bash
lsmod | grep mt76
```

### 步骤 3：确认无线接口出现

```bash
iw dev
```

### 步骤 4：启用监听模式

```bash
airmon-ng check kill
airmon-ng start wlan3
```

### 步骤 5：锁定 5 GHz 信道并扫描

```bash
iw wlan3mon set channel 36
airodump-ng --band a wlan3mon
```

### 步骤 6：测试数据包注入

```bash
aireplay-ng --test wlan3mon
```

### 步骤 7：开机自动启用（可选）

```bash
cat >> /etc/rc.local << 'EOF'
sleep 5
if iw dev wlan3 info > /dev/null 2>&1; then
    ip link set wlan3 down
    iw wlan3 set monitor control
    ip link set wlan3 up
    logger "AWUS036ACM set to monitor mode"
fi
EOF
```

---

## 6. 验证结果

所有测试在 MK7 Firmware 2.1.3 上使用正版 ALFA AWUS036ACM 执行，全部通过。

---

## 7. 建议

**ALFA AWUS036ACM 是目前能买到、最适合扩展 WiFi Pineapple Mark VII 至 5 GHz 的无线网卡。**

👉 [ALFA AWUS036ACM 产品页面](/zh-cn/products/alfa/awus036acm/)

我们是 ALFA Network 授权经销商，为所有 ALFA × HAK5 集成场景提供完整技术支持。

*需要设置协助？联系 Yupitek 技术支持团队：[yupitek.com/support](/zh-cn/support/)*
