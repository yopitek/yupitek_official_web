---
title: "AWUS036ACHM 逐卡实测：MediaTek MT7610U 单天线 AC600 在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・WPA3 能力"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM（MT7610U）在 Ubuntu 24.04 免装驱动，双频监听模式可用、2.4G 数据包注入 96–100%；开 AP 须关 802.11n，WPA3 须设 sae_pwe=0 旧 iPhone 才连得上。"
faq:
  - question: "AWUS036ACHM 在 Ubuntu 24.04 需要装驱动吗？"
    answer: "不需要。MT7610U 由 kernel 内置的 mt76x0u 驱动接管，Ubuntu 24.04（kernel 6.17）插上即认，不用 DKMS、不用额外固件；lsusb 可看到 USB ID 0e8d:7610。"
  - question: "AWUS036ACHM 能进 monitor mode 吗？能扫到多少 AP？"
    answer: "能。2.4GHz 与 5GHz 都能进 monitor mode；用 airodump-ng 跳频全频扫描 120 秒，实测扫到 19 个 AP、14 个用户端，分布在 ch1、2、5、6、36、149、157。"
  - question: "AWUS036ACHM 的数据包注入成功率多少？5GHz 可以吗？"
    answer: "2.4GHz 第 6 频道逐台注入回应率 96–100%（aireplay-ng --test，找到 4 台 AP）。5GHz（ch36、ch149）只验到广播注入可用，逐台测试回报 Found 0 APs，本次没有取得百分比，原因待查。"
  - question: "AWUS036ACHM 开 AP 时 iPhone 显示「无法加入网络」或「密码错误」怎么办？"
    answer: "先关掉 802.11n：hostapd 设置档不要加 ieee80211n=1 与 ht_capab，2.4GHz 用纯 hw_mode=g、5GHz 用纯 hw_mode=a（20 MHz）。否则 hostapd 会反复出现 handle_assoc_cb: STA not found，画面像密码错误，其实是 802.11n 关联失败。"
  - question: "AWUS036ACHM 的 WPA3-SAE 为什么旧 iPhone 连不上？"
    answer: "多半是 hostapd 的 sae_pwe 设置。实测 sae_pwe=0 时 iPhone 7 Plus 与 iPhone 15 Pro 都连得上；sae_pwe=2 时 iPhone 7 Plus 会关联成功但 4-way 交握失败而断线，看起来像密码错误。请搭配 ieee80211w=2，改完设置后让 iPhone 先忘记此网络再重连。"
draft: false
---

> 测试单位：Yopitek（ALFA Network 台湾经销）｜测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`|测试设备：自有 iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）|测试对象：自有办公室 Wi-Fi（SSID `YUPITEK`，2.4G ch5 / 5G ch36、157）。
>
> 本文为经销商对产品兼容性与能力边界的硬件验证。所有 Monitor / Injection / AP / WPA3 测试均于 Yopitek 自有设备、自有办公室 Wi-Fi、对自有测试手机进行，属正当能力验证；不针对任何第三方网络，亦不提供攻击操作步骤。文中 injection 仅送 probe request 做能力自测，不送攻击数据包。

## 重点摘要（TL;DR）

AWUS036ACHM 于 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）实测：双频 monitor 可用，2.4G 数据包注入 96–100%（5G 只验到广播注入），双频均可架设 AP 热点（须关闭 802.11n）。

- Ubuntu 24.04 免装驱动：MT7610U 由 kernel 6.17 内置的 mt76x0u 接管，插上即认，不用 DKMS、不用额外固件。
- 双频监听模式（monitor mode）可用；2.4G 数据包注入 96–100%。
- 5GHz 只验到广播注入，逐台回应率本次未取得（原因待查）。
- 开 AP 须关闭 802.11n；WPA3 须设 `sae_pwe=0`，旧款 iPhone 才连得上。
- 单天线 1T1R（AC600），吞吐与定位和 2T2R 的 ACM / ACH 不同级。

## 1. 这张卡与这个平台

AWUS036ACHM 是 ALFA 的单天线 AC600 卡，芯片为 MediaTek MT7610U，对应 Linux 内置驱动 `mt76x0u`。它是 AWUS036ACM（MT7612U、2T2R）的单流姊妹款：规格上是 1T1R（AC600），少了一条空间串流，但换来更小的体积与社区公认的长距离接收。morrownr/USB-WiFi 社区把它列入 Kali 推荐清单与「The Short List」，并标注 VIF、Active monitor、WPA3 皆为 Yes、Very Long range、单流、in-kernel。

我们把它插上 ASUS GX10（NVIDIA GB10、128GB UMA、ARM64），在 Ubuntu 24.04 LTS、kernel 6.17 上逐项量测 Monitor、Injection、AP 与 WPA3-SAE。先讲结论：这张卡在本平台能用，2.4GHz 的能力也相当完整。但有两个兼容雷得先知道：开 AP 必须关 802.11n，WPA3 必须设 `sae_pwe=0`；另外 5GHz 的逐台 injection 本次只验到广播。下表是整体速览：

| 能力项目 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（侧录） | ✅ | ✅ |
| Injection（注入） | ✅ 96–100% | ⚠️ 仅广播可用，逐台回应率未取得 |
| AP 热点 | ✅（须纯 802.11g） | ✅（须纯 802.11a，20 MHz） |
| WPA3-SAE | ✅（须 `sae_pwe=0`） | 未实测 |

> 图例：✅ 实测通过 ｜ 🟡 部分或单机可成立 ｜ ⚠️ 有限制 ｜ ❌ 不支持或失败。

## 2. 硬件与驱动（免装）

ACHM 插上 GX10 后，kernel 6.17 内置的 `mt76x0u` 直接辨识，不需要 DKMS、不需要额外固件、也不必从 GitHub 编 out-of-tree 驱动。确认网卡的三个指令：

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

接口名以 MAC 命名（`wlx<MAC>`），重插卡后名称不变，写脚本时可直接绑定。`iw phy info` 声明支持的接口模式包含 `managed`、`AP`、`monitor`、`mesh point`、`IBSS`、`P2P-client`、`P2P-GO`，涵盖本文要测的全部情境。

平台共通的两条安全守则，在 ACHM 上一样适用：第一，绝不运行 `airmon-ng check kill`，那会关掉 NetworkManager，让 GX10 对外断线；第二，全程只操作 `wlx*` 接口，不碰内置的 `wlP9s9`（GX10 对外上网主线）。要进 monitor／AP 一律用 `iw` 搭配 `nmcli dev set $IF managed no`，不动到系统主网卡。

## 3. 实测能力：Monitor / Injection / AP / WPA3

### 3-1. Monitor（2.4 + 5 GHz）✅

两个频段的侧录都正常。2.4GHz 第 6 频道，8 秒就收满 300 数据包的截取上限；5GHz 依频率活动量不同：ch36（5180）8 秒收满 300、5745 收 254、5785 收 54（某频道数据包少通常代表当下该频道没有活跃 AP，不是网卡问题）。

跳频全频扫描最能看出单天线卡的接收实力：

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

实测 120 秒扫出 19 个基地台、14 个用户端，分布在 ch1/2/5/6/36/149/157。对一张单流 AC600 卡来说，这个涵盖度足以当稳定的侧录来源，也呼应社区给它的「Very Long range」评价。

### 3-2. Injection（2.4 + 5 GHz）

这是 ACHM 两个频段差异最明显的地方，也是选型时要特别留意的一项。

2.4GHz 第 6 频道做 `aireplay-ng --test` 能力自测，结果漂亮：

```text
Injection is working!
Found 4 APs
30/30: 100%
```

四台基地台的回应率落在 96–100%，注入能力完整。

但切到 5GHz（ch36 与 ch149 都试过）就不一样：

```text
Injection is working!
Found 0 APs
```

也就是说，5GHz 的广播注入可用（driver 回报 `Injection is working!`），但 `aireplay-ng --test` 的逐台回应率，在两个 5G 频道都是 `Found 0 APs`，本次没有取得百分比。这是 ACHM 这张单天线卡在本平台的实测现象，原因待追查，我们不替它补一个没量到的数字。老实说：如果你的用途需要稳定的 5GHz 逐台注入，ACHM 本次只在 2.4GHz 验到完整注入率。

### 3-3. AP 热点（2.4 + 5 GHz）✅ — 但必须关 802.11n

ACHM 的第一个兼容雷在这里。开 AP 时，hostapd 设置档不要加 `ieee80211n=1` 与 `ht_capab`：2.4GHz 走纯 `hw_mode=g`、5GHz 走纯 `hw_mode=a`（20 MHz）。一个最小可用的 2.4GHz 设置长这样：

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 纯 802.11g, 不要加 ieee80211n=1 或 ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=请改成你的密码至少8码
```

实测 iPhone 7 Plus 两频都连入：2.4GHz 可见 `AP-STA-CONNECTED` 接着 `EAPOL-4WAY-HS-COMPLETED`；5GHz（ch36、20 MHz）测到 -71 dBm、rx 54 Mbit、`authorized: yes`。

反过来，如果设置档保留了 `ieee80211n=1`，hostapd 会反复喷 `handle_assoc_cb: STA not found`，iPhone 画面显示「无法加入网络」或「密码错误」，但那其实是 802.11n 关联失败，不是密码问题。移除 802.11n 就好。ACHM 是单天线卡，5GHz AP 本次采 20 MHz，没试 VHT80。

### 3-4. WPA3-SAE ✅ — 但必须 `sae_pwe=0`（最容易踩的兼容雷）

ACHM 的第二个、也是最值得单独讲的兼容雷。WPA3-SAE 的 hostapd 以 `sae_pwe` 控制密码元素（password element）的推导方式：`0` 是只用传统 Hunting-and-Pecking、`1` 是只用 Hash-to-Element（H2E）、`2` 是两者并存（同时支持 Hunting-and-Pecking 与 H2E）。差别直接决定旧 iPhone 连不连得上：

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 强制 PMF
ieee80211w=2
# 关键: 兼容 iPhone 7 Plus 这类旧端点
sae_pwe=0
sae_password=请改成你的密码
```

实测对照：

- `sae_pwe=0`：iPhone 15 Pro 与 iPhone 7 Plus **都连入**（`authorized: yes`、`MFP: yes`）。
- `sae_pwe=2`：iPhone 7 Plus 会**关联成功但 4-way 密钥交握失败而断线**，表面上看起来又像「密码错误」；iPhone 15 Pro 则可以连。

结论很直接：要兼容旧 iPhone（含 iPhone 7 Plus 这类 2016 年机种），hostapd 一定要设 `sae_pwe=0`。改完设置后，请让 iPhone 先「忘记此网络」再重连，避免残留的关联状态造成假性失败。这一点在 9 款总表上，ACHM 的 WPA3 字段是以「✅*」加星号特别标注的。

## 4. 高级与限制

先用一张表收敛本次 ACHM 的完整涵盖范围与状态，后续段落再就重点展开：

| 功能 | 状态 | 本次实测重点 |
|---|---|---|
| Monitor（2.4 + 5 GHz） | ✅ | 跳频 120 秒扫到 19 AP + 14 client |
| Injection 2.4 GHz | ✅ | 回应率 96–100% |
| Injection 5 GHz | ⚠️ | 广播可用，逐台回应率未取得 |
| AP（2.4 + 5 GHz） | ✅ | iPhone 两频连入，须关 802.11n |
| WPA3-SAE | ✅* | 于 2.4 GHz 实测（5 GHz 未实测）；新旧 iPhone 皆连入，须 `sae_pwe=0` |
| VIF（STA+AP、AP+monitor） | ✅ | 边上网边当热点，下载 198 Mbit/s |
| WPA handshake 截取 | ✅ 端到端（.22000，于 5 GHz ch36） | deauth 自有 iPhone，截取完整 4-way M1–M4，转出 hashcat `.22000` |
| Active monitor | 🟡 | 可设置侧录，ACK 未验 |
| Ad-hoc（IBSS） | 🟡 | 单机可创建，未与第二台互连 |
| Mesh（802.11s） | 🟡 | 单机可加入，未 peer link |
| Wi-Fi Direct（P2P） | ⬜ | 需第二台设备，略过 |

> ✅* ＝ WPA3-SAE 可用但须 `sae_pwe=0`；详见第 3-4 节。

**VIF（虚拟接口，同频道、最多 2 接口）。** ACHM 支持同一张卡切出多个接口同时运作，前提是各 VIF 用不同 MAC、AP VIF 不交给 NetworkManager 管、所有 VIF 同频道，ACHM 另需 AP 关 802.11n。两种组合都实测过：

- **STA + AP（一边上网一边当热点）**：iPhone 7 Plus 连入 AP（-66 dBm、authorized）的同时，主接口连上 YUPITEK，ping 30/30、avg 3.2 ms、下载 198 Mbit/s。
- **AP + Monitor**：开着 AP 的同时侧录，8 秒截取 300 frame，其中含 46 个自家 AP 的 beacon。

**handshake 截取。** ACHM 在 5GHz（ch36）完成端到端链路：deauth 自有 iPhone、截取完整 4-way（M1–M4），并转出 hashcat `.22000`。它是 9 款中完成端到端的 7 款之一（ACM、ACHM、ACH、ACS、EACS、AX、AXER）。其 5GHz 逐台注入回应率（`aireplay-ng --test`）仍未取得。

**mesh / IBSS（单机可创建）。** 这是 mt76 家族相对 Realtek rtw88/rtw89 的差异点。IBSS（Ad-hoc）约 9 秒就 `Joined IBSS`、能发出 beacon；Mesh（802.11s）可进入 `type mesh point`、发出 mesh beacon。两者本次都是单机成立、没跟第二台互连（缺第二台设备而略过），所以标 🟡。Realtek 的 rtw88/rtw89 卡（如 AWUS036ACH）在本平台虽可创建单机 IBSS，但不支持 802.11s mesh，所以要做 802.11s mesh 实验，ACM 与 ACHM 这两张 mt76 卡反而是少数选择。

**Active monitor 🟡。** 可设置、侧录正常，但 ACK 回应行为需要第二台设备才能验证，本次未验。

**Kali 工具（平台层级，与其他卡共通）。** `airmon-ng`、`kismet`、`bettercap`、`wifite`（git 版）、Wireshark/tshark 都可把 ACHM 当来源使用；只有 `hcxdumptool` 在本平台 `failed to arm interface`（AWUS036EACS 在 2.4 GHz 除外；内置驱动无 active-monitor 支持），截取请改用 `airodump-ng` 搭配 aircrack-ng 套件。ARM64 另需注意：`aircrack-ng` 常缺 prebuilt package 要自源代码编译、`wifite` 建议用 GitHub 版以绕过 apt 依赖冲突。

## 5. 适用情境与选型（连回 Hub）

把 ACHM 放回 9 款的选型脉络，它的位置很清楚：

**适合**

- **mesh（802.11s）实验**：mt76 驱动单机可创建 802.11s mesh（与 IBSS）；Realtek 卡可创建单机 IBSS，但做不到 802.11s mesh。
- **长距离单流 monitor 侧录**：跳频 120 秒扫到 19 AP + 14 client，社区评为 Very Long range。
- **2.4GHz injection、以及 AP / WPA3 热点**：2.4G 注入 96–100%，WPA3 设对 `sae_pwe=0` 后新旧 iPhone 都连得上。

**要留意（诚实限制）**

- 5GHz 逐台 injection 本次只验到广播，没有百分比。
- 开 AP 要关 802.11n、WPA3 要 `sae_pwe=0`，两个设置不对都会让旧 iPhone「看起来像密码错误」。
- 单天线 1T1R，吞吐与定位和 2T2R 的 ACM／ACH 不同级。

**选型指引**：如果你的核心需求是两频稳定注入加端到端 handshake，9 款里 AWUS036EACS / AWUS036ACH / AWUS036ACS 更合适；要 Wi-Fi 6 + AP 热点就看 AWUS036AX / AWUS036AXER；若主打 mesh / IBSS 单机实验或长距离侧录，ACHM（或它的 2T2R 姊妹 ACM）才是对的工具。最后提醒避雷：injection / handshake 用途别选 AWUS036AXM / AXML，这两张的 MT7921 注入在本平台是失败的。

完整的 9 型号硬件、驱动、Monitor / Injection / AP / WPA3 全矩阵与依用途的选型总评，见 Hub 总表：[9 款 ALFA 无线网卡 ARM64 / GX10 实测总矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常见问题（FAQ）

**Q：AWUS036ACHM 在 Ubuntu 24.04 需要装驱动吗？**
不需要。MT7610U 由 kernel 内置的 mt76x0u 驱动接管，Ubuntu 24.04（kernel 6.17）插上即认，不用 DKMS、不用额外固件；lsusb 可看到 USB ID 0e8d:7610。

**Q：AWUS036ACHM 能进 monitor mode 吗？能扫到多少 AP？**
能。2.4GHz 与 5GHz 都能进 monitor mode；用 airodump-ng 跳频全频扫描 120 秒，实测扫到 19 个 AP、14 个用户端，分布在 ch1、2、5、6、36、149、157。

**Q：AWUS036ACHM 的数据包注入成功率多少？5GHz 可以吗？**
2.4GHz 第 6 频道逐台注入回应率 96–100%（aireplay-ng --test，找到 4 台 AP）。5GHz（ch36、ch149）只验到广播注入可用，逐台测试回报 Found 0 APs，本次没有取得百分比，原因待查。

**Q：AWUS036ACHM 开 AP 时 iPhone 显示「无法加入网络」或「密码错误」怎么办？**
先关掉 802.11n：hostapd 设置档不要加 ieee80211n=1 与 ht_capab，2.4GHz 用纯 hw_mode=g、5GHz 用纯 hw_mode=a（20 MHz）。否则 hostapd 会反复出现 handle_assoc_cb: STA not found，画面像密码错误，其实是 802.11n 关联失败。

**Q：AWUS036ACHM 的 WPA3-SAE 为什么旧 iPhone 连不上？**
多半是 hostapd 的 sae_pwe 设置。实测 sae_pwe=0 时 iPhone 7 Plus 与 iPhone 15 Pro 都连得上；sae_pwe=2 时 iPhone 7 Plus 会关联成功但 4-way 交握失败而断线，看起来像密码错误。请搭配 ieee80211w=2，改完设置后让 iPhone 先忘记此网络再重连。

## 6. 延伸阅读

- 〔Hub 总表〕9 款 ALFA 无线网卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩阵与选型总评 → [/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 〔姊妹款〕AWUS036ACM（MT7612U / 2T2R）逐卡实测 — 内链待补（placeholder）
- 〔平台教学〕免装驱动：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驱动激活 ALFA 网卡 Monitor 与 AP — 内链待补（placeholder）
- 〔专题〕WPA3-SAE 时代的 handshake 截取能力与 `sae_pwe` 兼容性雷区 — 内链待补（placeholder）

---

*测试单位：Yopitek（ALFA Network 台湾经销）— https://www.yupitek.com ｜ 测试环境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）。数据引用自 2026-11-16～11-18 的实机测试报告，不针对任何第三方网络，亦不提供攻击操作步骤。*
