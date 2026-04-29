---
title: "ALFA AWUS036EACS 中国安装指南：Windows 与 Linux 使用说明"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "驱动", "中国", "bluetooth", "rtl8821cu"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中国境内安装 ALFA AWUS036EACS。这款纳米网卡在 Windows 下表现极佳，但在 Linux 下有一定局限性，请务必阅读本指南再开始。"
related_product: "/zh-cn/products/alfa/awus036eacs/"
series_order: 8
---

AWUS036EACS 是 ALFA 家族中最迷你的成员之一，它不仅有 WiFi 5，还自带了蓝牙 4.2。它非常适合那些想给老笔记本升级，但又不想要个大天线在外面晃的人。不过，买之前你要搞清楚一件事：它在 Windows 上很好用，但在 Linux（特别是 Kali）上并不推荐。

## Linux 用户请注意！

> **AWUS036EACS 在 Kali Linux、Ubuntu 或树莓派上工作并不稳定。** 它的芯片组 RTL8821CU 没有被良好维护的 Linux 驱动，开启监听模式（monitor mode）非常困难且容易报错。
>
> 如果你需要做无线安全研究，建议换成这两款：
> - **[AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/)** — 真正免驱，完美支持监听模式
> - **[AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/)** — 性价比最高的监听网卡

---

## Windows 10 / 11 安装步骤

在 Windows 下，这款网卡表现非常出色。

### 第一步：下载驱动

国内访问 Alfa 官网驱动库是没问题的：

[https://files.alfa.com.tw](https://files.alfa.com.tw)

进去后找 **AWUS036EACS** 文件夹，下载最新的 Windows 驱动包（一般是 `.zip` 或 `.exe`）。

### 第二步：安装

1. 解压下载的压缩包。
2. 右键点击安装程序，选择“以管理员身份运行”。
3. 一路点“下一步”，最后重启电脑。

### 第三步：确认状态

右键点击“此电脑” -> “管理” -> “设备管理器” -> “网络适配器”。

你应该能看到：`Realtek 8821CU Wireless LAN 802.11ac USB NIC`。看到它，就说明你可以正常上网了。

---

## 蓝牙如何开启？

装好驱动后，蓝牙通常会自动启用：

1. 打开 Windows 的“设置” -> “蓝牙和其他设备”。
2. 把蓝牙开关推到“开”。
3. 现在你可以连接蓝牙鼠标、耳机或键盘了。

---

## 常见问题

| 现象 | 可能原因 | 解决办法 |
|---------|-------------|-----|
| 网卡搜不到 5G 信号 | 频道不匹配 | 尝试在网卡属性里把区域设为美国（US） |
| 蓝牙连不上 | 驱动冲突 | 确认禁用电脑自带的板载蓝牙 |

## 更多 Alfa 网卡指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — 经典大天线
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — WiFi 6 新款

有问题？欢迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
