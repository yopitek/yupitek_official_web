---
title: "Flipper Zero 入门教程：开箱设置、固件更新与五大实用功能"
locale: zh-CN
hreflang_group: flipper-zero-beginners-guide-setup-tutorial
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yupitek
category: technical
tags:
  - Flipper Zero
  - 教程
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Flipper Zero 入门教程：开箱、固件更新与五大功能实测｜Yupitek"
seo_description: "Flipper Zero 是什么？从开箱、microSD 设置、qFlipper 固件更新，到 RFID／Sub-GHz／NFC／IR／BadUSB 五大功能实测，一篇带你完成 Flipper Zero 入门。"
---

# Flipper Zero 入门教程：开箱设置、固件更新与五大实用功能

> TL;DR：Flipper Zero 是一台掌上型的硬件探索工具，内置 125 kHz RFID、Sub-GHz、NFC、红外与 BLE，可用 USB-C 连接电脑模拟键盘（BadUSB）。入手后先装 microSD、用 qFlipper 或手机 App 更新固件，再从 RFID 读卡与 IR 遥控开始玩，就能快速上手。所有功能请只用在**你拥有或获得授权的设备**上。

## Flipper Zero 是什么？适合谁用？

Flipper Zero 是一台约巴掌大小的多功能携带装置，定位是“硬件探索工具”。它不是一般消费性 gadget，而是为资安研究人员、渗透测试新手、Maker 与 IoT 工程师设计的设备，用来读取、分析、模拟常见的无线协议与数字信号。

核心硬件包含：

- **125 kHz RFID**：读取与模拟低频门禁卡
- **Sub-GHz 无线**（CC1101 芯片）：分析 300–928 MHz 的遥控器、车库门、IoT 传感器信号
- **NFC（13.56 MHz）**：读取、写入与模拟高频卡
- **红外（IR）**：学习并重发电视、冷气等红外遥控码
- **BLE**：通过手机 App 配对控制与更新
- **USB-C**：连接电脑更新固件、模拟键盘（BadUSB / DuckyScript）
- **GPIO / iButton**：1-Wire 接触钥匙与硬件扩展

适合的读者：准备投入无线安全研究的学生、需要验证自家门禁/传感器可靠度的工程师、以及想了解 RFID/NFC 原理的 Maker。如果你只是想要一支“遥控器复制器”，它的 Sub-GHz 功能可以做到，但请先确认当地法令与使用场景。

## 开箱与初始设置：先装 microSD，再开机

Flipper Zero 出厂时不含 microSD 卡，但固件与数据存储**强烈建议**使用记忆卡。设置步骤如下：

1. **准备 microSD 卡**：建议 4 GB 以上，格式为 FAT32（FAT16/FAT32/exFAT 皆可）。将卡片**芯片朝上**插入机身底部卡槽。
2. **充电**：用 USB-C 连接充电器或电脑，第一次使用前充饱。
3. **开机**：长按机身背面的返回键（Back）约 3 秒，画面出现海豚动画即完成开机。
4. **确认系统版本**：进入 `设置 → 关于`，记录目前固件版本，下一步更新。

> 注意：Flipper Zero 开机默认是英文界面；部分第三方固件提供中文语系，但**不建议**新手先碰第三方固件，等官方固件流程跑熟再考虑。

## 固件更新：qFlipper 桌面版与手机 App

固件更新是 Flipper Zero 入门最重要的一步——原厂会持续修正 Bug、加入新协议支持，旧固件可能无法读取某些卡或信号。

### 方法一：qFlipper 桌面版（推荐）

1. 到 Flipper 官方网站下载对应平台的 qFlipper（Windows / macOS / Linux）。
2. 用 USB-C 连接 Flipper Zero 与电脑，开启 qFlipper。
3. 点右上角扳手图示（Advanced controls），选“Firmware update channel”。
4. 选 **Release（稳定版）**，点 Update。
5. 等待更新完成（约 5–10 分钟），装置会自动重启。

### 方法二：手机 App

1. 安装官方 Flipper Mobile App（iOS / Android）。
2. 手机开启蓝牙，与 Flipper Zero 配对（装置端：`设置 → Bluetooth`）。
3. 在 App 内点 Update，透过 BLE 传输更新，约需 10 分钟。

### 固件频道怎么选？

| 频道 | 稳定性 | 适合对象 |
|---|---|---|
| Release（稳定版） | 高 | **新手一律选这个** |
| Release Candidate（RC） | 中 | 想提前试新功能的使用者 |
| Development（开发版） | 低 | 开发者、测试者 |

> ⚠️ 更新过程不要拔线或断电；万一卡在开机画面，可进入 recovery 模式重刷（连按两次 Reset）。第三方固件（如 Xtreme）虽有扩充功能，但可能不稳定，新手请先用官方稳定版。

## 五大实用功能实测

### 1. 125 kHz RFID：读取与模拟低频卡

老式门禁卡（125 kHz）通常只有 ID 编码、没有验证机制。Flipper Zero 底部有 LF 天线，靠近卡片即可读取：

1. 主菜单 → `125 kHz RFID` → `Read`。
2. 将卡片平放靠近机身底部，读取成功会显示 UID 与资料。
3. 若要模拟，读取后选 `Emulate`，即可当作临时替代卡使用。

### 2. Sub-GHz：分析 300–928 MHz 无线信号

内置 CC1101 收发器，可捕捉遥控器、车库门、IoT 传感器发送的信号：

1. 主菜单 → `Sub-GHz` → `Read Raw`。
2. 按下遥控器按钮，画面会显示频率与信号波形。
3. 储存后可 `Replay` 重发；也可以手动设定频率扫描环境中的无线活动。

### 3. NFC：读取、写入与模拟 13.56 MHz 卡

NFC 模组支持常见的 13.56 MHz 标准，可读取悠游卡等非接触卡的 UID 与资料区块（能否完整模拟取决于卡片加密机制）：

1. 主菜单 → `NFC` → `Read`。
2. 将卡片放上机背感应区，读取卡片信息。
3. 依卡片类型可选 `Emulate` 或 `Write`。

### 4. IR：学习与重发红外遥控

内置红外发射/接收，可学习电视、冷气、投影机的遥控码并重发：

1. 主菜单 → `Infrared` → `Learn`。
2. 对准机顶红外窗按下遥控器按钮，学习成功后命名储存。
3. 之后在 `Infrared → Saved` 即可随时重发。

### 5. BadUSB / DuckyScript：USB-C 键盘模拟

连接电脑时，Flipper Zero 可模拟 USB 键盘，执行 DuckyScript 脚本（自动输入指令）：

1. 在 microSD 卡的 `badusb/` 文件夹放入 `.txt` 脚本（DuckyScript 语法）。
2. 用 USB-C 连接目标电脑，主菜单 → `BadUSB` → 选择脚本执行。

> ⚠️ **BadUSB 是高度敏感功能**：脚本会以键盘输入方式在电脑上执行指令，等同于“有人坐在电脑前打字”。只可以在你自己的电脑或明确授权测试的环境使用。

## 合法使用提醒（必读）

Flipper Zero 本身是合法工具，但使用场景有明确的法律边界：

- **复制/模拟门禁卡、遥控器**：只能针对你拥有或管理员授权的系统。未经授权读取或模拟他人门禁卡、车库遥控器，在台湾可能涉及刑法妨害秘密、电信法或个资法相关责任。
- **BadUSB**：未经授权在他人电脑执行脚本，属违法行为。
- **信号干扰**：刻意干扰他人无线设备（如车库门）同样有法律风险。

**原则很简单：只测试自己的东西，或白纸黑字拿到授权的东西。**

## 常见问题（FAQ）

**Q1：Flipper Zero 需要先装 microSD 卡吗？**
不是强制，但强烈建议。多数 App、信号库与 BadUSB 脚本都储存在 microSD，没有卡片会大幅限制功能。

**Q2：更新固件会让设备变砖吗？**
官方稳定版固件风险极低；只要更新过程不断电、不拔线，几乎不会失败。万一异常，可用 recovery 模式重刷。

**Q3：可以复制悠游卡吗？**
多数新一代票证卡有加密与金钥保护，Flipper Zero 只能读取 UID 或未加密区块，无法完整复制。且未经授权复制票证本身即违法。

**Q4：Flipper Zero 和 SDR（软件定义无线电）有什么差别？**
Flipper Zero 内置 Sub-GHz 收发器专攻常见协议（OOK/ASK/FSK 等），操作直观；SDR（如 HackRF、RTL-SDR）频率范围更广、可看原始频谱，但需要电脑与较深背景。两者是互补工具。

**Q5：哪里可以买到 Flipper Zero？**
Yupitek（榆合科技）提供 Flipper Zero 产品与相关配件，并提供技术咨询；购买后可来信 sales@yupitek.com 询问设置问题。

**Q6：可以装第三方固件吗？**
可以，但新手不建议。第三方固件（如 Xtreme）提供界面美化与额外功能，但稳定性与安全性需自行评估，且可能失去原厂更新支持。

## 总结

Flipper Zero 的入门路径很简单：**装 microSD → 更新官方稳定固件 → 从 RFID 读卡与 IR 遥控玩起 → 熟悉后再碰 Sub-GHz 与 BadUSB**。它是了解无线协议与硬件安全的绝佳起点，但请永远记得：功能越强，越要自律——只测试自己有权限的设备。

需要 Flipper Zero 或相关配件，欢迎来信 [sales@yupitek.com](mailto:sales@yupitek.com)，Yupitek 提供产品与技术咨询服 务。