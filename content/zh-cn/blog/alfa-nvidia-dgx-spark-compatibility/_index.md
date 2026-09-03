---
title: "ALFA 无线网卡是否支持 NVIDIA DGX Spark（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "边缘 AI / GPU 伺服器"
description: "DGX Spark 执行 NVIDIA DGX OS（基于 Ubuntu，kernel 6.x），对 ALFA 网卡的相容性与一般现代 Linux 桌面系统相同。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驱动，开箱即用；Realtek 晶片机型（AWUS036ACH / ACS / EACS / AX / AXER）需..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 NVIDIA DGX Spark（GB10 Grace Blackwell）个人 AI 超级电脑上使用？」

简短结论：DGX Spark 执行 NVIDIA DGX OS（基于 Ubuntu，kernel 6.x），对 ALFA 网卡的相容性与一般现代 Linux 桌面系统相同。MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驱动，开箱即用；Realtek 晶片机型（AWUS036ACH / ACS / EACS / AX / AXER）需编译 out-of-tree 驱动（ARM64 / aarch64 架构）。注意：DGX Spark 的 USB 埠均为 USB Type-C，ALFA 网卡为 USB Type-A，需使用 USB-C to USB-A 转接器或传输线。

判定母体：ALFA 现役 9 款 USB 网卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目标硬体规格架构

### 2.1 NVIDIA DGX Spark 硬体规格

| 项目 | 规格 |
|---|---|
| 产品名称 | NVIDIA DGX Spark |
| 核心晶片 | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架构，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 效能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS |
| 系统记忆体 | 128GB LPDDR5x 统一记忆体（256-bit，273 GB/s） |
| 储存 | 最高 4TB NVMe M.2 SSD（自加密） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps），其中 1 个支持 PD 输入（180W EPR PD3.1） |
| 显示输出 | 1× HDMI 2.1a |
| 有线网路 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（200G QSFP） |
| 无线网路 | Wi-Fi 7（内建）+ Bluetooth 5.4 |
| 作业系统 | NVIDIA DGX OS（基于 Ubuntu Linux，kernel 6.x） |
| 架构 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 约 1.2 kg |
| 供电 | 240W USB-C 电源供应器 |

### 2.2 软体环境：NVIDIA DGX OS

| 项目 | 说明 |
|---|---|
| 基础 | Ubuntu Linux（NVIDIA 客制化） |
| Kernel | Linux 6.x（具体版本随 DGX OS 更新） |
| 架构 | aarch64（ARM64） |
| 预装软体 | NVIDIA AI 软体堆叠（CUDA、cuDNN、TensorRT、PyTorch、Jupyter 等） |
| 套件管理 | apt（Debian/Ubuntu 系） |
| 驱动框架 | 标准 Linux kernel driver 架构（cfg80211 / mac80211） |

### 2.3 关键特征：现代 kernel + ARM64

DGX Spark 的软体环境对 ALFA 网卡相容性有两个关键影响：

- Kernel 6.x（现代）：所有进入 mainline 的 WiFi 驱动均可直接使用，包括 mt76（MT7612U / MT7610U）和 mt7921u（MT7921AUN）。这与 Jetson Nano 的 kernel 4.9 形成鲜明对比。
- ARM64（aarch64）架构：Realtek out-of-tree 驱动（8812au / 8821cu / rtl8852bu）需在 ARM64 上编译。这些驱动的上游（morrownr）已支持 ARM64 编译，但需确认 Makefile 中的 CONFIG_PLATFORM_ARM64 = y。

### 2.4 USB Type-C 转接需求

DGX Spark 的 4 个 USB 埠均为 Type-C，而 ALFA 全系列网卡（除 AXML 为 USB-C 外）均为 USB Type-A 介面：

| 机型 | 介面规格 | 是否需转接 |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ 不需转接（可直接插入） |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ 需要 USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ 需要 |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ 需要 |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ 需要 |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ 需要 |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ 需要 |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ 需要 |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ 需要 |

建议：使用支持 USB 3.2 Gen 2×2（20Gbps）的 USB-C to USB-A 转接器或传输线，确保 AWUS036ACH / ACM / AX 等 USB 3.x 机型可发挥全速。

## 3. 分析目前 ALFA 网路卡规格和晶片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下（判定母体：9 款）：

| 机型 | Wi-Fi 等级 | 晶片组 | 介面 | Linux 驱动状态 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel（mt7921u，kernel 5.19+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel（mt7921u） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89（kernel 5.16+，USB 支持陆续合入）或 out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree（morrownr/8812au，需 ARM64 编译） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel（mt76x2u）⭐ 首选 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree（8812au 涵盖） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree（morrownr/8821cu） |

## 4. 适用机型与晶片组

### 4.1 推荐等级分类

| 推荐等级 | 机型（晶片组） | 说明 |
|---|---|---|
| ⭐ 强烈推荐 | AWUS036ACM（MT7612U） | in-kernel 驱动，开箱即用，AC1200 双频，支持 AP / Monitor / Injection |
| ✅ 推荐 | AWUS036ACHM（MT7610U） | in-kernel 驱动，低功耗，AC433 双频 |
| ✅ 推荐（Wi-Fi 6E） | AWUS036AXML / AXM（MT7921AUN） | in-kernel 驱动，Wi-Fi 6E，AXML 为 USB-C 可直插 |
| ⚠️ 可用但需编译 | AWUS036ACH（RTL8812AU） | 需编译 morrownr/8812au（ARM64），完成后功能完整（含 Monitor / Injection） |
| ⚠️ 可用但需编译 | AWUS036ACS（RTL8811AU） | 由 8812au 驱动涵盖 |
| ⚠️ 可用但需编译 | AWUS036EACS（RTL8811CU） | 需编译 morrownr/8821cu（ARM64） |
| ⚠️ 可用但需注意 | AWUS036AX / AXER（RTL8832BU） | kernel 6.x 的 rtw89 可能已支持 USB；若无需编译 out-of-tree |

### 4.2 使用场景建议

| 使用场景 | 建议机型 | 说明 |
|---|---|---|
| 一般无线上网（最简单） | AWUS036ACM / ACHM | in-kernel 驱动，免编译，开箱即用 |
| 无线渗透测试 / 监听 / 注入 | AWUS036ACH 或 AWUS036ACM | 两者均支持 Monitor + Injection；ACH 需编译，ACM 开箱即用 |
| Wi-Fi 6E / 6GHz 频段 | AWUS036AXML / AXM | MT7921AUN in-kernel 驱动，kernel 6.x 完整支持 |
| 已有 AWUS036ACH 想继续用 | AWUS036ACH | 编译 ARM64 驱动即可，功能完整 |
| 不需要外接 WiFi（使用内建） | — | DGX Spark 已内建 Wi-Fi 7，一般上网不需外接 ALFA |

注意：DGX Spark 已内建 Wi-Fi 7 + Bluetooth 5.4，一般上网场景不需要外接 ALFA 网卡。外接 ALFA 的主要需求是：渗透测试（监听/注入）、特殊晶片组需求、或内建 WiFi 不够用的场景。

## 5. 环境需求

### 5.1 硬体需求

| 项目 | 需求 |
|---|---|
| USB 转接器 | USB-C to USB-A 转接器或传输线（AXML 除外） |
| 供电 | DGX Spark 原厂 240W USB-C 电源供应器（USB 埠供电充足） |
| 散热 | 原厂散热即可（USB WiFi 不会显著增加系统负载） |

### 5.2 软体需求

| 项目 | 需求 |
|---|---|
| DGX OS 版本 | 任意现役版本（kernel 6.x） |
| 编译工具（Realtek 晶片需要） | build-essential、git、bc、dkms |
| 无线管理工具 | iw、wpa_supplicant、network-manager（DGX OS 预设安装） |
| 网路 | 编译驱动期间需有线网路（10GbE）或内建 Wi-Fi 7 联网 |

## 6. 相容性判定

### ALFA 现役机型 × NVIDIA DGX Spark（GB10）相容性矩阵

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

判定依据：DGX OS kernel 6.x 的 mainline 驱动可用性 + morrownr 驱动的 ARM64 支持。MediaTek 晶片因驱动已进入 mainline，在 kernel 6.x 上开箱即用。Realtek 晶片需编译 out-of-tree 驱动，但 ARM64 编译已被上游支持。

## 7. 超详细 Step by Step 设定步骤

### 7.1 前置作业

**步骤 1：开机并登入 DGX Spark**（透过 SSH 或直接连接键盘萤幕）

```bash
ssh username@<dgx-spark-ip>
```

**步骤 2：确认系统架构与 kernel 版本**

```bash
uname -m
# 预期：aarch64
uname -r
# 预期：6.x.x（DGX OS kernel）
```

**步骤 3：（Realtek 晶片需要）安装编译工具**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 路径 A：MediaTek 晶片机型（AWUS036ACM / ACHM / AXML / AXM）— 开箱即用

**步骤 1：插入网卡**

使用 USB-C to USB-A 转接器（AXML 可直接插入 USB-C 埠），将 ALFA 网卡插入 DGX Spark 的 USB 埠。

**步骤 2：确认网卡被侦测**

```bash
lsusb
# 预期输出范例（AWUS036ACM / MT7612U）：
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**步骤 3：确认网路介面已自动建立**

```bash
ip link show
# 预期出现 wlan0 或 wlp... 介面（in-kernel 驱动自动载入）
```

**步骤 4：扫描 WiFi 网路**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**步骤 5：连线到 WiFi（使用 NetworkManager）**

```bash
nmcli dev wifi list
nmcli dev wifi connect "你的WiFi名称" password "你的WiFi密码"
```

**步骤 6：（可选）启用监听模式**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 路径 B：Realtek 晶片机型（AWUS036ACH / ACS / EACS）— 需编译

以 AWUS036ACH（RTL8812AU）为例：

**步骤 1：下载驱动原始码**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**步骤 2：确认 ARM64 编译选项**

编辑 Makefile，确认 `CONFIG_PLATFORM_ARM64 = y`（多数新版本自动侦测 aarch64）。

**步骤 3：编译与安装**

```bash
make
sudo make install
sudo modprobe 8812au
```

**步骤 4：插入 ALFA 网卡（透过 USB-C to USB-A 转接器），确认介面**

```bash
ip link show
# 预期出现 wlan0
```

**步骤 5：连线方式同 7.2 步骤 5（使用 nmcli）**

**步骤 6：（可选）监听模式与注入**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 路径 C：Wi-Fi 6 机型（AWUS036AX / AXER，RTL8832BU）

**步骤 1：先检查 kernel 是否已有 rtw89 USB 支持**

```bash
# 插入网卡后检查
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# 若自动出现 wlan0，代表 kernel 6.x 的 rtw89 已支持，可直接使用
```

**步骤 2：若 kernel 未自动支持，编译 out-of-tree 驱动**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# 确认 CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB-C 转接器不良 / 接触不良 | 更换 USB-C to USB-A 转接器；确认转接器支持资料传输（非仅充电）；尝试不同 USB-C 埠 |
| MediaTek 晶片插入后无 wlan 介面 | kernel module 未自动载入 / firmware 缺失 | 手动载入：`sudo modprobe mt76x2u`；检查 `dmesg \| grep mt76`；安装 firmware：`sudo apt install linux-firmware` |
| Realtek 驱动 make 报错 aarch64-linux-gnu-gcc: not found | 交叉编译设定错误 | 确认在 DGX Spark 上原生编译（非交叉编译）；Makefile 中不应设定 CROSS_COMPILE |
| modprobe 8812au 报 Operation not permitted | Secure Boot / 模组签章 | DGX Spark 预设不启用 Secure Boot；若有启用，需签章模组或关闭 Secure Boot |
| WiFi 连线不稳 / 速度慢 | USB-C 转接器仅支持 USB 2.0 | 更换支持 USB 3.2 Gen 2×2 的转接器；确认转接器标示「Data」而非「Charge Only」 |
| 内建 Wi-Fi 7 与外接 ALFA 冲突 | 两个无线介面路由冲突 | 停用内建 WiFi：`sudo nmcli radio wifi off` 或在 BIOS/UEFI 中停用；或设定路由优先顺序 |
| 6GHz（Wi-Fi 6E）无法使用 | Regulatory Domain 限制 | 设定法规区域：`sudo iw reg set US`（美国开放 6GHz）；确认 AWUS036AXML/AXM 的 firmware 支持 6GHz |
| AP 模式启动失败 | NetworkManager 与 hostapd 冲突 | 参考 Yupitek ALFA Soft AP 指南；停用 NetworkManager 管理该介面后手动设定 hostapd |
| 唤醒后网卡消失 | USB 自动暂停 | 停用 USB 自动暂停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 转接需求：除 AXML 外，所有 ALFA 网卡需 USB-C to USB-A 转接器，转接器品质会影响效能与稳定性
- Realtek 晶片需手动编译：RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU 未进入 mainline，需在 ARM64 上编译 out-of-tree 驱动
- 内建 Wi-Fi 7 可能与外接冲突：DGX Spark 已内建 Wi-Fi 7，同时使用内建与外接 WiFi 时可能出现路由或资源冲突
- AP 模式需手动设定：DGX OS 预设为开发环境，AP 热点模式需手动安装设定 hostapd / dnsmasq
- 6GHz 法规限制：Wi-Fi 6E 的 6GHz 频段可用性取决于法规区域设定，台湾地区 6GHz 开放状况需确认最新法规
- 驱动更新依赖上游：Realtek out-of-tree 驱动由社群（morrownr）维护，DGX OS kernel 更新后可能需要重新编译
- 渗透测试功能差异：MediaTek mt76 系列的注入功能在 kernel 6.x 上已改善，但 Realtek 8812au 仍是渗透测试社群的传统首选
- 蓝牙功能：AWUS036AXM 的蓝牙 5.2 功能在 DGX OS 上未经广泛验证（DGX Spark 已内建 BT 5.4）
- ⚠️ **RTL8832BU（AWUS036AX/AXER）驱动维护者已公开建议避免使用**：驱动维护者 morrownr 官方声明指出 rtl8852/32au 系列「是很糟糕的驱动，怀疑晶片本身有问题」，建议 Linux 使用者现阶段避开（来源见第 10 节）。本文第 4、6 节对这两款机型的「⚠️ 可用但需注意」评级应理解为业界共识偏向不建议，而非单纯的安装难度问题
- 本文所引用的 RTL8812AU「out-of-tree」判定为 2026 年初资讯；实际上该晶片的 mac80211 标准相容 in-kernel 驱动已于 **kernel 6.13 并入主线、6.14 起品质成熟**（morrownr 官方公告），DGX OS 若采用 6.14+ 核心，AWUS036ACH 有机会不需编译即可使用，建议客服在回复前先请客户回报 `uname -r` 确认

反驳条件：若 DGX OS 更新后 kernel 版本或 USB 控制器驱动变动导致行为不同，或 morrownr 驱动停止维护 ARM64 分支，本文第 6 节相容性矩阵需重新检视；若 rtw89 USB 支持在 kernel 6.x 正式完整落地，AWUS036AX / AXER 的判定可由「可用但需注意」升级。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| NVIDIA DGX Spark 官方页面 | DGX Spark 规格与平台资讯 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX 文档 | DGX OS 系统架构与 kernel 版本 | https://docs.nvidia.com/dgx/dgx-spark | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动（ARM64 支持） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驱动 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驱动 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Linux kernel mt76 驱动文档 | MediaTek mt76 / mt7921 mainline 驱动说明（含各晶片支持起始 kernel 版本） | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | ALFA 在 Linux 上的 AP 模式设定指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 产品总览（Yupitek） | ALFA 现役产品规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驱动维护者官方声明：建议避开 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU 驱动状态最新公告（kernel 6.13 并入主线、6.14 品质成熟） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[ALFA 无线网卡是否支持 ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 无线网卡是否支持 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 无线网卡是否支持 GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免责声明：本文相容性判定以 NVIDIA DGX OS（kernel 6.x, aarch64）为基准。MediaTek 晶片驱动为 Linux mainline，稳定性高；Realtek 晶片驱动为社群维护（morrownr），实际稳定性可能随版本变化。DGX Spark 已内建 Wi-Fi 7，外接 ALFA 网卡主要用于渗透测试或特殊晶片组需求。USB-C 转接器的品质会直接影响使用体验，建议选择有品牌、标示 USB 3.2 Gen 2×2 的转接器。
