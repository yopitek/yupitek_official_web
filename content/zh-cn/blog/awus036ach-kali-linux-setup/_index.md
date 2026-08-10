---
title: "ALFA AWUS036ACH Kali Linux 配置指南：监听模式与数据包注入（2026）"
description: "手把手教你在 Kali Linux 2024/2025 安装 ALFA AWUS036ACH，启用 airmon-ng 监听模式，验证数据包注入——附完整驱动安装命令。"
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "监听模式", "数据包注入", "RTL8812AU", "airmon-ng"]
featureimage: "/images/blog/awus036ach-kali-linux-setup.webp"
faq:
  - question: "AWUS036ACH 在 Kali Linux 上需要额外安装驱动吗？"
    answer: "需要。RTL8812AU 并非主线内核驱动，需从 aircrack-ng GitHub 仓库安装，建议使用 DKMS 确保内核更新后仍可运行。"
  - question: "如何确认 AWUS036ACH 已被系统检测到？"
    answer: "执行 lsusb 指令，寻找 ID 0bda:8812 即可确认 Realtek RTL8812AU 已被识别，再以 lsmod 确认驱动模块已加载。"
  - question: "启用监听模式后接口消失怎么办？"
    answer: "通常是 NetworkManager 重新接管接口所致。执行 airmon-ng check kill 终止干扰进程，再重新启用监听模式即可。"
  - question: "数据包注入测试成功率多少才算正常？"
    answer: "成功率 80% 以上代表运行可靠。低于 50% 则需检查天线位置、USB 供电是否充足，或驱动程序是否正确安装。"
  - question: "内核更新后 AWUS036ACH 驱动失效如何处理？"
    answer: "若使用 DKMS 安装，驱动会自动重建。若失效，执行 dkms autoinstall 并确认 linux-headers 软件包与当前内核版本一致。"
---




ALFA AWUS036ACH 在 Kali Linux 社区中赢得最高推荐，这并非没有原因。凭借 Realtek RTL8812AU 芯片组，它提供了自 2017 年以来安全专业人员所依赖的稳定监听模式和数据包注入能力。本指南将带你完成从开箱到在 Kali Linux 2024/2025 上验证数据包注入正常工作的每一步操作。

{{< tldr >}}
AWUS036ACH 搭载 RTL8812AU 芯片，通过 aircrack-ng 驱动搭配 DKMS 安装，可稳定启用监听模式与数据包注入，是 Kali Linux 渗透测试的标准配置。
{{< /tldr >}}


---

## 为什么 AWUS036ACH 是首选

在正式执行命令之前，有必要先了解这款网卡的独特之处。

**RTL8812AU 芯片组**

Realtek RTL8812AU 是一款双频（2.4 + 5 GHz）802.11ac 芯片组，对安全工具所需的帧级操作有着出色的支持。GitHub 上由 `aircrack-ng/rtl8812au` 维护的开源驱动程序，是 Aircrack-ng 团队与 Linux 安全社区多年协作的成果。它持续维护、定期针对新内核版本测试，并且对监听模式和数据包注入的支持是内置的——并非事后补丁。

**自 2017 年积累的社区沉淀**

遇到 AWUS036ACH 的问题时，你总能找到答案。这款网卡出现在数以千计的论坛帖子、YouTube 教程、Hack The Box 解题报告、Offensive Security 课程材料和 GitHub issue 中，其故障排除知识库无出其右。

**AC1200 双频性能**

网卡在 2.4 GHz 最高可达 300 Mbps，5 GHz 最高 867 Mbps，配备两根可拆卸的 RP-SMA 天线支持 2×2 MIMO，在保障完整渗透测试能力的同时提供真实的高吞吐量性能。

**USB 3.0**

USB 3.0 接口确保高带宽抓包或同时运行多个工具时不会出现瓶颈。

你可以在我们的商城找到它：[ALFA AWUS036ACH](/zh-cn/products/alfa/awus036ach/)。

---

## 前置条件

开始前，请确认以下几点：

- **Kali Linux 2024.x 或更新版本**（本指南在 Kali 2024.1 至 2025.1 上测试通过）
- **USB 3.0 端口** — 网卡兼容 USB 2.0，但吞吐量受限，建议使用 USB 3.0 以获得最佳效果
- **网络连接**，用于下载驱动程序
- **root 或 sudo 权限**
- **编译工具已安装** — 第 2 步中会涵盖

如果你在虚拟机中运行 Kali（VMware、VirtualBox、UTM），必须将 USB 设备直通给虚拟机。VMware 中：虚拟机 → 可移动设备 → 连接你的网卡；VirtualBox 中：设置 → USB → 为 Realtek 设备添加 USB 筛选器。

---

## 第 1 步：连接网卡并验证识别

将 AWUS036ACH 插入 USB 端口，运行：

```bash
lsusb
```

你应该看到类似以下的条目：

```
Bus 001 Device 004: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

关键标识符：
- **厂商 ID：** `0bda`（Realtek）
- **产品 ID：** `8812`（RTL8812AU）

如果设备完全不显示，请尝试换一个 USB 端口或数据线。如果显示了不同的产品 ID，可能是不同的硬件版本。

插入后立即检查内核消息日志：

```bash
dmesg | tail -20
```

如果驱动程序已经加载（全新安装的 Kali 上不太可能），你会看到类似这样的行：

```
usb 1-1: new high-speed USB device number 4 using xhci_hcd
usbcore: registered new interface driver rtl88XXau
```

在未安装驱动程序的情况下，你会看到 USB 设备被检测到，但没有创建无线接口。

---

## 第 2 步：安装 RTL8812AU 驱动程序

有两种安装方式。**方法 A（aircrack-ng 驱动）** 推荐用于 Kali Linux；**方法 B（DKMS）** 推荐在希望驱动程序在内核更新后自动持久化的情况下使用。

### 安装编译依赖

两种方法都需要相同的依赖：

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

这会安装与当前运行内核匹配的内核头文件，驱动程序编译过程必须依赖它。

### 方法 A：直接安装（aircrack-ng 驱动 — Kali 推荐）

```bash
# 克隆 aircrack-ng 维护的驱动
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# 编译驱动
make

# 安装驱动
sudo make install

# 加载驱动模块
sudo modprobe 88XXau
```

验证模块已加载：

```bash
lsmod | grep 88XXau
```

预期输出：

```
88XXau               3461120  0
cfg80211             1081344  1 88XXau
```

此时应该出现一个新的无线接口：

```bash
ip link show
# 或
iwconfig
```

你应该会看到一个新接口，通常是 `wlan0` 或 `wlan1`（如果已有其他无线接口）。

### 方法 B：DKMS 安装（跨内核更新持久化）

使用标准 `make install` 时，驱动模块仅针对当前内核编译。Kali 通过 `apt upgrade` 更新内核后（这经常发生），驱动将停止工作，直到你重新编译。

DKMS（动态内核模块支持）通过在安装新内核时自动重新编译驱动程序来解决这个问题。

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# 使用 DKMS 安装脚本
sudo make dkms_install
```

或者手动注册 DKMS：

```bash
# 从 Makefile 获取驱动版本
grep MODULE_VERSION Makefile | head -1
# 示例输出：v5.6.4.2

# 将源码复制到 DKMS 目录
sudo cp -r ../rtl8812au /usr/src/rtl8812au-5.6.4.2

# 注册、编译、安装
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

验证 DKMS 注册：

```bash
dkms status
# 预期：rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## 第 3 步：开启监听模式

驱动程序加载完毕、接口可见后，就可以开启监听模式了。

### 方法 A：airmon-ng（推荐）

首先，关闭可能干扰监听模式的进程：

```bash
sudo airmon-ng check kill
```

这会停止 NetworkManager、wpa_supplicant 及其他占用接口的守护进程。预期输出：

```
Killing these processes:
  PID Name
  1234 NetworkManager
  1235 wpa_supplicant
```

启动监听模式：

```bash
sudo airmon-ng start wlan0
```

如果接口名称不同，请替换 `wlan0`。预期输出：

```
PHY     Interface   Driver      Chipset
phy0    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)
```

监听模式接口名为 `wlan0mon`。

### 方法 B：iw（手动方式）

如果不想关闭 NetworkManager，或者 airmon-ng 不可用：

```bash
# 将接口关闭
sudo ip link set wlan0 down

# 切换到监听模式
sudo iw dev wlan0 set type monitor

# 重新启动接口
sudo ip link set wlan0 up
```

开启监听模式时指定信道：

```bash
sudo iw dev wlan0 set channel 6
```

---

## 第 4 步：验证监听模式

确认接口处于监听模式：

```bash
iwconfig
```

查找 `wlan0mon`（或 `wlan0`）条目，应显示：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

关键标志是 `Mode:Monitor`。如果显示 `Mode:Managed`，则监听模式未激活。

也可以使用：

```bash
iw dev wlan0mon info
```

预期输出中包含：

```
type monitor
```

### 用 Airodump-ng 验证

快速扫描确认网卡正在捕获流量：

```bash
sudo airodump-ng wlan0mon
```

你应该立即看到 WiFi 网络出现在输出中。按 `Ctrl+C` 停止。

---

## 第 5 步：测试数据包注入

数据包注入是发送任意 802.11 帧的能力。使用 aireplay-ng 的注入测试：

```bash
sudo aireplay-ng --test wlan0mon
```

这会广播测试帧并监听附近接入点的响应。成功的结果如下：

```
15:42:11  Trying broadcast probe requests...
15:42:11  Injection is working!
15:42:12  Found 3 APs

15:42:12  Trying directed probe requests...
15:42:12  aa:bb:cc:dd:ee:ff - channel: 6 - 'HomeNetwork' - 30/30: 100%
15:42:13  11:22:33:44:55:66 - channel: 11 - 'OfficeWiFi' - 28/30: 93%
```

百分比表示成功注入率。附近接入点达到 80% 以上即为正常，信号良好时通常为 100%。

输出中出现 `Injection is working!` 即表示配置完成，可以使用完整的 Aircrack-ng 套件了。

### 5 GHz 双频注入测试

测试 5 GHz 数据包注入，指定对应信道：

```bash
# 切换到 5 GHz 信道（例如信道 36）
sudo iwconfig wlan0mon channel 36
# 或
sudo iw dev wlan0mon set channel 36

# 运行注入测试
sudo aireplay-ng --test wlan0mon
```

---

## 故障排除

### "Interface not found" / 驱动安装后没有 wlan 接口

**原因：** 驱动模块加载失败。

**解决方案：**

```bash
# 检查模块加载错误
dmesg | grep -i 88XX
dmesg | grep -i rtl

# 尝试手动加载模块
sudo modprobe 88XXau

# 若 modprobe 失败，检查缺失的依赖
modinfo 88XXau

# 重新编译驱动
cd rtl8812au
make clean && make && sudo make install
```

同时确认内核头文件与运行中的内核版本匹配：

```bash
uname -r
ls /lib/modules/$(uname -r)/build
```

如果 `build` 目录不存在，重新安装头文件：

```bash
sudo apt install linux-headers-$(uname -r)
```

---

### 开启监听模式时提示 "Operation not permitted"

**原因：** 未使用 root 权限运行，或缺少相关权限。

**解决方案：**

始终对 airmon-ng 和 aireplay-ng 使用 `sudo`：

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

如果已经是 root 用户，确认当前用户确实是 root：

```bash
whoami
# 应输出：root
```

---

### 内核更新后提示 "No module named rtl8812au" / DKMS 失败

**原因：** DKMS 未为新内核重新编译驱动程序。

**解决方案：**

```bash
# 检查 DKMS 状态
dkms status

# 若 rtl8812au 显示为 "built" 但未为新内核 "installed"：
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)

# 若上述方法失败，删除并重新安装：
sudo dkms remove rtl8812au/5.6.4.2 --all
cd /path/to/rtl8812au
sudo make dkms_install
```

---

### 监听模式已启动但未捕获到流量

**原因：** 信道错误、干扰，或监管域限制。

**解决方案：**

```bash
# 检查当前信道
iwconfig wlan0mon

# 手动设置信道
sudo iwconfig wlan0mon channel 1

# 检查监管域
iw reg get

# 设置宽松监管域（请谨慎使用，遵守当地法规）
sudo iw reg set BO
```

---

### 注入成功率低（低于 50%）

**原因：** 距接入点过远、干扰，或电源管理问题。

**解决方案：**

```bash
# 关闭接口电源管理
sudo iwconfig wlan0mon power off

# 提高发射功率（使用前请确认当地法规是否允许）
sudo iw dev wlan0mon set txpower fixed 3000  # 30 dBm
```

---

## 恢复普通管理模式

测试结束后，若需要正常连接网络：

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

或使用 iw：

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---


{{< faq >}}

## 操作步骤速查表

| 步骤 | 命令 |
|---|---|
| 检查设备识别 | `lsusb \| grep Realtek` |
| 安装依赖 | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| 克隆驱动 | `git clone https://github.com/aircrack-ng/rtl8812au` |
| 编译并安装 | `make && sudo make install` |
| 加载模块 | `sudo modprobe 88XXau` |
| 关闭干扰进程 | `sudo airmon-ng check kill` |
| 开启监听模式 | `sudo airmon-ng start wlan0` |
| 验证监听模式 | `iwconfig wlan0mon` |
| 测试数据包注入 | `sudo aireplay-ng --test wlan0mon` |

在 Kali Linux 2024+ 上，[ALFA AWUS036ACH](/zh-cn/products/alfa/awus036ach/) 搭配 aircrack-ng 的 RTL8812AU 驱动，仍然是渗透测试社区中最可靠、文档最完善的 WiFi 网卡配置方案。一旦验证注入功能正常，你便可以使用完整的 Aircrack-ng 套件、Wireshark、Kismet、Bettercap，以及任何需要监听模式或数据包注入的工具。

## 参考文献

1. [aircrack-ng 官方 rtl8812au 驱动程序仓库](https://github.com/aircrack-ng/rtl8812au)
2. [Kali Linux 官方文档](https://www.kali.org/docs/)
3. [Realtek RTL8812AU 规格说明](https://www.realtek.com/)
4. [Linux Wireless 官方文档](https://wireless.wiki.kernel.org/)
