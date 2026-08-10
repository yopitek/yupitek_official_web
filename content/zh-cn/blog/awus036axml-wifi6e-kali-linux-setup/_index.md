---
title: "ALFA AWUS036AXML 安装教程：Wi-Fi 6E 网卡在 Kali Linux 上的监听模式与包注入实测"
locale: zh-CN
hreflang_group: awus036axml-wifi6e-kali-linux-setup
slug: awus036axml-wifi6e-kali-linux-setup
published: 2026-08-10
author: Yupitek
category: technical
tags:
  - AWUS036AXML
  - Kali Linux
hero_image: /static/img/AWUS036AXML/hero.webp
hero_alt: "AWUS036AXML 在 Kali Linux 上怎么装？Wi-Fi 6E 监听模式与包注入教程｜Yupitek"
seo_description: "ALFA AWUS036AXML（MT7921AUN 芯片）在 Kali Linux 上的安装教程：内置 mt7921u 驱动、kernel 版本条件、监听模式、包注入实测与常见排错。"
date: "2026-08-10"
draft: false
showBreadcrumbs: true
showTableOfContents: true
categories:
  - Technical
author: Yupitek
lastmod: "2026-08-10"
---

# ALFA AWUS036AXML 安装教程：Wi-Fi 6E 网卡在 Kali Linux 上的监听模式与包注入实测

> TL;DR：ALFA AWUS036AXML 搭载 MediaTek MT7921AUN 芯片，在 Kali Linux（kernel 5.18+）使用**内置 `mt7921u` 驱动即可运行**，不需要另外编译驱动；若要做稳定的 active monitor mode / 包注入，建议 kernel 6.12+ 与带电源的 USB Hub。插入后 `lsusb` 应看到 `0e8d:7961`，接着用 `airmon-ng` 或 `iw` 切换监听模式即可。

## 为什么 Wi-Fi 6E 网卡开始被渗透测试关注？

Wi-Fi 6E 新增的 **6 GHz 频段**（5925–7125 MHz）是近年企业无线网络升级的重点：新一代 AP、高密度会议室、工厂物联网都开始部署 6 GHz。对安全审计人员来说，如果审计对象的环境已引入 6 GHz，你的测试网卡**必须能听到这个频段**——否则审计范围直接少了一大块。

AWUS036AXML 是 ALFA Network 推出的 Wi-Fi 6E USB 网卡，支持 2.4 / 5 / 6 GHz 三频，与上一代热门的 AWUS036ACH（RTL8812AU，仅 2.4/5 GHz）相比，最大差异就是补上了 6 GHz 监听能力。如果你已熟悉 AWUS036ACH 的流程，这篇的步骤会非常亲切。

## AWUS036AXML 规格与版本条件

| 项目 | AWUS036AXML | AWUS036ACH（对照） | AWUS036ACM（对照） |
|---|---|---|---|
| 芯片组 | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| 频段 | 2.4 / 5 / 6 GHz（Wi-Fi 6E） | 2.4 / 5 GHz | 2.4 / 5 GHz |
| Linux 驱动 | `mt7921u`（**内核内置**） | `88XXau`（需自行编译/DKMS） | `mt76`（内核内置） |
| 建议 kernel | ≥ 5.18（6 GHz 支持） | 5.x（较旧亦可） | 5.x |
| active monitor mode | 建议 kernel ≥ 6.12 | 通用 | 通用 |
| USB ID（lsusb） | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| 功耗 | 约 2.7 W（建议带电源 Hub） | 较低 | 较低 |
| 包注入 | 支持（建议实测） | 支持 | 支持 |

> 版本条件说明：`mt7921u` 自 kernel 5.18 起进入主线，6 GHz 频段支持随内核逐步补齐；**active monitor mode（主动式监听）建议 kernel 6.12+**。Kali 2026 默认内核已是 6.14 等级，直接符合条件。

## 事前准备

1. **Kali Linux 2024.x 以上**（建议更新到最新：`sudo apt update && sudo apt full-upgrade -y`）。
2. 确认内核版本：`uname -r`，若低于 5.18 请先升级系统。
3. 一张可用的 USB 3.0 接口；若接在树莓派或 USB Hub 上，**建议用带电源 Hub**（AWUS036AXML 功耗约 2.7 W，供电不足会出现“插了却抓不到”）。
4. 合法测试权限：本教程所有指令仅用于你拥有或获得授权的网络环境。

## 步骤 1：连接网卡并确认系统抓到

插入网卡后，用 `lsusb` 确认设备是否被识别：

```bash
lsusb
```

预期输出中应有：

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` 就是 MT7921AUN 的 USB ID。若看不到，先检查供电（换 USB 接口或加电源 Hub）再试。

确认驱动已加载：

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

Kali 2026 默认内核包含 `mt7921u`，正常情况下插上即加载，**不需要下载或编译任何驱动**——这与 AWUS036ACH（RTL8812AU 需手动装 `88XXau`）是最大差别。

## 步骤 2：确认无线接口

```bash
ip link show
# 或
iwconfig
```

应看到新的无线接口，通常是 `wlan0` 或 `wlan1`（取决于系统既有接口数量）。以下示例以 `wlan1` 为准，请依实际名称替换。

## 步骤 3：启用监听模式

### 方法一：airmon-ng（推荐）

```bash
# 终止可能干扰的服务
sudo airmon-ng check kill

# 启用监听模式（wlan1 换成你的接口名称）
sudo airmon-ng start wlan1
```

成功后会看到 `wlan1mon` 虚拟接口。

### 方法二：iw（精简控制）

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

此方法直接改现有接口，不会建立 `wlan1mon`。

## 步骤 4：确认监听模式已启用

```bash
iwconfig
```

关键字段应为 `Mode:Monitor`：

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

也可以用 `iw dev` 确认 `type monitor`。接着用 `airodump-ng` 做端到端测试：

```bash
sudo airodump-ng wlan1mon
```

若能看到周边 BSSID 列表（含信道、信号强度、加密类型），代表监听模式正常。**扫描 6 GHz 频段**：

```bash
sudo airodump-ng --band 6g wlan1mon
```

> 注意：6 GHz 扫描需要你的网卡驱动/内核支持该频段（kernel 6.12+ 较稳）；若 `--band 6g` 不支持，先扫 5 GHz（`--band a`）确认基本功能，再更新内核后重试。

## 步骤 5：包注入测试

```bash
sudo aireplay-ng --test wlan1mon
```

预期输出关键行：

```text
Injection is working!
```

成功率 80% 以上代表运行可靠；若低于 50%，检查天线方向、USB 供电，或改用 USB 3.0 直连接口。

## 树莓派补充：便携式 Wi-Fi 审计平台

AWUS036AXML 也支持 Raspberry Pi 3B+ / 4 / 5（官方产品页列出），适合组成便携审计工具组。重点提醒：

- **供电**：Pi 的 USB 供电较紧，建议用带电源 USB Hub，避免“偶尔抓不到”。
- **系统**：Kali ARM64 官方镜像（Raspberry Pi 版）即可，安装后同样是内置 `mt7921u`。
- **验证**：`lsusb` 看到 `0e8d:7961`、`lsmod | grep mt7921` 有输出，就代表平台就绪。

## 常见排错

**Q：`lsusb` 看不到 `0e8d:7961` 怎么办？**
99% 是供电不足或连接松动。换一个 USB 3.0 直连接口；若接 Hub，改接带电源 Hub；再不行换一条短一点的 USB 线。

**Q：启用监听模式后接口自动跳回 managed？**
通常是 NetworkManager / wpa_supplicant 在后台抢回控制权。重跑 `sudo airmon-ng check kill`，或手动 `sudo systemctl stop NetworkManager wpa_supplicant`。

**Q：`iwconfig` 显示 `Mode:Managed` 或接口消失？**
驱动可能未被正确加载或内核太旧。先 `lsmod | grep mt7921` 确认模块，再 `uname -r` 确认 kernel ≥ 5.18。

**Q：6 GHz 扫不到任何网络？**
先确认 `iw dev wlan1mon info` 支持的频段；6 GHz 环境本身较少（新部署），且台湾 6 GHz 执照频段开放进度请依 NCC 公告为准。也可以先用 2.4/5 GHz 验证网卡功能正常。

**Q：跟 AWUS036ACH 比，该买哪张？**
审计对象已有 6 GHz 环境 → 选 AWUS036AXML；只需要 2.4/5 GHz 且预算优先 → AWUS036ACH 仍是非常成熟的选择。两者都在 Kali 上可用，差异在频段覆盖与驱动安装方式（AXML 内置免编译）。

## 常见问题（FAQ）

**Q1：AWUS036AXML 在 Kali Linux 需要另外装驱动吗？**
不需要。它使用内核内置的 `mt7921u` 驱动（kernel 5.18+），插入即用；不需要像 AWUS036ACH 那样编译 DKMS 驱动。

**Q2：AWUS036AXML 支持监听模式吗？**
支持。用 `airmon-ng` 或 `iw` 即可启用；要做 active monitor mode（如 deauth 相关测试）建议 kernel 6.12+。

**Q3：Wi-Fi 6E 的 6 GHz 频段在台湾能用于审计吗？**
6 GHz 属于受监管频段，使用前请确认 NCC 对 6 GHz 频段的开放进度与授权规定，并仅测试自己有权限的环境。

**Q4：接在树莓派上抓不到网卡怎么办？**
优先检查供电——AWUS036AXML 功耗约 2.7 W，建议用带电源 USB Hub，并使用质量好的 USB 线。

**Q5：AWUS036AXML 跟 AWUS036ACH 差在哪？**
AXML 是 Wi-Fi 6E（多了 6 GHz）且驱动内核内置；ACH 是双频（2.4/5 GHz）、RTL8812AU 需手动装驱动。两者都是 Kali 上成熟的审计网卡。

## 总结

AWUS036AXML 的安装流程比你想象的简单：**内核 5.18+ → 插入即用（`mt7921u`）→ 确认 `0e8d:7961` → airmon-ng 切监听 → aireplay-ng 验证注入**。它与 AWUS036ACH 的差异核心在于 6 GHz 频段与免编译驱动——如果你的审计范围已进入 Wi-Fi 6E 世代，这张卡是补齐频段覆盖的选择。记得所有测试只在合法授权环境进行。

ALFA Network 系列网卡由 Yupitek（榆合科技）在台湾提供销售与技术支持；需要 AWUS036AXML 或搭配的供电 Hub、天线，欢迎来信 [sales@yupitek.com](mailto:sales@yupitek.com)。