---
title: "解锁天空的频谱：使用 SDRlab H4M 被动接收航空语音与 NOAA 卫星云图教学"
date: 2026-08-18
draft: false
slug: "sdrlab-h4m-passive-reception-aviation-noaa"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "介绍软件定义无线电（SDR）被动接收原理，实战教学使用 SDRlab H4M 接收 118-137MHz 航空语音与 NOAA 137MHz 气象卫星云图。"
featureimage: "/images/blog/04_sdrlab_h4m_schematic.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "SDRlab H4M 是否具有发射无线电信号的功能？"
    answer: "不能。SDRlab H4M 为纯被动接收架构（Receive-Only），无任何射频功放与发射电路，符合各国无线电合法监听规范。"
---

![SDRlab H4M Passive Signal Reception Schematic](/images/blog/04_sdrlab_h4m_schematic.jpg)

> <strong>适用产品</strong>：SDRlab H4M（SKU: SDRLAB-H4M）
> <strong>难度</strong>：入门 → 进阶
> <strong>一句话摘要</strong>：只要有正确的天线与免费开源软件，你的桌面型电脑就能变成一台能「听」航空通信、甚至「看」到 800 公里外气象卫星云图的无限频谱接收机——而这一切，都只需要<strong>被动接收</strong>。

---

## 🛡️ 开头先讲安全红线

无线电的世界非常迷人，但越迷人越要守住分寸。

<strong>SDRlab H4M 是纯接收（Receive-only）设备</strong>，它天生没有发射能力，这正是它最适合入门的原因。本教程全程只使用<strong>被动监听（Passive Listening）</strong>：

> ⚠️ <strong>严禁任何发射与干扰</strong>
> - 严禁使用任何手段强化、改装本机为发射用途。
> - 严禁利用本设备干扰任何无线电通信（含航空、警消、广播等）。
> - 请仅监听依法可公开接收的信号；各国对于无线电接收的规范不同，使用前请确认所在地法规（台湾适用《电信管理法》相关规范）。
> - 接收到的内容仅供教育与研究用途，<strong>不得擅自重播、转售或移作商业用途</strong>。

守住这条线，才能长长久久享受频谱发现的乐趣。

---

## 一、软件定义无线电（SDR）与被动接收的基本原理

### 1.1 什么是「软件定义无线电」？

传统收音机把「选台、解调、放大」全部用硬件电路完成；而<strong>软件定义无线电（Software Defined Radio, SDR）</strong>把大部分工作交给通用硬件（模拟→数字转换后的数据流）与电脑里的软件搞定。硬件负责把天线抓到的高频信号降下来、数字化，剩下的解调（AM / FM / 解码 APT 卫星云图）全部由 <strong>GQRX、SDR#、CubicSDR、GNU Radio</strong> 这些开源软件在 CPU 上即时运算。

SDRlab H4M 的内部架构正是两种关键芯片的组合：

| 组件 | 芯片 | 任务 |
|------|------|------|
| 调谐器（Tuner） | <strong>R820T2</strong> | 把 0.5MHz – 1.7GHz 的高频信号筛选并降频到中频 |
| 数字解调芯片 | <strong>RTL2832U</strong> | 8-bit ADC 数字化 + USB 将 I/Q 数据流送往电脑 |
| 晶振 | 温度补偿晶振（TCXO） | 提供稳定参考频率，避免频率漂移 |

硬件光谱范围涵盖 <strong>0.5 MHz（长波）到 1700 MHz（L 波段）</strong>，因此 FM 广播、航空 AM、气象卫星、ADS-B、甚至业余无线电都能收。最高稳定采样带宽约 <strong>2.4 MHz</strong>（极限可达 3.2 MHz）。

### 1.2 什么是「被动接收」？

SDRlab H4M 的原理非常「老实」：<strong>它只听，不发</strong>。天线把空中的电磁波转成微弱的电压信号，接收器把这些信号放大、数字化后交给电脑。整个过程<strong>不会向空中发射任何能量</strong>，也因此是各国无线电法规中最友善、门槛最低的合法应用类型。

### 1.3 为什么铝合金外壳对于「听得到微弱信号」至关重要？

这是 SDRlab H4M 最容易被忽略、却最能影响成败的设计。

RTL-SDR 这类接收器非常灵敏，灵敏到连<strong>不想要的东西</strong>也一起收进来——尤其当你把它插在电脑旁：USB 供电的开关式电源杂讯、主机板高频频辐射、屏幕排线的电磁干扰，都会「灌进」接收前端，盖过你真正想听的微弱信号（例如 800 公里外的卫星）。

铝合金外壳在这里扮演三个角色：

1. <strong>法拉第笼式的电磁屏蔽（EMI Shielding）</strong>：金属外壳形成局部屏蔽，阻挡来自电脑与周边的环境射频杂讯，显著提升信号对杂讯比（SNR）。对于 NOAA 卫星这种只有几秒钟强的微弱信号，这往往是「收得到 / 收不到」的分水岭。
2. <strong>被动散热与频率稳定性</strong>：铝合金同时是良好的散热片。R820T2 调谐器对温度敏感，温度稳定 = 参考频率稳定，长期监听时不易漂移。
3. <strong>静电保护（ESD）与耐用性</strong>：铝壳接地能导走天线感应的静电，延长前端芯片寿命。

一句话总结：<strong>好的屏蔽不增加你的信号，而是帮你把杂讯挡在外面</strong>——这在密集的城市电磁环境里，CP 值极高。

---

## 二、实作：接收 118–137 MHz 航空 AM 语音（GQRX / SDR#）

118 MHz 到 137 MHz（VHF 航空通信频段）是航空器与地面塔台之间的<strong>振幅调变（AM）语音通信</strong>。航班在起降阶段会与塔台、近场台联系，内容包含高度、航向、跑道分配等。这是最容易入门、也最「有感」的频谱体验。

### 2.1 事前准备

- SDRlab H4M × 1
- 一台电脑（Windows / Linux / macOS 皆可）
- 天线：随附的偶极天线或伸缩天线即可，若要更好可用 V-Dipole 或调整天线长度到约 <strong>1.1 公尺（=137MHz 半波长）</strong> 附近
- 免费软件：<strong>GQRX</strong>（Linux/macOS）或 <strong>SDR#（SDRSharp）</strong>（Windows）

### 2.2 在 Linux 上用 GQRX

1. <strong>安装</strong>：
   ```bash
   sudo apt update
   sudo apt install -y rtl-sdr gqrx
   ```
2. <strong>发布 USB 装置</strong>：RTL-SDR 会被 Linux 内置 TV 调谐器驱动（`dvb_usb_rtl28xxu`）抢占，需先卸载再交给 `librtlsdr`：
   ```bash
   sudo rmmod dvb_usb_rtl28xxu
   # 一劳永逸: 将 blacklist 写入 /etc/modprobe.d/blacklist-rtl.conf
   # blacklist dvb_usb_rtl28xxu
   ```
3. <strong>启动 GQRX</strong>，第一次执行会跳出接收器设定窗口：
   - <strong>Device</strong> 选择 `Realtek RTL2838UHIDIR`（或对应 RTL-SDR 装置）
   - 确认采样率（Sample Rate）设为 2.4 MHz 或 2.048 MHz
   - 点 <strong>Start</strong>
4. <strong>切换到航空波段</strong>：
   - 在频率输入框输入 `127600000`（可先试你所在机场进场频率，或在网络上搜索当地的 ATIS／塔台频率）
   - <strong>Mode（模式）选 `AM`</strong>
   - 滤波器带宽（bandwidth）设 <strong>8–12 kHz</strong>（航空 AM 为窄频，太宽会收杂讯）
5. 若听到「沙沙声中夹着中文或英文语音」就成功了一半；试着在 118–137 间慢慢扫台。

### 2.3 在 Windows 上用 SDR#（SDRSharp）

1. <strong>下载 SDR#</strong>：到 RTL-SDR 官方网站下载 SDR# 压缩包并解压缩。
2. <strong>安装 Zadig 驱动</strong>（关键步骤）：把 RTL2832U 从 Windows 内置驱动切换成 <strong>WinUSB</strong>。开启 `zadig.exe` → Options 勾选 List All Devices → 选 RTL2832U → 点 <strong>Replace Driver</strong>。
3. 开启 `SDRSharp.exe`，在左上角确认装置被侦测，勾选 <strong>RTL-SDR（Tuner A）</strong>，按下播放键。
4. <strong>Mode 选 `AM`</strong>，频率输入 `118.000` – `137.000` MHz 之间的频率（注意显示单位为 MHz），再微调带宽与音量即可收听。

### 2.4 客服减量：航空接收常见排障检查清单（Support Intake）

遇到「完全没有声音」时，依序检查，并在联系客服前先完成此表：

| 症状 | 依序检查 | 最常见原因 |
|------|---------|-----------|
| 电脑抓不到装置 | 1. USB 接孔换一个 ● 2. 线材再接一次 ● 3. 重新插拔 | USB 供电不足／接触不良 |
| 扫不到任何台 | 1. 天线是否接上 ● 2. SMA 是否锁紧 ● 3. 频率是否在 118–137MHz ● 4. 是否靠近窗边 | 天线没接好或位置封闭 |
| 只有杂音没有语音 | 1. Mode 是否为 AM ● 2. 滤波带宽是否 8–12kHz ● 3. 机场是否太远 | 模式／带宽设定错误 |
| Linux 显示被占用 | 执行 `lsusb` 看是否为 dvb_usb 驱动 | 需 blacklist `dvb_usb_rtl28xxu` |
| Windows 装置无法描述 | 重新执行 Zadig 套用 WinUSB | 驱动未正确替换 |

> 💡 客服小技巧：联系 yupitek 客服时，<strong>附上 `lsusb` 或装置管理员截屏 + 你测试的频率与模式</strong>，能让技术人员直接定位问题，来回时间缩短一半以上。

---

## 三、进阶：解码 NOAA 气象卫星即时 APT 模拟云图

听完语音后，接下来的进阶关卡是把 <strong>750 公里外的气象卫星</strong>「看」在屏幕上。这一步需要一点耐心与天线摆位，但成功那一刻的成就感无可取代。

### 3.1 原理：NOAA POES 卫星与 APT 信号

美国国家海洋暨大气总署（NOAA）的 <strong>NOAA-15、NOAA-18、NOAA-19</strong> 三颗极轨气象卫星每天多次通过台湾上空，持续广播 <strong>APT（Automatic Picture Transmission）模拟信号</strong>——把红外线与可见光云图以每分钟 120 行的方式扫描广播：

| 卫星 | 下行频率（MHz） | 信号形式 | 带宽 |
|------|----------------|---------|------|
| NOAA-19 | <strong>137.100</strong> | APT 模拟 FM | ~34 kHz |
| NOAA-15 | <strong>137.620</strong> | APT 模拟 FM | ~34 kHz |
| NOAA-18 | <strong>137.9125</strong> | APT 模拟 FM | ~34 kHz |

卫星一次通过只有 <strong>8–12 分钟</strong>，且信号强度随高度角剧烈变化，因此「预测轨道 + 正确天线 + 对的软件」三者缺一不可。

### 3.2 硬件摆位

1. <strong>天线建议</strong>：使用 <strong>V-Dipole</strong>（两根 53 公分、夹角 120° 的偶极天线），这是业界公认 137 MHz 最划算的选择。
2. <strong>视野</strong>：让天线朝向天空开阔处（东南东或西南西方向），避开建筑与金属屏蔽。地平面愈干净，信号愈好。
3. <strong>接收器设定（GQRX 范例，以 NOAA-19 为例）</strong>：
   - 频率 `137.100 MHz`
   - <strong>Mode：FM（WFM）</strong>
   - 滤波带宽 <strong>约 40 kHz</strong>
4. <strong>预测通过时间</strong>：使用 <strong>GPredict</strong>（Linux/Windows）或 Heavens-Above 网站，查找下一次 NOAA-19 高度角 > 30° 的通过时段。

### 3.3 解码流程（WXtoImg / SatDump）

1. <strong>录制信号</strong>：在卫星通过期间，用 GQRX 或 SDR# 将音频录下来（或直接用虚拟音频线把 FM 音频送给解码器）。
2. <strong>解码</strong>：开启 <strong>WXtoImg</strong>（老牌免费软件）或跨平台开源的 <strong>SatDump</strong>，喂入音频档，自动同步行扫描线并输出全彩卫星云图。
3. <strong>产出</strong>：约 10 分钟后，你会得到一张覆盖东亚海域与台湾上空的可见光或红外线云图。
4. <strong>进阶细节</strong>：卫星通过时会产生<strong>都卜勒频移</strong>（逼近时频率偏高、远离时偏低），进阶玩家可在通过中途手动微调 ±3 kHz，或用自动追踪频率的解码器提升成功率。

> 💡 第一次失败很正常——轨道预测误差、天线角度、屏蔽物都会影响成败。把每次通过的「频率误差 + 天线位置」记录下来，通常第二次第三次就能收到清晰云图。

---

## 四、采购前兼容性确认工作表（Pre-purchase Worksheet）

在把 SDRlab H4M 放入购物车之前，花三分钟完成这张工作表，确保它符合你的需求，也让客服往后能更有效率地协助你：

| 检查项目 | 你的答案 | 说明与建议 |
|---------|---------|-----------|
| <strong>① 操作系统</strong> | □ Windows　□ macOS　□ Linux | H4M 三平台皆支持（Linux Kernel 4.0+、macOS 11–14、Windows 10/11）；Linux 建议额外确认 `rtl-sdr` 套件 |
| <strong>② 频率使用范围</strong> | 你想收哪个频段？ | 航空 118–137MHz／气象卫星 137MHz／FM 广播 88–108MHz／ADS-B 1090MHz 皆涵盖（0.5MHz–1.7GHz）|
| <strong>③ 天线状况</strong> | 有现成天线吗？ | 入门用随附天线即可；卫星云图建议再加购 V-Dipole（肢体两根 53cm 天线）|
| <strong>④ 带宽需求</strong> | 是否需要同时看大范围频谱？ | 稳定 2.4MHz 已足够语音与 APT；若需 GHz 级频谱即时观看，需考虑更高级设备 |
| <strong>⑤ 软件熟悉度</strong> | 用过 GQRX / SDR# / GNU Radio 吗？ | 初次使用建议从 GQRX 或 SDR# 开始，本教程涵盖完整步骤 |
| <strong>⑥ 法律与用途</strong> | 用途是否仅限被动监听？ | SDRLAB-H4M 为纯接收设备；确认用途为教育／研究／合法频谱观察 |
| <strong>⑦ 预算与配件</strong> | 是否需一并购入 SMA 转接线、支架？ | 配件可与 H4M 同单下单，节省运费 |

### 适合 / 不适合的场景

- ✅ <strong>适合</strong>：想入门无线电、想练天文／航空观察、学生与教程实验室、频谱发现与 RF 研究起步。
- ❌ <strong>不适合</strong>：想「发射」或干扰信号（本机完全不支持，也请勿尝试改装）；需要专业解调或 GHz 级远程监控的重度用户。

---

## 结语：用最便宜的方式，听见整片天空

SDRlab H4M 用不到一张高级显示卡的价格，把「无线电频谱」这片原本只有专业人士能碰触的领域，摊开在你桌上。从铝合金外壳的屏蔽设计、R820T2 调谐器与 RTL2832U 数字化的硬件分工，到 GQRX、SDR# 的一次设定，再到 NOAA 卫星云图的进阶解码——每一步都在强化同一个概念：

> <strong>接收，是最友善的入场券。</strong> 只听不发、宁静发现，频谱发现的乐趣才会一直留在你身边。

准备好让天空的语言进入你的屏幕了吗？把 SDRlab H4M（SKU: SDRLAB-H4M）加入购物车，配上 GQRX 或 SDR#，今晚就能开始。
