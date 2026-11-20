---
title: "SDRLab TRX-duo — 듀얼 채널 16비트 ZYNQ SDR 플랫폼"
seo_title: "TRX-duo | SDRLab 대만 | Yopitek"
description: "Xilinx Zynq 7010 SoC, 125 MS/s, Red Pitaya 호환의 SDRLab TRX-duo 듀얼 채널 16비트 ADC/DAC SDR 플랫폼. Yopitek에서 대만 공급."
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/trx-duo.png"
hideFeatureImage: true
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16비트 ADC"]
faq:
  - question: "SDRLab TRX-duo의 프로세서와 인터페이스는 무엇입니까?"
    answer: "듀얼 코어 ARM Cortex-A9, 512 MB RAM, 1 Gbit Ethernet, USB Type-C (USB 2.0)를 갖춘 Xilinx Zynq 7010 SoC를 사용합니다. Wi-Fi는 외부 동글이 필요하며 포함되어 있지 않습니다."
  - question: "TRX-duo의 수신 및 송신 사양은 어떻게 됩니까?"
    answer: "수신은 125 MS/s의 LTC2208 16비트 ADC 2개를 사용하며 풀스케일은 0.5 Vpp / −2 dBm입니다. 송신은 125 MS/s의 14비트 DAC 2채널을 사용하며 50 Ω 부하에서 1 Vpp / +4 dBm입니다."
  - question: "TRX-duo는 어떤 소프트웨어와 호환됩니까?"
    answer: "Red Pitaya 소프트웨어 생태계와 호환되며, HDSDR, SDR#, PowerSDR, SDR Console V3 등의 SDR 소프트웨어와도 호환됩니다."
  - question: "TRX-duo는 어떤 확장 I/O를 제공합니까?"
    answer: "디지털 I/O 16개, 아날로그 입력 4개 (0–3.3 V, 100 kS/s, 12비트), 아날로그 출력 4개 (0–1.8 V)를 제공하며, I2C, UART, SPI와 +3.3 V 전원 출력을 지원합니다."
---

SDRLab TRX-duo는 Xilinx Zynq 7010 SoC 기반으로 Red Pitaya 소프트웨어 생태계와 호환되는 듀얼 채널 16비트 SDR 트랜시버 플랫폼으로, 고급 무선 연구와 아마추어 무선에 적합합니다. 125 MS/s의 LTC2208 16비트 ADC 2개와 14비트 DAC 송신 채널 2개를 갖추고 있습니다. 대만 내 견적은 Yopitek에 문의해 주십시오.

## 특징

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- 듀얼 채널 트랜시버 설계 (RX 2 + TX 2), Red Pitaya 소프트웨어 생태계와 완벽하게 호환
- 2× LTC2208 고정밀 16비트 ADC로 넓은 다이내믹 레인지와 높은 감도를 제공
- 듀얼 채널 송신용 14비트 DAC
- 온보드 Xilinx Zynq 7010 SoC (듀얼 코어 ARM Cortex-A9 + FPGA) — 디코딩 소프트웨어를 장치에서 직접 실행 가능
- 원격 네트워크 배포를 지원하여 원격 SDR 수신 스테이션 구축 가능
- HDSDR, SDR#, PowerSDR, SDR Console V3 등 주요 SDR 소프트웨어와 호환

## 사양

| 사양 | 값 / 설명 |
|---------------|---------------------|
| 프로세서 | 듀얼 코어 ARM Cortex-A9 (Zynq 7010 SoC) |
| FPGA | Xilinx Zynq 7010 |
| RAM | 512 MB |
| 수신 채널 | 2 (SMA 커넥터) |
| ADC 해상도 | 16비트 (LTC2208) |
| ADC 샘플링 속도 | 125 MS/s |
| ADC 풀스케일 전압 | 0.5 Vpp / −2 dBm |
| 입력 전압 범위 | DC 최대 50 V (AC 결합), 1 Vpp RF |
| 입력 보호 | RF 트랜스포머 + AC 결합 |
| 송신 채널 | 2 |
| DAC 해상도 | 14비트 |
| DAC 샘플링 속도 | 125 MS/s |
| 송신 출력 전압 | 1 Vpp / +4 dBm |
| 송신 부하 임피던스 | 50 Ω |
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | 외부 Wi-Fi 동글 필요 (미포함) |
| 확장 GPIO | 디지털 I/O 16개, 아날로그 입력 4개, 아날로그 출력 4개 |
| 아날로그 입력 전압 범위 | 0–3.3 V |
| 아날로그 출력 전압 범위 | 0–1.8 V |
| 아날로그 입력 샘플링 속도 | 100 kS/s / 12비트 |
| 통신 인터페이스 | I2C, UART, SPI |
| 확장 전원 출력 | +3.3 V |

## 활용 사례

- HF(단파) 아마추어 무선 송수신 (CW, SSB, AM, FM)
- 원격 SDR 수신 스테이션 구축 (네트워크 전체 원격 접속)
- HF 스펙트럼 분석 및 신호 연구
- 아마추어 무선 실험 (콘테스트, 천체 관측)

---

{{< alert >}}
제품 견적이 필요하십니까? [문의해 주십시오](/ko/contact/)
{{< /alert >}}

[제조사 스토어 페이지 (OpenSourceSDRLab)](https://opensourcesdrlab.com/products/trx-duo-compatible-with-red-pitaya-sdr-dual-16bit-adc-zynq7010?VariantsId=10980)

{{< faq >}}
