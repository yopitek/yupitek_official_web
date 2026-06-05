---
title: "在 Raspberry Pi 搭配 Kali Linux 使用 ALFA WiFi 网卡：完整安装教程"
description: "在运行 Kali Linux ARM64 的 Raspberry Pi 上安装 ALFA USB WiFi 网卡。涵盖 AWUS036ACH RTL8812AU 驱动编译、监听模式，以及便携式渗透测试平台搭建。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
---

运行 Kali Linux 的笔记本电脑是标准的渗透测试工作站——但绝非唯一选择。Raspberry Pi 4 或 Pi 5 搭配 ALFA USB WiFi 网卡，能打造出一个体积小巧、无风扇、被动散热的平台：可以放进夹克口袋、靠 USB-C 移动电源供电，并在目标环境中无人看守运行数小时。Kali Linux ARM64 镜像由 Offensive Security 官方提供，无需模拟即可在 Pi 4 和 Pi 5 上原生运行，完整提供 Aircrack-ng、Kismet、Wireshark、Bettercap 等 Kali 标准工具包。

最大的障碍是驱动程序。AWUS036ACH 内置的 RTL8812AU 芯片不在主线内核中，这意味着你不能插上网卡就期望它直接工作。你必须针对运行中的 ARM64 内核编译驱动程序——而编译参数与 x86-64 不同。本教程带你完成每一个步骤。

---

## 推荐硬件

并非每种 Pi 型号、网卡和电源供应器的组合都能稳定运行。以下表格整理了已知可良好运作的组合及相应取舍。

| 组件 | 推荐选择 | 备注 |
|---|---|---|
| 单板计算机 | Raspberry Pi 5（4 GB 或 8 GB） | Pi 4（4 GB+）也能正常运行；Pi 3B+ 速度不足以应付实时封包捕获 |
| 主要网卡 | ALFA AWUS036ACH | RTL8812AU 芯片；ARM 驱动支持最佳；双频 AC1200 |
| 备选网卡 | ALFA AWUS036ACM | MT7612U 芯片；内核内置驱动 (mt76x2u)；Kali ARM64 免驱即插即用 |
| WiFi 6 网卡 | ALFA AWUS036AXM 或 AXML | MT7921AUN 芯片；内核 5.18 起内置；需安装 firmware-misc-nonfree |
| USB 集线器 | 有源 USB 3.0 集线器 | AWUS036ACH 耗电约 500 mW；不加集线器可能导致 Pi USB 电压不足 |
| 存储 | MicroSD 32 GB+（Class 10 / A2） | A2 规格内存卡启动及 apt 操作明显更快 |
| 电源供应器 | 官方 Pi USB-C 电源供应器（≥ 3 A） | 第三方充电器是稳定性问题的常见来源 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH 是高电流 USB 设备。在没有有源 USB 集线器的情况下直接插入 Raspberry Pi 4 或 Pi 5，可能在负载下导致 Pi 降频或重启。同时使用其他 USB 外设时，务必使用有源集线器。
{{< /alert >}}

---

## 在 Raspberry Pi 上安装 Kali Linux ARM64

### 下载 ARM 镜像

Kali Linux 在 [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm) 提供 Raspberry Pi 官方 ARM64 镜像。下载标注为 **Raspberry Pi 4（64 位）** 或 **Raspberry Pi 5（64 位）** 的镜像。请勿使用 32 位镜像——本教程的驱动编译步骤需要 ARM64 内核。

### 烧录至 MicroSD

可使用 Raspberry Pi Imager 图形工具或命令行的 `dd` 进行烧录：

```bash
# 将 /dev/sdX 替换为你的实际 SD 卡设备（用 lsblk 确认）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

使用 Raspberry Pi Imager 时，选择**使用自定义镜像** → 选择 Kali `.img.xz` 文件 → 选择 SD 卡 → 开始烧录。

### 首次开机与初始设置

插入 SD 卡，连接显示器和键盘（或先设置无头访问），然后开机。默认账号密码为：

- **用户名：** `kali`
- **密码：** `kali`

登录后运行 `kali-tweaks` 并依提示加固默认配置。在安装任何驱动程序前，先完整更新系统：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
若计划通过 SSH 访问 Pi，在首次开机前，可在 SD 卡的 `/boot` 分区放置一个名为 `ssh` 的空白文件来启用 SSH。此机制与标准 Raspberry Pi OS 相同。
{{< /alert >}}

---

## 在 Kali ARM64 安装 RTL8812AU 驱动程序（AWUS036ACH / ACM）

RTL8812AU 驱动程序未包含在主线 Linux 内核中。在 ARM64 上，你必须从源码编译，或安装 Kali 打包的 DKMS 版本。以下介绍两种方法——建议先尝试软件包方式，仅在遇到内核版本不兼容时才改用手动编译。

### 方法一：Kali 软件包（推荐起点）

Kali Linux 提供 RTL8812AU 驱动程序的 DKMS 打包版本，内核更新时会自动重新编译。

```bash
sudo apt install realtek-rtl88xxau-dkms
```

安装完成后重启，并验证模块已加载：

```bash
sudo modprobe 88XXau
ip link show
```

若看到 `wlan1` 接口（假设 `wlan0` 是 Pi 的内置网卡），表示驱动程序运行正常。此软件包可能比 GitHub 源码晚几周，但是最简便的起点。

{{< alert "circle-info" >}}
Kali 软件包通常足以应付大多数 ARM64 环境。只有在 DKMS 软件包无法针对当前内核版本编译时，才需进行以下的手动编译（可用 `uname -r` 查看内核版本）。
{{< /alert >}}

### 方法二：从源码手动编译（ARM64）

若 DKMS 软件包失败——最常见的原因是内核版本比软件包最后测试的版本更新——请从 GitHub 的 Aircrack-ng fork 直接编译。这是 ARM64 支持的权威来源。

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 将平台标志从 x86 切换至 ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

`sed` 命令是与 x86-64 编译的关键差异。若不执行这些命令，Makefile 会默认使用 x86 平台路径，生成的模块将无法在 ARM64 上加载。

编译成功后，加载模块并验证：

```bash
sudo modprobe 88XXau
ip link show
```

应会看到新的接口——通常是 `wlan1`。若 `ip link show` 显示该接口，表示驱动程序运行正常。

---

## Raspberry Pi 上的 MT7921AUN（AWUS036AXM / AXML）

AWUS036AXM 和 AXML 使用的 MediaTek MT7921AUN 芯片自内核 5.18 起已内置于主线内核。Kali Linux ARM64 镜像使用的内核版本远高于此门槛，这意味着插上网卡驱动程序就会自动加载——无需编译。

唯一需要的额外步骤是安装 MT7921AUN 所需的闭源固件：

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

重启后，确认网卡已被检测且接口已启动：

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

若 `lsusb` 显示 MediaTek 设备，且 `ip link show` 列出新的无线接口，网卡即已就绪。MT7921AUN 的监听模式支持自内核 5.18 起已大幅改善，但在某些封包注入测试中可能不如 RTL8812AU 稳定。若需最大程度兼容旧有渗透测试工作流程，AWUS036ACH 仍是更稳健的选择。

---

## 在 Raspberry Pi 上启用监听模式

Raspberry Pi 有内置 WiFi 接口（`wlan0`）。保持它连接至你的网络以维持 SSH 访问。专用 ALFA 网卡（`wlan1`）只用于监听模式和封包捕获。在无头 Pi 上绝不要将 `wlan0` 切换至监听模式——这会中断你的 SSH 连接。

```bash
# 终止干扰监听模式的进程（NetworkManager、wpa_supplicant）
sudo airmon-ng check kill

# 在 ALFA 网卡接口上启用监听模式
sudo airmon-ng start wlan1

# 确认监听模式已启动
sudo iwconfig wlan1mon

# 开始在所有信道上捕获
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` 会创建名为 `wlan1mon` 的新接口。后续工具请一律针对 `wlan1mon` 而非 `wlan1` 运行。可用 `iwconfig` 或 `ip link show` 确认接口名称。
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
运行 `airmon-ng check kill` 会停止 NetworkManager 和 wpa_supplicant。若你通过 `wlan0` 以 SSH 连接，这也会中断你的 SSH 会话。对于无头设置，在运行这些命令前请先通过以太网或第二个有线接口连接，或使用 `tmux` 让会话在断线后仍可恢复。
{{< /alert >}}

若要停用监听模式并恢复 managed 模式：

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## 便携式渗透测试设置技巧

让硬件正常运行只是一半的工作。以下实用建议是稳定野外套件与令人沮丧的故障堆之间的差异所在。

**网络架构：** 使用 `wlan0`（Pi 内置 WiFi）维持管理连接——从同一 LAN 或热点上的笔电通过 SSH 连入 Pi。`wlan1`（ALFA 网卡）完全用于渗透测试活动。绝不混用两个角色。

**无头操作：** 避免在野外连接键盘、鼠标和显示器。在首次开机时设置好 SSH，通过笔电上的终端访问所有功能。`tmux` 会话在重新连接后仍可恢复，在网络状况不稳定时特别宝贵。

**电源：** 使用最低 3 A 的官方 Raspberry Pi USB-C 电源供应器。若使用 AWUS036ACH，另加一个额定 2.5 A 以上的有源 USB 集线器。优质 USB-C 移动电源（65 W+）可同时为 Pi、集线器和网卡供电，依负载可持续 4–6 小时。

**存储：** 将 Kismet 日志和捕获文件写入 USB SSD，而非 MicroSD 卡。MicroSD 卡有写入次数限制，在持续记录工作负载下会快速劣化。连接至有源集线器的 USB 3.0 SSD 更快且更耐用。

**外壳：** 选择有开放 USB 端口或切口的 Pi 外壳，以容纳有源集线器。带被动散热鳍片的铝制外壳有助于在持续捕获时控制温度。

---

## 在 Raspberry Pi 上运行 Kismet

Kismet 是被动 WiFi 扫描器，以后台服务器模式运行，并提供基于浏览器的网页界面。非常适合无头 Pi 部署：让 Pi 持续运行，从同一网络上的任何设备查看网页界面。

```bash
sudo apt install kismet

# 使用 ALFA 网卡以监听模式启动 Kismet
kismet -c wlan1
```

{{< alert "circle-info" >}}
直接传入接口名称时，Kismet 会自行将接口切换至监听模式。启动 Kismet 前无需运行 `airmon-ng start`，Kismet 会在内部管理接口生命周期。
{{< /alert >}}

启动后，从网络上任何浏览器访问 Kismet 网页界面：

```
http://raspberrypi.local:2501
```

首次运行时，Kismet 会提示你创建管理员账号和密码。登录后，你可以查看检测到的网络、关联的客户端、信号强度历史记录，以及已连接 GPS 设备的 GPS 数据。

Kismet 默认将所有数据记录至 `~/.kismet/` 中的 `.kismet` 数据库文件，稍后可以导出供分析或上传至 WiGLE。

---

## 使用案例：战驾（Wardriving）设置

运行 Kismet 并搭配 ALFA 网卡和 GPS 设备的 Raspberry Pi，是一套完整的自给自足战驾套件——比任何专用战驾设备都更小巧、更便宜。

**所需组件：**
- Raspberry Pi 4 或 Pi 5
- ALFA AWUS036ACH
- USB GPS 设备（u-blox 芯片与 Kismet 兼容性良好）
- 有源 USB 集线器
- USB-C 移动电源（65 W+，支持直通充电）

**设置步骤：**

1. 安装 Kismet 和 GPS 软件包：

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. 配置 `gpsd` 读取 GPS 设备：

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. 启动带 GPS 支持的 Kismet：

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. 将 Pi、集线器、网卡和移动电源装入袋子或外壳，放置于车辆中。通过连接至与 Pi 相同 WiFi 网络的手机热点或平板电脑访问 Kismet 网页界面。

Kismet 日志会为每个检测到的网络存储 GPS 坐标。使用 `kismetdb_to_wigle`（Kismet 附带）将 `.kismet` 数据库导出为 WiGLE CSV 格式，并上传至 WiGLE 进行地图标记。

{{< alert "triangle-exclamation" >}}
进行任何网络扫描活动前，请务必遵守当地法律。在许多司法管辖区，仅进行被动扫描的战驾是合法的；未经授权主动探测或连接网络则不合法。请了解你所在地区的相关法规。
{{< /alert >}}

---

## 延伸阅读

关于桌面版 Kali Linux 和 Ubuntu 上完整的 RTL8812AU 驱动程序安装指南，请参阅[在 Kali Linux 和 Ubuntu 安装 ALFA 驱动程序](/zh-cn/blog/install-alfa-driver-kali-ubuntu/)。若尚在考虑购买哪款网卡，[2026 ALFA WiFi 网卡购买指南](/zh-cn/blog/alfa-wifi-adapter-buyer-guide-2026/)涵盖每款现行型号的芯片组详情和使用场景建议。
