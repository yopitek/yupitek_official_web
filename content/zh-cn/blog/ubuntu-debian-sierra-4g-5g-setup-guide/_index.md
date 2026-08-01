---
title: "Ubuntu / Debian / Linux Mint 安装 Sierra 4G/5G 模组完整教程：EM7455、EM7565、EM919x、MC7455 设置与 GNSS 定位"
description: "在 Ubuntu/Debian/Linux Mint 上怎么安装 Sierra 4G/5G 模组？这篇教程带你装好 ModemManager、使用 qmicli/mbimcli 拨号连接，并且设置 GNSS 定位。涵盖 EM7455、EM7565、EM919x、MC7455。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-cn/products/sierra/"
faq:
  - question: "Ubuntu 可以直接用 Sierra 4G/5G 模组上网吗？"
    answer: "可以。只要安装 modemmanager、libqmi-utils 等软件包，用 NetworkManager 填入 APN 就能上网。"
  - question: "Sierra 模组在 Linux 下怎么开启 GNSS 定位？"
    answer: "使用 ModemManager 命令：先用 mmcli -m 0 --location-enable-gps-raw，再用 --location-get 获取坐标。请确保 GNSS 天线已接好。"
---

想在 Ubuntu、Debian 或 Linux Mint 上安装 Sierra Wireless 的模组（EM7455、EM7565、MC7455、EM919x）吗？其实 Linux 原生就支持这些设备，只要你知道怎么安装对的软件包（像是 ModemManager 跟 libqmi-utils）。这篇文章从硬件怎么接、驱动怎么装、怎么拨号上网，一路讲到怎么把 GNSS 定位功能开起来。不管你是要做无人机还是工业电脑，照着做准没错。

{{< tldr >}}
想在 Ubuntu、Debian 或 Linux Mint 上安装 Sierra Wireless 的模组（EM7455、EM7565、MC7455、EM919x）吗？其实 Linux 原生就支持这些设备，只要安装对的软件包（ModemManager 跟 libqmi-utils）。从硬件怎么接、驱动怎么装、怎么拨号上网，一路讲到怎么把 GNSS 定位功能开起来。不管你是要做无人机还是工业电脑，照着做准没错。
{{< /tldr >}}

**一句话总结：在 Linux 装这些 Sierra 模组超简单。只要用 `apt` 装好 `modemmanager` 跟相关工具，就能用 NetworkManager 连上网络，甚至连 GPS 定位都能轻松读出来！**

很多人拿到 EM7455、EM7565、EM919x 或 MC7455，插上主板后却不知道怎么设置上网。其实，这些模组在 Linux 里的支持度非常成熟。它们都是通过 USB，用 QMI 或是 MBIM 协议在通信。接下来我们就一步步带你把它们设置好。

> 规格数字与技术依据皆来自 Sierra Wireless 官方规格书。本文由榆閤科技（Yupitek）整理。

---

## 动手前：先看懂你手上的硬件

硬件没搞对，软件再怎么敲命令都没用。

| 模组 | 封装插槽 | 速度等级 | Linux 主流通信协议 | 天线数量 |
|---|---|---|---|---|
| **EM7455** | M.2 (长 42mm) | Cat 6 (300/50 Mbps) | QMI | 3 个 (Main, GNSS, Aux) |
| **EM7565** | M.2 (长 42mm) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 个 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (长 **52mm**) | 5G NR / LTE Cat 20 | MBPW 等宽带套件 | 4 个以上 |
| **MC7455** | mPCIe (旧型插槽) | Cat 6 (300/50 Mbps) | QMI | 3 个 U.FL 接头 |

**两个硬件防呆重点：**
1. **EM919x 比较长**：它是 52mm 长，不要硬塞进 42mm 的孔位里，会弄坏板子。
2. **没有天线 = 没信号**：至少要把主天线（Main）接上。如果要玩定位，一定要买一根 GPS 天线接在 **GNSS 接头** 上。

---

## 步骤一：安装 Linux 必备工具

在 Ubuntu / Debian / Linux Mint 里面，你不用自己写码编译驱动，软件源都帮你准备好了。

打开终端，敲这两行：
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
装完之后，确认服务有跑起来：
```bash
systemctl status ModemManager
```
有了这几个工具，你的 Linux 就能看得懂这张 4G/5G 网卡了。

---

## 步骤二：确认系统有抓到网卡

把网卡插好、开机后，用下面三个命令检查：

1. **查 USB 硬件：**
   ```bash
   lsusb
   ```
   （应该要看到 Sierra 或 Qualcomm 相关的设备）

2. **查内核驱动：**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   （看到 `cdc-wdm0` 跟 `wwan0` 就是成功挂载了）

3. **查 ModemManager 状态：**
   ```bash
   mmcli -L
   ```
   （会列出一串调制解调器的名字跟编号，记下这个编号，通常是 `0`）

---

## 步骤三：超简单的拨号连接（用 NetworkManager）

如果你用的是桌面版的 Ubuntu 或 Mint，用系统自带的网络管理工具最方便。

```bash
# 新增一个连接（把 "internet" 换成你运营商的 APN）
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# 启动它！
nmcli connection up mobile
```
就这么简单！你可以用 `ip addr show` 看看 `wwan0` 有没有拿到 IP。

### （进阶）没有桌面环境的纯文字连接法
如果是无头服务器（headless server）或嵌入式板子，你可以直接用 `qmicli` 下命令：
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## 步骤四：把 GPS 定位功能开起来！

这几颗模组都有内置强大的 GNSS 定位系统（支持 GPS、GLONASS 等）。
根据官方规格：
- EM7455 / EM7565 / MC7455：热启动 1秒、冷启动 32秒。水平精度大约在 2~5 米内。
- 5G 的 EM919x：冷启动更快（≤28秒），精度也略有提升（<4m 95%）。

**要在 Linux 抓坐标，这样做最快：**

1. 启用 GPS 功能：
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. 获取当前坐标：
```bash
mmcli -m 0 --location-get
```
画面就会喷出当前的经纬度啦！如果要实时串流给其他程序用，可以搭配 `gpsd` 一起使用。

---

## 常见的踩坑与急救

1. **`mmcli -L` 什么都不显示**：可能是 `ModemManager` 挂了，或者你的 USB 供电根本推不动网卡。
2. **GPS 定位一直失败**：你是不是把 GPS 天线插到 Main 或 Aux 上了？GNSS 有自己专属的孔！
3. **EM919x 速度上不去**：它是 5G 网卡，支持 USB 3.1 Gen 2 甚至 PCIe Gen 3。如果你把它插在 USB 2.0 的孔，官方是不保证性能的。

## 结论

在 Linux 上玩 Sierra 模组，其实没有想象中难。确认好硬件插槽跟天线，装上 `modemmanager` 家族的软件包，再设置一下 APN 就能愉快上网了。这套流程非常适合要做边缘计算（Edge Computing）或是工业物联网（IIoT）的工程师们！

## 采购信息（Call To Action）

想要把 Sierra 模组整合进你的 Ubuntu 设备里吗？Yupitek（榆閤科技）提供完整的模组、天线、转接板方案，并且能提供你第一线的技术支持。
欢迎来信：**sales@yupitek.com**
看看产品：[Sierra Wireless 系列](https://yupitek.com/zh-cn/products/sierra/)

{{< faq >}}
