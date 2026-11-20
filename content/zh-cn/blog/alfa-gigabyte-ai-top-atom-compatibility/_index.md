---
title: "ALFA 无线网卡是否支持 GIGABYTE AI TOP ATOM（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-gigabyte-ai-top-atom-compatibility"
tags:
  - "ALFA"
  - "GIGABYTE"
  - "AI-TOP-ATOM"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "边缘 AI / GPU 伺服器"
description: "ALFA 9 款 USB 网卡在 GIGABYTE AI TOP ATOM（GB10）的兼容性：ASUS GX10 实测 kernel 6.17 全部使用内置驱动、插上即用免 DKMS；EACS／ACH／ACS 注入最稳，AXM／AXML 注入失败。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本文已依 2026-11 GX10 实测更新：在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）上，ALFA 现役 9 款网卡全部使用 kernel 内置驱动，插上即可用，不需 DKMS。完整数据见 [ALFA 9 款网卡 ARM64 实测总表](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。仅在 GX10 实测，其他 GB10 机型未逐台测试。

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 GIGABYTE AI TOP ATOM（型号 ATAGB10-9000，NVIDIA GB10 Grace Blackwell）个人 AI 超级电脑上使用？」

简短结论：GIGABYTE AI TOP ATOM 与 NVIDIA DGX Spark 使用同一款 GB10 芯片与 NVIDIA kernel 系列。我们在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）实测 ALFA 现役 9 款 USB 网卡（AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML），全部使用 kernel 内置驱动，插上即可用，不需编译或 DKMS。预期行为相同，但仅在 GX10 实测，GIGABYTE AI TOP ATOM 未逐台测试。功能差异：MediaTek MT7921 机型（AWUS036AXM / AXML）在 stock kernel 6.17 上数据包注入（packet injection）失败，monitor、AP、WPA3 可用；其余 7 款的 monitor 与注入皆实测可用。各卡驱动进入主线的最低 kernel 版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低于该版本的旧 kernel 才需要社区 DKMS 驱动。注意：AI TOP ATOM 的 USB 端口均为 USB Type-C，ALFA 网卡（AXML 除外）需使用 USB-C to USB-A 转接器。

## 2. 分析目标硬件规格架构

### 2.1 GIGABYTE AI TOP ATOM 硬件规格

| 项目 | 规格 |
|---|---|
| 产品名称 | GIGABYTE AI TOP ATOM（型号：ATAGB10-9000 / ATAGB10-9001） |
| 核心芯片 | NVIDIA GB10 Grace Blackwell Superchip（DGX Spark 平台） |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架构，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 性能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS，支持最高 2000 亿参数模型 |
| 系统内存 | 128GB LPDDR5x 统一内存（256-bit，273 GB/s） |
| 存储 | 最高 4TB M.2 NVMe SSD（ATAGB10-9000 为 PCIe Gen5 4TB；9001 为 Gen4 4TB） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps），其中 1 个为电源输入（与 GB10 参考设计一致） |
| 显示输出 | 1× HDMI 2.1a（可经由 USB-C DP Alt Mode 扩充） |
| 有线网络 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC |
| 无线网络 | Wi-Fi 7 + Bluetooth 5.4 |
| 操作系统 | NVIDIA DGX OS（基于 Ubuntu Linux，kernel 6.x） |
| 架构 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 约 1.2 kg |
| 供电 | 240W USB-C 电源供应器 |
| 保修 | 1 年原厂保修 |

> 规格查核注记：尺寸 50.5mm / 重量 1.2kg 与 GIGABYTE 官方规格一致；蓝牙版本依 GIGABYTE 官方规格页为 **BT 5.4**（[官方规格页](https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM/sp)）。USB 配置为 3 个数据端口 + 1 个供电端口（官方规格为 4× Type-C，其中 1 个 dedicated to system power）。

### 2.2 软件环境：NVIDIA DGX OS

| 项目 | 内容 |
|---|---|
| 基础 OS | Ubuntu Linux（NVIDIA 定制） |
| Kernel | Linux 6.x |
| 架构 | aarch64（ARM64） |
| 预装软件 | NVIDIA AI 软件堆栈（CUDA、cuDNN、TensorRT、PyTorch、Jupyter、Ollama 等）+ GIGABYTE AI TOP Utility |
| 软件包管理 | apt |

### 2.3 与 DGX Spark 的差异

| 差异项 | AI TOP ATOM | NVIDIA DGX Spark |
|---|---|---|
| 结构设计 | GIGABYTE / AORUS 定制机壳 | NVIDIA 参考机壳 |
| 品牌定位 | 个人 AI 超级电脑（桌面 / 办公室） | 桌面 AI 开发参考平台 |
| 存储 | 最高 4TB（Gen5 / Gen4 版本） | 最高 4TB |
| 配件 | GIGABYTE 原厂配件 + AI TOP Utility | NVIDIA 原厂配件 |
| 保修 | 1 年 | 依销售通路 |

对 ALFA 兼容性的影响：预期无影响（仅在 GX10 实测，其他 GB10 机型未逐台测试）。USB 控制器、kernel 版本、驱动框架均与 DGX Spark 完全相同。

### 2.4 USB Type-C 转接需求

AI TOP ATOM 的 USB 端口均为 Type-C，ALFA 全系列网卡（除 AXML 为 USB-C 外）均为 USB Type-A，需使用转接器。建议选择支持 USB 3.2 Gen 2×2（20Gbps）的转接器，确保 AWUS036ACH / ACM / AX 等 USB 3.x 机型可发挥全速。

## 3. 分析目前 ALFA 网卡规格和芯片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下：

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
| 桌面 AI 开发无线上网 | 9 款皆可（例如 AWUS036ACM / ACHM） | 全部为 kernel 内置驱动，插上即可用 |
| 无线渗透测试 / 安全研究 | AWUS036EACS / ACH / ACS | 注入实测 96–100%，可端到端截取 WPA handshake；勿选 AXM / AXML（注入失败） |
| Wi-Fi 6 + AP 热点 | AWUS036AX / AXER | 2x2、80MHz AP 实测可用 |
| 6GHz 频段 | AWUS036AXML | 实测可在 6GHz 创建 WPA3 AP；AXM 同芯片但 6GHz 未实测 |
| 不需要外置 WiFi | — | AI TOP ATOM 已内置 Wi-Fi 7，一般上网不需外置 |

## 5. 环境需求

### 5.1 硬件需求

| 项目 | 需求 |
|---|---|
| USB 转接器 | USB-C to USB-A 转接器或传输线（AXML 除外），建议支持 USB 3.2 Gen 2×2 |
| 供电 | GIGABYTE 原厂 240W USB-C 电源供应器 |

### 5.2 软件需求

| 项目 | 需求 |
|---|---|
| DGX OS 版本 | 任意现役版本（kernel 6.x） |
| Kernel 版本 | kernel 6.17（实测 6.17.0-1014-nvidia）已内置全部 9 款网卡的驱动，不需编译工具；各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低于该版本才需安装社区 DKMS 驱动 |
| 无线管理工具 | iw、network-manager（DGX OS 默认安装） |

## 6. 兼容性判定

### ALFA 现役机型 × GIGABYTE AI TOP ATOM（GB10）兼容性矩阵

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

判定依据：2026-11-16～11-18 于 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）实机测试，测试对象为自有 Wi-Fi 与自有手机。GIGABYTE AI TOP ATOM 使用同一款 GB10 与 NVIDIA kernel 系列，预期行为相同，但仅在 GX10 实测，GIGABYTE AI TOP ATOM 未逐台测试。完整数据见 [ALFA 9 款网卡 ARM64 实测总表](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 7. 超详细 Step by Step 设置步骤

GIGABYTE AI TOP ATOM 的安装步骤与 NVIDIA DGX Spark 预期相同（步骤在 GX10 实测）。以下为精简版，完整步骤请参考 [ALFA 无线网卡是否支持 NVIDIA DGX Spark](/zh-cn/blog/alfa-nvidia-dgx-spark-compatibility/) 第 7 节。

### 7.1 MediaTek 芯片机型（AWUS036ACM / ACHM / AXM / AXML）

- 使用 USB-C to USB-A 转接器（AXML 可直插），将 ALFA 网卡插入 AI TOP ATOM 的 USB-C 数据端口
- 确认检测：`lsusb`
- 确认接口：`ip link show`（应自动出现 wlx 开头的接口）
- 连接 WiFi：`nmcli dev wifi connect "SSID" password "密码"`

### 7.2 Realtek 芯片机型（AWUS036ACH / ACS / EACS / AX / AXER）

kernel 6.17（GX10 实测版本）已内置全部 Realtek 机型的驱动，步骤与 MediaTek 机型相同，不需编译（最低版本：EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）：

```bash
# 1. 确认 kernel 版本 (6.17 以上即内置全部 Realtek 机型驱动; GX10 实测为 6.17.0-1014-nvidia)
uname -r

# 2. 插入网卡后确认驱动已自动加载
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. 连接 WiFi
nmcli dev wifi connect "SSID" password "密码"
```

各机型自动加载的模块：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`、AX / AXER → `rtw89_8852bu`。若 `uname -r` 低于该卡的最低版本（旧版系统），才需要安装社区维护的 DKMS 驱动（例如 RTL8812AU 的 morrownr/8812au-20210820）。

### 7.3 监听模式（渗透测试）

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

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 网卡 | USB-C 转接器不良 / 仅充电规格 | 更换支持数据传输的 USB 3.2 Gen 2×2 转接器；尝试不同 USB-C 端口 |
| MediaTek 芯片无 wlan 接口 | module 未自动加载 / firmware 缺失 | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；检查 `dmesg \| grep mt76` |
| Realtek 卡插上后没有 wlan 接口 | kernel 低于该卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），未内置对应驱动 | 以 `uname -r` 确认版本；升级 kernel，或在旧 kernel 安装社区 DKMS 驱动 |
| 反复切换 monitor／AP 后扫不到任何信号 | RX 停滞（RX stall） | 拔插网卡让 USB 重新枚举 |
| EACS／AXML 重插后没有 wlx 接口 | 蓝牙＋Wi-Fi 复合设备 probe 卡住 | 换一个 USB 端口重插 |
| WiFi 速度慢 | 转接器仅支持 USB 2.0 | 更换 USB 3.2 Gen 2×2 转接器 |
| 内置 Wi-Fi 7 与外置冲突 | 路由冲突 | `sudo nmcli radio wifi off` 禁用内置 WiFi 后再使用外置 |
| 6GHz 无法使用 | Regulatory Domain 限制 | `sudo iw reg set US`；确认最新法规 |
| 系统唤醒后网卡消失 | USB 自动暂停 | `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 转接需求：除 AXML 外，所有 ALFA 网卡需 USB-C to USB-A 转接器
- MT7921 机型注入失败：AWUS036AXM / AXML 在 stock kernel 6.17 上数据包注入失败，无法 deauth 或截取 handshake；monitor、AP、WPA3 可用。主因是 kernel 6.16 以后的 mac80211 chanctx 回归，社区修补版驱动仍有速率限制
- 实测范围：仅在 ASUS GX10（kernel 6.17.0-1014-nvidia）实测；GIGABYTE AI TOP ATOM 未逐台测试，预期行为相同
- hcxdumptool 不可用：除 EACS 在 2.4 GHz 外，其余卡皆出现 `failed to arm`，请改用 airodump-ng + aireplay-ng
- 内置 Wi-Fi 7 可能与外置冲突：AI TOP ATOM 已内置 Wi-Fi 7 + BT 5.4
- AP 模式需手动设置：DGX OS 默认为开发环境
- 6GHz 法规限制：Wi-Fi 6E 可用性取决于法规区域
- 旧 kernel：kernel 低于该卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）的系统，Realtek 机型才需社区 DKMS 驱动，且每次 kernel 更新后需重新编译
- GIGABYTE 硬件差异不影响兼容性：结构与散热设计差异不影响 USB WiFi 驱动兼容性
- 保修与技术支持：kernel 6.17 以上不需安装第三方驱动；若在旧 kernel 安装社区 DKMS 驱动，GIGABYTE 技术支持可能不涵盖第三方驱动问题

反驳条件：以上判定以 DGX OS（Ubuntu 基底、kernel 6.x）为前提。GIGABYTE 若推出非 DGX OS 的自有固件版本，判定需重新验证；蓝牙版本（5.4）以出货批量规格为准，建议收货后以官方页面覆核。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| GIGABYTE AI TOP ATOM 官方产品页 | AI TOP ATOM 硬件规格（ATAGB10-9000） | https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 已查核 | 2026-09-03 |
| GIGABYTE AI TOP ATOM 官方页（简中镜像站） | 产品特色与规格 | https://www.gigabyte.cn/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 已查核 | 2026-09-03 |
| GIGABYTE AI TOP ATOM Review（LinuxGizmos） | 第三方评测与规格确认（50.5mm） | https://linuxgizmos.com/gigabyte-ai-top-atom-introduces-nvidia-grace-blackwell-gb10-performance-for-the-desktop/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX Spark 官方页面 | GB10 平台信息 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA 9 款网卡 ARM64 实测总表（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 实机测试 | https://yupitek.com/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 实测 | 2026-11-18 |
| ALFA Network 产品总览（Yopitek） | ALFA 现役产品规格 | /zh-cn/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 NVIDIA DGX Spark](/zh-cn/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无线网卡是否支持 ASUS Ascent GX10](/zh-cn/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 无线网卡是否支持 ALTOS BrainSphere GB10 F1](/zh-cn/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 无线网卡是否支持 MSI EdgeXpert](/zh-cn/blog/alfa-msi-edgexpert-compatibility/)

免责声明：本文兼容性判定以 2026-11 在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）的实机测试为基准。GIGABYTE AI TOP ATOM 与 GX10 使用同一款 GB10 与 NVIDIA kernel 系列，预期行为相同，但未逐台测试。GX10 实测的 kernel 6.17 已内置 ALFA 9 款网卡的驱动（各卡最低版本不同），kernel 低于该卡最低版本时才需社区 DKMS 驱动。AI TOP ATOM 已内置 Wi-Fi 7，外置 ALFA 主要用于渗透测试或特殊芯片组需求。监听与注入仅限在自有或已取得授权的网络进行。
