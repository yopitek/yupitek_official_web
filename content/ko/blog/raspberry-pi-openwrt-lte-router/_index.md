---
title: "Raspberry Pi와 OpenWrt로 4G/5G 라우터 만들기: Sierra 모듈 지원 매트릭스 및 설정 가이드"
description: "Raspberry Pi와 Sierra Wireless 4G/5G 모듈(EM7455, EM7565, EM7511, EM919x, MC7455)로 나만의 OpenWrt 라우터를 구축합니다. 전체 지원 매트릭스, QMI/MBIM 설정, wwan0 인터넷 연결 방법과 함께 전원 및 안테나 가이드라인을 다룹니다."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yopitek"
lastmod: 2026-11-20
related_product: "/ko/products/sierra/"
faq:
  - question: "Raspberry Pi의 OpenWrt 라우터에는 어떤 Sierra 모듈을 선택해야 합니까?"
    answer: "입문자는 튜토리얼이 풍부하고 문제를 찾아보기 쉬운 EM7455로 시작하시기 바랍니다. 높은 업로드 처리량이 필요하면 EM7565 또는 EM7511, 5G에는 EM919x, 구형 mPCIe 슬롯에는 MC7455를 선택하십시오."
  - question: "QMI와 MBIM의 차이점은 무엇입니까?"
    answer: "QMI는 Qualcomm의 프로토콜이며, MBIM은 이후에 표준화된 프로토콜입니다. 둘 다 OpenWrt에서 동작하지만, 온라인 가이드는 대부분 QMI를 사용합니다."
  - question: "Raspberry Pi가 모듈을 인식하지 못하면 어떻게 해야 합니까?"
    answer: "가장 흔한 원인은 Raspberry Pi의 USB 전원 공급 부족입니다(최대 돌입 전류가 2.5A에 달할 수 있음). 어댑터 보드의 전원 공급과 케이블링을 확인하고, 모듈이 부팅을 마칠 때까지 약 10초간 기다리십시오."
---

Raspberry Pi로 Sierra Wireless 4G/5G 모듈을 완전하게 동작하는 OpenWrt 라우터로 만들 수 있을까요? 가능합니다. EM7455, EM7565, EM7511, EM919x와 같은 M.2 모듈은 Linux에서 기본적으로 지원됩니다. `kmod-usb-net-qmi-wwan` 또는 `kmod-usb-net-cdc-mbim`을 설치하고 `wwan0`를 설정하면 바로 인터넷에 연결됩니다. 본 문서에서는 전체 모듈 지원 매트릭스, 단계별 설정 방법, 그리고 피해야 할 전원 및 안테나 관련 함정을 다룹니다.

{{< tldr >}}
Raspberry Pi와 Sierra 4G/5G 모듈의 조합은 안정적인 OpenWrt 라우터가 됩니다. 대부분의 M.2 모듈(EM7455, EM7565, EM7511)은 USB를 사용하고, EM919x는 PCIe Gen3 레인을 추가로 제공하며, MC7455는 EM7455의 mPCIe 버전입니다. OpenWrt에서는 `wwan0`를 사용하는 QMI 프로토콜이 권장 방식입니다. `kmod-usb-net-qmi-wwan`, `uqmi`, `luci-proto-qmi`를 설치하고 `/etc/config/network`에 APN을 설정한 후 네트워크를 재시작하십시오. 속도 측면에서 EM7455 / MC7455는 LTE Cat 6(300/50 Mbps), EM7565 / EM7511은 Cat 12(600/150 Mbps)이며, EM919x 제품군은 5G Sub-6를 제공합니다(EM9190은 mmWave를 추가 지원).
{{< /tldr >}}

## OpenWrt에서의 Sierra 모듈 전체 지원 매트릭스

시작하기 전에 사용하시는 모듈을 이 표에서 확인하십시오.

| 모델 | 속도 등급 | 베이스밴드 칩 | 폼 팩터 | Linux 데이터 경로 | GNSS 측위 |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (Linux에서 둘 다 지원) | QZSS 추가 |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | QZSS 추가 |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (9190은 mmWave 추가) | SDX55 | M.2 (길이 52mm) | Windows/Linux | L1 + L5 (선택 사항) |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50.95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### 모듈 선택 방법

- **입문하는 메이커**: **EM7455**를 선택하십시오. 가이드가 풍부하고 문제를 찾아보기 쉽습니다.
- **높은 업로드 수요(라이브 스트리밍, 감시)**: 최대 150 Mbps 업로드를 지원하는 **EM7565** 또는 **EM7511**을 선택하십시오.
- **5G 필수**: 5G 속도를 위해 **EM9190**을 선택하십시오.
- **구형 mPCIe 슬롯만 있는 경우**: **MC7455**를 선택하십시오.

## 하드웨어를 연결하는 세 가지 방법

### A. Raspberry Pi 5 + M.2 HAT (PCIe)

Pi 5는 PCIe를 제공하므로 M.2 HAT+ 캐리어 보드를 사용하면 M.2 WWAN 모듈을 직접 꽂을 수 있습니다(B-Key인지 확인하십시오).

### B. Raspberry Pi 4B 이하 + USB WWAN 어댑터 인클로저

EM 시리즈 모듈은 USB 2.0/3.0도 지원하므로, Pi의 USB 포트에 M.2-USB 인클로저(대개 SIM 슬롯 내장)를 연결하는 것이 가장 간단하고 접근하기 쉬운 방법입니다.

### C. MC7455 (mPCIe) 어댑터

MC7455는 구형 mPCIe 인터페이스를 사용하므로 mPCIe-USB 또는 mPCIe-M.2 어댑터 보드가 필요합니다.

> ⚠️ **전원이 가장 큰 함정입니다**: 모듈은 3.135~4.4 V(일반적으로 3.3V)를 사용합니다. "모듈이 인식되지 않음" 오류는 대개 Raspberry Pi의 USB 전원이 충분한 전력을 공급하지 못한다는 의미입니다. 돌입 전류가 2.5A까지 급증할 수 있으므로 전원 공급 장치에 충분한 여유를 두십시오.

## QMI와 MBIM 이해하기

두 프로토콜 모두 4G/5G 모듈이 네트워크에 연결되는 방식을 제어합니다.

- **QMI**: Qualcomm 고유의 프로토콜로, 대부분의 Linux/OpenWrt 가이드에서 사용합니다(인터페이스는 `wwan0`로 나타납니다).
- **MBIM**: 이후에 표준화된 프로토콜로, Windows와 Linux 모두에서 사용할 수 있습니다(인터페이스는 역시 `wwan0`로 나타납니다).

**어느 쪽을 선택해야 합니까?** 대부분의 사용자는 QMI를 바로 사용하면 됩니다. 펌웨어에서 특별히 요구하는 경우에만 MBIM으로 전환하십시오.

## 실습 1부: OpenWrt에서 QMI 설정하기

네 단계이며 컴파일은 필요하지 않습니다.

### 1. 패키지 설치

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Raspberry Pi가 모듈을 인식하는지 확인

```bash
lsusb                                  # look for a Sierra device
ls /dev/cdc-wdm*                       # QMI control channel
dmesg | grep qmi_wwan                  # check that the driver loaded
ip link show wwan0                     # check that the interface appeared
```

### 3. 네트워크 파일 설정 (`/etc/config/network`)

QMI 섹션을 추가하고 APN을 사용 중인 통신사의 APN으로 교체하십시오.

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. 네트워크 재시작

```bash
/etc/init.d/network restart
ifup wwan
```

이것으로 끝입니다. `wwan0`가 IP 주소를 받으면 인터넷에 연결된 것입니다.

## 안테나와 SIM: 건너뛰지 마십시오

모듈에는 **내장 안테나가 없으며**, 안테나 품질이 처리량을 직접적으로 좌우합니다.

- **주 안테나**: 필수입니다.
- **보조 안테나(Aux)**: MIMO 속도를 위해 필요하며, 생략하면 처리량이 감소합니다.
- **GNSS 안테나**: 측위 용도에만 필요합니다. 주 안테나와 혼동하지 마십시오.

## 흔한 함정 (입문자 필독)

1. **`lsusb`에 아무것도 표시되지 않음**: 99%는 전원 부족, 어댑터 보드의 접촉 불량 또는 불량 케이블이 원인입니다.
2. **너무 성급함**: 모듈은 부팅할 시간이 필요합니다. 꽂은 후 10초간 기다린 다음 명령을 실행하십시오.
3. **5G 모듈(EM919x)은 발열이 큼**: 100°C 안팎의 온도가 흔하므로(최대 115°C) 냉각을 계획하십시오.
4. **ModemManager 충돌**: 기본 Linux 시스템에서 수동으로 작업할 때는 `ModemManager`가 모듈을 가로채지 않도록 먼저 중지하십시오(`systemctl stop ModemManager`).

## 요약

OpenWrt가 설치된 Raspberry Pi로 Sierra 모듈을 구동하는 일은 체크리스트에 따라 진행하는 과정입니다. 하드웨어(폼 팩터, 전압, 안테나)를 확인하고, QMI/MBIM 드라이버를 설치한 다음, APN을 설정하십시오. 이 가이드가 프로젝트의 시행착오를 줄이고 Raspberry Pi를 4G/5G 최대 속도로 동작시키는 데 도움이 되기를 바랍니다.

## 구매 안내 (Call To Action)

EM7455, EM7565, EM7511 모듈 또는 호환되는 M.2 어댑터 보드와 안테나가 필요하시면, Yopitek이 완전한 하드웨어 솔루션과 기술 상담을 제공합니다.

이메일 문의: **sales@yupitek.com**

제품 보기: [Yopitek Sierra Wireless 시리즈](https://yupitek.com/ko/products/sierra/)
