---



title: "Kali Linux 2026 启用监听模式完整教程：WiFi 网卡配置指南"
description: "手把手教你在 Kali Linux 2024/2025 使用 airmon-ng 或 iw 命令启用监听模式，涵盖兼容 ALFA 网卡、故障排除，以及用 airodump-ng 验证。"
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["监听模式", "Kali-Linux", "airmon-ng", "iw", "WiFi网卡", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
faq:
  - question: "监听模式与受管理模式有何不同？"
    answer: "监听模式让网卡捕获空中所有 802.11 讯框，不受管理模式只接收目标 MAC 符合自身数据包的限制，是无线渗透测试的基础。"
  - question: "airmon-ng 与 iw 指令启用监听模式有何差异？"
    answer: "airmon-ng 会自动处理干扰进程并建立 wlan0mon 虚拟接口；iw 则直接修改现有接口，不另建接口，适合需要精简控制时使用。"
  - question: "启用监听模式后接口自动切回受管理模式怎么办？"
    answer: "wpa_supplicant 或 NetworkManager 在背景重新启动所致。执行 airmon-ng check kill 终止这些进程即可解决。"
  - question: "哪些 ALFA 网卡在 Kali Linux 上完整支持监听模式？"
    answer: "AWUS036ACH（RTL8812AU）、AWUS036AXML（MT7921AUN）、AWUS036ACM（MT7612U）三款均完整支持，其中 ACM 为即插即用。"
  - question: "airodump-ng 显示 Fixed channel wlan0mon: -1 错误如何解决？"
    answer: "表示 airodump-ng 无法切换信道。执行 iwconfig wlan0mon channel 1 指定信道，并终止残留的 wpa_supplicant 程序。"
---
监听模式是无线网卡的一种特殊工作模式，能让网卡捕获空中传输的**所有** 802.11 帧——而不仅仅是发给本机的数据包。在通常的"管理模式"下，网卡只接收目标 MAC 地址与本机匹配的数据包，其余一律丢弃。监听模式则彻底取消了这道过滤。

## 什么是监听模式，它对渗透测试有何意义

{{< tldr >}}
监听模式解除网卡只接收自身数据包的限制，是无线渗透测试的根基。使用 airmon-ng 或 iw 指令搭配 ALFA 网卡即可在 Kali Linux 上稳定启用。
{{< /tldr >}}


监听模式让无线网卡截取空中所有 802.11 讯框，是 airodump-ng、Wireshark、Kismet 等工具运作的基础。Kali Linux 上可通过 airmon-ng 或 iw 指令启用。




对无线渗透测试人员来说，监听模式是一切工作的基础。没有它，**airodump-ng**、**Wireshark**（无线抓包模式）或 **Kismet** 等工具就无法被动截获网络流量。监听模式具体支持以下场景：

- **被动侦察** — 在不发送任何帧的情况下，扫描周边所有接入点和客户端。
- **握手包捕获** — 监听客户端认证过程中产生的 WPA/WPA2 四次握手包。
- **去认证攻击** — 发送 802.11 管理帧（除监听模式外还需要支持数据包注入）。
- **流氓接入点检测** — 识别网络中未经授权的接入点。
- **协议分析** — 深度解析 802.11 管理帧、控制帧和数据帧。

并非所有无线网卡都支持监听模式。该功能取决于**芯片组**以及编译进内核的**驱动程序**。面向家庭用户销售的消费级网卡几乎从不支持。专为安全研究设计的网卡——例如 ALFA Network 系列——则采用了能干净暴露监听模式的芯片组与驱动程序。

---

## 前置条件

启用监听模式之前，请确认以下几点：

1. 你正在运行 **Kali Linux**（推荐 2024.1 或更高版本），并配备兼容的内核。
2. 无线网卡已插入（USB 网卡）或安装到位（PCIe/mini-PCIe）。
3. 你拥有 **root 或 sudo** 权限。
4. 已确认网络接口名称：执行 `ip link` 或 `iwconfig`，记下无线网络接口（通常为 `wlan0`、`wlan1`，或以 `wlx...` 开头的名称）。

```bash
ip link show
```

查找以 `wlan` 开头，或以 `wlx` 加 MAC 地址命名的条目。

---

## 方法一：使用 airmon-ng 启用监听模式

`airmon-ng` 是 **aircrack-ng** 套件的组成部分，也是 Kali Linux 上切换监听模式最常用的工具。它能自动处理许多边缘情况，包括停止那些会干扰模式切换的进程。

### 第一步 — 终止干扰进程

NetworkManager、wpa_supplicant 和 dhclient 都会与监听模式产生冲突，需要先将它们关闭：

```bash
sudo airmon-ng check kill
```

预期输出：

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **注意：** 此操作会断开当前所有网络连接。如果测试期间仍需访问互联网，请改用有线连接，或将第二块无线网卡保持在管理模式。

### 第二步 — 启动监听模式

```bash
sudo airmon-ng start wlan0
```

预期输出：

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

此时网卡已进入监听模式，并自动创建了一个新的虚拟网络接口——通常命名为 **wlan0mon**。

### 第三步 — 指定信道（可选，但推荐）

默认情况下，网卡会在各信道间跳频扫描。如需针对性抓包，可将其锁定在特定信道：

```bash
sudo iwconfig wlan0mon channel 6
```

---

## 方法二：使用 iw 启用监听模式

`iw` 是现代化的底层无线配置工具。当 `airmon-ng` 不可用或行为异常时，这种方式能让你更直接地控制网卡。

```bash
# 将网络接口关闭
sudo ip link set wlan0 down

# 设置为监听模式
sudo iw dev wlan0 set type monitor

# 重新启用网络接口
sudo ip link set wlan0 up
```

三条命令合并执行：

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

与 airmon-ng 不同，此方法直接修改现有的 `wlan0` 网络接口，而不会另外创建 `wlan0mon` 接口。执行后验证修改是否生效：

```bash
iw dev wlan0 info
```

在输出中查找 `type monitor` 字段。

---

## 验证监听模式

### 使用 iwconfig 验证

```bash
iwconfig
```

处于监听模式的网络接口将显示如下信息：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

关键字段是 **Mode:Monitor**。

### 使用 iw dev 验证

```bash
iw dev
```

在对应网络接口条目下查找 `type monitor`。若显示 `type managed`，则说明监听模式未成功启用。

---

## 使用 airodump-ng 测试

监听模式启用后，用 `airodump-ng` 进行端到端测试：

```bash
sudo airodump-ng wlan0mon
```

正常情况下，你应该立即看到屏幕上滚动显示附近接入点的实时列表，包含 BSSID、信道、信号强度（PWR）、加密类型和 ESSID 等信息。若屏幕空白或出现报错，请参考下方的故障排除章节。

仅扫描 5 GHz 频段：

```bash
sudo airodump-ng --band a wlan0mon
```

针对特定网络抓包并保存供后续分析：

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## ALFA 网卡兼容性对照表

[ALFA Network](/zh-cn/products/alfa/) 无线网卡是 Kali Linux 无线测试的行业标准。以下型号均完整支持监听模式：

| 型号 | 芯片组 | 频段 | 监听模式 | 数据包注入 | 备注 |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | 渗透测试最热门型号 |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E，需要内核 5.18+ |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | Linux 驱动程序支持极佳 |

上表所有型号均已在 Kali Linux 2024.x 和 2025.x 上验证驱动程序兼容性。对于 RTL8812AU 等芯片组，若你的内核版本较新，可能需要从 Aircrack-ng GitHub 仓库手动安装驱动程序。

---

## 故障排除

### "无法启用监听模式"或网络接口消失

这通常是 NetworkManager 重新接管网络接口导致的。再次执行 `airmon-ng check kill`，然后重试。若问题持续存在，手动停止 NetworkManager：

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### 监听模式自动恢复为管理模式

部分驱动程序会在几秒钟后自动将网卡重置回管理模式，通常是因为 wpa_supplicant 在后台重新启动了。检查正在运行的进程：

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

根据 PID 终止找到的进程，然后重新启用监听模式。

### airmon-ng 执行后网络接口名称发生变化

在某些系统上，新创建的接口可能被命名为 `wlan0mon`、`mon0` 或其他名称。每次执行 `airmon-ng start` 后，务必用 `iwconfig` 或 `iw dev` 确认实际的网络接口名称，再将其用于 airodump-ng。

### airodump-ng 出现 "Fixed channel wlan0mon: -1" 错误

这表示 airodump-ng 无法切换信道。尝试手动指定：

```bash
sudo iwconfig wlan0mon channel 1
```

若仍然失败，终止所有残留的 wpa_supplicant 进程后重试。

### 新内核上的 RTL8812AU 驱动程序问题

在较新的内核版本中，内核自带的 RTL8812AU 驱动程序有时不能完整支持监听模式。此时需安装社区驱动程序：

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

安装完成后重启系统。

---

## 测试完毕后关闭监听模式

测试结束后，请务必将网卡恢复至管理模式。若保持监听模式，网卡将无法正常连接网络。

### 使用 airmon-ng：

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### 使用 iw：

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

执行 `iwconfig` 确认网络接口已恢复至管理模式，然后重新连接网络。

---


{{< faq >}}

## 总结

在 Kali Linux 上启用监听模式分两步走：先停止干扰服务，再使用 `airmon-ng` 或 `iw` 切换网络接口模式。成功的关键在于使用具备受支持芯片组的无线网卡。搭载 RTL8812AU、MT7921AUN、MT7612U 芯片组的 ALFA Network 无线网卡，在 Kali Linux 上的开箱即用体验最为可靠。

浏览 [Yopitek 提供的完整 ALFA Network 无线网卡产品线](/zh-cn/products/alfa/)——台湾 ALFA Network 授权经销商——找到最适合你无线安全研究的网卡。

## 参考文献

1. [aircrack-ng 官方文档](https://www.aircrack-ng.org/documentation.html)
2. [Kali Linux 官方文档](https://www.kali.org/docs/)
3. [Linux Wireless mac80211 子系统](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [iw 指令使用说明](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
