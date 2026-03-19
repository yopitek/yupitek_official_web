---
title: "SDRLab TRX-duo — 双通道 16-bit ZYNQ SDR 平台"
description: "SDRLab TRX-duo，双通道 16-bit ADC/DAC SDR 平台，Xilinx Zynq 7010 SoC，兼容 Red Pitaya，10kHz–60MHz 直接采样，适合进阶 HF 无线通信研究。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---

## 产品特色

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- 双通道收发设计（2 RX + 2 TX），兼容 Red Pitaya 软件生态系
- 采用 2× LTC2208 高精度 16-bit ADC，具备高动态范围与高灵敏度
- 14-bit DAC 实现双通道发射
- 板载 Xilinx Zynq 7010 SoC（双核 ARM Cortex-A9 + FPGA），可直接在设备上运行解码软件
- 支持网络远程部署，可架设远程 SDR 接收站
- 兼容 HDSDR、SDR#、PowerSDR、SDR Console V3 等主流软件
- 比官方 Red Pitaya SDRlab 122-16（约 $622 USD）便宜约一半

## 产品规格

| 规格项目 | 数值／说明 |
|---------|-----------|
| 处理器 | 双核 ARM Cortex-A9（Zynq 7010 SoC）|
| FPGA | Xilinx Zynq 7010 |
| 内存（RAM）| 512 MB |
| 接收频率范围 | 10 kHz – 60 MHz（直接采样）|
| 接收通道数 | 2（SMA 连接器）|
| ADC 分辨率 | 16-bit（LTC2208）|
| ADC 采样率 | 125 MS/s |
| ADC 全量程电压 | 0.5 Vpp / −2 dBm |
| 输入电压范围 | DC 最大 50 V（AC 耦合），1 Vpp RF |
| 输入保护 | RF 变压器 + AC 耦合 |
| 发射通道数 | 2 |
| DAC 分辨率 | 14-bit |
| DAC 采样率 | 125 MS/s |
| 发射输出电压 | 1 Vpp / +4 dBm |
| 发射负载阻抗 | 50 Ω |
| 发射功率 | 约 2.5 mW（需外接功率放大器）|
| 以太网 | 1 Gbit |
| USB | Type-C（USB 2.0）|
| Wi-Fi | 需外接 Wi-Fi 加密狗（不含）|
| 扩展 GPIO | 数字 I/O × 16、模拟输入 × 4、模拟输出 × 4 |
| 模拟输入电压范围 | 0–3.3 V |
| 模拟输出电压范围 | 0–1.8 V |
| 模拟输入采样率 | 100 kS/s / 12-bit |
| 通信接口 | I2C、UART、SPI |
| 扩展电源输出 | +3.3 V |
| 操作系统 | 板载 Linux（Red Pitaya 固件）|

## 应用环境

- HF（短波）业余无线电收发（CW、SSB、AM、FM）
- 多频段 WSPR 弱信号监测（最多 8 频段同时）
- 远程 SDR 接收站架设（全网络远程访问）
- HF 频谱分析与信号研究
- HPSDR 兼容应用软件开发
- 业余无线电通信实验（无线电竞赛、天文观测）

---

{{< gallery >}}
  <img src="/images/products/sdrlab/trx-duo.png" alt="SDRLab TRX-duo" />
{{< /gallery >}}

---

{{< alert >}}
需要询问报价？[联系我们](/zh-cn/contact/)
{{< /alert >}}
