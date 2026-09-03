---
title: "ALFA USB 网卡 Linux 驱动怎么选：MediaTek 免编译 vs Realtek 需编译"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "驱动 / 选购指南"
description: "> **技术支持文件 · 2026-09-03 初版（依 blog-writing-rules.md v1.0 规范撰写）** > 判定母体：Yupitek 现役 ALFA USB 网卡中本次技术文件矩阵已收录的 6 款机型（3 款 MediaTek、3 款 Realtek）。 > 相关文章：[AL"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **技术支持文件 · 2026-09-03 初版（依 blog-writing-rules.md v1.0 规范撰写）**
> 判定母体：Yupitek 现役 ALFA USB 网卡中本次技术文件矩阵已收录的 6 款机型（3 款 MediaTek、3 款 Realtek）。
> 相关文章：[ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)｜[ALFA 无线网卡是否支持 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA 无线网卡是否支持 DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## 一句话结论

**6 款盘点机型中，3 款 MediaTek 晶片（MT7610U / MT7612U / MT7921AUN）在现代 kernel 已内建驱动、插上即用；3 款 Realtek 晶片（RTL8812AU / RTL8811CU / RTL8832BU）一律需要手动编译 out-of-tree 驱动。** 想省事，先看晶片再下单。

---

## 第一幕：场景——为什么有人插上就能用，有人编译两小时

两个真实情境：

- 客户 A 把 **AWUS036ACM** 插上 Ubuntu 桌机，`lsusb` 一跑、NetworkManager 直接出现 wlan0——什么都没装。
- 客户 B 把 **AWUS036ACH** 插上同样的机器，网卡完全没反应，得上 GitHub 拉原始码、装 build 工具、编译、重开机。

差别不在运气，也不在 Linux 发行版，而在**晶片组属于哪个阵营**：MediaTek 的 USB WiFi 晶片驱动（mt76 系列）早已进入 Linux kernel mainline；Realtek 的高阶 USB WiFi 晶片驱动至今仍以 out-of-tree（核心之外）形式散布，要靠社群维护的驱动 repo 手动安装。

## 第二幕：机制——in-kernel 与 out-of-tree 差在哪

### MediaTek：mt76 主线驱动，插上即用

MediaTek USB 晶片的驱动由 kernel 的 **mt76** 子系统涵盖：

| 机型 | 晶片组 | kernel 驱动模组 | 免编译条件 |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | kernel 内建，无版本门槛疑虑 |
| AWUS036ACM | MT7612U | mt76x2u | kernel 内建，无版本门槛疑虑 |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **需 kernel 5.19+** |

⚠️ 唯一的坑：**MT7921AUN 的 kernel 门槛是 5.19+**。老平台（如 Jetson Nano 的 JetPack 4.x，kernel 4.9）无法 backport，直接不可用——这是我们在 Jetson Nano 技术文件中验证过的结论（见 [ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4）。

### Realtek：out-of-tree，一律手动编译

Realtek USB 晶片没有可用的 mainline 驱动，依赖社群维护的驱动 repo。目前最活跃的维护者是 **morrownr**，本盘点 3 款晶片对应 3 个 repo：

| 机型 | 晶片组 | 驱动 repo（morrownr 维护） | 2026-09-03 查核 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ 已查核 |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ 已查核 |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ 已查核 |

### 套用到三种典型环境

| 环境 | kernel | MediaTek 阵营（3 款） | Realtek 阵营（3 款） |
|---|---|---|---|
| GB10 / DGX Spark 类平台 | 6.x + aarch64 | 全数可用（mt76 内建） | 全数需编译（ARM64 可成） |
| Jetson Nano（JetPack 4.x） | 4.9 | 7610U/7612U 可用；MT7921AUN **不可用** | 8812au 可编译（ARM64 支持）；其余未验证 |
| OpenWrt 路由器 | 依版本 | 全数可用（MT7921AUN 需 23.05+） | 需对应 kmod 或编译，难度高 |

（各环境的完整判定矩阵见 [ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)、[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)、[ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)。）

## 第三幕：工具箱——三分钟判定流程与安装步骤

### 判定表：拿到网卡先做这三步

```bash
# 步骤 1：确认系统看得到网卡（记下 VID:PID）
lsusb

# 步骤 2：查 kernel 是否已载入对应驱动
lsmod | grep -E "mt76|rtl8"

# 步骤 3：确认 kernel 版本（决定 MT7921AUN 可否使用）
uname -r
```

判定逻辑（母体：上表 6 款机型）：

1. `lsusb` 出现 **MediaTek / MT76xx** → in-kernel 阵营，kernel ≥ 5.19（MT7921AUN 机型）或任意近代 kernel，即插即用。
2. `lsusb` 出现 **Realtek RTL88xx** → out-of-tree 阵营，走下方安装步骤。
3. `lsusb` **完全没有**新装置 → 先换 USB 埠／线材排除硬体问题，再确认机型是否为 Wi-Fi 6 的 RTL8832BU（部分批次需 `usb_modeswitch`，该步骤属于个别机型问题，不在本盘点矩阵内，暂不展开）。

### Realtek 阵营通用安装（以 AWUS036ACH 为例）

```bash
# 步骤 1：安装编译依赖（Debian/Ubuntu 系）
sudo apt install build-essential dkms linux-headers-$(uname -r)

# 步骤 2：取得驱动原始码（机型对应 repo 见上表）
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# 步骤 3：安装（DKMS 注册，换 kernel 不用重装）
sudo ./install-driver.sh

# 步骤 4：重开机后验证
lsmod | grep 88XXau
ip link   # 应出现新的 wlan 介面
```

> **表 1 结论：判定先于安装——先看晶片组，90 秒决定你是「插上即用」还是「进 repo 编译」，不必先撞墙。**

### 选购建议（结论句）

- **要免编译**：选 MediaTek 阵营（AWUS036ACHM / ACM / AXML），近代 kernel 全部即插即用。
- **要 Wi-Fi 6 且免编译**：选 AWUS036AXML（MT7921AUN），但先确认 kernel ≥ 5.19。
- **有特殊需求非 Realtek 不可**（如特定 monitor mode 工具链）：预留 20–40 分钟做驱动编译，并确认目标平台有 kernel headers。

## 已知限制与反驳条件

本文结论在以下条件**不成立**，请改采替代方案：

1. **kernel 5.19 以下 + MT7921AUN**：mt7921u 无法 backport（依赖现代 kernel 基础设施），结论反转为「不可用」。这是本文最重要的例外。
2. **非 x86/ARM64 Linux**（如某些 MIPS 路由器）：morrownr repo 未保证可编译，需以 OpenWrt 的 kmod 优先（见 [ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)）。
3. **驱动 repo 版本演进**：morrownr repo 以日期命名（如 rtl8852bu-20250826），未来可能改版或移除；安装前请以 repo 现况为准。
4. **monitor mode / AP 模式能力**：同晶片不同 kernel 版本的能力有差异（例如 OpenWrt 22.03+ 的 rtl8812au-ct 在 24.10 有 crash 回报），精细的能力矩阵以各环境专文为准。
5. **RTL8832BU（AWUS036AX/AXER）不在本文盘点的 6 款机型内，但客服常会被连带问到**：驱动维护者 morrownr 已公开表示该晶片系列「是很糟糕的驱动，怀疑晶片本身有问题」，建议 Linux 使用者现阶段避开，不只是「需要编译」的难度问题，回复客户时应如实说明。

## 参考来源

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux 驱动 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驱动 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驱动 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Yupitek ALFA 产品总览 | 现役机型与规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| Yupitek Blog：Soft AP 指南 | AP 模式实作验证文 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| 本站技术文件 9 篇 | 判定矩阵与环境验证基础 | 相对连结（见文首「相关文章」） | ✅ 已查核 | 2026-09-03 |

> kernel mt76 官方 wiki 页：https://wireless.wiki.kernel.org/en/users/drivers/mediatek （已查核，列出各晶片支持起始 kernel 版本，可作为快速核对依据）

## 免责声明

本文件由榆合科技（Yopitek Ltd）技术支持整理，规格与驱动状态可能随 kernel 与驱动 repo 更新而变动，安装前请以官方 repo 与原厂规格页为准。ALFA Network 为本公司正式授权代理品牌。
