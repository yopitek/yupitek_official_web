---
title: "Kali Linux 内核更新后网卡罢工？RTL8812AU 驱动 DKMS 编译失败与 Secure Boot 排障"
date: 2026-08-18
draft: false
slug: "kali-linux-rtl8812au-dkms-secure-boot-mok-setup"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "详解 Kali Linux 内核升级时 RTL8812AU 驱动失效原因，提供稳定社区驱动安装步骤与 Secure Boot 开启下的 MOK 模块签署排障教程。"
featureimage: "/images/blog/05_dkms_mok_flow_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "遇到 Secure Boot 阻挡未签署驱动时，应该关闭 Secure Boot 吗？"
    answer: "不建议。安全做法是通过 mokutil 导入自签密钥（MOK 机制），在维持系统安全防护的同时完成模块加载。"
---

![Linux Kernel DKMS and Secure Boot MOK Flowchart](/images/blog/05_dkms_mok_flow_blueprint.jpg)

> **适用硬件**：ALFA AWUS036ACH（Realtek RTL8812AU）
> **适用平台**：Kali Linux、Debian／Ubuntu 等 Debian 系发行版（Linux x86_64／ARM64）
> **不支持**：macOS（含 Apple Silicon）——详见下方「兼容性与平台红线」。

---

## TL;DR

AWUS036ACH 使用的是 **非内核内置（out-of-tree）** 的 Realtek 驱动。执行 `apt upgrade` 升级内核（Kernel）后，旧模组因为内核 ABI 已变更而失效，这**不是网卡坏掉，而是驱动模组需要重新编译**。

解法是安装社区维护的 `aircrack-ng/rtl8812au`（或是 `morrownr/8814au`）驱动，并通过 **DKMS** 让它在新内核安装时自动重新编译。如果系统开启 **Secure Boot**，内核会拒绝加载未签署的自订模组，此时必须通过 **MOK（Machine Owner Key）金钥签署**机制汇入您的自签金钥——**请不要关闭 Secure Boot**。

---

## 为什么每次 `apt upgrade` 之后网卡就罢工？

### 问题根源：内核 ABI 与 out-of-tree 模组

Linux 的硬件驱动程序多以「**内核模组（Kernel Module）**」的形式存在，副档名通常是 `.ko`。常见的两种类型：

| 类型 | 说明 | 内核更新后行为 |
|------|------|--------------|
| **In-tree（内核内置）** | 驱动原始码直接收录在 Linux Kernel 原始码树，例如 `mt7921u`、`mt76x2u` | 随内核一起编译，更新后自动可用，**不需任何手动处理** |
| **Out-of-tree（内核外挂）** | 驱动原始码在内核树之外，例如 Realtek `rtl8812au` | 只针对「当时的内核版本」编译，新内核 ABI 变更后**模组失效** |

AWUS036ACH 的 `RTL8812AU` 属于 out-of-tree。Linux 对模组与内核之间的兼容性（Kernel ABI / vermagic）要求严格，模组必须与**目前执行中的内核版本完全一致**（含 `uname -r` 的完整版本字符串）才允许加载。

当您执行：

```bash
sudo apt update && sudo apt upgrade -y
```

系统若更新了 `linux-image-*`（内核映像档），重开机后执行的就是新内核；而旧内核时期编译的 `88XXau.ko` 模组无法加载到新内核，于是发生「网卡插上去，系统却完全抓不到」。

### 症状快速辨识

| 症状 | 典型原因 |
|------|---------|
| `lsusb` 看得到网卡，但 `ip link` 没有 `wlan` 接口 | **驱动模组没有被加载**（最常见） |
| `sudo modprobe 88XXau` 回传错误 | 模组与目前内核不兼容或根本不存在 |
| `dmesg` 出现 `Required key not available` | **Secure Boot 没有签署**（见第五章） |
| `dmesg` 出现 `Module 88XXau was not signed` 或 `signature` | Secure Boot 签章验证失败 |
| 编译时出现 `Bad return status for module build` | 缺少或版本不符的 `linux-headers`（见第四章） |

> **判断口诀**：先看 `lsusb` 确认硬件被 USB 层抓到 → 再看 `dmesg` 确认驱动层为什么加载失败。两者分开诊断，才不会误判成硬件故障。

---

## 动手前先检查：你真的需要社区驱动吗？

### 1. 内核 6.13+ 先试内置支持

自 **Linux 6.13** 起，`rtl8812au` 系列已有以 `mac80211` 为基础的内核内置驱动加入主线（`lwfinger/rtw88` 生态系）。若您的内核是 6.13 或更新版本，**优先试试内置驱动**：

```bash
# 先确认内核版本
uname -r

# 检查内建模组是否已存在
lsmod | grep 88XXau
lsmod | grep rtw

# 直接插入网卡后确认接口
ip link
```

如果内置驱动就能抓到接口，您**不需要**任何 DKMS 编译步骤。不过要注意：对资安研究而言，**完整的监听模式（Monitor Mode）与数据包注入（Packet Injection）支持**，社区驱动仍然是最成熟、最稳定的选择——这是很多人仍选择编译 `rtl8812au` 社区驱动的原因。

### 2. 确认芯片与 USB ID

在动手前先确认您手上的型号与芯片对应：

| 型号 | 芯片 | USB Vendor:Product | MIMO | 频段与速率 |
|------|------|--------------------|------|-----------|
| **ALFA AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | 2×2 | 2.4 GHz 300 Mbps ＋ 5 GHz 867 Mbps（AC1200） |

```bash
lsusb
# 预期看到:
# Bus ... Device ...: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...
# 或
# Bus ... Device ...: ID 0bda:8813 Realtek Semiconductor Corp. RTL8814AU ...
```

> 芯片与型号对错，之后选错驱动会编到怀疑人生——下载驱动前**务必先跑一次 `lsusb`**。

---

## 移除旧驱动：从干净环境开始

编译新的社区驱动前，先把系统里既有的旧版 Realtek 驱动清干净，避免「两个驱动打架」导致接口名称混乱或加载冲突。

### 方式一：通过 DKMS 卸载

如果您或先前安装流程有用 DKMS，进到原始码目录执行官方移除指令：

```bash
cd rtl8812au          # 换成你之前 clone 的驱动目录
sudo make dkms_remove
```

### 方式二：直接用 dkms 指令移除

不知道原始码在哪也没关系，直接用 `dkms` 列出并移除：

```bash
sudo dkms status
# 例如输出:
# 8812au/5.6.4.2, 6.1.0-kali9-amd64, x86_64: installed

# 移除该版本的所有内核建置
sudo dkms remove 8812au/5.6.4.2 --all
```

### 方式三：把模组从内核模组目录中移除

如果以前是用 `make install` 直接安装（没有 DKMS）：

```bash
# 找出残留的模组档
find /lib/modules -name "*88XXau*" 2>/dev/null

# 手动删除 (请依实际路径)
sudo rm -f /lib/modules/$(uname -r)/kernel/drivers/net/wireless/rtl8812au/88XXau.ko
sudo depmod -a
sudo modprobe -r 88XXau 2>/dev/null
```

**验证已清干净：**

```bash
sudo dkms status        # 应无 8812au / 8814au 相关项目
lsmod | grep 88XXau     # 应无输出
```

---

## 用 DKMS 安装最稳定的社区驱动

### 为什么要用 DKMS？

DKMS（Dynamic Kernel Module Support）的内核价值：当您**之后再次升级内核**时，DKMS 会在新内核安装完成后**自动重新编译并安装**驱动模组。这正是解决开头「每次 `apt upgrade` 网卡就罢工」的根本办法——一次设定，之后终生自动重建。

### 1. 安装编译相依套件

```bash
sudo apt update
sudo apt install bc mokutil build-essential libelf-dev linux-headers-$(uname -r) dkms
```

> **重点**：`linux-headers-$(uname -r)` 的版本**必须与目前执行的内核完全一致**。只要是版本对不上，编译 100% 会失败并回报 `Bad return status for module build`。

如果编译时才想到要补 headers，可以先确认：

```bash
dpkg -l | grep linux-headers
# 确认里面有 linux-headers-$(uname -r) 对应的版本
```

### 2. 抓取并用 DKMS 安装驱动

**AVUS036ACH（RTL8812AU）** 请使用 aircrack-ng 社区长期维护的仓库（同时也支持 RTL8814AU）：

```bash
git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

> 以 `-b v5.6.4.2` 固定版本可以避免「最新 master 与特定内核不兼容」的风险，这是社区实务上最稳定的做法。安装完成后**重开机一次**，让新内核最干净的状态重新加载。

### 3. 验证驱动已加载

```bash
lsusb                              # 仍须看到 0bda:8812 或 0bda:8813
sudo modprobe 88XXau               # 手动加载 (若未自动加载)
lsmod | grep 88XXau                # 应列出 88XXau
ip link                            # 应出现 wlan0 / wlan1 等无线接口
sudo dkms status                   # 应显示 installed
```

若接口被命名成 `wlx...`，那是 NetworkManager 的 predictible naming 正常行为，不影响使用。

---

## 启用监听模式（Monitor Mode）与数据包注入测试

这个网卡被拿来做资安研究的内核原因，就是监听模式与数据包注入。在确认驱动加载、接口出现后，可以用标准流程验证：

```bash
# 1. 关闭会干扰监听的网络服务
sudo airmon-ng check kill

# 2. 把接口 (以 wlan1 为例) 切换到监听模式
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# 3. 确认已进入 monitor 模式
iwconfig
# wlan1   IEEE 802.11 ... Mode:Monitor ...

# 4. 数据包注入测试
sudo aireplay-ng --test wlan1
# 预期看到: Injection is working!
```

> **合法性提醒**：Monitor Mode 与数据包注入仅限用于**您拥有或已获明确授权**的网络环境（自家实验室、教程课程、企业委托的渗透测试）。请遵守当地法规，并只对授权目标操作。

---

## Secure Boot 下的安全排障：MOK 金钥签署

### 为什么内核会拒绝加载自订模组？

现代的 Ubuntu／Kali 安装默认启用 **UEFI Secure Boot**。这是 UEFI 韧体与内核共同创建的一道**开机链信任防线**：内核只会加载**经过信任金钥签署**的模组。发行版官方模组由发行版的签署金钥签署；而您**自己编译的 DKMS 模组**没有这个签章，因此内核会拒绝加载并回报 `Required key not available`。

**正确且安全的解法**，是让您的机器「信任您自己的金钥」——也就是把您这台机器产生的公钥，注册为 **MOK（Machine Owner Key，机器拥有者金钥）**。这完全是自行掌控、不需要关闭任何安全防护的做法。

> ⚠️ **安全红线**：请**不要**为了让驱动加载而关闭 Secure Boot。Secure Boot 是系统启动链的重要防护，关闭它等同于降低整台机器对 rootkit 与开机层攻击的防御。通过 MOK 签署即可安全加载驱动，不需要付出这个代价。

### MOK 运作原理（白话版）

```
您编译出的模组 (88XXau.ko)
        │  以"机器本金钥"签署 (private key / mok.key)
        ▼
内核加载前检查签章
        │  用"MOK 公钥"(mok.pub) 验证
        ▼
内核信任此金钥? (已在 UEFI MOK 清单中?)
   │是                     │否
   ▼                       ▼
加载成功 ✅         拒绝加载: Required key not available ❌
```

### 1. 检查 DKMS 的签署金钥是否已自动产生

在 Ubuntu／Kali 这类发行版，启用 Secure Boot 时，**DKMS 会在第一次编译时自动产生一对签署金钥**：

```bash
ls -l /var/lib/dkms/mok.key /var/lib/dkms/mok.pub
# mok.key  = 私钥 (本机签署用, 切勿外流)
# mok.pub  = 公钥 (汇入 UEFI 用)
```

> 若这两个档案不存在，代表您的 DKMS 版本较旧或 Secure Boot 侦测未正确触发。先执行一次 `sudo dkms autoinstall` 让它产生；若仍无，再回来确认 Secure Boot 状态。

### 2. 汇入 MOK 公钥（mokutil --import）

```bash
sudo mokutil --import /var/lib/dkms/mok.pub
```

执行后系统会请您**设定一组一次性密码（One-time password）**。这组密码只在下一次重新启动、于 UEFI 的 MOK 管理画面中使用，**请务必记住**。

确认汇入已排入队列：

```bash
sudo mokutil --list-new
# 应列出 /var/lib/dkms/mok.pub
```

### 3. 重新启动，进入 MOK 管理画面完成注册

1. 重新开机。
2. 开机过程中会出现 **MOK Management（蓝底白字的 UEFI 管理画面）**。
3. 依序操作：
   - 选择 **Enroll MOK** → **Continue** → **Yes**
   - 输入您在第 2 步设定的**一次性密码**
   - 选择 **Reboot** 完成注册并重新开机。

> **小提醒**：如果没看到 MOK 管理画面，通常是因为您的装置是通过 `shim` 开机才不会显示；请确认开机加载器（如 GRUB）是通过 shim 被签署的，一般 Ubuntu／Kali 默认即是如此。

### 4. 验证 MOK 已生效

```bash
# 检查 MOK 公钥是否已被内核信任
sudo mokutil --test-key /var/lib/dkms/mok.pub

# 查看内核证书链 (应能看到 MOK 相关项目)
sudo dmesg | grep -i cert

# 现在重新加载模组
sudo modprobe 88XXau
lsmod | grep 88XXau
```

若 `dmesg` 不再出现 `Required key not available`，且 `88XXau` 成功加载，您的驱动就在 Secure Boot 开启的状态下正常运作了。

### 常见签署错误对照表

| `dmesg` 消息 | 原因 | 正确做法 |
|-------------|------|---------|
| `Required key not available` | 模组未签署，或 MOK 尚未注册 | 完成 `mokutil --import` ＋ MOK 注册流程（本节步骤 2–3） |
| `Module XXX was not signed` | Secure Boot 开启但 DKMS 未签署 | 确认 `/var/lib/dkms/mok.key` 存在并重新 `sudo dkms autoinstall` |
| `Bad return status for module build` | headers 缺失或与内核不符 | `apt install linux-headers-$(uname -r)` 后重编 |
| `disagrees about version of symbol` | 模组与目前内核版本不同步 | 重新 `sudo make dkms_install`，勿跨版本混用 |

---

## 采购前兼容性确认工作表

> 如果您正在评估要不要购入 AWUS036ACH，请先逐项核对下列清单，避免买回家才发现环境不符——这份表格同时也是日后开技术支持单时的自助检查表。

| # | 检查项目 | 通过条件 | 过不了怎么办 |
|---|---------|---------|------------|
| 1 | 操作系统 | Linux（Kali / Debian / Ubuntu） | **macOS 不使用此二型号**（见下方红线） |
| 2 | 内核版本 | 已知版本并有对应 headers | 手动编译前先 `lsusb` 确认芯片 |
| 3 | 是否有编译环境 | 可执行 `gcc`、`make`、`dkms` | `apt install build-essential dkms` |
| 4 | Secure Boot 状态 | 已知是否开启 | `mokutil --sb-state` 查找 |
| 5 | USB 供电 | 直插主机板 USB 3.0 或**有供电的 USB Hub** | 高功率网卡需稳定供电（ACH 最高 0.7A@5V） |
| 6 | 需要监听／注入？ | 是→社区驱动 DKMS；否→可考虑内核 ≥6.13 内置 | 见第二章 |

### 平台红线（Support Boundary）

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| Kali Linux / Debian / Ubuntu | ✅ 支持 | 需 DKMS 编译社区驱动 |
| Raspberry Pi 3B+ / 4 / 5（Linux） | ✅ 支持 | 建议 2.5A–3A 电源，避免注入时压降掉卡 |
| **macOS（Intel）** | ⚠️ 最高 10.15 Catalina，且需旧驱动 | 不建议，官方已停止支持 |
| **macOS（Apple Silicon M1/M2/M3/M4）** | ❌ **不支持** | 无可用驱动，请改用原生内核支持的 MediaTek 型号（如 AWUS036AXML） |
| Windows 10 / 11 | ✅ 支持 | 使用 Realtek 官方驱动 |

---

## 常见问题（FAQ）

**Q1：为什么我每次升级内核，网卡就失灵，难道是硬件坏了？**
不是。RTL8812AU/RTL8814AU 的驱动是 out-of-tree（内核外挂），它只针对「安装时的特定内核版本」编译。内核更新后旧模组与新内核不兼容，系统就加载失败。**用 DKMS 安装后，之后的内核更新会自动重建模组，问题就不再出现。**

**Q2：Secure Boot 开着，会不会永远灌不了这个驱动？**
不会。只要通过 MOK 机制把机器自己的公钥（`/var/lib/dkms/mok.pub`）注册为信任金钥，DKMS 重新编译后会自动用 `mok.key` 签署模组，内核即可加载。这完全不需要关闭 Secure Boot。

**Q3：`aircrack-ng/rtl8812au` 和 `morrownr` 的仓库差在哪？怎么选？**
`aircrack-ng/rtl8812au` 是 aircrack-ng 社区长期维护、被 Kali 官方文档引用最广的版本，支持 RTL8812AU 与 RTL8814AU。**AWUS036ACH 建议用 `aircrack-ng/rtl8812au`（固定 `v5.6.4.2`）**。这是 DKMS 安装、日后自动重建，功能与稳定性都在业界水准之上。

**Q4：我看到有人说直接关掉 Secure Boot 最省事，我可以做吗？**
**不建议。** Secure Boot 是开机链的信任根基，关闭会让整台机器暴露在针对启动过程与 rootkit 的攻击风险中。用 MOK 签署只花您一次重新开机的时间，就能在保留防护的前提下加载驱动——**安全做法才值得复制到工作机上**。

**Q5：内核升级后，DKMS 到底要不要我再去手动跑一次？**
一般**不需要**。DKMS 安装后，系统每当安装新内核，都会自动触发重新编译您的模组。您只需要在升级后重开机；万一看到编译失败消息，优先检查 `linux-headers-$(uname -r)` 是否已同步更新即可。

**Q6：Raspberry Pi 上插入后频繁断线或注入到一半掉卡，是驱动问题吗？**
多半是**供电不足**。这两款高功率网卡在数据包注入时瞬间电流较高（AWUS036ACH 最高约 0.7A@5V），Pi 的 USB 电源若不足会直接掉卡。请改用 **2.5A–3A 的电源供应器**或**有独立供电的 USB Hub**，并可加入 `options 88XXau rtw_power_mgnt=0 rtw_enusbss=0` 关闭 USB 省电，避免动态省电干扰注入。

---

## 结论

Kali Linux 内核更新后网卡「罢工」是 out-of-tree 驱动最典型的宿命，**不是硬件故障，也不是系统中毒**。只要掌握三件事就能根治：

1. **认清根源**——RTL8812AU/RTL8814AU 需要为每个内核版本重新编译，内置驱动（内核 ≥6.13）或原生内核支持型号（如 MediaTek MT7921AU）可省去大部分编译麻烦。
2. **用 DKMS 一劳永逸**——`sudo make dkms_install` 之后，未来内核升级会自动重建模组，不再需要每次手动处理。
3. **Secure Boot 不是障碍**——通过 MOK 金钥签署（`mokutil --import /var/lib/dkms/mok.pub` ＋ UEFI 注册）即可安全加载自订模组，全程不需关闭任何安全防护。

如果您正在采购，AWUS036ACH（RTL8812AU）是 Linux 资安社区高度验证的选择；而若您希望**即插即用、零编译**，可参考原生内核支持的 MediaTek 系列型号。动手之前，记得先跑完「采购前兼容性确认工作表」，并确认您使用网卡的目的符合法规与授权范围。

---

## 参考资源

| 资源 | 连结 |
|------|------|
| aircrack-ng RTL8812AU 社区驱动（含 RTL8814AU） | https://github.com/aircrack-ng/rtl8812au |
| morrownr USB-WiFi 情境指南（含 MOK 说明） | https://github.com/morrownr/USB-WiFi |
| Linux 内核内置 RTL8xxx（rtw88/mac80211 生态系） | https://github.com/lwfinger/rtw88 |
| ALFA AWUS036ACH 官方产品页 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036ACH 官方文档 | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Ubuntu Secure Boot 签署 DKMS 模组指引 | https://ubuntu.com/ 搜索「dkms secure boot mok」 |
| Yopitek 技术支持 | https://yupitek.com/ |

> **合法使用声明**：本文所述之监听模式、数据包注入等操作，仅限于您拥有或已获得明确授权之网络环境。用户须自行遵守所在地法律规范，并确保所有测试皆有合法授权依据。
