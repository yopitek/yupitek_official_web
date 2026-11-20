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
description: "ALFA 9 款 USB 网卡在 NVIDIA DGX Spark（GB10）的兼容性：ASUS GX10 实测 kernel 6.17 全部使用内置驱动、插上即用免 DKMS；EACS／ACH／ACS 注入最稳，AXM／AXML 注入失败。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本文已依 2026-11 GX10 实测更新：在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）上，ALFA 现役 9 款网卡全部使用 kernel 内置驱动，插上即可用，不需 DKMS。完整数据见 [ALFA 9 款网卡 ARM64 实测总表](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。仅在 GX10 实测，其他 GB10 机型未逐台测试。

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 NVIDIA DGX Spark（GB10 Grace Blackwell）个人 AI 超级电脑上使用？」

简短结论：DGX Spark 运行 NVIDIA DGX OS（基于 Ubuntu，kernel 6.x）。我们在同为 GB10 平台的 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）实测 ALFA 现役 9 款 USB 网卡，全部使用 kernel 内置驱动，插上即可用，不需编译或 DKMS。DGX Spark 使用同一款 GB10 与 NVIDIA kernel 系列，预期行为相同，但仅在 GX10 实测，DGX Spark 未逐台测试。功能差异：MediaTek MT7921 机型（AWUS036AXM / AXML）在 stock kernel 6.17 上数据包注入失败，monitor、AP、WPA3 可用；其余 7 款的 monitor 与注入皆实测可用。各卡驱动进入主线的最低 kernel 版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低于该版本的旧 kernel 才需要社区 DKMS 驱动。注意：DGX Spark 的 USB 端口均为 USB Type-C，ALFA 网卡为 USB Type-A，需使用 USB-C to USB-A 转接器或传输线。

判定母体：ALFA 现役 9 款 USB 网卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目标硬件规格架构

### 2.1 NVIDIA DGX Spark 硬件规格

| 项目 | 规格 |
|---|---|
| 产品名称 | NVIDIA DGX Spark |
| 核心芯片 | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架构，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 性能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS |
| 系统内存 | 128GB LPDDR5x 统一内存（256-bit，273 GB/s） |
| 存储 | 最高 4TB NVMe M.2 SSD（自加密） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps），其中 1 个支持 PD 输入（180W EPR PD3.1） |
| 显示输出 | 1× HDMI 2.1a |
| 有线网络 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（200G QSFP） |
| 无线网络 | Wi-Fi 7（内置）+ Bluetooth 5.4 |
| 操作系统 | NVIDIA DGX OS（基于 Ubuntu Linux，kernel 6.x） |
| 架构 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 约 1.2 kg |
| 供电 | 240W USB-C 电源供应器 |

### 2.2 软件环境：NVIDIA DGX OS

| 项目 | 说明 |
|---|---|
| 基础 | Ubuntu Linux（NVIDIA 定制） |
| Kernel | Linux 6.x（具体版本随 DGX OS 更新） |
| 架构 | aarch64（ARM64） |
| 预装软件 | NVIDIA AI 软件堆栈（CUDA、cuDNN、TensorRT、PyTorch、Jupyter 等） |
| 软件包管理 | apt（Debian/Ubuntu 系） |
| 驱动框架 | 标准 Linux kernel driver 架构（cfg80211 / mac80211） |

### 2.3 关键特征：现代 kernel + ARM64

DGX Spark 的软件环境对 ALFA 网卡兼容性有两个关键影响：

- Kernel 6.x（现代）：kernel 6.17（GX10 实测版本）已内置本文 9 款网卡的驱动，包括 mt76（MT7612U / MT7610U，4.19+）、mt7921u（MT7921AUN，5.18+）、rtw88（RTL8821CU 6.2+；RTL8812AU / RTL8811AU 6.13+）与 rtw89（RTL8832BU，6.17+）。这与 Jetson Nano 的 kernel 4.9 形成鲜明对比。
- ARM64（aarch64）架构：使用 kernel 内置驱动时不需要在 ARM64 上编译任何东西；只有 kernel 低于该卡最低版本的旧系统，Realtek 机型才需要编译社区 DKMS 驱动（如 morrownr 系列，需确认 Makefile 中 CONFIG_PLATFORM_ARM64 = y）。

### 2.4 USB Type-C 转接需求

DGX Spark 的 4 个 USB 端口均为 Type-C，而 ALFA 全系列网卡（除 AXML 为 USB-C 外）均为 USB Type-A 接口：

| 机型 | 接口规格 | 是否需转接 |
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

## 3. 分析目前 ALFA 网卡规格和芯片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下（判定母体：9 款）：

| 机型 | Wi-Fi 等级 | 芯片组 | 接口 | Linux 内置驱动（最低 kernel 版本） |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E（6GHz 实测可用） | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ 内置（mt7921u，5.18+） |
| AWUS036AXM | Wi-Fi 6E（厂商标示，6GHz 未实测） | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ 内置（mt7921u，5.18+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 内置（rtw89_8852bu，6.17+） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 内置（rtw89_8852bu，6.17+） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 内置（rtw88_8812au，6.13+） |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ 内置（mt76x0u，4.19+） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ 内置（mt76x2u，4.19+） |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ 内置（rtw88_8821au，6.13+） |
| AWUS036EACS | Wi-Fi 5 (AC600) + 蓝牙 | Realtek RTL8821CU | USB 2.0 | ✅ 内置（rtw88_8821cu，6.2+） |

注：GX10 实测的 kernel 6.17 已内置全部 9 款驱动；各卡最低 kernel 版本不同（见上表括号）。kernel 低于该卡最低版本的旧系统，才需要安装社区维护的 DKMS 驱动。

## 4. 适用机型与芯片组

### 4.1 推荐等级分类

| 推荐等级 | 机型（芯片组） | 说明 |
|---|---|---|
| ⭐ 渗透测试首选 | AWUS036EACS（RTL8821CU）/ AWUS036ACH（RTL8812AU）/ AWUS036ACS（RTL8811AU） | 内置驱动免安装；注入实测 EACS、ACH 双频 100%，ACS 2.4GHz 100%、5GHz 96%；可端到端截取 WPA handshake |
| ✅ 推荐 | AWUS036ACM（MT7612U） | 内置驱动免安装；monitor、注入（2.4GHz 63–83%、5GHz 76%）、AP、WPA3 皆可用 |
| ✅ 推荐 | AWUS036ACHM（MT7610U） | 内置驱动免安装；2.4GHz 注入 96–100%，5GHz 注入仅广播可用；WPA3 AP 需设置 sae_pwe=0 |
| ✅ 推荐（Wi-Fi 6） | AWUS036AX / AXER（RTL8832BU） | 内置驱动免安装；monitor 接收强，注入可用（2.4GHz：AX 96%、AXER 73%），AP 支持 80MHz |
| ⚠️ 仅适合连接／AP | AWUS036AXML / AXM（MT7921AUN） | 内置驱动免安装；monitor、AP、WPA3 可用，但 stock kernel 6.17 上注入失败，不适合渗透测试；AXML 为 USB-C 可直插 |

### 4.2 使用场景建议

| 使用场景 | 建议机型 | 说明 |
|---|---|---|
| 一般无线上网（最简单） | 9 款皆可（例如 AWUS036ACM / ACHM） | 全部为 kernel 内置驱动，插上即可用 |
| 无线渗透测试 / 监听 / 注入 | AWUS036EACS / ACH / ACS | 注入实测 96–100%，可端到端截取 WPA handshake；勿选 AXM / AXML（注入失败） |
| Wi-Fi 6 + AP 热点 | AWUS036AX / AXER | 2x2、80MHz AP 实测可用 |
| 6GHz 频段 | AWUS036AXML | 实测可在 6GHz 创建 WPA3 AP；AXM 同芯片但 6GHz 未实测 |
| 已有 AWUS036ACH 想继续用 | AWUS036ACH | kernel 6.13 以上内置 rtw88_8812au，插上即可用，双频注入实测 100% |
| 不需要外置 WiFi（使用内置） | — | DGX Spark 已内置 Wi-Fi 7，一般上网不需外置 ALFA |

注意：DGX Spark 已内置 Wi-Fi 7 + Bluetooth 5.4，一般上网场景不需要外置 ALFA 网卡。外置 ALFA 的主要需求是：渗透测试（监听/注入）、特殊芯片组需求、或内置 WiFi 不够用的场景。

## 5. 环境需求

### 5.1 硬件需求

| 项目 | 需求 |
|---|---|
| USB 转接器 | USB-C to USB-A 转接器或传输线（AXML 除外） |
| 供电 | DGX Spark 原厂 240W USB-C 电源供应器（USB 端口供电充足） |
| 散热 | 原厂散热即可（USB WiFi 不会显著增加系统负载） |

### 5.2 软件需求

| 项目 | 需求 |
|---|---|
| DGX OS 版本 | 任意现役版本（kernel 6.x） |
| Kernel 版本 | kernel 6.17（GX10 实测 6.17.0-1014-nvidia）已内置全部 9 款网卡的驱动，不需编译工具；各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低于该版本才需安装社区 DKMS 驱动 |
| 无线管理工具 | iw、wpa_supplicant、network-manager（DGX OS 默认安装） |

## 6. 兼容性判定

### ALFA 现役机型 × NVIDIA DGX Spark（GB10）兼容性矩阵

| 机型 | 芯片组 | 驱动（kernel 内置） | USB 检测 | STA 上网 | AP 模式 | Monitor | 数据包注入 | 安装难度 | 综合评价 |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 双频 100% | 免安装 | ⭐ 最佳 |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 双频 100% | 免安装 | ⭐ 最佳 |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100%／5G 96% | 免安装 | ⭐ 最佳 |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83%／5G 76% | 免安装 | ✅ 良好 |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100%／5G 仅广播 | 免安装 | ✅ 良好 |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 接收强 | ✅ 2.4G 96%／5G 可用 | 免安装 | ✅ 良好 |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 接收强 | ✅ 2.4G 73%／5G 可用 | 免安装 | ✅ 良好 |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 接收弱 | ❌ 失败 | 免安装 | ⚠️ 仅连接／AP |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 接收弱 | ❌ 失败 | 免安装 | ⚠️ 仅连接／AP |

判定依据：2026-11-16～11-18 于 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）实机测试，测试对象为自有 Wi-Fi 与自有手机。DGX Spark 使用同一款 GB10 与 NVIDIA kernel 系列，预期行为相同，但仅在 GX10 实测，DGX Spark 未逐台测试。完整数据见 [ALFA 9 款网卡 ARM64 实测总表](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 7. 超详细 Step by Step 设置步骤

### 7.1 前置作业

**步骤 1：开机并登录 DGX Spark**（通过 SSH 或直接连接键盘屏幕）

```bash
ssh username@<dgx-spark-ip>
```

**步骤 2：确认系统架构与 kernel 版本**

```bash
uname -m
# 预期: aarch64
uname -r
# 预期: 6.x.x (DGX OS kernel)
```

**步骤 3：确认 kernel 版本是否为 6.17 以上**

kernel 6.17 以上已内置全部 9 款网卡的驱动，不需要安装编译工具。各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）；低于该版本时，Realtek 机型才需要社区 DKMS 驱动（见 7.3 最后一段）。

### 7.2 路径 A：MediaTek 芯片机型（AWUS036ACM / ACHM / AXML / AXM）— 开箱即用

**步骤 1：插入网卡**

使用 USB-C to USB-A 转接器（AXML 可直接插入 USB-C 端口），将 ALFA 网卡插入 DGX Spark 的 USB 端口。

**步骤 2：确认网卡被检测**

```bash
lsusb
# 预期输出范例 (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**步骤 3：确认网络接口已自动创建**

```bash
ip link show
# 预期出现 wlx 开头的接口 (依 MAC 命名, in-kernel 驱动自动加载)
```

**步骤 4：扫描 WiFi 网络**（以下以 wlan0 示意，请换成 `ip link show` 查到的接口名称）

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**步骤 5：连接到 WiFi（使用 NetworkManager）**

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

### 7.3 路径 B：Realtek Wi-Fi 5 机型（AWUS036ACH / ACS / EACS）— kernel 6.13+ 免安装（EACS 6.2+）

**步骤 1：插入网卡并确认驱动已自动加载**

```bash
uname -r          # ACH/ACS 需 6.13 以上, EACS 需 6.2 以上
lsusb
lsmod | grep rtw88
ip link show
```

各机型自动加载的模块：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`（EACS 另含蓝牙，实测可用）。

**步骤 2：连接方式同 7.2 步骤 5（使用 nmcli）**

**步骤 3：（可选）监听模式与注入**

⚠️ 仅在自有或已取得授权的网络进行监听与注入测试。

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # 换成 ip link 查到的接口名称
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- 不要运行 `airmon-ng check kill`：它会关闭 NetworkManager，让主机对外断线。
- AWUS036AXM / AXML 在 stock kernel 6.17 上 `aireplay-ng --test` 会失败（Found 0 APs），无法 deauth 或截取 handshake。
- hcxdumptool 8.x 在 9 款卡上都出现 `failed to arm`，唯 EACS 在 2.4 GHz 除外（驱动不支持 active monitor），请改用 airodump-ng + aireplay-ng。

**旧 kernel（ACH／ACS 低于 6.13、EACS 低于 6.2）才需要的步骤**：安装 `build-essential git bc dkms` 后，编译社区驱动，例如 RTL8812AU 使用 morrownr/8812au-20210820（确认 Makefile 中 `CONFIG_PLATFORM_ARM64 = y`）。版本足够时请直接使用内置驱动。

### 7.4 路径 C：Wi-Fi 6 机型（AWUS036AX / AXER，RTL8832BU）— kernel 6.17+ 免安装

```bash
lsusb                      # 预期出现 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

GX10 实测：kernel 内置 `rtw89_8852bu` 自动加载，monitor 接收强，注入可用（2.4GHz：AX 96%、AXER 73%），AP 支持 80MHz。rtw89_8852bu 自 kernel 6.17 才进入主线，kernel 6.16 以下的系统需要社区 DKMS 驱动（morrownr/rtl8852bu-20250826）。

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB-C 转接器不良 / 接触不良 | 更换 USB-C to USB-A 转接器；确认转接器支持数据传输（非仅充电）；尝试不同 USB-C 端口 |
| MediaTek 芯片插入后无 wlan 接口 | kernel module 未自动加载 / firmware 缺失 | 手动加载：`sudo modprobe mt76x2u`；检查 `dmesg \| grep mt76`；安装 firmware：`sudo apt install linux-firmware` |
| Realtek 卡插上后没有 wlan 接口 | kernel 低于该卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），未内置对应驱动 | 以 `uname -r` 确认版本；升级 kernel，或在旧 kernel 安装社区 DKMS 驱动 |
| 旧 kernel 安装 DKMS 驱动后 modprobe 报 Operation not permitted | Secure Boot / 模块签名 | 需签名模块或关闭 Secure Boot（使用内置驱动不会遇到）|
| 反复切换 monitor／AP 后扫不到任何信号 | RX 停滞（RX stall） | 拔插网卡让 USB 重新枚举 |
| EACS／AXML 重插后没有 wlx 接口 | 蓝牙＋Wi-Fi 复合设备 probe 卡住 | 换一个 USB 端口重插 |
| WiFi 连接不稳 / 速度慢 | USB-C 转接器仅支持 USB 2.0 | 更换支持 USB 3.2 Gen 2×2 的转接器；确认转接器标示「Data」而非「Charge Only」 |
| 内置 Wi-Fi 7 与外置 ALFA 冲突 | 两个无线接口路由冲突 | 禁用内置 WiFi：`sudo nmcli radio wifi off` 或在 BIOS/UEFI 中禁用；或设置路由优先级 |
| 6GHz（Wi-Fi 6E）无法使用 | Regulatory Domain 限制 | 设置法规区域：`sudo iw reg set US`（美国开放 6GHz）；AXML 已实测可在 6GHz 运作，AXM 未实测 |
| AP 模式启动失败 | NetworkManager 与 hostapd 冲突 | 参考 Yopitek ALFA Soft AP 指南；禁用 NetworkManager 管理该接口后手动设置 hostapd |
| 唤醒后网卡消失 | USB 自动暂停 | 禁用 USB 自动暂停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 转接需求：除 AXML 外，所有 ALFA 网卡需 USB-C to USB-A 转接器，转接器质量会影响性能与稳定性
- MT7921 机型注入失败：AWUS036AXM / AXML 在 stock kernel 6.17 上数据包注入失败，无法 deauth 或截取 handshake；monitor、AP、WPA3 可用。主因是 kernel 6.16 以后的 mac80211 chanctx 回归，社区修补版驱动仍有速率限制
- 实测范围：仅在 ASUS GX10（kernel 6.17.0-1014-nvidia）实测；DGX Spark 未逐台测试，预期行为相同
- hcxdumptool 不可用：除 EACS 在 2.4 GHz 外，其余卡皆出现 `failed to arm`，请改用 airodump-ng + aireplay-ng
- 内置 Wi-Fi 7 可能与外置冲突：DGX Spark 已内置 Wi-Fi 7，同时使用内置与外置 WiFi 时可能出现路由或资源冲突
- AP 模式需手动设置：DGX OS 默认为开发环境，AP 热点模式需手动安装设置 hostapd / dnsmasq
- 6GHz 法规限制：Wi-Fi 6E 的 6GHz 频段可用性取决于法规区域设置，台湾地区 6GHz 开放状况需确认最新法规
- 旧 kernel：kernel 低于该卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）的系统，Realtek 机型才需社区 DKMS 驱动（morrownr），且每次 kernel 更新后需重新编译
- 渗透测试功能差异：GX10 实测注入成功率以 Realtek rtw88 机型最高（EACS、ACH 双频 100%）；MediaTek mt76 机型（ACM / ACHM）可用；MT7921（AXM / AXML）失败
- 蓝牙功能：AWUS036AXML 与 AWUS036EACS 的蓝牙在 GX10 上实测可用；AWUS036AXM 的蓝牙未单独验证（DGX Spark 已内置 BT 5.4）
- RTL8832BU（AWUS036AX / AXER）：驱动维护者 morrownr 曾公开建议避开 rtl8852/32au 系列的 out-of-tree 驱动（来源见第 10 节）。本次 GX10 实测使用的是 kernel 内置 `rtw89_8852bu`，monitor、注入、AP、WPA3 皆可用；此结论仅适用于 kernel 6.17 以上的内置驱动
- RTL8812AU（AWUS036ACH）：mac80211 标准的 in-kernel 驱动 `rtw88_8812au` 已于 kernel 6.13 并入主线、6.14 起质量成熟（morrownr 公告）。GX10 实测 kernel 6.17 插上即用、双频注入 100%。客服回复前可先请客户反馈 `uname -r` 确认是否为 6.13 以上

反驳条件：若 DGX OS 更新后 kernel 版本或 USB 控制器驱动变动导致行为不同，或在 DGX Spark 实机上测得与 GX10 不同的结果，本文第 6 节兼容性矩阵需重新查看；若日后 kernel 修正 mt7921u 的注入问题，AWUS036AXM / AXML 的评价可由「仅连接／AP」升级。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| NVIDIA DGX Spark 官方页面 | DGX Spark 规格与平台信息 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX 文档 | DGX OS 系统架构与 kernel 版本 | https://docs.nvidia.com/dgx/dgx-spark | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动（ARM64 支持） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux 驱动（旧 kernel 用） | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驱动 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Linux kernel mt76 驱动文档 | MediaTek mt76 / mt7921 mainline 驱动说明（含各芯片支持起始 kernel 版本） | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yopitek） | ALFA 在 Linux 上的 AP 模式设置指南 | /zh-cn/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA 9 款网卡 ARM64 实测总表（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 实机测试 | https://yupitek.com/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 实测 | 2026-11-18 |
| ALFA Network 产品总览（Yopitek） | ALFA 现役产品规格 | /zh-cn/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驱动维护者官方声明：建议避开 rtl8852/32au（RTL8832BU）芯片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU 驱动状态最新公告（kernel 6.13 并入主线、6.14 质量成熟） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 MSI EdgeXpert](/zh-cn/blog/alfa-msi-edgexpert-compatibility/)｜[ALFA 无线网卡是否支持 ASUS Ascent GX10](/zh-cn/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 无线网卡是否支持 ALTOS BrainSphere GB10 F1](/zh-cn/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 无线网卡是否支持 GIGABYTE AI TOP ATOM](/zh-cn/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 无线网卡是否支持 NVIDIA Jetson Nano](/zh-cn/blog/alfa-nvidia-jetson-nano-compatibility/)

免责声明：本文兼容性判定以 2026-11 在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）的实机测试为基准。DGX Spark 与 GX10 使用同一款 GB10 与 NVIDIA kernel 系列，预期行为相同，但未逐台测试。GX10 实测的 kernel 6.17 已内置 ALFA 9 款网卡的驱动（各卡最低版本不同），kernel 低于该卡最低版本时才需社区 DKMS 驱动（morrownr）。DGX Spark 已内置 Wi-Fi 7，外置 ALFA 网卡主要用于渗透测试或特殊芯片组需求。USB-C 转接器的质量会直接影响使用体验，建议选择有品牌、标示 USB 3.2 Gen 2×2 的转接器。监听与注入仅限在自有或已取得授权的网络进行。
