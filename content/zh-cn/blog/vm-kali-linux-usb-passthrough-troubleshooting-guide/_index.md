---
title: "虚拟机 Kali Linux 抓不到外接网卡？VirtualBox/VMware USB 穿透与断线诊断手册"
description: "标准化 USB 穿透排障手册：VirtualBox Extension Pack、USB 3.0 (xHCI) 控制器、vboxusers 群组、VMware USB 仲裁服务、lsusb→iwconfig→dmesg 诊断流程与 FAQ。"
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "我换了 USB 连接端口结果 lsusb 就消失了，是网卡坏了吗？"
    answer: "不一定。先确认你插的是不是「仅充电」连接端口，或主机为了省电把装置休眠了。换回主机板背板的一般 USB 连接端口，或重新插拔一次，多半就恢复。"
  - question: "VM 视窗右下角 USB 图示是空的，怎么办？"
    answer: "依序检查：① 扩充套件版本是否与 VirtualBox 完全相符；② Linux 主机是否在 vboxusers 群组（需重新登入）；③ 主机端 lsusb 还看不看得到网卡；④ 是否有其他软体（例如主机端驱动工具）占用了装置。"
  - question: "设定 USB 过滤器后，主机自己反而不能用网卡了？"
    answer: "这是正常的。穿透给 Guest 后，装置控制权在 Guest 身上，主机端无法同时使用。要用回主机做其他事情时，先在 VM 视窗的 USB 图示把它「退还（release）」回主机。"
  - question: "Guest 内 lsusb 看得到，但没 wlan 介面，该装什么驱动？"
    answer: "看晶片：AWUS036AXML（MediaTek MT7921AU）核心内建 mt7921u 驱动，Kernel 5.18+ 随插即用；先确认 apt install linux-firmware 已更新。AWUS036ACH（Realtek RTL8812AU）属于核心外挂（out-of-tree）驱动，需安装社群维护的 aircrack-ng/rtl8812au 并用 DKMS 编译（并留意 Secure Boot 的 MOK 签署，请勿关闭 Secure Boot）。"
  - question: "为什么选了 USB 3.0 控制器 Guest 反而进不了系统？"
    answer: "少数旧版 Guest 核心对 xHCI 的支援较差。若 Kali 是较旧版本，可先试「关机 → 改回 USB 2.0 (EHCI) Controller → 开机 → 升级核心 → 再改回 USB 3.0」。尽量让 Kali 保持最新版本，xHCI 支援较完整。"
  - question: "网卡在真机上很快，进虚拟机就变慢，是正常的吗？"
    answer: "是的，虚拟机内的网卡效能大致等同「透过 USB 模拟层的转送」，会比真机直插多一些损耗（overhead）；正确的 USB 3.0 (xHCI) 控制器与更新版 Hypervisor 能把损耗压到最低。若效能严重低落，优先确认控制器不是停在 USB 1.1。"
---

> **适用平台**：Windows / Linux / macOS 主机 + Oracle VirtualBox / VMware Workstation 虚拟机（Guest = Kali Linux / Debian / Ubuntu）
> **引导硬件**：ALFA AWUS036ACH（Realtek RTL8812AU）/ ALFA AWUS036AXML（MediaTek MT7921AU）
> **本篇定位**：标准化「USB 穿透（USB Pass-through）」排障诊断手册。macOS 主机的 USB 穿透限制说明见第五章。

---

{{< tldr >}}

很多 Kali 使用者把网卡插在主机上，却在虚拟机里看不到无线介面。**这种情况多半出在三个非常常见的原因**，网卡本身坏掉的机率很低：

1. **VirtualBox 没装扩充套件（Extension Pack）**：没有它，Guest 连 USB 2.0/3.0 控制器都用不了（USB 1.1 的传输速率上限仅 12 Mbps，根本不够网卡用）。
2. **USB 穿透设定没做**：主机预设「独占」所有 USB 装置，Guest 要嘛手动挂载、要嘛设定「USB 过滤器（VM USB Filter）」来自动接管网卡。
3. **Guest 内部的驱动程式没载入**：USB 层穿过去了（`lsusb` 看得到），但 Linux 没有相对应的驱动程式，所以 `ip link` 没出现 `wlan` 介面。

排障顺序：先主机端硬体、再 Guest 端穿透、最后查驱动层——完整诊断口诀见 1.3。

{{< /tldr >}}

---

## 1. 为什么虚拟机预设用不到主机的无线网卡？

### 1.1 你的 USB 网卡「同时」只属于一个作业系统

USB 的运作是**单一主控（single host）**架构：一个 USB 装置在同一个时间点，只能被一个「USB 主控制器（Host Controller）」控制。当网卡插在主机上，装置会先被**主机作业系统（Host OS）**列举（enumerate）并接管。主机的驱动程式认识它、控制它。

虚拟机（Guest VM）不是插在 USB 汇流排上的实体装置，它只是跑在主机里、由管理程式（Hypervisor）扮演出的「假硬体」。所以 Guest 想要使用 USB 网卡，**必须由主机把装置主动「移交」给 Guest**——这个机制就叫 **USB 穿透（USB Pass-through / USB Redirection）**。

### 1.2 USB 穿透到底穿透了什么？

以 VirtualBox 为例，穿透流程是这样的：

```
实体 USB 网卡（AWUS036ACH / AWUS036AXML）
       │  插在主机的 USB 实体连接埠
       ▼
主机作业系统（Host OS）的 USB 主控制器
       │  Hypervisor（VirtualBox）拦截并重新导向
       ▼
虚拟的 USB 主控制器（模拟的 EHCI / xHCI）
       │  Guest（Kali）看起来「就像插在自己身上」
       ▼
Kali 的 USB 驱动程式 → 无线网卡驱动 → wlan 介面
```

穿透成功后，这个装置在**主机端的控制权会转给 Guest**，行为上像被「拔走」，主机上无法再使用它。转而在 Guest 内变成一个全新的 USB 装置。**这是正常现象，不是 bug。** 主机的一个 USB 装置不能同时给两边用。

### 1.3 「抓不到」其实有三个层次

| 层次 | 检查工具 | 症状 | 代表意义 |
|------|---------|------|---------|
| **USB 穿透层** | Guest 内 `lsusb` | `lsusb` 完全看不到网卡的 VID:PID | 穿透失败（Extension Pack / 控制器 / 过滤器问题） |
| **驱动程式层** | Guest 内 `dmesg` | `lsusb` 看得到，但 `dmesg` 有错误（如缺韌体、`Required key not available`） | Guest 内部缺驱动程式或模组载入失败 |
| **无线介面层** | Guest 内 `iwconfig` / `ip link` | `lsusb` 与 `dmesg` 都正常，却没有 `wlan` 介面 | 驱动程式载入了但介面未注册，或模式／设定问题 |

> **判断口诀**：先看 `lsusb` 判断「装置有没有穿透进 Guest」，再看 `ip link` 判断「驱动程式有没有认识它」。**别一开始就怀疑网卡坏了。**

---

## 2. VirtualBox：先装 Extension Pack，再设 USB 3.0 控制器

### 2.1 扩充套件（Extension Pack）是非装不可的

VirtualBox 基础套件**只内建 USB 1.1（OHCI）控制器**的模拟，而 USB 1.1 的传输速率完全不夠网卡使用。**USB 2.0（EHCI）与 USB 3.0（xHCI）控制器都要靠 Oracle 官方「扩充套件（Extension Pack）」**才有。

没有装 Extension Pack 的症状很典型：Guest 设定里选不到 USB 2.0 / USB 3.0 控制器，或一挂载网卡就回报「装置连线到虚拟机失败（error code E_FAIL / VERR_PDM_NO_USB_PORTS）」。

### 2.2 版本必须「完全不差」地对上

Extension Pack 的版本**必须与 VirtualBox 主程式版本完全一致**（例如 VirtualBox 7.0.20 就要配 7.0.20 的 Extension Pack），差一个小版本都可能安装失败或载入失败。

```bash
# 查看目前 VirtualBox 版本
vboxmanage --version
```

到 Oracle 官方下载页（https://www.virtualbox.org/wiki/Downloads）下载对应版本的
`Oracle_VM_VirtualBox_Extension_Pack-<版本>.vbox-extpack`，然后：

```bash
# 方式一：GUI 安装（VirtualBox 主程式 → 档案 → 工具 → Extension Pack Manager → 安装）
# 方式二：指令安装
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# 确认已安装
VBoxManage list extpacks
```

> 安装时会显示 Oracle 授权（Personal Use and Evaluation License）；个人使用免费，商用环境请依授权内容办理。

### 2.3 Linux 主机：把自己加入 vboxusers 群组

在 Linux 主机上，VirtualBox 要存取 USB 装置，**需要使用者属于 `vboxusers` 群组**。很多人安装了扩充套件却还是失败，就是卡在权限。

```bash
# 加入群组（以你的使用者名称取代 <user>）
sudo usermod -aG vboxusers $USER

# 登出再登入（或重新开机）让群组生效；确认群组已生效
id $USER
```

### 2.4 设定 USB 3.0（xHCI）控制器

1. 选取你的 Kali 虚拟机 → **设定（Settings）→ 连接埠（Ports）→ USB**。
2. 勾选「Enable USB Controller」，并选择 **USB 3.0 (xHCI) Controller**。
   - AWUS036AXML 是 USB 3.2 Gen 1（USB-C）规格，**务必选 USB 3.0 (xHCI)**，选 USB 2.0 会限制传输速率。
   - AWUS036ACH 为 USB Type-A 介面，在 USB 2.0 与 USB 3.0 控制器下皆可使用；若要较佳传输速率，一样选 USB 3.0 (xHCI)。
3. 修改控制器后**关机再开机**（不是在 Guest 内执行 reboot）才能套用变更。

### 2.5 手动挂载与 VMware 对照

开启 Kali 虚拟机后，注意视窗**右下角的 USB 图示**（一支 USB 插头）：

1. 点 USB 图示 → 会列出目前插在主机上的 USB 装置。
2. 你的网卡应该显示类似 `Realtek 802.11ac NIC`（ACH），或 `ALFA AWUS036AXML` / MediaTek（AXML）。
3. 点它一下，装置就会「移交」给 Kali。

如果清单是空的，代表穿透层出了问题——回去 2.2 / 2.3 / 2.4 检查（含 USB 控制器未启用），或直接跑第六章排障工作表。

**VMware 对照**：VMware Workstation / Fusion **不需要**额外扩充套件就有 USB 穿透功能，但有两个常见检查点：

1. **主机端服务**：Linux 主机上请确认 `vmware-usbarbitrator`（USB 仲裁服务）有在跑：
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # 如果没在跑，启动并设为开机自动执行
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **虚拟机设定**：虚拟机设定 → USB Controller → 勾选 **USB 3.1（或 USB 3.0）**。
3. **手动连线**：VMware 视窗选单 → **可移除装置（Removable Devices）→ 你的网卡 → 连线（Connect）**。

> **对照重点**：VirtualBox 卡在「没装扩充套件」；VMware 卡在「仲裁服务没跑」或「控制器 USB 3.0 没开」。先确认你用的是哪家，再对号入座。

---

## 3. 诊断工具三步骤：lsusb → iwconfig → dmesg

穿透设定做完后，用三个指令把问题定位到「穿透层」还是「驱动层」。

### 第 0 步：主机端先确认硬体正常（别把问题赖给网卡）

在**主机作业系统**开终端机执行：

```bash
lsusb
```

预期看到（依型号）：

```
# AWUS036ACH（Realtek RTL8812AU）
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# 或 AWUS036AXML（MediaTek MT7921AU）
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- 主机看得到 → 硬体与线材正常，问题在穿透或 Guest 驱动。
- 主机也看不到 → **先检查主机端**（换 USB 连接埠、换线、另一台主机交叉测试），再考虑开技术支援单。

### 第 1 步：Guest 端 lsusb——穿透成功没有？

在 **Kali 虚拟机内**执行：

```bash
lsusb
```

- 看得到同样的 VID:PID → **穿透成功**，跳到第 2 步。
- 看不到 → **穿透失败**，回去检查第二章（Extension Pack / 控制器 / vboxusers 群组），或确认网卡是否被主机的其他软体占用。

### 第 2 步：iwconfig / ip link——无线介面出现没有？

```bash
iwconfig
# 或（较新版本）
iw dev
ip link
```

- 出现 `wlan0` / `wlx...` 介面 → **全部打通**，可以开始使用了。
- 没有无线介面但 `lsusb` 看得到 → 问题在 **Guest 的驱动程式层**，看第 3 步。

### 第 3 步：dmesg——驱动层为什么失败？

```bash
# 观察核心刚才的讯息
sudo dmesg | tail -30
# 过滤 USB 与无线相关的讯息
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

常见的 `dmesg` 结果对照：

| `dmesg` 讯息 | 原因 | 处理方式 |
|-------------|------|---------|
| `usb 3-1: new high-speed USB device ...` 之后没有后续 | 装置列举完成，但没有可用的驱动程式 | Guest 内安装对应驱动程式（见 FAQ Q4） |
| `Direct firmware load failed` / `firmware_loading` | 缺少韌体（firmware）档案 | `apt install firmware-realtek` 后重新载入模组 |
| `Required key not available` | Secure Boot 开启，模组未签署 | 透过 MOK 金钥签署（请勿关闭 Secure Boot） |
| `disagrees about version of symbol` | 驱动版本与核心不符 | 重新以 DKMS 编译安装 |

> **重点理解**：`lsusb` 看得到只能证明「USB 穿透了吧」，**不代表驱动程式已载入**。常见的「穿透成功但没有 wlan」就是卡在 Guest 内部没有对应的驱动程式。

---

## 4. USB VM Filter：插上就自动挂载 + 断线疑难

### 4.1 为什么要设 USB 过滤器（USB Filter）？

手动挂载（第二章 2.5）的问题是：**每次重开 Kali 虚拟机都要再点一次**。设定「USB 过滤器」后，只要网卡一插上（或虚拟机一开机），VirtualBox 就会**自动把符合条件的装置转进 Guest**。

设定方法（VirtualBox）：

1. 虚拟机设定 → USB → 点右边 **「＋」新增过滤器 → 选择你的网卡装置**。
2. VirtualBox 会自动填入一笔过滤规则（含供应商 ID / 产品 ID / 序号等栏位）：
   - **名称（Name）**：例如 `ALFA AWUS036AXML` 或 `AWUS036ACH`
   - **供应商 ID（Vendor ID）**：AWUS036ACH 为 `0bda`、AWUS036AXML 为 `0e8d`
   - **产品 ID（Product ID）**：AWUS036ACH 为 `8812`、AWUS036AXML 为 `7961`
3. 若有多支同型号网卡，把「序号（Serial Number）」栏位也补上，避免过滤到另一支。

> 小技巧：过滤器上按滑鼠右键 → **编辑过滤器**，可只保留 Vendor ID 与 Product ID（宽松匹配）或补上序号（精准匹配）。

### 4.2 频繁断线：多半是供电或控制器问题

高功率网卡（AWUS036ACH 监听／注入时瞬时电流较高；AWUS036AXML 为 USB 3 规格）在虚拟机内偶发「用一用就掉卡／断线」。以下是典型原因与对策：

| 现象 | 原因 | 对策 |
|------|------|------|
| 穿透后供电不足、一直掉卡 | 虚拟 USB 控制器模拟的供电能力较保守，或主机连接埠供电不足 | 主机端改用**主机板背板 USB 连接埠**或有独立供电的 USB Hub |
| 网卡一下有一下没有 | 主机的 **USB 省电（autosuspend）** 把装置睡掉了 | 在主机设定中关闭「该装置」的 USB 自动休眠（请勿关闭系统整体安全防护） |
| 挂载即失败、error code 一串 | 控制器选错（USB 1.1/2.0 撑不起 USB 3 装置） | 改选「USB 3.0 (xHCI) Controller」并关机重开 |
| 主机待命（sleep）后醒来网卡失效 | 主机睡眠时 Hypervisor 的 USB 重新导向断裂 | 使用前避免主机待命；或唤醒后重新挂载一次 |

### 4.3 安全提醒

要降低掉卡，可关闭**单一 USB 装置**的自动休眠，但这仅限「该装置」层级。请**不要**为了省麻烦而关闭系统层级的安全性防护（防火墙、Secure Boot），那会付出不成比例的代价。

---

## 5. macOS 主机的限制与平台红线

### 5.1 macOS 主机的 USB 穿透有先天限制

从 macOS 主机跑虚拟机做 USB 穿透，是**最容易卡关的组合**，请先确认你的情况：

| macOS 主机 | VirtualBox | VMware Fusion |
|-----------|-----------|---------------|
| **Apple Silicon（M1/M2/M3/M4）** | ⚠️ **USB 穿透支援受限／不完整**，官方公告的已知限制之一；即使网卡驱动正常，穿透层也可能直接用不了 | ⚠️ 支援较完整，但仍建议先「主机直插」确认网卡在 macOS 端正常 |
| **Intel（Intel Mac）** | ✅ 可用，但需先通过**核心延伸功能（Kernel Extension）认可**流程（系统设定 → 安全性与隐私权 → 允许 Oracle 相关核心延伸功能），并安装与版本完全相符的 Extension Pack | ✅ 可用 |

**建议**：若你的主机是 macOS，优先以「主机直插 → `system_profiler SPUSBDataType` → 确认网卡在主机端正常」作为所有排障的第一关。**macOS 端不支援的型号请勿贴进虚拟机排障清单**，那会浪费大量时间。

### 5.2 平台红线（Support Boundary）

| 平台 | 支援状态 | 说明 |
|------|---------|------|
| Windows 主机 + VirtualBox / VMware + Kali Guest | ✅ 支援 | 本章所有流程皆适用 |
| Linux 主机 + VirtualBox / VMware + Kali Guest | ✅ 支援 | 记得 vboxusers 群组（VB）与 vmware-usbarbitrator 服务（VMware） |
| **macOS（Apple Silicon）** + VirtualBox | ⚠️ **USB 穿透受限** | 建议改用 VMware Fusion，或使用 Linux／Windows 主机 |
| macOS（Intel）+ VirtualBox | ✅ 支援 | 需完成核心延伸功能认可 + 版本相符的 Extension Pack |
| **Guest 为 macOS** | ❌ 不建议 | 本文以 Kali / Debian / Ubuntu 等 Linux Guest 为前提 |

> **支援边界**：排障时请务必先确认「主机端网卡是否正常」，再谈虚拟机设定的问题。若主机端本身抓不到网卡，任何虚拟机设定都救不回来——那时的下一步是主机端的驱动程式问题（可参考本站其他驱动排障文章）。

---

## 6. 标准排障工作表：报修前先跑一遍（客服 Intake）

> 遇到「虚拟机抓不到网卡」，依序完成下表，并把结果记下来。**完整跑过这份工作表，再决定要不要开技术支援单**——很多时候自己就解掉了，也大幅缩短客服来回时间。

### Step 1：主机端硬体检查

| 检查项 | 指令 | 记录栏 |
|-------|------|-------|
| 主机作业系统与架构 | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| 主机看得到网卡？ | 主机 `lsusb` | VID:PID \_\_\_\_\_ |
| USB 连接埠与线材 | 换 port、换线再试一次 | 结果 \_\_\_\_\_ |

### Step 2：虚拟化软体（Hypervisor）层检查

| 检查项 | 操作 | 记录栏 |
|-------|------|-------|
| 虚拟化软体与版本 | VirtualBox：`vboxmanage --version` ／ VMware：Help → About | \_\_\_\_\_ |
| 扩充套件版本相符？ | VirtualBox：`VBoxManage list extpacks` | 版本 \_\_\_\_\_ |
| 主机权限 / 服务 | Linux 主机：`id` 看是否有 vboxusers；VMware：`systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB 控制器设定 | VirtualBox：USB 3.0 (xHCI) Controller 有勾？ | 是 / 否 |

### Step 3：穿透结果检查

| 检查项 | 指令 | 记录栏 |
|-------|------|-------|
| Guest 看得到网卡？ | Guest 内 `lsusb` | \_\_\_\_\_ |
| 无线介面出现？ | Guest 内 `iwconfig` / `ip link` | \_\_\_\_\_ |
| 驱动层讯息 | Guest 内 `sudo dmesg \| tail -30` | \_\_\_\_\_ |
| 使用的 Guest 核心 | `uname -r` | \_\_\_\_\_ |

### Step 4：判断与纪录

- `lsusb`（Guest）看不到 → **穿透层**问题 → 复习第二章与 Step 2。
- `lsusb` 看得到、`ip link` 没有 wlan → **驱动层**问题 → 复习第三章第 3 步。
- 都正常但不稳定 → **供电／省电／控制器**问题 → 第四章。

### 客服 Intake 资讯封包

打通技术支援电话／送出工单前，一次附上下列资讯，就能让客服直接切入正题：

> **主机 OS + 架构、虚拟化软体与版本、是否安装扩充套件及版本、主机端 `lsusb` 输出、Guest 端 `lsusb` 输出、Guest 端 `ip link` / `iwconfig` 输出、`dmesg` 相关讯息、网卡型号与连接方式（USB-C / USB-A、直插或 Hub）**

---

## 7. 常见问题（FAQ）

**Q1：我换了 USB 连接端口结果 `lsusb` 就消失了，是网卡坏了吗？**
不一定。先确认你插的是不是「仅充电」连接端口，或主机为了省电把装置休眠了。换回主机板背板的一般 USB 连接端口，或重新插拔一次，多半就恢复。

**Q2：VM 视窗右下角 USB 图示是空的，怎么办？**
依序检查：① 扩充套件版本是否与 VirtualBox 完全相符；② Linux 主机是否在 `vboxusers` 群组（需重新登入）；③ 主机端 `lsusb` 还看不看得到网卡；④ 是否有其他软体（例如主机端驱动工具）占用了装置。

**Q3：设定 USB 过滤器后，主机自己反而不能用网卡了？**
这是正常的。穿透给 Guest 后，装置控制权在 Guest 身上，主机端无法同时使用。要用回主机做其他事情时，先在 VM 视窗的 USB 图示把它「退还（release）」回主机。

**Q4：Guest 内 `lsusb` 看得到，但没 wlan 介面，该装什么驱动？**
看晶片：
- **AWUS036AXML（MediaTek MT7921AU）**：核心内建 `mt7921u` 驱动，Kernel 5.18+ 随插即用；先确认 `apt install linux-firmware` 已更新。
- **AWUS036ACH（Realtek RTL8812AU）**：属于核心外挂（out-of-tree）驱动，需安装社群维护的 `aircrack-ng/rtl8812au` 并用 DKMS 编译（并留意 Secure Boot 的 MOK 签署，请勿关闭 Secure Boot）。

**Q5：为什么选了 USB 3.0 控制器 Guest 反而进不了系统？**
少数旧版 Guest 核心对 xHCI 的支援较差。若 Kali 是较旧版本，可先试「关机 → 改回 USB 2.0 (EHCI) Controller → 开机 → 升级核心 → 再改回 USB 3.0」。尽量让 Kali 保持最新版本，xHCI 支援较完整。

**Q6：网卡在真机上很快，进虚拟机就变慢，是正常的吗？**
是的，虚拟机内的网卡效能大致等同「透过 USB 模拟层的转送」，会比真机直插多一些损耗（overhead）；正确的 USB 3.0 (xHCI) 控制器与更新版 Hypervisor 能把损耗压到最低。若效能严重低落，优先确认控制器不是停在 USB 1.1。

---

## 8. 结论与硬体建议

「虚拟机抓不到外接网卡」九成以上是**穿透设定**或**Guest 驱动**没做好，硬体故障反而少见。把本文的动作照顺序跑完：

1. **主机端 `lsusb` 先确认硬体没问题。**
2. **VirtualBox 一定装版本相符的 Extension Pack**、Linux 主机记得加入 `vboxusers` 群组；VMware 确认 `vmware-usbarbitrator` 服务在跑。
3. **USB 控制器设为 USB 3.0 (xHCI)**，并用 USB 过滤器让网卡自动挂载。
4. **Guest 内依 `lsusb → iwconfig / ip link → dmesg` 定位层次**，缺驱动补驱动，别再猜网卡坏了。

**推荐硬体**：ALFA AWUS036AXML（MediaTek MT7921AU）在较新核心的 Kali 上**核心内建驱动、随插即用**，虚拟机穿透后最省心。ALFA AWUS036ACH（Realtek RTL8812AU）同样堪用，但要记得在 Guest 内以 DKMS 编译社群驱动并处理 Secure Boot 签署（可参考本站关于 RTL8812AU DKMS 排障的文章）。两者皆建议在主机端使用有独立供电的 USB 连接埠／Hub，把「掉卡」的变数一次排除。

**下一步**：把第六章的排障工作表存一份在你的 Kali 虚拟机桌面；每次「抓不到网卡」就先整份跑完，再决定要不要开技术支援单——照表操课，资料治百病。

---

## 参考资源

| 资源 | 连结 |
|------|------|
| Oracle VirtualBox 官方下载页（Extension Pack） | https://www.virtualbox.org/wiki/Downloads |
| VirtualBox 官方手册：USB 设定与过滤器 | https://www.virtualbox.org/manual/（搜寻「USB」章节） |
| VirtualBox 手册：已知限制（含 Apple Silicon USB 穿透限制） | https://www.virtualbox.org/manual/（Changelog / Limitations） |
| VirtualBox Extension Pack 安装指令 | `vboxmanage help extpack` |
| aircrack-ng RTL8812AU 社群驱动（AWUS036ACH Guest 内使用） | https://github.com/aircrack-ng/rtl8812au |
| ALFA AWUS036ACH 官方产品页 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036AXML 官方产品页 | https://www.alfa.com.tw/ |
| Yupitek 技术支援 | https://yupitek.com/ |

> **合法使用声明**：在虚拟机内启用监听模式、封包注入等资安操作，仅限於您拥有或已获得明确授权之网路环境。使用者须自行遵守所在地法律规范，并确保所有测试皆有合法授权依据。