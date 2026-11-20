---
title: "OpenWrt 또는 Raspberry Pi에서 Sierra EM7565가 인식되지 않나요? QMI/MBIM 문제 해결 완벽 가이드"
description: "OpenWrt나 Raspberry Pi에서 EM7565가 인식되지 않거나 QMI 포트가 사라졌습니까? 이 가이드는 lsusb와 dmesg부터 USB 컴포지션, 드라이버 로딩, EM7565 설정 단계까지 안내하여 하드웨어 및 소프트웨어 연결 문제를 해결하도록 돕습니다."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yopitek"
lastmod: 2026-11-20
related_product: "/ko/products/sierra/em7565/"
faq:
  - question: "OpenWrt에서 EM7565가 인식되지 않는 가장 흔한 원인은 무엇입니까?"
    answer: "가장 흔한 원인은 전원 부족(VCC가 3.135 ~ 4.4V 범위를 벗어남)으로 lsusb에 아무것도 표시되지 않는 경우, 또는 USB 컴포지션 설정이 잘못되어 QMI 인터페이스가 비활성화된 경우입니다."
  - question: "EM7565가 계속 재설정되며 부팅되지 않습니다. 고장입니까?"
    answer: "반드시 그렇지는 않습니다. SED 보호 메커니즘이 있어서, 비정상 재시작이 연속 6회 발생하면 보호 상태로 진입하며, 펌웨어를 다시 로드하면 복구됩니다."
---

OpenWrt나 Raspberry Pi에서 EM7565가 나타나지 않습니까? 모듈을 교체하기 전에 공식 사양서의 디버깅 절차를 따라 점검해 보십시오. 이 가이드는 USB 하드웨어 링크 확인, USB 컴포지션 점검, 올바른 Linux 드라이버 로딩, 시스템 서비스 간섭 배제, 까다로운 펌웨어 SED 상태 처리까지 다룹니다. 다섯 단계를 따라가면 근본 원인을 빠르게 찾을 수 있습니다.

{{< tldr >}}
EM7565가 인식되지 않을 때는 다음 다섯 가지를 확인하십시오. 1. `lsusb`로 USB 계층을 확인합니다(전원 공급과 어댑터 보드 점검). 2. QMI/MBIM 인터페이스와 `/dev/cdc-wdm0`의 존재 여부를 확인하고, `qmi_wwan` / `cdc_mbim` 드라이버와 USB 컴포지션을 점검합니다. 3. `ModemManager`를 중지하여 시스템 서비스 간섭을 배제합니다. 4. 전원 시퀀싱을 점검합니다(전원 투입 후 100ms 이내에는 어떤 신호도 구동하지 말고, 리플은 100mVp-p 미만으로 유지). 5. 펌웨어 상태를 점검합니다. 부팅 실패가 연속 6회 발생하면 SED 보호가 작동하며 펌웨어를 다시 로드해야 합니다. 원칙은 하드웨어 먼저, 그다음 소프트웨어, 펌웨어는 마지막입니다.
{{< /tldr >}}

**EM7565는 Qualcomm MDM9250 기반의 M.2 WWAN Type 3042-S3-B 4G LTE-Advanced 모듈입니다. QMI와 MBIM USB 인터페이스를 모두 지원합니다.** OpenWrt나 Raspberry Pi가 이 모듈을 인식하지 못할 때, 결함은 보통 세 곳 중 하나에 있습니다. USB에 전원이 공급되지 않았거나, USB 컴포지션이 잘못된 구성에 머물러 있거나, Linux 드라이버가 제대로 로드되지 않은 경우입니다. 드물게 반복된 재시작 후 모듈이 보호 모드로 진입하기도 합니다. Sierra Wireless 공식 매뉴얼을 바탕으로 신뢰할 수 있는 단계별 디버깅 순서를 정리했습니다.

> 제품 링크: [Yopitek Sierra Wireless 시리즈](https://yupitek.com/ko/products/sierra/)

## 빠른 결론: EM7565가 인식되지 않을 때의 다섯 단계

디버깅에서 가장 흔한 실수는 곧바로 펌웨어를 다시 플래시하는 것입니다. **먼저 하드웨어를 확인하고, 그다음 소프트웨어를 확인하며, 펌웨어는 마지막에 건드리십시오.**

1. **USB 계층 점검**: `lsusb`를 실행하여 모듈이 나타나는지 확인합니다. 나타나지 않으면 전원 공급(VCC는 3.135 ~ 4.4V여야 함), 어댑터 보드, USB 케이블을 점검합니다.
2. **QMI/MBIM 인터페이스 점검**: `lsusb`에는 모듈이 보이는데 `/dev/cdc-wdm0`가 없습니까? `qmi_wwan` / `cdc_mbim` 드라이버가 로드되었는지, 그리고 USB 컴포지션이 진단 모드만 노출하고 있지 않은지 확인합니다.
3. **시스템 서비스 점검**: 시스템의 `ModemManager`가 모듈을 점유하고 있을 수 있습니다.
4. **전원 시퀀싱 점검**: 전원 투입 후 최소 100ms 동안은 어떤 신호도 구동하지 말고, 전원 리플을 100mVp-p 미만으로 유지하십시오. 전압이 불안정하면 USB 링크가 반복적으로 끊겼다 다시 연결됩니다.
5. **펌웨어 상태 점검**: 부팅 실패 후 모듈이 연속 6회 재설정되면 SED(Smart Error Detection) 보호 상태로 진입하며, 펌웨어를 다시 로드해야 합니다.

## EM7565 이해하기: 어떤 모듈입니까?

디버깅에 앞서 EM7565를 간단히 정리합니다. 외부 안테나 3개(Main, GNSS, Aux)가 필요한 M.2 모듈이며, 안테나는 포함되어 있지 않습니다.

| 항목 | 공식 사양 (Doc# 41110788, Rev 8) |
|---|---|
| **칩셋** | Qualcomm MDM9250 |
| **폼 팩터** | M.2 (3042-S3-B) / 42 × 30 mm, 두께 최대 1.50mm, 6.5g |
| **다운로드 최대** | Cat 12 (3CA, 256QAM) 최대 600 Mbps |
| **업로드 최대** | Cat 13 (2CA, 64QAM) 최대 150 Mbps |
| **LTE 대역** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66 (참고: B42/B43/B48은 규제 승인 대기 중이어서 비활성화됨) |
| **호스트 인터페이스** | USB 2.0 및 USB 3.0; QMI / MBIM / AT 명령 |
| **공급 전압** | VCC 3.135V(최소) / 3.3V(표준) / 4.4V(최대), 리플 ≤ 100mVp-p |
| **동작 온도** | 내부 온도를 90°C 미만(가능하면 80°C 미만)으로 유지 |

## 1단계: USB 계층부터 시작

호스트가 하드웨어를 실제로 인식하고 있습니까?

```bash
lsusb
```

1199로 시작하는 Sierra Wireless 장치가 나타나면 하드웨어 링크가 구성된 것입니다. 아무것도 나타나지 않는다면 다음을 확인하십시오.

- 전원 공급을 점검합니다. EM7565의 부팅 시 돌입 전류는 2.2A ~ 2.5A에 달할 수 있습니다(최대 동작 전류 1.5A). 많은 Raspberry Pi USB 어댑터 케이스는 이를 공급하지 못합니다.
- 시간을 주십시오. USB 열거가 완료되도록 꽂은 후 10초 정도 기다립니다.

그런 다음 커널 로그를 확인합니다.

```bash
dmesg | tail -50
```

`qmi_wwan`이 `/dev/cdc-wdm0`를 생성하는 것이 보이면 모듈은 연결할 준비가 된 것입니다.

## 2단계: USB 컴포지션 점검

`lsusb`에는 모듈이 보이는데 `/dev/cdc-wdm0`가 나타나지 않는다면, 모듈의 QMI/MBIM 채널이 비활성화되어 있을 수 있습니다. 모듈 내부의 USB 컴포지션이라는 설정이 어떤 채널을 노출할지 결정합니다.

`AT!USBCOMP?` 명령으로 조회하십시오. 부주의하게 전환하면 모든 채널이 사라질 수 있으므로, 변경하기 전에 원래 파라미터를 기록해 두고 공식 AT 명령 매뉴얼(Doc#41111748)을 참고하십시오.

## 3단계: ModemManager 간섭 배제

데스크톱 Linux나 Raspberry Pi에서는 내장 서비스인 `ModemManager`가 4G 모듈을 가로채는 경우가 많습니다. 일단 제어권을 잡으면 직접 입력한 `qmicli` 명령이 멈춥니다.

수동으로 디버깅하는 동안에는 먼저 이를 중지하십시오.

```bash
sudo systemctl stop ModemManager
```

모듈이 정상임을 확인한 후, 수동으로 다이얼링할지 ModemManager에 제어권을 돌려줄지 결정하십시오.

## 4단계: 펌웨어가 잠겨 있습니까? (SED 보호)

전원 투입 후 모듈이 끝없이 재부팅한다면 **SED(Smart Error Detection)** 상태에 진입했을 수 있습니다.

공식 사양서에는 명확히 기재되어 있습니다. 부팅 직후 재설정이 6회 발생하면 모듈은 스스로 부트로더에 머물며 펌웨어 재로드를 기다립니다. 이는 보통 전압 강하가 심한 불안정한 전원 공급 때문에 발생합니다.

모듈이 죽었다고 단정하지 마십시오. 더 나은 전원 공급 장치로 바꾸고 공식 도구로 펌웨어를 다시 플래시하면 복구할 수 있습니다.

## QMI로 다이얼링하기 (OpenWrt 예시)

위의 문제를 해결하고 `/dev/cdc-wdm0`가 나타났다면, OpenWrt에서 다이얼링은 간단합니다.

1. 필요한 패키지를 설치합니다.

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. `/etc/config/network`에 APN을 설정합니다(이동통신사의 값을 사용).

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. 네트워크를 재시작합니다.

```bash
/etc/init.d/network restart
```

`wwan0` 인터페이스가 나타나면 온라인 상태가 됩니다.

## 요약

OpenWrt나 Raspberry Pi에서 EM7565가 보이지 않는 문제는 컴퓨터를 수리하는 것과 같습니다. 순서만 올바르면 빠르게 해결됩니다.

1. **하드웨어**: `lsusb`가 정상이며 전압이 안정적입니까?
2. **인터페이스**: USB 컴포지션이 올바릅니까?
3. **소프트웨어**: 드라이버가 설치되어 있으며, ModemManager가 장치를 두고 경합하고 있지는 않습니까?
4. **펌웨어**: 너무 많은 재시작으로 모듈이 잠기지는 않았습니까?

펌웨어를 무작정 다시 플래시하지만 않는다면, 대부분의 문제는 10분 안에 진단할 수 있습니다.

## 구매 안내 (Call To Action)

사용 중인 어댑터 보드나 안테나가 EM7565와 호환되는지 확신이 서지 않으십니까? Yopitek은 Sierra Wireless 전체 제품군과 완전한 하드웨어 통합 솔루션을 제공합니다.

이메일 문의: **sales@yupitek.com**

제품 보기: [EM7565 제품 페이지](https://yupitek.com/ko/products/sierra/em7565/)
