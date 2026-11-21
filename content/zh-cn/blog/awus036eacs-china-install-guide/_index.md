---
title: "ALFA AWUS036EACS 中国安装指南：Windows 与 Linux 使用说明"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "驱动", "中国", "bluetooth", "rtl8821cu"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中国境内安装 ALFA AWUS036EACS。这款纳米网卡在 Windows 下表现极佳；在 Linux 内核 6.2+ 下已由内置的 rtw88_8821cu 驱动支持，免编译、插上即用，监听与注入实测可用。"
related_product: "/zh-cn/products/alfa/awus036eacs/"
series_order: 8
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
faq:
  - question: "AWUS036EACS 用什么芯片？支持蓝牙吗？"
    answer: "采用 Realtek RTL8821CU 芯片，支持 WiFi 5 与蓝牙 4.2。"
  - question: "AWUS036EACS 适合在 Linux 上使用吗？"
    answer: "适合。Linux 内核 6.2 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已内置 rtw88_8821cu 驱动，免编译、插上即用；实测 Monitor mode 与封包注入两频（2.4G / 5G）100%，并可端到端捕获 WPA .22000，蓝牙亦实测可用。"
  - question: "AWUS036EACS 在 Windows 上怎么安装驱动？"
    answer: "从 Alfa 官网 files.alfa.com.tw 下载 Windows 驱动包，以管理员身份安装后重启即可。"
  - question: "AWUS036EACS 的蓝牙怎么开启？"
    answer: "安装驱动后通常自动启用，在 Windows 设定中开启蓝牙开关即可连接设备。"
  - question: "如果需要 Linux 上的无线安全研究网卡，该选哪款？"
    answer: "AWUS036EACS 本身在内核 6.2+ 下即可用于监听与封包注入，还附带蓝牙。若想要更多选择，AWUS036ACM 或 AWUS036ACS 同样在 Linux 上完整支持监听模式。仅限自有或已授权的网络。"
---




AWUS036EACS 是 ALFA 家族中最迷你的成员之一，它不仅有 WiFi 5，还自带了蓝牙 4.2。它非常适合那些想给老笔记本升级，但又不想要个大天线在外面晃的人。它不仅在 Windows 上很好用，在 Linux 内核 6.2+ 上也已由内置的 rtw88_8821cu 驱动支持，免编译、插上即用。

{{< tldr >}}
AWUS036EACS 采用 RTL8821CU 芯片，WiFi 5 加蓝牙 4.2 迷你网卡，Windows 安装简单；Linux 内核 6.2+ 已内置 rtw88_8821cu 驱动，免编译，Monitor 与封包注入实测可用，蓝牙也实测可用。
{{< /tldr >}}

> **AWUS036EACS 在 Linux 内核 6.2+ 上即插即用。** 内核 6.2 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已内置 rtw88_8821cu 驱动，免编译；实测 Monitor mode 与封包注入两频（2.4G / 5G）100%，并可端到端捕获 WPA .22000；蓝牙（BT）也实测可用（BR/EDR + BLE 均可扫到设备，并与 WiFi 共存）。仅限自有或已授权的网络。
>
> **操作提醒：** 这是 BT+WiFi 复合卡，反复切换模式后 WiFi 接收可能卡住（`ip link set up` 回 `Operation already in progress`、`iw ... set channel` 回 `-16 busy`）。每个测试阶段开始前，把网卡拔下换一个 USB 接口重插即可恢复。
>
> 同系列其他 Linux 网卡：
> - **[AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/)** — MT7612U 内核内建，支持 VIF
> - **[AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/)** — RTL8811AU，监听模式



## Linux 用户看这里：内核 6.2+ 即插即用

> **AWUS036EACS 在 Linux 内核 6.2+ 上即插即用。** 内核 6.2 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已内置 rtw88_8821cu 驱动，免编译；实测 Monitor mode 与封包注入两频（2.4G / 5G）100%，并可端到端捕获 WPA .22000；蓝牙（BT）也实测可用（BR/EDR + BLE 均可扫到设备，并与 WiFi 共存）。仅限自有或已授权的网络。
>
> **操作提醒：** 这是 BT+WiFi 复合卡，反复切换模式后 WiFi 接收可能卡住（`ip link set up` 回 `Operation already in progress`、`iw ... set channel` 回 `-16 busy`）。每个测试阶段开始前，把网卡拔下换一个 USB 接口重插即可恢复。
>
> 同系列其他 Linux 网卡：
> - **[AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/)** — MT7612U 内核内建，支持 VIF
> - **[AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/)** — RTL8811AU，监听模式

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


{{< faq >}}

## 更多 Alfa 网卡指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — 经典大天线
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — WiFi 6 新款

有问题？欢迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。

## 参考文献

1. [ALFA Network 官网](https://www.alfa.com.tw/)
2. [Alfa 官方驱动下载](https://files.alfa.com.tw)
3. [Realtek 官方网站](https://www.realtek.com/)
