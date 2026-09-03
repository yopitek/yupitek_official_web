---
title: "ALFA 无线网卡是否支持 ASUS Ascent GX10（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "边缘 AI / GPU 伺服器"
description: "ASUS Ascent GX10 与 NVIDIA DGX Spark 共享相同的 GB10 硬体平台与 DGX OS 软体环境，对 ALFA 网卡的相容性完全一致（判定母体：ALFA 现役 9 款 USB 网卡）。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM，4 款）使用 in-kernel 驱动，开箱即用；Realtek 晶片机型（AWUS03..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 ASUS Ascent GX10（NVIDIA GB10 Grace Blackwell）AI 超级电脑上使用？」

简短结论：ASUS Ascent GX10 与 NVIDIA DGX Spark 共享相同的 GB10 硬体平台与 DGX OS 软体环境，对 ALFA 网卡的相容性完全一致（判定母体：ALFA 现役 9 款 USB 网卡）。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM，4 款）使用 in-kernel 驱动，开箱即用；Realtek 晶片机型（AWUS036ACH / ACS / EACS / AX / AXER，5 款）需在 ARM64 上编译 out-of-tree 驱动。注意：GX10 的 USB 埠均为 USB Type-C（3 个资料埠 + 1 个 PD 输入埠），ALFA 网卡（AXML 除外）需使用 USB-C to USB-A 转接器。

## 2. 分析目标硬体规格架构

### 2.1 ASUS Ascent GX10 硬体规格

| 项目 | 规格 |
|---|---|
| 产品名称 | ASUS Ascent GX10 |
| 核心晶片 | NVIDIA GB10 Grace Blackwell Superchip（DGX Spark 平台） |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架构，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 效能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS |
| 系统记忆体 | 128GB LPDDR5x 统一记忆体（256-bit，273 GB/s） |
| 储存 | 最高 4TB NVMe M.2 SSD（自加密） |
| USB | 3× USB 3.2 Gen 2×2 Type-C（20Gbps，DP Alt Mode / DisplayPort 2.1）+ 1× USB 3.2 Gen 2×2 Type-C（PD 输入，180W EPR PD3.1） |
| 显示输出 | 1× HDMI 2.1（可搭配 USB-C DP Alt Mode 做多萤幕输出） |
| 有线网路 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（2× 200G QSFP112） |
| 无线网路 | Wi-Fi 7（MediaTek AW-EM637，2×2 MIMO）+ Bluetooth 5.4 |
| 作业系统 | NVIDIA DGX OS（基于 Ubuntu Linux，kernel 6.x） |
| 架构 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 51 mm（5.91 × 5.91 × 2.01 inch） |
| 重量 | 1.48 kg |
| 散热 | ASUS 专利散热系统（静音风扇 + 热导管） |
| 其他 | Kensington 防盗锁孔 |

> ⚠️ 规格修正注记：原稿尺寸写「150 × 150 × 50 mm」且无重量，经查核 ASUS 官方 techspec 为 **150 × 150 × 51 mm / 1.48 kg**，已修正。HDMI 版本依官方为 2.1（原稿写 2.1b 已修正）。见第 10 节参考来源。

### 2.2 软体环境：NVIDIA DGX OS

| 项目 | 内容 |
|---|---|
| 基础 OS | Ubuntu Linux（NVIDIA 客制化） |
| Kernel | Linux 6.x |
| 架构 | aarch64（ARM64） |
| 预装软体 | NVIDIA AI 软体堆叠（CUDA、cuDNN、TensorRT、PyTorch、Jupyter 等） |
| 套件管理 | apt |

### 2.3 与 DGX Spark 的差异

| 差异项 | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| 散热设计 | ASUS 专利散热系统 | NVIDIA 参考散热 |
| 机构设计 | ASUS 客制化机壳 | NVIDIA 参考机壳 |
| 无线模组 | MediaTek AW-EM637（Wi-Fi 7） | 同级 Wi-Fi 7 模组 |
| 配件 | ASUS 原厂配件 | NVIDIA 原厂配件 |
| 保固 | ASUS 保固 | NVIDIA 保固 |

对 ALFA 相容性的影响：零影响。USB 控制器、kernel 版本、驱动框架均与 DGX Spark 完全相同。

### 2.4 USB Type-C 转接需求

GX10 的 4 个 USB 埠均为 Type-C：

- 3 个资料埠（支持 DP Alt Mode，可接萤幕）
- 1 个 PD 输入埠（用于供电）

ALFA 全系列网卡（除 AXML 为 USB-C 外）均为 USB Type-A，需使用转接器。

## 3. 分析目前 ALFA 网路卡规格和晶片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下：

| 机型 | Wi-Fi 等级 | 晶片组 | 介面 | Linux 驱动状态 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel（mt7921u） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel（mt7921u） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree（8812au） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel（mt76x2u）⭐ 首选 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree（8812au 涵盖） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree（8821cu） |

## 4. 适用机型与晶片组

### 4.1 推荐等级分类

| 推荐等级 | 机型（晶片组） | 说明 |
|---|---|---|
| ⭐ 强烈推荐 | AWUS036ACM（MT7612U） | in-kernel 驱动，开箱即用，AC1200 双频，支持 AP / Monitor / Injection |
| ✅ 推荐 | AWUS036ACHM（MT7610U） | in-kernel 驱动，低功耗，AC433 双频 |
| ✅ 推荐（Wi-Fi 6E） | AWUS036AXML / AXM（MT7921AUN） | in-kernel 驱动，Wi-Fi 6E，AXML 为 USB-C 可直插 |
| ⚠️ 可用但需编译 | AWUS036ACH（RTL8812AU） | 需编译 morrownr/8812au（ARM64），完成后功能完整 |
| ⚠️ 可用但需编译 | AWUS036ACS / EACS | 需编译对应 out-of-tree 驱动 |
| ⚠️ 可用但需注意 | AWUS036AX / AXER（RTL8832BU） | kernel 6.x 的 rtw89 可能已支持；若无需编译 |

### 4.2 使用场景建议

| 使用场景 | 建议机型 | 说明 |
|---|---|---|
| 一般无线上网（最简单） | AWUS036ACM / ACHM | in-kernel 驱动，免编译 |
| 无线渗透测试 / 监听 / 注入 | AWUS036ACH 或 AWUS036ACM | 两者均支持 Monitor + Injection |
| Wi-Fi 6E / 6GHz | AWUS036AXML / AXM | MT7921AUN in-kernel 驱动 |
| 不需要外接 WiFi | — | GX10 已内建 Wi-Fi 7，一般上网不需外接 |

## 5. 环境需求

### 5.1 硬体需求

| 项目 | 需求 |
|---|---|
| USB 转接器 | USB-C to USB-A 转接器或传输线（AXML 除外），建议支持 USB 3.2 Gen 2×2 |
| 供电 | ASUS GX10 原厂 USB-C 电源供应器（180W EPR PD3.1） |

### 5.2 软体需求

| 项目 | 需求 |
|---|---|
| DGX OS 版本 | 任意现役版本（kernel 6.x） |
| 编译工具（Realtek 晶片需要） | build-essential、git、bc、dkms |
| 无线管理工具 | iw、network-manager（DGX OS 预设安装） |

## 6. 相容性判定

### ALFA 现役机型 × ASUS Ascent GX10（GB10）相容性矩阵

| 机型 | 晶片组 | 驱动方式 | USB 侦测 | STA 上网 | AP 模式 | Monitor | 安装难度 | 综合评价 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | 免安装 | ⭐ 最佳 |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安装 | ✅ 良好 |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安装 | ✅ 良好 |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安装 | ✅ 良好 |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | 中（编译） | ⚠️ 可用 |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | 中（编译） | ⚠️ 可用 |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | 中（编译） | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | 中-高 | ⚠️ 可用 |
| AWUS036AXER | RTL8832BU | 同上 | ✅ | ⚠️ | ⚠️ | ❌ | 中-高 | ⚠️ 可用 |

判定依据：ASUS GX10 与 DGX Spark 共享相同的 GB10 硬体平台与 DGX OS（kernel 6.x, aarch64），相容性判定与 DGX Spark 完全一致。

## 7. 超详细 Step by Step 设定步骤

ASUS GX10 的安装步骤与 NVIDIA DGX Spark 完全相同。以下为精简版，完整步骤请参考 [ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) 第 7 节。

### 7.1 MediaTek 晶片机型（开箱即用）

- 使用 USB-C to USB-A 转接器（AXML 可直插），将 ALFA 网卡插入 GX10 的 USB-C 资料埠
- 确认侦测：`lsusb`
- 确认介面：`ip link show`（应自动出现 wlan0）
- 连线 WiFi：`nmcli dev wifi connect "SSID" password "密码"`

### 7.2 Realtek 晶片机型（需编译）

以 AWUS036ACH（RTL8812AU）为例：

```bash
# 1. 安装编译工具
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. 下载并编译驱动
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# 确认 Makefile 中 CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe 8812au

# 3. 插入网卡后确认介面
ip link show

# 4. 连线 WiFi
nmcli dev wifi connect "SSID" password "密码"
```

### 7.3 监听模式（渗透测试）

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB-C 转接器不良 / 仅充电规格 | 更换支持资料传输的 USB 3.2 Gen 2×2 转接器；尝试不同 USB-C 埠 |
| MediaTek 晶片无 wlan 介面 | module 未自动载入 / firmware 缺失 | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；检查 `dmesg \| grep mt76` |
| Realtek 驱动编译失败 | 交叉编译设定错误 | 确认在 GX10 上原生编译；Makefile 不应设定 CROSS_COMPILE |
| WiFi 速度慢 | 转接器仅支持 USB 2.0 | 更换 USB 3.2 Gen 2×2 转接器 |
| 内建 Wi-Fi 7 与外接冲突 | 路由冲突 | `sudo nmcli radio wifi off` 停用内建 WiFi 后再使用外接 |
| 6GHz 无法使用 | Regulatory Domain 限制 | `sudo iw reg set US`；确认最新法规 |

## 9. 已知限制

- USB Type-C 转接需求：除 AXML 外，所有 ALFA 网卡需 USB-C to USB-A 转接器
- Realtek 晶片需手动编译：RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU 未进入 mainline
- 内建 Wi-Fi 7 可能与外接冲突：GX10 已内建 Wi-Fi 7（MediaTek AW-EM637）
- AP 模式需手动设定：DGX OS 预设为开发环境
- 6GHz 法规限制：Wi-Fi 6E 可用性取决于法规区域
- 驱动更新依赖上游：Realtek out-of-tree 驱动由社群维护，kernel 更新后需重新编译
- ASUS 硬体差异不影响相容性：散热与机构设计差异不影响 USB WiFi 驱动相容性

反驳条件：以上判定以 DGX OS（Ubuntu 基底、kernel 6.x）为前提。若 ASUS 未来推出非 DGX OS 韧体（如自家 Android / 客制化系统版本），判定需重新验证。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| ASUS Ascent GX10 官方 Techspec | GX10 硬体规格（**150×150×51mm / 1.48kg** / USB 配置 / HDMI 2.1） | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ 已查核 | 2026-09-03 |
| ASUS Ascent GX10 官方商城（UK） | GX10 产品页（150 × 150 × 51mm） | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX Spark 官方页面 | GB10 平台资讯 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | ALFA Linux AP 模式指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 产品总览（Yupitek） | ALFA 现役产品规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无线网卡是否支持 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 无线网卡是否支持 GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 无线网卡是否支持 MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

免责声明：本文相容性判定以 ASUS Ascent GX10 预装的 NVIDIA DGX OS（kernel 6.x, aarch64）为基准。GX10 与 DGX Spark 共享相同硬体平台，相容性完全一致。MediaTek 晶片驱动为 Linux mainline，稳定性高；Realtek 晶片驱动为社群维护。GX10 已内建 Wi-Fi 7，外接 ALFA 主要用于渗透测试或特殊晶片组需求。
