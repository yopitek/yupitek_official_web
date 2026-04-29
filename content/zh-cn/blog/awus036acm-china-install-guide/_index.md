---
title: "ALFA AWUS036ACM 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "驱动", "中国", "vif", "免驱"]
categories: ["驱动指南"]
series: ["Alfa 中国安装指南"]
description: "手把手教你在中国境内安装 ALFA AWUS036ACM。这是 Linux 系统下最省心的网卡，内置 MT7612U 驱动，完美支持监听模式和虚拟接口（VIF）。"
related_product: "/zh-cn/products/alfa/awus036acm/"
---

如果你正在寻找一款在 Linux 下真正“免驱”且强大的网卡，ALFA AWUS036ACM 就是你的终极选择。它采用的 MediaTek MT7612U 芯片驱动已经内置在 Linux 内核里了。这意味着你不需要去 GitHub 下载乱七八糟的补丁，插上就能用。本指南将带你确认驱动状态，并开启它的高级功能。

## 为什么选 AWUS036ACM？

- **真正免驱**：驱动内置在内核 4.19+ 中。
- **最佳虚拟接口支持 (VIF)**：它是极少数能同时开启“连接 WiFi”和“监听模式”的网卡。
- **极其稳定**：不会因为内核更新而导致驱动失效。

## 在你开始之前

1. **ALFA AWUS036ACM** 网卡
2. USB 3.0 数据线
3. 稳定的网络连接（用于下载固件包）

插上设备，运行命令确认：

```bash
lsusb
```

看到 `ID 0e8d:7612 MediaTek Inc.` 就说明识别成功了。

---

## 驱动与固件安装

虽然驱动是内置的，但你可能需要安装 MediaTek 的固件包（firmware）。

### 第一步：换到国内镜像源（加速下载）

```bash
sudo nano /etc/apt/sources.list
```

把源换成中科大（USTC）或清华（Tsinghua）镜像，然后刷新：

```bash
sudo apt update
```

### 第二步：安装固件

```bash
sudo apt install -y linux-firmware
sudo reboot
```

重启后，驱动就会自动加载。检查一下：

```bash
lsmod | grep mt76x2u
```

只要看到输出，就说明你已经准备好起飞了。

---

## 开启高级功能

### 1. 监听模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### 2. 同时使用监听和上网 (VIF)

这是 ACM 最酷的功能。你可以创建一个虚拟接口来监听，而不中断当前的 WiFi 连接。

```bash
# 创建监听接口 mon0
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

现在你可以用 `wlan0` 上网，同时用 `mon0` 抓包。

---

## 常见问题

| 现象 | 可能原因 | 解决办法 |
|---------|-------------|-----|
| 网卡灯不亮 | 供电不足 | 换到 USB 3.0 接口，或者使用带供电的 Hub |
| 无法开启监听 | 进程冲突 | 记得先运行 `airmon-ng check kill` |

## 更多 Alfa 中国指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — 高功率战神
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — WiFi 6E 新旗舰

有问题？欢迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
