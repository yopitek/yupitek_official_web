---



title: "HAK5 WiFi Pineapple Pager × ALFA Network：外接 USB 无线网卡兼容性评估与设置指南"
description: "这是一份深入评估 HAK5 WiFi Pineapple Pager 在 OpenWrt 环境下与 ALFA Network 外接 USB 无线网卡兼容性的技术报告与安装指南。了解 MIPS 架构交叉编译、USB 2.0 供电限制及驱动程序设置细节。"
date: 2026-06-19
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
faq:
  - question: "HAK5 WiFi Pineapple Pager 可以外接 ALFA 网卡吗？"
    answer: "可以，但需注意 MIPS 架构限制与 USB 2.0 供电。AWUS036ACM 为首选，核心内置驱动最稳定。"
  - question: "为什么 Pager 需要外接供电 USB Hub？"
    answer: "Pager 仅配 USB 2.0 接口，最大输出 500mA，高功率 ALFA 网卡峰值达 720mA，直接插入会导致重启或核心崩溃。"
  - question: "AWUS036ACM 为什么是 Pager 首选网卡？"
    answer: "MT7612U 驱动已整合于 OpenWrt 6.6 核心，Pager 上以 opkg 直接安装，无需交叉编译，最稳定可靠。"
  - question: "MIPS 架构对驱动安装有什么限制？"
    answer: "Pager 基于 MIPS32 的 MT7628AN，不支持 DKMS，无 GCC 工具链，非内置驱动必须在外部 x86 主机交叉编译。"
  - question: "RTL8812AU 在 Pager 上有什么已知问题？"
    answer: "RTL8812AU 在 MIPS 平台存在 wiphy_register 核心错误，导致接口无法加载，需套用社群修正 patch，建议改用 AWUS036ACM。"
---
在将任何高功率 USB 无线网卡插入 HAK5 Pager 之前，您必须了解以下两大主要障碍：CPU 架构与 USB 供电限制。

# HAK5 WiFi Pineapple Pager × ALFA Network：外接 USB 无线网卡兼容性评估与设置指南

无线网络安全审计需要高度精准、多功能性以及合适的硬件支持。**HAK5 WiFi Pineapple Pager** 作为搭载强大 **PineAP v8** 引擎的超便携、口袋型审计工具，吸引了大量渗透测试人员的关注。

{{< tldr >}}
Pager 采 MIPS 架构不支持 DKMS，AWUS036ACM 因 MT7612U 驱动内置于 OpenWrt 6.6 核心而随插即用；AWUS036ACH 需交叉编译且有 wiphy bug，USB 2.0 供电仅 500mA 需外接 Hub。
{{< /tldr >}}


HAK5 WiFi Pineapple Pager 可外接 ALFA 网卡，首选 AWUS036ACM 核心内置驱动最稳定，高功率网卡需搭配外接供电 USB Hub 避免核心崩溃。




然而，为了扩大审计范围、执行双频（2.4 GHz 与 5 GHz）同步操作，或在不干扰 Pineapple 内部无线电的情况下进行多信道被动监听，安全专家经常会问：**我可以在 HAK5 Pager 上外接 ALFA Network 无线网卡吗？**

简短的答案是：**可以，但需要注意关键的硬件和软件限制。**

在这份详尽的指南中，我们将剖析技术限制（例如 CPU 架构和 USB 供电限制），评估 ALFA 现售产品线的兼容性，并提供逐步的 CLI 安装与疑难排解指南。

---

## 1. 关键技术限制

### 1.1 CPU 架构：MIPS 架构限制
与运行在 x86_64 的标准 Kali Linux 主机或运行在 ARM 的 Raspberry Pi 不同，HAK5 Pager 搭载的是 **MediaTek MT7628AN SoC**（一个 **MIPS32r2, Little-Endian** 核心，在 OpenWrt 中编译为 `mipsel_24kc` 平台）。

> [!IMPORTANT]
> 由于 Pager OS 基于 **OpenWrt（版本 24.10.1，内核 6.6.86）**，因此它**不支持 DKMS**（动态内核模块支持）。您无法直接在 Pager 上编译内核驱动程序源码，因为系统不含 GCC 与 Make 工具。任何非内置的驱动程序都必须在外部 x86_64 Linux 主机上，使用 OpenWrt SDK 进行交叉编译。

### 1.2 USB 2.0 供电：电压稳定性限制
HAK5 Pager 仅配备单个 USB 2.0 Host 接口。根据标准 USB 2.0 规范，其最大电流输出为 **500 mA @ 5V（2.5W）**。

像 ALFA AWUS036ACH（RTL8812AU）或 AWUS036AXML（MT7921AUN）这类高功率无线网卡，在执行主动注入（Packet Injection）或密集数据包扫描时，其峰值耗电量高达 **720 mA（3.6W）**。

> [!WARNING]
> 若将高功率 ALFA 网卡直接插入 Pager 的 USB 接口，会导致电压不稳，从而引发**设备重启、内核崩溃（Kernel Panic）或网卡断线**。若要稳定运行高功率网卡，您**必须**通过一个**带外部供电的 USB Hub（5V/2A 以上）**连接网卡。

---

## 2. ALFA 网卡兼容性评估矩阵

下表评估了目前在售的 ALFA Network USB 无线网卡与运行 Pager OS（内核 6.6）之 HAK5 Pager 的兼容性：

| ALFA 型号 | 芯片组 | 支持频段 | USB 耗电量 | 内核 6.6 支持状态 | 安装方式 | Monitor 与 Injection 支持 | 评估结论与采购建议 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | ~600 mA (需 Hub) | **内核内置 (Native)** | 使用 `opkg` 直接安装 | ✅ 支持 / ✅ 支持 | 🏆 **首选推荐（最稳定）** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | ~720 mA (需供电 Hub) | 内核未内置 (Out-of-Kernel) | 需使用 SDK 交叉编译 | ✅ 支持 / ✅ 支持 | ⭐⭐ **高级用户**（MIPS 平台有 wiphy bug） |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4/5/6 GHz (WiFi 6E) | ~720 mA (需供电 Hub) | **内核内置 (Native)** | 使用 `opkg` + 手动置入固件 | ✅ 支持 / ✅ 支持 | ⭐⭐⭐ **潜力大**，但供电要求严格 |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | ~400 mA (Pager 可直接供电) | 部分内置 | 使用 `opkg` 安装 | ✅ 支持 / ✅ 支持 | ⭐⭐⭐ **预算折中方案** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | ~500 mA (边缘) | 内核未内置 | 需使用 SDK 交叉编译 | ✅ 支持 / ✅ 支持 | ⭐⭐ **普通**（需要手动编译驱动） |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | ~500 mA | 内核未内置 | 不建议 | ❌ **不支持监听** | ❌ **无法使用** |

---

## 3. 逐步设置指南

以下为最推荐型号的 CLI 详细设置指令。

### 3.1 方案 A：AWUS036ACM (MT7612U) — 免驱动直接支持（最推荐）

**AWUS036ACM** 是 HAK5 Pager 的最佳搭配。其搭载的 MediaTek `mt76` 主线驱动已完整整合于 Linux 6.6 内核中，完全无需繁琐的内核编译。

#### 步骤 1：连接硬件
1. 将有源 USB Hub 连接至 HAK5 Pager 的 USB 接口。
2. 将 AWUS036ACM 插入 Hub 中。
3. 通过 SSH 登录 Pager：
   ```bash
   ssh root@172.16.42.1
   ```

#### 步骤 2：验证设备识别
运行 `lsusb` 确认系统已成功识别 MediaTek 芯片组：
```bash
lsusb
# 应显示以下信息：
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### 步骤 3：使用 opkg 安装驱动套件
更新软件包源并安装必要的内核模块与固件：
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### 步骤 4：修正 MIPS 架构下的 USB Scatter-Gather 崩溃问题
在 MIPS 架构的 OpenWrt 设备上，`mt76-usb` 驱动程序在启用 USB Scatter-Gather (USB SG) 时，上传固件极易崩溃（回报 `-110` 错误）。

> [!TIP]
> 为确保无线连接的稳定性，必须通过内核参数禁用 USB SG 模式。

在 `/etc/modules.d/` 下写入禁用参数：
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
重启 Pager 以加载全新参数：
```bash
reboot
```

#### 步骤 5：验证 Monitor Mode 与数据包注入
重启完成后，SSH 登录并检查无线网卡接口：
```bash
iw dev
# 应看到新增的 wlan 接口（如 wlan2）
```

启用 Monitor Mode：
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
验证接口状态：
```bash
iw dev wlan2 info
# 应看到："type monitor"
```

---

### 3.2 方案 B：AWUS036ACH (RTL8812AU) — 高级交叉编译

**AWUS036ACH** 在 Kali Linux 下极具威力和灵敏度，但在 OpenWrt 主线内核 6.6 中未包含其驱动程序，必须手动进行交叉编译。

#### 前提条件
- 一台运行 Ubuntu 22.04 或 Debian 12 的开发主机 (x86_64)。
- 适用于 `ramips/mt76x8` 目标板的 OpenWrt SDK。

#### 步骤 1：在开发主机上下载并解压 SDK
在您的 Ubuntu 主机上运行：
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### 步骤 2：导入 rtl8812au 驱动源码
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### 步骤 3：配置与编译内核模块
进入配置菜单并选取无线网卡驱动：
```bash
make menuconfig
# 进入：Kernel modules -> Wireless Drivers -> 勾选 kmod-rtl8812au
```
开始编译：
```bash
make package/kernel/rtl8812au/compile V=s
```

#### 步骤 4：发送并安装 `.ipk` 至 Pager
编译完成后，生成的 `.ipk` 安装包会位于 `bin/packages/mipsel_24kc/` 中。将其复制至 Pager 安装：
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> 在 MIPS 架构平台上，`rtl8812au` 外置驱动程序存在知名的 `wiphy_register` 内核错误，会导致硬件接口无法在系统中加载。若遇到此情况，必须在编译前套用社区提供的 MIPS 修正 patch。因此我们仍极度建议优先采用 **AWUS036ACM**。

---

## 4. 解锁的无线渗透审计能力

在 HAK5 Pager 上外接兼容的 ALFA 网卡可直接解锁多项高级安全测试功能：

1. **5 GHz 频段审计扩展**：Pager 内置的无线芯片能力有限，新增外接双频网卡能保证您的监听及攻击范围扩充至 5 GHz 频段，捕获现代企业级 AP 的 WPA/WPA2 握手包。
2. **专用攻击发射电台**：您可以将 Pager 内置的无线电专用于 client 欺骗（Evil Twin / KARMA 攻击），而将外接的 ALFA 网卡 (`wlan2`) 专门配置为连续的 Deauth 断开信号注入源。
3. **PineAP 深度整合**：可在 Pager Web 管理界面或命令行中，将外置网卡设置为 PineAP 的主要侦测或射频发射界面，将 client 诱捕与回应速度提升 100 倍以上。

---


{{< faq >}}

## 5. 结论与采购建议

将 ALFA Network 无线网卡整合到 HAK5 WiFi Pineapple Pager 中，可构建一个低调且性能强大的移动渗透测试基站。然而，硬件配置细节至关重要：

- **快速部署、免维护首选**：请购买 [ALFA AWUS036ACM](https://yupitek.com/zh-cn/products/alfa/awus036acm)。其原生 MediaTek 驱动在 OpenWrt 6.6 内核上极为稳定且开箱即用。
- **供电保证**：务必随身携带优质的 **外置供电 USB Hub**，以确保高功率网卡的射频输出功率稳定，防止断线。

如有进一步技术咨询、大宗硬件采购或定制 OpenWrt SDK 编译需求，欢迎随时联系 **Yupitek 技术支持团队**：

- 🌐 官方网站：[www.yupitek.com](https://www.yupitek.com)
- 📧 联系信箱：[sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 联系电话：+886-2-87325338
- 📍 公司地址：台北市信义区富阳街34巷72號1楼

## 参考文献

1. [Hak5 官方文档 — WiFi Pineapple 产品文件](https://documentation.hak5.org/)
2. [OpenWrt 官方网站 — OpenWrt 24.10 发行版](https://openwrt.org/)
3. [OpenWrt mt76 驱动程序仓库 — GitHub](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au — 社群驱动 GitHub 仓库](https://github.com/aircrack-ng/rtl8812au)
5. [ALFA Network 官方网站](https://www.alfa.com.tw/)
