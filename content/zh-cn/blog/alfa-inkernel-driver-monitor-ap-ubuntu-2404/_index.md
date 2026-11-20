---
title: "免装驱动：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驱动激活 ALFA 网卡 Monitor 与 AP 模式（rtw88 / rtw89 / mt76 实测）"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Ubuntu 24.04 / kernel 6.17 免装驱动教学：用 in-kernel rtw88 / rtw89 / mt76 驱动激活 ALFA 网卡 Monitor 与 AP 模式，含 WPA3 热点兼容性设置与 Kali 工具链注意事项。"
faq:
  - question: "Ubuntu 24.04 要怎么让 ALFA 网卡进入 monitor mode？"
    answer: "在 kernel 6.17 以上，只要把接口交出 NetworkManager 管理、切换成 monitor 接口模式即可，不需安装第三方驱动；本文测试的 rtw88 / rtw89 / mt76 三个驱动家族流程一致，详细指令见文中步骤。"
  - question: "为什么在 Ubuntu 上 ALFA 网卡不用另外装驱动？"
    answer: "因为 Realtek rtw88／rtw89 与 MediaTek mt76 已陆续把这些 USB 芯片纳入 mainline kernel 的 in-kernel 支持（各卡最低版本不同，从 4.19 到 6.17；Ubuntu 24.04 上的 AX、AXER 需要 kernel 6.17 以上，例如 24.04.4 的 HWE）；kernel 6.17（GX10 实测）9 款卡均已内置，插上即认、免编译、免 DKMS。"
  - question: "用 ALFA 网卡架 WPA3 热点，旧 iPhone 连不上怎么办？"
    answer: "实测发现两个常见原因：一是 hostapd 的 sae_pwe 需设为 0 而非 2 才兼容旧款 iPhone；二是保留 802.11n 设置可能让旧设备关联失败，兼容性优先时建议关闭 802.11n。"
  - question: "rtw88、rtw89、mt76 哪个驱动家族支持 mesh 或 IBSS？"
    answer: "实测中 mt76 家族（如 AWUS036ACM / ACHM）可单机创建 mesh（802.11s）与 IBSS；Realtek rtw88 可单机 join IBSS（以 ACH 实测为准）但不支持 mesh，rtw89 则连 IBSS 都未声明支持。"
draft: false
---

> 本文为标准 Linux 网络设置教学，示范如何在新版 kernel 用**内置（in-kernel）驱动**激活 ALFA 无线网卡的 Monitor（监听）与 AP（热点）模式。
> 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有数据均为 Yopitek 于自有设备、自有办公室 Wi-Fi（SSID `YUPITEK`）上的产品兼容性实测节录。
> ⚠️ **合法使用**：Monitor 模式仅限监听自己拥有或已取得授权的网络；AP 模式请遵守当地无线电法规。本文不涉及针对第三方网络的任何攻击操作。

---

## 重点摘要（TL;DR）

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）上，Yopitek（ALFA Network 台湾经销）实测的 9 款 ALFA USB 无线网卡全部走 in-kernel 驱动（`rtw88` / `rtw89` / `mt76`），免装驱动即可用同一套流程启用 Monitor 与 AP 模式，2.4G 与 5G AP 下 iPhone 7 Plus / 15 Pro 都能正常连接；各卡最低 kernel 介于 4.19 至 6.17。

- **新 kernel 免装驱动**：Realtek `rtw88` / `rtw89` 与 MediaTek `mt76` 已把 ALFA 这些 USB 芯片纳入 in-kernel 支持；kernel 6.17（GX10 实测）9 张卡均已内置，各卡最低版本不同，插上即用、免编译、免 DKMS。
- **Monitor 与 AP 流程三家族一致**：交回 NetworkManager →`iw` 切 monitor／`hostapd` 起 AP。
- **两个兼容性雷**：开 AP 建议关 802.11n（`ieee80211n=0`）、WPA3-SAE 用 `sae_pwe=0`，否则旧款 iPhone 连不上。
- **高级模式分级**：mesh 仅 `mt76`；IBSS 单机 `mt76` 与 `rtw88`（ACH）可 join，`rtw89` 未声明。
- **平台铁则**：绝不运行 `airmon-ng check kill`（会让 GX10 断网），只操作外置的 `wlx*` 接口。

## 1. 为什么「免装驱动」是这一代的重点

过去在 Linux 上使用 ALFA 这类 USB 无线网卡，最常见的门槛就是驱动。RTL8812AU、MT7610U 这些芯片早年都没有进 mainline kernel，用户得从 GitHub 抓 out-of-tree 项目（例如 `morrownr/USB-WiFi`、`aircrack-ng/rtl8812au`），再透过 DKMS 绑定当前 kernel 版本编译。每次 kernel 更新，DKMS 就得重编一次；一旦编译失败，网卡就直接消失。对需要稳定维运的经销验证或教学环境来说，这是长期的痛点。

近年的 mainline kernel 让情况出现转折：Realtek 的 `rtw88`、`rtw89` 与 MediaTek 的 `mt76` 三大驱动家族陆续把这些 USB 芯片正式纳入 in-kernel 支持。kernel 6.17（GX10 实测）9 张卡均已内置，各卡最低版本不同（见下表“最低 kernel”栏），**插上即认、免编译、免 DKMS**。更重要的是，原本两个最多人用的 out-of-tree 项目（morrownr 与 aircrack-ng 的 rtl8812au）现在都已改为导向这颗内置驱动，bug 回报也统一回到 `lwfinger/rtw88`。换句话说，手动编驱动这个步骤，在新 kernel 上已经可以直接省略。

`lwfinger/rtw88` 社区仍在活跃维护，持续把修正往上游送，内置驱动的稳定度因此跟着 kernel 一起更新，用户不必再各自维护分支、也不会每次升级就被 DKMS 编译失败卡住。对经销验证与教学环境来说，同一套操作步骤能跨多张卡、跨多次 kernel 更新重复使用，维护成本明显下降，这也是本文把重点放在「免装驱动」的原因。

本文测试涵盖的芯片与对应内置驱动模块如下：

| 芯片家族 | 芯片型号 | 内置驱动模块 | 最低 kernel | 世代 / 串流 | 代表卡 |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1（+BT） | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> 若你的系统 kernel 低于该卡的最低版本（见上表），才需要走旧路：用 DKMS 安装 out-of-tree 驱动（rtw88 系列可用 `lwfinger/rtw88`）。以 Ubuntu 24.04 为例：GA kernel 6.8 已内置 ACM、ACHM、AXM、AXML、EACS 的驱动；HWE 6.14 再加上 ACH、ACS。AX、AXER 需要 kernel 6.17 以上（例如 24.04.4 的 HWE）。本文以 GX10 的 kernel 6.17 为准。

---

## 2. 确认驱动已加载并绑定

在切换任何模式前，先确认卡被正确辨识、驱动已绑定、接口名称已生成。以 Realtek 的 AWUS036ACH（`rtw88_8812au`）为例，四个检查步骤如下。

**步骤一：确认 USB 设备被枚举。** 用 `lsusb` 找 USB ID（Realtek 多为 `0bda:xxxx`，MediaTek 多为 `0e8d:xxxx`）：

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**步骤二：确认驱动绑定与 USB 速率。** `lsusb -t` 可同时看到绑定的 driver 与连接速度（`5000M` 代表走 USB 3.0）：

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

MediaTek 卡则可改用 `dmesg` 观察驱动初始化消息，同时确认接口改名：

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**步骤三：取得接口名称。** Ubuntu 采可预测命名（predictable naming），ALFA 外置卡一律是 `wlx` 加上 MAC 地址。这个名称由 MAC 决定，**重新插拔后不会改变**，方便脚本化。内置的对外网卡则是另一组名称（GX10 上为 `wlP9s9`），务必分辨清楚：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**步骤四：查找芯片声明支持的接口模式。** 这一步决定了后面哪些模式能用：

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88（ACH）会列出 `IBSS / managed / AP / AP/VLAN / monitor`，但**没有** mesh 与 P2P；MediaTek mt76（ACHM）则会额外列出 `mesh point / P2P-client / P2P-GO`。这份清单就是各家族能力差异的第一手依据，详见第 5 节。

---

## 3. 激活 Monitor 模式（2.4 GHz / 5 GHz）

Monitor（监听）模式让网卡不关联任何 AP、直接接收空中的 802.11 frame，常用于自家网络的数据包诊断、频谱巡检与信号覆盖评估。三个家族的激活流程一致，差别只在个别家族的稳定性注意事项（见第 5、6 节）。

**通用激活步骤：**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # 交回给我们自己管, 避免 NetworkManager 介入
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

看到 `type monitor` 就代表切换成功。接着指定要监听的频道。**2.4 GHz** 用 `set channel`：

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

**5 GHz** 用频率指定较不易出错（ch36 = 5180 MHz）：

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**预期结果（实测节录）：** AWUS036ACH 于 ch1 / ch6 / ch11 分别抓到 92 / 214 / 71 个 frame；5 GHz 的 ch36 / ch149 / ch157 分别抓到 260 / 137 / 127 个 frame，代表 2.4G 与 5G 监听都正常。MediaTek 的 ACHM 以 `airodump-ng --band abg` 跳频扫描 120 秒，可在 ch1/5/6/36/149/157 一带找到 19 个基地台、14 个用户端。某频道抓到 0 数据包，通常只是当下该频道没有 AP，不是网卡故障。

切到 monitor 模式后，常见的标准诊断工具都能直接在 `wlx*` 接口上运作：`airmon-ng` 用来列出网卡与驱动状态、`kismet` 可当成数据源实时侧录并产生 `.kismet` log、`Wireshark` 与 `tshark` 负责解析截取到的数据包、`bettercap` 则可做频道巡检。这些工具在三个家族上都实测可用，很适合用来盘点自家无线环境的频道使用状况与信号覆盖。唯一要注意的是 `hcxdumptool` 8.x 在本平台对三个家族都会 `failed to arm`，唯 EACS 在 2.4 GHz 除外（内置驱动不提供 active-monitor），若需要类似功能请改用 `airodump-ng` 搭配 aircrack-ng 套件。

> **5 GHz 提醒：** 默认 regdomain（`country 00`）下，许多 5 GHz 频道是 passive/no-IR，监听可以但主动发送受限。若后续要做授权范围内的 5 GHz 测试，请先 `sudo iw reg set US` 解锁、测完再 `sudo iw reg set TW` 设回。Realtek `rtw88_8812au` 另有已知的 5G RX-stuck 现象（反复切模式后 5G 收不到数据包），遇到时请实体拔插一次卡再优先做 5G。

---

## 4. 激活 AP / 热点模式（2.4 GHz / 5 GHz）

AP（热点）模式用 `hostapd` 把网卡变成一个 Wi-Fi 基地台。三个家族的流程相同：先把接口交出 NetworkManager，再用一份 `hostapd` 设置档启动。以下是通用的最小设置。

**4-1. 2.4 GHz（纯 802.11g）**

创建设置档 `/tmp/ap24.conf`：

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<你的密码至少8码>
```

启动：

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

当用户端连上时，`hostapd` 会依序输出 `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED`，看到最后一行就代表四向交握完成、连接成功。

**4-2. 5 GHz（纯 802.11a，ch36）**

把上面设置改成 5 GHz：

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2 的卡（如 rtw89 的 AX/AXER、mt76 的 ACM/AXM）可再加 VHT80 设置拉到 80 MHz 带宽；单天线或求兼容性时，维持 20 MHz 纯 a 即可。

**4-3. 两个关键兼容性设置**

1. **开 AP 建议关 802.11n**（`ieee80211n=0`，走纯 g / 纯 a）。实测旧款用户端（iPhone 7 Plus）在保留 `ieee80211n=1` 时会关联失败、画面误报「密码错误」，实际是 `handle_assoc_cb: STA not found`；移除 802.11n 即第一次就连上。
2. **WPA3-SAE 请用 `sae_pwe=0`**（hunting-and-pecking）。用 `sae_pwe=2`（强制 H2E）时旧机密钥交握会失败。WPA3 段落范例：

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

这两个雷在 Realtek 与 MediaTek 卡上都一样会遇到，属于用户端兼容性而非驱动差异。本文测试的九张卡在 2.4G 与 5G AP 下都能让 iPhone 7 Plus / 15 Pro 正常连入。

**4-4. 一边上网、一边当热点（STA + AP）**

mt76 家族支持用一张卡同时连上现有 Wi-Fi、又另建一个 AP VIF 当中继热点。实测 ACHM 在主接口连着 YUPITEK 的同时开出 5 GHz 热点让 iPhone 连入，下载仍有 198 Mbit/s、ping 平均 3.2 ms。此组合需满足三个条件：AP VIF 要用不同的 MAC、接口名称维持 `wlx` 格式、且所有 VIF 都在同一个频道。Realtek 卡此组合未被 phy 保证（rtw88 的 managed + monitor 虽可用，但 STA + AP 并不稳定），要做中继热点建议优先选 mt76 家族。

---

## 5. 三芯片家族差异与限制

基本的 managed / monitor / AP 三模式，三个家族都支持、表现一致。差异在**高级接口模式**（mesh、IBSS、active monitor、P2P）：这完全取决于驱动声明，和卡的天线数无关。以下是实测汇整。

| 高级模式 | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor（2.4G/5G） | ✅ | ✅ | ✅ |
| AP（hostapd） | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS（单机） | 🟡 单机可创建 | 🟡 单机可创建 | ❌ 驱动未声明 |
| Mesh（802.11s，单机） | 🟡 单机可创建 | ❌ `-95` 不支持 | ❌ 驱动未声明 |
| Active monitor | 🟡 可设置 | ❌ `-95` 不支持 | N/A |
| Wi-Fi Direct（P2P） | 需第二台设备 | ❌ `-95` 不支持 | N/A |

**MediaTek mt76（ACM / ACHM / AXM / AXML）** 是高级模式最完整的一家。`iw phy info` 就声明了 `mesh point`、`IBSS`、`P2P-client/GO`。实测单机即可 `Joined IBSS`、`type mesh point` 并发出对应 beacon（与第二台 peer link 因缺第二台设备未验）。如果你的用途是 mesh 或 IBSS 单机实验，mt76 家族是首选。要特别注意的是 Wi-Fi 6 的 MT7921（AXM/AXML）虽然模式齐全、AP 稳定，但在本平台无法做 frame injection（主因是 stock kernel 6.16+ 的 mac80211 chanctx 回归，非芯片先天；社区同型号改用 git／patched 驱动虽可运作但 firmware 锁速率，对应 morrownr/USB-WiFi #387、morrownr/mt76 #18），不适合需要注入的高级测试。

**Realtek rtw88（ACH / ACS / EACS）** 支持 `IBSS / managed / AP / AP/VLAN / monitor`。IBSS 单机可创建（`Joined IBSS`，以 ACH 实测为准；EACS 虽列出 iftype 但实测 join 无效），但 **mesh（802.11s）、active monitor、Wi-Fi Direct 三者实测皆回 `Operation not supported (-95)`**。另一个 rtw88 专属特性是 VIF：`iw phy` 旗标虽写「interface combinations are not supported」，但 ACH 实测 managed + monitor 两接口可同时 up、monitor VIF 抓到 100 个 frame，「边上网边侧录」可行；不过 phy 未保证此组合，重负载长跑仍建议用 mt76 家族。

**Realtek rtw89（AX / AXER）** 是本文最新的 Wi-Fi 6 家族，monitor 与 AP（含 VHT80）都表现良好、接收灵敏度强。但在高级模式上，active monitor / mesh / IBSS / P2P 在驱动层即未声明（N/A），因此这些单机实验请改用 mt76 卡。rtw89 的定位是稳定的 Wi-Fi 6 监听与热点，不是高级接口模式的实验平台。

> 一句话选型：**要 mesh / IBSS 单机 → mt76（ACM / ACHM）；要 Wi-Fi 6 热点与强接收 → rtw89（AX / AXER）；要双频通用与 VIF → rtw88（ACH）。**

---

## 6. 平台安全注意（GX10 + Ubuntu ARM64）

在 GX10 这类「内置网卡负责对外上网、外置 ALFA 卡做测试」的机器上，以下几点是维运铁则，照做才不会把自己弄断网。

1. **绝不运行 `airmon-ng check kill`。** 这个指令会关掉 NetworkManager，连带让 GX10 的对外连接中断。本文全程只用 `iw` 与 `nmcli dev set <接口> managed no`，不碰 `check kill`。
2. **只操作 `wlx*`，绝不碰内置 `wlP9s9`。** `wlP9s9` 是 GX10 对外上网的主线，任何 down / 改模式的动作都只能对 ALFA 的 `wlx*` 接口下，下指令前务必用 `echo $IF` 确认目标。
3. **RX stall 用拔插复原。** 反复切换 monitor / AP 后若扫不到任何东西，多半是驱动的接收卡死（Realtek 5G 尤其常见）。软件通常救不回来，直接**实体拔插一次**卡，USB 会重新枚举、接口名称因 MAC 不变而维持一致。
4. **BT+WiFi 复合卡换 USB 孔。** EACS、AXML 这类蓝牙加 Wi-Fi 的复合设备，重插时偶尔 Wi-Fi probe 会卡死、生不出 `wlx` 接口，换一个 USB 孔通常就正常。
5. **5 GHz 发送先设 regdomain。** 默认 `country 00` 下 5 GHz 多为 no-IR、禁止主动发送。授权范围内测试前 `sudo iw reg set US` 解锁，测完 `sudo iw reg set TW` 设回。
6. **ARM64 的套件注意。** GX10 是 aarch64，`aircrack-ng` 常缺 prebuilt wheel/package，需自源代码编译；`wifite` 建议用 GitHub 版以绕过 apt 依赖冲突。另外 `hcxdumptool` 8.x 在本平台对三个家族都会 `failed to arm`，唯 EACS 在 2.4 GHz 除外（内置驱动无 active-monitor 支持），监听截取请改用 `airodump-ng` 搭配 aircrack-ng 套件。

**测试结束后恢复一般模式：**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # 预期 type managed
```

---

## 常见问题（FAQ）

**Q：Ubuntu 24.04 要怎么让 ALFA 网卡进入 monitor mode？**
A：在 kernel 6.17 以上，只要把接口交出 NetworkManager 管理、切换成 monitor 接口模式即可，不需安装第三方驱动；本文测试的 rtw88 / rtw89 / mt76 三个驱动家族流程一致，详细指令见文中步骤。

**Q：为什么在 Ubuntu 上 ALFA 网卡不用另外装驱动？**
A：因为 Realtek `rtw88`／`rtw89` 与 MediaTek `mt76` 已陆续把这些 USB 芯片纳入 mainline kernel 的 in-kernel 支持（各卡最低版本不同，从 4.19 到 6.17；Ubuntu 24.04 上的 AX、AXER 需要 kernel 6.17 以上，例如 24.04.4 的 HWE）；kernel 6.17（GX10 实测）9 款卡均已内置，插上即认、免编译、免 DKMS。

**Q：用 ALFA 网卡架 WPA3 热点，旧 iPhone 连不上怎么办？**
A：实测发现两个常见原因：一是 hostapd 的 `sae_pwe` 需设为 0 而非 2 才兼容旧款 iPhone；二是保留 802.11n 设置可能让旧设备关联失败，兼容性优先时建议关闭 802.11n。

**Q：`rtw88`、`rtw89`、`mt76` 哪个驱动家族支持 mesh 或 IBSS？**
A：实测中 `mt76` 家族（如 AWUS036ACM / ACHM）可单机创建 mesh（802.11s）与 IBSS；Realtek `rtw88` 可单机 join IBSS（以 ACH 实测为准）但不支持 mesh，`rtw89` 则连 IBSS 都未声明支持。

## 7. 延伸阅读

- 九张 ALFA 卡的完整能力比较与选型总评 → [ALFA 无线网卡总评 Hub（总表）](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Realtek rtw88 代表卡逐步教学 → [AWUS036ACH 单卡实测](/zh-cn/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- MediaTek mt76 代表卡逐步教学 → [AWUS036ACHM 单卡实测](/zh-cn/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*测试单位：Yopitek（ALFA Network 台湾经销）— https://www.yupitek.com ｜ 测试环境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）*
