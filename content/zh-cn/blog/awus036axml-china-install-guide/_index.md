---
title: "ALFA AWUS036AXML 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "驱动", "中国", "wifi6e", "vif"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中国境内安装 ALFA WiFi 6E 旗舰网卡 AWUS036AXML。涵盖内置驱动确认、固件安装以及监听模式开启，全程使用国内镜像源。"
related_product: "/zh-cn/products/alfa/awus036axml/"
series_order: 7
featureimage: "/images/blog/awus036axml-china-install-guide.webp"
faq:
  - question: "AWUS036AXML 用什么芯片？跟 AWUS036AXM 一样吗？"
    answer: "同样采用 MediaTek MT7921AUN 芯片，但 AWUS036AXML 是 USB-C 接口的旗舰版。"
  - question: "AWUS036AXML 的驱动需要手动安装吗？"
    answer: "不需要，mt7921u 驱动自 Linux 核心 5.18 起已内置，仅需安装固件软件包。"
  - question: "AWUS036AXML 支持 VIF 虚拟接口吗？"
    answer: "支持，MT7921AUN 完整支持核心原生 VIF，可同时执行监控接口和受管接口。"
  - question: "Ubuntu 22.04 安装 AWUS036AXML 为什么驱动加载失败？"
    answer: "Ubuntu 22.04 默认核心 5.15 太旧，需安装 HWE 核心升级至 5.18 以上。"
  - question: "AWUS036AXML 的 USB ID 是多少？"
    answer: "MediaTek MT7921AUN 的 USB ID 为 0e8d:7961，用 lsusb 可确认。"
---




AWUS036AXML 是 ALFA 的 WiFi 6E 旗舰型号。它最厉害的地方在于支持 6GHz 频段，而且采用了 MediaTek MT7921AUN 芯片，驱动已经内置在 Linux 内核（5.18+）里了。这意味着在现代系统中，你基本不需要手动编译驱动，只需要装好固件包就行。本指南会带你快速搞定这一切。

{{< tldr >}}
AWUS036AXML 采用 MT7921AUN 芯片，WiFi 6E 三频 USB-C 旗舰网卡，驱动核心内置，安装固件后即可使用监控模式、数据包注入与 VIF。
{{< /tldr >}}

1. **ALFA AWUS036AXML** 网卡和 USB-C 数据线
2. 一个带供电的 USB Hub —— 旗舰网卡功耗较高，树莓派用户必备
3. 稳定的网络连接（用于下载 20MB 左右的固件）



## 在你开始之前

1. **ALFA AWUS036AXML** 网卡和 USB-C 数据线
2. 一个带供电的 USB Hub —— 旗舰网卡功耗较高，树莓派用户必备
3. 稳定的网络连接（用于下载 20MB 左右的固件）

插上网卡，看看系统识别到没：

```bash
lsusb
```

找这一行：`ID 0e8d:7961 MediaTek Inc.`。看到它，我们就成功了一半。

---

## 快速安装流程

### 第一步：换到国内镜像源（避开 GitHub）

```bash
sudo nano /etc/apt/sources.list
```

建议使用中科大（USTC）源：
`deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

刷新列表：

```bash
sudo apt update
```

### 第二步：安装固件包

虽然驱动是内置的，但没有固件（firmware）网卡还是动不了。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

重启后，检查驱动是否正常工作：

```bash
lsmod | grep mt7921
iwconfig
```

只要看到 `wlan0` 或 `wlan1` 出现，就说明大功告成。

---

## 开启高级功能

### 1. 监听模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### 2. 虚拟接口 (VIF) 支持

AXML 完美支持 VIF，你可以一边连接 WiFi 上网，一边开个 mon0 接口抓包。

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

---

## 常见问题

| 现象 | 可能原因 | 解决办法 |
|---------|-------------|-----|
| `lsusb` 看不到设备 | 供电不足或线材问题 | 换个 USB 3.0 口，或换根短一点的线 |
| 搜不到 6GHz 信号 | 区域设置限制 | 运行 `sudo iw reg set US` 切换区域 |


{{< faq >}}

## 更多旗舰指南

- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — L型便携款
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — 经典免驱款

有问题？欢迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。

## 参考文献

1. [Linux Kernel mt7921 驱动](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng 官方文档](https://www.aircrack-ng.org/)
3. [ALFA Network 官网](https://www.alfa.com.tw/)
4. [Kali Linux 官方文档](https://www.kali.org/docs/)
