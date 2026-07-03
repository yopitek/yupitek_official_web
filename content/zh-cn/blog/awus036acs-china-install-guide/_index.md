---



title: "ALFA AWUS036ACS 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036ACS 驱动。包含 RTL8811AU DKMS 驱动安装、监听模式和数据包注入教程。支持 Kali Linux, Ubuntu 22/24, Debian 和 树莓派。无需访问 GitHub。"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "驱动", "中国", "监听模式", "rtl8811au"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-cn/products/alfa/awus036acs/"
series_order: 3
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
faq:
  - question: "AWUS036ACS 用什么芯片？跟 AWUS036ACH 一样吗？"
    answer: "采用 Realtek RTL8811AU 芯片，与 RTL8812AU 共用同一个驱动程序软件包。"
  - question: "AWUS036ACS 支持监听模式吗？"
    answer: "支持，RTL8811AU 完美支持监听模式与数据包注入，是安全研究的经济实惠选择。"
  - question: "在中国安装 AWUS036ACS 需要翻墙吗？"
    answer: "不需要，Kali 用 apt 装 DKMS 驱动，Ubuntu/Debian 从 Gitee 下载源码编译即可。"
  - question: "AWUS036ACS 的 USB ID 是多少？"
    answer: "Realtek RTL8811AU 的 USB ID 为 0bda:0811，用 lsusb 可确认。"
  - question: "Kali Linux 安装 AWUS036ACS 驱动的指令是什么？"
    answer: "Kali 可直接执行 sudo apt install realtek-rtl88xxau-dkms 安装驱动。"
---




刚收到这款精巧的 AWUS036ACS，迫不及待插上电脑却发现 Linux 没反应？别急，这很正常。虽然它内置的 RTL8811AU 芯片是安全研究的神器，完美支持监听模式和数据包注入，但驱动并不在系统内核里，得咱们亲自动手装一下。

{{< tldr >}}
AWUS036ACS 采用 RTL8811AU 芯片，Kali 用 apt 装 DKMS 驱动，Ubuntu/Debian 从 Gitee 编译，支持监听模式与数据包注入。
{{< /tldr >}}


国内的小伙伴访问 GitHub 可能不太顺畅，所以我特意帮大家找好了 Gitee 镜像。不用翻墙，咱们现在就开始一步步把它“驯服”。

## 动手前的准备

在开始折腾之前，请确保你手边有这些东西：

1. **ALFA AWUS036ACS** 网卡本人
2. 包装盒里那根 USB 2.0 数据线
3. 畅通的网络（用来下载国内镜像源的包）

插上网卡，咱们先看看系统认出它没。打开终端输入：

```bash
lsusb
```

如果你在输出里扫到了这一行：

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

看到 `0bda:0811` 就稳了。接下来，根据你的系统选对应的教程就行。

## 你的系统是哪一个？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

如果是老手已经装好了驱动，可以直接跳到：

- [开启监听模式](#enable-monitor-mode)
- [测试数据包注入](#test-packet-injection)
- [虚拟机 USB 透传避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1. 先换个“快车道”（切换国内镜像）

为了下载不卡顿，咱们先给系统换上国内的镜像源。

```bash
sudo nano /etc/apt/sources.list
```

把里面的内容全删了，换成这个中科大的：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，**Enter** 确认，再按 **Ctrl+X** 退出。然后让系统刷新一下：

```bash
sudo apt update
```

> **小贴士：** 万一中科大源偶尔闹脾气，可以用清华源备用：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 2. 把编译工具装齐

这一步是给驱动搭建“手术台”。

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### 3. 从 Gitee 把驱动“搬”过来

GitHub 连不上？没关系，咱们用国内的 Gitee 镜像。

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **注意：** 如果这个链接失效了，直接在 Gitee 搜 `8821au`，找个最新的就行。

---

### 4. 正式安装并重启

```bash
sudo ./install-driver.sh
sudo reboot
```

重启回来，咱们检查下驱动有没有乖乖工作：

```bash
lsmod | grep 88XXau
```

看到 `88XXau` 就算成功了一大半。接着确认下网卡接口：

```bash
iwconfig
```

去找 `wlan0` 或 `wlan1`。

---

### 5. 开启监听模式 {#enable-monitor-mode}

这是最关键的一步，把网卡切换到“监听”状态。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

再用 `iwconfig` 瞧瞧，看到 `Mode:Monitor` 的 `wlan1mon` 接口了吗？那就是它！

---

### 6. 测试数据包注入 {#test-packet-injection}

光能听还不行，还得能发包。

```bash
sudo aireplay-ng --test wlan1mon
```

如果看到下面这两行，恭喜你，你的 ACS 已经完全起飞了：

```
Trying broadcast probe requests...
Injection is working!
```

---

## Ubuntu 22.04 / 24.04

### 1. 切换阿里云镜像

#### 如果是 Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

内容换成阿里云的：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### 如果是 Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

换成这个：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

别忘了跑一下：

```bash
sudo apt update
```

---

### 2. 安装依赖并部署驱动

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### 3. 验证功能

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### 1. 换成清华镜像

```bash
sudo nano /etc/apt/sources.list
```

粘贴这个（适用于 Debian 12）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

跑一下更新：`sudo apt update`。

### 2. 编译与安装

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

之后的操作和 Kali 是一样一样的。

---

## 树莓派 (Raspberry Pi) 4B / 5

### 1. 镜像选择

建议直接用 Kali ARM64。
国内镜像下载：[华为云 Kali 镜像](https://repo.huaweicloud.com/kali-images/)。

### 2. 系统升级与驱动安装

```bash
# 换源
sudo nano /etc/apt/sources.list
# 换成中科大：deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware

sudo apt update && sudo apt full-upgrade -y
sudo reboot

# 装依赖和驱动
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

## 虚拟机 USB 透传避坑指南 {#virtual-machine-usb-passthrough}

很多小伙伴卡在虚拟机里找不到网卡，其实就差这么几步：

### VirtualBox
1. 关掉虚拟机。
2. **设置 -> USB** -> 勾选 **USB 2.0 控制器**。
3. 点那个带 **+** 的小图标，选 **Realtek (ID: 0bda:0811)**。
4. 开机，进系统 `lsusb` 检查。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **Realtek 8811AU**，点 **连接**。

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|---------|-------------|-----|
| `lsusb` 刷不出 0bda:0811 | 没插紧或 USB 口供电不足 | 换个口，或者直接插主板背后的口 |
| `install-driver.sh` 报错 | 没装内核头文件 | 跑一下 `sudo apt install linux-headers-$(uname -r)` |
| `airmon-ng` 开启失败 | 被系统自带网络管理干扰了 | 必须先跑 `sudo airmon-ng check kill` |
| 注入测试是 "No Answer" | 离路由器太远了 | 凑近点试试。记得是用 `wlan1mon` 这个名字 |

> **特别提醒：** RTL8811AU 不支持 VIF。也就是说，它不能一边开着监听模式一边连 Wi-Fi 上网，它得专心干一件事。

## 国内常用资源汇总

| 资源名称 | 地址 | 用途 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 官方驱动包 |
| 8821au 驱动镜像 | [Gitee 镜像](https://gitee.com/mirrors/8821au) | 国内免翻墙克隆 |
| 中科大镜像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 首选 |
| 阿里云镜像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推荐 |


{{< faq >}}

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U, 支持 VIF
- AWUS036ACS ← 你在这里
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — MT7921AUN, L型接口
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

折腾过程中遇到搞不定的，欢迎在下面评论区留言，或者去 [yupitek.com](https://yupitek.com/zh-cn/contact/) 找我们。

## 参考文献

1. [aircrack-ng 官方文档](https://www.aircrack-ng.org/)
2. [ALFA Network 官网](https://www.alfa.com.tw/)
3. [Kali Linux 官方文档](https://www.kali.org/docs/)
4. [Gitee rtl8812au 镜像](https://gitee.com/mirrors/rtl8812au)
