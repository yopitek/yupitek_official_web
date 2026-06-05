---
title: "完整教程：在中国大陆 Linux 系统安装所有 Alfa USB WiFi 网卡 — Kali、Ubuntu、Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "驱动程序", "中国", "监控模式", "封包注入", "无线网络"]
categories: ["驱动程序安装教程"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "终极 Alfa USB WiFi 网卡 Linux 安装指南，适用于中国大陆用户。涵盖 Kali Linux、Ubuntu 22/24、Debian、Raspberry Pi，全程使用境内镜像，无需访问 GitHub。"
featureimage: "/images/blog/alfa-china-install-complete-guide.webp"
---

## 欢迎阅读 Alfa Linux 终极安装指南

如果您正在阅读本文，您可能购买了 Alfa USB WiFi 网卡后遇到了以下问题：

- 您在中国大陆，无法访问 GitHub
- 驱动程序安装步骤复杂难懂
- 您需要启用监控模式（Monitor Mode）和封包注入（Packet Injection）进行无线测试
- 不确定您的 Alfa 型号需要哪个驱动程序

本指南解决**所有上述问题**。我们将带您在**所有主要 Linux 发行版**上安装**每一款 Alfa USB WiFi 网卡**，全程仅使用**中国大陆可访问的镜像**。无需 GitHub，告别挫败感。

---

## 为什么需要这份指南

Alfa USB WiFi 网卡深受渗透测试员、网络工程师和无线爱好者的欢迎，因为它们支持监控模式和封包注入——这些功能是大多数消费级 WiFi 网卡所没有的。

但问题在于：**大多数驱动程序安装教程都假设您能访问 GitHub**。在中国大陆这是不可能的。本指南专为中国大陆用户设计，全程仅使用境内可访问的镜像和资源。

---

## 快速型号对照表

开始之前，先确认您使用的 Alfa 网卡型号及其芯片组：

### AX 系列（Wi-Fi 6 / 802.11ax）

| 型号 | 芯片组 | 驱动程序 | 最适合 |
|------|--------|---------|--------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | 通用，覆盖范围好 |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | 紧凑设计 |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | 超紧凑 |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | 增强功率 |

### AC 系列（Wi-Fi 5 / 802.11ac）

| 型号 | 芯片组 | 驱动程序 | 最适合 |
|------|--------|---------|--------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | 高功率，覆盖范围极佳 |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **最佳 VIF 支持**，即插即用 |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | 经济实惠 |

### 如何确认您的型号？

1. 查看网卡上的标签
2. 查看原包装盒
3. 若是网购，查看订单记录

确认型号后，直接跳至对应章节，或依照通用流程操作。

---

## 开始前的准备

请确保以下物品就绪：

1. **Alfa USB WiFi 网卡** — 适合您需求的型号
2. **USB 连接线** — 原厂附送的即可
3. **有源 USB Hub** — 若使用 Raspberry Pi 则必备
4. **可用的网络连接** — 用于连接中国大陆境内镜像
5. **sudo 权限** — 安装驱动程序需要管理员权限

先插入网卡，确认系统能检测到：

```bash
lsusb
```

在输出中寻找网卡的厂商 ID：

- **Alfa 网卡**显示为 `0e8d`（MediaTek）或 `0bda`（Realtek）
- 示例：`Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- 示例：`Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

若看到 ID，代表网卡已被检测到，请继续前往驱动程序安装章节。

若未看到，请换一个 USB 口，更换连接线，再次执行 `lsusb`。

---

## 选择您的操作系统

直接跳至对应章节：

- [Kali Linux](#kali-linux-安装)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-安装)
- [Debian 12 (Bookworm)](#debian-12-bookworm-安装)
- [Raspberry Pi OS（64 位）](#raspberry-pi-os-安装)

已安装驱动程序？直接跳至高级章节：

- [启用监控模式](#在任何网卡上启用监控模式)
- [测试封包注入](#测试封包注入)
- [虚拟接口（VIF）支持](#虚拟接口-vif-支持)
- [虚拟机 USB 直通](#虚拟机-usb-直通)

---

## 中国大陆可用镜像参考

本指南所有步骤仅使用以下中国大陆可访问的镜像：

| 资源 | URL | 用途 |
|------|-----|------|
| **Alfa 官方下载** | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动程序包、固件 |
| **Alfa 文档** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 产品手册（英文）|
| **清华大学镜像** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里云镜像** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推荐）|
| **中科大镜像** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推荐）|
| **华为云镜像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 镜像（备用）|
| **Gitee（GitHub 替代）** | [gitee.com](https://gitee.com) | 驱动程序源代码 |

---

## Kali Linux 安装

Kali Linux 已预装无线工具，让 Alfa 网卡正常工作只需几个步骤。

### 第一步：切换至中国大陆镜像

打开软件源列表：

```bash
sudo nano /etc/apt/sources.list
```

将所有内容替换为：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：**Ctrl+O**，Enter，再 **Ctrl+X**。更新：

```bash
sudo apt update
```

> **备用镜像：** 若中科大（USTC）速度慢，改用清华（Tsinghua）：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### 第二步：按芯片组安装驱动程序

#### AX 系列（RTL8832BU）

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC 系列 - Realtek（RTL8812AU / RTL8811AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 系列 - MediaTek（MT7612U）

MT7612U 驱动程序已内置于 Kali 内核，确认是否已加载：

```bash
lsmod | grep mt76
```

若看到 `mt76x2u`，已完成。若未出现：

```bash
sudo modprobe mt76x2u
```

### 第三步：确认驱动程序已加载

再次执行 `lsusb`，网卡应会显示。然后检查无线接口：

```bash
iwconfig
```

寻找 `wlan0` 或 `wlan1`。若接口出现，代表驱动程序正常工作。

### 第四步：启用监控模式

停止干扰进程：

```bash
sudo airmon-ng check kill
```

启动监控模式：

```bash
sudo airmon-ng start wlan0
```

验证：

```bash
iwconfig
```

寻找显示 `Mode:Monitor` 的 `wlan0mon`，完成！

---

## Ubuntu 22.04 / 24.04 安装

### 第一步：切换至中国大陆镜像

#### Ubuntu 24.04（Noble）

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

替换为：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

**Ctrl+O** 保存，**Ctrl+X** 退出。

#### Ubuntu 22.04（Jammy）

```bash
sudo nano /etc/apt/sources.list
```

替换为：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存并退出。

#### 更新包索引

```bash
sudo apt update
```

### 第二步：安装编译依赖

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 第三步：安装驱动程序

#### AX 系列（RTL8832BU）

从 Gitee 克隆：

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC 系列 - Realtek（RTL8812AU）

从 Gitee 克隆：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC 系列 - MediaTek（MT7612U）

驱动程序已内置于 Ubuntu 内核，直接加载：

```bash
sudo modprobe mt76x2u
```

### 第四步：启用监控模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

寻找显示 `Mode:Monitor` 的 `wlan0mon`。

---

## Debian 12 (Bookworm) 安装

### 第一步：切换至中国大陆镜像

```bash
sudo nano /etc/apt/sources.list
```

替换为：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

保存并退出，更新：

```bash
sudo apt update
```

### 第二步：安装非自由固件

```bash
sudo apt install -y firmware-misc-nonfree
```

### 第三步：安装编译依赖

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 第四步：安装驱动程序

#### AX 系列（RTL8832BU）

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC 系列 - Realtek（RTL8812AU）

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC 系列 - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### 第五步：安装 Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### 第六步：启用监控模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

寻找显示 `Mode:Monitor` 的 `wlan0mon`。

---

## Raspberry Pi OS 安装

> **重要提示：** AWUS036ACH 消耗约 500mW，AWUS036ACM 消耗约 400mW。**务必使用有源 USB Hub** 以防止 Pi 在负载下降频或崩溃。

### 第一步：下载 Kali Linux ARM64 镜像

前往：https://www.kali.org/get-kali/#kali-arm

选择 **Raspberry Pi 4（64 位）** 或 **Raspberry Pi 5（64 位）**。请勿使用 32 位版本。

> **中国大陆镜像：** 若 kali.org 速度慢，使用华为云：https://repo.huaweicloud.com/kali-images/

### 第二步：烧录至 MicroSD

确认 SD 卡的设备路径：

```bash
lsblk
```

烧录镜像（将 `/dev/sdX` 替换为您的实际路径）：

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

等待 `sync` 完成。启动 Pi，默认账号密码：**kali / kali**。

### 第三步：切换至中国大陆镜像

```bash
sudo nano /etc/apt/sources.list
```

替换为：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存并应用：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 第四步：安装驱动程序

#### AX 系列（RTL8832BU）

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC 系列 - Realtek（RTL8812AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 系列 - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### 第五步：启用监控模式

Pi 有内置 Wi-Fi，Alfa 网卡通常显示为 `wlan1`：

```bash
iwconfig
```

然后：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

寻找显示 `Mode:Monitor` 的 `wlan1mon`。

---

## 在任何网卡上启用监控模式

驱动程序安装完成后，启用监控模式非常简单：

### 第一步：确认接口名称

```bash
iwconfig
```

记下是 `wlan0` 还是 `wlan1`。

### 第二步：停止干扰进程

```bash
sudo airmon-ng check kill
```

### 第三步：启动监控模式

```bash
sudo airmon-ng start wlan0
```

若接口名称不同，请替换 `wlan0`。

### 第四步：验证

```bash
iwconfig
```

寻找接口名称末尾加上 `mon`（如 `wlan0mon`）且显示 `Mode:Monitor`。

---

## 测试封包注入

确认网卡可以发送自定义封包——无线测试的必备功能。

```bash
sudo aireplay-ng --test wlan0mon
```

**成功的输出如下：**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**若失败：**
- 重新启动后再试
- 确认没有其他进程占用接口（`iwconfig`）
- 靠近 WiFi AP 进行测试
- 确认使用的是 `wlan0mon` 而非 `wlan0`

---

## 虚拟接口（VIF）支持

VIF（虚拟接口功能）允许在单一网卡上同时运行多个接口，例如：

- 同时运行**托管模式**（`wlan0`）和**监控模式**（`mon0`）
- 在保持网络连接的同时捕获流量

### 哪些网卡支持 VIF？

| 芯片组 | VIF 支持 | 备注 |
|--------|---------|------|
| **MT7612U（AWUS036ACM）** | ✅ 完整原生支持 | VIF 工作流程的最佳选择 |
| **RTL8812AU（AWUS036ACH）** | ⚠️ 有限 | 无法同时运行托管模式和监控模式 |
| **RTL8832BU（AX 系列）** | ⚠️ 有限 | 请查阅特定型号文档 |

### 创建虚拟接口（MT7612U）

若您使用 AWUS036ACM（MT7612U）：

```bash
# 在 wlan0 保持托管模式的同时创建监控接口
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

确认两个接口均已启用：

```bash
iwconfig
```

您应看到：
- `wlan0` — 托管模式（已连接至 AP）
- `mon0` — 监控模式（捕获所有流量）

### 使用场景

**保持连接的同时捕获流量：**

```bash
sudo airodump-ng mon0
```

`wlan0` 继续正常运作，`mon0` 同时捕获所有流量。

**伪造 AP + 监控：**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 虚拟机 USB 直通

在虚拟机中运行 Linux？您需要将 USB 网卡直通到虚拟机内部。

### VirtualBox

1. 关闭虚拟机
2. 进入 **设置 → USB**
3. 启用 **USB 3.0（xHCI）控制器**
4. 点击 **+** 添加 USB 筛选器
5. 选择您的 Alfa 网卡（ID：`0bda:8812` 或 `0e8d:7612`）
6. 启动虚拟机

在虚拟机内执行 `lsusb` 确认，然后按照 Kali Linux 步骤操作。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. 启动虚拟机
2. 菜单：**虚拟机 → USB 与蓝牙**
3. 找到您的 Alfa 网卡并点击 **连接**
4. 网卡出现在虚拟机内

执行 `lsusb` 确认，然后按照驱动程序安装步骤操作。

---

## 故障排除

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| `lsusb` 没有显示网卡 ID | 连接线故障或供电不足 | 换 USB 口。Pi 请用有源 Hub |
| `modprobe` 说"Module not found" | 缺少内核模块 | 执行 `sudo apt install linux-modules-extra-$(uname -r)` |
| 驱动程序正常但无法切换监控模式 | NetworkManager 干扰 | 先执行 `sudo airmon-ng check kill` |
| 监控模式已启动但没有捕获到任何东西 | 接口名称或信道错误 | 执行 `iwconfig`，设置信道：`iwconfig wlan0mon channel 6` |
| 注入测试失败 | 使用了错误的接口 | 使用 `wlan0mon` 而非 `wlan0` |
| VIF 创建失败 | 驱动程序未完全加载 | 拔插网卡，或重新加载模块 |

---

## 附录：完整 Alfa 型号列表

| 型号 | 芯片组 | 驱动程序 | 中国大陆镜像来源 |
|------|--------|---------|----------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | 内核内置驱动程序 |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## 结语

本指南涵盖了在**所有主要 Linux 发行版**上安装**所有 Alfa USB WiFi 网卡**的方法，全程使用**中国大陆可访问的资源**。完成后您应能：

✅ 为任何 Alfa 网卡安装驱动程序  
✅ 在 Kali、Ubuntu、Debian 或 Raspberry Pi 上启用监控模式  
✅ 测试封包注入  
✅ 使用支持型号的虚拟接口（VIF）  
✅ 将网卡直通至虚拟机  

**有疑问或问题？** 请查阅本系列中特定型号的教程，或通过 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。

---

## 相关教程

本文是 **Alfa 中国大陆安装指南**系列的一部分：

- [AWUS036ACH 安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU，高功率
- [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U，最佳 VIF 支持
- [AWUS036ACS 安装指南](/zh-cn/blog/awus036acs-china-install-guide/) — RTL8811AU，经济实惠
- [AWUS036AX 安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — Wi-Fi 6，RTL8832BU
- [AWUS036AXM 安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — Wi-Fi 6，紧凑设计
- [AWUS036AXML 安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — Wi-Fi 6，超紧凑
- [AWUS036AXER 安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — Wi-Fi 6，增强功率
- [AWUS036EAC 安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8814AU，高功率

---

*最后更新：2026 年 4 月 24 日*
