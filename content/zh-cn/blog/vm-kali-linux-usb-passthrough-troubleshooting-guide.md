---
title: "虚拟机 Kali Linux 抓不到外接网卡？VirtualBox/VMware USB 穿透与断线诊断手册"
date: 2026-08-18
draft: false
slug: "vm-kali-linux-usb-passthrough-troubleshooting-guide"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "全面解析 VirtualBox 与 VMware 的 USB 穿透机制，解决 Kali 虚拟机无法识别外接 USB 网卡、Extension Pack 设置及自动过滤器排障方案。"
featureimage: "/images/blog/08_usb_passthrough_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "为什么虚拟机默认使用 NAT 或 Bridge 时无法使用网卡的监听模式？"
    answer: "NAT/Bridge 模式下虚拟机仅获得虚拟以太网卡（eth0），只有通过 USB Pass-Through 实体穿透才能直接控制原生无线射频接口。"
---

![Virtual Machine USB Pass-Through Blueprint](/images/blog/08_usb_passthrough_blueprint.jpg)

> **适用平台**：Windows / Linux / macOS 主机 + Oracle VirtualBox / VMware Workstation 虚拟机（Guest = Kali Linux / Debian / Ubuntu）
> **引导硬件**：ALFA AWUS036ACH（Realtek RTL8812AU）/ ALFA AWUS036AXML（MediaTek MT7921AU）
> **本篇定位**：标准化「USB 穿透（USB Pass-through）」排障診斷手冊。macOS 主机的 USB 穿透限制说明见第五章。

---

## TL;DR

很多 Kali 用户把网卡插在主机上，卻在虚拟机里看不到无线接口——**这幾乎都不是网卡坏掉**，而是三个非常常见的原因之一：

1. **VirtualBox 没装擴充套件（Extension Pack）**：没有它，Guest 连 USB 2.0/3.0 控制器都用不了（USB 1.1 的傳输速率上限僅 12 Mbps，根本不够网卡用）。
2. **USB 穿透设定没做**：主机默认「独占」所有 USB 装置，Guest 要嘛手动挂载、要嘛设定「USB 過濾器（VM USB Filter）」来自动接管网卡。
3. **Guest 內部的驅动程序没加载**：USB 层穿過去了（`lsusb` 看得到），但 Linux 没有相对应的驅动程序，所以 `ip link` 没出现 `wlan` 接口。

診斷口訣：**主机端 `lsusb` 确認硬件正常 → Guest 端 `lsusb` 确認穿透成功 → Guest 端 `iwconfig` / `ip link` 确認无线接口 → 還没有就看 `dmesg` 找驅动层原因。** 依序往下走，就能在三分鐘內判斷問题出在哪一层。

---

## 1. 为什么虚拟机默认调用不到主机的无线网卡？

### 1.1 你的 USB 网卡「同时」只屬於一个操作系统

USB 的運作是**单一主控（single host）**架构：一个 USB 装置在同一个时间點，只能被一个「USB 主控制器（Host Controller）」控制。当网卡插在主机上，装置会先被**主机操作系统（Host OS）**列舉（enumerate）並接管，主机的驅动程序認識它、控制它。

虚拟机（Guest VM）不是插在 USB 汇流排上的实体装置，它只是跑在主机里、由管理程序（Hypervisor）扮演出的「假硬件」。所以 Guest 想要使用 USB 网卡，**必須由主机把装置主动「移交」给 Guest**——这个机制就叫 **USB 穿透（USB Pass-through / USB Redirection）**。

### 1.2 USB 穿透到底穿透了什么？

以 VirtualBox 为例，穿透流程是这樣的：

```
实体 USB 网卡（AWUS036ACH / AWUS036AXML）
       │  插在主机的 USB 实体接口
       ▼
主机操作系统（Host OS）的 USB 主控制器
       │  Hypervisor（VirtualBox）攔截並重新导向
       ▼
虚拟的 USB 主控制器（模拟的 EHCI / xHCI）
       │  Guest（Kali）看起来「就像插在自己身上」
       ▼
Kali 的 USB 驅动程序 → 无线网卡驅动 → wlan 接口
```

穿透成功后，这个装置在**主机端会被移转控制权**（行为上像被「拔走」，主机上无法再使用它），转而在 Guest 內变成一个全新的 USB 装置。**这是正常现象，不是 bug。** 主机的一个 USB 装置不能同时给兩邊用。

### 1.3 「抓不到」其实有三个层次

| 层次 | 檢查工具 | 症状 | 代表意義 |
|------|---------|------|---------|
| **USB 穿透层** | Guest 內 `lsusb` | `lsusb` 完全看不到网卡的 VID:PID | 穿透失败（Extension Pack / 控制器 / 過濾器問题） |
| **驅动程序层** | Guest 內 `dmesg` | `lsusb` 看得到，但 `dmesg` 有错误（如缺韧体、`Required key not available`） | Guest 內部缺驅动程序或模组加载失败 |
| **无线接口层** | Guest 內 `iwconfig` / `ip link` | `lsusb` 與 `dmesg` 都正常，卻没有 `wlan` 接口 | 驅动程序加载了但接口未註冊，或模式／设定問题 |

> **判斷口訣**：先看 `lsusb` 判斷「装置有没有穿透进 Guest」，再看 `ip link` 判斷「驅动程序有没有認識它」。**别一开始就懷疑网卡坏了。**

---

## 2. VirtualBox：先装 Extension Pack，再设 USB 3.0 控制器

### 2.1 擴充套件（Extension Pack）是非装不可的

VirtualBox 基礎套件**只內建 USB 1.1（OHCI）控制器**的模拟，而 USB 1.1 的傳输速率完全不够网卡使用。**USB 2.0（EHCI）與 USB 3.0（xHCI）控制器都要靠 Oracle 官方「擴充套件（Extension Pack）」**才有。

没有装 Extension Pack 的症状很典型：Guest 设定里选不到 USB 2.0 / USB 3.0 控制器，或一挂载网卡就回報「装置连接到虚拟机失败（error code E_FAIL / VERR_PDM_NO_USB_PORTS）」。

### 2.2 版本必須「完全不差」地对上

Extension Pack 的版本**必須與 VirtualBox 主程序版本完全一致**（例如 VirtualBox 7.0.20 就要配 7.0.20 的 Extension Pack），差一个小版本都可能安装失败或加载失败。

```bash
# 查看目前 VirtualBox 版本
vboxmanage --version
```

到 Oracle 官方下载頁（https://www.virtualbox.org/wiki/Downloads）下载对应版本的
`Oracle_VM_VirtualBox_Extension_Pack-<版本>.vbox-extpack`，然后：

```bash
# 方式一：GUI 安装（VirtualBox 主程序 → 档案 → 工具 → Extension Pack Manager → 安装）
# 方式二：指令安装
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# 确認已安装
VBoxManage list extpacks
```

> 安装时会显示 Oracle 授权（Personal Use and Evaluation License）；个人使用免費，商用建制请依授权內容辦理。

### 2.3 Linux 主机：把自己加入 vboxusers 群组

在 Linux 主机上，VirtualBox 要存取 USB 装置，**需要用户屬於 `vboxusers` 群组**。很多人安装了擴充套件卻還是失败，就是卡在权限。

```bash
# 加入群组（以你的用户名称取代 <user>）
sudo usermod -aG vboxusers $USER

# 登出再登入（或重新开机）让群组生效；确認群组已生效
id $USER
```

### 2.4 设定 USB 3.0（xHCI）控制器

1. 选取你的 Kali 虚拟机 → **设定（Settings）→ 接口（Ports）→ USB**。
2. 勾选「Enable USB Controller」，並选择 **USB 3.0 (xHCI) Controller**。
   - AWUS036AXML 是 USB 3.2 Gen 1（USB-C）规格，**务必选 USB 3.0 (xHCI)**，选 USB 2.0 会限制傳输速率。
   - AWUS036ACH 为 USB Type-A 接口，在 USB 2.0 與 USB 3.0 控制器下皆可使用；若要較佳傳输速率，一樣选 USB 3.0 (xHCI)。
3. 修改控制器后**关机再开机**（不是在 Guest 內执行 reboot）才能套用变更。

### 2.5 手动挂载：視窗右下角的 USB 圖示

开启 Kali 虚拟机后，注意視窗**右下角的 USB 圖示**（一支 USB 插頭）：

1. 點 USB 圖示 → 会列出目前插在主机上的 USB 装置。
2. 你的网卡应该显示类似 `Realtek 802.11ac NIC`（ACH），或 `ALFA AWUS036AXML` / MediaTek（AXML）。
3. 點它一下，装置就会「移交」给 Kali。

如果清单是空的，代表穿透层出了問题——回去 2.2 / 2.3 檢查，或直接跑第六章排障工作表。

### 2.6 VMware 对照：內建支持，但有兩个檢查點

VMware Workstation / Fusion **不需要**额外擴充套件就有 USB 穿透功能，但有兩个常见檢查點：

1. **主机端服务**：Linux 主机上请确認 `vmware-usbarbitrator`（USB 仲裁服务）有在跑：
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # 如果没在跑，启动並设为开机自动执行
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **虚拟机设定**：虚拟机设定 → USB Controller → 勾选 **USB 3.1（或 USB 3.0）**。
3. **手动连接**：VMware 視窗选单 → **可移除装置（Removable Devices）→ 你的网卡 → 连接（Connect）**。

> **对照重點**：VirtualBox 卡在「没装擴充套件」；VMware 卡在「仲裁服务没跑」或「控制器 USB 3.0 没开」。先确認你用的是哪家，再对号入座。

---

## 3. 診斷工具三步驟：lsusb → iwconfig → dmesg

穿透设定做完后，用三个指令把問题定位到「穿透层」還是「驅动层」。

### 第 0 步：主机端先确認硬件正常（别把問题赖给网卡）

在**主机操作系统**开终端执行：

```bash
lsusb
```

預期看到（依型号）：

```
# AWUS036ACH（Realtek RTL8812AU）
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# 或 AWUS036AXML（MediaTek MT7921AU）
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- 主机看得到 → 硬件與线材正常，問题在穿透或 Guest 驅动。
- 主机也看不到 → **先檢查主机端**（换 USB 接口、换线、另一台主机交叉测试），再考虑开技术支持单。

### 第 1 步：Guest 端 lsusb——穿透成功没有？

在 **Kali 虚拟机內**执行：

```bash
lsusb
```

- 看得到同樣的 VID:PID → **穿透成功**，跳到第 2 步。
- 看不到 → **穿透失败**，回去檢查第二章（Extension Pack / 控制器 / vboxusers 群组），或确認网卡是否被主机的其他软件占用。

### 第 2 步：iwconfig / ip link——无线接口出现没有？

```bash
iwconfig
# 或（較新版本）
iw dev
ip link
```

- 出现 `wlan0` / `wlx...` 接口 → **全部打通**，可以开始使用了。
- 没有无线接口但 `lsusb` 看得到 → 問题在 **Guest 的驅动程序层**，看第 3 步。

### 第 3 步：dmesg——驅动层为什么失败？

```bash
# 观察内核刚才的訊息
sudo dmesg | tail -30
# 過濾 USB 與无线相关的訊息
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

常见的 `dmesg` 結果对照：

| `dmesg` 訊息 | 原因 | 处理方式 |
|-------------|------|---------|
| `usb 3-1: new high-speed USB device ...` 之后没有后续 | 装置列舉完成，但没有可用的驅动程序 | Guest 內安装对应驅动程序（见 FAQ Q4） |
| `Direct firmware load failed` / `firmware_loading` | 缺少韧体（firmware）档案 | `apt install firmware-realtek` 后重新加载模组 |
| `Required key not available` | Secure Boot 开启，模组未签署 | 通过 MOK 金钥签署（请勿关闭 Secure Boot） |
| `disagrees about version of symbol` | 驅动版本與内核不符 | 重新以 DKMS 编译安装 |

> **重點理解**：`lsusb` 看得到只能證明「USB 穿透了吧」，**不代表驅动程序已加载**。常见的「穿透成功但没有 wlan」就是卡在 Guest 內部没有对应的驅动程序。

---

## 4. USB VM Filter：插上就自动挂载 + 斷线疑难

### 4.1 为什么要设 USB 過濾器（USB Filter）？

手动挂载（第二章 2.5）的問题是：**每次重开 Kali 虚拟机都要再點一次**。设定「USB 過濾器」后，只要网卡一插上（或虚拟机一开机），VirtualBox 就会**自动把符合条件的装置转进 Guest**。

设定方法（VirtualBox）：

1. 虚拟机设定 → USB → 點右邊 **「＋」新增過濾器 → 选择你的网卡装置**。
2. VirtualBox 会自动填入一笔過濾规则（含供应商 ID / 產品 ID / 序号等欄位）：
   - **名称（Name）**：例如 `ALFA AWUS036AXML` 或 `AWUS036ACH`
   - **供应商 ID（Vendor ID）**：AWUS036ACH 为 `0bda`、AWUS036AXML 为 `0e8d`
   - **產品 ID（Product ID）**：AWUS036ACH 为 `8812`、AWUS036AXML 为 `7961`
3. 若有多支同型号网卡，把「序号（Serial Number）」欄位也补上，避免過濾到另一支。

> 小技巧：過濾器上按滑鼠右键 → **编輯過濾器**，可只保留 Vendor ID 與 Product ID（寬鬆匹配）或补上序号（精准匹配）。

### 4.2 频繁斷线：通常不是网卡坏，是供电或控制器

高功率网卡（AWUS036ACH 监听／注入时瞬时电流較高；AWUS036AXML 为 USB 3 规格）在虚拟机內偶发「用一用就掉卡／斷线」的典型原因與对策：

| 现象 | 原因 | 对策 |
|------|------|------|
| 穿透后供电不足、一直掉卡 | 虚拟 USB 控制器模拟的供电能力較保守，或主机接口供电不足 | 主机端改用**主机板背板 USB 接口**或有独立供电的 USB Hub |
| 网卡一下有一下没有 | 主机的 **USB 省电（autosuspend）** 把装置睡掉了 | 在主机设定中关闭「该装置」的 USB 自动休眠（请勿关闭系统整体安全防护） |
| 挂载即失败、error code 一串 | 控制器选错（USB 1.1/2.0 撐不起 USB 3 装置） | 改选「USB 3.0 (xHCI) Controller」並关机重开 |
| 主机待命（sleep）后醒来网卡失效 | 主机睡眠时 Hypervisor 的 USB 重新导向斷裂 | 使用前避免主机待命；或喚醒后重新挂载一次 |

### 4.3 安全提醒

要降低掉卡，可关闭**单一 USB 装置**的自动休眠，但这僅限「该装置」层级。请**不要**为了省麻煩而关闭系统层级的安全性防护（防火牆、Secure Boot），那会付出不成比例的代价。

---

## 5. macOS 主机的限制與平台红线

### 5.1 macOS 主机的 USB 穿透有先天限制

从 macOS 主机跑虚拟机做 USB 穿透，是**最容易卡关的组合**，请先确認你的情況：

| macOS 主机 | VirtualBox | VMware Fusion |
|-----------|-----------|---------------|
| **Apple Silicon（M1/M2/M3/M4）** | ⚠️ **USB 穿透支持受限／不完整**，官方公告的已知限制之一；即使网卡驅动正常，穿透层也可能直接用不了 | ⚠️ 支持較完整，但仍建议先「主机直插」确認网卡在 macOS 端正常 |
| **Intel（Intel Mac）** | ✅ 可用，但需先通過**内核延伸功能（Kernel Extension）認可**流程（系统设定 → 安全性與隱私权 → 允许 Oracle 相关内核延伸功能），並安装與版本完全相符的 Extension Pack | ✅ 可用 |

**建议**：若你的主机是 macOS，優先以「主机直插 → `system_profiler SPUSBDataType` → 确認网卡在主机端正常」作为所有排障的第一关。**macOS 端不支持的型号请勿贴进虚拟机排障清单**，那会浪費大量时间。

### 5.2 平台红线（Support Boundary）

| 平台 | 支持状态 | 说明 |
|------|---------|------|
| Windows 主机 + VirtualBox / VMware + Kali Guest | ✅ 支持 | 本章所有流程皆适用 |
| Linux 主机 + VirtualBox / VMware + Kali Guest | ✅ 支持 | 記得 vboxusers 群组（VB）與 vmware-usbarbitrator 服务（VMware） |
| **macOS（Apple Silicon）** + VirtualBox | ⚠️ **USB 穿透受限** | 建议改用 VMware Fusion，或使用 Linux／Windows 主机 |
| macOS（Intel）+ VirtualBox | ✅ 支持 | 需完成内核延伸功能認可 + 版本相符的 Extension Pack |
| **Guest 为 macOS** | ❌ 不建议 | 本文以 Kali / Debian / Ubuntu 等 Linux Guest 为前提 |

> **支持邊界**：排障时请务必先确認「主机端网卡是否正常」，再談虚拟机设定的問题。若主机端本身抓不到网卡，任何虚拟机设定都救不回来——那时的下一步是主机端的驅动程序問题（可参考本站其他驅动排障文章）。

---

## 6. 标准排障工作表：報修前先跑一遍（客服 Intake）

> 遇到「虚拟机抓不到网卡」，依序完成下表，並把結果記下来。**完整跑過这份工作表，再决定要不要开技术支持单**——很多时候自己就解掉了，也大幅縮短客服来回时间。

### Step 1：主机端硬件檢查

| 檢查項 | 指令 | 記录欄 |
|-------|------|-------|
| 主机操作系统與架构 | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| 主机看得到网卡？ | 主机 `lsusb` | VID:PID \_\_\_\_\_ |
| USB 接口與线材 | 换 port、换线再试一次 | 結果 \_\_\_\_\_ |

### Step 2：虚拟化软件（Hypervisor）层檢查

| 檢查項 | 操作 | 記录欄 |
|-------|------|-------|
| 虚拟化软件與版本 | VirtualBox：`vboxmanage --version` ／ VMware：Help → About | \_\_\_\_\_ |
| 擴充套件版本相符？ | VirtualBox：`VBoxManage list extpacks` | 版本 \_\_\_\_\_ |
| 主机权限 / 服务 | Linux 主机：`id` 看是否有 vboxusers；VMware：`systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB 控制器设定 | VirtualBox：USB 3.0 (xHCI) Controller 有勾？ | 是 / 否 |

### Step 3：穿透結果檢查

| 檢查項 | 指令 | 記录欄 |
|-------|------|-------|
| Guest 看得到网卡？ | Guest 內 `lsusb` | \_\_\_\_\_ |
| 无线接口出现？ | Guest 內 `iwconfig` / `ip link` | \_\_\_\_\_ |
| 驅动层訊息 | Guest 內 `sudo dmesg \| tail -30` | \_\_\_\_\_ |
| 使用的 Guest 内核 | `uname -r` | \_\_\_\_\_ |

### Step 4：判斷與紀录

- `lsusb`（Guest）看不到 → **穿透层**問题 → 複習第二章與 Step 2。
- `lsusb` 看得到、`ip link` 没有 wlan → **驅动层**問题 → 複習第三章第 3 步。
- 都正常但不稳定 → **供电／省电／控制器**問题 → 第四章。

### 客服 Intake 信息数据包

打通技术支持电话／送出工单前，一次附上下列信息，就能让客服直接切入正题：

> **主机 OS + 架构、虚拟化软件與版本、是否安装擴充套件及版本、主机端 `lsusb` 输出、Guest 端 `lsusb` 输出、Guest 端 `ip link` / `iwconfig` 输出、`dmesg` 相关訊息、网卡型号與连接方式（USB-C / USB-A、直插或 Hub）**

---

## 7. 常见問题（FAQ）

**Q1：我换了 USB 接口結果 `lsusb` 就消失了，是网卡坏了嗎？**
不一定。先确認你插的是不是「僅充电」接口，或主机为了省电把装置休眠了。换回主机板背板的一般 USB 接口，或重新插拔一次，多半就恢復。

**Q2：VM 視窗右下角 USB 圖示是空的，怎么辦？**
依序檢查：① 擴充套件版本是否與 VirtualBox 完全相符；② Linux 主机是否在 `vboxusers` 群组（需重新登入）；③ 主机端 `lsusb` 還看不看得到网卡；④ 是否有其他软件（例如主机端驅动工具）佔用了装置。

**Q3：设定 USB 過濾器后，主机自己反而不能用网卡了？**
这是正常的。穿透给 Guest 后，装置控制权在 Guest 身上，主机端无法同时使用。要用回主机做其他事情时，先在 VM 視窗的 USB 圖示把它「退還（release）」回主机。

**Q4：Guest 內 `lsusb` 看得到，但没 wlan 接口，该装什么驅动？**
看芯片：
- **AWUS036AXML（MediaTek MT7921AU）**：内核內建 `mt7921u` 驅动，Kernel 5.18+ 即插即用；先确認 `apt install linux-firmware` 已更新。
- **AWUS036ACH（Realtek RTL8812AU）**：屬於内核外挂（out-of-tree）驅动，需安装社群维护的 `aircrack-ng/rtl8812au` 並用 DKMS 编译（並留意 Secure Boot 的 MOK 签署，请勿关闭 Secure Boot）。

**Q5：为什么选了 USB 3.0 控制器 Guest 反而进不了系统？**
少数旧版 Guest 内核对 xHCI 的支持較差。若 Kali 是較旧版本，可先试「关机 → 改回 USB 2.0 (EHCI) Controller → 开机 → 升级内核 → 再改回 USB 3.0」。尽量让 Kali 保持最新版本，xHCI 支持較完整。

**Q6：网卡在真机上很快，进虚拟机就变慢，是正常的嗎？**
是的，虚拟机內的网卡效能大致等同「通过 USB 模拟层的转介」，会比真机直插多一些损耗（overhead）；正确的 USB 3.0 (xHCI) 控制器與更新版 Hypervisor 能把损耗压到最低。若效能嚴重低落，優先确認控制器不是停在 USB 1.1。

---

## 8. 結论與硬件建议

「虚拟机抓不到外接网卡」九成以上不是硬件故障，而是**穿透设定**或**Guest 驅动**兩件事其中一件没做好。把本文的动作照順序跑完：

1. **主机端 `lsusb` 先确認硬件没問题。**
2. **VirtualBox 一定装版本相符的 Extension Pack**、Linux 主机記得加入 `vboxusers` 群组；VMware 确認 `vmware-usbarbitrator` 服务在跑。
3. **USB 控制器设为 USB 3.0 (xHCI)**，並用 USB 過濾器让网卡自动挂载。
4. **Guest 內依 `lsusb → iwconfig / ip link → dmesg` 定位层次**，缺驅动补驅动，别再猜网卡坏了。

**推薦硬件**：ALFA AWUS036AXML（MediaTek MT7921AU）在較新内核的 Kali 上**内核內建驅动、即插即用**，虚拟机穿透后最省心；ALFA AWUS036ACH（Realtek RTL8812AU）同樣堪用，但要記得在 Guest 內以 DKMS 编译社群驅动並处理 Secure Boot 签署（可参考本站关於 RTL8812AU DKMS 排障的文章）。兩者皆建议在主机端使用有独立供电的 USB 接口／Hub，把「掉卡」的变数一次排除。

**下一步**：把第六章的排障工作表存一份在你的 Kali 虚拟机桌面；每次「抓不到网卡」就先整份跑完，再决定要不要开技术支持单——照表操課，資料治百病。

---

## 参考資源

| 資源 | 连結 |
|------|------|
| Oracle VirtualBox 官方下载頁（Extension Pack） | https://www.virtualbox.org/wiki/Downloads |
| VirtualBox 官方手冊：USB 设定與過濾器 | https://www.virtualbox.org/manual/（搜尋「USB」章節） |
| VirtualBox 手冊：已知限制（含 Apple Silicon USB 穿透限制） | https://www.virtualbox.org/manual/（Changelog / Limitations） |
| VirtualBox Extension Pack 安装指令 | `vboxmanage help extpack` |
| aircrack-ng RTL8812AU 社群驅动（AWUS036ACH Guest 內使用） | https://github.com/aircrack-ng/rtl8812au |
| ALFA AWUS036ACH 官方產品頁 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036AXML 官方產品頁 | https://www.alfa.com.tw/ |
| Yupitek 技术支持 | https://yupitek.com/ |

> **合法使用声明**：在虚拟机內启用监听模式、数据包注入等資安操作，僅限於您拥有或已獲得明确授权之网络环境。用户須自行遵守所在地法律规范，並确保所有测试皆有合法授权依据。
