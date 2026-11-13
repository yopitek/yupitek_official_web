---
title: "SDRLab Flipper Zero 5G 扩充板 — 双频 Wi-Fi 安全研究模组"
description: "Flipper Zero 5G 扩充板，ESP32-C5 双频（2.4+5GHz）Wi-Fi，预烧 Deauth 固件，GPIO 供电，兼容 Momentum/Unleashed。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 扩充", "5GHz", "Wi-Fi", "Deauth", "信息安全研究"]
---


# SDRLab Flipper Zero 5G 扩充板 — 双频 Wi-Fi 安全研究模组

> **合法使用声明**：本扩充板仅供授权的资安研究及合法研究使用。对未经你拥有或未取得书面授权的网路、装置或基础设施进行测试，在多数国家均属违法行为。请确认符合当地无线频率使用法规，并负责任、合乎伦理地使用本产品。

---

## 一、这是什么

一块装在 Flipper Zero 背面 GPIO 排针上的无线研究扩充板。把你手里那台只有 2.4GHz 的 Flipper，一次补齐三种无线能力：

- **Wi-Fi 双频 2.4GHz + 5GHz**
- **433MHz Sub-GHz** 射频
- **主动 GPS**

外加一块 **2.8 吋彩色 TFT 萤幕**、**800mAh 可热插拔电池**、**四组 SMA 天线介面与四支天线全附**，以及**出厂预烧好的 ESP32 Marauder 5G 韧体**。

不需要买刷机器、不需要自己编译韧体。接上、设定三个参数，就能开始用。

---

## 二、产品特色

### 三种无线一次到位
- **Wi-Fi 双频 2.4GHz + 5GHz** — 扫描现代 5GHz 网路，补足旧板只能看 2.4GHz 的限制
- **433MHz Sub-GHz（A07 射频模组，10 dBm）** — 让 Flipper 内建收讯不良的环境多一个选择
- **主动 GPS** — wardrive 记录可以自动加上座标，接上 Flipper 时由主机供电、脱离时自动切换内建电池

### 2.8 吋彩色 TFT 萤幕
扫描结果、讯号强度、电量直接显示在板上，不用盯著电脑终端机猜。内建 Marauder UI。

### 四组 SMA 天线介面，四支天线全附（3 dBi／GPS 20 dBi）
背壳丝印清楚标示四个介面对应关系：

| 丝印 | 位置 | 用途 |
|---|---|---|
| `433M A` | 上缘左 | 433MHz 射频（A07 模组，10 dBm） |
| `GPS` | 上缘右 | 主动 GPS 天线 |
| `2.4G` | 左翼 | Wi-Fi 2.4GHz |
| `2.4G/5G` | 右翼 | Wi-Fi 双频 2.4GHz + 5GHz |

四个介面为独立的螺丝固定式 SMA 母座，**四支天线皆随货附上**：Wi-Fi 天线 3 dBi（11 cm）、433M 天线 3 dBi、GPS 天线 20 dBi。

### 800mAh 热插拔电池
出机箱就内建 800mAh 锂聚合物电池。可以脱离 Flipper 单机开机抓封包，扫完再插回主机当扩充板用。

### 出厂预烧 Marauder 5G 韧体
开箱即用，不需要另外购买刷机器。板上保留 TypeC 烧录口（正面左侧），供进阶使用者自行升级韧体。

### 金手指 + TVS 突波保护
所有讯号脚位镀金，每脚内建 TVS 瞬态电压抑制二极体，插拔 Flipper 时提供突波保护。

### 韧体生态相容
适用 Momentum、Unleashed、Xtreme 等含 WiFi Marauder 与 GPS 应用的客制韧体。

---

## 三、产品规格

| 规格项目 | 数值／说明 |
|---|---|
| **主晶片** | **Espressif ESP32-C5** |
| **Wi-Fi 天线介面** | **4 组 SMA 母座**：433M A／GPS／2.4G／2.4G+5G，**四支天线全附**（Wi-Fi 3 dBi／11 cm、433M 3 dBi、GPS 20 dBi） |
| **Sub-GHz** | 433MHz A07 射频模组，**10 dBm** 输出 |
| **GNSS** | 主动 GPS 模组，**自动切换供电**（接主机用主机电源、脱离用内建电池） |
| **萤幕** | **2.8 吋彩色 TFT**，内建 Marauder UI |
| **电池** | **800 mAh 锂聚合物**，可热插拔 |
| **连接介面** | Flipper Zero 标准 GPIO 排针（**2×8 针**），金手指 + 每脚 TVS 保护 |
| **预载韧体** | **ESP32 Marauder 5G**（开源，出厂预烧） |
| **韧体相容** | Momentum、Unleashed、Xtreme |

### 随附配件
- 主机 ×1（已组装，含 2.8 吋萤幕）
- 天线 ×4 — `2.4G`（3 dBi／11 cm）／`2.4G+5G` 双频（3 dBi／11 cm）／`433M A`（3 dBi）／`GPS`（20 dBi）各 1 支
- Flipper GPIO 排针连接

### 需另行购买
- **Flipper Zero 主机**（本板为扩充板，不含主机）

---

## 四、开始使用：三个必设参数

本板出厂已烧好韧体，不需要刷写。接上 Flipper 之后只需要设定三组脚位：

| 功能 | 设定路径 | 值 |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 或 14** |
| **ESP32（WiFi / Marauder）** | 同上 → **ESP32 Pin** | **15、16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS 与 ESP32 是两组不同的 UART 脚位，不可设成同一组**，否则 GPS 与 Wi-Fi 都会没有反应。

设定完成后重新启动 Flipper，进入 `Apps → GPIO` 即可看到对应的 WiFi Marauder 与 GPS 应用程式。

---

## 五、应用环境

- **双频 Wi-Fi 扫描** — 被动枚举 2.4GHz 与 5GHz 网路；撷取 SSID、BSSID、频道、RSSI、加密类型及连线客户端
- **WPA 握手包撷取** — 嗅探 EAPOL／PMKID 握手封包，用于已授权网路的安全稽核
- **Deauth 测试** — 传送 Deauth 封包测试网路韧性，仅限自有或已授权网路
- **Wardrive 网路拓扑映射** — GPS 标记的 Wi-Fi 与装置记录，输出 CSV 供后续分析
- **433MHz 射频研究** — 透过 Flipper 的 Sub-GHz 选单操作，适合评估 Flipper 内建收讯不良的环境
- **Evil Portal 演练** — 在授权环境下原型设计测试入口页
- **IoT 无线协定研究** — 在受控实验环境分析 IoT 装置在双频上的行为

---

## 六、已知限制（请务必留意）

- **5GHz Deauth 的稳定度取决于韧体版本**。开源 Marauder 韧体在 ESP32-C5 上对 5GHz deauth 的支援仍在持续改进中，建议以 **2.4GHz** 进行 deauth 测试为主；5GHz 建议以扫描、讯号监测、wardrive 记录为主要用途。实际表现请以当下韧体版本实测为准。
- **GPS 天线具方向性**，虽然商品标示为全向天线。天线请朝向开阔天空方向放置以取得定位，首次冷启动需要数分钟下载卫星星历资料。室内效果较差，建议到户外或靠窗使用。
- **GPS 回报时间为 UTC+0**，韧体选单中没有时区设定选项。台湾时间（UTC+8）请自行加 8 小时。
- **GPS 与 ESP32 是两组不同的 UART 脚位**（GPS：13 或 14；ESP32：15、16），两者不可设成同一组，否则 GPS 与 Wi-Fi 都会无回应。
- **TypeC 烧录口位于正面左侧**，仅供烧录韧体。
- **GPS 自动切换供电** — 接在 Flipper 上时由主机供电，脱离后改用内建电池，切换瞬间可能有短暂重启，属正常现象。

---

**产品页连结**：https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**完整使用手册**：https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/

**原厂商店页（OpenSourceSDRLab）**：https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754
