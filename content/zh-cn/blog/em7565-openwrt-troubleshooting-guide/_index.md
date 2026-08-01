---
title: "EM7565 在 OpenWrt／树莓派上识别不到？QMI／MBIM 排错完整指南"
description: "EM7565 在 OpenWrt 或树莓派上识别不到、QMI port 消失？这篇排错指南带你从 lsusb、dmesg 查到 USB composition，再到驱动加载与 EM7565 设置步骤，轻松排除硬件与软件连接问题。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-cn/products/sierra/em7565/"
faq:
  - question: "EM7565 在 OpenWrt 上识别不到，最常见的原因是什么？"
    answer: "最常见的是供电不足（VCC 不在 3.135 至 4.4V 内）导致 lsusb 看不到，或是 USB composition 设置错误没有打开 QMI 接口。"
  - question: "EM7565 反复重置、卡住不开机，是坏了吗？"
    answer: "不一定。它有 SED 保护机制，连续 6 次不正常重启后会进入保护状态，重新下载固件即可恢复。"
---

你的 EM7565 在 OpenWrt 或树莓派上死活识别不到吗？先别急着换模块。这篇文章帮你整理了官方规格书里的排错流程：从 USB 硬件层面确认有没有上线，检查 USB composition，加载正确的 Linux 驱动，排除系统服务干扰，以及处理棘手的固件 SED 状态。照着这五个步骤做，帮你快速找出问题症结！

{{< tldr >}}
EM7565 识别不到时照这五步查：1. 用 `lsusb` 确认 USB 层级（检查供电与转接板）。2. 确认 QMI/MBIM 接口与 `/dev/cdc-wdm0` 是否存在，检查 `qmi_wwan` / `cdc_mbim` 驱动与 USB composition。3. 停用 `ModemManager` 排除系统服务干扰。4. 确认供电时序（上电 100ms 内勿驱动信号，纹波上限 100mVp-p）。5. 确认固件状态：连续 6 次开机失败会进入 SED 保护，需重新下载固件。原则：先硬件、再软件、最后固件。
{{< /tldr >}}

**EM7565 是一颗基于 Qualcomm MDM9250 的 M.2 WWAN Type 3042-S3-B 4G LTE-Advanced 模块。它同时支持 QMI 与 MBIM 两种 USB 接口。** 如果它在 OpenWrt 或树莓派上「识别不到」，通常是三个地方出错：USB 没通电、USB composition 停在错误的组合，或是 Linux 驱动没正确加载。偶尔它还会因为连续重启进入保护模式。这篇文章我们照着 Sierra Wireless 的官方手册，帮大家整理出一套最不容易出错的排查流程。

> 产品链接：[Yupitek Sierra Wireless 专区](https://yupitek.com/zh-cn/products/sierra/)

## 快速结论：EM7565 识别不到时，照这五步查

大家在排错的时候最常犯的错就是：一上来就急着刷固件。**先确认硬件再动软件，最后才搞固件。**

1. **确认 USB 层级**：打个 `lsusb` 看看有没有模块。没有的话，先检查供电（VCC 要在 3.135 至 4.4V）、转接板和 USB 线。
2. **确认 QMI／MBIM 接口**：`lsusb` 看到了，却没有 `/dev/cdc-wdm0`？查一下 `qmi_wwan` / `cdc_mbim` 驱动有没有加载，以及 USB composition 是不是只开了纯诊断模式。
3. **确认系统服务**：有时候是系统的 `ModemManager` 把模块占用了。
4. **确认供电时序**：上电后至少 100ms 内不要驱动任何信号，而且电源纹波上限是 100mVp-p，电压不稳会让 USB 一直断线重连。
5. **确认固件状态**：如果模块连续 6 次开机失败重置，它会进入 SED（Smart Error Detection）保护状态，这时候就需要重新下载固件了。

## 认识 EM7565：它是一颗什么样的模块？

在开始排错前，我们先快速过一下 EM7565 的底细。这是一颗需要外接三支天线（Main、GNSS、Aux）的 M.2 模块，不含天线。

| 项目 | 官方规格（Doc# 41110788，Rev 8） |
|---|---|
| **芯片** | Qualcomm MDM9250 |
| **封装尺寸** | M.2 (3042-S3-B) / 42 × 30 mm，厚度最高 1.50mm，重量 6.5g |
| **下载峰值** | Cat 12 (3CA, 256QAM) 最高 600 Mbps |
| **上传峰值** | Cat 13 (2CA, 64QAM) 最高 150 Mbps |
| **LTE 频段** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66（注：B42/B43/B48 当时列为 disabled，待法规核准） |
| **通信接口** | USB 2.0 与 USB 3.0；QMI / MBIM / AT 命令 |
| **供电电压** | VCC 3.135V(min) / 3.3V(typ) / 4.4V(max)，纹波 ≤ 100mVp-p |
| **工作温度** | 建议内部温度保持在 <90°C（最好 <80°C） |

## 步骤一：从 USB 层级开始查

这台机器到底有没有「看见」这个硬件？

```bash
lsusb
```

如果出现 Sierra Wireless 或 1199 开头的设备，恭喜，硬件连上了。如果看不到：

- 请检查电源：EM7565 瞬时开机电流可以达到 2.2A 至 2.5A（最大电流 1.5A）。很多树莓派的 USB 转接盒根本推不动它。
- 给它一点时间：插上去之后等个 10 秒，让 USB 慢慢跑完流程。

接着看内核日志：

```bash
dmesg | tail -50
```

如果你看到 `qmi_wwan` 挂载出 `/dev/cdc-wdm0`，代表它已经准备好连接了。

## 步骤二：检查 USB composition

如果 `lsusb` 看得到模块，却没有 `/dev/cdc-wdm0` 跑出来，可能是模块把 QMI/MBIM 通道关起来了。模块里面有一个叫做 USB composition 的设置，决定它要露出哪些通道。

这时候你需要用 `AT!USBCOMP?` 命令去查。如果你随便乱切换，很可能会把通道全部搞丢，所以切换前请先记下原来的参数，并去查阅官方的 AT 命令手册（Doc#41111748）。

## 步骤三：排除 ModemManager 干扰

在桌面版 Linux 或树莓派上，有个叫 `ModemManager` 的内置服务会「多管闲事」地把 4G 模块抢走。当它抢走控制权后，你自己敲 `qmicli` 命令就会卡住。

手动排错的时候，先把这个家伙关掉：

```bash
sudo systemctl stop ModemManager
```

等你确定模块都没问题了，再来决定要手动拨号，还是把它交还给 ModemManager。

## 步骤四：固件是不是锁死了？（SED 保护机制）

如果你发现模块开机后无限重启，那它可能已经进入了 **SED（Smart Error Detection）** 状态。

官方规格书写得很清楚：只要开机不久后连续发生 6 次重置，模块就会停在 bootloader 里面装死，等你重新把固件刷进去。这通常是因为你的电源太不稳（电压狂掉）造成的。

这时候不要以为模块坏了，换个好一点的电源，然后用官方工具重刷固件就能救回来。

## QMI 怎么拨号上网？（OpenWrt 示例）

当你搞定上面那些问题，`/dev/cdc-wdm0` 出现后，在 OpenWrt 拨号其实超简单。

1. 装好必备软件包：

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. 到 `/etc/config/network` 设置你的 APN（以运营商为准）：

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. 重启网络：

```bash
/etc/init.d/network restart
```

这样 `wwan0` 接口就会出现，开开心心上网去了。

## 总结

EM7565 在 OpenWrt 或树莓派上识别不到，其实就跟修电脑一样，顺序对了就很快：

1. **看硬件**：`lsusb` 和电压稳不稳。
2. **看接口**：USB composition 对不对。
3. **看软件**：驱动有没有装，ModemManager 有没有冲突。
4. **看固件**：是不是重启太多次把自己锁起来了。

只要不一上来就乱刷固件，大部分问题都能在十分钟内找出原因！

## 采购信息（Call To Action）

不确定手上的转接板、天线能不能配 EM7565？Yupitek（榆閤科技）提供 Sierra Wireless 全系列产品和完善的硬件集成方案。

欢迎来信：**sales@yupitek.com**

看看产品：[EM7565 产品页面](https://yupitek.com/zh-cn/products/sierra/em7565/)
