---
title: "ALFA AWUS036EACS 单卡实测：RTL8821CU（BT + WiFi 复合）在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・端到端 handshake"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS（蓝牙+Wi-Fi 复合）在 Ubuntu 24.04 ARM64 实测：免装驱动，两频注入 100%、Monitor、AP、WPA3-SAE，端到端 handshake（79 ACKs、.22000）通过。附 USB 重插风险。平台 ASUS GX10、RTL8821CU。"
faq:
  - question: "AWUS036EACS 在 Ubuntu 24.04 ARM64 要装驱动吗？"
    answer: "在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8821CU 由内置 rtw88_8821cu 驱动，插上即辨识，免编译、免 DKMS；接口名称为 wlx 加 MAC，重插后不变。"
  - question: "AWUS036EACS 的 monitor mode 与数据包注入表现如何？"
    answer: "monitor 在 2.4G、5G 都稳，多数频道收满 300 frames；aireplay-ng --test 两频皆 30/30（100%）。5G 注入前需 iw reg set US 解除 TW 对 TX 的限制。"
  - question: "AWUS036EACS 能截取 WPA handshake 吗？"
    answer: "能。自有 AP 加自有 iPhone 7 Plus 端到端实测：deauth 收到 79 ACKs，截取完整 M1–M4，hcxpcapngtool --all 转出 .22000（784 bytes、2 组 EAPOL pairs）。仅限自有或已授权网络。"
  - question: "AWUS036EACS 插上后 lsusb 看得到、却没有 wlx 网络接口怎么办？"
    answer: "这是 BT+Wi-Fi 复合设备的 probe 竞态：蓝牙已绑 btusb，Wi-Fi 的 rtw88_8821cu 卡住。实测重载模块、手动 bind 多半无效，可靠解法是拔卡后换另一个 USB 孔重插。"
  - question: "AWUS036EACS 支持 mesh、IBSS 或 hcxdumptool 吗？"
    answer: "不支持。rtw88 的 active-monitor、IBSS、mesh、P2P 回 -95 或 join 无效；hcxdumptool 8.x 仅在 2.4 GHz 可 arm（5 GHz 会 failed to arm），请改用 airodump-ng + aireplay-ng。VHT 仅 80 MHz。要 mesh / IBSS 请选 AWUS036ACM / ACHM。"
draft: false
---

> 测试单位：Yopitek（ALFA Network 台湾经销）｜测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜测试设备：自有 iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）｜测试对象：自有办公室 Wi-Fi（SSID YUPITEK，2.4G ch5 / 5G ch36、157）。
>
> 本文为 AWUS036EACS 单卡的能力与兼容性实测。所有 Monitor / Injection / handshake 截取，均于 Yopitek 自有设备、自有办公室 Wi-Fi、对自有测试手机进行，属经销商对硬件的正当能力验证；不针对任何第三方网络，亦不提供攻击操作步骤。

**重点摘要（TL;DR）**：AWUS036EACS 在 GX10 / Ubuntu 24.04（kernel 6.17）免装驱动；两频注入 100%，端到端 .22000 通过（79 ACKs）；BT+Wi-Fi 复合卡须留意重插。

## 1. 这张卡与测试平台

AWUS036EACS 是 ALFA 的轻量随身型 Wi-Fi 5（802.11ac）USB 网卡，芯片是 Realtek RTL8821CU，1x1 单串流、2.4GHz 与 5GHz 双频，还内置蓝牙，属于 BT + WiFi 复合设备。这篇把它单独搬上 Yopitek 的实验桌，在 ASUS GX10（ARM64）配 Ubuntu 24.04 的环境逐项验收，回答客户最在意的几个问题：驱动在 ARM64 上认不认、能进哪些模式、性能到哪里。

先把定位讲清楚。这是经销商对自家货的兼容性与能力边界验证，不是攻击教学。文中所有 injection 与 handshake 相关的能力量测，一律在自有封闭环境、对自有设备进行，不提供任何对外部网络的操作步骤。

测试平台与方法比照本批其他单卡文：

- 运算平台：ASUS GX10（ARM64 / aarch64）
- 操作系统：Ubuntu 24.04 LTS，kernel 6.17.0-1014-nvidia
- 驱动策略：使用 kernel 内置（in-kernel）驱动，插上即辨识，不装任何第三方 DKMS 模块
- 测试设备：Apple iPhone 7 Plus（WPA3-SAE 另以 iPhone 15 Pro 复测）
- 测试环境：自有办公室 Wi-Fi，SSID YUPITEK，2.4GHz ch5 / 5GHz ch36、ch157
- 安全守则：全程只操作 `wlx*` 接口，不碰内置对外上网主线；绝不运行 `airmon-ng check kill`（会关掉 NetworkManager 使 GX10 对外断线）

## 2. 硬件与驱动：BT + WiFi 复合设备的真相

先看底细。下表是 AWUS036EACS 在 kernel 6.17 上实际挂载的状态：

| 项目 | 内容 |
|---|---|
| 芯片 | Realtek RTL8821CU（1x1 单串流） |
| 世代 | Wi-Fi 5（802.11ac），2.4 + 5GHz |
| 复合功能 | BT + WiFi 复合设备（内含蓝牙） |
| USB ID | `0bda:c820` |
| 驱动 | `rtw88_8821cu`（in-kernel，kernel 6.2 起支持 USB） |
| 固件 | 24.11.0（H2C version 12，实测 dmesg） |
| VHT 带宽 | 仅 80MHz（无 160 / 80+80） |

以 `iw phy` 查找，支持的 interface mode 为 `managed` / `AP` / `AP/VLAN` / `monitor`（`IBSS` 有列出但实测 join 无效）；频段涵盖 2.4GHz ch1–13 与 5GHz ch36–165（其中 ch52–144 为 DFS 频段）；cipher 含 CCMP-256、GCMP-128 / GCMP-256 与 CMAC，具备在 AP 端跑 WPA3 的条件。

驱动部分没有悬念。RTL8821CU 的 USB 支持自 kernel 6.2 并入主线 `rtw88`，GX10 的 kernel 6.17 已内置 `rtw88_8821cu`，插上即加载，不需要编译或 DKMS。早期 in-kernel 版本的 AP mode 曾有 bug，已由 macid patch（linux-next-20240911 起）修复，本次 kernel 6.17 上的 AP 三模式实测皆正常收尾。确认方式：

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Wi-Fi 接口加载后会以 `wlx` + MAC 命名（例如 `wlx00c0cab3a52e`），而非 `wlan0`；重插后名称不变，写脚本时可稳定引用。

真正要留意的是「复合设备」这件事。用 `lsusb -t` 查看，会看到同一颗 RTL8821CU 底下挂了多个 USB interface：蓝牙功能绑 `btusb`，Wi-Fi 功能另外绑 `rtw88_8821cu`。

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- 蓝牙
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- 蓝牙
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

（Bus／Port 编号会随插拔次数改变；重点是 interface 0/1 走 `btusb`、interface 2 才是 Wi-Fi 的 `rtw88_8821cu`。）

**BT + WiFi 复合设备的重插风险（部署前必读）。** 因为蓝牙与 Wi-Fi 共用同一个 USB 设备，在某些 USB 孔或快速重插的情况下，可能发生蓝牙已经绑上 `btusb`、但 Wi-Fi 那个 interface 的 probe 卡住，结果 `lsusb` 看得到 `0bda:c820`、却生不出 `wlx` 接口的竞态。实测中，`modprobe -r` 后重载、或手动 `bind` 多半无效（`bind` 会回 `Operation already in progress`）。可靠解法只有一个：拔卡、换一个 USB 孔重插，换孔后枚举干净、`wlx` 接口即正常出现。这是这张卡相较于非复合的 AWUS036ACS（RTL8811AU）额外要知道的操作细节，先知道就不会误判成卡片故障。

## 3. 实测能力：Monitor / Injection / AP / WPA3

下表是 AWUS036EACS 的核心能力实测摘要，每条均于 2026-11-18 在 GX10 实机运行：

| 能力项目 | 2.4GHz | 5GHz | 实测重点 |
|---|---|---|---|
| Monitor | ✅ 强 | ✅ 强 | 多数频道满额 300 frames；社区 #453「ch1 卡死」未重现 |
| Injection | ✅ 100%（30/30） | ✅ 100%（30/30） | Power 2.4G -38.27 / 5G -76.10；本批 ac 卡注入最强 |
| AP 热点 | ✅ 干净收尾 | ✅ VHT 80MHz | `hostapd` 建站，iPhone 7 Plus 连入并完成 4-way |
| WPA3-SAE（AP 端） | ✅ iPhone 连入 | 未实测 | SAE-only + 强制 PMF（`ieee80211w=2`、`sae_pwe=0`） |
| WPA handshake 截取 | — | ✅ 端到端 | M1–M4 完整，deauth 收 79 ACKs，转出 `.22000` |

Monitor（监听模式）在 2.4 与 5GHz 都稳。六个频道逐一截取，多数都收到满额 300 frames。对 8821cu 来说，这里还有一个很重要的正面结果：rtw88 社区长期追踪的 GitHub #453「8821cu 在 kernel ≥6.9、STA up 时 monitor 卡在 ch1」，在 GX10 这个环境并未重现，5GHz 的 ch36、ch149、ch157 都能稳定收满 300 帧。要跨 2.4 / 5GHz 做频谱勘查或数据包解析，这张卡的 monitor 可以放心用。

Injection（数据包注入）的表现最亮眼。以 `aireplay-ng --test` 量测，2.4GHz 与 5GHz 都是 30/30、100%，是本批 ac 卡里注入最强的一张（同为 1x1 的 AWUS036ACS 在 5G 只有 96%）。这里有个台湾在地的细节：5GHz 的 TX 在 regulatory domain 设为 TW 时会被锁，量测前先 `iw reg set US` 解锁，测完再 `iw reg set TW` 还原。

AP 热点这边，以 `hostapd` 分别架 2.4GHz（WPA2）、5GHz（VHT 80MHz）、WPA3-SAE 三种，iPhone 7 Plus 都能连入并完成 4-way handshake，关站也收尾干净（`AP-DISABLED` / `TERMINATING`）。没有出现某些卡会有的 beacon re-key 问题，2.4G 这点比姊妹卡 ACS 更稳。WPA3 采 SAE-only 搭配强制 PMF（`ieee80211w=2`、`sae_pwe=0`），以 iPhone 15 Pro 成功连入，确认 RTL8821CU 在 AP 端的 WPA3-SAE 可用。

Kali 工具链（平台层）在这张卡上也都带得起来：`airmon-ng` 侦测得到 EACS（`rtw88_8821cu`），但一样不要用 `check kill`；`kismet` 以本卡当 data source 启动成功，实测产出约 733 KB 的 `.kismet` log；`bettercap` 2.32 的 `wifi.recon on` 正常运作（txpower 警告可忽略）；`wifite`（git 3.0.0）扫到 10 台以上 AP、含自家 YUPITEK（ch5、PWR 84），这一版没有 `--band` 旗标，要改用 `-c 1,6,11,36,149,157` 指定频道；`Wireshark` / `tshark` 4.x 在 monitor ch6 实截取并解析 325 frames；`macchanger` 的随机 MAC 伪装也能用。工具层这一段跟本批其他卡一致，差异主要落在前面的 injection 与 monitor 硬件能力。

## 4. 端到端 handshake：亮点与诚实限制

这张卡的亮点能力，是把 injection 与 capture 串成一条完整可用的链。在自家 YUPITEK AP 与自有 iPhone 7 Plus 之间，整条链实机跑通：对自有 iPhone 送出 deauth（injection，实测收到 79 个 ACKs，证实注入数据包确实到达 client）→ iPhone 重新连接时收齐完整的 4-way handshake（握手，M1、M2、M3、M4 各 1）→ 以 `hcxpcapngtool --all` 转出 hashcat 格式的 `.22000`（784 bytes，2 组 EAPOL pairs，RC checked）。整个流程只为验证卡片能力，对象全程是自家 AP 与自有手机，不涉及任何第三方网络。

实务上两个关键细节值得记下：办公室同时有多台同名 YUPITEK AP 在 ch36，截取时不要锁 `--bssid`，直接收整个频道，才不会把 iPhone 实际连的那台滤掉；另外 `hcxpcapngtool` 默认较严格，要加 `--all` 才转得出 `.22000`。

诚实限制也要一次讲清楚：

- **不支持 active-monitor / IBSS（Ad-hoc）/ Mesh（802.11s）/ Wi-Fi Direct（P2P）。** 这些模式在 `rtw88` 下回 `-95`（Operation not supported），或列得出来但 join 无效，属驱动层限制，无解。需要 mesh / IBSS 实验的客户应改走 MediaTek 的 AWUS036ACM / ACHM。
- **`hcxdumptool` 8.x 受限。** 它需要 active-monitor；本卡仅在 2.4 GHz 可 arm，5 GHz 会 `failed to arm`（同批其余卡皆 `failed to arm interface`）；改用 `airodump-ng` + `aireplay-ng` 即可，本卡注入 100%，不受影响。
- **VHT 仅 80MHz。** 单串流、无 160MHz 或 80+80，定位就是轻量随身卡，不是冲吞吐的角色。
- **VIF 为部分支持。** 仅支持被动 monitor 接口与 managed 接口在同一频道并存（software monitor，实测 100 frames）；不支持独立的双 VIF。

## 5. 适用情境与选型

综合实测，AWUS036EACS 的定位很清楚：需要双频 Monitor + Injection + 端到端 handshake 验证，又想要一张轻巧、内置蓝牙的随身卡，它就是合适解。两频注入 100% 与干净的 AP / WPA3 表现，让它在授权范围内的无线审核与资安教学用途上，和 AWUS036ACH、AWUS036ACS 同列首选群。

什么情况建议改选别张：

- **现场会频繁重插、或机箱 USB 孔品质参差** → 复合设备的 probe 竞态会增加困扰，可考虑非复合的 AWUS036ACS（RTL8811AU，同为 1x1 ac，少了蓝牙那层变量）。
- **要做 mesh / IBSS 实验** → `rtw88` 不支持，改用 MediaTek 的 AWUS036ACM / ACHM。
- **追求最强接收或长距离 monitor** → 双天线的 AWUS036ACH 或 Wi-Fi 6 的 AWUS036AXER 更合适。
- **避雷**：若用途是 injection / handshake，不要选 MT7921 的 AWUS036AXM / AXML，注入在本平台直接失败。

想一次看完 9 款 ALFA 卡的 Monitor / Injection / AP / WPA3 横向对照与完整选型矩阵，请回到总表：[2026 最完整实测：9 款 ALFA 无线网卡在 ASUS GX10 的全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常见问题（FAQ）

**Q：AWUS036EACS 在 Ubuntu 24.04 ARM64 要装驱动吗？**
在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8821CU 由内置 rtw88_8821cu 驱动，插上即辨识，免编译、免 DKMS；接口名称为 wlx 加 MAC，重插后不变。

**Q：AWUS036EACS 的 monitor mode（监听模式）与数据包注入表现如何？**
monitor 在 2.4G、5G 都稳，多数频道收满 300 frames；`aireplay-ng --test` 两频皆 30/30（100%）。5G 注入前需 `iw reg set US` 解除 TW 对 TX 的限制。

**Q：AWUS036EACS 能截取 WPA handshake（握手数据包）吗？**
能。自有 AP 加自有 iPhone 7 Plus 端到端实测：deauth 收到 79 ACKs，截取完整 M1–M4，`hcxpcapngtool --all` 转出 .22000（784 bytes、2 组 EAPOL pairs）。仅限自有或已授权网络。

**Q：AWUS036EACS 插上后 lsusb 看得到、却没有 wlx 网络接口怎么办？**
这是 BT+Wi-Fi 复合设备的 probe 竞态：蓝牙已绑 btusb，Wi-Fi 的 rtw88_8821cu 卡住。实测重载模块、手动 bind 多半无效，可靠解法是拔卡后换另一个 USB 孔重插。

**Q：AWUS036EACS 支持 mesh、IBSS 或 hcxdumptool 吗？**
不支持。rtw88 的 active-monitor、IBSS、mesh、P2P 回 -95 或 join 无效；hcxdumptool 8.x 仅在 2.4 GHz 可 arm（5 GHz 会 failed to arm），请改用 airodump-ng + aireplay-ng。VHT 仅 80 MHz。要 mesh / IBSS 请选 AWUS036ACM / ACHM。

---

## 6. 延伸阅读

- [2026 最完整实测：9 款 ALFA 无线网卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)（Hub 总表）
- [WPA3-SAE 时代的无线审核：9 款 ALFA 卡 handshake 截取能力实测](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [免装驱动：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驱动激活 ALFA 网卡 Monitor 与 AP 模式](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 同属 rtw88 USB ac 卡 → [AWUS036ACS 单卡实测报告（RTL8811AU）](/zh-cn/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*测试单位：Yopitek（ALFA Network 台湾经销）— https://www.yupitek.com*
