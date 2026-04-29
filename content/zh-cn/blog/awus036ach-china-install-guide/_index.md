---
title: "ALFA AWUS036ACH 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "驱动", "中国", "监听模式"]
categories: ["驱动指南"]
series: ["Alfa 中国安装指南"]
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036ACH 驱动。涵盖 Kali Linux, Ubuntu 22/24, Debian 和 树莓派。无需访问 GitHub。"
related_product: "/zh-cn/products/alfa/awus036ach/"
---

你刚拿到 ALFA AWUS036ACH，结果 Linux 系统没反应？别担心，这很正常。这款网卡用的芯片需要 RTL8812AU 驱动，而且它不是插上就能用的。本指南会带你花大约 30 分钟完成安装，全程只用国内镜像源，完全不需要翻墙去 GitHub。

## 在你开始之前

请准备好以下物品：

1. **ALFA AWUS036ACH** 网卡
2. USB 数据线（包装盒里那根就挺好）
3. 一个带供电的 USB Hub —— 如果你用的是树莓派，这很重要
4. 稳定的网络连接

插上网卡，先确认系统有没有看到它：

```bash
lsusb
```

在输出里找这一行：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

只要看到 `0bda:8812`，就说明网卡被识别到了。接下来根据你的系统看下面的步骤。

## 选择你的操作系统

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

已经安装好了？直接跳到：

- [开启监听模式](#enable-monitor-mode)
- [测试数据包注入](#test-packet-injection)

---

## Kali Linux

Kali 自带了很多无线工具。装好 AWUS036ACH 驱动只需要四步。先换到国内镜像源，这样下载速度才够快。

### 第一步：切换到国内镜像源

打开终端，编辑源列表：

```bash
sudo nano /etc/apt/sources.list
```

删掉里面的内容，粘贴这一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，回车，再按 **Ctrl+X** 退出。刷新一下：

```bash
sudo apt update
```

> **小贴士：** 如果中科大（USTC）比较慢，可以试试清华源：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安装驱动

Kali 的软件库里已经有了预编译好的 DKMS 驱动。一行命令搞定：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS 的好处是，以后你更新内核时，驱动会自动重新编译，不用你再动手。

装完后确认驱动加载成功：

```bash
lsmod | grep 8812au
```

看到 `8812au` 就对了。

---

### 第三步：开启监听模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

用 `iwconfig` 确认一下，你应该能看到 `wlan1mon`，模式是 `Monitor`。

---

### 第四步：测试数据包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

看到 `Injection is working!` 说明你已经完全准备好了。

---

## Ubuntu 22.04 / 24.04

Ubuntu 不像 Kali 那样自带驱动，我们需要手动编译。

### 第一步：换到阿里云镜像

#### Ubuntu 24.04

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

把地址换成：`http://mirrors.aliyun.com/ubuntu/`

#### Ubuntu 22.04

```bash
sudo nano /etc/apt/sources.list
```

把所有的 `archive.ubuntu.com` 换成 `mirrors.aliyun.com`。

然后刷新：

```bash
sudo apt update
```

### 第二步：安装编译工具

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

### 第三步：从 Gitee 下载驱动

国内访问 GitHub 慢，我们用 Gitee 镜像：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
sudo ./install-driver.sh
sudo reboot
```

重启后，网卡应该就能正常工作了。

---

## 常见问题

| 现象 | 可能原因 | 解决办法 |
|---------|-------------|-----|
| `lsusb` 看不到设备 | 线没插好或供电不足 | 换个 USB 口或用带供电的 Hub |
| 安装驱动报错 | 缺内核头文件 | 运行 `sudo apt install linux-headers-$(uname -r)` |

## 国内镜像站参考

| 资源 | 地址 | 用途 |
|----------|-----|---------|
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 首选 |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 首选 |
| Gitee | [gitee.com](https://gitee.com) | 驱动源码 |

## 更多 Alfa 网卡中国指南

- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U，免驱首选
- [AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/) — RTL8811AU
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — WiFi 6E

有问题？欢迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
