---
title: "Flipper Zero 5G Expansion Board 图解安装与使用手册 (v2.0)"
description: "本指南为 Flipper Zero 5G 扩展模块安装与操作指引 v2.0，配有完整高清 isometric 工程设计图，带领新手无痛安装天线、插槽及 GPIO 设定。"
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Flipper Zero 5G Expansion Board 图解安装与使用手册 (v2.0)

> **目标读者**：完全没有接触过本模块的新手客户。  
> **编写原则**：针对所有“容易出错”或“术语难懂”的步骤提供高清设计图解，告别文字猜测，实现一步一图的无痛安装。

---

## 00. 开箱与配件清单

欢迎使用 Flipper Zero 5G 扩展模块！在开始前，请先确认您的包装内包含以下配件。

![开箱全家福与配件图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*图 1：开箱配件全家福*

### ⚠️ 配件清单说明
*   **标配包含**：
    1.  5G 扩展板主模块 (5G Expansion Board) x 1
    2.  433MHz 棒状天线 (短黑天线) x 1
    3.  GPS 陶瓷主动式天线 (正方形天线) x 1
    4.  WiFi 双频贴片天线 (黑色扁平天线) x 1
*   **不包含 (需自行准备)**：
    *   **Flipper Zero 主机** (本模块不附带主机)
    *   **MicroSD 记忆卡** (模块运作必需，需自行购买)

---

## 01. 认识你的 5G 模块

在插上天线或连接主机前，请先花一分钟熟悉模块上的各个关键界面与硬件布局。

### 正面界面说明

![模块正面标注图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*图 2：正面硬件配置标注*

*   **屏幕 (LCD Screen)**：显示目前的连接状态、IP 地址与运作模式。
*   **拨动开关 (Toggle Switch)**：控制模块屏幕的电源，往上拨为开启。
*   **MicroSD 卡槽 (SD Card Slot)**：用于存储系统固件设定与 Log 资料。
*   **GPIO 插槽**：与 Flipper Zero 主机顶部对接的母座。
*   **指示灯 (LED Indicators)**：显示电源与充电状态。

### 侧面天线端口说明

![侧面天线端口标注图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*图 3：天线端口位置与功能印刷*

*   **433M A**：连接 433MHz 棒状天线。
*   **GPS**：连接 GPS 陶瓷天线。
*   **2.4G** 与 **2.4G/5G**：连接 WiFi 双频贴片天线。

> ⚠️ **出货批次版本重要提醒**：  
> 天线端口位置会依据生产批次而有微幅调整（如 GPS 与 WiFi 连接口位置可能左右对调）。**请务必以您手上模块外壳上的实际印刷标签为准**，切勿单凭记忆盲插，以免信号不佳或损坏硬件。

---

## 02. 安装步骤指引 (Step-by-Step)

### Step 1 | 准备与安装 MicroSD 记忆卡

5G 模块需要一张记忆卡来存储设定。

1.  **规格要求**：容量为 **32GB 以下**，格式必须为 **FAT32**。
2.  **卡片方向**：请金属接脚朝下，插入 MicroSD 卡槽内，轻压至卡住。

![MicroSD 卡插槽特写](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*图 4：MicroSD 卡正确插入方向特写*

---

### Step 2 | 安装三根天线

请将标配的三根天线锁入对应的 SMA 天线接头。注意不要用力过猛，转至紧贴即可。

![天线安装接线图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*图 5：三种天线锁附与对接路径示意*

| 天线类型 | 对应天线端口 | 安装说明 |
| :--- | :--- | :--- |
| **GPS 陶瓷天线** | **GPS 端口** | 接头为正方形陶瓷座，带有长线 |
| **WiFi 双频贴片天线** | **2.4G/5G 端口** | 黑色扁平贴片天线 |
| **433MHz 棒状天线** | **433M A 端口** | 黑色短棒状硬天线 |

#### ⚠️ GPS 天线摆放方向警告
GPS 天线具有方向性。安装时，**陶瓷面 (通常有黏贴双面胶的反面，或无文字面) 必须朝上 (面向天空)**，否则将无法成功定位！

![GPS 天线朝向对比图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*图 6：GPS 天线正确 (朝天) 与错误 (朝地) 摆放对比*

---

### Step 3 | 与 Flipper Zero 主机对接

将 5G 模块插入 Flipper Zero 顶部的 GPIO 引脚。

1.  请先**将 Flipper Zero 关机**，以防热插拔造成硬件损坏。
2.  对齐 Flipper Zero 顶部的 GPIO 引脚与模块底部的插槽。

![GPIO 对接 alignment 图](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*图 7：GPIO 对接位置与对齐线*

3.  双手均匀施力，将模块**轻压到底**。
4.  **检查平整度**：完成后，请从侧面观察，模块与 Flipper Zero 之间应**完全贴合、没有任何缝隙**。

![GPIO 插入贴合度确认](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*图 8：完全插入且无缝隙的正确对接状态*

---

### Step 4 | Flipper Zero 软件设定

对接完成后，将 Flipper Zero 开机，接着进行软件引脚 (GPIO Pin) 设定。

以 **Momentum 固件** 为例，请至以下路径进行设定：

1.  **开启屏幕电源**：将模块左前方的拨动开关拨至 **UP** 位置。
    ![屏幕拨动开关 UP 特写](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *图 9：屏幕拨动开关切换至 UP 位置以开启显示*

2.  **GPS Pin 设定**：
    *   路径：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   设定值：改为 **13** 或 **14** (依手册或硬件出货说明)。
3.  **ESP32 Pin 设定 (WiFi/蓝牙功能)**：
    *   路径：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   设定值：改为 **15, 16**。
4.  **433MHz 射频模块设定**：
    *   进入 `Sub-GHz` ➔ `Advanced Settings` ➔ 将 Module 改为 **External** (启用外接天线)。

---

### Step 5 | 充电与电量检查

本模块内建可充电式电池。

![USB-C 介面对比与警告](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*图 10：上方充电专用孔 (CHARGE ONLY) 与侧面烧录专用孔 (FLASH ONLY) 对照*

*   **顶部 USB-C 端口**：**仅供充电使用** (标示有 CHARGE ONLY)。请务必插在此孔进行充电！
*   **侧面 USB-C 端口**：**仅供固件烧录使用** (标示有 FLASH ONLY)。切勿用于日常充电，否则无法补充电力。

#### 电量 LED 指示灯状态：
模块正面有 4 颗电量指示灯，代表不同的剩余电量百分比：

![电量指示灯图解](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*图 11：4 颗 LED 灯对应的剩余电量*

*   1 颗灯亮：电量约 25% (请尽速充电)
*   2 颗灯亮：电量约 50%
*   3 颗灯亮：电量约 75%
*   4 颗灯亮：电量 100% (已充满)

---

## 03. 常见错误自我检查表 (新手疑难排解)

如果您的模块无法正常运作，请逐一检查以下项目：

*   [ ] **GPIO 引脚是否完全插到底？** (模块与 Flipper Zero 顶部应无缝隙贴合，参考图 8)
*   [ ] **GPS 天线方向是否正确？** (陶瓷面必须面朝天空，参考图 6)
*   [ ] **天线是否锁错孔？** (不同批次的位置可能不同，请核对外壳文字印刷，参考图 3)
*   [ ] **MicroSD 卡规格是否符合？** (容量需 32GB 以下，且格式为 FAT32，参考图 4)
*   [ ] **屏幕开关是否已拨至 UP？** (参考图 9)

---

## 04. 固件升级与烧录 (进阶功能)

当官方发布新版固件时，您需要透过侧面 USB-C 端口进行固件烧录。

1.  准备一条连接至电脑的 USB-C 线。
2.  **关键步骤**：在将线插入模块**侧面 USB-C 端口 (FLASH ONLY)** 的同时，**按住模块背面/右侧的烧录按键**，使芯片进入 Boot 烧录模式。

![固件烧录按键与插入顺序](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*图 12：按住烧录键并同时插入 USB 传输线的步骤示意*
