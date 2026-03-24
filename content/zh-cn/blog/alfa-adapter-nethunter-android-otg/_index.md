---
title: "在 Android 上通过 USB OTG 搭配 Kali NetHunter 使用 ALFA WiFi 网卡"
description: "如何通过 USB OTG 在 Android 的 Kali NetHunter 上使用 ALFA USB WiFi 网卡。涵盖 AWUS036ACH 驱动程序、监听模式命令、OTG 数据线需求及支持设备。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
---

您的 Android 手机本身就是一台放在口袋里的强大计算机。在已 Root 的设备上安装 Kali NetHunter，并通过 USB OTG 插入 ALFA WiFi 网卡，它就成为一个真正具备实力的口袋型渗透测试平台。无需笔记本电脑，无需笨重的硬件，只需您的手机、一条短小的 OTG 数据线，以及一块支持监听模式和数据包注入的网卡。

本指南涵盖让 ALFA AWUS036ACH（或兼容网卡）在 NetHunter 下正常工作所需的一切——从硬件选择到驱动程序加载、监听模式激活，以及 NetHunter 应用程序内置的无线工具。

---

## 什么是 Kali NetHunter？

Kali NetHunter 是 Kali Linux 官方的移动端渗透测试平台。NetHunter 不会替换 Android，而是在现有 Android 系统上安装一个 Kali Linux chroot 环境。您的手机继续作为普通 Android 设备运行，同时执行完整的 Kali Linux 用户空间及其所有工具。

**主要特点：**

- 无需清除 Android 数据——您的应用、联系人和数据保持完整
- 包含 NetHunter 应用，这是一个专用的攻击模块和硬件控制启动器
- 提供完整终端，可访问 Kali 工具集（Metasploit、Aircrack-ng、Nmap 等数百种工具）
- 需要已 Root 的 Android 设备才能获得完整功能

**三个版本：**

| 版本 | 需要 Root | 内核修改 | 使用场景 |
|---|---|---|---|
| NetHunter（完整版）| 是 | 是（自定义内核）| 完整攻击面、硬件接口支持 |
| NetHunter Lite | 是 | 否 | 仅 Root 工具，无需自定义内核 |
| NetHunter Rootless | 否 | 否 | 有限工具，不支持硬件攻击 |

若要通过 USB OTG 网卡支持监听模式，您需要搭载包含 RTL8812AU 模块的自定义内核的**完整 NetHunter 版本**。

**官方支持设备**包括 OnePlus、Google Pixel 及部分 Samsung Galaxy 机型。完整且最新的列表请参阅 [NetHunter 官方设备页面](https://www.kali.org/docs/nethunter/)。

**USB OTG 是必要条件。** 购买硬件前，请确认您的特定设备型号支持 USB OTG。大多数现代设备支持，但部分入门级机型和旧款硬件可能缺乏必要的 USB 控制器支持。

---

## 硬件需求

正确配置此设置意味着在每个层面选择兼容的硬件。链路中任何一个不匹配——设备、数据线或网卡——都会导致网卡无法出现在 `lsusb`、间歇性断线或驱动程序失败。

| 项目 | 需求 | 备注 |
|---|---|---|
| Android 设备 | 已 Root、支持 NetHunter、支持 USB OTG | 购买前确认 OTG 支持；需要搭载自定义内核的完整 NetHunter |
| USB OTG 数据线 / 转接头 | 根据设备接口选择 USB-C OTG 或 Micro-USB OTG | 品质很重要——劣质数据线会导致间歇性断线 |
| ALFA WiFi 网卡 | 推荐 AWUS036ACH 或 AWUS036ACM | AWUS036ACH（RTL8812AU）在 NetHunter 中拥有最佳内核模块支持；AWUS036ACM（MT7612U）亦兼容 |
| 带电源的 USB OTG 集线器 | 强烈推荐 | 防止网卡引起的电池耗尽和 USB 不稳定 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH 从 USB 接口汲取约 **500mW** 的功率。在没有专用电源的情况下直接从手机电池供电，将大幅加快电池耗电速度，并可能导致网卡在负载下重置或断线。带电源的 OTG 集线器——从墙壁插座取电并将数据传递给手机——可以完全解决此问题。
{{< /alert >}}

**选择带电源 OTG 集线器的注意事项：**

寻找明确标注支持 USB OTG 电力传输直通的集线器。这意味着集线器从 USB 充电器获取 5V 电源，从充电器（而非手机）为连接的设备供电，并仍在手机和连接设备之间传递数据。并非所有 USB 集线器都支持这一点——购买前请仔细查看产品规格。

---

## NetHunter 支持的 ALFA 网卡

NetHunter 的自定义内核包含针对特定芯片组预编译的内核模块。RTL8812AU 芯片组系列拥有最强的支持，因为它很早就被集成进来，并持续获得维护。

| 网卡 | 芯片组 | NetHunter 支持 | 备注 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ 最佳支持 | NetHunter 内核包含 `88XXau` 模块；监听模式和数据包注入完全支持 |
| AWUS036ACM | MT7612U | ✅ 良好支持 | 替代芯片组；通常可用；请根据您的特定设备内核进行确认 |
| AWUS036ACS | RTL8811AU | ✅ 可用 | 与 RTL8812AU 同一驱动程序系列；功耗较低（约 300mW） |
| AWUS036AXM | MT7921AUN | ⚠️ 有限 | WiFi 6E 网卡；内核模块可用性取决于设备和内核版本 |
| AWUS036AXML | MT7921AUN | ⚠️ 有限 | 与 AXM 相同芯片组；NetHunter 内核中未普遍支持 |

**建议：** 为了可靠的 NetHunter 操作，请坚持使用基于 RTL8812AU 的网卡。若您需要具备广泛 NetHunter 兼容性的双频 AC1200 功能，**AWUS036ACH** 是正确的选择。

---

## 设置步骤

以下步骤假设您拥有一台已安装完整 NetHunter 的已 Root Android 设备，以及已备好的 USB OTG 数据线或集线器。

### 步骤 1：打开 NetHunter 应用

在 Android 设备上启动 NetHunter 应用，前往 **Kali Services** 确认 chroot 环境正在运行。若未运行，请点击 **Start** 启动它。在内核能够将 USB 设备暴露给 Kali 工具之前，chroot 必须处于活动状态。

### 步骤 2：通过 OTG 连接 ALFA 网卡

将 USB OTG 数据线或集线器插入手机的 USB 接口，然后将 ALFA 网卡连接到 OTG 数据线或集线器。若使用带电源的集线器，请先将集线器的电源适配器连接到墙壁插座。

### 步骤 3：授予 USB 权限

Android 将显示一个权限对话框，询问是否允许 NetHunter 应用访问 USB 设备。点击**确定**，若您希望在未来的操作中跳过此提示，请勾选**始终允许**。若您在未授予权限的情况下关闭此对话框，网卡将无法从 Kali chroot 访问。

### 步骤 4：在 `lsusb` 中确认网卡

打开 NetHunter 终端并运行：

```bash
lsusb
```

您应该看到包含 **Realtek Semiconductor** 及设备 ID 的条目。对于 AWUS036ACH，预期输出类似于：

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

若 Realtek 设备未出现，问题在硬件层面——请检查 OTG 数据线，尝试不同的数据线，或确认设备的开发者选项中已启用 OTG。

### 步骤 5：加载驱动程序

```bash
sudo modprobe 88XXau
```

在大多数 NetHunter 版本中，驱动程序会在检测到网卡时自动加载。若连接网卡后接口未出现，请手动运行此命令。

### 步骤 6：确认接口

```bash
ip link show | grep wlan
```

您应该看到 `wlan1`（若您的设备内置 WiFi 接口占用 `wlan0`，则可能是 `wlan2`）。

### 步骤 7：启用监听模式

```bash
sudo airmon-ng start wlan1
```

若 `airmon-ng` 报告可能干扰监听模式的进程，请先终止它们（请参阅下方的命令部分），然后重新运行此命令。监听模式启动后，接口将重命名为 `wlan1mon`。

---

## NetHunter 上的监听模式命令

```bash
# 确认系统识别网卡
lsusb | grep -i realtek

# 若连接网卡后未自动加载，手动加载驱动程序
sudo modprobe 88XXau

# 终止干扰监听模式的进程（NetworkManager、wpa_supplicant 等）
sudo airmon-ng check kill

# 在 ALFA 网卡接口上启动监听模式
sudo airmon-ng start wlan1

# 扫描所有可见网络（按 Ctrl+C 停止）
sudo airodump-ng wlan1mon

# 捕获特定网络的流量
# -c：信道，--bssid：目标 AP MAC 地址，-w：输出文件前缀
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

---

## NetHunter WiFi 攻击（仅限授权测试）

{{< alert "triangle-exclamation" >}}
所有无线安全测试必须**仅在您拥有或已获得明确书面授权进行测试的网络和设备上**执行。未经授权访问计算机网络在全球大多数司法管辖区属于违法行为。此处描述的工具仅供授权渗透测试、安全研究和教育目的使用。Yupitek 对任何滥用行为不承担任何责任。
{{< /alert >}}

**WiFi Evil Portal（WPS3）：** 可直接在 NetHunter 应用主菜单中使用。在授权的社会工程评估中创建带有强制门户的恶意接入点，用于凭证收集。需要支持 AP 模式的外部网卡。

**MANA Rogue AP 工具包：** 位于 **NetHunter 应用 > Wireless Attacks > MANA Toolkit**。完整功能需要兼容的外部 WiFi 网卡——Android 内置 WiFi 芯片对于大多数 MANA 配置并不足够。

---

## 电池与电源管理

**功耗：** AWUS036ACH 在主动使用期间持续汲取约 500mW。在典型的 3,500 mAh Android 电池上，与正常手机使用相比，这将使您的电池耗电速度大约翻倍。

**使用带电源的 OTG 集线器：** 这是最有效的解决方案。集线器从墙壁插座取电并将其提供给 ALFA 网卡，手机 USB 接口仅传输数据。

**屏幕管理：** 将显示超时设置为 30 秒（**设置 > 显示 > 休眠**）并将亮度降至最低。

**散热注意事项：** 长时间使用网卡加上手机壳可能导致热量积聚。长时间捕获操作时请移除手机壳。

---

## 故障排除

**网卡未被识别（`lsusb` 什么都没显示）：**
1. 确认已启用 USB OTG——查看**设置 > 开发者选项 > OTG**
2. 尝试不同的 OTG 数据线——数据线质量是常见的失败点
3. 确认您的设备支持 USB OTG

**驱动程序未加载（`modprobe` 后没有 `wlan1` 接口）：**
1. 在 NetHunter 终端查看 `dmesg` 中的错误信息：`dmesg | tail -30`
2. 确认 NetHunter chroot 正在运行
3. 确认您的 NetHunter 版本包含 `88XXau` 模块：`find /lib/modules -name "*88XX*"`

**`wlan1` 接口在使用中消失：**
几乎必然是 USB 电源问题。使用带电源的 OTG 集线器。

**权限被拒绝错误：**
确保您在 NetHunter chroot 中以 root 身份运行命令。先运行 `sudo su`，然后再执行命令。

**监听模式已启动但 `airodump-ng` 中未显示任何网络：**
1. 尝试 `sudo airodump-ng --band abg wlan1mon` 扫描所有频段
2. 确认在启动监听模式前已运行 `airmon-ng check kill`

---

## 相关指南

- [AWUS036ACH 在 Kali Linux（桌面/笔记本）上的设置指南](/zh-cn/blog/awus036ach-kali-linux-setup/)
- [在 Raspberry Pi 和 Kali 上使用 ALFA 网卡](/zh-cn/blog/alfa-adapter-raspberry-pi-kali/)
